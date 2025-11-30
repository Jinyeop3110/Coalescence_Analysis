#!/usr/bin/env python3
"""
Generate R² heatmap for 100reps mean_std_grid data

Purpose: Calculate and visualize R² values for species vs community dominance correlation
         across all mean/std combinations as a heatmap
Output:
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_100reps_grid_R2_Heatmap.svg
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

def calculate_r2_for_combination(combo_data):
    """Calculate R² for a single mean/std combination."""

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

        all_species_dominance.append(species_dominance)
        all_community_dominance.append(community_dominance)

    # Calculate R² if we have enough data
    if len(all_species_dominance) < 5:
        return np.nan, 0

    x = np.array(all_species_dominance)
    y = np.array(all_community_dominance)

    # Duplicate data points for symmetry
    x = np.concatenate((x, 1-x))
    y = np.concatenate((y, 1-y))

    # Calculate R²
    try:
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared, len(all_species_dominance)
    except:
        return np.nan, len(all_species_dominance)

def plot_r2_heatmap():
    """Generate R² heatmap for all mean/std combinations."""

    # Load data
    json_file = 'Simulation_Data/mean_std_grid_100reps/Community_mean_std_grid_100reps.json'

    with open(json_file, 'r') as f:
        community_data = json.load(f)

    print(f"Loaded 100reps grid data with {len(community_data)} mean/std combinations")

    # Parse all combinations to extract unique mean and std values
    mean_values = set()
    std_values = set()

    for combo_key in community_data.keys():
        # Parse "mean0.10_std0.20" format
        parts = combo_key.split('_')
        mean_val = float(parts[0].replace('mean', ''))
        std_val = float(parts[1].replace('std', ''))
        mean_values.add(mean_val)
        std_values.add(std_val)

    mean_values = sorted(list(mean_values))
    std_values = sorted(list(std_values))

    print(f"Mean values: {mean_values}")
    print(f"Std values: {std_values}")

    # Create R² matrix
    r2_matrix = np.zeros((len(std_values), len(mean_values)))
    n_points_matrix = np.zeros((len(std_values), len(mean_values)))

    # Calculate R² for each combination
    for i, std_val in enumerate(std_values):
        for j, mean_val in enumerate(mean_values):
            combo_key = f'mean{mean_val:.2f}_std{std_val:.2f}'

            if combo_key in community_data:
                print(f"Processing {combo_key}...")
                try:
                    r2, n_points = calculate_r2_for_combination(community_data[combo_key])
                    r2_matrix[i, j] = r2
                    n_points_matrix[i, j] = n_points
                    print(f"  {combo_key}: R² = {r2:.3f}, n = {n_points}")
                except Exception as e:
                    print(f"  {combo_key}: Failed - {e}")
                    r2_matrix[i, j] = np.nan
                    n_points_matrix[i, j] = 0
            else:
                print(f"  {combo_key}: Not found in data")
                r2_matrix[i, j] = np.nan
                n_points_matrix[i, j] = 0

    # Create heatmap
    mm = 1 / 25.4
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(180*mm, 80*mm), facecolor='w')

    # Plot R² heatmap
    im1 = ax1.imshow(r2_matrix, cmap='viridis', aspect='auto', origin='lower',
                     vmin=0, vmax=1, interpolation='nearest')

    ax1.set_xticks(range(len(mean_values)))
    ax1.set_yticks(range(len(std_values)))
    ax1.set_xticklabels([f'{v:.1f}' for v in mean_values])
    ax1.set_yticklabels([f'{v:.1f}' for v in std_values])
    ax1.set_xlabel('Mean Interaction Strength (μ)', fontsize=10)
    ax1.set_ylabel('Std Interaction Strength (σ)', fontsize=10)
    ax1.set_title('R² Values', fontsize=11)

    # Add R² values as text
    for i in range(len(std_values)):
        for j in range(len(mean_values)):
            if not np.isnan(r2_matrix[i, j]):
                text_color = 'white' if r2_matrix[i, j] < 0.5 else 'black'
                ax1.text(j, i, f'{r2_matrix[i, j]:.2f}',
                        ha='center', va='center', color=text_color, fontsize=7)

    # Add colorbar
    cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label('R²', fontsize=9)

    # Plot sample size heatmap
    im2 = ax2.imshow(n_points_matrix, cmap='Blues', aspect='auto', origin='lower',
                     interpolation='nearest')

    ax2.set_xticks(range(len(mean_values)))
    ax2.set_yticks(range(len(std_values)))
    ax2.set_xticklabels([f'{v:.1f}' for v in mean_values])
    ax2.set_yticklabels([f'{v:.1f}' for v in std_values])
    ax2.set_xlabel('Mean Interaction Strength (μ)', fontsize=10)
    ax2.set_ylabel('Std Interaction Strength (σ)', fontsize=10)
    ax2.set_title('Sample Size (n)', fontsize=11)

    # Add sample sizes as text
    for i in range(len(std_values)):
        for j in range(len(mean_values)):
            if n_points_matrix[i, j] > 0:
                text_color = 'white' if n_points_matrix[i, j] > 50 else 'black'
                ax2.text(j, i, f'{int(n_points_matrix[i, j])}',
                        ha='center', va='center', color=text_color, fontsize=7)

    # Add colorbar
    cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    cbar2.set_label('Number of Points', fontsize=9)

    plt.tight_layout()

    output_file = 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_100reps_grid_R2_Heatmap.svg'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Saved: {output_file}")

    # Print summary statistics
    print("\n=== Summary Statistics ===")
    valid_r2 = r2_matrix[~np.isnan(r2_matrix)]
    print(f"Mean R²: {np.mean(valid_r2):.3f}")
    print(f"Median R²: {np.median(valid_r2):.3f}")
    print(f"Min R²: {np.min(valid_r2):.3f}")
    print(f"Max R²: {np.max(valid_r2):.3f}")
    print(f"Std R²: {np.std(valid_r2):.3f}")

if __name__ == '__main__':
    plot_r2_heatmap()
    print("\nAnalysis complete!")
