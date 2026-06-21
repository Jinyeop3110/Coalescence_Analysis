"""
simulate_hybrid_original.py
===========================

Run the original-hybrid (gLV_pH_set1 port) coalescence simulation.

Fixed:  alpha = 0.3.
Sweep:  tension in {0.0, 0.3, 0.6, 1.0} x mode in {continuous, binary}.
        100 pool seeds per cell; one coalescence event per pool (num_C=2).

Outputs:
    hybrid_original_results.json  — per-event records keyed by
        f"{mode}_tau={tau:.2f}" plus a summary block.

The classification is done with the same pipeline as every other Q5 /
R1-4 analysis: common_setup.metric_VectorDecomposition_onlyPositive →
calculate_assymetricity → characterize_case (0=Dom, 1=Mix, 2=Res).
|phi| is computed from pH_feedback_model.selection_phi for consistency.
"""
from __future__ import annotations

import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

_orig_cwd = os.getcwd()
os.chdir(CODE_DIR)
from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity, characterize_case,
)
os.chdir(_orig_cwd)

from hybrid_original_model import (
    sample_hybrid_pool, assemble_pool, run_coalescence, EXTINCTION,
)
from pH_feedback_model import selection_phi


# ---- Config ----------------------------------------------------------------
ALPHA       = 0.3
TENSIONS    = [0.0, 0.3, 0.6, 1.0]
MODES       = ["continuous", "binary"]
N_POOL      = 24
SP_PER_C    = 12
NUM_C       = 2
N_POOLS     = 100
SEED        = 42
OUTPUT      = os.path.join(HERE, "hybrid_original_results.json")


def run_cell(mode: str, tau: float, seed: int):
    rng = np.random.default_rng(seed)
    events = []
    n_blowup = 0
    n_degen = 0
    for rep in range(N_POOLS):
        pool = sample_hybrid_pool(
            N_POOL, alpha=ALPHA, tension=tau, rng=rng, mode=mode,
        )
        ret = assemble_pool(pool, NUM_C, SP_PER_C, rng, return_env=True)
        if ret is None:
            n_blowup += 1
            continue
        _, sc, envs = ret
        for i in range(NUM_C):
            for j in range(i + 1, NUM_C):
                n_c = run_coalescence(pool, sc[i], sc[j])
                if n_c is None:
                    n_blowup += 1
                    continue
                nA, nB = sc[i], sc[j]
                if (np.linalg.norm(nA) == 0 or
                        np.linalg.norm(nB) == 0 or
                        np.linalg.norm(n_c) == 0):
                    n_degen += 1
                    continue
                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(
                        nA, nB, n_c)
                except (np.linalg.LinAlgError, FloatingPointError,
                        ZeroDivisionError):
                    n_degen += 1
                    continue
                if (any(np.isnan([u, v, k])) or
                        any(np.isinf([u, v, k]))):
                    n_degen += 1
                    continue
                x_mag, y_asym = calculate_assymetricity(u, v, k)
                cls = characterize_case(x_mag, y_asym)
                if cls is None:
                    n_degen += 1
                    continue
                phi = selection_phi(nA, nB, n_c)
                events.append({
                    "rep": int(rep),
                    "pair": [int(i), int(j)],
                    "class": int(cls),
                    "phi": None if np.isnan(phi) else float(phi),
                    "env_A": float(envs[i]),
                    "env_B": float(envs[j]),
                    "surv_A": int(np.sum(nA > EXTINCTION)),
                    "surv_B": int(np.sum(nB > EXTINCTION)),
                    "surv_C": int(np.sum(n_c > EXTINCTION)),
                    "u": float(u),
                    "v": float(v),
                    "k": float(k),
                })

    n_ev = len(events)
    dom = sum(1 for e in events if e["class"] == 0)
    mix = sum(1 for e in events if e["class"] == 1)
    res = sum(1 for e in events if e["class"] == 2)
    phis = [e["phi"] for e in events if e["phi"] is not None]
    envs_A = [abs(e["env_A"]) for e in events]
    envs_B = [abs(e["env_B"]) for e in events]
    envs_all = envs_A + envs_B

    summary = {
        "mode": mode,
        "tau": tau,
        "alpha": ALPHA,
        "n_pools_requested": N_POOLS,
        "n_blowup": int(n_blowup),
        "n_degenerate": int(n_degen),
        "n_events": int(n_ev),
        "dom_frac": float(dom / n_ev) if n_ev else None,
        "mix_frac": float(mix / n_ev) if n_ev else None,
        "res_frac": float(res / n_ev) if n_ev else None,
        "phi_mean": float(np.mean(phis)) if phis else None,
        "phi_std": float(np.std(phis)) if phis else None,
        "phi_n": int(len(phis)),
        "env_abs_mean": float(np.mean(envs_all)) if envs_all else None,
    }
    return summary, events


def main():
    t0 = time.time()
    runs = {}
    for mode in MODES:
        for tau in TENSIONS:
            key = f"{mode}_tau={tau:.2f}"
            print(f"[{time.time()-t0:6.1f}s] running {key} ...", flush=True)
            seed = hash((mode, tau, SEED)) & 0xFFFFFFFF
            summary, events = run_cell(mode, tau, seed)
            runs[key] = {"summary": summary, "events": events}
            s = summary
            dom = s["dom_frac"]
            dom_s = f"{dom:.2f}" if dom is not None else "-"
            phim = s["phi_mean"]
            phim_s = f"{phim:.2f}" if phim is not None else "-"
            print(f"         n_ev={s['n_events']:>3d}  "
                  f"Dom={dom_s}  |phi|={phim_s}  "
                  f"blow={s['n_blowup']}  env={s['env_abs_mean']:.2f}"
                  if s['env_abs_mean'] is not None else
                  f"         n_ev={s['n_events']:>3d}  "
                  f"Dom={dom_s}  |phi|={phim_s}  "
                  f"blow={s['n_blowup']}")

    metadata = {
        "alpha": ALPHA,
        "tensions": TENSIONS,
        "modes": MODES,
        "N_pool": N_POOL,
        "sp_per_C": SP_PER_C,
        "num_C": NUM_C,
        "n_pools": N_POOLS,
        "seed_base": SEED,
    }
    with open(OUTPUT, "w") as f:
        json.dump({"metadata": metadata, "runs": runs}, f, indent=2)
    print(f"\nWrote {OUTPUT}  ({time.time()-t0:.1f}s total)")


if __name__ == "__main__":
    main()
