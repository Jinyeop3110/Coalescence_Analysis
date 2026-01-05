#!/usr/bin/env python3
"""
Rank-Abundance Plot for Parental Communities (Subcommunities).

This script generates rank-abundance curves to visualize the skewness
of relative abundance distributions in parental communities.

Two versions:
1. Total normalized abundance: Each ASV's abundance summed across all communities
2. Community-wise: Each line represents one subcommunity's rank-abundance curve

Author: Gore Lab
Date: November 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_setup import (
    Communities_data,
    Processed_sequences_synthetic,
    Processed_sequences_natural
)

# Plot style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def get_subcommunity_abundances(data_type='synthetic'):
    """
    Get abundance profiles for all subcommunities (parental communities).

    Returns:
        list of dicts with keys: 'sample_idx', 'medium', 'replicate', 'abundances'
    """
    if data_type == 'synthetic':
        communities = Communities_data[Communities_data['CommunityOrigin'] == 'S']
        processed_seq = Processed_sequences_synthetic
    else:
        communities = Communities_data[Communities_data['CommunityOrigin'] == 'N']
        processed_seq = Processed_sequences_natural

    # Filter for subcommunities (parental communities before coalescence)
    subcommunities = communities[communities['CoalescenceType'] == 'S']

    # Get abundance columns
    abundance_cols = [c for c in processed_seq.columns if 'NormalizedAbundance' in c]

    results = []
    for _, row in subcommunities.iterrows():
        sample_idx = row['SampleIDX']
        medium = row['Medium']
        replicate = row['Replicate']

        # Get abundance vector
        seq_row = processed_seq[processed_seq['SampleIDX'] == sample_idx]
        if len(seq_row) > 0:
            abundances = seq_row[abundance_cols].values[0].astype(float)
            results.append({
                'sample_idx': sample_idx,
                'medium': medium,
                'replicate': replicate,
                'abundances': abundances
            })

    return results


def plot_total_rank_abundance(subcommunity_data, save_path=None):
    """
    Plot rank-abundance curve of total abundance across all communities.
    Each ASV's abundance is summed across all communities and then normalized.
    """
    # Sum abundances across all communities
    all_abundances = np.array([d['abundances'] for d in subcommunity_data])
    total_abundance = np.sum(all_abundances, axis=0)

    # Normalize to relative abundance
    total_abundance = total_abundance / np.sum(total_abundance)

    # Sort by rank (highest to lowest)
    sorted_abundance = np.sort(total_abundance)[::-1]

    # Filter to non-zero values
    nonzero_mask = sorted_abundance > 1e-6
    sorted_abundance = sorted_abundance[nonzero_mask]
    ranks = np.arange(1, len(sorted_abundance) + 1)

    # Create figure
    fig, ax = plt.subplots(figsize=(3.5, 3))

    ax.semilogy(ranks, sorted_abundance, 'o-', color='#D55E00',
                markersize=5, linewidth=1.5, markeredgecolor='black',
                markeredgewidth=0.3)

    ax.set_xlabel('ASV Rank', fontsize=10)
    ax.set_ylabel('Relative Abundance', fontsize=10)
    ax.set_title('Total Abundance\n(summed across communities)', fontsize=10)

    # Add Gini coefficient
    gini = calculate_gini(sorted_abundance)
    ax.text(0.95, 0.95, f'Gini = {gini:.3f}',
            transform=ax.transAxes, ha='right', va='top',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.pdf'), format='pdf', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()

    return sorted_abundance, gini


def plot_communitywise_rank_abundance(subcommunity_data, save_path=None,
                                       color_by='medium', alpha=0.3):
    """
    Plot rank-abundance curves for each subcommunity.
    Each line represents one community's rank-abundance profile.
    """
    fig, ax = plt.subplots(figsize=(4, 3.5))

    # Color mapping
    medium_colors = {'L': '#0072B2', 'M': '#009E73', 'H': '#D55E00'}  # Nutr-, Base, Nutr+
    medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}

    # Track for legend
    plotted_mediums = set()
    gini_values = []

    for d in subcommunity_data:
        abundances = d['abundances']
        medium = d['medium']

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
        gini_values.append(gini)

        # Plot
        color = medium_colors.get(medium, '#666666')
        label = medium_labels.get(medium, medium) if medium not in plotted_mediums else None
        plotted_mediums.add(medium)

        ax.semilogy(ranks, sorted_ab, '-', color=color, alpha=alpha, linewidth=0.8, label=label)

    ax.set_xlabel('ASV Rank', fontsize=10)
    ax.set_ylabel('Relative Abundance', fontsize=10)
    ax.set_title('Community-wise Abundance\n(each line = one community)', fontsize=10)

    # Add legend
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)

    # Add mean Gini
    mean_gini = np.mean(gini_values)
    ax.text(0.95, 0.60, f'Mean Gini = {mean_gini:.3f}\n(n={len(gini_values)})',
            transform=ax.transAxes, ha='right', va='top',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.pdf'), format='pdf', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()

    return gini_values


def plot_combined_rank_abundance(subcommunity_data, save_path=None):
    """
    Combined figure with both total and community-wise rank-abundance.
    """
    fig, axes = plt.subplots(1, 2, figsize=(7, 3))

    # ========== Panel A: Total Abundance ==========
    ax = axes[0]

    # Sum abundances across all communities
    all_abundances = np.array([d['abundances'] for d in subcommunity_data])
    total_abundance = np.sum(all_abundances, axis=0)
    total_abundance = total_abundance / np.sum(total_abundance)

    sorted_total = np.sort(total_abundance)[::-1]
    nonzero_mask = sorted_total > 1e-6
    sorted_total = sorted_total[nonzero_mask]
    ranks = np.arange(1, len(sorted_total) + 1)

    ax.semilogy(ranks, sorted_total, 'o-', color='#D55E00',
                markersize=4, linewidth=1.2, markeredgecolor='black',
                markeredgewidth=0.3)

    gini_total = calculate_gini(sorted_total)
    ax.text(0.95, 0.95, f'Gini = {gini_total:.3f}',
            transform=ax.transAxes, ha='right', va='top',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('ASV Rank', fontsize=10)
    ax.set_ylabel('Relative Abundance', fontsize=10)
    ax.set_title('Total (summed)', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.text(-0.15, 1.05, 'A', transform=ax.transAxes, fontsize=12, fontweight='bold')

    # ========== Panel B: Community-wise ==========
    ax = axes[1]

    medium_colors = {'L': '#0072B2', 'M': '#009E73', 'H': '#D55E00'}
    medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
    plotted_mediums = set()
    gini_values = []

    for d in subcommunity_data:
        abundances = d['abundances']
        medium = d['medium']

        abundances = abundances / np.sum(abundances) if np.sum(abundances) > 0 else abundances
        sorted_ab = np.sort(abundances)[::-1]
        nonzero_mask = sorted_ab > 1e-6
        sorted_ab = sorted_ab[nonzero_mask]

        if len(sorted_ab) == 0:
            continue

        ranks = np.arange(1, len(sorted_ab) + 1)
        gini = calculate_gini(sorted_ab)
        gini_values.append(gini)

        color = medium_colors.get(medium, '#666666')
        label = medium_labels.get(medium, medium) if medium not in plotted_mediums else None
        plotted_mediums.add(medium)

        ax.semilogy(ranks, sorted_ab, '-', color=color, alpha=0.3, linewidth=0.8, label=label)

    ax.set_xlabel('ASV Rank', fontsize=10)
    ax.set_ylabel('Relative Abundance', fontsize=10)
    ax.set_title('Community-wise', fontsize=10)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)

    mean_gini = np.mean(gini_values)
    ax.text(0.95, 0.55, f'Mean Gini = {mean_gini:.3f}\n(n={len(gini_values)})',
            transform=ax.transAxes, ha='right', va='top',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.text(-0.15, 1.05, 'B', transform=ax.transAxes, fontsize=12, fontweight='bold')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.pdf'), format='pdf', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()

    return gini_total, gini_values


def plot_separated_by_medium(subcommunity_data, save_path=None):
    """
    Figure with separate panels for each nutrient condition (Nutr-, Base, Nutr+).
    Each panel shows community-wise rank-abundance curves for that medium.
    """
    fig, axes = plt.subplots(1, 3, figsize=(9, 3))

    medium_order = ['L', 'M', 'H']
    medium_colors = {'L': '#0072B2', 'M': '#009E73', 'H': '#D55E00'}
    medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
    panel_labels = ['A', 'B', 'C']

    gini_by_medium = {}

    for idx, medium in enumerate(medium_order):
        ax = axes[idx]

        # Filter data for this medium
        medium_data = [d for d in subcommunity_data if d['medium'] == medium]
        gini_values = []

        for d in medium_data:
            abundances = d['abundances']

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
            gini_values.append(gini)

            # Plot each community line
            ax.semilogy(ranks, sorted_ab, '-', color=medium_colors[medium],
                       alpha=0.4, linewidth=0.8)

        gini_by_medium[medium] = gini_values

        # Add statistics
        if gini_values:
            mean_gini = np.mean(gini_values)
            ax.text(0.95, 0.95, f'Gini = {mean_gini:.3f}\n(n={len(gini_values)})',
                    transform=ax.transAxes, ha='right', va='top',
                    fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax.set_xlabel('ASV Rank', fontsize=10)
        if idx == 0:
            ax.set_ylabel('Relative Abundance', fontsize=10)
        ax.set_title(medium_labels[medium], fontsize=11, fontweight='bold',
                    color=medium_colors[medium])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.text(-0.15, 1.05, panel_labels[idx], transform=ax.transAxes,
               fontsize=12, fontweight='bold')

        # Set consistent y-axis limits
        ax.set_ylim(1e-4, 1.5)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.svg'), format='svg', bbox_inches='tight')
        plt.savefig(save_path.replace('.png', '.pdf'), format='pdf', bbox_inches='tight')
        print(f"Saved: {save_path}")

    plt.close()

    return gini_by_medium


def calculate_gini(abundances):
    """Calculate Gini coefficient for abundance distribution."""
    abundances = np.array(abundances, dtype=float)
    abundances = abundances[abundances > 0]

    if len(abundances) == 0:
        return 0

    abundances = np.sort(abundances)
    n = len(abundances)
    cumsum = np.cumsum(abundances)

    gini = (2 * np.sum((np.arange(1, n + 1) * abundances))) / (n * np.sum(abundances)) - (n + 1) / n
    return max(0, min(1, gini))


def main(data_type='synthetic'):
    """Generate rank-abundance plots."""
    print(f"Loading {data_type} subcommunity data...")
    subcommunity_data = get_subcommunity_abundances(data_type)
    print(f"Loaded {len(subcommunity_data)} subcommunities")

    # Output directory
    save_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Figure", "SkewedDistributionTest"
    )
    os.makedirs(save_dir, exist_ok=True)

    # Generate individual plots
    print("\nGenerating total rank-abundance plot...")
    plot_total_rank_abundance(
        subcommunity_data,
        save_path=os.path.join(save_dir, f"rank_abundance_total_{data_type}.png")
    )

    print("\nGenerating community-wise rank-abundance plot...")
    plot_communitywise_rank_abundance(
        subcommunity_data,
        save_path=os.path.join(save_dir, f"rank_abundance_communitywise_{data_type}.png")
    )

    # Generate combined plot
    print("\nGenerating combined rank-abundance plot...")
    gini_total, gini_values = plot_combined_rank_abundance(
        subcommunity_data,
        save_path=os.path.join(save_dir, f"rank_abundance_combined_{data_type}.png")
    )

    # Generate separated by medium plot
    print("\nGenerating separated by medium rank-abundance plot...")
    gini_by_medium = plot_separated_by_medium(
        subcommunity_data,
        save_path=os.path.join(save_dir, f"rank_abundance_by_medium_{data_type}.png")
    )

    print(f"\n=== Statistics ===")
    print(f"Total abundance Gini: {gini_total:.3f}")
    print(f"Community-wise mean Gini: {np.mean(gini_values):.3f} ± {np.std(gini_values):.3f}")
    print(f"  Range: [{np.min(gini_values):.3f}, {np.max(gini_values):.3f}]")

    print(f"\n=== By Medium ===")
    medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
    for medium in ['L', 'M', 'H']:
        if medium in gini_by_medium and gini_by_medium[medium]:
            vals = gini_by_medium[medium]
            print(f"  {medium_labels[medium]}: Gini = {np.mean(vals):.3f} ± {np.std(vals):.3f} (n={len(vals)})")


if __name__ == "__main__":
    main(data_type='synthetic')
