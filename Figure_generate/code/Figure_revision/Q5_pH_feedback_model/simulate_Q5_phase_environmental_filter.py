"""
simulate_Q5_phase_environmental_filter.py
=========================================

Generate per-event records for the trait-based environmental-filtering null
model. The output schema matches Q5_phase_events.csv so the result can be
rendered in the same style as Fig. Q5-pH.

Output:
    Q5_phase_events_filter.csv
"""

from __future__ import annotations

import csv
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

import environmental_filter_model as filt
import pH_feedback_model as phmod


SEED = 42
N_POOL = 24
SP_PER_C = 12
NUM_C = 2
N_POOLS = 500


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def richness(x: np.ndarray) -> int:
    return int(np.sum(np.asarray(x) > phmod.EXTINCTION))


def record_event(rows, params, pool_idx, parent_i, parent_j, nA, nB, nC):
    valid = (
        np.any(nA > phmod.EXTINCTION)
        and np.any(nB > phmod.EXTINCTION)
        and np.any(nC > phmod.EXTINCTION)
    )
    if not valid:
        return False

    cls, pdi, u, v, k = filt.classify_coalescence(nA, nB, nC)
    phi = filt.selection_phi(nA, nB, nC)
    rows.append({
        "model": "filter",
        "strength": params.name,
        "pool": pool_idx,
        "parent_i": parent_i,
        "parent_j": parent_j,
        "mu": 0.0,
        "tau": params.gamma,
        "theta": params.theta,
        "sigma": params.sigma,
        "gamma": params.gamma,
        "threshold": params.threshold,
        "sim_a": cosine_sim(nA, nC),
        "sim_b": cosine_sim(nB, nC),
        "pdi": pdi,
        "outcome": cls,
        "phi": phi if np.isfinite(phi) else "",
        "richness_a": richness(nA),
        "richness_b": richness(nB),
        "richness_c": richness(nC),
    })
    return True


def run_level(params, rng, rows):
    n_valid = 0
    for pool_idx in range(N_POOLS):
        pool = filt.sample_trait_pool(N_POOL, rng)
        _, parents = filt.assemble_pool(pool, params, NUM_C, SP_PER_C, rng)
        for i in range(NUM_C):
            for j in range(i + 1, NUM_C):
                nC = filt.run_coalescence(pool, params, parents[i], parents[j])
                if record_event(rows, params, pool_idx, i, j, parents[i], parents[j], nC):
                    n_valid += 1
    return n_valid


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    rows = []
    for params in filt.DEFAULT_FILTER_LEVELS:
        print(
            f"[Q5-filter] strength={params.name} "
            f"theta={params.theta} sigma={params.sigma} "
            f"gamma={params.gamma} threshold={params.threshold}"
        )
        n_valid = run_level(params, rng, rows)
        print(f"  valid events: {n_valid}")

    out_path = os.path.join(HERE, "Q5_phase_events_filter.csv")
    fieldnames = [
        "model", "strength", "pool", "parent_i", "parent_j",
        "mu", "tau", "theta", "sigma", "gamma", "threshold",
        "sim_a", "sim_b", "pdi", "outcome", "phi",
        "richness_a", "richness_b", "richness_c",
    ]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[Q5-filter] wrote {len(rows)} rows to {out_path}")
    print(f"[Q5-filter] runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
