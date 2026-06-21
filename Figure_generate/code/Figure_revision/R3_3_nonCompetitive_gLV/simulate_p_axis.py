#!/usr/bin/env python
"""
R3-4 reciprocal pair-coupling sweep.

For each unordered pair (i, j), a fraction |p| of pairs is converted from the
iid competitive baseline. The sign of p controls the converted structure:

  p > 0  symmetric competition: alpha_ij = alpha_ji = alpha,
         with alpha drawn from U[0, 2mu].
  p < 0  antisymmetric exploitation: alpha_ij = alpha and alpha_ji = -alpha,
         with alpha drawn from U[0, 2mu].
  p = 0  iid competitive baseline: alpha_ij and alpha_ji are independently
         drawn from U[0, 2mu].

This preserves the baseline competitive marginal for iid pairs and tests
whether the Dominance trend depends on independent reciprocal coefficients.

Outputs:
  p_axis_results.json         Dom/Mix/Res fractions + |phi| per (mu, p)
"""

import os
import json
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, HERE)
from simulate_non_competitive import (
    N_POOL, SP_PER_C, NUM_C, T_END, EXTINCTION, BLOWUP_CAP, MAX_RESAMPLE,
    run_gLV, community_row_sum_stable, run_coalescence,
    classify, selection_correlation,
)

MU_VALUES = [0.30, 0.60, 0.80]

# Unified axis: 5 values of p, always with the U[0, 2mu] marginal for iid pairs.
# Operational definition: for each unordered pair (i, j),
#   * with prob (1 - |p|): draw alpha_ij, alpha_ji iid from U[0, 2 mu]
#                          (paper baseline "iid competition")
#   * with prob |p|: draw alpha ~ U[0, 2 mu], then
#        - if p > 0 (symmetric competition): alpha_ij = alpha_ji = alpha
#        - if p < 0 (exploitation):          alpha_ij = alpha, alpha_ji = -alpha
# Diagonal is fixed at 1.0 throughout (= -1 self-regulation in the standard
# gLV sign convention, cf. LV.py).
CASES = [
    ('pneg1',  'p = -1',   -1.0),
    ('pneg05', 'p = -0.5', -0.5),
    ('p0',     'p = 0',     0.0),
    ('ppos05', 'p = +0.5', +0.5),
    ('ppos1',  'p = +1',   +1.0),
]

N_POOLS = 200                 # 200 pools x 6 events = 1200 events per (mu, case)


# ---- Unified interaction-matrix sampler --------------------------------
def sample_I_unified(mu, p, rng):
    """Draw one N_POOL x N_POOL interaction matrix under the U[0, 2mu] marginal
    and signed-p coupling."""
    N = N_POOL
    I = np.empty((N, N), dtype=float)
    iu, ju = np.triu_indices(N, k=1)
    n_pairs = len(iu)

    baseline_draw = lambda size: rng.uniform(0.0, 2.0 * mu, size=size)

    if abs(p) < 1e-10:
        # Fully iid competition (paper baseline).
        I[iu, ju] = baseline_draw(n_pairs)
        I[ju, iu] = baseline_draw(n_pairs)
    else:
        convert_mask = rng.random(n_pairs) < abs(p)
        n_conv = int(convert_mask.sum())
        n_iid = n_pairs - n_conv

        if n_iid > 0:
            I[iu[~convert_mask], ju[~convert_mask]] = baseline_draw(n_iid)
            I[ju[~convert_mask], iu[~convert_mask]] = baseline_draw(n_iid)

        if n_conv > 0:
            conv_alpha = baseline_draw(n_conv)
            I[iu[convert_mask], ju[convert_mask]] = conv_alpha
            if p > 0:
                # symmetric competition: alpha_ji = alpha_ij (both positive)
                I[ju[convert_mask], iu[convert_mask]] = conv_alpha
            else:
                # exploitation: alpha_ji = -alpha_ij (anti-symmetric)
                I[ju[convert_mask], iu[convert_mask]] = -conv_alpha

    np.fill_diagonal(I, 1.0)
    return I


# ---- Assembly (mirrors simulate_non_competitive.py) --------------------
def assemble_pool(mu, p, rng):
    """Assemble one pool. For p < 0 (exploitation/antisymmetric) we skip the
    row-sum pre-filter because the U[0, 2mu]-flipped marginal makes it reject
    every sample at mu >= 0.1; dynamical BLOWUP_CAP does the stability work
    instead (standard practice for mixed-sign gLV, cf. Allesina-Tang 2012,
    Bastolla et al. 2009, Dougoud et al. 2018)."""
    use_row_sum = (p >= 0)
    for attempt in range(MAX_RESAMPLE):
        I = sample_I_unified(mu, p, rng)
        g = np.ones(N_POOL)
        k = np.ones(N_POOL)

        perm = rng.permutation(N_POOL)
        comms = np.zeros((NUM_C, N_POOL), dtype=bool)
        for c in range(NUM_C):
            comms[c, perm[c * SP_PER_C:(c + 1) * SP_PER_C]] = True

        if use_row_sum and not all(
                community_row_sum_stable(I, comms[c]) for c in range(NUM_C)):
            continue

        y_init = rng.random(N_POOL) * 0.1
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
    return None


# ---- Driver ------------------------------------------------------------
def run():
    t0 = time.time()
    rng = np.random.default_rng(20260422)
    results = {}

    for mu in MU_VALUES:
        for case_key, case_label, p in CASES:
            key = f'mu={mu:.2f}_{case_key}'
            print(f'\n[{key}] {case_label}  -- {N_POOLS} pools', flush=True)
            events = []
            rejects = 0
            outcomes = {'Dominance': 0, 'Mixture': 0, 'Restructuring': 0}
            for pool_idx in range(N_POOLS):
                sub_rng = np.random.default_rng(rng.integers(1 << 31))
                out = assemble_pool(mu, p, sub_rng)
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
                'case': case_key,
                'p': p,
                'label': case_label,
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

    out_path = os.path.join(HERE, 'p_axis_results.json')
    with open(out_path, 'w') as fh:
        json.dump({
            'parameters': {
                'N_POOL': N_POOL, 'SP_PER_C': SP_PER_C, 'NUM_C': NUM_C,
                'N_POOLS': N_POOLS, 'MU_VALUES': MU_VALUES,
                'CASES': [{'key': k, 'label': l, 'p': pp}
                          for (k, l, pp) in CASES],
            },
            'results': results,
        }, fh, indent=2)
    print(f'Saved {out_path}')


if __name__ == '__main__':
    run()
