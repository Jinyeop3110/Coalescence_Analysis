"""
simulate_Q5_phase_hybrid_original.py
====================================

Produce per-event (sim_a, sim_b, outcome, phi) records for the
original-form hybrid (gLV_pH_set1 port) at three matched
interaction-strength levels, for BOTH preference modes (continuous and
binary).  Same CSV schema as Q5_phase_events.csv so that
make_Q5_phase_figures.py can render the same 4-panel layout as
Q5-gLV / Q5-pH.

Strength mapping (alpha = 0.3 fixed):
    weak   : tau = 0.3
    mid    : tau = 0.6
    strong : tau = 1.0

Output : Q5_phase_events_hybrid_orig.csv (same columns as Q5_phase_events.csv)
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

import pH_feedback_model as phmod
from hybrid_original_model import (
    sample_hybrid_pool, assemble_pool, run_coalescence, EXTINCTION,
)


# Match the sim geometry of Q5_all_models / Q5_phase for comparability.
ALPHA     = 0.3
N_POOL    = 24
SP_PER_C  = 12
NUM_C     = 2
N_POOLS   = 100   # same as simulate_hybrid_original.py (more than gLV/pH's 40)
SEED      = 42

STRENGTH_LEVELS = [
    ("weak",   0.3),
    ("mid",    0.6),
    ("strong", 1.0),
]
MODES = ["continuous", "binary"]


def cosine_sim(a, b):
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def record_event(rows, model, strength, pool, i, j, tau, nA, nB, nC):
    cls, pdi, u, v, k = phmod.classify_coalescence(nA, nB, nC)
    phi = phmod.selection_phi(nA, nB, nC)
    rows.append({
        "model": model, "strength": strength,
        "pool": pool, "parent_i": i, "parent_j": j,
        "mu": ALPHA, "tau": tau,
        "sim_a": cosine_sim(nA, nC),
        "sim_b": cosine_sim(nB, nC),
        "pdi": pdi,
        "outcome": cls,
        "phi": phi if np.isfinite(phi) else "",
    })


def run_one(model_label, mode, strength, tau, rng, rows):
    for pool_idx in range(N_POOLS):
        pool = sample_hybrid_pool(
            N_POOL, alpha=ALPHA, tension=tau, rng=rng, mode=mode,
        )
        res = assemble_pool(pool, NUM_C, SP_PER_C, rng, return_env=True)
        if res is None:
            continue
        _, parents, _ = res
        for i in range(NUM_C):
            for j in range(i + 1, NUM_C):
                nC = run_coalescence(pool, parents[i], parents[j])
                if nC is None:
                    continue
                record_event(rows, model_label, strength, pool_idx, i, j,
                             tau, parents[i], parents[j], nC)


def main():
    t0 = time.time()
    rows = []
    for mode in MODES:
        model_label = f"hybrid_orig_{mode}"
        rng = np.random.default_rng(hash((mode, SEED)) & 0xFFFFFFFF)
        for sname, tau in STRENGTH_LEVELS:
            print(f"[Q5-phase-hybrid-orig] mode={mode} strength={sname} tau={tau}")
            run_one(model_label, mode, sname, tau, rng, rows)

    out_path = os.path.join(HERE, "Q5_phase_events_hybrid_orig.csv")
    fieldnames = ["model", "strength", "pool", "parent_i", "parent_j",
                  "mu", "tau", "sim_a", "sim_b", "pdi", "outcome", "phi"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"[Q5-phase-hybrid-orig] wrote {len(rows)} rows to {out_path}")
    print(f"[Q5-phase-hybrid-orig] runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
