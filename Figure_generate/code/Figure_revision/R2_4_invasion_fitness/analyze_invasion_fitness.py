#!/usr/bin/env python
"""
R2-4: Pairwise Selection Correlation vs Invasion Fitness

This script connects pairwise selection correlation to invasion fitness theory
in the gLV model.

For each species i in community A, we compute its invasion fitness into
community B:
    lambda_i = g_i * (1 - sum_j alpha_ij * x_j* / k_i)
where x_j* are B's steady-state abundances.

We then ask: do species from the same assembled community tend to have
correlated invasion success? This "pairwise selection correlation" should
increase with interaction strength mu, because stronger interactions create
more structured communities that act as coherent units during coalescence.

Data source: 10reps fine WITH_MATRICES dataset (has full interaction matrices).
"""

import os
import sys
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from itertools import combinations

# ─── Path setup ───────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, CODE_DIR)

from COLORMAP import (
    PHASE_DIAGRAM_COLORS,
    get_phase_diagram_colors,
    SECONDARY_COLORS,
)

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


def get_survivors(vec, threshold=1e-3):
    """Return indices of species with abundance above threshold."""
    return np.where(np.array(vec) > threshold)[0]


def compute_invasion_fitness(species_idx, I_matrix, g, k, target_abundances):
    """
    Compute invasion growth rate of species `species_idx` into a community
    with steady-state abundances `target_abundances`.

    lambda_i = g_i * (1 - sum_j alpha_ij * x_j* / k_i)

    Parameters
    ----------
    species_idx : int
        Index of the invading species.
    I_matrix : ndarray (N x N)
        Full interaction matrix.
    g : ndarray (N,)
        Growth rates.
    k : ndarray (N,)
        Carrying capacities.
    target_abundances : ndarray (N,)
        Steady-state abundances of the target (resident) community.

    Returns
    -------
    float
        Invasion fitness (growth rate when rare in target community).
    """
    alpha_row = I_matrix[species_idx, :]  # interactions of invader with all species
    invasion_fitness = g[species_idx] * (
        1.0 - np.sum(alpha_row * target_abundances) / k[species_idx]
    )
    return invasion_fitness


def compute_pairwise_invasion_correlation(comm_A_survivors, I_matrix, g, k,
                                           target_abundances):
    """
    Compute the pairwise correlation of invasion fitness among species
    from the same community invading a target community.

    For species from community A, compute each species' invasion fitness
    into community B. Then compute the fraction of species pairs that
    have concordant invasion outcomes (both succeed or both fail).

    Returns
    -------
    concordance : float
        Fraction of species pairs with concordant invasion success.
    n_invaders : int
        Number of species that can invade.
    n_total : int
        Total number of species considered.
    fitness_values : list
        Invasion fitness of each species.
    """
    fitness_values = []
    for sp_idx in comm_A_survivors:
        lam = compute_invasion_fitness(sp_idx, I_matrix, g, k, target_abundances)
        fitness_values.append(lam)

    fitness_values = np.array(fitness_values)

    # Binary: can species invade? (lambda > 0)
    can_invade = fitness_values > 0
    n_invaders = int(np.sum(can_invade))
    n_total = len(can_invade)

    # Pairwise concordance
    if n_total < 2:
        return np.nan, n_invaders, n_total, fitness_values.tolist()

    concordant = 0
    total_pairs = 0
    for i in range(n_total):
        for j in range(i + 1, n_total):
            if can_invade[i] == can_invade[j]:
                concordant += 1
            total_pairs += 1

    concordance = concordant / total_pairs if total_pairs > 0 else np.nan
    return concordance, n_invaders, n_total, fitness_values.tolist()


def main():
    # ── Load data ─────────────────────────────────────────────────────────
    data_path = os.path.join(
        CODE_DIR,
        'Simulation_Data',
        '48species_10reps_fine_WITH_MATRICES',
        'Community_10reps_fine_WITH_MATRICES.json',
    )
    print(f"Loading data from:\n  {data_path}")
    with open(data_path, 'r') as f:
        sim_data = json.load(f)

    mu_keys_sorted = sorted(sim_data.keys(), key=float)
    print(f"Found {len(mu_keys_sorted)} mu values")

    # ── Compute invasion fitness and pairwise correlations ────────────────
    mu_vals = []
    mean_concordance = []
    se_concordance = []
    mean_frac_invade = []
    se_frac_invade = []

    # Store fitness pairs for scatter plot at a specific mu
    scatter_mu = '0.50'
    scatter_fitness_pairs = []  # (fitness_i, fitness_j) from same community

    # Also collect all individual fitness values per mu for distribution plot
    all_fitness_by_mu = {}

    for mu_key in mu_keys_sorted:
        mu_val = float(mu_key)
        reps = sim_data[mu_key]

        concordance_list = []
        frac_invade_list = []
        fitness_all = []

        for rep_key, rep_data in reps.items():
            sc_list = rep_data['sc_list']
            I_mat = np.array(rep_data['parameters']['interaction_matrix'])
            g = np.array(rep_data['parameters']['growth_rates'])
            k = np.array(rep_data['parameters']['carrying_capacities'])

            # All pairwise community combinations
            for c_A in range(4):
                for c_B in range(4):
                    if c_A == c_B:
                        continue

                    surv_A = get_survivors(sc_list[str(c_A)])
                    target_abund = np.array(sc_list[str(c_B)])

                    if len(surv_A) < 2:
                        continue
                    if np.sum(target_abund > 1e-3) < 1:
                        continue

                    conc, n_inv, n_tot, fit_vals = \
                        compute_pairwise_invasion_correlation(
                            surv_A, I_mat, g, k, target_abund
                        )

                    if not np.isnan(conc):
                        concordance_list.append(conc)
                        frac_invade_list.append(n_inv / n_tot if n_tot > 0 else 0)
                        fitness_all.extend(fit_vals)

                    # Collect scatter pairs for the chosen mu
                    if mu_key == scatter_mu and len(fit_vals) >= 2:
                        for i_idx in range(len(fit_vals)):
                            for j_idx in range(i_idx + 1, len(fit_vals)):
                                scatter_fitness_pairs.append(
                                    (fit_vals[i_idx], fit_vals[j_idx])
                                )

        if len(concordance_list) > 0:
            mu_vals.append(mu_val)
            mean_concordance.append(np.mean(concordance_list))
            se_concordance.append(np.std(concordance_list) / np.sqrt(len(concordance_list)))
            mean_frac_invade.append(np.mean(frac_invade_list))
            se_frac_invade.append(np.std(frac_invade_list) / np.sqrt(len(frac_invade_list)))
            all_fitness_by_mu[mu_val] = fitness_all

        print(f"  mu={mu_val:.2f}: concordance={np.mean(concordance_list):.3f} "
              f"+/- {np.std(concordance_list):.3f}, "
              f"frac_invade={np.mean(frac_invade_list):.3f}, "
              f"n_events={len(concordance_list)}")

    mu_vals = np.array(mu_vals)
    mean_concordance = np.array(mean_concordance)
    se_concordance = np.array(se_concordance)
    mean_frac_invade = np.array(mean_frac_invade)
    se_frac_invade = np.array(se_frac_invade)

    # ── Expected concordance under random invasion ────────────────────────
    # If each species independently invades with probability p, then
    # concordance = p^2 + (1-p)^2 = 1 - 2p(1-p)
    expected_concordance = 1 - 2 * mean_frac_invade * (1 - mean_frac_invade)

    excess_concordance = mean_concordance - expected_concordance

    # ── Create figures ────────────────────────────────────────────────────
    phase_colors = get_phase_diagram_colors()
    color_dom = phase_colors[0]

    fig, axes = plt.subplots(1, 3, figsize=(180 * mm, 55 * mm))

    # --- Panel A: Scatter of invasion fitness pairs (same community) ---
    ax = axes[0]
    if len(scatter_fitness_pairs) > 0:
        pairs = np.array(scatter_fitness_pairs)
        ax.scatter(pairs[:, 0], pairs[:, 1], s=5, alpha=0.3, color='#1f77b4',
                   edgecolors='none', rasterized=True)
        ax.axhline(0, color='grey', linewidth=0.5, linestyle='--')
        ax.axvline(0, color='grey', linewidth=0.5, linestyle='--')

        # Annotate quadrants
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        # Count in each quadrant
        n_pp = np.sum((pairs[:, 0] > 0) & (pairs[:, 1] > 0))
        n_nn = np.sum((pairs[:, 0] < 0) & (pairs[:, 1] < 0))
        n_pn = np.sum((pairs[:, 0] > 0) & (pairs[:, 1] < 0))
        n_np = np.sum((pairs[:, 0] < 0) & (pairs[:, 1] > 0))
        n_total_pairs = len(pairs)
        concordant_frac = (n_pp + n_nn) / n_total_pairs if n_total_pairs > 0 else 0

        ax.text(0.95, 0.95,
                f'Concordant: {concordant_frac:.1%}',
                transform=ax.transAxes, ha='right', va='top', fontsize=6,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='grey', alpha=0.8))

        # Pearson correlation
        r_val, p_val = stats.pearsonr(pairs[:, 0], pairs[:, 1])
        ax.text(0.95, 0.82,
                f'r={r_val:.2f}, p={p_val:.1e}',
                transform=ax.transAxes, ha='right', va='top', fontsize=6)

    ax.set_xlabel(r'Invasion fitness $\lambda_i$')
    ax.set_ylabel(r'Invasion fitness $\lambda_j$')
    ax.set_title(f'$\\mu$ = {scatter_mu}', fontsize=7, fontweight='bold')
    ax.set_title('A', fontsize=10, fontweight='bold', loc='left')
    sns.despine(ax=ax)

    # --- Panel B: Pairwise concordance vs mu ---
    ax = axes[1]
    ax.errorbar(mu_vals, mean_concordance, yerr=se_concordance,
                fmt='o-', color='#1f77b4', markersize=3, linewidth=1,
                label='Observed', capsize=2, capthick=0.5, elinewidth=0.5)
    ax.plot(mu_vals, expected_concordance, 's--', color='grey', markersize=3,
            linewidth=1, alpha=0.7, label='Independent null')
    ax.fill_between(mu_vals, expected_concordance, mean_concordance,
                    alpha=0.15, color='#1f77b4')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel('Pairwise invasion\nconcordance')
    ax.legend(fontsize=6, frameon=False)
    ax.set_xlim([0, 1.25])
    ax.set_ylim([0.4, 1.05])
    ax.set_title('B', fontsize=10, fontweight='bold', loc='left')
    sns.despine(ax=ax)

    # --- Panel C: Excess concordance vs mu ---
    ax = axes[2]
    ax.bar(mu_vals, excess_concordance, width=0.04, color='#1f77b4',
           alpha=0.7, edgecolor='none')
    ax.axhline(0, color='black', linewidth=0.5, linestyle='-')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel('Excess concordance\n(obs $-$ null)')
    ax.set_xlim([0, 1.25])
    ax.set_title('C', fontsize=10, fontweight='bold', loc='left')
    sns.despine(ax=ax)

    plt.tight_layout()

    for ext in ['svg', 'pdf', 'png']:
        out_path = os.path.join(SCRIPT_DIR, f'invasion_fitness_analysis.{ext}')
        fig.savefig(out_path, bbox_inches='tight', dpi=300)
        print(f"Saved: {out_path}")
    plt.close(fig)

    # ── Supplementary: Invasion fitness distributions at selected mu ──────
    selected_mus = [0.10, 0.30, 0.50, 0.70, 0.90, 1.10]
    available_mus = sorted(all_fitness_by_mu.keys())
    selected_mus = [m for m in selected_mus if m in available_mus]

    if len(selected_mus) >= 2:
        fig2, axes2 = plt.subplots(1, len(selected_mus),
                                   figsize=(len(selected_mus) * 30 * mm, 50 * mm),
                                   sharey=True)
        if len(selected_mus) == 1:
            axes2 = [axes2]

        for idx, mu_sel in enumerate(selected_mus):
            ax = axes2[idx]
            fitness = np.array(all_fitness_by_mu[mu_sel])
            ax.hist(fitness, bins=30, color='#1f77b4', alpha=0.7,
                    edgecolor='none', density=True)
            ax.axvline(0, color='red', linewidth=0.5, linestyle='--')
            frac_pos = np.mean(fitness > 0)
            ax.set_title(f'$\\mu$={mu_sel:.1f}\n({frac_pos:.0%} invade)',
                         fontsize=6)
            ax.set_xlabel(r'$\lambda_i$', fontsize=7)
            if idx == 0:
                ax.set_ylabel('Density', fontsize=7)
            sns.despine(ax=ax)

        plt.tight_layout()
        for ext in ['svg', 'pdf', 'png']:
            out_path = os.path.join(SCRIPT_DIR,
                                    f'invasion_fitness_distributions.{ext}')
            fig2.savefig(out_path, bbox_inches='tight', dpi=300)
            print(f"Saved: {out_path}")
        plt.close(fig2)

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY: Invasion Fitness & Pairwise Selection Correlation")
    print("=" * 70)
    print(f"{'mu':>6s}  {'Concordance':>12s}  {'Null':>8s}  {'Excess':>8s}  "
          f"{'Frac_invade':>12s}")
    print("-" * 55)
    for i, mu in enumerate(mu_vals):
        print(f"{mu:6.2f}  {mean_concordance[i]:12.3f}  "
              f"{expected_concordance[i]:8.3f}  {excess_concordance[i]:8.3f}  "
              f"{mean_frac_invade[i]:12.3f}")

    # Correlation
    r, p = stats.pearsonr(mu_vals, excess_concordance)
    print(f"\nCorrelation (excess concordance vs mu): r={r:.3f}, p={p:.2e}")
    print(f"Mean excess concordance (mu >= 0.3): "
          f"{np.mean(excess_concordance[mu_vals >= 0.3]):.3f}")

    print("\nDone.")


if __name__ == '__main__':
    main()
