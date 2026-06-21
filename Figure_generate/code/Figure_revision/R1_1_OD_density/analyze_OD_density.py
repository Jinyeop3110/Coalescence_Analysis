"""
analyze_OD_density.py  (R1-1, refactor v2)

Reviewer 1 asked whether absolute community density (OD) could explain the
Dominance outcomes and the same-parent pairwise selection correlation.

This script addresses two questions with three figures (LN / MN / HN panels each):

  Fig_R1_1A_winner_loser_OD.pdf
      Question 1a: Does absolute OD set the direction of Dominance?
      Scatter of (OD_loser, OD_winner) for Dominance events; (min, max)
      reference points for Mixture / Restructuring on the same axes.
      If denser parental communities always win, Dominance points sit above y=x.

  Fig_R1_1B_OD_vs_PDI.pdf
      Question 1b: Does signed OD difference predict PDI?
      Per-event scatter of (OD_A - OD_B) vs PDI = 2/pi * arctan(u/v).
      A flat slope says density does not set direction at the event level.
      Gray reflections (OD_B - OD_A, 1-PDI) shown for symmetry.

  Fig_R1_1C_pairwise_corr_vs_OD.pdf
      Question 2: Do high-OD events show higher within-community pairwise
      selection correlation?
      Panel C1 (binned): parental-community OD tertiles within each medium,
      within-community correlations with bootstrap 95% CIs and a cross-community
      reference.
      Panel C2 (continuous): per-event scatter of parental-community OD vs within-community
      correlation, colored by medium, with per-medium Spearman rho.

Run from Figure_generate/code/ or from the script's folder.
"""

import sys, os
from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ---------------------------------------------------------------------------
# Path setup — import project-wide helpers
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, CODE_DIR)
os.chdir(CODE_DIR)

from common_setup import (
    Coalescence_data, Communities_data,
    Processed_sequences_synthetic,
    Syn_Coal_IDX,
    exception_list,
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
    mm,
)
from COLORMAP import (
    PHASE_DIAGRAM_COLORS,
    get_medium_colors,
)
from PairwiseCorrelationAnalysis_PerEvent import (
    calculate_correlation_single_event,
    determine_species_origins_single_event,
)

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
sns.set_style("ticks")
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
plt.rcParams['text.usetex'] = False
np.random.seed(42)

COLOR_DOM  = PHASE_DIAGRAM_COLORS['dominance']
COLOR_MIX  = PHASE_DIAGRAM_COLORS['mixing']
COLOR_REST = PHASE_DIAGRAM_COLORS['restructuring']
MEDIUM_CLR = get_medium_colors()  # index 0=LN, 1=MN, 2=HN
MEDIUMS = ['LN', 'MN', 'HN']
MEDIUM_PRETTY = {'LN': r'Nutr$-$', 'MN': 'Base', 'HN': r'Nutr$+$'}
POOL_SIZES = [6, 12, 24]


def same_origin_corr_for_origin(offspring, parent1, parent2, origin, threshold=1e-4):
    """Per-event within-community fate correlation for one parental community."""
    species_origins = determine_species_origins_single_event(parent1, parent2, threshold)
    offspring_presence = (offspring > threshold).astype(int)
    species = np.where(species_origins == origin)[0]
    if len(species) < 2:
        return np.nan

    concordances = []
    for i, j in combinations(species, 2):
        concordances.append(int(offspring_presence[i] == offspring_presence[j]))
    return 2 * float(np.mean(concordances)) - 1

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------
def get_community_od(sample_idx):
    row = Communities_data[Communities_data['SampleIDX'] == sample_idx]
    if row.empty:
        return np.nan
    return float(row['fieldOD7'].values[0])


def get_abundance_vector(sample_idx):
    idx = np.where(Processed_sequences_synthetic['SampleIDX'] == sample_idx)[0]
    if len(idx) == 0:
        return None
    return np.array(Processed_sequences_synthetic.iloc[idx[0]].values[1:], dtype=float)


def calculate_pdi(u, v):
    if v > 0:
        return (2 / np.pi) * np.arctan(u / v)
    if u > 0:
        return 1.0
    return np.nan


# ---------------------------------------------------------------------------
# Build per-event record table
# ---------------------------------------------------------------------------
records = []
n_decomp_fail = 0

for medium in MEDIUMS:
    for sp in POOL_SIZES:
        for sample_idx in Syn_Coal_IDX.get(f"{medium}_{sp}", []):
            if sample_idx in exception_list:
                continue
            coal_row = Coalescence_data[Coalescence_data['SampleIDX'] == sample_idx]
            if coal_row.empty:
                continue
            sub1 = coal_row['SampleIDX_Sub1'].values[0]
            sub2 = coal_row['SampleIDX_Sub2'].values[0]

            od1 = get_community_od(sub1)
            od2 = get_community_od(sub2)
            if np.isnan(od1) or np.isnan(od2):
                continue

            c_mix = get_abundance_vector(sample_idx)
            c_1 = get_abundance_vector(sub1)
            c_2 = get_abundance_vector(sub2)
            if c_mix is None or c_1 is None or c_2 is None:
                continue
            # abundance threshold used throughout the paper
            c_1 = c_1 * (c_1 > 1e-4)
            c_2 = c_2 * (c_2 > 1e-4)
            c_mix = c_mix * (c_mix > 1e-4)

            try:
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
            except Exception:
                n_decomp_fail += 1
                continue

            x_val, y_val = calculate_assymetricity(u, v, k)
            outcome = characterize_case(x_val, y_val)
            if outcome is None:
                continue

            pdi = calculate_pdi(u, v)
            winner = 1 if u > v else 2  # only semantic for Dominance

            # same- and cross-origin correlation for this single event
            corr = calculate_correlation_single_event(c_mix, c_1, c_2, threshold=1e-4)
            same_corr = corr['same_origin_corr'] if corr is not None else np.nan
            cross_corr = corr['mixed_origin_corr'] if corr is not None else np.nan
            same_corr_sub1 = same_origin_corr_for_origin(c_mix, c_1, c_2, origin=0, threshold=1e-4)
            same_corr_sub2 = same_origin_corr_for_origin(c_mix, c_1, c_2, origin=1, threshold=1e-4)

            records.append({
                'SampleIDX': sample_idx,
                'Medium': medium,
                'PoolSize': sp,
                'OD_Sub1': od1,
                'OD_Sub2': od2,
                'meanOD': 0.5 * (od1 + od2),
                'dOD_signed': od1 - od2,
                'u': u, 'v': v, 'k': k,
                'PDI': pdi,
                'outcome': outcome,   # 0=Dom, 1=Mix, 2=Rest
                'winner': winner,
                'same_corr': same_corr,
                'same_corr_sub1': same_corr_sub1,
                'same_corr_sub2': same_corr_sub2,
                'cross_corr': cross_corr,
            })

df = pd.DataFrame(records)
df['winner_OD'] = np.where(df['winner'] == 1, df['OD_Sub1'], df['OD_Sub2'])
df['loser_OD']  = np.where(df['winner'] == 1, df['OD_Sub2'], df['OD_Sub1'])
df['winner_is_denser'] = (df['winner_OD'] > df['loser_OD']).astype(int)

print(f"Events with OD + decomposition: {len(df)}   decomposition failures: {n_decomp_fail}")
for m in MEDIUMS:
    sub = df[df['Medium'] == m]
    print(f"  {m}: n={len(sub)}  Dom={(sub['outcome']==0).sum()}  "
          f"Mix={(sub['outcome']==1).sum()}  Rest={(sub['outcome']==2).sum()}")


# ===========================================================================
# Fig R1-1A: Winner OD vs Loser OD per medium (Dominance only)
#   1x3 panels — tests "does the denser parental community win?" in Dominance events.
# ===========================================================================
fig, axes = plt.subplots(1, 3, figsize=(150*mm, 55*mm), facecolor='w',
                         sharex=True, sharey=True)

od_all = np.concatenate([df['OD_Sub1'].values, df['OD_Sub2'].values])
od_max = float(np.nanmax(od_all)) * 1.05
od_pad = od_max * 0.035

for ax, medium in zip(axes, MEDIUMS):
    sub = df[df['Medium'] == medium]
    dom = sub[sub['outcome'] == 0]

    ax.axhline(0.0, color='gray', linestyle=':', linewidth=0.5, alpha=0.55)
    ax.axvline(0.0, color='gray', linestyle=':', linewidth=0.5, alpha=0.55)
    ax.plot([0, od_max], [0, od_max], '--', color='gray', linewidth=0.5, alpha=0.6)

    if len(dom) > 0:
        ax.scatter(dom['loser_OD'], dom['winner_OD'],
                   s=20, color=COLOR_DOM, alpha=0.58,
                   edgecolors='black', linewidths=0.3, label='Dominance')
        n_denser = int(dom['winner_is_denser'].sum())
        n_total = len(dom)
        frac = n_denser / n_total
        binom_p = stats.binomtest(n_denser, n_total, 0.5).pvalue
        ax.text(0.03, 0.97,
                f'Higher-OD parental\ncommunity wins:\n{n_denser} of {n_total} events ({frac:.0%})\n'
                f'p value={binom_p:.2g}',
                transform=ax.transAxes, fontsize=6, va='top', ha='left')

    ax.set_title(MEDIUM_PRETTY[medium], fontsize=9)
    ax.set_xlim(-od_pad, od_max)
    ax.set_ylim(-od_pad, od_max)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('Loser OD$_{600}$', fontsize=7)
    sns.despine(ax=ax)
axes[0].set_ylabel('Winner OD$_{600}$', fontsize=7)

fig.tight_layout()
for ext in ['pdf', 'svg', 'png']:
    fig.savefig(os.path.join(SCRIPT_DIR, f'Fig_R1_1A_winner_loser_OD.{ext}'),
                dpi=300, bbox_inches='tight')
plt.close(fig)
print('Wrote Fig_R1_1A_winner_loser_OD')


# ===========================================================================
# Fig R1-1B: signed ΔOD vs PDI per medium
# ===========================================================================
fig, axes = plt.subplots(1, 3, figsize=(150*mm, 55*mm), facecolor='w', sharex=True, sharey=True)

dOD_abs_max = float(np.nanmax(np.abs(df['dOD_signed']))) * 1.05

for ax, medium in zip(axes, MEDIUMS):
    sub = df[df['Medium'] == medium].dropna(subset=['PDI'])

    # neutral reference lines
    ax.axhline(0.5, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.axvline(0.0, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)

    # reflected gray points for visual symmetry (consistent with Fig 1E etc.)
    ax.scatter(-sub['dOD_signed'], 1 - sub['PDI'],
               s=10, color='lightgray', alpha=0.5, edgecolors='none', zorder=1)

    for outcome_val, clr, label in [(0, COLOR_DOM, 'Dominance'),
                                     (1, COLOR_MIX, 'Mixture'),
                                     (2, COLOR_REST, 'Restructuring')]:
        grp = sub[sub['outcome'] == outcome_val]
        if len(grp) > 0:
            ax.scatter(grp['dOD_signed'], grp['PDI'],
                       s=16, color=clr, alpha=0.75,
                       edgecolors='black', linewidths=0.3,
                       label=label, zorder=2)

    if len(sub) >= 3:
        rho, pval = stats.spearmanr(sub['dOD_signed'], sub['PDI'])
        ax.text(0.03, 0.05,
                f'Spearman $\\rho$={rho:.2f}\np value={pval:.2g}',
                transform=ax.transAxes, fontsize=6, va='bottom', ha='left')

    ax.set_title(MEDIUM_PRETTY[medium], fontsize=9)
    ax.set_xlim(-dOD_abs_max, dOD_abs_max)
    ax.set_ylim(-0.05, 1.05)
    sns.despine(ax=ax)

axes[0].set_ylabel(r'PDI = $\frac{2}{\pi}\arctan(u/v)$', fontsize=7)
for ax in axes:
    ax.set_xlabel(r'OD$_A$ - OD$_B$', fontsize=7)
axes[-1].legend(loc='lower right', fontsize=6, frameon=False)

fig.tight_layout()
for ext in ['pdf', 'svg', 'png']:
    fig.savefig(os.path.join(SCRIPT_DIR, f'Fig_R1_1B_OD_vs_PDI.{ext}'),
                dpi=300, bbox_inches='tight')
plt.close(fig)
print('Wrote Fig_R1_1B_OD_vs_PDI')


# ===========================================================================
# Fig R1-1C: within-community pairwise selection correlation vs parental community OD
# ===========================================================================
def bootstrap_mean_ci(values, n_boot=2000, ci=95):
    values = np.asarray(values, dtype=float)
    values = values[~np.isnan(values)]
    if len(values) == 0:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(42)
    boot = rng.choice(values, size=(n_boot, len(values)), replace=True).mean(axis=1)
    lo = np.percentile(boot, (100 - ci) / 2)
    hi = np.percentile(boot, 100 - (100 - ci) / 2)
    return float(np.mean(values)), float(lo), float(hi)


df_corr = df.dropna(subset=['same_corr', 'cross_corr']).copy()
parent_records = []
for _, row in df.iterrows():
    if not np.isnan(row['same_corr_sub1']):
        parent_records.append({
            'SampleIDX': row['SampleIDX'],
            'Medium': row['Medium'],
            'ParentalCommunity': 'A',
            'parent_OD': row['OD_Sub1'],
            'same_parental_corr': row['same_corr_sub1'],
            'cross_corr': row['cross_corr'],
        })
    if not np.isnan(row['same_corr_sub2']):
        parent_records.append({
            'SampleIDX': row['SampleIDX'],
            'Medium': row['Medium'],
            'ParentalCommunity': 'B',
            'parent_OD': row['OD_Sub2'],
            'same_parental_corr': row['same_corr_sub2'],
            'cross_corr': row['cross_corr'],
        })
df_parent = pd.DataFrame(parent_records).dropna(subset=['same_parental_corr', 'parent_OD'])

# Assign parental-community OD tertile within each medium
tertile_labels = ['Low', 'Mid', 'High']
df_parent['parent_OD_tertile'] = np.nan
tertile_edges_by_medium = {}
tertile_range_text_by_medium = {}
for m in MEDIUMS:
    mask = df_parent['Medium'] == m
    vals = df_parent.loc[mask, 'parent_OD'].values
    edges = np.quantile(vals, [0, 1/3, 2/3, 1])
    tertile_edges_by_medium[m] = edges
    tertile_range_text_by_medium[m] = [
        f'OD$_{{600}}$ = {edges[i]:.2f}-{edges[i+1]:.2f}'
        for i in range(3)
    ]
    bin_idx = np.digitize(vals, edges[1:-1], right=False)
    df_parent.loc[mask, 'parent_OD_tertile'] = [tertile_labels[i] for i in bin_idx]

fig, axes = plt.subplots(2, 3, figsize=(170*mm, 86*mm), facecolor='w',
                         gridspec_kw={'height_ratios': [1.0, 1.0]})

tertile_pos = np.arange(len(tertile_labels))

corr_min = float(min(df_parent['same_parental_corr'].min(), df_corr['cross_corr'].min())) - 0.05
corr_max = float(max(df_parent['same_parental_corr'].max(), df_corr['cross_corr'].max())) + 0.05

for col_i, m in enumerate(MEDIUMS):
    # --- Row 1: binned within-community bars by parental OD tertile ---
    ax = axes[0][col_i]
    same_means, same_los, same_his = [], [], []
    ns = []
    for t in tertile_labels:
        cell = df_parent[(df_parent['Medium'] == m) & (df_parent['parent_OD_tertile'] == t)]
        ns.append(len(cell))
        ms, los, his = bootstrap_mean_ci(cell['same_parental_corr'].values)
        same_means.append(ms); same_los.append(los); same_his.append(his)

    ax.bar(tertile_pos, same_means, width=0.55,
           color=MEDIUM_CLR[col_i], alpha=0.85,
           edgecolor='black', linewidth=0.4, label='within-community')
    ax.errorbar(tertile_pos, same_means,
                yerr=[np.array(same_means)-np.array(same_los),
                      np.array(same_his)-np.array(same_means)],
                fmt='none', color='black', linewidth=0.6, capsize=2)

    cross_cell = df_corr[df_corr['Medium'] == m]
    cross_mean, cross_lo, cross_hi = bootstrap_mean_ci(cross_cell['cross_corr'].values)
    ax.axhspan(cross_lo, cross_hi, color='gray', alpha=0.12, linewidth=0)
    ax.axhline(cross_mean, color='gray', linewidth=1.0, linestyle='--',
               label='cross-community mean')

    ax.axhline(0, color='black', linewidth=0.3)
    ax.set_xticks(tertile_pos)
    ax.set_xticklabels(tertile_labels, fontsize=7)
    for ti, od_range in enumerate(tertile_range_text_by_medium[m]):
        ax.text(tertile_pos[ti], -0.17, od_range,
                transform=ax.get_xaxis_transform(),
                ha='center', va='top', fontsize=4.7, clip_on=False)
    ax.set_ylim(corr_min, corr_max)
    if col_i == 0:
        ax.set_ylabel('within-community\npairwise correlation', fontsize=7)
        ax.legend(loc='upper right', fontsize=6, frameon=False)
    else:
        ax.set_ylabel('')
    ax.set_title(MEDIUM_PRETTY[m], fontsize=9)
    sns.despine(ax=ax)

    # --- Row 2: per-event parental-community scatter and Spearman trend ---
    ax = axes[1][col_i]
    sub = df_parent[df_parent['Medium'] == m]

    ax.scatter(sub['parent_OD'], sub['same_parental_corr'],
               s=18, color=MEDIUM_CLR[col_i], alpha=0.8,
               edgecolors='black', linewidths=0.3)
    edges = tertile_edges_by_medium[m]
    for boundary in tertile_edges_by_medium[m][1:-1]:
        ax.axvline(boundary, color='gray', linewidth=0.6, linestyle=':', alpha=0.65)
    for label, x_left, x_right in zip(tertile_labels, edges[:-1], edges[1:]):
        ax.text((x_left + x_right) / 2, 0.04, label,
                transform=ax.get_xaxis_transform(),
                ha='center', va='bottom', fontsize=5.5,
                color='dimgray',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.72, pad=0.6))
    ax.axhspan(cross_lo, cross_hi, color='gray', alpha=0.12, linewidth=0)
    ax.axhline(cross_mean, color='gray', linewidth=1.0, linestyle='--')

    # linear fits
    x_arr = sub['parent_OD'].values
    if len(x_arr) >= 3:
        y_arr = sub['same_parental_corr'].values
        fit = np.polyfit(x_arr, y_arr, 1)
        xs = np.linspace(x_arr.min(), x_arr.max(), 50)
        ax.plot(xs, np.polyval(fit, xs), '-',
                color=MEDIUM_CLR[col_i], linewidth=0.8, alpha=0.7)

        rho_s, p_s = stats.spearmanr(sub['parent_OD'], sub['same_parental_corr'])
        ax.text(0.03, 0.97,
                f'within $\\rho$={rho_s:+.2f}\n'
                f'p value={p_s:.2g}',
                transform=ax.transAxes, fontsize=6, va='top', ha='left',
                family='monospace')

    ax.axhline(0, color='gray', linewidth=0.4, linestyle='--')
    ax.set_ylim(corr_min, corr_max)
    x_pad = (edges[-1] - edges[0]) * 0.04
    ax.set_xlim(edges[0] - x_pad, edges[-1] + x_pad)
    ax.set_xlabel(r'Parental community OD$_{600}$', fontsize=7)
    if col_i == 0:
        ax.set_ylabel('within-community\npairwise correlation', fontsize=7)
    else:
        ax.set_ylabel('')
    sns.despine(ax=ax)

fig.text(0.015, 0.73, 'OD tertiles', rotation=90, va='center', ha='left', fontsize=8)
fig.text(0.015, 0.27, 'Per-event OD', rotation=90, va='center', ha='left', fontsize=8)
fig.tight_layout(h_pad=1.7, w_pad=1.1, rect=[0.025, 0, 1, 1])
for ext in ['pdf', 'svg', 'png']:
    fig.savefig(os.path.join(SCRIPT_DIR, f'Fig_R1_1C_pairwise_corr_vs_OD.{ext}'),
                dpi=300, bbox_inches='tight')
plt.close(fig)
print('Wrote Fig_R1_1C_pairwise_corr_vs_OD')


# ===========================================================================
# Console summary
# ===========================================================================
print('\n===== R1-1 Summary Statistics =====')
print('\n[Q1a] Dominance: is the winner the denser parental community?')
for m in MEDIUMS:
    dom_m = df[(df['Medium'] == m) & (df['outcome'] == 0)]
    if len(dom_m) == 0:
        print(f'  {m}: no Dominance events')
        continue
    n_den = int(dom_m['winner_is_denser'].sum())
    n = len(dom_m)
    p = stats.binomtest(n_den, n, 0.5).pvalue
    print(f'  {m}: winner denser in {n_den}/{n} ({n_den/n:.1%}), binomial p={p:.3g}')
dom_all = df[df['outcome'] == 0]
if len(dom_all) > 0:
    n_den = int(dom_all['winner_is_denser'].sum())
    n = len(dom_all)
    p = stats.binomtest(n_den, n, 0.5).pvalue
    print(f'  All media pooled: {n_den}/{n} ({n_den/n:.1%}), binomial p={p:.3g}')

print('\n[Q1b] Signed ΔOD vs PDI (per-event Spearman):')
for m in MEDIUMS:
    sub = df[df['Medium'] == m].dropna(subset=['PDI'])
    if len(sub) < 3:
        continue
    rho, p = stats.spearmanr(sub['dOD_signed'], sub['PDI'])
    print(f'  {m}: rho={rho:.3f}, p={p:.3g}, n={len(sub)}')

print('\n[Q2] parental OD vs same-parental correlation (Spearman):')
for m in MEDIUMS:
    sub = df_parent[df_parent['Medium'] == m]
    if len(sub) < 3:
        continue
    rho_s, p_s = stats.spearmanr(sub['parent_OD'], sub['same_parental_corr'])
    cross_cell = df_corr[df_corr['Medium'] == m]
    cross_mean, cross_lo, cross_hi = bootstrap_mean_ci(cross_cell['cross_corr'].values)
    print(f'  {m}: same rho={rho_s:+.3f} p={p_s:.3g} n={len(sub)}; '
          f'cross mean={cross_mean:+.3f} [{cross_lo:+.2f},{cross_hi:+.2f}]')

print('\n[Q2] parental OD tertile means (same-parental) per medium:')
for m in MEDIUMS:
    for t in tertile_labels:
        cell = df_parent[(df_parent['Medium'] == m) & (df_parent['parent_OD_tertile'] == t)]
        if len(cell) == 0:
            continue
        ms, lo_s, hi_s = bootstrap_mean_ci(cell['same_parental_corr'].values)
        od_min = cell['parent_OD'].min()
        od_max = cell['parent_OD'].max()
        print(f'  {m} {t:<4} OD={od_min:.3f}-{od_max:.3f} n={len(cell):3d}  '
              f'same={ms:+.3f}[{lo_s:+.2f},{hi_s:+.2f}]')

print('\n===== Done (R1-1 refactor) =====')
