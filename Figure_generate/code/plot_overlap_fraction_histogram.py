#!/usr/bin/env python3
"""
Plot histogram of overlapping ASVs fraction across media conditions.

ASVs_overlap1 = Fraction of ASVs in the coalesced community that were present
                in BOTH parental communities before mixing.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os


EXCEPTION_LIST = {
    'P4-02', 'P4-03', 'P4-23', 'P4-24', 'P7-97', 'P8-12',
    'P8-91',
    'P5-73', 'P5-69', 'P5-64', 'P5-61', 'P5-59', 'P5-56',
    'P5-47', 'P5-50',
    'P5-39', 'P5-87', 'P5-54', 'P6-02', 'P6-47', 'P6-74', 'P6-57',
}


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


def load_coalescence_data():
    """Load processed coalescence event data"""
    file_path = '../../Analyzed/processed_CoalescenceEvent_synthetic.xlsx'
    df = pd.read_excel(file_path)
    print(f"Loaded {len(df)} coalescence events")
    df = df[~df['SampleIDX'].isin(EXCEPTION_LIST)].copy()
    print(f"Retained {len(df)} valid coalescence events after excluding missing/invalid samples")
    return df


def create_overlap_histogram(df, output_dir):
    """
    Create histogram of overlapping ASVs fraction across media conditions.
    """
    print("\nCreating overlap fraction histogram...")

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
        ax.text(0.95, 0.95, f'Mean: {mean_val:.3f}\nStd: {std_val:.3f}',
                transform=ax.transAxes, va='top', ha='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                fontsize=9)

    axes[0].set_ylabel('Number of Coalescence Events')

    plt.suptitle('Fraction of Coalesced ASVs Present in Both Parents', fontsize=12, y=1.02)
    plt.tight_layout()

    # Save figures
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_histogram.svg'),
                dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_histogram.png'),
                dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_histogram.pdf'),
                dpi=300, bbox_inches='tight')

    print(f"  Saved figures to {output_dir}/")
    plt.close(fig)

    return all_stats


def create_combined_barplot(df, output_dir):
    """
    Create a bar plot comparing overlap fraction across media conditions.
    """
    print("\nCreating combined bar plot...")

    # Medium mapping
    medium_colors = {'L': '#A7216A', 'M': '#802000', 'H': '#E24912'}
    medium_labels = ['Nutr-', 'Base', 'Nutr+']
    medium_codes = ['L', 'M', 'H']

    overlap_col = 'ASVs_overlap1_3'

    fig, ax = plt.subplots(figsize=(5, 4))

    means = []
    stds = []
    ns = []

    for medium_code in medium_codes:
        subset = df[df['Medium'] == medium_code]
        overlap_values = subset[overlap_col].dropna().values
        means.append(np.mean(overlap_values))
        stds.append(np.std(overlap_values) / np.sqrt(len(overlap_values)))  # SEM
        ns.append(len(overlap_values))

    x_pos = np.arange(len(medium_codes))
    bars = ax.bar(x_pos, means, yerr=stds,
                  color=[medium_colors[m] for m in medium_codes],
                  alpha=0.8, capsize=5, edgecolor='black', linewidth=0.8,
                  error_kw={'elinewidth': 1.5, 'capthick': 1.5})

    ax.set_ylabel('Overlap Fraction')
    ax.set_xlabel('Medium')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(medium_labels)
    ax.set_ylim(0, 0.35)
    ax.set_title('Fraction of Coalesced ASVs\nPresent in Both Parents')

    # Add sample size annotations
    for i, (mean, n) in enumerate(zip(means, ns)):
        ax.text(i, mean + 0.03, f'n={n}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()

    # Save figures
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_barplot.svg'),
                dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_barplot.png'),
                dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'overlap_fraction_barplot.pdf'),
                dpi=300, bbox_inches='tight')

    print(f"  Saved bar plot to {output_dir}/")
    plt.close(fig)


def main():
    """Main function to generate overlap fraction plots"""

    # Set style
    set_academic_style()

    # Output directory
    output_dir = 'Figure/Overlap_Fraction'
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    print("\n=== Overlap Fraction Analysis ===\n")

    # Load data
    df = load_coalescence_data()

    # Create histogram
    stats = create_overlap_histogram(df, output_dir)

    # Create bar plot
    create_combined_barplot(df, output_dir)

    # Print summary
    print("\n=== Summary ===")
    print("ASVs_overlap1_3: Fraction of coalesced ASVs present in BOTH parents")
    print("-" * 50)
    for medium, s in stats.items():
        print(f"  {medium}: {s['mean']:.3f} ± {s['std']:.3f} (n={s['n']})")

    print(f"\nFigures saved to: {output_dir}/")
    print("  - overlap_fraction_histogram.svg/png/pdf")
    print("  - overlap_fraction_barplot.svg/png/pdf")


if __name__ == "__main__":
    main()
