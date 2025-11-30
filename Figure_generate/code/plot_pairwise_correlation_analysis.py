#!/usr/bin/env python3
"""
Run pairwise correlation analysis and create visualizations.

Creates:
1. Box plots comparing same-origin vs mixed-origin correlations
2. Distribution histograms for both groups
3. Permutation test null distribution
4. Summary tables with statistics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import sys
import os

sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

from PairwiseCorrelationAnalysis import analyze_pairwise_correlations


def load_all_coalescence_data():
    """Load ALL synthetic coalescence data combined."""
    from common_setup import Coalescence_data

    Processed_sequences_synthetic_path = "../../Postprocessed/processed_Sequences_synthetic.xlsx"
    Processed_sequences_natural_path = "../../Postprocessed/processed_Sequences_natural.xlsx"

    sequences_synthetic = pd.read_excel(Processed_sequences_synthetic_path)
    sequences_natural = pd.read_excel(Processed_sequences_natural_path)
    processed_sequences = pd.concat([sequences_synthetic, sequences_natural])

    offspring_list = []
    parent1_list = []
    parent2_list = []
    nutrient_conditions = []

    print("Loading coalescence data...")

    for idx, row in Coalescence_data.iterrows():
        try:
            if row['CommunityOrigin'] != 'S' or row['CoalescenceType'] != 'C':
                continue

            medium = row['Medium']
            nutrient_mapping = {'L': 'LN', 'M': 'MN', 'H': 'HN'}
            nutrient_condition = nutrient_mapping.get(medium)

            if nutrient_condition is None:
                continue

            mixture_sample_id = row['SampleIDX']
            parent1_sample_id = row['SampleIDX_Sub1']
            parent2_sample_id = row['SampleIDX_Sub2']

            mixture_rows = processed_sequences[processed_sequences['SampleIDX'] == mixture_sample_id]
            parent1_rows = processed_sequences[processed_sequences['SampleIDX'] == parent1_sample_id]
            parent2_rows = processed_sequences[processed_sequences['SampleIDX'] == parent2_sample_id]

            if mixture_rows.empty or parent1_rows.empty or parent2_rows.empty:
                continue

            mixture_vector = mixture_rows.iloc[0, 1:].values.astype(float)
            parent1_vector = parent1_rows.iloc[0, 1:].values.astype(float)
            parent2_vector = parent2_rows.iloc[0, 1:].values.astype(float)

            mixture_vector = np.nan_to_num(mixture_vector, 0)
            parent1_vector = np.nan_to_num(parent1_vector, 0)
            parent2_vector = np.nan_to_num(parent2_vector, 0)

            threshold = 1e-3
            mixture_vector = mixture_vector * (mixture_vector > threshold)
            parent1_vector = parent1_vector * (parent1_vector > threshold)
            parent2_vector = parent2_vector * (parent2_vector > threshold)

            if np.sum(mixture_vector) > 0:
                mixture_vector = mixture_vector / np.sum(mixture_vector)
            if np.sum(parent1_vector) > 0:
                parent1_vector = parent1_vector / np.sum(parent1_vector)
            if np.sum(parent2_vector) > 0:
                parent2_vector = parent2_vector / np.sum(parent2_vector)

            n_observed_species = np.sum(mixture_vector > 0)

            if (n_observed_species >= 3 and
                np.sum(mixture_vector) > 0 and
                np.sum(parent1_vector) > 0 and
                np.sum(parent2_vector) > 0):

                offspring_list.append(mixture_vector)
                parent1_list.append(parent1_vector)
                parent2_list.append(parent2_vector)
                nutrient_conditions.append(nutrient_condition)

        except Exception as e:
            continue

    print(f"Loaded {len(offspring_list)} replicates")
    return offspring_list, parent1_list, parent2_list, nutrient_conditions


def plot_correlation_distributions(results_dict, save_dir):
    """
    Create distribution histograms for same-origin vs mixed-origin correlations.
    """
    conditions = ['ALL', 'LN', 'MN', 'HN']

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, condition in enumerate(conditions):
        ax = axes[idx]
        results = results_dict[condition]
        pair_data = results['pair_data']

        same_corrs = [p['correlation'] for p in pair_data if p['pair_type'] == 'same_origin']
        mixed_corrs = [p['correlation'] for p in pair_data if p['pair_type'] == 'mixed_origin']

        # Plot histograms
        ax.hist(same_corrs, bins=30, alpha=0.6, color='red', label='Same-origin', edgecolor='black')
        ax.hist(mixed_corrs, bins=30, alpha=0.6, color='gray', label='Mixed-origin', edgecolor='black')

        # Add mean lines
        ax.axvline(np.mean(same_corrs), color='darkred', linewidth=2.5, linestyle='--',
                  label=f'Same mean: {np.mean(same_corrs):.3f}')
        ax.axvline(np.mean(mixed_corrs), color='black', linewidth=2.5, linestyle='--',
                  label=f'Mixed mean: {np.mean(mixed_corrs):.3f}')

        # Add statistics
        test_results = results['test_results']
        p_val = test_results['permutation_pvalue']
        diff = test_results['observed_difference']
        cohen_d = test_results['cohens_d']

        sig_text = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'

        stats_text = f'Δ = {diff:.4f}\nCohen\'s d = {cohen_d:.3f}\np = {p_val:.4f} {sig_text}'
        ax.text(0.98, 0.95, stats_text,
               transform=ax.transAxes, fontsize=11, verticalalignment='top',
               horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

        ax.set_xlabel('Pairwise Correlation', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title(f'{condition} (n={results["n_replicates"]} replicates)',
                    fontsize=13, fontweight='bold')
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(alpha=0.3)

    plt.tight_layout()
    save_path = os.path.join(save_dir, 'correlation_distributions.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def plot_correlation_barplots_with_null(results_dict, save_dir):
    """
    Create bar plots comparing observed vs null model for same-origin and mixed-origin.
    """
    conditions = ['ALL', 'LN', 'MN', 'HN']

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, condition in enumerate(conditions):
        ax = axes[idx]
        results = results_dict[condition]
        summary = results['summary']
        null_results = results['null_results']

        # Observed values
        obs_same = summary['mean_corr_same']
        obs_mixed = summary['mean_corr_mixed']

        # Null model expected values
        exp_same = null_results['expected_same_mean']
        exp_mixed = null_results['expected_mixed_mean']

        # Standard errors
        err_same = null_results['expected_same_std']
        err_mixed = null_results['expected_mixed_std']

        # Bar positions
        x = np.arange(2)
        width = 0.35

        # Plot bars
        bars1 = ax.bar(x - width/2, [obs_same, obs_mixed], width,
                       label='Observed', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
        bars2 = ax.bar(x + width/2, [exp_same, exp_mixed], width,
                       label='Null Model', color='#95a5a6', alpha=0.8, edgecolor='black', linewidth=1.5)

        # Add error bars for null model
        ax.errorbar(x + width/2, [exp_same, exp_mixed], yerr=[err_same, err_mixed],
                   fmt='none', color='black', capsize=5, linewidth=2)

        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.4f}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')

        # Styling
        ax.set_ylabel('Mean Pairwise Correlation', fontsize=12, fontweight='bold')
        ax.set_title(f'{condition} (n={results["n_replicates"]} replicates)',
                    fontsize=13, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(['Same-Origin\n(A-A + B-B)', 'Mixed-Origin\n(A-B)'], fontsize=11)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Add difference statistics
        test_results = results['test_results']
        p_val = test_results['permutation_pvalue']
        obs_diff = test_results['observed_difference']
        exp_diff = exp_same - exp_mixed
        cohens_d = test_results['cohens_d']

        sig_text = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'

        # Add bracket showing difference
        y_max = max(obs_same, obs_mixed, exp_same + err_same, exp_mixed + err_mixed)
        y_min = min(obs_same, obs_mixed, exp_same - err_same, exp_mixed - err_mixed)
        bracket_y = y_max + (y_max - y_min) * 0.1

        ax.plot([x[0], x[1]], [bracket_y, bracket_y], 'k-', linewidth=2)

        text_str = f'Δ(obs) = {obs_diff:.4f}\nΔ(null) = {exp_diff:.4f}\nd = {cohens_d:.3f}, p = {p_val:.4f} {sig_text}'
        ax.text(np.mean(x), bracket_y * 1.01, text_str,
               ha='center', va='bottom', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        # Set y-axis limits
        ax.set_ylim(y_min - (y_max - y_min) * 0.05, bracket_y * 1.2)

    plt.tight_layout()
    save_path = os.path.join(save_dir, 'correlation_barplots_with_null.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def plot_correlation_boxplots(results_dict, save_dir):
    """
    Create box plots comparing same-origin vs mixed-origin correlations.
    """
    conditions = ['ALL', 'LN', 'MN', 'HN']

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, condition in enumerate(conditions):
        ax = axes[idx]
        results = results_dict[condition]
        pair_data = results['pair_data']

        same_corrs = [p['correlation'] for p in pair_data if p['pair_type'] == 'same_origin']
        mixed_corrs = [p['correlation'] for p in pair_data if p['pair_type'] == 'mixed_origin']

        # Create box plot
        bp = ax.boxplot([same_corrs, mixed_corrs],
                        labels=['Same-origin\n(A-A + B-B)', 'Mixed-origin\n(A-B)'],
                        patch_artist=True,
                        widths=0.6,
                        showfliers=True)

        # Color boxes
        bp['boxes'][0].set_facecolor('#e74c3c')
        bp['boxes'][0].set_alpha(0.7)
        bp['boxes'][1].set_facecolor('#95a5a6')
        bp['boxes'][1].set_alpha(0.7)

        # Add mean markers
        means = [np.mean(same_corrs), np.mean(mixed_corrs)]
        ax.plot([1, 2], means, 'D', color='blue', markersize=10, label='Mean', zorder=3)

        # Add statistics
        test_results = results['test_results']
        p_val = test_results['permutation_pvalue']
        diff = test_results['observed_difference']
        cohen_d = test_results['cohens_d']

        sig_text = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'

        # Add significance bracket
        y_max = max(max(same_corrs), max(mixed_corrs))
        y_min = min(min(same_corrs), min(mixed_corrs))
        bracket_y = y_max + (y_max - y_min) * 0.05

        ax.plot([1, 2], [bracket_y, bracket_y], 'k-', linewidth=2)
        ax.text(1.5, bracket_y * 1.01, sig_text, ha='center', va='bottom', fontsize=14, fontweight='bold')

        stats_text = f'Δ = {diff:.4f}\nCohen\'s d = {cohen_d:.3f}\np = {p_val:.4f}'
        ax.text(0.98, 0.02, stats_text,
               transform=ax.transAxes, fontsize=11, verticalalignment='bottom',
               horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

        ax.set_ylabel('Pairwise Correlation', fontsize=12, fontweight='bold')
        ax.set_title(f'{condition} (n={results["n_replicates"]} replicates)',
                    fontsize=13, fontweight='bold')
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(alpha=0.3, axis='y')
        ax.set_ylim(y_min - (y_max - y_min) * 0.1, bracket_y * 1.15)

    plt.tight_layout()
    save_path = os.path.join(save_dir, 'correlation_boxplots.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def plot_permutation_test(results_dict, save_dir):
    """
    Plot permutation test null distributions.
    """
    conditions = ['ALL', 'LN', 'MN', 'HN']

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, condition in enumerate(conditions):
        ax = axes[idx]
        results = results_dict[condition]
        test_results = results['test_results']

        permuted_diffs = test_results['permuted_diffs']
        observed_diff = test_results['observed_difference']
        p_val = test_results['permutation_pvalue']

        # Plot histogram of permuted differences
        ax.hist(permuted_diffs, bins=50, alpha=0.7, color='gray', edgecolor='black',
               label='Null distribution')

        # Add observed value
        ax.axvline(observed_diff, color='red', linewidth=2.5, linestyle='--',
                  label=f'Observed: {observed_diff:.4f}')

        # Add expected (should be ~0)
        ax.axvline(0, color='blue', linewidth=2.5, linestyle=':',
                  label='Expected: 0')

        sig_text = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'

        ax.text(0.98, 0.95, f'p = {p_val:.4f} {sig_text}',
               transform=ax.transAxes, fontsize=12, verticalalignment='top',
               horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

        ax.set_xlabel('Difference (Same - Mixed)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title(f'{condition} - Permutation Test (10,000 permutations)',
                    fontsize=13, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    save_path = os.path.join(save_dir, 'permutation_test_distribution.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def create_summary_table(results_dict, save_dir):
    """Create summary table with all statistics."""
    summary_data = []

    for condition, results in results_dict.items():
        summary = results['summary']
        test_results = results['test_results']
        null_results = results['null_results']

        summary_data.append({
            'condition': condition,
            'n_replicates': results['n_replicates'],
            'n_pairs_same': summary['n_pairs_same_origin'],
            'n_pairs_mixed': summary['n_pairs_mixed_origin'],
            'mean_corr_same_obs': summary['mean_corr_same'],
            'mean_corr_mixed_obs': summary['mean_corr_mixed'],
            'mean_corr_same_null': null_results['expected_same_mean'],
            'mean_corr_mixed_null': null_results['expected_mixed_mean'],
            'difference_obs': test_results['observed_difference'],
            'difference_null': null_results['expected_same_mean'] - null_results['expected_mixed_mean'],
            'cohens_d': test_results['cohens_d'],
            't_pvalue': test_results['t_pvalue'],
            'u_pvalue': test_results['u_pvalue'],
            'perm_pvalue': test_results['permutation_pvalue'],
            'significant': 'YES' if test_results['permutation_pvalue'] < 0.05 else 'NO'
        })

    summary_df = pd.DataFrame(summary_data)
    save_path = os.path.join(save_dir, 'correlation_summary.csv')
    summary_df.to_csv(save_path, index=False)
    print(f"Saved: {save_path}")

    print("\nSummary Table:")
    print(summary_df[['condition', 'n_replicates', 'n_pairs_same', 'n_pairs_mixed',
                      'mean_corr_same_obs', 'mean_corr_mixed_obs',
                      'mean_corr_same_null', 'mean_corr_mixed_null',
                      'difference_obs', 'difference_null',
                      'cohens_d', 'perm_pvalue', 'significant']].to_string())


def save_pair_data(results_dict, save_dir):
    """Save detailed pair data to CSV."""
    for condition, results in results_dict.items():
        pair_df = pd.DataFrame(results['pair_data'])
        save_path = os.path.join(save_dir, f'pair_correlations_{condition}.csv')
        pair_df.to_csv(save_path, index=False)
        print(f"Saved: {save_path}")


def main():
    """Main function."""
    save_dir = "Figure/AsymmetricityNullModelAnalysis/correlation_analysis"
    os.makedirs(save_dir, exist_ok=True)

    # Load data
    offspring_list, parent1_list, parent2_list, nutrient_conditions = load_all_coalescence_data()

    results_dict = {}

    # Analyze ALL
    print("\n" + "="*80)
    print("Analyzing ALL conditions combined...")
    print("="*80)
    results_all = analyze_pairwise_correlations(
        offspring_list, parent1_list, parent2_list,
        threshold=1e-4, min_variance_pairs=3
    )
    results_dict['ALL'] = results_all

    # Analyze by nutrient
    for nutrient in ['LN', 'MN', 'HN']:
        print("\n" + "="*80)
        print(f"Analyzing {nutrient}...")
        print("="*80)

        indices = [i for i, c in enumerate(nutrient_conditions) if c == nutrient]
        off_subset = [offspring_list[i] for i in indices]
        p1_subset = [parent1_list[i] for i in indices]
        p2_subset = [parent2_list[i] for i in indices]

        results = analyze_pairwise_correlations(
            off_subset, p1_subset, p2_subset,
            threshold=1e-4, min_variance_pairs=3
        )
        results_dict[nutrient] = results

    # Create visualizations
    print("\n" + "="*80)
    print("Creating visualizations...")
    print("="*80)

    plot_correlation_barplots_with_null(results_dict, save_dir)
    plot_correlation_distributions(results_dict, save_dir)
    plot_correlation_boxplots(results_dict, save_dir)
    plot_permutation_test(results_dict, save_dir)
    create_summary_table(results_dict, save_dir)
    save_pair_data(results_dict, save_dir)

    print("\n" + "="*80)
    print("COMPLETE!")
    print(f"Results saved to: {save_dir}")
    print("="*80)


if __name__ == "__main__":
    main()
