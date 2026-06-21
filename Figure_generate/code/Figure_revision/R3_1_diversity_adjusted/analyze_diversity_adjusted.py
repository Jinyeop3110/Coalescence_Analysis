#!/usr/bin/env python3
"""
analyze_diversity_adjusted.py
-----------------------------
R3-1 rebuttal: re-classify all coalescence events with a diversity-adjusted
Dominance threshold that scales with community richness (inverse Simpson).

The standard threshold y > 0.5 is replaced with:
    y_adj(N_eff) = 0.5 + k / sqrt(N_eff)     (additive form, primary)
    y_adj(N_eff) = 0.5 * (1 + k / sqrt(N_eff))  (multiplicative form, secondary)

We sweep k and report how the Dominance / Mixing / Restructuring proportions
evolve, overall and per medium.
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Path / import setup (mirror R3_1_additive_null)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

from COLORMAP import (
    MEDIUM_COLORS,
    PHASE_DIAGRAM_COLORS,
    get_medium_color,
)
from common_setup import (
    normalize,
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
)

CLASS_NAMES = {0: "Dominance", 1: "Mixing", 2: "Restructuring"}
CLASS_COLORS = {
    0: PHASE_DIAGRAM_COLORS["Dominance"],
    1: PHASE_DIAGRAM_COLORS["Mixing"],
    2: PHASE_DIAGRAM_COLORS["Restructuring"],
}
MEDIUM_MAP = {"L": "Nutr-", "M": "Base", "H": "Nutr+"}
MEDIUM_MAP_SHORT = {"L": "LN", "M": "MN", "H": "HN"}

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
sns.set_style("ticks")
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["figure.dpi"] = 200
mpl.rcParams["font.size"] = 8
mpl.rcParams["axes.linewidth"] = 0.5
mpl.rcParams["xtick.minor.width"] = 0.4
mpl.rcParams["xtick.major.width"] = 0.5
mpl.rcParams["ytick.minor.width"] = 0.4
mpl.rcParams["ytick.major.width"] = 0.5
plt.rcParams["text.usetex"] = False
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
coalescence_path = os.path.join(ROOT, "Analyzed", "processed_CoalescenceEvent_synthetic.xlsx")
sequences_path = os.path.join(ROOT, "Postprocessed", "processed_Sequences_synthetic.xlsx")

print("Loading data...")
coal_df = pd.read_excel(coalescence_path)
seq_df = pd.read_excel(sequences_path)

seq_lookup = {}
for _, row in seq_df.iterrows():
    sid = row["SampleIDX"]
    vec = row.iloc[1:].values.astype(float)
    seq_lookup[sid] = vec

# Exception list (same as common_setup.py)
exception_list = set(
    ["P4-02", "P4-03", "P4-23", "P4-24", "P7-97", "P8-12"]
    + ["P8-91"]
    + ["P5-73", "P5-69", "P5-64", "P5-61", "P5-59", "P5-56"]
    + ["P5-47", "P5-50"]
    + ["P5-39", "P5-87", "P5-54", "P6-02", "P6-47", "P6-74", "P6-57"]
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def inv_simpson(v):
    """Inverse Simpson index = 1 / sum(p_i^2)."""
    v = np.asarray(v, dtype=float)
    s = v.sum()
    if s <= 0:
        return np.nan
    p = v / s
    denom = np.sum(p ** 2)
    if denom <= 0:
        return np.nan
    return 1.0 / denom


def classify_with_adjusted_threshold(x, y, y_adj):
    """Mirror characterize_case but with a custom Dominance y-threshold.
    We keep the x^2 > 0.5 boundary fixed (primary analysis)."""
    if x ** 2 > 0.5 and y > y_adj:
        return 0  # Dominance
    if x ** 2 > 0.5 and y <= y_adj:
        return 1  # Mixing
    return 2  # Restructuring


def classify_event(n_C, n_A, n_B):
    """Return dict with u,v,k coeffs, (x,y), baseline class, or None."""
    n_A = np.asarray(n_A, dtype=float)
    n_B = np.asarray(n_B, dtype=float)
    n_C = np.asarray(n_C, dtype=float)
    if n_A.sum() < 1e-12 or n_B.sum() < 1e-12 or n_C.sum() < 1e-12:
        return None
    try:
        u, v, k = metric_VectorDecomposition_onlyPositive(n_A, n_B, n_C)
    except (np.linalg.LinAlgError, FloatingPointError, ZeroDivisionError):
        return None
    if not (np.isfinite(u) and np.isfinite(v) and np.isfinite(k)):
        return None
    x, y = calculate_assymetricity(u, v, k)
    if not (np.isfinite(x) and np.isfinite(y)):
        return None
    baseline = characterize_case(x, y)
    return dict(u=u, v=v, k=k, x=x, y=y, baseline=baseline)


# ---------------------------------------------------------------------------
# Per-event analysis
# ---------------------------------------------------------------------------
print("Classifying events and computing inverse Simpson...")
results = []

for _, event in coal_df.iterrows():
    sid = event["SampleIDX"]
    if sid in exception_list:
        continue
    sid_a = event["SampleIDX_Sub1"]
    sid_b = event["SampleIDX_Sub2"]
    medium = event["Medium"]

    n_C = seq_lookup.get(sid)
    n_A = seq_lookup.get(sid_a)
    n_B = seq_lookup.get(sid_b)
    if n_C is None or n_A is None or n_B is None:
        continue

    cls = classify_event(n_C, n_A, n_B)
    if cls is None:
        continue

    N_eff_C = inv_simpson(n_C)
    N_eff_A = inv_simpson(n_A)
    N_eff_B = inv_simpson(n_B)

    if not np.isfinite(N_eff_C):
        continue

    results.append({
        "SampleIDX": sid,
        "Medium": medium,
        "u": cls["u"],
        "v": cls["v"],
        "k_coef": cls["k"],
        "x": cls["x"],
        "y": cls["y"],
        "baseline_class": cls["baseline"],
        "N_eff_C": N_eff_C,
        "N_eff_A": N_eff_A,
        "N_eff_B": N_eff_B,
    })

df = pd.DataFrame(results)
print(f"\nTotal events classified: {len(df)}")

# ---------------------------------------------------------------------------
# Sweep k for both additive and multiplicative forms
# ---------------------------------------------------------------------------
k_values = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
k_report = [0.0, 0.5, 1.0, 2.0]  # values surfaced in console / memo

sweep_additive = {}      # k -> dataframe-like dict of class fractions
sweep_multiplic = {}

for k in k_values:
    # additive form: y_adj = 0.5 + k / sqrt(N_eff)
    y_adj_add = 0.5 + k / np.sqrt(df["N_eff_C"].values)
    # multiplicative form
    y_adj_mul = 0.5 * (1.0 + k / np.sqrt(df["N_eff_C"].values))

    classes_add = np.array([
        classify_with_adjusted_threshold(xi, yi, ya)
        for xi, yi, ya in zip(df["x"].values, df["y"].values, y_adj_add)
    ])
    classes_mul = np.array([
        classify_with_adjusted_threshold(xi, yi, ya)
        for xi, yi, ya in zip(df["x"].values, df["y"].values, y_adj_mul)
    ])
    sweep_additive[k] = classes_add
    sweep_multiplic[k] = classes_mul


def class_fractions(class_arr):
    tot = len(class_arr)
    return {c: (class_arr == c).sum() / tot if tot else 0 for c in [0, 1, 2]}


# Overall fractions per k
overall_add = {k: class_fractions(sweep_additive[k]) for k in k_values}
overall_mul = {k: class_fractions(sweep_multiplic[k]) for k in k_values}

# Per-medium fractions per k
per_med_add = {med: {} for med in ["L", "M", "H"]}
per_med_mul = {med: {} for med in ["L", "M", "H"]}
for k in k_values:
    for med in ["L", "M", "H"]:
        mask = (df["Medium"] == med).values
        per_med_add[med][k] = class_fractions(sweep_additive[k][mask])
        per_med_mul[med][k] = class_fractions(sweep_multiplic[k][mask])

# Store additive classifications as columns in df for cross-reference
for k in k_values:
    df[f"class_add_k{k}"] = sweep_additive[k]
    df[f"class_mul_k{k}"] = sweep_multiplic[k]


# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 72)
print("DIVERSITY-ADJUSTED DOMINANCE THRESHOLD")
print("Primary form: y_adj(N_eff) = 0.5 + k / sqrt(N_eff)")
print("=" * 72)

print("\nN_eff (inverse Simpson) summary:")
for col in ["N_eff_C", "N_eff_A", "N_eff_B"]:
    s = df[col].dropna()
    print(f"  {col}: mean={s.mean():.2f}  median={s.median():.2f}  "
          f"min={s.min():.2f}  max={s.max():.2f}  [n={len(s)}]")

print("\nPer-medium N_eff_C summary:")
for med in ["L", "M", "H"]:
    s = df.loc[df["Medium"] == med, "N_eff_C"]
    print(f"  {MEDIUM_MAP[med]:6s} (n={len(s):3d})  mean={s.mean():.2f}  "
          f"median={s.median():.2f}")

print("\nDominance / Mixing / Restructuring fractions (ADDITIVE form):")
print(f"{'k':>6s}  {'Dom':>7s}  {'Mix':>7s}  {'Rest':>7s}   |  "
      f"{'Nutr-':>7s}  {'Base':>7s}  {'Nutr+':>7s}  (Dom per-medium)")
for k in k_values:
    o = overall_add[k]
    m_l = per_med_add["L"][k][0]
    m_m = per_med_add["M"][k][0]
    m_h = per_med_add["H"][k][0]
    print(f"{k:6.2f}  {o[0]:7.1%}  {o[1]:7.1%}  {o[2]:7.1%}   |  "
          f"{m_l:7.1%}  {m_m:7.1%}  {m_h:7.1%}")

print("\nDominance / Mixing / Restructuring fractions (MULTIPLICATIVE form):")
print(f"{'k':>6s}  {'Dom':>7s}  {'Mix':>7s}  {'Rest':>7s}   |  "
      f"{'Nutr-':>7s}  {'Base':>7s}  {'Nutr+':>7s}  (Dom per-medium)")
for k in k_values:
    o = overall_mul[k]
    m_l = per_med_mul["L"][k][0]
    m_m = per_med_mul["M"][k][0]
    m_h = per_med_mul["H"][k][0]
    print(f"{k:6.2f}  {o[0]:7.1%}  {o[1]:7.1%}  {o[2]:7.1%}   |  "
          f"{m_l:7.1%}  {m_m:7.1%}  {m_h:7.1%}")

# Events that flip out of Dominance between k=0 and increasing k
print("\nEvents flipping OUT of Dominance (additive form):")
print(f"{'k':>6s}  {'# Dom @ k':>10s}  {'# flipped':>10s}  {'# remain':>10s}")
base_dom_mask = (sweep_additive[0.0] == 0)
base_dom_n = base_dom_mask.sum()
for k in k_values:
    dom_now_mask = (sweep_additive[k] == 0)
    flipped = int(base_dom_mask.sum() - dom_now_mask.sum()) if k > 0 else 0
    # This is just the count; every additional flip is a strictly lost dominance
    print(f"{k:6.2f}  {int(dom_now_mask.sum()):10d}  "
          f"{int((base_dom_mask & ~dom_now_mask).sum()):10d}  "
          f"{int((base_dom_mask & dom_now_mask).sum()):10d}")


# ---------------------------------------------------------------------------
# Helper: save figure as PDF
# ---------------------------------------------------------------------------
def save_pdf(fig, basename):
    path = os.path.join(SAVE_DIR, f"{basename}.pdf")
    fig.savefig(path, bbox_inches="tight", dpi=300)
    print(f"  Saved {path}")


# ===========================================================================
# FIGURE A: sweep figure (scatter + dominance-fraction-vs-k + flip counts)
# ===========================================================================
print("\nGenerating Fig_R3_1_diversity_adjusted_sweep.pdf ...")

fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.0))

# --- (a) Scatter of (N_eff_C, y) colored by medium + threshold curves ---
ax = axes[0]
for med in ["L", "M", "H"]:
    sub = df[df["Medium"] == med]
    ax.scatter(sub["N_eff_C"], sub["y"], s=10, alpha=0.6,
               color=get_medium_color(med), edgecolors="none",
               label=MEDIUM_MAP[med])

# Threshold curves for several k (additive form)
N_grid = np.linspace(df["N_eff_C"].min() * 0.9, df["N_eff_C"].max() * 1.05, 200)
N_grid = np.clip(N_grid, 1.0, None)
linestyles = ["-", "--", "-.", ":"]
for i, k in enumerate(k_report):
    y_curve = 0.5 + k / np.sqrt(N_grid)
    y_curve = np.clip(y_curve, 0, 1.05)
    ax.plot(N_grid, y_curve, color="k", linewidth=0.9,
            linestyle=linestyles[i % len(linestyles)], label=f"k = {k}")

ax.set_xlabel(r"$N_{\mathrm{eff}}$ (inverse Simpson of $n_C$)")
ax.set_ylabel("y (PDI / asymmetricity)")
ax.set_title("Per-event PDI vs richness\nwith adjusted Dominance curve", fontsize=8)
ax.set_ylim(-0.02, 1.08)
ax.legend(fontsize=6, frameon=False, loc="lower right", ncol=2)
sns.despine(ax=ax)

# --- (b) Dominance fraction vs k overall + per medium ---
ax = axes[1]
dom_overall = [overall_add[k][0] for k in k_values]
ax.plot(k_values, dom_overall, "-o", color="black", markersize=4, linewidth=1.2,
        label="Overall")
for med in ["L", "M", "H"]:
    dom_med = [per_med_add[med][k][0] for k in k_values]
    ax.plot(k_values, dom_med, "-o", color=get_medium_color(med),
            markersize=4, linewidth=1.2, label=MEDIUM_MAP[med])
ax.set_xlabel(r"adjustment strength $k$")
ax.set_ylabel("Dominance fraction")
ax.set_title("Dominance vs adjustment strength\n(additive form)", fontsize=8)
ax.set_ylim(-0.02, None)
ax.legend(fontsize=6, frameon=False, loc="upper right")
sns.despine(ax=ax)

# --- (c) Classification shifts: count leaving Dominance ---
ax = axes[2]
# Stacked: for each k, count how many events are Dom -> Mix (or Dom -> Rest),
# versus still Dom.
still_dom = []
flipped_mix = []
flipped_rest = []
for k in k_values:
    base_mask = base_dom_mask
    cur = sweep_additive[k]
    still_dom.append(int(((base_mask) & (cur == 0)).sum()))
    flipped_mix.append(int(((base_mask) & (cur == 1)).sum()))
    flipped_rest.append(int(((base_mask) & (cur == 2)).sum()))

kv = np.array(k_values)
width = (kv[1] - kv[0]) * 0.8 if len(kv) > 1 else 0.1
ax.bar(kv, still_dom, width=width, color=CLASS_COLORS[0], label="still Dominance",
       edgecolor="k", linewidth=0.3)
ax.bar(kv, flipped_mix, width=width, bottom=still_dom, color=CLASS_COLORS[1],
       label="-> Mixing", edgecolor="k", linewidth=0.3)
bot = np.array(still_dom) + np.array(flipped_mix)
ax.bar(kv, flipped_rest, width=width, bottom=bot, color=CLASS_COLORS[2],
       label="-> Restructuring", edgecolor="k", linewidth=0.3)
ax.set_xlabel(r"adjustment strength $k$")
ax.set_ylabel("Events classified Dominance at k=0")
ax.set_title("Fate of baseline Dominance events", fontsize=8)
ax.legend(fontsize=6, frameon=False, loc="upper right")
sns.despine(ax=ax)

for i, a in enumerate(axes):
    a.text(-0.18, 1.05, f"({chr(ord('a') + i)})", transform=a.transAxes,
           fontsize=10, fontweight="bold", va="bottom", ha="right")

fig.tight_layout()
save_pdf(fig, "Fig_R3_1_diversity_adjusted_sweep")
plt.close(fig)


# ===========================================================================
# FIGURE B: per-medium richness + dominance by richness tertile
# ===========================================================================
print("Generating Fig_R3_1_per_medium_richness.pdf ...")

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.0))

# --- (a) N_eff_C distribution per medium ---
ax = axes[0]
positions = {"L": 0, "M": 1, "H": 2}
box_data = [df.loc[df["Medium"] == m, "N_eff_C"].values for m in ["L", "M", "H"]]
bp = ax.boxplot(box_data, positions=[0, 1, 2], widths=0.55,
                patch_artist=True, showfliers=False)
for patch, med in zip(bp["boxes"], ["L", "M", "H"]):
    patch.set_facecolor(get_medium_color(med))
    patch.set_alpha(0.5)
    patch.set_edgecolor("k")
    patch.set_linewidth(0.5)
for whisker in bp["whiskers"]:
    whisker.set(color="k", linewidth=0.5)
for cap in bp["caps"]:
    cap.set(color="k", linewidth=0.5)
for med_idx, med in enumerate(["L", "M", "H"]):
    y = df.loc[df["Medium"] == med, "N_eff_C"].values
    xj = np.random.uniform(-0.12, 0.12, size=len(y)) + med_idx
    ax.scatter(xj, y, color=get_medium_color(med), s=5, alpha=0.6,
               edgecolors="none")
ax.set_xticks([0, 1, 2])
ax.set_xticklabels([MEDIUM_MAP[m] for m in ["L", "M", "H"]])
ax.set_ylabel(r"$N_{\mathrm{eff}}$ (inverse Simpson, $n_C$)")
ax.set_title("Coalesced-community richness per medium", fontsize=8)
sns.despine(ax=ax)

# --- (b) Baseline Dominance fraction by N_eff_C tertile per medium ---
ax = axes[1]
# Compute tertile thresholds from all data
q33, q66 = np.quantile(df["N_eff_C"].values, [1 / 3, 2 / 3])

def tertile_of(v):
    if v < q33:
        return "low"
    elif v < q66:
        return "mid"
    return "high"

df["tertile"] = df["N_eff_C"].apply(tertile_of)

tertile_order = ["low", "mid", "high"]
bar_width = 0.26
x_pos = np.arange(len(tertile_order))
for i, med in enumerate(["L", "M", "H"]):
    fracs = []
    ns = []
    for t in tertile_order:
        sub = df[(df["Medium"] == med) & (df["tertile"] == t)]
        if len(sub) == 0:
            fracs.append(0)
            ns.append(0)
        else:
            fracs.append((sub["baseline_class"] == 0).mean())
            ns.append(len(sub))
    pos = x_pos + (i - 1) * bar_width
    bars = ax.bar(pos, fracs, width=bar_width, color=get_medium_color(med),
                  edgecolor="k", linewidth=0.4, label=MEDIUM_MAP[med])
    for b, n in zip(bars, ns):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.015,
                f"n={n}", ha="center", va="bottom", fontsize=5)

ax.set_xticks(x_pos)
ax.set_xticklabels([f"{t}\n({MEDIUM_MAP_SHORT.get('', '')}"
                    + f"$N_{{eff}}$)" if False else t
                    for t in tertile_order])
ax.set_xticklabels([f"low\n(<{q33:.1f})", f"mid\n({q33:.1f}-{q66:.1f})",
                    f"high\n(>{q66:.1f})"])
ax.set_ylabel("Baseline Dominance fraction")
ax.set_title("Dominance by richness tertile (k = 0)", fontsize=8)
ax.legend(fontsize=6, frameon=False, loc="upper right")
ax.set_ylim(0, max(0.5, ax.get_ylim()[1]))
sns.despine(ax=ax)

for i, a in enumerate(axes):
    a.text(-0.18, 1.05, f"({chr(ord('a') + i)})", transform=a.transAxes,
           fontsize=10, fontweight="bold", va="bottom", ha="right")

fig.tight_layout()
save_pdf(fig, "Fig_R3_1_per_medium_richness")
plt.close(fig)

# ===========================================================================
# JOINT-AXIS ADJUSTMENT (y AND x^2) -- sensitivity check
# ===========================================================================
# Tighten BOTH the Dominance y-threshold AND the retention x^2-threshold
# as a function of N_eff. This tests whether the Dominance signal survives
# simultaneous correction for low-richness geometric inflation on both axes.
#
#   y_adj(N_eff)   = min(1, 0.5 + k_y / sqrt(N_eff))
#   x2_adj(N_eff)  = min(1, 0.5 + k_x / sqrt(N_eff))
# ===========================================================================


def classify_joint(x, y, y_adj, x2_adj):
    if x ** 2 > x2_adj and y > y_adj:
        return 0   # Dominance
    if x ** 2 > x2_adj and y <= y_adj:
        return 1   # Mixing
    return 2       # Restructuring


print("\n" + "=" * 72)
print("JOINT-AXIS ADJUSTMENT: tighten BOTH y_adj AND x2_adj simultaneously")
print("=" * 72)

k_grid_joint = [0.0, 0.25, 0.5, 0.75, 1.0]
joint_results = {}
for k_y in k_grid_joint:
    for k_x in k_grid_joint:
        y_thr = np.minimum(1.0, 0.5 + k_y / np.sqrt(df["N_eff_C"].values))
        x2_thr = np.minimum(1.0, 0.5 + k_x / np.sqrt(df["N_eff_C"].values))
        classes = np.array([
            classify_joint(xi, yi, y_a, x2_a)
            for xi, yi, y_a, x2_a in zip(df["x"].values, df["y"].values, y_thr, x2_thr)
        ])
        per_med = {}
        for med in ["L", "M", "H"]:
            mask = (df["Medium"] == med).values
            per_med[med] = (classes[mask] == 0).mean() if mask.sum() else np.nan
        joint_results[(k_y, k_x)] = dict(
            D=(classes == 0).mean(),
            M=(classes == 1).mean(),
            R=(classes == 2).mean(),
            per_med=per_med,
            classes=classes,
        )

# Console: diagonal sweep
print("\nDiagonal sweep (k_y = k_x = k):")
print(f"{'k':>6s}  {'Dom':>7s}  {'Mix':>7s}  {'Rest':>7s}   |  {'LN':>6s}  {'MN':>6s}  {'HN':>6s}")
for k in k_grid_joint:
    r = joint_results[(k, k)]
    print(f"{k:6.2f}  {r['D']:7.1%}  {r['M']:7.1%}  {r['R']:7.1%}   |  "
          f"{r['per_med']['L']:6.1%}  {r['per_med']['M']:6.1%}  {r['per_med']['H']:6.1%}")

# Console: selected off-diagonal cells
print("\nSelected off-diagonal (k_y, k_x) cells (pooled Dominance):")
for (ky, kx) in [(0.5, 0.0), (0.0, 0.5), (0.5, 0.5), (1.0, 0.5), (0.5, 1.0)]:
    r = joint_results[(ky, kx)]
    print(f"  (k_y={ky}, k_x={kx}): Dom={r['D']:.1%}  Mix={r['M']:.1%}  Rest={r['R']:.1%}   "
          f"|  LN={r['per_med']['L']:.1%}  MN={r['per_med']['M']:.1%}  HN={r['per_med']['H']:.1%}")

# Build heatmaps
K = len(k_grid_joint)
heat_D = np.zeros((K, K))
heat_ln = np.zeros((K, K))
heat_mn = np.zeros((K, K))
heat_hn = np.zeros((K, K))
for i, k_y in enumerate(k_grid_joint):
    for j, k_x in enumerate(k_grid_joint):
        r = joint_results[(k_y, k_x)]
        heat_D[i, j] = r["D"]
        heat_ln[i, j] = r["per_med"]["L"]
        heat_mn[i, j] = r["per_med"]["M"]
        heat_hn[i, j] = r["per_med"]["H"]

# ---- Figure: joint-axis adjustment ----
print("\nGenerating Fig_R3_1_diversity_adjusted_joint.pdf ...")
fig, axes = plt.subplots(2, 3, figsize=(10.5, 6.3))

# (a) Diagonal sweep: Dominance fraction vs k, overall + per medium
ax = axes[0, 0]
overall_diag = [joint_results[(k, k)]["D"] for k in k_grid_joint]
ax.plot(k_grid_joint, overall_diag, "-o", color="black", markersize=5, linewidth=1.3, label="Overall")
for med in ["L", "M", "H"]:
    diag = [joint_results[(k, k)]["per_med"][med] for k in k_grid_joint]
    ax.plot(k_grid_joint, diag, "-o", color=get_medium_color(med),
            markersize=5, linewidth=1.2, label=MEDIUM_MAP[med])
# Overlay y-only sweep as dashed for comparison
y_only_overall = [overall_add[k][0] for k in k_grid_joint]
ax.plot(k_grid_joint, y_only_overall, "--", color="gray", linewidth=1.0,
        label="y-only (Option H)")
ax.set_xlabel(r"joint adjustment $k = k_y = k_x$")
ax.set_ylabel("Dominance fraction")
ax.set_title("(a) Joint diagonal sweep", fontsize=8)
ax.legend(fontsize=6, frameon=False, loc="upper right")
sns.despine(ax=ax)

# (b) Stacked classification composition at diagonal sweep
ax = axes[0, 1]
diag_D = np.array([joint_results[(k, k)]["D"] for k in k_grid_joint])
diag_M = np.array([joint_results[(k, k)]["M"] for k in k_grid_joint])
diag_R = np.array([joint_results[(k, k)]["R"] for k in k_grid_joint])
kg = np.array(k_grid_joint)
ax.fill_between(kg, 0, diag_D, color=CLASS_COLORS[0], alpha=0.85, label="Dominance")
ax.fill_between(kg, diag_D, diag_D + diag_M, color=CLASS_COLORS[1], alpha=0.85, label="Mixing")
ax.fill_between(kg, diag_D + diag_M, diag_D + diag_M + diag_R,
                color=CLASS_COLORS[2], alpha=0.85, label="Restructuring")
ax.set_xlabel(r"joint adjustment $k$")
ax.set_ylabel("Class fraction")
ax.set_ylim(0, 1)
ax.set_xlim(kg[0], kg[-1])
ax.set_title("(b) Class composition vs k (diagonal)", fontsize=8)
ax.legend(fontsize=6, frameon=False, loc="center right")
sns.despine(ax=ax)

# (c) Pooled Dominance heatmap vs (k_y, k_x)
ax = axes[0, 2]
im = ax.imshow(heat_D, origin="lower", cmap="viridis", vmin=0, vmax=heat_D.max())
for i in range(K):
    for j in range(K):
        ax.text(j, i, f"{heat_D[i, j]*100:.0f}", ha="center", va="center",
                fontsize=6, color="white" if heat_D[i, j] < 0.3 else "black")
ax.set_xticks(range(K)); ax.set_xticklabels([f"{k}" for k in k_grid_joint], fontsize=6)
ax.set_yticks(range(K)); ax.set_yticklabels([f"{k}" for k in k_grid_joint], fontsize=6)
ax.set_xlabel(r"$k_x$ (retention adj.)")
ax.set_ylabel(r"$k_y$ (PDI adj.)")
ax.set_title("(c) Pooled Dominance %", fontsize=8)
plt.colorbar(im, ax=ax, shrink=0.7)

# (d-f) Per-medium heatmaps
for col_idx, (med, heat) in enumerate(zip(["L", "M", "H"], [heat_ln, heat_mn, heat_hn])):
    ax = axes[1, col_idx]
    im = ax.imshow(heat, origin="lower", cmap="viridis", vmin=0, vmax=1.0)
    for i in range(K):
        for j in range(K):
            ax.text(j, i, f"{heat[i, j]*100:.0f}", ha="center", va="center",
                    fontsize=6, color="white" if heat[i, j] < 0.4 else "black")
    ax.set_xticks(range(K)); ax.set_xticklabels([f"{k}" for k in k_grid_joint], fontsize=6)
    ax.set_yticks(range(K)); ax.set_yticklabels([f"{k}" for k in k_grid_joint], fontsize=6)
    ax.set_xlabel(r"$k_x$")
    ax.set_ylabel(r"$k_y$")
    ax.set_title(f"({chr(ord('d') + col_idx)}) {MEDIUM_MAP[med]} Dominance %", fontsize=8)
    plt.colorbar(im, ax=ax, shrink=0.7)

fig.tight_layout()
save_pdf(fig, "Fig_R3_1_diversity_adjusted_joint")
plt.close(fig)

# ---- Save joint-axis CSV ----
joint_rows = []
for (k_y, k_x), r in joint_results.items():
    row = {"k_y": k_y, "k_x": k_x,
           "overall_Dominance": r["D"],
           "overall_Mixing": r["M"],
           "overall_Restructuring": r["R"]}
    for med in ["L", "M", "H"]:
        row[f"{MEDIUM_MAP_SHORT[med]}_Dominance"] = r["per_med"][med]
    joint_rows.append(row)
joint_csv = pd.DataFrame(joint_rows).sort_values(["k_y", "k_x"])
joint_csv_path = os.path.join(SAVE_DIR, "diversity_adjusted_joint.csv")
joint_csv.to_csv(joint_csv_path, index=False, float_format="%.4f")
print(f"Joint-axis table written to {joint_csv_path}")


# ---------------------------------------------------------------------------
# Dump sweep table as CSV for the memo
# ---------------------------------------------------------------------------
rows = []
for k in k_values:
    row = {"k": k, "form": "additive"}
    row["overall_Dominance"] = overall_add[k][0]
    row["overall_Mixing"] = overall_add[k][1]
    row["overall_Restructuring"] = overall_add[k][2]
    for med in ["L", "M", "H"]:
        row[f"{MEDIUM_MAP_SHORT[med]}_Dominance"] = per_med_add[med][k][0]
        row[f"{MEDIUM_MAP_SHORT[med]}_Mixing"] = per_med_add[med][k][1]
        row[f"{MEDIUM_MAP_SHORT[med]}_Restructuring"] = per_med_add[med][k][2]
    rows.append(row)
for k in k_values:
    row = {"k": k, "form": "multiplicative"}
    row["overall_Dominance"] = overall_mul[k][0]
    row["overall_Mixing"] = overall_mul[k][1]
    row["overall_Restructuring"] = overall_mul[k][2]
    for med in ["L", "M", "H"]:
        row[f"{MEDIUM_MAP_SHORT[med]}_Dominance"] = per_med_mul[med][k][0]
        row[f"{MEDIUM_MAP_SHORT[med]}_Mixing"] = per_med_mul[med][k][1]
        row[f"{MEDIUM_MAP_SHORT[med]}_Restructuring"] = per_med_mul[med][k][2]
    rows.append(row)

sweep_csv = pd.DataFrame(rows)
sweep_csv_path = os.path.join(SAVE_DIR, "diversity_adjusted_sweep.csv")
sweep_csv.to_csv(sweep_csv_path, index=False, float_format="%.4f")
print(f"\nSweep table written to {sweep_csv_path}")

per_event_csv_path = os.path.join(SAVE_DIR, "diversity_adjusted_per_event.csv")
df.to_csv(per_event_csv_path, index=False, float_format="%.4f")
print(f"Per-event table written to {per_event_csv_path}")


# ---------------------------------------------------------------------------
# Final summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 72)
print("FINAL SUMMARY")
print("=" * 72)
print(f"\nTotal events: {len(df)}")
print(f"Baseline (k=0) Dominance count: {int((df['baseline_class']==0).sum())}")

print("\nDominance fraction by k (additive form):")
for k in k_report:
    o = overall_add[k]
    pm = per_med_add
    print(f"  k = {k}:  overall = {o[0]:.1%}  |  "
          f"{MEDIUM_MAP['L']} = {pm['L'][k][0]:.1%}  "
          f"{MEDIUM_MAP['M']} = {pm['M'][k][0]:.1%}  "
          f"{MEDIUM_MAP['H']} = {pm['H'][k][0]:.1%}")

print("\nFlips out of Dominance (relative to k=0):")
for k in k_report:
    cur_mask = sweep_additive[k] == 0
    flipped = int((base_dom_mask & ~cur_mask).sum())
    print(f"  k = {k}:  {flipped} flipped out "
          f"({flipped}/{int(base_dom_n)} = "
          f"{flipped / max(int(base_dom_n), 1):.1%})")

print("\nDone.")
