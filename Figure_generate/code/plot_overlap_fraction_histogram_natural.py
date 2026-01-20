#!/usr/bin/env python3
"""
Plot histogram of overlapping ASVs fraction for NATURAL communities across media conditions.

ASVs_overlap1 = Fraction of ASVs in the coalesced community that were present
                in BOTH parental communities before mixing.

Author: Gore Lab
Date: January 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os


def set_academic_style():
    """Set matplotlib parameters for academic paper quality figures"""
    rcParams['font.family'] = 'Arial'
    rcParams['font.size'] = 10
    rcParams['axes.titlesize'] = 12
    rcParams['axes.labelsize'] = 11
    rcParams['xtick.labelsize'] = 10
    rcParams['ytick.labelsize'] = 10
    rcParams['legend.fontsize'] = 9
    rcParams['axes.linewidth'] = 1.0
    rcParams['xtick.major.width'] = 1.0
    rcParams['ytick.major.width'] = 1.0
    rcParams['axes.spines.top'] = False
    rcParams['axes.spines.right'] = False
    rcParams['savefig.dpi'] = 300
    rcParams['savefig.bbox'] = 'tight'
    rcParams['pdf.fonttype'] = 42


def load_coalescence_data_natural():
    """Load processed coalescence event data for natural communities"""
    file_path = '../../Analyzed/processed_CoalescenceEvent_natural.xlsx'
    df = pd.read_excel(file_path, engine='openpyxl')
    print(f"Loaded {len(df)} natural coalescence events")
    return df


def create_overlap_histogram_natural(df, output_dir):
    """
    Create histogram of overlapping ASVs fraction across media conditions for natural communities.
    """
    print("\nCreating overlap fraction histogram for natural communities...")

    # Medium mapping
    medium_map = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
    medium_colors = {'L': '#A7216A', 'M': '#802000', 'H': '#E24912'}  # From COLORMAP

    # Use threshold level 3 (common choice)
    overlap_col = 'ASVs_overlap1_3'

    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

    all_stats = {}

    for idx, (medium_code, medium_name) in enumerate([('L', 'Nutr-'), ('M', 'Base'), ('H', 'Nutr+')]):
        ax = axes[idx]

        # Get data for this medium
        subset = df[df['Medium'] == medium_code]
        overlap_values = subset[overlap_col].dropna().values

        n_events = len(overlap_values)
        mean_val = np.mean(overlap_values)
        std_val = np.std(overlap_values)

        all_stats[medium_name] = {'n': n_events, 'mean': mean_val, 'std': std_val}

        # Create histogram
        ax.hist(overlap_values, bins=15, edgecolor='black', linewidth=0.8,
                color=medium_colors[medium_code], alpha=0.8, range=(0, 1))

        ax.set_xlabel('Overlap Fraction')
        ax.set_title(f'{medium_name}\n(n = {n_events})')
        ax.set_xlim(0, 1)

        # Add mean line and annotation
        ax.axvline(mean_val, color='black', linestyle='--', linewidth=1.5)
        ax.text(0.95, 0.95, f'Mean: {mean_val:.2f}\nStd: {std_val:.2f}',
                transform=ax.transAxes, va='top', ha='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                fontsize=9)

    axes[0].set_ylabel('Number of Coalescence Events')

    plt.suptitle('Natural Communities: Fraction of Coalesced ASVs Present in Both Parents',
                 fontsize=12, y=1.02)
    plt.tight_layout()

    # Save figures
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_histogram_natural.svg'),
                dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_histogram_natural.png'),
                dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_histogram_natural.pdf'),
                dpi=300, bbox_inches='tight')

    print(f"  Saved figures to {output_dir}/")
    plt.close(fig)

    return all_stats


def main():
    """Main function to generate overlap fraction plots for natural communities"""

    # Set style
    set_academic_style()

    # Output directory
    output_dir = 'Figure/Overlap_Fraction'
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    print("\n=== Overlap Fraction Analysis (Natural Communities) ===\n")

    # Load data
    df = load_coalescence_data_natural()

    # Create histogram
    stats = create_overlap_histogram_natural(df, output_dir)

    # Print summary
    print("\n=== Summary ===")
    print("ASVs_overlap1_3: Fraction of coalesced ASVs present in BOTH parents")
    print("-" * 50)
    for medium, s in stats.items():
        print(f"  {medium}: {s['mean']:.2f} ± {s['std']:.2f} (n={s['n']})")

    print(f"\nFigures saved to: {output_dir}/")
    print("  - overlap_fraction_histogram_natural.svg/png/pdf")


if __name__ == "__main__":
    main()
