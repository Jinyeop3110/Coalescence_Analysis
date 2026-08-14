#!/usr/bin/env python3
"""Generate Response Fig. R1-2 from strict pH-contrast summary counts."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


LATEX_DIR = Path(__file__).resolve().parents[4]
OUTS = [
    LATEX_DIR / "revision" / "revision_figure_folder" / "Fig_R1_2_acidalk_per_medium.pdf",
    LATEX_DIR / "supplementary_figs" / "Fig_R1_2_acidalk_per_medium.pdf",
]


def pct(n, d):
    return 100 * n / d


def main():
    media = ["Base", "Nutr+"]
    pairs = ["Acid--Alk", "Same pH"]

    # Strict pH thresholds matching Extended Data Fig. 8:
    # acidic pH < 6.5; alkaline pH > 7.5; intermediate-pH pairs excluded.
    #
    # The active response reports Dominance-vs-non-Dominance counts for this
    # strict subset.  The non-Dominance segment is split into Mixture and
    # Restructuring so the display matches the manuscript outcome convention;
    # Fisher tests below compare Dominance against pooled non-Dominance.
    outcomes = {
        "Base": {
            "p": "0.33",
            "or": "0.55",
            "Acid--Alk": {"Dominance": 24, "Mixture": 2, "Restructuring": 15},
            "Same pH": {"Dominance": 23, "Mixture": 1, "Restructuring": 8},
        },
        "Nutr+": {
            "p": "0.018",
            "or": "5.27",
            "Acid--Alk": {"Dominance": 29, "Mixture": 2, "Restructuring": 1},
            "Same pH": {"Dominance": 22, "Mixture": 3, "Restructuring": 9},
        },
    }
    acid_wins = {
        "Base": (23, 41, "56.1%", "0.42"),
        "Nutr+": (29, 32, "90.6%", "0.002"),
    }

    colors = {
        "Dominance_Base": "#9c4428",
        "Dominance_Nutr+": "#e95d2f",
        "Mixture": "#a5d6a7",
        "Restructuring": "#c184cf",
        "Base": "#9c4428",
        "Nutr+": "#f49a7d",
    }

    plt.rcParams.update(
        {
            "font.size": 7.0,
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.linewidth": 0.6,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
        }
    )

    fig = plt.figure(figsize=(6.25, 2.82))
    gs = fig.add_gridspec(
        1,
        4,
        width_ratios=[0.82, 0.82, 0.18, 1.35],
        wspace=0.18,
    )
    axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 3])]

    for ax, medium in zip(axes[:2], media):
        x = np.array([0.0, 0.68])
        bar_width = 0.48
        fractions = {name: [] for name in ["Dominance", "Mixture", "Restructuring"]}
        count_labels = []
        for pair in pairs:
            total = sum(outcomes[medium][pair].values())
            for outcome in fractions:
                fractions[outcome].append(outcomes[medium][pair][outcome] / total)
            count_labels.append(f"n={total}")

        dom_color = colors[f"Dominance_{medium}"]
        bottom = np.zeros(len(pairs))
        for outcome, color in [
            ("Dominance", dom_color),
            ("Mixture", colors["Mixture"]),
            ("Restructuring", colors["Restructuring"]),
        ]:
            vals = np.array(fractions[outcome])
            ax.bar(
                x,
                vals,
                bottom=bottom,
                width=bar_width,
                color=color,
                edgecolor="black",
                linewidth=0.6,
            )
            bottom += vals
        for xi, frac, count_label in zip(x, fractions["Dominance"], count_labels):
            label_color = "white" if frac > 0.35 else "black"
            ax.text(xi, frac / 2, f"{frac*100:.0f}%", ha="center", va="center", fontsize=7, color=label_color, fontweight="bold")
            ax.text(xi, 1.025, count_label, ha="center", va="bottom", fontsize=6.8)
        ax.set_xticks(x)
        ax.set_xticklabels(["Acid-\nAlk", "Same\npH"])
        ax.set_xlim(-0.34, 1.02)
        ax.set_ylim(0, 1.12)
        ax.set_title(medium, color=dom_color, fontsize=7.5, pad=5)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(length=3)
        ax.text(
            0.5,
            -0.33,
            f"Acid-Alk vs same-pH:\nFisher p = {outcomes[medium]['p']}",
            ha="center",
            va="top",
            fontsize=7,
            transform=ax.transAxes,
        )
    axes[0].set_ylabel("Outcome fraction")
    axes[1].set_yticklabels([])

    ax = axes[2]
    rng = np.random.default_rng(42)
    x_positions = np.array([0.0, 0.55])
    for xi, medium in zip(x_positions, media):
        wins, total, label, p_value = acid_wins[medium]
        losses = total - wins
        y = np.array([1] * wins + [-1] * losses, dtype=float)
        jitter = rng.uniform(-0.08, 0.08, size=total)
        ax.scatter(
            np.full(total, xi) + jitter,
            y + rng.normal(0, 0.035, size=total),
            s=12,
            color=colors[medium],
            alpha=0.72,
            edgecolor="none",
            zorder=2,
        )
        mean = float(np.mean(y))
        sem = float(np.std(y, ddof=1) / np.sqrt(total)) if total > 1 else 0.0
        ax.errorbar(
            xi,
            mean,
            yerr=sem,
            fmt="s",
            color="black",
            markerfacecolor=colors[f"Dominance_{medium}"],
            markeredgecolor="black",
            markersize=6,
            capsize=3,
            linewidth=1.1,
            zorder=3,
        )
        ax.text(
            xi,
            1.05,
            f"acid wins\n{label}, p={p_value}",
            ha="center",
            va="bottom",
            fontsize=7,
        )
    ax.axhline(0, color="0.5", linestyle="--", linewidth=0.7)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(media)
    ax.set_xlim(-0.22, 0.77)
    ax.set_ylim(-1.15, 1.36)
    ax.set_title("Acid-Alk pairs only", fontsize=7.5, pad=12)
    ax.set_ylabel("Signed outcome\n(+ acid wins / - alk wins)", labelpad=2)
    ax.spines[["top", "right"]].set_visible(False)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=colors["Dominance_Nutr+"], ec="black", lw=0.6),
        plt.Rectangle((0, 0), 1, 1, color=colors["Mixture"], ec="black", lw=0.6),
        plt.Rectangle((0, 0), 1, 1, color=colors["Restructuring"], ec="black", lw=0.6),
    ]
    fig.legend(
        handles,
        ["Dominance", "Mixture", "Restructuring"],
        frameon=False,
        ncol=3,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.018),
        fontsize=7,
    )
    fig.subplots_adjust(left=0.07, right=0.99, top=0.86, bottom=0.32, wspace=0.45)
    for out in OUTS:
        out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, bbox_inches="tight")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
