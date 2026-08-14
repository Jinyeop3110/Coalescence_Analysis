#!/usr/bin/env python3
"""Generate the three-bar outcome comparison proposed for main Figure 1.

The artwork is intentionally self-contained and sized as a compact figure panel
for placement in Illustrator. PDF text is stored as editable TrueType text.
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch


HERE = Path(__file__).resolve().parent
OUT_STEM = HERE / "fig1_outcome_comparison"

# Counts shown in the proposed panel. Segment order is bottom to top.
GROUPS = [
    ("Coalescence", (54, 3, 26)),
    ("Direct\nAssembly", (18, 4, 35)),
    ("Null model", (17, 66, 0)),
]

COLORS = {
    "Dominance": "#E57373",
    "Mixture": "#81C784",
    "Restructuring": "#BA68C8",
}
OUTCOMES = tuple(COLORS)


def add_dominance_bracket(ax, y_top: float) -> None:
    """Draw the compact left-side bracket used in the visual reference."""
    x_outer = -0.49
    x_inner = -0.34
    radius = 0.012
    vertices = [
        (x_inner, 0.006),
        (x_outer + radius, 0.006),
        (x_outer, 0.006),
        (x_outer, 0.006 + radius),
        (x_outer, y_top - radius),
        (x_outer, y_top),
        (x_outer + radius, y_top),
        (x_inner, y_top),
    ]
    codes = [
        MplPath.MOVETO,
        MplPath.LINETO,
        MplPath.CURVE3,
        MplPath.CURVE3,
        MplPath.LINETO,
        MplPath.CURVE3,
        MplPath.CURVE3,
        MplPath.LINETO,
    ]
    ax.add_patch(
        PathPatch(
            MplPath(vertices, codes),
            fill=False,
            color="black",
            linewidth=0.85,
            capstyle="round",
            joinstyle="round",
            clip_on=False,
        )
    )
    ax.text(
        x_outer - 0.135,
        y_top / 2,
        "Dominance",
        rotation=90,
        ha="center",
        va="center",
        fontsize=9.0,
    )


def format_percent(count: int, total: int) -> str:
    return f"{100 * count / total:.1f}%"


def render_outcome_comparison(
    groups: list[tuple[str, tuple[int, int, int]]],
    out_stem: Path,
    title: str | None = None,
    labels_at_top: bool = True,
) -> None:
    """Render one three-bar Dominance/Mixture/Restructuring comparison."""
    mpl.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 8,
            "axes.linewidth": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )

    # The untitled 0.92 aspect ratio follows the supplied visual reference.
    fig_height = 3.70 if title else 3.48
    fig, ax = plt.subplots(figsize=(3.20, fig_height))
    x_positions = (0.00, 0.78, 1.56)
    bar_width = 0.42

    if len(groups) != len(x_positions):
        raise ValueError("The comparison layout requires exactly three groups")

    for x, (_, counts) in zip(x_positions, groups):
        total = sum(counts)
        bottom = 0.0
        for outcome, count in zip(OUTCOMES, counts):
            fraction = count / total
            if count:
                ax.bar(
                    x,
                    fraction,
                    width=bar_width,
                    bottom=bottom,
                    color=COLORS[outcome],
                    edgecolor="white",
                    linewidth=0.75,
                    zorder=2,
                )
            bottom += fraction

        # Keep labels centered in the same major segments as the mock-up.
        dominance_y = counts[0] / total / 2
        restructuring_y = (counts[0] + counts[1]) / total + counts[2] / total / 2
        labels = [
            (dominance_y, counts[0], x == x_positions[0]),
            (restructuring_y, counts[2], False),
        ]
        if counts[2] == 0:  # additive null: label its large Mixture segment
            mixture_y = counts[0] / total + counts[1] / total / 2
            labels = [(dominance_y, counts[0], False), (mixture_y, counts[1], False)]

        for y, count, bold in labels:
            # Keep the two-line label legible when a bottom segment is tiny,
            # as in the simulation additive null (1/499 Dominance events).
            display_y = max(y, 0.045)
            ax.text(
                x,
                display_y,
                f"{format_percent(count, total)}\n({count}/{total})",
                ha="center",
                va="center",
                fontsize=7.25,
                fontweight="bold" if bold else "normal",
                linespacing=1.05,
                zorder=4,
            )

    observed_dominance = groups[0][1][0] / sum(groups[0][1])

    # Reference line and restrained frame reproduce the supplied composition.
    ax.axhline(
        observed_dominance,
        xmin=0.078,
        xmax=0.945,
        color="black",
        linewidth=0.8,
        linestyle=(0, (4, 3)),
        zorder=3,
    )
    ax.hlines(1.0, -0.36, 1.90, color="black", linewidth=0.85, zorder=5)
    ax.hlines(0.0, -0.36, 1.90, color="black", linewidth=0.85, zorder=5)
    add_dominance_bracket(ax, observed_dominance)

    ax.set_xlim(-0.60, 2.02)
    ax.set_ylim(-0.005, 1.105)
    ax.set_xticks(x_positions)
    ax.set_xticklabels([group[0] for group in groups], fontsize=8.5, linespacing=1.0)
    ax.tick_params(
        axis="x",
        top=labels_at_top,
        bottom=True,
        labeltop=labels_at_top,
        labelbottom=not labels_at_top,
        direction="in",
        length=2.4,
        width=0.65,
        pad=5.5,
    )
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    if title:
        fig.suptitle(title, x=0.57, y=0.985, fontsize=9.0)
        if labels_at_top:
            fig.subplots_adjust(left=0.15, right=0.99, bottom=0.025, top=0.82)
        else:
            fig.subplots_adjust(left=0.15, right=0.99, bottom=0.15, top=0.90)
    else:
        fig.subplots_adjust(left=0.15, right=0.99, bottom=0.025, top=0.91)
    fig.savefig(out_stem.with_suffix(".pdf"), transparent=True)
    fig.savefig(out_stem.with_suffix(".svg"), transparent=True)
    fig.savefig(out_stem.with_suffix(".png"), dpi=400, transparent=False)
    plt.close(fig)

    for group, counts in groups:
        total = sum(counts)
        summary = ", ".join(
            f"{outcome} {count}/{total} ({format_percent(count, total)})"
            for outcome, count in zip(OUTCOMES, counts)
        )
        print(f"{group.replace(chr(10), ' ')}: {summary}")
    print(f"Saved {out_stem}.pdf, .svg, and .png")


def main() -> None:
    render_outcome_comparison(GROUPS, OUT_STEM)


if __name__ == "__main__":
    main()
