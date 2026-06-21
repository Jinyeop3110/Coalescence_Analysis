"""
make_Q5_comparison_per_model.py
===============================

Q5 summary figure in the exact R3-4b convention: one subplot per model
(or model-variant), x-axis = interaction-strength level (weak / mid /
strong), stacked Dom/Mix/Res bars.

Layout (1 x 5):
    A  gLV baseline                         (mu = 0.3 / 0.6 / 0.9)
    B  Ratzke-Gore pH feedback              (interaction_strength = 1e-10 / 1e-9 / 3e-8)
    C  pH+LV hybrid (orig., continuous)     (tau = 0.3 / 0.6 / 1.0 at alpha=0.3)
    D  pH+LV hybrid (orig., binary)         (tau = 0.3 / 0.6 / 1.0 at alpha=0.3)
    E  pairwise selection correlation |phi|, 4 lines (one per variant)

Input : Q5_all_models_results.json
Output: Fig_Q5_three_models_per_model.{pdf,svg,png}
"""
from __future__ import annotations

import json
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

HERE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(HERE, "Q5_all_models_results.json")

sns.set_style("ticks")
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 7.5
mpl.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['text.usetex'] = False

OUTCOMES = [('frac_Dominance',    'Dominance',    '#1f77b4'),
            ('frac_Mixture',      'Mixture',      '#9ecae1'),
            ('frac_Restructuring','Restructuring','#d62728')]

STRENGTHS = ['weak', 'mid', 'strong']

# Per-variant knob values and JSON key templates
VARIANTS = [
    ('gLV',          'A  gLV baseline',
     '#4e79a7',
     {'weak': 'gLV_mu=0.30', 'mid': 'gLV_mu=0.60', 'strong': 'gLV_mu=0.90'},
     {'weak': r'$\mu$=0.3', 'mid': r'$\mu$=0.6', 'strong': r'$\mu$=0.9'}),
    ('pH',           'B  Ratzke--Gore pH feedback',
     '#f28e2b',
     {'weak': 'pH_tau=1.00', 'mid': 'pH_tau=10.00', 'strong': 'pH_tau=300.00'},
     {'weak': r'$c_{\max}$=1e-10', 'mid': r'$c_{\max}$=1e-9', 'strong': r'$c_{\max}$=3e-8'}),
    ('hyb_cont',     r'C  pH+LV hybrid (orig., continuous)',
     '#59a14f',
     {'weak': 'hybrid_orig_continuous_tau=0.30',
      'mid':  'hybrid_orig_continuous_tau=0.60',
      'strong': 'hybrid_orig_continuous_tau=1.00'},
     {'weak': r'$\tau$=0.3', 'mid': r'$\tau$=0.6', 'strong': r'$\tau$=1.0'}),
    ('hyb_bin',      r'D  pH+LV hybrid (orig., binary)',
     '#2ca02c',
     {'weak': 'hybrid_orig_binary_tau=0.30',
      'mid':  'hybrid_orig_binary_tau=0.60',
      'strong': 'hybrid_orig_binary_tau=1.00'},
     {'weak': r'$\tau$=0.3', 'mid': r'$\tau$=0.6', 'strong': r'$\tau$=1.0'}),
]


def panel_stacked(ax, results, keys_per_strength, knob_labels, title):
    """Per-model panel: 3 stacked bars at weak/mid/strong."""
    x = np.arange(len(STRENGTHS))
    bottoms = np.zeros(len(STRENGTHS))
    for okey, oname, ocolor in OUTCOMES:
        heights = np.array([
            (results[keys_per_strength[s]][okey] or 0.0) * 100.0
            for s in STRENGTHS
        ])
        ax.bar(x, heights, bottom=bottoms, color=ocolor,
               edgecolor='black', lw=0.3, width=0.72, label=oname)
        if okey == 'frac_Dominance':
            for xi, h in zip(x, heights):
                ax.text(xi, h / 2 if h > 8 else h + 2, f'{h:.0f}%',
                        ha='center', va='center' if h > 8 else 'bottom',
                        fontsize=7,
                        color='white' if h > 8 else 'black',
                        fontweight='bold')
        bottoms += heights
    # two-line ticks: "weak\n(mu=0.3)" etc.
    tick_labels = [f'{s}\n{knob_labels[s]}' for s in STRENGTHS]
    ax.set_xticks(x)
    ax.set_xticklabels(tick_labels, fontsize=6.8)
    ax.set_ylim(0, 105)
    ax.set_ylabel('% outcomes')
    ax.set_xlabel('interaction-strength level')
    ax.set_title(title, fontsize=8.5, fontweight='bold', loc='left')
    sns.despine(ax=ax)


def panel_phi(ax, results):
    x = np.arange(len(STRENGTHS))
    for (vkey, _, vcolor, keys_per_strength, _) in VARIANTS:
        vals = []
        for s in STRENGTHS:
            v = results[keys_per_strength[s]].get('psc_phi', float('nan'))
            vals.append(v if v is not None else float('nan'))
        label = {'gLV':'gLV', 'pH':'pH-feedback',
                 'hyb_cont':'hybrid (cont.)',
                 'hyb_bin':'hybrid (bin.)'}[vkey]
        marker = {'gLV':'o', 'pH':'s', 'hyb_cont':'^', 'hyb_bin':'D'}[vkey]
        ax.plot(x, vals, marker=marker, color=vcolor,
                markersize=6, linewidth=1.3, label=label)
    ax.set_xticks(x)
    ax.set_xticklabels(STRENGTHS, fontsize=6.8)
    ax.set_xlabel('interaction-strength level')
    ax.set_ylabel(r'$|\phi|$ (origin$\to$persistence)')
    ax.set_ylim(0, 1.0)
    ax.legend(loc='upper left', frameon=False, fontsize=6.5, handlelength=1.6)
    ax.set_title('E  Pairwise selection correlation',
                 fontsize=8.5, fontweight='bold', loc='left')
    sns.despine(ax=ax)


def main():
    with open(JSON_PATH) as f:
        data = json.load(f)
    results = data['results']

    fig, axes = plt.subplots(1, 5, figsize=(15.0, 3.5),
                             gridspec_kw={'wspace': 0.45})

    for col, (vkey, title, _, keys_per_strength, knob_labels) in enumerate(VARIANTS):
        ax = axes[col]
        panel_stacked(ax, results, keys_per_strength, knob_labels, title)
        if col == 0:
            ax.legend(loc='upper right', frameon=False,
                      fontsize=6.2, handlelength=1.2)

    panel_phi(axes[4], results)

    for ax in axes:
        ax.tick_params(axis='both', which='major', labelsize=6.5)

    fig.suptitle('Q5: three models (four variants) at matched interaction-strength levels',
                 fontsize=10, y=1.02)

    out_base = os.path.join(HERE, 'Fig_Q5_three_models_per_model')
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f'Wrote {out_base}.pdf')


if __name__ == "__main__":
    main()
