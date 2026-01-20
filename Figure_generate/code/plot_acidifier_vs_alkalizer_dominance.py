#!/usr/bin/env python3
"""
plot_acidifier_vs_alkalizer_dominance.py

Generate figures showing that acidifiers beat alkalizers in Nutr+ medium.
This supports the mechanistic claim linking pH modification to coalescence outcomes.

Three figure options:
A) Bar plot: Final abundance of acidifiers vs alkalizers after coalescence
B) Scatter: Dominant species' pH modification ability vs coalescence outcome (PDI)
C) Histogram: Community pH after coalescence showing acidic bias in Nutr+

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

# Define acidifiers and alkalizers based on Parent_Communities_Medium_H.csv
# Acidifiers: species whose abundance negatively correlates with community pH
ACIDIFIERS = {
    'NormalizedAbundance3': {'name': 'ASV3', 'r': -0.49},
    'NormalizedAbundance12': {'name': 'ASV12', 'r': -0.53},
    'NormalizedAbundance13': {'name': 'ASV13', 'r': -0.51},
}

# Alkalizers: species whose abundance positively correlates with community pH
ALKALIZERS = {
    'NormalizedAbundance1': {'name': 'ASV1', 'r': 0.29},
    'NormalizedAbundance2': {'name': 'ASV2', 'r': 0.29},
    'NormalizedAbundance10': {'name': 'ASV10', 'r': 0.31},
}

def get_parent_and_coalesced_data(medium='H'):
    """Get parent community and coalesced community data for a given medium"""

    # Get all coalesced community indices
    coal_idx_list = []
    for pool in [6, 12, 24]:
        coal_idx_list.extend(Community_PermutateList("F", "S", medium, "C", pool))

    # Get all parent community indices
    parent_idx_list = []
    for pool in [6, 12, 24]:
        parent_idx_list.extend(Community_PermutateList("F", "S", medium, "S", pool))

    # Get abundance data for coalesced communities
    coal_abundances = getAbundance_fromList(Processed_sequences_synthetic, coal_idx_list)

    # Get abundance data for parent communities
    parent_abundances = getAbundance_fromList(Processed_sequences_synthetic, parent_idx_list)

    # Get pH data for coalesced communities
    coal_communities = getCommunities(Communities_data, coal_idx_list)

    # Get pH data for parent communities
    parent_communities = getCommunities(Communities_data, parent_idx_list)

    return {
        'coal_idx': coal_idx_list,
        'parent_idx': parent_idx_list,
        'coal_abundances': coal_abundances,
        'parent_abundances': parent_abundances,
        'coal_communities': coal_communities,
        'parent_communities': parent_communities
    }


def figure_option_A_bar_plot():
    """
    Option A: Bar plot showing final abundance of acidifiers vs alkalizers after coalescence
    Compare before (parent) vs after (coalesced) abundances
    """
    print("\n" + "="*60)
    print("OPTION A: Bar plot - Acidifier vs Alkalizer abundance")
    print("="*60)

    colors = get_medium_colors()

    fig, axes = plt.subplots(1, 3, figsize=(180*mm, 60*mm), dpi=150)

    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        ax = axes[medium_idx]
        data = get_parent_and_coalesced_data(medium)

        # Calculate mean abundances
        acidifier_cols = [int(col.replace('NormalizedAbundance', '')) - 1 for col in ACIDIFIERS.keys()]
        alkalizer_cols = [int(col.replace('NormalizedAbundance', '')) - 1 for col in ALKALIZERS.keys()]

        # Parent abundances
        parent_acidifier = np.nanmean(data['parent_abundances'][:, acidifier_cols])
        parent_alkalizer = np.nanmean(data['parent_abundances'][:, alkalizer_cols])

        # Coalesced abundances
        coal_acidifier = np.nanmean(data['coal_abundances'][:, acidifier_cols])
        coal_alkalizer = np.nanmean(data['coal_abundances'][:, alkalizer_cols])

        # Calculate SEM
        parent_acidifier_sem = stats.sem(np.nanmean(data['parent_abundances'][:, acidifier_cols], axis=1))
        parent_alkalizer_sem = stats.sem(np.nanmean(data['parent_abundances'][:, alkalizer_cols], axis=1))
        coal_acidifier_sem = stats.sem(np.nanmean(data['coal_abundances'][:, acidifier_cols], axis=1))
        coal_alkalizer_sem = stats.sem(np.nanmean(data['coal_abundances'][:, alkalizer_cols], axis=1))

        # Bar positions
        x = np.array([0, 1, 2.5, 3.5])
        heights = [parent_acidifier, parent_alkalizer, coal_acidifier, coal_alkalizer]
        errors = [parent_acidifier_sem, parent_alkalizer_sem, coal_acidifier_sem, coal_alkalizer_sem]
        bar_colors = ['#d62728', '#1f77b4', '#d62728', '#1f77b4']  # red for acidifiers, blue for alkalizers
        hatches = ['', '', '///', '///']  # hatched for coalesced

        bars = ax.bar(x, heights, yerr=errors, capsize=3, color=bar_colors,
                     edgecolor='black', linewidth=0.8, alpha=0.7)

        # Add hatching to coalesced bars
        for i, bar in enumerate(bars):
            if i >= 2:
                bar.set_hatch('///')

        ax.set_xticks([0.5, 3])
        ax.set_xticklabels(['Parent', 'Coalesced'])
        ax.set_ylabel('Mean Abundance')

        medium_labels = {'L': 'Nutr$-$', 'M': 'Base', 'H': 'Nutr$+$'}
        ax.set_title(medium_labels[medium], fontweight='bold', color=colors[medium_idx])

        # Add legend only on first panel
        if medium_idx == 0:
            from matplotlib.patches import Patch
            legend_elements = [Patch(facecolor='#d62728', alpha=0.7, label='Acidifiers'),
                             Patch(facecolor='#1f77b4', alpha=0.7, label='Alkalizers')]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=7)

        # Print stats
        print(f"\n{medium_labels[medium]}:")
        print(f"  Parent  - Acidifiers: {parent_acidifier:.3f} ± {parent_acidifier_sem:.3f}")
        print(f"  Parent  - Alkalizers: {parent_alkalizer:.3f} ± {parent_alkalizer_sem:.3f}")
        print(f"  Coalesced - Acidifiers: {coal_acidifier:.3f} ± {coal_acidifier_sem:.3f}")
        print(f"  Coalesced - Alkalizers: {coal_alkalizer:.3f} ± {coal_alkalizer_sem:.3f}")

        # Calculate change
        acidifier_change = (coal_acidifier - parent_acidifier) / parent_acidifier * 100
        alkalizer_change = (coal_alkalizer - parent_alkalizer) / parent_alkalizer * 100
        print(f"  Acidifier change: {acidifier_change:+.1f}%")
        print(f"  Alkalizer change: {alkalizer_change:+.1f}%")

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_OptionA_acidifier_alkalizer_bar.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_OptionA_acidifier_alkalizer_bar.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_OptionA_acidifier_alkalizer_bar.pdf', bbox_inches='tight')
    plt.close()

    print(f"\n✓ Saved: {output_dir}/Fig_OptionA_acidifier_alkalizer_bar.[svg/png/pdf]")


def figure_option_B_scatter():
    """
    Option B: Scatter plot - Dominant species' pH modification ability vs coalescence outcome (PDI)
    For each coalescence event, identify the dominant species and plot its pH effect vs PDI
    """
    print("\n" + "="*60)
    print("OPTION B: Scatter - Dominant species pH effect vs PDI")
    print("="*60)

    colors = get_medium_colors()

    # Load monoculture pH data to get species' pH modification ability
    # Using the correlation coefficients as proxy for pH modification
    species_ph_effect = {}
    for col, info in ACIDIFIERS.items():
        species_idx = int(col.replace('NormalizedAbundance', '')) - 1
        species_ph_effect[species_idx] = info['r']  # negative = acidifier
    for col, info in ALKALIZERS.items():
        species_idx = int(col.replace('NormalizedAbundance', '')) - 1
        species_ph_effect[species_idx] = info['r']  # positive = alkalizer

    fig, axes = plt.subplots(1, 3, figsize=(180*mm, 60*mm), dpi=150)

    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        ax = axes[medium_idx]

        # Get coalescence data
        coal_idx_list = []
        for pool in [6, 12, 24]:
            coal_idx_list.extend(Community_PermutateList("F", "S", medium, "C", pool))

        ph_effects = []
        pdis = []

        for coal_idx in coal_idx_list:
            # Get coalescence event data
            coal_event = Coalescence_data[Coalescence_data['SampleIDX'] == coal_idx]
            if len(coal_event) == 0:
                continue

            # Get PDI (Parental Dominance Index)
            pdi = coal_event['SimilarityTo1_BC_5'].values[0]

            # Get coalesced community abundance
            coal_abundance = getAbundance(Processed_sequences_synthetic, coal_idx)
            if coal_abundance is None:
                continue

            coal_abundance = np.array(coal_abundance)

            # Find dominant species
            dominant_idx = np.argmax(coal_abundance)

            # Get pH effect of dominant species (if known)
            if dominant_idx in species_ph_effect:
                ph_effect = species_ph_effect[dominant_idx]
                ph_effects.append(ph_effect)
                pdis.append(pdi)

        if len(ph_effects) > 5:
            # Plot scatter
            ax.scatter(ph_effects, pdis, alpha=0.5, s=20, color=colors[medium_idx])

            # Add regression line only if there's variance in x
            if len(set(ph_effects)) > 1:
                slope, intercept, r, p, se = stats.linregress(ph_effects, pdis)
                x_line = np.array([min(ph_effects), max(ph_effects)])
                y_line = slope * x_line + intercept
                ax.plot(x_line, y_line, color='black', linewidth=1.5, linestyle='--')

                # Add R² annotation
                ax.annotate(f'R² = {r**2:.2f}\np = {p:.3f}',
                           xy=(0.05, 0.95), xycoords='axes fraction',
                           verticalalignment='top', fontsize=8)

                print(f"\n{['Nutr-', 'Base', 'Nutr+'][medium_idx]}:")
                print(f"  n = {len(ph_effects)}")
                print(f"  R² = {r**2:.3f}, p = {p:.4f}")
                print(f"  slope = {slope:.3f}")
            else:
                print(f"\n{['Nutr-', 'Base', 'Nutr+'][medium_idx]}:")
                print(f"  n = {len(ph_effects)} (insufficient variance for regression)")

        ax.set_xlabel("Dominant Species' pH Effect\n(negative = acidifier)")
        ax.set_ylabel('PDI (similarity to parent 1)')
        ax.axhline(0.5, color='gray', linestyle=':', alpha=0.5)
        ax.axvline(0, color='gray', linestyle=':', alpha=0.5)

        medium_labels = {'L': 'Nutr$-$', 'M': 'Base', 'H': 'Nutr$+$'}
        ax.set_title(medium_labels[medium], fontweight='bold', color=colors[medium_idx])

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_OptionB_dominant_pH_vs_PDI.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_OptionB_dominant_pH_vs_PDI.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_OptionB_dominant_pH_vs_PDI.pdf', bbox_inches='tight')
    plt.close()

    print(f"\n✓ Saved: {output_dir}/Fig_OptionB_dominant_pH_vs_PDI.[svg/png/pdf]")


def figure_option_C_histogram():
    """
    Option C: Histogram of community pH after coalescence showing acidic bias in Nutr+
    Compare pH distributions across media
    """
    print("\n" + "="*60)
    print("OPTION C: Histogram - Community pH after coalescence")
    print("="*60)

    colors = get_medium_colors()

    fig, axes = plt.subplots(1, 3, figsize=(180*mm, 60*mm), dpi=150)

    all_ph_data = {}

    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        ax = axes[medium_idx]

        # Get parent community pH
        parent_idx_list = []
        for pool in [6, 12, 24]:
            parent_idx_list.extend(Community_PermutateList("F", "S", medium, "S", pool))

        parent_communities = getCommunities(Communities_data, parent_idx_list)
        parent_ph = parent_communities['fieldPH7'].dropna().values

        # Get coalesced community pH
        coal_idx_list = []
        for pool in [6, 12, 24]:
            coal_idx_list.extend(Community_PermutateList("F", "S", medium, "C", pool))

        coal_communities = getCommunities(Communities_data, coal_idx_list)
        coal_ph = coal_communities['fieldPH7'].dropna().values

        all_ph_data[medium] = {'parent': parent_ph, 'coalesced': coal_ph}

        # Create overlapping histograms
        bins = np.linspace(3.5, 9.5, 25)

        ax.hist(parent_ph, bins=bins, alpha=0.5, label='Parent',
               color='gray', edgecolor='black', linewidth=0.5, density=True)
        ax.hist(coal_ph, bins=bins, alpha=0.7, label='Coalesced',
               color=colors[medium_idx], edgecolor='black', linewidth=0.5, density=True)

        # Add mean lines
        ax.axvline(np.mean(parent_ph), color='gray', linestyle='--', linewidth=2, label=f'Parent mean: {np.mean(parent_ph):.1f}')
        ax.axvline(np.mean(coal_ph), color=colors[medium_idx], linestyle='-', linewidth=2, label=f'Coalesced mean: {np.mean(coal_ph):.1f}')

        # Add neutral pH line
        ax.axvline(7.0, color='green', linestyle=':', alpha=0.5)

        ax.set_xlabel('Community pH')
        ax.set_ylabel('Density')
        ax.set_xlim(3.5, 9.5)

        medium_labels = {'L': 'Nutr$-$', 'M': 'Base', 'H': 'Nutr$+$'}
        ax.set_title(medium_labels[medium], fontweight='bold', color=colors[medium_idx])

        if medium_idx == 2:  # Only legend on last panel
            ax.legend(fontsize=6, loc='upper right')

        # Statistical test
        t_stat, p_val = stats.ttest_ind(parent_ph, coal_ph)

        print(f"\n{medium_labels[medium]}:")
        print(f"  Parent pH: {np.mean(parent_ph):.2f} ± {np.std(parent_ph):.2f} (n={len(parent_ph)})")
        print(f"  Coalesced pH: {np.mean(coal_ph):.2f} ± {np.std(coal_ph):.2f} (n={len(coal_ph)})")
        print(f"  pH shift: {np.mean(coal_ph) - np.mean(parent_ph):+.2f}")
        print(f"  t-test: t={t_stat:.2f}, p={p_val:.4f}")

        # Count acidic vs alkaline
        acidic_parent = np.sum(parent_ph < 7) / len(parent_ph) * 100
        acidic_coal = np.sum(coal_ph < 7) / len(coal_ph) * 100
        print(f"  % acidic (pH<7): Parent={acidic_parent:.1f}%, Coalesced={acidic_coal:.1f}%")

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_OptionC_pH_histogram.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_OptionC_pH_histogram.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_OptionC_pH_histogram.pdf', bbox_inches='tight')
    plt.close()

    print(f"\n✓ Saved: {output_dir}/Fig_OptionC_pH_histogram.[svg/png/pdf]")

    return all_ph_data


def figure_option_C_alt_ratio():
    """
    Alternative Option C: Show ratio of acidifiers to alkalizers changes after coalescence
    """
    print("\n" + "="*60)
    print("OPTION C-alt: Acidifier/Alkalizer ratio before vs after coalescence")
    print("="*60)

    colors = get_medium_colors()

    fig, ax = plt.subplots(1, 1, figsize=(80*mm, 70*mm), dpi=150)

    acidifier_cols = [int(col.replace('NormalizedAbundance', '')) - 1 for col in ACIDIFIERS.keys()]
    alkalizer_cols = [int(col.replace('NormalizedAbundance', '')) - 1 for col in ALKALIZERS.keys()]

    x_positions = []
    ratios_parent = []
    ratios_coal = []
    ratios_parent_sem = []
    ratios_coal_sem = []

    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        data = get_parent_and_coalesced_data(medium)

        # Calculate ratio for each community
        parent_acidifier_sum = np.nansum(data['parent_abundances'][:, acidifier_cols], axis=1)
        parent_alkalizer_sum = np.nansum(data['parent_abundances'][:, alkalizer_cols], axis=1)
        parent_ratio = parent_acidifier_sum / (parent_alkalizer_sum + 1e-6)

        coal_acidifier_sum = np.nansum(data['coal_abundances'][:, acidifier_cols], axis=1)
        coal_alkalizer_sum = np.nansum(data['coal_abundances'][:, alkalizer_cols], axis=1)
        coal_ratio = coal_acidifier_sum / (coal_alkalizer_sum + 1e-6)

        # Use log ratio for better visualization
        parent_log_ratio = np.log2(parent_ratio + 0.01)
        coal_log_ratio = np.log2(coal_ratio + 0.01)

        ratios_parent.append(np.nanmean(parent_log_ratio))
        ratios_coal.append(np.nanmean(coal_log_ratio))
        ratios_parent_sem.append(stats.sem(parent_log_ratio[~np.isnan(parent_log_ratio)]))
        ratios_coal_sem.append(stats.sem(coal_log_ratio[~np.isnan(coal_log_ratio)]))

        x_positions.append(medium_idx)

        medium_labels = {'L': 'Nutr$-$', 'M': 'Base', 'H': 'Nutr$+$'}
        print(f"\n{medium_labels[medium]}:")
        print(f"  Parent log2(A/Alk): {np.nanmean(parent_log_ratio):.2f} ± {stats.sem(parent_log_ratio[~np.isnan(parent_log_ratio)]):.2f}")
        print(f"  Coalesced log2(A/Alk): {np.nanmean(coal_log_ratio):.2f} ± {stats.sem(coal_log_ratio[~np.isnan(coal_log_ratio)]):.2f}")

        # T-test
        t_stat, p_val = stats.ttest_ind(parent_log_ratio[~np.isnan(parent_log_ratio)],
                                        coal_log_ratio[~np.isnan(coal_log_ratio)])
        print(f"  t-test: t={t_stat:.2f}, p={p_val:.4f}")

    # Plot
    x = np.array(x_positions)
    width = 0.35

    bars1 = ax.bar(x - width/2, ratios_parent, width, yerr=ratios_parent_sem,
                   label='Parent', color='gray', alpha=0.7, capsize=3)
    bars2 = ax.bar(x + width/2, ratios_coal, width, yerr=ratios_coal_sem,
                   label='Coalesced', color=[colors[i] for i in range(3)], alpha=0.7, capsize=3)

    ax.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax.set_ylabel('log$_2$(Acidifier/Alkalizer ratio)')
    ax.set_xticks(x)
    ax.set_xticklabels(['Nutr$-$', 'Base', 'Nutr$+$'])
    ax.legend()

    # Add annotation
    ax.annotate('Acidifier\ndominance', xy=(0.02, 0.98), xycoords='axes fraction',
               verticalalignment='top', fontsize=7, color='red')
    ax.annotate('Alkalizer\ndominance', xy=(0.02, 0.02), xycoords='axes fraction',
               verticalalignment='bottom', fontsize=7, color='blue')

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_OptionC_alt_ratio.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_OptionC_alt_ratio.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_OptionC_alt_ratio.pdf', bbox_inches='tight')
    plt.close()

    print(f"\n✓ Saved: {output_dir}/Fig_OptionC_alt_ratio.[svg/png/pdf]")


def figure_combined_publication():
    """
    Combined figure for publication:
    Panel A: Acidifier/Alkalizer abundance comparison (bar)
    Panel B: pH distribution after coalescence (histogram, Nutr+ only)
    """
    print("\n" + "="*60)
    print("COMBINED FIGURE for publication")
    print("="*60)

    colors = get_medium_colors()

    fig = plt.figure(figsize=(180*mm, 70*mm), dpi=150)

    # Panel A: Bar plot for all media
    ax1 = fig.add_subplot(121)

    acidifier_cols = [int(col.replace('NormalizedAbundance', '')) - 1 for col in ACIDIFIERS.keys()]
    alkalizer_cols = [int(col.replace('NormalizedAbundance', '')) - 1 for col in ALKALIZERS.keys()]

    bar_width = 0.35
    x_pos = np.array([0, 1.5, 3])  # Positions for L, M, H

    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        data = get_parent_and_coalesced_data(medium)

        # Coalesced abundances only
        coal_acidifier = np.nanmean(data['coal_abundances'][:, acidifier_cols])
        coal_alkalizer = np.nanmean(data['coal_abundances'][:, alkalizer_cols])
        coal_acidifier_sem = stats.sem(np.nanmean(data['coal_abundances'][:, acidifier_cols], axis=1))
        coal_alkalizer_sem = stats.sem(np.nanmean(data['coal_abundances'][:, alkalizer_cols], axis=1))

        ax1.bar(x_pos[medium_idx] - bar_width/2, coal_acidifier, bar_width,
               yerr=coal_acidifier_sem, color='#d62728', alpha=0.7, capsize=3,
               edgecolor='black', linewidth=0.5)
        ax1.bar(x_pos[medium_idx] + bar_width/2, coal_alkalizer, bar_width,
               yerr=coal_alkalizer_sem, color='#1f77b4', alpha=0.7, capsize=3,
               edgecolor='black', linewidth=0.5)

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(['Nutr$-$', 'Base', 'Nutr$+$'])
    ax1.set_ylabel('Mean Abundance After Coalescence')
    ax1.set_title('A', fontweight='bold', loc='left', fontsize=12)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#d62728', alpha=0.7, label='Acidifiers (ASV3,12,13)'),
                      Patch(facecolor='#1f77b4', alpha=0.7, label='Alkalizers (ASV1,2,10)')]
    ax1.legend(handles=legend_elements, loc='upper left', fontsize=7)

    # Panel B: pH histogram for Nutr+ only
    ax2 = fig.add_subplot(122)

    medium = 'H'
    parent_idx_list = []
    for pool in [6, 12, 24]:
        parent_idx_list.extend(Community_PermutateList("F", "S", medium, "S", pool))
    parent_communities = getCommunities(Communities_data, parent_idx_list)
    parent_ph = parent_communities['fieldPH7'].dropna().values

    coal_idx_list = []
    for pool in [6, 12, 24]:
        coal_idx_list.extend(Community_PermutateList("F", "S", medium, "C", pool))
    coal_communities = getCommunities(Communities_data, coal_idx_list)
    coal_ph = coal_communities['fieldPH7'].dropna().values

    bins = np.linspace(3.5, 9.5, 20)

    ax2.hist(parent_ph, bins=bins, alpha=0.5, label=f'Parent (mean={np.mean(parent_ph):.1f})',
            color='gray', edgecolor='black', linewidth=0.5, density=True)
    ax2.hist(coal_ph, bins=bins, alpha=0.7, label=f'Coalesced (mean={np.mean(coal_ph):.1f})',
            color=colors[2], edgecolor='black', linewidth=0.5, density=True)

    ax2.axvline(7.0, color='green', linestyle=':', alpha=0.7, label='Neutral pH')
    ax2.axvline(np.mean(parent_ph), color='gray', linestyle='--', linewidth=2)
    ax2.axvline(np.mean(coal_ph), color=colors[2], linestyle='-', linewidth=2)

    ax2.set_xlabel('Community pH')
    ax2.set_ylabel('Density')
    ax2.set_xlim(3.5, 9.5)
    ax2.set_title('B (Nutr$+$)', fontweight='bold', loc='left', fontsize=12)
    ax2.legend(fontsize=7, loc='upper right')

    # Add arrow showing shift toward acidic
    shift = np.mean(coal_ph) - np.mean(parent_ph)
    if shift < 0:
        ax2.annotate('', xy=(np.mean(coal_ph), 0.35), xytext=(np.mean(parent_ph), 0.35),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2),
                    xycoords=('data', 'axes fraction'))
        ax2.text((np.mean(coal_ph) + np.mean(parent_ph))/2, 0.38, f'Δ = {shift:.2f}',
                transform=ax2.get_xaxis_transform(), ha='center', fontsize=8, color='red')

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_acidifier_dominance_combined.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_acidifier_dominance_combined.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_acidifier_dominance_combined.pdf', bbox_inches='tight')
    plt.close()

    print(f"\n✓ Saved: {output_dir}/Fig_acidifier_dominance_combined.[svg/png/pdf]")


def main():
    """Generate all figure options"""
    print("="*60)
    print("ACIDIFIER vs ALKALIZER DOMINANCE ANALYSIS")
    print("="*60)
    print("\nGenerating all figure options...")
    print("Acidifiers: ASV3 (r=-0.49), ASV12 (r=-0.53), ASV13 (r=-0.51)")
    print("Alkalizers: ASV1 (r=0.29), ASV2 (r=0.29), ASV10 (r=0.31)")

    # Generate all options
    figure_option_A_bar_plot()
    figure_option_B_scatter()
    figure_option_C_histogram()
    figure_option_C_alt_ratio()
    figure_combined_publication()

    print("\n" + "="*60)
    print("ALL FIGURES GENERATED!")
    print("="*60)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  - Fig_OptionA_acidifier_alkalizer_bar.[svg/png/pdf]")
    print("  - Fig_OptionB_dominant_pH_vs_PDI.[svg/png/pdf]")
    print("  - Fig_OptionC_pH_histogram.[svg/png/pdf]")
    print("  - Fig_OptionC_alt_ratio.[svg/png/pdf]")
    print("  - Fig_acidifier_dominance_combined.[svg/png/pdf]")


if __name__ == "__main__":
    main()
