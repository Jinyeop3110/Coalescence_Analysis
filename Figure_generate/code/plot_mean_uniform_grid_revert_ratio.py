#!/usr/bin/env python3
"""
Generate revert ratio plot for mean_uniform_grid_100reps data

Purpose: Calculate and visualize revert ratio as a function of mean interaction strength
         (i.e., plot intensity vs revert ratio)

Output:
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_mean_uniform_grid_Revert_Ratio.svg
"""

from common_setup import *
import json
import numpy as np

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

def metric_VectorDecomposition_onlyPositive(u,v,m):
    u=normalize(u)
    v=normalize(v)
    m=normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])

    e12=np.matmul(np.linalg.inv(A),np.array([np.sum(m*u), np.sum(m*v)]))

    x1=(e12[0])*(e12[0]>0)
    x2=(e12[1])*(e12[1]>0)
    x3=np.linalg.norm(m-(e12[0]*u)-(e12[1]*v))
    convert=np.sqrt((1-x3**2)/(x1**2+x2**2))

    return convert*x1, convert*x2, x3

def calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2):
    """Calculate species-level dominance using Lotka-Volterra equilibrium."""

    if alpha_12 > 1.0 and alpha_21 > 1.0:
        return 0.5
    elif alpha_12 > 1.0 and alpha_21 < 1.0:
        return 0.0
    elif alpha_12 < 1.0 and alpha_21 > 1.0:
        return 1.0
    elif alpha_12 < 1.0 and alpha_21 < 1.0:
        if alpha_12 + alpha_21 < 2.0:
            denominator = 2 - alpha_12 - alpha_21
            if abs(denominator) < 1e-10:
                return 0.5
            return (1 - alpha_12) / denominator
        else:
            return 0.5
    else:
        return 0.5

def calculate_revert_ratio_for_combination(combo_data):
    """Calculate revert ratio for a single mean combination.

    Revert ratio = fraction of cases where species prediction doesn't match community outcome.
    """

    total_count = 0
    revert_count = 0

    # Process each replicate
    for rep_key in combo_data.keys():
        rep_data = combo_data[rep_key]

        # Extract community compositions
        c1 = np.array(rep_data['sc_list']['c1'])
        c2 = np.array(rep_data['sc_list']['c2'])
        c_mix = np.array(rep_data['cc_list']['c1_c2'])

        # Extract LV parameters
        params = rep_data['parameters']
        interaction_matrix = params['interaction_matrix']

        c1_dominant_idx = np.argmax(c1)
        c2_dominant_idx = np.argmax(c2)

        alpha_12 = interaction_matrix[c1_dominant_idx][c2_dominant_idx]
        alpha_21 = interaction_matrix[c2_dominant_idx][c1_dominant_idx]
        K1 = 1.0
        K2 = 1.0

        # Calculate vector decomposition
        try:
            u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)
        except (np.linalg.LinAlgError, ValueError):
            continue

        # Skip if any values are NaN or inf
        if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
            continue

        # FILTER: Only consider cases where u²+v² > 0.5
        mixing_strength = u**2 + v**2
        if mixing_strength <= 0.5:
            continue

        # Calculate community-level dominance
        community_dominance = np.arctan(u / (v + 1e-8)) / (np.pi / 2)

        if np.isnan(community_dominance) or np.isinf(community_dominance):
            continue

        # Calculate species-level dominance
        lv_dominance = calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2)
        ratio = lv_dominance / (1 - lv_dominance + 1e-8)
        species_dominance = np.arctan(ratio) / (np.pi / 2)

        if np.isnan(species_dominance) or np.isinf(species_dominance):
            continue

        # Check if this is a revert case
        species_predicts_c1 = species_dominance > 0.5
        community_shows_c1 = community_dominance > 0.5

        if species_predicts_c1 != community_shows_c1:
            revert_count += 1

        total_count += 1

    # Calculate revert ratio
    if total_count < 5:
        return np.nan, 0

    revert_ratio = revert_count / total_count
    return revert_ratio, total_count

def plot_revert_ratio_vs_intensity():
    """Generate revert ratio vs intensity plot for mean_uniform_grid data."""

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

    # Calculate revert ratio for each mean value
    revert_ratios = []
    sample_sizes = []
    valid_means = []

    for mean_val in mean_values:
        combo_key = f'mean{mean_val:.2f}'

        if combo_key in community_data:
            print(f"Processing {combo_key}...")
            try:
                revert_ratio, n_points = calculate_revert_ratio_for_combination(community_data[combo_key])

                if not np.isnan(revert_ratio):
                    revert_ratios.append(revert_ratio)
                    sample_sizes.append(n_points)
                    valid_means.append(mean_val)
                    print(f"  {combo_key}: Revert ratio = {revert_ratio:.3f}, n = {n_points}")
                else:
                    print(f"  {combo_key}: Insufficient data (n < 5)")
            except Exception as e:
                print(f"  {combo_key}: Failed - {e}")
        else:
            print(f"  {combo_key}: Not found in data")

    # Convert to arrays
    valid_means = np.array(valid_means)
    revert_ratios = np.array(revert_ratios)
    sample_sizes = np.array(sample_sizes)

    # Create plot
    mm = 1 / 25.4
    fig, ax = plt.subplots(1, 1, figsize=(120*mm, 90*mm), facecolor='w', edgecolor='k')

    # Plot revert ratio vs mean interaction strength
    ax.plot(valid_means, revert_ratios, 'o-', color='#e74c3c', markersize=8,
            linewidth=2, alpha=0.8, label='Revert Ratio')

    # Add sample size as text annotations
    for i, (mean_val, rr, n) in enumerate(zip(valid_means, revert_ratios, sample_sizes)):
        if i % 2 == 0:  # Only annotate every other point to avoid crowding
            ax.text(mean_val, rr + 0.02, f'n={n}', fontsize=7, ha='center',
                   va='bottom', alpha=0.7)

    # Add horizontal line at 0.5 (random chance)
    ax.axhline(0.5, color='grey', linestyle='--', linewidth=1, alpha=0.5,
              label='Random (50%)')

    # Formatting
    ax.set_xlabel('Mean Interaction Strength (μ)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Revert Ratio\n(Mismatch Fraction)', fontsize=11, fontweight='bold')
    ax.set_title('Species vs Community Dominance Mismatch', fontsize=12, fontweight='bold')

    ax.set_xlim(min(valid_means) - 0.05, max(valid_means) + 0.05)
    ax.set_ylim(0, 1.0)
    ax.set_yticks(np.arange(0, 1.1, 0.2))

    ax.legend(loc='best', fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    output_file = 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_mean_uniform_grid_Revert_Ratio.svg'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Saved: {output_file}")

    # Print summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Mean Revert Ratio: {np.mean(revert_ratios):.3f}")
    print(f"Median Revert Ratio: {np.median(revert_ratios):.3f}")
    print(f"Min Revert Ratio: {np.min(revert_ratios):.3f} (at μ={valid_means[np.argmin(revert_ratios)]:.2f})")
    print(f"Max Revert Ratio: {np.max(revert_ratios):.3f} (at μ={valid_means[np.argmax(revert_ratios)]:.2f})")
    print(f"Std Revert Ratio: {np.std(revert_ratios):.3f}")

if __name__ == '__main__':
    plot_revert_ratio_vs_intensity()
    print("\nAnalysis complete!")
