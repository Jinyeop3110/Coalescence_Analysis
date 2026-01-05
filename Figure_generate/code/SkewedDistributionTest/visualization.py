"""
Visualization functions for Skewed Distribution Test Analysis

Creates publication-ready figures comparing experimental asymmetricity
with null model predictions.

Author: Gore Lab Coalescence Analysis
Date: November 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from scipy import stats
import os

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['pdf.fonttype'] = 42


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


def plot_asymmetricity_comparison(exp_asymm, null_results, comparison_stats,
                                 save_path=None, title_suffix=""):
    """
    Create box plot comparing experimental vs null model asymmetricity distributions.

    Args:
        exp_asymm: Array of experimental asymmetricity values
        null_results: Dict with 'abundance_weighted' and 'shuffled' null asymmetricities
        comparison_stats: Dict with statistical comparison results
        save_path: Path to save the figure
        title_suffix: Additional text for title
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    colors = {
        'experimental': '#2C7BB6',
        'abundance_weighted': '#D7191C',
        'shuffled': '#FDAE61'
    }

    # --- Panel A: Abundance-Weighted Null Model ---
    ax = axes[0]

    data_to_plot = [
        exp_asymm[~np.isnan(exp_asymm)],
        null_results['abundance_weighted'][~np.isnan(null_results['abundance_weighted'])]
    ]
    labels = ['Experimental', 'Abundance-\nWeighted Null']

    bp = ax.boxplot(data_to_plot, patch_artist=True, widths=0.6, showfliers=False)

    bp['boxes'][0].set_facecolor(colors['experimental'])
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_facecolor(colors['abundance_weighted'])
    bp['boxes'][1].set_alpha(0.7)

    for i, data in enumerate(data_to_plot):
        x_jitter = np.random.normal(i + 1, 0.08, len(data))
        ax.scatter(x_jitter, data, alpha=0.4, s=15,
                  color=colors['experimental'] if i == 0 else colors['abundance_weighted'],
                  edgecolors='white', linewidth=0.3)

    # Add significance annotation
    if 'abundance_weighted' in comparison_stats:
        p_val = comparison_stats['abundance_weighted']['mann_whitney_u']['p_value']
        stars = get_significance_stars(p_val)
        y_max = max(np.max(data_to_plot[0]), np.max(data_to_plot[1]))
        y_pos = y_max + 0.05

        ax.plot([1, 2], [y_pos, y_pos], 'k-', linewidth=1)
        ax.text(1.5, y_pos + 0.02, stars, ha='center', va='bottom', fontsize=14, fontweight='bold')

        # Add p-value text
        ax.text(1.5, y_pos + 0.08, f'p = {p_val:.2e}', ha='center', va='bottom', fontsize=9)

    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel('Vector Asymmetricity', fontsize=12)
    ax.set_title('A. Abundance-Weighted Selection Null Model', fontsize=12, fontweight='bold')
    ax.set_ylim(-0.05, 1.15)

    # Add interpretation text
    if 'abundance_weighted' in comparison_stats:
        exp_mean = comparison_stats['abundance_weighted']['exp_mean']
        null_mean = comparison_stats['abundance_weighted']['null_mean']
        diff = exp_mean - null_mean

        if comparison_stats['abundance_weighted']['mann_whitney_u']['significant']:
            if diff > 0:
                interpretation = "Exp > Null: Skewness alone\ndoes NOT explain asymmetricity"
            else:
                interpretation = "Exp < Null: Experimental data\nis more symmetric than expected"
        else:
            interpretation = "No significant difference:\nSkewness may explain asymmetricity"

        ax.text(0.02, 0.98, interpretation, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # --- Panel B: Shuffled Abundance Null Model ---
    ax = axes[1]

    data_to_plot = [
        exp_asymm[~np.isnan(exp_asymm)],
        null_results['shuffled'][~np.isnan(null_results['shuffled'])]
    ]
    labels = ['Experimental', 'Shuffled\nAbundance Null']

    bp = ax.boxplot(data_to_plot, patch_artist=True, widths=0.6, showfliers=False)

    bp['boxes'][0].set_facecolor(colors['experimental'])
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_facecolor(colors['shuffled'])
    bp['boxes'][1].set_alpha(0.7)

    for i, data in enumerate(data_to_plot):
        x_jitter = np.random.normal(i + 1, 0.08, len(data))
        ax.scatter(x_jitter, data, alpha=0.4, s=15,
                  color=colors['experimental'] if i == 0 else colors['shuffled'],
                  edgecolors='white', linewidth=0.3)

    # Add significance annotation
    if 'shuffled' in comparison_stats:
        p_val = comparison_stats['shuffled']['mann_whitney_u']['p_value']
        stars = get_significance_stars(p_val)
        y_max = max(np.max(data_to_plot[0]), np.max(data_to_plot[1]))
        y_pos = y_max + 0.05

        ax.plot([1, 2], [y_pos, y_pos], 'k-', linewidth=1)
        ax.text(1.5, y_pos + 0.02, stars, ha='center', va='bottom', fontsize=14, fontweight='bold')
        ax.text(1.5, y_pos + 0.08, f'p = {p_val:.2e}', ha='center', va='bottom', fontsize=9)

    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel('Vector Asymmetricity', fontsize=12)
    ax.set_title('B. Shuffled Abundance Null Model', fontsize=12, fontweight='bold')
    ax.set_ylim(-0.05, 1.15)

    # Add interpretation text
    if 'shuffled' in comparison_stats:
        exp_mean = comparison_stats['shuffled']['exp_mean']
        null_mean = comparison_stats['shuffled']['null_mean']

        if comparison_stats['shuffled']['mann_whitney_u']['significant']:
            interpretation = "Significant difference:\nSpecific abundance patterns\nmatter for asymmetricity"
        else:
            interpretation = "No significant difference:\nShuffling does not destroy\nthe pattern"

        ax.text(0.02, 0.98, interpretation, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_asymmetricity_by_condition(exp_asymm, null_asymm_dict, nutrient_conditions,
                                   null_model_name, save_path=None):
    """
    Create comparison plot stratified by nutrient condition.

    Args:
        exp_asymm: Array of experimental asymmetricity values
        null_asymm_dict: Dict with null asymmetricities by condition or single array
        nutrient_conditions: List of nutrient conditions for each event
        null_model_name: Name of the null model
        save_path: Path to save figure
    """
    conditions = ['LN', 'MN', 'HN']
    colors = {'experimental': '#2C7BB6', 'null': '#D7191C'}

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    for i, condition in enumerate(conditions):
        ax = axes[i]

        # Get experimental data for this condition
        cond_mask = np.array([c == condition for c in nutrient_conditions])
        exp_cond = exp_asymm[cond_mask]
        exp_cond = exp_cond[~np.isnan(exp_cond)]

        # Get null data (either condition-specific or use all)
        if isinstance(null_asymm_dict, dict) and condition in null_asymm_dict:
            null_cond = null_asymm_dict[condition]
        elif isinstance(null_asymm_dict, np.ndarray):
            null_cond = null_asymm_dict
        else:
            null_cond = null_asymm_dict.get('all', np.array([]))

        null_cond = null_cond[~np.isnan(null_cond)] if len(null_cond) > 0 else np.array([])

        if len(exp_cond) < 3 or len(null_cond) < 3:
            ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(f'{condition}')
            continue

        # Box plots
        data_to_plot = [exp_cond, null_cond]
        labels = ['Exp', 'Null']

        bp = ax.boxplot(data_to_plot, patch_artist=True, widths=0.6, showfliers=False)
        bp['boxes'][0].set_facecolor(colors['experimental'])
        bp['boxes'][0].set_alpha(0.7)
        bp['boxes'][1].set_facecolor(colors['null'])
        bp['boxes'][1].set_alpha(0.7)

        # Scatter points
        for j, data in enumerate(data_to_plot):
            if len(data) > 100:
                data_sample = np.random.choice(data, 100, replace=False)
            else:
                data_sample = data
            x_jitter = np.random.normal(j + 1, 0.08, len(data_sample))
            ax.scatter(x_jitter, data_sample, alpha=0.4, s=12,
                      color=colors['experimental'] if j == 0 else colors['null'],
                      edgecolors='white', linewidth=0.3)

        # Statistical test
        u_stat, p_val = stats.mannwhitneyu(exp_cond, null_cond, alternative='two-sided')
        stars = get_significance_stars(p_val)

        y_max = max(np.max(exp_cond), np.max(null_cond))
        ax.plot([1, 2], [y_max + 0.05, y_max + 0.05], 'k-', linewidth=1)
        ax.text(1.5, y_max + 0.07, stars, ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_xticklabels(labels, fontsize=11)
        ax.set_ylabel('Vector Asymmetricity' if i == 0 else '', fontsize=11)
        ax.set_title(f'{condition} (n={len(exp_cond)})', fontsize=12, fontweight='bold')
        ax.set_ylim(-0.05, 1.2)

        # Add stats text
        stats_text = f'Exp: {np.mean(exp_cond):.3f}\nNull: {np.mean(null_cond):.3f}\np={p_val:.2e}'
        ax.text(0.98, 0.02, stats_text, transform=ax.transAxes, fontsize=8,
               ha='right', va='bottom',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.suptitle(f'Asymmetricity: Experimental vs {null_model_name}', fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_skewness_correlation(asymmetricities, skewness_metrics, correlation_results,
                             save_path=None):
    """
    Plot correlation between parental skewness and offspring asymmetricity.

    Args:
        asymmetricities: Array of asymmetricity values
        skewness_metrics: Dict with Gini/evenness metrics
        correlation_results: Dict with correlation statistics
        save_path: Path to save figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    valid_idx = ~np.isnan(asymmetricities)
    asymm = asymmetricities[valid_idx]

    metrics_to_plot = [
        ('gini_difference', 'Gini Difference |G1 - G2|', 'Parental Inequality Difference'),
        ('mean_gini', 'Mean Gini (G1 + G2)/2', 'Mean Parental Inequality'),
        ('evenness_p1', 'Evenness Parent 1', 'Parent 1 Evenness'),
        ('evenness_p2', 'Evenness Parent 2', 'Parent 2 Evenness')
    ]

    for i, (metric_name, xlabel, title) in enumerate(metrics_to_plot):
        ax = axes.flat[i]

        metric_vals = skewness_metrics[metric_name][valid_idx]

        # Scatter plot
        ax.scatter(metric_vals, asymm, alpha=0.5, s=30, color='#2C7BB6', edgecolors='white', linewidth=0.5)

        # Add regression line
        if len(metric_vals) > 3:
            z = np.polyfit(metric_vals, asymm, 1)
            p = np.poly1d(z)
            x_line = np.linspace(np.min(metric_vals), np.max(metric_vals), 100)
            ax.plot(x_line, p(x_line), 'r--', linewidth=2, alpha=0.8)

        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel('Vector Asymmetricity', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')

        # Add correlation stats
        if metric_name in correlation_results:
            r = correlation_results[metric_name]['pearson_r']
            p_val = correlation_results[metric_name]['pearson_p']
            sig = '*' if p_val < 0.05 else ''

            stats_text = f'r = {r:.3f}{sig}\np = {p_val:.2e}'
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
                   va='top', ha='left',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def plot_distribution_histograms(exp_asymm, null_results, save_path=None):
    """
    Create overlapping histogram comparison of distributions.

    Args:
        exp_asymm: Experimental asymmetricity values
        null_results: Dict with null model asymmetricities
        save_path: Path to save figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    exp_clean = exp_asymm[~np.isnan(exp_asymm)]

    colors = {
        'experimental': '#2C7BB6',
        'abundance_weighted': '#D7191C',
        'shuffled': '#FDAE61'
    }

    # Panel A: Abundance-weighted
    ax = axes[0]
    null_aw = null_results['abundance_weighted']
    null_aw = null_aw[~np.isnan(null_aw)]

    bins = np.linspace(0, 1, 25)

    ax.hist(exp_clean, bins=bins, alpha=0.6, color=colors['experimental'],
           label=f'Experimental (n={len(exp_clean)})', density=True, edgecolor='white')
    ax.hist(null_aw, bins=bins, alpha=0.6, color=colors['abundance_weighted'],
           label=f'Abundance-Weighted Null (n={len(null_aw)})', density=True, edgecolor='white')

    ax.axvline(np.mean(exp_clean), color=colors['experimental'], linestyle='--', linewidth=2, label=f'Exp mean: {np.mean(exp_clean):.3f}')
    ax.axvline(np.mean(null_aw), color=colors['abundance_weighted'], linestyle='--', linewidth=2, label=f'Null mean: {np.mean(null_aw):.3f}')

    ax.set_xlabel('Vector Asymmetricity', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('A. Abundance-Weighted Selection Null Model', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')

    # Panel B: Shuffled
    ax = axes[1]
    null_sh = null_results['shuffled']
    null_sh = null_sh[~np.isnan(null_sh)]

    ax.hist(exp_clean, bins=bins, alpha=0.6, color=colors['experimental'],
           label=f'Experimental (n={len(exp_clean)})', density=True, edgecolor='white')
    ax.hist(null_sh, bins=bins, alpha=0.6, color=colors['shuffled'],
           label=f'Shuffled Null (n={len(null_sh)})', density=True, edgecolor='white')

    ax.axvline(np.mean(exp_clean), color=colors['experimental'], linestyle='--', linewidth=2, label=f'Exp mean: {np.mean(exp_clean):.3f}')
    ax.axvline(np.mean(null_sh), color=colors['shuffled'], linestyle='--', linewidth=2, label=f'Null mean: {np.mean(null_sh):.3f}')

    ax.set_xlabel('Vector Asymmetricity', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('B. Shuffled Abundance Null Model', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()


def create_summary_figure(exp_asymm, null_results, comparison_stats,
                         skewness_metrics, correlation_results,
                         save_path=None):
    """
    Create comprehensive summary figure with all analysis components.
    """
    fig = plt.figure(figsize=(16, 12))

    # Create grid layout
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

    colors = {
        'experimental': '#2C7BB6',
        'abundance_weighted': '#D7191C',
        'shuffled': '#FDAE61'
    }

    exp_clean = exp_asymm[~np.isnan(exp_asymm)]

    # --- Panel A: Box comparison (Abundance-Weighted) ---
    ax1 = fig.add_subplot(gs[0, 0])
    null_aw = null_results['abundance_weighted'][~np.isnan(null_results['abundance_weighted'])]

    data = [exp_clean, null_aw]
    bp = ax1.boxplot(data, patch_artist=True, widths=0.6, showfliers=False)
    bp['boxes'][0].set_facecolor(colors['experimental'])
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_facecolor(colors['abundance_weighted'])
    bp['boxes'][1].set_alpha(0.7)

    for j, d in enumerate(data):
        if len(d) > 50:
            d = np.random.choice(d, 50, replace=False)
        x_jitter = np.random.normal(j + 1, 0.08, len(d))
        ax1.scatter(x_jitter, d, alpha=0.4, s=15,
                   color=colors['experimental'] if j == 0 else colors['abundance_weighted'],
                   edgecolors='white', linewidth=0.3)

    if 'abundance_weighted' in comparison_stats:
        p_val = comparison_stats['abundance_weighted']['mann_whitney_u']['p_value']
        stars = get_significance_stars(p_val)
        ax1.plot([1, 2], [1.05, 1.05], 'k-', linewidth=1)
        ax1.text(1.5, 1.07, stars, ha='center', fontsize=12, fontweight='bold')

    ax1.set_xticklabels(['Exp', 'A-W Null'])
    ax1.set_ylabel('Vector Asymmetricity')
    ax1.set_title('A. Abundance-Weighted Null', fontweight='bold')
    ax1.set_ylim(-0.05, 1.2)

    # --- Panel B: Box comparison (Shuffled) ---
    ax2 = fig.add_subplot(gs[0, 1])
    null_sh = null_results['shuffled'][~np.isnan(null_results['shuffled'])]

    data = [exp_clean, null_sh]
    bp = ax2.boxplot(data, patch_artist=True, widths=0.6, showfliers=False)
    bp['boxes'][0].set_facecolor(colors['experimental'])
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_facecolor(colors['shuffled'])
    bp['boxes'][1].set_alpha(0.7)

    for j, d in enumerate(data):
        if len(d) > 50:
            d = np.random.choice(d, 50, replace=False)
        x_jitter = np.random.normal(j + 1, 0.08, len(d))
        ax2.scatter(x_jitter, d, alpha=0.4, s=15,
                   color=colors['experimental'] if j == 0 else colors['shuffled'],
                   edgecolors='white', linewidth=0.3)

    if 'shuffled' in comparison_stats:
        p_val = comparison_stats['shuffled']['mann_whitney_u']['p_value']
        stars = get_significance_stars(p_val)
        ax2.plot([1, 2], [1.05, 1.05], 'k-', linewidth=1)
        ax2.text(1.5, 1.07, stars, ha='center', fontsize=12, fontweight='bold')

    ax2.set_xticklabels(['Exp', 'Shuffled Null'])
    ax2.set_ylabel('Vector Asymmetricity')
    ax2.set_title('B. Shuffled Abundance Null', fontweight='bold')
    ax2.set_ylim(-0.05, 1.2)

    # --- Panel C: Summary statistics table ---
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.axis('off')

    summary_text = "SUMMARY STATISTICS\n" + "=" * 30 + "\n\n"
    summary_text += f"Experimental (n={len(exp_clean)})\n"
    summary_text += f"  Mean: {np.mean(exp_clean):.3f}\n"
    summary_text += f"  Median: {np.median(exp_clean):.3f}\n"
    summary_text += f"  Std: {np.std(exp_clean):.3f}\n\n"

    if 'abundance_weighted' in comparison_stats:
        aw = comparison_stats['abundance_weighted']
        summary_text += f"Abundance-Weighted Null\n"
        summary_text += f"  Mean: {aw['null_mean']:.3f}\n"
        summary_text += f"  Effect size: {aw['effect_size']['cohens_d']:.3f} ({aw['effect_size']['interpretation']})\n"
        summary_text += f"  p-value: {aw['mann_whitney_u']['p_value']:.2e}\n\n"

    if 'shuffled' in comparison_stats:
        sh = comparison_stats['shuffled']
        summary_text += f"Shuffled Null\n"
        summary_text += f"  Mean: {sh['null_mean']:.3f}\n"
        summary_text += f"  Effect size: {sh['effect_size']['cohens_d']:.3f} ({sh['effect_size']['interpretation']})\n"
        summary_text += f"  p-value: {sh['mann_whitney_u']['p_value']:.2e}\n"

    ax3.text(0.1, 0.9, summary_text, transform=ax3.transAxes, fontsize=9,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # --- Panel D: Gini difference correlation ---
    ax4 = fig.add_subplot(gs[1, 0])
    valid_idx = ~np.isnan(exp_asymm)
    asymm = exp_asymm[valid_idx]
    gini_diff = skewness_metrics['gini_difference'][valid_idx]

    ax4.scatter(gini_diff, asymm, alpha=0.5, s=30, color='#2C7BB6', edgecolors='white')
    if len(gini_diff) > 3:
        z = np.polyfit(gini_diff, asymm, 1)
        p = np.poly1d(z)
        x_line = np.linspace(np.min(gini_diff), np.max(gini_diff), 100)
        ax4.plot(x_line, p(x_line), 'r--', linewidth=2)

    if 'gini_difference' in correlation_results:
        r = correlation_results['gini_difference']['pearson_r']
        p_val = correlation_results['gini_difference']['pearson_p']
        ax4.text(0.02, 0.98, f'r = {r:.3f}\np = {p_val:.2e}', transform=ax4.transAxes,
                fontsize=9, va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    ax4.set_xlabel('Gini Difference |G1 - G2|')
    ax4.set_ylabel('Vector Asymmetricity')
    ax4.set_title('C. Gini Difference vs Asymmetricity', fontweight='bold')

    # --- Panel E: Mean Gini correlation ---
    ax5 = fig.add_subplot(gs[1, 1])
    mean_gini = skewness_metrics['mean_gini'][valid_idx]

    ax5.scatter(mean_gini, asymm, alpha=0.5, s=30, color='#2C7BB6', edgecolors='white')
    if len(mean_gini) > 3:
        z = np.polyfit(mean_gini, asymm, 1)
        p = np.poly1d(z)
        x_line = np.linspace(np.min(mean_gini), np.max(mean_gini), 100)
        ax5.plot(x_line, p(x_line), 'r--', linewidth=2)

    if 'mean_gini' in correlation_results:
        r = correlation_results['mean_gini']['pearson_r']
        p_val = correlation_results['mean_gini']['pearson_p']
        ax5.text(0.02, 0.98, f'r = {r:.3f}\np = {p_val:.2e}', transform=ax5.transAxes,
                fontsize=9, va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    ax5.set_xlabel('Mean Parental Gini')
    ax5.set_ylabel('Vector Asymmetricity')
    ax5.set_title('D. Mean Gini vs Asymmetricity', fontweight='bold')

    # --- Panel F: Distribution histograms ---
    ax6 = fig.add_subplot(gs[1, 2])
    bins = np.linspace(0, 1, 20)

    ax6.hist(exp_clean, bins=bins, alpha=0.6, color=colors['experimental'],
            label='Experimental', density=True, edgecolor='white')
    ax6.hist(null_aw, bins=bins, alpha=0.6, color=colors['abundance_weighted'],
            label='A-W Null', density=True, edgecolor='white')
    ax6.hist(null_sh, bins=bins, alpha=0.4, color=colors['shuffled'],
            label='Shuffled Null', density=True, edgecolor='white')

    ax6.set_xlabel('Vector Asymmetricity')
    ax6.set_ylabel('Density')
    ax6.set_title('E. Distribution Comparison', fontweight='bold')
    ax6.legend(fontsize=8)

    # --- Panel G: Interpretation ---
    ax7 = fig.add_subplot(gs[2, :])
    ax7.axis('off')

    interpretation_text = """
    INTERPRETATION GUIDE
    """ + "=" * 100 + """

    NULL MODEL 1: Abundance-Weighted Random Selection
    - Tests if species with higher abundance in combined parental pool are more likely to survive
    - If Experimental = Null: Skewed abundances explain asymmetricity (high-abundance species dominate)
    - If Experimental > Null: Real asymmetricity exceeds what skewness alone predicts (ecological factors matter)
    - If Experimental < Null: Experimental data is more symmetric than expected from skewness

    NULL MODEL 2: Shuffled Abundance
    - Keeps species identities but randomizes which species are abundant within each parent
    - If Experimental = Null: Asymmetricity does not depend on specific species having high abundance
    - If Experimental != Null: Specific species being dominant matters (identity-dependent effects)

    CORRELATION ANALYSIS
    - Gini Difference: If high correlation, asymmetricity tracks parental inequality differences
    - Mean Gini: If high correlation, asymmetricity increases with overall community skewness
    """

    ax7.text(0.02, 0.95, interpretation_text, transform=ax7.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))

    plt.suptitle('Skewed Distribution Test: Does Parental Abundance Skewness Explain Asymmetricity?',
                fontsize=14, fontweight='bold', y=0.98)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()
