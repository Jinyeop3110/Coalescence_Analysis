"""
pH_feedback_model.py
====================

Reusable simulator for a pH-feedback microbial model following the
Ratzke / Gore lab framework. Intended as a genuine non-gLV alternative for
the coalescence analysis (internal memo Q5).

Canonical ODE form, adapted from the public Ratzke pH-model simulation
repository for the coalescence setting:

    g_i(p)   = exp(-(p - p_pref_i)**2 / (2 * p_c**2))
    dn_i/dt  = n_i * (1 - n_i) * (g_i(p) * (kgrowth + kdeath) - kdeath)
    dp/dt    = K * sum_i(c_i * n_i) + lambda_dilution * (p_fresh - p)

- n_i        : biomass / density of species i (logistic saturation is applied
               per species, matching the original public model code).
- p          : proton concentration (inverse of pH - low p is alkaline,
               high p is acidic).
- p_pref_i   : proton concentration at which species i grows optimally.
- p_c        : Gaussian pH-tolerance width.
- c_i        : per-cell rate of proton production (c>0, acidifier) or
               consumption (c<0, alkalinizer).
- kgrowth    : maximum growth-rate scale.
- kdeath     : death-rate scale.
- b          : half-width of the accessible proton-concentration window.
- K          : pH modification scale used in the original model.
- p_fresh    : fresh-medium environmental coordinate, used here for
               continuous relaxation instead of daily serial dilution.
- lambda_dilution : continuous relaxation strength toward p_fresh.

The public Ratzke code uses p_pref ~ U(4.5, 9.5), p_c=2.5, kgrowth=10,
kdeath=10, and K=1e10. These are the defaults exposed below.  We do not
apply the original daily dilution/reset loop here; instead, the p equation
has a continuous relaxation term so the coalescence simulations can be run
as single assembly and merger integrations.

The *interaction-strength* knob analogous to mu in the pairwise gLV is the
magnitude of pH modification relative to pH tolerance, i.e. |c| / sigma,
equivalently the "pH shift per unit biomass" divided by the "pH range a
species can still grow in". When |c|/sigma is small, each species barely
perturbs the pH felt by its neighbours and species interact weakly.  When
|c|/sigma is large, one species can push p outside another species' growth
range and drive it extinct -- strong pH-mediated interaction.  This
mapping is made explicit in Ratzke, Barrere & Gore 2020
(Nat. Ecol. Evol. 4:376-383, DOI 10.1038/s41559-020-1099-4): they show
experimentally that *nutrient concentration sets |c|*, so that the knob
from our paper (nutrients) maps onto |c|/sigma in this model.  That is
precisely the analogue we need for Q5.

Sources used (cited for equation fidelity, not hallucinated):

  [1] Ratzke C, Gore J. (2018) "Modifying and reacting to the environmental
      pH can drive bacterial interactions." PLoS Biology 16(3):e2004248.
      Eqs. 1-2 in main text; S1 Text provides identical form with
      sigma=4, delta=0.5, |c|=0.1, b=5.
  [2] Ratzke C, Barrere J, Gore J. (2020) "Strength of species interactions
      determines biodiversity and stability in microbial communities."
      Nat. Ecol. Evol. 4:376-383. Establishes nutrient -> |c| -> interaction
      strength mapping used here as the pH_tension knob.
  [3] Ratzke C, Denk J, Gore J. (2018) "Ecological suicide in microbes."
      Nat. Ecol. Evol. 2:867-872. Single-species version of the same ODE.

Interface contract (for downstream pipeline parity with R3_3_nonCompetitive_gLV):

- simulate_single_community(...) returns a non-negative abundance vector of
  length N_POOL_default, with zeros in species that went extinct. This is
  the same shape and dtype as the gLV simulator's output, so the exact
  common_setup.metric_VectorDecomposition_onlyPositive pipeline works on it.
- run_coalescence(...) mixes two such vectors 50/50 and integrates to
  steady state in the *same chemistry* (pH included); returns a vector of
  the same shape.

"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from scipy.integrate import solve_ivp

# ---- Canonical Ratzke 2018 parameters (defaults) -----------------------
DEFAULT_PC    = 2.5       # pH-tolerance width in original code
DEFAULT_SIGMA = DEFAULT_PC # backwards-compatible alias
DEFAULT_KGROWTH = 10.0    # original code kgrowth
DEFAULT_KDEATH  = 10.0    # original code kdeath
DEFAULT_DELTA = DEFAULT_KDEATH # backwards-compatible alias
DEFAULT_C_MAG = 1e-10     # interaction_strength scale in original code
DEFAULT_B     = 5.0       # p \in [0, 2b] = [0, 10]
DEFAULT_K     = 1e10      # pH modification multiplier in original code
DEFAULT_P0    = 7.0       # original starting / fresh-medium p coordinate
DEFAULT_P_FRESH = 7.0
DEFAULT_LAMBDA_DILUTION = 1.0

# Numerical safety
EXTINCTION    = 1e-3      # below this after integration -> zero
BLOWUP_CAP    = 10.0      # sanity check on abundances
T_END         = 200.0     # integration horizon in arbitrary time units
RTOL          = 1e-6
ATOL          = 1e-9


# ---- Species parameter container ---------------------------------------
@dataclass
class SpeciesPool:
    """A frozen draw of species parameters. All arrays have length N."""
    p_pref: np.ndarray          # preferred proton concentration per species
    sigma:  np.ndarray          # Gaussian width per species (usually p_c=2.5)
    c:      np.ndarray          # signed per-cell pH-modification rate
    K:      float = DEFAULT_K
    delta:  float = DEFAULT_DELTA
    b:      float = DEFAULT_B
    kgrowth: float = DEFAULT_KGROWTH
    kdeath: float = DEFAULT_KDEATH
    p_fresh: float = DEFAULT_P_FRESH
    lambda_dilution: float = DEFAULT_LAMBDA_DILUTION

    def N(self) -> int:
        return int(self.p_pref.shape[0])

    def subset(self, mask: np.ndarray) -> "SpeciesPool":
        """Return a pool restricted to species in mask (bool, length N)."""
        idx = np.where(mask)[0]
        return SpeciesPool(
            p_pref=self.p_pref[idx].copy(),
            sigma=self.sigma[idx].copy(),
            c=self.c[idx].copy(),
            K=self.K, delta=self.delta, b=self.b,
            kgrowth=self.kgrowth, kdeath=self.kdeath,
            p_fresh=self.p_fresh,
            lambda_dilution=self.lambda_dilution,
        )


# ---- Species sampling ---------------------------------------------------
def sample_species_pool(
    N: int,
    rng: np.random.Generator,
    c_mag: float = DEFAULT_C_MAG,
    p_pref_range: tuple = (4.5, 9.5),  # original code: random_sample()*5+4.5
    sigma_range:  tuple = (DEFAULT_PC, DEFAULT_PC),
    link_c_to_p_pref: bool = False,
    p_pref_mode: str = "uniform",      # "uniform" | "bimodal"
    b: float = DEFAULT_B,
    K: float = DEFAULT_K,
    delta: float = DEFAULT_DELTA,
    kgrowth: float = DEFAULT_KGROWTH,
    kdeath: float = DEFAULT_KDEATH,
    p_fresh: float = DEFAULT_P_FRESH,
    lambda_dilution: float = DEFAULT_LAMBDA_DILUTION,
) -> SpeciesPool:
    """Draw N species from the canonical distributions.

    p_pref ~ U(p_pref_range) when p_pref_mode="uniform" (default; matches
    the public Ratzke simulation code). When p_pref_mode="bimodal", half the species are
    drawn from N(b-2, 0.3) (alkaline specialists) and half from
    N(b+2, 0.3) (acidic specialists), clipped to (0, 2b). This bimodal
    draw matches the experimental pH isolate distribution documented in
    R1-2 (strongly bimodal near pH 5 and pH 8/9) and is the recommended
    mode for Q5 Dominance sweeps -- it produces pH-driven Dominance which
    the uniform mode washes out.

    sigma is fixed to p_c=2.5 by default, matching the public Ratzke
    simulation code. Passing a range keeps the older exploratory behavior
    available for sensitivity checks.

    c_i sign:
        link_c_to_p_pref = True:
            c_i > 0 if p_pref_i > b (acidic optimum -> acidifier),
            c_i < 0 if p_pref_i < b (alkaline optimum -> alkalinizer).
          "Species modify pH toward their own optimum" reading of
          Ratzke 2018; retained only as a sensitivity option.
        link_c_to_p_pref = False (default):
            c_i ~ U(-c_mag, c_mag), matching the public Ratzke code's
            2*(random_sample-0.5)*interaction_strength.
    """
    if p_pref_mode == "uniform":
        p_pref = rng.uniform(*p_pref_range, size=N)
    elif p_pref_mode == "bimodal":
        # Gentle bimodal (same as pH_plus_LV_model): peaks at b +/- 1.5,
        # scale 0.8 so the two camps overlap slightly with neutral p0.
        half = N // 2
        alk = rng.normal(loc=b - 1.5, scale=0.8, size=half)
        aci = rng.normal(loc=b + 1.5, scale=0.8, size=N - half)
        p_pref = np.concatenate([alk, aci])
        rng.shuffle(p_pref)
        p_pref = np.clip(p_pref, 0.1, 2.0 * b - 0.1)
    else:
        raise ValueError(f"Unknown p_pref_mode: {p_pref_mode!r}")

    if sigma_range[0] == sigma_range[1]:
        sigma = np.full(N, float(sigma_range[0]))
    else:
        sigma = rng.uniform(*sigma_range, size=N)
    if link_c_to_p_pref:
        sign = np.where(p_pref > b, +1.0, -1.0)
        c = sign * c_mag
    else:
        c = rng.uniform(-c_mag, c_mag, size=N)
    return SpeciesPool(
        p_pref=p_pref, sigma=sigma, c=c, K=K, delta=delta, b=b,
        kgrowth=kgrowth, kdeath=kdeath, p_fresh=p_fresh,
        lambda_dilution=lambda_dilution,
    )


# ---- ODE RHS -----------------------------------------------------------
def _rhs(t, y, pool: SpeciesPool):
    """State vector y = [n_1, ..., n_N, p]. Returns dy/dt.

    Implements exactly:
        dn_i/dt = n_i (1 - n_i) (g_i(p) * (kgrowth + kdeath) - kdeath)
        g_i(p)  = exp(-((p-p_pref_i)^2)/(2*sigma_i^2))
        dp/dt   = K * sum_i(c_i n_i)
                + lambda_dilution * (p_fresh - p)

    Numerical guard: n_i is clipped to >= 0 before use; p is clipped to
    [0, 2b] before use in the growth terms.
    """
    N = pool.N()
    n = np.maximum(y[:N], 0.0)
    p_raw = y[N]
    p = min(max(p_raw, 0.0), 2.0 * pool.b)
    logistic = 1.0 - n
    # Gaussian growth kernel per species
    gauss = np.exp(-((p - pool.p_pref) ** 2) / (2.0 * pool.sigma ** 2))
    growth = gauss * (pool.kgrowth + pool.kdeath) - pool.kdeath
    dn = n * logistic * growth
    # Proton dynamics
    net_c = pool.K * np.sum(pool.c * n)
    dilution = pool.lambda_dilution * (pool.p_fresh - p)
    dp = net_c + dilution
    dy = np.empty_like(y)
    dy[:N] = dn
    dy[N] = dp
    return dy


def _integrate(pool: SpeciesPool,
               n0: np.ndarray,
               p0: float,
               t_end: float = T_END,
               method: str | None = None):
    """Integrate to t_end and return (n_final, p_final) or (None, None).

    Tries a cascade of methods for robustness: RK45 first (non-stiff,
    cheap), then LSODA (automatic stiffness handling), then BDF
    (implicit, handles stiffness but slower). Each attempt uses the same
    tolerances.  Returns the first successful result; returns
    (None, None) only if all fail.
    """
    y0 = np.concatenate([n0.astype(float), [float(p0)]])
    methods = [method] if method else ["RK45", "LSODA", "BDF"]
    y_final = None
    for m in methods:
        try:
            sol = solve_ivp(
                lambda t, y: _rhs(t, y, pool),
                (0.0, t_end), y0,
                method=m, t_eval=[t_end],
                rtol=RTOL, atol=ATOL,
            )
        except Exception:
            continue
        if not sol.success:
            continue
        y_final = np.asarray(sol.y)[:, -1]
        if np.all(np.isfinite(y_final)):
            break
        y_final = None
    if y_final is None:
        return None, None
    N = pool.N()
    n_final = y_final[:N]
    p_final = float(y_final[N])
    # Clamp trivial negatives from numerical error
    n_final = np.where(n_final < 0, 0.0, n_final)
    if np.any(n_final > BLOWUP_CAP):
        return None, None
    n_final = np.where(n_final < EXTINCTION, 0.0, n_final)
    return n_final, p_final


# ---- High-level assembly -----------------------------------------------
def simulate_single_community(
    pool: SpeciesPool,
    community_mask: np.ndarray,
    rng: np.random.Generator,
    p0: float = DEFAULT_P0,
    t_end: float = T_END,
    n0_scale: float = 0.05,
    return_pH: bool = False,
) -> np.ndarray | None:
    """Assemble a community by integrating the pH-feedback ODE on the
    subset of species selected by community_mask (bool, length = pool.N()).

    Returns a length-pool.N() abundance vector with zeros outside the
    selected support and after extinction. Returns None on integration
    failure.

    If return_pH is True, returns (n_full, p_final) instead; useful so the
    coalescence step can inherit the parent's equilibrium pH rather than
    resetting to neutral p0.
    """
    N = pool.N()
    if community_mask.sum() == 0:
        return (np.zeros(N), p0) if return_pH else np.zeros(N)
    sub = pool.subset(community_mask)
    # Initial biomass: small positive random draw on the *selected* species only.
    n0_sub = rng.uniform(0.5 * n0_scale, 1.5 * n0_scale, size=sub.N())
    n_final_sub, p_final = _integrate(sub, n0_sub, p0=p0, t_end=t_end)
    if n_final_sub is None:
        return None
    n_full = np.zeros(N)
    idx = np.where(community_mask)[0]
    n_full[idx] = n_final_sub
    if return_pH:
        return n_full, float(p_final)
    return n_full


def run_coalescence(
    pool: SpeciesPool,
    n_A: np.ndarray,
    n_B: np.ndarray,
    p0: float = DEFAULT_P0,
    t_end: float = T_END,
) -> np.ndarray | None:
    """Coalesce two parent communities 50/50 and re-integrate the full ODE
    to steady state. Returns length-N abundance vector (zeros for species
    not in either parent), or None on failure.
    """
    N = pool.N()
    mix = 0.5 * (n_A + n_B)
    mask = mix > EXTINCTION
    if mask.sum() == 0:
        return np.zeros(N)
    sub = pool.subset(mask)
    n0_sub = mix[mask]
    n_final_sub, p_final = _integrate(sub, n0_sub, p0=p0, t_end=t_end)
    if n_final_sub is None:
        return None
    out = np.zeros(N)
    idx = np.where(mask)[0]
    out[idx] = n_final_sub
    return out


# ---- Pool-level assembly (multiple parents per pool) -------------------
def assemble_pool(
    pool: SpeciesPool,
    num_C: int,
    sp_per_C: int,
    rng: np.random.Generator,
    p0: float = DEFAULT_P0,
    t_end: float = T_END,
    return_pH: bool = False,
) -> tuple[np.ndarray, list] | None:
    """Partition the species into num_C non-overlapping communities of
    sp_per_C species and integrate each independently.

    Returns (comm_masks [num_C, N] bool, sc_list [num_C x N] abundance)
    or None on repeated integration failure. If return_pH=True also
    returns per-parent equilibrium proton concentrations:
    (masks, sc_list, pH_list).
    """
    N = pool.N()
    if num_C * sp_per_C > N:
        raise ValueError(f"Need {num_C}*{sp_per_C}={num_C*sp_per_C} species "
                         f"but pool has only N={N}.")
    perm = rng.permutation(N)
    masks = np.zeros((num_C, N), dtype=bool)
    sc = []
    pHs = []
    for c in range(num_C):
        masks[c, perm[c * sp_per_C:(c + 1) * sp_per_C]] = True
        out = simulate_single_community(pool, masks[c], rng,
                                        p0=p0, t_end=t_end, return_pH=True)
        if out is None:
            return None
        n_c, p_c = out
        sc.append(n_c)
        pHs.append(p_c)
    if return_pH:
        return masks, sc, pHs
    return masks, sc


# ---- Outcome classification (matches common_setup) ---------------------
def classify_coalescence(n_A: np.ndarray,
                         n_B: np.ndarray,
                         n_C: np.ndarray) -> tuple[str, float, float, float, float]:
    """Thin wrapper around common_setup.metric_VectorDecomposition_onlyPositive
    + calculate_assymetricity + characterize_case. Returns
    (label_str, pdi, u, v, k). Imported lazily so the module can be used
    outside the Figure_generate tree too.
    """
    import sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    code_dir = os.path.abspath(os.path.join(here, "..", ".."))
    # common_setup uses RELATIVE paths (../../Analyzed/...) to load excel
    # sheets on import, so we must be cd'd to code_dir before the import.
    if code_dir not in sys.path:
        sys.path.insert(0, code_dir)
    _cwd = os.getcwd()
    try:
        os.chdir(code_dir)
        from common_setup import (  # noqa: E402
            metric_VectorDecomposition_onlyPositive,
            calculate_assymetricity,
            characterize_case,
        )
    finally:
        os.chdir(_cwd)
    LABELS = {0: "Dominance", 1: "Mixture", 2: "Restructuring"}
    # Degenerate inputs
    if np.all(n_A == 0) and np.all(n_B == 0):
        return "Restructuring", 0.5, 0.0, 0.0, 1.0
    if np.all(n_C == 0):
        return "Restructuring", 0.5, 0.0, 0.0, 1.0
    try:
        u, v, k = metric_VectorDecomposition_onlyPositive(n_A, n_B, n_C)
    except np.linalg.LinAlgError:
        return "Restructuring", 0.5, 0.0, 0.0, 1.0
    x, y = calculate_assymetricity(u, v, k)
    cls = characterize_case(x, y)
    if cls is None:
        cls = 2
    # PDI analogue: which parent pulled harder
    denom = u + v
    pdi = float(u / denom) if denom > 0 else 0.5
    return LABELS[cls], pdi, float(u), float(v), float(k)


def selection_phi(n_A: np.ndarray,
                  n_B: np.ndarray,
                  n_C: np.ndarray,
                  eps: float = EXTINCTION) -> float:
    """|phi|: absolute correlation between species origin (0=A-only, 1=B-only)
    and persistence (1 if species present in n_C). Returns nan when the
    origin or persist vector is constant.
    """
    surv_A = n_A > eps
    surv_B = n_B > eps
    surv_C = n_C > eps
    exclusive = surv_A ^ surv_B   # in exactly one parent
    idx = np.where(exclusive)[0]
    if idx.size < 2:
        return float("nan")
    origin = surv_B[idx].astype(int)          # 0 if A-only, 1 if B-only
    persist = surv_C[idx].astype(int)
    if len(set(origin)) < 2 or len(set(persist)) < 2:
        return float("nan")
    phi = np.corrcoef(origin, persist)[0, 1]
    return float(abs(phi)) if np.isfinite(phi) else float("nan")


# ---- Convenience: pH-tension knob --------------------------------------
def scale_interaction_strength(pool: SpeciesPool,
                               tension: float) -> SpeciesPool:
    """Return a pool whose pH-modification magnitude |c| is scaled by
    `tension`. tension=1.0 corresponds to the canonical c_mag; tension<1
    is weak interactions (nutrient-poor analogue), tension>1 is strong
    (nutrient-rich analogue).  This is the exact move validated by
    Ratzke, Barrere, Gore 2020: nutrient concentration controls |c|.
    """
    new_c = np.sign(pool.c) * (np.abs(pool.c) * tension)
    return SpeciesPool(
        p_pref=pool.p_pref.copy(),
        sigma=pool.sigma.copy(),
        c=new_c,
        K=pool.K, delta=pool.delta, b=pool.b,
        kgrowth=pool.kgrowth, kdeath=pool.kdeath,
        p_fresh=pool.p_fresh,
        lambda_dilution=pool.lambda_dilution,
    )
