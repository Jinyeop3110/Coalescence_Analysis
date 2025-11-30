#!/usr/bin/env python3
"""
Calculate and plot coexistence fraction (richness / pool_size) for parent communities.
For MN (and LN, HN), calculates what fraction of species from the initial pool survive.
"""

from common_setup import *
from pathlib import Path
import os

# Create output directory
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Parent_communities"
os.makedirs(output_dir, exist_ok=True)

def calculate_richness(composition, threshold=1e-4):
    """Calculate species richness (number of species present above threshold)"""
    return np.sum(np.array(composition) > threshold)

def main():
    """Calculate coexistence fractions for parent communities"""
    print("Calculating coexistence fractions for parent communities...")

    # Color scheme
    from COLORMAP import get_medium_colors
    colors = get_medium_colors()  # [LN, MN, HN]

    # Pool sizes for each condition
    pool_sizes = [6, 12, 24]
    mediums = ['LN', 'MN', 'HN']
    medium_labels = ['Low\nNutrient', 'Medium\nNutrient', 'High\nNutrient']

    # Storage for results
    coexistence_fractions = {medium: {pool: [] for pool in pool_sizes} for medium in mediums}

    # Process each medium and pool size
    for medium in mediums:
        print(f"\nProcessing {medium}...")
        for pool_size in pool_sizes:
            condition = f"{medium}_{pool_size}"

            # Get parent community indices
            parent_idx_list = Syn_Sub_IDX[condition]

            # Calculate richness for each parent community
            for parent_idx in parent_idx_list:
                # Get composition
                composition = getAbundance(Processed_sequences_synthetic, parent_idx)
                if composition is None:
                    continue

                # Calculate richness
                richness = calculate_richness(composition)

                # Calculate coexistence fraction
                coexistence_fraction = richness / pool_size
                coexistence_fractions[medium][pool_size].append(coexistence_fraction)

            n_samples = len(coexistence_fractions[medium][pool_size])
            mean_frac = np.mean(coexistence_fractions[medium][pool_size])
            print(f"  {condition}: {n_samples} samples, mean fraction = {mean_frac:.3f}")

    # Create bar plot
    mm = 1 / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(180*mm, 60*mm), sharey=True)

    for ax_idx, pool_size in enumerate(pool_sizes):
        ax = axes[ax_idx]

        # Prepare data for this pool size
        x_pos = np.arange(len(mediums))
        means = []
        stds = []

        for medium in mediums:
            fractions = coexistence_fractions[medium][pool_size]
            means.append(np.mean(fractions))
            stds.append(np.std(fractions))

        # Create bar plot
        bars = ax.bar(x_pos, means, yerr=stds,
                      color=[colors[0], colors[1], colors[2]],
                      alpha=0.7, capsize=3,
                      error_kw={'elinewidth': 0.8, 'capthick': 0.8})

        # Styling
        ax.set_xlabel(f'Pool Size = {pool_size}')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(medium_labels, fontsize=7)
        ax.set_ylim([0, 1])
        ax.set_yticks([0, 0.5, 1])

        # Add horizontal line at y=1
        ax.axhline(y=1, color='k', linestyle='--', linewidth=0.5, alpha=0.3)

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Add y-label only to first subplot
    axes[0].set_ylabel('Richness / Pool Size')

    plt.tight_layout()
    fig.savefig(f'{output_dir}/ParentCommunity_CoexistenceFraction_by_PoolSize.svg', bbox_inches='tight')
    print(f"\n✅ Saved: ParentCommunity_CoexistenceFraction_by_PoolSize.svg")

    # Alternative view: grouped by medium
    fig2, axes2 = plt.subplots(1, 3, figsize=(180*mm, 60*mm), sharey=True)

    for ax_idx, medium in enumerate(mediums):
        ax = axes2[ax_idx]

        # Prepare data for this medium
        x_pos = np.arange(len(pool_sizes))
        means = []
        stds = []

        for pool_size in pool_sizes:
            fractions = coexistence_fractions[medium][pool_size]
            means.append(np.mean(fractions))
            stds.append(np.std(fractions))

        # Create bar plot
        bars = ax.bar(x_pos, means, yerr=stds,
                      color=colors[ax_idx],
                      alpha=0.7, capsize=3,
                      error_kw={'elinewidth': 0.8, 'capthick': 0.8})

        # Styling
        ax.set_xlabel(medium_labels[ax_idx])
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f'{p}' for p in pool_sizes])
        ax.set_ylim([0, 1])
        ax.set_yticks([0, 0.5, 1])

        # Add horizontal line at y=1
        ax.axhline(y=1, color='k', linestyle='--', linewidth=0.5, alpha=0.3)

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Add y-label only to first subplot
    axes2[0].set_ylabel('Richness / Pool Size')

    # Add common x-label
    fig2.text(0.5, -0.02, 'Pool Size', ha='center', fontsize=10)

    plt.tight_layout()
    fig2.savefig(f'{output_dir}/ParentCommunity_CoexistenceFraction_by_Medium.svg', bbox_inches='tight')
    print(f"✅ Saved: ParentCommunity_CoexistenceFraction_by_Medium.svg")

    # Summary statistics
    print("\n" + "="*60)
    print("SUMMARY: Coexistence Fraction (Richness / Pool Size)")
    print("="*60)
    for medium in mediums:
        print(f"\n{medium}:")

        # Calculate weighted mean across pool sizes
        all_fractions = []
        all_weights = []

        for pool_size in pool_sizes:
            fractions = coexistence_fractions[medium][pool_size]
            n_samples = len(fractions)
            print(f"  Pool {pool_size}: {np.mean(fractions):.3f} ± {np.std(fractions):.3f} (n={n_samples})")

            # Collect for weighted mean
            all_fractions.extend(fractions)
            all_weights.extend([1] * n_samples)  # Each sample has equal weight

        # Weighted mean across all pool sizes
        weighted_mean = np.average(all_fractions, weights=all_weights)
        print(f"  → Weighted mean across all pools: {weighted_mean:.3f} (total n={len(all_fractions)})")

    # Create summary plot: mean across pool sizes for each medium
    fig3, ax = plt.subplots(figsize=(60*mm, 60*mm))

    x_pos = np.arange(len(mediums))
    weighted_means = []
    weighted_stds = []

    for medium in mediums:
        all_fractions = []
        for pool_size in pool_sizes:
            all_fractions.extend(coexistence_fractions[medium][pool_size])
        weighted_means.append(np.mean(all_fractions))
        weighted_stds.append(np.std(all_fractions))

    bars = ax.bar(x_pos, weighted_means, yerr=weighted_stds,
                  color=[colors[0], colors[1], colors[2]],
                  alpha=0.7, capsize=3,
                  error_kw={'elinewidth': 0.8, 'capthick': 0.8})

    ax.set_ylabel('Richness / Pool Size')
    ax.set_xlabel('Nutrient Condition')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(medium_labels, fontsize=7)
    ax.set_ylim([0, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.axhline(y=1, color='k', linestyle='--', linewidth=0.5, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    fig3.savefig(f'{output_dir}/ParentCommunity_CoexistenceFraction_WeightedMean.svg', bbox_inches='tight')
    print(f"\n✅ Saved: ParentCommunity_CoexistenceFraction_WeightedMean.svg")

    plt.close('all')
    print(f"\n✅ Analysis complete! Figures saved to {output_dir}")

if __name__ == "__main__":
    main()
