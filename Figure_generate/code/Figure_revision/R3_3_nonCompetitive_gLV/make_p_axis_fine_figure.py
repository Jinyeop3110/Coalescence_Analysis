#!/usr/bin/env python
"""
Render the fine reciprocal-coupling p-axis sweep.

Output:
  ../R3_4_pair_coupling_fine.pdf
"""

import json
import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_JSON = os.path.join(SCRIPT_DIR, 'p_axis_fine_results.json')
CODE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, CODE_ROOT)
from COLORMAP import PHASE_DIAGRAM_COLORS  # noqa: E402

OUTCOMES = [
    ('Dominance', PHASE_DIAGRAM_COLORS['dominance']),
    ('Mixture', PHASE_DIAGRAM_COLORS['mixing']),
    ('Restructuring', PHASE_DIAGRAM_COLORS['restructuring']),
]
FACILITATIVE_COLOR = '#2A9D8F'
NONNEGATIVE_COLOR = '#BDBDBD'
NONNEGATIVE_EDGE = '0.30'

sns.set_style('ticks')
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def key_for(mu, p):
    if abs(p) < 1e-10:
        case = 'p0'
    else:
        prefix = 'ppos' if p > 0 else 'pneg'
        case = f'{prefix}{abs(p):.1f}'.replace('.', 'p')
    return f'mu={mu:.2f}_{case}'


def add_analytic_p_legend(ax):
    """Compact analytic directed-coefficient densities for representative p values."""
    inset = ax.inset_axes([0.11, 1.10, 0.81, 0.25], transform=ax.transAxes)
    reps = [(-1.0, -1), (0.0, 0), (1.0, 1)]
    y0s = [0.72, 0.42, 0.12]
    for (p, label), y0 in zip(reps, y0s):
        if p < 0:
            neg_weight = abs(p) / 2.0
            pos_weight = 1.0 - neg_weight
        else:
            neg_weight = 0.0
            pos_weight = 1.0
        if neg_weight > 0:
            inset.fill_between([-2, 0], [y0 + 0.18 * neg_weight, y0 + 0.18 * neg_weight],
                               [y0, y0], color=FACILITATIVE_COLOR, alpha=0.42)
        inset.fill_between([0, 2], [y0 + 0.18 * pos_weight, y0 + 0.18 * pos_weight],
                           [y0, y0], color=NONNEGATIVE_COLOR, alpha=0.55)
        inset.plot([-2, 0], [y0, y0], color='0.35', lw=0.4)
        inset.plot([0, 2], [y0, y0], color=NONNEGATIVE_EDGE, lw=0.4)
    inset.axvline(0, color='0.20', lw=0.65)
    inset.set_xlim(-2, 2.1)
    inset.set_ylim(0, 1.0)
    inset.set_xticks([-2, 0, 2])
    inset.set_yticks(y0s)
    inset.set_yticklabels(['$p=-1$', '$p=0$', '$p=+1$'])
    inset.set_xlabel(r'directed coefficient $\alpha_{ij}/\mu$',
                     fontsize=5.3, labelpad=0.4)
    inset.set_ylabel('example', fontsize=5.3, labelpad=2.4)
    inset.tick_params(axis='both', labelsize=5.0, length=1.4, pad=1.5)
    for spine in ('right', 'top'):
        inset.spines[spine].set_visible(False)
    inset.spines['left'].set_linewidth(0.45)
    inset.spines['bottom'].set_linewidth(0.45)


def main():
    with open(RESULTS_JSON) as fh:
        data = json.load(fh)
    records = data['results']
    mu_values = data['parameters']['MU_VALUES']
    p_values = data['parameters']['P_VALUES']

    fig, axes = plt.subplots(1, len(mu_values), figsize=(11.2, 4.35),
                             sharey=True, gridspec_kw={'wspace': 0.18})
    x = np.arange(len(p_values))

    for ax, mu in zip(axes, mu_values):
        bottoms = np.zeros(len(p_values))
        for outcome, color in OUTCOMES:
            heights = np.array([
                100.0 * records[key_for(mu, p)][f'frac_{outcome}']
                for p in p_values
            ])
            ax.bar(x, heights, bottom=bottoms, color=color,
                   edgecolor='black', lw=0.25, width=0.82,
                   label=outcome)
            bottoms += heights

        dom = np.array([
            100.0 * records[key_for(mu, p)]['frac_Dominance']
            for p in p_values
        ])
        ax.plot(x, dom, color='black', lw=1.0, marker='o', ms=2.7,
                label='Dominance fraction')
        ax.axvline(p_values.index(0.0), color='0.25', lw=0.8, ls=':')
        ax.set_title(f'$\\mu={mu:.2f}$', fontsize=9, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'{p:g}' for p in p_values], rotation=90)
        ax.set_xlabel('pair-coupling $p$')
        ax.set_ylim(0, 105)
        add_analytic_p_legend(ax)
        sns.despine(ax=ax)

    axes[0].set_ylabel('% outcomes')
    axes[-1].legend(loc='upper left', bbox_to_anchor=(1.02, 1.0),
                    frameon=False, fontsize=6.8, handlelength=1.2,
                    borderaxespad=0.0)
    fig.suptitle('Fine reciprocal pair-coupling sweep',
                 fontsize=10, y=1.33)

    out_base = os.path.join(SCRIPT_DIR, '..', 'R3_4_pair_coupling_fine')
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight', dpi=200)
    print(f'Saved {out_base}.pdf')


if __name__ == '__main__':
    main()
