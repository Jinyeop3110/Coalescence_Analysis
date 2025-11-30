#!/usr/bin/env python
"""
Plot assembly effect on mean interaction strength

This script analyzes how the community-weighted mean interaction strength
changes before and after coalescence (assembly) as a function of the
interaction strength parameter.

For each community:
- Calculate weighted mean interaction strength before coalescence (single communities)
- Calculate weighted mean interaction strength after coalescence (mixed communities)
- Plot the change as a function of mean interaction strength parameter
"""

import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("ticks")
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 11

# Parameters
N = 48  # Total number of species
num_per_community = 12  # Species per community

def calculate_mean_interaction_all_species(interaction_matrix):
    """
    Calculate mean interaction strength assuming all species exist.

    Simply averages all off-diagonal elements of the interaction matrix.

    Parameters:
    -----------
    interaction_matrix : array-like (N, N)
        Interaction matrix

    Returns:
    --------
    mean_interaction : float
        Mean of off-diagonal interaction terms
    """
    interaction_matrix = np.array(interaction_matrix)
    N = interaction_matrix.shape[0]

    # Get all off-diagonal elements
    off_diagonal = []
    for i in range(N):
        for j in range(N):
            if i != j:
                off_diagonal.append(interaction_matrix[i, j])

    return np.mean(off_diagonal)


def calculate_mean_interaction_present_species(abundances, interaction_matrix):
    """
    Calculate mean interaction strength for species that are present.

    Only considers off-diagonal interactions between species that survived
    (abundance > threshold).

    Parameters:
    -----------
    abundances : array-like (N,)
        Species abundances
    interaction_matrix : array-like (N, N)
        Interaction matrix

    Returns:
    --------
    mean_interaction : float
        Mean of off-diagonal interaction terms for present species
    """
    abundances = np.array(abundances)
    interaction_matrix = np.array(interaction_matrix)

    # Find species that are present (abundance > 1e-6)
    present = abundances > 1e-6

    if np.sum(present) < 2:  # Need at least 2 species for interactions
        return np.nan

    # Get indices of present species
    present_indices = np.where(present)[0]

    # Get off-diagonal interactions among present species
    interactions = []
    for i in present_indices:
        for j in present_indices:
            if i != j:
                interactions.append(interaction_matrix[i, j])

    if len(interactions) == 0:
        return np.nan

    return np.mean(interactions)


def calculate_cross_community_interaction(abundances_c1, abundances_c2, interaction_matrix):
    """
    Calculate mean cross-community interaction strength.

    Measures how species in community 1 are affected by species in community 2,
    and vice versa. This represents the interaction strength between the two
    parent communities before they are mixed.

    Parameters:
    -----------
    abundances_c1 : array-like (N,)
        Species abundances in community 1
    abundances_c2 : array-like (N,)
        Species abundances in community 2
    interaction_matrix : array-like (N, N)
        Interaction matrix

    Returns:
    --------
    mean_cross_interaction : float
        Mean of cross-community interaction terms
    """
    abundances_c1 = np.array(abundances_c1)
    abundances_c2 = np.array(abundances_c2)
    interaction_matrix = np.array(interaction_matrix)

    # Find species present in each community
    present_c1 = abundances_c1 > 1e-6
    present_c2 = abundances_c2 > 1e-6

    if np.sum(present_c1) < 1 or np.sum(present_c2) < 1:
        return np.nan

    # Get indices of present species
    indices_c1 = np.where(present_c1)[0]
    indices_c2 = np.where(present_c2)[0]

    # Calculate cross-community interactions
    # How c1 species are affected by c2 species, and vice versa
    cross_interactions = []

    # Species in c1 affected by species in c2
    for i in indices_c1:
        for j in indices_c2:
            cross_interactions.append(interaction_matrix[i, j])

    # Species in c2 affected by species in c1
    for i in indices_c2:
        for j in indices_c1:
            cross_interactions.append(interaction_matrix[i, j])

    if len(cross_interactions) == 0:
        return np.nan

    return np.mean(cross_interactions)


def analyze_assembly_effect(data_file):
    """
    Analyze assembly effect on mean interaction strength

    Returns:
    --------
    results : dict
        Dictionary with mean values as keys and raw data points
    """
    print(f"Loading data from {data_file}...")
    with open(data_file, 'r') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} parameter combinations")

    # Extract mean values from keys
    mean_values = sorted([float(key.replace('mean', '')) for key in data.keys()])
    print(f"Mean values: {mean_values}")

    results = {}

    for mean_val in mean_values:
        key = f"mean{mean_val:.2f}"
        print(f"\nProcessing {key}...")

        before_coalescence = []  # Mean interaction before assembly
        after_coalescence = []   # Mean interaction after assembly

        # Process each replicate
        for rep_key, rep_data in data[key].items():
            interaction_matrix = np.array(rep_data['parameters']['interaction_matrix'])

            # Get single community states (before coalescence)
            sc_list = rep_data['sc_list']

            # Get coalescence states (after assembly)
            cc_list = rep_data['cc_list']

            # Process all pairwise coalescence events
            coalescence_pairs = [
                ('c1', 'c2', 'c1_c2'),
                ('c1', 'c3', 'c1_c3'),
                ('c1', 'c4', 'c1_c4'),
                ('c2', 'c3', 'c2_c3'),
                ('c2', 'c4', 'c2_c4'),
                ('c3', 'c4', 'c3_c4')
            ]

            for c1_name, c2_name, cc_name in coalescence_pairs:
                # Before assembly: mean interaction assuming all species exist
                before_mean = calculate_mean_interaction_all_species(interaction_matrix)

                # Get abundances of parent communities
                abundances_c1 = np.array(sc_list[c1_name])
                abundances_c2 = np.array(sc_list[c2_name])

                # Cross-community interaction: how c1 affects c2 and vice versa
                parent_mean = calculate_cross_community_interaction(abundances_c1, abundances_c2, interaction_matrix)

                # Get abundances after coalescence
                abundances_cc = np.array(cc_list[cc_name])

                # After assembly: mean interaction only for species that survived
                after_mean = calculate_mean_interaction_present_species(abundances_cc, interaction_matrix)

                if not np.isnan(after_mean):
                    before_coalescence.append(before_mean)
                    after_coalescence.append(after_mean)

                    # Store parent community mean as well
                    if 'parent_values' not in results.get(mean_val, {}):
                        if mean_val not in results:
                            results[mean_val] = {}
                        results[mean_val]['parent_values'] = []
                    if not np.isnan(parent_mean):
                        results[mean_val]['parent_values'].append(parent_mean)

        # Calculate parent community statistics
        parent_values = results.get(mean_val, {}).get('parent_values', [])

        # Store raw data points and statistics
        results[mean_val].update({
            'before_values': before_coalescence,
            'after_values': after_coalescence,
            'before_mean': np.mean(before_coalescence) if before_coalescence else np.nan,
            'before_std': np.std(before_coalescence) if before_coalescence else np.nan,
            'before_sem': np.std(before_coalescence) / np.sqrt(len(before_coalescence)) if before_coalescence else np.nan,
            'after_mean': np.mean(after_coalescence) if after_coalescence else np.nan,
            'after_std': np.std(after_coalescence) if after_coalescence else np.nan,
            'after_sem': np.std(after_coalescence) / np.sqrt(len(after_coalescence)) if after_coalescence else np.nan,
            'parent_mean': np.mean(parent_values) if parent_values else np.nan,
            'parent_std': np.std(parent_values) if parent_values else np.nan,
            'parent_sem': np.std(parent_values) / np.sqrt(len(parent_values)) if parent_values else np.nan,
            'n_samples': len(before_coalescence)
        })

        print(f"  {key}: {len(before_coalescence)} coalescence events")
        print(f"    Before assembly:  {results[mean_val]['before_mean']:.4f} ± {results[mean_val]['before_sem']:.4f}")
        print(f"    Inter-community:  {results[mean_val]['parent_mean']:.4f} ± {results[mean_val]['parent_sem']:.4f}")
        print(f"    Intra-community:  {results[mean_val]['after_mean']:.4f} ± {results[mean_val]['after_sem']:.4f}")

    return results


def plot_assembly_effect(results, output_dir):
    """
    Plot assembly effect on mean interaction strength with scatter plots and regression lines
    """
    from scipy import stats

    mean_values = sorted(results.keys())

    # Create combined scatter plot with all data
    fig, ax = plt.subplots(figsize=(3.536, 3.54))  # 80% of original x size (4.42 * 0.8)

    # Collect all data points
    all_before = np.concatenate([results[m]['before_values'] for m in mean_values])
    all_after = np.concatenate([results[m]['after_values'] for m in mean_values])
    all_parent = np.concatenate([results[m]['parent_values'] for m in mean_values if results[m].get('parent_values')])

    # Randomly sample 100 points for scatter plot
    np.random.seed(42)  # For reproducibility
    n_sample = 100

    # Sample inter-community points
    if len(all_parent) > n_sample:
        parent_indices = np.random.choice(len(all_parent), n_sample, replace=False)
        sampled_before_parent = all_before[:len(all_parent)][parent_indices]
        sampled_parent = all_parent[parent_indices]
    else:
        sampled_before_parent = all_before[:len(all_parent)]
        sampled_parent = all_parent

    # Sample intra-community points
    if len(all_after) > n_sample:
        after_indices = np.random.choice(len(all_after), n_sample, replace=False)
        sampled_before_after = all_before[after_indices]
        sampled_after = all_after[after_indices]
    else:
        sampled_before_after = all_before
        sampled_after = all_after

    # Scatter plot for inter-community interactions - red with reduced alpha
    ax.scatter(sampled_before_parent, sampled_parent, alpha=0.15, s=12, color='red', edgecolors='none')

    # Scatter plot for intra-community interactions - blue with reduced alpha
    ax.scatter(sampled_before_after, sampled_after, alpha=0.2, s=12, color='lightblue', edgecolors='none')

    # Plot mean inter-community interactions - red line with points
    mean_before_vals = [results[m]['before_mean'] for m in mean_values]
    mean_parent_vals = [results[m]['parent_mean'] for m in mean_values]
    ax.plot(mean_before_vals, mean_parent_vals, '-o', color='red', linewidth=1.8, alpha=0.8,
           markersize=4, markerfacecolor='red', markeredgewidth=0,
           label='Pre-assembly')

    # Plot mean intra-community interactions - blue line with points
    mean_after_vals = [results[m]['after_mean'] for m in mean_values]
    ax.plot(mean_before_vals, mean_after_vals, '-o', color='cornflowerblue', linewidth=1.8,
           markersize=4, markerfacecolor='cornflowerblue', markeredgewidth=0,
           label='Post-assembly')

    ax.set_xlim([0, 1.2])
    ax.set_ylim([0, 1.5])

    # Set sparser ticks
    ax.set_xticks([0, 0.4, 0.8, 1.2])
    ax.set_yticks([0, 0.5, 1.0, 1.5])

    ax.set_xlabel('Interaction strength (μ)', fontsize=14)
    ax.set_ylabel('Mean Pairwise interaction', fontsize=14)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    sns.despine()
    plt.tight_layout()

    # Save figure
    output_file = output_dir / "Assembly_effect_scatter_combined.svg"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file}")

    output_file_png = output_dir / "Assembly_effect_scatter_combined.png"
    plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file_png}")

    # Save test version to verify changes
    output_file_test = output_dir / "Assembly_effect_scatter_combined_UPDATED.svg"
    plt.savefig(output_file_test, dpi=300, bbox_inches='tight')
    print(f"✓ Saved test figure: {output_file_test}")

    plt.close()


def main():
    # Paths
    data_file = Path("Simulation_Data/mean_uniform_grid_100reps/Community_mean_uniform_grid_100reps.json")
    output_dir = Path("Figure_generate/code/Figure/Assembly_effect_simulation")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("Assembly Effect on Mean Interaction Strength Analysis")
    print("="*70)

    # Analyze data
    results = analyze_assembly_effect(data_file)

    # Plot results
    print("\n" + "="*70)
    print("Generating plots...")
    print("="*70)
    plot_assembly_effect(results, output_dir)

    print("\n" + "="*70)
    print("✓✓✓ ANALYSIS COMPLETE! ✓✓✓")
    print("="*70)


if __name__ == "__main__":
    main()
