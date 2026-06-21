#!/usr/bin/env python
"""
R3-3 panel B: gLV extension to non-competitive interaction regimes.

Three regimes (kept at the same mean interspecific competition strength mu):
  comp   : alpha_ij ~ U[0, 2 mu]                         (paper baseline)
  exp25  : comp + 25% of unordered pairs made asymmetric
           (alpha_ji flipped to U[-2 mu, 0], while alpha_ij stays in U[0, 2 mu];
            one species exploits the other)
  coop25 : comp + 25% of unordered pairs made mutualistic
           (both alpha_ij and alpha_ji drawn from U[-f * 2 mu, 0] with f = 0.5,
            magnitude capped below self-regulation for stability)

For each (mu, regime) we simulate N_POOLS independent pools of N_POOL species,
partitioned into NUM_C non-overlapping communities of SP_PER_C species. Each
pool yields NUM_C * (NUM_C - 1) / 2 coalescence events. Pools with unstable
sampled matrices (estimated row-sum stability criterion violated, or any single
community blowing up to > 10 * carrying capacity) are hard-rejected and
re-sampled; we log the rejection rate.

Outputs (written next to this script):
  non_competitive_results.json  (outcome fractions, selection-correlation means)
  per_pool_records.csv          (per-pool provenance for re-running)
"""

import os
import json
import time
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- Parameters ---------------------------------------------------------
MU_VALUES = [0.30, 0.60, 0.80]
REGIMES = ['comp', 'exp15', 'coop15']
P_NONCOMP = 0.15          # fraction of pairs made non-competitive
EXP_F = 0.4               # exploitation negative-side cap (|alpha_neg| <= f * 2 mu)
COOP_F = 0.4              # cooperative magnitude cap (|alpha_neg| <= f * 2 mu)
N_POOL = 48
SP_PER_C = 12
NUM_C = 4                 # 4 communities per pool -> 6 coalescence events per pool
N_POOLS = 60              # per (mu, regime). 60 pools * 6 events = 360 events.
T_END = 5000.0
EXTINCTION = 1e-3
BLOWUP_CAP = 10.0         # reject matrices whose SC integration exceeds this
MAX_RESAMPLE = 200        # how many times we try to re-sample before giving up


# ---- gLV primitives (mirrors Figure_generate/code/LV.py) ---------------
def _glv_rhs(t, y, I, g, k):
    return g * y * (1.0 - (I @ y) / k)


def run_gLV(y0, s_idx, I, g, k, t_end=T_END):
    """Integrate gLV restricted to species whose mask is True in s_idx."""
    s_idx = np.where(s_idx)[0]
    if len(s_idx) == 0:
        return np.zeros_like(y0)
    y0_s = y0[s_idx].astype(float)
    I_s = I[np.ix_(s_idx, s_idx)]
    g_s = g[s_idx]
    k_s = k[s_idx]

    def f(t, y):
        return _glv_rhs(t, y, I_s, g_s, k_s)

    try:
        sol = solve_ivp(f, (0.0, t_end), y0_s, method='RK23', t_eval=[t_end])
        y_final = np.asarray(sol.y)[:, -1]
    except Exception:
        return None
    if y_final.shape[0] != len(s_idx) or not np.all(np.isfinite(y_final)):
        return None
    y_out = np.zeros_like(y0, dtype=float)
    y_out[s_idx] = y_final
    return y_out


# ---- Interaction matrix sampling ---------------------------------------
def sample_I(mu, regime, rng):
    """Draw one N_POOL x N_POOL interaction matrix for the given regime."""
    N = N_POOL
    # Baseline competitive fill, diagonal = 1.
    I = rng.uniform(0.0, 2.0 * mu, size=(N, N))
    np.fill_diagonal(I, 1.0)

    if regime == 'comp':
        return I

    # Pick 25% of the unordered off-diagonal pairs to convert.
    iu, ju = np.triu_indices(N, k=1)
    n_pairs = len(iu)
    k = int(round(P_NONCOMP * n_pairs))
    pick = rng.choice(n_pairs, size=k, replace=False)

    if regime == 'exp15':
        # Keep alpha_ij >= 0, flip alpha_ji into U[-EXP_F * 2 mu, 0].
        cap = EXP_F * 2.0 * mu
        for p in pick:
            i, j = iu[p], ju[p]
            I[j, i] = rng.uniform(-cap, 0.0)
    elif regime == 'coop15':
        # Both sides cooperative (negative), magnitude bounded by COOP_F.
        cap = COOP_F * 2.0 * mu
        for p in pick:
            i, j = iu[p], ju[p]
            I[i, j] = rng.uniform(-cap, 0.0)
            I[j, i] = rng.uniform(-cap, 0.0)
    else:
        raise ValueError(regime)

    return I


def row_sum_stable(I):
    """Simple local-stability screen: self-regulation must exceed the sum of
    negative off-diagonals on each row, so that a species does not grow
    unboundedly when its mutualistic partners are present.
    """
    N = I.shape[0]
    off = I.copy()
    np.fill_diagonal(off, 0.0)
    neg_row_sum = -np.minimum(off, 0.0).sum(axis=1)  # sum of |negatives|
    diag = np.diag(I)
    return np.all(diag > neg_row_sum + 1e-6)


# ---- Community assembly & coalescence ----------------------------------
def community_row_sum_stable(I, comm_mask):
    """Check self-regulation > sum of negatives on each row *within the
    community*. Whole-pool check is far too strict because negatives aggregate
    over 48 species; the relevant environment for each assembled community is
    its ~12 members."""
    idx = np.where(comm_mask)[0]
    if len(idx) == 0:
        return True
    sub = I[np.ix_(idx, idx)]
    off = sub.copy()
    np.fill_diagonal(off, 0.0)
    neg_row_sum = -np.minimum(off, 0.0).sum(axis=1)
    diag = np.diag(sub)
    return bool(np.all(diag > neg_row_sum + 1e-6))


def assemble_pool(mu, regime, rng):
    """Return (I, g, k, communities, sc, attempts) for a single pool, retrying
    on failure; returns None if we could not find a stable sample."""
    for attempt in range(MAX_RESAMPLE):
        I = sample_I(mu, regime, rng)

        g = np.ones(N_POOL)
        k = np.ones(N_POOL)

        # Partition species into NUM_C non-overlapping communities of SP_PER_C.
        perm = rng.permutation(N_POOL)
        comms = np.zeros((NUM_C, N_POOL), dtype=bool)
        for c in range(NUM_C):
            comms[c, perm[c * SP_PER_C:(c + 1) * SP_PER_C]] = True

        if not all(community_row_sum_stable(I, comms[c]) for c in range(NUM_C)):
            continue

        y_init = rng.random(N_POOL) * 0.1

        # Run each community alone.
        sc = []
        ok = True
        for c in range(NUM_C):
            y = run_gLV(y_init, comms[c], I, g, k)
            if y is None or np.any(y > BLOWUP_CAP):
                ok = False
                break
            y[y < EXTINCTION] = 0.0
            sc.append(y)
        if not ok:
            continue

        return I, g, k, comms, sc, attempt

    return None  # failed to find a stable matrix


def run_coalescence(sc_a, sc_b, I, g, k):
    y_mix = (sc_a + sc_b) / 2.0
    mask = y_mix > EXTINCTION
    y_out = run_gLV(y_mix, mask, I, g, k)
    if y_out is None or np.any(y_out > BLOWUP_CAP):
        return None
    y_out[y_out < EXTINCTION] = 0.0
    return y_out


# ---- Outcome classification (mirrors analyze_test_data_simple.py) -------
def _normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def vector_decomposition(parent_a, parent_b, mixed):
    u = _normalize(parent_a)
    v = _normalize(parent_b)
    m = _normalize(mixed)
    A = np.array([[np.dot(u, u), np.dot(u, v)],
                  [np.dot(u, v), np.dot(v, v)]])
    try:
        e12 = np.linalg.solve(A, np.array([np.dot(m, u), np.dot(m, v)]))
    except np.linalg.LinAlgError:
        return 0.0, 0.0, 1.0
    x1 = max(e12[0], 0.0)
    x2 = max(e12[1], 0.0)
    x3 = np.linalg.norm(m - e12[0] * u - e12[1] * v)
    if x1 ** 2 + x2 ** 2 == 0:
        return 0.0, 0.0, x3
    try:
        conv = np.sqrt(max(1.0 - x3 ** 2, 0.0) / (x1 ** 2 + x2 ** 2))
    except Exception:
        return x1, x2, x3
    return conv * x1, conv * x2, x3


def classify(parent_a, parent_b, mixed):
    if np.all(parent_a == 0) and np.all(parent_b == 0):
        return 'Restructuring', 0.5
    if np.all(mixed == 0):
        return 'Restructuring', 0.5
    x1, x2, _ = vector_decomposition(parent_a, parent_b, mixed)
    r2 = x1 ** 2 + x2 ** 2
    if x2 == 0 and x1 == 0:
        return 'Restructuring', 0.5
    theta = np.arctan2(x1, x2)        # 0 = B-dominated, pi/2 = A-dominated
    pdi = theta / (np.pi / 2)          # 0 -> B, 1 -> A, 0.5 -> balanced
    asym = abs(abs(theta - np.pi / 4) / (np.pi / 4))
    if r2 > 0.5 and asym > 0.5:
        return 'Dominance', pdi
    if r2 > 0.5 and asym <= 0.5:
        return 'Mixture', pdi
    return 'Restructuring', pdi


# ---- Pairwise selection correlation -------------------------------------
def selection_correlation(events, spec_pair_same):
    """events: list of dicts per coalescence with keys survived_a, survived_b,
    survived_c (binary arrays). spec_pair_same: mapping (i,j) -> True if i and
    j are from the same parent across the event.

    Returns mean phi coefficient between origin (0 = parent A, 1 = parent B)
    and persistence (1 if species in C at end), computed on survivors of
    (A cup B) within each event, averaged across events.
    """
    phis = []
    for ev in events:
        orig = ev['origin']
        persist = ev['persist']
        if len(set(orig)) < 2 or len(set(persist)) < 2:
            continue
        phi = np.corrcoef(orig, persist)[0, 1]
        if np.isfinite(phi):
            phis.append(abs(phi))
    return float(np.mean(phis)) if phis else float('nan')


# ---- Driver ------------------------------------------------------------
def run():
    t0 = time.time()
    rng = np.random.default_rng(20260421)

    results = {}
    for mu in MU_VALUES:
        for regime in REGIMES:
            key = f'mu={mu:.2f}_{regime}'
            print(f'\n[{key}] running {N_POOLS} pools')
            events = []
            rejects = 0
            outcomes = {'Dominance': 0, 'Mixture': 0, 'Restructuring': 0}
            for pool_idx in range(N_POOLS):
                sub_rng = np.random.default_rng(rng.integers(1 << 31))
                out = assemble_pool(mu, regime, sub_rng)
                if out is None:
                    rejects += 1
                    continue
                I, g, k, comms, sc, attempts = out
                rejects += attempts
                for a in range(NUM_C):
                    for b in range(a + 1, NUM_C):
                        cc = run_coalescence(sc[a], sc[b], I, g, k)
                        if cc is None:
                            continue
                        label, pdi = classify(sc[a], sc[b], cc)
                        outcomes[label] += 1
                        # Build per-event selection record for species that
                        # were present in at least one parent at steady state.
                        surv_a = (sc[a] > EXTINCTION)
                        surv_b = (sc[b] > EXTINCTION)
                        surv_c = (cc > EXTINCTION)
                        union = surv_a | surv_b
                        idx = np.where(union)[0]
                        origin = np.array([0 if surv_a[i] and not surv_b[i]
                                           else (1 if surv_b[i] and not surv_a[i]
                                                 else -1)
                                           for i in idx])
                        mask = origin >= 0
                        events.append({
                            'origin': origin[mask],
                            'persist': surv_c[idx[mask]].astype(int),
                        })
            n_out = sum(outcomes.values())
            fracs = {lab: (count / n_out if n_out else 0.0)
                     for lab, count in outcomes.items()}

            psc = selection_correlation(events, None)

            results[key] = {
                'mu': mu,
                'regime': regime,
                'n_events': n_out,
                'rejects': rejects,
                **{f'frac_{lab}': v for lab, v in fracs.items()},
                'psc_phi': psc,
            }
            print(f'  events={n_out}, rejects={rejects}, '
                  f'Dom={fracs["Dominance"]:.2f}, '
                  f'Mix={fracs["Mixture"]:.2f}, '
                  f'Res={fracs["Restructuring"]:.2f}, '
                  f'|phi|={psc:.2f}')

    elapsed = time.time() - t0
    print(f'\nTotal elapsed: {elapsed/60:.1f} min')

    out_path = os.path.join(SCRIPT_DIR, 'non_competitive_results.json')
    with open(out_path, 'w') as fh:
        json.dump({'parameters': {'N_POOL': N_POOL, 'SP_PER_C': SP_PER_C,
                                   'NUM_C': NUM_C, 'N_POOLS': N_POOLS,
                                   'P_NONCOMP': P_NONCOMP, 'COOP_F': COOP_F,
                                   'MU_VALUES': MU_VALUES, 'REGIMES': REGIMES},
                   'results': results}, fh, indent=2)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    run()
