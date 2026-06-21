#!/usr/bin/env python3
"""
R2-3: Continuous Similarity Measures Alongside Categories
=========================================================
Reviewer R2, Point #3 — Show continuous distributions, not just categories.

The Dominance/Mixture/Restructuring categories depend on thresholds.
Present the underlying continuous metrics so readers can judge robustness.

Metrics (from vector decomposition):
  - x = sqrt(u^2 + v^2) : retention magnitude (parental similarity)
  - y = asymmetricity    : how much one parental community dominates
  - PDI = (2/pi) arctan(u/v) : manuscript parental dominance index
  - Category boundaries: x^2 > 0.5 & y > 0.5 = Dominance
                          x^2 > 0.5 & y < 0.5 = Mixture
                          x^2 < 0.5            = Restructuring

Output figures:
  - Panel A: 2D scatter of (x^2, y) with threshold lines and category colors
  - Panel B: PDI, asymmetry, and retention distributions by medium
  - Panel C: Boundary sensitivity across PDI and retention boundaries
  - Panel D: 2D scatter faceted by medium
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from scipy import stats

# ── Setup paths ────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
CODE_DIR = os.path.join(PROJECT_ROOT, 'Figure_generate', 'code')
sys.path.insert(0, CODE_DIR)

from COLORMAP import (get_medium_color, get_medium_colors, MEDIUM_COLORS,
                       get_phase_diagram_color, get_phase_diagram_colors,
                       PHASE_DIAGRAM_COLORS)
from common_setup import (metric_VectorDecomposition_onlyPositive,
                           calculate_assymetricity, characterize_case,
                           exception_list)

# ── Matplotlib style ──────────────────────────────────────────────────────
sns.set_style("ticks")
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.4
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.4
mpl.rcParams['ytick.major.width'] = 0.5
plt.rcParams['text.usetex'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

mm = 0.1 / 2.54

# ── Reproducibility ──────────────────────────────────────────────────────
np.random.seed(42)

# ── Load data ──────────────────────────────────────────────────────────────
ASV_PATH = os.path.join(PROJECT_ROOT, 'Postprocessed', 'processed_Sequences_synthetic.xlsx')
COALESCENCE_PATH = os.path.join(PROJECT_ROOT, 'Analyzed', 'processed_CoalescenceEvent_synthetic.xlsx')

print("Loading data...")
asv_data = pd.read_excel(ASV_PATH)
coalescence_data = pd.read_excel(COALESCENCE_PATH)

medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
medium_order = ['L', 'M', 'H']

# ── Helper: get abundance vector ──────────────────────────────────────────
# NOTE: This intentionally reimplements getAbundance from common_setup rather
# than using the imported version, because it applies a local threshold filter
# (zeroing values below threshold) which the imported getAbundance does not do.
def get_abundance(sample_idx, threshold=0.001):
    """Get normalized abundance vector for a sample, with threshold applied."""
    row = asv_data[asv_data['SampleIDX'] == sample_idx]
    if len(row) == 0:
        return None
    abundances = np.array(row.iloc[0, 1:], dtype=float)
    abundances = abundances * (abundances > threshold)
    return abundances


def _run_vd_for_threshold(threshold, compute_bc=False):
    """
    Compute VD-derived metrics for all coalescence events at a given threshold.

    Parameters
    ----------
    threshold : float
        ASV abundance threshold (values below are zeroed).
    compute_bc : bool
        If True, also compute Bray-Curtis similarity to each parental community.

    Returns
    -------
    pd.DataFrame with columns: SampleIDX, Medium, u, v, k,
        x_magnitude, y_asymmetricity, x_squared, category,
        and optionally BC_to_parent1, BC_to_parent2.
    """
    recs = []
    for _, row in coalescence_data.iterrows():
        sid = row['SampleIDX']
        if sid in exception_list:
            continue

        sub1_id = row['SampleIDX_Sub1']
        sub2_id = row['SampleIDX_Sub2']

        n_A = get_abundance(sub1_id, threshold)
        n_B = get_abundance(sub2_id, threshold)
        n_C = get_abundance(sid, threshold)

        if n_A is None or n_B is None or n_C is None:
            continue
        if np.linalg.norm(n_A) == 0 or np.linalg.norm(n_B) == 0 or np.linalg.norm(n_C) == 0:
            continue

        try:
            u, v, k = metric_VectorDecomposition_onlyPositive(n_A, n_B, n_C)
        except (np.linalg.LinAlgError, FloatingPointError, ZeroDivisionError):
            continue

        if np.any(np.isnan([u, v, k])) or np.any(np.isinf([u, v, k])):
            continue

        x_mag, y_asym = calculate_assymetricity(u, v, k)
        category = characterize_case(x_mag, y_asym)
        if category is None:
            continue

        if v > 0:
            pdi = (2 / np.pi) * np.arctan(u / v)
        elif u > 0:
            pdi = 1.0
        else:
            pdi = np.nan

        rec = {
            'SampleIDX': sid,
            'Medium': row['Medium'],
            'u': u, 'v': v, 'k': k,
            'x_magnitude': x_mag,
            'y_asymmetricity': y_asym,
            'x_squared': x_mag ** 2,
            'pdi': pdi,
            'category': category,
        }
        if compute_bc:
            n_A_norm = n_A / (np.sum(n_A) + 1e-12)
            n_B_norm = n_B / (np.sum(n_B) + 1e-12)
            n_C_norm = n_C / (np.sum(n_C) + 1e-12)
            rec['BC_to_parent1'] = 1 - 0.5 * np.sum(np.abs(n_C_norm - n_A_norm))
            rec['BC_to_parent2'] = 1 - 0.5 * np.sum(np.abs(n_C_norm - n_B_norm))
        recs.append(rec)
    return pd.DataFrame(recs)


# ── Compute continuous metrics for all coalescence events ─────────────────
THRESHOLD = 0.001  # abundance threshold for ASVs
print(f"Computing vector decomposition metrics (threshold={THRESHOLD})...")

records = _run_vd_for_threshold(THRESHOLD, compute_bc=True).to_dict('records')

df = pd.DataFrame(records)
df['category_name'] = df['category'].map({0: 'Dominance', 1: 'Mixture', 2: 'Restructuring'})
df['Medium_label'] = df['Medium'].map(medium_labels)

# Manuscript PDI = (2/pi) arctan(u/v) in [0,1], with the v=0, u>0
# boundary defined as PDI = 1.
# y_asymmetricity folds this around 0.5, so it cannot show bimodality.
df['pdi_for_reflection'] = df['pdi']

print(f"Total valid events: {len(df)}")
print(f"By medium: {df['Medium'].value_counts().to_dict()}")
print(f"By category: {df['category_name'].value_counts().to_dict()}")


def sarle_bimodality_coefficient(x):
    """Sarle's BC = (g1^2 + 1) / (g2 + 3*(n-1)^2/((n-2)(n-3))).
    BC > ~0.555 suggests bimodality (rough threshold)."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 4:
        return np.nan
    g1 = stats.skew(x, bias=False)
    g2 = stats.kurtosis(x, bias=False)  # excess kurtosis
    correction = 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))
    return (g1 ** 2 + 1) / (g2 + correction)


# Reflection-symmetric PDI values (event + its reflection) for modality test
pdi_by_medium_reflected = {}
bc_by_medium = {}
for m in medium_order:
    vals = df[df['Medium'] == m]['pdi_for_reflection'].dropna().values
    # reflected = 1 - PDI; combine for symmetric distribution
    vals_sym = np.concatenate([vals, 1.0 - vals])
    pdi_by_medium_reflected[m] = vals_sym
    bc_by_medium[m] = sarle_bimodality_coefficient(vals_sym)

print("\nSarle's bimodality coefficient (PDI, reflection-symmetrized):")
for m in medium_order:
    bc = bc_by_medium[m]
    flag = 'bimodal' if bc > 0.555 else 'unimodal'
    print(f"  {medium_labels[m]}: BC = {bc:.3f}  ({flag}; threshold 0.555)")

# ── Color definitions ─────────────────────────────────────────────────────
cat_colors = get_phase_diagram_colors()  # [dominance, mixing, restructuring]
cat_names = ['Dominance', 'Mixture', 'Restructuring']

# ── Statistical tests ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STATISTICAL TESTS")
print("=" * 60)

for metric_name, metric_col in [('asymmetry y', 'y_asymmetricity'),
                                  ('x^2 (retention)', 'x_squared')]:
    groups = [df[df['Medium'] == m][metric_col].dropna() for m in medium_order]
    kw_stat, kw_p = stats.kruskal(*groups)
    print(f"\n{metric_name}:")
    print(f"  Kruskal-Wallis H = {kw_stat:.4f}, p = {kw_p:.4e}")
    for m, g in zip(medium_order, groups):
        print(f"  {medium_labels[m]}: n={len(g)}, "
              f"median={g.median():.3f}, mean={g.mean():.3f} +/- {g.std():.3f}")

# ── Figure A: 2D scatter of (x^2, y) with category colors ────────────────
print("\nGenerating Figure A: 2D scatter with category regions...")

fig, ax = plt.subplots(figsize=(65 * mm, 60 * mm))

# Draw category regions as background
# Restructuring: x^2 < 0.5
ax.axvspan(0, 0.5, alpha=0.08, color=cat_colors[2], zorder=0)
# Mixture: x^2 > 0.5 and y < 0.5
ax.fill_between([0.5, 1.05], 0, 0.5, alpha=0.08, color=cat_colors[1], zorder=0)
# Dominance: x^2 > 0.5 and y > 0.5
ax.fill_between([0.5, 1.05], 0.5, 1.05, alpha=0.08, color=cat_colors[0], zorder=0)

# Threshold lines
ax.axvline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
ax.axhline(0.5, xmin=0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)

# Scatter points colored by category
for cat_i, cat_name in enumerate(cat_names):
    sub = df[df['category_name'] == cat_name]
    ax.scatter(sub['x_squared'], sub['y_asymmetricity'],
               s=12, color=cat_colors[cat_i], alpha=0.6,
               edgecolors='white', linewidths=0.3,
               label=f'{cat_name} (n={len(sub)})', zorder=3)

ax.set_xlabel(r'Retention ($x^2$)', fontsize=8)
ax.set_ylabel('Asymmetricity (y)', fontsize=8)
ax.set_xlim(-0.02, 1.05)
ax.set_ylim(-0.02, 1.05)
ax.legend(fontsize=6, frameon=False, loc='lower right')

# Category labels
ax.text(0.25, 0.9, 'Restructuring', ha='center', va='center',
        fontsize=6, color=cat_colors[2], alpha=0.7, transform=ax.transAxes)
ax.text(0.75, 0.15, 'Mixture', ha='center', va='center',
        fontsize=6, color=cat_colors[1], alpha=0.7, transform=ax.transAxes)
ax.text(0.75, 0.85, 'Dominance', ha='center', va='center',
        fontsize=6, color=cat_colors[0], alpha=0.7, transform=ax.transAxes)

sns.despine(ax=ax)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'scatter_retention_vs_PDI.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)

# ── Figure B: continuous distributions by medium ───────────────────────────
print("\nGenerating Figure B: Marginal distributions by medium...")

fig, axes = plt.subplots(3, 3, figsize=(175 * mm, 120 * mm), sharex='col')
column_titles = ['PDI distribution', 'Asymmetry magnitude', 'Parental retention']

for row_idx, m in enumerate(medium_order):
    color = get_medium_color(m)
    medium_df = df[df['Medium'] == m]

    # Column 1: PDI. Include reflected values because parent labels A/B are
    # arbitrary and the category definition is symmetric.
    ax = axes[row_idx, 0]
    sub = pdi_by_medium_reflected[m]
    ax.hist(sub, bins=21, alpha=0.35, color=color, density=True, edgecolor='none')
    if len(sub) > 3:
        kde_x = np.linspace(0, 1, 200)
        kde = stats.gaussian_kde(sub, bw_method=0.18)
        ax.plot(kde_x, kde(kde_x), color=color, linewidth=1.2)
    for xpos in [0.25, 0.5, 0.75]:
        ax.axvline(xpos, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
    ax.set_ylabel('Density', fontsize=8)
    ax.text(0.03, 0.93, f'{medium_labels[m]} (n={len(medium_df)})',
            transform=ax.transAxes, fontsize=7, va='top', ha='left',
            color=color, fontweight='bold')

    # Column 2: y (asymmetricity)
    ax = axes[row_idx, 1]
    sub = medium_df['y_asymmetricity'].dropna()
    ax.hist(sub, bins=15, alpha=0.35, color=color, density=True, edgecolor='none')
    if len(sub) > 3:
        kde_x = np.linspace(0, 1, 200)
        kde = stats.gaussian_kde(sub, bw_method=0.25)
        ax.plot(kde_x, kde(kde_x), color=color, linewidth=1.2)
    ax.axvline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)

    # Column 3: x^2 (retention)
    ax = axes[row_idx, 2]
    sub = medium_df['x_squared'].dropna()
    ax.hist(sub, bins=15, alpha=0.35, color=color, density=True, edgecolor='none')
    if len(sub) > 3:
        kde_x = np.linspace(0, 1, 200)
        kde = stats.gaussian_kde(sub, bw_method=0.25)
        ax.plot(kde_x, kde(kde_x), color=color, linewidth=1.2)
    ax.axvline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)

for col_idx, title in enumerate(column_titles):
    axes[0, col_idx].set_title(title, fontsize=7, fontweight='bold')
for ax in axes[:, 0]:
    ax.set_xlim(-0.02, 1.02)
for ax in axes[:, 1]:
    ax.set_xlim(-0.02, 1.02)
for ax in axes[:, 2]:
    ax.set_xlim(-0.02, 1.02)
axes[-1, 0].set_xlabel(r'PDI $(2/\pi)\arctan(u/v)$', fontsize=8)
axes[-1, 1].set_xlabel('Asymmetricity $y$', fontsize=8)
axes[-1, 2].set_xlabel(r'Retention ($x^2$)', fontsize=8)

sns.despine(fig=fig)
plt.tight_layout(h_pad=1.0, w_pad=1.5)

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'marginal_distributions_by_medium.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)

# ── Figure B0: continuous distributions for Base medium only ──────────────
print("\nGenerating Figure B0: Base-only marginal distributions...")

base_key = 'M'
base_df = df[df['Medium'] == base_key]
base_color = get_medium_color(base_key)

fig, axes = plt.subplots(1, 3, figsize=(150 * mm, 45 * mm))

# Panel B0.1: PDI in Base medium. Include reflected values because parent
# labels A/B are arbitrary and the category definition is symmetric.
ax = axes[0]
base_pdi = pdi_by_medium_reflected[base_key]
ax.hist(base_pdi, bins=21, alpha=0.35, color=base_color,
        density=True, edgecolor='none')
if len(base_pdi) > 3:
    kde_x = np.linspace(0, 1, 200)
    kde = stats.gaussian_kde(base_pdi, bw_method=0.18)
    ax.plot(kde_x, kde(kde_x), color=base_color, linewidth=1.2)
for xpos in [0.25, 0.5, 0.75]:
    ax.axvline(xpos, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
ax.set_xlabel(r'PDI $(2/\pi)\arctan(u/v)$', fontsize=8)
ax.set_ylabel('Density', fontsize=8)
ax.set_xlim(-0.02, 1.02)
ax.set_title(f'Base PDI (n={len(base_df)})', fontsize=7, fontweight='bold')

# Panel B0.2: y (asymmetricity) in Base medium
ax = axes[1]
sub = base_df['y_asymmetricity'].dropna()
ax.hist(sub, bins=15, alpha=0.35, color=base_color,
        density=True, edgecolor='none')
if len(sub) > 3:
    kde_x = np.linspace(0, 1, 200)
    kde = stats.gaussian_kde(sub, bw_method=0.25)
    ax.plot(kde_x, kde(kde_x), color=base_color, linewidth=1.2)
ax.axvline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
ax.set_xlabel('Asymmetricity $y$', fontsize=8)
ax.set_ylabel('Density', fontsize=8)
ax.set_xlim(-0.02, 1.02)
ax.set_title('Base asymmetry magnitude', fontsize=7, fontweight='bold')

# Panel B0.3: x^2 (retention) in Base medium
ax = axes[2]
sub = base_df['x_squared'].dropna()
ax.hist(sub, bins=15, alpha=0.35, color=base_color,
        density=True, edgecolor='none')
if len(sub) > 3:
    kde_x = np.linspace(0, 1, 200)
    kde = stats.gaussian_kde(sub, bw_method=0.25)
    ax.plot(kde_x, kde(kde_x), color=base_color, linewidth=1.2)
ax.axvline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
ax.set_xlabel(r'Retention ($x^2$)', fontsize=8)
ax.set_ylabel('Density', fontsize=8)
ax.set_xlim(-0.02, 1.02)
ax.set_title('Base parental retention', fontsize=7, fontweight='bold')

sns.despine(fig=fig)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'marginal_distributions_base_only.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)


def plot_single_medium_marginals(medium_key, output_prefix):
    """Save one-row PDI, asymmetry, and retention marginals for one medium."""
    medium_df = df[df['Medium'] == medium_key]
    color = get_medium_color(medium_key)
    label = medium_labels[medium_key]

    fig, axes = plt.subplots(1, 3, figsize=(150 * mm, 45 * mm))

    ax = axes[0]
    sub = pdi_by_medium_reflected[medium_key]
    ax.hist(sub, bins=21, alpha=0.35, color=color,
            density=True, edgecolor='none')
    if len(sub) > 3:
        kde_x = np.linspace(0, 1, 200)
        kde = stats.gaussian_kde(sub, bw_method=0.18)
        ax.plot(kde_x, kde(kde_x), color=color, linewidth=1.2)
    for xpos in [0.25, 0.5, 0.75]:
        ax.axvline(xpos, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
    ax.set_xlabel(r'PDI $(2/\pi)\arctan(u/v)$', fontsize=8)
    ax.set_ylabel('Density', fontsize=8)
    ax.set_xlim(-0.02, 1.02)
    ax.set_title(f'{label} PDI (n={len(medium_df)})', fontsize=7, fontweight='bold')

    ax = axes[1]
    sub = medium_df['y_asymmetricity'].dropna()
    ax.hist(sub, bins=15, alpha=0.35, color=color,
            density=True, edgecolor='none')
    if len(sub) > 3:
        kde_x = np.linspace(0, 1, 200)
        kde = stats.gaussian_kde(sub, bw_method=0.25)
        ax.plot(kde_x, kde(kde_x), color=color, linewidth=1.2)
    ax.axvline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
    ax.set_xlabel('Asymmetricity $y$', fontsize=8)
    ax.set_ylabel('Density', fontsize=8)
    ax.set_xlim(-0.02, 1.02)
    ax.set_title(f'{label} asymmetry magnitude', fontsize=7, fontweight='bold')

    ax = axes[2]
    sub = medium_df['x_squared'].dropna()
    ax.hist(sub, bins=15, alpha=0.35, color=color,
            density=True, edgecolor='none')
    if len(sub) > 3:
        kde_x = np.linspace(0, 1, 200)
        kde = stats.gaussian_kde(sub, bw_method=0.25)
        ax.plot(kde_x, kde(kde_x), color=color, linewidth=1.2)
    ax.axvline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
    ax.set_xlabel(r'Retention ($x^2$)', fontsize=8)
    ax.set_ylabel('Density', fontsize=8)
    ax.set_xlim(-0.02, 1.02)
    ax.set_title(f'{label} parental retention', fontsize=7, fontweight='bold')

    sns.despine(fig=fig)
    plt.tight_layout()

    for ext in ['svg', 'pdf', 'png']:
        outpath = os.path.join(SCRIPT_DIR, f'{output_prefix}.{ext}')
        fig.savefig(outpath, bbox_inches='tight', dpi=300)
        print(f"  Saved: {outpath}")
    plt.close(fig)


print("\nGenerating Figure B1/B2: Nutrient-specific marginal distributions...")
plot_single_medium_marginals('L', 'marginal_distributions_nutr_minus_only')
plot_single_medium_marginals('H', 'marginal_distributions_nutr_plus_only')

# ── Figure C: boundary sensitivity across classification thresholds ───────
print("\nGenerating Figure C: Boundary sensitivity analysis...")

BASELINE_PDI_IMBALANCE = 0.25
BASELINE_RETENTION = 0.5

df['pdi_imbalance'] = np.abs(df['pdi'] - 0.5)
pdi_thresholds = np.linspace(0.05, 0.45, 17)
retention_thresholds = np.linspace(0.20, 0.80, 17)


def dominance_fraction(sub, pdi_min=BASELINE_PDI_IMBALANCE,
                       retention_min=BASELINE_RETENTION):
    calls = (sub['x_squared'] > retention_min) & (sub['pdi_imbalance'] >= pdi_min)
    return 100 * calls.mean()


pdi_sweep = {
    m: [dominance_fraction(df[df['Medium'] == m], pdi_min=t)
        for t in pdi_thresholds]
    for m in medium_order
}
retention_sweep = {
    m: [dominance_fraction(df[df['Medium'] == m], retention_min=t)
        for t in retention_thresholds]
    for m in medium_order
}

baseline_values = {
    medium_labels[m]: dominance_fraction(df[df['Medium'] == m])
    for m in medium_order
}
print("  Baseline dominance fractions (|PDI-0.5| >= 0.25, x^2 > 0.5):")
for label, value in baseline_values.items():
    print(f"    {label}: {value:.1f}%")

fig, axes = plt.subplots(1, 2, figsize=(115 * mm, 45 * mm), sharey=True)

ax = axes[0]
for m in medium_order:
    ax.plot(pdi_thresholds, pdi_sweep[m], marker='o', markersize=2.8,
            linewidth=1.2, color=get_medium_color(m), label=medium_labels[m])
ax.axvline(BASELINE_PDI_IMBALANCE, color='gray', linewidth=0.8,
           linestyle='--', alpha=0.8)
ax.set_xlabel(r'Distance from equal contribution $|PDI - 0.5|$', fontsize=7)
ax.set_ylabel('Dominance (%)', fontsize=7)
ax.set_ylim(0, 100)
ax.set_title(r'PDI boundary ($x^2 > 0.5$)', fontsize=7)
ax.legend(fontsize=6, frameon=False, loc='upper right')
ax.text(0.02, 0.98, 'A', transform=ax.transAxes, ha='left', va='top',
        fontsize=8)

ax = axes[1]
for m in medium_order:
    ax.plot(retention_thresholds, retention_sweep[m], marker='o', markersize=2.8,
            linewidth=1.2, color=get_medium_color(m), label=medium_labels[m])
ax.axvline(BASELINE_RETENTION, color='gray', linewidth=0.8,
           linestyle='--', alpha=0.8)
ax.set_xlabel(r'Minimum retention $x^2$', fontsize=7)
ax.set_ylabel('Dominance (%)', fontsize=7)
ax.set_ylim(0, 100)
ax.set_title(r'Retention boundary ($|PDI - 0.5| \geq 0.25$)', fontsize=7)
ax.text(0.02, 0.98, 'B', transform=ax.transAxes, ha='left', va='top',
        fontsize=8)

for ax in axes:
    ax.tick_params(labelsize=6)

sns.despine(fig=fig)
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.22, top=0.88,
                    wspace=0.35)

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'boundary_sensitivity_by_medium.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)

# ── Figure D: 2D scatter faceted by medium ────────────────────────────────
print("\nGenerating Figure D: 2D scatter faceted by medium...")

fig, axes = plt.subplots(1, 3, figsize=(160 * mm, 50 * mm), sharey=True, sharex=True)

for ax_i, m in enumerate(medium_order):
    ax = axes[ax_i]

    # Background regions
    ax.axvspan(0, 0.5, alpha=0.06, color=cat_colors[2], zorder=0)
    ax.fill_between([0.5, 1.05], 0, 0.5, alpha=0.06, color=cat_colors[1], zorder=0)
    ax.fill_between([0.5, 1.05], 0.5, 1.05, alpha=0.06, color=cat_colors[0], zorder=0)
    ax.axvline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.4)
    ax.axhline(0.5, xmin=0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.4)

    sub = df[df['Medium'] == m]
    for cat_i, cat_name in enumerate(cat_names):
        cat_sub = sub[sub['category_name'] == cat_name]
        ax.scatter(cat_sub['x_squared'], cat_sub['y_asymmetricity'],
                   s=14, color=cat_colors[cat_i], alpha=0.6,
                   edgecolors='white', linewidths=0.3, zorder=3)

    # Category fractions
    n_total = len(sub)
    fracs = sub['category_name'].value_counts()
    frac_text = '\n'.join([f'{c}: {fracs.get(c, 0)/n_total:.0%}'
                           for c in cat_names])
    ax.text(0.02, 0.98, frac_text, transform=ax.transAxes,
            ha='left', va='top', fontsize=5.5, color='gray')

    ax.set_xlabel(r'Retention ($x^2$)', fontsize=7)
    ax.set_title(f'{medium_labels[m]} (n={n_total})', fontsize=8, fontweight='bold')
    ax.set_xlim(-0.02, 1.05)
    ax.set_ylim(-0.02, 1.05)

axes[0].set_ylabel('Asymmetricity (y)', fontsize=7)

sns.despine(fig=fig)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'scatter_by_medium.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)

# ── Figure D: Bray-Curtis similarity to parents ──────────────────────────
print("\nGenerating Figure E: Bray-Curtis similarity to parents...")

fig, axes = plt.subplots(1, 2, figsize=(120 * mm, 55 * mm))

# Panel D1: Scatter BC to parent 1 vs parent 2
ax = axes[0]
for m in medium_order:
    sub = df[df['Medium'] == m]
    ax.scatter(sub['BC_to_parent1'], sub['BC_to_parent2'],
               s=10, color=get_medium_color(m), alpha=0.5,
               label=medium_labels[m], edgecolors='none')

ax.plot([0, 1], [0, 1], 'k--', linewidth=0.5, alpha=0.4)
ax.set_xlabel('Bray-Curtis similarity to Parent 1', fontsize=7)
ax.set_ylabel('Bray-Curtis similarity to Parent 2', fontsize=7)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.legend(fontsize=6, frameon=False)

# Panel D2: Max BC similarity distribution by medium
ax = axes[1]
df['BC_max'] = df[['BC_to_parent1', 'BC_to_parent2']].max(axis=1)
for m in medium_order:
    sub = df[df['Medium'] == m]['BC_max'].dropna()
    ax.hist(sub, bins=15, alpha=0.35, color=get_medium_color(m),
            label=medium_labels[m], density=True, edgecolor='none')
    if len(sub) > 3:
        kde_x = np.linspace(0, 1, 200)
        kde = stats.gaussian_kde(sub, bw_method=0.25)
        ax.plot(kde_x, kde(kde_x), color=get_medium_color(m), linewidth=1.2)

ax.set_xlabel('Max BC similarity to either parent', fontsize=7)
ax.set_ylabel('Density', fontsize=7)
ax.legend(fontsize=6, frameon=False)

sns.despine(fig=fig)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'bray_curtis_similarity.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)

# ── Print summary ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY TABLE")
print("=" * 60)
for m in medium_order:
    sub = df[df['Medium'] == m]
    n = len(sub)
    print(f"\n{medium_labels[m]} (n={n}):")
    for cat_name in cat_names:
        c = len(sub[sub['category_name'] == cat_name])
        print(f"  {cat_name}: {c} ({c/n:.1%})")
    print(f"  asymmetry y median={sub['y_asymmetricity'].median():.3f}, "
          f"mean={sub['y_asymmetricity'].mean():.3f}")
    print(f"  x^2 (ret)  median={sub['x_squared'].median():.3f}, "
          f"mean={sub['x_squared'].mean():.3f}")

print("\nDone!")

# ── Threshold sensitivity sweep ────────────────────────────────────────────
# Critical gap: show that Dominance fraction and continuous metric distributions
# are robust to the choice of ASV abundance threshold.
print("\n" + "=" * 60)
print("THRESHOLD SENSITIVITY SWEEP")
print("=" * 60)
print("Addressing R2's concern: are results robust to threshold choice?")

SWEEP_THRESHOLDS = [0.0001, 0.001, 0.01, 0.033]
sweep_summary = []

for thresh in SWEEP_THRESHOLDS:
    df_sw = _run_vd_for_threshold(thresh, compute_bc=False)
    if len(df_sw) == 0:
        continue

    # Overall Dominance fraction
    dom_frac_overall = (df_sw['category'] == 0).mean()

    # Per-medium Dominance fraction
    per_med = {}
    for m in medium_order:
        sub = df_sw[df_sw['Medium'] == m]
        per_med[m] = (sub['category'] == 0).mean() if len(sub) > 0 else np.nan

    sweep_summary.append({
        'threshold': thresh,
        'n_events': len(df_sw),
        'dom_frac_overall': dom_frac_overall,
        **{f'dom_frac_{m}': per_med[m] for m in medium_order},
    })
    print(f"\n  Threshold={thresh}: n={len(df_sw)}, "
          f"Dom={dom_frac_overall:.3f} | "
          + " | ".join([f"{medium_labels[m]}={per_med[m]:.3f}" for m in medium_order]))

df_sweep = pd.DataFrame(sweep_summary)

# Figure: Dominance fraction vs threshold by medium
fig_thresh, ax_thresh = plt.subplots(figsize=(80 * mm, 55 * mm))

med_colors_list = [get_medium_color(m) for m in medium_order]
for m, color in zip(medium_order, med_colors_list):
    col = f'dom_frac_{m}'
    ax_thresh.plot(range(len(df_sweep)), df_sweep[col],
                   'o-', color=color, markersize=5, linewidth=1.2,
                   label=medium_labels[m])

ax_thresh.plot(range(len(df_sweep)), df_sweep['dom_frac_overall'],
               's--', color='black', markersize=5, linewidth=1, alpha=0.5,
               label='Overall')

ax_thresh.set_xticks(range(len(df_sweep)))
ax_thresh.set_xticklabels([f'{t}' for t in df_sweep['threshold'].values], fontsize=7)
ax_thresh.set_xlabel('ASV abundance threshold', fontsize=8)
ax_thresh.set_ylabel('Dominance fraction', fontsize=8)
ax_thresh.set_ylim(0, 1)
ax_thresh.legend(fontsize=6, frameon=False)
ax_thresh.set_title('Threshold sensitivity', fontsize=8, fontweight='bold')
sns.despine(ax=ax_thresh)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'threshold_sensitivity.{ext}')
    fig_thresh.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig_thresh)

print("\nDone (R2-3 extended with threshold sensitivity)!")
