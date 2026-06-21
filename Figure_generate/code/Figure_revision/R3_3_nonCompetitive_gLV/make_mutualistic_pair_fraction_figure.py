#!/usr/bin/env python
"""
Render R3-4 mutualistic-pair fraction sweep.

Output:
  ../R3_4_mutualistic_pair_fraction.{pdf,png,svg}
"""

import json
import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_JSON = os.path.join(
    SCRIPT_DIR, 'mutualistic_pair_fraction_results.json')
CODE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, CODE_ROOT)
from COLORMAP import PHASE_DIAGRAM_COLORS  # noqa: E402

MU_VALUES = [0.30, 0.60, 0.80]
MUTUAL_PAIR_FRACTIONS = [0.00, 0.10, 0.20, 0.30, 0.40]
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
mpl.rcParams['font.size'] = 7.5
mpl.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def load_results():
    with open(RESULTS_JSON) as fh:
        return json.load(fh)


def add_pair_type_strip(ax, mutual_fraction):
    """Show the two pair classes on the alpha/mu axis."""
    inset = ax.inset_axes([0.13, 1.10, 0.79, 0.26], transform=ax.transAxes)
    comp_weight = 1.0 - mutual_fraction
    mut_weight = mutual_fraction
    max_density = comp_weight / 2.0

    if mut_weight > 0:
        mut_density = mut_weight / 0.2
        max_density = max(max_density, mut_density)
        inset.fill_between([-0.2, 0], [mut_density, mut_density], [0, 0],
                           color=FACILITATIVE_COLOR, alpha=0.42,
                           step='post')
        inset.plot([-0.2, -0.2, 0, 0],
                   [0, mut_density, mut_density, 0],
                   color=FACILITATIVE_COLOR, lw=0.9)
        inset.text(-0.1, mut_density * 0.55, r'$\alpha<0$',
                   ha='center', va='center', fontsize=5.0)
    comp_density = comp_weight / 2.0
    inset.fill_between([0, 2], [comp_density, comp_density], [0, 0],
                       color=NONNEGATIVE_COLOR, alpha=0.55, step='post')
    inset.plot([0, 0, 2, 2],
               [0, comp_density, comp_density, 0],
               color=NONNEGATIVE_EDGE, lw=0.9)
    if comp_density > 0:
        inset.text(1.0, comp_density * 0.55, r'$\alpha\geq0$',
                   ha='center', va='center', fontsize=5.0)
    inset.axvline(0, color='0.20', lw=0.65)
    inset.set_xlim(-0.35, 2.05)
    inset.set_ylim(0, max(0.6, max_density * 1.18))
    inset.set_xticks([-0.2, 0, 1, 2])
    inset.set_xticklabels(['-0.2', '0', '1', '2'])
    inset.set_yticks([0, max_density])
    inset.set_yticklabels(['0', f'{max_density:.2f}'])
    inset.set_xlabel(r'normalized coefficient $\alpha_{ij}/\mu$',
                     fontsize=5.3, labelpad=0.4)
    inset.set_ylabel('density', fontsize=5.3, labelpad=2.4)
    inset.tick_params(axis='both', labelsize=5.0, length=1.4, pad=1.5)
    for spine in ('right', 'top'):
        inset.spines[spine].set_visible(False)
    inset.spines['left'].set_linewidth(0.45)
    inset.spines['bottom'].set_linewidth(0.45)


def panel_phase_by_q(ax, records, mutual_fraction, panel_letter):
    x = np.arange(len(MU_VALUES))
    bottoms = np.zeros(len(MU_VALUES))
    title = (f'{panel_letter}  no mutualistic pairs'
             if mutual_fraction == 0
             else f'{panel_letter}  {100 * mutual_fraction:.0f}% mutualistic pairs')

    for outcome, color in OUTCOMES:
        heights = []
        for mu in MU_VALUES:
            key = f'mu={mu:.2f}_q={mutual_fraction:.2f}'
            rec = records[key]
            heights.append(100.0 * rec[f'frac_{outcome}'])
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

    ax.text(0.02, 0.98, f'$q$={100 * mutual_fraction:.0f}%',
            transform=ax.transAxes, ha='left', va='top', fontsize=6.7)
    ax.set_xticks(x)
    ax.set_xticklabels([f'$\\mu$={mu:.2f}' for mu in MU_VALUES], fontsize=6.8)
    ax.set_xlabel('mean competitive coefficient $\\mu$', fontsize=7.5)
    ax.set_ylim(0, 105)
    ax.set_ylabel('% outcomes', fontsize=7.5)
    ax.set_title(title, fontsize=8.5, fontweight='bold', loc='left')
    sns.despine(ax=ax)
    add_pair_type_strip(ax, mutual_fraction)


def make_figure(data):
    records = data['results']
    gamma = data['parameters']['GAMMA']
    f_mutual = data['parameters']['F_MUTUAL']
    fig, axes = plt.subplots(
        1, len(MUTUAL_PAIR_FRACTIONS), figsize=(15.0, 4.35),
        gridspec_kw={'wspace': 0.45})

    for i, (ax, mutual_fraction) in enumerate(
            zip(axes, MUTUAL_PAIR_FRACTIONS)):
        panel_phase_by_q(ax, records, mutual_fraction, chr(ord('A') + i))

    axes[-1].legend(loc='upper left', bbox_to_anchor=(1.02, 1.0),
                    frameon=False, fontsize=6.2, handlelength=1.2,
                    borderaxespad=0.0)

    fig.suptitle(
        f'Weak mutualistic-pair sweep '
        f'($\\alpha_{{ij}},\\alpha_{{ji}}\\sim U[-{f_mutual:.1f}\\mu,0]$; '
        f'$\\gamma={gamma:.2f}$)',
        fontsize=10,
        y=1.33,
    )

    for ax in axes:
        ax.tick_params(axis='both', which='major', labelsize=6.5)

    out_base = os.path.join(SCRIPT_DIR, '..',
                            'R3_4_mutualistic_pair_fraction')
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight', dpi=200)
    print(f'Saved {out_base}.pdf')


def main():
    data = load_results()
    make_figure(data)


if __name__ == '__main__':
    main()
