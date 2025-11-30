#!/usr/bin/env python3
"""
Create clean, publication-quality bar plots for pairwise correlation analysis.

Each nutrient condition gets its own subplot showing:
- Same-origin correlation (observed)
- Mixed-origin correlation (observed)
- Null model expectation (single bar, no distinction)

Statistical significance indicated with stars.
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


def plot_clean_barplots(results_dict, save_dir):
    """
    Create separate bar plots for each nutrient condition with 3 bars:
    1. Same-origin (observed)
    2. Mixed-origin (observed)
    3. Null model (no distinction)

    All bars include SEM error bars.
    Each condition is saved as a separate figure (PNG and SVG).
    """
    # Rename conditions
    condition_names = {
        'LN': 'Nutr-',
        'MN': 'Base',
        'HN': 'Nutr+'
    }

    conditions = ['LN', 'MN', 'HN']

    for condition in conditions:
        # Create single subplot for this condition (70% of original size)
        fig, ax = plt.subplots(1, 1, figsize=(2.45, 2.45))

        results = results_dict[condition]
        summary = results['summary']
        null_results = results['null_results']
        test_results = results['test_results']
        pair_data = results['pair_data']

        # Observed values
        obs_same = summary['mean_corr_same']
        obs_mixed = summary['mean_corr_mixed']

        # Calculate SEM for observed values
        n_same = summary['n_pairs_same_origin']
        n_mixed = summary['n_pairs_mixed_origin']
        std_same = summary['std_corr_same']
        std_mixed = summary['std_corr_mixed']

        sem_same = std_same / np.sqrt(n_same) if n_same > 0 else 0
        sem_mixed = std_mixed / np.sqrt(n_mixed) if n_mixed > 0 else 0

        # Null model (average of same and mixed null expectations)
        null_mean = np.mean([null_results['expected_same_mean'],
                            null_results['expected_mixed_mean']])
        null_std = np.mean([null_results['expected_same_std'],
                           null_results['expected_mixed_std']])

        # Calculate SEM for null model (from the null distribution itself)
        null_same_means = null_results['null_same_means']
        null_mixed_means = null_results['null_mixed_means']
        all_null_means = np.concatenate([null_same_means, null_mixed_means])
        sem_null = np.std(all_null_means) / np.sqrt(len(all_null_means)) if len(all_null_means) > 0 else null_std

        # Bar positions
        x = np.arange(3)
        width = 0.6

        # Colors
        colors = ['#e74c3c', '#3498db', '#95a5a6']  # red, blue, gray

        # Plot bars
        bars = ax.bar(x, [obs_same, obs_mixed, null_mean], width,
                      color=colors, alpha=0.8, edgecolor='black', linewidth=1.0)

        # Add error bars for ALL three bars (using SEM)
        ax.errorbar([0], [obs_same], yerr=[sem_same],
                   fmt='none', color='black', capsize=3, linewidth=1.2)
        ax.errorbar([1], [obs_mixed], yerr=[sem_mixed],
                   fmt='none', color='black', capsize=3, linewidth=1.2)
        ax.errorbar([2], [null_mean], yerr=[sem_null],
                   fmt='none', color='black', capsize=3, linewidth=1.2)

        # Statistical significance
        # Test 1: Same vs Null
        p_same_vs_null = test_results['permutation_pvalue']
        stars_same = get_significance_stars(p_same_vs_null)

        # Test 2: Same vs Mixed (use t-test)
        p_same_vs_mixed = test_results['t_pvalue']
        stars_diff = get_significance_stars(p_same_vs_mixed)

        # Add significance brackets and stars
        # Update y_max and y_min to account for SEM error bars
        y_max = max(obs_same + sem_same, obs_mixed + sem_mixed, null_mean + sem_null)
        y_min = min(obs_same - sem_same, obs_mixed - sem_mixed, null_mean - sem_null)
        y_range = y_max - y_min

        # Bracket 1: Same vs Mixed
        if stars_diff != 'ns':
            bracket_y1 = y_max + y_range * 0.05
            ax.plot([0, 1], [bracket_y1, bracket_y1], 'k-', linewidth=0.8)
            ax.plot([0, 0], [bracket_y1 - y_range*0.01, bracket_y1], 'k-', linewidth=0.8)
            ax.plot([1, 1], [bracket_y1 - y_range*0.01, bracket_y1], 'k-', linewidth=0.8)
            ax.text(0.5, bracket_y1, stars_diff, ha='center', va='bottom', fontsize=9)

        # Bracket 2: Same vs Null
        if stars_same != 'ns':
            bracket_y2 = y_max + y_range * 0.18
            ax.plot([0, 2], [bracket_y2, bracket_y2], 'k-', linewidth=0.8)
            ax.plot([0, 0], [bracket_y2 - y_range*0.01, bracket_y2], 'k-', linewidth=0.8)
            ax.plot([2, 2], [bracket_y2 - y_range*0.01, bracket_y2], 'k-', linewidth=0.8)
            ax.text(1, bracket_y2, stars_same, ha='center', va='bottom', fontsize=9)

        # Styling
        ax.set_ylabel('Pairwise Correlation', fontsize=9)
        # Title removed per user request
        ax.set_xticks(x)
        ax.set_xticklabels(['Same-\nOrigin', 'Mixed-\nOrigin', 'Random\nSelection'], fontsize=8)
        ax.grid(axis='y', alpha=0.3, linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Set y-axis limits
        if stars_same != 'ns' or stars_diff != 'ns':
            ax.set_ylim(y_min - y_range * 0.05, bracket_y2 + y_range * 0.08)
        else:
            ax.set_ylim(y_min - y_range * 0.05, y_max + y_range * 0.1)

        plt.tight_layout()

        # Save as PNG
        save_path_png = os.path.join(save_dir, f'correlation_barplot_{condition}.png')
        plt.savefig(save_path_png, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path_png}")

        # Save as SVG
        save_path_svg = os.path.join(save_dir, f'correlation_barplot_{condition}.svg')
        plt.savefig(save_path_svg, format='svg', bbox_inches='tight')
        print(f"Saved: {save_path_svg}")

        plt.close()


def create_clean_summary_table(results_dict, save_dir):
    """Create clean summary table."""
    condition_names = {
        'LN': 'Nutr-',
        'MN': 'Base',
        'HN': 'Nutr+'
    }

    summary_data = []

    for condition in ['LN', 'MN', 'HN']:
        results = results_dict[condition]
        summary = results['summary']
        test_results = results['test_results']
        null_results = results['null_results']

        null_mean = np.mean([null_results['expected_same_mean'],
                            null_results['expected_mixed_mean']])

        summary_data.append({
            'Condition': condition_names[condition],
            'n': results['n_replicates'],
            'Same-Origin': f"{summary['mean_corr_same']:.4f}",
            'Mixed-Origin': f"{summary['mean_corr_mixed']:.4f}",
            'Null': f"{null_mean:.4f}",
            'Δ(Same-Mixed)': f"{test_results['observed_difference']:.4f}",
            'p-value': f"{test_results['permutation_pvalue']:.4f}",
            'Significance': get_significance_stars(test_results['permutation_pvalue'])
        })

    summary_df = pd.DataFrame(summary_data)
    save_path = os.path.join(save_dir, 'correlation_summary_clean.csv')
    summary_df.to_csv(save_path, index=False)
    print(f"Saved: {save_path}")

    print("\nClean Summary Table:")
    print(summary_df.to_string(index=False))


def main():
    """Main function."""
    save_dir = "Figure/AsymmetricityNullModelAnalysis/correlation_analysis"
    os.makedirs(save_dir, exist_ok=True)

    # Load data
    offspring_list, parent1_list, parent2_list, nutrient_conditions = load_all_coalescence_data()

    results_dict = {}

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
            threshold=1e-4, min_variance_pairs=3, n_simulations=1000
        )
        results_dict[nutrient] = results

    # Create visualizations
    print("\n" + "="*80)
    print("Creating clean visualizations...")
    print("="*80)

    plot_clean_barplots(results_dict, save_dir)
    create_clean_summary_table(results_dict, save_dir)

    print("\n" + "="*80)
    print("COMPLETE!")
    print(f"Results saved to: {save_dir}")
    print("="*80)


if __name__ == "__main__":
    main()
