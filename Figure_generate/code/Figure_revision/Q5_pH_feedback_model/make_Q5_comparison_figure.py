"""
make_Q5_comparison_figure.py
============================

Render the 3-model comparison figure for internal memo Q5, styled to match
the paper's convention for model-variant figures (cf.\
R3_3_pair_additivity/make_R3_3_figure.py row 2, which pairs per-mu stacked
outcome bars + a per-variant |phi| bar panel).

Layout: 1 x 4
    A, B, C : one panel per *interaction-strength level*
              (weak / mid / strong).  Within each panel, stacked bars
              per model (gLV / pH-feedback / pH+LV hybrid) showing
              % Dominance / Mixture / Restructuring.
    D       : |phi| grouped bar chart; x-axis is the strength level,
              grouped bars one per model.

Convention matched to R3_3:
    - Dominance / Mixture / Restructuring colors identical to R3_3.
    - Model colors one each (gLV/pH/hybrid), same legend-placement style.
    - Panel letters bold upper-left.
    - Arial 7.5, ylim 0-105 for stacks, 0-1 for |phi|.

The three "strength levels" map to model knobs as follows:
    weak   : gLV mu=0.3 ; pH tau=0.5 ; hybrid (alpha=0.3, tau=0.3, binary)
    mid    : gLV mu=0.6 ; pH tau=2.0 ; hybrid (alpha=0.3, tau=0.6, binary)
    strong : gLV mu=0.9 ; pH tau=5.0 ; hybrid (alpha=0.3, tau=1.0, binary)
For the hybrid we fix alpha=0.3 and use the original-form (gLV_pH_set1
port, binary species-preference mode) so that "hybrid strength" comes
entirely from the pH-coupling knob tau.  These are approximate
"matched" points chosen so each model shows its full dynamic range
across the three panels.  The matching is qualitative, not a
tension-to-mu calibration, and this is flagged in the memo Q5 caveat
list.

Input : Q5_all_models_results.json
Output: Fig_Q5_three_models.{pdf,svg,png}
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

# R3_3 palette (keep identical so figures compose visually across the memo)
OUTCOMES = [('frac_Dominance',    'Dominance',    '#1f77b4'),
            ('frac_Mixture',      'Mixture',      '#9ecae1'),
            ('frac_Restructuring','Restructuring','#d62728')]

MODELS = [('gLV',       'gLV',                   '#4e79a7'),
          ('pH',        'pH-feedback',           '#f28e2b'),
          ('hybrid',    'pH+LV hybrid (orig.)',  '#59a14f')]

STRENGTH_LEVELS = [
    ('weak',   'weak',   {'gLV_mu': 0.3, 'pH_tau': 0.5,
                           'hybrid_tau': 0.3}),
    ('mid',    'mid',    {'gLV_mu': 0.6, 'pH_tau': 2.0,
                           'hybrid_tau': 0.6}),
    ('strong', 'strong', {'gLV_mu': 0.9, 'pH_tau': 5.0,
                           'hybrid_tau': 1.0}),
]


def load_payload():
    with open(JSON_PATH) as f:
        return json.load(f)


def key_for(model, spec):
    """Return the JSON key for a given model + strength spec."""
    if model == 'gLV':
        return f"gLV_mu={spec['gLV_mu']:.2f}"
    if model == 'pH':
        return f"pH_tau={spec['pH_tau']:.2f}"
    if model == 'hybrid':
        return f"hybrid_orig_binary_tau={spec['hybrid_tau']:.2f}"
    raise ValueError(model)


def panel_stacked(ax, results, spec, title):
    """Per-strength panel: stacked Dom/Mix/Res bars, one per model."""
    x = np.arange(len(MODELS))
    bottoms = np.zeros(len(MODELS))
    for okey, oname, ocolor in OUTCOMES:
        heights = np.array([
            results[key_for(mk, spec)][okey] * 100.0
            for (mk, _, _) in MODELS
        ])
        ax.bar(x, heights, bottom=bottoms, color=ocolor,
               edgecolor='black', lw=0.3, width=0.72, label=oname)
        # annotate Dominance height at the top of each stacked bar's Dom segment
        if okey == 'frac_Dominance':
            for xi, h in zip(x, heights):
                ax.text(xi, h / 2 if h > 8 else h + 2,
                        f'{h:.0f}%',
                        ha='center',
                        va='center' if h > 8 else 'bottom',
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


def panel_phi(ax, results):
    """|phi| grouped bar panel; x = strength, colored groups = models."""
    x = np.arange(len(STRENGTH_LEVELS))
    width = 0.26
    for k, (mk, mname, mcolor) in enumerate(MODELS):
        vals = []
        for (_, _, spec) in STRENGTH_LEVELS:
            v = results[key_for(mk, spec)].get('psc_phi', float('nan'))
            vals.append(v)
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
    data = load_payload()
    results = data['results']

    # Match R3_3 row-2 footprint (10.5 in wide x ~5 in tall) for the
    # 1x4 stacked-variants + phi-bars composition.
    fig, axes = plt.subplots(1, 4, figsize=(10.5, 4.6),
                              gridspec_kw={'wspace': 0.55})

    for col, (lkey, lname, spec) in enumerate(STRENGTH_LEVELS):
        ax = axes[col]
        sub_mu = spec['gLV_mu']
        sub_tau = spec['pH_tau']
        title = f"{lname}: $\\mu$={sub_mu:.1f}, $\\tau$={sub_tau:.1f}"
        panel_stacked(axes[col], results, spec, title)
        if col == 0:
            axes[col].legend(loc='upper right', frameon=False,
                              fontsize=6.2, handlelength=1.2)

    panel_phi(axes[3], results)

    # Panel letters (R3_3 convention: bold top-left, offset to margin)
    letters = ['A', 'B', 'C', 'D']
    for idx, ax in enumerate(axes):
        ax.text(-0.18, 1.08, letters[idx], transform=ax.transAxes,
                fontsize=10, fontweight='bold', ha='right', va='bottom')

    for ax in axes:
        ax.tick_params(axis='both', which='major', labelsize=6.5)

    fig.suptitle('Q5: three models at matched interaction-strength levels',
                 fontsize=9.5, y=1.02)

    out_base = os.path.join(HERE, 'Fig_Q5_three_models')
    for ext in ('pdf', 'png', 'svg'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight', dpi=200)
    plt.close(fig)
    print(f'Wrote {out_base}.pdf (R3_3-style layout)')


if __name__ == "__main__":
    main()
