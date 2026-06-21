#!/usr/bin/env python
"""
Render the R3-4 mean-vs-variance coefficient sweep.

Output:
  ../R3_4_mean_variance_grid.{pdf,png,svg}
"""

import json
import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_JSON = os.path.join(SCRIPT_DIR, 'mean_variance_grid_results.json')
CODE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, CODE_ROOT)
from COLORMAP import PHASE_DIAGRAM_COLORS  # noqa: E402

MEAN_VALUES = [0.00, 0.20, 0.40, 0.60, 0.80]
HALF_WIDTH_VALUES = [0.00, 0.20, 0.40, 0.60, 0.80]
OUTCOME_CMAPS = {
    'dominance': LinearSegmentedColormap.from_list(
        'dominance_outcome', ['#FFFFFF', PHASE_DIAGRAM_COLORS['dominance']]),
    'mixing': LinearSegmentedColormap.from_list(
        'mixture_outcome', ['#FFFFFF', PHASE_DIAGRAM_COLORS['mixing']]),
    'restructuring': LinearSegmentedColormap.from_list(
        'restructuring_outcome',
        ['#FFFFFF', PHASE_DIAGRAM_COLORS['restructuring']]),
}

sns.set_style('ticks')
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 7.5
mpl.rcParams['axes.linewidth'] = 0.5


def load_results():
    with open(RESULTS_JSON) as fh:
        return json.load(fh)


def matrix(records, field, scale=1.0):
    arr = np.zeros((len(HALF_WIDTH_VALUES), len(MEAN_VALUES)))
    for i, h in enumerate(HALF_WIDTH_VALUES):
        for j, mean_alpha in enumerate(MEAN_VALUES):
            key = f'mean={mean_alpha:.2f}_h={h:.2f}'
            arr[i, j] = scale * records[key][field]
    return arr


def annotate_percent(ax, values, fmt='{:.0f}'):
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            val = values[i, j]
            ax.text(j, i, fmt.format(val),
                    ha='center', va='center', fontsize=6.0,
                    color='black')


def add_negative_support_boundary(ax):
    # Negative coefficients appear for U[m-h,m+h] when h > m.
    x = np.arange(len(MEAN_VALUES))
    y = np.arange(len(HALF_WIDTH_VALUES))
    ax.plot(x, y, color='white', lw=1.4)
    ax.plot(x, y, color='black', lw=0.55, ls='--')


def draw_heatmap(ax, values, title, cmap, vmin=0, vmax=100, cbar=False):
    im = ax.imshow(values, origin='lower', aspect='equal', cmap=cmap,
                   vmin=vmin, vmax=vmax)
    annotate_percent(ax, values)
    add_negative_support_boundary(ax)
    ax.set_xticks(np.arange(len(MEAN_VALUES)))
    ax.set_yticks(np.arange(len(HALF_WIDTH_VALUES)))
    ax.set_xticklabels([f'{x:.1f}' for x in MEAN_VALUES], fontsize=6.5)
    ax.set_yticklabels(
        [f'{h / np.sqrt(3.0):.2f}' for h in HALF_WIDTH_VALUES],
        fontsize=6.5,
    )
    ax.set_xlabel('mean coefficient $m$', fontsize=7.5)
    ax.set_ylabel('coefficient std $h/\\sqrt{3}$', fontsize=7.5)
    ax.set_title(title, fontsize=8.5, fontweight='bold', loc='left')
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)
    if cbar:
        cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        cb.ax.tick_params(labelsize=6.0, length=2)
        cb.set_label('% outcomes', fontsize=6.5)
    return im


def draw_phi_heatmap(ax, values):
    plot_values = np.array(values, copy=True)
    plot_values[~np.isfinite(plot_values)] = 0.0
    im = ax.imshow(plot_values, origin='lower', aspect='equal', cmap='magma',
                   vmin=0, vmax=1)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            val = values[i, j]
            if np.isfinite(val):
                text = f'{val:.2f}'
                color = 'white' if val > 0.45 else 'black'
            else:
                text = 'n/a'
                color = 'white'
            ax.text(j, i, text, ha='center', va='center',
                    fontsize=6.0, color=color)
    add_negative_support_boundary(ax)
    ax.set_xticks(np.arange(len(MEAN_VALUES)))
    ax.set_yticks(np.arange(len(HALF_WIDTH_VALUES)))
    ax.set_xticklabels([f'{x:.1f}' for x in MEAN_VALUES], fontsize=6.5)
    ax.set_yticklabels(
        [f'{h / np.sqrt(3.0):.2f}' for h in HALF_WIDTH_VALUES],
        fontsize=6.5,
    )
    ax.set_xlabel('mean coefficient $m$', fontsize=7.5)
    ax.set_ylabel('coefficient std $h/\\sqrt{3}$', fontsize=7.5)
    ax.set_title('D  same-parent concordance $|\\phi|$',
                 fontsize=8.5, fontweight='bold', loc='left')
    ax.tick_params(length=0)
    cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.ax.tick_params(labelsize=6.0, length=2)
    cb.set_label('$|\\phi|$', fontsize=6.5)


def make_figure(data):
    records = data['results']
    dom = matrix(records, 'frac_Dominance', scale=100.0)
    mix = matrix(records, 'frac_Mixture', scale=100.0)
    res = matrix(records, 'frac_Restructuring', scale=100.0)
    phi = matrix(records, 'psc_phi', scale=1.0)

    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.0),
                             constrained_layout=True)
    draw_heatmap(axes[0, 0], dom, 'A  Dominance',
                 OUTCOME_CMAPS['dominance'], cbar=True)
    draw_heatmap(axes[0, 1], mix, 'B  Mixture',
                 OUTCOME_CMAPS['mixing'], cbar=True)
    draw_heatmap(axes[1, 0], res, 'C  Restructuring',
                 OUTCOME_CMAPS['restructuring'], cbar=True)
    draw_phi_heatmap(axes[1, 1], phi)

    fig.suptitle(
        'Mean-vs-variance sweep of interaction coefficients '
        '($\\alpha_{ij}\\sim U[m-h,m+h]$)',
        fontsize=10.5,
    )
    fig.text(
        0.5, -0.02,
        'Dashed diagonal marks $h=m$; above it, the coefficient distribution '
        'contains negative $\\alpha_{ij}$ values (positive ecological effects).',
        ha='center',
        fontsize=7.0,
    )

    out_base = os.path.join(SCRIPT_DIR, '..', 'R3_4_mean_variance_grid')
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight', dpi=250)
    print(f'Saved {out_base}.pdf')


def main():
    make_figure(load_results())


if __name__ == '__main__':
    main()
