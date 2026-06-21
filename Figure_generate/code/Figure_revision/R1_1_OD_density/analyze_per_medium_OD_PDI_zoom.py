"""
analyze_per_medium_OD_PDI_zoom.py
=================================

Per-medium zoomed version of the R1-1 OD-density analysis, produced for
the internal memo (\S Q1 and parallel sections).  Generalizes the earlier
LN-only ``analyze_LN_OD_PDI_zoom.py`` to also render MN (Base) and HN
(Nutr+) on their own self-scaled OD windows, so each medium's winner-vs-
loser OD pattern and signed-dOD / PDI relation is visible without being
squashed by the across-media shared axes of Fig. R1-1A/B.

For each medium the script writes three figures:

    Fig_{LN,MN,HN}_zoom_winner_loser_OD.{pdf,svg,png}
    Fig_{LN,MN,HN}_zoom_dOD_vs_PDI.{pdf,svg,png}
    Fig_{LN,MN,HN}_zoom_combined.{pdf,svg,png}

The combined figures are what get copied into
``latex/revision/revision_figure_folder`` as
``internal_{LN,MN,HN}_OD_PDI_zoom.pdf`` and cited in
``internal_memo.tex``.

Auxiliary PDI boundary lines at y = 0.25 and y = 0.75 are drawn on the
signed-dOD vs PDI panel to mark the Dominance / Mixture region on the
PDI axis (round-number auxiliary lines; the exact Dom/Mix classifier
boundary in PDI units is approximately 0.293 / 0.707 but 0.25 / 0.75
are used here as simple visual guides).

Data pipeline is identical to ``analyze_OD_density.py`` (same abundance
threshold, same vector-decomposition, same outcome classifier); only the
rendering differs.
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

# Auxiliary PDI boundary lines separating Dominance (PDI > 0.75 or < 0.25)
# from Mixture (0.25 < PDI < 0.75). These are simple round-number guides;
# the exact classifier boundary in PDI is ~0.293 / ~0.707.
PDI_AUX_LOW = 0.25
PDI_AUX_HIGH = 0.75

MEDIA = [
    ('LN', r'Nutr$-$'),
    ('MN', r'Base'),
    ('HN', r'Nutr$+$'),
]


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


def build_per_event_df(medium_tag):
    records = []
    n_decomp_fail = 0
    for sp in POOL_SIZES:
        for sample_idx in Syn_Coal_IDX.get(f"{medium_tag}_{sp}", []):
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
                'Medium': medium_tag,
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
    if not df.empty:
        df['winner_OD'] = np.where(df['winner'] == 1, df['OD_Sub1'], df['OD_Sub2'])
        df['loser_OD']  = np.where(df['winner'] == 1, df['OD_Sub2'], df['OD_Sub1'])
        df['winner_is_denser'] = (df['winner_OD'] > df['loser_OD']).astype(int)
    return df, n_decomp_fail


# ---------------------------------------------------------------------------
# Per-medium rendering
# ---------------------------------------------------------------------------
def render_medium(medium_tag, medium_pretty):
    df, n_decomp_fail = build_per_event_df(medium_tag)
    tag = medium_tag

    print(f"[{tag}-zoom] events with OD + decomposition: {len(df)}   "
          f"decomp fails: {n_decomp_fail}")
    if df.empty:
        print(f"[{tag}-zoom] no events — skipping")
        return None
    print(f"[{tag}-zoom] Dom={(df['outcome']==0).sum()}  "
          f"Mix={(df['outcome']==1).sum()}  Rest={(df['outcome']==2).sum()}")
    print(f"[{tag}-zoom] OD_Sub1 range  [{df['OD_Sub1'].min():.3f}, {df['OD_Sub1'].max():.3f}]")
    print(f"[{tag}-zoom] OD_Sub2 range  [{df['OD_Sub2'].min():.3f}, {df['OD_Sub2'].max():.3f}]")

    # Tight per-medium axis range
    od_all = np.concatenate([df['OD_Sub1'].values, df['OD_Sub2'].values])
    od_lo = float(np.nanmin(od_all)) - 0.02
    od_hi = float(np.nanmax(od_all)) + 0.02
    od_lo = max(od_lo, 0.0)
    dOD_abs_max = float(np.nanmax(np.abs(df['dOD_signed']))) * 1.10

    dom = df[df['outcome'] == 0]
    sub = df.dropna(subset=['PDI'])
    od_pad = (od_hi - od_lo) * 0.035
    od_axis_lo = max(0.0, od_lo) - od_pad

    # ---- Panel (b) regression / Spearman bookkeeping (needed for both figs)
    fit = None
    rho = pval = pearson_r = pearson_p = None
    xs = np.linspace(-dOD_abs_max, dOD_abs_max, 100)
    if len(sub) >= 3:
        x_arr = sub['dOD_signed'].values
        y_arr = sub['PDI'].values
        fit = np.polyfit(x_arr, y_arr, 1)
        rho, pval = stats.spearmanr(sub['dOD_signed'], sub['PDI'])
        pearson_r, pearson_p = stats.pearsonr(sub['dOD_signed'], sub['PDI'])

    # =======================================================================
    # Standalone panel (a): winner OD vs loser OD for Dominance events
    # =======================================================================
    fig_a, ax_a = plt.subplots(1, 1, figsize=(75*mm, 70*mm), facecolor='w')
    ax_a.axhline(0.0, color='gray', linestyle=':', linewidth=0.5, alpha=0.55)
    ax_a.axvline(0.0, color='gray', linestyle=':', linewidth=0.5, alpha=0.55)
    ax_a.plot([0, od_hi], [0, od_hi], '--', color='gray',
              linewidth=0.6, alpha=0.7)
    ax_a.scatter(dom['loser_OD'], dom['winner_OD'],
                 s=35, color=COLOR_DOM, alpha=0.58,
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
    ax_a.set_title(f'{medium_pretty}  (zoomed)', fontsize=9)
    ax_a.set_xlim(od_axis_lo, od_hi)
    ax_a.set_ylim(od_axis_lo, od_hi)
    ax_a.set_aspect('equal', adjustable='box')
    ax_a.set_xlabel(r'Loser OD$_{600}$', fontsize=8)
    ax_a.set_ylabel(r'Winner OD$_{600}$', fontsize=8)
    sns.despine(ax=ax_a)
    fig_a.tight_layout()
    for ext in ['pdf', 'svg', 'png']:
        fig_a.savefig(os.path.join(SCRIPT_DIR,
                                   f'Fig_{tag}_zoom_winner_loser_OD.{ext}'),
                      dpi=300, bbox_inches='tight')
    plt.close(fig_a)
    print(f'[{tag}-zoom] wrote Fig_{tag}_zoom_winner_loser_OD')

    # =======================================================================
    # Standalone panel (b): signed dOD vs PDI for all events
    # =======================================================================
    fig_b, ax_b = plt.subplots(1, 1, figsize=(75*mm, 70*mm), facecolor='w')
    ax_b.axhline(0.5, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    ax_b.axvline(0.0, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    # Auxiliary Dominance/Mixture PDI boundaries
    ax_b.axhline(PDI_AUX_HIGH, color='black', linestyle=':',
                 linewidth=0.6, alpha=0.7)
    ax_b.axhline(PDI_AUX_LOW, color='black', linestyle=':',
                 linewidth=0.6, alpha=0.7)
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
    if fit is not None:
        ax_b.plot(xs, np.polyval(fit, xs), '-', color='black',
                  linewidth=0.8, alpha=0.75, zorder=3,
                  label=f'linear fit (slope={fit[0]:+.2f})')
        ax_b.text(0.03, 0.97,
                  f'Spearman $\\rho$={rho:+.2f}, p={pval:.2g}\n'
                  f'Pearson r={pearson_r:+.2f}, p={pearson_p:.2g}\n'
                  f'n={len(sub)}',
                  transform=ax_b.transAxes, fontsize=7, va='top', ha='left')
    # Annotate aux lines
    ax_b.text(dOD_abs_max, PDI_AUX_HIGH, ' PDI=0.75',
              fontsize=6, color='black', va='bottom', ha='right', alpha=0.7)
    ax_b.text(dOD_abs_max, PDI_AUX_LOW, ' PDI=0.25',
              fontsize=6, color='black', va='top', ha='right', alpha=0.7)
    ax_b.set_title(f'{medium_pretty}  (zoomed)', fontsize=9)
    ax_b.set_xlim(-dOD_abs_max, dOD_abs_max)
    ax_b.set_ylim(-0.05, 1.05)
    ax_b.set_xlabel(r'OD$_{\mathrm{Sub1}} - $OD$_{\mathrm{Sub2}}$', fontsize=8)
    ax_b.set_ylabel(r'PDI $= u / (u+v)$', fontsize=8)
    ax_b.legend(loc='lower right', fontsize=6, frameon=False)
    sns.despine(ax=ax_b)
    fig_b.tight_layout()
    for ext in ['pdf', 'svg', 'png']:
        fig_b.savefig(os.path.join(SCRIPT_DIR,
                                   f'Fig_{tag}_zoom_dOD_vs_PDI.{ext}'),
                      dpi=300, bbox_inches='tight')
    plt.close(fig_b)
    print(f'[{tag}-zoom] wrote Fig_{tag}_zoom_dOD_vs_PDI')

    # =======================================================================
    # Combined 1x2 figure (this is what the internal memo cites)
    # =======================================================================
    fig_c, axes = plt.subplots(1, 2, figsize=(160*mm, 72*mm), facecolor='w')

    # --- (a) winner vs loser OD ---
    ax = axes[0]
    ax.axhline(0.0, color='gray', linestyle=':', linewidth=0.5, alpha=0.55)
    ax.axvline(0.0, color='gray', linestyle=':', linewidth=0.5, alpha=0.55)
    ax.plot([0, od_hi], [0, od_hi], '--', color='gray',
            linewidth=0.6, alpha=0.7)
    ax.scatter(dom['loser_OD'], dom['winner_OD'],
               s=35, color=COLOR_DOM, alpha=0.58,
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
    ax.set_title(f'(a) {medium_pretty}: winner vs loser OD', fontsize=9)
    ax.set_xlim(od_axis_lo, od_hi)
    ax.set_ylim(od_axis_lo, od_hi)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel(r'Loser OD$_{600}$', fontsize=8)
    ax.set_ylabel(r'Winner OD$_{600}$', fontsize=8)
    sns.despine(ax=ax)

    # --- (b) signed dOD vs PDI ---
    ax = axes[1]
    ax.axhline(0.5, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.axvline(0.0, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.axhline(PDI_AUX_HIGH, color='black', linestyle=':',
               linewidth=0.6, alpha=0.7)
    ax.axhline(PDI_AUX_LOW, color='black', linestyle=':',
               linewidth=0.6, alpha=0.7)
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
    if fit is not None:
        ax.plot(xs, np.polyval(fit, xs), '-', color='black',
                linewidth=0.8, alpha=0.75, zorder=3,
                label=f'linear fit')
        ax.text(0.03, 0.97,
                f'Spearman $\\rho$={rho:+.2f}, p={pval:.2g}\n'
                f'Pearson r={pearson_r:+.2f}, p={pearson_p:.2g}\n'
                f'n={len(sub)}',
                transform=ax.transAxes, fontsize=7, va='top', ha='left')
    ax.text(dOD_abs_max, PDI_AUX_HIGH, ' PDI=0.75',
            fontsize=6, color='black', va='bottom', ha='right', alpha=0.7)
    ax.text(dOD_abs_max, PDI_AUX_LOW, ' PDI=0.25',
            fontsize=6, color='black', va='top', ha='right', alpha=0.7)
    ax.set_title(f'(b) {medium_pretty}: signed $\\Delta$OD vs PDI', fontsize=9)
    ax.set_xlim(-dOD_abs_max, dOD_abs_max)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel(r'OD$_{\mathrm{Sub1}} - $OD$_{\mathrm{Sub2}}$', fontsize=8)
    ax.set_ylabel(r'PDI $= u/(u+v)$', fontsize=8)
    ax.legend(loc='lower right', fontsize=6, frameon=False)
    sns.despine(ax=ax)

    fig_c.tight_layout()
    for ext in ['pdf', 'svg', 'png']:
        fig_c.savefig(os.path.join(SCRIPT_DIR,
                                   f'Fig_{tag}_zoom_combined.{ext}'),
                      dpi=300, bbox_inches='tight')
    plt.close(fig_c)
    print(f'[{tag}-zoom] wrote Fig_{tag}_zoom_combined')

    return {
        'tag': tag,
        'medium_pretty': medium_pretty,
        'n_events': len(df),
        'n_dom': int((df['outcome'] == 0).sum()),
        'dom_winner_denser': int(dom['winner_is_denser'].sum()) if len(dom) else 0,
        'dom_total': len(dom),
        'od_range': (float(od_all.min()), float(od_all.max())),
        'spearman_rho': rho,
        'spearman_p': pval,
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'slope': fit[0] if fit is not None else None,
    }


# ---------------------------------------------------------------------------
# Main: loop over LN, MN, HN
# ---------------------------------------------------------------------------
summaries = []
for tag, pretty in MEDIA:
    s = render_medium(tag, pretty)
    if s is not None:
        summaries.append(s)

print('\n===== Per-medium zoom summary =====')
for s in summaries:
    lo, hi = s['od_range']
    line = (f"  {s['tag']} ({s['medium_pretty']}): "
            f"n={s['n_events']}  Dom={s['n_dom']}  "
            f"OD window=[{lo:.3f}, {hi:.3f}]")
    if s['dom_total'] > 0:
        n_den = s['dom_winner_denser']
        n = s['dom_total']
        p = stats.binomtest(n_den, n, 0.5).pvalue
        line += (f"  winner_denser={n_den}/{n} ({n_den/n:.1%}, "
                 f"binom p={p:.3g})")
    if s['spearman_rho'] is not None:
        line += (f"  Spearman rho={s['spearman_rho']:+.3f} "
                 f"(p={s['spearman_p']:.3g}); "
                 f"slope={s['slope']:+.3f}")
    print(line)
print('===== Done =====')
