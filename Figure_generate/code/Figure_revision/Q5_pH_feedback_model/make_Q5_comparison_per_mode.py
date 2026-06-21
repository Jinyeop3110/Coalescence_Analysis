"""
make_Q5_comparison_per_mode.py
==============================

Variant of make_Q5_comparison_figure.py with one row per original-hybrid
mode (continuous, binary), matched to the Response-Fig-R3-4b convention
(subplot per condition).

Layout (2 rows x 4 cols):
    Row 1 (continuous): A/B/C stacked Dom/Mix/Res at weak/mid/strong,
                        D grouped |phi| bars.  Hybrid = continuous.
    Row 2 (binary)    : E/F/G stacked Dom/Mix/Res at weak/mid/strong,
                        H grouped |phi| bars.  Hybrid = binary.

Strength mapping:
    gLV    : mu in {0.3, 0.6, 0.9}
    pH     : tau in {0.5, 2.0, 5.0}
    hybrid : alpha=0.3 fixed, tau in {0.3, 0.6, 1.0}  (mode differs by row)

Input : Q5_all_models_results.json  (must contain hybrid_orig_{mode}_tau=*)
Output: Fig_Q5_three_models_per_mode.{pdf,svg,png}
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

MODELS = [('gLV',       'gLV',           '#4e79a7'),
          ('pH',        'pH-feedback',   '#f28e2b'),
          ('hybrid',    'hybrid (orig.)','#59a14f')]

STRENGTH_LEVELS = [
    ('weak',   'weak',   {'gLV_mu': 0.3, 'pH_tau': 0.5, 'hybrid_tau': 0.3}),
    ('mid',    'mid',    {'gLV_mu': 0.6, 'pH_tau': 2.0, 'hybrid_tau': 0.6}),
    ('strong', 'strong', {'gLV_mu': 0.9, 'pH_tau': 5.0, 'hybrid_tau': 1.0}),
]


def key_for(model, spec, mode):
    if model == 'gLV':
        return f"gLV_mu={spec['gLV_mu']:.2f}"
    if model == 'pH':
        return f"pH_tau={spec['pH_tau']:.2f}"
    if model == 'hybrid':
        return f"hybrid_orig_{mode}_tau={spec['hybrid_tau']:.2f}"
    raise ValueError(model)


def panel_stacked(ax, results, spec, title, mode):
    x = np.arange(len(MODELS))
    bottoms = np.zeros(len(MODELS))
    for okey, oname, ocolor in OUTCOMES:
        heights = np.array([
            (results[key_for(mk, spec, mode)][okey] or 0.0) * 100.0
            for (mk, _, _) in MODELS
        ])
        ax.bar(x, heights, bottom=bottoms, color=ocolor,
               edgecolor='black', lw=0.3, width=0.72, label=oname)
        if okey == 'frac_Dominance':
            for xi, h in zip(x, heights):
                ax.text(xi, h / 2 if h > 8 else h + 2, f'{h:.0f}%',
                        ha='center', va='center' if h > 8 else 'bottom',
                        fontsize=6.5,
                        color='white' if h > 8 else 'black',
                        fontweight='bold')
        bottoms += heights
    ax.set_xticks(x)
    ax.set_xticklabels([m[1] for m in MODELS], rotation=20, ha='right',
                       fontsize=6.8)
    ax.set_ylim(0, 105)
    ax.set_ylabel('% outcomes')
    ax.set_title(title, fontsize=8)
    sns.despine(ax=ax)


def panel_phi(ax, results, mode):
    x = np.arange(len(STRENGTH_LEVELS))
    width = 0.26
    for k, (mk, mname, mcolor) in enumerate(MODELS):
        vals = []
        for (_, _, spec) in STRENGTH_LEVELS:
            v = results[key_for(mk, spec, mode)].get('psc_phi', float('nan'))
            vals.append(v if v is not None else float('nan'))
        ax.bar(x + (k - 1) * width, vals, width,
               color=mcolor, edgecolor='black', lw=0.3, label=mname)
        for xi, v in zip(x + (k - 1) * width, vals):
            if np.isfinite(v):
                ax.text(xi, v + 0.02, f'{v:.2f}',
                        ha='center', va='bottom', fontsize=6.2)
    ax.set_xticks(x)
    ax.set_xticklabels([lname for (_, lname, _) in STRENGTH_LEVELS])
    ax.set_xlabel('interaction-strength level')
    ax.set_ylabel(r'$|\phi|$ (origin$\to$persistence)')
    ax.set_ylim(0, 1.1)
    ax.legend(loc='upper left', frameon=False, fontsize=6.5, handlelength=1.2)
    sns.despine(ax=ax)


def main():
    with open(JSON_PATH) as f:
        data = json.load(f)
    results = data['results']

    fig, axes = plt.subplots(2, 4, figsize=(12.0, 8.0),
                             gridspec_kw={'wspace': 0.55, 'hspace': 0.55})

    row_mode = [('continuous', 'A-D', 'continuous hybrid'),
                ('binary',     'E-H', 'binary hybrid')]
    letters_row = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H']]

    for r, (mode, _, row_label) in enumerate(row_mode):
        for col, (lkey, lname, spec) in enumerate(STRENGTH_LEVELS):
            ax = axes[r, col]
            sub_mu = spec['gLV_mu']
            sub_tau_pH = spec['pH_tau']
            sub_tau_hyb = spec['hybrid_tau']
            title = (f"{lname}: $\\mu$={sub_mu:.1f}, "
                     f"$\\tau_{{pH}}$={sub_tau_pH:.1f}, "
                     f"$\\tau_{{hyb}}$={sub_tau_hyb:.1f}")
            panel_stacked(ax, results, spec, title, mode)
            if col == 0 and r == 0:
                ax.legend(loc='upper right', frameon=False,
                          fontsize=6.2, handlelength=1.2)
        panel_phi(axes[r, 3], results, mode)

        # Row-level label on the far left
        axes[r, 0].text(-0.55, 0.5, row_label,
                        transform=axes[r, 0].transAxes,
                        fontsize=10, fontweight='bold',
                        ha='center', va='center', rotation=90)

    for r in range(2):
        for c in range(4):
            axes[r, c].text(-0.18, 1.10, letters_row[r][c],
                            transform=axes[r, c].transAxes,
                            fontsize=10, fontweight='bold',
                            ha='right', va='bottom')
            axes[r, c].tick_params(axis='both', which='major', labelsize=6.5)

    fig.suptitle('Q5: three models at matched strength, per hybrid mode',
                 fontsize=10, y=0.995)

    out_base = os.path.join(HERE, 'Fig_Q5_three_models_per_mode')
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f'Wrote {out_base}.pdf')


if __name__ == "__main__":
    main()
