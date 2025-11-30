"""
AsymmetricityNullModelAnalysis_simulation.py - Null Model Analysis for Simulation Data

This module performs asymmetricity null model analysis on simulation data,
similar to the analysis done on experimental data in AsymmetricityNullModelAnalysis.py.

It analyzes coalescence simulations across different interaction strengths and
compares observed asymmetricity patterns with null model expectations.

Two null models are implemented:
1. Neutral Mixing: Tests whether asymmetricity arises from neutral mixing processes
2. Random Selection: Tests whether diversity asymmetricity is due to differential species retention

Output directory: Figure/AsymmetricityNullModelAnalysis_simulation/

Author: Gore Lab Coalescence Analysis Team
Date: January 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib to non-interactive backend
plt.ioff()
import matplotlib
matplotlib.use('Agg')

# Import existing analysis functions
from AsymmetricityAnalysis import (
    analyze_single_coalescence_asymmetricity
)

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_simulation_coalescence_data(simulation_dir, interaction_strengths=None):
    """
    Load simulation coalescence data from JSON files.

    Args:
        simulation_dir: Path to simulation data directory
        interaction_strengths: List of mean interaction strengths to analyze
                             If None, analyzes all available strengths

    Returns:
        offspring_list: List of offspring community vectors
        parent1_list: List of parent1 community vectors
        parent2_list: List of parent2 community vectors
        interaction_conditions: List of interaction strength labels
        metadata: Dict with additional metadata
    """
    print(f"Loading simulation data from {simulation_dir}...")

    simulation_path = Path(simulation_dir)

    # Try to find the Community JSON file
    json_files = list(simulation_path.glob("Community_*.json"))

    if not json_files:
        print(f"No Community JSON files found in {simulation_dir}")
        return None, None, None, None, None

    # Use the first JSON file found (or coalescence if available)
    coalescence_files = [f for f in json_files if 'coalescence' in f.name.lower()]
    if coalescence_files:
        json_file = coalescence_files[0]
    else:
        json_file = json_files[0]

    print(f"Loading from: {json_file}")

    with open(json_file, 'r') as f:
        data = json.load(f)

    offspring_list = []
    parent1_list = []
    parent2_list = []
    interaction_conditions = []

    print(f"Loaded {len(data)} parameter combinations")

    # Extract all mean values if not specified
    if interaction_strengths is None:
        interaction_strengths = []
        for combo_key in data.keys():
            try:
                # Keys can be float values directly (e.g., '0.3', '0.5', '0.8')
                # or formatted strings (e.g., 'mean0.20_std0.10')
                if 'mean' in combo_key:
                    mean_str = combo_key.split('_')[0].replace('mean', '')
                    interaction_strengths.append(float(mean_str))
                else:
                    # Try to parse as direct float
                    interaction_strengths.append(float(combo_key))
            except:
                continue
        interaction_strengths = sorted(list(set(interaction_strengths)))
        print(f"Found interaction strengths: {interaction_strengths}")

    # Process each parameter combination
    for combo_key in data.keys():
        # Check if this combo matches one of our target interaction strengths
        mean_val = None

        # Try different key formats
        try:
            # Direct float key (e.g., '0.3')
            key_float = float(combo_key)
            if key_float in interaction_strengths:
                mean_val = key_float
        except:
            # String key with 'mean' prefix (e.g., 'mean0.20_std0.10')
            for strength in interaction_strengths:
                if f'mean{strength:.2f}_' in combo_key or f'mean{strength:.1f}_' in combo_key:
                    mean_val = strength
                    break

        if mean_val is None:
            continue

        combo_data = data[combo_key]

        # Process each replicate
        for rep_key in combo_data.keys():
            try:
                rep_data = combo_data[rep_key]

                # Extract parent communities and offspring
                # Structure has sc_list with numeric keys ('0', '1', '2', '3')
                # and cc_list with pair keys ('0_1', '0_2', '1_2', etc.)
                if 'sc_list' in rep_data and 'cc_list' in rep_data:
                    sc_list = rep_data['sc_list']
                    cc_list = rep_data['cc_list']

                    # Get all single communities (sc_list keys)
                    sc_keys = [k for k in sc_list.keys() if k.isdigit()]

                    # Get all coalescence pairs (cc_list keys)
                    cc_keys = [k for k in cc_list.keys() if '_' in k]

                    # Process each coalescence pair
                    for cc_key in cc_keys:
                        try:
                            # Parse parent indices from key like '0_1'
                            parent_indices = cc_key.split('_')
                            if len(parent_indices) != 2:
                                continue

                            idx1, idx2 = parent_indices[0], parent_indices[1]

                            # Get parent communities
                            if idx1 in sc_list and idx2 in sc_list:
                                c1 = np.array(sc_list[idx1])
                                c2 = np.array(sc_list[idx2])
                                c_mix = np.array(cc_list[cc_key])

                                # Validate data
                                if len(c1) > 0 and len(c2) > 0 and len(c_mix) > 0:
                                    # Normalize
                                    c1 = c1 / np.sum(c1) if np.sum(c1) > 0 else c1
                                    c2 = c2 / np.sum(c2) if np.sum(c2) > 0 else c2
                                    c_mix = c_mix / np.sum(c_mix) if np.sum(c_mix) > 0 else c_mix

                                    # Filter out communities with too few species
                                    if np.sum(c_mix > 0) >= 3:
                                        parent1_list.append(c1)
                                        parent2_list.append(c2)
                                        offspring_list.append(c_mix)
                                        interaction_conditions.append(f'mean_{mean_val:.2f}')
                        except Exception as e:
                            continue

            except Exception as e:
                continue

    print(f"Successfully loaded {len(offspring_list)} coalescence events")
    if len(offspring_list) > 0:
        # Count by interaction strength
        from collections import Counter
        condition_counts = Counter(interaction_conditions)
        for condition, count in sorted(condition_counts.items()):
            print(f"  {condition}: {count} events")

    metadata = {
        'interaction_strengths': interaction_strengths,
        'simulation_dir': str(simulation_dir),
        'data_file': str(json_file)
    }

    return offspring_list, parent1_list, parent2_list, interaction_conditions, metadata

# =============================================================================
# NULL MODEL GENERATORS (same as experimental analysis)
# =============================================================================

def generate_random_selection_null(parent1_list, parent2_list, interaction_conditions,
                                 n_permutations=1000, selection_prob=0.5):
    """
    Generate null model where each species has equal probability of being selected.

    For simulations, we use a uniform selection probability since we don't have
    nutrient conditions.
    """
    null_offspring_list = []
    null_parent1_list = []
    null_parent2_list = []

    for _ in range(n_permutations):
        # Randomly select parent pair
        idx = np.random.randint(0, len(parent1_list))
        p1 = parent1_list[idx].copy()
        p2 = parent2_list[idx].copy()

        # Combine parent communities to get total species pool
        combined = p1 + p2

        # Each species is selected with probability selection_prob
        n_species = len(combined)
        selection_mask = np.random.binomial(1, selection_prob, n_species).astype(bool)

        # Create offspring with only selected species
        offspring = np.zeros(n_species)
        if np.any(selection_mask):
            # Selected species get random abundances
            offspring[selection_mask] = np.random.exponential(1, np.sum(selection_mask))
            offspring = offspring / np.sum(offspring)

        null_offspring_list.append(offspring)
        null_parent1_list.append(p1)
        null_parent2_list.append(p2)

    return null_offspring_list, null_parent1_list, null_parent2_list

def generate_neutral_mixing_null(parent1_list, parent2_list, n_permutations=1000):
    """
    Generate null model assuming perfect neutral mixing without interactions.
    Offspring = α*Parent1 + (1-α)*Parent2 where α is randomly sampled.
    """
    null_offspring_list = []
    null_parent1_list = []
    null_parent2_list = []

    for _ in range(n_permutations):
        # Randomly select parent pair
        idx = np.random.randint(0, len(parent1_list))
        p1 = parent1_list[idx].copy()
        p2 = parent2_list[idx].copy()

        # Random mixing coefficient
        alpha = np.random.uniform(0, 1)

        # Create neutral mixture
        offspring = alpha * p1 + (1 - alpha) * p2
        offspring = offspring / np.sum(offspring) if np.sum(offspring) > 0 else offspring

        null_offspring_list.append(offspring)
        null_parent1_list.append(p1)
        null_parent2_list.append(p2)

    return null_offspring_list, null_parent1_list, null_parent2_list

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_experimental_asymmetricity(offspring_list, parent1_list, parent2_list,
                                     interaction_conditions,
                                     similarity_metrics=['bray_curtis', 'jensen_shannon'],
                                     diversity_threshold=1e-3, threshold=0):
    """
    Calculate asymmetricity metrics for given data.
    """
    results = {
        'similarity_asymmetricity': {metric: [] for metric in similarity_metrics},
        'vector_asymmetricity': [],
        'diversity_asymmetricity_type1': [],
        'diversity_asymmetricity_type2': [],
        'retention_asymmetricity_type1': [],
        'retention_asymmetricity_type2': [],
        'interaction_conditions': interaction_conditions
    }

    for i, (offspring, parent1, parent2) in enumerate(zip(offspring_list, parent1_list, parent2_list)):
        try:
            # Use the comprehensive analysis function from AsymmetricityAnalysis
            asym_results = analyze_single_coalescence_asymmetricity(
                offspring, parent1, parent2,
                similarity_metrics=similarity_metrics,
                diversity_threshold=diversity_threshold,
                threshold=threshold
            )

            # Extract results
            for metric in similarity_metrics:
                results['similarity_asymmetricity'][metric].append(
                    asym_results['similarity'][metric] if 'similarity' in asym_results else np.nan
                )

            results['vector_asymmetricity'].append(
                asym_results.get('vector', np.nan)
            )
            results['diversity_asymmetricity_type1'].append(
                asym_results.get('diversity_type1', np.nan)
            )
            results['diversity_asymmetricity_type2'].append(
                asym_results.get('diversity_type2', np.nan)
            )
            results['retention_asymmetricity_type1'].append(
                asym_results.get('retention_type1', np.nan)
            )
            results['retention_asymmetricity_type2'].append(
                asym_results.get('retention_type2', np.nan)
            )

        except Exception as e:
            # Handle invalid cases
            for metric in similarity_metrics:
                results['similarity_asymmetricity'][metric].append(np.nan)
            results['vector_asymmetricity'].append(np.nan)
            results['diversity_asymmetricity_type1'].append(np.nan)
            results['diversity_asymmetricity_type2'].append(np.nan)
            results['retention_asymmetricity_type1'].append(np.nan)
            results['retention_asymmetricity_type2'].append(np.nan)

    return results

def analyze_asymmetricity_with_null_models(offspring_list, parent1_list, parent2_list,
                                         interaction_conditions,
                                         similarity_metrics=['bray_curtis', 'jensen_shannon'],
                                         diversity_threshold=1e-3,
                                         n_permutations=1000,
                                         threshold=0):
    """
    Analyze asymmetricity patterns compared to multiple null models.
    """
    print("Analyzing experimental asymmetricity...")

    # Calculate experimental asymmetricity
    exp_results = analyze_experimental_asymmetricity(
        offspring_list, parent1_list, parent2_list, interaction_conditions,
        similarity_metrics, diversity_threshold, threshold
    )

    print("Generating null models...")

    # Generate null models
    null_models = {}

    # Neutral mixing model
    print("Generating neutral mixing null model...")
    null_models['neutral_mixing'] = generate_neutral_mixing_null(
        parent1_list, parent2_list, n_permutations
    )

    # Random selection model
    print("Generating random selection null model...")
    null_models['random_selection'] = generate_random_selection_null(
        parent1_list, parent2_list, interaction_conditions, n_permutations
    )

    # Analyze each null model
    null_results = {}
    for null_name, (null_offspring, null_parent1, null_parent2) in null_models.items():
        print(f"Analyzing {null_name} null model...")

        # Create dummy conditions for null model
        null_conditions = ['NULL'] * len(null_offspring)

        null_results[null_name] = analyze_experimental_asymmetricity(
            null_offspring, null_parent1, null_parent2, null_conditions,
            similarity_metrics, diversity_threshold, threshold
        )

    return exp_results, null_results

# =============================================================================
# PLOTTING FUNCTIONS
# =============================================================================

def plot_diversity_vs_random_selection(exp_results, null_results, save_path=None):
    """
    Plot diversity asymmetricity vs random selection for simulation data.
    """
    interaction_strengths = sorted(list(set(exp_results['interaction_conditions'])))
    diversity_types = ['diversity_asymmetricity_type1', 'diversity_asymmetricity_type2']

    fig, axes = plt.subplots(2, 1, figsize=(20, 12))

    for i, div_type in enumerate(diversity_types):
        ax = axes[i]

        # Prepare data for plotting
        plot_data = []
        plot_labels = []

        for condition in interaction_strengths:
            # Find experimental data for this condition
            exp_indices = [k for k, c in enumerate(exp_results['interaction_conditions'])
                          if c == condition]
            exp_values = [exp_results[div_type][k] for k in exp_indices]
            exp_values = [v for v in exp_values if not np.isnan(v)]

            # Null model data
            if 'random_selection' in null_results:
                null_values = [v for v in null_results['random_selection'][div_type]
                              if not np.isnan(v)]

                if exp_values and null_values:
                    plot_data.extend([exp_values, null_values])
                    plot_labels.extend([f'Exp {condition}', f'Null {condition}'])

        # Create box plot with scatter
        if plot_data:
            positions = range(len(plot_data))

            # Create box plots
            box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True,
                                 showfliers=False, widths=0.6)

            # Color experimental data differently from null
            for k, patch in enumerate(box_parts['boxes']):
                if k % 2 == 0:  # Experimental data
                    patch.set_facecolor('#1f77b4')
                    patch.set_alpha(0.7)
                else:  # Null data
                    patch.set_facecolor('#ff7f0e')
                    patch.set_alpha(0.7)

            # Add scatter points
            for k, data in enumerate(plot_data):
                # Subsample if too many points
                if len(data) > 100:
                    data_sample = np.random.choice(data, 100, replace=False)
                else:
                    data_sample = data

                # Add jitter to x-positions
                x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))

                if k % 2 == 0:  # Experimental data
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8,
                             color='#1f77b4', edgecolors='white', linewidth=0.5)
                else:  # Null data
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8,
                             color='#ff7f0e', edgecolors='white', linewidth=0.5)

            # Statistical significance annotations
            y_min, y_max = ax.get_ylim()
            y_range = y_max - y_min

            for k, condition in enumerate(interaction_strengths):
                exp_idx = k * 2
                null_idx = k * 2 + 1

                if exp_idx < len(plot_data) and null_idx < len(plot_data):
                    exp_vals = plot_data[exp_idx]
                    null_vals = plot_data[null_idx]

                    if len(exp_vals) > 0 and len(null_vals) > 0:
                        try:
                            statistic, p_value = stats.mannwhitneyu(
                                exp_vals, null_vals, alternative='two-sided'
                            )

                            # Position for significance annotation
                            x_pos = k * 2 + 0.5
                            y_pos = y_max + 0.05 * y_range

                            if p_value < 0.001:
                                sig_text = '***'
                            elif p_value < 0.01:
                                sig_text = '**'
                            elif p_value < 0.05:
                                sig_text = '*'
                            else:
                                sig_text = 'ns'

                            # Draw line and significance
                            ax.plot([exp_idx, null_idx], [y_pos, y_pos], 'k-', linewidth=1)
                            ax.text(x_pos, y_pos + 0.02 * y_range, sig_text,
                                   ha='center', va='bottom', fontweight='bold')
                        except:
                            pass

            ax.set_xticks(positions)
            ax.set_xticklabels(plot_labels, rotation=45, ha='right')
            ax.set_ylabel(f'{div_type.replace("_", " ").title()}')
            ax.set_title(f'{div_type.replace("_", " ").title()} vs Random Selection (Simulation Data)')

            # Add formula explanation
            if div_type == 'diversity_asymmetricity_type1':
                formula_text = "Type 1: |spp_from_p1_only - spp_from_p2_only| / (spp_from_p1_only + spp_from_p2_only)\nExcludes overlapping species"
            else:
                formula_text = "Type 2: |spp_from_p1_total - spp_from_p2_total| / (spp_from_p1_total + spp_from_p2_total)\nIncludes overlapping species (counted for both)"

            ax.text(0.98, 0.02, formula_text, transform=ax.transAxes,
                    fontsize=7, verticalalignment='bottom', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        print(f"Saved diversity vs random selection plot: {save_path}")

    plt.close()

def plot_vector_vs_neutral_mixing(exp_results, null_results, save_path=None):
    """
    Plot vector asymmetricity vs neutral mixing for simulation data.
    """
    interaction_strengths = sorted(list(set(exp_results['interaction_conditions'])))

    fig, ax = plt.subplots(1, 1, figsize=(18, 8))

    # Prepare data for plotting
    plot_data = []
    plot_labels = []

    for condition in interaction_strengths:
        # Find experimental data for this condition
        exp_indices = [k for k, c in enumerate(exp_results['interaction_conditions'])
                      if c == condition]
        exp_values = [exp_results['vector_asymmetricity'][k] for k in exp_indices]
        exp_values = [v for v in exp_values if not np.isnan(v)]

        # Neutral mixing null model data
        if 'neutral_mixing' in null_results:
            null_values = [v for v in null_results['neutral_mixing']['vector_asymmetricity']
                          if not np.isnan(v)]

            if exp_values and null_values:
                plot_data.extend([exp_values, null_values])
                plot_labels.extend([f'Exp {condition}', f'Null {condition}'])

    # Create box plot with scatter
    if plot_data:
        positions = range(len(plot_data))

        # Create box plots
        box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True,
                             showfliers=False, widths=0.6)

        # Color experimental data differently from null
        for k, patch in enumerate(box_parts['boxes']):
            if k % 2 == 0:  # Experimental data
                patch.set_facecolor('#1f77b4')
                patch.set_alpha(0.7)
            else:  # Null data
                patch.set_facecolor('#ff7f0e')
                patch.set_alpha(0.7)

        # Add scatter points
        for k, data in enumerate(plot_data):
            # Subsample if too many points
            if len(data) > 100:
                data_sample = np.random.choice(data, 100, replace=False)
            else:
                data_sample = data

            # Add jitter to x-positions
            x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))

            if k % 2 == 0:  # Experimental data
                ax.scatter(x_jitter, data_sample, alpha=0.6, s=8,
                         color='#1f77b4', edgecolors='white', linewidth=0.5)
            else:  # Null data
                ax.scatter(x_jitter, data_sample, alpha=0.6, s=8,
                         color='#ff7f0e', edgecolors='white', linewidth=0.5)

        ax.set_xticks(positions)
        ax.set_xticklabels(plot_labels, rotation=45, ha='right')
        ax.set_ylabel('Vector Asymmetricity')
        ax.set_title('Vector Asymmetricity vs Neutral Mixing (Simulation Data)')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
            print(f"Saved vector vs neutral mixing plot: {save_path}")

        plt.close()

def plot_similarity_asymmetricity(exp_results, null_results, save_path=None):
    """
    Plot similarity asymmetricity for simulation data.
    """
    interaction_strengths = sorted(list(set(exp_results['interaction_conditions'])))
    metrics = list(exp_results['similarity_asymmetricity'].keys())

    fig, axes = plt.subplots(len(metrics), 1, figsize=(18, 8 * len(metrics)))
    if len(metrics) == 1:
        axes = [axes]

    for i, metric in enumerate(metrics):
        ax = axes[i]

        # Prepare data for plotting
        plot_data = []
        plot_labels = []

        for condition in interaction_strengths:
            # Find experimental data for this condition
            exp_indices = [k for k, c in enumerate(exp_results['interaction_conditions'])
                          if c == condition]
            exp_values = [exp_results['similarity_asymmetricity'][metric][k] for k in exp_indices]
            exp_values = [v for v in exp_values if not np.isnan(v)]

            # Null model data (using neutral mixing)
            if 'neutral_mixing' in null_results:
                null_values = [v for v in null_results['neutral_mixing']['similarity_asymmetricity'][metric]
                              if not np.isnan(v)]

                if exp_values and null_values:
                    plot_data.extend([exp_values, null_values])
                    plot_labels.extend([f'Exp {condition}', f'Null {condition}'])

        # Create box plot with scatter
        if plot_data:
            positions = range(len(plot_data))

            # Create box plots
            box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True,
                                 showfliers=False, widths=0.6)

            # Color experimental data differently from null
            for k, patch in enumerate(box_parts['boxes']):
                if k % 2 == 0:  # Experimental data
                    patch.set_facecolor('#1f77b4')
                    patch.set_alpha(0.7)
                else:  # Null data
                    patch.set_facecolor('#ff7f0e')
                    patch.set_alpha(0.7)

            # Add scatter points
            for k, data in enumerate(plot_data):
                if len(data) > 100:
                    data_sample = np.random.choice(data, 100, replace=False)
                else:
                    data_sample = data

                x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))

                if k % 2 == 0:
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8,
                             color='#1f77b4', edgecolors='white', linewidth=0.5)
                else:
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8,
                             color='#ff7f0e', edgecolors='white', linewidth=0.5)

            ax.set_xticks(positions)
            ax.set_xticklabels(plot_labels, rotation=45, ha='right')
            ax.set_ylabel(f'{metric.replace("_", " ").title()} Asymmetricity')
            ax.set_title(f'{metric.replace("_", " ").title()} Asymmetricity vs Neutral Mixing (Simulation Data)')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        print(f"Saved similarity asymmetricity plot: {save_path}")

    plt.close()

# =============================================================================
# MAIN ANALYSIS FUNCTION
# =============================================================================

def run_simulation_null_model_analysis(simulation_dir, interaction_strengths=None,
                                      n_permutations=1000, save_plots=True,
                                      save_dir=None):
    """
    Run complete asymmetricity null model analysis on simulation data.

    Args:
        simulation_dir: Path to simulation data directory
        interaction_strengths: List of interaction strengths to analyze
        n_permutations: Number of permutations for null models
        save_plots: Whether to save plots
        save_dir: Directory to save plots
    """
    print("="*80)
    print("SIMULATION ASYMMETRICITY NULL MODEL ANALYSIS")
    print("="*80)

    # Load simulation data
    offspring_list, parent1_list, parent2_list, interaction_conditions, metadata = \
        load_simulation_coalescence_data(simulation_dir, interaction_strengths)

    if not offspring_list:
        print("No simulation data found!")
        return None

    print(f"\nLoaded {len(offspring_list)} coalescence events")

    # Run analysis with null models
    exp_results, null_results = analyze_asymmetricity_with_null_models(
        offspring_list, parent1_list, parent2_list, interaction_conditions,
        n_permutations=n_permutations
    )

    # Generate plots
    if save_plots:
        if save_dir is None:
            save_dir = "Figure/AsymmetricityNullModelAnalysis_simulation"

        save_dir_path = Path(save_dir)
        save_dir_path.mkdir(parents=True, exist_ok=True)

        print("\nGenerating plots...")

        # Diversity asymmetricity plots
        plot_diversity_vs_random_selection(
            exp_results, null_results,
            save_path=str(save_dir_path / "diversity_asymmetricity_vs_random_selection.png")
        )

        # Vector asymmetricity plots
        try:
            plot_vector_vs_neutral_mixing(
                exp_results, null_results,
                save_path=str(save_dir_path / "vector_asymmetricity_vs_neutral_mixing.png")
            )
        except Exception as e:
            print(f"Warning: Could not generate vector asymmetricity plot: {e}")

        # Similarity asymmetricity plots
        try:
            plot_similarity_asymmetricity(
                exp_results, null_results,
                save_path=str(save_dir_path / "similarity_asymmetricity_vs_neutral_mixing.png")
            )
        except Exception as e:
            print(f"Warning: Could not generate similarity asymmetricity plot: {e}")

        print(f"\nPlots saved to {save_dir}/")

    # Print summary statistics
    print_summary_statistics(exp_results, null_results)

    return {
        'experimental_results': exp_results,
        'null_results': null_results,
        'metadata': metadata
    }

def print_summary_statistics(exp_results, null_results):
    """Print summary statistics of the analysis."""
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)

    interaction_strengths = sorted(list(set(exp_results['interaction_conditions'])))

    for condition in interaction_strengths:
        print(f"\n{condition}:")
        print("-" * 40)

        # Get data for this condition
        exp_indices = [k for k, c in enumerate(exp_results['interaction_conditions'])
                      if c == condition]

        if not exp_indices:
            continue

        print(f"  N events: {len(exp_indices)}")

        # Diversity Type 1
        exp_div1 = [exp_results['diversity_asymmetricity_type1'][i] for i in exp_indices]
        exp_div1 = [v for v in exp_div1 if not np.isnan(v)]
        null_div1 = [v for v in null_results['random_selection']['diversity_asymmetricity_type1']
                     if not np.isnan(v)]

        if exp_div1 and null_div1:
            try:
                stat, p_val = stats.mannwhitneyu(exp_div1, null_div1, alternative='two-sided')
                sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
                print(f"  Diversity Type 1: mean_exp={np.mean(exp_div1):.3f}, mean_null={np.mean(null_div1):.3f}, p={p_val:.4f} {sig}")
            except Exception as e:
                print(f"  Diversity Type 1: mean_exp={np.mean(exp_div1):.3f}, mean_null={np.mean(null_div1):.3f} (test failed)")

        # Diversity Type 2
        exp_div2 = [exp_results['diversity_asymmetricity_type2'][i] for i in exp_indices]
        exp_div2 = [v for v in exp_div2 if not np.isnan(v)]
        null_div2 = [v for v in null_results['random_selection']['diversity_asymmetricity_type2']
                     if not np.isnan(v)]

        if exp_div2 and null_div2:
            try:
                stat, p_val = stats.mannwhitneyu(exp_div2, null_div2, alternative='two-sided')
                sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
                print(f"  Diversity Type 2: mean_exp={np.mean(exp_div2):.3f}, mean_null={np.mean(null_div2):.3f}, p={p_val:.4f} {sig}")
            except Exception as e:
                print(f"  Diversity Type 2: mean_exp={np.mean(exp_div2):.3f}, mean_null={np.mean(null_div2):.3f} (test failed)")

        # Vector asymmetricity
        exp_vec = [exp_results['vector_asymmetricity'][i] for i in exp_indices]
        exp_vec = [v for v in exp_vec if not np.isnan(v)]
        null_vec = [v for v in null_results['neutral_mixing']['vector_asymmetricity']
                   if not np.isnan(v)]

        if exp_vec and null_vec:
            try:
                stat, p_val = stats.mannwhitneyu(exp_vec, null_vec, alternative='two-sided')
                sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
                print(f"  Vector: mean_exp={np.mean(exp_vec):.3f}, mean_null={np.mean(null_vec):.3f}, p={p_val:.4f} {sig}")
            except Exception as e:
                print(f"  Vector: mean_exp={np.mean(exp_vec):.3f}, mean_null={np.mean(null_vec):.3f} (test failed)")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Example usage with a specific simulation directory
    simulation_dir = "Simulation_Data/48species_100reps_final"

    # You can specify which interaction strengths to analyze
    # If None, all available strengths will be analyzed automatically
    interaction_strengths = None  # Auto-detect available interaction strengths

    results = run_simulation_null_model_analysis(
        simulation_dir=simulation_dir,
        interaction_strengths=interaction_strengths,
        n_permutations=1000,
        save_plots=True,
        save_dir="Figure/AsymmetricityNullModelAnalysis_simulation"
    )
