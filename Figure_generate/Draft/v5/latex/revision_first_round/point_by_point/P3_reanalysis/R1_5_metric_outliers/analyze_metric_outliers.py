#!/usr/bin/env python3
"""Event-level audit of why Jaccard and Jensen-Shannon differ in R1-5.

The analysis mirrors the metric definitions used in
`Figure_generate/code/plot_stacked_bar_class_fractions.py` for the
Base-medium robustness panel, then adds per-event switch diagnostics.
"""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial.distance import braycurtis, euclidean, jensenshannon
from scipy.stats import fisher_exact, mannwhitneyu


ROOT = Path(__file__).resolve().parents[8]
OUT_DIR = Path(__file__).resolve().parent

COALESCENCE_PATH = ROOT / "Analyzed/processed_CoalescenceEvent_synthetic.xlsx"
SEQUENCES_PATH = ROOT / "Postprocessed/processed_Sequences_synthetic.xlsx"

THRESHOLD = 1e-4
RARE_THRESHOLD = 0.01

EXCEPTION_LIST = {
    "P4-02",
    "P4-03",
    "P4-23",
    "P4-24",
    "P7-97",
    "P8-12",
    "P8-91",
    "P5-73",
    "P5-69",
    "P5-64",
    "P5-61",
    "P5-59",
    "P5-56",
    "P5-47",
    "P5-50",
    "P5-39",
    "P5-87",
    "P5-54",
    "P6-02",
    "P6-47",
    "P6-74",
    "P6-57",
}

CLASS_NAMES = {
    0: "Dominance",
    1: "Mixture",
    2: "Restructuring",
}


def normalize(v: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def metric_vector_decomposition(
    c1: np.ndarray, c2: np.ndarray, c_mix: np.ndarray
) -> tuple[float, float, float, np.ndarray]:
    u = normalize(c1)
    v = normalize(c2)
    m = normalize(c_mix)

    basis = np.array([[np.sum(u * u), np.sum(u * v)], [np.sum(u * v), np.sum(v * v)]])
    coeffs = np.matmul(np.linalg.inv(basis), np.array([np.sum(m * u), np.sum(m * v)]))

    x1 = coeffs[0] * (coeffs[0] > 0)
    x2 = coeffs[1] * (coeffs[1] > 0)
    orthogonal_vec = m - (coeffs[0] * u) - (coeffs[1] * v)
    x3 = np.linalg.norm(orthogonal_vec)
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2 + 1e-10))

    return convert * x1, convert * x2, x3, orthogonal_vec


def metric_euclidean(
    c1: np.ndarray, c2: np.ndarray, c_mix: np.ndarray, orthogonal_vec: np.ndarray
) -> tuple[float, float, float]:
    c1_norm = normalize(c1)
    c2_norm = normalize(c2)
    c_mix_norm = normalize(c_mix)
    orth_norm = normalize(orthogonal_vec)

    max_dist = np.sqrt(2)
    sims = np.array(
        [
            max(0, 1 - euclidean(c_mix_norm, c1_norm) / max_dist),
            max(0, 1 - euclidean(c_mix_norm, c2_norm) / max_dist),
            max(0, 1 - euclidean(c_mix_norm, orth_norm) / max_dist),
        ]
    )
    norm = np.linalg.norm(sims)
    return tuple(sims / norm) if norm > 0 else (0.0, 0.0, 0.0)


def metric_bray_curtis(
    c1: np.ndarray, c2: np.ndarray, c_mix: np.ndarray, orthogonal_vec: np.ndarray
) -> tuple[float, float, float]:
    sims = np.array(
        [
            max(0, 1 - braycurtis(c_mix, c1)),
            max(0, 1 - braycurtis(c_mix, c2)),
            max(0, 1 - braycurtis(c_mix, orthogonal_vec)),
        ]
    )
    norm = np.linalg.norm(sims)
    return tuple(sims / norm) if norm > 0 else (0.0, 0.0, 0.0)


def metric_jensen_shannon(
    c1: np.ndarray, c2: np.ndarray, c_mix: np.ndarray, orthogonal_vec: np.ndarray
) -> tuple[float, float, float]:
    c1_norm = c1 / (np.sum(c1) + 1e-10)
    c2_norm = c2 / (np.sum(c2) + 1e-10)
    c_mix_norm = c_mix / (np.sum(c_mix) + 1e-10)
    orth_positive = np.maximum(orthogonal_vec, 0)
    orth_norm = orth_positive / (np.sum(orth_positive) + 1e-10)

    sims = np.array(
        [
            max(0, 1 - jensenshannon(c_mix_norm, c1_norm)),
            max(0, 1 - jensenshannon(c_mix_norm, c2_norm)),
            max(0, 1 - jensenshannon(c_mix_norm, orth_norm)),
        ]
    )
    norm = np.linalg.norm(sims)
    return tuple(sims / norm) if norm > 0 else (0.0, 0.0, 0.0)


def metric_jaccard(
    c1: np.ndarray, c2: np.ndarray, c_mix: np.ndarray, orthogonal_vec: np.ndarray
) -> tuple[float, float, float]:
    c1_binary = (c1 > THRESHOLD).astype(float)
    c2_binary = (c2 > THRESHOLD).astype(float)
    c_mix_binary = (c_mix > THRESHOLD).astype(float)
    orthogonal_binary = (orthogonal_vec > THRESHOLD).astype(float)

    def jaccard_similarity(a: np.ndarray, b: np.ndarray) -> float:
        union = np.sum(np.maximum(a, b))
        if union == 0:
            return 0.0
        return float(np.sum(np.minimum(a, b)) / union)

    sims = np.array(
        [
            jaccard_similarity(c_mix_binary, c1_binary),
            jaccard_similarity(c_mix_binary, c2_binary),
            jaccard_similarity(c_mix_binary, orthogonal_binary),
        ]
    )
    norm = np.linalg.norm(sims)
    return tuple(sims / norm) if norm > 0 else (0.0, 0.0, 0.0)


def classify_outcome(u: float, v: float, k: float) -> int:
    x = np.sqrt(u**2 + v**2)
    y = np.abs(np.abs(np.arctan(u / (v + 1e-8))) - np.pi / 4) / (np.pi / 4)

    if (x**2 > 0.5) and (y > 0.5):
        return 0
    if (x**2 > 0.5) and (y < 0.5):
        return 1
    if x**2 < 0.5:
        return 2
    return 1


def asymmetry(u: float, v: float) -> float:
    return float(np.abs(np.abs(np.arctan(u / (v + 1e-8))) - np.pi / 4) / (np.pi / 4))


def load_base_events() -> pd.DataFrame:
    coalescence = pd.read_excel(COALESCENCE_PATH)
    base = coalescence[
        (coalescence["Medium"] == "M")
        & (coalescence["CoalescenceType"] == "C")
        & (~coalescence["SampleIDX"].isin(EXCEPTION_LIST))
    ].copy()

    # Matches the existing robustness figure: Base medium, synthetic, pool sizes 6/12/24.
    base = base[
        ((base["CommunityIDX"] >= 1) & (base["CommunityIDX"] <= 14))
        | ((base["CommunityIDX"] >= 15) & (base["CommunityIDX"] <= 41))
        | ((base["CommunityIDX"] >= 42) & (base["CommunityIDX"] <= 47))
    ].copy()
    base["pool_size"] = np.select(
        [
            base["CommunityIDX"].between(1, 14),
            base["CommunityIDX"].between(15, 41),
            base["CommunityIDX"].between(42, 47),
        ],
        [6, 12, 24],
        default=np.nan,
    )
    return base.sort_values("SampleIDX")


def abundance_lookup() -> dict[str, np.ndarray]:
    sequences = pd.read_excel(SEQUENCES_PATH)
    return {
        row["SampleIDX"]: row.iloc[1:].to_numpy(dtype=float)
        for _, row in sequences.iterrows()
    }


def support_features(c1: np.ndarray, c2: np.ndarray, c_mix: np.ndarray) -> dict[str, float]:
    c1_support = c1 > THRESHOLD
    c2_support = c2 > THRESHOLD
    mix_support = c_mix > THRESHOLD

    p1_only = c1_support & ~c2_support
    p2_only = c2_support & ~c1_support

    p1_retained = p1_only & mix_support
    p2_retained = p2_only & mix_support
    retained = p1_retained | p2_retained

    p1_abundance = float(np.sum(c_mix[p1_only]))
    p2_abundance = float(np.sum(c_mix[p2_only]))
    retained_abundance = p1_abundance + p2_abundance

    p1_richness = int(np.sum(p1_retained))
    p2_richness = int(np.sum(p2_retained))
    retained_richness = p1_richness + p2_richness

    rare_mask = (c_mix > THRESHOLD) & (c_mix < RARE_THRESHOLD)
    rare_retained_mask = retained & (c_mix < RARE_THRESHOLD)

    return {
        "parent1_richness": int(np.sum(c1_support)),
        "parent2_richness": int(np.sum(c2_support)),
        "mix_richness": int(np.sum(mix_support)),
        "retained_richness": retained_richness,
        "retained_richness_skew": abs(p1_richness - p2_richness) / max(retained_richness, 1),
        "retained_abundance": retained_abundance,
        "retained_abundance_skew": abs(p1_abundance - p2_abundance) / max(retained_abundance, 1e-10),
        "rare_taxa_count": int(np.sum(rare_mask)),
        "rare_abundance_fraction": float(np.sum(c_mix[rare_mask]) / max(np.sum(c_mix), 1e-10)),
        "rare_retained_taxa_fraction": float(np.sum(rare_retained_mask) / max(retained_richness, 1)),
    }


def compute_event_table() -> pd.DataFrame:
    events = load_base_events()
    abundances = abundance_lookup()
    metric_funcs = OrderedDict(
        [
            ("vector", None),
            ("euclidean", metric_euclidean),
            ("bray_curtis", metric_bray_curtis),
            ("jensen_shannon", metric_jensen_shannon),
            ("jaccard", metric_jaccard),
        ]
    )

    rows = []
    for _, event in events.iterrows():
        sample_id = event["SampleIDX"]
        c_mix = abundances[sample_id]
        c1 = abundances[event["SampleIDX_Sub1"]]
        c2 = abundances[event["SampleIDX_Sub2"]]
        c1 = c1 * (c1 > THRESHOLD)
        c2 = c2 * (c2 > THRESHOLD)

        vector_u, vector_v, vector_k, orthogonal_vec = metric_vector_decomposition(c1, c2, c_mix)
        row = {
            "sample_id": sample_id,
            "parent1_id": event["SampleIDX_Sub1"],
            "parent2_id": event["SampleIDX_Sub2"],
            "community_idx": event["CommunityIDX"],
            "pool_size": int(event["pool_size"]),
            **support_features(c1, c2, c_mix),
        }

        for metric_name, metric_func in metric_funcs.items():
            if metric_name == "vector":
                u, v, k = vector_u, vector_v, vector_k
            else:
                u, v, k = metric_func(c1, c2, c_mix, orthogonal_vec)
            label = CLASS_NAMES[classify_outcome(u, v, k)]
            row[f"{metric_name}_u"] = u
            row[f"{metric_name}_v"] = v
            row[f"{metric_name}_k"] = k
            row[f"{metric_name}_retention"] = np.sqrt(u**2 + v**2)
            row[f"{metric_name}_asymmetry"] = asymmetry(u, v)
            row[f"{metric_name}_label"] = label

        row["jaccard_switch"] = row["jaccard_label"] != row["vector_label"]
        row["jensen_shannon_switch"] = row["jensen_shannon_label"] != row["vector_label"]
        row["jaccard_dominance_lost"] = (
            row["vector_label"] == "Dominance" and row["jaccard_label"] != "Dominance"
        )
        row["jensen_shannon_dominance_lost"] = (
            row["vector_label"] == "Dominance" and row["jensen_shannon_label"] != "Dominance"
        )
        rows.append(row)

    return pd.DataFrame(rows)


def count_labels(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for metric in ["vector", "euclidean", "bray_curtis", "jensen_shannon", "jaccard"]:
        counts = events[f"{metric}_label"].value_counts()
        total = int(counts.sum())
        for label in ["Dominance", "Mixture", "Restructuring"]:
            count = int(counts.get(label, 0))
            rows.append(
                {
                    "metric": metric,
                    "label": label,
                    "count": count,
                    "total": total,
                    "fraction": count / total if total else np.nan,
                }
            )
    return pd.DataFrame(rows)


def confusion(events: pd.DataFrame, metric: str) -> pd.DataFrame:
    return pd.crosstab(
        events["vector_label"],
        events[f"{metric}_label"],
        rownames=["vector"],
        colnames=[metric],
        dropna=False,
    ).reindex(index=["Dominance", "Mixture", "Restructuring"], columns=["Dominance", "Mixture", "Restructuring"], fill_value=0)


def compare_switch_features(events: pd.DataFrame) -> pd.DataFrame:
    features = [
        "retained_abundance_skew",
        "retained_richness_skew",
        "mix_richness",
        "retained_richness",
        "rare_taxa_count",
        "rare_abundance_fraction",
        "rare_retained_taxa_fraction",
    ]
    rows = []
    for metric in ["jaccard", "jensen_shannon"]:
        switch_col = f"{metric}_dominance_lost"
        subset = events[events["vector_label"] == "Dominance"].copy()
        for feature in features:
            switched = subset.loc[subset[switch_col], feature].dropna()
            stable = subset.loc[~subset[switch_col], feature].dropna()
            if len(switched) > 0 and len(stable) > 0:
                _, p_value = mannwhitneyu(switched, stable, alternative="two-sided")
            else:
                p_value = np.nan
            rows.append(
                {
                    "metric": metric,
                    "feature": feature,
                    "dominance_lost_n": int(len(switched)),
                    "dominance_stable_n": int(len(stable)),
                    "dominance_lost_median": float(switched.median()) if len(switched) else np.nan,
                    "dominance_stable_median": float(stable.median()) if len(stable) else np.nan,
                    "mannwhitney_p": p_value,
                }
            )

        abundance_strong = subset["retained_abundance_skew"] > 0.5
        richness_weak = subset["retained_richness_skew"] <= 0.5
        contingency = pd.crosstab(subset[switch_col], abundance_strong & richness_weak)
        table = np.array(
            [
                [
                    contingency.loc[True, True] if True in contingency.index and True in contingency.columns else 0,
                    contingency.loc[True, False] if True in contingency.index and False in contingency.columns else 0,
                ],
                [
                    contingency.loc[False, True] if False in contingency.index and True in contingency.columns else 0,
                    contingency.loc[False, False] if False in contingency.index and False in contingency.columns else 0,
                ],
            ]
        )
        _, fisher_p = fisher_exact(table)
        rows.append(
            {
                "metric": metric,
                "feature": "abundance_skew_high_but_richness_skew_low",
                "dominance_lost_n": int(np.sum(subset[switch_col])),
                "dominance_stable_n": int(np.sum(~subset[switch_col])),
                "dominance_lost_median": float(np.mean((abundance_strong & richness_weak)[subset[switch_col]])),
                "dominance_stable_median": float(np.mean((abundance_strong & richness_weak)[~subset[switch_col]])),
                "mannwhitney_p": fisher_p,
            }
        )
    return pd.DataFrame(rows)


def write_text_summary(
    events: pd.DataFrame,
    label_counts: pd.DataFrame,
    feature_summary: pd.DataFrame,
) -> None:
    lines = [
        "# R1-5 Metric-Outlier Audit",
        "",
        f"Events analyzed: {len(events)} Base-medium synthetic coalescence events after the existing exclusion list.",
        "",
        "## Outcome Counts",
        "",
    ]

    for metric in ["vector", "euclidean", "bray_curtis", "jensen_shannon", "jaccard"]:
        metric_counts = label_counts[label_counts["metric"] == metric]
        count_text = ", ".join(
            f"{row.label} {row['count']}/{row.total} ({row.fraction:.1%})"
            for _, row in metric_counts.iterrows()
        )
        lines.append(f"- {metric}: {count_text}")

    lines.extend(["", "## Confusion Versus Vector Decomposition", ""])
    for metric in ["jensen_shannon", "jaccard"]:
        lines.append(f"### {metric}")
        lines.append("")
        lines.append(confusion(events, metric).to_markdown())
        lines.append("")

    lines.extend(["## Dominance-Loss Feature Summary", ""])
    for metric in ["jensen_shannon", "jaccard"]:
        subset = feature_summary[feature_summary["metric"] == metric]
        lines.append(f"### {metric}")
        lines.append("")
        lines.append(subset.to_markdown(index=False, floatfmt=".4g"))
        lines.append("")

    vector_dom = events[events["vector_label"] == "Dominance"]
    for metric in ["jensen_shannon", "jaccard"]:
        lost = int(vector_dom[f"{metric}_dominance_lost"].sum())
        total = len(vector_dom)
        lines.append(
            f"- {metric} reclassified {lost}/{total} vector-Dominance events "
            f"({lost / total:.1%}) as non-Dominance."
        )

    (OUT_DIR / "metric_outlier_summary.md").write_text("\n".join(lines) + "\n")


def plot_results(events: pd.DataFrame, label_counts: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(8.0, 6.2))

    metric_order = ["vector", "euclidean", "bray_curtis", "jensen_shannon", "jaccard"]
    label_order = ["Dominance", "Mixture", "Restructuring"]
    colors = {"Dominance": "#A7216A", "Mixture": "#E24912", "Restructuring": "#4C78A8"}

    ax = axes[0, 0]
    bottoms = np.zeros(len(metric_order))
    for label in label_order:
        values = []
        for metric in metric_order:
            row = label_counts[(label_counts["metric"] == metric) & (label_counts["label"] == label)]
            values.append(float(row["fraction"].iloc[0]) * 100)
        ax.bar(metric_order, values, bottom=bottoms, color=colors[label], edgecolor="white", label=label)
        bottoms += np.array(values)
    ax.set_ylabel("Outcome fraction (%)")
    ax.set_ylim(0, 100)
    ax.set_title("A. Classification by metric")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(frameon=False, fontsize=8)

    for ax, metric, title in [
        (axes[0, 1], "jensen_shannon", "B. JS vs vector"),
        (axes[1, 0], "jaccard", "C. Jaccard vs vector"),
    ]:
        matrix = confusion(events, metric)
        image = ax.imshow(matrix.values, cmap="Blues", vmin=0)
        ax.set_xticks(range(3), labels=label_order, rotation=35, ha="right")
        ax.set_yticks(range(3), labels=label_order)
        ax.set_xlabel(metric)
        ax.set_ylabel("Vector decomposition")
        ax.set_title(title)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, str(matrix.values[i, j]), ha="center", va="center", fontsize=9)
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    ax = axes[1, 1]
    vector_dom = events[events["vector_label"] == "Dominance"].copy()
    for metric, marker, color in [
        ("jensen_shannon", "o", "#6A4C93"),
        ("jaccard", "s", "#2A9D8F"),
    ]:
        lost = vector_dom[f"{metric}_dominance_lost"]
        ax.scatter(
            vector_dom.loc[~lost, "retained_richness_skew"],
            vector_dom.loc[~lost, "retained_abundance_skew"],
            s=26,
            marker=marker,
            facecolors="none",
            edgecolors=color,
            alpha=0.75,
            label=f"{metric} stable",
        )
        ax.scatter(
            vector_dom.loc[lost, "retained_richness_skew"],
            vector_dom.loc[lost, "retained_abundance_skew"],
            s=30,
            marker=marker,
            color=color,
            alpha=0.85,
            label=f"{metric} lost",
        )
    ax.set_xlabel("Retained richness skew")
    ax.set_ylabel("Retained abundance skew")
    ax.set_title("D. Vector-Dominance events")
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.legend(frameon=False, fontsize=7)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "metric_outlier_audit.pdf", bbox_inches="tight")
    fig.savefig(OUT_DIR / "metric_outlier_audit.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    events = compute_event_table()
    label_counts = count_labels(events)
    feature_summary = compare_switch_features(events)

    events.to_csv(OUT_DIR / "metric_outlier_event_table.csv", index=False)
    label_counts.to_csv(OUT_DIR / "metric_outlier_label_counts.csv", index=False)
    feature_summary.to_csv(OUT_DIR / "metric_outlier_feature_summary.csv", index=False)
    write_text_summary(events, label_counts, feature_summary)
    plot_results(events, label_counts)

    print(f"Wrote {len(events)} event records to {OUT_DIR / 'metric_outlier_event_table.csv'}")
    print(f"Wrote summary to {OUT_DIR / 'metric_outlier_summary.md'}")
    print(f"Wrote figure to {OUT_DIR / 'metric_outlier_audit.pdf'}")


if __name__ == "__main__":
    main()
