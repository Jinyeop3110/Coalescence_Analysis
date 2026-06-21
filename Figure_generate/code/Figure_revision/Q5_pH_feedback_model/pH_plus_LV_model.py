"""
pH_plus_LV_model.py
===================

Third model for internal-memo Q5: a *hybrid* of the Ratzke-Gore pH-feedback
framework and the paper's own pairwise gLV.  Built as an adaptation of the
pH+LV variant from `/Users/jysong/Desktop/Codes/pH_model_Simulation/LV.py`
(`gLV_pH_set1`), re-grounded in the Ratzke-Gore pH ODE so that all three
Q5 models share a common pH chemistry and differ only in how species
interact.  We do not reproduce the original additive `q . env` structure
verbatim; we use a multiplicative form that keeps the Ratzke Gaussian
growth kernel intact and adds the gLV competition term on top, which is
the minimal edit that makes the model a true superset of both.

Equations
---------
Species dynamics:
    dn_i/dt = n_i * ( gauss_i(p) - delta - (A n)_i / K )

where:
    gauss_i(p) = exp(-((p - p_pref_i) / sigma_i)**2)
    A_{ii} = 1  (self-regulation, same as R3_3 gLV)
    A_{ij} ~ U(0, 2*mu)  for i != j,  mu = gLV interaction strength

Proton dynamics (identical to Ratzke & Gore 2018):
    dp/dt = ( sum_i c_i n_i ) * p * (2b - p) / b

Limits and reductions
---------------------
- mu = 0  AND  alpha_{ii}=1 (default): reduces to a neutral competition
  for space similar to Ratzke 2018 logistic `1 - sum n_j / K` up to a
  diagonal factor. We therefore *preserve the Ratzke competition regime
  as the mu=0 limit*.
- pH_tension = 0 (c_mag = 0) and flat gauss_i (p_pref all = p0): reduces
  to the baseline gLV of R3_3 with constant r_i = (1-delta).
- pH_tension > 0 and mu = 0: reduces (up to the diagonal) to the pure
  pH-feedback model of pH_feedback_model.py.
- pH_tension > 0 and mu > 0: full hybrid, the case we care about for Q5.

Both knobs are now independent:
    mu          = mean non-self gLV interaction coefficient
    pH_tension  = multiplicative scaling of |c| (same knob as pH-only model)

Headline metric
---------------
Dominance fraction. |phi| (origin -> persistence) is still reported but is
a secondary signal; the primary comparison with the paper's headline
result is the class-frequency Dominance axis.

Classification uses the identical common_setup pipeline as
pH_feedback_model.py and the gLV simulator in R3_3_nonCompetitive_gLV.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from scipy.integrate import solve_ivp

# Re-use Ratzke-Gore defaults from the pH-only model so the two are
# numerically comparable at mu=0.
from pH_feedback_model import (
    DEFAULT_SIGMA, DEFAULT_DELTA, DEFAULT_C_MAG, DEFAULT_B,
    DEFAULT_K, DEFAULT_P0,
    EXTINCTION, BLOWUP_CAP, T_END, RTOL, ATOL,
    classify_coalescence, selection_phi,
)


# ---- Species+interaction pool ------------------------------------------
@dataclass
class HybridPool:
    """Species parameters plus the gLV interaction matrix.

    Arrays p_pref, sigma, c are length N (identical to SpeciesPool in
    pH_feedback_model).  alpha is shape (N, N) with diagonal = 1 and
    off-diagonal ~ U(0, 2*mu).
    """
    p_pref: np.ndarray
    sigma:  np.ndarray
    c:      np.ndarray
    alpha:  np.ndarray      # (N, N)
    mu:     float           # stored for bookkeeping / reproducibility
    K:      float = DEFAULT_K
    delta:  float = DEFAULT_DELTA
    b:      float = DEFAULT_B

    def N(self) -> int:
        return int(self.p_pref.shape[0])

    def subset(self, mask: np.ndarray) -> "HybridPool":
        idx = np.where(mask)[0]
        A = self.alpha[np.ix_(idx, idx)].copy()
        return HybridPool(
            p_pref=self.p_pref[idx].copy(),
            sigma=self.sigma[idx].copy(),
            c=self.c[idx].copy(),
            alpha=A,
            mu=self.mu,
            K=self.K, delta=self.delta, b=self.b,
        )


# ---- Sampling ----------------------------------------------------------
def sample_hybrid_pool(
    N: int,
    mu: float,
    rng: np.random.Generator,
    c_mag: float = DEFAULT_C_MAG,
    p_pref_mode: str = "bimodal",         # "uniform" | "bimodal"
    p_pref_range: tuple = (2.0, 8.0),
    sigma_range:  tuple = (1.0, 2.0),      # narrower than pure pH by default
    link_c_to_p_pref: bool = True,
    b: float = DEFAULT_B,
    K: float = DEFAULT_K,
    delta: float = DEFAULT_DELTA,
) -> HybridPool:
    """Sample N species and their N x N gLV matrix.

    p_pref_mode:
        "uniform"  : p_pref ~ U(p_pref_range). Matches the pH-only default.
        "bimodal"  : p_pref drawn from two narrow Gaussians at (b-2, b+2),
                     50/50.  Matches the experimental pH isolate
                     distribution (R1-2: strongly bimodal around pH 5 and
                     pH 8/9).  *This is the default for the hybrid* because
                     it produces the pH-driven Dominance signal we need;
                     see the README of this folder.
    sigma_range default tightened to U(1, 2) (specialized species) so that
    pH-mismatched species die quickly when the environment shifts, which
    is what produces Dominance in the pH axis.

    alpha: diag=1, off-diag ~ U(0, 2*mu). Same convention as R3_3.
    """
    # species optima
    if p_pref_mode == "bimodal":
        # Gentle bimodal: peaks at b +/- 1.5 (not +/-2), scale 0.8 (not 0.3),
        # so the two "pH camps" overlap a little with the neutral midpoint
        # and the coalescence step can converge without mass extinction.
        half = N // 2
        alk = rng.normal(loc=b - 1.5, scale=0.8, size=half)
        aci = rng.normal(loc=b + 1.5, scale=0.8, size=N - half)
        p_pref = np.concatenate([alk, aci])
        rng.shuffle(p_pref)
        p_pref = np.clip(p_pref, 0.1, 2.0 * b - 0.1)
    elif p_pref_mode == "uniform":
        p_pref = rng.uniform(*p_pref_range, size=N)
    else:
        raise ValueError(f"Unknown p_pref_mode: {p_pref_mode!r}")

    sigma = rng.uniform(*sigma_range, size=N)

    # pH-modification sign
    if link_c_to_p_pref:
        sign = np.where(p_pref > b, +1.0, -1.0)
    else:
        sign = np.where(rng.random(N) < 0.5, +1.0, -1.0)
    c = sign * c_mag

    # gLV interaction matrix
    A = rng.uniform(0.0, 2.0 * mu, size=(N, N))
    np.fill_diagonal(A, 1.0)

    return HybridPool(p_pref=p_pref, sigma=sigma, c=c,
                      alpha=A, mu=mu,
                      K=K, delta=delta, b=b)


# ---- ODE RHS -----------------------------------------------------------
def _rhs(t, y, pool: HybridPool):
    """State vector y = [n_1, ..., n_N, p]. Returns dy/dt.

    Implements:
        dn_i/dt = n_i * (gauss_i(p) - delta - (A n)_i / K)
        dp/dt   = (sum_i c_i n_i) * p * (2b - p) / b
    """
    N = pool.N()
    n = np.maximum(y[:N], 0.0)
    p_raw = y[N]
    p = min(max(p_raw, 0.0), 2.0 * pool.b)

    gauss = np.exp(-((p - pool.p_pref) / pool.sigma) ** 2)
    r_eff = gauss - pool.delta                      # per-species growth
    comp = pool.alpha @ n                           # gLV competition term
    dn = n * (r_eff - comp / pool.K)

    net_c = np.sum(pool.c * n)
    p_factor = p * (2.0 * pool.b - p) / pool.b
    dp = net_c * p_factor

    dy = np.empty_like(y)
    dy[:N] = dn
    dy[N] = dp
    return dy


def _integrate(pool: HybridPool, n0: np.ndarray, p0: float,
               t_end: float = T_END, method: str | None = None):
    """Integrate and return (n_final, p_final) or (None, None)."""
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
    n_final = np.where(n_final < 0, 0.0, n_final)
    if np.any(n_final > BLOWUP_CAP):
        return None, None
    n_final = np.where(n_final < EXTINCTION, 0.0, n_final)
    return n_final, p_final


# ---- High-level assembly and coalescence -------------------------------
def simulate_single_community(
    pool: HybridPool,
    community_mask: np.ndarray,
    rng: np.random.Generator,
    p0: float = DEFAULT_P0,
    t_end: float = T_END,
    n0_scale: float = 0.05,
    return_pH: bool = False,
) -> np.ndarray | None:
    N = pool.N()
    if community_mask.sum() == 0:
        return (np.zeros(N), p0) if return_pH else np.zeros(N)
    sub = pool.subset(community_mask)
    n0_sub = rng.uniform(0.5 * n0_scale, 1.5 * n0_scale, size=sub.N())
    n_final_sub, p_final = _integrate(sub, n0_sub, p0=p0, t_end=t_end)
    if n_final_sub is None:
        return None
    n_full = np.zeros(N)
    n_full[np.where(community_mask)[0]] = n_final_sub
    if return_pH:
        return n_full, float(p_final)
    return n_full


def run_coalescence(
    pool: HybridPool,
    n_A: np.ndarray,
    n_B: np.ndarray,
    p0: float = DEFAULT_P0,
    t_end: float = T_END,
) -> np.ndarray | None:
    N = pool.N()
    mix = 0.5 * (n_A + n_B)
    mask = mix > EXTINCTION
    if mask.sum() == 0:
        return np.zeros(N)
    sub = pool.subset(mask)
    n0_sub = mix[mask]
    n_final_sub, _ = _integrate(sub, n0_sub, p0=p0, t_end=t_end)
    if n_final_sub is None:
        return None
    out = np.zeros(N)
    out[np.where(mask)[0]] = n_final_sub
    return out


def assemble_pool(
    pool: HybridPool,
    num_C: int,
    sp_per_C: int,
    rng: np.random.Generator,
    p0: float = DEFAULT_P0,
    t_end: float = T_END,
    return_pH: bool = False,
) -> tuple[np.ndarray, list] | None:
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


# ---- Knob helpers ------------------------------------------------------
def scale_pH_tension(pool: HybridPool, tension: float) -> HybridPool:
    """Scale |c| by `tension`; leave alpha, p_pref, sigma untouched."""
    new_c = np.sign(pool.c) * (np.abs(pool.c) * tension)
    return HybridPool(
        p_pref=pool.p_pref.copy(),
        sigma=pool.sigma.copy(),
        c=new_c,
        alpha=pool.alpha.copy(),
        mu=pool.mu,
        K=pool.K, delta=pool.delta, b=pool.b,
    )
