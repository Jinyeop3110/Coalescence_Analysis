"""
make_Q5_phase_figures.py
========================

Per-model phase-diagram figures for the pH-feedback control analysis:

    - Scatter panels on the left, one per interaction-strength level
      (weak / mid / strong), each showing per-event points in the
      Sim(A,C)-Sim(B,C) plane with the paper's classifier boundaries
      overlaid (outer quarter-arc r=1, inner quarter-arc r=1/sqrt(2),
      two radial dashed lines at pi/8 and 3*pi/8).
    - A stacked-bar "phase diagram" panel on the right summarizing
      Dominance / Mixture / Restructuring fractions across the three
      strength levels.

One figure is produced per model (gLV, pH-feedback, pH+LV hybrid) so
each model's behavior across strength is readable in isolation.

Input : Q5_phase_events.csv (produced by simulate_Q5_phase_diagrams.py)
Output:
    Fig_Q5_phase_gLV.{pdf,svg,png}
    Fig_Q5_phase_pH.{pdf,svg,png}
    Fig_Q5_phase_hybrid.{pdf,svg,png}
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
CSV_PATH = os.path.join(HERE, "Q5_phase_events.csv")

sns.set_style("ticks")
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['text.usetex'] = False

# Use the paper's outcome palette in both scatter and phase bars. The pH
# panels often place many events exactly at (0,0), (1,0), or (0,1); class
# color plus tiny deterministic jitter keeps those dense piles visible.
OUTCOME_COLORS = {
    "Dominance":     "#1f77b4",
    "Mixture":       "#9ecae1",
    "Restructuring": "#d62728",
}
OUTCOMES = ["Dominance", "Mixture", "Restructuring"]

STRENGTHS = [("weak",   "weak\n($\\mu$=0.3,$c_{max}$=1e-10)"),
             ("mid",    "mid\n($\\mu$=0.6,$c_{max}$=1e-9)"),
             ("strong", "strong\n($\\mu$=0.9,$c_{max}$=3e-8)")]

MODELS = [("gLV",    "gLV baseline"),
          ("pH",     "pH-feedback"),
          ("hybrid", "pH+LV hybrid")]


def draw_reference_boundaries(ax):
    """Copy of the R3-2.0 boundary recipe: outer arc + inner arc at
    r=1/sqrt(2) + two dashed radial lines at pi/8, 3*pi/8."""
    theta = np.linspace(0, np.pi / 2, 300)
    ax.plot(np.cos(theta), np.sin(theta),
            color="black", linewidth=1.4)
    inner_r = math.sqrt(0.5)
    ax.plot(inner_r * np.cos(theta), inner_r * np.sin(theta),
            color="black", linewidth=0.8, linestyle=(0, (4, 4)))
    for ang in (np.pi / 8, 3 * np.pi / 8):
        ax.plot([0, math.cos(ang)], [0, math.sin(ang)],
                color="black", linewidth=0.8, linestyle=(0, (4, 4)))
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
        # Deterministic visual jitter only; does not alter source data.
        rng = np.random.default_rng(12345)
        jitter = rng.normal(0.0, 0.008, size=(len(df), 2))
        x = np.clip(df["sim_a"].to_numpy() + jitter[:, 0], 0.0, 1.0)
        y = np.clip(df["sim_b"].to_numpy() + jitter[:, 1], 0.0, 1.0)
        colors = df["outcome"].map(OUTCOME_COLORS).to_numpy()
        ax.scatter(x, y, s=20, alpha=0.72, color=colors,
                   edgecolors="white", linewidths=0.25)
    draw_reference_boundaries(ax)
    ax.set_title(title, fontsize=8, pad=4)
    ax.set_xlabel("Sim$(A, C)$", fontsize=8)
    ax.set_ylabel("Sim$(B, C)$", fontsize=8)


def plot_phase_bars(ax, df_model):
    x = np.arange(len(STRENGTHS))
    bottoms = np.zeros(len(STRENGTHS))
    for outcome in OUTCOMES:
        heights = []
        for (skey, _) in STRENGTHS:
            sub = df_model[df_model["strength"] == skey]
            if len(sub) == 0:
                heights.append(0.0)
            else:
                heights.append((sub["outcome"] == outcome).mean() * 100.0)
        heights = np.array(heights)
        ax.bar(x, heights, bottom=bottoms,
               color=OUTCOME_COLORS[outcome], edgecolor="black",
               linewidth=0.3, width=0.7, label=outcome)
        if outcome == "Dominance":
            for xi, h in zip(x, heights):
                ax.text(xi, h / 2 if h > 8 else h + 2,
                        f"{h:.0f}%",
                        ha="center",
                        va="center" if h > 8 else "bottom",
                        fontsize=7,
                        color="white" if h > 8 else "black",
                        fontweight="bold")
        bottoms += heights
    ax.set_xticks(x)
    ax.set_xticklabels([s[1] for s in STRENGTHS], fontsize=6.5)
    ax.set_ylim(0, 105)
    ax.set_ylabel("% outcomes", fontsize=8)
    ax.set_title("phase diagram", fontsize=8, pad=4)
    sns.despine(ax=ax)


def make_one(df_all, model_key, model_label):
    df = df_all[df_all["model"] == model_key]
    fig = plt.figure(figsize=(11.5, 3.3))
    gs = fig.add_gridspec(1, 5, wspace=0.35,
                          width_ratios=[1, 1, 1, 0.12, 0.9])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])
    # gs[0, 3] is a spacer
    ax_d = fig.add_subplot(gs[0, 4])

    for ax, (skey, slabel) in zip([ax_a, ax_b, ax_c], STRENGTHS):
        sub = df[df["strength"] == skey]
        plot_scatter(ax, sub, slabel.replace("\n", " "))

    plot_phase_bars(ax_d, df)

    ax_d.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0),
                frameon=False, fontsize=6.5, handlelength=1.2)

    # panel letters
    letters = ["A", "B", "C", "D"]
    for idx, ax in enumerate([ax_a, ax_b, ax_c, ax_d]):
        ax.text(-0.12, 1.10, letters[idx], transform=ax.transAxes,
                fontsize=10, fontweight="bold", ha="right", va="bottom")

    fig.suptitle(f"{model_label}: phase diagram across interaction-strength levels",
                 fontsize=9.5, y=1.05)

    out_base = os.path.join(HERE, f"Fig_Q5_phase_{model_key}")
    for ext in ("pdf", "png", "svg"):
        fig.savefig(f"{out_base}.{ext}", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"Wrote {out_base}.pdf")


def main():
    df = pd.read_csv(CSV_PATH)
    for mkey, mlabel in MODELS:
        make_one(df, mkey, mlabel)


if __name__ == "__main__":
    main()
