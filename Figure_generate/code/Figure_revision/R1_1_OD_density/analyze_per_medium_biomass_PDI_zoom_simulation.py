"""
analyze_per_medium_biomass_PDI_zoom_simulation.py
=================================================

Simulation analogue of ``analyze_per_medium_OD_PDI_zoom.py``.

Replaces experimental community OD_{600} with the natural gLV analogue, the
total final-day biomass Sum_i y_i of each parent community, and reruns the
exact same vector-decomposition / classification pipeline used by the main
paper (``common_setup.metric_VectorDecomposition_onlyPositive`` ->
``calculate_assymetricity`` -> ``characterize_case``).

Data source
-----------
    Simulation_Data/48species_100reps_final/Community_100reps_final.json

This is the canonical 48-species, 100-rep main-text run produced by
``run_48species_100reps_final.py``. The JSON is keyed by interaction
strength mu in {'0.3', '0.6', '0.8'} which the paper maps to media
Nutr- / Base / Nutr+ respectively. Each rep contains ``sc_list`` (four
final parent abundance vectors of length 48) and ``cc_list`` (six
coalesced vectors, one per parent pair).

For each (mu, rep, pair (i, j)):
    c1     = sc_list[i]
    c2     = sc_list[j]
    c_mix  = cc_list[f'{i}_{j}']
    biom_i = sum(c1)         # simulation analogue of parent OD
    biom_j = sum(c2)
    (u, v, k)  = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)
    (x, y)     = calculate_assymetricity(u, v, k)
    outcome    = characterize_case(x, y)
    PDI        = u / (u + v)
    winner     = 1 if u > v else 2

For each mu the script writes three figures, mirroring the experimental
zoom script:

    Fig_{LN,MN,HN}_zoom_simulation_winner_loser_biomass.{pdf,svg,png}
    Fig_{LN,MN,HN}_zoom_simulation_dOD_vs_PDI.{pdf,svg,png}
    Fig_{LN,MN,HN}_zoom_simulation_combined.{pdf,svg,png}

The combined files are the ones the internal memo cites.
"""

import sys, os, json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, CODE_DIR)
os.chdir(CODE_DIR)

from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
    mm,
)
from COLORMAP import PHASE_DIAGRAM_COLORS

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

PDI_AUX_LOW = 0.25
PDI_AUX_HIGH = 0.75

SIM_JSON = os.path.join(
    CODE_DIR,
    "Simulation_Data",
    "48species_100reps_final",
    "Community_100reps_final.json",
)

# mu -> (medium tag, pretty label, aesthetic)
MEDIA = [
    ('0.3', 'LN', r'Nutr$-$  ($\mu=0.3$)'),
    ('0.6', 'MN', r'Base  ($\mu=0.6$)'),
    ('0.8', 'HN', r'Nutr$+$  ($\mu=0.8$)'),
]


# ---------------------------------------------------------------------------
# Build per-event dataframe from the simulation JSON
# ---------------------------------------------------------------------------
def build_per_event_records(all_results, mu_key):
    """Return list of per-event dicts for one interaction strength."""
    records = []
    n_decomp_fail = 0
    reps = all_results[mu_key]
    for rep_key, rep_data in reps.items():
        sc_list = rep_data['sc_list']
        cc_list = rep_data['cc_list']
        sc_keys = sorted([k for k in sc_list.keys() if k.isdigit()], key=int)
        for ii in range(len(sc_keys)):
            for jj in range(ii + 1, len(sc_keys)):
                i_key, j_key = sc_keys[ii], sc_keys[jj]
                pair_key = f'{i_key}_{j_key}'
                if pair_key not in cc_list:
                    continue
                c1 = np.asarray(sc_list[i_key], dtype=float)
                c2 = np.asarray(sc_list[j_key], dtype=float)
                cmix = np.asarray(cc_list[pair_key], dtype=float)

                biom1 = float(c1.sum())
                biom2 = float(c2.sum())
                if biom1 <= 0 or biom2 <= 0:
                    continue

                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
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
                    'mu': mu_key,
                    'rep': rep_key,
                    'pair': pair_key,
                    'OD_Sub1': biom1,
                    'OD_Sub2': biom2,
                    'meanOD': 0.5 * (biom1 + biom2),
                    'dOD_signed': biom1 - biom2,
                    'dOD_abs': abs(biom1 - biom2),
                    'u': u, 'v': v, 'k': k,
                    'PDI': pdi,
                    'outcome': outcome,
                    'winner': winner,
                })
    return records, n_decomp_fail


# ---------------------------------------------------------------------------
# Per-medium rendering
# ---------------------------------------------------------------------------
def render_medium(all_results, mu_key, medium_tag, medium_pretty):
    records, n_decomp_fail = build_per_event_records(all_results, mu_key)

    tag = medium_tag
    print(f"[{tag}-zoom-sim  mu={mu_key}] events with biomass + decomp: "
          f"{len(records)}   decomp fails: {n_decomp_fail}")
    if not records:
        print(f"[{tag}-zoom-sim] no events — skipping")
        return None

    OD_Sub1 = np.array([r['OD_Sub1'] for r in records])
    OD_Sub2 = np.array([r['OD_Sub2'] for r in records])
    dOD = np.array([r['dOD_signed'] for r in records])
    PDI = np.array([r['PDI'] for r in records])
    outcome = np.array([r['outcome'] for r in records])
    winner = np.array([r['winner'] for r in records])

    n_dom = int((outcome == 0).sum())
    n_mix = int((outcome == 1).sum())
    n_rest = int((outcome == 2).sum())
    print(f"[{tag}-zoom-sim] Dom={n_dom}  Mix={n_mix}  Rest={n_rest}")
    print(f"[{tag}-zoom-sim] Sub1 biomass range "
          f"[{OD_Sub1.min():.3f}, {OD_Sub1.max():.3f}]")
    print(f"[{tag}-zoom-sim] Sub2 biomass range "
          f"[{OD_Sub2.min():.3f}, {OD_Sub2.max():.3f}]")

    # Tight per-medium axis
    od_all = np.concatenate([OD_Sub1, OD_Sub2])
    od_lo = float(np.nanmin(od_all)) - 0.02 * (od_all.max() - od_all.min() + 1e-9)
    od_hi = float(np.nanmax(od_all)) + 0.02 * (od_all.max() - od_all.min() + 1e-9)
    od_lo = max(od_lo, 0.0)
    dOD_abs_max = float(np.nanmax(np.abs(dOD))) * 1.10

    # Dominance-only subset
    dom_mask = (outcome == 0)
    if dom_mask.any():
        winner_OD = np.where(winner[dom_mask] == 1,
                             OD_Sub1[dom_mask], OD_Sub2[dom_mask])
        loser_OD = np.where(winner[dom_mask] == 1,
                            OD_Sub2[dom_mask], OD_Sub1[dom_mask])
        winner_is_denser = (winner_OD > loser_OD).astype(int)
    else:
        winner_OD = np.array([])
        loser_OD = np.array([])
        winner_is_denser = np.array([])

    # Panel (b) regression + stats
    fit = None
    rho = pval = pearson_r = pearson_p = None
    xs = np.linspace(-dOD_abs_max, dOD_abs_max, 100)
    valid = ~np.isnan(PDI)
    if valid.sum() >= 3:
        fit = np.polyfit(dOD[valid], PDI[valid], 1)
        rho, pval = stats.spearmanr(dOD[valid], PDI[valid])
        pearson_r, pearson_p = stats.pearsonr(dOD[valid], PDI[valid])

    # ====================================================================
    # Standalone (a): winner vs loser biomass for Dominance events
    # ====================================================================
    fig_a, ax_a = plt.subplots(1, 1, figsize=(75*mm, 70*mm), facecolor='w')
    ax_a.plot([od_lo, od_hi], [od_lo, od_hi], '--', color='gray',
              linewidth=0.6, alpha=0.7)
    if winner_OD.size > 0:
        ax_a.scatter(loser_OD, winner_OD,
                     s=22, color=COLOR_DOM, alpha=0.70,
                     edgecolors='black', linewidths=0.3, label='Dominance')
        n_denser = int(winner_is_denser.sum())
        n_total = int(winner_is_denser.size)
        frac = n_denser / n_total
        binom_p = stats.binomtest(n_denser, n_total, 0.5).pvalue
        ax_a.text(0.03, 0.97,
                  f'winner denser:\n{n_denser}/{n_total} ({frac:.0%})\n'
                  f'binom p={binom_p:.2g}',
                  transform=ax_a.transAxes, fontsize=7, va='top', ha='left')
    ax_a.set_title(f'{medium_pretty}  (simulation)', fontsize=9)
    ax_a.set_xlim(od_lo, od_hi)
    ax_a.set_ylim(od_lo, od_hi)
    ax_a.set_aspect('equal', adjustable='box')
    ax_a.set_xlabel(r'Loser biomass  $\sum_i y_i$', fontsize=8)
    ax_a.set_ylabel(r'Winner biomass  $\sum_i y_i$', fontsize=8)
    sns.despine(ax=ax_a)
    fig_a.tight_layout()
    for ext in ['pdf', 'svg', 'png']:
        fig_a.savefig(os.path.join(
            SCRIPT_DIR,
            f'Fig_{tag}_zoom_simulation_winner_loser_biomass.{ext}'),
            dpi=300, bbox_inches='tight')
    plt.close(fig_a)
    print(f'[{tag}-zoom-sim] wrote Fig_{tag}_zoom_simulation_winner_loser_biomass')

    # ====================================================================
    # Standalone (b): signed dOD vs PDI for all events
    # ====================================================================
    fig_b, ax_b = plt.subplots(1, 1, figsize=(75*mm, 70*mm), facecolor='w')
    ax_b.axhline(0.5, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    ax_b.axvline(0.0, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    ax_b.axhline(PDI_AUX_HIGH, color='black', linestyle=':',
                 linewidth=0.6, alpha=0.7)
    ax_b.axhline(PDI_AUX_LOW, color='black', linestyle=':',
                 linewidth=0.6, alpha=0.7)
    ax_b.scatter(-dOD[valid], 1 - PDI[valid],
                 s=10, color='lightgray', alpha=0.35, edgecolors='none', zorder=1)
    for outcome_val, clr, label in [(0, COLOR_DOM, 'Dominance'),
                                     (1, COLOR_MIX, 'Mixing'),
                                     (2, COLOR_REST, 'Restructuring')]:
        m = valid & (outcome == outcome_val)
        if m.any():
            ax_b.scatter(dOD[m], PDI[m],
                         s=18, color=clr, alpha=0.70,
                         edgecolors='black', linewidths=0.3,
                         label=label, zorder=2)
    if fit is not None:
        ax_b.plot(xs, np.polyval(fit, xs), '-', color='black',
                  linewidth=0.8, alpha=0.75, zorder=3,
                  label=f'linear fit (slope={fit[0]:+.2f})')
        ax_b.text(0.03, 0.97,
                  f'Spearman $\\rho$={rho:+.2f}, p={pval:.2g}\n'
                  f'Pearson r={pearson_r:+.2f}, p={pearson_p:.2g}\n'
                  f'n={int(valid.sum())}',
                  transform=ax_b.transAxes, fontsize=7, va='top', ha='left')
    ax_b.text(dOD_abs_max, PDI_AUX_HIGH, ' PDI=0.75',
              fontsize=6, color='black', va='bottom', ha='right', alpha=0.7)
    ax_b.text(dOD_abs_max, PDI_AUX_LOW, ' PDI=0.25',
              fontsize=6, color='black', va='top', ha='right', alpha=0.7)
    ax_b.set_title(f'{medium_pretty}  (simulation)', fontsize=9)
    ax_b.set_xlim(-dOD_abs_max, dOD_abs_max)
    ax_b.set_ylim(-0.05, 1.05)
    ax_b.set_xlabel(r'biomass$_{\mathrm{Sub1}} - $biomass$_{\mathrm{Sub2}}$',
                    fontsize=8)
    ax_b.set_ylabel(r'PDI $= u / (u+v)$', fontsize=8)
    ax_b.legend(loc='lower right', fontsize=6, frameon=False)
    sns.despine(ax=ax_b)
    fig_b.tight_layout()
    for ext in ['pdf', 'svg', 'png']:
        fig_b.savefig(os.path.join(
            SCRIPT_DIR,
            f'Fig_{tag}_zoom_simulation_dOD_vs_PDI.{ext}'),
            dpi=300, bbox_inches='tight')
    plt.close(fig_b)
    print(f'[{tag}-zoom-sim] wrote Fig_{tag}_zoom_simulation_dOD_vs_PDI')

    # ====================================================================
    # Combined 1x2 (cited in internal memo)
    # ====================================================================
    fig_c, axes = plt.subplots(1, 2, figsize=(160*mm, 72*mm), facecolor='w')

    ax = axes[0]
    ax.plot([od_lo, od_hi], [od_lo, od_hi], '--', color='gray',
            linewidth=0.6, alpha=0.7)
    if winner_OD.size > 0:
        ax.scatter(loser_OD, winner_OD,
                   s=22, color=COLOR_DOM, alpha=0.70,
                   edgecolors='black', linewidths=0.3)
        n_denser = int(winner_is_denser.sum())
        n_total = int(winner_is_denser.size)
        frac = n_denser / n_total
        binom_p = stats.binomtest(n_denser, n_total, 0.5).pvalue
        ax.text(0.03, 0.97,
                f'winner denser:\n{n_denser}/{n_total} ({frac:.0%})\n'
                f'binom p={binom_p:.2g}',
                transform=ax.transAxes, fontsize=7, va='top', ha='left')
    ax.set_title(f'(a) {medium_pretty}: winner vs loser biomass', fontsize=9)
    ax.set_xlim(od_lo, od_hi)
    ax.set_ylim(od_lo, od_hi)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel(r'Loser biomass  $\sum_i y_i$', fontsize=8)
    ax.set_ylabel(r'Winner biomass  $\sum_i y_i$', fontsize=8)
    sns.despine(ax=ax)

    ax = axes[1]
    ax.axhline(0.5, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.axvline(0.0, color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.axhline(PDI_AUX_HIGH, color='black', linestyle=':',
               linewidth=0.6, alpha=0.7)
    ax.axhline(PDI_AUX_LOW, color='black', linestyle=':',
               linewidth=0.6, alpha=0.7)
    ax.scatter(-dOD[valid], 1 - PDI[valid],
               s=10, color='lightgray', alpha=0.35, edgecolors='none', zorder=1)
    for outcome_val, clr, label in [(0, COLOR_DOM, 'Dominance'),
                                     (1, COLOR_MIX, 'Mixing'),
                                     (2, COLOR_REST, 'Restructuring')]:
        m = valid & (outcome == outcome_val)
        if m.any():
            ax.scatter(dOD[m], PDI[m],
                       s=18, color=clr, alpha=0.70,
                       edgecolors='black', linewidths=0.3,
                       label=label, zorder=2)
    if fit is not None:
        ax.plot(xs, np.polyval(fit, xs), '-', color='black',
                linewidth=0.8, alpha=0.75, zorder=3, label='linear fit')
        ax.text(0.03, 0.97,
                f'Spearman $\\rho$={rho:+.2f}, p={pval:.2g}\n'
                f'Pearson r={pearson_r:+.2f}, p={pearson_p:.2g}\n'
                f'n={int(valid.sum())}',
                transform=ax.transAxes, fontsize=7, va='top', ha='left')
    ax.text(dOD_abs_max, PDI_AUX_HIGH, ' PDI=0.75',
            fontsize=6, color='black', va='bottom', ha='right', alpha=0.7)
    ax.text(dOD_abs_max, PDI_AUX_LOW, ' PDI=0.25',
            fontsize=6, color='black', va='top', ha='right', alpha=0.7)
    ax.set_title(f'(b) {medium_pretty}: signed $\\Delta$biomass vs PDI',
                 fontsize=9)
    ax.set_xlim(-dOD_abs_max, dOD_abs_max)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel(r'biomass$_{\mathrm{Sub1}} - $biomass$_{\mathrm{Sub2}}$',
                  fontsize=8)
    ax.set_ylabel(r'PDI $= u/(u+v)$', fontsize=8)
    ax.legend(loc='lower right', fontsize=6, frameon=False)
    sns.despine(ax=ax)

    fig_c.tight_layout()
    for ext in ['pdf', 'svg', 'png']:
        fig_c.savefig(os.path.join(
            SCRIPT_DIR,
            f'Fig_{tag}_zoom_simulation_combined.{ext}'),
            dpi=300, bbox_inches='tight')
    plt.close(fig_c)
    print(f'[{tag}-zoom-sim] wrote Fig_{tag}_zoom_simulation_combined')

    return {
        'tag': tag,
        'mu': mu_key,
        'medium_pretty': medium_pretty,
        'n_events': len(records),
        'n_dom': n_dom,
        'n_mix': n_mix,
        'n_rest': n_rest,
        'dom_winner_denser': int(winner_is_denser.sum())
            if winner_is_denser.size else 0,
        'dom_total': int(winner_is_denser.size),
        'od_range': (float(od_all.min()), float(od_all.max())),
        'spearman_rho': rho,
        'spearman_p': pval,
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'slope': fit[0] if fit is not None else None,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
print(f"Loading {SIM_JSON}")
with open(SIM_JSON) as f:
    all_results = json.load(f)
print(f"  mu keys: {list(all_results.keys())}")

summaries = []
for mu_key, tag, pretty in MEDIA:
    s = render_medium(all_results, mu_key, tag, pretty)
    if s is not None:
        summaries.append(s)

print('\n===== Per-medium simulation zoom summary =====')
for s in summaries:
    lo, hi = s['od_range']
    line = (f"  {s['tag']} (mu={s['mu']}): n={s['n_events']}  "
            f"Dom={s['n_dom']}  Mix={s['n_mix']}  Rest={s['n_rest']}  "
            f"biomass window=[{lo:.3f}, {hi:.3f}]")
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
