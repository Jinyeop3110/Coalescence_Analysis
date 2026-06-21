#!/usr/bin/env python3
"""
R3-2: Richness Across Media Conditions (Experimental)
======================================================
Reviewer R3, Point #2 — Does nutrient enrichment reduce species richness?

If richness decreases with nutrient enrichment, the increase in Dominance
outcomes could partly be a geometric artifact of lower dimensionality.

Analysis:
  1. Count ASV richness (# ASVs above threshold) for each community
  2. Separate parental (S) vs coalesced (C) communities
  3. Compare richness distributions across LN / MN / HN
  4. Statistical test: Kruskal-Wallis across conditions

Output figures:
  - Panel A: Richness by medium (parental vs coalesced, side by side)
  - Panel B: Richness of coalesced vs mean parental richness
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from scipy import stats
from scipy.stats import entropy as scipy_entropy
from sklearn.linear_model import LogisticRegression

# ── Setup paths ────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
CODE_DIR = os.path.join(PROJECT_ROOT, 'Figure_generate', 'code')
sys.path.insert(0, CODE_DIR)

from COLORMAP import get_medium_color, get_medium_colors, MEDIUM_COLORS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Matplotlib style (matching common_setup.py) ───────────────────────────
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

mm = 0.1 / 2.54  # mm to inches conversion factor

# ── Load data ──────────────────────────────────────────────────────────────
ASV_PATH = os.path.join(PROJECT_ROOT, 'Postprocessed', 'processed_Sequences_synthetic.xlsx')
COMMUNITIES_PATH = os.path.join(PROJECT_ROOT, 'Analyzed', 'processed_Communities_synthetic.xlsx')
COALESCENCE_PATH = os.path.join(PROJECT_ROOT, 'Analyzed', 'processed_CoalescenceEvent_synthetic.xlsx')

print("Loading data...")
asv_data = pd.read_excel(ASV_PATH)
communities_data = pd.read_excel(COMMUNITIES_PATH)
coalescence_data = pd.read_excel(COALESCENCE_PATH)

# Exception list (bad samples)
exception_list = [
    'P4-02', 'P4-03', 'P4-23', 'P4-24', 'P7-97', 'P8-12', 'P8-91',
    'P5-73', 'P5-69', 'P5-64', 'P5-61', 'P5-59', 'P5-56',
    'P5-47', 'P5-50',
    'P5-39', 'P5-87', 'P5-54', 'P6-02', 'P6-47', 'P6-74', 'P6-57'
]

# ── Helper: compute richness from ASV abundances ──────────────────────────
def compute_richness(asv_df, sample_idx, threshold=0.001):
    """Count number of ASVs above threshold for a given sample."""
    row = asv_df[asv_df['SampleIDX'] == sample_idx]
    if len(row) == 0:
        return np.nan
    abundances = np.array(row.iloc[0, 1:], dtype=float)
    return int(np.sum(abundances > threshold))


def compute_shannon(asv_df, sample_idx, threshold=0.001):
    """Compute Shannon diversity index (base e) for a given sample."""
    row = asv_df[asv_df['SampleIDX'] == sample_idx]
    if len(row) == 0:
        return np.nan
    abundances = np.array(row.iloc[0, 1:], dtype=float)
    abundances = abundances[abundances > threshold]
    if len(abundances) == 0:
        return 0.0
    p = abundances / abundances.sum()
    return float(scipy_entropy(p))  # Shannon H = -sum(p * log(p))


# ── Compute richness for all communities ──────────────────────────────────
THRESHOLDS = [0.001, 0.01, 0.033, 0.1]
THRESHOLD_MAIN = 0.001  # Main threshold for figures

medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
medium_order = ['L', 'M', 'H']

print("Computing richness and Shannon diversity for all communities...")

records = []
for _, row in communities_data.iterrows():
    sid = row['SampleIDX']
    if sid in exception_list:
        continue
    if sid not in asv_data['SampleIDX'].values:
        continue

    shannon_main = compute_shannon(asv_data, sid, threshold=THRESHOLD_MAIN)
    for thresh in THRESHOLDS:
        richness = compute_richness(asv_data, sid, threshold=thresh)
        records.append({
            'SampleIDX': sid,
            'Medium': row['Medium'],
            'CoalescenceType': row['CoalescenceType'],
            'CommunityIDX': row['CommunityIDX'],
            'Threshold': thresh,
            'Richness': richness,
            'Shannon': shannon_main if thresh == THRESHOLD_MAIN else np.nan,
        })

df = pd.DataFrame(records)
df['Type'] = df['CoalescenceType'].map({'S': 'Parental', 'C': 'Coalesced'})
df['Medium_label'] = df['Medium'].map(medium_labels)

# Build lookup caches so later loops don't re-call compute_richness/compute_shannon
# for samples that were already processed above.
_df_main = df[df['Threshold'] == THRESHOLD_MAIN]
richness_cache = _df_main.set_index('SampleIDX')['Richness'].to_dict()
shannon_cache = (_df_main[_df_main['Shannon'].notna()]
                 .set_index('SampleIDX')['Shannon'].to_dict())

print(f"Total records: {len(df)}")
print(f"By type: {df.groupby('CoalescenceType')['SampleIDX'].nunique().to_dict()}")

# ── Statistical tests ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STATISTICAL TESTS (Kruskal-Wallis)")
print("=" * 60)

stat_results = {}
for ct_label in ['Parental', 'Coalesced']:
    sub = df[(df['Type'] == ct_label) & (df['Threshold'] == THRESHOLD_MAIN)]
    groups = [sub[sub['Medium'] == m]['Richness'].dropna() for m in medium_order]

    kw_stat, kw_p = stats.kruskal(*groups)
    stat_results[ct_label] = {'H': kw_stat, 'p': kw_p}
    print(f"\n{ct_label} communities (threshold={THRESHOLD_MAIN}):")
    print(f"  Kruskal-Wallis H = {kw_stat:.4f}, p = {kw_p:.4e}")
    for m, g in zip(medium_order, groups):
        print(f"  {medium_labels[m]}: n={len(g)}, median={g.median():.1f}, "
              f"mean={g.mean():.2f} +/- {g.std():.2f}")

    # Pairwise Mann-Whitney U tests
    from itertools import combinations
    print("  Pairwise Mann-Whitney U:")
    for (m1, g1), (m2, g2) in combinations(zip(medium_order, groups), 2):
        u_stat, u_p = stats.mannwhitneyu(g1, g2, alternative='two-sided')
        print(f"    {medium_labels[m1]} vs {medium_labels[m2]}: "
              f"U = {u_stat:.1f}, p = {u_p:.4e}")

# ── Figure A: Richness by medium, parental vs coalesced ───────────────────
print("\nGenerating Figure A: Richness by medium condition...")

fig, axes = plt.subplots(1, 2, figsize=(120 * mm, 55 * mm), sharey=True)
med_colors = [get_medium_color(m) for m in medium_order]

for ax_i, (ct_label, ax) in enumerate(zip(['Parental', 'Coalesced'], axes)):
    sub = df[(df['Type'] == ct_label) & (df['Threshold'] == THRESHOLD_MAIN)]

    positions = np.arange(len(medium_order))
    bp_data = [sub[sub['Medium'] == m]['Richness'].dropna().values for m in medium_order]

    # Violin plot
    vp = ax.violinplot(bp_data, positions=positions, showmeans=False,
                       showmedians=False, showextrema=False)
    for i, body in enumerate(vp['bodies']):
        body.set_facecolor(med_colors[i])
        body.set_alpha(0.3)
        body.set_edgecolor('none')

    # Box plot overlay
    bp = ax.boxplot(bp_data, positions=positions, widths=0.25,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=1),
                    whiskerprops=dict(linewidth=0.5),
                    capprops=dict(linewidth=0.5),
                    boxprops=dict(linewidth=0.5))
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor(med_colors[i])
        patch.set_alpha(0.6)

    # Scatter individual points (jittered)
    for i, m in enumerate(medium_order):
        vals = sub[sub['Medium'] == m]['Richness'].dropna().values
        jitter = np.random.default_rng(42).uniform(-0.1, 0.1, size=len(vals))
        ax.scatter(positions[i] + jitter, vals, s=6, color=med_colors[i],
                   alpha=0.5, edgecolors='none', zorder=5)

    ax.set_xticks(positions)
    ax.set_xticklabels([medium_labels[m] for m in medium_order])
    ax.set_title(f'{ct_label}', fontsize=8, fontweight='bold')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Add p-value annotation
    kw_p = stat_results[ct_label]['p']
    p_text = f'p = {kw_p:.3f}' if kw_p > 0.001 else f'p = {kw_p:.1e}'
    ax.text(0.95, 0.95, f'KW {p_text}', transform=ax.transAxes,
            ha='right', va='top', fontsize=6, color='gray')

axes[0].set_ylabel('Species richness\n(# ASVs > 0.1%)')
fig.suptitle('', y=1.02)

sns.despine(fig=fig)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'richness_by_medium.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)

# ── Figure B: Richness across multiple thresholds ─────────────────────────
print("\nGenerating Figure B: Richness across thresholds...")

fig, axes = plt.subplots(1, len(THRESHOLDS), figsize=(180 * mm, 50 * mm), sharey=False)

for t_i, thresh in enumerate(THRESHOLDS):
    ax = axes[t_i]
    sub = df[(df['Type'] == 'Parental') & (df['Threshold'] == thresh)]

    bp_data = [sub[sub['Medium'] == m]['Richness'].dropna().values for m in medium_order]
    positions = np.arange(len(medium_order))

    bp = ax.boxplot(bp_data, positions=positions, widths=0.4,
                    patch_artist=True, showfliers=True,
                    flierprops=dict(marker='.', markersize=3, alpha=0.5),
                    medianprops=dict(color='black', linewidth=1),
                    whiskerprops=dict(linewidth=0.5),
                    capprops=dict(linewidth=0.5),
                    boxprops=dict(linewidth=0.5))
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor(med_colors[i])
        patch.set_alpha(0.6)

    ax.set_xticks(positions)
    ax.set_xticklabels([medium_labels[m] for m in medium_order], fontsize=7)
    ax.set_title(f'Threshold > {thresh}', fontsize=7)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # KW test
    groups_t = [sub[sub['Medium'] == m]['Richness'].dropna() for m in medium_order]
    if all(len(g) > 0 for g in groups_t):
        kw_stat, kw_p = stats.kruskal(*groups_t)
        p_text = f'p={kw_p:.3f}' if kw_p > 0.001 else f'p={kw_p:.1e}'
        ax.text(0.95, 0.95, p_text, transform=ax.transAxes,
                ha='right', va='top', fontsize=5.5, color='gray')

axes[0].set_ylabel('Richness (parental)')
sns.despine(fig=fig)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'richness_thresholds.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)

# ── Figure C: Coalesced richness vs mean parental richness ────────────────
print("\nGenerating Figure C: Coalesced vs mean parental richness...")

# For each coalescence event, get richness of result and both parents
coal_richness_records = []
for _, row in coalescence_data.iterrows():
    sid = row['SampleIDX']
    if sid in exception_list:
        continue
    sub1 = row['SampleIDX_Sub1']
    sub2 = row['SampleIDX_Sub2']

    r_coal = richness_cache.get(sid, np.nan)
    r_sub1 = richness_cache.get(sub1, np.nan)
    r_sub2 = richness_cache.get(sub2, np.nan)

    if np.isnan(r_coal) or np.isnan(r_sub1) or np.isnan(r_sub2):
        continue

    coal_richness_records.append({
        'SampleIDX': sid,
        'Medium': row['Medium'],
        'Richness_coal': r_coal,
        'Richness_sub1': r_sub1,
        'Richness_sub2': r_sub2,
        'Richness_mean_parents': (r_sub1 + r_sub2) / 2,
        'Richness_max_parents': max(r_sub1, r_sub2),
    })

df_coal = pd.DataFrame(coal_richness_records)
df_coal['Medium_label'] = df_coal['Medium'].map(medium_labels)

fig, axes = plt.subplots(1, 2, figsize=(120 * mm, 55 * mm))

# Panel C1: Scatter — coalesced richness vs mean parental richness
ax = axes[0]
for m in medium_order:
    sub = df_coal[df_coal['Medium'] == m]
    ax.scatter(sub['Richness_mean_parents'], sub['Richness_coal'],
               s=10, color=get_medium_color(m), alpha=0.5,
               label=medium_labels[m], edgecolors='none')

lims = [0, max(df_coal['Richness_mean_parents'].max(),
               df_coal['Richness_coal'].max()) + 1]
ax.plot(lims, lims, 'k--', linewidth=0.5, alpha=0.5, label='y=x')
ax.set_xlim(lims)
ax.set_ylim(lims)
ax.set_xlabel('Mean parental richness')
ax.set_ylabel('Coalesced richness')
ax.legend(fontsize=6, frameon=False, loc='upper left')

# Panel C2: Richness change (coal - mean parental richness) by medium
ax = axes[1]
df_coal['Richness_change'] = df_coal['Richness_coal'] - df_coal['Richness_mean_parents']
bp_data = [df_coal[df_coal['Medium'] == m]['Richness_change'].dropna().values
           for m in medium_order]
positions = np.arange(len(medium_order))

bp = ax.boxplot(bp_data, positions=positions, widths=0.4,
                patch_artist=True, showfliers=False,
                medianprops=dict(color='black', linewidth=1),
                whiskerprops=dict(linewidth=0.5),
                capprops=dict(linewidth=0.5),
                boxprops=dict(linewidth=0.5))
for i, patch in enumerate(bp['boxes']):
    patch.set_facecolor(med_colors[i])
    patch.set_alpha(0.6)

ax.axhline(0, color='gray', linewidth=0.5, linestyle='--')
ax.set_xticks(positions)
ax.set_xticklabels([medium_labels[m] for m in medium_order])
ax.set_ylabel('Richness change\n(coalesced - mean parental)')

sns.despine(fig=fig)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    outpath = os.path.join(SCRIPT_DIR, f'richness_coalesced_vs_parental.{ext}')
    fig.savefig(outpath, bbox_inches='tight', dpi=300)
    print(f"  Saved: {outpath}")
plt.close(fig)

# ── Print summary table ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY TABLE")
print("=" * 60)
for ct_label in ['Parental', 'Coalesced']:
    print(f"\n--- {ct_label} communities (threshold = {THRESHOLD_MAIN}) ---")
    sub = df[(df['Type'] == ct_label) & (df['Threshold'] == THRESHOLD_MAIN)]
    summary = sub.groupby('Medium')['Richness'].agg(['count', 'mean', 'std', 'median'])
    summary.index = summary.index.map(medium_labels)
    print(summary.to_string())

print("\n--- Coalesced richness vs parental richness ---")
for m in medium_order:
    sub = df_coal[df_coal['Medium'] == m]
    change = sub['Richness_change']
    print(f"  {medium_labels[m]}: n={len(sub)}, "
          f"mean change = {change.mean():.2f} +/- {change.std():.2f}, "
          f"median change = {change.median():.1f}")

print("\nDone!")

# ── Shannon diversity: comparison across media ────────────────────────────
print("\n" + "=" * 60)
print("SHANNON DIVERSITY (threshold = {})".format(THRESHOLD_MAIN))
print("=" * 60)

df_shannon = df[(df['Threshold'] == THRESHOLD_MAIN) & df['Shannon'].notna()].copy()

for ct_label in ['Parental', 'Coalesced']:
    sub = df_shannon[df_shannon['Type'] == ct_label]
    groups_sh = [sub[sub['Medium'] == m]['Shannon'].dropna() for m in medium_order]
    kw_stat, kw_p = stats.kruskal(*groups_sh)
    print(f"\n{ct_label} communities:")
    print(f"  Kruskal-Wallis H = {kw_stat:.4f}, p = {kw_p:.4e}")
    for m, g in zip(medium_order, groups_sh):
        print(f"  {medium_labels[m]}: n={len(g)}, median={g.median():.3f}, "
              f"mean={g.mean():.3f} +/- {g.std():.3f}")

# ── Logistic regression: Dominance ~ parental richness + medium ───────────
# Critical gap identified in CRITIQUE_SUMMARY: formally test whether richness
# explains Dominance frequency beyond the medium effect.
print("\n" + "=" * 60)
print("LOGISTIC REGRESSION: Dominance ~ mean_parental_richness + medium")
print("=" * 60)
print("(Addresses R3-2a: does richness explain Dominance beyond medium?)")

# We need coalescence outcome data — classify events using vector decomposition
try:
    from common_setup import (
        metric_VectorDecomposition_onlyPositive,
        calculate_assymetricity,
        characterize_case,
    )

    # Build per-coalescence-event richness + outcome table
    logit_records = []
    for _, row in coalescence_data.iterrows():
        sid = row['SampleIDX']
        if sid in exception_list:
            continue
        sub1 = row['SampleIDX_Sub1']
        sub2 = row['SampleIDX_Sub2']
        medium = row['Medium']

        r1 = richness_cache.get(sub1, np.nan)
        r2 = richness_cache.get(sub2, np.nan)
        sh1 = shannon_cache.get(sub1, np.nan)
        sh2 = shannon_cache.get(sub2, np.nan)
        if np.isnan(r1) or np.isnan(r2):
            continue

        # Get abundance vectors for outcome classification
        row_coal = asv_data[asv_data['SampleIDX'] == sid]
        row_s1 = asv_data[asv_data['SampleIDX'] == sub1]
        row_s2 = asv_data[asv_data['SampleIDX'] == sub2]
        if len(row_coal) == 0 or len(row_s1) == 0 or len(row_s2) == 0:
            continue

        c_mix = np.array(row_coal.iloc[0, 1:], dtype=float)
        c_1 = np.array(row_s1.iloc[0, 1:], dtype=float)
        c_2 = np.array(row_s2.iloc[0, 1:], dtype=float)
        c_1 = c_1 * (c_1 > THRESHOLD_MAIN)
        c_2 = c_2 * (c_2 > THRESHOLD_MAIN)
        c_mix = c_mix * (c_mix > THRESHOLD_MAIN)

        try:
            u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
            x_val, y_val = calculate_assymetricity(u, v, k)
            outcome = characterize_case(x_val, y_val)
        except Exception:
            continue

        if outcome is None:
            continue

        logit_records.append({
            'SampleIDX': sid,
            'Medium': medium,
            'Richness_mean_parents': (r1 + r2) / 2,
            'Richness_max_parents': max(r1, r2),
            'Shannon_mean_parents': (sh1 + sh2) / 2 if not np.isnan(sh1) and not np.isnan(sh2) else np.nan,
            'outcome': outcome,
            'is_dominance': int(outcome == 0),
        })

    df_logit = pd.DataFrame(logit_records).dropna(subset=['Richness_mean_parents'])
    print(f"\nTotal events for logistic regression: {len(df_logit)}")
    print(f"Dominance rate: {df_logit['is_dominance'].mean():.3f}")

    # Model 1: Dominance ~ medium only (baseline)
    X_med = pd.get_dummies(df_logit[['Medium']], drop_first=True).astype(float)
    y_lr = df_logit['is_dominance'].values
    lr_med = LogisticRegression(solver='lbfgs', max_iter=500)
    lr_med.fit(X_med, y_lr)
    print(f"\nModel 1 (Dominance ~ medium only): accuracy={lr_med.score(X_med, y_lr):.3f}")

    # Model 2: Dominance ~ richness only
    X_rich = df_logit[['Richness_mean_parents']].values
    lr_rich = LogisticRegression(solver='lbfgs', max_iter=500)
    lr_rich.fit(X_rich, y_lr)
    print(f"Model 2 (Dominance ~ richness only): "
          f"coef={lr_rich.coef_[0][0]:.4f}, accuracy={lr_rich.score(X_rich, y_lr):.3f}")

    # Model 3: Dominance ~ richness + medium
    X_both = pd.concat([df_logit[['Richness_mean_parents']].reset_index(drop=True),
                         pd.get_dummies(df_logit[['Medium']], drop_first=True).reset_index(drop=True)],
                        axis=1).astype(float)
    lr_both = LogisticRegression(solver='lbfgs', max_iter=500)
    lr_both.fit(X_both, y_lr)
    print(f"Model 3 (Dominance ~ richness + medium):")
    for feat, coef in zip(X_both.columns, lr_both.coef_[0]):
        print(f"  {feat}: {coef:.4f}")
    print(f"  Intercept: {lr_both.intercept_[0]:.4f}")
    print(f"  Accuracy: {lr_both.score(X_both, y_lr):.3f}")
    print(f"\nIf richness coef in Model 3 ≈ 0 → richness effect absorbed by medium.")
    print(f"If richness coef in Model 3 ≠ 0 → richness independently predicts Dominance.")

    # Model 4: Dominance ~ Shannon + medium
    df_logit_sh = df_logit.dropna(subset=['Shannon_mean_parents'])
    if len(df_logit_sh) > 10:
        y_lr_sh = df_logit_sh['is_dominance'].values
        X_shan = pd.concat([df_logit_sh[['Shannon_mean_parents']].reset_index(drop=True),
                             pd.get_dummies(df_logit_sh[['Medium']], drop_first=True).reset_index(drop=True)],
                            axis=1).astype(float)
        lr_shan = LogisticRegression(solver='lbfgs', max_iter=500)
        lr_shan.fit(X_shan, y_lr_sh)
        print(f"\nModel 4 (Dominance ~ Shannon + medium):")
        for feat, coef in zip(X_shan.columns, lr_shan.coef_[0]):
            print(f"  {feat}: {coef:.4f}")
        print(f"  Accuracy: {lr_shan.score(X_shan, y_lr_sh):.3f}")

except ImportError as e:
    print(f"\nCould not import common_setup for logistic regression: {e}")
    print("Run this script from the Figure_generate/code directory to enable logistic regression.")
except Exception as e:
    print(f"\nLogistic regression failed: {e}")

print("\nDone (R3-2a extended)!")
