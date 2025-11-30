#!/usr/bin/env python3
"""
Generate correlation plots for mean_uniform_grid_100reps data

Purpose: Plot species-level dominance vs community-level dominance for uniform distribution data
         across different mean interaction strengths (μ = 0.0 to 1.2)

Output:
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_mean_uniform_grid_Subplots.svg
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

def plot_mean_uniform_grid_correlation_subplots():
    """Plot correlation for mean_uniform_grid data as subplots (μ = 0.1 to 1.2)."""

    # Load data
    json_file = 'Simulation_Data/mean_uniform_grid_100reps/Community_mean_uniform_grid_100reps.json'

    with open(json_file, 'r') as f:
        community_data = json.load(f)

    print(f"Loaded mean_uniform_grid_100reps data with {len(community_data)} mean combinations")

    # Parse all mean values from the data
    mean_values = set()
    for combo_key in community_data.keys():
        # Parse "mean0.10" format
        mean_val = float(combo_key.replace('mean', ''))
        mean_values.add(mean_val)

    mean_values = sorted(list(mean_values))
    print(f"Mean values found: {mean_values}")

    # Select mean values from 0.1 to 1.2
    selected_means = [m for m in mean_values if 0.1 <= m <= 1.2]
    print(f"Selected means (0.1-1.2): {selected_means}")

    # Setup figure with 3x4 subplots (12 panels for means 0.1 to 1.2)
    mm = 1 / 25.4
    fig, axes = plt.subplots(3, 4, figsize=(180*mm, 135*mm), facecolor='w', edgecolor='k')
    axes = axes.flatten()

    for subplot_idx, mean_val in enumerate(selected_means):
        if subplot_idx >= len(axes):
            break

        ax = axes[subplot_idx]
        combo_key = f'mean{mean_val:.2f}'

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
            c1 = np.array(rep_data['sc_list']['c1'])
            c2 = np.array(rep_data['sc_list']['c2'])
            c_mix = np.array(rep_data['cc_list']['c1_c2'])

            # Extract LV parameters
            params = rep_data['parameters']
            interaction_matrix = params['interaction_matrix']

            # Find dominant species
            c1_dominant_idx = np.argmax(c1)
            c2_dominant_idx = np.argmax(c2)

            # Get interaction coefficients
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
        ax.set_title(f'μ={mean_val:.1f}', fontsize=9)

        # Set axis properties
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])

        # Add axis labels for bottom and left plots
        if subplot_idx >= 8:  # Bottom row
            ax.set_xlabel('Species Dominance', fontsize=8)
        if subplot_idx % 4 == 0:  # Left column
            ax.set_ylabel('Community Dominance', fontsize=8)

        print(f"  {combo_key}: R² = {r_squared:.3f}, slope = {slope:.3f}, {len(x_original)} points")

    plt.tight_layout()
    output_file = 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_mean_uniform_grid_Subplots.svg'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Saved: {output_file}")

if __name__ == '__main__':
    plot_mean_uniform_grid_correlation_subplots()
    print("\nAnalysis complete!")
