#!/usr/bin/env python3
"""
R1-4: Pool Size / Richness Effects
====================================
Reviewer R1, Point #4.

The reviewer asked two questions:
  (i)  Is there no significant effect of initial pool size on experimental
       coalescence outcomes?
  (ii) As a complementary model check, how do Dominance frequency and pairwise
       selection correlation change with model pool size?

Figure layout (2 rows x 3 cols):
  Row 1 (experiment, pool sizes 6 / 12 / 24):
      A  realized parental richness vs pool size
      B  ASV richness per inoculated isolate x medium, grouped by initial pool size
      C  Dominance fraction x medium, grouped by initial pool size
      D  pairwise selection correlation x medium, grouped by initial pool size
  Row 2 (gLV model, pool sizes 4,6,9,12,24,48; mu in {0.3, 0.6, 0.8}):
      E  Dominance fraction x model pool size x mu
      F  pairwise selection correlation x model pool size x mu

For the model panels we use the pool-size ablation simulations
(`Simulation_Data/{4,6,9,12,24,48}percomm_ablation_species_number`).  The
interaction matrices were not stored in those JSONs, but the random seed
used to build each matrix *was* saved, so we reconstruct every matrix
deterministically from its seed.
"""

import sys
import os
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from scipy import stats

# ── Paths ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
CODE_DIR = os.path.join(PROJECT_ROOT, 'Figure_generate', 'code')
sys.path.insert(0, CODE_DIR)

_orig_cwd = os.getcwd()
os.chdir(CODE_DIR)
from COLORMAP import get_phase_diagram_colors
from PairwiseCorrelationAnalysis_PerEvent import calculate_correlation_single_event
from common_setup import (metric_VectorDecomposition_onlyPositive,
                           calculate_assymetricity, characterize_case,
                           exception_list)
os.chdir(_orig_cwd)

# ── Style ─────────────────────────────────────────────────────────────────
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
THRESHOLD = 0.001

medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
medium_order = ['L', 'M', 'H']
medium_colors = {'L': '#4A90D9', 'M': '#2ECC71', 'H': '#E67E22'}

pool_exp = [6, 12, 24]
pool_colors_exp = {6: '#4A90D9', 12: '#2ECC71', 24: '#E67E22'}

# Model sweep: three mu levels analogous to Nutr-, Base, Nutr+
MU_LEVELS = ['0.30', '0.60', '0.80']
MU_COLORS = {'0.30': '#4A90D9', '0.60': '#2ECC71', '0.80': '#E67E22'}
MU_LABELS = {'0.30': r'$\mu = 0.30$',
             '0.60': r'$\mu = 0.60$',
             '0.80': r'$\mu = 0.80$'}

# ── Experimental data ─────────────────────────────────────────────────────
ASV_PATH = os.path.join(PROJECT_ROOT, 'Postprocessed',
                        'processed_Sequences_synthetic.xlsx')
COMMUNITIES_PATH = os.path.join(PROJECT_ROOT, 'Analyzed',
                                'processed_Communities_synthetic.xlsx')
COALESCENCE_PATH = os.path.join(PROJECT_ROOT, 'Analyzed',
                                'processed_CoalescenceEvent_synthetic.xlsx')

print("Loading experimental data...")
asv_data = pd.read_excel(ASV_PATH)
communities_data = pd.read_excel(COMMUNITIES_PATH)
coalescence_data = pd.read_excel(COALESCENCE_PATH)


def get_pool_size_sub(cidx):
    cidx = int(cidx)
    if cidx <= 9:
        return 6
    if cidx <= 18:
        return 12
    if cidx <= 30:
        return 24
    return None


def get_pool_size_coal(cidx):
    cidx = int(cidx)
    if cidx <= 14:
        return 6
    if cidx <= 41:
        return 12
    if cidx <= 47:
        return 24
    return None


def compute_richness(asv_df, sid, threshold=THRESHOLD):
    row = asv_df[asv_df['SampleIDX'] == sid]
    if len(row) == 0:
        return np.nan
    ab = np.array(row.iloc[0, 1:], dtype=float)
    return int(np.sum(ab > threshold))


def get_abundance(sid, threshold=THRESHOLD):
    row = asv_data[asv_data['SampleIDX'] == sid]
    if len(row) == 0:
        return None
    ab = np.array(row.iloc[0, 1:], dtype=float)
    ab = ab * (ab > threshold)
    return ab


# ── Pairwise species selection helper ────────────────────────────────────
# The manuscript uses this concordance-based same-parent versus cross-parent
# pairwise fate metric (cf. Fig. 2D). The
# canonical per-event implementation lives in
# Figure_generate/code/PairwiseCorrelationAnalysis_PerEvent.py and is
# imported as calculate_correlation_single_event.
#
# Key points of the canonical definition, to avoid the two drift-prone
# variants of this metric:
#   (i)  Shared species (present in both parents, which is the common
#        case in the experiments because all parents are drawn from a
#        54-species library) are assigned to the parent with the larger
#        abundance, NOT discarded.  The set-difference "exclusive only"
#        variant throws out most of the experimental data and collapses
#        the same-vs-cross signal.
#   (ii) The correlation metric is concordance-based:
#            corr = 2 * mean( 1[presence_i == presence_j] ) - 1
#        so both-present AND both-absent count as concordant.  The
#        simpler joint-presence rate (mean(presence_i * presence_j))
#        under-counts concordance and biases Nutr+ (many shared absences)
#        toward zero.
#
# Small wrapper so the two call sites in this script get a (phi_abs,
# same_corr, cross_corr) triple whether or not the event has enough
# species to compute both parts.

def count_surv(vec, thr=THRESHOLD):
    return int(np.sum(np.array(vec) > thr))


def surv_idx(vec, thr=THRESHOLD):
    return np.where(np.array(vec) > thr)[0]


def _pair_selection_stats(sc_i, sc_j, cc_ij):
    """Per-event pairwise fate concordance using the canonical
    concordance-based correlation from PairwiseCorrelationAnalysis_PerEvent.
    Returns (|phi|, same_origin_corr, mixed_origin_corr).  The |phi| is
    kept as a scalar summary (origin -> persistence); same/cross are the
    two values plotted in panels C and D.  All three share the same
    presence threshold as the rest of this script.
    """
    result = calculate_correlation_single_event(
        np.asarray(cc_ij), np.asarray(sc_i), np.asarray(sc_j),
        threshold=THRESHOLD)
    if result is None:
        return np.nan, np.nan, np.nan

    same_corr = result['same_origin_corr']
    cross_corr = result['mixed_origin_corr']

    # Origin -> persistence |phi| (optional scalar; retained for
    # compatibility with the simulation summary table).  We recompute it
    # here using the same origin-assignment rule the canonical function
    # uses, namely "assign shared species to the more-abundant parent".
    sc_i = np.asarray(sc_i)
    sc_j = np.asarray(sc_j)
    cc = np.asarray(cc_ij)
    present_i = sc_i > THRESHOLD
    present_j = sc_j > THRESHOLD
    both = present_i & present_j
    origin = np.full(sc_i.shape, -1, dtype=int)
    origin[present_i & ~both] = 0
    origin[present_j & ~both] = 1
    both_idx = np.where(both)[0]
    origin[both_idx] = np.where(sc_i[both_idx] >= sc_j[both_idx], 0, 1)
    mask = origin >= 0
    if mask.sum() < 3 or cc[mask].std() == 0 or origin[mask].std() == 0:
        phi_abs = np.nan
    else:
        persist = (cc[mask] > THRESHOLD).astype(float)
        if persist.std() == 0:
            phi_abs = 0.0
        else:
            phi_abs = abs(np.corrcoef(origin[mask], persist)[0, 1])

    return phi_abs, same_corr, cross_corr


# Parental experimental communities
parent_records = []
for _, row in communities_data.iterrows():
    if row['CoalescenceType'] != 'S':
        continue
    sid = row['SampleIDX']
    if sid in exception_list or sid not in asv_data['SampleIDX'].values:
        continue
    ps = get_pool_size_sub(row['CommunityIDX'])
    if ps is None:
        continue
    r = compute_richness(asv_data, sid)
    parent_records.append({
        'SampleIDX': sid, 'Medium': row['Medium'],
        'PoolSize': ps, 'Richness': r,
        'AssemblySurvivalRatio': r / ps if ps else np.nan,
    })
df_parents = pd.DataFrame(parent_records)

# Coalescence experimental outcomes
coal_records = []
for _, row in coalescence_data.iterrows():
    sid = row['SampleIDX']
    if sid in exception_list:
        continue
    ps = get_pool_size_coal(row['CommunityIDX'])
    if ps is None:
        continue
    n_A = get_abundance(row['SampleIDX_Sub1'])
    n_B = get_abundance(row['SampleIDX_Sub2'])
    n_C = get_abundance(sid)
    if n_A is None or n_B is None or n_C is None:
        continue
    if np.linalg.norm(n_A) == 0 or np.linalg.norm(n_B) == 0 or np.linalg.norm(n_C) == 0:
        continue
    try:
        u, v, k = metric_VectorDecomposition_onlyPositive(n_A, n_B, n_C)
    except (np.linalg.LinAlgError, FloatingPointError, ZeroDivisionError):
        continue
    if np.isnan(u) or np.isnan(v) or np.isnan(k) \
       or np.isinf(u) or np.isinf(v) or np.isinf(k):
        continue
    x_mag, y_asym = calculate_assymetricity(u, v, k)
    cat = characterize_case(x_mag, y_asym)
    if cat is None:
        continue
    # Pairwise species selection on the experimental event
    psc_phi_abs, psc_same_cop, psc_cross_cop = _pair_selection_stats(
        n_A, n_B, n_C)
    present_A = np.asarray(n_A) > THRESHOLD
    present_B = np.asarray(n_B) > THRESHOLD
    present_C = np.asarray(n_C) > THRESHOLD
    parent_richness_sum = int(present_A.sum() + present_B.sum())
    survival_ratio = (
        int((present_A & present_C).sum() + (present_B & present_C).sum())
        / parent_richness_sum
        if parent_richness_sum > 0 else np.nan
    )
    coal_records.append({
        'SampleIDX': sid, 'Medium': row['Medium'],
        'PoolSize': ps, 'category': cat,
        'SurvivalRatio': survival_ratio,
        'psc_phi_abs':   psc_phi_abs,
        'psc_same_cop':  psc_same_cop,
        'psc_cross_cop': psc_cross_cop,
    })
df_coal = pd.DataFrame(coal_records)
df_coal['category_name'] = df_coal['category'].map(
    {0: 'Dominance', 1: 'Mixture', 2: 'Restructuring'})

print(f"  parents: {len(df_parents)}, coalescence events: {len(df_coal)}")


# ── Simulation data: reconstruct matrices and compute stats ───────────────
SIM_CONFIGS = [
    {"num_S": 4,  "N": 16,  "name": "4percomm"},
    {"num_S": 6,  "N": 24,  "name": "6percomm"},
    {"num_S": 9,  "N": 36,  "name": "9percomm"},
    {"num_S": 12, "N": 48,  "name": "12percomm"},
    {"num_S": 24, "N": 96,  "name": "24percomm"},
    {"num_S": 48, "N": 192, "name": "48percomm"},
]
SIM_MAX_REPS = 100   # reps per (pool size, mu); tight error bars, fast


def reconstruct_I(seed, N, mu):
    np.random.seed(seed)
    I = np.eye(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                I[i, j] = np.random.uniform(0, 2 * mu)
    return I


def analyze_sim_config(cfg, mu_key, max_reps=SIM_MAX_REPS):
    """Return per-rep summary rows for one (pool size, mu) combination."""
    path = os.path.join(
        CODE_DIR, 'Simulation_Data',
        f"{cfg['num_S']}percomm_ablation_species_number",
        f"Community_ablation_{cfg['name']}.json",
    )
    if not os.path.exists(path):
        print(f"  [skip] {path} missing")
        return []

    with open(path, 'r') as f:
        sim = json.load(f)
    if mu_key not in sim:
        return []
    reps = sim[mu_key]
    rep_keys = sorted(reps.keys())[:max_reps]

    rows = []
    for rk in rep_keys:
        rd = reps[rk]
        N = rd['parameters']['N']
        num_C = rd['parameters']['num_C']
        mu = rd['parameters']['mu']
        seed = rd['parameters']['seed']

        I = reconstruct_I(seed, N, mu)
        within_vals, between_vals = [], []
        for ci in range(num_C):
            si = surv_idx(rd['sc_list'][str(ci)])
            if len(si) >= 2:
                block = I[np.ix_(si, si)]
                within_vals.append(np.mean(block[~np.eye(len(si), dtype=bool)]))
            for cj in range(ci + 1, num_C):
                sj = surv_idx(rd['sc_list'][str(cj)])
                if len(si) >= 1 and len(sj) >= 1:
                    block = I[np.ix_(si, sj)]
                    between_vals.append(np.mean(block))

        within_mean = np.mean(within_vals) if within_vals else np.nan
        between_mean = np.mean(between_vals) if between_vals else np.nan

        dom_flags = []
        psc_phi, psc_same, psc_cross = [], [], []
        for ci in range(num_C):
            for cj in range(ci + 1, num_C):
                key = f"{ci}_{cj}"
                if key not in rd['cc_list']:
                    continue
                n_A = np.array(rd['sc_list'][str(ci)])
                n_B = np.array(rd['sc_list'][str(cj)])
                n_C = np.array(rd['cc_list'][key])
                if np.linalg.norm(n_A) == 0 or np.linalg.norm(n_B) == 0 \
                   or np.linalg.norm(n_C) == 0:
                    continue
                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(
                        n_A, n_B, n_C)
                except (np.linalg.LinAlgError, FloatingPointError,
                        ZeroDivisionError):
                    continue
                if any(np.isnan([u, v, k])) or any(np.isinf([u, v, k])):
                    continue
                x_mag, y_asym = calculate_assymetricity(u, v, k)
                cat = characterize_case(x_mag, y_asym)
                if cat is not None:
                    dom_flags.append(int(cat == 0))

                phi_abs, same_cop, cross_cop = _pair_selection_stats(
                    n_A, n_B, n_C)
                if not np.isnan(phi_abs):
                    psc_phi.append(phi_abs)
                if not np.isnan(same_cop):
                    psc_same.append(same_cop)
                if not np.isnan(cross_cop):
                    psc_cross.append(cross_cop)

        rows.append({
            'num_S': cfg['num_S'],
            'mu': float(mu),
            'mu_key': mu_key,
            'rep': rk,
            'within_alpha': within_mean,
            'between_alpha': between_mean,
            'dom_count': int(sum(dom_flags)),
            'total_pairs': len(dom_flags),
            'psc_phi_abs': np.mean(psc_phi) if psc_phi else np.nan,
            'psc_same_cop': np.mean(psc_same) if psc_same else np.nan,
            'psc_cross_cop': np.mean(psc_cross) if psc_cross else np.nan,
            'psc_n_events': len(psc_phi),
        })
    return rows


print("\nAnalyzing simulations at mu in %s ..." % MU_LEVELS)
sim_rows = []
for mu_key in MU_LEVELS:
    for cfg in SIM_CONFIGS:
        print(f"  {cfg['name']} @ mu={mu_key} ...", end=' ', flush=True)
        batch = analyze_sim_config(cfg, mu_key)
        print(f"{len(batch)} reps")
        sim_rows.extend(batch)
df_sim = pd.DataFrame(sim_rows)
print(f"  total simulation rows: {len(df_sim)}")


# ── Statistics ────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STATISTICS")
print("=" * 60)

print("\n[experiment]")
print("Richness KW across pool sizes:",
      stats.kruskal(*[df_parents[df_parents['PoolSize'] == p]['Richness']
                      .dropna() for p in pool_exp]))
print("ASV richness per inoculated isolate KW across pool sizes:",
      stats.kruskal(*[df_parents[df_parents['PoolSize'] == p]['AssemblySurvivalRatio']
                      .dropna() for p in pool_exp]))
ct = pd.crosstab(df_coal['PoolSize'], df_coal['category_name'])
chi2, chi2_p, _, _ = stats.chi2_contingency(ct)
print(f"Outcome-distribution chi2 across pool sizes: chi2={chi2:.3f}, p={chi2_p:.3e}")
print(ct)

# per medium x pool size
print("\nMedium-stratified Dominance fractions:")
for m in medium_order:
    row = []
    for ps in pool_exp:
        sub = df_coal[(df_coal['Medium'] == m) & (df_coal['PoolSize'] == ps)]
        n = len(sub)
        f = (sub['category'] == 0).mean() if n else np.nan
        row.append(f"pool={ps}: {f:.2f} (n={n})")
    print(f"  {medium_labels[m]:<6}: " + "  ".join(row))

print("\n[simulation]")
for mu_key in MU_LEVELS:
    print(f"\n  mu = {mu_key}")
    for ps in sorted(df_sim['num_S'].unique()):
        sub = df_sim[(df_sim['num_S'] == ps) & (df_sim['mu_key'] == mu_key)]
        if len(sub) == 0:
            continue
        w, b = sub['within_alpha'].dropna(), sub['between_alpha'].dropna()
        dom_pool = sub['dom_count'].sum() / max(sub['total_pairs'].sum(), 1)
        psc_phi = sub['psc_phi_abs'].dropna()
        psc_same = sub['psc_same_cop'].dropna()
        psc_cross = sub['psc_cross_cop'].dropna()
        print(f"    pool={ps:>2}: within={w.mean():.3f}  between={b.mean():.3f}"
              f"  Dom={dom_pool:.3f}"
              f"  |phi|={psc_phi.mean():.3f}"
              f"  same_cop={psc_same.mean():.3f}  cross_cop={psc_cross.mean():.3f}"
              f"  (n_reps={len(sub)})")


# ── Figure (2 rows x 3 cols) ──────────────────────────────────────────────
# Layout:
#   A experiment: realized richness        | B experiment: richness per inoc.    | C experiment: Dominance
#   D experiment: pairwise fate concord.   | E model: Dominance           | F model: pairwise fate concord.
fig, axes = plt.subplots(2, 3, figsize=(200 * mm, 115 * mm))
positions_exp = np.arange(len(pool_exp))
positions_med = np.arange(len(medium_order))

# ---- A. experiment: realized richness ----
ax = axes[0, 0]
width = 0.24
offsets = [-width, 0, width]
rng = np.random.default_rng(42)
for off, ps in zip(offsets, pool_exp):
    data = [
        df_parents[(df_parents['Medium'] == m) & (df_parents['PoolSize'] == ps)]
        ['Richness'].dropna().values
        for m in medium_order
    ]
    pos = positions_med + off
    bp = ax.boxplot(data, positions=pos, widths=0.18,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=1),
                    whiskerprops=dict(linewidth=0.5),
                    capprops=dict(linewidth=0.5),
                    boxprops=dict(linewidth=0.5))
    for patch in bp['boxes']:
        patch.set_facecolor(pool_colors_exp[ps]); patch.set_alpha(0.55)
    for x, vals in zip(pos, data):
        if len(vals) == 0:
            continue
        jitter = rng.uniform(-0.035, 0.035, size=len(vals))
        ax.scatter(np.full(len(vals), x) + jitter, vals, s=5,
                   color=pool_colors_exp[ps], alpha=0.45,
                   edgecolors='none', zorder=5)
ax.set_xticks(positions_med)
ax.set_xticklabels([medium_labels[m] for m in medium_order])
ax.set_xlabel('Medium')
ax.set_ylabel('Realized richness (ASVs)')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_title('A  Experiment: realized richness', fontsize=8,
             fontweight='bold', loc='left')
ax.legend(
    handles=[
        mpl.patches.Patch(facecolor=pool_colors_exp[ps], edgecolor='black',
                          alpha=0.55, label=f'{ps} species')
        for ps in pool_exp
    ],
    fontsize=6, frameon=False, loc='upper left', ncol=3,
    columnspacing=0.5, handlelength=1.0,
    title='Initial pool', title_fontsize=6,
)

# ---- B. experiment: ASV richness per inoculated isolate x medium, grouped by pool size ----
ax = axes[0, 1]
width = 0.24
offsets = [-width, 0, width]
rng = np.random.default_rng(43)
for off, ps in zip(offsets, pool_exp):
    data = [
        df_parents[(df_parents['Medium'] == m) & (df_parents['PoolSize'] == ps)]
        ['AssemblySurvivalRatio'].dropna().values
        for m in medium_order
    ]
    pos = positions_med + off
    bp = ax.boxplot(data, positions=pos, widths=0.18,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=1),
                    whiskerprops=dict(linewidth=0.5),
                    capprops=dict(linewidth=0.5),
                    boxprops=dict(linewidth=0.5))
    for patch in bp['boxes']:
        patch.set_facecolor(pool_colors_exp[ps]); patch.set_alpha(0.55)
    for x, vals in zip(pos, data):
        if len(vals) == 0:
            continue
        jitter = rng.uniform(-0.035, 0.035, size=len(vals))
        ax.scatter(np.full(len(vals), x) + jitter, vals, s=5,
                   color=pool_colors_exp[ps], alpha=0.45,
                   edgecolors='none', zorder=5)
ax.set_xticks(positions_med)
ax.set_xticklabels([medium_labels[m] for m in medium_order])
ax.set_xlabel('Medium')
ax.set_ylabel('ASV richness per\ninoculated isolate')
ax.set_ylim(0, 2.6)
ax.set_title('B  Experiment: ASV richness / isolate', fontsize=8,
             fontweight='bold', loc='left')
ax.legend(
    handles=[
        mpl.patches.Patch(facecolor=pool_colors_exp[ps], edgecolor='black',
                          alpha=0.55, label=f'{ps} species')
        for ps in pool_exp
    ],
    fontsize=6, frameon=False, loc='upper right', ncol=3,
    columnspacing=0.5, handlelength=1.0,
    title='Initial pool', title_fontsize=6,
)

# ---- C. experiment: Dominance fraction x medium, grouped by pool size ----
ax = axes[0, 2]
width = 0.26
offsets = [-width, 0, width]
for off, ps in zip(offsets, pool_exp):
    fracs, errs = [], []
    for m in medium_order:
        sub = df_coal[(df_coal['Medium'] == m) & (df_coal['PoolSize'] == ps)]
        n = len(sub)
        if n:
            f = (sub['category'] == 0).mean()
            se = np.sqrt(f * (1 - f) / n)
        else:
            f, se = 0, 0
        fracs.append(f); errs.append(se)
    ax.bar(positions_med + off, fracs, width,
           yerr=errs, color=pool_colors_exp[ps], alpha=0.85,
           edgecolor='black', linewidth=0.4,
           capsize=2, error_kw={'linewidth': 0.5},
           label=f'{ps} species')
ax.set_xticks(positions_med)
ax.set_xticklabels([medium_labels[m] for m in medium_order])
ax.set_xlabel('Medium')
ax.set_ylabel('Dominance fraction')
ax.set_ylim(0, 1.05)
ax.legend(fontsize=6, frameon=False, loc='upper right',
          ncol=3, columnspacing=0.5, handlelength=1.0,
          title='Initial pool', title_fontsize=6)
ax.set_title(fr'C  Experiment: Dominance (outcome $p$=0.69)',
             fontsize=8, fontweight='bold', loc='left')

# ---- D. experiment: pairwise selection correlation grouped by pool size ----
ax = axes[1, 0]
for ps in pool_exp:
    same_means, same_ses, cross_means, cross_ses = [], [], [], []
    for m in medium_order:
        sub = df_coal[(df_coal['Medium'] == m) & (df_coal['PoolSize'] == ps)]
        s = sub['psc_same_cop'].dropna()
        c = sub['psc_cross_cop'].dropna()
        same_means.append(s.mean() if len(s) else np.nan)
        same_ses.append(s.std() / np.sqrt(max(len(s), 1)) if len(s) else 0)
        cross_means.append(c.mean() if len(c) else np.nan)
        cross_ses.append(c.std() / np.sqrt(max(len(c), 1)) if len(c) else 0)
    col = pool_colors_exp[ps]
    ax.errorbar(positions_med, same_means, yerr=same_ses,
                fmt='o-', color=col, markersize=4, linewidth=1.1,
                capsize=2, elinewidth=0.5,
                label=f'{ps} same')
    ax.errorbar(positions_med, cross_means, yerr=cross_ses,
                fmt='s--', color=col, markersize=4, linewidth=1.1,
                capsize=2, elinewidth=0.5, markerfacecolor='white',
                label=f'{ps} cross')
ax.set_xticks(positions_med)
ax.set_xticklabels([medium_labels[m] for m in medium_order])
ax.set_xlabel('Medium')
ax.set_ylabel('Pairwise selection correlation')
ax.set_ylim(-0.8, 1.0)
ax.axhline(0, color='gray', linewidth=0.4, linestyle=':')
ax.set_title('D  Experiment: pairwise selection correlation',
             fontsize=8, fontweight='bold', loc='left')
ax.legend(fontsize=5, frameon=False, loc='upper right',
          ncol=2, columnspacing=0.6, handlelength=1.2, labelspacing=0.2)

# ---- E. model: Dominance fraction x pool size x mu ----
pool_sim_sorted = sorted(df_sim['num_S'].unique())
positions_sim = np.arange(len(pool_sim_sorted))
ax = axes[1, 1]
width = 0.26
offsets = [-width, 0, width]
for off, mu_key in zip(offsets, MU_LEVELS):
    fracs, errs = [], []
    for ps in pool_sim_sorted:
        sub = df_sim[(df_sim['num_S'] == ps) & (df_sim['mu_key'] == mu_key)]
        n = sub['total_pairs'].sum()
        k = sub['dom_count'].sum()
        f = k / n if n else 0
        se = np.sqrt(f * (1 - f) / n) if n else 0
        fracs.append(f); errs.append(se)
    ax.bar(positions_sim + off, fracs, width,
           yerr=errs, color=MU_COLORS[mu_key], alpha=0.85,
           edgecolor='black', linewidth=0.4,
           capsize=2, error_kw={'linewidth': 0.5},
           label=MU_LABELS[mu_key])
ax.set_xticks(positions_sim)
ax.set_xticklabels([str(p) for p in pool_sim_sorted])
ax.set_xlabel('Initial pool size (model)')
ax.set_ylabel('Dominance fraction')
ax.set_ylim(0, 1.05)
ax.legend(fontsize=6, frameon=False, loc='upper left',
          ncol=3, columnspacing=0.5, handlelength=1.0)
ax.set_title(r'E  Model: Dominance across $\mu$',
             fontsize=8, fontweight='bold', loc='left')

# ---- F. model: same vs cross pairwise selection correlation vs pool size ----
ax = axes[1, 2]
for mu_key in MU_LEVELS:
    same_means, same_ses, cross_means, cross_ses = [], [], [], []
    for ps in pool_sim_sorted:
        sub = df_sim[(df_sim['num_S'] == ps) & (df_sim['mu_key'] == mu_key)]
        s = sub['psc_same_cop'].dropna()
        c = sub['psc_cross_cop'].dropna()
        same_means.append(s.mean() if len(s) else np.nan)
        same_ses.append(s.std() / np.sqrt(max(len(s), 1)) if len(s) else 0)
        cross_means.append(c.mean() if len(c) else np.nan)
        cross_ses.append(c.std() / np.sqrt(max(len(c), 1)) if len(c) else 0)
    col = MU_COLORS[mu_key]
    ax.errorbar(positions_sim, same_means, yerr=same_ses, fmt='o-',
                color=col, markersize=4, linewidth=1.1,
                capsize=2, elinewidth=0.5,
                label=MU_LABELS[mu_key] + ' same')
    ax.errorbar(positions_sim, cross_means, yerr=cross_ses, fmt='s--',
                color=col, markersize=4, linewidth=1.1,
                capsize=2, elinewidth=0.5, markerfacecolor='white',
                label=MU_LABELS[mu_key] + ' cross')
ax.set_xticks(positions_sim)
ax.set_xticklabels([str(p) for p in pool_sim_sorted])
ax.set_xlabel('Initial pool size (model)')
ax.set_ylabel('Pairwise selection correlation')
ax.set_ylim(-0.8, 1.0)
ax.axhline(0, color='gray', linewidth=0.4, linestyle=':')
ax.set_title('F  Model: pairwise selection correlation',
             fontsize=8, fontweight='bold', loc='left')
ax.legend(fontsize=5, frameon=False, loc='upper right',
          ncol=2, columnspacing=0.6, handlelength=1.2, labelspacing=0.2)

sns.despine(fig=fig)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    out = os.path.join(SCRIPT_DIR, f'pool_size_analysis.{ext}')
    fig.savefig(out, bbox_inches='tight', dpi=300)
    print(f"  saved: {out}")
plt.close(fig)

# ── Two-panel export for R3-3 response reuse ──────────────────────────────
print("\nGenerating two-panel richness/survival export for richness-control responses...")
fig, axes_ab = plt.subplots(1, 2, figsize=(135 * mm, 58 * mm))

# ---- A. experiment: realized richness ----
ax = axes_ab[0]
width = 0.24
offsets = [-width, 0, width]
rng = np.random.default_rng(42)
for off, ps in zip(offsets, pool_exp):
    data = [
        df_parents[(df_parents['Medium'] == m) & (df_parents['PoolSize'] == ps)]
        ['Richness'].dropna().values
        for m in medium_order
    ]
    pos = positions_med + off
    bp = ax.boxplot(data, positions=pos, widths=0.18,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=1),
                    whiskerprops=dict(linewidth=0.5),
                    capprops=dict(linewidth=0.5),
                    boxprops=dict(linewidth=0.5))
    for patch in bp['boxes']:
        patch.set_facecolor(pool_colors_exp[ps]); patch.set_alpha(0.55)
    for x, vals in zip(pos, data):
        if len(vals) == 0:
            continue
        jitter = rng.uniform(-0.035, 0.035, size=len(vals))
        ax.scatter(np.full(len(vals), x) + jitter, vals, s=5,
                   color=pool_colors_exp[ps], alpha=0.45,
                   edgecolors='none', zorder=5)
ax.set_xticks(positions_med)
ax.set_xticklabels([medium_labels[m] for m in medium_order])
ax.set_xlabel('Medium')
ax.set_ylabel('Realized richness (ASVs)')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_title('A  Experiment: realized richness', fontsize=8,
             fontweight='bold', loc='left')
ax.legend(
    handles=[
        mpl.patches.Patch(facecolor=pool_colors_exp[ps], edgecolor='black',
                          alpha=0.55, label=f'{ps} species')
        for ps in pool_exp
    ],
    fontsize=6, frameon=False, loc='upper left', ncol=3,
    columnspacing=0.5, handlelength=1.0,
    title='Initial pool', title_fontsize=6,
)

# ---- B. experiment: ASV richness per inoculated isolate x medium, grouped by pool size ----
ax = axes_ab[1]
width = 0.24
offsets = [-width, 0, width]
rng = np.random.default_rng(43)
for off, ps in zip(offsets, pool_exp):
    data = [
        df_parents[(df_parents['Medium'] == m) & (df_parents['PoolSize'] == ps)]
        ['AssemblySurvivalRatio'].dropna().values
        for m in medium_order
    ]
    pos = positions_med + off
    bp = ax.boxplot(data, positions=pos, widths=0.18,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=1),
                    whiskerprops=dict(linewidth=0.5),
                    capprops=dict(linewidth=0.5),
                    boxprops=dict(linewidth=0.5))
    for patch in bp['boxes']:
        patch.set_facecolor(pool_colors_exp[ps]); patch.set_alpha(0.55)
    for x, vals in zip(pos, data):
        if len(vals) == 0:
            continue
        jitter = rng.uniform(-0.035, 0.035, size=len(vals))
        ax.scatter(np.full(len(vals), x) + jitter, vals, s=5,
                   color=pool_colors_exp[ps], alpha=0.45,
                   edgecolors='none', zorder=5)
ax.set_xticks(positions_med)
ax.set_xticklabels([medium_labels[m] for m in medium_order])
ax.set_xlabel('Medium')
ax.set_ylabel('ASV richness per\ninoculated isolate')
ax.set_ylim(0, 2.6)
ax.set_title('B  Experiment: ASV richness / isolate', fontsize=8,
             fontweight='bold', loc='left')
ax.legend(
    handles=[
        mpl.patches.Patch(facecolor=pool_colors_exp[ps], edgecolor='black',
                          alpha=0.55, label=f'{ps} species')
        for ps in pool_exp
    ],
    fontsize=6, frameon=False, loc='upper right', ncol=3,
    columnspacing=0.5, handlelength=1.0,
    title='Initial pool', title_fontsize=6,
)

sns.despine(fig=fig)
plt.tight_layout()

for ext in ['svg', 'pdf', 'png']:
    out = os.path.join(SCRIPT_DIR, f'pool_size_analysis_AB.{ext}')
    fig.savefig(out, bbox_inches='tight', dpi=300)
    print(f"  saved: {out}")
plt.close(fig)


# ── Supplementary: richness by pool size per medium (kept, unchanged) ────
print("\nGenerating supplementary: richness by pool size per medium...")
fig, axes = plt.subplots(1, 3, figsize=(160 * mm, 50 * mm), sharey=True)
for ax_i, m in enumerate(medium_order):
    ax = axes[ax_i]
    sub = df_parents[df_parents['Medium'] == m]
    bp_data = [sub[sub['PoolSize'] == p]['Richness'].dropna().values
               for p in pool_exp]
    bp = ax.boxplot(bp_data, positions=positions_exp, widths=0.4,
                    patch_artist=True, showfliers=True,
                    flierprops=dict(marker='.', markersize=3, alpha=0.5),
                    medianprops=dict(color='black', linewidth=1),
                    whiskerprops=dict(linewidth=0.5),
                    capprops=dict(linewidth=0.5),
                    boxprops=dict(linewidth=0.5))
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor(pool_colors_exp[pool_exp[i]]); patch.set_alpha(0.6)
    for i, ps in enumerate(pool_exp):
        vals = sub[sub['PoolSize'] == ps]['Richness'].dropna().values
        jitter = np.random.default_rng(42).uniform(-0.1, 0.1, size=len(vals))
        ax.scatter(positions_exp[i] + jitter, vals, s=6,
                   color=pool_colors_exp[ps], alpha=0.4,
                   edgecolors='none', zorder=5)
    ax.set_xticks(positions_exp)
    ax.set_xticklabels([str(p) for p in pool_exp])
    ax.set_xlabel('Initial pool size')
    ax.set_title(medium_labels[m], fontsize=8, fontweight='bold')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    groups_m = [sub[sub['PoolSize'] == p]['Richness'].dropna() for p in pool_exp]
    if all(len(g) > 0 for g in groups_m):
        kw_stat, kw_p = stats.kruskal(*groups_m)
        p_text = f'p={kw_p:.3f}' if kw_p > 0.001 else f'p={kw_p:.1e}'
        ax.text(0.95, 0.95, f'KW {p_text}', transform=ax.transAxes,
                ha='right', va='top', fontsize=5.5, color='gray')
axes[0].set_ylabel('Realized richness')
sns.despine(fig=fig); plt.tight_layout()
for ext in ['svg', 'pdf', 'png']:
    out = os.path.join(SCRIPT_DIR, f'pool_size_by_medium.{ext}')
    fig.savefig(out, bbox_inches='tight', dpi=300)
    print(f"  saved: {out}")
plt.close(fig)

print("\nDone.")
