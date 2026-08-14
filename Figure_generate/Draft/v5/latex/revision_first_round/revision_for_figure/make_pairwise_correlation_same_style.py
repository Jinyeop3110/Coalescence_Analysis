#!/usr/bin/env python3
"""Generate same-style pairwise selection correlation preview figures.

The goal is to regenerate preview figures in the same visual language as the
current manuscript: jittered event dots, square mean markers with s.e.m., and a
gray random-selection baseline.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


SCRIPT_PATH = Path(__file__).resolve()
OUT_DIR = SCRIPT_PATH.parent
FIG2D_DIR = OUT_DIR / "Fig2D"
V4_DIR = OUT_DIR.parents[2]
SESSION_DIR = V4_DIR.parents[2]
FIGURE_GENERATE_DIR = SESSION_DIR / "Figure_generate"
CODE_DIR = FIGURE_GENERATE_DIR / "code"

sys.path.append(str(CODE_DIR))
from PairwiseCorrelationAnalysis_PerEvent import (  # noqa: E402
    calculate_correlation_single_event,
)


SIM_JSON = CODE_DIR / "Simulation_Data/48species_200reps_fine/Community_200reps_fine.json"
SIM_SUMMARY = CODE_DIR / "Figure/AsymmetricityNullModelAnalysis_simulation/correlation_analysis/correlation_summary_simulation.csv"
EXP_SUMMARY = CODE_DIR / "Figure/AsymmetricityNullModelAnalysis/correlation_analysis/correlation_summary_clean.csv"
SYNTHETIC_SEQ = SESSION_DIR / "Postprocessed/processed_Sequences_synthetic.xlsx"
NATURAL_SEQ = SESSION_DIR / "Postprocessed/processed_Sequences_natural.xlsx"
COAL_SYN = SESSION_DIR / "Analyzed/processed_CoalescenceEvent_synthetic.xlsx"

COLORS = {
    "same": "#d94b3d",
    "cross": "#2f80c0",
    "null": "#7f8c8d",
    "point_edge": "#222222",
}
# The original plotting scripts use 2.5 x 2.5 inch standalone panels. Fig. 2D
# is embedded more narrowly inside the composite figure, so the Fig2D previews
# use narrow panels while preserving the same dot/square/baseline style.
PANEL_FIGSIZE = (2.2, 2.5)
COMBINED_FIGSIZE = (PANEL_FIGSIZE[0] * 2 * 0.72, PANEL_FIGSIZE[1] * 0.8)


def pstars(p_value: float) -> str:
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "ns"


def sem(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return float("nan")
    return float(np.std(values, ddof=0) / np.sqrt(len(values)))


def load_simulation_json() -> dict:
    with SIM_JSON.open() as handle:
        return json.load(handle)


def simulation_result(data: dict, summary: pd.DataFrame, mu: float, threshold: float = 1e-4) -> dict:
    key = f"{mu:.2f}"
    param_data = data[key]
    pair_types = ["0_1", "0_2", "0_3", "1_2", "1_3", "2_3"]
    same_corrs: list[float] = []
    cross_corrs: list[float] = []

    for pair_type in pair_types:
        idx1, idx2 = pair_type.split("_")
        for rep_data in param_data.values():
            cc_list = rep_data["cc_list"]
            if pair_type not in cc_list:
                continue
            offspring = np.asarray(cc_list[pair_type], dtype=float)
            parent1 = np.asarray(rep_data["sc_list"][idx1], dtype=float)
            parent2 = np.asarray(rep_data["sc_list"][idx2], dtype=float)
            result = calculate_correlation_single_event(offspring, parent1, parent2, threshold)
            if result is None:
                continue
            same_corrs.append(result["same_origin_corr"])
            cross_corrs.append(result["mixed_origin_corr"])

    same = np.asarray(same_corrs, dtype=float)
    cross = np.asarray(cross_corrs, dtype=float)
    if len(same) == 0 or len(same) != len(cross):
        raise RuntimeError(f"Unexpected simulation correlation counts for mu={mu}")

    t_stat, paired_t_p_value = stats.ttest_rel(same, cross)
    summary_row = summary[np.isclose(summary["Interaction_Strength"].astype(float), mu)]
    if summary_row.empty:
        raise RuntimeError(f"No simulation summary row found for mu={mu}")
    null_mean = float(summary_row.iloc[0]["Random"])
    permutation_p_value = float(summary_row.iloc[0]["p-value"])
    return {
        "source": "Simulation",
        "condition": f"$\\mu={mu:.1f}$",
        "same": same,
        "cross": cross,
        "mean_same": float(np.mean(same)),
        "mean_cross": float(np.mean(cross)),
        "sem_same": sem(same),
        "sem_cross": sem(cross),
        "null_mean": null_mean,
        "p_value": permutation_p_value,
        "permutation_p_value": permutation_p_value,
        "paired_t_stat": float(t_stat),
        "paired_t_p_value": float(paired_t_p_value),
        "n": int(len(same)),
    }


def stratified_sample(values: np.ndarray, n_display: int = 100, n_bins: int = 10, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.asarray(values, dtype=float)
    sorted_indices = np.argsort(values)
    selected = []
    points_per_bin = n_display // n_bins

    for i in range(n_bins):
        start = i * len(sorted_indices) // n_bins
        end = (i + 1) * len(sorted_indices) // n_bins
        bin_indices = sorted_indices[start:end]
        if len(bin_indices) == 0:
            continue
        n_samples = points_per_bin + (1 if i < (n_display % n_bins) else 0)
        selected.extend(rng.choice(bin_indices, size=min(n_samples, len(bin_indices)), replace=False))

    return values[np.asarray(selected, dtype=int)]


def load_experiment_events() -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray], list[str]]:
    sequences = pd.concat(
        [pd.read_excel(SYNTHETIC_SEQ), pd.read_excel(NATURAL_SEQ)],
        ignore_index=True,
    )
    coalescence = pd.read_excel(COAL_SYN)
    sequence_by_id = sequences.set_index("SampleIDX")
    nutrient_map = {"L": "LN", "M": "MN", "H": "HN"}

    offspring_list: list[np.ndarray] = []
    parent1_list: list[np.ndarray] = []
    parent2_list: list[np.ndarray] = []
    nutrient_conditions: list[str] = []

    for _, row in coalescence.iterrows():
        if row.get("CommunityOrigin") != "S" or row.get("CoalescenceType") != "C":
            continue
        nutrient = nutrient_map.get(row.get("Medium"))
        if nutrient is None:
            continue

        sample_ids = [row.get("SampleIDX"), row.get("SampleIDX_Sub1"), row.get("SampleIDX_Sub2")]
        if any(sample_id not in sequence_by_id.index for sample_id in sample_ids):
            continue

        vectors = []
        for sample_id in sample_ids:
            row_values = sequence_by_id.loc[sample_id]
            if isinstance(row_values, pd.DataFrame):
                row_values = row_values.iloc[0]
            vector = row_values.to_numpy(dtype=float)
            vector = np.nan_to_num(vector, nan=0.0)
            vector = vector * (vector > 1e-3)
            total = vector.sum()
            if total <= 0:
                break
            vectors.append(vector / total)
        if len(vectors) != 3:
            continue

        if np.sum(vectors[0] > 0) < 3:
            continue

        offspring_list.append(vectors[0])
        parent1_list.append(vectors[1])
        parent2_list.append(vectors[2])
        nutrient_conditions.append(nutrient)

    return offspring_list, parent1_list, parent2_list, nutrient_conditions


def experiment_results(summary: pd.DataFrame) -> dict[str, dict]:
    offspring, parent1, parent2, nutrients = load_experiment_events()
    labels = {"LN": "Nutr-", "MN": "Base", "HN": "Nutr+"}
    results = {}

    for nutrient in ["LN", "MN", "HN"]:
        idx = [i for i, value in enumerate(nutrients) if value == nutrient]
        same_corrs = []
        cross_corrs = []
        for i in idx:
            result = calculate_correlation_single_event(offspring[i], parent1[i], parent2[i], threshold=1e-4)
            if result is None:
                continue
            same_corrs.append(result["same_origin_corr"])
            cross_corrs.append(result["mixed_origin_corr"])

        same = np.asarray(same_corrs, dtype=float)
        cross = np.asarray(cross_corrs, dtype=float)
        t_stat, paired_t_p_value = stats.ttest_rel(same, cross)
        summary_row = summary[summary["Condition"] == labels[nutrient]]
        if summary_row.empty:
            raise RuntimeError(f"No experimental summary row found for {labels[nutrient]}")
        null_mean = float(summary_row.iloc[0]["Random"])
        permutation_p_value = float(summary_row.iloc[0]["p-value"])
        results[nutrient] = {
            "source": "Experiment",
            "condition": labels[nutrient],
            "same": same,
            "cross": cross,
            "mean_same": float(np.mean(same)),
            "mean_cross": float(np.mean(cross)),
            "sem_same": sem(same),
            "sem_cross": sem(cross),
            "null_mean": null_mean,
            "p_value": permutation_p_value,
            "permutation_p_value": permutation_p_value,
            "paired_t_stat": float(t_stat),
            "paired_t_p_value": float(paired_t_p_value),
            "n": int(len(same)),
        }

    return results


def draw_panel(ax, result: dict, title: str | None = None, y_limits: tuple[float, float] = (-0.4, 0.4)) -> None:
    x = np.arange(2)
    colors = [COLORS["same"], COLORS["cross"]]
    rng = np.random.default_rng(42)

    if result["source"] == "Simulation":
        same_display = stratified_sample(result["same"], seed=101)
        cross_display = stratified_sample(result["cross"], seed=202)
        jitter = 0.05
        dot_alpha = 0.25
        dot_size = 10
    else:
        same_display = result["same"]
        cross_display = result["cross"]
        jitter = 0.10
        dot_alpha = 0.30
        dot_size = 15

    ax.scatter(
        x[0] + rng.normal(0, jitter, len(same_display)),
        same_display,
        alpha=dot_alpha,
        s=dot_size,
        color=colors[0],
        edgecolors="none",
        zorder=2,
    )
    ax.scatter(
        x[1] + rng.normal(0, jitter, len(cross_display)),
        cross_display,
        alpha=dot_alpha,
        s=dot_size,
        color=colors[1],
        edgecolors="none",
        zorder=2,
    )

    ax.axhline(result["null_mean"], color=COLORS["null"], linewidth=2, alpha=0.7, zorder=1)

    means = [result["mean_same"], result["mean_cross"]]
    sems = [result["sem_same"], result["sem_cross"]]
    for x_pos, mean, err, color in zip([0, 1], means, sems, colors):
        ax.errorbar(
            x_pos,
            mean,
            yerr=err,
            fmt="s",
            markersize=6,
            capsize=5,
            capthick=1.5,
            elinewidth=1.5,
            color=color,
            ecolor="black",
            markeredgecolor="black",
            markeredgewidth=0.5,
            zorder=10,
        )

    ylim_low, ylim_high = y_limits
    ax.set_ylim(ylim_low, ylim_high)
    stars = pstars(result["p_value"])
    if stars != "ns":
        y_max = max(result["mean_same"] + result["sem_same"], result["mean_cross"] + result["sem_cross"], result["null_mean"])
        y_min = min(result["mean_same"] - result["sem_same"], result["mean_cross"] - result["sem_cross"], result["null_mean"])
        y_range = max(y_max - y_min, 0.1)
        bracket_y = min(y_max + y_range * 0.05, ylim_high - 0.08 * (ylim_high - ylim_low))
        tick = 0.01 * (ylim_high - ylim_low)
        ax.plot([0, 1], [bracket_y, bracket_y], color="black", linewidth=0.8)
        ax.plot([0, 0], [bracket_y - tick, bracket_y], color="black", linewidth=0.8)
        ax.plot([1, 1], [bracket_y - tick, bracket_y], color="black", linewidth=0.8)
        ax.text(0.5, bracket_y, stars, ha="center", va="bottom", fontsize=9)

    ax.set_xlabel("")
    ax.set_ylabel("Pairwise selection correlation", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(["Same\nParent", "Cross\nParents"], fontsize=9.5)
    ax.tick_params(axis="y", labelsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5, steps=[1, 2, 5, 10]))
    if title:
        ax.set_title(title, fontsize=11)
    sns.despine(ax=ax)


def save_figure(fig, stem: str, out_dir: Path = OUT_DIR) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for ext in ["png", "svg"]:
        kwargs = {"dpi": 300} if ext == "png" else {}
        path = out_dir / f"{stem}.{ext}"
        fig.savefig(path, bbox_inches="tight", **kwargs)
        print(f"Saved {path}")


def compact_combined_axes(axes: np.ndarray) -> None:
    for ax in axes:
        ax.title.set_fontsize(10)
        ax.tick_params(axis="both", labelsize=8)
        for label in ax.get_xticklabels():
            label.set_fontsize(8)
    axes[0].yaxis.label.set_fontsize(8.5)


def write_summary(sim_results: dict[float, dict], exp_results: dict[str, dict]) -> None:
    rows = []
    for key, result in sim_results.items():
        rows.append(summary_row(f"simulation_mu_{key:.1f}", result))
    for key, result in exp_results.items():
        rows.append(summary_row(f"experiment_{key}", result))
    pd.DataFrame(rows).to_csv(OUT_DIR / "pairwise_correlation_same_style_summary.csv", index=False)


def summary_row(name: str, result: dict) -> dict:
    return {
        "name": name,
        "source": result["source"],
        "condition": result["condition"],
        "n": result["n"],
        "mean_same": result["mean_same"],
        "sem_same": result["sem_same"],
        "mean_cross": result["mean_cross"],
        "sem_cross": result["sem_cross"],
        "delta_same_minus_cross": result["mean_same"] - result["mean_cross"],
        "null_mean": result["null_mean"],
        "permutation_count": 1000,
        "permutation_p_value": result["permutation_p_value"],
        "paired_t_stat": result["paired_t_stat"],
        "paired_t_p_value": result["paired_t_p_value"],
    }


def main() -> None:
    sns.set_theme(style="white", context="paper")
    plt.rcParams.update(
        {
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "font.family": "Arial",
            "axes.linewidth": 0.8,
        }
    )

    print("Loading and analyzing simulation data...", flush=True)
    sim_data = load_simulation_json()
    sim_summary = pd.read_csv(SIM_SUMMARY)
    sim_results = {mu: simulation_result(sim_data, sim_summary, mu) for mu in [0.3, 0.6, 0.8]}

    print("Loading and analyzing experimental data...", flush=True)
    exp_summary = pd.read_csv(EXP_SUMMARY)
    exp_results = experiment_results(exp_summary)

    print("Writing same-style figure previews...", flush=True)
    fig, ax = plt.subplots(1, 1, figsize=PANEL_FIGSIZE)
    draw_panel(ax, sim_results[0.6], "Simulation", y_limits=(-0.55, 0.55))
    fig.tight_layout()
    save_figure(fig, "simulation_pairwise_correlation_same_style", FIG2D_DIR)
    plt.close(fig)

    fig, ax = plt.subplots(1, 1, figsize=PANEL_FIGSIZE)
    draw_panel(ax, exp_results["MN"], "Experiment", y_limits=(-0.1, 0.35))
    fig.tight_layout()
    save_figure(fig, "experiment_pairwise_correlation_same_style", FIG2D_DIR)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=COMBINED_FIGSIZE, sharey=False)
    draw_panel(axes[0], sim_results[0.6], "Simulation", y_limits=(-0.55, 0.55))
    draw_panel(axes[1], exp_results["MN"], "Experiment", y_limits=(-0.1, 0.35))
    axes[1].set_ylabel("")
    compact_combined_axes(axes)
    fig.tight_layout(w_pad=0.6)
    save_figure(fig, "combined_pairwise_correlation_same_style", FIG2D_DIR)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(PANEL_FIGSIZE[0] * 3, PANEL_FIGSIZE[1]), sharey=False)
    sim_y_limits = {0.3: (-0.4, 0.4), 0.6: (-0.55, 0.55), 0.8: (-0.6, 0.55)}
    for ax, mu in zip(axes, [0.3, 0.6, 0.8]):
        draw_panel(ax, sim_results[mu], f"Simulation {sim_results[mu]['condition']}", y_limits=sim_y_limits[mu])
    for i, ax in enumerate(axes):
        ax.text(-0.22, 1.04, chr(ord("a") + i), transform=ax.transAxes, fontsize=13, fontweight="bold")
        if i > 0:
            ax.set_ylabel("")
    fig.tight_layout(w_pad=1.2)
    save_figure(fig, "pairwise_correlation_simulation_all_same_style")
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(PANEL_FIGSIZE[0] * 3, PANEL_FIGSIZE[1]), sharey=True)
    for ax, nutrient in zip(axes, ["LN", "MN", "HN"]):
        draw_panel(ax, exp_results[nutrient], f"Experiment {exp_results[nutrient]['condition']}", y_limits=(-0.2, 0.6))
    for i, ax in enumerate(axes):
        ax.text(-0.22, 1.04, chr(ord("a") + i), transform=ax.transAxes, fontsize=13, fontweight="bold")
        if i > 0:
            ax.set_ylabel("")
    fig.tight_layout(w_pad=1.2)
    save_figure(fig, "pairwise_correlation_experiment_all_same_style")
    plt.close(fig)

    write_summary(sim_results, exp_results)
    print(f"Saved {OUT_DIR / 'pairwise_correlation_same_style_summary.csv'}")


if __name__ == "__main__":
    main()
