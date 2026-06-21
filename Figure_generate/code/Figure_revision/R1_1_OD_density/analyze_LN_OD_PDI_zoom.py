"""
analyze_LN_OD_PDI_zoom.py
========================

Zoomed Nutr-minus (LN) version of the R1-1 OD-density analysis, produced
for the internal memo (\S Q1).  The question is:

    In Nutr-, can community OD explain PDI?

The shared-axes master figure (Fig_R1_1A_winner_loser_OD) squashes the
Nutr- cluster into a dense blob at OD ~ 0.3-0.5 because the x/y range is
driven by Nutr+ (OD up to ~2).  Here we re-render only Nutr- on its own
tight range so the trend (or lack of trend) is visible, and we add the
signed-dOD vs PDI panel with a regression line and Spearman rho for the
same subset.

Outputs:
    Fig_LN_zoom_winner_loser_OD.{pdf,svg,png}
    Fig_LN_zoom_dOD_vs_PDI.{pdf,svg,png}
    Fig_LN_zoom_combined.{pdf,svg,png}

The combined figure is what gets copied into latex/revision/revision_figure_folder
as internal_LN_OD_PDI_zoom.pdf and cited in internal_memo.tex.

Data pipeline is identical to analyze_OD_density.py (same
abundance threshold, same vector-decomposition, same outcome classifier),
only the rendering differs.
"""

import sys, os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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
MEDIUM_CLR = get_medium_colors()  # 0=LN, 1=MN, 2=HN
POOL_SIZES = [6, 12, 24]
TARGET_MEDIUM = 'LN'
MEDIUM_PRETTY = r'Nutr$-$'


# ---------------------------------------------------------------------------
# Data helpers (same as analyze_OD_density.py)
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


# ---------------------------------------------------------------------------
# Build per-event record table for LN only
# ---------------------------------------------------------------------------
records = []
n_decomp_fail = 0

for sp in POOL_SIZES:
    for sample_idx in Syn_Coal_IDX.get(f"{TARGET_MEDIUM}_{sp}", []):
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

        denom = u + v
        pdi = u / denom if denom > 0 else np.nan
        winner = 1 if u > v else 2

        records.append({
            'SampleIDX': sample_idx,
            'Medium': TARGET_MEDIUM,
            'PoolSize': sp,
            'OD_Sub1': od1,
            'OD_Sub2': od2,
            'meanOD': 0.5 * (od1 + od2),
            'dOD_signed': od1 - od2,
            'dOD_abs': abs(od1 - od2),
            'u': u, 'v': v, 'k': k,
            'PDI': pdi,
            'outcome': outcome,
            'winner': winner,
        })

df = pd.DataFrame(records)
df['winner_OD'] = np.where(df['winner'] == 1, df['OD_Sub1'], df['OD_Sub2'])
df['loser_OD']  = np.where(df['winner'] == 1, df['OD_Sub2'], df['OD_Sub1'])
df['winner_is_denser'] = (df['winner_OD'] > df['loser_OD']).astype(int)

print(f"[LN-zoom]  events with OD + decomposition: {len(df)}   decomp fails: {n_decomp_fail}")
print(f"[LN-zoom]  Dom={(df['outcome']==0).sum()}  "
      f"Mix={(df['outcome']==1).sum()}  Rest={(df['outcome']==2).sum()}")
print(f"[LN-zoom]  OD_Sub1 range  [{df['OD_Sub1'].min():.3f}, {df['OD_Sub1'].max():.3f}]")
print(f"[LN-zoom]  OD_Sub2 range  [{df['OD_Sub2'].min():.3f}, {df['OD_Sub2'].max():.3f}]")


# ---------------------------------------------------------------------------
# Tight LN-only axis range
# ---------------------------------------------------------------------------
od_all_LN = np.concatenate([df['OD_Sub1'].values, df['OD_Sub2'].values])
od_lo = float(np.nanmin(od_all_LN)) - 0.02
od_hi = float(np.nanmax(od_all_LN)) + 0.02
od_lo = max(od_lo, 0.0)

dOD_abs_max = float(np.nanmax(np.abs(df['dOD_signed']))) * 1.10


# ===========================================================================
# Panel (a): winner OD vs loser OD for Dominance events, LN-zoomed
# ===========================================================================
fig_a, ax_a = plt.subplots(1, 1, figsize=(75*mm, 70*mm), facecolor='w')

dom = df[df['outcome'] == 0]
ax_a.plot([od_lo, od_hi], [od_lo, od_hi], '--', color='gray', linewidth=0.6, alpha=0.7)
ax_a.scatter(dom['loser_OD'], dom['winner_OD'],
             s=35, color=COLOR_DOM, alpha=0.85,
             edgecolors='black', linewidths=0.4, label='Dominance')

if len(dom) > 0:
    n_denser = int(dom['winner_is_denser'].sum())
    n_total = len(dom)
    frac = n_denser / n_total
    binom_p = stats.binomtest(n_denser, n_total, 0.5).pvalue
    ax_a.text(0.03, 0.97,
              f'winner denser:\n{n_denser}/{n_total} ({frac:.0%})\n'
              f'binom p={binom_p:.2g}',
              transform=ax_a.transAxes, fontsize=7, va='top', ha='left')

ax_a.set_title(f'{MEDIUM_PRETTY}  (zoomed)', fontsize=9)
ax_a.set_xlim(od_lo, od_hi)
ax_a.set_ylim(od_lo, od_hi)
ax_a.set_aspect('equal', adjustable='box')
ax_a.set_xlabel(r'Loser OD$_{600}$', fontsize=8)
ax_a.set_ylabel(r'Winner OD$_{600}$', fontsize=8)
sns.despine(ax=ax_a)

fig_a.tight_layout()
for ext in ['pdf', 'svg', 'png']:
    fig_a.savefig(os.path.join(SCRIPT_DIR, f'Fig_LN_zoom_winner_loser_OD.{ext}'),
                  dpi=300, bbox_inches='tight')
plt.close(fig_a)
print('[LN-zoom]  wrote Fig_LN_zoom_winner_loser_OD')


# ===========================================================================
# Panel (b): signed dOD vs PDI for all LN events, zoomed, with regression
# ===========================================================================
fig_b, ax_b = plt.subplots(1, 1, figsize=(75*mm, 70*mm), facecolor='w')

ax_b.axhline(0.5, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
ax_b.axvline(0.0, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)

sub = df.dropna(subset=['PDI'])
ax_b.scatter(-sub['dOD_signed'], 1 - sub['PDI'],
             s=14, color='lightgray', alpha=0.5, edgecolors='none', zorder=1)

for outcome_val, clr, label in [(0, COLOR_DOM, 'Dominance'),
                                 (1, COLOR_MIX, 'Mixing'),
                                 (2, COLOR_REST, 'Restructuring')]:
    grp = sub[sub['outcome'] == outcome_val]
    if len(grp) > 0:
        ax_b.scatter(grp['dOD_signed'], grp['PDI'],
                     s=26, color=clr, alpha=0.80,
                     edgecolors='black', linewidths=0.4,
                     label=label, zorder=2)

# regression line using the original (non-reflected) event set
if len(sub) >= 3:
    x_arr = sub['dOD_signed'].values
    y_arr = sub['PDI'].values
    fit = np.polyfit(x_arr, y_arr, 1)
    xs = np.linspace(-dOD_abs_max, dOD_abs_max, 100)
    ax_b.plot(xs, np.polyval(fit, xs), '-', color='black',
              linewidth=0.8, alpha=0.75, zorder=3,
              label=f'linear fit (slope={fit[0]:+.2f})')

    rho, pval = stats.spearmanr(sub['dOD_signed'], sub['PDI'])
    pearson_r, pearson_p = stats.pearsonr(sub['dOD_signed'], sub['PDI'])
    ax_b.text(0.03, 0.97,
              f'Spearman $\\rho$={rho:+.2f}, p={pval:.2g}\n'
              f'Pearson r={pearson_r:+.2f}, p={pearson_p:.2g}\n'
              f'n={len(sub)}',
              transform=ax_b.transAxes, fontsize=7, va='top', ha='left')

ax_b.set_title(f'{MEDIUM_PRETTY}  (zoomed)', fontsize=9)
ax_b.set_xlim(-dOD_abs_max, dOD_abs_max)
ax_b.set_ylim(-0.05, 1.05)
ax_b.set_xlabel(r'OD$_{\mathrm{Sub1}} - $OD$_{\mathrm{Sub2}}$', fontsize=8)
ax_b.set_ylabel(r'PDI $= u / (u+v)$', fontsize=8)
ax_b.legend(loc='lower right', fontsize=6, frameon=False)
sns.despine(ax=ax_b)

fig_b.tight_layout()
for ext in ['pdf', 'svg', 'png']:
    fig_b.savefig(os.path.join(SCRIPT_DIR, f'Fig_LN_zoom_dOD_vs_PDI.{ext}'),
                  dpi=300, bbox_inches='tight')
plt.close(fig_b)
print('[LN-zoom]  wrote Fig_LN_zoom_dOD_vs_PDI')


# ===========================================================================
# Combined 1x2 figure (this is what the internal memo cites)
# ===========================================================================
fig_c, axes = plt.subplots(1, 2, figsize=(160*mm, 72*mm), facecolor='w')

# --- (a) winner vs loser OD ---
ax = axes[0]
ax.plot([od_lo, od_hi], [od_lo, od_hi], '--', color='gray', linewidth=0.6, alpha=0.7)
ax.scatter(dom['loser_OD'], dom['winner_OD'],
           s=35, color=COLOR_DOM, alpha=0.85,
           edgecolors='black', linewidths=0.4)
if len(dom) > 0:
    n_denser = int(dom['winner_is_denser'].sum())
    n_total = len(dom)
    frac = n_denser / n_total
    binom_p = stats.binomtest(n_denser, n_total, 0.5).pvalue
    ax.text(0.03, 0.97,
            f'winner denser:\n{n_denser}/{n_total} ({frac:.0%})\n'
            f'binom p={binom_p:.2g}',
            transform=ax.transAxes, fontsize=7, va='top', ha='left')
ax.set_title(f'(a) {MEDIUM_PRETTY}: winner vs loser OD', fontsize=9)
ax.set_xlim(od_lo, od_hi)
ax.set_ylim(od_lo, od_hi)
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel(r'Loser OD$_{600}$', fontsize=8)
ax.set_ylabel(r'Winner OD$_{600}$', fontsize=8)
sns.despine(ax=ax)

# --- (b) signed dOD vs PDI ---
ax = axes[1]
ax.axhline(0.5, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
ax.axvline(0.0, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
ax.scatter(-sub['dOD_signed'], 1 - sub['PDI'],
           s=14, color='lightgray', alpha=0.5, edgecolors='none', zorder=1)
for outcome_val, clr, label in [(0, COLOR_DOM, 'Dominance'),
                                 (1, COLOR_MIX, 'Mixing'),
                                 (2, COLOR_REST, 'Restructuring')]:
    grp = sub[sub['outcome'] == outcome_val]
    if len(grp) > 0:
        ax.scatter(grp['dOD_signed'], grp['PDI'],
                   s=26, color=clr, alpha=0.80,
                   edgecolors='black', linewidths=0.4,
                   label=label, zorder=2)
if len(sub) >= 3:
    ax.plot(xs, np.polyval(fit, xs), '-', color='black',
            linewidth=0.8, alpha=0.75, zorder=3,
            label=f'linear fit')
    ax.text(0.03, 0.97,
            f'Spearman $\\rho$={rho:+.2f}, p={pval:.2g}\n'
            f'Pearson r={pearson_r:+.2f}, p={pearson_p:.2g}\n'
            f'n={len(sub)}',
            transform=ax.transAxes, fontsize=7, va='top', ha='left')
ax.set_title(f'(b) {MEDIUM_PRETTY}: signed $\\Delta$OD vs PDI', fontsize=9)
ax.set_xlim(-dOD_abs_max, dOD_abs_max)
ax.set_ylim(-0.05, 1.05)
ax.set_xlabel(r'OD$_{\mathrm{Sub1}} - $OD$_{\mathrm{Sub2}}$', fontsize=8)
ax.set_ylabel(r'PDI $= u/(u+v)$', fontsize=8)
ax.legend(loc='lower right', fontsize=6, frameon=False)
sns.despine(ax=ax)

fig_c.tight_layout()
for ext in ['pdf', 'svg', 'png']:
    fig_c.savefig(os.path.join(SCRIPT_DIR, f'Fig_LN_zoom_combined.{ext}'),
                  dpi=300, bbox_inches='tight')
plt.close(fig_c)
print('[LN-zoom]  wrote Fig_LN_zoom_combined')


# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------
print('\n===== LN zoom summary =====')
if len(dom) > 0:
    n_den = int(dom['winner_is_denser'].sum())
    n = len(dom)
    p = stats.binomtest(n_den, n, 0.5).pvalue
    print(f'  Dominance (n={n}): winner denser {n_den}/{n} ({n_den/n:.1%}), '
          f'binom p={p:.3g}')
if len(sub) >= 3:
    print(f'  Signed dOD vs PDI (n={len(sub)}): Spearman rho={rho:+.3f} p={pval:.3g}; '
          f'Pearson r={pearson_r:+.3f} p={pearson_p:.3g}; '
          f'linear slope={fit[0]:+.3f}')
print(f'  LN parental OD window: [{od_all_LN.min():.3f}, {od_all_LN.max():.3f}]')
print('===== Done =====')
