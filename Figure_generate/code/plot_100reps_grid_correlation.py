#!/usr/bin/env python3
"""
Generate correlation plots for 100reps mean_std_grid data

Purpose: Plot species-level dominance vs community-level dominance for 100reps grid datasets
Output:
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_100reps_grid_Subplots.svg
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
            return (1 - alpha_12) / denominator
        else:
            # Case 4b: Both < 1 but sum > 2 - bistability (priority effects)
            # Cannot predict from pairwise LV alone
            return 0.5

    # Edge cases where alphas equal exactly 1
    else:
        return 0.5

def plot_100reps_grid_correlation_subplots():
    """Plot correlation for 100reps grid data as subplots (6 selected mean/std combinations)."""

    # Load data
    json_file = 'Simulation_Data/mean_std_grid_100reps/Community_mean_std_grid_100reps.json'

    with open(json_file, 'r') as f:
        community_data = json.load(f)

    print(f"Loaded 100reps grid data with {len(community_data)} mean/std combinations")

    # Select 6 interesting mean/std combinations to plot
    # We'll choose:
    # - Low mean, low std: mean0.10_std0.10
    # - Low mean, high std: mean0.10_std0.50
    # - Medium mean, low std: mean0.30_std0.10
    # - Medium mean, medium std: mean0.30_std0.30
    # - High mean, low std: mean0.50_std0.10
    # - High mean, high std: mean0.50_std0.50
    selected_combinations = [
        ('mean0.10_std0.10', 'μ=0.1, σ=0.1'),
        ('mean0.10_std0.50', 'μ=0.1, σ=0.5'),
        ('mean0.30_std0.10', 'μ=0.3, σ=0.1'),
        ('mean0.30_std0.30', 'μ=0.3, σ=0.3'),
        ('mean0.50_std0.10', 'μ=0.5, σ=0.1'),
        ('mean0.50_std0.50', 'μ=0.5, σ=0.5'),
    ]

    # Setup figure with 2x3 subplots
    mm = 1 / 25.4
    fig, axes = plt.subplots(2, 3, figsize=(150*mm, 100*mm), facecolor='w', edgecolor='k')
    axes = axes.flatten()

    for subplot_idx, (combo_key, combo_label) in enumerate(selected_combinations):
        ax = axes[subplot_idx]

        if combo_key not in community_data:
            print(f"Warning: {combo_key} not found in data")
            continue

        combo_data = community_data[combo_key]
        print(f"\nProcessing {combo_key} with {len(combo_data)} replicates...")

        # Collect data across all replicates
        all_species_dominance = []
        all_community_dominance = []

        # Process each replicate
        for rep_key in combo_data.keys():
            rep_data = combo_data[rep_key]

            # Extract community compositions
            # c1 and c2 are the two parent communities
            # c1_c2 is the mixed/coalesced community
            c1 = np.array(rep_data['sc_list']['c1'])
            c2 = np.array(rep_data['sc_list']['c2'])
            c_mix = np.array(rep_data['cc_list']['c1_c2'])

            # Extract LV parameters from the parameters section
            params = rep_data['parameters']
            # The interaction_matrix is a full 48x48 matrix
            # We need to find which species are dominant in c1 and c2
            # and get their interaction coefficients
            interaction_matrix = params['interaction_matrix']

            # Find the dominant species in each community
            c1_dominant_idx = np.argmax(c1)
            c2_dominant_idx = np.argmax(c2)

            # Get the interaction coefficients between dominant species
            # alpha_12 is how species 2 (c2_dominant) affects species 1 (c1_dominant)
            # alpha_21 is how species 1 (c1_dominant) affects species 2 (c2_dominant)
            alpha_12 = interaction_matrix[c1_dominant_idx][c2_dominant_idx]
            alpha_21 = interaction_matrix[c2_dominant_idx][c1_dominant_idx]
            K1 = 1.0
            K2 = 1.0

            # Calculate vector decomposition
            try:
                u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)
            except (np.linalg.LinAlgError, ValueError):
                # Skip if vector decomposition fails (singular matrix or other errors)
                continue

            # Skip if any values are NaN or inf
            if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                continue

            # FILTER: Only consider cases where u²+v² > 0.5 (substantial mixing)
            mixing_strength = u**2 + v**2
            if mixing_strength <= 0.5:
                continue

            # Calculate community-level dominance (arctan normalized)
            community_dominance = np.arctan(u / (v + 1e-8)) / (np.pi / 2)

            # Skip if community dominance is NaN or inf
            if np.isnan(community_dominance) or np.isinf(community_dominance):
                continue

            # Calculate species-level dominance from LV equilibrium
            lv_dominance = calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2)

            # Apply arctan normalization to species dominance
            # Convert from proportion to arctan normalized
            ratio = lv_dominance / (1 - lv_dominance + 1e-8)
            species_dominance = np.arctan(ratio) / (np.pi / 2)

            # Skip if species dominance is NaN or inf
            if np.isnan(species_dominance) or np.isinf(species_dominance):
                continue

            all_species_dominance.append(species_dominance)
            all_community_dominance.append(community_dominance)

        # Convert to arrays
        x = np.array(all_species_dominance)
        y = np.array(all_community_dominance)

        print(f"  {combo_key}: {len(x)} data points after filtering")

        if len(x) == 0:
            print(f"  Warning: No data points for {combo_key}")
            continue

        # Store original before duplication
        x_original = x.copy()
        y_original = y.copy()

        # Duplicate data points for symmetry
        x = np.concatenate((x, 1-x))
        y = np.concatenate((y, 1-y))

        # Calculate regression using ALL points
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        # Plot duplicated points (grey, transparent)
        x_duplicated = 1 - x_original
        y_duplicated = 1 - y_original
        ax.scatter(x_duplicated, y_duplicated, color='grey', s=2, alpha=0.2, zorder=1)

        # Plot original points (colored)
        ax.scatter(x_original, y_original, color='C0', s=2, alpha=0.5, zorder=2)

        # Add regression line
        ax.plot([0, 1], slope * np.array([0, 1]) + intercept,
                color='black', alpha=0.8, linewidth=1, zorder=3)

        # Add R² annotation
        ax.text(0.05, 0.95, f'$R^2$ = {r_squared:.2f}',
                transform=ax.transAxes, fontsize=8, verticalalignment='top')

        # Set title
        ax.set_title(combo_label, fontsize=9)

        # Set axis properties
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])

        # Add axis labels for bottom and left plots
        if subplot_idx >= 3:  # Bottom row
            ax.set_xlabel('Species Dominance', fontsize=8)
        if subplot_idx % 3 == 0:  # Left column
            ax.set_ylabel('Community Dominance', fontsize=8)

        print(f"  {combo_key}: R² = {r_squared:.3f}, slope = {slope:.3f}, {len(x_original)} points")

    plt.tight_layout()
    output_file = 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_100reps_grid_Subplots.svg'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Saved: {output_file}")

if __name__ == '__main__':
    plot_100reps_grid_correlation_subplots()
    print("\nAnalysis complete!")
