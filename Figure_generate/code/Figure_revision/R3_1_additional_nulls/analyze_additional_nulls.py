#!/usr/bin/env python3
"""R3-1 additional null models (Null A / B / C) for the reviewer 3 rebuttal."""

import sys
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Path / import setup
# ---------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

from COLORMAP import (
    MEDIUM_COLORS,
    PHASE_DIAGRAM_COLORS,
    get_medium_color,
)
from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
)

SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

CLASS_NAMES = {0: "Dominance", 1: "Mixing", 2: "Restructuring"}
CLASS_COLORS = {
    0: PHASE_DIAGRAM_COLORS["Dominance"],
    1: PHASE_DIAGRAM_COLORS["Mixing"],
    2: PHASE_DIAGRAM_COLORS["Restructuring"],
}
MEDIUM_MAP = {"L": "LN", "M": "MN", "H": "HN"}
MEDIUM_LABELS_SHORT = {"L": "LN (Nutr-)", "M": "MN (Base)", "H": "HN (Nutr+)"}
MEDIUM_ORDER = ["L", "M", "H"]

# ---------------------------------------------------------------------------
# Style (rcParams from common_setup)
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

RNG = np.random.default_rng(42)
B_DRAWS = 500

# ---------------------------------------------------------------------------
# Data load
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

exception_list = set(
    ["P4-02", "P4-03", "P4-23", "P4-24", "P7-97", "P8-12"]
    + ["P8-91"]
    + ["P5-73", "P5-69", "P5-64", "P5-61", "P5-59", "P5-56"]
    + ["P5-47", "P5-50"]
    + ["P5-39", "P5-87", "P5-54", "P6-02", "P6-47", "P6-74", "P6-57"]
)


# ---------------------------------------------------------------------------
# Core pipeline helpers
# ---------------------------------------------------------------------------
def classify_vector(n_C, n_A, n_B):
    """Run decomposition + asymm + characterize, return class or None."""
    n_A = np.asarray(n_A, dtype=float)
    n_B = np.asarray(n_B, dtype=float)
    n_C = np.asarray(n_C, dtype=float)
    if np.sum(n_A) < 1e-12 or np.sum(n_B) < 1e-12 or np.sum(n_C) < 1e-12:
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
    return characterize_case(x, y)


def inverse_simpson(p):
    """N_eff = 1 / sum(p_i^2) on a normalized vector."""
    s = np.sum(p)
    if s <= 0:
        return np.nan
    q = p / s
    ss = np.sum(q * q)
    if ss <= 0:
        return np.nan
    return 1.0 / ss


# ---------------------------------------------------------------------------
# Build the per-event table (filter to ~263 events)
# ---------------------------------------------------------------------------
print("Building event table...")
events = []
for _, ev in coal_df.iterrows():
    sid = ev["SampleIDX"]
    if sid in exception_list:
        continue
    sid1 = ev["SampleIDX_Sub1"]
    sid2 = ev["SampleIDX_Sub2"]
    medium = ev["Medium"]
    n_C = seq_lookup.get(sid)
    n_A = seq_lookup.get(sid1)
    n_B = seq_lookup.get(sid2)
    if n_C is None or n_A is None or n_B is None:
        continue
    if np.sum(n_A) < 1e-12 or np.sum(n_B) < 1e-12 or np.sum(n_C) < 1e-12:
        continue
    obs_cls = classify_vector(n_C, n_A, n_B)
    if obs_cls is None:
        continue
    n_A_n = n_A / np.sum(n_A)
    n_B_n = n_B / np.sum(n_B)
    n_C_n = n_C / np.sum(n_C)
    events.append({
        "SampleIDX": sid,
        "Medium": medium,
        "n_A": n_A_n,
        "n_B": n_B_n,
        "n_C": n_C_n,
        "obs_class": obs_cls,
        "Neff_C": inverse_simpson(n_C_n),
    })

events_df = pd.DataFrame(events)
print(f"Total events: {len(events_df)}")


# ---------------------------------------------------------------------------
# N_eff tertile bins (on n_C)
# ---------------------------------------------------------------------------
neff_vals = events_df["Neff_C"].values
# Tertiles (3 bins)
t_low, t_mid = np.quantile(neff_vals, [1 / 3, 2 / 3])
def neff_tertile(v):
    if v <= t_low:
        return 0
    if v <= t_mid:
        return 1
    return 2

events_df["Neff_tertile"] = events_df["Neff_C"].apply(neff_tertile)
TERTILE_LABELS = {0: "Low N_eff", 1: "Mid N_eff", 2: "High N_eff"}
print(f"N_eff tertile boundaries: low<={t_low:.2f} < mid<={t_mid:.2f} < high")

# Also use quartile bins (4 bins) for Null B
q_edges = np.quantile(neff_vals, [0.25, 0.5, 0.75])
def neff_quartile(v):
    if v <= q_edges[0]:
        return 0
    if v <= q_edges[1]:
        return 1
    if v <= q_edges[2]:
        return 2
    return 3

events_df["Neff_quartile"] = events_df["Neff_C"].apply(neff_quartile)


# ===========================================================================
# NULL A — richness-matched identity-permuted null
# ===========================================================================
def null_A_draw(n_A, n_B, n_C, rng):
    """One Null A draw: n_C's sorted shape assigned to random species in supp(A U B)."""
    supp = np.where((n_A > 0) | (n_B > 0))[0]
    nz_C = n_C[n_C > 0]
    if len(nz_C) == 0 or len(supp) == 0:
        return None
    shape = np.sort(nz_C)[::-1]  # descending
    k = len(shape)
    if k > len(supp):
        # can't place k distinct ranks into smaller support; truncate shape
        shape = shape[: len(supp)]
        k = len(shape)
    pick = rng.choice(supp, size=k, replace=False)
    out = np.zeros_like(n_A)
    out[pick] = shape
    s = out.sum()
    if s <= 0:
        return None
    return out / s


def run_null_A(events_df, B=B_DRAWS, rng=None):
    if rng is None:
        rng = np.random.default_rng(42)
    rates = np.zeros(len(events_df))
    mean_null_cls = np.zeros((len(events_df), 3))
    for i, ev in events_df.iterrows():
        counts = np.zeros(3)
        for _ in range(B):
            nC_null = null_A_draw(ev["n_A"], ev["n_B"], ev["n_C"], rng)
            if nC_null is None:
                continue
            cls = classify_vector(nC_null, ev["n_A"], ev["n_B"])
            if cls is None:
                continue
            counts[cls] += 1
        tot = counts.sum()
        if tot > 0:
            mean_null_cls[i] = counts / tot
            rates[i] = counts[0] / tot
        else:
            rates[i] = np.nan
            mean_null_cls[i] = np.nan
    return rates, mean_null_cls


print("\nRunning Null A...")
nullA_rates, nullA_frac = run_null_A(events_df, B=B_DRAWS, rng=np.random.default_rng(42))
events_df["nullA_dom_rate"] = nullA_rates
events_df["nullA_frac_D"] = nullA_frac[:, 0]
events_df["nullA_frac_M"] = nullA_frac[:, 1]
events_df["nullA_frac_R"] = nullA_frac[:, 2]


# ===========================================================================
# NULL B — richness-stratified bootstrap of observed n_C
# ===========================================================================
def null_B_draw(donor_nC, n_A, n_B):
    """Intersect donor n_C support with supp(A U B), renormalize."""
    supp = (n_A > 0) | (n_B > 0)
    out = np.asarray(donor_nC, dtype=float).copy()
    out[~supp] = 0.0
    s = out.sum()
    if s <= 0:
        return None
    return out / s


def run_null_B(events_df, variant="within_medium", B=B_DRAWS, rng=None, bin_col="Neff_quartile"):
    """variant in {'within_medium','any_medium'}."""
    if rng is None:
        rng = np.random.default_rng(42)
    n_events = len(events_df)
    rates = np.full(n_events, np.nan)
    frac = np.full((n_events, 3), np.nan)

    # Pre-build donor pools per (medium, bin) or (bin)
    pools = {}
    if variant == "within_medium":
        for med in MEDIUM_ORDER:
            for b in events_df[bin_col].unique():
                sel = events_df[(events_df["Medium"] == med) & (events_df[bin_col] == b)]
                pools[(med, b)] = sel.index.to_numpy()
    else:
        for b in events_df[bin_col].unique():
            sel = events_df[events_df[bin_col] == b]
            pools[(None, b)] = sel.index.to_numpy()

    for i, ev in events_df.iterrows():
        key = (ev["Medium"], ev[bin_col]) if variant == "within_medium" else (None, ev[bin_col])
        pool = pools.get(key, np.array([], dtype=int))
        pool = pool[pool != i]  # exclude self
        if len(pool) == 0:
            continue
        counts = np.zeros(3)
        picks = rng.choice(pool, size=B, replace=True)
        for j in picks:
            donor_nC = events_df.at[j, "n_C"]
            nC_null = null_B_draw(donor_nC, ev["n_A"], ev["n_B"])
            if nC_null is None:
                continue
            cls = classify_vector(nC_null, ev["n_A"], ev["n_B"])
            if cls is None:
                continue
            counts[cls] += 1
        tot = counts.sum()
        if tot > 0:
            frac[i] = counts / tot
            rates[i] = counts[0] / tot
    return rates, frac


print("\nRunning Null B (within medium, same quartile)...")
nullB_wm_rates, nullB_wm_frac = run_null_B(events_df, variant="within_medium",
                                            B=B_DRAWS, rng=np.random.default_rng(43))
events_df["nullB_wm_dom_rate"] = nullB_wm_rates

print("Running Null B (any medium, same quartile)...")
nullB_any_rates, nullB_any_frac = run_null_B(events_df, variant="any_medium",
                                              B=B_DRAWS, rng=np.random.default_rng(44))
events_df["nullB_any_dom_rate"] = nullB_any_rates


# ===========================================================================
# NULL C — weighted mixing sweep alpha*nA + (1-alpha)*nB
# ===========================================================================
ALPHAS = np.round(np.linspace(0, 1, 11), 2)


def run_null_C(events_df, alphas=ALPHAS):
    n_events = len(events_df)
    n_alpha = len(alphas)
    cls_matrix = np.full((n_events, n_alpha), -1, dtype=int)
    for i, ev in events_df.iterrows():
        nA, nB = ev["n_A"], ev["n_B"]
        for a_idx, a in enumerate(alphas):
            mix = a * nA + (1 - a) * nB
            s = mix.sum()
            if s <= 0:
                continue
            mix = mix / s
            cls = classify_vector(mix, nA, nB)
            if cls is None:
                continue
            cls_matrix[i, a_idx] = cls
    return cls_matrix


print("\nRunning Null C (alpha sweep)...")
nullC_cls = run_null_C(events_df, ALPHAS)
# per-event fraction of alphas landing in Dominance
events_df["nullC_frac_dom"] = np.mean(nullC_cls == 0, axis=1)
# at alpha=0.5
alpha05_idx = int(np.argmin(np.abs(ALPHAS - 0.5)))
events_df["nullC_class_at_0.5"] = nullC_cls[:, alpha05_idx]
events_df["nullC_any_alpha_dom"] = (nullC_cls == 0).any(axis=1).astype(int)


# ---------------------------------------------------------------------------
# Summary utilities
# ---------------------------------------------------------------------------
def pooled_dom_rate(series):
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) == 0:
        return np.nan
    return float(s.mean())


def boot_ci(vals, nboot=1000, ci=95, rng=None):
    vals = np.asarray(vals, dtype=float)
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return (np.nan, np.nan)
    if rng is None:
        rng = np.random.default_rng(0)
    boots = np.array([rng.choice(vals, size=len(vals), replace=True).mean()
                      for _ in range(nboot)])
    lo = np.percentile(boots, (100 - ci) / 2)
    hi = np.percentile(boots, 100 - (100 - ci) / 2)
    return (float(lo), float(hi))


# ---------------------------------------------------------------------------
# Console summary: per-medium and per-tertile Dominance rates
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("SUMMARY: Dominance rates (per medium)")
print("=" * 70)
summary_rows = []
for med in ["all"] + MEDIUM_ORDER:
    sub = events_df if med == "all" else events_df[events_df["Medium"] == med]
    med_label = "ALL" if med == "all" else MEDIUM_MAP[med]
    obs_D = (sub["obs_class"] == 0).mean() if len(sub) else np.nan
    nA_D = sub["nullA_dom_rate"].mean()
    nBwm_D = sub["nullB_wm_dom_rate"].mean()
    nBany_D = sub["nullB_any_dom_rate"].mean()
    nC05_D = (sub["nullC_class_at_0.5"] == 0).mean() if len(sub) else np.nan
    nCany_D = (sub["nullC_any_alpha_dom"] == 1).mean() if len(sub) else np.nan
    summary_rows.append(dict(medium=med_label, n=len(sub),
                             obs_D=obs_D, nullA_D=nA_D,
                             nullB_wm_D=nBwm_D, nullB_any_D=nBany_D,
                             nullC05_D=nC05_D, nullC_any_D=nCany_D))
    print(f"{med_label:5s} (n={len(sub):3d}): "
          f"Obs={obs_D:.3f}  A={nA_D:.3f}  B_wm={nBwm_D:.3f}  "
          f"B_any={nBany_D:.3f}  C@0.5={nC05_D:.3f}  C_any={nCany_D:.3f}")
summary_df = pd.DataFrame(summary_rows)

print("\n" + "=" * 70)
print("SUMMARY: Dominance rates (per N_eff tertile)")
print("=" * 70)
tertile_rows = []
for t in [0, 1, 2]:
    sub = events_df[events_df["Neff_tertile"] == t]
    obs_D = (sub["obs_class"] == 0).mean() if len(sub) else np.nan
    nA_D = sub["nullA_dom_rate"].mean()
    nBwm_D = sub["nullB_wm_dom_rate"].mean()
    nBany_D = sub["nullB_any_dom_rate"].mean()
    nC05_D = (sub["nullC_class_at_0.5"] == 0).mean() if len(sub) else np.nan
    tertile_rows.append(dict(tertile=TERTILE_LABELS[t], n=len(sub),
                             obs_D=obs_D, nullA_D=nA_D,
                             nullB_wm_D=nBwm_D, nullB_any_D=nBany_D,
                             nullC05_D=nC05_D))
    print(f"{TERTILE_LABELS[t]:12s} (n={len(sub):3d}): "
          f"Obs={obs_D:.3f}  A={nA_D:.3f}  B_wm={nBwm_D:.3f}  "
          f"B_any={nBany_D:.3f}  C@0.5={nC05_D:.3f}")
tertile_df = pd.DataFrame(tertile_rows)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def save_pdf(fig, name):
    path = os.path.join(SAVE_DIR, name)
    fig.savefig(path, bbox_inches="tight", dpi=300)
    print(f"  Saved {name}")
    plt.close(fig)


# ===========================================================================
# FIGURE: Null A
# ===========================================================================
print("\nPlotting Fig_NullA_permutation...")
figA, axesA = plt.subplots(1, 3, figsize=(9.0, 2.8))

# (i) per-event Null-A Dominance rate vs observed class
axA0 = axesA[0]
for cls_i in [0, 1, 2]:
    vals = events_df.loc[events_df["obs_class"] == cls_i, "nullA_dom_rate"].dropna()
    if len(vals) == 0:
        continue
    jitter = RNG.normal(0, 0.06, size=len(vals))
    axA0.scatter(np.full(len(vals), cls_i) + jitter, vals,
                 color=CLASS_COLORS[cls_i], s=8, alpha=0.5,
                 edgecolors="none", label=CLASS_NAMES[cls_i])
axA0.set_xticks([0, 1, 2])
axA0.set_xticklabels(["Dom", "Mix", "Rest"], fontsize=7)
axA0.set_xlabel("Observed class")
axA0.set_ylabel("Null A Dominance rate (per event)")
axA0.set_ylim(-0.05, 1.05)
axA0.axhline(0.5, color="k", ls="--", lw=0.4, alpha=0.5)
sns.despine(ax=axA0)
axA0.set_title("(a) Per-event null Dominance rate", fontsize=8)

# (ii) per-medium contingency: observed Dominance fraction vs mean null Dominance rate
axA1 = axesA[1]
meds = MEDIUM_ORDER
x_pos = np.arange(len(meds))
width = 0.35
obs_vals = [(events_df[events_df["Medium"] == m]["obs_class"] == 0).mean() for m in meds]
null_means = []
null_cis = []
for m in meds:
    sub = events_df[events_df["Medium"] == m]
    vals = sub["nullA_dom_rate"].dropna().values
    null_means.append(np.mean(vals) if len(vals) else np.nan)
    null_cis.append(boot_ci(vals, nboot=1000, rng=np.random.default_rng(10)))
colors_bar = [get_medium_color(m) for m in meds]
axA1.bar(x_pos - width/2, obs_vals, width, color=colors_bar,
         edgecolor="k", linewidth=0.4, label="Observed")
yerr_lo = [null_means[i] - null_cis[i][0] for i in range(len(meds))]
yerr_hi = [null_cis[i][1] - null_means[i] for i in range(len(meds))]
axA1.bar(x_pos + width/2, null_means, width, color=colors_bar,
         edgecolor="k", linewidth=0.4, alpha=0.4,
         yerr=[yerr_lo, yerr_hi], capsize=3, label="Null A (mean+/-95% CI)")
axA1.set_xticks(x_pos)
axA1.set_xticklabels([MEDIUM_LABELS_SHORT[m] for m in meds], fontsize=7)
axA1.set_ylabel("Dominance fraction")
axA1.set_title("(b) Per-medium Dominance: Obs vs Null A", fontsize=8)
axA1.legend(fontsize=6, frameon=False, loc="upper right")
axA1.set_ylim(0, max(0.5, max(obs_vals + null_means) * 1.3 + 0.05))
sns.despine(ax=axA1)

# (iii) stratified by N_eff tertile
axA2 = axesA[2]
x_pos2 = np.arange(3)
obs_t = [(events_df[events_df["Neff_tertile"] == t]["obs_class"] == 0).mean() for t in [0, 1, 2]]
nA_t = [events_df[events_df["Neff_tertile"] == t]["nullA_dom_rate"].mean() for t in [0, 1, 2]]
axA2.bar(x_pos2 - width/2, obs_t, width, color="#444444",
         edgecolor="k", linewidth=0.4, label="Observed")
axA2.bar(x_pos2 + width/2, nA_t, width, color="#BBBBBB",
         edgecolor="k", linewidth=0.4, label="Null A")
axA2.set_xticks(x_pos2)
axA2.set_xticklabels([TERTILE_LABELS[t] for t in [0, 1, 2]], fontsize=7)
axA2.set_ylabel("Dominance fraction")
axA2.set_title("(c) Stratified by N_eff tertile", fontsize=8)
axA2.legend(fontsize=6, frameon=False)
axA2.set_ylim(0, max(0.5, max(obs_t + nA_t) * 1.3 + 0.05))
sns.despine(ax=axA2)

figA.tight_layout()
save_pdf(figA, "Fig_NullA_permutation.pdf")


# ===========================================================================
# FIGURE: Null B
# ===========================================================================
print("\nPlotting Fig_NullB_bootstrap...")
figB, axesB = plt.subplots(1, 3, figsize=(9.5, 2.8))

# (i) per-medium Obs vs Null B (two variants)
axB0 = axesB[0]
x_pos = np.arange(len(meds))
width = 0.25
obs_vals = [(events_df[events_df["Medium"] == m]["obs_class"] == 0).mean() for m in meds]
wm_vals = [events_df[events_df["Medium"] == m]["nullB_wm_dom_rate"].mean() for m in meds]
any_vals = [events_df[events_df["Medium"] == m]["nullB_any_dom_rate"].mean() for m in meds]
colors_bar = [get_medium_color(m) for m in meds]
axB0.bar(x_pos - width, obs_vals, width, color=colors_bar,
         edgecolor="k", linewidth=0.4, label="Observed")
axB0.bar(x_pos, wm_vals, width, color=colors_bar, alpha=0.55,
         edgecolor="k", linewidth=0.4, hatch="//", label="Null B (within-medium)")
axB0.bar(x_pos + width, any_vals, width, color=colors_bar, alpha=0.3,
         edgecolor="k", linewidth=0.4, label="Null B (any-medium)")
axB0.set_xticks(x_pos)
axB0.set_xticklabels([MEDIUM_LABELS_SHORT[m] for m in meds], fontsize=7)
axB0.set_ylabel("Dominance fraction")
axB0.set_title("(a) Per-medium: Obs vs Null B variants", fontsize=8)
axB0.legend(fontsize=5, frameon=False, loc="upper right")
sns.despine(ax=axB0)

# (ii) Dominance rate vs N_eff quartile bin
axB1 = axesB[1]
bins = sorted(events_df["Neff_quartile"].unique())
obs_q = [(events_df[events_df["Neff_quartile"] == b]["obs_class"] == 0).mean() for b in bins]
wm_q = [events_df[events_df["Neff_quartile"] == b]["nullB_wm_dom_rate"].mean() for b in bins]
any_q = [events_df[events_df["Neff_quartile"] == b]["nullB_any_dom_rate"].mean() for b in bins]
axB1.plot(bins, obs_q, "o-", color="k", lw=1.2, label="Observed", markersize=5)
axB1.plot(bins, wm_q, "s--", color="#1976D2", lw=1.0, label="Null B (within-medium)", markersize=5)
axB1.plot(bins, any_q, "^--", color="#D32F2F", lw=1.0, label="Null B (any-medium)", markersize=5)
axB1.set_xlabel("N_eff quartile bin (of n_C)")
axB1.set_ylabel("Dominance fraction")
axB1.set_title("(b) Dominance scaling with N_eff bin", fontsize=8)
axB1.legend(fontsize=6, frameon=False)
axB1.set_xticks(bins)
sns.despine(ax=axB1)

# (iii) per-event scatter: obs class vs null B within-medium rate, by tertile
axB2 = axesB[2]
for t in [0, 1, 2]:
    sub = events_df[events_df["Neff_tertile"] == t]
    vals = sub["nullB_wm_dom_rate"].dropna()
    jitter = RNG.normal(0, 0.06, size=len(vals))
    axB2.scatter(np.full(len(vals), t) + jitter, vals,
                 s=8, alpha=0.5, edgecolors="none",
                 color=["#A7216A", "#802000", "#E24912"][t],
                 label=TERTILE_LABELS[t])
axB2.set_xticks([0, 1, 2])
axB2.set_xticklabels([TERTILE_LABELS[t] for t in [0, 1, 2]], fontsize=7)
axB2.set_ylabel("Null B (within) Dominance rate")
axB2.set_ylim(-0.05, 1.05)
axB2.set_title("(c) Per-event Null B rate by N_eff tertile", fontsize=8)
sns.despine(ax=axB2)

figB.tight_layout()
save_pdf(figB, "Fig_NullB_bootstrap.pdf")


# ===========================================================================
# FIGURE: Null C
# ===========================================================================
print("\nPlotting Fig_NullC_mixing_sweep...")
figC, axesC = plt.subplots(2, 2, figsize=(8.5, 5.5))

# (i-pooled) classification fraction vs alpha
axC0 = axesC[0, 0]
frac_D = np.mean(nullC_cls == 0, axis=0)
frac_M = np.mean(nullC_cls == 1, axis=0)
frac_R = np.mean(nullC_cls == 2, axis=0)
axC0.plot(ALPHAS, frac_D, "-o", color=CLASS_COLORS[0], lw=1.4, markersize=4, label="Dominance")
axC0.plot(ALPHAS, frac_M, "-o", color=CLASS_COLORS[1], lw=1.4, markersize=4, label="Mixing")
axC0.plot(ALPHAS, frac_R, "-o", color=CLASS_COLORS[2], lw=1.4, markersize=4, label="Restructuring")
axC0.axvline(0.5, color="gray", ls="--", lw=0.5)
axC0.set_xlabel(r"$\alpha$  ($\alpha\,n_A + (1-\alpha)\,n_B$)")
axC0.set_ylabel("Classification fraction")
axC0.set_ylim(-0.03, 1.03)
axC0.set_title("(a) Pooled classification vs $\\alpha$", fontsize=8)
axC0.legend(fontsize=6, frameon=False)
sns.despine(ax=axC0)

# (i-per-medium) Dominance vs alpha by medium
axC1 = axesC[0, 1]
for m in meds:
    idx = events_df["Medium"] == m
    sub_cls = nullC_cls[idx.values, :]
    dom_frac = np.mean(sub_cls == 0, axis=0)
    axC1.plot(ALPHAS, dom_frac, "-o", color=get_medium_color(m), lw=1.4, markersize=4,
              label=MEDIUM_LABELS_SHORT[m])
axC1.axvline(0.5, color="gray", ls="--", lw=0.5)
axC1.set_xlabel(r"$\alpha$")
axC1.set_ylabel("Dominance fraction")
axC1.set_title("(b) Dominance vs $\\alpha$ per medium", fontsize=8)
axC1.legend(fontsize=6, frameon=False)
sns.despine(ax=axC1)

# (ii) distribution of per-event count of alphas classified as Dominance
axC2 = axesC[1, 0]
count_dom = (nullC_cls == 0).sum(axis=1)
max_c = int(count_dom.max()) if len(count_dom) else 11
bins_ = np.arange(max_c + 2) - 0.5
axC2.hist(count_dom, bins=bins_, color="#888888", edgecolor="k", linewidth=0.3)
axC2.set_xlabel(r"# of $\alpha$ values classified as Dominance (out of 11)")
axC2.set_ylabel("Event count")
axC2.set_title("(c) Per-event Dominance-positive $\\alpha$ count", fontsize=8)
sns.despine(ax=axC2)

# Stacked bar: per-medium, per alpha, stacked fractions (optional: just for medium='M')
axC3 = axesC[1, 1]
idx = events_df["Medium"] == "M"
sub_cls = nullC_cls[idx.values, :]
fD = np.mean(sub_cls == 0, axis=0)
fM = np.mean(sub_cls == 1, axis=0)
fR = np.mean(sub_cls == 2, axis=0)
axC3.fill_between(ALPHAS, 0, fD, color=CLASS_COLORS[0], alpha=0.85, label="Dominance", step="mid")
axC3.fill_between(ALPHAS, fD, fD + fM, color=CLASS_COLORS[1], alpha=0.85, label="Mixing", step="mid")
axC3.fill_between(ALPHAS, fD + fM, fD + fM + fR, color=CLASS_COLORS[2], alpha=0.85,
                  label="Restructuring", step="mid")
axC3.set_xlabel(r"$\alpha$")
axC3.set_ylabel("Fraction")
axC3.set_ylim(0, 1)
axC3.set_title("(d) Stacked classification (MN medium)", fontsize=8)
axC3.legend(fontsize=6, frameon=False, loc="upper right")
sns.despine(ax=axC3)

figC.tight_layout()
save_pdf(figC, "Fig_NullC_mixing_sweep.pdf")


# ===========================================================================
# FIGURE: All-nulls summary
# ===========================================================================
print("\nPlotting Fig_R3_1_all_nulls_summary...")
figS, axS = plt.subplots(figsize=(8.0, 3.8))
null_labels = ["Observed", "Additive\n(alpha=0.5)", "Null A", "Null B\n(within)",
               "Null B\n(any)", "Null C@0.5", "Null C any-alpha"]

# Additive null is always ~0 Dominance (mathematically). Compute pooled just to confirm:
add_null_per_med = {}
for m in meds:
    sub = events_df[events_df["Medium"] == m]
    cnt = 0
    tot = 0
    for _, ev in sub.iterrows():
        mix = 0.5 * ev["n_A"] + 0.5 * ev["n_B"]
        s = mix.sum()
        if s <= 0:
            continue
        mix = mix / s
        cls = classify_vector(mix, ev["n_A"], ev["n_B"])
        if cls is None:
            continue
        tot += 1
        if cls == 0:
            cnt += 1
    add_null_per_med[m] = (cnt / tot) if tot else np.nan

x_pos = np.arange(len(null_labels))
width = 0.25
for mi, m in enumerate(meds):
    sub = events_df[events_df["Medium"] == m]
    vals = [
        (sub["obs_class"] == 0).mean(),
        add_null_per_med[m],
        sub["nullA_dom_rate"].mean(),
        sub["nullB_wm_dom_rate"].mean(),
        sub["nullB_any_dom_rate"].mean(),
        (sub["nullC_class_at_0.5"] == 0).mean(),
        (sub["nullC_any_alpha_dom"] == 1).mean(),
    ]
    axS.bar(x_pos + (mi - 1) * width, vals, width, color=get_medium_color(m),
            edgecolor="k", linewidth=0.4, label=MEDIUM_LABELS_SHORT[m])
    for xi, v in enumerate(vals):
        if np.isfinite(v):
            axS.text(xi + (mi - 1) * width, v + 0.008, f"{v:.2f}",
                     ha="center", va="bottom", fontsize=5)
axS.set_xticks(x_pos)
axS.set_xticklabels(null_labels, fontsize=7)
axS.set_ylabel("Dominance fraction")
axS.set_title("Dominance rates: Observed vs all nulls, per medium", fontsize=9)
axS.legend(fontsize=7, frameon=False, loc="upper right")
sns.despine(ax=axS)
axS.set_ylim(0, 1.05)

figS.tight_layout()
save_pdf(figS, "Fig_R3_1_all_nulls_summary.pdf")


# ---------------------------------------------------------------------------
# Dump summary CSVs for the memo
# ---------------------------------------------------------------------------
summary_df.to_csv(os.path.join(SAVE_DIR, "summary_per_medium.csv"), index=False)
tertile_df.to_csv(os.path.join(SAVE_DIR, "summary_per_tertile.csv"), index=False)
events_df.drop(columns=["n_A", "n_B", "n_C"]).to_csv(
    os.path.join(SAVE_DIR, "per_event_results.csv"), index=False)
print("\nWrote summary_per_medium.csv, summary_per_tertile.csv, per_event_results.csv")

# Additive-null per medium (for memo)
print("\nAdditive null (alpha=0.5) per medium Dominance rate:")
for m in meds:
    print(f"  {MEDIUM_MAP[m]}: {add_null_per_med[m]:.3f}")

print("\nDone.")
