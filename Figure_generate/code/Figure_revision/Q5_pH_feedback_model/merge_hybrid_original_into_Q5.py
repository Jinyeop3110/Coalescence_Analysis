"""
merge_hybrid_original_into_Q5.py
================================

Take the original-form hybrid results (hybrid_original_results.json) and
inject them into the shared Q5 results JSON under new keys, so the
summary figure (make_Q5_comparison_figure.py) can render "hybrid" as the
original-form variant instead of the Ratzke-based one.

We keep the old `hybrid_mu=*_tau=*` keys in place for historical
comparison; they are simply no longer referenced by the summary figure.

New keys written:
    hybrid_orig_binary_tau=0.30
    hybrid_orig_binary_tau=0.60
    hybrid_orig_binary_tau=1.00
(and the analogous continuous ones for completeness)

Field mapping from hybrid_original_results.json summary to Q5 schema:
    frac_Dominance       <- dom_frac
    frac_Mixture         <- mix_frac
    frac_Restructuring   <- res_frac
    psc_phi              <- phi_mean
    n_events             <- n_events
    rejects              <- n_blowup + n_degenerate
    regime               <- "hybrid_original_<mode>"
    alpha                <- 0.30
    tau                  <- tau
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "hybrid_original_results.json")
DST = os.path.join(HERE, "Q5_all_models_results.json")


def to_q5(s):
    return {
        "regime": f"hybrid_original_{s['mode']}",
        "alpha": s["alpha"],
        "tau": s["tau"],
        "n_events": s["n_events"],
        "rejects": s["n_blowup"] + s["n_degenerate"],
        "frac_Dominance": s["dom_frac"],
        "frac_Mixture": s["mix_frac"],
        "frac_Restructuring": s["res_frac"],
        "psc_phi": s["phi_mean"],
    }


def main():
    with open(SRC) as f:
        src = json.load(f)
    with open(DST) as f:
        dst = json.load(f)

    added = []
    for key, rec in src["runs"].items():
        # key looks like "binary_tau=0.30" or "continuous_tau=1.00"
        mode, tau_part = key.split("_tau=")
        tau = float(tau_part)
        new_key = f"hybrid_orig_{mode}_tau={tau:.2f}"
        dst["results"][new_key] = to_q5(rec["summary"])
        added.append(new_key)

    with open(DST, "w") as f:
        json.dump(dst, f, indent=2)
    print(f"Merged {len(added)} keys into {DST}")
    for k in sorted(added):
        r = dst["results"][k]
        print(f"  {k}: Dom={r['frac_Dominance']:.2f}  |phi|={r['psc_phi']:.2f}  n={r['n_events']}  rej={r['rejects']}")


if __name__ == "__main__":
    main()
