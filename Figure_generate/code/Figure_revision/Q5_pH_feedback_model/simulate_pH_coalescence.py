"""
simulate_pH_coalescence.py
==========================

Thin driver around pH_feedback_model.py. Runs a small sweep of the
pH-tension knob (analogue of mu in the pairwise gLV simulator) and
writes pH_feedback_results.json with the same schema as
R3_3_nonCompetitive_gLV/non_competitive_results.json so downstream
memo plotting code works unchanged.

Output JSON structure:
  {
    "parameters": { ...species / pool settings... },
    "results": {
      "tension=0.50_pH_feedback": { regime, pH_tension, n_events,
                                    rejects, frac_Dominance,
                                    frac_Mixture, frac_Restructuring,
                                    psc_phi },
      ...
    }
  }
"""

import os
import json
import time
import numpy as np

from pH_feedback_model import (
    DEFAULT_SIGMA, DEFAULT_DELTA, DEFAULT_C_MAG, DEFAULT_B, DEFAULT_K,
    DEFAULT_P0, T_END,
    sample_species_pool, scale_interaction_strength, assemble_pool,
    run_coalescence, classify_coalescence, selection_phi,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- Sweep parameters --------------------------------------------------
# 3 tension levels bracketing the canonical c_mag = 0.1. The exact
# numerical mapping to mu in the pairwise gLV is NOT 1-to-1; the point of
# this sweep is to produce an analogous low/mid/high interaction regime
# in a pH-feedback model. Comparison against mu is a downstream memo job.
PH_TENSION_VALUES = [0.5, 1.0, 1.5]

# Species pool and partitioning. Matches the paper's 12-isolate setup:
# N_POOL = 24 species, split into NUM_C=2 communities of SP_PER_C=12.
# (The gLV simulator uses 48/4/12; we use 24/2/12 because each ODE here
# is more expensive and 12 species per parent is what the experiment has.)
N_POOL   = 24
SP_PER_C = 12
NUM_C    = 2
N_POOLS  = 40    # 40 pools * 1 coalescence/pool = 40 events per tension
MAX_POOL_RETRIES = 5

# Species-parameter sampling ranges (see docstring of sample_species_pool).
# link_c_to_p_pref=True ties acidifier/alkalinizer sign to pH optimum,
# matching the Ratzke 2018 "species modify pH toward their optimum"
# reading. Setting False recovers pure random sign assignment.
P_PREF_RANGE      = (2.0, 8.0)
SIGMA_RANGE       = (2.0, 5.0)
LINK_C_TO_P_PREF  = True

# Initial proton concentration (neutral mid-range, same as Ratzke 2018).
P0 = DEFAULT_P0


def run():
    t_start = time.time()
    rng_master = np.random.default_rng(20260422)

    results = {}
    for tension in PH_TENSION_VALUES:
        key = f"tension={tension:.2f}_pH_feedback"
        print(f"\n[{key}] {N_POOLS} pools x {NUM_C*(NUM_C-1)//2} events each")
        outcomes = {"Dominance": 0, "Mixture": 0, "Restructuring": 0}
        phis = []
        rejects = 0

        for pool_idx in range(N_POOLS):
            sub_seed = int(rng_master.integers(1 << 31))
            sub_rng = np.random.default_rng(sub_seed)

            # Fresh species draw per pool so the pH_pref landscape varies.
            base_pool = sample_species_pool(
                N_POOL, sub_rng,
                c_mag=DEFAULT_C_MAG,
                p_pref_range=P_PREF_RANGE,
                sigma_range=SIGMA_RANGE,
                link_c_to_p_pref=LINK_C_TO_P_PREF,
            )
            pool = scale_interaction_strength(base_pool, tension)

            # Try to assemble; retry on ODE failure with new inits.
            asm = None
            for _retry in range(MAX_POOL_RETRIES):
                asm = assemble_pool(
                    pool, num_C=NUM_C, sp_per_C=SP_PER_C,
                    rng=sub_rng, p0=P0, t_end=T_END,
                )
                if asm is not None:
                    break
                rejects += 1
            if asm is None:
                continue

            masks, sc = asm

            # Run all NUM_C * (NUM_C-1) / 2 coalescence events in this pool.
            for a in range(NUM_C):
                for b in range(a + 1, NUM_C):
                    n_C = run_coalescence(pool, sc[a], sc[b],
                                          p0=P0, t_end=T_END)
                    if n_C is None:
                        rejects += 1
                        continue
                    label, pdi, u, v, k = classify_coalescence(
                        sc[a], sc[b], n_C)
                    outcomes[label] += 1
                    phi = selection_phi(sc[a], sc[b], n_C)
                    if np.isfinite(phi):
                        phis.append(phi)

        n_total = sum(outcomes.values())
        fracs = {lab: (cnt / n_total if n_total else 0.0)
                 for lab, cnt in outcomes.items()}
        psc_phi = float(np.mean(phis)) if phis else float("nan")

        results[key] = {
            "regime": "pH_feedback",
            "pH_tension": float(tension),
            "n_events": int(n_total),
            "rejects": int(rejects),
            "frac_Dominance":    float(fracs["Dominance"]),
            "frac_Mixture":      float(fracs["Mixture"]),
            "frac_Restructuring": float(fracs["Restructuring"]),
            "psc_phi": psc_phi,
        }
        print(f"  events={n_total}, rejects={rejects}, "
              f"Dom={fracs['Dominance']:.2f}, "
              f"Mix={fracs['Mixture']:.2f}, "
              f"Res={fracs['Restructuring']:.2f}, "
              f"|phi|={psc_phi:.2f}")

    elapsed = time.time() - t_start
    print(f"\nTotal elapsed: {elapsed/60:.1f} min")

    out_path = os.path.join(SCRIPT_DIR, "pH_feedback_results.json")
    payload = {
        "parameters": {
            "PH_TENSION_VALUES": PH_TENSION_VALUES,
            "N_POOL": N_POOL, "SP_PER_C": SP_PER_C, "NUM_C": NUM_C,
            "N_POOLS": N_POOLS,
            "P_PREF_RANGE": list(P_PREF_RANGE),
            "SIGMA_RANGE":  list(SIGMA_RANGE),
            "LINK_C_TO_P_PREF": LINK_C_TO_P_PREF,
            "DEFAULT_C_MAG":  DEFAULT_C_MAG,
            "DEFAULT_SIGMA":  DEFAULT_SIGMA,
            "DEFAULT_DELTA":  DEFAULT_DELTA,
            "DEFAULT_B":      DEFAULT_B,
            "DEFAULT_K":      DEFAULT_K,
            "P0":             P0,
            "T_END":          T_END,
            "REFERENCE_SOURCES": [
                "Ratzke & Gore 2018 PLOS Biol 16:e2004248 (Eqs 1-2)",
                "Ratzke, Barrere, Gore 2020 Nat Ecol Evol 4:376 "
                "(nutrient -> |c| -> interaction strength)",
                "Ratzke, Denk, Gore 2018 Nat Ecol Evol 2:867 (single-species ODE)",
            ],
        },
        "results": results,
    }
    with open(out_path, "w") as fh:
        json.dump(payload, fh, indent=2)
    print(f"Saved {out_path}")


if __name__ == "__main__":
    run()
