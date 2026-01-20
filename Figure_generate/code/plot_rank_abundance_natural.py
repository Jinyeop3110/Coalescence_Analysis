#!/usr/bin/env python3
"""
Rank-Abundance Plot: Natural Sample-Derived Communities.

Generates rank-abundance distributions for natural sample-derived communities
across nutrient conditions, similar to synthetic community plots (Suppl. Figs 18-20).

Reports mean ASV richness with 0.1% threshold for main text.

Author: Gore Lab
Date: January 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Plot style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# Data paths
COALESCENCE_NATURAL_PATH = "../../Analyzed/processed_CoalescenceEvent_natural.xlsx"
COMMUNITIES_NATURAL_PATH = "../../Analyzed/processed_Communities_natural.xlsx"
PROCESSED_SEQUENCES_NATURAL_PATH = "../../Postprocessed/processed_Sequences_natural.xlsx"
METADATA_PATH = "../../Postprocessed/Metadata.xlsx"

# Output directory
OUTPUT_DIR = "Figure/RankAbundance_Natural"


def get_medium_color(medium):
    """Get color for each medium condition."""
    colors = {
        'L': '#A7216A',  # Nutr-
        'M': '#802000',  # Base
        'H': '#E24912',  # Nutr+
        'LN': '#A7216A',
        'MN': '#802000',
        'HN': '#E24912'
    }
    return colors.get(medium, '#333333')


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


def count_asv_richness(abundance_vector, threshold=0.001):
    """Count number of ASVs above threshold (0.1% = 0.001)."""
    return np.sum(np.array(abundance_vector) > threshold)


def load_natural_community_data():
    """Load natural community abundance data."""
    print("Loading natural community data...")

    try:
        communities_data = pd.read_excel(COMMUNITIES_NATURAL_PATH, engine='openpyxl')
        processed_sequences = pd.read_excel(PROCESSED_SEQUENCES_NATURAL_PATH, engine='openpyxl')
        metadata = pd.read_excel(METADATA_PATH, engine='openpyxl')
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None

    print(f"  Communities: {len(communities_data)} records")
    print(f"  Sequences: {len(processed_sequences)} records")

    return communities_data, processed_sequences, metadata


def get_natural_community_abundances(communities_data, processed_sequences, metadata, medium='M'):
    """
    Get abundance profiles for natural parental and coalesced communities.

    Args:
        communities_data: DataFrame with community metadata
        processed_sequences: DataFrame with abundance data
        metadata: DataFrame with sample metadata
        medium: 'L' (Nutr-), 'M' (Base), or 'H' (Nutr+)

    Returns:
        parental_data: list of abundance arrays for parental communities
        coalesced_data: list of abundance arrays for coalesced communities
    """
    # Filter for natural communities
    communities = communities_data[communities_data['CommunityOrigin'] == 'N']
    communities = communities[communities['Medium'] == medium]

    # Get abundance columns (skip SampleIDX column)
    abundance_cols = [c for c in processed_sequences.columns if c != 'SampleIDX']

    parental_data = []
    coalesced_data = []

    for _, row in communities.iterrows():
        sample_idx = row['SampleIDX']
        coal_type = row.get('CoalescenceType', 'S')  # Default to 'S' if not present

        # Get abundance vector
        seq_row = processed_sequences[processed_sequences['SampleIDX'] == sample_idx]
        if len(seq_row) > 0:
            abundances = seq_row[abundance_cols].values[0].astype(float)
            abundances = np.nan_to_num(abundances, 0)

            # Normalize
            if np.sum(abundances) > 0:
                abundances = abundances / np.sum(abundances)

            if coal_type == 'S':  # Subcommunity = Parental
                parental_data.append(abundances)
            elif coal_type == 'C':  # Coalesced
                coalesced_data.append(abundances)

    return parental_data, coalesced_data


def plot_natural_rank_abundance(parental_data, coalesced_data, medium='M', save_path=None):
    """
    Plot rank-abundance curves for natural communities.

    Args:
        parental_data: list of abundance arrays for parental communities
        coalesced_data: list of abundance arrays for coalesced communities
        medium: 'L' (Nutr-), 'M' (Base), or 'H' (Nutr+)
        save_path: Path to save the figure
    """
    medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}
    medium_color = get_medium_color(medium)

    fig, axes = plt.subplots(1, 2, figsize=(7, 3))

    # ========== Panel A: Parental Communities ==========
    ax = axes[0]
    gini_values_parental = []
    richness_values_parental = []

    for abundances in parental_data:
        # Sort by rank
        sorted_ab = np.sort(abundances)[::-1]
        nonzero_mask = sorted_ab > 1e-6
        sorted_ab = sorted_ab[nonzero_mask]

        if len(sorted_ab) == 0:
            continue

        ranks = np.arange(1, len(sorted_ab) + 1)

        # Calculate Gini and richness
        gini = calculate_gini(sorted_ab)
        gini_values_parental.append(gini)

        richness = count_asv_richness(abundances, threshold=0.001)
        richness_values_parental.append(richness)

        # Plot each community line
        ax.semilogy(ranks, sorted_ab, '-', color=medium_color, alpha=0.5, linewidth=1.0)

    # Add statistics
    if gini_values_parental:
        mean_gini = np.mean(gini_values_parental)
        std_gini = np.std(gini_values_parental)
        mean_richness = np.mean(richness_values_parental)
        std_richness = np.std(richness_values_parental)
        ax.text(0.95, 0.95,
                f'Gini = {mean_gini:.2f}±{std_gini:.2f}\n'
                f'Richness = {mean_richness:.1f}±{std_richness:.1f}\n'
                f'(n={len(gini_values_parental)})',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('ASV Rank', fontsize=10)
    ax.set_ylabel('Relative Abundance', fontsize=10)
    ax.set_title('Parental Communities', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.text(-0.15, 1.05, 'A', transform=ax.transAxes, fontsize=12, fontweight='bold')
    ax.set_ylim(1e-4, 1.5)
    ax.axhline(y=0.001, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)  # 0.1% threshold

    # ========== Panel B: Coalesced Communities ==========
    ax = axes[1]
    gini_values_coalesced = []
    richness_values_coalesced = []

    for abundances in coalesced_data:
        # Sort by rank
        sorted_ab = np.sort(abundances)[::-1]
        nonzero_mask = sorted_ab > 1e-6
        sorted_ab = sorted_ab[nonzero_mask]

        if len(sorted_ab) == 0:
            continue

        ranks = np.arange(1, len(sorted_ab) + 1)

        # Calculate Gini and richness
        gini = calculate_gini(sorted_ab)
        gini_values_coalesced.append(gini)

        richness = count_asv_richness(abundances, threshold=0.001)
        richness_values_coalesced.append(richness)

        # Plot each community line
        ax.semilogy(ranks, sorted_ab, '-', color=medium_color, alpha=0.5, linewidth=1.0)

    # Add statistics
    if gini_values_coalesced:
        mean_gini = np.mean(gini_values_coalesced)
        std_gini = np.std(gini_values_coalesced)
        mean_richness = np.mean(richness_values_coalesced)
        std_richness = np.std(richness_values_coalesced)
        ax.text(0.95, 0.95,
                f'Gini = {mean_gini:.2f}±{std_gini:.2f}\n'
                f'Richness = {mean_richness:.1f}±{std_richness:.1f}\n'
                f'(n={len(gini_values_coalesced)})',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('ASV Rank', fontsize=10)
    ax.set_ylabel('Relative Abundance', fontsize=10)
    ax.set_title('Coalesced Communities', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.text(-0.15, 1.05, 'B', transform=ax.transAxes, fontsize=12, fontweight='bold')
    ax.set_ylim(1e-4, 1.5)
    ax.axhline(y=0.001, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)  # 0.1% threshold

    # Add medium label as suptitle
    fig.suptitle(f'{medium_labels[medium]} - Natural Communities', fontsize=12, fontweight='bold',
                 color=medium_color, y=1.02)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        svg_path = save_path.replace('.pdf', '.svg')
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        print(f"  Saved: {save_path}")

    plt.close()

    return gini_values_parental, gini_values_coalesced, richness_values_parental, richness_values_coalesced


def main():
    """Generate rank-abundance plots for natural communities."""
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}\n")

    # Load data
    communities_data, processed_sequences, metadata = load_natural_community_data()

    if communities_data is None:
        print("Failed to load data!")
        return

    medium_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}

    print("\n" + "="*60)
    print("NATURAL COMMUNITY RANK-ABUNDANCE ANALYSIS")
    print("="*60)

    all_richness_parental = []
    all_richness_coalesced = []

    for medium in ['L', 'M', 'H']:
        print(f"\n=== {medium_labels[medium]} ===")

        parental_data, coalesced_data = get_natural_community_abundances(
            communities_data, processed_sequences, metadata, medium=medium
        )

        print(f"  Parental communities: {len(parental_data)}")
        print(f"  Coalesced communities: {len(coalesced_data)}")

        if len(parental_data) == 0 and len(coalesced_data) == 0:
            print("  No data found for this condition")
            continue

        gini_p, gini_c, richness_p, richness_c = plot_natural_rank_abundance(
            parental_data, coalesced_data,
            medium=medium,
            save_path=os.path.join(OUTPUT_DIR, f"rank_abundance_natural_{medium_labels[medium]}.pdf")
        )

        if richness_p:
            all_richness_parental.extend(richness_p)
            print(f"  Parental: Gini = {np.mean(gini_p):.3f} ± {np.std(gini_p):.3f}, "
                  f"Richness = {np.mean(richness_p):.1f} ± {np.std(richness_p):.1f} (n={len(richness_p)})")
        if richness_c:
            all_richness_coalesced.extend(richness_c)
            print(f"  Coalesced: Gini = {np.mean(gini_c):.3f} ± {np.std(gini_c):.3f}, "
                  f"Richness = {np.mean(richness_c):.1f} ± {np.std(richness_c):.1f} (n={len(richness_c)})")

    # Overall summary
    print("\n" + "="*60)
    print("SUMMARY FOR MAIN TEXT (0.1% threshold)")
    print("="*60)

    if all_richness_parental:
        print(f"\nNatural parental communities (pooled):")
        print(f"  Mean ASV richness: {np.mean(all_richness_parental):.1f} ± {np.std(all_richness_parental):.1f}")
        print(f"  n = {len(all_richness_parental)} communities")

    if all_richness_coalesced:
        print(f"\nNatural coalesced communities (pooled):")
        print(f"  Mean ASV richness: {np.mean(all_richness_coalesced):.1f} ± {np.std(all_richness_coalesced):.1f}")
        print(f"  n = {len(all_richness_coalesced)} communities")

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"\nFigures saved to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
