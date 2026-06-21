"""
hybrid_original_model.py
========================

Faithful port of the lab's original intended pH+LV hybrid
(`gLV_pH_set1`) from /Users/jysong/Desktop/Codes/pH_model_Simulation/
(the working form is in main_simulation.ipynb; LV.py's copy is stale and
references undefined globals).

Equations (N_env = 1):
    dn_i/dt  = g_i * n_i * [ 1 - (I n)_i / k_i + q_i * env ]
    denv/dt  = delta_env * [ -env + sum_i p_i n_i - cubic * env^3 ]

So pH enters species growth ADDITIVELY through q_i * env, NOT multiplicatively
through I.  I (alpha_ij) is sampled once and never changes.  This matches
the original hybrid's structure exactly; it is a different coupling scheme
than pH_plus_LV_model.py (which uses Gaussian niches and the Ratzke-Gore
logistic pH ODE).

Hyperparameters
---------------
alpha       Off-diagonal interaction mean.  I[i,j] ~ U(0, 2*alpha) for i!=j,
            diagonal = 1.  Fixed at 0.3 for the current Q5 sweep.
tension     Single scalar pH-effect knob: p_i = tension * omega_p_i,
            q_i = tension * omega_q_i.  tension = 0 collapses to pure gLV.
mode        'continuous': omega_p, omega_q ~ U(-1, 1)
            'binary'    : omega_p, omega_q in {-1, +1}, 50/50
            In both modes omega_p and omega_q are sampled INDEPENDENTLY
            (no symmetry between production and response).

Fixed parameters (Jang's original defaults, preserved):
    g_i = 1, k_i = 1, delta_env = 0.1, cubic = 0.001, N_env = 1
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from scipy.integrate import solve_ivp

from pH_feedback_model import (
    EXTINCTION, BLOWUP_CAP, T_END, RTOL, ATOL,
)


DEFAULT_DELTA_ENV = 0.1
DEFAULT_CUBIC_DAMP = 0.001
DEFAULT_ENV0 = 0.0          # fresh medium starts at neutral env


# ---- Pool ------------------------------------------------------------------
@dataclass
class OriginalHybridPool:
    I: np.ndarray            # (N, N)  gLV interaction matrix
    g: np.ndarray            # (N,)    intrinsic growth rates
    k: np.ndarray            # (N,)    carrying capacities
    p: np.ndarray            # (N,)    species -> env (N_env = 1)
    q: np.ndarray            # (N,)    env -> species
    alpha: float
    tension: float
    mode: str
    delta_env: float = DEFAULT_DELTA_ENV
    cubic_damp: float = DEFAULT_CUBIC_DAMP

    def N(self) -> int:
        return int(self.I.shape[0])

    def subset(self, mask: np.ndarray) -> "OriginalHybridPool":
        idx = np.where(mask)[0]
        return OriginalHybridPool(
            I=self.I[np.ix_(idx, idx)].copy(),
            g=self.g[idx].copy(),
            k=self.k[idx].copy(),
            p=self.p[idx].copy(),
            q=self.q[idx].copy(),
            alpha=self.alpha,
            tension=self.tension,
            mode=self.mode,
            delta_env=self.delta_env,
            cubic_damp=self.cubic_damp,
        )


# ---- Sampling --------------------------------------------------------------
def sample_hybrid_pool(
    N: int,
    alpha: float,
    tension: float,
    rng: np.random.Generator,
    mode: str = "continuous",
) -> OriginalHybridPool:
    """Sample N species, the N x N gLV matrix, and two length-N pH vectors.

    I: diagonal = 1, off-diagonal ~ U(0, 2*alpha).  Matches the original
    uniform_distribution(u, o) with o = 0.

    p_i (species -> env) and q_i (env -> species) are sampled independently;
    tension scales both.  The original gLV_pH_set1 kept them independent
    (f_p and f_q separate callables in InitializeSpeciesPool_ver1), so we
    do the same here.
    """
    I = rng.uniform(0.0, 2.0 * alpha, size=(N, N))
    np.fill_diagonal(I, 1.0)
    g = np.ones(N)
    k = np.ones(N)

    if mode == "continuous":
        omega_p = rng.uniform(-1.0, 1.0, size=N)
        omega_q = rng.uniform(-1.0, 1.0, size=N)
    elif mode == "binary":
        omega_p = rng.choice([-1.0, 1.0], size=N).astype(float)
        omega_q = rng.choice([-1.0, 1.0], size=N).astype(float)
    else:
        raise ValueError(f"Unknown mode: {mode!r} (expected 'continuous' or 'binary')")

    p = tension * omega_p
    q = tension * omega_q

    return OriginalHybridPool(
        I=I, g=g, k=k, p=p, q=q,
        alpha=float(alpha), tension=float(tension), mode=mode,
    )


# ---- ODE -------------------------------------------------------------------
def _rhs(t, y, pool: OriginalHybridPool):
    """State y = [n_1, ..., n_N, env]. N_env = 1."""
    N = pool.N()
    n = np.maximum(y[:N], 0.0)
    env = y[N]

    comp = pool.I @ n
    growth_mult = 1.0 - comp / pool.k + pool.q * env
    dn = pool.g * n * growth_mult

    denv = pool.delta_env * (
        -env + float(np.dot(pool.p, n)) - pool.cubic_damp * env ** 3
    )

    dy = np.empty_like(y)
    dy[:N] = dn
    dy[N] = denv
    return dy


def _integrate(pool: OriginalHybridPool, n0: np.ndarray, env0: float,
               t_end: float = T_END, method: str | None = None):
    y0 = np.concatenate([n0.astype(float), [float(env0)]])
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
    env_final = float(y_final[N])
    n_final = np.where(n_final < 0, 0.0, n_final)
    if np.any(n_final > BLOWUP_CAP):
        return None, None
    n_final = np.where(n_final < EXTINCTION, 0.0, n_final)
    return n_final, env_final


# ---- Assembly and coalescence ----------------------------------------------
def simulate_single_community(
    pool: OriginalHybridPool,
    community_mask: np.ndarray,
    rng: np.random.Generator,
    env0: float = DEFAULT_ENV0,
    t_end: float = T_END,
    n0_scale: float = 0.05,
    return_env: bool = False,
):
    N = pool.N()
    if community_mask.sum() == 0:
        return (np.zeros(N), env0) if return_env else np.zeros(N)
    sub = pool.subset(community_mask)
    n0_sub = rng.uniform(0.5 * n0_scale, 1.5 * n0_scale, size=sub.N())
    n_final_sub, env_final = _integrate(sub, n0_sub, env0=env0, t_end=t_end)
    if n_final_sub is None:
        return None
    n_full = np.zeros(N)
    n_full[np.where(community_mask)[0]] = n_final_sub
    if return_env:
        return n_full, float(env_final)
    return n_full


def run_coalescence(
    pool: OriginalHybridPool,
    n_A: np.ndarray,
    n_B: np.ndarray,
    env0: float = DEFAULT_ENV0,
    t_end: float = T_END,
):
    N = pool.N()
    mix = 0.5 * (n_A + n_B)
    mask = mix > EXTINCTION
    if mask.sum() == 0:
        return np.zeros(N)
    sub = pool.subset(mask)
    n0_sub = mix[mask]
    n_final_sub, _ = _integrate(sub, n0_sub, env0=env0, t_end=t_end)
    if n_final_sub is None:
        return None
    out = np.zeros(N)
    out[np.where(mask)[0]] = n_final_sub
    return out


def assemble_pool(
    pool: OriginalHybridPool,
    num_C: int,
    sp_per_C: int,
    rng: np.random.Generator,
    env0: float = DEFAULT_ENV0,
    t_end: float = T_END,
    return_env: bool = False,
):
    N = pool.N()
    if num_C * sp_per_C > N:
        raise ValueError(
            f"Need {num_C}*{sp_per_C}={num_C*sp_per_C} species "
            f"but pool has only N={N}."
        )
    perm = rng.permutation(N)
    masks = np.zeros((num_C, N), dtype=bool)
    sc = []
    envs = []
    for c in range(num_C):
        masks[c, perm[c * sp_per_C:(c + 1) * sp_per_C]] = True
        out = simulate_single_community(
            pool, masks[c], rng, env0=env0, t_end=t_end, return_env=True
        )
        if out is None:
            return None
        n_c, env_c = out
        sc.append(n_c)
        envs.append(env_c)
    if return_env:
        return masks, sc, envs
    return masks, sc
