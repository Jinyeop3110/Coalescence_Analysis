#!/usr/bin/env python3
"""Generate response-only evidence figure for Reviewer 2 Question 3.

This script intentionally lives in this worker folder and recomputes the
continuous similarity summaries from processed data files. It does not import
revision figure code from other folders.
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kruskal


ROOT = Path("/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404")
WORK = ROOT / "Figure_generate/Draft/v5/latex/revision/new review responses_2026-05-14/reviewer2_agents/R2_Q3_classification_continuous_similarity"
FIG_DIR = WORK / "figures"
OUT_DIR = WORK / "figure_code"

ASV_PATH = ROOT / "Postprocessed/processed_Sequences_synthetic.xlsx"
COAL_PATH = ROOT / "Analyzed/processed_CoalescenceEvent_synthetic.xlsx"

EXCLUDE = {
    "P4-02", "P4-03", "P4-23", "P4-24", "P7-97", "P8-12", "P8-91",
    "P5-73", "P5-69", "P5-64", "P5-61", "P5-59", "P5-56", "P5-47",
    "P5-50", "P5-39", "P5-87", "P5-54", "P6-02", "P6-47", "P6-74",
    "P6-57",
}

MEDIUM_ORDER = ["L", "M", "H"]
MEDIUM_LABELS = {"L": "Nutr-", "M": "Base", "H": "Nutr+"}
MEDIUM_COLORS = {"L": "#C13C8A", "M": "#8B6B32", "H": "#E68632"}
CLASS_NAMES = {0: "Dominance", 1: "Mixture", 2: "Restructuring"}
CLASS_COLORS = {"Dominance": "#4C78A8", "Mixture": "#59A14F", "Restructuring": "#E15759"}


def abundance_lookup(asv_table):
    values = {}
    for _, row in asv_table.iterrows():
        values[row["SampleIDX"]] = row.iloc[1:].to_numpy(dtype=float)
    return values


def threshold_and_unit(vec, threshold=0.001):
    out = np.array(vec, dtype=float)
    out[out < threshold] = 0.0
    norm = np.linalg.norm(out)
    if norm == 0:
        return None
    return out / norm


def continuous_coordinates(parent_a, parent_b, offspring):
    gram = np.array(
        [
            [np.dot(parent_a, parent_a), np.dot(parent_a, parent_b)],
            [np.dot(parent_a, parent_b), np.dot(parent_b, parent_b)],
        ]
    )
    rhs = np.array([np.dot(offspring, parent_a), np.dot(offspring, parent_b)])
    raw_u, raw_v = np.linalg.solve(gram, rhs)
    orthogonal_vec = offspring - raw_u * parent_a - raw_v * parent_b
    residual = np.linalg.norm(orthogonal_vec)
    u_pos = raw_u if raw_u > 0 else 0.0
    v_pos = raw_v if raw_v > 0 else 0.0
    denom = u_pos * u_pos + v_pos * v_pos
    if denom <= 0:
        return None
    scale = np.sqrt(max(0.0, 1.0 - residual * residual) / denom)
    u = scale * u_pos
    v = scale * v_pos
    retention_sq = u * u + v * v
    pdi = (2.0 / np.pi) * np.arctan2(u, v)
    asymmetry = abs(pdi - 0.5) / 0.5
    return u, v, residual, retention_sq, pdi, asymmetry, orthogonal_vec


def classify(retention_sq, asymmetry):
    if retention_sq <= 0.5:
        return "Restructuring"
    if asymmetry > 0.5:
        return "Dominance"
    return "Mixture"


def jaccard_similarity(x, y, threshold=1e-4):
    xb = x > threshold
    yb = y > threshold
    union = np.logical_or(xb, yb).sum()
    if union == 0:
        return np.nan
    return np.logical_and(xb, yb).sum() / union


def classify_three_way_similarity(sim_a, sim_b, sim_orth):
    if not np.isfinite(sim_a) or not np.isfinite(sim_b) or not np.isfinite(sim_orth):
        return None
    norm = np.sqrt(sim_a * sim_a + sim_b * sim_b + sim_orth * sim_orth)
    if norm == 0:
        return None
    u = sim_a / norm
    v = sim_b / norm
    retention_sq = u * u + v * v
    pdi = (2.0 / np.pi) * np.arctan2(u, v)
    asymmetry = abs(pdi - 0.5) / 0.5
    return classify(retention_sq, asymmetry)


def build_table():
    asv = pd.read_excel(ASV_PATH)
    coal = pd.read_excel(COAL_PATH)
    abund = abundance_lookup(asv)
    rows = []
    for _, event in coal.iterrows():
        sid = event["SampleIDX"]
        if sid in EXCLUDE:
            continue
        parent_a_raw = abund.get(event["SampleIDX_Sub1"])
        parent_b_raw = abund.get(event["SampleIDX_Sub2"])
        offspring_raw = abund.get(sid)
        if parent_a_raw is None or parent_b_raw is None or offspring_raw is None:
            continue
        parent_a = threshold_and_unit(parent_a_raw)
        parent_b = threshold_and_unit(parent_b_raw)
        offspring = threshold_and_unit(offspring_raw)
        if parent_a is None or parent_b is None or offspring is None:
            continue

        coords = continuous_coordinates(
            parent_a, parent_b, offspring
        )
        if coords is None:
            continue
        u, v, residual, retention_sq, pdi, asymmetry, orthogonal_vec = coords
        dot_class = classify(retention_sq, asymmetry)

        parent_a_thr = np.where(parent_a_raw >= 0.0001, parent_a_raw, 0.0)
        parent_b_thr = np.where(parent_b_raw >= 0.0001, parent_b_raw, 0.0)
        offspring_thr = offspring_raw
        jac_a = jaccard_similarity(offspring_thr, parent_a_thr)
        jac_b = jaccard_similarity(offspring_thr, parent_b_thr)
        jac_orth = jaccard_similarity(offspring_thr, np.maximum(orthogonal_vec, 0.0))
        jac_class = classify_three_way_similarity(jac_a, jac_b, jac_orth)

        rows.append(
            {
                "SampleIDX": sid,
                "Medium": event["Medium"],
                "Medium_label": MEDIUM_LABELS[event["Medium"]],
                "u": u,
                "v": v,
                "residual": residual,
                "retention_sq": retention_sq,
                "pdi": pdi,
                "asymmetry": asymmetry,
                "dot_class": dot_class,
                "jaccard_to_A": jac_a,
                "jaccard_to_B": jac_b,
                "jaccard_to_residual": jac_orth,
                "jaccard_class": jac_class,
            }
        )
    return pd.DataFrame(rows)


def summarize(df):
    records = []
    for med in MEDIUM_ORDER:
        sub = df[df["Medium"] == med]
        records.append(
            {
                "metric": "continuous_asymmetry",
                "medium": MEDIUM_LABELS[med],
                "n": len(sub),
                "median": sub["asymmetry"].median(),
                "mean": sub["asymmetry"].mean(),
            }
        )
        records.append(
            {
                "metric": "retention_sq",
                "medium": MEDIUM_LABELS[med],
                "n": len(sub),
                "median": sub["retention_sq"].median(),
                "mean": sub["retention_sq"].mean(),
            }
        )
        for method, col in [("dot_product", "dot_class"), ("jaccard", "jaccard_class")]:
            counts = sub[col].value_counts()
            for cls in ["Dominance", "Mixture", "Restructuring"]:
                records.append(
                    {
                        "metric": method,
                        "medium": MEDIUM_LABELS[med],
                        "class": cls,
                        "n": int(counts.get(cls, 0)),
                        "fraction": counts.get(cls, 0) / len(sub),
                    }
                )
    asym_groups = [df[df["Medium"] == med]["asymmetry"] for med in MEDIUM_ORDER]
    ret_groups = [df[df["Medium"] == med]["retention_sq"] for med in MEDIUM_ORDER]
    kw_asym = kruskal(*asym_groups)
    kw_ret = kruskal(*ret_groups)
    records.append({"metric": "kruskal_asymmetry", "H": kw_asym.statistic, "p": kw_asym.pvalue})
    records.append({"metric": "kruskal_retention_sq", "H": kw_ret.statistic, "p": kw_ret.pvalue})
    summary = pd.DataFrame(records)
    df.to_csv(OUT_DIR / "r2_q3_event_metrics.csv", index=False)
    summary.to_csv(OUT_DIR / "r2_q3_summary_stats.csv", index=False)
    return summary


def draw_figure(df):
    mpl.rcParams.update(
        {
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "font.family": "DejaVu Sans",
            "axes.linewidth": 0.7,
            "font.size": 8,
        }
    )
    fig = plt.figure(figsize=(7.2, 3.3))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.25], wspace=0.38)

    ax = fig.add_subplot(gs[0, 0])
    for med in MEDIUM_ORDER:
        sub = df[df["Medium"] == med]
        ax.scatter(
            sub["retention_sq"],
            sub["asymmetry"],
            s=16,
            color=MEDIUM_COLORS[med],
            alpha=0.72,
            linewidth=0.2,
            edgecolor="white",
            label=f"{MEDIUM_LABELS[med]} (n={len(sub)})",
        )
    ax.axvline(0.5, color="0.35", lw=0.8, ls="--")
    ax.axhline(0.5, color="0.35", lw=0.8, ls="--")
    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(-0.03, 1.04)
    ax.set_xlabel("Retention magnitude, $r^2$")
    ax.set_ylabel("Parental asymmetry")
    ax.text(0.03, 0.94, "Restructuring", transform=ax.transAxes, color="0.35")
    ax.text(0.56, 0.08, "Mixture", transform=ax.transAxes, color="0.35")
    ax.text(0.56, 0.91, "CLS", transform=ax.transAxes, color="0.35")
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(-0.02, 0.57), fontsize=7)
    ax.set_title("A  Continuous similarity space", loc="left", fontweight="bold")

    ax2 = fig.add_subplot(gs[0, 1])
    width = 0.35
    x_base = np.arange(len(MEDIUM_ORDER))
    bottom_dot = np.zeros(len(MEDIUM_ORDER))
    bottom_jac = np.zeros(len(MEDIUM_ORDER))
    for cls in ["Dominance", "Mixture", "Restructuring"]:
        dot_vals = []
        jac_vals = []
        for med in MEDIUM_ORDER:
            sub = df[df["Medium"] == med]
            dot_vals.append((sub["dot_class"] == cls).mean())
            jac_vals.append((sub["jaccard_class"] == cls).mean())
        ax2.bar(x_base - width / 2, dot_vals, width, bottom=bottom_dot, color=CLASS_COLORS[cls], edgecolor="white", lw=0.4)
        ax2.bar(x_base + width / 2, jac_vals, width, bottom=bottom_jac, color=CLASS_COLORS[cls], edgecolor="white", lw=0.4, hatch="//" if cls == "Dominance" else None)
        bottom_dot += np.array(dot_vals)
        bottom_jac += np.array(jac_vals)

    ax2.set_xticks(x_base)
    ax2.set_xticklabels([MEDIUM_LABELS[m] for m in MEDIUM_ORDER])
    for i in range(len(MEDIUM_ORDER)):
        ax2.text(i - width / 2, -0.08, "dot", ha="center", va="top", fontsize=7, rotation=0)
        ax2.text(i + width / 2, -0.08, "Jac", ha="center", va="top", fontsize=7, rotation=0)
    ax2.set_ylim(0, 1.0)
    ax2.set_ylabel("Outcome fraction")
    handles = [plt.Rectangle((0, 0), 1, 1, color=CLASS_COLORS[c]) for c in ["Dominance", "Mixture", "Restructuring"]]
    ax2.legend(handles, ["CLS", "Mixture", "Restructuring"], frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=7)
    ax2.set_title("B  Dot product vs Jaccard classification", loc="left", fontweight="bold")

    for axis in [ax, ax2]:
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.tick_params(width=0.7, length=3)

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / "r2_q3_continuous_similarity_and_metric_divergence.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / "r2_q3_continuous_similarity_and_metric_divergence.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = build_table()
    summary = summarize(df)
    draw_figure(df)
    print(f"Wrote {len(df)} event records")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
