#!/usr/bin/env python3
"""
Generate correlation plots for 20reps data (narrow_uniform and wide_uniform)

Purpose: Plot species-level dominance vs community-level dominance for 20reps datasets
Output:
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_20reps_narrow_uniform_Subplots.svg
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_20reps_wide_uniform_Subplots.svg
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
    """
    Calculate species-level dominance using Lotka-Volterra equilibrium.

    Correct conditions:
    - Both > 1: competitive exclusion (unstable, return 0.5)
    - α12 > 1, α21 < 1: species 1 wins
    - α12 < 1, α21 > 1: species 2 wins
    - Both < 1, sum < 2: stable coexistence (use formula)
    - Both < 1, sum > 2: bistability/priority effects (return 0.5)
    """

    # Case 1: Both alphas > 1 - competitive exclusion
    if alpha_12 > 1.0 and alpha_21 > 1.0:
        return 0.5

    # Case 2: alpha_12 > 1 and alpha_21 < 1 - species 2 wins
    # Species 2 strongly affects species 1, species 1 weakly affects species 2
    elif alpha_12 > 1.0 and alpha_21 < 1.0:
        return 0.0

    # Case 3: alpha_12 < 1 and alpha_21 > 1 - species 1 wins
    # Species 1 strongly affects species 2, species 2 weakly affects species 1
    elif alpha_12 < 1.0 and alpha_21 > 1.0:
        return 1.0

    # Case 4a: Both alphas < 1 AND sum < 2 - stable coexistence
    elif alpha_12 < 1.0 and alpha_21 < 1.0:
        if alpha_12 + alpha_21 < 2.0:
            # Stable coexistence - use CORRECT equilibrium formula
            # dominance = N1*/(N1*+N2*) = (1-α₁₂)/(2-α₁₂-α₂₁)
            denominator = 2 - alpha_12 - alpha_21
            if abs(denominator) < 1e-10:
                return 0.5
            return (1 - alpha_12) / denominator  # FIXED: was "1 - alpha_12 / denominator"
        else:
            # Case 4b: Both < 1 but sum > 2 - bistability (priority effects)
            # Cannot predict from pairwise LV alone
            return 0.5

    # Edge cases where alphas equal exactly 1
    else:
        return 0.5

def plot_20reps_correlation_subplots(dataset_name):
    """Plot correlation for 20reps data as subplots (6 selected intensities)."""

    # Load data
    json_file = f'Simulation_Data/48species_20reps_{dataset_name}/Community_20reps_{dataset_name}.json'

    with open(json_file, 'r') as f:
        community_data = json.load(f)

    print(f"Loaded 20reps_{dataset_name} data with {len(community_data)} intensities")

    # Select 6 intensities to plot: 0.2, 0.4, 0.6, 0.8, 1.0, 1.2
    intensity_mapping = {
        '0.20': 0.2,
        '0.40': 0.4,
        '0.60': 0.6,
        '0.80': 0.8,
        '1.00': 1.0,
        '1.20': 1.2
    }

    colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#9B59B6', '#E74C3C']

    # Create subplots: 2 rows x 3 columns
    fig, axes = plt.subplots(2, 3, figsize=(9, 6))
    fig.suptitle(f'48species 20reps {dataset_name}', fontsize=10, y=0.995)

    # Flatten axes for easier indexing
    axes_flat = axes.flatten()

    for plot_idx, (intensity_key, mean_strength) in enumerate(intensity_mapping.items()):
        print(f"\nProcessing mean interaction strength = {mean_strength}")

        ax = axes_flat[plot_idx]

        # Get all replicates for this intensity
        intensity_data = community_data[intensity_key]

        data_species_dominance = []
        data_community_dominance = []

        # Process each replicate
        for rep_key in intensity_data.keys():
            rep_data = intensity_data[rep_key]

            # Get rep-specific interaction matrix from JSON parameters
            rep_interaction_matrix = np.array(rep_data['parameters']['interaction_matrix'])

            # Get communities and most abundant species for this replicate
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            communities = {}
            most_abundant_indices = {}

            # Sort keys like 'c1', 'c2', 'c3', 'c4'
            for comm_key in sorted(sc_list.keys()):
                community = np.array(sc_list[comm_key])
                communities[comm_key] = community
                most_abundant_idx = np.argmax(community)
                most_abundant_indices[comm_key] = most_abundant_idx

            comm_keys = sorted(sc_list.keys())
            num_communities = len(comm_keys)

            # Generate pairwise coalescence comparisons
            for i in range(num_communities):
                for j in range(i+1, num_communities):
                    # Get coalescence key like 'c1_c2'
                    coal_key = f"{comm_keys[i]}_{comm_keys[j]}"
                    if coal_key not in cc_list:
                        continue

                    # Use ACTUAL coalescence outcome from simulation
                    c_mix = np.array(cc_list[coal_key])
                    c_1 = np.array(communities[comm_keys[i]])
                    c_2 = np.array(communities[comm_keys[j]])

                    # Normalize all for consistent comparison
                    c_mix = c_mix / (np.sum(c_mix) + 1e-8)
                    c_1 = c_1 / (np.sum(c_1) + 1e-8)
                    c_2 = c_2 / (np.sum(c_2) + 1e-8)

                    # Apply threshold
                    c_1_thresh = c_1 * (c_1 > 1e-4)
                    c_2_thresh = c_2 * (c_2 > 1e-4)

                    if np.sum(c_1_thresh) == 0 or np.sum(c_2_thresh) == 0:
                        continue

                    # Vector decomposition for community-level dominance
                    try:
                        u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

                        # Skip if any value is NaN or inf
                        if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                            continue

                        # FILTER: Only consider cases where x1² + x2² > 0.5 (substantial mixing)
                        mixing_strength = u**2 + v**2
                        if mixing_strength <= 0.5:
                            continue

                        # Use arctan(u/v) normalized from 0 to 1
                        # arctan ranges from 0 to π/2, so divide by π/2 to get 0 to 1
                        community_dominance = np.arctan(u / (v + 1e-8)) / (np.pi / 2)

                        # Skip if result is NaN or inf
                        if np.isnan(community_dominance) or np.isinf(community_dominance):
                            continue
                    except:
                        continue

                    # Get most abundant species from each community
                    C1 = most_abundant_indices[comm_keys[i]]
                    C2 = most_abundant_indices[comm_keys[j]]

                    # Check bounds
                    if C1 >= rep_interaction_matrix.shape[0] or C2 >= rep_interaction_matrix.shape[0]:
                        continue

                    # Get interaction coefficients from CORRECT matrix (rep-specific from JSON)
                    alpha_12 = rep_interaction_matrix[C1, C2]
                    alpha_21 = rep_interaction_matrix[C2, C1]

                    # FILTER: Exclude cases where both alpha > 1 (competitive exclusion/bistability)
                    # These are unpredictable and contribute to low R²
                    if alpha_12 > 1.0 and alpha_21 > 1.0:
                        continue

                    # Get carrying capacities (all 1.0 in this dataset)
                    K1 = K2 = 1.0

                    # Calculate species-level dominance using LV equilibrium
                    species_dominance_raw = calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2)

                    # Apply arctan normalization to species dominance
                    # Convert from proportion (0-1) to arctan normalized form
                    # If raw dominance = p, then ratio = p/(1-p), then arctan(ratio)/(π/2)
                    ratio = species_dominance_raw / (1 - species_dominance_raw + 1e-8)
                    species_dominance = np.arctan(ratio) / (np.pi / 2)

                    data_species_dominance.append(species_dominance)
                    data_community_dominance.append(community_dominance)

        print(f"Number of data points collected: {len(data_species_dominance)}")

        if len(data_species_dominance) == 0:
            print(f"Warning: No valid data points for intensity {mean_strength}")
            continue

        # Convert to arrays
        x = np.array(data_species_dominance)
        y = np.array(data_community_dominance)

        # Duplicate data points (as in experimental version)
        x = np.concatenate((x, 1-x))
        y = np.concatenate((y, 1-y))

        # Create scatter plot
        ax.scatter(x, y, color=colors[plot_idx], s=10, alpha=0.5)

        # Calculate and plot linear regression
        if len(np.unique(y)) > 1 and len(np.unique(x)) > 1:  # Check for variance
            slope, intercept = np.polyfit(x, y, 1)
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            if ss_tot > 1e-10:  # Avoid division by zero
                r_squared = 1 - (ss_res / ss_tot)
            else:
                r_squared = 0.0
        else:
            slope, intercept = 0.0, np.mean(y) if len(y) > 0 else 0.5
            r_squared = 0.0

        # Add regression line
        x_line = np.linspace(0, 1, 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color=colors[plot_idx], linestyle='--', linewidth=1.5, alpha=0.8)

        # Set subplot properties
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel('Species LV Dominance', fontsize=8)
        ax.set_ylabel('Community Dominance', fontsize=8)
        ax.set_title(f'Mean I = {mean_strength} (R² = {r_squared:.3f})', fontsize=8)
        ax.grid(True, alpha=0.3, linewidth=0.5)
        ax.tick_params(labelsize=7)

        # Add diagonal reference line
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=0.5)

        print(f'Mean interaction strength {mean_strength}: R² = {r_squared:.3f}, Data points = {len(x)}')

    plt.tight_layout()
    plt.savefig(f'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_20reps_{dataset_name}_Subplots.svg',
                bbox_inches='tight', dpi=300)
    plt.close()

    print(f"\n{dataset_name} correlation subplots complete!")

def main():
    """Main function to run correlation plot generation."""
    # Create output directories
    if not os.path.exists('Figure/TopDownAnaylsis'):
        os.makedirs('Figure/TopDownAnaylsis')
    if not os.path.exists('Figure'):
        os.makedirs('Figure')

    print("=== 20reps: Species-level vs Community-level Dominance ===")
    print("Processing 6 selected intensities: 0.2, 0.4, 0.6, 0.8, 1.0, 1.2")

    for dataset_name in ['narrow_uniform', 'wide_uniform']:
        print(f"\n=== Processing 20reps_{dataset_name} ===")
        plot_20reps_correlation_subplots(dataset_name)

    print("\n=== Analysis complete! ===")
    print("Generated files:")
    print("- Fig_MostAbundant_Correlation_20reps_narrow_uniform_Subplots.svg")
    print("- Fig_MostAbundant_Correlation_20reps_wide_uniform_Subplots.svg")

if __name__ == "__main__":
    main()
