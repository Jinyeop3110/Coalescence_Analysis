"""
simulate_Q5_phase_diagrams.py
=============================

Companion to simulate_Q5_all_models.py: run the three models (gLV,
pH-feedback, pH+LV hybrid) at three matched interaction-strength levels
and dump per-event (sim_a, sim_b, class) rows so we can render
Response-Fig-R3-2.0-style phase-diagram figures (scatter in the
Sim(A,C)-Sim(B,C) plane + adjacent stacked-bar panel).

Output
------
Q5_phase_events.csv with columns:
    model      : "gLV" | "pH" | "hybrid"
    strength   : "weak" | "mid" | "strong"
    pool       : int
    parent_i   : int
    parent_j   : int
    mu         : float  (0 for pH-only)
    tau        : float  (0 for gLV)
    sim_a      : float  = <n_A, n_C> / (|n_A| |n_C|)   (L2/cosine)
    sim_b      : float  = <n_B, n_C> / (|n_B| |n_C|)
    pdi        : float  = u / (u + v) from common_setup decomposition
    outcome    : "Dominance" | "Mixture" | "Restructuring"
    phi        : float  origin-to-persistence |phi| for the event

Run:
    cd Figure_generate/code/Figure_revision/Q5_pH_feedback_model
    python simulate_Q5_phase_diagrams.py
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
import pH_plus_LV_model as hybmod
from simulate_Q5_all_models import (
    N_POOL, SP_PER_C, NUM_C, N_POOLS, SEED,
    P_PREF_MODE, SIGMA_RANGE, LINK_C,
    sample_gLV_alpha, _gLV_integrate,
)

# Matched strength levels (diagonal through the grid)
STRENGTH_LEVELS = [
    ("weak",   0.3, 1.0),
    ("mid",    0.6, 10.0),
    ("strong", 0.9, 300.0),
]


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """L2/cosine similarity; returns 0 if either vector is all-zero."""
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def record_event(rows, model, strength, pool, i, j, mu, tau, nA, nB, nC):
    valid = (
        np.any(nA > phmod.EXTINCTION)
        and np.any(nB > phmod.EXTINCTION)
        and np.any(nC > phmod.EXTINCTION)
    )
    if not valid:
        return False
    cls, pdi, u, v, k = phmod.classify_coalescence(nA, nB, nC)
    phi = phmod.selection_phi(nA, nB, nC)
    rows.append({
        "model": model, "strength": strength,
        "pool": pool, "parent_i": i, "parent_j": j,
        "mu": mu, "tau": tau,
        "sim_a": cosine_sim(nA, nC),
        "sim_b": cosine_sim(nB, nC),
        "pdi": pdi,
        "outcome": cls,
        "phi": phi if np.isfinite(phi) else "",
    })
    return True


# ------------------------------------------------------------------
# gLV runs
# ------------------------------------------------------------------
def run_gLV(strength_name, mu, rng, rows):
    for pool_idx in range(N_POOLS):
        A = sample_gLV_alpha(N_POOL, mu, rng)
        perm = rng.permutation(N_POOL)
        masks = np.zeros((NUM_C, N_POOL), dtype=bool)
        parents = []
        ok = True
        for c in range(NUM_C):
            masks[c, perm[c * SP_PER_C:(c + 1) * SP_PER_C]] = True
            idx = np.where(masks[c])[0]
            n0 = rng.uniform(0.025, 0.075, size=len(idx))
            A_sub = A[np.ix_(idx, idx)]
            nss_sub = _gLV_integrate(A_sub, n0)
            if nss_sub is None:
                ok = False
                break
            nss = np.zeros(N_POOL)
            nss[idx] = nss_sub
            parents.append(nss)
        if not ok:
            continue
        for i in range(NUM_C):
            for j in range(i + 1, NUM_C):
                mix = 0.5 * (parents[i] + parents[j])
                mask = mix > phmod.EXTINCTION
                if mask.sum() == 0:
                    continue
                idx = np.where(mask)[0]
                A_sub = A[np.ix_(idx, idx)]
                nC_sub = _gLV_integrate(A_sub, mix[mask])
                if nC_sub is None:
                    continue
                nC = np.zeros(N_POOL)
                nC[idx] = nC_sub
                record_event(rows, "gLV", strength_name, pool_idx, i, j,
                             mu, 0.0, parents[i], parents[j], nC)


# ------------------------------------------------------------------
# pH-feedback runs
# ------------------------------------------------------------------
def run_pH(strength_name, tau, rng, rows):
    for pool_idx in range(N_POOLS):
        pool = phmod.sample_species_pool(
            N_POOL, rng,
            c_mag=phmod.DEFAULT_C_MAG * tau,
            p_pref_mode=P_PREF_MODE,
            sigma_range=SIGMA_RANGE,
            link_c_to_p_pref=LINK_C,
        )
        res = phmod.assemble_pool(pool, NUM_C, SP_PER_C, rng, return_pH=True)
        if res is None:
            continue
        masks, parents, parent_pHs = res
        for i in range(NUM_C):
            for j in range(i + 1, NUM_C):
                p_mix = 0.5 * (parent_pHs[i] + parent_pHs[j])
                nC = phmod.run_coalescence(pool, parents[i], parents[j], p0=p_mix)
                if nC is None:
                    continue
                record_event(rows, "pH", strength_name, pool_idx, i, j,
                             0.0, tau, parents[i], parents[j], nC)


# ------------------------------------------------------------------
# pH+LV hybrid runs
# ------------------------------------------------------------------
def run_hybrid(strength_name, mu, tau, rng, rows):
    for pool_idx in range(N_POOLS):
        pool = hybmod.sample_hybrid_pool(
            N_POOL, mu=mu, rng=rng,
            c_mag=phmod.DEFAULT_C_MAG * tau,
            p_pref_mode=P_PREF_MODE,
            sigma_range=SIGMA_RANGE,
            link_c_to_p_pref=LINK_C,
        )
        res = hybmod.assemble_pool(pool, NUM_C, SP_PER_C, rng, return_pH=True)
        if res is None:
            continue
        masks, parents, parent_pHs = res
        for i in range(NUM_C):
            for j in range(i + 1, NUM_C):
                p_mix = 0.5 * (parent_pHs[i] + parent_pHs[j])
                nC = hybmod.run_coalescence(pool, parents[i], parents[j], p0=p_mix)
                if nC is None:
                    continue
                record_event(rows, "hybrid", strength_name, pool_idx, i, j,
                             mu, tau, parents[i], parents[j], nC)


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    rows = []
    for sname, mu, tau in STRENGTH_LEVELS:
        print(f"[Q5-phase]  running strength={sname}  mu={mu}  tau={tau}")
        run_gLV(sname, mu, rng, rows)
        run_pH(sname, tau, rng, rows)
        run_hybrid(sname, mu, tau, rng, rows)

    out_path = os.path.join(HERE, "Q5_phase_events.csv")
    fieldnames = ["model", "strength", "pool", "parent_i", "parent_j",
                  "mu", "tau", "sim_a", "sim_b", "pdi", "outcome", "phi"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"[Q5-phase]  wrote {len(rows)} rows to {out_path}")
    print(f"[Q5-phase]  total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
