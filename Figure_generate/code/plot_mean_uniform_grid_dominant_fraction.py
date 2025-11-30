#!/usr/bin/env python3
"""
Generate dominant species fraction analysis for mean_uniform_grid_100reps data

Purpose: Analyze how the fraction of the most abundant species in subcommunities
         changes with mean interaction strength

Output:
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Fraction_mean_uniform_grid.svg
    (Mean interaction strength vs dominant species fraction for c1 and c2)
"""

from common_setup import *
import json
import numpy as np

def analyze_dominant_fractions():
    """Analyze dominant species fractions for each mean interaction strength."""

    # Load data
    json_file = 'Simulation_Data/mean_uniform_grid_100reps/Community_mean_uniform_grid_100reps.json'

    with open(json_file, 'r') as f:
        community_data = json.load(f)

    print(f"Loaded mean_uniform_grid_100reps data with {len(community_data)} mean combinations")

    # Parse all mean values
    mean_values = set()
    for combo_key in community_data.keys():
        mean_val = float(combo_key.replace('mean', ''))
        mean_values.add(mean_val)

    mean_values = sorted(list(mean_values))
    print(f"Mean values: {mean_values}")

    # Collect dominant fractions for each mean value
    results = {}

    for mean_val in mean_values:
        combo_key = f'mean{mean_val:.2f}'

        if combo_key not in community_data:
            continue

        combo_data = community_data[combo_key]
        print(f"Processing {combo_key} with {len(combo_data)} replicates...")

        c1_dominant_fractions = []
        c2_dominant_fractions = []

        # Process each replicate
        for rep_key in combo_data.keys():
            rep_data = combo_data[rep_key]

            # Extract community compositions
            c1 = np.array(rep_data['sc_list']['c1'])
            c2 = np.array(rep_data['sc_list']['c2'])

            # Calculate total abundance
            c1_total = np.sum(c1)
            c2_total = np.sum(c2)

            # Get dominant species abundance
            c1_dominant = np.max(c1)
            c2_dominant = np.max(c2)

            # Calculate fractions
            if c1_total > 0:
                c1_fraction = c1_dominant / c1_total
                c1_dominant_fractions.append(c1_fraction)

            if c2_total > 0:
                c2_fraction = c2_dominant / c2_total
                c2_dominant_fractions.append(c2_fraction)

        results[mean_val] = {
            'c1_mean': np.mean(c1_dominant_fractions),
            'c1_std': np.std(c1_dominant_fractions),
            'c1_median': np.median(c1_dominant_fractions),
            'c2_mean': np.mean(c2_dominant_fractions),
            'c2_std': np.std(c2_dominant_fractions),
            'c2_median': np.median(c2_dominant_fractions),
            'n': len(c1_dominant_fractions)
        }

        print(f"  {combo_key}: c1 dominant fraction = {results[mean_val]['c1_mean']:.3f} ± {results[mean_val]['c1_std']:.3f}")
        print(f"  {combo_key}: c2 dominant fraction = {results[mean_val]['c2_mean']:.3f} ± {results[mean_val]['c2_std']:.3f}")

    # Extract data for plotting
    valid_means = sorted(list(results.keys()))
    c1_means = [results[m]['c1_mean'] for m in valid_means]
    c1_stds = [results[m]['c1_std'] for m in valid_means]
    c2_means = [results[m]['c2_mean'] for m in valid_means]
    c2_stds = [results[m]['c2_std'] for m in valid_means]

    # Create plot
    mm = 1 / 25.4
    fig, ax = plt.subplots(1, 1, figsize=(120*mm, 90*mm), facecolor='w', edgecolor='k')

    # Plot c1 dominant fraction
    ax.errorbar(valid_means, c1_means, yerr=c1_stds, fmt='o-', color='#3498db',
                markersize=8, linewidth=2, alpha=0.8, capsize=4, capthick=1.5,
                label='Community 1')

    # Plot c2 dominant fraction
    ax.errorbar(valid_means, c2_means, yerr=c2_stds, fmt='s-', color='#e74c3c',
                markersize=8, linewidth=2, alpha=0.8, capsize=4, capthick=1.5,
                label='Community 2')

    # Formatting
    ax.set_xlabel('Mean Interaction Strength (μ)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Dominant Species Fraction', fontsize=11, fontweight='bold')
    ax.set_title('Most Abundant Species Fraction in Subcommunities', fontsize=12, fontweight='bold')

    ax.set_xlim(min(valid_means) - 0.05, max(valid_means) + 0.05)
    ax.set_ylim(0, 1.0)
    ax.set_yticks(np.arange(0, 1.1, 0.2))

    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    output_file = 'Figure/TopDownAnaylsis/Fig_MostAbundant_Fraction_mean_uniform_grid.svg'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Saved: {output_file}")

    # Print summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Community 1 - Mean dominant fraction: {np.mean(c1_means):.3f}")
    print(f"Community 1 - Range: {np.min(c1_means):.3f} to {np.max(c1_means):.3f}")
    print(f"Community 2 - Mean dominant fraction: {np.mean(c2_means):.3f}")
    print(f"Community 2 - Range: {np.min(c2_means):.3f} to {np.max(c2_means):.3f}")

if __name__ == '__main__':
    analyze_dominant_fractions()
    print("\nAnalysis complete!")
