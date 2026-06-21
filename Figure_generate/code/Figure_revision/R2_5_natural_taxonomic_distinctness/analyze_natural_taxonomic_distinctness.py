#!/usr/bin/env python3
"""Taxonomic distinctness checks for natural sample-derived communities.

This response-only analysis addresses whether natural-community coalescence
outcomes can be explained by complete medium-driven taxonomic convergence after
laboratory enrichment. It uses only post-stabilization 16S data, so it cannot
measure pre-to-post stabilization convergence directly.
"""

from itertools import combinations
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = Path(__file__).resolve().parent
COMMUNITIES_PATH = ROOT / "Analyzed" / "processed_Communities_natural.xlsx"
EVENTS_PATH = ROOT / "Analyzed" / "processed_CoalescenceEvent_natural.xlsx"
SEQUENCES_PATH = ROOT / "Postprocessed" / "processed_Sequences_natural.xlsx"
RAW_OTU_PATH = ROOT / "SEQanalysis" / "onlyNatural" / "M_OTUtableGreenGenes.csv"
RAW_TAXONOMY_PATH = ROOT / "SEQanalysis" / "onlyNatural" / "M_TAXAtableGreenGenes.csv"

THRESHOLD = 0.001
MEDIA = [("L", "Nutr-"), ("M", "Base"), ("H", "Nutr+")]
COLORS = {"L": "#A7216A", "M": "#802000", "H": "#E24912"}


def normalize(v):
    v = np.asarray(v, dtype=float)
    total = v.sum()
    return v / total if total > 0 else v


def richness(v):
    return int(np.sum(v > THRESHOLD))


def jaccard_similarity(a, b):
    pa = a > THRESHOLD
    pb = b > THRESHOLD
    union = np.sum(pa | pb)
    return np.nan if union == 0 else np.sum(pa & pb) / union


def bray_curtis_similarity(a, b):
    denom = np.sum(a + b)
    return np.nan if denom == 0 else 1.0 - np.sum(np.abs(a - b)) / denom


def rank_labels(taxonomy, rank):
    """Return taxonomy labels, keeping unresolved ASVs distinct at each rank."""
    labels = []
    for asv, label in zip(taxonomy["ASV"], taxonomy[rank]):
        if pd.isna(label) or str(label).strip() in {"", "NA", "nan", "None"}:
            labels.append(f"Unresolved {rank} {asv}")
        else:
            labels.append(str(label).strip())
    return np.asarray(labels)


def load_data():
    communities = pd.read_excel(COMMUNITIES_PATH)
    events = pd.read_excel(EVENTS_PATH)
    sequences = pd.read_csv(RAW_OTU_PATH)
    taxonomy = pd.read_csv(RAW_TAXONOMY_PATH)
    sample_col = sequences.columns[0]
    abundance_cols = [c for c in sequences.columns if c.startswith("ASV")]
    taxonomy = taxonomy.set_index("Unnamed: 0").loc[abundance_cols].reset_index()
    taxonomy = taxonomy.rename(columns={"Unnamed: 0": "ASV"})
    sequences["SampleIDX"] = (
        sequences[sample_col]
        .astype(str)
        .str.replace("_F_filt.fastq.gz", "", regex=False)
    )
    seq_map = {
        row["SampleIDX"]: normalize(row[abundance_cols].to_numpy(dtype=float))
        for _, row in sequences.iterrows()
    }
    collapsed_maps = {"ASV": seq_map}
    for rank in ["Genus", "Family", "Phylum"]:
        labels = rank_labels(taxonomy, rank)
        unique_labels = pd.Index(labels).drop_duplicates().to_list()
        collapsed = {}
        for sample, abund in seq_map.items():
            vals = np.zeros(len(unique_labels), dtype=float)
            for i, label in enumerate(unique_labels):
                vals[i] = abund[labels == label].sum()
            collapsed[sample] = normalize(vals)
        collapsed_maps[rank] = collapsed

    parental = communities[
        (communities["CommunityOrigin"] == "N")
        & (communities["CoalescenceType"] == "S")
        & (communities["Timepoint"] == "F")
    ].copy()
    coalesced = events[
        (events["CommunityOrigin"] == "N")
        & (events["CoalescenceType"] == "C")
        & (events["Timepoint"] == "F")
    ].copy()
    return parental, coalesced, collapsed_maps


def richness_table(parental, coalesced, seq_map, level):
    rows = []
    for kind, frame in [("parental", parental), ("coalesced", coalesced)]:
        for _, row in frame.iterrows():
            sample = row["SampleIDX"]
            if sample not in seq_map:
                continue
            rows.append(
                {
                    "kind": kind,
                    "level": level,
                    "medium": row["Medium"],
                    "richness": richness(seq_map[sample]),
                }
            )
    return pd.DataFrame(rows)


def parental_pairwise_table(parental, seq_map, level):
    rows = []
    for medium, _ in MEDIA:
        sub = parental[parental["Medium"] == medium]
        for _, a in sub.iterrows():
            for _, b in sub.iterrows():
                if a["SampleIDX"] >= b["SampleIDX"]:
                    continue
                va = seq_map[a["SampleIDX"]]
                vb = seq_map[b["SampleIDX"]]
                group = (
                    "same source"
                    if int(a["CommunityIDX"]) == int(b["CommunityIDX"])
                    else "different source"
                )
                rows.append(
                    {
                        "medium": medium,
                        "level": level,
                        "group": group,
                        "jaccard": jaccard_similarity(va, vb),
                        "bray": bray_curtis_similarity(va, vb),
                    }
                )
    return pd.DataFrame(rows)


def coalesced_pairwise_table(coalesced, seq_map, level):
    rows = []
    for medium, _ in MEDIA:
        ids = [s for s in coalesced[coalesced["Medium"] == medium]["SampleIDX"] if s in seq_map]
        for a, b in combinations(ids, 2):
            rows.append(
                {
                    "medium": medium,
                    "level": level,
                    "jaccard": jaccard_similarity(seq_map[a], seq_map[b]),
                    "bray": bray_curtis_similarity(seq_map[a], seq_map[b]),
                }
            )
    return pd.DataFrame(rows)


def own_parent_table(parental, coalesced, seq_map, level):
    rows = []
    for _, ev in coalesced.iterrows():
        sample = ev["SampleIDX"]
        if sample not in seq_map:
            continue
        own_ids = [ev["SampleIDX_Sub1"], ev["SampleIDX_Sub2"]]
        own_ids = [sid for sid in own_ids if sid in seq_map]
        unrelated_ids = [
            sid
            for sid in parental[parental["Medium"] == ev["Medium"]]["SampleIDX"]
            if sid in seq_map and sid not in own_ids
        ]
        if len(own_ids) != 2 or not unrelated_ids:
            continue

        vc = seq_map[sample]
        own_j = np.mean([jaccard_similarity(vc, seq_map[sid]) for sid in own_ids])
        own_b = np.mean([bray_curtis_similarity(vc, seq_map[sid]) for sid in own_ids])
        un_j = np.mean([jaccard_similarity(vc, seq_map[sid]) for sid in unrelated_ids])
        un_b = np.mean([bray_curtis_similarity(vc, seq_map[sid]) for sid in unrelated_ids])
        rows.extend(
            [
                {
                    "event": sample,
                    "medium": ev["Medium"],
                    "level": level,
                    "comparison": "own parents",
                    "jaccard": own_j,
                    "bray": own_b,
                },
                {
                    "event": sample,
                    "medium": ev["Medium"],
                    "level": level,
                    "comparison": "unrelated parents",
                    "jaccard": un_j,
                    "bray": un_b,
                },
            ]
        )
    return pd.DataFrame(rows)


def jittered_box(ax, groups, positions, colors, ylabel, ylim=None):
    rng = np.random.default_rng(11)
    bp = ax.boxplot(
        groups,
        positions=positions,
        widths=0.42,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 0.8},
        whiskerprops={"linewidth": 0.6},
        capprops={"linewidth": 0.6},
        boxprops={"linewidth": 0.6},
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.22)
        patch.set_edgecolor(color)
    for xpos, vals, color in zip(positions, groups, colors):
        vals = np.asarray(vals, dtype=float)
        jitter = rng.normal(0, 0.045, len(vals))
        ax.scatter(np.full(len(vals), xpos) + jitter, vals, s=9, color=color, alpha=0.55, linewidth=0)
    ax.set_ylabel(ylabel)
    if ylim is not None:
        ax.set_ylim(*ylim)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot(richness_df, parental_pairs, coalesced_pairs, own_parent):
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
    fig, axes = plt.subplots(2, 3, figsize=(8.6, 5.6))

    def plot_richness(ax, level, ylabel):
        groups, positions, colors, labels = [], [], [], []
        pos = 0
        for medium, label in MEDIA:
            for kind in ["parental", "coalesced"]:
                vals = richness_df[
                    (richness_df["level"] == level)
                    & (richness_df["medium"] == medium)
                    & (richness_df["kind"] == kind)
                ]["richness"].to_numpy()
                groups.append(vals)
                positions.append(pos)
                colors.append(COLORS[medium])
                labels.append(f"{label}\n{kind}")
                pos += 1
            pos += 0.55
        jittered_box(ax, groups, positions, colors, ylabel, ylim=(0, None))
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=45, ha="right")

    def plot_pairwise(ax, level, ylabel):
        groups, positions, colors, labels = [], [], [], []
        pos = 0
        for medium, label in MEDIA:
            medium_positions = []
            vals_same_parental = parental_pairs[
                (parental_pairs["level"] == level)
                & (parental_pairs["medium"] == medium)
                & (parental_pairs["group"] == "same source")
            ]["jaccard"].to_numpy()
            vals_diff_parental = parental_pairs[
                (parental_pairs["level"] == level)
                & (parental_pairs["medium"] == medium)
                & (parental_pairs["group"] == "different source")
            ]["jaccard"].to_numpy()
            vals_coalesced = coalesced_pairs[
                (coalesced_pairs["level"] == level)
                & (coalesced_pairs["medium"] == medium)
            ]["jaccard"].to_numpy()
            for vals, kind in [
                (vals_same_parental, "S"),
                (vals_diff_parental, "D"),
                (vals_coalesced, "C"),
            ]:
                groups.append(vals)
                positions.append(pos)
                colors.append(COLORS[medium])
                labels.append(kind)
                medium_positions.append(pos)
                ax.text(
                    pos,
                    1.0,
                    f"n={len(vals)}",
                    ha="center",
                    va="top",
                    fontsize=5.5,
                    color="#666666",
                )
                pos += 1
            ax.text(
                np.mean(medium_positions),
                -0.33,
                label,
                ha="center",
                va="top",
                transform=ax.get_xaxis_transform(),
            )
            pos += 0.55
        jittered_box(ax, groups, positions, colors, ylabel, ylim=(-0.03, 1.03))
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=0, ha="center")

    def plot_own_parent(ax, level, metric, ylabel):
        positions = []
        labels = []
        pos = 0
        for medium, label in MEDIA:
            sub = own_parent[
                (own_parent["level"] == level)
                & (own_parent["medium"] == medium)
            ]
            own = sub[sub["comparison"] == "own parents"].sort_values("event")
            unrelated = sub[sub["comparison"] == "unrelated parents"].sort_values("event")
            x_own = pos
            x_un = pos + 0.48
            own_vals = own[metric].to_numpy(dtype=float)
            un_vals = unrelated[metric].to_numpy(dtype=float)
            n_ev = len(own_vals)
            if n_ev >= 1 and len(un_vals) == n_ev:
                try:
                    pval = wilcoxon(own_vals, un_vals, alternative="greater").pvalue
                    ptxt = "p<0.001" if pval < 1e-3 else f"p={pval:.3f}"
                except ValueError:
                    ptxt = "p=n/a"
            else:
                ptxt = "p=n/a"
            ax.text(
                (x_own + x_un) / 2,
                1.0,
                f"{ptxt}\nn={n_ev}",
                ha="center",
                va="top",
                fontsize=5.5,
                color="#333333",
            )
            for (_, row_o), (_, row_u) in zip(own.iterrows(), unrelated.iterrows()):
                ax.plot([x_own, x_un], [row_o[metric], row_u[metric]], color="#BDBDBD", linewidth=0.45, zorder=1)
            for x, vals, color in [
                (x_own, own[metric].to_numpy(), COLORS[medium]),
                (x_un, unrelated[metric].to_numpy(), "#808080"),
            ]:
                ax.scatter(
                    np.full(len(vals), x) + np.random.default_rng(17).normal(0, 0.025, len(vals)),
                    vals,
                    s=11,
                    color=color,
                    alpha=0.7,
                    linewidth=0,
                    zorder=2,
                )
            positions.extend([x_own, x_un])
            labels.extend([f"{label}\nown", "unrel."])
            pos += 1.35
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_ylabel(ylabel)
        ax.set_ylim(-0.03, 1.03)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plot_richness(axes[0, 0], "ASV", "ASV richness")
    plot_richness(axes[1, 0], "Genus", "Genus richness")
    plot_pairwise(axes[0, 1], "ASV", "Pairwise ASV\nJaccard similarity")
    plot_pairwise(axes[1, 1], "Genus", "Pairwise Genus\nJaccard similarity")
    plot_own_parent(axes[0, 2], "ASV", "jaccard", "Outcome-parent\nASV Jaccard similarity")
    plot_own_parent(axes[1, 2], "Genus", "jaccard", "Outcome-parent\nGenus Jaccard similarity")

    for ax, title in zip(
        axes[0],
        [
            "Richness",
            "Post-stabilization baseline\nand outcome distinctness",
            "Final outcome\nparental signal",
        ],
    ):
        ax.set_title(title, fontsize=8.5, pad=8)

    for letter, ax in zip("abcdef", axes.flat):
        ax.text(-0.16, 1.05, letter, transform=ax.transAxes, fontweight="bold")

    fig.tight_layout(w_pad=1.2, h_pad=1.1)
    fig.savefig(OUT_DIR / "Fig_R2_5_natural_taxonomic_distinctness.pdf")
    fig.savefig(OUT_DIR / "Fig_R2_5_natural_taxonomic_distinctness.png", dpi=300)
    plt.close(fig)


def write_summary(richness_df, parental_pairs, coalesced_pairs, own_parent):
    lines = [
        "Natural sample-derived taxonomic distinctness summary",
        f"Richness threshold: {THRESHOLD:.4f} relative abundance",
        "",
        "Richness:",
    ]
    for level in ["ASV", "Genus", "Family", "Phylum"]:
        lines.append(f"{level}:")
        for medium, label in MEDIA:
            for kind in ["parental", "coalesced"]:
                vals = richness_df[
                    (richness_df["level"] == level)
                    & (richness_df["medium"] == medium)
                    & (richness_df["kind"] == kind)
                ]["richness"].to_numpy(dtype=float)
                lines.append(f"  {label}, {kind}: {vals.mean():.2f} +/- {vals.std(ddof=0):.2f} (n={len(vals)})")

    lines.append("")
    lines.append("Post-stabilization parental pairwise similarities:")
    for level in ["ASV", "Genus", "Family", "Phylum"]:
        lines.append(f"{level}:")
        for medium, label in MEDIA:
            sub = parental_pairs[
                (parental_pairs["level"] == level)
                & (parental_pairs["medium"] == medium)
            ]
            for group in ["same source", "different source"]:
                vals_j = sub[sub["group"] == group]["jaccard"].to_numpy(dtype=float)
                vals_b = sub[sub["group"] == group]["bray"].to_numpy(dtype=float)
                lines.append(
                    f"  {label}, {group}: Jaccard {vals_j.mean():.3f} +/- {vals_j.std(ddof=0):.3f} "
                    f"(n={len(vals_j)}); Bray-Curtis similarity {vals_b.mean():.3f} +/- {vals_b.std(ddof=0):.3f}"
                )

    lines.append("")
    lines.append("Pairwise similarity among coalesced outcomes:")
    for level in ["ASV", "Genus", "Family", "Phylum"]:
        lines.append(f"{level}:")
        for medium, label in MEDIA:
            vals_j = coalesced_pairs[
                (coalesced_pairs["level"] == level)
                & (coalesced_pairs["medium"] == medium)
            ]["jaccard"].to_numpy(dtype=float)
            vals_b = coalesced_pairs[
                (coalesced_pairs["level"] == level)
                & (coalesced_pairs["medium"] == medium)
            ]["bray"].to_numpy(dtype=float)
            lines.append(
                f"  {label}: coalesced-coalesced Jaccard {vals_j.mean():.3f} +/- {vals_j.std(ddof=0):.3f} "
                f"(n={len(vals_j)}); Bray-Curtis similarity {vals_b.mean():.3f} +/- {vals_b.std(ddof=0):.3f}"
            )

    lines.append("")
    lines.append("Own-parent versus unrelated-parent similarity for coalesced outcomes:")
    for level in ["ASV", "Genus", "Family", "Phylum"]:
        lines.append(f"{level}:")
        for metric, name in [("jaccard", "Jaccard"), ("bray", "Bray-Curtis similarity")]:
            sub = own_parent[own_parent["level"] == level]
            own = (
                sub[sub["comparison"] == "own parents"]
                .sort_values("event")[metric]
                .to_numpy(dtype=float)
            )
            unrelated = (
                sub[sub["comparison"] == "unrelated parents"]
                .sort_values("event")[metric]
                .to_numpy(dtype=float)
            )
            stat = wilcoxon(own, unrelated, alternative="greater")
            lines.append(
                f"  Pooled {name}: own parents {own.mean():.3f} +/- {own.std(ddof=0):.3f}; "
                f"unrelated same-medium parents {unrelated.mean():.3f} +/- {unrelated.std(ddof=0):.3f}; "
                f"own > unrelated in {int(np.sum(own > unrelated))}/{len(own)} events; "
                f"paired Wilcoxon p = {stat.pvalue:.3e}"
            )

    lines.append("")
    lines.append("Per-medium own vs unrelated parent (paired, Jaccard):")
    for level in ["ASV", "Genus", "Family", "Phylum"]:
        lines.append(f"{level}:")
        for medium, label in MEDIA:
            sub = own_parent[
                (own_parent["level"] == level) & (own_parent["medium"] == medium)
            ]
            own = (
                sub[sub["comparison"] == "own parents"]
                .sort_values("event")["jaccard"]
                .to_numpy(dtype=float)
            )
            unrelated = (
                sub[sub["comparison"] == "unrelated parents"]
                .sort_values("event")["jaccard"]
                .to_numpy(dtype=float)
            )
            try:
                pval = wilcoxon(own, unrelated, alternative="greater").pvalue
                ptxt = f"{pval:.3e}"
            except ValueError:
                ptxt = "n/a"
            lines.append(
                f"  {label}: own {own.mean():.3f} +/- {own.std(ddof=0):.3f}; "
                f"unrelated same-medium {unrelated.mean():.3f} +/- {unrelated.std(ddof=0):.3f}; "
                f"n={len(own)} events; own > unrelated in {int(np.sum(own > unrelated))}/{len(own)}; "
                f"paired Wilcoxon p = {ptxt}"
            )

    lines.extend(
        [
            "",
            "Limitation: all measurements are post-stabilization 16S profiles.",
            "The analysis tests for complete post-stabilization taxonomic collapse",
            "and retained parent-specific taxonomic signal, but cannot quantify",
            "pre-to-post enrichment convergence or functional convergence.",
        ]
    )
    (OUT_DIR / "natural_taxonomic_distinctness_summary.txt").write_text("\n".join(lines) + "\n")


def main():
    parental, coalesced, collapsed_maps = load_data()
    richness_df = pd.concat(
        [richness_table(parental, coalesced, seq_map, level) for level, seq_map in collapsed_maps.items()],
        ignore_index=True,
    )
    parental_pairs = pd.concat(
        [parental_pairwise_table(parental, seq_map, level) for level, seq_map in collapsed_maps.items()],
        ignore_index=True,
    )
    coalesced_pairs = pd.concat(
        [coalesced_pairwise_table(coalesced, seq_map, level) for level, seq_map in collapsed_maps.items()],
        ignore_index=True,
    )
    own_parent = pd.concat(
        [own_parent_table(parental, coalesced, seq_map, level) for level, seq_map in collapsed_maps.items()],
        ignore_index=True,
    )
    write_summary(richness_df, parental_pairs, coalesced_pairs, own_parent)
    plot(richness_df, parental_pairs, coalesced_pairs, own_parent)


if __name__ == "__main__":
    main()
