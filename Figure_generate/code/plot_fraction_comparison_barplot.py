#!/usr/bin/env python3
"""
Create bar plots comparing frac_same vs frac_AB with null model expectations.

Shows:
1. Observed frac_same vs frac_AB
2. Expected frac_same vs frac_AB (from null model)
3. Statistical test for difference
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import sys
import os

sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

from CooccurrenceNullModelAnalysis import analyze_cooccurrence_with_null_model


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


def test_difference_same_vs_mixed(results):
    """
    Test if frac_same is significantly different from frac_AB.

    Uses the null distribution to calculate the difference and test significance.
    """
    stats = results['statistics']
    null_dist = results['null_distribution']

    # Observed difference
    obs_diff = stats['observed']['frac_same'] - stats['observed']['frac_AB']

    # Null distribution of differences
    null_diff = null_dist['frac_same'] - null_dist['frac_AB']

    # Calculate z-score
    z_score = (obs_diff - np.mean(null_diff)) / (np.std(null_diff) + 1e-10)

    # Calculate empirical p-value (two-sided)
    p_value = np.mean(np.abs(null_diff - np.mean(null_diff)) >= np.abs(obs_diff - np.mean(null_diff)))

    return {
        'observed_difference': obs_diff,
        'expected_difference': np.mean(null_diff),
        'null_std': np.std(null_diff),
        'z_score': z_score,
        'p_value': p_value
    }


def plot_fraction_comparison_barplot(results_dict, save_dir):
    """
    Create bar plots comparing frac_same vs frac_AB for all conditions.
    """
    conditions = ['ALL', 'LN', 'MN', 'HN']

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, condition in enumerate(conditions):
        ax = axes[idx]
        results = results_dict[condition]
        stats = results['statistics']

        # Test difference
        diff_stats = test_difference_same_vs_mixed(results)

        # Data for plotting
        obs_same = stats['observed']['frac_same']
        obs_mixed = stats['observed']['frac_AB']
        exp_same = stats['expected']['frac_same_mean']
        exp_mixed = stats['expected']['frac_AB_mean']

        # Bar positions
        x = np.arange(2)
        width = 0.35

        # Plot bars
        bars1 = ax.bar(x - width/2, [obs_same, obs_mixed], width,
                       label='Observed', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
        bars2 = ax.bar(x + width/2, [exp_same, exp_mixed], width,
                       label='Null Model', color='#95a5a6', alpha=0.8, edgecolor='black', linewidth=1.5)

        # Add error bars for null model
        err_same = stats['expected']['frac_same_std']
        err_mixed = stats['expected']['frac_AB_std']
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
        ax.set_ylabel('Fraction of Pairs Co-present', fontsize=12, fontweight='bold')
        ax.set_title(f'{condition} (n={results["n_replicates"]} replicates)',
                    fontsize=13, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(['Same-Origin\n(A-A + B-B)', 'Mixed-Origin\n(A-B)'], fontsize=11)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Add difference statistics
        z_score = diff_stats['z_score']
        p_value = diff_stats['p_value']
        obs_diff = diff_stats['observed_difference']
        exp_diff = diff_stats['expected_difference']

        sig_text = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'

        # Add bracket showing difference
        y_max = max(obs_same, obs_mixed, exp_same + err_same, exp_mixed + err_mixed) * 1.15
        ax.plot([x[0], x[1]], [y_max, y_max], 'k-', linewidth=2)

        text_str = f'Δ(obs) = {obs_diff:.4f}\nΔ(null) = {exp_diff:.4f}\nz = {z_score:.2f}, p = {p_value:.4f} {sig_text}'
        ax.text(np.mean(x), y_max * 1.02, text_str,
               ha='center', va='bottom', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        # Set y-axis limits
        ax.set_ylim(0, y_max * 1.25)

    plt.tight_layout()
    save_path = os.path.join(save_dir, 'fraction_comparison_barplot.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def plot_difference_distribution(results_dict, save_dir):
    """
    Plot the distribution of (frac_same - frac_AB) from null model.
    """
    conditions = ['ALL', 'LN', 'MN', 'HN']

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, condition in enumerate(conditions):
        ax = axes[idx]
        results = results_dict[condition]
        null_dist = results['null_distribution']
        stats = results['statistics']

        # Calculate differences
        null_diff = null_dist['frac_same'] - null_dist['frac_AB']
        obs_diff = stats['observed']['frac_same'] - stats['observed']['frac_AB']
        exp_diff = np.mean(null_diff)

        # Plot histogram
        ax.hist(null_diff, bins=50, alpha=0.7, color='gray', edgecolor='black',
               label='Null distribution')

        # Add observed and expected lines
        ax.axvline(obs_diff, color='red', linewidth=2.5, linestyle='--',
                  label=f'Observed: {obs_diff:.4f}')
        ax.axvline(exp_diff, color='blue', linewidth=2.5, linestyle=':',
                  label=f'Expected: {exp_diff:.4f}')

        # Calculate and display statistics
        diff_stats = test_difference_same_vs_mixed(results)
        z_score = diff_stats['z_score']
        p_value = diff_stats['p_value']
        sig_text = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'

        ax.text(0.98, 0.95, f'z = {z_score:.2f}\np = {p_value:.4f} {sig_text}',
               transform=ax.transAxes, fontsize=12, verticalalignment='top',
               horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

        ax.set_xlabel('Difference (frac_same - frac_AB)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title(f'{condition} (n={results["n_replicates"]} replicates)',
                    fontsize=13, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    save_path = os.path.join(save_dir, 'difference_distribution.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def create_summary_table(results_dict, save_dir):
    """Create summary table with difference statistics."""
    summary_data = []

    for condition, results in results_dict.items():
        stats = results['statistics']
        diff_stats = test_difference_same_vs_mixed(results)

        summary_data.append({
            'condition': condition,
            'n_replicates': results['n_replicates'],
            'frac_same_obs': stats['observed']['frac_same'],
            'frac_AB_obs': stats['observed']['frac_AB'],
            'frac_same_exp': stats['expected']['frac_same_mean'],
            'frac_AB_exp': stats['expected']['frac_AB_mean'],
            'difference_obs': diff_stats['observed_difference'],
            'difference_exp': diff_stats['expected_difference'],
            'z_score': diff_stats['z_score'],
            'p_value': diff_stats['p_value'],
            'significant': 'YES' if diff_stats['p_value'] < 0.05 else 'NO'
        })

    summary_df = pd.DataFrame(summary_data)
    save_path = os.path.join(save_dir, 'fraction_difference_summary.csv')
    summary_df.to_csv(save_path, index=False)
    print(f"Saved: {save_path}")

    print("\nSummary Table:")
    print(summary_df[['condition', 'n_replicates', 'difference_obs', 'difference_exp', 'z_score', 'p_value', 'significant']].to_string())


def main():
    """Main function."""
    save_dir = "Figure/AsymmetricityNullModelAnalysis/cooccurrence_analysis/merged"
    os.makedirs(save_dir, exist_ok=True)

    # Load data
    offspring_list, parent1_list, parent2_list, nutrient_conditions = load_all_coalescence_data()

    results_dict = {}

    # Analyze ALL
    print("\n" + "="*80)
    print("Analyzing ALL conditions combined...")
    print("="*80)
    results_all = analyze_cooccurrence_with_null_model(
        offspring_list, parent1_list, parent2_list,
        threshold=1e-4, n_simulations=10000, random_seed=42
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

        results = analyze_cooccurrence_with_null_model(
            off_subset, p1_subset, p2_subset,
            threshold=1e-4, n_simulations=10000, random_seed=42
        )
        results_dict[nutrient] = results

    # Create plots
    print("\n" + "="*80)
    print("Creating visualizations...")
    print("="*80)

    plot_fraction_comparison_barplot(results_dict, save_dir)
    plot_difference_distribution(results_dict, save_dir)
    create_summary_table(results_dict, save_dir)

    print("\n" + "="*80)
    print("COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    main()
