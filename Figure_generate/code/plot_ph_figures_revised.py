#!/usr/bin/env python3
"""
plot_ph_figures_revised.py

Revised pH-related figures for supplementary:
1. Fig S23: Combined ASV abundance vs community pH for both Base and Nutr+
   - Shows how key acidifier/alkalizer ASVs determine parent community pH
2. Fig S24 revised: Two panels showing pH difference vs outcome for Base and Nutr+
   (replacing the combined figure that only showed Nutr+ in panel B)

Author: Gore Lab
Date: January 2025
"""

from common_setup import *
from COLORMAP import get_medium_colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Create output directory
output_dir = "Figure/pH_Analysis"
os.makedirs(output_dir, exist_ok=True)


def load_parent_community_data():
    """Load parent community data with species abundance and pH"""
    print("Loading parent community data...")

    # Load abundance data
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)

    # Load metadata and communities data
    metadata = pd.read_excel("../../Postprocessed/Metadata.xlsx")
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])

    # Merge all data
    full_data = abundance_data.merge(
        metadata[['SampleIDX', 'CoalescenceType', 'Medium', 'CommunityIDX']],
        on='SampleIDX', how='inner'
    ).merge(
        communities_data[['SampleIDX', 'fieldPH1', 'fieldPH7']],
        on='SampleIDX', how='inner'
    )

    # Filter for PARENT communities only (CoalescenceType == 'S')
    parent_communities = full_data[full_data['CoalescenceType'] == 'S'].copy()

    # Remove records with missing pH data
    parent_communities = parent_communities[~parent_communities['fieldPH7'].isna()].copy()

    print(f"✓ Loaded {len(parent_communities)} parent communities with pH data")

    return parent_communities


def get_key_asvs():
    """
    Define key acidifier and alkalizer ASVs based on monoculture pH data.
    These are the ASVs that show strongest pH modification in monoculture.
    Based on Figure 15 (two_panel_ph_asv_figure.pdf):
    - Acidifiers (monoculture pH < 5.5): ASV 3, ASV 8, ASV 12
    - Alkalizers (monoculture pH > 6.5): ASV 9, ASV 11
    """
    # Key acidifiers (lower community pH when present)
    acidifiers = {
        'NormalizedAbundance3': 'ASV 3',   # Enterobacter - monoculture pH 3.8
        'NormalizedAbundance8': 'ASV 8',   # Citrobacter - monoculture pH 4.2
        'NormalizedAbundance12': 'ASV 12', # Serratia - monoculture pH 3.2
    }

    # Key alkalizers (raise community pH when present)
    alkalizers = {
        'NormalizedAbundance9': 'ASV 9',   # Pseudomonas - monoculture pH 5.5
        'NormalizedAbundance11': 'ASV 11', # Stenotrophomonas - monoculture pH 6.8
    }

    return acidifiers, alkalizers


def plot_asv_vs_community_ph(parent_communities):
    """
    Create combined figure showing ASV abundance vs parent community pH
    for key acidifiers and alkalizers, comparing Base and Nutr+ media.

    Layout:
    - Top row: Alkalizers (ASV 9, ASV 11) x 2 media = 4 panels
    - Bottom row: Acidifiers (ASV 3, ASV 8, ASV 12) x 2 media = 6 panels

    Note: Alkalizers on top because they show positive correlation (higher abundance = higher pH)
          Acidifiers on bottom because they show negative correlation (higher abundance = lower pH)
    """
    print("\nGenerating ASV vs Community pH figure...")

    acidifiers, alkalizers = get_key_asvs()

    # Create figure with different number of columns per row
    # Use gridspec for flexible layout
    n_acidifiers = len(acidifiers)  # 3
    n_alkalizers = len(alkalizers)  # 2
    n_cols = max(n_acidifiers, n_alkalizers) * 2  # 6 columns to fit all

    fig, axes = plt.subplots(2, n_cols, figsize=(n_cols * 40 * mm, 120 * mm), dpi=150)

    colors_media = get_medium_colors()
    media_list = [('M', 'Base', colors_media[1]), ('H', 'Nutr$+$', colors_media[2])]

    # Plot alkalizers (top row) - ASV 9, ASV 11
    for asv_idx, (asv_col, asv_label) in enumerate(alkalizers.items()):
        for med_idx, (medium, med_label, color) in enumerate(media_list):
            ax = axes[0, asv_idx * 2 + med_idx]

            # Filter for medium
            data = parent_communities[parent_communities['Medium'] == medium].copy()

            if asv_col in data.columns:
                x = data[asv_col].values
                y = data['fieldPH7'].values

                # Remove NaN
                valid = ~(np.isnan(x) | np.isnan(y))
                x = x[valid]
                y = y[valid]

                if len(x) > 3:
                    ax.scatter(x, y, alpha=0.4, s=20, color=color)

                    # Linear regression
                    slope, intercept, r, p, se = stats.linregress(x, y)
                    x_line = np.array([0, max(x)])
                    y_line = slope * x_line + intercept
                    ax.plot(x_line, y_line, color=color, linewidth=2)

                    # Annotate
                    sig_marker = '*' if p < 0.05 else ''
                    ax.text(0.95, 0.95, f'r = {r:.2f}{sig_marker}\np = {p:.3f}',
                           transform=ax.transAxes, ha='right', va='top', fontsize=9)

            ax.set_xlabel(f'{asv_label} Abundance')
            ax.set_ylabel('Community pH')
            ax.set_title(f'{asv_label}\n{med_label}', fontsize=10, fontweight='bold')
            ax.set_ylim(4, 9)

    # Hide extra axes in top row (if alkalizers < acidifiers)
    for extra_idx in range(n_alkalizers * 2, n_cols):
        axes[0, extra_idx].set_visible(False)

    # Plot acidifiers (bottom row) - ASV 3, ASV 8, ASV 12
    for asv_idx, (asv_col, asv_label) in enumerate(acidifiers.items()):
        for med_idx, (medium, med_label, color) in enumerate(media_list):
            ax = axes[1, asv_idx * 2 + med_idx]

            # Filter for medium
            data = parent_communities[parent_communities['Medium'] == medium].copy()

            if asv_col in data.columns:
                x = data[asv_col].values
                y = data['fieldPH7'].values

                # Remove NaN
                valid = ~(np.isnan(x) | np.isnan(y))
                x = x[valid]
                y = y[valid]

                if len(x) > 3:
                    ax.scatter(x, y, alpha=0.4, s=20, color=color)

                    # Linear regression
                    slope, intercept, r, p, se = stats.linregress(x, y)
                    x_line = np.array([0, max(x)])
                    y_line = slope * x_line + intercept
                    ax.plot(x_line, y_line, color=color, linewidth=2)

                    # Annotate
                    sig_marker = '*' if p < 0.05 else ''
                    ax.text(0.95, 0.95, f'r = {r:.2f}{sig_marker}\np = {p:.3f}',
                           transform=ax.transAxes, ha='right', va='top', fontsize=9)

            ax.set_xlabel(f'{asv_label} Abundance')
            ax.set_ylabel('Community pH')
            ax.set_title(f'{asv_label}\n{med_label}', fontsize=10, fontweight='bold')
            ax.set_ylim(4, 9)

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_S23_ASV_vs_pH_combined.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_S23_ASV_vs_pH_combined.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_S23_ASV_vs_pH_combined.pdf', bbox_inches='tight')
    plt.close()

    print(f"✓ Saved: {output_dir}/Fig_S23_ASV_vs_pH_combined.[svg/png/pdf]")


def analyze_acidic_vs_alkaline_competition():
    """
    Analyze acidic vs alkaline community competition for all media.
    """
    print("\nAnalyzing acidic vs alkaline competition...")

    results = {}

    for medium in ['L', 'M', 'H']:
        results[medium] = {
            'acidic_wins': 0,
            'alkaline_wins': 0,
            'tie': 0,
            'total': 0,
            'events': [],
            'ph_diffs': [],
            'pdis': []
        }

        # Get all coalescence events
        coal_idx_list = []
        for pool in [6, 12, 24]:
            coal_idx_list.extend(Community_PermutateList("F", "S", medium, "C", pool))

        for coal_idx in coal_idx_list:
            coal_event = Coalescence_data[Coalescence_data['SampleIDX'] == coal_idx]
            if len(coal_event) == 0:
                continue

            parent1_idx = coal_event['SampleIDX_Sub1'].values[0]
            parent2_idx = coal_event['SampleIDX_Sub2'].values[0]

            parent1_comm = Communities_data[Communities_data['SampleIDX'] == parent1_idx]
            parent2_comm = Communities_data[Communities_data['SampleIDX'] == parent2_idx]

            if len(parent1_comm) == 0 or len(parent2_comm) == 0:
                continue

            ph1 = parent1_comm['fieldPH7'].values[0]
            ph2 = parent2_comm['fieldPH7'].values[0]

            if np.isnan(ph1) or np.isnan(ph2):
                continue

            # Only consider events where one is acidic and one is alkaline
            neutral_zone = 0.5
            if not ((ph1 < 7 - neutral_zone and ph2 > 7 + neutral_zone) or
                    (ph1 > 7 + neutral_zone and ph2 < 7 - neutral_zone)):
                continue

            pdi = coal_event['SimilarityTo1_BC_5'].values[0]
            if np.isnan(pdi):
                continue

            if ph1 < ph2:
                acidic_parent = 1
                ph_diff = ph2 - ph1
                if pdi > 0.6:
                    results[medium]['acidic_wins'] += 1
                    winner = 'acidic'
                elif pdi < 0.4:
                    results[medium]['alkaline_wins'] += 1
                    winner = 'alkaline'
                else:
                    results[medium]['tie'] += 1
                    winner = 'tie'
            else:
                acidic_parent = 2
                ph_diff = ph1 - ph2
                if pdi < 0.4:
                    results[medium]['acidic_wins'] += 1
                    winner = 'acidic'
                elif pdi > 0.6:
                    results[medium]['alkaline_wins'] += 1
                    winner = 'alkaline'
                else:
                    results[medium]['tie'] += 1
                    winner = 'tie'

            results[medium]['total'] += 1
            results[medium]['ph_diffs'].append(ph_diff)
            results[medium]['pdis'].append(pdi if acidic_parent == 1 else 1 - pdi)
            results[medium]['events'].append({
                'coal_idx': coal_idx,
                'ph1': ph1,
                'ph2': ph2,
                'acidic_parent': acidic_parent,
                'pdi': pdi,
                'winner': winner
            })

    return results


def plot_ph_diff_vs_outcome_two_panel(results):
    """
    Create two-panel figure showing pH difference vs outcome for Base and Nutr+.
    This replaces the single-panel Panel B in the original Fig S24.
    """
    print("\nGenerating pH diff vs outcome two-panel figure...")

    fig, axes = plt.subplots(1, 2, figsize=(140*mm, 65*mm), dpi=150)
    colors_media = get_medium_colors()

    media = ['M', 'H']
    media_labels = ['Base', 'Nutr$+$']
    color_indices = [1, 2]
    panel_labels = ['A', 'B']

    for idx, (medium, med_label, color_idx, panel) in enumerate(zip(media, media_labels, color_indices, panel_labels)):
        ax = axes[idx]

        ph_diffs = results[medium]['ph_diffs']
        pdis = results[medium]['pdis']

        if len(ph_diffs) > 3:
            ax.scatter(ph_diffs, pdis, alpha=0.6, s=40, color=colors_media[color_idx])

            if len(set(ph_diffs)) > 1:
                slope, intercept, r, p, se = stats.linregress(ph_diffs, pdis)
                x_line = np.array([min(ph_diffs), max(ph_diffs)])
                y_line = slope * x_line + intercept
                ax.plot(x_line, y_line, color='black', linewidth=2, linestyle='--')

                ax.annotate(f'R² = {r**2:.2f}\np = {p:.3f}',
                           xy=(0.05, 0.95), xycoords='axes fraction',
                           verticalalignment='top', fontsize=10)

        ax.axhline(0.5, color='gray', linestyle=':', alpha=0.5)

        # Winner region shading
        ax.axhspan(0.6, 1.0, alpha=0.1, color='red')
        ax.axhspan(0.0, 0.4, alpha=0.1, color='blue')

        ax.set_xlabel('pH Difference (alkaline − acidic parent)')
        ax.set_ylabel('Similarity to Acidic Parent')
        ax.set_ylim(0, 1)
        ax.set_title(f'{panel} ({med_label})', fontweight='bold', loc='left', fontsize=12)

        # Add winner labels
        ax.text(0.95, 0.85, 'Acidic\nwins', transform=ax.transAxes, ha='right',
               fontsize=9, color='#d62728', fontweight='bold')
        ax.text(0.95, 0.15, 'Alkaline\nwins', transform=ax.transAxes, ha='right',
               fontsize=9, color='#1f77b4', fontweight='bold')

        # Add n
        n = len(ph_diffs)
        ax.text(0.05, 0.05, f'n = {n}', transform=ax.transAxes, fontsize=9)

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_S24_pH_diff_vs_outcome_Base_Nutr+.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_S24_pH_diff_vs_outcome_Base_Nutr+.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_S24_pH_diff_vs_outcome_Base_Nutr+.pdf', bbox_inches='tight')
    plt.close()

    print(f"✓ Saved: {output_dir}/Fig_S24_pH_diff_vs_outcome_Base_Nutr+.[svg/png/pdf]")


def main():
    """Main function"""
    print("="*70)
    print("REVISED pH FIGURES FOR SUPPLEMENTARY")
    print("="*70)

    # Load data
    parent_communities = load_parent_community_data()

    # Generate Fig S23: ASV abundance vs community pH
    plot_asv_vs_community_ph(parent_communities)

    # Analyze competition
    results = analyze_acidic_vs_alkaline_competition()

    # Generate Fig S24 replacement: Two-panel pH diff vs outcome
    plot_ph_diff_vs_outcome_two_panel(results)

    print("\n" + "="*70)
    print("COMPLETED")
    print("="*70)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  - Fig_S23_ASV_vs_pH_combined.[svg/png/pdf]")
    print("  - Fig_S24_pH_diff_vs_outcome_Base_Nutr+.[svg/png/pdf]")


if __name__ == "__main__":
    main()
