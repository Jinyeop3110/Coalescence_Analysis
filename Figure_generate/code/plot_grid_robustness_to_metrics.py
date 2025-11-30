#!/usr/bin/env python3
"""
Generate R² and Revert Ratio heatmaps for mean_std_grid data (flexible for any n_reps)

Purpose: Calculate and visualize both R² values and revert ratios across parameter space.
         Works with checkpoint files or final data files.
         Handles missing or incomplete data gracefully.

Usage:
  python plot_grid_robustness_to_metrics.py [data_file]

  If no file specified, will use latest checkpoint from 500reps simulation

Output:
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_[n]reps_grid_R2_Heatmap.svg
  - Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_[n]reps_grid_Revert_Ratio_Heatmap.svg
"""

from common_setup import *
import json
import numpy as np
import sys
import os
import glob

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

def calculate_metrics_for_combination(combo_data):
    """Calculate both R² and revert ratio for a single mean/std combination.

    Returns:
        r2: R² value (or np.nan if insufficient data)
        revert_ratio: Fraction of mismatched predictions (or np.nan if insufficient data)
        n_points: Number of valid data points
    """

    all_species_dominance = []
    all_community_dominance = []
    revert_count = 0

    # Process each replicate
    for rep_key in combo_data.keys():
        rep_data = combo_data[rep_key]

        # Skip if this replicate doesn't have the required data
        if 'sc_list' not in rep_data or 'cc_list' not in rep_data or 'parameters' not in rep_data:
            continue

        # Extract community compositions
        try:
            c1 = np.array(rep_data['sc_list']['c1'])
            c2 = np.array(rep_data['sc_list']['c2'])
            c_mix = np.array(rep_data['cc_list']['c1_c2'])
        except KeyError:
            continue

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

        # Valid data point - add to lists
        all_species_dominance.append(species_dominance)
        all_community_dominance.append(community_dominance)

        # Check if this is a revert case
        species_predicts_c1 = species_dominance > 0.5
        community_shows_c1 = community_dominance > 0.5
        if species_predicts_c1 != community_shows_c1:
            revert_count += 1

    # Calculate metrics if we have enough data
    n_points = len(all_species_dominance)

    if n_points < 5:
        return np.nan, np.nan, 0

    # Calculate R²
    x = np.array(all_species_dominance)
    y = np.array(all_community_dominance)

    # Duplicate data points for symmetry
    x_full = np.concatenate((x, 1-x))
    y_full = np.concatenate((y, 1-y))

    try:
        slope, intercept = np.polyfit(x_full, y_full, 1)
        y_pred = slope * x_full + intercept
        ss_res = np.sum((y_full - y_pred) ** 2)
        ss_tot = np.sum((y_full - np.mean(y_full)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
    except:
        r2 = np.nan

    # Calculate revert ratio
    revert_ratio = revert_count / n_points

    return r2, revert_ratio, n_points

def plot_heatmaps(data_file):
    """Generate both R² and Revert Ratio heatmaps."""

    # Load data
    print(f"Loading data from {data_file}...")

    try:
        with open(data_file, 'r') as f:
            community_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Checkpoint file is corrupted or incomplete: {e}")
        print("Try using an earlier checkpoint or wait for simulation to complete.")
        return

    print(f"Loaded grid data with {len(community_data)} mean/std combinations")

    # Determine n_reps from filename
    if '100reps' in data_file:
        n_reps = 100
    elif '500reps' in data_file:
        n_reps = 500
    elif 'checkpoint' in data_file:
        # Extract from path
        n_reps = int(data_file.split('_')[-2].replace('reps', ''))
    else:
        n_reps = 'unknown'

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

    # Create matrices
    r2_matrix = np.zeros((len(std_values), len(mean_values)))
    revert_matrix = np.zeros((len(std_values), len(mean_values)))
    n_points_matrix = np.zeros((len(std_values), len(mean_values)))

    # Calculate metrics for each combination
    for i, std_val in enumerate(std_values):
        for j, mean_val in enumerate(mean_values):
            combo_key = f'mean{mean_val:.2f}_std{std_val:.2f}'

            if combo_key in community_data:
                print(f"Processing {combo_key}...")
                try:
                    r2, revert_ratio, n_points = calculate_metrics_for_combination(community_data[combo_key])
                    r2_matrix[i, j] = r2
                    revert_matrix[i, j] = revert_ratio
                    n_points_matrix[i, j] = n_points

                    if not np.isnan(r2):
                        print(f"  {combo_key}: R² = {r2:.3f}, Revert = {revert_ratio:.3f}, n = {n_points}")
                    else:
                        print(f"  {combo_key}: Insufficient data (n = {n_points})")

                except Exception as e:
                    print(f"  {combo_key}: Failed - {e}")
                    r2_matrix[i, j] = np.nan
                    revert_matrix[i, j] = np.nan
                    n_points_matrix[i, j] = 0
            else:
                print(f"  {combo_key}: Not found in data")
                r2_matrix[i, j] = np.nan
                revert_matrix[i, j] = np.nan
                n_points_matrix[i, j] = 0

    # Plot R² heatmap
    print("\n" + "="*60)
    print("Generating R² heatmap...")
    print("="*60)

    mm = 1 / 25.4
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(180*mm, 80*mm), facecolor='w')

    # Plot R² values
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

    cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label('R²', fontsize=9)

    # Plot sample sizes
    im2 = ax2.imshow(n_points_matrix, cmap='Blues', aspect='auto', origin='lower',
                     interpolation='nearest')

    ax2.set_xticks(range(len(mean_values)))
    ax2.set_yticks(range(len(std_values)))
    ax2.set_xticklabels([f'{v:.1f}' for v in mean_values])
    ax2.set_yticklabels([f'{v:.1f}' for v in std_values])
    ax2.set_xlabel('Mean Interaction Strength (μ)', fontsize=10)
    ax2.set_ylabel('Std Interaction Strength (σ)', fontsize=10)
    ax2.set_title('Sample Size (n)', fontsize=11)

    for i in range(len(std_values)):
        for j in range(len(mean_values)):
            if n_points_matrix[i, j] > 0:
                text_color = 'white' if n_points_matrix[i, j] > 50 else 'black'
                ax2.text(j, i, f'{int(n_points_matrix[i, j])}',
                        ha='center', va='center', color=text_color, fontsize=7)

    cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    cbar2.set_label('Number of Points', fontsize=9)

    plt.tight_layout()

    r2_output = f'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_{n_reps}reps_grid_R2_Heatmap.svg'
    plt.savefig(r2_output, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Saved: {r2_output}")

    # Print R² statistics
    print("\n=== R² Summary Statistics ===")
    valid_r2 = r2_matrix[~np.isnan(r2_matrix)]
    if len(valid_r2) > 0:
        print(f"Mean R²: {np.mean(valid_r2):.3f}")
        print(f"Median R²: {np.median(valid_r2):.3f}")
        print(f"Min R²: {np.min(valid_r2):.3f}")
        print(f"Max R²: {np.max(valid_r2):.3f}")
        print(f"Std R²: {np.std(valid_r2):.3f}")
        print(f"Valid combinations: {len(valid_r2)}/{r2_matrix.size}")
    else:
        print("No valid R² values computed")

    # Plot Revert Ratio heatmap
    print("\n" + "="*60)
    print("Generating Revert Ratio heatmap...")
    print("="*60)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(180*mm, 80*mm), facecolor='w')

    # Plot revert ratio values
    im1 = ax1.imshow(revert_matrix, cmap='RdYlGn_r', aspect='auto', origin='lower',
                     vmin=0, vmax=1, interpolation='nearest')

    ax1.set_xticks(range(len(mean_values)))
    ax1.set_yticks(range(len(std_values)))
    ax1.set_xticklabels([f'{v:.1f}' for v in mean_values])
    ax1.set_yticklabels([f'{v:.1f}' for v in std_values])
    ax1.set_xlabel('Mean Interaction Strength (μ)', fontsize=10)
    ax1.set_ylabel('Std Interaction Strength (σ)', fontsize=10)
    ax1.set_title('Revert Ratio (Mismatch Fraction)', fontsize=11)

    for i in range(len(std_values)):
        for j in range(len(mean_values)):
            if not np.isnan(revert_matrix[i, j]):
                text_color = 'white' if revert_matrix[i, j] > 0.5 else 'black'
                ax1.text(j, i, f'{revert_matrix[i, j]:.2f}',
                        ha='center', va='center', color=text_color, fontsize=7)

    cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label('Revert Ratio', fontsize=9)

    # Plot sample sizes (same as R² plot)
    im2 = ax2.imshow(n_points_matrix, cmap='Blues', aspect='auto', origin='lower',
                     interpolation='nearest')

    ax2.set_xticks(range(len(mean_values)))
    ax2.set_yticks(range(len(std_values)))
    ax2.set_xticklabels([f'{v:.1f}' for v in mean_values])
    ax2.set_yticklabels([f'{v:.1f}' for v in std_values])
    ax2.set_xlabel('Mean Interaction Strength (μ)', fontsize=10)
    ax2.set_ylabel('Std Interaction Strength (σ)', fontsize=10)
    ax2.set_title('Sample Size (n)', fontsize=11)

    for i in range(len(std_values)):
        for j in range(len(mean_values)):
            if n_points_matrix[i, j] > 0:
                text_color = 'white' if n_points_matrix[i, j] > 50 else 'black'
                ax2.text(j, i, f'{int(n_points_matrix[i, j])}',
                        ha='center', va='center', color=text_color, fontsize=7)

    cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    cbar2.set_label('Number of Points', fontsize=9)

    plt.tight_layout()

    revert_output = f'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_{n_reps}reps_grid_Revert_Ratio_Heatmap.svg'
    plt.savefig(revert_output, bbox_inches='tight')
    plt.close()

    print(f"\n✅ Saved: {revert_output}")

    # Print Revert Ratio statistics
    print("\n=== Revert Ratio Summary Statistics ===")
    valid_revert = revert_matrix[~np.isnan(revert_matrix)]
    if len(valid_revert) > 0:
        print(f"Mean Revert Ratio: {np.mean(valid_revert):.3f}")
        print(f"Median Revert Ratio: {np.median(valid_revert):.3f}")
        print(f"Min Revert Ratio: {np.min(valid_revert):.3f}")
        print(f"Max Revert Ratio: {np.max(valid_revert):.3f}")
        print(f"Std Revert Ratio: {np.std(valid_revert):.3f}")
        print(f"Valid combinations: {len(valid_revert)}/{revert_matrix.size}")
    else:
        print("No valid Revert Ratio values computed")

if __name__ == '__main__':
    # Determine which data file to use
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        # Find latest checkpoint from 500reps
        checkpoint_dir = 'Simulation_Data/mean_std_grid_500reps'
        checkpoints = glob.glob(f'{checkpoint_dir}/checkpoint_*.json')

        if checkpoints:
            # Get the checkpoint with highest number (most recent)
            checkpoints.sort(key=lambda x: int(x.split('_')[-1].replace('.json', '')))
            data_file = checkpoints[-1]
            print(f"Using latest checkpoint: {data_file}")
        else:
            # Default to 100reps
            data_file = 'Simulation_Data/mean_std_grid_100reps/Community_mean_std_grid_100reps.json'
            print(f"No checkpoints found, using: {data_file}")

    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        sys.exit(1)

    plot_heatmaps(data_file)
    print("\nAnalysis complete!")
