#!/usr/bin/env python3
"""Simulation parent-vector norm imbalance diagnostics for Reviewer 3."""

from __future__ import annotations

import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, CODE_DIR)

_prev_cwd = os.getcwd()
os.chdir(CODE_DIR)
from common_setup import (  # noqa: E402
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
)
from COLORMAP import get_phase_diagram_colors  # noqa: E402
os.chdir(_prev_cwd)


CLASS_NAMES = {0: "Dominance", 1: "Mixture", 2: "Restructuring", None: "Boundary"}
PDI_DOMINANCE_FOLD_THRESHOLD = 1.0 + math.sqrt(2.0)


def classify_vector(n_c: np.ndarray, n_a: np.ndarray, n_b: np.ndarray) -> str:
    u, v, k = metric_VectorDecomposition_onlyPositive(n_a, n_b, n_c)
    x, y = calculate_assymetricity(u, v, k)
    return CLASS_NAMES[characterize_case(x, y)]


def load_simulation_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    data_path = os.path.join(
        CODE_DIR,
        "Simulation_Data",
        "48species_200reps_fine",
        "Community_200reps_fine.json",
    )
    with open(data_path, "r") as handle:
        sim_data = json.load(handle)

    parent_rows = []
    event_rows = []
    for mu_key in sorted(sim_data.keys(), key=float):
        mu = float(mu_key)
        for rep_key, rep_data in sim_data[mu_key].items():
            sc_list = rep_data["sc_list"]
            cc_list = rep_data["cc_list"]

            for sc_key, sc_vec in sc_list.items():
                vec = np.asarray(sc_vec, dtype=float)
                parent_rows.append(
                    {
                        "mu": mu,
                        "rep": rep_key,
                        "subcommunity": sc_key,
                        "l2_norm": float(np.linalg.norm(vec)),
                        "richness": int(np.sum(vec > 1e-3)),
                    }
                )

            for cc_key in cc_list:
                parts = cc_key.split("_")
                n_a = np.asarray(sc_list[parts[0]], dtype=float)
                n_b = np.asarray(sc_list[parts[1]], dtype=float)
                norm_a = float(np.linalg.norm(n_a))
                norm_b = float(np.linalg.norm(n_b))
                if min(norm_a, norm_b) <= 1e-12:
                    continue

                additive = (n_a + n_b) / 2.0
                try:
                    null_class = classify_vector(additive, n_a, n_b)
                except Exception:
                    null_class = "Boundary"

                event_rows.append(
                    {
                        "mu": mu,
                        "rep": rep_key,
                        "event": cc_key,
                        "norm_a": norm_a,
                        "norm_b": norm_b,
                        "norm_ratio": max(norm_a, norm_b) / min(norm_a, norm_b),
                        "null_class": null_class,
                    }
                )

    return pd.DataFrame(parent_rows), pd.DataFrame(event_rows)


def summarize_by_mu(parents: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mu in sorted(events["mu"].unique()):
        parent_mu = parents[parents["mu"] == mu]
        event_mu = events[events["mu"] == mu]
        counts = event_mu["null_class"].value_counts()
        rows.append(
            {
                "mu": mu,
                "n_events": len(event_mu),
                "norm_median": parent_mu["l2_norm"].median(),
                "norm_q25": parent_mu["l2_norm"].quantile(0.25),
                "norm_q75": parent_mu["l2_norm"].quantile(0.75),
                "ratio_median": event_mu["norm_ratio"].median(),
                "ratio_q25": event_mu["norm_ratio"].quantile(0.25),
                "ratio_q75": event_mu["norm_ratio"].quantile(0.75),
                "ratio_q95": event_mu["norm_ratio"].quantile(0.95),
                "dominance_fraction": counts.get("Dominance", 0) / len(event_mu),
                "mixture_fraction": counts.get("Mixture", 0) / len(event_mu),
                "restructuring_fraction": counts.get("Restructuring", 0) / len(event_mu),
            }
        )
    return pd.DataFrame(rows)


def make_figure(summary: pd.DataFrame, out_pdf: str) -> None:
    phase_colors = get_phase_diagram_colors()
    class_colors = {
        "Dominance": phase_colors[0],
        "Mixture": phase_colors[1],
        "Restructuring": phase_colors[2],
    }

    fig, axes = plt.subplots(1, 3, figsize=(8.7, 2.7))

    ax = axes[0]
    ax.fill_between(
        summary["mu"],
        summary["norm_q25"],
        summary["norm_q75"],
        color="#4c78a8",
        alpha=0.22,
        linewidth=0,
        label="25th-75th percentile",
    )
    ax.plot(summary["mu"], summary["norm_median"], color="#4c78a8", marker="o", markersize=3, linewidth=1.2)
    ax.set_yscale("log")
    ax.set_title("A", loc="left", fontweight="bold")
    ax.set_xlabel(r"interaction strength $\mu$")
    ax.set_ylabel(r"sub-community $\|n\|_2$")
    ax.legend(frameon=False, fontsize=6, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    ax.fill_between(
        summary["mu"],
        summary["ratio_q25"],
        summary["ratio_q75"],
        color="#4c78a8",
        alpha=0.22,
        linewidth=0,
        label="25th-75th percentile",
    )
    ax.plot(summary["mu"], summary["ratio_median"], color="#4c78a8", marker="o", markersize=3, linewidth=1.2, label="median")
    ax.plot(summary["mu"], summary["ratio_q95"], color="#4c78a8", linestyle=":", linewidth=1.0, label="95th pct.")
    ax.axhline(PDI_DOMINANCE_FOLD_THRESHOLD, color="0.15", linewidth=0.8, linestyle="--")
    ax.text(
        0.03,
        PDI_DOMINANCE_FOLD_THRESHOLD * 1.07,
        r"PDI $<0.25$ or $>0.75$",
        transform=ax.get_yaxis_transform(),
        ha="left",
        va="bottom",
        fontsize=6.5,
        color="0.15",
    )
    ax.set_yscale("log")
    ax.set_title("B", loc="left", fontweight="bold")
    ax.set_xlabel(r"interaction strength $\mu$")
    ax.set_ylabel(r"parental $\|n\|_2$ fold difference")
    ax.legend(frameon=False, fontsize=6, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[2]
    bottoms = np.zeros(len(summary))
    for cls in ["Dominance", "Mixture", "Restructuring"]:
        vals = summary[f"{cls.lower()}_fraction"].to_numpy(float)
        ax.bar(
            summary["mu"],
            vals,
            bottom=bottoms,
            width=0.035,
            color=class_colors[cls],
            edgecolor="white",
            linewidth=0.2,
            label=cls,
        )
        bottoms += vals
    ax.set_title("C", loc="left", fontweight="bold")
    ax.set_xlabel(r"interaction strength $\mu$")
    ax.set_ylabel("additive-null fraction")
    ax.set_ylim(0, 1)
    ax.legend(frameon=False, fontsize=6, loc="center left", bbox_to_anchor=(0.02, 0.52))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout(w_pad=1.1)
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf.replace(".pdf", ".png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parents, events = load_simulation_data()
    summary = summarize_by_mu(parents, events)
    parents.to_csv(os.path.join(SCRIPT_DIR, "sim_parent_norm_vectors.csv"), index=False)
    events.to_csv(os.path.join(SCRIPT_DIR, "sim_parent_norm_events.csv"), index=False)
    summary.to_csv(os.path.join(SCRIPT_DIR, "sim_parent_norm_summary.csv"), index=False)
    make_figure(summary, os.path.join(SCRIPT_DIR, "Fig_R3_3_sim_parent_norm_asymmetry.pdf"))

    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    print("Overall additive-null classes:", events["null_class"].value_counts().to_dict())


if __name__ == "__main__":
    main()
