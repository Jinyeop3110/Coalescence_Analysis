#!/usr/bin/env python3
"""
Create ZOOMED barplot for simulation data at u=0.3 and u=0.8 with y-axis range -0.4 to 0.4
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


def analyze_simulation_per_event_by_pair_type(json_data, interaction_strength, threshold=1e-4, n_simulations=1000):
    """
    Analyze simulation data using per-event correlations, grouped by pair type.
    """
    key = f'{interaction_strength:.2f}'
    param_data = json_data[key]

    coalescence_pair_types = ['0_1', '0_2', '0_3', '1_2', '1_3', '2_3']

    all_pair_type_results = []

    print(f"\nAnalyzing interaction strength {interaction_strength}...")
    print(f"Number of replicates: {len(param_data)}")

    for pair_type in coalescence_pair_types:
        print(f"\n  Analyzing pair type {pair_type}...")

        idx1, idx2 = pair_type.split('_')

        event_results = []

        for rep_key, rep_data in param_data.items():
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            if pair_type in cc_list:
                offspring = np.array(cc_list[pair_type])
                parent1 = np.array(sc_list[idx1])
                parent2 = np.array(sc_list[idx2])

                result = calculate_correlation_single_event(
                    offspring, parent1, parent2, threshold
                )

                if result is not None:
                    event_results.append(result)

        print(f"    Valid events: {len(event_results)}")

        if len(event_results) == 0:
            continue

        same_corrs = [r['same_origin_corr'] for r in event_results]
        mixed_corrs = [r['mixed_origin_corr'] for r in event_results]

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

    print(f"\n  Averaging across {len(all_pair_type_results)} pair types...")

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

    t_stat, t_pval = stats.ttest_rel(all_same_corrs, all_mixed_corrs)

    print(f"\n  Paired t-test:")
    print(f"    t = {t_stat:.4f}, p = {t_pval:.4f}")

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

                species_origins_orig = determine_species_origins_single_event(
                    parent1, parent2, threshold
                )

                valid_species = np.where(species_origins_orig >= 0)[0]

                if len(valid_species) < 3:
                    continue

                shuffled_origins = species_origins_orig.copy()
                shuffled_labels = species_origins_orig[valid_species].copy()
                np.random.shuffle(shuffled_labels)
                shuffled_origins[valid_species] = shuffled_labels

                offspring_presence = (offspring > threshold).astype(int)
                species_A = np.where(shuffled_origins == 0)[0]
                species_B = np.where(shuffled_origins == 1)[0]

                if len(species_A) < 1 or len(species_B) < 1:
                    continue

                from itertools import combinations

                same_conc = []
                if len(species_A) >= 2:
                    for i, j in combinations(species_A, 2):
                        same_conc.append(int(offspring_presence[i] == offspring_presence[j]))
                if len(species_B) >= 2:
                    for i, j in combinations(species_B, 2):
                        same_conc.append(int(offspring_presence[i] == offspring_presence[j]))

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
        'same_origin_corrs': all_same_corrs,
        'mixed_origin_corrs': all_mixed_corrs,
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


def plot_barplot_zoomed(results, save_dir, u_value):
    """
    Create ZOOMED bar plot for simulation data with y-axis range -0.4 to 0.4.
    """
    fig, ax = plt.subplots(1, 1, figsize=(2.5, 2.5))

    summary = results['summary']
    null_results = results['null_results']
    test_results = results['test_results']

    obs_same = summary['mean_corr_same']
    obs_mixed = summary['mean_corr_mixed']

    n_events = results['n_events']
    std_same = summary['std_corr_same']
    std_mixed = summary['std_corr_mixed']

    sem_same = std_same / np.sqrt(n_events) if n_events > 0 else 0
    sem_mixed = std_mixed / np.sqrt(n_events) if n_events > 0 else 0

    null_mean = np.mean([null_results['expected_same_mean'],
                        null_results['expected_mixed_mean']])

    x = np.arange(2)
    colors = ['#e74c3c', '#3498db']

    np.random.seed(42)
    jitter_amount = 0.05

    same_origin_corrs = results['same_origin_corrs']
    mixed_origin_corrs = results['mixed_origin_corrs']

    # Stratified sampling
    n_display = 50

    same_corrs_array = np.array(same_origin_corrs)
    same_sorted_indices = np.argsort(same_corrs_array)
    n_bins = 10
    points_per_bin = n_display // n_bins

    same_selected_indices = []
    for i in range(n_bins):
        bin_start = i * len(same_sorted_indices) // n_bins
        bin_end = (i + 1) * len(same_sorted_indices) // n_bins
        bin_indices = same_sorted_indices[bin_start:bin_end]
        n_samples = points_per_bin + (1 if i < (n_display % n_bins) else 0)
        selected = np.random.choice(bin_indices, size=min(n_samples, len(bin_indices)), replace=False)
        same_selected_indices.extend(selected)

    mixed_corrs_array = np.array(mixed_origin_corrs)
    mixed_sorted_indices = np.argsort(mixed_corrs_array)

    mixed_selected_indices = []
    for i in range(n_bins):
        bin_start = i * len(mixed_sorted_indices) // n_bins
        bin_end = (i + 1) * len(mixed_sorted_indices) // n_bins
        bin_indices = mixed_sorted_indices[bin_start:bin_end]
        n_samples = points_per_bin + (1 if i < (n_display % n_bins) else 0)
        selected = np.random.choice(bin_indices, size=min(n_samples, len(bin_indices)), replace=False)
        mixed_selected_indices.extend(selected)

    same_corrs_display = same_corrs_array[same_selected_indices]
    mixed_corrs_display = mixed_corrs_array[mixed_selected_indices]

    x_same = x[0] + np.random.normal(0, jitter_amount, len(same_corrs_display))
    x_mixed = x[1] + np.random.normal(0, jitter_amount, len(mixed_corrs_display))

    ax.scatter(x_same, same_corrs_display, alpha=0.25, s=10, color=colors[0], edgecolors='none')
    ax.scatter(x_mixed, mixed_corrs_display, alpha=0.25, s=10, color=colors[1], edgecolors='none')

    ax.errorbar(x[0], obs_same, yerr=sem_same,
               fmt='s', markersize=12, capsize=5, capthick=1.5,
               color=colors[0], ecolor='black', linewidth=1.5,
               markeredgecolor='black', markeredgewidth=0.5, zorder=10)

    ax.errorbar(x[1], obs_mixed, yerr=sem_mixed,
               fmt='s', markersize=12, capsize=5, capthick=1.5,
               color=colors[1], ecolor='black', linewidth=1.5,
               markeredgecolor='black', markeredgewidth=0.5, zorder=10)

    ax.axhline(y=null_mean, color='#95a5a6', linestyle='-',
               linewidth=2, alpha=0.7, zorder=5)

    p_same_vs_mixed = test_results['t_pvalue']
    stars_diff = get_significance_stars(p_same_vs_mixed)

    y_max = max(obs_same + sem_same, obs_mixed + sem_mixed, null_mean)
    y_min = min(obs_same - sem_same, obs_mixed - sem_mixed, null_mean)
    y_range = y_max - y_min

    if stars_diff != 'ns':
        bracket_y1 = y_max + y_range * 0.05
        ax.plot([0, 1], [bracket_y1, bracket_y1], 'k-', linewidth=0.8)
        ax.plot([0, 0], [bracket_y1 - y_range*0.01, bracket_y1], 'k-', linewidth=0.8)
        ax.plot([1, 1], [bracket_y1 - y_range*0.01, bracket_y1], 'k-', linewidth=0.8)
        ax.text(0.5, bracket_y1, stars_diff, ha='center', va='bottom', fontsize=9)

    ax.set_ylabel('Pairwise selection correlation', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(['Same\nParent', 'Cross\nParents'], fontsize=10)

    ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}'))
    ax.tick_params(axis='y', labelsize=10)

    sns.despine()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # ZOOMED y-axis range: -0.4 to 0.4
    ax.set_ylim(-0.4, 0.4)

    plt.tight_layout()

    # Format u_value for filename
    u_str = f"u{u_value}"

    save_path_png = os.path.join(save_dir, f'correlation_barplot_simulation_{u_str}_zoomed.png')
    plt.savefig(save_path_png, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path_png}")

    save_path_pdf = os.path.join(save_dir, f'correlation_barplot_simulation_{u_str}_zoomed.pdf')
    plt.savefig(save_path_pdf, format='pdf', bbox_inches='tight')
    print(f"Saved: {save_path_pdf}")

    save_path_svg = os.path.join(save_dir, f'correlation_barplot_simulation_{u_str}_zoomed.svg')
    plt.savefig(save_path_svg, format='svg', bbox_inches='tight')
    print(f"Saved: {save_path_svg}")

    plt.close()


def main():
    """Main function."""
    print("="*80)
    print("CREATING ZOOMED BARPLOTS FOR SIMULATION u=0.3 AND u=0.8")
    print("="*80)

    json_path = 'Simulation_Data/48species_200reps_fine/Community_200reps_fine.json'
    data = load_simulation_data(json_path)

    save_dir = "Figure/AsymmetricityNullModelAnalysis_simulation/correlation_analysis"
    os.makedirs(save_dir, exist_ok=True)

    # Analyze and plot for u=0.3
    print("\n" + "="*80)
    print("ANALYZING u=0.3")
    print("="*80)

    results_03 = analyze_simulation_per_event_by_pair_type(
        data, 0.30, threshold=1e-4, n_simulations=1000
    )
    plot_barplot_zoomed(results_03, save_dir, 0.3)

    print("\n" + "="*80)
    print("SUMMARY for u=0.3:")
    print("="*80)
    print(f"n_events: {results_03['n_events']}")
    print(f"Same Parent: {results_03['summary']['mean_corr_same']:.4f}")
    print(f"Cross Parents: {results_03['summary']['mean_corr_mixed']:.4f}")
    print(f"Random: {np.mean([results_03['null_results']['expected_same_mean'], results_03['null_results']['expected_mixed_mean']]):.4f}")
    print(f"Δ(Same-Mixed): {results_03['test_results']['observed_difference']:.4f}")
    print(f"p-value: {results_03['test_results']['permutation_pvalue']:.4f}")
    print(f"Significance: {get_significance_stars(results_03['test_results']['permutation_pvalue'])}")

    # Analyze and plot for u=0.8
    print("\n" + "="*80)
    print("ANALYZING u=0.8")
    print("="*80)

    results_08 = analyze_simulation_per_event_by_pair_type(
        data, 0.80, threshold=1e-4, n_simulations=1000
    )
    plot_barplot_zoomed(results_08, save_dir, 0.8)

    print("\n" + "="*80)
    print("SUMMARY for u=0.8:")
    print("="*80)
    print(f"n_events: {results_08['n_events']}")
    print(f"Same Parent: {results_08['summary']['mean_corr_same']:.4f}")
    print(f"Cross Parents: {results_08['summary']['mean_corr_mixed']:.4f}")
    print(f"Random: {np.mean([results_08['null_results']['expected_same_mean'], results_08['null_results']['expected_mixed_mean']]):.4f}")
    print(f"Δ(Same-Mixed): {results_08['test_results']['observed_difference']:.4f}")
    print(f"p-value: {results_08['test_results']['permutation_pvalue']:.4f}")
    print(f"Significance: {get_significance_stars(results_08['test_results']['permutation_pvalue'])}")

    print("\n" + "="*80)
    print("COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
