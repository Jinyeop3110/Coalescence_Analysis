#!/usr/bin/env python3
"""
plot_dominance_fraction_vs_interaction.py

Purpose: Plot how CLS fraction (dominance fraction) increases with interaction strength
         using similar style to Assembly_effect_scatter_combined.svg

Uses data from: Simulation_Data/mean_uniform_grid_100reps/Community_mean_uniform_grid_100reps.json
Output: Figure/AsymmetricityNullModelAnalysis_simulation/correlation_analysis/
"""

import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("ticks")
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 11


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """Vector decomposition to get (u, v, k) components"""
    def normalize(vec):
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    u = normalize(u)
    v = normalize(v)
    m = normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))

    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)

    orthogonal_vec = m - (e12[0]*u) - (e12[1]*v)
    x3 = np.linalg.norm(orthogonal_vec)
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2 + 1e-10))

    return convert*x1, convert*x2, x3


def classify_outcome(u, v, k):
    """
    Classify outcome into Dominance, Mixing, or Restructuring.
    Returns: 0 (Dominance), 1 (Mixing), 2 (Restructuring)
    """
    x = np.sqrt(u**2 + v**2)
    y = np.abs(np.abs(np.arctan(u / (v + 1e-8))) - np.pi/4) / (np.pi/4)

    if (x**2 > 0.5) * (y > 0.5):
        return 0  # Dominance
    elif (x**2 > 0.5) * (y < 0.5):
        return 1  # Mixing
    elif (x**2 < 0.5):
        return 2  # Restructuring
    else:
        return 1  # Default to mixing


def analyze_dominance_fraction(data_file):
    """
    Calculate dominance fraction for each interaction strength.

    Returns:
    --------
    results : dict
        Dictionary with mean values as keys and dominance/mixing/restructuring counts
    """
    print(f"Loading data from {data_file}...")
    with open(data_file, 'r') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} parameter combinations")

    # Extract mean values from keys
    mean_values = sorted([float(key.replace('mean', '')) for key in data.keys()])
    print(f"Mean interaction strengths: {mean_values}")

    results = {}

    for mean_val in mean_values:
        key = f"mean{mean_val:.2f}"
        print(f"\nProcessing {key}...")

        dominance_count = 0
        mixing_count = 0
        restructuring_count = 0
        total_count = 0

        # Process each replicate
        for rep_key, rep_data in data[key].items():
            # Get single community states (before coalescence)
            sc_list = rep_data['sc_list']
            # Get coalescence states (after assembly)
            cc_list = rep_data['cc_list']

            # Process all pairwise coalescence events
            coalescence_pairs = [
                ('c1', 'c2', 'c1_c2'),
                ('c1', 'c3', 'c1_c3'),
                ('c1', 'c4', 'c1_c4'),
                ('c2', 'c3', 'c2_c3'),
                ('c2', 'c4', 'c2_c4'),
                ('c3', 'c4', 'c3_c4')
            ]

            for c1_name, c2_name, cc_name in coalescence_pairs:
                c1 = np.array(sc_list[c1_name])
                c2 = np.array(sc_list[c2_name])
                c_mix = np.array(cc_list[cc_name])

                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)

                    if not (np.isnan(u) or np.isnan(v) or np.isnan(k)):
                        # Classify
                        outcome = classify_outcome(u, v, k)
                        if outcome == 0:
                            dominance_count += 1
                        elif outcome == 1:
                            mixing_count += 1
                        else:
                            restructuring_count += 1
                        total_count += 1
                except:
                    continue

        # Calculate fractions
        if total_count > 0:
            dominance_fraction = dominance_count / total_count
            mixing_fraction = mixing_count / total_count
            restructuring_fraction = restructuring_count / total_count
        else:
            dominance_fraction = np.nan
            mixing_fraction = np.nan
            restructuring_fraction = np.nan

        results[mean_val] = {
            'dominance_count': dominance_count,
            'mixing_count': mixing_count,
            'restructuring_count': restructuring_count,
            'total_count': total_count,
            'dominance_fraction': dominance_fraction,
            'mixing_fraction': mixing_fraction,
            'restructuring_fraction': restructuring_fraction
        }

        print(f"  Total events: {total_count}")
        print(f"    Dominance: {dominance_count} ({dominance_fraction:.3f})")
        print(f"    Mixing: {mixing_count} ({mixing_fraction:.3f})")
        print(f"    Restructuring: {restructuring_count} ({restructuring_fraction:.3f})")

    return results


def plot_dominance_fraction(results, output_dir):
    """
    Plot dominance fraction vs interaction strength with similar style to
    Assembly_effect_scatter_combined.svg
    """
    mean_values = sorted(results.keys())

    # Create figure with similar dimensions
    fig, ax = plt.subplots(figsize=(3.536, 3.54))  # Same as Assembly_effect plot

    # Prepare data
    x_vals = []
    y_dominance = []
    y_mixing = []
    y_restructuring = []

    for mean_val in mean_values:
        if results[mean_val]['total_count'] > 0:
            x_vals.append(mean_val)
            y_dominance.append(results[mean_val]['dominance_fraction'])
            y_mixing.append(results[mean_val]['mixing_fraction'])
            y_restructuring.append(results[mean_val]['restructuring_fraction'])

    # Plot lines with similar style
    ax.plot(x_vals, y_dominance, '-o', color='#e74c3c', linewidth=1.8,
           markersize=4, markerfacecolor='#e74c3c', markeredgewidth=0,
           label='Dominance', alpha=0.8)

    ax.plot(x_vals, y_mixing, '-o', color='#9b59b6', linewidth=1.8,
           markersize=4, markerfacecolor='#9b59b6', markeredgewidth=0,
           label='Mixing', alpha=0.8)

    ax.plot(x_vals, y_restructuring, '-o', color='#2ecc71', linewidth=1.8,
           markersize=4, markerfacecolor='#2ecc71', markeredgewidth=0,
           label='Restructuring', alpha=0.8)

    # Set axis limits and ticks
    ax.set_xlim([0, 1.2])
    ax.set_ylim([0, 1.0])
    ax.set_xticks([0, 0.4, 0.8, 1.2])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

    # Labels
    ax.set_xlabel('Interaction strength (μ)', fontsize=14)
    ax.set_ylabel('Outcome fraction', fontsize=14)
    ax.legend(loc='best', fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    sns.despine()
    plt.tight_layout()

    # Save figure
    output_file = output_dir / "CLS_dominance_fraction_vs_interaction_strength.svg"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved figure: {output_file}")

    output_file_png = output_dir / "CLS_dominance_fraction_vs_interaction_strength.png"
    plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file_png}")

    plt.close()


def plot_dominance_only(results, output_dir):
    """
    Plot only dominance fraction vs interaction strength (simpler version)
    """
    mean_values = sorted(results.keys())

    # Create figure with similar dimensions
    fig, ax = plt.subplots(figsize=(3.536, 3.54))

    # Prepare data
    x_vals = []
    y_dominance = []

    for mean_val in mean_values:
        if results[mean_val]['total_count'] > 0:
            x_vals.append(mean_val)
            y_dominance.append(results[mean_val]['dominance_fraction'])

    # Plot with scatter and line
    ax.plot(x_vals, y_dominance, '-o', color='#e74c3c', linewidth=1.8,
           markersize=5, markerfacecolor='#e74c3c', markeredgewidth=0,
           alpha=0.8)

    # Set axis limits and ticks
    ax.set_xlim([0, 1.2])
    ax.set_ylim([0, 1.0])
    ax.set_xticks([0, 0.4, 0.8, 1.2])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

    # Labels
    ax.set_xlabel('Interaction strength (μ)', fontsize=14)
    ax.set_ylabel('Dominance fraction', fontsize=14)
    ax.grid(True, alpha=0.3)

    sns.despine()
    plt.tight_layout()

    # Save figure
    output_file = output_dir / "CLS_dominance_fraction_only_vs_interaction_strength.svg"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file}")

    output_file_png = output_dir / "CLS_dominance_fraction_only_vs_interaction_strength.png"
    plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file_png}")

    plt.close()


def plot_dominance_only_reversed(results, output_dir):
    """
    Plot only dominance fraction vs interaction strength (REVERSED x-axis: large to small)
    """
    mean_values = sorted(results.keys(), reverse=True)  # Reverse order

    # Create figure with similar dimensions
    fig, ax = plt.subplots(figsize=(3.536, 3.54))

    # Prepare data
    x_vals = []
    y_dominance = []

    for mean_val in mean_values:
        if results[mean_val]['total_count'] > 0:
            x_vals.append(mean_val)
            y_dominance.append(results[mean_val]['dominance_fraction'])

    # Plot with scatter and line
    ax.plot(x_vals, y_dominance, '-o', color='#e74c3c', linewidth=1.8,
           markersize=5, markerfacecolor='#e74c3c', markeredgewidth=0,
           alpha=0.8)

    # Set axis limits and ticks (REVERSED)
    ax.set_xlim([1.2, 0])  # Reversed
    ax.set_ylim([0, 1.0])
    ax.set_xticks([1.2, 0.8, 0.4, 0])  # Reversed order
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

    # Labels
    ax.set_xlabel('Interaction strength (μ)', fontsize=14)
    ax.set_ylabel('Dominance fraction', fontsize=14)
    ax.grid(True, alpha=0.3)

    sns.despine()
    plt.tight_layout()

    # Save figure
    output_file = output_dir / "CLS_dominance_fraction_only_vs_interaction_strength_REVERSED.svg"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file}")

    output_file_png = output_dir / "CLS_dominance_fraction_only_vs_interaction_strength_REVERSED.png"
    plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file_png}")

    plt.close()


def plot_dominance_fraction_reversed(results, output_dir):
    """
    Plot dominance fraction vs interaction strength (REVERSED x-axis: large to small)
    """
    mean_values = sorted(results.keys(), reverse=True)  # Reverse order

    # Create figure with similar dimensions
    fig, ax = plt.subplots(figsize=(3.536, 3.54))

    # Prepare data
    x_vals = []
    y_dominance = []
    y_mixing = []
    y_restructuring = []

    for mean_val in mean_values:
        if results[mean_val]['total_count'] > 0:
            x_vals.append(mean_val)
            y_dominance.append(results[mean_val]['dominance_fraction'])
            y_mixing.append(results[mean_val]['mixing_fraction'])
            y_restructuring.append(results[mean_val]['restructuring_fraction'])

    # Plot lines with similar style
    ax.plot(x_vals, y_dominance, '-o', color='#e74c3c', linewidth=1.8,
           markersize=4, markerfacecolor='#e74c3c', markeredgewidth=0,
           label='Dominance', alpha=0.8)

    ax.plot(x_vals, y_mixing, '-o', color='#9b59b6', linewidth=1.8,
           markersize=4, markerfacecolor='#9b59b6', markeredgewidth=0,
           label='Mixing', alpha=0.8)

    ax.plot(x_vals, y_restructuring, '-o', color='#2ecc71', linewidth=1.8,
           markersize=4, markerfacecolor='#2ecc71', markeredgewidth=0,
           label='Restructuring', alpha=0.8)

    # Set axis limits and ticks (REVERSED)
    ax.set_xlim([1.2, 0])  # Reversed
    ax.set_ylim([0, 1.0])
    ax.set_xticks([1.2, 0.8, 0.4, 0])  # Reversed order
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

    # Labels
    ax.set_xlabel('Interaction strength (μ)', fontsize=14)
    ax.set_ylabel('Outcome fraction', fontsize=14)
    ax.legend(loc='best', fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    sns.despine()
    plt.tight_layout()

    # Save figure
    output_file = output_dir / "CLS_dominance_fraction_vs_interaction_strength_REVERSED.svg"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file}")

    output_file_png = output_dir / "CLS_dominance_fraction_vs_interaction_strength_REVERSED.png"
    plt.savefig(output_file_png, dpi=300, bbox_inches='tight')
    print(f"✓ Saved figure: {output_file_png}")

    plt.close()


def main():
    # Paths
    data_file = Path("Simulation_Data/mean_uniform_grid_100reps/Community_mean_uniform_grid_100reps.json")
    output_dir = Path("Figure/AsymmetricityNullModelAnalysis_simulation/correlation_analysis")

    # Check if data file exists
    if not data_file.exists():
        print(f"ERROR: Data file not found: {data_file}")
        print(f"Please check the path and try again.")
        return

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("CLS Dominance Fraction vs Interaction Strength Analysis")
    print("="*70)

    # Analyze data
    results = analyze_dominance_fraction(data_file)

    # Plot results
    print("\n" + "="*70)
    print("Generating plots...")
    print("="*70)
    plot_dominance_fraction(results, output_dir)
    plot_dominance_only(results, output_dir)

    # Generate reversed x-axis versions
    print("\n" + "="*70)
    print("Generating REVERSED x-axis plots...")
    print("="*70)
    plot_dominance_fraction_reversed(results, output_dir)
    plot_dominance_only_reversed(results, output_dir)

    print("\n" + "="*70)
    print("✓✓✓ ANALYSIS COMPLETE! ✓✓✓")
    print("="*70)


if __name__ == "__main__":
    main()
