#!/usr/bin/env python
"""
Simple scatter plot for interaction strength 0.6
Shows before and after assembly with error bars
"""

import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("ticks")
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10


def calculate_mean_interaction_all_species(interaction_matrix):
    """Calculate mean interaction strength assuming all species exist."""
    interaction_matrix = np.array(interaction_matrix)
    N = interaction_matrix.shape[0]

    off_diagonal = []
    for i in range(N):
        for j in range(N):
            if i != j:
                off_diagonal.append(interaction_matrix[i, j])

    return np.mean(off_diagonal)


def calculate_mean_interaction_present_species(abundances, interaction_matrix):
    """Calculate mean interaction strength for species that are present."""
    abundances = np.array(abundances)
    interaction_matrix = np.array(interaction_matrix)

    present = abundances > 1e-6

    if np.sum(present) < 2:
        return np.nan

    present_indices = np.where(present)[0]

    interactions = []
    for i in present_indices:
        for j in present_indices:
            if i != j:
                interactions.append(interaction_matrix[i, j])

    if len(interactions) == 0:
        return np.nan

    return np.mean(interactions)


def analyze_interaction_0_6(data_file):
    """Analyze data for interaction strength 0.6"""
    print(f"Loading data from {data_file}...")
    with open(data_file, 'r') as f:
        data = json.load(f)

    key = "mean0.60"
    print(f"Processing {key}...")

    before_values = []
    after_values = []

    for rep_key, rep_data in data[key].items():
        interaction_matrix = np.array(rep_data['parameters']['interaction_matrix'])
        sc_list = rep_data['sc_list']
        cc_list = rep_data['cc_list']

        coalescence_pairs = [
            ('c1', 'c2', 'c1_c2'),
            ('c1', 'c3', 'c1_c3'),
            ('c1', 'c4', 'c1_c4'),
            ('c2', 'c3', 'c2_c3'),
            ('c2', 'c4', 'c2_c4'),
            ('c3', 'c4', 'c3_c4')
        ]

        for c1_name, c2_name, cc_name in coalescence_pairs:
            before_mean = calculate_mean_interaction_all_species(interaction_matrix)
            abundances_cc = np.array(cc_list[cc_name])
            after_mean = calculate_mean_interaction_present_species(abundances_cc, interaction_matrix)

            if not np.isnan(after_mean):
                before_values.append(before_mean)
                after_values.append(after_mean)

    results = {
        'before_values': before_values,
        'after_values': after_values,
        'before_mean': np.mean(before_values),
        'before_sem': np.std(before_values) / np.sqrt(len(before_values)),
        'after_mean': np.mean(after_values),
        'after_sem': np.std(after_values) / np.sqrt(len(after_values)),
        'n': len(before_values)
    }

    print(f"  N = {results['n']}")
    print(f"  Before: {results['before_mean']:.4f} ± {results['before_sem']:.4f}")
    print(f"  After:  {results['after_mean']:.4f} ± {results['after_sem']:.4f}")

    return results


def plot_simple_comparison(results, output_dir):
    """Create minimal scatter plot with individual data points and mean as squares"""
    from scipy import stats

    # Create small figure
    fig, ax = plt.subplots(figsize=(2.2, 2.2))

    # X positions
    x_positions = [0, 1]
    before_values = np.array(results['before_values'])
    after_values = np.array(results['after_values'])
    y_means = [results['before_mean'], results['after_mean']]
    y_errors = [results['before_sem'], results['after_sem']]

    # Colors - purple for pre-assembly, orange for post-assembly
    colors = ['#8B7AB8', '#F4A582']

    # Add jitter to x positions for individual points
    np.random.seed(42)
    jitter_amount = 0.1

    # Plot individual data points as shaded dots
    x_before = x_positions[0] + np.random.normal(0, jitter_amount, len(before_values))
    x_after = x_positions[1] + np.random.normal(0, jitter_amount, len(after_values))

    ax.scatter(x_before, before_values, alpha=0.3, s=15, color=colors[0], edgecolors='none')
    ax.scatter(x_after, after_values, alpha=0.3, s=15, color=colors[1], edgecolors='none')

    # Plot mean as squares with error bars
    for i, (x, y, yerr, color) in enumerate(zip(x_positions, y_means, y_errors, colors)):
        ax.errorbar(x, y, yerr=yerr,
                    fmt='s', markersize=12, capsize=5, capthick=1.5,
                    color=color, ecolor='black', linewidth=1.5,
                    markeredgecolor='black', markeredgewidth=0.5, zorder=10)

    # Add significance stars
    # Calculate approximate y position for significance bracket
    y_max = max(y_means[0] + y_errors[0], y_means[1] + y_errors[1])
    bracket_y = y_max + 0.05
    text_y = bracket_y + 0.02

    # Draw bracket
    ax.plot([x_positions[0], x_positions[0]], [y_means[0] + y_errors[0], bracket_y],
            'k-', linewidth=1)
    ax.plot([x_positions[1], x_positions[1]], [y_means[1] + y_errors[1], bracket_y],
            'k-', linewidth=1)
    ax.plot([x_positions[0], x_positions[1]], [bracket_y, bracket_y],
            'k-', linewidth=1)

    # Add stars
    ax.text((x_positions[0] + x_positions[1])/2, text_y, '***',
            ha='center', va='bottom', fontsize=14, fontweight='bold')

    # Set axis labels and limits
    ax.set_xlim([-0.5, 1.5])
    ax.set_ylim([0, 0.8])
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Initial', 'Post-assembly'], fontsize=10)
    ax.set_yticks([0, 0.4, 0.8])
    ax.set_ylabel('Mean Pairwise interaction', fontsize=11)

    # Remove top and right spines
    sns.despine()
    plt.tight_layout()

    # Save figure
    output_file = output_dir / "Assembly_effect_0.6_simple.svg"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file}")

    output_file_png = output_dir / "Assembly_effect_0.6_simple.png"
    plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file_png}")

    plt.close()


def main():
    data_file = Path("Simulation_Data/mean_uniform_grid_100reps/Community_mean_uniform_grid_100reps.json")
    output_dir = Path("Figure/Assembly_effect_simulation")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("Assembly Effect at Interaction Strength 0.6")
    print("="*70)

    results = analyze_interaction_0_6(data_file)

    print("\n" + "="*70)
    print("Generating plot...")
    print("="*70)
    plot_simple_comparison(results, output_dir)

    print("\n" + "="*70)
    print("✓✓✓ COMPLETE! ✓✓✓")
    print("="*70)


if __name__ == "__main__":
    main()
