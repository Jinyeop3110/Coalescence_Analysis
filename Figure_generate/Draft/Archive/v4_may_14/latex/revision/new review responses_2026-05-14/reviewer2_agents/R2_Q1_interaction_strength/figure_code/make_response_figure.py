#!/usr/bin/env python3
"""Generate the Reviewer 2 Q1 response figure.

The figure is intentionally a compact synthesis of values already reported in
the v4 manuscript and revision memos. It does not perform a new statistical
analysis.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def setup_style():
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 8,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def add_panel_label(ax, label):
    ax.text(
        -0.15,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="top",
        ha="left",
    )


def main():
    setup_style()

    media = ["Nutr-", "Base", "Nutr+"]
    x = np.arange(len(media))
    colors = ["#b85bbf", "#7a5a42", "#d9822b"]

    # Values from v4 Results/Figs. 4 and 5 and R1_2/R3_2 revision memos.
    failed_invasion = np.array([2, 33, 48])
    failed_invasion_sem = np.array([1, 4, 4])
    dominance = np.array([39, 65, 76])
    mixture = np.array([53, 4, 6])
    dominant_asv = np.array([44, 51, 67])
    dominant_asv_sem = np.array([2, 5, 4])
    parental_richness_median = np.array([12.0, 9.0, 7.5])
    acid_win = np.array([63.6, 86.4])
    acid_win_x = np.array([1, 2])

    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.35), constrained_layout=True)

    ax = axes[0]
    ax.errorbar(
        x,
        failed_invasion,
        yerr=failed_invasion_sem,
        color="#1f4f78",
        marker="o",
        linewidth=1.8,
        capsize=3,
        label="Failed invasions",
    )
    ax.plot(x, dominance, color="#aa2e25", marker="s", linewidth=1.8, label="Dominance")
    ax.plot(x, mixture, color="#2f7d55", marker="^", linewidth=1.4, label="Mixture")
    ax.set_xticks(x)
    ax.set_xticklabels(media)
    ax.set_ylim(0, 85)
    ax.set_ylabel("Fraction of events or assays (%)")
    ax.set_title("Outcome-level interaction intensity")
    ax.legend(frameon=False, loc="upper left", fontsize=7)
    add_panel_label(ax, "A")

    ax = axes[1]
    width = 0.36
    ax.bar(
        x - width / 2,
        dominant_asv,
        width,
        yerr=dominant_asv_sem,
        capsize=3,
        color=colors,
        edgecolor="black",
        linewidth=0.5,
        label="Dominant ASV abundance",
    )
    ax.set_ylim(0, 80)
    ax.set_ylabel("Dominant ASV abundance (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(media)
    ax.set_title("Network restructuring with enrichment")
    ax2 = ax.twinx()
    ax2.plot(
        x + width / 2,
        parental_richness_median,
        color="black",
        marker="D",
        linewidth=1.5,
        label="Median parental richness",
    )
    ax2.set_ylim(0, 14)
    ax2.set_ylabel("Median parental richness")
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, frameon=False, loc="upper right", fontsize=7)
    add_panel_label(ax, "B")

    ax = axes[2]
    ax.bar(
        acid_win_x,
        acid_win,
        color=[colors[1], colors[2]],
        edgecolor="black",
        linewidth=0.5,
        width=0.55,
    )
    ax.axhline(50, color="0.4", linestyle="--", linewidth=1)
    ax.text(0.93, 52, "50% null", fontsize=7, color="0.3")
    ax.text(1, acid_win[0] + 4, "p = 0.10", ha="center", va="bottom", fontsize=7)
    ax.text(2, acid_win[1] + 4, "p = 9.4e-7", ha="center", va="bottom", fontsize=7)
    ax.set_xlim(0.35, 2.65)
    ax.set_ylim(0, 100)
    ax.set_xticks(acid_win_x)
    ax.set_xticklabels(["Base", "Nutr+"])
    ax.set_ylabel("Acidic parent wins acid-alk pairs (%)")
    ax.set_title("Environmental feedback route")
    add_panel_label(ax, "C")

    for axis in axes:
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
    axes[1].spines["right"].set_visible(True)
    axes[1].spines["top"].set_visible(False)

    for suffix in ["pdf", "png"]:
        fig.savefig(OUT_DIR / f"r2_q1_nutrient_interaction_feedback.{suffix}", dpi=300)


if __name__ == "__main__":
    main()
