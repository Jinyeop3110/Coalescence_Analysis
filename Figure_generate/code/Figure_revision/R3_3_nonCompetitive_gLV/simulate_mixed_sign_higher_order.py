#!/usr/bin/env python
"""
R3-4 Version A: mixed-sign gLV with density-dependent self-limitation.

This is the facilitation-facing counterpart to simulate_p_axis.py. Instead of
changing reciprocal-pair correlation at a non-negative marginal, this script
adds an iid facilitative tail:

    alpha_ij ~ U[-f * mu, (2 + f) * mu]

so E[alpha_ij] = mu for every f. In the paper's sign convention,
alpha_ij < 0 is facilitation. Dynamics are stabilized with a higher-order
self-limitation term:

    dn_i/dt = n_i * (1 - (A n)_i - gamma * n_i^2)

where gamma = 0.10 by default. The extra term is cubic self-regulation in
abundance dynamics and represents density-dependent self-limitation.

Outputs:
  mixed_sign_higher_order_results.json
"""

import json
import os
import time

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, HERE)
from simulate_non_competitive import (  # noqa: E402
    N_POOL, SP_PER_C, NUM_C, T_END, EXTINCTION, BLOWUP_CAP, MAX_RESAMPLE,
    classify, selection_correlation,
)


MU_VALUES = [0.30, 0.60, 0.80]
F_VALUES = [0.00, 0.10, 0.20, 0.40, 0.80]
GAMMA = 0.10
N_POOLS = int(os.environ.get('N_POOLS', '200'))
ODE_METHOD = 'LSODA'
OUT_PATH = os.path.join(HERE, 'mixed_sign_higher_order_results.json')


def _glv_rhs_higher_order(t, y, I, gamma):
    return y * (1.0 - (I @ y) - gamma * y ** 2)


def run_gLV_higher_order(y0, s_idx, I, gamma=GAMMA, t_end=T_END):
    """Integrate mixed-sign gLV restricted to species in s_idx."""
    s_idx = np.where(s_idx)[0]
    if len(s_idx) == 0:
        return np.zeros_like(y0)

    y0_s = y0[s_idx].astype(float)
    I_s = I[np.ix_(s_idx, s_idx)]

    def f_rhs(t, y):
        return _glv_rhs_higher_order(t, y, I_s, gamma)

    try:
        # Mixed-sign systems can become stiff near the boundary between
        # facilitation and self-limitation; LSODA avoids pathological RK23
        # slowdowns in those cells while preserving the same ODE definition.
        sol = solve_ivp(f_rhs, (0.0, t_end), y0_s, method=ODE_METHOD,
                        t_eval=[t_end])
        if not sol.success:
            return None
        y_final = np.asarray(sol.y)[:, -1]
    except Exception:
        return None

    if y_final.shape[0] != len(s_idx) or not np.all(np.isfinite(y_final)):
        return None
    if np.any(y_final < -1e-7):
        return None
    y_final = np.maximum(y_final, 0.0)

    y_out = np.zeros_like(y0, dtype=float)
    y_out[s_idx] = y_final
    return y_out


def sample_I_mixed_sign(mu, f_tail, rng):
    """Mean-preserving iid mixed-sign interaction matrix."""
    low = -f_tail * mu
    high = (2.0 + f_tail) * mu
    I = rng.uniform(low, high, size=(N_POOL, N_POOL))
    np.fill_diagonal(I, 1.0)
    return I


def assemble_pool(mu, f_tail, rng, gamma=GAMMA):
    """Return (I, communities, single-community states, attempts)."""
    for attempt in range(MAX_RESAMPLE):
        I = sample_I_mixed_sign(mu, f_tail, rng)

        perm = rng.permutation(N_POOL)
        comms = np.zeros((NUM_C, N_POOL), dtype=bool)
        for c in range(NUM_C):
            comms[c, perm[c * SP_PER_C:(c + 1) * SP_PER_C]] = True

        y_init = rng.random(N_POOL) * 0.1

        sc = []
        ok = True
        for c in range(NUM_C):
            y = run_gLV_higher_order(y_init, comms[c], I, gamma=gamma)
            if y is None or np.any(y > BLOWUP_CAP):
                ok = False
                break
            y[y < EXTINCTION] = 0.0
            sc.append(y)
        if not ok:
            continue

        return I, comms, sc, attempt

    return None


def run_coalescence(sc_a, sc_b, I, gamma=GAMMA):
    y_mix = (sc_a + sc_b) / 2.0
    mask = y_mix > EXTINCTION
    y_out = run_gLV_higher_order(y_mix, mask, I, gamma=gamma)
    if y_out is None or np.any(y_out > BLOWUP_CAP):
        return None
    y_out[y_out < EXTINCTION] = 0.0
    return y_out


def frac_negative_for_tail(f_tail):
    if f_tail <= 0:
        return 0.0
    return f_tail / (2.0 + 2.0 * f_tail)


def summarize_abundances(vectors):
    if not vectors:
        return {'mean_richness': float('nan'), 'mean_max_abundance': float('nan')}
    richness = [float(np.sum(v > EXTINCTION)) for v in vectors]
    max_abund = [float(np.max(v)) if len(v) else 0.0 for v in vectors]
    return {
        'mean_richness': float(np.mean(richness)),
        'mean_max_abundance': float(np.mean(max_abund)),
        'p95_max_abundance': float(np.percentile(max_abund, 95)),
    }


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
                    'F_VALUES': F_VALUES,
                    'GAMMA': GAMMA,
                    'ODE_METHOD': ODE_METHOD,
                    'EXTINCTION': EXTINCTION,
                    'BLOWUP_CAP': BLOWUP_CAP,
                },
                'results': results,
            }, fh, indent=2)

    for mu in MU_VALUES:
        for f_tail in F_VALUES:
            key = f'mu={mu:.2f}_f={f_tail:.2f}'
            print(f'\n[{key}] gamma={GAMMA:.2f} -- {N_POOLS} pools',
                  flush=True)
            events = []
            rejects = 0
            coalescence_failures = 0
            outcomes = {'Dominance': 0, 'Mixture': 0, 'Restructuring': 0}
            sc_vectors = []
            cc_vectors = []

            for pool_idx in range(N_POOLS):
                sub_rng = np.random.default_rng(rng.integers(1 << 31))
                out = assemble_pool(mu, f_tail, sub_rng, gamma=GAMMA)
                if out is None:
                    rejects += MAX_RESAMPLE
                    continue
                I, comms, sc, attempts = out
                rejects += attempts
                sc_vectors.extend(sc)

                for a in range(NUM_C):
                    for b in range(a + 1, NUM_C):
                        cc = run_coalescence(sc[a], sc[b], I, gamma=GAMMA)
                        if cc is None:
                            coalescence_failures += 1
                            continue
                        cc_vectors.append(cc)
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
            sc_summary = summarize_abundances(sc_vectors)
            cc_summary = summarize_abundances(cc_vectors)

            results[key] = {
                'mu': mu,
                'f_tail': f_tail,
                'gamma': GAMMA,
                'frac_alpha_negative_expected': frac_negative_for_tail(f_tail),
                'n_pools_requested': N_POOLS,
                'n_events': n_out,
                'rejects': rejects,
                'coalescence_failures': coalescence_failures,
                **{f'frac_{lab}': v for lab, v in fracs.items()},
                'psc_phi': psc,
                'assembled': sc_summary,
                'coalesced': cc_summary,
            }

            print(f'  events={n_out}, rejects={rejects}, '
                  f'coal_fail={coalescence_failures}, '
                  f'Dom={fracs["Dominance"]:.2f}, '
                  f'Mix={fracs["Mixture"]:.2f}, '
                  f'Res={fracs["Restructuring"]:.2f}, '
                  f'|phi|={psc:.2f}, '
                  f'cc_rich={cc_summary["mean_richness"]:.1f}',
                  flush=True)
            write_checkpoint()

    elapsed = time.time() - t0
    print(f'\nTotal elapsed: {elapsed/60:.1f} min')

    write_checkpoint()
    print(f'Saved {OUT_PATH}')


if __name__ == '__main__':
    run()
