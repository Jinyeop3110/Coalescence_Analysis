#!/usr/bin/env python3
"""
Single compact figure for skewness null model comparison.

Author: Gore Lab
Date: November 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from scipy import stats
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_setup import (
    Coalescence_data,
    Processed_sequences_synthetic,
    exception_list,
)
from skewed_distribution_null_models import (
    load_coalescence_data,
    normalize_vector,
    calculate_vector_asymmetricity,
    generate_abundance_weighted_null_batch,
    generate_shuffled_abundance_null_batch,
)

# Plot style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def get_significance_stars(p_value):
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return 'ns'


def plot_merged_comparison(exp_asymm, null_aw, null_sh, save_path=None):
    """
    Single compact figure with scatter + mean errorbar style (like correlation_barplot).
    """
    # Clean data
    exp_clean = exp_asymm[~np.isnan(exp_asymm)]
    null_aw_clean = null_aw[~np.isnan(null_aw)]
    null_sh_clean = null_sh[~np.isnan(null_sh)]

    # Statistical tests
    u_aw, p_aw = stats.mannwhitneyu(exp_clean, null_aw_clean, alternative='two-sided')
    u_sh, p_sh = stats.mannwhitneyu(exp_clean, null_sh_clean, alternative='two-sided')

    stars_aw = get_significance_stars(p_aw)
    stars_sh = get_significance_stars(p_sh)

    # Means and SEM
    exp_mean = np.mean(exp_clean)
    exp_sem = stats.sem(exp_clean)
    null_aw_mean = np.mean(null_aw_clean)
    null_aw_sem = stats.sem(null_aw_clean)
    null_sh_mean = np.mean(null_sh_clean)
    null_sh_sem = stats.sem(null_sh_clean)

    # Colors
    colors = ['#D55E00', '#0072B2', '#009E73']

    # Create small figure
    fig, ax = plt.subplots(figsize=(2.8, 3.2))

    # Positions
    positions = [0, 1, 2]

    # Sample 100 points for scatter
    np.random.seed(42)
    max_points = 100
    jitter_amount = 0.12

    exp_sample = np.random.choice(exp_clean, min(max_points, len(exp_clean)), replace=False)
    aw_sample = np.random.choice(null_aw_clean, min(max_points, len(null_aw_clean)), replace=False)
    sh_sample = np.random.choice(null_sh_clean, min(max_points, len(null_sh_clean)), replace=False)

    # Plot scatter points (background)
    x_exp = positions[0] + np.random.normal(0, jitter_amount, len(exp_sample))
    x_aw = positions[1] + np.random.normal(0, jitter_amount, len(aw_sample))
    x_sh = positions[2] + np.random.normal(0, jitter_amount, len(sh_sample))

    ax.scatter(x_exp, exp_sample, alpha=0.3, s=15, color=colors[0], edgecolors='none')
    ax.scatter(x_aw, aw_sample, alpha=0.3, s=15, color=colors[1], edgecolors='none')
    ax.scatter(x_sh, sh_sample, alpha=0.3, s=15, color=colors[2], edgecolors='none')

    # Plot mean as squares with error bars
    ax.errorbar(positions[0], exp_mean, yerr=exp_sem,
               fmt='s', markersize=10, capsize=4, capthick=1.2,
               color=colors[0], ecolor='black', linewidth=1.2,
               markeredgecolor='black', markeredgewidth=0.5, zorder=10)
    ax.errorbar(positions[1], null_aw_mean, yerr=null_aw_sem,
               fmt='s', markersize=10, capsize=4, capthick=1.2,
               color=colors[1], ecolor='black', linewidth=1.2,
               markeredgecolor='black', markeredgewidth=0.5, zorder=10)
    ax.errorbar(positions[2], null_sh_mean, yerr=null_sh_sem,
               fmt='s', markersize=10, capsize=4, capthick=1.2,
               color=colors[2], ecolor='black', linewidth=1.2,
               markeredgecolor='black', markeredgewidth=0.5, zorder=10)

    # Significance annotations
    y_max = max(np.max(exp_sample), np.max(aw_sample), np.max(sh_sample))

    # Exp vs AW
    y_line1 = y_max + 0.06
    ax.plot([0, 1], [y_line1, y_line1], 'k-', linewidth=0.8)
    ax.text(0.5, y_line1 + 0.01, stars_aw, ha='center', va='bottom',
           fontsize=9)

    # Exp vs Shuffled
    y_line2 = y_max + 0.16
    ax.plot([0, 2], [y_line2, y_line2], 'k-', linewidth=0.8)
    ax.text(1.0, y_line2 + 0.01, stars_sh, ha='center', va='bottom',
           fontsize=9)

    # Labels
    ax.set_xticks(positions)
    ax.set_xticklabels(['Exp', 'Abund.\nweight.', 'Shuffled'], fontsize=9)

    # Y-axis label with equation
    ylabel = r'Parental asymmetry $|2\mathrm{PDI} - 1|$'
    ax.set_ylabel(ylabel, fontsize=9)

    # Set limits
    ax.set_ylim(-0.05, y_line2 + 0.12)
    ax.set_xlim(-0.5, 2.5)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.pdf'), format='pdf', bbox_inches='tight')
        print(f"Saved: {save_path}")
        print(f"Saved: {save_path.replace('.png', '.svg')}")
        print(f"Saved: {save_path.replace('.png', '.pdf')}")

    plt.close()

    # Print stats
    print(f"\nStatistics:")
    print(f"  Experimental: mean = {exp_mean:.3f}, n = {len(exp_clean)}")
    print(f"  Abundance-weighted: mean = {null_aw_mean:.3f}, n = {len(null_aw_clean)}")
    print(f"  Shuffled: mean = {null_sh_mean:.3f}, n = {len(null_sh_clean)}")
    print(f"  Exp vs Abund-weight: U = {u_aw:.1f}, p = {p_aw:.2e} ({stars_aw})")
    print(f"  Exp vs Shuffled: U = {u_sh:.1f}, p = {p_sh:.2e} ({stars_sh})")

    return [
        {
            'comparison': 'experimental_vs_abundance_weighted_null',
            'n_experimental': len(exp_clean),
            'n_null': len(null_aw_clean),
            'experimental_mean': exp_mean,
            'experimental_sem': exp_sem,
            'null_mean': null_aw_mean,
            'null_sem': null_aw_sem,
            'mann_whitney_u': u_aw,
            'p_value': p_aw,
        },
        {
            'comparison': 'experimental_vs_shuffled_abundance_null',
            'n_experimental': len(exp_clean),
            'n_null': len(null_sh_clean),
            'experimental_mean': exp_mean,
            'experimental_sem': exp_sem,
            'null_mean': null_sh_mean,
            'null_sem': null_sh_sem,
            'mann_whitney_u': u_sh,
            'p_value': p_sh,
        },
    ]


def load_base_medium_coalescence_data(threshold=1e-3):
    """Load Base-medium synthetic coalescence events after manuscript exclusions."""
    offspring_list = []
    parent1_list = []
    parent2_list = []
    sample_ids = []

    for _, row in Coalescence_data.iterrows():
        if row['CommunityOrigin'] != 'S' or row['CoalescenceType'] != 'C':
            continue
        if row['Medium'] != 'M':
            continue
        if row['SampleIDX'] in exception_list:
            continue

        vectors = []
        for sample_id in [row['SampleIDX'], row['SampleIDX_Sub1'], row['SampleIDX_Sub2']]:
            sequence_rows = Processed_sequences_synthetic[
                Processed_sequences_synthetic['SampleIDX'] == sample_id
            ]
            if sequence_rows.empty:
                break
            vector = sequence_rows.iloc[0, 1:].values.astype(float)
            vector = np.nan_to_num(vector, nan=0.0)
            vector = vector * (vector > threshold)
            if np.sum(vector) <= 0:
                break
            vectors.append(normalize_vector(vector))

        if len(vectors) != 3:
            continue
        if np.sum(vectors[0] > 0) < 3:
            continue

        offspring_list.append(vectors[0])
        parent1_list.append(vectors[1])
        parent2_list.append(vectors[2])
        sample_ids.append(row['SampleIDX'])

    metadata = {
        'nutrient_conditions': ['MN'] * len(offspring_list),
        'sample_ids': sample_ids,
        'n_events': len(offspring_list),
        'analysis_scope': 'Base-medium synthetic coalescence events after manuscript exclusions',
    }

    print(f"Loaded {len(offspring_list)} Base-medium coalescence events")
    return offspring_list, parent1_list, parent2_list, metadata


def write_summary(summary_rows, save_path, metadata, n_permutations):
    fieldnames = [
        'analysis_scope',
        'n_permutations',
        'comparison',
        'n_experimental',
        'n_null',
        'experimental_mean',
        'experimental_sem',
        'null_mean',
        'null_sem',
        'mann_whitney_u',
        'p_value',
    ]
    with open(save_path, 'w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow({
                'analysis_scope': metadata['analysis_scope'],
                'n_permutations': n_permutations,
                **row,
            })
    print(f"Saved summary: {save_path}")


def main(data_type='synthetic_base', n_permutations=500):
    """Generate the single comparison plot."""
    print("Loading data...")
    if data_type == 'synthetic_base':
        offspring_list, parent1_list, parent2_list, metadata = load_base_medium_coalescence_data()
    else:
        offspring_list, parent1_list, parent2_list, metadata = load_coalescence_data(data_type)
        metadata['analysis_scope'] = f'{data_type} coalescence events passing sequence filters'

    print("Calculating experimental asymmetricity...")
    exp_asymm = []
    for off, p1, p2 in zip(offspring_list, parent1_list, parent2_list):
        asym, _ = calculate_vector_asymmetricity(p1, p2, off)
        exp_asymm.append(asym)
    exp_asymm = np.array(exp_asymm)

    # Estimate retention rate
    retention_rates = []
    for off, p1, p2 in zip(offspring_list, parent1_list, parent2_list):
        combined = np.sum((np.array(p1) > 1e-4) | (np.array(p2) > 1e-4))
        offspring_sp = np.sum(np.array(off) > 1e-4)
        if combined > 0:
            retention_rates.append(offspring_sp / combined)
    mean_retention = np.mean(retention_rates)

    print("Generating null models...")
    np.random.seed(42)
    null_off_aw, null_p1_aw, null_p2_aw = generate_abundance_weighted_null_batch(
        parent1_list, parent2_list, n_permutations=n_permutations,
        retention_rate=mean_retention
    )

    null_off_sh, null_p1_sh, null_p2_sh = generate_shuffled_abundance_null_batch(
        parent1_list, parent2_list, offspring_list, n_permutations=n_permutations
    )

    print("Calculating null asymmetricities...")
    null_asymm_aw = np.array([calculate_vector_asymmetricity(p1, p2, off)[0]
                              for off, p1, p2 in zip(null_off_aw, null_p1_aw, null_p2_aw)])
    null_asymm_sh = np.array([calculate_vector_asymmetricity(p1, p2, off)[0]
                              for off, p1, p2 in zip(null_off_sh, null_p1_sh, null_p2_sh)])

    # Output directory
    save_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Figure", "SkewedDistributionTest"
    )
    os.makedirs(save_dir, exist_ok=True)

    print("Generating plot...")
    summary_rows = plot_merged_comparison(
        exp_asymm, null_asymm_aw, null_asymm_sh,
        save_path=os.path.join(save_dir, f"skewness_null_comparison_{data_type}.png")
    )
    write_summary(
        summary_rows,
        os.path.join(save_dir, f"skewness_null_comparison_{data_type}_summary.csv"),
        metadata,
        n_permutations,
    )


if __name__ == "__main__":
    main(data_type='synthetic_base', n_permutations=500)
