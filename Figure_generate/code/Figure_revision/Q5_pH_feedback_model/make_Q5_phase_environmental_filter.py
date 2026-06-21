"""
make_Q5_phase_environmental_filter.py
=====================================

Render a Q5 phase-diagram figure for the trait-based environmental-filtering
null model. Layout matches Fig_Q5_phase_pH: three Sim(A,C)-Sim(B,C) scatter
panels and one stacked outcome-fraction panel.

Input:
    Q5_phase_events_filter.csv

Output:
    Fig_Q5_phase_filter.{pdf,png,svg}
"""

from __future__ import annotations

import math
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "Q5_phase_events_filter.csv")

sns.set_style("ticks")
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["font.size"] = 8
mpl.rcParams["axes.linewidth"] = 0.5
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["text.usetex"] = False

OUTCOME_COLORS = {
    "Dominance": "#1f77b4",
    "Mixture": "#9ecae1",
    "Restructuring": "#d62728",
}
OUTCOMES = ["Dominance", "Mixture", "Restructuring"]
STRENGTHS = [
    ("Nutr-", "Nutr$-$\n($\\gamma$=2.80)"),
    ("Base", "Base\n($\\gamma$=7.95)"),
    ("Nutr+", "Nutr$+$\n($\\gamma$=10.15)"),
]


def draw_reference_boundaries(ax):
    theta = np.linspace(0, np.pi / 2, 300)
    ax.plot(np.cos(theta), np.sin(theta), color="black", linewidth=1.4)
    inner_r = math.sqrt(0.5)
    ax.plot(
        inner_r * np.cos(theta),
        inner_r * np.sin(theta),
        color="black",
        linewidth=0.8,
        linestyle=(0, (4, 4)),
    )
    for ang in (np.pi / 8, 3 * np.pi / 8):
        ax.plot(
            [0, math.cos(ang)],
            [0, math.sin(ang)],
            color="black",
            linewidth=0.8,
            linestyle=(0, (4, 4)),
        )
    ax.plot([0, 0], [0, 1], color="black", linewidth=1.0)
    ax.plot([0, 1], [0, 0], color="black", linewidth=1.0)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.02)
    ax.set_aspect("equal")
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.tick_params(length=0, pad=1)
    for spine in ax.spines.values():
        spine.set_visible(False)


def plot_scatter(ax, df, title):
    if len(df) > 0:
        rng = np.random.default_rng(12345)
        jitter = rng.normal(0.0, 0.008, size=(len(df), 2))
        x = np.clip(df["sim_a"].to_numpy() + jitter[:, 0], 0.0, 1.0)
        y = np.clip(df["sim_b"].to_numpy() + jitter[:, 1], 0.0, 1.0)
        colors = df["outcome"].map(OUTCOME_COLORS).to_numpy()
        ax.scatter(
            x,
            y,
            s=18,
            alpha=0.70,
            color=colors,
            edgecolors="white",
            linewidths=0.25,
        )
    draw_reference_boundaries(ax)
    mean_rich = df["richness_c"].mean() if len(df) else float("nan")
    ax.set_title(f"{title}\nmean C richness={mean_rich:.1f}", fontsize=8, pad=4)
    ax.set_xlabel("Sim$(A, C)$", fontsize=8)
    ax.set_ylabel("Sim$(B, C)$", fontsize=8)


def plot_phase_bars(ax, df_all):
    x = np.arange(len(STRENGTHS))
    bottoms = np.zeros(len(STRENGTHS))
    for outcome in OUTCOMES:
        heights = []
        for skey, _ in STRENGTHS:
            sub = df_all[df_all["strength"] == skey]
            heights.append((sub["outcome"] == outcome).mean() * 100.0)
        heights = np.array(heights)
        ax.bar(
            x,
            heights,
            bottom=bottoms,
            color=OUTCOME_COLORS[outcome],
            edgecolor="black",
            linewidth=0.3,
            width=0.7,
            label=outcome,
        )
        if outcome == "Dominance":
            for xi, h in zip(x, heights):
                ax.text(
                    xi,
                    h / 2 if h > 8 else h + 2,
                    f"{h:.0f}%",
                    ha="center",
                    va="center" if h > 8 else "bottom",
                    fontsize=7,
                    color="white" if h > 8 else "black",
                    fontweight="bold",
                )
        bottoms += heights
    ax.set_xticks(x)
    ax.set_xticklabels([label for _, label in STRENGTHS], fontsize=6.5)
    ax.set_ylim(0, 105)
    ax.set_ylabel("% outcomes", fontsize=8)
    ax.set_title("phase diagram", fontsize=8, pad=4)
    sns.despine(ax=ax)


def main():
    df = pd.read_csv(CSV_PATH)
    fig = plt.figure(figsize=(11.5, 3.3))
    gs = fig.add_gridspec(1, 5, wspace=0.35, width_ratios=[1, 1, 1, 0.12, 0.9])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])
    ax_d = fig.add_subplot(gs[0, 4])

    for ax, (skey, slabel) in zip([ax_a, ax_b, ax_c], STRENGTHS):
        plot_scatter(ax, df[df["strength"] == skey], slabel.replace("\n", " "))
    plot_phase_bars(ax_d, df)
    ax_d.legend(
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        frameon=False,
        fontsize=6.5,
        handlelength=1.2,
    )

    for label, ax in zip(["A", "B", "C", "D"], [ax_a, ax_b, ax_c, ax_d]):
        ax.text(
            -0.12,
            1.10,
            label,
            transform=ax.transAxes,
            fontsize=10,
            fontweight="bold",
            ha="right",
            va="bottom",
        )

    fig.suptitle(
        "Q5 / trait-based environmental filtering: gamma-only richness-matched filters",
        fontsize=9.5,
        y=1.07,
    )
    out_base = os.path.join(HERE, "Fig_Q5_phase_filter")
    for ext in ("pdf", "png", "svg"):
        fig.savefig(f"{out_base}.{ext}", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"Wrote {out_base}.pdf")


if __name__ == "__main__":
    main()
