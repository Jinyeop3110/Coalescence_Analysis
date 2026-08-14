#!/usr/bin/env python3
"""Post-stabilization taxonomic distinctness of natural sample-derived communities.

This response-only analysis asks whether the natural communities, after seven
serial dilution cycles in defined media, are taxonomically indistinguishable
across environmental source samples. It does not test convergence during
stabilization because no pre-stabilization ASV table is available in the
processed dataset.
"""

from pathlib import Path
from itertools import combinations

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[9]
COMMUNITIES_PATH = ROOT / "Analyzed" / "processed_Communities_natural.xlsx"
SEQUENCES_PATH = ROOT / "Postprocessed" / "processed_Sequences_natural.xlsx"
OUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

THRESHOLD = 0.001
MEDIA = [("L", "Nutr-"), ("M", "Base"), ("H", "Nutr+")]
COLORS = {"L": "#A7216A", "M": "#802000", "H": "#E24912"}


def bray_curtis_similarity(a, b):
    denom = np.sum(a + b)
    if denom == 0:
        return np.nan
    return 1.0 - np.sum(np.abs(a - b)) / denom


def jaccard_similarity(a, b, threshold=THRESHOLD):
    pa = a > threshold
    pb = b > threshold
    union = np.sum(pa | pb)
    if union == 0:
        return np.nan
    return np.sum(pa & pb) / union


def load_parental_natural():
    communities = pd.read_excel(COMMUNITIES_PATH)
    sequences = pd.read_excel(SEQUENCES_PATH)
    abundance_cols = [c for c in sequences.columns if c != "SampleIDX"]

    natural_parental = communities[
        (communities["CommunityOrigin"] == "N")
        & (communities["CoalescenceType"] == "S")
        & (communities["Timepoint"] == "F")
    ].copy()

    merged = natural_parental.merge(sequences, on="SampleIDX", how="inner")
    records = []
    for _, row in merged.iterrows():
        abund = row[abundance_cols].to_numpy(dtype=float)
        total = np.sum(abund)
        if total > 0:
            abund = abund / total
        records.append(
            {
                "sample_idx": row["SampleIDX"],
                "medium": row["Medium"],
                "community_idx": int(row["CommunityIDX"]),
                "replicate": int(row["Replicate"]),
                "richness": int(np.sum(abund > THRESHOLD)),
                "abundance": abund,
            }
        )
    return records


def pairwise_metrics(records):
    rows = []
    for medium, _ in MEDIA:
        medium_records = [r for r in records if r["medium"] == medium]
        for a, b in combinations(medium_records, 2):
            group = (
                "same source"
                if a["community_idx"] == b["community_idx"]
                else "different source"
            )
            rows.append(
                {
                    "medium": medium,
                    "group": group,
                    "jaccard": jaccard_similarity(a["abundance"], b["abundance"]),
                    "bray_curtis_similarity": bray_curtis_similarity(
                        a["abundance"], b["abundance"]
                    ),
                }
            )
    return pd.DataFrame(rows)


def write_summary(records, metrics):
    richness = np.array([r["richness"] for r in records], dtype=float)
    lines = [
        "Post-stabilization natural community taxonomic summary",
        f"Input communities: {COMMUNITIES_PATH}",
        f"Input ASV table: {SEQUENCES_PATH}",
        f"Richness threshold: {THRESHOLD:.4f} relative abundance",
        f"Natural parental communities analyzed: n = {len(records)}",
        f"ASV richness, mean +/- SD: {richness.mean():.2f} +/- {richness.std(ddof=0):.2f}",
        "",
        "Pairwise similarity among stabilized natural parental communities:",
    ]
    for medium, label in MEDIA:
        sub = metrics[metrics["medium"] == medium]
        for group in ["same source", "different source"]:
            vals_j = sub[sub["group"] == group]["jaccard"].dropna().to_numpy()
            vals_b = (
                sub[sub["group"] == group]["bray_curtis_similarity"]
                .dropna()
                .to_numpy()
            )
            lines.append(
                f"{label}, {group}: Jaccard {vals_j.mean():.3f} +/- {vals_j.std(ddof=0):.3f} "
                f"(n={len(vals_j)}); Bray-Curtis similarity {vals_b.mean():.3f} +/- "
                f"{vals_b.std(ddof=0):.3f} (n={len(vals_b)})"
            )
    lines.extend(
        [
            "",
            "Limitation: the processed data contain only final stabilized communities",
            "and coalesced communities, not environmental inocula before stabilization.",
            "Therefore this analysis cannot measure taxonomic convergence during",
            "stabilization or functional guild convergence.",
        ]
    )
    (OUT_DIR / "post_stabilization_taxonomic_summary.txt").write_text(
        "\n".join(lines) + "\n"
    )


def plot(metrics):
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 8,
            "axes.linewidth": 0.6,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "xtick.direction": "in",
            "ytick.direction": "in",
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(6.7, 2.6), sharey=False)
    metric_specs = [
        ("jaccard", "ASV Jaccard similarity"),
        ("bray_curtis_similarity", "Bray-Curtis similarity"),
    ]
    rng = np.random.default_rng(7)

    for ax, (metric, ylabel) in zip(axes, metric_specs):
        positions = []
        labels = []
        data = []
        colors = []
        pos = 0
        for medium, label in MEDIA:
            for group in ["same source", "different source"]:
                vals = metrics[
                    (metrics["medium"] == medium) & (metrics["group"] == group)
                ][metric].dropna()
                positions.append(pos)
                labels.append(f"{label}\n{group}")
                data.append(vals)
                colors.append(COLORS[medium])
                pos += 1
            pos += 0.6

        bp = ax.boxplot(
            data,
            positions=positions,
            widths=0.5,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "black", "linewidth": 0.8},
            whiskerprops={"linewidth": 0.6},
            capprops={"linewidth": 0.6},
            boxprops={"linewidth": 0.6},
        )
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.25)
            patch.set_edgecolor(color)

        for xpos, vals, color in zip(positions, data, colors):
            jitter = rng.normal(0, 0.055, len(vals))
            ax.scatter(
                np.full(len(vals), xpos) + jitter,
                vals,
                s=11,
                color=color,
                alpha=0.65,
                linewidth=0,
            )

        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_ylabel(ylabel)
        ax.set_ylim(-0.03, 1.03)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].text(-0.16, 1.05, "a", transform=axes[0].transAxes, fontweight="bold")
    axes[1].text(-0.16, 1.05, "b", transform=axes[1].transAxes, fontweight="bold")
    fig.tight_layout(w_pad=1.3)
    fig.savefig(OUT_DIR / "post_stabilization_taxonomic_distinctness.pdf")
    fig.savefig(OUT_DIR / "post_stabilization_taxonomic_distinctness.png", dpi=300)
    plt.close(fig)


def main():
    records = load_parental_natural()
    metrics = pairwise_metrics(records)
    write_summary(records, metrics)
    plot(metrics)


if __name__ == "__main__":
    main()
