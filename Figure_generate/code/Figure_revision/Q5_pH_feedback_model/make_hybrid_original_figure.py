"""
make_hybrid_original_figure.py
==============================

Render hybrid_original_results.json into a 1x2 figure:
    A  Outcome-class frequencies (Dom/Mix/Res) as stacked bars,
       grouped by mode (continuous, binary) at each tau.
    B  |phi| (community-level selection correlation) vs tau,
       two lines: continuous and binary.
"""
import json
import os

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "hybrid_original_results.json")

sns.set_style("ticks")
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

mm = 0.1 / 2.54

CLASS_COLORS = {
    'Dom': '#E67E22',   # Dominance   — warm orange (paper convention)
    'Mix': '#2ECC71',   # Mixing      — green
    'Res': '#4A90D9',   # Restructuring — blue
}
MODE_COLORS = {
    'continuous': '#333333',
    'binary':     '#C0392B',
}
MODE_MARKERS = {
    'continuous': 'o',
    'binary':     's',
}


def load_results():
    with open(RESULTS) as f:
        data = json.load(f)
    meta = data['metadata']
    rows = []
    for key, rec in data['runs'].items():
        rows.append(rec['summary'])
    return meta, rows


def main():
    meta, rows = load_results()
    taus = meta['tensions']
    modes = meta['modes']

    # Index summaries by (mode, tau) for convenience
    lookup = {(r['mode'], float(r['tau'])): r for r in rows}

    fig, axes = plt.subplots(1, 3, figsize=(200 * mm, 65 * mm))

    # ---- A, B: stacked bars per mode -----------------------------------
    n_taus = len(taus)
    x = np.arange(n_taus)
    bar_w = 0.62
    panel_letter = {'continuous': 'A', 'binary': 'B'}
    for mi, mode in enumerate(modes):
        ax = axes[mi]
        for ti, tau in enumerate(taus):
            r = lookup[(mode, float(tau))]
            d = r['dom_frac'] or 0.0
            m = r['mix_frac'] or 0.0
            s = r['res_frac'] or 0.0
            n = r['n_events']
            xv = x[ti]
            ax.bar(xv, d, bar_w, color=CLASS_COLORS['Dom'],
                   edgecolor='black', linewidth=0.4,
                   label='Dominance' if ti == 0 else None)
            ax.bar(xv, m, bar_w, bottom=d, color=CLASS_COLORS['Mix'],
                   edgecolor='black', linewidth=0.4,
                   label='Mixing' if ti == 0 else None)
            ax.bar(xv, s, bar_w, bottom=d + m, color=CLASS_COLORS['Res'],
                   edgecolor='black', linewidth=0.4,
                   label='Restructuring' if ti == 0 else None)
            if n < 100:
                ax.text(xv, 1.02, f'n={n}', ha='center', va='bottom',
                        fontsize=5, color='gray')
        ax.set_xticks(x)
        ax.set_xticklabels([f'{t:.1f}' for t in taus])
        ax.set_xlabel(r'$\tau$ (pH effect)')
        if mi == 0:
            ax.set_ylabel('Fraction of coalescence events')
        ax.set_ylim(0, 1.10)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        if mi == 0:
            ax.legend(fontsize=6, frameon=False, loc='upper left',
                      ncol=1, handlelength=1.0)
        ax.set_title(fr'{panel_letter[mode]}  {mode} ($\alpha=0.3$)',
                     fontsize=8, fontweight='bold', loc='left')

    # ---- C: |phi| vs tau -----------------------------------------------
    ax = axes[2]
    for mode in modes:
        ys, yerr, xs = [], [], []
        for tau in taus:
            r = lookup[(mode, float(tau))]
            m = r['phi_mean']
            s = r['phi_std']
            n = r['phi_n']
            xs.append(tau)
            ys.append(m if m is not None else np.nan)
            yerr.append(s / np.sqrt(max(n, 1)) if (s is not None and n) else 0.0)
        ax.errorbar(xs, ys, yerr=yerr,
                    marker=MODE_MARKERS[mode], color=MODE_COLORS[mode],
                    markersize=5, linewidth=1.2, capsize=2, elinewidth=0.5,
                    label=mode)
    ax.set_xlabel(r'$\tau$ (pH effect)')
    ax.set_ylabel(r'$|\phi|$ (origin, persistence)')
    ax.set_ylim(0, 0.8)
    ax.set_xticks(taus)
    ax.set_xticklabels([f'{t:.1f}' for t in taus])
    ax.legend(fontsize=7, frameon=False, loc='upper left',
              handlelength=1.6)
    ax.set_title(r'C  Pairwise selection correlation $|\phi|$',
                 fontsize=8, fontweight='bold', loc='left')

    sns.despine(fig=fig)
    plt.tight_layout()

    for ext in ['svg', 'pdf', 'png']:
        out = os.path.join(HERE, f'Fig_Q5_hybrid_original.{ext}')
        fig.savefig(out, bbox_inches='tight', dpi=300)
        print(f"  saved: {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
