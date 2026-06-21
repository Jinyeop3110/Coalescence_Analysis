#!/usr/bin/env python
"""
R1-7: Interaction Matrix After Assembly - Block Structure Visualization

This script demonstrates that ecological assembly creates structured interaction
matrices from an initially random species pool. After assembly, the effective
interaction submatrix for survivors shows within-community blocks that differ
from between-community blocks.

Data source: 10reps fine WITH_MATRICES dataset (contains full 48x48 interaction
matrices, growth rates, carrying capacities, and community compositions).
"""

import os
import sys
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ─── Path setup ───────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, CODE_DIR)

# ─── Figure style ─────────────────────────────────────────────────────────────
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
TARGET_MU = '0.50'
EXAMPLE_REPS = ['rep_000', 'rep_001', 'rep_002']
SPECIES_PER_COMMUNITY = 12
HEATMAP_CMAP = mpl.colormaps['Greys'].copy()
HEATMAP_CMAP.set_bad('#f2f2f2')


def count_richness(vec, threshold=1e-3):
    """Count species with abundance above threshold."""
    return int(np.sum(np.array(vec) > threshold))


def get_survivors(vec, threshold=1e-3):
    """Return indices of species that survived assembly."""
    return np.where(np.array(vec) > threshold)[0]


def get_initial_species(rep_data, community_idx):
    """Reconstruct initially seeded species for a parental community."""
    I_mat = np.array(rep_data['parameters']['interaction_matrix'])
    n_species = I_mat.shape[0]
    seed = int(rep_data['parameters']['seed'])

    # The simulation generated the interaction matrix, then permuted the species
    # indices into four non-overlapping parental communities.
    np.random.seed(seed)
    _ = np.random.random((n_species, n_species))
    all_species = np.random.permutation(n_species)

    start = community_idx * SPECIES_PER_COMMUNITY
    return all_species[start:start + SPECIES_PER_COMMUNITY]


def ordered_survivors(rep_data, comm_a='0', comm_b='1'):
    """Return post-assembly survivor ordering and group sizes."""
    sc_list = rep_data['sc_list']
    surv_a = get_survivors(sc_list[comm_a])
    surv_b = get_survivors(sc_list[comm_b])
    shared = np.intersect1d(surv_a, surv_b)
    only_a = np.setdiff1d(surv_a, shared)
    only_b = np.setdiff1d(surv_b, shared)
    ordered = np.concatenate([only_a, shared, only_b])
    return ordered, len(only_a), len(shared), len(only_b), surv_a, surv_b


def draw_matrix(ax, matrix, n_a, n_shared, note, show_ylabel=False):
    """Draw one interaction matrix with community boundary and annotation."""
    shown = matrix.copy()
    np.fill_diagonal(shown, np.nan)
    im = ax.imshow(shown, cmap=HEATMAP_CMAP, aspect='equal', vmin=0, vmax=1.0,
                   interpolation='nearest')

    boundary1 = n_a - 0.5
    ax.axhline(boundary1, color='white', linewidth=1.3)
    ax.axvline(boundary1, color='white', linewidth=1.3)
    if n_shared > 0:
        boundary2 = n_a + n_shared - 0.5
        ax.axhline(boundary2, color='white', linewidth=0.9, linestyle='--')
        ax.axvline(boundary2, color='white', linewidth=0.9, linestyle='--')

    ax.set_xticks([])
    ax.set_yticks([])
    if show_ylabel:
        ax.set_ylabel('Species index', fontsize=7)
    ax.text(0.5, -0.12, note, transform=ax.transAxes, ha='center', va='top',
            fontsize=5.6)
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)
    return im


def _collect_block_stats(reps_dict):
    """
    Collect within- and between-community mean interaction strengths for all
    community pairs across all repetitions in *reps_dict*.

    Returns
    -------
    within_means, between_means : np.ndarray, np.ndarray
    """
    within_means = []
    between_means = []

    for rep_key, rep_data in reps_dict.items():
        sc = rep_data['sc_list']
        I_mat = np.array(rep_data['parameters']['interaction_matrix'])
        n_communities = len(sc)

        for c_i in range(n_communities):
            for c_j in range(c_i + 1, n_communities):
                s_i = get_survivors(sc[str(c_i)])
                s_j = get_survivors(sc[str(c_j)])

                if len(s_i) < 2 or len(s_j) < 2:
                    continue

                block_ii = I_mat[np.ix_(s_i, s_i)]
                within_means.append(np.mean(block_ii[~np.eye(len(s_i), dtype=bool)]))

                block_jj = I_mat[np.ix_(s_j, s_j)]
                within_means.append(np.mean(block_jj[~np.eye(len(s_j), dtype=bool)]))

                block_ij = I_mat[np.ix_(s_i, s_j)]
                between_means.append(np.mean(block_ij))

    return np.array(within_means), np.array(between_means)


def main():
    np.random.seed(42)

    # ── Load data with interaction matrices ───────────────────────────────
    data_path = os.path.join(
        CODE_DIR,
        'Simulation_Data',
        '48species_10reps_fine_WITH_MATRICES',
        'Community_10reps_fine_WITH_MATRICES.json',
    )
    print(f"Loading data from:\n  {data_path}")
    with open(data_path, 'r') as f:
        sim_data = json.load(f)

    # Use moderate interaction strength for clear visualization
    target_mu = TARGET_MU
    if target_mu not in sim_data:
        available = sorted(sim_data.keys(), key=float)
        target_mu = available[len(available) // 2]
        print(f"mu=0.50 not found; using mu={target_mu}")

    reps = sim_data[target_mu]
    print(f"Using mu={target_mu} with {len(reps)} repetitions")

    example_reps = [rep for rep in EXAMPLE_REPS if rep in reps]
    if len(example_reps) < 3:
        example_reps = sorted(reps.keys())[:3]
    print(f"Example repetitions: {example_reps}")

    mu_val = float(target_mu)

    # Collect within/between stats across all reps before plotting, so the
    # same summary accompanies the example matrices.
    within_means, between_means = _collect_block_stats(reps)

    print(f"\nAcross all reps (mu={target_mu}):")
    print(f"  Within-community interaction (off-diag): "
          f"mean={np.mean(within_means):.3f} +/- {np.std(within_means):.3f}")
    print(f"  Between-community interaction: "
          f"mean={np.mean(between_means):.3f} +/- {np.std(between_means):.3f}")

    mw_stat, mw_p = stats.mannwhitneyu(within_means, between_means, alternative='two-sided')
    print(f"\nMann-Whitney U test (within vs between interaction strength):")
    print(f"  U = {mw_stat:.1f}, p = {mw_p:.4e}")
    sig = "***" if mw_p < 0.001 else ("**" if mw_p < 0.01 else ("*" if mw_p < 0.05 else "n.s."))
    print(f"  Significance: {sig}")
    print(f"  Interpretation: within={'<' if np.mean(within_means) < np.mean(between_means) else '>'}between "
          f"({np.mean(within_means):.3f} vs {np.mean(between_means):.3f})")

    # Create a compact multi-example figure: before/after matrices for three
    # replicates plus a smaller pooled within-vs-between summary.
    fig = plt.figure(figsize=(178 * mm, 86 * mm))
    gs = fig.add_gridspec(
        nrows=2,
        ncols=4,
        width_ratios=[1.0, 1.0, 1.0, 0.86],
        left=0.08,
        right=0.98,
        top=0.82,
        bottom=0.24,
        wspace=0.34,
        hspace=0.54,
    )

    heatmap_axes = []
    last_im = None

    for row, rep_key in enumerate(example_reps[:3]):
        rep_data = reps[rep_key]
        I_matrix = np.array(rep_data['parameters']['interaction_matrix'])

        init_A = get_initial_species(rep_data, 0)
        init_B = get_initial_species(rep_data, 1)
        initial_ordered = np.concatenate([init_A, init_B])
        I_before = I_matrix[np.ix_(initial_ordered, initial_ordered)]

        ordered_indices, n_A, n_shared, n_B, surv_A, surv_B = ordered_survivors(rep_data)
        I_after = I_matrix[np.ix_(ordered_indices, ordered_indices)]

        print(
            f"{rep_key}: before A={len(init_A)}, B={len(init_B)}; "
            f"after A={len(surv_A)}, B={len(surv_B)}, shared={n_shared}"
        )
        print(f"  A survivors: {surv_A.tolist()}")
        print(f"  B survivors: {surv_B.tolist()}")

        before_ax = fig.add_subplot(gs[0, row])
        after_ax = fig.add_subplot(gs[1, row])
        heatmap_axes.extend([before_ax, after_ax])

        before_note = 'A=12, B=12 seeded'
        after_note = f'A={len(surv_A)}/12, B={len(surv_B)}/12 survivors'

        last_im = draw_matrix(before_ax, I_before, len(init_A), 0, before_note,
                              show_ylabel=False)
        last_im.set_clim(0, 2 * mu_val)
        last_im = draw_matrix(after_ax, I_after, n_A, n_shared, after_note)
        last_im.set_clim(0, 2 * mu_val)

        before_ax.set_title(f'Rep. {row + 1}', fontsize=7.5, pad=3)

    fig.text(0.022, 0.70, 'A\nBefore\nassembly', ha='left', va='center',
             fontsize=8.5, fontweight='bold', linespacing=1.05)
    fig.text(0.022, 0.40, 'B\nAfter\nassembly', ha='left', va='center',
             fontsize=8.5, fontweight='bold', linespacing=1.05)

    cax = fig.add_axes([0.105, 0.105, 0.51, 0.026])
    cbar = fig.colorbar(last_im, cax=cax, orientation='horizontal')
    cbar.set_label(r'Interaction coefficient $\alpha_{ij}$', fontsize=7)
    cbar.ax.tick_params(labelsize=6)

    # --- Panel C: Block mean comparison (across all reps) ---
    ax = fig.add_subplot(gs[:, 3])

    # Box/strip plot
    data_box = [within_means, between_means]
    positions = [0, 1]
    bp = ax.boxplot(data_box, positions=positions, widths=0.5,
                    patch_artist=True, showfliers=False,
                    medianprops=dict(color='black', linewidth=1))
    bp['boxes'][0].set_facecolor('#6baed6')
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_facecolor('#fd8d3c')
    bp['boxes'][1].set_alpha(0.7)

    # Add individual points with jitter
    for i, vals in enumerate(data_box):
        jitter = np.random.normal(0, 0.05, len(vals))
        ax.scatter(np.full(len(vals), positions[i]) + jitter, vals,
                   alpha=0.25, s=6, color='grey', zorder=3)

    # Significance bracket — anchor at Q3+1.5*IQR (whisker top) of the higher group
    q3_within = np.percentile(within_means, 75)
    iqr_within = q3_within - np.percentile(within_means, 25)
    q3_between = np.percentile(between_means, 75)
    iqr_between = q3_between - np.percentile(between_means, 25)
    whisker_top = max(q3_within + 1.5 * iqr_within, q3_between + 1.5 * iqr_between)
    y_sig = whisker_top * 1.08
    ax.plot([0, 0, 1, 1], [y_sig * 0.97, y_sig, y_sig, y_sig * 0.97],
            'k-', linewidth=0.8)
    ax.text(0.5, y_sig * 1.01, sig, ha='center', va='bottom', fontsize=8)

    ax.set_xticks(positions)
    ax.set_xticklabels(['Within', 'Between'], fontsize=7)
    ax.set_ylabel(r'Mean $\alpha_{ij}$', fontsize=7)
    ax.axhline(float(target_mu), color='grey', linewidth=0.5, linestyle='--',
               zorder=0)
    ax.text(0.08, float(target_mu) + 0.006, 'pool mean', color='grey',
            fontsize=5.5, ha='left', va='bottom')
    ax.set_title('C  Pooled coefficients', fontsize=8.5, fontweight='bold', loc='left')
    ax.tick_params(axis='y', labelsize=7)
    sns.despine(ax=ax)

    # ── Save ──────────────────────────────────────────────────────────────
    for ext in ['svg', 'pdf', 'png']:
        out_path = os.path.join(SCRIPT_DIR, f'interaction_matrix_assembly.{ext}')
        fig.savefig(out_path, bbox_inches='tight', dpi=300)
        print(f"Saved: {out_path}")
    plt.close(fig)

    # ── Multi-mu analysis: within vs between across interaction strengths ─
    print("\n\nComputing within vs between across all mu values...")
    mu_keys_sorted = sorted(sim_data.keys(), key=float)

    mu_plot = []
    within_plot_mean = []
    within_plot_se = []
    between_plot_mean = []
    between_plot_se = []
    ratio_plot = []

    for mu_key in mu_keys_sorted:
        mu_val_local = float(mu_key)
        within_all, between_all = _collect_block_stats(sim_data[mu_key])

        if len(within_all) > 0 and len(between_all) > 0:
            mu_plot.append(mu_val_local)
            within_plot_mean.append(np.mean(within_all))
            within_plot_se.append(np.std(within_all) / np.sqrt(len(within_all)))
            between_plot_mean.append(np.mean(between_all))
            between_plot_se.append(np.std(between_all) / np.sqrt(len(between_all)))
            # Ratio: between/within
            ratio_plot.append(np.mean(between_all) / (np.mean(within_all) + 1e-10))

    mu_plot = np.array(mu_plot)
    within_plot_mean = np.array(within_plot_mean)
    within_plot_se = np.array(within_plot_se)
    between_plot_mean = np.array(between_plot_mean)
    between_plot_se = np.array(between_plot_se)

    # Supplementary figure: within vs between across mu
    fig2, axes2 = plt.subplots(1, 2, figsize=(130 * mm, 55 * mm))

    ax = axes2[0]
    ax.errorbar(mu_plot, within_plot_mean, yerr=within_plot_se,
                fmt='o-', color='#6baed6', markersize=3, linewidth=1,
                label='Within-community', capsize=2, capthick=0.5, elinewidth=0.5)
    ax.errorbar(mu_plot, between_plot_mean, yerr=between_plot_se,
                fmt='s-', color='#fd8d3c', markersize=3, linewidth=1,
                label='Between-community', capsize=2, capthick=0.5, elinewidth=0.5)
    # Reference line: diagonal (y = x means within = mu)
    ax.plot(mu_plot, mu_plot, '--', color='grey', linewidth=0.5,
            label=r'$\alpha_{ij} = \mu$')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel(r'Mean $\alpha_{ij}$ (off-diagonal)')
    ax.legend(fontsize=5, frameon=False)
    ax.set_xlim([0, 1.25])
    ax.set_title('A', fontsize=10, fontweight='bold', loc='left')
    sns.despine(ax=ax)

    ax = axes2[1]
    ax.plot(mu_plot, np.array(ratio_plot), 'o-', color='black', markersize=3,
            linewidth=1)
    ax.axhline(1.0, color='grey', linewidth=0.5, linestyle='--')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel('Between / Within ratio')
    ax.set_xlim([0, 1.25])
    ax.set_title('B', fontsize=10, fontweight='bold', loc='left')
    sns.despine(ax=ax)

    plt.tight_layout()

    for ext in ['svg', 'pdf', 'png']:
        out_path = os.path.join(SCRIPT_DIR, f'interaction_matrix_mu_comparison.{ext}')
        fig2.savefig(out_path, bbox_inches='tight', dpi=300)
        print(f"Saved: {out_path}")
    plt.close(fig2)

    print("\nDone.")


if __name__ == '__main__':
    main()
