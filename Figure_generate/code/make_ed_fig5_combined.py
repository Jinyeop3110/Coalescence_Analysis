#!/usr/bin/env python3
"""Regenerate Extended Data Fig. 5 with visible mean markers in panel c."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[1]
sys.path.append(str(SCRIPT_DIR))

from PairwiseCorrelationAnalysis_PerEvent import calculate_correlation_single_event  # noqa: E402


DATA_PATH = SCRIPT_DIR / "Simulation_Data/48species_200reps_fine/Community_200reps_fine.json"
SUMMARY_PATH = SCRIPT_DIR / "Figure/AsymmetricityNullModelAnalysis_simulation/correlation_analysis/correlation_summary_simulation.csv"
OUT_DIR = ROOT_DIR / "Figure_generate/Draft/v4/latex/figures/extended_data"
ARCHIVE_DIR = OUT_DIR / "archive"
sys.path.append(str(OUT_DIR))

from combine_extended_figures import combine_figure  # noqa: E402


def load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def collect_event_correlations(data: dict, mu: float, threshold: float = 1e-4) -> dict:
    key = f"{mu:.2f}"
    param_data = data[key]
    pair_types = ["0_1", "0_2", "0_3", "1_2", "1_3", "2_3"]
    same_corrs = []
    cross_corrs = []

    for pair_type in pair_types:
        idx1, idx2 = pair_type.split("_")
        for rep_data in param_data.values():
            cc_list = rep_data["cc_list"]
            if pair_type not in cc_list:
                continue
            result = calculate_correlation_single_event(
                np.asarray(cc_list[pair_type]),
                np.asarray(rep_data["sc_list"][idx1]),
                np.asarray(rep_data["sc_list"][idx2]),
                threshold,
            )
            if result is None:
                continue
            same_corrs.append(result["same_origin_corr"])
            cross_corrs.append(result["mixed_origin_corr"])

    same = np.asarray(same_corrs, dtype=float)
    cross = np.asarray(cross_corrs, dtype=float)
    if len(same) != len(cross):
        raise ValueError(f"Unequal same/cross counts for mu={mu}")

    t_stat, p_value = stats.ttest_rel(same, cross)
    return {
        "mu": mu,
        "same": same,
        "cross": cross,
        "mean_same": float(np.mean(same)),
        "mean_cross": float(np.mean(cross)),
        "sem_same": float(np.std(same) / np.sqrt(len(same))),
        "sem_cross": float(np.std(cross) / np.sqrt(len(cross))),
        "p_value": float(p_value),
    }


def stratified_sample(values: np.ndarray, n_display: int = 100, n_bins: int = 10, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.asarray(values)
    sorted_indices = np.argsort(values)
    selected = []
    points_per_bin = n_display // n_bins

    for i in range(n_bins):
        start = i * len(sorted_indices) // n_bins
        end = (i + 1) * len(sorted_indices) // n_bins
        bin_indices = sorted_indices[start:end]
        n_samples = points_per_bin + (1 if i < (n_display % n_bins) else 0)
        if len(bin_indices) == 0:
            continue
        selected.extend(rng.choice(bin_indices, size=min(n_samples, len(bin_indices)), replace=False))

    return values[np.asarray(selected, dtype=int)]


def stars(p_value: float) -> str:
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "ns"


def plot_bar_panel(ax, result: dict, null_mean: float, label: str, y_limits: tuple[float, float]) -> None:
    colors = {"same": "#e74c3c", "cross": "#3498db", "null": "#95a5a6"}
    rng = np.random.default_rng(42)
    x = np.array([0, 1])
    jitter = 0.05

    same_display = stratified_sample(result["same"], seed=101)
    cross_display = stratified_sample(result["cross"], seed=202)
    ax.scatter(
        x[0] + rng.normal(0, jitter, len(same_display)),
        same_display,
        alpha=0.25,
        s=12,
        color=colors["same"],
        edgecolors="none",
        zorder=2,
    )
    ax.scatter(
        x[1] + rng.normal(0, jitter, len(cross_display)),
        cross_display,
        alpha=0.25,
        s=12,
        color=colors["cross"],
        edgecolors="none",
        zorder=2,
    )

    ax.axhline(null_mean, color=colors["null"], linewidth=2, alpha=0.75, zorder=1)
    ax.errorbar(
        x[0],
        result["mean_same"],
        yerr=result["sem_same"],
        fmt="s",
        markersize=6,
        capsize=6,
        capthick=1.2,
        color=colors["same"],
        ecolor="black",
        markeredgecolor="black",
        markeredgewidth=0.8,
        linewidth=1.2,
        zorder=10,
    )
    ax.errorbar(
        x[1],
        result["mean_cross"],
        yerr=result["sem_cross"],
        fmt="s",
        markersize=6,
        capsize=6,
        capthick=1.2,
        color=colors["cross"],
        ecolor="black",
        markeredgecolor="black",
        markeredgewidth=0.8,
        linewidth=1.2,
        zorder=10,
    )

    ylim_low, ylim_high = y_limits
    bracket_y = ylim_high - 0.08 * (ylim_high - ylim_low)
    if stars(result["p_value"]) != "ns":
        ax.plot([0, 1], [bracket_y, bracket_y], color="black", linewidth=0.8)
        tick = 0.015 * (ylim_high - ylim_low)
        ax.plot([0, 0], [bracket_y - tick, bracket_y], color="black", linewidth=0.8)
        ax.plot([1, 1], [bracket_y - tick, bracket_y], color="black", linewidth=0.8)
        ax.text(0.5, bracket_y, stars(result["p_value"]), ha="center", va="bottom", fontsize=10)

    ax.set_ylim(*y_limits)
    ax.set_xlim(-0.4, 1.4)
    ax.set_xticks(x)
    ax.set_xticklabels(["Same\nParent", "Cross\nParents"], fontsize=10)
    ax.set_ylabel("Pairwise selection correlation", fontsize=10)
    ax.tick_params(axis="y", labelsize=9)
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    sns.despine(ax=ax)
    ax.tick_params(
        axis="both",
        which="major",
        direction="in",
        length=5,
        width=0.8,
        bottom=True,
        left=True,
    )


def plot_trend_panel(ax, summary: pd.DataFrame) -> None:
    x = summary["Interaction_Strength"].to_numpy(dtype=float)
    same = summary["Same Parent"].to_numpy(dtype=float)
    cross = summary["Cross Parents"].to_numpy(dtype=float)
    random = summary["Random"].to_numpy(dtype=float)

    ax.plot(x, same, "-o", color="#e74c3c", markeredgecolor="black", markersize=5, label="Same Parent")
    ax.plot(x, cross, "-s", color="#3498db", markeredgecolor="black", markersize=5, label="Cross Parents")
    ax.plot(x, random, "-", color="#95a5a6", linewidth=3, alpha=0.75, label="Random Selection")
    ax.axhline(0, color="0.5", linestyle="--", linewidth=0.8)
    ax.set_xlabel("Interaction Strength", fontsize=10)
    ax.set_ylabel("Pairwise Selection Correlation", fontsize=10)
    ax.set_xlim(0, 1.22)
    ax.set_ylim(-0.75, 1.08)
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.tick_params(labelsize=9)
    ax.legend(frameon=True, fancybox=False, edgecolor="black", fontsize=8, loc="upper center")
    sns.despine(ax=ax)
    ax.tick_params(
        axis="both",
        which="major",
        direction="in",
        length=5,
        width=0.8,
        bottom=True,
        left=True,
    )


def save_panel(fig, stem: str) -> None:
    """Save an unlabeled panel into the extended-data archive."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ["pdf"]:
        path = ARCHIVE_DIR / f"{stem}.{ext}"
        kwargs = {"dpi": 300} if ext == "png" else {}
        fig.savefig(path, bbox_inches="tight", **kwargs)
        print(f"Saved {path}")


def main() -> None:
    data = load_json(DATA_PATH)
    summary = pd.read_csv(SUMMARY_PATH)
    summary["Same Parent"] = pd.to_numeric(summary["Same Parent"])
    summary["Cross Parents"] = pd.to_numeric(summary["Cross Parents"])
    summary["Random"] = pd.to_numeric(summary["Random"])

    mus = [0.3, 0.6, 0.8]
    results = {mu: collect_event_correlations(data, mu) for mu in mus}
    random_by_mu = {
        row.Interaction_Strength: float(row.Random)
        for row in summary.itertuples(index=False)
    }

    sns.set_style("white")

    panel_specs = [
        ("ED_Fig2a_correlation_u0.3", 0.3, (-0.55, 0.55)),
        ("ED_Fig2b_correlation_u0.6", 0.6, (-0.55, 0.55)),
        ("ED_Fig2c_correlation_u0.8", 0.8, (-0.8, 0.8)),
    ]
    for stem, mu, y_limits in panel_specs:
        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        plot_bar_panel(ax, results[mu], random_by_mu[mu], "", y_limits)
        fig.tight_layout()
        save_panel(fig, stem)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(3.9, 2.9))
    plot_trend_panel(ax, summary)
    fig.tight_layout()
    save_panel(fig, "ED_Fig2d_correlation_vs_mu")
    plt.close(fig)

    combine_figure(
        input_files=[
            "ED_Fig2a_correlation_u0.3.pdf",
            "ED_Fig2b_correlation_u0.6.pdf",
            "ED_Fig2c_correlation_u0.8.pdf",
            "ED_Fig2d_correlation_vs_mu.pdf",
        ],
        grid_layout=[[0, 1, 2], [3]],
        output_name="ED_Fig5_combined.pdf",
        labels=["a", "b", "c", "d"],
    )


if __name__ == "__main__":
    main()
