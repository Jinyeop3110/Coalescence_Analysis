#!/usr/bin/env python3
"""
Rank-Abundance Plot: Parental vs Coalesced Communities.

Compares rank-abundance distributions between parental (sub)communities
and coalesced communities for each nutrient condition.

Author: Gore Lab
Date: November 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_setup import (
    Communities_data,
    Processed_sequences_synthetic,
)
from COLORMAP import get_medium_color

# Plot style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def get_community_abundances_by_type(medium='M'):
    """
    Get abundance profiles for parental and coalesced communities for a specific medium.

    Args:
        medium: 'L' (Nutr-), 'M' (Base), or 'H' (Nutr+)

    Returns:
        parental_data: list of abundance arrays for parental communities
        coalesced_data: list of abundance arrays for coalesced communities
    """
    # Filter for synthetic communities
    communities = Communities_data[Communities_data['CommunityOrigin'] == 'S']
    communities = communities[communities['Medium'] == medium]

    # Get abundance columns
    abundance_cols = [c for c in Processed_sequences_synthetic.columns if 'NormalizedAbundance' in c]

    parental_data = []
    coalesced_data = []

    for _, row in communities.iterrows():
        sample_idx = row['SampleIDX']
        coal_type = row['CoalescenceType']

        # Get abundance vector
        seq_row = Processed_sequences_synthetic[Processed_sequences_synthetic['SampleIDX'] == sample_idx]
        if len(seq_row) > 0:
            abundances = seq_row[abundance_cols].values[0].astype(float)

            if coal_type == 'S':  # Subcommunity = Parental
                parental_data.append(abundances)
            elif coal_type == 'C':  # Coalesced
                coalesced_data.append(abundances)

    return parental_data, coalesced_data


def calculate_gini(abundances):
    """Calculate Gini coefficient for abundance distribution."""
    abundances = np.array(abundances, dtype=float)
    abundances = abundances[abundances > 0]

    if len(abundances) == 0:
        return 0

    abundances = np.sort(abundances)
    n = len(abundances)

    gini = (2 * np.sum((np.arange(1, n + 1) * abundances))) / (n * np.sum(abundances)) - (n + 1) / n
    return max(0, min(1, gini))


def plot_parental_vs_coalesced(medium='M', save_path=None):
    """
    Plot rank-abundance curves comparing parental vs coalesced communities.

    Args:
        medium: 'L' (Nutr-), 'M' (Base), or 'H' (Nutr+)
        save_path: Path to save the figure
    """
    medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
    medium_color = get_medium_color(medium)

    parental_data, coalesced_data = get_community_abundances_by_type(medium)

    fig, axes = plt.subplots(1, 2, figsize=(7, 3))

    # ========== Panel A: Parental Communities ==========
    ax = axes[0]
    gini_values_parental = []

    for abundances in parental_data:
        # Normalize
        abundances = abundances / np.sum(abundances) if np.sum(abundances) > 0 else abundances

        # Sort by rank
        sorted_ab = np.sort(abundances)[::-1]
        nonzero_mask = sorted_ab > 1e-6
        sorted_ab = sorted_ab[nonzero_mask]

        if len(sorted_ab) == 0:
            continue

        ranks = np.arange(1, len(sorted_ab) + 1)

        # Calculate Gini
        gini = calculate_gini(sorted_ab)
        gini_values_parental.append(gini)

        # Plot each community line
        ax.semilogy(ranks, sorted_ab, '-', color=medium_color, alpha=0.4, linewidth=0.8)

    # Add statistics
    if gini_values_parental:
        mean_gini = np.mean(gini_values_parental)
        std_gini = np.std(gini_values_parental)
        ax.text(0.95, 0.95, f'Gini = {mean_gini:.2f}±{std_gini:.2f}\n(n={len(gini_values_parental)})',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('ASV Rank', fontsize=10)
    ax.set_ylabel('Relative Abundance', fontsize=10)
    ax.set_title('Parental Communities', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.text(-0.15, 1.05, 'A', transform=ax.transAxes, fontsize=12, fontweight='bold')
    ax.set_ylim(1e-4, 1.5)

    # ========== Panel B: Coalesced Communities ==========
    ax = axes[1]
    gini_values_coalesced = []

    for abundances in coalesced_data:
        # Normalize
        abundances = abundances / np.sum(abundances) if np.sum(abundances) > 0 else abundances

        # Sort by rank
        sorted_ab = np.sort(abundances)[::-1]
        nonzero_mask = sorted_ab > 1e-6
        sorted_ab = sorted_ab[nonzero_mask]

        if len(sorted_ab) == 0:
            continue

        ranks = np.arange(1, len(sorted_ab) + 1)

        # Calculate Gini
        gini = calculate_gini(sorted_ab)
        gini_values_coalesced.append(gini)

        # Plot each community line
        ax.semilogy(ranks, sorted_ab, '-', color=medium_color, alpha=0.4, linewidth=0.8)

    # Add statistics
    if gini_values_coalesced:
        mean_gini = np.mean(gini_values_coalesced)
        std_gini = np.std(gini_values_coalesced)
        ax.text(0.95, 0.95, f'Gini = {mean_gini:.2f}±{std_gini:.2f}\n(n={len(gini_values_coalesced)})',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('ASV Rank', fontsize=10)
    ax.set_ylabel('Relative Abundance', fontsize=10)
    ax.set_title('Coalesced Communities', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.text(-0.15, 1.05, 'B', transform=ax.transAxes, fontsize=12, fontweight='bold')
    ax.set_ylim(1e-4, 1.5)

    # Add medium label as suptitle
    fig.suptitle(medium_labels[medium], fontsize=12, fontweight='bold', color=medium_color, y=1.02)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.pdf'), format='pdf', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()

    return gini_values_parental, gini_values_coalesced


def main():
    """Generate rank-abundance plots for each medium."""
    # Output directory
    save_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Figure", "SkewedDistributionTest"
    )
    os.makedirs(save_dir, exist_ok=True)

    medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}

    print("Generating rank-abundance plots (parental vs coalesced)...\n")

    for medium in ['L', 'M', 'H']:
        print(f"=== {medium_labels[medium]} ===")
        gini_parental, gini_coalesced = plot_parental_vs_coalesced(
            medium=medium,
            save_path=os.path.join(save_dir, f"rank_abundance_parental_vs_coalesced_{medium}.png")
        )

        if gini_parental and gini_coalesced:
            print(f"  Parental: Gini = {np.mean(gini_parental):.3f} ± {np.std(gini_parental):.3f} (n={len(gini_parental)})")
            print(f"  Coalesced: Gini = {np.mean(gini_coalesced):.3f} ± {np.std(gini_coalesced):.3f} (n={len(gini_coalesced)})")
        print()


if __name__ == "__main__":
    main()
