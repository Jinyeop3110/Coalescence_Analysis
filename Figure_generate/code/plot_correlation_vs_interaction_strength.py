#!/usr/bin/env python3
"""
Plot correlation values vs interaction strength for simulation data.

Creates line plots showing:
- Same-origin correlation vs interaction strength
- Mixed-origin correlation vs interaction strength
- Random selection (null model) vs interaction strength
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

def load_simulation_summary():
    """Load the simulation correlation summary CSV."""
    csv_path = "Figure/AsymmetricityNullModelAnalysis_simulation/correlation_analysis/correlation_summary_simulation.csv"
    df = pd.read_csv(csv_path)
    return df


def plot_correlations_vs_interaction(df, save_dir):
    """
    Create line plot of correlations vs interaction strength.

    Shows two lines:
    - Same-origin (red)
    - Mixed-origin (blue)
    - Random selection baseline (grey horizontal line)
    """
    # Extract data
    interaction_strengths = df['Interaction_Strength'].values
    same_origin = df['Same Parent'].astype(float).values
    mixed_origin = df['Cross Parents'].astype(float).values
    random_selection = df['Random'].astype(float).values

    # Calculate mean random selection value for baseline
    random_baseline = np.mean(random_selection)

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(4, 3))

    # Plot lines
    ax.plot(interaction_strengths, same_origin, 'o-',
            color='#e74c3c', linewidth=2, markersize=8,
            label='Same Parent', markeredgecolor='black', markeredgewidth=1)

    ax.plot(interaction_strengths, mixed_origin, 's-',
            color='#3498db', linewidth=2, markersize=8,
            label='Cross Parents', markeredgecolor='black', markeredgewidth=1)

    # Add random selection as horizontal baseline
    ax.axhline(y=random_baseline, color='#95a5a6', linestyle='-',
               linewidth=2, alpha=0.7, label='Random Selection')

    # Add horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)

    # Labels and styling
    ax.set_xlabel('Interaction Strength', fontsize=11)
    ax.set_ylabel('Pairwise Selection Correlation', fontsize=11)
    ax.legend(fontsize=9, frameon=True, fancybox=False, edgecolor='black')
    ax.grid(axis='both', alpha=0.3, linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Save
    save_path_png = os.path.join(save_dir, 'correlation_vs_interaction_strength.png')
    plt.savefig(save_path_png, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path_png}")

    save_path_svg = os.path.join(save_dir, 'correlation_vs_interaction_strength.svg')
    plt.savefig(save_path_svg, format='svg', bbox_inches='tight')
    print(f"Saved: {save_path_svg}")

    # Also save PDF
    save_path_pdf = os.path.join(save_dir, 'correlation_vs_interaction_strength.pdf')
    plt.savefig(save_path_pdf, format='pdf', bbox_inches='tight')
    print(f"Saved: {save_path_pdf}")

    # Copy to supplementary_figs directory
    import shutil
    script_dir = os.path.dirname(os.path.abspath(__file__))
    supp_dir = os.path.join(script_dir, '..', 'Draft', 'v3', 'latex', 'supplementary_figs')
    supp_dir = os.path.normpath(supp_dir)
    os.makedirs(supp_dir, exist_ok=True)
    shutil.copy2(save_path_png, os.path.join(supp_dir, 'correlation_vs_interaction_strength.png'))
    shutil.copy2(save_path_svg, os.path.join(supp_dir, 'correlation_vs_interaction_strength.svg'))
    shutil.copy2(save_path_pdf, os.path.join(supp_dir, 'correlation_vs_interaction_strength.pdf'))
    print(f"Copied to supplementary_figs")

    plt.close()


def plot_difference_vs_interaction(df, save_dir):
    """
    Create line plot of Δ(Same-Mixed) vs interaction strength.

    Shows how the difference between same-origin and mixed-origin
    correlations changes with interaction strength.
    """
    # Extract data
    interaction_strengths = df['Interaction_Strength'].values
    differences = df['Δ(Same-Mixed)'].astype(float).values

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(4, 3))

    # Plot line
    ax.plot(interaction_strengths, differences, 'o-',
            color='#2ecc71', linewidth=2.5, markersize=10,
            markeredgecolor='black', markeredgewidth=1.5)

    # Add horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)

    # Labels and styling
    ax.set_xlabel('Interaction Strength', fontsize=11)
    ax.set_ylabel('Δ(Same Parent − Cross Parents)', fontsize=11)
    ax.grid(axis='both', alpha=0.3, linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Save
    save_path_png = os.path.join(save_dir, 'correlation_difference_vs_interaction_strength.png')
    plt.savefig(save_path_png, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path_png}")

    save_path_svg = os.path.join(save_dir, 'correlation_difference_vs_interaction_strength.svg')
    plt.savefig(save_path_svg, format='svg', bbox_inches='tight')
    print(f"Saved: {save_path_svg}")

    plt.close()


def plot_combined_view(df, save_dir):
    """
    Create a 2-panel figure:
    - Top: Same-origin and Mixed-origin vs interaction strength
    - Bottom: Difference (Δ) vs interaction strength
    """
    # Extract data
    interaction_strengths = df['Interaction_Strength'].values
    same_origin = df['Same Parent'].astype(float).values
    mixed_origin = df['Cross Parents'].astype(float).values
    random_selection = df['Random'].astype(float).values
    differences = df['Δ(Same-Mixed)'].astype(float).values

    # Calculate mean random selection value for baseline
    random_baseline = np.mean(random_selection)

    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4.5, 6), sharex=True)

    # Top panel: Individual correlations
    ax1.plot(interaction_strengths, same_origin, 'o-',
            color='#e74c3c', linewidth=2, markersize=8,
            label='Same Parent', markeredgecolor='black', markeredgewidth=1)

    ax1.plot(interaction_strengths, mixed_origin, 's-',
            color='#3498db', linewidth=2, markersize=8,
            label='Cross Parents', markeredgecolor='black', markeredgewidth=1)

    # Add random selection as horizontal baseline
    ax1.axhline(y=random_baseline, color='#95a5a6', linestyle='-',
                linewidth=2, alpha=0.7, label='Random Selection')

    ax1.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.set_ylabel('Pairwise Correlation', fontsize=11)
    ax1.legend(fontsize=9, frameon=True, fancybox=False, edgecolor='black', loc='upper left')
    ax1.grid(axis='both', alpha=0.3, linewidth=0.5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.text(0.02, 0.98, 'A', transform=ax1.transAxes,
             fontsize=14, fontweight='bold', va='top')

    # Bottom panel: Difference
    ax2.plot(interaction_strengths, differences, 'o-',
            color='#2ecc71', linewidth=2.5, markersize=10,
            markeredgecolor='black', markeredgewidth=1.5)

    ax2.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    ax2.set_xlabel('Interaction Strength', fontsize=11)
    ax2.set_ylabel('Δ(Same − Mixed)', fontsize=11)
    ax2.grid(axis='both', alpha=0.3, linewidth=0.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.text(0.02, 0.98, 'B', transform=ax2.transAxes,
             fontsize=14, fontweight='bold', va='top')

    plt.tight_layout()

    # Save
    save_path_png = os.path.join(save_dir, 'correlation_vs_interaction_combined.png')
    plt.savefig(save_path_png, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path_png}")

    save_path_svg = os.path.join(save_dir, 'correlation_vs_interaction_combined.svg')
    plt.savefig(save_path_svg, format='svg', bbox_inches='tight')
    print(f"Saved: {save_path_svg}")

    plt.close()


def main():
    """Main function."""
    print("="*80)
    print("PLOTTING CORRELATION VS INTERACTION STRENGTH")
    print("="*80)

    # Load data
    df = load_simulation_summary()

    print("\nSimulation data:")
    print(df.to_string(index=False))

    save_dir = "Figure/AsymmetricityNullModelAnalysis_simulation/correlation_analysis"
    os.makedirs(save_dir, exist_ok=True)

    print("\n" + "="*80)
    print("Creating line plots...")
    print("="*80 + "\n")

    # Create plots
    plot_correlations_vs_interaction(df, save_dir)
    plot_difference_vs_interaction(df, save_dir)
    plot_combined_view(df, save_dir)

    print("\n" + "="*80)
    print("COMPLETE!")
    print(f"Results saved to: {save_dir}")
    print("="*80)


if __name__ == "__main__":
    main()
