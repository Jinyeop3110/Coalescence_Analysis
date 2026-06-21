#!/usr/bin/env python3
"""Quantify raw parent count-vector norm imbalance for the R3-2 simple additive null caveat."""

from __future__ import annotations

import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", ".."))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, CODE_DIR)

_prev_cwd = os.getcwd()
os.chdir(CODE_DIR)
from common_setup import (  # noqa: E402
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
)
os.chdir(_prev_cwd)


EXCEPTION_LIST = set(
    ["P4-02", "P4-03", "P4-23", "P4-24", "P7-97", "P8-12"]
    + ["P8-91"]
    + ["P5-73", "P5-69", "P5-64", "P5-61", "P5-59", "P5-56"]
    + ["P5-47", "P5-50"]
    + ["P5-39", "P5-87", "P5-54", "P6-02", "P6-47", "P6-74", "P6-57"]
)

MEDIUM_ORDER = ["L", "M", "H"]
MEDIUM_LABELS = {"L": "Nutr-", "M": "Base", "H": "Nutr+"}
MEDIUM_COLORS = {"L": "#4c78a8", "M": "#5f9e6e", "H": "#d65f5f"}
CLASS_NAMES = {0: "Dominance", 1: "Mixture", 2: "Restructuring", None: "Boundary"}
CLASS_COLORS = {"Dominance": "#ef8a7a", "Mixture": "#98d87a", "Restructuring": "#b26bd2"}
REVIEWER_STYLE_COLOR = "#8f8f8f"
REVIEWER_STYLE_SEED = 42
REVIEWER_STYLE_N_SAMPLES = 1000
PDI_DOMINANCE_FOLD_THRESHOLD = 1.0 + math.sqrt(2.0)


def classify_vector(n_c: np.ndarray, n_a: np.ndarray, n_b: np.ndarray) -> tuple[str, float, float]:
    u, v, k = metric_VectorDecomposition_onlyPositive(n_a, n_b, n_c)
    x, y = calculate_assymetricity(u, v, k)
    return CLASS_NAMES[characterize_case(x, y)], float(x), float(y)


def load_event_table() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    coal = pd.read_excel(os.path.join(PROJECT_ROOT, "Analyzed", "processed_CoalescenceEvent_synthetic.xlsx"))
    raw = pd.read_csv(os.path.join(PROJECT_ROOT, "SEQanalysis", "excludeNatural", "M_OTUtableGreenGenes.csv"))
    sample_sheet = pd.read_excel(os.path.join(PROJECT_ROOT, "Postprocessed", "Sample_Sheet.xlsx"), sheet_name="samples")

    raw_ids = raw.iloc[:, 0].astype(str).str.replace("_F_filt.fastq.gz", "", regex=False)
    raw_values = raw.iloc[:, 1:].apply(pd.to_numeric, errors="coerce").fillna(0)
    raw_lookup = {sample_id: raw_values.iloc[i].to_numpy(float) for i, sample_id in enumerate(raw_ids)}
    raw_count = pd.DataFrame(
        {
            "SampleIDX": raw_ids,
            "total_reads": raw_values.sum(axis=1),
            "raw_l2_norm": np.linalg.norm(raw_values.to_numpy(float), axis=1),
        }
    )
    medium_map = (
        sample_sheet[sample_sheet["community_origin"] == "Synthetic"][["sample_id", "medium"]]
        .rename(columns={"sample_id": "SampleIDX", "medium": "Medium_label"})
    )
    medium_reverse = {"Nutr-": "L", "Base": "M", "Nutr+": "H"}
    raw_count = raw_count.merge(medium_map, on="SampleIDX", how="inner")
    raw_count["Medium"] = raw_count["Medium_label"].map(medium_reverse)

    event_rows = []
    parent_rows = []
    for _, event in coal.iterrows():
        sid = event["SampleIDX"]
        if sid in EXCEPTION_LIST:
            continue

        n_a = raw_lookup.get(event["SampleIDX_Sub1"])
        n_b = raw_lookup.get(event["SampleIDX_Sub2"])
        if n_a is None or n_b is None:
            continue
        if min(np.sum(n_a), np.sum(n_b)) <= 1e-12:
            continue

        norm_a = float(np.linalg.norm(n_a))
        norm_b = float(np.linalg.norm(n_b))
        ratio = max(norm_a, norm_b) / min(norm_a, norm_b)
        additive = n_a + n_b
        null_class, null_x, null_y = classify_vector(additive, n_a, n_b)

        event_rows.append(
            {
                "SampleIDX": sid,
                "Medium": event["Medium"],
                "raw_norm_A": norm_a,
                "raw_norm_B": norm_b,
                "raw_norm_low": min(norm_a, norm_b),
                "raw_norm_high": max(norm_a, norm_b),
                "raw_norm_difference": abs(norm_a - norm_b),
                "raw_norm_ratio": ratio,
                "abs_log2_raw_norm_ratio": abs(math.log2(norm_a / norm_b)),
                "null_class": null_class,
                "null_x": null_x,
                "null_y": null_y,
            }
        )

        for label, sample_id, vec, norm in [
            ("A", event["SampleIDX_Sub1"], n_a, norm_a),
            ("B", event["SampleIDX_Sub2"], n_b, norm_b),
        ]:
            parent_rows.append(
                {
                    "EventSampleIDX": sid,
                    "ParentSampleIDX": sample_id,
                    "Parent": label,
                    "Medium": event["Medium"],
                    "total_reads": float(np.sum(vec)),
                    "raw_l2_norm": norm,
                    "top_asv_reads": float(np.max(vec)),
                }
            )

    return pd.DataFrame(event_rows), pd.DataFrame(parent_rows), raw_count


def summary_table(events: pd.DataFrame, parents: pd.DataFrame, raw_count: pd.DataFrame) -> pd.DataFrame:
    rows = []
    unique_parents = parents.drop_duplicates("ParentSampleIDX")
    for medium in MEDIUM_ORDER:
        ev = events[events["Medium"] == medium]
        pa = unique_parents[unique_parents["Medium"] == medium]
        rows.append(
            {
                "Medium": medium,
                "Medium_label": MEDIUM_LABELS[medium],
                "n_events": len(ev),
                "n_parent_communities": len(pa),
                "parent_total_reads_median": pa["total_reads"].median(),
                "parent_total_reads_q25": pa["total_reads"].quantile(0.25),
                "parent_total_reads_q75": pa["total_reads"].quantile(0.75),
                "parent_total_reads_q05": pa["total_reads"].quantile(0.05),
                "parent_total_reads_q95": pa["total_reads"].quantile(0.95),
                "parent_total_reads_min": pa["total_reads"].min(),
                "parent_total_reads_max": pa["total_reads"].max(),
                "parent_raw_l2_median": pa["raw_l2_norm"].median(),
                "parent_raw_l2_q25": pa["raw_l2_norm"].quantile(0.25),
                "parent_raw_l2_q75": pa["raw_l2_norm"].quantile(0.75),
                "pair_low_raw_l2_median": ev["raw_norm_low"].median(),
                "pair_high_raw_l2_median": ev["raw_norm_high"].median(),
                "raw_norm_ratio_median": ev["raw_norm_ratio"].median(),
                "raw_norm_ratio_q25": ev["raw_norm_ratio"].quantile(0.25),
                "raw_norm_ratio_q75": ev["raw_norm_ratio"].quantile(0.75),
                "raw_norm_ratio_max": ev["raw_norm_ratio"].max(),
                "null_y_median": ev["null_y"].median(),
                "null_y_q25": ev["null_y"].quantile(0.25),
                "null_y_q75": ev["null_y"].quantile(0.75),
                "null_y_max": ev["null_y"].max(),
                "simple_additive_null_mixture_fraction": np.mean(ev["null_class"] == "Mixture"),
            }
        )
    return pd.DataFrame(rows)


def jittered_scatter(ax: plt.Axes, x_center: int, values: np.ndarray, color: str, seed: int) -> None:
    rng = np.random.default_rng(seed)
    x = x_center + rng.uniform(-0.16, 0.16, size=len(values))
    ax.scatter(x, values, s=10, color=color, alpha=0.45, linewidths=0)


def draw_box(ax: plt.Axes, x_center: int, values: np.ndarray, color: str) -> None:
    ax.boxplot(
        [values],
        positions=[x_center],
        widths=0.42,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 1.2},
        boxprops={"facecolor": color, "alpha": 0.30, "edgecolor": color, "linewidth": 1.0},
        whiskerprops={"color": color, "linewidth": 1.0},
        capprops={"color": color, "linewidth": 1.0},
    )


def sample_skewed_reviewer_style_norm_ratios(n: int, n_samples: int = REVIEWER_STYLE_N_SAMPLES) -> np.ndarray:
    """Norm-fold differences for the skewed reviewer-style simple additive null model."""
    n_index = {2: 0, 4: 1, 6: 2, 8: 3}[n]
    rng = np.random.default_rng(REVIEWER_STYLE_SEED + 28 + n_index)
    ratios = []
    for _ in range(n_samples):
        a = np.zeros(2 * n)
        b = np.zeros(2 * n)
        a[:n] = 10 ** rng.uniform(-3.0, 0.0, size=n)
        b[n:] = 10 ** rng.uniform(-3.0, 0.0, size=n)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        ratios.append(max(norm_a, norm_b) / min(norm_a, norm_b))
    return np.asarray(ratios, dtype=float)


def make_figure(events: pd.DataFrame, parents: pd.DataFrame, raw_count: pd.DataFrame, out_pdf: str) -> None:
    unique_parents = parents.drop_duplicates("ParentSampleIDX")
    fig, axes = plt.subplots(1, 3, figsize=(8.7, 2.7))

    ax = axes[0]
    bins = np.linspace(0, unique_parents["raw_l2_norm"].max(), 22)
    for medium in MEDIUM_ORDER:
        vals = unique_parents[unique_parents["Medium"] == medium]["raw_l2_norm"].to_numpy(float)
        ax.hist(
            vals,
            bins=bins,
            density=True,
            histtype="step",
            linewidth=1.7,
            color=MEDIUM_COLORS[medium],
            label=MEDIUM_LABELS[medium],
        )
    ax.set_title("A", loc="left", fontweight="bold")
    ax.set_xlabel(r"raw count-vector $\|n\|_2$ (16S reads)")
    ax.set_ylabel("density")
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    plot_items = []
    for medium in MEDIUM_ORDER:
        plot_items.append(
            (
                MEDIUM_LABELS[medium],
                events[events["Medium"] == medium]["raw_norm_ratio"].to_numpy(float),
                MEDIUM_COLORS[medium],
            )
        )
    plot_items.extend(
        [
            ("Skewed\nN=2", sample_skewed_reviewer_style_norm_ratios(2), REVIEWER_STYLE_COLOR),
            ("Skewed\nN=4", sample_skewed_reviewer_style_norm_ratios(4), REVIEWER_STYLE_COLOR),
        ]
    )
    for i, (_, vals, color) in enumerate(plot_items, start=1):
        jittered_scatter(ax, i, vals, color, seed=200 + 10 * i)
        draw_box(ax, i, vals, color)
    ax.set_title("B", loc="left", fontweight="bold")
    ax.set_xticks(range(1, len(plot_items) + 1))
    ax.set_xticklabels([label for label, _, _ in plot_items], fontsize=7)
    ax.set_yscale("log")
    ax.set_ylabel(r"parental $\|n\|_2$ fold difference")
    ax.axhline(1, color="0.2", linewidth=0.6)
    ax.axhline(
        PDI_DOMINANCE_FOLD_THRESHOLD,
        color="0.15",
        linewidth=0.8,
        linestyle="--",
    )
    ax.text(
        0.02,
        PDI_DOMINANCE_FOLD_THRESHOLD * 1.05,
        r"PDI $<0.25$ or $>0.75$",
        transform=ax.get_yaxis_transform(),
        ha="left",
        va="bottom",
        fontsize=6.5,
        color="0.15",
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[2]
    class_order = ["Dominance", "Mixture", "Restructuring"]
    x = np.arange(len(MEDIUM_ORDER))
    bottoms = np.zeros(len(MEDIUM_ORDER))
    totals = np.array([len(events[events["Medium"] == medium]) for medium in MEDIUM_ORDER], dtype=float)
    for cls in class_order:
        counts = np.array(
            [np.sum(events[events["Medium"] == medium]["null_class"] == cls) for medium in MEDIUM_ORDER],
            dtype=float,
        )
        fractions = counts / totals
        ax.bar(
            x,
            fractions,
            bottom=bottoms,
            width=0.62,
            color=CLASS_COLORS[cls],
            edgecolor="white",
            linewidth=0.6,
            label=cls,
        )
        if cls == "Mixture":
            for xi, bottom, frac, count, total in zip(x, bottoms, fractions, counts, totals):
                if frac > 0:
                    ax.text(
                        xi,
                        bottom + frac / 2,
                        f"{int(count)}/{int(total)}",
                        ha="center",
                        va="center",
                        fontsize=7,
                    )
        bottoms += fractions
    ax.set_title("C", loc="left", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([MEDIUM_LABELS[m] for m in MEDIUM_ORDER])
    ax.set_ylim(0, 1)
    ax.set_ylabel("simple additive null fraction")
    ax.legend(frameon=False, fontsize=6, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout(w_pad=1.1)
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf.replace(".pdf", ".png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    events, parents, raw_count = load_event_table()
    events.to_csv(os.path.join(SCRIPT_DIR, "parent_norm_asymmetry_events.csv"), index=False)
    parents.to_csv(os.path.join(SCRIPT_DIR, "parent_norm_asymmetry_parent_vectors.csv"), index=False)
    raw_count.to_csv(os.path.join(SCRIPT_DIR, "parent_norm_asymmetry_raw_read_counts.csv"), index=False)
    summary = summary_table(events, parents, raw_count)
    summary.to_csv(os.path.join(SCRIPT_DIR, "parent_norm_asymmetry_summary.csv"), index=False)
    make_figure(events, parents, raw_count, os.path.join(SCRIPT_DIR, "Fig_R3_2_parent_norm_asymmetry.pdf"))

    print(summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("Simple additive null classes:", events["null_class"].value_counts().to_dict())


if __name__ == "__main__":
    main()
