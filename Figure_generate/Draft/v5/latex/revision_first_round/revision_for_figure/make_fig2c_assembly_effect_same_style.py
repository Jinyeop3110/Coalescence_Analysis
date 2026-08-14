#!/usr/bin/env python3
"""Generate same-style Fig. 2C mean pairwise interaction panel."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


SCRIPT_PATH = Path(__file__).resolve()
OUT_DIR = SCRIPT_PATH.parent
FIG2C_DIR = OUT_DIR / "Fig2C"
V4_DIR = OUT_DIR.parents[2]
SESSION_DIR = V4_DIR.parents[2]
CODE_DIR = SESSION_DIR / "Figure_generate" / "code"

DATA_PATH = CODE_DIR / "Simulation_Data/mean_uniform_grid_100reps/Community_mean_uniform_grid_100reps.json"
INTERACTION_STRENGTH = 0.60
FIGSIZE = (2.0, 2.1)

COLORS = {
    "initial": "#8B7AB8",
    "post": "#F4A582",
}


def calculate_mean_interaction_all_species(interaction_matrix: np.ndarray) -> float:
    interaction_matrix = np.asarray(interaction_matrix, dtype=float)
    mask = ~np.eye(interaction_matrix.shape[0], dtype=bool)
    return float(np.mean(interaction_matrix[mask]))


def calculate_mean_interaction_present_species(abundances: np.ndarray, interaction_matrix: np.ndarray) -> float:
    abundances = np.asarray(abundances, dtype=float)
    interaction_matrix = np.asarray(interaction_matrix, dtype=float)
    present_indices = np.where(abundances > 1e-6)[0]
    if len(present_indices) < 2:
        return float("nan")

    submatrix = interaction_matrix[np.ix_(present_indices, present_indices)]
    mask = ~np.eye(submatrix.shape[0], dtype=bool)
    return float(np.mean(submatrix[mask]))


def analyze_interaction_strength(data_path: Path, interaction_strength: float) -> dict:
    with data_path.open() as handle:
        data = json.load(handle)

    key = f"mean{interaction_strength:.2f}"
    coalescence_pairs = [
        ("c1", "c2", "c1_c2"),
        ("c1", "c3", "c1_c3"),
        ("c1", "c4", "c1_c4"),
        ("c2", "c3", "c2_c3"),
        ("c2", "c4", "c2_c4"),
        ("c3", "c4", "c3_c4"),
    ]
    initial_values: list[float] = []
    post_values: list[float] = []

    for rep_data in data[key].values():
        interaction_matrix = np.asarray(rep_data["parameters"]["interaction_matrix"], dtype=float)
        initial_mean = calculate_mean_interaction_all_species(interaction_matrix)
        cc_list = rep_data["cc_list"]

        for _, _, cc_name in coalescence_pairs:
            post_mean = calculate_mean_interaction_present_species(
                np.asarray(cc_list[cc_name], dtype=float),
                interaction_matrix,
            )
            if np.isnan(post_mean):
                continue
            initial_values.append(initial_mean)
            post_values.append(post_mean)

    initial = np.asarray(initial_values, dtype=float)
    post = np.asarray(post_values, dtype=float)
    t_stat, p_value = stats.ttest_rel(initial, post)

    return {
        "interaction_strength": interaction_strength,
        "initial": initial,
        "post": post,
        "initial_mean": float(np.mean(initial)),
        "post_mean": float(np.mean(post)),
        "initial_sem": float(np.std(initial, ddof=0) / np.sqrt(len(initial))),
        "post_sem": float(np.std(post, ddof=0) / np.sqrt(len(post))),
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "n": int(len(initial)),
    }


def save_summary(result: dict) -> None:
    FIG2C_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [
            {
                "interaction_strength": result["interaction_strength"],
                "n": result["n"],
                "initial_mean": result["initial_mean"],
                "initial_sem": result["initial_sem"],
                "post_assembly_mean": result["post_mean"],
                "post_assembly_sem": result["post_sem"],
                "paired_t_stat": result["t_stat"],
                "paired_t_p_value": result["p_value"],
            }
        ]
    ).to_csv(FIG2C_DIR / "fig2c_assembly_effect_summary.csv", index=False)


def draw_panel(ax, result: dict) -> None:
    x = np.array([0.0, 0.78])
    rng = np.random.default_rng(42)
    jitter = 0.10
    values = [result["initial"], result["post"]]
    means = [result["initial_mean"], result["post_mean"]]
    sems = [result["initial_sem"], result["post_sem"]]
    colors = [COLORS["initial"], COLORS["post"]]

    for x_pos, group_values, color in zip(x, values, colors):
        ax.scatter(
            x_pos + rng.normal(0, jitter, len(group_values)),
            group_values,
            alpha=0.30,
            s=10,
            color=color,
            edgecolors="none",
            zorder=2,
        )

    for x_pos, mean, err, color in zip(x, means, sems, colors):
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

    ylim_low, ylim_high = 0.0, 0.8
    ax.set_ylim(ylim_low, ylim_high)
    y_max = max(means[0] + sems[0], means[1] + sems[1])
    bracket_y = min(y_max + 0.08, ylim_high - 0.06)
    tick = 0.04
    ax.plot([x[0], x[1]], [bracket_y, bracket_y], color="black", linewidth=0.8)
    ax.plot([x[0], x[0]], [bracket_y - tick, bracket_y], color="black", linewidth=0.8)
    ax.plot([x[1], x[1]], [bracket_y - tick, bracket_y], color="black", linewidth=0.8)
    ax.text(np.mean(x), bracket_y, "***", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_xlim(-0.30, 1.08)
    ax.set_ylabel("Mean pairwise interaction", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(["Initial", "Post-\nassembly"], fontsize=9.5)
    ax.yaxis.set_major_locator(MultipleLocator(0.2))

    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")
    ax.tick_params(
        axis="both",
        which="major",
        direction="in",
        length=4,
        width=0.8,
        color="black",
        bottom=True,
        left=True,
        top=False,
        right=False,
    )
    ax.tick_params(axis="x", labelsize=9.5)
    ax.tick_params(axis="y", labelsize=9)
    ax.spines["left"].set_visible(True)
    ax.spines["bottom"].set_visible(True)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_figure(fig, stem: str) -> None:
    FIG2C_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ["png", "svg"]:
        kwargs = {"dpi": 300} if ext == "png" else {}
        path = FIG2C_DIR / f"{stem}.{ext}"
        fig.savefig(path, bbox_inches="tight", **kwargs)
        print(f"Saved {path}")


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

    print("Loading and analyzing Fig. 2C assembly-effect data...", flush=True)
    result = analyze_interaction_strength(DATA_PATH, INTERACTION_STRENGTH)
    save_summary(result)

    fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
    draw_panel(ax, result)
    fig.tight_layout()
    save_figure(fig, "fig2c_assembly_effect_same_style")
    plt.close(fig)


if __name__ == "__main__":
    main()
