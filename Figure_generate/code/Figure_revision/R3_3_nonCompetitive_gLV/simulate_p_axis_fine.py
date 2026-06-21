#!/usr/bin/env python
"""
R3-4 reciprocal pair-coupling sweep, fine p grid.

This is a higher-resolution companion to simulate_p_axis.py. It keeps the same
non-negative marginal alpha_ij ~ U[0, 2mu] and sweeps p from -1 to +1 in steps
of 0.2. For p > 0, converted pairs are symmetric competition; for p < 0,
converted pairs are antisymmetric exploitation.

Output:
  p_axis_fine_results.json
"""

import json
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, HERE)
from simulate_p_axis import (  # noqa: E402
    MU_VALUES, sample_I_unified, run_coalescence, classify,
    selection_correlation,
)
from simulate_non_competitive import (  # noqa: E402
    N_POOL, SP_PER_C, NUM_C, EXTINCTION, BLOWUP_CAP, MAX_RESAMPLE,
    run_gLV, community_row_sum_stable,
)


P_VALUES = [round(x, 1) for x in np.arange(-1.0, 1.0001, 0.2)]
N_POOLS = int(os.environ.get('N_POOLS', '200'))
OUT_PATH = os.path.join(HERE, 'p_axis_fine_results.json')


def case_key(p):
    if abs(p) < 1e-10:
        return 'p0'
    prefix = 'ppos' if p > 0 else 'pneg'
    return f'{prefix}{abs(p):.1f}'.replace('.', 'p')


def case_label(p):
    return f'p = {p:+.1f}' if p else 'p = 0'


def assemble_pool(mu, p, rng):
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


def run():
    t0 = time.time()
    rng = np.random.default_rng(20260430)
    results = {}

    def write_checkpoint():
        with open(OUT_PATH, 'w') as fh:
            json.dump({
                'parameters': {
                    'N_POOL': N_POOL,
                    'SP_PER_C': SP_PER_C,
                    'NUM_C': NUM_C,
                    'N_POOLS': N_POOLS,
                    'MU_VALUES': MU_VALUES,
                    'P_VALUES': P_VALUES,
                },
                'results': results,
            }, fh, indent=2)

    for mu in MU_VALUES:
        for p in P_VALUES:
            key = f'mu={mu:.2f}_{case_key(p)}'
            print(f'\n[{key}] {case_label(p)} -- {N_POOLS} pools',
                  flush=True)
            events = []
            rejects = 0
            coalescence_failures = 0
            outcomes = {'Dominance': 0, 'Mixture': 0, 'Restructuring': 0}

            for pool_idx in range(N_POOLS):
                sub_rng = np.random.default_rng(rng.integers(1 << 31))
                out = assemble_pool(mu, p, sub_rng)
                if out is None:
                    rejects += MAX_RESAMPLE
                    continue
                I, g, k, comms, sc, attempts = out
                rejects += attempts

                for a in range(NUM_C):
                    for b in range(a + 1, NUM_C):
                        cc = run_coalescence(sc[a], sc[b], I, g, k)
                        if cc is None:
                            coalescence_failures += 1
                            continue
                        label, pdi = classify(sc[a], sc[b], cc)
                        outcomes[label] += 1

                        surv_a = (sc[a] > EXTINCTION)
                        surv_b = (sc[b] > EXTINCTION)
                        surv_c = (cc > EXTINCTION)
                        union = surv_a | surv_b
                        idx = np.where(union)[0]
                        origin = np.array([
                            0 if surv_a[i] and not surv_b[i]
                            else (1 if surv_b[i] and not surv_a[i] else -1)
                            for i in idx
                        ])
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
                'case': case_key(p),
                'p': p,
                'label': case_label(p),
                'n_events': n_out,
                'rejects': rejects,
                'coalescence_failures': coalescence_failures,
                **{f'frac_{lab}': v for lab, v in fracs.items()},
                'psc_phi': psc,
            }
            print(f'  events={n_out}, rejects={rejects}, '
                  f'coal_fail={coalescence_failures}, '
                  f'Dom={fracs["Dominance"]:.2f}, '
                  f'Mix={fracs["Mixture"]:.2f}, '
                  f'Res={fracs["Restructuring"]:.2f}, |phi|={psc:.2f}',
                  flush=True)
            write_checkpoint()

    elapsed = time.time() - t0
    print(f'\nTotal elapsed: {elapsed/60:.1f} min')
    write_checkpoint()
    print(f'Saved {OUT_PATH}')


if __name__ == '__main__':
    run()
