#!/usr/bin/env python3
"""
Analyze how dominant species fraction in coalesced communities changes with mean interaction strength
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from common_setup import *

def analyze_dominant_fraction_by_intensity(dataset_name):
    """Analyze dominant species fraction vs mean interaction strength."""

    # Load data
    json_file = f'Simulation_Data/48species_20reps_{dataset_name}/Community_20reps_{dataset_name}.json'

    with open(json_file, 'r') as f:
        community_data = json.load(f)

    print(f"\n{'='*80}")
    print(f"Analyzing {dataset_name}: Dominant Species Fraction vs Mean Interaction Strength")
    print(f"{'='*80}")

    # Get all intensities
    intensities = sorted([float(k) for k in community_data.keys()])

    results = {}

    for intensity in intensities:
        intensity_key = f'{intensity:.2f}'
        intensity_data = community_data[intensity_key]

        dominant_fractions_c1 = []  # Fraction of most abundant from c1 in c_mix
        dominant_fractions_c2 = []  # Fraction of most abundant from c2 in c_mix
        relative_dominant_fractions = []  # c1_dominant / (c1_dominant + c2_dominant)

        # Process each replicate
        for rep_key in intensity_data.keys():
            rep_data = intensity_data[rep_key]

            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            communities = {}
            most_abundant_indices = {}

            # Get communities and their most abundant species
            for comm_key in sorted(sc_list.keys()):
                community = np.array(sc_list[comm_key])
                # Normalize
                community = community / (np.sum(community) + 1e-8)
                communities[comm_key] = community
                most_abundant_idx = np.argmax(community)
                most_abundant_indices[comm_key] = most_abundant_idx

            comm_keys = sorted(sc_list.keys())

            # Process all pairwise coalescences
            for i in range(len(comm_keys)):
                for j in range(i+1, len(comm_keys)):
                    coal_key = f"{comm_keys[i]}_{comm_keys[j]}"
                    if coal_key not in cc_list:
                        continue

                    c_mix = np.array(cc_list[coal_key])
                    c_1 = communities[comm_keys[i]]
                    c_2 = communities[comm_keys[j]]

                    # Normalize c_mix
                    c_mix = c_mix / (np.sum(c_mix) + 1e-8)

                    # Get most abundant species indices
                    C1_idx = most_abundant_indices[comm_keys[i]]
                    C2_idx = most_abundant_indices[comm_keys[j]]

                    # Skip if both communities have the same dominant species
                    if C1_idx == C2_idx:
                        continue

                    # Get fractions in coalesced community
                    frac_C1_in_mix = c_mix[C1_idx]
                    frac_C2_in_mix = c_mix[C2_idx]

                    dominant_fractions_c1.append(frac_C1_in_mix)
                    dominant_fractions_c2.append(frac_C2_in_mix)

                    # Calculate relative fraction
                    total = frac_C1_in_mix + frac_C2_in_mix
                    if total > 0:
                        relative_fraction = frac_C1_in_mix / total
                        relative_dominant_fractions.append(relative_fraction)

        # Calculate statistics
        if len(dominant_fractions_c1) > 0:
            results[intensity] = {
                'mean_c1': np.mean(dominant_fractions_c1),
                'mean_c2': np.mean(dominant_fractions_c2),
                'mean_combined': np.mean(dominant_fractions_c1) + np.mean(dominant_fractions_c2),
                'std_c1': np.std(dominant_fractions_c1),
                'std_c2': np.std(dominant_fractions_c2),
                'mean_relative': np.mean(relative_dominant_fractions),
                'std_relative': np.std(relative_dominant_fractions),
                'n_events': len(dominant_fractions_c1)
            }

            print(f"\nIntensity {intensity:.2f}:")
            print(f"  Mean fraction of C1 dominant in c_mix: {results[intensity]['mean_c1']:.4f} ± {results[intensity]['std_c1']:.4f}")
            print(f"  Mean fraction of C2 dominant in c_mix: {results[intensity]['mean_c2']:.4f} ± {results[intensity]['std_c2']:.4f}")
            print(f"  Mean combined fraction (C1+C2):        {results[intensity]['mean_combined']:.4f}")
            print(f"  Mean relative fraction (C1/(C1+C2)):   {results[intensity]['mean_relative']:.4f} ± {results[intensity]['std_relative']:.4f}")
            print(f"  Number of coalescence events:          {results[intensity]['n_events']}")

    return results

def plot_dominant_fraction_trends(results_narrow, results_wide):
    """Plot how dominant species fractions change with interaction strength."""

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Extract data for narrow_uniform
    intensities_narrow = sorted(results_narrow.keys())
    mean_c1_narrow = [results_narrow[i]['mean_c1'] for i in intensities_narrow]
    mean_c2_narrow = [results_narrow[i]['mean_c2'] for i in intensities_narrow]
    mean_combined_narrow = [results_narrow[i]['mean_combined'] for i in intensities_narrow]
    mean_relative_narrow = [results_narrow[i]['mean_relative'] for i in intensities_narrow]

    # Extract data for wide_uniform
    intensities_wide = sorted(results_wide.keys())
    mean_c1_wide = [results_wide[i]['mean_c1'] for i in intensities_wide]
    mean_c2_wide = [results_wide[i]['mean_c2'] for i in intensities_wide]
    mean_combined_wide = [results_wide[i]['mean_combined'] for i in intensities_wide]
    mean_relative_wide = [results_wide[i]['mean_relative'] for i in intensities_wide]

    # Plot 1: Individual dominant species fractions (narrow)
    ax = axes[0, 0]
    ax.plot(intensities_narrow, mean_c1_narrow, 'o-', label='C1 dominant', color='#1f77b4')
    ax.plot(intensities_narrow, mean_c2_narrow, 's-', label='C2 dominant', color='#ff7f0e')
    ax.set_xlabel('Mean Interaction Strength', fontsize=10)
    ax.set_ylabel('Mean Fraction in Coalesced Community', fontsize=10)
    ax.set_title('narrow_uniform: Individual Dominant Species', fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 2: Individual dominant species fractions (wide)
    ax = axes[0, 1]
    ax.plot(intensities_wide, mean_c1_wide, 'o-', label='C1 dominant', color='#1f77b4')
    ax.plot(intensities_wide, mean_c2_wide, 's-', label='C2 dominant', color='#ff7f0e')
    ax.set_xlabel('Mean Interaction Strength', fontsize=10)
    ax.set_ylabel('Mean Fraction in Coalesced Community', fontsize=10)
    ax.set_title('wide_uniform: Individual Dominant Species', fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 3: Combined dominant fraction (both datasets)
    ax = axes[1, 0]
    ax.plot(intensities_narrow, mean_combined_narrow, 'o-', label='narrow_uniform', color='#2ca02c', linewidth=2)
    ax.plot(intensities_wide, mean_combined_wide, 's-', label='wide_uniform', color='#d62728', linewidth=2)
    ax.set_xlabel('Mean Interaction Strength', fontsize=10)
    ax.set_ylabel('Mean Combined Fraction (C1+C2)', fontsize=10)
    ax.set_title('Combined Dominant Species Fraction', fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Plot 4: Relative fraction (should be ~0.5)
    ax = axes[1, 1]
    ax.plot(intensities_narrow, mean_relative_narrow, 'o-', label='narrow_uniform', color='#2ca02c', linewidth=2)
    ax.plot(intensities_wide, mean_relative_wide, 's-', label='wide_uniform', color='#d62728', linewidth=2)
    ax.axhline(y=0.5, color='black', linestyle='--', alpha=0.5, label='Equal (0.5)')
    ax.set_xlabel('Mean Interaction Strength', fontsize=10)
    ax.set_ylabel('Mean Relative Fraction C1/(C1+C2)', fontsize=10)
    ax.set_title('Relative Dominance (should be ~0.5)', fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.45, 0.55)

    plt.tight_layout()
    plt.savefig('Figure/TopDownAnaylsis/Fig_DominantFraction_vs_Intensity.svg', bbox_inches='tight', dpi=300)
    plt.close()

    print("\n" + "="*80)
    print("Plot saved: Figure/TopDownAnaylsis/Fig_DominantFraction_vs_Intensity.svg")
    print("="*80)

def main():
    """Main analysis function."""

    # Analyze both datasets
    results_narrow = analyze_dominant_fraction_by_intensity('narrow_uniform')
    results_wide = analyze_dominant_fraction_by_intensity('wide_uniform')

    # Create comparison plots
    plot_dominant_fraction_trends(results_narrow, results_wide)

    # Summary comparison
    print("\n" + "="*80)
    print("SUMMARY COMPARISON")
    print("="*80)

    print("\nCombined Dominant Fraction (C1+C2) Trend:")
    print("\nnarrow_uniform:")
    for intensity in sorted(results_narrow.keys()):
        print(f"  I={intensity:.2f}: {results_narrow[intensity]['mean_combined']:.4f}")

    print("\nwide_uniform:")
    for intensity in sorted(results_wide.keys()):
        print(f"  I={intensity:.2f}: {results_wide[intensity]['mean_combined']:.4f}")

    # Calculate trend (decrease rate)
    intensities_narrow = sorted(results_narrow.keys())
    intensities_wide = sorted(results_wide.keys())
    combined_narrow = [results_narrow[i]['mean_combined'] for i in intensities_narrow]
    combined_wide = [results_wide[i]['mean_combined'] for i in intensities_wide]

    decrease_narrow = combined_narrow[0] - combined_narrow[-1]
    decrease_wide = combined_wide[0] - combined_wide[-1]

    print(f"\nDecrease from lowest to highest intensity:")
    print(f"  narrow_uniform: {decrease_narrow:.4f} ({combined_narrow[0]:.4f} → {combined_narrow[-1]:.4f})")
    print(f"  wide_uniform:   {decrease_wide:.4f} ({combined_wide[0]:.4f} → {combined_wide[-1]:.4f})")

if __name__ == "__main__":
    main()
