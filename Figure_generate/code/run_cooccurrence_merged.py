#!/usr/bin/env python3
"""
Run Co-occurrence Analysis with Simulation-Based Null Model - MERGED ONLY

This script runs the simulation-based null model approach on MERGED data only
(combining all nutrient conditions and species pools, plus by-nutrient merged).

Uses FRACTIONS instead of raw counts for better interpretability.
"""

import numpy as np
import pandas as pd
import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

from CooccurrenceNullModelAnalysis import (
    analyze_cooccurrence_with_null_model,
    print_null_model_summary
)


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

    print("Loading ALL synthetic coalescence data...")

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

    print(f"Successfully loaded {len(offspring_list)} coalescence events")
    print(f"Nutrient distribution: LN={nutrient_conditions.count('LN')}, MN={nutrient_conditions.count('MN')}, HN={nutrient_conditions.count('HN')}")

    return offspring_list, parent1_list, parent2_list, nutrient_conditions


def plot_fraction_null_distribution(results, save_path=None):
    """Plot null distribution vs observed values using FRACTIONS."""
    stats = results['statistics']
    null_dist = results['null_distribution']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    metrics = [
        ('frac_AA', 'Same-Origin (A-A) Pair Fraction'),
        ('frac_BB', 'Same-Origin (B-B) Pair Fraction'),
        ('frac_AB', 'Mixed-Origin (A-B) Pair Fraction'),
        ('frac_same', 'All Same-Origin Pair Fraction')
    ]

    for idx, (metric, title) in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]

        # Plot null distribution
        ax.hist(null_dist[metric], bins=50, alpha=0.7, color='gray',
                edgecolor='black', label='Null distribution')

        # Plot observed value
        obs_value = stats['observed'][metric]
        ax.axvline(obs_value, color='red', linewidth=2, linestyle='--',
                  label=f'Observed: {obs_value:.4f}')

        # Plot expected value
        exp_mean = stats['expected'][f'{metric}_mean']
        ax.axvline(exp_mean, color='blue', linewidth=2, linestyle=':',
                  label=f'Expected: {exp_mean:.4f}')

        # Add z-score and p-value
        z_key = f"z_{metric.split('_')[1]}"
        p_key = f"p_{metric.split('_')[1]}"

        z_score = stats['z_scores'][z_key]
        p_value = stats['p_values_two_sided'][p_key]

        sig = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'

        ax.text(0.98, 0.95, f'z = {z_score:.2f}\np = {p_value:.4f} {sig}',
                transform=ax.transAxes, fontsize=11, verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        ax.set_xlabel('Fraction of Pairs Co-present')
        ax.set_ylabel('Frequency')
        ax.set_title(title, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot: {save_path}")

    plt.close()


def run_merged_analysis(save_dir="Figure/AsymmetricityNullModelAnalysis/cooccurrence_analysis/merged"):
    """Run null model analysis on merged data only."""
    os.makedirs(save_dir, exist_ok=True)

    # Load all data
    offspring_list, parent1_list, parent2_list, nutrient_conditions = load_all_coalescence_data()

    results_dict = {}

    # Analysis 1: Overall merged (all conditions combined)
    print("\n" + "="*80)
    print("MERGED ANALYSIS: ALL CONDITIONS COMBINED")
    print("="*80)

    results_all = analyze_cooccurrence_with_null_model(
        offspring_list, parent1_list, parent2_list,
        threshold=1e-4, n_simulations=10000, random_seed=42
    )

    print_null_model_summary(results_all)
    results_dict['ALL'] = results_all

    # Save overall merged results
    plot_fraction_null_distribution(
        results_all,
        save_path=os.path.join(save_dir, "fraction_distribution_ALL_merged.png")
    )

    results_all['null_distribution'].to_csv(
        os.path.join(save_dir, "null_distribution_ALL_merged.csv"),
        index=False
    )

    # Analysis 2: Merged by nutrient condition
    summary_data = []

    for nutrient in ['LN', 'MN', 'HN']:
        print("\n" + "="*80)
        print(f"MERGED ANALYSIS: {nutrient} (all species pools combined)")
        print("="*80)

        # Filter by nutrient
        indices = [i for i, c in enumerate(nutrient_conditions) if c == nutrient]

        off_subset = [offspring_list[i] for i in indices]
        p1_subset = [parent1_list[i] for i in indices]
        p2_subset = [parent2_list[i] for i in indices]

        results = analyze_cooccurrence_with_null_model(
            off_subset, p1_subset, p2_subset,
            threshold=1e-4, n_simulations=10000, random_seed=42
        )

        print_null_model_summary(results)
        results_dict[nutrient] = results

        # Save results
        nutrient_dir = os.path.join(save_dir, nutrient)
        os.makedirs(nutrient_dir, exist_ok=True)

        plot_fraction_null_distribution(
            results,
            save_path=os.path.join(nutrient_dir, f"fraction_distribution_{nutrient}_merged.png")
        )

        results['null_distribution'].to_csv(
            os.path.join(nutrient_dir, f"null_distribution_{nutrient}_merged.csv"),
            index=False
        )

    # Create summary table
    summary_data = []

    for condition, results in results_dict.items():
        stats = results['statistics']
        summary_data.append({
            'condition': condition,
            'n_replicates': results['n_replicates'],
            'frac_AA_obs': stats['observed']['frac_AA'],
            'frac_BB_obs': stats['observed']['frac_BB'],
            'frac_AB_obs': stats['observed']['frac_AB'],
            'frac_same_obs': stats['observed']['frac_same'],
            'frac_AA_exp': stats['expected']['frac_AA_mean'],
            'frac_BB_exp': stats['expected']['frac_BB_mean'],
            'frac_AB_exp': stats['expected']['frac_AB_mean'],
            'frac_same_exp': stats['expected']['frac_same_mean'],
            'z_same': stats['z_scores']['z_same'],
            'p_same': stats['p_values_two_sided']['p_same'],
            'enrichment_ratio': stats['enrichment']['enrichment_ratio'],
            'enrichment_ratio_null': stats['enrichment']['enrichment_ratio_null'],
            'relative_enrichment': stats['enrichment']['relative_enrichment'],
            'significant': 'YES' if stats['p_values_two_sided']['p_same'] < 0.05 else 'NO'
        })

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(os.path.join(save_dir, "merged_summary.csv"), index=False)

    print("\n" + "="*80)
    print("MERGED NULL MODEL ANALYSIS COMPLETE")
    print("="*80)
    print(f"Results saved to: {save_dir}")
    print(f"\nSummary Table:")
    print(summary_df[['condition', 'n_replicates', 'frac_same_obs', 'frac_same_exp', 'z_same', 'p_same', 'significant']].to_string())

    return results_dict


if __name__ == "__main__":
    results = run_merged_analysis()
