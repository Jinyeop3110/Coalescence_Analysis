#!/usr/bin/env python3
"""
CORRECTED: Create clean bar plots using PER-EVENT correlation analysis.

Key difference from the old version:
- OLD: Calculated correlations ACROSS events (treating all events as replicates)
- NEW: Calculate correlations WITHIN each event, then average across events

This is the correct approach when each event has different parent pairs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import sys
import os

sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

from PairwiseCorrelationAnalysis_PerEvent import analyze_pairwise_correlations_per_event


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

    print(f"Loaded {len(offspring_list)} coalescence events")
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
    Create separate bar plots for each nutrient condition with 3 bars.
    Style similar to Assembly_effect_0.6_simple.svg with squares and shaded scatter.
    """
    condition_names = {
        'LN': 'Nutr-',
        'MN': 'Base',
        'HN': 'Nutr+'
    }

    conditions = ['LN', 'MN', 'HN']

    for condition in conditions:
        # Match simulation barplot size: 2.5 x 2.5
        fig, ax = plt.subplots(1, 1, figsize=(2.5, 2.5))

        results = results_dict[condition]
        summary = results['summary']
        null_results = results['null_results']
        test_results = results['test_results']

        # Observed values
        obs_same = summary['mean_corr_same']
        obs_mixed = summary['mean_corr_mixed']

        # Calculate SEM
        n_events = results['n_valid_events']
        std_same = summary['std_corr_same']
        std_mixed = summary['std_corr_mixed']

        sem_same = std_same / np.sqrt(n_events) if n_events > 0 else 0
        sem_mixed = std_mixed / np.sqrt(n_events) if n_events > 0 else 0

        # Null model
        null_mean = np.mean([null_results['expected_same_mean'],
                            null_results['expected_mixed_mean']])

        # SEM for null
        null_same_means = null_results['null_same_means']
        null_mixed_means = null_results['null_mixed_means']
        all_null_means = np.concatenate([null_same_means, null_mixed_means])
        sem_null = np.std(all_null_means) / np.sqrt(len(all_null_means)) if len(all_null_means) > 0 else 0

        # Positions - only 2 bars now
        x = np.arange(2)
        colors = ['#e74c3c', '#3498db']

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

        # Add random selection as horizontal grey line (baseline)
        ax.axhline(y=null_mean, color='#95a5a6', linestyle='-',
                   linewidth=2, alpha=0.7, zorder=5)

        # Statistical significance
        p_same_vs_null = test_results['permutation_pvalue']
        stars_same = get_significance_stars(p_same_vs_null)

        p_same_vs_mixed = test_results['t_pvalue']
        stars_diff = get_significance_stars(p_same_vs_mixed)

        y_max = max(obs_same + sem_same, obs_mixed + sem_mixed, null_mean)
        y_min = min(obs_same - sem_same, obs_mixed - sem_mixed, null_mean)
        y_range = y_max - y_min

        bracket_y1 = None

        # Only show bracket for same vs mixed comparison
        if stars_diff != 'ns':
            bracket_y1 = y_max + y_range * 0.05
            ax.plot([0, 1], [bracket_y1, bracket_y1], 'k-', linewidth=0.8)
            ax.plot([0, 0], [bracket_y1 - y_range*0.01, bracket_y1], 'k-', linewidth=0.8)
            ax.plot([1, 1], [bracket_y1 - y_range*0.01, bracket_y1], 'k-', linewidth=0.8)
            ax.text(0.5, bracket_y1, stars_diff, ha='center', va='bottom', fontsize=9)

        ax.set_ylabel('Pairwise selection correlation', fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(['Same\nParent', 'Cross\nParents'], fontsize=10)

        # Make y-axis ticks at 0.1 intervals
        ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}'))
        ax.tick_params(axis='y', labelsize=10)

        # No grid, use despine like Assembly_effect_0.6_simple
        sns.despine()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Fixed y-axis range for consistency across conditions
        ax.set_ylim(-0.2, 0.6)

        plt.tight_layout()

        save_path_png = os.path.join(save_dir, f'correlation_barplot_{condition}.png')
        plt.savefig(save_path_png, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path_png}")

        save_path_pdf = os.path.join(save_dir, f'correlation_barplot_{condition}.pdf')
        plt.savefig(save_path_pdf, format='pdf', bbox_inches='tight')
        print(f"Saved: {save_path_pdf}")

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
            'n_events': results['n_valid_events'],
            'Same Parent': f"{summary['mean_corr_same']:.4f}",
            'Cross Parents': f"{summary['mean_corr_mixed']:.4f}",
            'Random': f"{null_mean:.4f}",
            'Δ(Same-Mixed)': f"{test_results['observed_difference']:.4f}",
            'p-value': f"{test_results['permutation_pvalue']:.4f}",
            'Significance': get_significance_stars(test_results['permutation_pvalue'])
        })

    summary_df = pd.DataFrame(summary_data)
    save_path = os.path.join(save_dir, 'correlation_summary_clean.csv')
    summary_df.to_csv(save_path, index=False)
    print(f"Saved: {save_path}")

    print("\nSummary Table:")
    print(summary_df.to_string(index=False))


def main():
    """Main function."""
    save_dir = "Figure/AsymmetricityNullModelAnalysis/correlation_analysis"
    os.makedirs(save_dir, exist_ok=True)

    # Load data
    offspring_list, parent1_list, parent2_list, nutrient_conditions = load_all_coalescence_data()

    results_dict = {}

    # Analyze by nutrient using PER-EVENT approach
    for nutrient in ['LN', 'MN', 'HN']:
        print("\n" + "="*80)
        print(f"Analyzing {nutrient} (PER-EVENT CORRELATION)...")
        print("="*80)

        indices = [i for i, c in enumerate(nutrient_conditions) if c == nutrient]
        off_subset = [offspring_list[i] for i in indices]
        p1_subset = [parent1_list[i] for i in indices]
        p2_subset = [parent2_list[i] for i in indices]

        results = analyze_pairwise_correlations_per_event(
            off_subset, p1_subset, p2_subset,
            threshold=1e-4, n_simulations=1000
        )
        results_dict[nutrient] = results

    # Create visualizations
    print("\n" + "="*80)
    print("Creating visualizations...")
    print("="*80)

    plot_clean_barplots(results_dict, save_dir)
    create_clean_summary_table(results_dict, save_dir)

    print("\n" + "="*80)
    print("COMPLETE!")
    print(f"Results saved to: {save_dir}")
    print("="*80)


if __name__ == "__main__":
    main()
