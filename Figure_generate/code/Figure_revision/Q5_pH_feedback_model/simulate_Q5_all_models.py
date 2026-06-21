"""
simulate_Q5_all_models.py
=========================

Run all three Q5 models on a common knob sweep and write a single
comparison JSON.  Dominance fraction is the PRIMARY metric (the paper's
headline result is Dominance rising with nutrient/interaction strength);
|phi| is reported as a secondary.

Models
------
1. gLV baseline (imported from R3_3_nonCompetitive_gLV/simulate_non_competitive.py).
   Knob: mu. No pH dynamics. This is the paper's main model.
2. pH-feedback (Ratzke & Gore 2018), from pH_feedback_model.py.
   Knob: pH_tension (|c|). No alpha_{ij} beyond self-regulation.
3. pH+LV hybrid, from pH_plus_LV_model.py.
   Knobs: mu AND pH_tension, independently.

All three use bimodal p_pref (matching R1-2 experimental isolate
distribution) and narrower sigma for a fair, biologically-plausible
comparison focused on the Dominance axis.

Output: Q5_all_models_results.json, same schema as the pH-only JSON.

Run:
    cd Figure_generate/code/Figure_revision/Q5_pH_feedback_model
    python simulate_Q5_all_models.py
"""

from __future__ import annotations

import json
import os
import sys
import time
import numpy as np

# ensure common_setup is importable from here
HERE = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import pH_feedback_model as phmod
import pH_plus_LV_model as hybmod


# --------------------------------------------------------------------------
# Shared config
# --------------------------------------------------------------------------
SEED          = 42
N_POOL        = 24
SP_PER_C      = 12
NUM_C         = 2
N_POOLS       = 100
P_PREF_MODE   = "uniform"     # public Ratzke code: po ~ U(4.5, 9.5)
SIGMA_RANGE   = (phmod.DEFAULT_PC, phmod.DEFAULT_PC)  # public code: pc = 2.5
LINK_C        = False         # public code: cp ~ U(-interaction_strength, +interaction_strength)

# Pure pH-feedback uses the original public-code interaction_strength grid.
# In pH_feedback_model.py DEFAULT_C_MAG = 1e-10, so tau is simply
# interaction_strength / 1e-10.
MU_VALUES     = [0.1, 0.3, 0.6, 0.9]
PH_INTERACTION_STRENGTHS = [0.0, 1e-10, 1e-9, 1e-8, 1e-6, 1e-5, 1e-4, 1e-2]
PH_TENSIONS   = [s / phmod.DEFAULT_C_MAG for s in PH_INTERACTION_STRENGTHS]

# Hybrid grid: 2-D (mu, pH_tension)
HYBRID_MU     = [0.1, 0.3, 0.6, 0.9]
HYBRID_PH     = [0.0, 0.5, 2.0, 5.0]


# --------------------------------------------------------------------------
# A minimal gLV baseline (no pH) matching R3_3 comp-regime but using the
# same event-generation structure as the pH models so numbers are directly
# comparable.  We do not re-import the R3_3 script because that script is
# not factored into functions; the equivalent self-contained implementation
# lives here and is only a few lines.
# --------------------------------------------------------------------------
from scipy.integrate import solve_ivp


def sample_gLV_alpha(N, mu, rng):
    A = rng.uniform(0.0, 2.0 * mu, size=(N, N))
    np.fill_diagonal(A, 1.0)
    return A


def _gLV_rhs(t, n, A, K):
    n = np.maximum(n, 0.0)
    return n * (1.0 - (A @ n) / K)


def _gLV_integrate(A, n0, K=1.0, t_end=phmod.T_END):
    sol = solve_ivp(
        lambda t, y: _gLV_rhs(t, y, A, K),
        (0.0, t_end), n0,
        method="RK45", t_eval=[t_end],
        rtol=phmod.RTOL, atol=phmod.ATOL,
    )
    if not sol.success:
        return None
    n = np.asarray(sol.y)[:, -1]
    if not np.all(np.isfinite(n)):
        return None
    n = np.where(n < 0, 0.0, n)
    if np.any(n > phmod.BLOWUP_CAP):
        return None
    n = np.where(n < phmod.EXTINCTION, 0.0, n)
    return n


def gLV_assemble_and_coalesce(N, mu, num_C, sp_per_C, rng):
    A = sample_gLV_alpha(N, mu, rng)
    perm = rng.permutation(N)
    masks = np.zeros((num_C, N), dtype=bool)
    parents = []
    for c in range(num_C):
        masks[c, perm[c * sp_per_C:(c + 1) * sp_per_C]] = True
        idx = np.where(masks[c])[0]
        n0 = rng.uniform(0.025, 0.075, size=len(idx))
        A_sub = A[np.ix_(idx, idx)]
        n_ss_sub = _gLV_integrate(A_sub, n0)
        if n_ss_sub is None:
            return None
        n_ss = np.zeros(N)
        n_ss[idx] = n_ss_sub
        parents.append(n_ss)
    # coalesce all pairs
    events = []
    for i in range(num_C):
        for j in range(i + 1, num_C):
            mix = 0.5 * (parents[i] + parents[j])
            m = mix > phmod.EXTINCTION
            if m.sum() == 0:
                continue
            idx = np.where(m)[0]
            A_sub = A[np.ix_(idx, idx)]
            n_ss_sub = _gLV_integrate(A_sub, mix[m])
            if n_ss_sub is None:
                continue
            n_C = np.zeros(N)
            n_C[idx] = n_ss_sub
            events.append((parents[i], parents[j], n_C))
    return events


# --------------------------------------------------------------------------
# Per-regime runner: gLV (pure)
# --------------------------------------------------------------------------
def run_gLV(mu, rng):
    labels = {"Dominance": 0, "Mixture": 0, "Restructuring": 0}
    phis = []
    rejects = 0
    n_events = 0
    for _ in range(N_POOLS):
        out = gLV_assemble_and_coalesce(N_POOL, mu, NUM_C, SP_PER_C, rng)
        if out is None:
            rejects += 1
            continue
        for (nA, nB, nC) in out:
            cls, pdi, u, v, k = phmod.classify_coalescence(nA, nB, nC)
            labels[cls] = labels.get(cls, 0) + 1
            phi = phmod.selection_phi(nA, nB, nC)
            if np.isfinite(phi):
                phis.append(phi)
            n_events += 1
    total = sum(labels.values())
    return {
        "regime": "gLV",
        "mu": float(mu),
        "pH_tension": 0.0,
        "n_events": n_events,
        "rejects": rejects,
        "frac_Dominance": labels["Dominance"] / total if total else float("nan"),
        "frac_Mixture":   labels["Mixture"]   / total if total else float("nan"),
        "frac_Restructuring": labels["Restructuring"] / total if total else float("nan"),
        "psc_phi": float(np.mean(phis)) if phis else float("nan"),
    }


# --------------------------------------------------------------------------
# Per-regime runner: pH-feedback (pure)
# --------------------------------------------------------------------------
def run_pH(pH_tension, rng):
    labels = {"Dominance": 0, "Mixture": 0, "Restructuring": 0}
    phis = []
    rejects = 0
    invalid_degenerate = 0
    n_events = 0
    for _ in range(N_POOLS):
        pool = phmod.sample_species_pool(
            N_POOL, rng,
            c_mag=phmod.DEFAULT_C_MAG * pH_tension,
            p_pref_mode=P_PREF_MODE,
            sigma_range=SIGMA_RANGE,
            link_c_to_p_pref=LINK_C,
        )
        res = phmod.assemble_pool(pool, NUM_C, SP_PER_C, rng, return_pH=True)
        if res is None:
            rejects += 1
            continue
        masks, parents, parent_pHs = res
        for i in range(NUM_C):
            for j in range(i + 1, NUM_C):
                nA, nB = parents[i], parents[j]
                # inherit an averaged environment instead of resetting to p0
                p_mix = 0.5 * (parent_pHs[i] + parent_pHs[j])
                nC = phmod.run_coalescence(pool, nA, nB, p0=p_mix)
                if nC is None:
                    continue
                valid = (
                    np.any(nA > phmod.EXTINCTION)
                    and np.any(nB > phmod.EXTINCTION)
                    and np.any(nC > phmod.EXTINCTION)
                )
                if not valid:
                    invalid_degenerate += 1
                    continue
                cls, pdi, u, v, k = phmod.classify_coalescence(nA, nB, nC)
                labels[cls] = labels.get(cls, 0) + 1
                phi = phmod.selection_phi(nA, nB, nC)
                if np.isfinite(phi):
                    phis.append(phi)
                n_events += 1
    total = sum(labels.values())
    return {
        "regime": "pH_feedback",
        "mu": 0.0,
        "pH_tension": float(pH_tension),
        "n_events": n_events,
        "rejects": rejects,
        "invalid_degenerate": invalid_degenerate,
        "frac_Dominance": labels["Dominance"] / total if total else float("nan"),
        "frac_Mixture":   labels["Mixture"]   / total if total else float("nan"),
        "frac_Restructuring": labels["Restructuring"] / total if total else float("nan"),
        "psc_phi": float(np.mean(phis)) if phis else float("nan"),
    }


# --------------------------------------------------------------------------
# Per-regime runner: pH+LV hybrid
# --------------------------------------------------------------------------
def run_hybrid(mu, pH_tension, rng):
    labels = {"Dominance": 0, "Mixture": 0, "Restructuring": 0}
    phis = []
    rejects = 0
    n_events = 0
    for _ in range(N_POOLS):
        pool = hybmod.sample_hybrid_pool(
            N_POOL, mu=mu, rng=rng,
            c_mag=phmod.DEFAULT_C_MAG * pH_tension,
            p_pref_mode=P_PREF_MODE,
            sigma_range=SIGMA_RANGE,
            link_c_to_p_pref=LINK_C,
        )
        res = hybmod.assemble_pool(pool, NUM_C, SP_PER_C, rng, return_pH=True)
        if res is None:
            rejects += 1
            continue
        masks, parents, parent_pHs = res
        for i in range(NUM_C):
            for j in range(i + 1, NUM_C):
                nA, nB = parents[i], parents[j]
                p_mix = 0.5 * (parent_pHs[i] + parent_pHs[j])
                nC = hybmod.run_coalescence(pool, nA, nB, p0=p_mix)
                if nC is None:
                    continue
                cls, pdi, u, v, k = phmod.classify_coalescence(nA, nB, nC)
                labels[cls] = labels.get(cls, 0) + 1
                phi = phmod.selection_phi(nA, nB, nC)
                if np.isfinite(phi):
                    phis.append(phi)
                n_events += 1
    total = sum(labels.values())
    return {
        "regime": "pH_plus_LV",
        "mu": float(mu),
        "pH_tension": float(pH_tension),
        "n_events": n_events,
        "rejects": rejects,
        "frac_Dominance": labels["Dominance"] / total if total else float("nan"),
        "frac_Mixture":   labels["Mixture"]   / total if total else float("nan"),
        "frac_Restructuring": labels["Restructuring"] / total if total else float("nan"),
        "psc_phi": float(np.mean(phis)) if phis else float("nan"),
    }


# --------------------------------------------------------------------------
# Main driver
# --------------------------------------------------------------------------
def main():
    rng = np.random.default_rng(SEED)
    t0 = time.time()
    results = {}

    print(f"[Q5] Shared config: N_POOL={N_POOL}, SP_PER_C={SP_PER_C}, "
          f"NUM_C={NUM_C}, N_POOLS={N_POOLS}, p_pref_mode={P_PREF_MODE}, "
          f"sigma_range={SIGMA_RANGE}, link_c={LINK_C}")

    # 1) gLV sweep over mu
    print("\n[Q5] gLV baseline (mu sweep)")
    for mu in MU_VALUES:
        key = f"gLV_mu={mu:.2f}"
        rec = run_gLV(mu, rng)
        results[key] = rec
        print(f"  {key}  n={rec['n_events']:4d}  "
              f"Dom={rec['frac_Dominance']:.3f}  "
              f"Mix={rec['frac_Mixture']:.3f}  "
              f"Res={rec['frac_Restructuring']:.3f}  "
              f"|phi|={rec['psc_phi']:.3f}")

    # 2) pH-feedback sweep over pH_tension
    print("\n[Q5] pH-feedback (pH_tension sweep)")
    for tau in PH_TENSIONS:
        key = f"pH_tau={tau:.2f}"
        rec = run_pH(tau, rng)
        results[key] = rec
        print(f"  {key}  n={rec['n_events']:4d}  "
              f"Dom={rec['frac_Dominance']:.3f}  "
              f"Mix={rec['frac_Mixture']:.3f}  "
              f"Res={rec['frac_Restructuring']:.3f}  "
              f"|phi|={rec['psc_phi']:.3f}")

    # 3) Hybrid grid (mu x pH_tension)
    print("\n[Q5] pH+LV hybrid (mu x pH_tension grid)")
    for mu in HYBRID_MU:
        for tau in HYBRID_PH:
            key = f"hybrid_mu={mu:.2f}_tau={tau:.2f}"
            rec = run_hybrid(mu, tau, rng)
            results[key] = rec
            print(f"  {key}  n={rec['n_events']:4d}  "
                  f"Dom={rec['frac_Dominance']:.3f}  "
                  f"Mix={rec['frac_Mixture']:.3f}  "
                  f"Res={rec['frac_Restructuring']:.3f}  "
                  f"|phi|={rec['psc_phi']:.3f}")

    payload = {
        "parameters": {
            "SEED": SEED,
            "N_POOL": N_POOL,
            "SP_PER_C": SP_PER_C,
            "NUM_C": NUM_C,
            "N_POOLS": N_POOLS,
            "MU_VALUES": MU_VALUES,
            "PH_TENSIONS": PH_TENSIONS,
            "HYBRID_MU": HYBRID_MU,
            "HYBRID_PH": HYBRID_PH,
            "P_PREF_MODE": P_PREF_MODE,
            "SIGMA_RANGE": list(SIGMA_RANGE),
            "LINK_C_TO_P_PREF": LINK_C,
            "DEFAULT_C_MAG": phmod.DEFAULT_C_MAG,
            "DEFAULT_SIGMA": phmod.DEFAULT_SIGMA,
            "DEFAULT_DELTA": phmod.DEFAULT_DELTA,
            "DEFAULT_B": phmod.DEFAULT_B,
            "DEFAULT_K": phmod.DEFAULT_K,
            "P0": phmod.DEFAULT_P0,
            "T_END": phmod.T_END,
        },
        "results": results,
    }
    out_path = os.path.join(HERE, "Q5_all_models_results.json")
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\n[Q5] wrote {out_path}")
    print(f"[Q5] total runtime: {time.time() - t0:.1f} s")
    return payload


if __name__ == "__main__":
    main()
