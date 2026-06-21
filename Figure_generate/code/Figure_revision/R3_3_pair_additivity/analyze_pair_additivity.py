#!/usr/bin/env python
"""
R3-3 panel A: Pairwise monoculture vs coculture CFU additivity.

For each nutrient condition (LN/Nutr-, MN/Base, HN/Nutr+) and each unordered
pair (i, j) of the 12 most-abundant isolates, we compare:

  additive null : M_i + M_j     (sum of monoculture colony counts)
  observed      : mean( C_A , C_B )   where
                  C_A = CC1[i,j] + CC2[i,j]   (direction i-resident)
                  C_B = CC1[j,i] + CC2[j,i]   (direction j-resident)

A pair is scored "net competitive" (sub-additive) if observed < additive.
We also compute the Relative Yield Total RYT = C_i/M_i + C_j/M_j averaged
across directions (RYT < 1 --> net competitive).

Data: Postprocessed/PairwiseColonyCountings_processed_230915.xlsx
Sheets used: {LN,MN,HN}_mono, {LN,MN,HN}_1, {LN,MN,HN}_2
"""

import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
DATA_PATH = os.path.join(ROOT, 'Postprocessed',
                         'PairwiseColonyCountings_processed_230915.xlsx')

MEDIA = [('LN', 'Nutr$-$', '#6baed6'),
         ('MN', 'Base',    '#9ecae1'),
         ('HN', 'Nutr$+$', '#08519c')]

sns.set_style('ticks')
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def load_medium(med):
    """Return (M, CC1, CC2) arrays, indexed species 1..12 -> 0..11."""
    mono = pd.read_excel(DATA_PATH, sheet_name=f'{med}_mono')
    cc1 = pd.read_excel(DATA_PATH, sheet_name=f'{med}_1')
    cc2 = pd.read_excel(DATA_PATH, sheet_name=f'{med}_2')

    # Mono: rows rep1/rep2, cols 1..12.
    M_rep = mono.iloc[:, 1:].to_numpy(dtype=float)
    M = np.nanmean(M_rep, axis=0)

    # CC1 / CC2: rows species 1..12 (first col is label), cols 1..12.
    CC1 = cc1.iloc[:, 1:].to_numpy(dtype=float)
    CC2 = cc2.iloc[:, 1:].to_numpy(dtype=float)
    return M, CC1, CC2


def pair_stats(M, CC1, CC2, min_mono=2.0):
    """Return list of dicts with one entry per unordered pair."""
    n = len(M)
    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            Mi, Mj = M[i], M[j]
            if not np.isfinite(Mi) or not np.isfinite(Mj):
                continue
            if Mi < min_mono or Mj < min_mono:
                continue  # unreliable denominator for RYT

            # Direction A: i-row, j-col. CC1 = i count, CC2 = j count.
            C_A_i, C_A_j = CC1[i, j], CC2[i, j]
            # Direction B: j-row, i-col. CC1 = j count, CC2 = i count.
            C_B_j, C_B_i = CC1[j, i], CC2[j, i]

            tot_A = C_A_i + C_A_j if np.isfinite(C_A_i) and np.isfinite(C_A_j) else np.nan
            tot_B = C_B_i + C_B_j if np.isfinite(C_B_i) and np.isfinite(C_B_j) else np.nan
            tot = np.nanmean([tot_A, tot_B])

            additive = Mi + Mj

            ryt_A = (C_A_i / Mi + C_A_j / Mj) if np.isfinite(C_A_i) and np.isfinite(C_A_j) else np.nan
            ryt_B = (C_B_i / Mi + C_B_j / Mj) if np.isfinite(C_B_i) and np.isfinite(C_B_j) else np.nan
            ryt = np.nanmean([ryt_A, ryt_B])

            if not np.isfinite(tot):
                continue

            rows.append(dict(
                i=i + 1, j=j + 1,
                Mi=Mi, Mj=Mj, additive=additive,
                coculture_total=tot,
                delta=tot - additive,
                delta_rel=(tot - additive) / additive if additive > 0 else np.nan,
                ryt=ryt,
                subadditive=tot < additive,
                ryt_lt_1=ryt < 1 if np.isfinite(ryt) else np.nan,
            ))
    return pd.DataFrame(rows)


def species_stats(M, CC1, CC2, min_mono=2.0):
    """Return one entry per focal species in an unordered pair.

    The focal species' coculture count is averaged across the two invasion
    directions, then compared to that same species' monoculture count.
    """
    n = len(M)
    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            Mi, Mj = M[i], M[j]
            if not np.isfinite(Mi) or not np.isfinite(Mj):
                continue
            if Mi < min_mono or Mj < min_mono:
                continue  # keep denominator convention aligned with RYT

            # Direction A: i-row, j-col. CC1 = i count, CC2 = j count.
            C_A_i, C_A_j = CC1[i, j], CC2[i, j]
            # Direction B: j-row, i-col. CC1 = j count, CC2 = i count.
            C_B_j, C_B_i = CC1[j, i], CC2[j, i]

            for sp, partner, mono, counts in [
                (i + 1, j + 1, Mi, [C_A_i, C_B_i]),
                (j + 1, i + 1, Mj, [C_A_j, C_B_j]),
            ]:
                finite = [x for x in counts if np.isfinite(x)]
                if not finite:
                    continue
                coculture = float(np.mean(finite))
                rows.append(dict(
                    species=sp,
                    partner=partner,
                    mono=mono,
                    coculture=coculture,
                    rel_yield=coculture / mono if mono > 0 else np.nan,
                    suppressed=coculture < mono,
                ))
    return pd.DataFrame(rows)


def summarize(df, label):
    n = len(df)
    n_sub = int(df['subadditive'].sum())
    n_ryt = int(df['ryt_lt_1'].sum())
    print(f'  {label}: n={n}, sub-additive = {n_sub}/{n} = {100*n_sub/n:.1f}%, '
          f'RYT<1 = {n_ryt}/{n} = {100*n_ryt/n:.1f}%, '
          f'median rel.delta = {df["delta_rel"].median():+.2f}, '
          f'median RYT = {df["ryt"].median():.2f}')
    return n, n_sub, n_ryt


def summarize_species(df, label):
    n = len(df)
    n_sup = int(df['suppressed'].sum())
    print(f'  {label}: species observations n={n}, '
          f'suppressed = {n_sup}/{n} = {100*n_sup/n:.1f}%, '
          f'median relative yield = {df["rel_yield"].median():.2f}')
    return n, n_sup


def make_figure(all_pairs, out_path_base):
    fig, axes = plt.subplots(1, 4, figsize=(11.5, 2.8),
                              gridspec_kw={'width_ratios': [1, 1, 1, 0.9]})

    # Panels 0..2: observed coculture vs additive, per medium.
    all_vals = []
    for df in all_pairs.values():
        all_vals += df['additive'].tolist()
        all_vals += df['coculture_total'].tolist()
    vmax = np.nanpercentile(all_vals, 99) * 1.1

    for ax, (med, label, color) in zip(axes[:3], MEDIA):
        df = all_pairs[med]
        ax.plot([0, vmax], [0, vmax], color='0.6', lw=0.8, ls='--')
        ax.scatter(df['additive'], df['coculture_total'],
                   s=14, color=color, alpha=0.75, edgecolor='white', lw=0.3)
        n_sub = int(df['subadditive'].sum())
        n = len(df)
        ax.text(0.04, 0.94, f'{label}\nsub-additive: {n_sub}/{n} ({100*n_sub/n:.0f}%)',
                transform=ax.transAxes, ha='left', va='top', fontsize=7.5)
        ax.set_xlabel('$M_i + M_j$  (monoculture sum, CFU)')
        ax.set_ylabel('$C_i + C_j$  (coculture total, CFU)')
        ax.set_xlim(0, vmax)
        ax.set_ylim(0, vmax)
        ax.set_aspect('equal', adjustable='box')

    # Panel 3: stacked fraction bars (% sub-additive per medium).
    ax = axes[3]
    labels = [m[1] for m in MEDIA]
    colors = [m[2] for m in MEDIA]
    fracs = []
    for (med, _, _) in MEDIA:
        df = all_pairs[med]
        fracs.append(df['subadditive'].mean())
    bars = ax.bar(labels, [100*f for f in fracs], color=colors, edgecolor='black', lw=0.4)
    for bar, f in zip(bars, fracs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{100*f:.0f}%', ha='center', va='bottom', fontsize=8)
    ax.set_ylabel('% pairs sub-additive')
    ax.set_ylim(0, 105)
    ax.set_xlabel('Medium')

    for ax in axes:
        ax.tick_params(axis='both', which='major', labelsize=7)

    plt.tight_layout()
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_path_base}.{ext}', bbox_inches='tight', dpi=200)
    print(f'  saved {out_path_base}.pdf')


def main():
    print('Loading pairwise colony-count data.')
    all_pairs = {}
    all_species = {}
    print('Per-medium summary:')
    for (med, label, _) in MEDIA:
        M, CC1, CC2 = load_medium(med)
        df = pair_stats(M, CC1, CC2)
        all_pairs[med] = df
        summarize(df, label)
        sdf = species_stats(M, CC1, CC2)
        all_species[med] = sdf
        summarize_species(sdf, label)

    out_base = os.path.join(SCRIPT_DIR, 'pair_additivity')
    make_figure(all_pairs, out_base)

    # Persist the per-pair numbers for reproducibility.
    for (med, _, _) in MEDIA:
        all_pairs[med].to_csv(os.path.join(SCRIPT_DIR, f'per_pair_{med}.csv'),
                              index=False)
        all_species[med].to_csv(os.path.join(SCRIPT_DIR, f'per_species_{med}.csv'),
                                index=False)


if __name__ == '__main__':
    main()
