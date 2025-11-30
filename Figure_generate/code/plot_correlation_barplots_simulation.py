#!/usr/bin/env python3
"""
Per-Event Correlation Analysis for SIMULATION Data

Uses the same per-event approach as the experimental analysis:
- For each coalescence event, calculate same-origin and mixed-origin correlations
- Average across all events
- Group by pair type (0_1, 0_2, etc.) then average across pair types

This matches the experimental analysis approach.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import json
import os
import sys

sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

from PairwiseCorrelationAnalysis_PerEvent import (
    calculate_correlation_single_event,
    determine_species_origins_single_event
)
from scipy import stats


def load_simulation_data(json_path):
    """Load simulation data from JSON file."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


def analyze_simulation_per_event_by_pair_type(json_data, interaction_strength, threshold=1e-4, n_simulations=100):
    """
    Analyze simulation data using per-event correlations, grouped by pair type.

    For each pair type (0_1, 0_2, etc.):
    1. Collect all events of that type across replicates
    2. Calculate per-event correlations
    3. Average across events

    Then average results across all pair types.
    """
    # Format key with 2 decimal places to match JSON format
    key = f'{interaction_strength:.2f}'
    param_data = json_data[key]

    coalescence_pair_types = ['0_1', '0_2', '0_3', '1_2', '1_3', '2_3']

    all_pair_type_results = []

    print(f"\nAnalyzing interaction strength {interaction_strength}...")
    print(f"Number of replicates: {len(param_data)}")

    for pair_type in coalescence_pair_types:
        print(f"\n  Analyzing pair type {pair_type}...")

        idx1, idx2 = pair_type.split('_')

        # Collect all events of this pair type
        event_results = []

        for rep_key, rep_data in param_data.items():
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            if pair_type in cc_list:
                offspring = np.array(cc_list[pair_type])
                parent1 = np.array(sc_list[idx1])
                parent2 = np.array(sc_list[idx2])

                # Calculate per-event correlation
                result = calculate_correlation_single_event(
                    offspring, parent1, parent2, threshold
                )

                if result is not None:
                    event_results.append(result)

        print(f"    Valid events: {len(event_results)}")

        if len(event_results) == 0:
            continue

        # Extract correlations for this pair type
        same_corrs = [r['same_origin_corr'] for r in event_results]
        mixed_corrs = [r['mixed_origin_corr'] for r in event_results]

        # Summary for this pair type
        pair_type_summary = {
            'pair_type': pair_type,
            'n_events': len(event_results),
            'mean_same': np.mean(same_corrs),
            'mean_mixed': np.mean(mixed_corrs),
            'std_same': np.std(same_corrs),
            'std_mixed': np.std(mixed_corrs),
            'same_corrs': same_corrs,
            'mixed_corrs': mixed_corrs
        }

        all_pair_type_results.append(pair_type_summary)

        print(f"    Same-origin: {pair_type_summary['mean_same']:.4f} ± {pair_type_summary['std_same']:.4f}")
        print(f"    Mixed-origin: {pair_type_summary['mean_mixed']:.4f} ± {pair_type_summary['std_mixed']:.4f}")

    # Average across all pair types
    print(f"\n  Averaging across {len(all_pair_type_results)} pair types...")

    # Concatenate all correlations across pair types
    all_same_corrs = []
    all_mixed_corrs = []

    for pt_result in all_pair_type_results:
        all_same_corrs.extend(pt_result['same_corrs'])
        all_mixed_corrs.extend(pt_result['mixed_corrs'])

    mean_same = np.mean(all_same_corrs)
    mean_mixed = np.mean(all_mixed_corrs)
    std_same = np.std(all_same_corrs)
    std_mixed = np.std(all_mixed_corrs)

    print(f"    Overall same-origin: {mean_same:.4f} ± {std_same:.4f}")
    print(f"    Overall mixed-origin: {mean_mixed:.4f} ± {std_mixed:.4f}")

    # Paired t-test
    t_stat, t_pval = stats.ttest_rel(all_same_corrs, all_mixed_corrs)

    print(f"\n  Paired t-test:")
    print(f"    t = {t_stat:.4f}, p = {t_pval:.4f}")

    # Null model: shuffle origins within each event
    print(f"\n  Generating null model ({n_simulations} simulations)...")

    null_same_means = []
    null_mixed_means = []

    for sim in range(n_simulations):
        if (sim + 1) % 100 == 0:
            print(f"    Completed {sim + 1}/{n_simulations} simulations")

        sim_same = []
        sim_mixed = []

        for pt_result in all_pair_type_results:
            pair_type = pt_result['pair_type']
            idx1, idx2 = pair_type.split('_')

            for rep_key, rep_data in param_data.items():
                sc_list = rep_data['sc_list']
                cc_list = rep_data['cc_list']

                if pair_type not in cc_list:
                    continue

                offspring = np.array(cc_list[pair_type])
                parent1 = np.array(sc_list[idx1])
                parent2 = np.array(sc_list[idx2])

                # Determine original species origins
                species_origins_orig = determine_species_origins_single_event(
                    parent1, parent2, threshold
                )

                # Only shuffle among valid species
                valid_species = np.where(species_origins_orig >= 0)[0]

                if len(valid_species) < 3:
                    continue

                shuffled_origins = species_origins_orig.copy()
                shuffled_labels = species_origins_orig[valid_species].copy()
                np.random.shuffle(shuffled_labels)
                shuffled_origins[valid_species] = shuffled_labels

                # Calculate with shuffled origins
                offspring_presence = (offspring > threshold).astype(int)
                species_A = np.where(shuffled_origins == 0)[0]
                species_B = np.where(shuffled_origins == 1)[0]

                if len(species_A) < 1 or len(species_B) < 1:
                    continue

                from itertools import combinations

                # Same-origin concordances
                same_conc = []
                if len(species_A) >= 2:
                    for i, j in combinations(species_A, 2):
                        same_conc.append(int(offspring_presence[i] == offspring_presence[j]))
                if len(species_B) >= 2:
                    for i, j in combinations(species_B, 2):
                        same_conc.append(int(offspring_presence[i] == offspring_presence[j]))

                # Mixed-origin concordances
                mixed_conc = []
                for i in species_A:
                    for j in species_B:
                        mixed_conc.append(int(offspring_presence[i] == offspring_presence[j]))

                if len(same_conc) > 0 and len(mixed_conc) > 0:
                    sim_same.append(2 * np.mean(same_conc) - 1)
                    sim_mixed.append(2 * np.mean(mixed_conc) - 1)

        if len(sim_same) > 0:
            null_same_means.append(np.mean(sim_same))
            null_mixed_means.append(np.mean(sim_mixed))

    null_same_means = np.array(null_same_means)
    null_mixed_means = np.array(null_mixed_means)

    # Permutation p-value
    observed_diff = mean_same - mean_mixed
    null_diffs = null_same_means - null_mixed_means
    perm_pval = np.mean(np.abs(null_diffs) >= np.abs(observed_diff))

    print(f"\n  Null Model Results:")
    print(f"    Expected same-origin: {np.mean(null_same_means):.4f}")
    print(f"    Expected mixed-origin: {np.mean(null_mixed_means):.4f}")
    print(f"    Permutation p-value: {perm_pval:.4f}")

    return {
        'interaction_strength': interaction_strength,
        'n_events': len(all_same_corrs),
        'pair_type_results': all_pair_type_results,
        'same_origin_corrs': all_same_corrs,  # Add individual correlations for scatter plot
        'mixed_origin_corrs': all_mixed_corrs,  # Add individual correlations for scatter plot
        'summary': {
            'mean_corr_same': mean_same,
            'mean_corr_mixed': mean_mixed,
            'std_corr_same': std_same,
            'std_corr_mixed': std_mixed,
        },
        'test_results': {
            't_statistic': t_stat,
            't_pvalue': t_pval,
            'observed_difference': observed_diff,
            'permutation_pvalue': perm_pval,
        },
        'null_results': {
            'null_same_means': null_same_means,
            'null_mixed_means': null_mixed_means,
            'expected_same_mean': np.mean(null_same_means),
            'expected_mixed_mean': np.mean(null_mixed_means),
            'expected_same_std': np.std(null_same_means),
            'expected_mixed_std': np.std(null_mixed_means),
        }
    }


def get_significance_stars(p_value):
    """Convert p-value to significance stars."""
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return 'ns'


def plot_simulation_correlation_barplots(results_dict, save_dir):
    """
    Create bar plots for each interaction strength.
    Style similar to Assembly_effect_0.6_simple.svg with squares and shaded scatter.
    """

    for interaction_key, results in results_dict.items():
        # Use wider x-axis: 3.0 width x 2.0 height
        fig, ax = plt.subplots(1, 1, figsize=(3.0, 2.0))

        summary = results['summary']
        null_results = results['null_results']
        test_results = results['test_results']

        obs_same = summary['mean_corr_same']
        obs_mixed = summary['mean_corr_mixed']

        # Calculate SEM
        n_events = results['n_events']
        std_same = summary['std_corr_same']
        std_mixed = summary['std_corr_mixed']

        sem_same = std_same / np.sqrt(n_events) if n_events > 0 else 0
        sem_mixed = std_mixed / np.sqrt(n_events) if n_events > 0 else 0

        # Null model
        null_mean = np.mean([null_results['expected_same_mean'],
                            null_results['expected_mixed_mean']])

        null_same_means = null_results['null_same_means']
        null_mixed_means = null_results['null_mixed_means']
        all_null_means = np.concatenate([null_same_means, null_mixed_means])
        sem_null = np.std(all_null_means) / np.sqrt(len(all_null_means)) if len(all_null_means) > 0 else 0

        # Positions
        x = np.arange(3)
        colors = ['#e74c3c', '#3498db', '#95a5a6']

        # Add jitter to plot individual event data points as shaded scatter
        np.random.seed(42)
        jitter_amount = 0.1

        # Get individual event correlations
        same_origin_corrs = results['same_origin_corrs']
        mixed_origin_corrs = results['mixed_origin_corrs']

        # Plot individual data points as shaded dots
        x_same = x[0] + np.random.normal(0, jitter_amount, len(same_origin_corrs))
        x_mixed = x[1] + np.random.normal(0, jitter_amount, len(mixed_origin_corrs))

        ax.scatter(x_same, same_origin_corrs, alpha=0.3, s=15, color=colors[0], edgecolors='none')
        ax.scatter(x_mixed, mixed_origin_corrs, alpha=0.3, s=15, color=colors[1], edgecolors='none')

        # Plot mean as squares with error bars
        ax.errorbar(x[0], obs_same, yerr=sem_same,
                   fmt='s', markersize=12, capsize=5, capthick=1.5,
                   color=colors[0], ecolor='black', linewidth=1.5,
                   markeredgecolor='black', markeredgewidth=0.5, zorder=10)

        ax.errorbar(x[1], obs_mixed, yerr=sem_mixed,
                   fmt='s', markersize=12, capsize=5, capthick=1.5,
                   color=colors[1], ecolor='black', linewidth=1.5,
                   markeredgecolor='black', markeredgewidth=0.5, zorder=10)

        ax.errorbar(x[2], null_mean, yerr=sem_null,
                   fmt='s', markersize=12, capsize=5, capthick=1.5,
                   color=colors[2], ecolor='black', linewidth=1.5,
                   markeredgecolor='black', markeredgewidth=0.5, zorder=10)

        # Statistical significance
        p_same_vs_null = test_results['permutation_pvalue']
        stars_same = get_significance_stars(p_same_vs_null)

        p_same_vs_mixed = test_results['t_pvalue']
        stars_diff = get_significance_stars(p_same_vs_mixed)

        y_max = max(obs_same + sem_same, obs_mixed + sem_mixed, null_mean + sem_null)
        y_min = min(obs_same - sem_same, obs_mixed - sem_mixed, null_mean - sem_null)
        y_range = y_max - y_min

        bracket_y1 = None
        bracket_y2 = None

        if stars_diff != 'ns':
            bracket_y1 = y_max + y_range * 0.05
            ax.plot([0, 1], [bracket_y1, bracket_y1], 'k-', linewidth=0.8)
            ax.plot([0, 0], [bracket_y1 - y_range*0.01, bracket_y1], 'k-', linewidth=0.8)
            ax.plot([1, 1], [bracket_y1 - y_range*0.01, bracket_y1], 'k-', linewidth=0.8)
            ax.text(0.5, bracket_y1, stars_diff, ha='center', va='bottom', fontsize=9)

        if stars_same != 'ns':
            bracket_y2 = y_max + y_range * 0.18
            ax.plot([0, 2], [bracket_y2, bracket_y2], 'k-', linewidth=0.8)
            ax.plot([0, 0], [bracket_y2 - y_range*0.01, bracket_y2], 'k-', linewidth=0.8)
            ax.plot([2, 2], [bracket_y2 - y_range*0.01, bracket_y2], 'k-', linewidth=0.8)
            ax.text(1, bracket_y2, stars_same, ha='center', va='bottom', fontsize=9)

        ax.set_ylabel('Pairwise Correlation', fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(['Same\nParent', 'Cross\nParents', 'Random\nSelection'], fontsize=10)

        # Make y-axis ticks more sparse
        ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=5))
        ax.tick_params(axis='y', labelsize=10)

        # No grid, use despine like Assembly_effect_0.6_simple
        sns.despine()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if stars_same != 'ns' or stars_diff != 'ns':
            y_limit = max([b for b in [bracket_y1, bracket_y2] if b is not None])
            ax.set_ylim(y_min - y_range * 0.05, y_limit + y_range * 0.08)
        else:
            ax.set_ylim(y_min - y_range * 0.05, y_max + y_range * 0.1)

        plt.tight_layout()

        save_path_png = os.path.join(save_dir, f'correlation_barplot_{interaction_key}.png')
        plt.savefig(save_path_png, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path_png}")

        save_path_svg = os.path.join(save_dir, f'correlation_barplot_{interaction_key}.svg')
        plt.savefig(save_path_svg, format='svg', bbox_inches='tight')
        print(f"Saved: {save_path_svg}")

        plt.close()


def create_summary_table(results_dict, save_dir):
    """Create summary CSV table."""
    summary_data = []

    for interaction_key in sorted(results_dict.keys(), key=float):
        results = results_dict[interaction_key]
        summary = results['summary']
        test_results = results['test_results']
        null_results = results['null_results']

        null_mean = np.mean([null_results['expected_same_mean'],
                            null_results['expected_mixed_mean']])

        summary_data.append({
            'Interaction_Strength': float(interaction_key),
            'n_events': results['n_events'],
            'Same Parent': f"{summary['mean_corr_same']:.4f}",
            'Cross Parents': f"{summary['mean_corr_mixed']:.4f}",
            'Random': f"{null_mean:.4f}",
            'Δ(Same-Mixed)': f"{test_results['observed_difference']:.4f}",
            'p-value': f"{test_results['permutation_pvalue']:.4f}",
            'Significance': get_significance_stars(test_results['permutation_pvalue'])
        })

    summary_df = pd.DataFrame(summary_data)
    save_path = os.path.join(save_dir, 'correlation_summary_simulation.csv')
    summary_df.to_csv(save_path, index=False)
    print(f"Saved: {save_path}")

    print("\nSimulation Correlation Summary:")
    print(summary_df.to_string(index=False))


def main():
    """Main function."""
    print("="*80)
    print("PER-EVENT SIMULATION CORRELATION ANALYSIS")
    print("="*80)

    # Load data - use fine-resolution dataset
    json_path = 'Simulation_Data/48species_200reps_fine/Community_200reps_fine.json'
    data = load_simulation_data(json_path)

    interaction_strengths = sorted([float(k) for k in data.keys()])
    print(f"\nLoaded {len(interaction_strengths)} interaction strengths")

    save_dir = "Figure/AsymmetricityNullModelAnalysis_simulation/correlation_analysis"
    os.makedirs(save_dir, exist_ok=True)

    results_dict = {}

    print("\n" + "="*80)

    for interaction_strength in interaction_strengths:
        results = analyze_simulation_per_event_by_pair_type(
            data, interaction_strength, threshold=1e-4, n_simulations=50
        )
        # Use formatted key to match JSON
        key = f'{interaction_strength:.2f}'
        results_dict[key] = results
        print("="*80)

    # Create visualizations
    print("\nCREATING VISUALIZATIONS")
    print("="*80)
    plot_simulation_correlation_barplots(results_dict, save_dir)
    create_summary_table(results_dict, save_dir)

    print("\n" + "="*80)
    print("COMPLETE!")
    print(f"Results saved to: {save_dir}")
    print("="*80)


if __name__ == "__main__":
    main()
