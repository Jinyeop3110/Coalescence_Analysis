#!/usr/bin/env python
"""
Response Fig. R3-4 is produced as TWO separate figures, since the
experimental panels and simulation panels convey different messages.

Figure A (R3_4_experiment.{pdf,png,svg}) -- experimental suppression:
  A: per-medium scatter C_i vs M_i for each species-in-pair, Nutr-
  B: per-medium scatter C_i vs M_i for each species-in-pair, Base
  C: per-medium scatter C_i vs M_i for each species-in-pair, Nutr+
  D: bar summary of % species observations suppressed across media

Figure B (R3_4_simulation.{pdf,png,svg}) -- gLV regime phase diagrams:
  Three subplots (one per interaction regime: comp / exploit / coop),
  each an interaction-strength-dependent phase diagram (stacked Dom/Mix/
  Restructuring across mu), styled after the right panel of
  Fig_Q5_phase_gLV.
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
CODE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
DATA_PATH = os.path.join(ROOT, 'Postprocessed',
                         'PairwiseColonyCountings_processed_230915.xlsx')
SIM_JSON = os.path.join(SCRIPT_DIR, '..', 'R3_3_nonCompetitive_gLV',
                         'p_axis_results.json')

sys.path.insert(0, CODE_ROOT)
sys.path.insert(0, SCRIPT_DIR)
from analyze_pair_additivity import load_medium, pair_stats, species_stats
from COLORMAP import PHASE_DIAGRAM_COLORS

MEDIA = [('LN', 'Nutr$-$', '#6baed6'),
         ('MN', 'Base',    '#2b83ba'),
         ('HN', 'Nutr$+$', '#08306b')]
MU_VALUES = [0.30, 0.60, 0.80]
# Panel order: monotonic reciprocal-coupling axis, p=-1 to p=+1.
# (case_key, panel title for Q5-summary style "A  <name> (p=...)").
P_VALUES = [
    ('pneg1',  -1.0, 'antisymmetric exploitation ($p=-1$)'),
    ('pneg05', -0.5, 'antisymmetric exploitation ($p=-0.5$)'),
    ('p0',      0.0, 'i.i.d. baseline ($p=0$)'),
    ('ppos05', +0.5, 'symmetric competition ($p=+0.5$)'),
    ('ppos1',  +1.0, 'symmetric competition ($p=+1$)'),
]
PANEL_LETTERS = ['A', 'B', 'C', 'D', 'E']
OUTCOMES = [('Dominance',    PHASE_DIAGRAM_COLORS['dominance']),
            ('Mixture',      PHASE_DIAGRAM_COLORS['mixing']),
            ('Restructuring',PHASE_DIAGRAM_COLORS['restructuring'])]
FACILITATIVE_COLOR = '#2A9D8F'
NONNEGATIVE_COLOR = '#BDBDBD'
NONNEGATIVE_EDGE = '0.30'

sns.set_style('ticks')
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 7.5
mpl.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def load_experiment():
    pairs_by_med = {}
    species_by_med = {}
    for (med, _, _) in MEDIA:
        M, CC1, CC2 = load_medium(med)
        pairs_by_med[med] = pair_stats(M, CC1, CC2)
        species_by_med[med] = species_stats(M, CC1, CC2)
    return pairs_by_med, species_by_med


def load_sim():
    with open(SIM_JSON) as fh:
        data = json.load(fh)
    return data['results']


def add_analytic_p_histogram(ax, p):
    """Draw the analytic directed-coefficient density of alpha/mu for this p."""
    inset = ax.inset_axes([0.13, 1.10, 0.79, 0.26], transform=ax.transAxes)
    if p < 0:
        neg_weight = abs(p) / 2.0
        pos_weight = 1.0 - neg_weight
    else:
        neg_weight = 0.0
        pos_weight = 1.0

    max_density = 0.0
    if neg_weight > 0:
        neg_density = neg_weight / 2.0
        max_density = max(max_density, neg_density)
        inset.fill_between([-2, 0], [neg_density, neg_density], [0, 0],
                           color=FACILITATIVE_COLOR, alpha=0.42,
                           step='post')
        inset.plot([-2, -2, 0, 0], [0, neg_density, neg_density, 0],
                   color=FACILITATIVE_COLOR, lw=0.9)
        inset.text(-1.0, neg_density * 0.55, r'$\alpha<0$',
                   ha='center', va='center', fontsize=5.0)
    pos_density = pos_weight / 2.0
    max_density = max(max_density, pos_density)
    inset.fill_between([0, 2], [pos_density, pos_density], [0, 0],
                       color=NONNEGATIVE_COLOR, alpha=0.55, step='post')
    inset.plot([0, 0, 2, 2], [0, pos_density, pos_density, 0],
               color=NONNEGATIVE_EDGE, lw=0.9)
    inset.text(1.0, pos_density * 0.55, r'$\alpha\geq0$',
               ha='center', va='center', fontsize=5.0)
    inset.axvline(0, color='0.20', lw=0.65)
    inset.set_xlim(-2.0, 2.0)
    inset.set_ylim(0, 0.62)
    inset.set_xticks([-2, 0, 2])
    inset.set_yticks([0, max_density])
    inset.set_yticklabels(['0', f'{max_density:.2f}'])
    inset.set_xlabel(r'directed coefficient $\alpha_{ij}/\mu$',
                     fontsize=5.3, labelpad=0.4)
    inset.set_ylabel('density', fontsize=5.3, labelpad=2.4)
    inset.tick_params(axis='both', labelsize=5.0, length=1.4, pad=1.5)
    for spine in ('right', 'top'):
        inset.spines[spine].set_visible(False)
    inset.spines['left'].set_linewidth(0.45)
    inset.spines['bottom'].set_linewidth(0.45)


def panel_scatter(ax, df, label, color):
    vmax = np.nanpercentile(
        np.concatenate([df['mono'], df['coculture']]), 99) * 1.1
    ax.plot([0, vmax], [0, vmax], color='0.55', lw=0.8, ls='--')
    ax.fill_between([0, vmax], [0, vmax], [0, 0], color='#d9d9d9',
                    alpha=0.25, lw=0)
    ax.scatter(df['mono'], df['coculture'],
               s=14, color=color, alpha=0.75,
               edgecolor='white', lw=0.3)
    n = len(df)
    n_sup = int(df['suppressed'].sum())
    median_rel = df['rel_yield'].median()
    ax.text(0.04, 0.96,
            f'{label}\nsuppressed: {100*n_sup/n:.0f}%\nmedian $C_i/M_i$: {median_rel:.2f}',
            transform=ax.transAxes, ha='left', va='top', fontsize=7)
    ax.text(0.96, 0.06, 'below diagonal:\nsuppressed in coculture',
            transform=ax.transAxes, ha='right', va='bottom', fontsize=6.5,
            color='0.25')
    ax.set_xlabel('$M_i$ in monoculture (CFU)')
    ax.set_ylabel('$C_i$ in coculture (CFU)')
    ax.set_xlim(0, vmax)
    ax.set_ylim(0, vmax)
    ax.set_aspect('equal', adjustable='box')


def panel_bar_exp(ax, pairs_by_med, species_by_med):
    x = np.arange(len(MEDIA))
    sub = [species_by_med[m[0]]['suppressed'].mean() * 100 for m in MEDIA]
    bars = ax.bar(x, sub, 0.55, color=[m[2] for m in MEDIA],
                  edgecolor='black', lw=0.3)
    for bar, v in zip(bars, sub):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f'{v:.0f}', ha='center', va='bottom', fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels([m[1] for m in MEDIA])
    ax.set_ylabel('% species observations suppressed')
    ax.set_ylim(0, 115)


def panel_phase_by_p(ax, sim, case_key, p, title):
    """Stacked Dominance/Mixture/Restructuring fractions across mu for one p
    value. One panel per p (five panels total). Mirrors the Q5-summary
    (Fig_Q5_three_models_per_model) layout: bar title at top-left, mu on
    the x-axis, stacked Dom/Mix/Res bars."""
    x = np.arange(len(MU_VALUES))
    bottoms = np.zeros(len(MU_VALUES))
    for outcome, color in OUTCOMES:
        heights = []
        for mu in MU_VALUES:
            key = f'mu={mu:.2f}_{case_key}'
            rec = sim.get(key)
            if rec is None or rec.get('n_events', 0) == 0:
                heights.append(0.0)
            else:
                heights.append(100 * rec[f'frac_{outcome}'])
        heights = np.array(heights)
        ax.bar(x, heights, bottom=bottoms, color=color, edgecolor='black',
               lw=0.3, label=outcome, width=0.72)
        if outcome == 'Dominance':
            for xi, h in zip(x, heights):
                ax.text(xi, h / 2 if h > 8 else h + 2,
                        f'{h:.0f}%',
                        ha='center',
                        va='center' if h > 8 else 'bottom',
                        fontsize=7,
                        color='white' if h > 8 else 'black',
                        fontweight='bold')
        bottoms += heights
    ax.set_xticks(x)
    ax.set_xticklabels([f'$\\mu$={mu:.2f}' for mu in MU_VALUES], fontsize=6.8)
    ax.set_xlabel('interaction strength $\\mu$', fontsize=7.5)
    ax.set_ylim(0, 105)
    ax.set_ylabel('% outcomes', fontsize=7.5)
    ax.set_title(title, fontsize=8.5, fontweight='bold', loc='left')
    sns.despine(ax=ax)
    add_analytic_p_histogram(ax, p)


def add_letters(fig, axes, offset_x=-0.18, offset_y=1.08, size=10):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for idx, ax in enumerate(axes):
        ax.text(offset_x, offset_y, letters[idx], transform=ax.transAxes,
                fontsize=size, fontweight='bold', ha='right', va='bottom')


def make_figure_experiment(pairs, species):
    fig = plt.figure(figsize=(10.5, 2.8))
    gs = fig.add_gridspec(1, 4, wspace=0.45, width_ratios=[1, 1, 1, 1])

    axes = []
    for col, (med, label, color) in enumerate(MEDIA):
        ax = fig.add_subplot(gs[0, col])
        panel_scatter(ax, species[med], label, color)
        axes.append(ax)
    ax_bar = fig.add_subplot(gs[0, 3])
    panel_bar_exp(ax_bar, pairs, species)
    axes.append(ax_bar)

    add_letters(fig, axes)
    for ax in fig.axes:
        ax.tick_params(axis='both', which='major', labelsize=6.5)

    out_base = os.path.join(SCRIPT_DIR, '..', 'R3_4_experiment')
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f'Saved {out_base}.pdf')


def make_figure_simulation(sim):
    fig, axes = plt.subplots(1, 5, figsize=(15.0, 4.2),
                             gridspec_kw={'wspace': 0.45})

    for col, (case_key, p, name) in enumerate(P_VALUES):
        ax = axes[col]
        panel_phase_by_p(ax, sim, case_key, p,
                          f'{PANEL_LETTERS[col]}  {name}')

    axes[-1].legend(loc='upper left', bbox_to_anchor=(1.02, 1.0),
                    frameon=False, fontsize=6.2, handlelength=1.2,
                    borderaxespad=0.0)

    for ax in axes:
        ax.tick_params(axis='both', which='major', labelsize=6.5)

    out_base = os.path.join(SCRIPT_DIR, '..', 'R3_4_simulation')
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f'Saved {out_base}.pdf')


def main():
    pairs, species = load_experiment()
    sim = load_sim()
    make_figure_experiment(pairs, species)
    make_figure_simulation(sim)


if __name__ == '__main__':
    main()
