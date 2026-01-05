#!/usr/bin/env python3
"""
Simple, clean visualization for skewness null model comparison.
Follows the style of correlation_barplot figures.

Author: Gore Lab
Date: November 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from scipy import stats
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skewed_distribution_null_models import (
    load_coalescence_data,
    calculate_vector_asymmetricity,
    generate_abundance_weighted_null_batch,
    generate_shuffled_abundance_null_batch,
    normalize_vector
)

# Plot style settings
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


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


def plot_simple_comparison(exp_asymm, null_asymm, null_model_name,
                          save_path=None, colors=None):
    """
    Create simple bar plot with scatter comparing experimental vs null.

    Args:
        exp_asymm: Experimental asymmetricity values
        null_asymm: Null model asymmetricity values
        null_model_name: Name for x-axis label
        save_path: Path to save figure
        colors: Tuple of (exp_color, null_color)
    """
    if colors is None:
        colors = ('#D55E00', '#0072B2')  # Orange-red, Blue

    # Clean data
    exp_clean = exp_asymm[~np.isnan(exp_asymm)]
    null_clean = null_asymm[~np.isnan(null_asymm)]

    # Statistical test
    u_stat, p_val = stats.mannwhitneyu(exp_clean, null_clean, alternative='two-sided')
    stars = get_significance_stars(p_val)

    # Calculate means
    exp_mean = np.mean(exp_clean)
    null_mean = np.mean(null_clean)

    # Create figure
    fig, ax = plt.subplots(figsize=(3.5, 4))

    # Bar positions
    positions = [0, 1]
    bar_width = 0.5

    # Draw bars (just the mean, like in reference)
    ax.bar(positions[0], exp_mean, width=bar_width, color=colors[0],
           edgecolor='black', linewidth=1, alpha=0.85)
    ax.bar(positions[1], null_mean, width=bar_width, color=colors[1],
           edgecolor='black', linewidth=1, alpha=0.85)

    # Add scatter points with jitter
    np.random.seed(42)

    # Subsample if too many points
    max_points = 80
    if len(exp_clean) > max_points:
        exp_sample = np.random.choice(exp_clean, max_points, replace=False)
    else:
        exp_sample = exp_clean

    if len(null_clean) > max_points:
        null_sample = np.random.choice(null_clean, max_points, replace=False)
    else:
        null_sample = null_clean

    # Scatter for experimental
    x_jitter_exp = np.random.normal(positions[0], 0.12, len(exp_sample))
    ax.scatter(x_jitter_exp, exp_sample, alpha=0.5, s=25,
              color=colors[0], edgecolors='none')

    # Scatter for null
    x_jitter_null = np.random.normal(positions[1], 0.12, len(null_sample))
    ax.scatter(x_jitter_null, null_sample, alpha=0.5, s=25,
              color=colors[1], edgecolors='none')

    # Add significance annotation
    y_max = max(np.max(exp_sample), np.max(null_sample))
    y_line = y_max + 0.08

    ax.plot([0, 1], [y_line, y_line], 'k-', linewidth=1)
    ax.text(0.5, y_line + 0.02, stars, ha='center', va='bottom',
           fontsize=14, fontweight='bold')

    # Labels
    ax.set_xticks(positions)
    ax.set_xticklabels(['Experimental', null_model_name], fontsize=11)

    # Y-axis label with equation
    ylabel = r'One-sided selection $\left| \frac{\arctan(a/b)}{\pi/4} - 1 \right|$'
    ax.set_ylabel(ylabel, fontsize=11)

    # Set y limits
    ax.set_ylim(-0.02, y_line + 0.15)
    ax.set_xlim(-0.6, 1.6)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()

    return {'p_value': p_val, 'exp_mean': exp_mean, 'null_mean': null_mean}


def plot_both_null_models(exp_asymm, null_aw, null_sh, save_path=None):
    """
    Create side-by-side comparison for both null models.
    """
    # Clean data
    exp_clean = exp_asymm[~np.isnan(exp_asymm)]
    null_aw_clean = null_aw[~np.isnan(null_aw)]
    null_sh_clean = null_sh[~np.isnan(null_sh)]

    # Statistical tests
    _, p_aw = stats.mannwhitneyu(exp_clean, null_aw_clean, alternative='two-sided')
    _, p_sh = stats.mannwhitneyu(exp_clean, null_sh_clean, alternative='two-sided')

    stars_aw = get_significance_stars(p_aw)
    stars_sh = get_significance_stars(p_sh)

    # Means
    exp_mean = np.mean(exp_clean)
    null_aw_mean = np.mean(null_aw_clean)
    null_sh_mean = np.mean(null_sh_clean)

    # Colors
    colors = {
        'exp': '#D55E00',      # Orange-red
        'aw': '#0072B2',       # Blue
        'sh': '#009E73'        # Green
    }

    # Create figure
    fig, ax = plt.subplots(figsize=(5, 4))

    # Bar positions
    positions = [0, 1, 2]
    bar_width = 0.55

    # Draw bars
    ax.bar(positions[0], exp_mean, width=bar_width, color=colors['exp'],
           edgecolor='black', linewidth=1, alpha=0.85)
    ax.bar(positions[1], null_aw_mean, width=bar_width, color=colors['aw'],
           edgecolor='black', linewidth=1, alpha=0.85)
    ax.bar(positions[2], null_sh_mean, width=bar_width, color=colors['sh'],
           edgecolor='black', linewidth=1, alpha=0.85)

    # Add scatter points
    np.random.seed(42)
    max_points = 60

    # Sample data
    exp_sample = np.random.choice(exp_clean, min(max_points, len(exp_clean)), replace=False)
    aw_sample = np.random.choice(null_aw_clean, min(max_points, len(null_aw_clean)), replace=False)
    sh_sample = np.random.choice(null_sh_clean, min(max_points, len(null_sh_clean)), replace=False)

    # Scatter
    ax.scatter(np.random.normal(0, 0.1, len(exp_sample)), exp_sample,
              alpha=0.5, s=20, color=colors['exp'], edgecolors='none')
    ax.scatter(np.random.normal(1, 0.1, len(aw_sample)), aw_sample,
              alpha=0.5, s=20, color=colors['aw'], edgecolors='none')
    ax.scatter(np.random.normal(2, 0.1, len(sh_sample)), sh_sample,
              alpha=0.5, s=20, color=colors['sh'], edgecolors='none')

    # Significance annotations
    y_max = max(np.max(exp_sample), np.max(aw_sample), np.max(sh_sample))

    # Exp vs AW
    y_line1 = y_max + 0.08
    ax.plot([0, 1], [y_line1, y_line1], 'k-', linewidth=1)
    ax.text(0.5, y_line1 + 0.02, stars_aw, ha='center', va='bottom',
           fontsize=12, fontweight='bold')

    # Exp vs Shuffled
    y_line2 = y_max + 0.20
    ax.plot([0, 2], [y_line2, y_line2], 'k-', linewidth=1)
    ax.text(1.0, y_line2 + 0.02, stars_sh, ha='center', va='bottom',
           fontsize=12, fontweight='bold')

    # Labels
    ax.set_xticks(positions)
    ax.set_xticklabels(['Experimental', 'Abundance-\nweighted', 'Shuffled'], fontsize=10)

    # Y-axis label with equation
    ylabel = r'One-sided selection $\left| \frac{\arctan(a/b)}{\pi/4} - 1 \right|$'
    ax.set_ylabel(ylabel, fontsize=11)

    # Set limits
    ax.set_ylim(-0.02, y_line2 + 0.15)
    ax.set_xlim(-0.6, 2.6)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_by_nutrient_condition(exp_asymm, null_asymm, nutrient_conditions,
                               null_model_name, save_path=None):
    """
    Create comparison stratified by nutrient condition (LN, MN, HN).
    """
    conditions = ['LN', 'MN', 'HN']
    colors = {'exp': '#D55E00', 'null': '#0072B2'}

    fig, axes = plt.subplots(1, 3, figsize=(9, 3.5))

    for i, condition in enumerate(conditions):
        ax = axes[i]

        # Filter by condition
        cond_mask = np.array([c == condition for c in nutrient_conditions])
        exp_cond = exp_asymm[cond_mask]
        exp_cond = exp_cond[~np.isnan(exp_cond)]

        # Use all null data (or could filter if null has conditions)
        null_cond = null_asymm[~np.isnan(null_asymm)]

        if len(exp_cond) < 3:
            ax.text(0.5, 0.5, 'Insufficient\ndata', ha='center', va='center',
                   transform=ax.transAxes)
            ax.set_title(condition, fontsize=12, fontweight='bold')
            continue

        # Statistical test
        _, p_val = stats.mannwhitneyu(exp_cond, null_cond, alternative='two-sided')
        stars = get_significance_stars(p_val)

        # Means
        exp_mean = np.mean(exp_cond)
        null_mean = np.mean(null_cond)

        # Bars
        positions = [0, 1]
        bar_width = 0.5

        ax.bar(0, exp_mean, width=bar_width, color=colors['exp'],
               edgecolor='black', linewidth=1, alpha=0.85)
        ax.bar(1, null_mean, width=bar_width, color=colors['null'],
               edgecolor='black', linewidth=1, alpha=0.85)

        # Scatter
        np.random.seed(42 + i)
        max_points = 50

        exp_sample = np.random.choice(exp_cond, min(max_points, len(exp_cond)), replace=False)
        null_sample = np.random.choice(null_cond, min(max_points, len(null_cond)), replace=False)

        ax.scatter(np.random.normal(0, 0.1, len(exp_sample)), exp_sample,
                  alpha=0.5, s=20, color=colors['exp'], edgecolors='none')
        ax.scatter(np.random.normal(1, 0.1, len(null_sample)), null_sample,
                  alpha=0.5, s=20, color=colors['null'], edgecolors='none')

        # Significance
        y_max = max(np.max(exp_sample), np.max(null_sample))
        y_line = y_max + 0.08

        ax.plot([0, 1], [y_line, y_line], 'k-', linewidth=1)
        ax.text(0.5, y_line + 0.02, stars, ha='center', va='bottom',
               fontsize=12, fontweight='bold')

        # Labels
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Exp', 'Null'], fontsize=10)
        ax.set_title(condition, fontsize=12, fontweight='bold')

        if i == 0:
            ylabel = r'One-sided selection $\left| \frac{\arctan(a/b)}{\pi/4} - 1 \right|$'
            ax.set_ylabel(ylabel, fontsize=10)

        ax.set_ylim(-0.02, y_line + 0.15)
        ax.set_xlim(-0.5, 1.5)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.suptitle(f'vs {null_model_name}', fontsize=11, y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def run_simple_plots(data_type='synthetic', n_permutations=500):
    """
    Generate all simple comparison plots.
    """
    print("Loading data...")
    offspring_list, parent1_list, parent2_list, metadata = load_coalescence_data(data_type)

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

    print("Generating plots...")

    # Individual comparisons
    plot_simple_comparison(
        exp_asymm, null_asymm_aw, 'Abundance-\nweighted',
        save_path=os.path.join(save_dir, f"simple_comparison_aw_{data_type}.png"),
        colors=('#D55E00', '#0072B2')
    )

    plot_simple_comparison(
        exp_asymm, null_asymm_sh, 'Shuffled',
        save_path=os.path.join(save_dir, f"simple_comparison_shuffled_{data_type}.png"),
        colors=('#D55E00', '#009E73')
    )

    # Combined plot
    plot_both_null_models(
        exp_asymm, null_asymm_aw, null_asymm_sh,
        save_path=os.path.join(save_dir, f"simple_comparison_both_{data_type}.png")
    )

    # By nutrient condition
    plot_by_nutrient_condition(
        exp_asymm, null_asymm_aw, metadata['nutrient_conditions'],
        'Abundance-weighted',
        save_path=os.path.join(save_dir, f"simple_by_condition_aw_{data_type}.png")
    )

    plot_by_nutrient_condition(
        exp_asymm, null_asymm_sh, metadata['nutrient_conditions'],
        'Shuffled',
        save_path=os.path.join(save_dir, f"simple_by_condition_sh_{data_type}.png")
    )

    print("\nDone!")
    print(f"Experimental mean: {np.nanmean(exp_asymm):.3f}")
    print(f"Abundance-weighted null mean: {np.nanmean(null_asymm_aw):.3f}")
    print(f"Shuffled null mean: {np.nanmean(null_asymm_sh):.3f}")


if __name__ == "__main__":
    run_simple_plots(data_type='synthetic', n_permutations=500)
