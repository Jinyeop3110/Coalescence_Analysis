#!/usr/bin/env python3
"""
Run Co-occurrence Analysis with Simulation-Based Null Model

This script runs the new simulation-based null model approach and compares
it with the previous Fisher's exact test approach.
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


def load_coalescence_data_by_condition():
    """Load coalescence data grouped by nutrient condition and species pool."""
    from common_setup import Coalescence_data

    Processed_sequences_synthetic_path = "../../Postprocessed/processed_Sequences_synthetic.xlsx"
    Processed_sequences_natural_path = "../../Postprocessed/processed_Sequences_natural.xlsx"

    sequences_synthetic = pd.read_excel(Processed_sequences_synthetic_path)
    sequences_natural = pd.read_excel(Processed_sequences_natural_path)
    processed_sequences = pd.concat([sequences_synthetic, sequences_natural])

    data_groups = {}

    print("Loading coalescence data by condition and species pool...")

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

            community_idx = row['CommunityIDX']
            if community_idx <= 14:
                experimental_species_pool = 6
            elif community_idx <= 41:
                experimental_species_pool = 12
            elif community_idx <= 47:
                experimental_species_pool = 24
            else:
                continue

            if (n_observed_species >= 3 and
                np.sum(mixture_vector) > 0 and
                np.sum(parent1_vector) > 0 and
                np.sum(parent2_vector) > 0):

                group_key = f"{nutrient_condition}_{experimental_species_pool}"

                if group_key not in data_groups:
                    data_groups[group_key] = {
                        'offspring': [],
                        'parent1': [],
                        'parent2': []
                    }

                data_groups[group_key]['offspring'].append(mixture_vector)
                data_groups[group_key]['parent1'].append(parent1_vector)
                data_groups[group_key]['parent2'].append(parent2_vector)

        except Exception as e:
            continue

    print("\nData loading summary:")
    for group_key in sorted(data_groups.keys()):
        n_replicates = len(data_groups[group_key]['offspring'])
        print(f"  {group_key}: {n_replicates} replicates")

    return data_groups


def plot_null_distribution(results, save_path=None):
    """Plot null distribution vs observed values."""
    stats = results['statistics']
    null_dist = results['null_distribution']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    metrics = [
        ('T_AA', 'Same-Origin (A-A) Pairs'),
        ('T_BB', 'Same-Origin (B-B) Pairs'),
        ('T_AB', 'Mixed-Origin (A-B) Pairs'),
        ('T_same', 'All Same-Origin (AA+BB) Pairs')
    ]

    for idx, (metric, title) in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]

        # Plot null distribution
        ax.hist(null_dist[metric], bins=50, alpha=0.7, color='gray',
                edgecolor='black', label='Null distribution')

        # Plot observed value
        obs_value = stats['observed'][metric] if metric != 'T_same' else stats['observed']['T_same']
        ax.axvline(obs_value, color='red', linewidth=2, linestyle='--',
                  label=f'Observed: {obs_value:.1f}')

        # Plot expected value
        exp_mean = stats['expected'][f'{metric}_mean']
        ax.axvline(exp_mean, color='blue', linewidth=2, linestyle=':',
                  label=f'Expected: {exp_mean:.1f}')

        # Add z-score and p-value
        z_score = stats['z_scores'][f'z_{metric.split("_")[1]}'] if metric != 'T_same' else stats['z_scores']['z_same']
        p_value = stats['p_values_two_sided'][f'p_{metric.split("_")[1]}'] if metric != 'T_same' else stats['p_values_two_sided']['p_same']

        sig = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'

        ax.text(0.98, 0.95, f'z = {z_score:.2f}\np = {p_value:.4f} {sig}',
                transform=ax.transAxes, fontsize=11, verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        ax.set_xlabel('Number of Co-present Pairs')
        ax.set_ylabel('Frequency')
        ax.set_title(title, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot: {save_path}")

    plt.close()


def run_null_model_analysis_all_conditions(save_dir="Figure/AsymmetricityNullModelAnalysis/null_model_analysis"):
    """Run null model analysis for all conditions."""
    os.makedirs(save_dir, exist_ok=True)

    # Load data
    data_groups = load_coalescence_data_by_condition()

    all_results = {}
    summary_data = []

    for group_key, data in data_groups.items():
        print("\n" + "="*80)
        print(f"ANALYZING: {group_key}")
        print("="*80)

        offspring_list = data['offspring']
        parent1_list = data['parent1']
        parent2_list = data['parent2']

        if len(offspring_list) < 3:
            print(f"Skipping {group_key}: insufficient replicates ({len(offspring_list)})")
            continue

        # Run null model analysis
        results = analyze_cooccurrence_with_null_model(
            offspring_list, parent1_list, parent2_list,
            threshold=1e-4, n_simulations=10000, random_seed=42
        )

        # Print summary
        print_null_model_summary(results)

        # Save results
        all_results[group_key] = results

        # Create visualizations
        group_dir = os.path.join(save_dir, group_key)
        os.makedirs(group_dir, exist_ok=True)

        plot_null_distribution(
            results,
            save_path=os.path.join(group_dir, f"null_distribution_{group_key}.png")
        )

        # Save null distribution
        results['null_distribution'].to_csv(
            os.path.join(group_dir, f"null_distribution_{group_key}.csv"),
            index=False
        )

        # Add to summary
        stats = results['statistics']
        summary_data.append({
            'condition': group_key,
            'n_replicates': results['n_replicates'],
            'T_AA_obs': stats['observed']['T_AA'],
            'T_BB_obs': stats['observed']['T_BB'],
            'T_AB_obs': stats['observed']['T_AB'],
            'T_same_obs': stats['observed']['T_same'],
            'T_AA_exp': stats['expected']['T_AA_mean'],
            'T_BB_exp': stats['expected']['T_BB_mean'],
            'T_AB_exp': stats['expected']['T_AB_mean'],
            'T_same_exp': stats['expected']['T_same_mean'],
            'z_same': stats['z_scores']['z_same'],
            'p_same': stats['p_values_two_sided']['p_same'],
            'significant': 'YES' if stats['p_values_two_sided']['p_same'] < 0.05 else 'NO'
        })

    # Save summary table
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(os.path.join(save_dir, "null_model_summary.csv"), index=False)

    print("\n" + "="*80)
    print("NULL MODEL ANALYSIS COMPLETE")
    print("="*80)
    print(f"Results saved to: {save_dir}")
    print(f"\nSummary Table:")
    print(summary_df[['condition', 'n_replicates', 'z_same', 'p_same', 'significant']].to_string())

    return all_results


if __name__ == "__main__":
    results = run_null_model_analysis_all_conditions()
