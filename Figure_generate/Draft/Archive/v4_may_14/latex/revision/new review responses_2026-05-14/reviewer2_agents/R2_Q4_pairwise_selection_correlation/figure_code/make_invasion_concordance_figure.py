#!/usr/bin/env python3
"""Generate an independent R2-Q4 response-support figure.

The analysis uses the archived gLV simulation dataset with full interaction
matrices. For each ordered pair of assembled communities, each surviving
species in the source community is treated as a rare invader into the target
community equilibrium. The per-capita invasion growth rate is

    lambda_i = g_i * (1 - sum_j alpha_ij x_j / k_i).

The script then asks whether species from the same source community have
concordant invasion outcomes more often than expected if each species invaded
independently with the observed success probability.
"""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


DEFAULT_DATA = Path(
    "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/"
    "Figure_generate/code/Simulation_Data/48species_10reps_fine_WITH_MATRICES/"
    "Community_10reps_fine_WITH_MATRICES.json"
)
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "figures"
THRESHOLD = 1e-3


def survivors(abundance):
    arr = np.asarray(abundance, dtype=float)
    return np.flatnonzero(arr > THRESHOLD)


def invasion_rates(source_indices, interaction_matrix, growth_rates, carrying_capacities, resident):
    rates = []
    resident = np.asarray(resident, dtype=float)
    for idx in source_indices:
        pressure = float(np.dot(interaction_matrix[idx, :], resident))
        rates.append(growth_rates[idx] * (1.0 - pressure / carrying_capacities[idx]))
    return np.asarray(rates, dtype=float)


def concordance_from_rates(rates):
    if len(rates) < 2:
        return np.nan
    signs = rates > 0
    pair_values = [signs[i] == signs[j] for i, j in combinations(range(len(signs)), 2)]
    return float(np.mean(pair_values))


def summarize(data_path):
    with data_path.open("r") as handle:
        dataset = json.load(handle)

    rows = []
    scatter_pairs = []
    for mu_key in sorted(dataset, key=float):
        per_pair_concordance = []
        per_pair_invade_fraction = []
        per_pair_count = 0

        for replicate in dataset[mu_key].values():
            communities = replicate["sc_list"]
            params = replicate["parameters"]
            alpha = np.asarray(params["interaction_matrix"], dtype=float)
            growth = np.asarray(params["growth_rates"], dtype=float)
            capacity = np.asarray(params["carrying_capacities"], dtype=float)

            community_ids = sorted(communities, key=int)
            for source_id in community_ids:
                source_survivors = survivors(communities[source_id])
                if len(source_survivors) < 2:
                    continue
                for target_id in community_ids:
                    if target_id == source_id:
                        continue
                    resident = np.asarray(communities[target_id], dtype=float)
                    if not np.any(resident > THRESHOLD):
                        continue

                    rates = invasion_rates(source_survivors, alpha, growth, capacity, resident)
                    concordance = concordance_from_rates(rates)
                    if np.isnan(concordance):
                        continue

                    per_pair_count += 1
                    per_pair_concordance.append(concordance)
                    per_pair_invade_fraction.append(float(np.mean(rates > 0)))

                    if mu_key == "0.50":
                        for i, j in combinations(range(len(rates)), 2):
                            scatter_pairs.append((float(rates[i]), float(rates[j])))

        mean_conc = float(np.mean(per_pair_concordance))
        sem_conc = float(stats.sem(per_pair_concordance))
        mean_p = float(np.mean(per_pair_invade_fraction))
        sem_p = float(stats.sem(per_pair_invade_fraction))
        independent_null = 1.0 - 2.0 * mean_p * (1.0 - mean_p)
        rows.append(
            {
                "mu": float(mu_key),
                "n_ordered_community_pairs": per_pair_count,
                "mean_concordance": mean_conc,
                "sem_concordance": sem_conc,
                "mean_invasion_success_fraction": mean_p,
                "sem_invasion_success_fraction": sem_p,
                "independent_null_concordance": independent_null,
                "excess_concordance": mean_conc - independent_null,
            }
        )

    return rows, np.asarray(scatter_pairs, dtype=float)


def write_tables(rows, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    csv_path = outdir / "invasion_concordance_summary.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    mu = np.asarray([row["mu"] for row in rows])
    excess = np.asarray([row["excess_concordance"] for row in rows])
    pearson_r, pearson_p = stats.pearsonr(mu, excess)
    summary = {
        "pearson_r_excess_vs_mu": float(pearson_r),
        "pearson_p_excess_vs_mu": float(pearson_p),
        "mean_excess_mu_ge_0_3": float(np.mean(excess[mu >= 0.3])),
        "data_source": str(DEFAULT_DATA),
        "null_model": "independent invasion with observed success probability p",
    }
    json_path = outdir / "invasion_concordance_summary.json"
    json_path.write_text(json.dumps(summary, indent=2) + "\n")
    return csv_path, json_path, summary


def make_figure(rows, scatter_pairs, outdir, summary):
    mpl.rcParams.update(
        {
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "font.family": "Arial",
            "font.size": 8,
            "axes.linewidth": 0.7,
            "xtick.direction": "in",
            "ytick.direction": "in",
        }
    )

    mu = np.asarray([row["mu"] for row in rows])
    concordance = np.asarray([row["mean_concordance"] for row in rows])
    concordance_sem = np.asarray([row["sem_concordance"] for row in rows])
    null = np.asarray([row["independent_null_concordance"] for row in rows])
    excess = np.asarray([row["excess_concordance"] for row in rows])

    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.25), constrained_layout=True)

    ax = axes[0]
    if len(scatter_pairs):
        ax.scatter(scatter_pairs[:, 0], scatter_pairs[:, 1], s=4, alpha=0.22, lw=0, color="#2B6CB0")
    ax.axhline(0, color="0.35", lw=0.8, ls=":")
    ax.axvline(0, color="0.35", lw=0.8, ls=":")
    ax.set_xlabel(r"Invasion fitness $\lambda_i$")
    ax.set_ylabel(r"Invasion fitness $\lambda_j$")
    ax.set_title(r"a  Same-parent pairs at $\mu=0.50$", loc="left", fontweight="bold")

    ax = axes[1]
    ax.errorbar(mu, concordance, yerr=concordance_sem, fmt="o-", ms=3.5, lw=1.2, color="#2B6CB0", label="Observed")
    ax.plot(mu, null, "s--", ms=3, lw=1.0, color="0.45", label="Independent null")
    ax.set_xlabel(r"Interaction strength $\mu$")
    ax.set_ylabel("Invasion-outcome\nconcordance")
    ax.set_ylim(0.38, 1.04)
    ax.legend(frameon=False, fontsize=7)
    ax.set_title("b  Concordance", loc="left", fontweight="bold")

    ax = axes[2]
    ax.bar(mu, excess, width=0.045, color="#2B6CB0", alpha=0.82)
    ax.axhline(0, color="0.2", lw=0.8)
    ax.text(
        0.04,
        0.94,
        f"r = {summary['pearson_r_excess_vs_mu']:.3f}\n"
        f"p = {summary['pearson_p_excess_vs_mu']:.1e}",
        transform=ax.transAxes,
        va="top",
        ha="left",
    )
    ax.set_xlabel(r"Interaction strength $\mu$")
    ax.set_ylabel("Excess concordance\n(observed - null)")
    ax.set_title("c  Excess same-parent signal", loc="left", fontweight="bold")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    pdf_path = outdir / "R2_Q4_invasion_concordance.pdf"
    png_path = outdir / "R2_Q4_invasion_concordance.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return pdf_path, png_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    args = parser.parse_args()

    rows, scatter_pairs = summarize(args.data)
    _, _, summary = write_tables(rows, args.outdir)
    pdf_path, png_path = make_figure(rows, scatter_pairs, args.outdir, summary)
    print(f"Wrote {pdf_path}")
    print(f"Wrote {png_path}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
