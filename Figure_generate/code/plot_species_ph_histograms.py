#!/usr/bin/env python3
"""
plot_species_ph_histograms.py

Create histograms showing:
1. Species → pH: How species change pH (monoculture pH after 15h growth)
2. pH → Species: Optimal pH for growth (species pH preference)

Author: Gore Lab
Date: January 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os

# Set up style
rcParams['font.family'] = 'Arial'
rcParams['font.size'] = 10
rcParams['axes.titlesize'] = 12
rcParams['axes.labelsize'] = 11
rcParams['xtick.labelsize'] = 10
rcParams['ytick.labelsize'] = 10
rcParams['axes.linewidth'] = 1.0
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

output_dir = "Figure/pH_Analysis"
os.makedirs(output_dir, exist_ok=True)

def load_monoculture_ph_data():
    """Load pH after 15h monoculture growth"""
    file_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/230623_pH.xlsx'

    df = pd.read_excel(file_path, sheet_name='after 15h', header=None)

    # Find data start
    data_start = None
    for i in range(len(df)):
        if df.iloc[i, 0] == 'A':
            data_start = i
            break

    # Extract pH values
    data = []
    for row_idx, row_label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        if data_start + row_idx >= len(df):
            break
        row_data = df.iloc[data_start + row_idx, 1:13]
        for col_idx, raw_value in enumerate(row_data):
            if pd.notna(raw_value) and isinstance(raw_value, (int, float)):
                ph_final = float(raw_value) / 10.0
                data.append({
                    'Well': f'{row_label}{col_idx+1}',
                    'pH_after_15h': ph_final,
                    'pH_change': ph_final - 6.5
                })

    return pd.DataFrame(data)

def load_optimal_ph_data():
    """Load optimal pH for growth data"""
    return pd.read_csv(f'{output_dir}/species_ph_preferences.csv')


# =============================================================================
# VERSION 1: Simple side-by-side histograms
# =============================================================================
def plot_version1_simple_histograms(mono_df, opt_df):
    """Simple side-by-side histograms"""

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Panel A: pH after monoculture growth (Species → pH)
    ax1 = axes[0]
    bins_mono = np.arange(2.5, 8.5, 0.5)
    ax1.hist(mono_df['pH_after_15h'], bins=bins_mono,
             color='#4C72B0', edgecolor='black', linewidth=0.8, alpha=0.8)
    ax1.axvline(6.5, color='red', linestyle='--', linewidth=1.5, label='Initial pH (6.5)')
    ax1.set_xlabel('pH after 15h growth')
    ax1.set_ylabel('Number of species')
    ax1.set_title('A. Species → pH\n(Monoculture pH change)', fontweight='bold')
    ax1.legend(loc='upper right', fontsize=8)

    # Add mean line
    mean_ph = mono_df['pH_after_15h'].mean()
    ax1.axvline(mean_ph, color='green', linestyle=':', linewidth=1.5, alpha=0.8)
    ax1.text(mean_ph + 0.1, ax1.get_ylim()[1] * 0.9, f'Mean: {mean_ph:.1f}',
             fontsize=8, color='green')

    # Panel B: Optimal pH for growth (pH → Species)
    ax2 = axes[1]
    bins_opt = np.arange(3.5, 10.5, 1.0)
    ax2.hist(opt_df['Optimal_pH'], bins=bins_opt,
             color='#55A868', edgecolor='black', linewidth=0.8, alpha=0.8)
    ax2.set_xlabel('Optimal pH for growth')
    ax2.set_ylabel('Number of species')
    ax2.set_title('B. pH → Species\n(Optimal growth pH)', fontweight='bold')

    # Add mean line
    mean_opt = opt_df['Optimal_pH'].mean()
    ax2.axvline(mean_opt, color='blue', linestyle=':', linewidth=1.5, alpha=0.8)
    ax2.text(mean_opt + 0.2, ax2.get_ylim()[1] * 0.9, f'Mean: {mean_opt:.1f}',
             fontsize=8, color='blue')

    plt.tight_layout()

    for ext in ['svg', 'png', 'pdf']:
        fig.savefig(f'{output_dir}/v1_simple_histograms.{ext}', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: v1_simple_histograms")


# =============================================================================
# VERSION 2: Histograms with acidifier/alkalizer coloring
# =============================================================================
def plot_version2_colored_histograms(mono_df, opt_df):
    """Histograms with acidifier (red) and alkalizer (blue) coloring"""

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Panel A: pH after monoculture growth with coloring
    ax1 = axes[0]
    initial_ph = 6.5

    # Separate acidifiers and alkalizers
    acidifiers = mono_df[mono_df['pH_after_15h'] < initial_ph]['pH_after_15h']
    alkalizers = mono_df[mono_df['pH_after_15h'] >= initial_ph]['pH_after_15h']

    bins_mono = np.arange(2.5, 8.5, 0.5)

    ax1.hist(acidifiers, bins=bins_mono, color='#d62728', edgecolor='black',
             linewidth=0.8, alpha=0.7, label=f'Acidifiers (n={len(acidifiers)})')
    ax1.hist(alkalizers, bins=bins_mono, color='#1f77b4', edgecolor='black',
             linewidth=0.8, alpha=0.7, label=f'Alkalizers (n={len(alkalizers)})')

    ax1.axvline(initial_ph, color='black', linestyle='-', linewidth=2, label='Initial pH')
    ax1.set_xlabel('pH after 15h growth')
    ax1.set_ylabel('Number of species')
    ax1.set_title('A. Species → pH\n(Monoculture pH modification)', fontweight='bold')
    ax1.legend(loc='upper right', fontsize=8)

    # Panel B: Optimal pH with coloring by acidophile/alkaliphile
    ax2 = axes[1]

    # Classify by optimal pH
    acidophiles = opt_df[opt_df['Optimal_pH'] < 6.5]['Optimal_pH']
    neutrals = opt_df[(opt_df['Optimal_pH'] >= 6.5) & (opt_df['Optimal_pH'] <= 7.5)]['Optimal_pH']
    alkaliphiles = opt_df[opt_df['Optimal_pH'] > 7.5]['Optimal_pH']

    bins_opt = np.arange(3.5, 10.5, 1.0)

    ax2.hist(acidophiles, bins=bins_opt, color='#d62728', edgecolor='black',
             linewidth=0.8, alpha=0.7, label=f'Acidophiles (n={len(acidophiles)})')
    ax2.hist(neutrals, bins=bins_opt, color='gray', edgecolor='black',
             linewidth=0.8, alpha=0.7, label=f'Neutrals (n={len(neutrals)})')
    ax2.hist(alkaliphiles, bins=bins_opt, color='#1f77b4', edgecolor='black',
             linewidth=0.8, alpha=0.7, label=f'Alkaliphiles (n={len(alkaliphiles)})')

    ax2.set_xlabel('Optimal pH for growth')
    ax2.set_ylabel('Number of species')
    ax2.set_title('B. pH → Species\n(pH preference for growth)', fontweight='bold')
    ax2.legend(loc='upper left', fontsize=8)

    plt.tight_layout()

    for ext in ['svg', 'png', 'pdf']:
        fig.savefig(f'{output_dir}/v2_colored_histograms.{ext}', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: v2_colored_histograms")


# =============================================================================
# VERSION 3: pH change histogram (delta pH)
# =============================================================================
def plot_version3_ph_change_histogram(mono_df):
    """Histogram of pH change (delta from initial)"""

    fig, ax = plt.subplots(figsize=(6, 4))

    bins = np.arange(-4, 2, 0.5)

    # Color by direction of change
    acidifying = mono_df[mono_df['pH_change'] < 0]['pH_change']
    alkalizing = mono_df[mono_df['pH_change'] >= 0]['pH_change']

    ax.hist(acidifying, bins=bins, color='#d62728', edgecolor='black',
            linewidth=0.8, alpha=0.7, label=f'Acidifying (n={len(acidifying)})')
    ax.hist(alkalizing, bins=bins, color='#1f77b4', edgecolor='black',
            linewidth=0.8, alpha=0.7, label=f'Alkalizing (n={len(alkalizing)})')

    ax.axvline(0, color='black', linestyle='-', linewidth=2)
    ax.set_xlabel('ΔpH (Final - Initial)')
    ax.set_ylabel('Number of species')
    ax.set_title('pH Change by Species in Monoculture\n(Initial pH = 6.5)', fontweight='bold')
    ax.legend(loc='upper left', fontsize=9)

    # Add annotations
    mean_change = mono_df['pH_change'].mean()
    ax.text(0.95, 0.95, f'Mean ΔpH: {mean_change:.2f}\nMedian ΔpH: {mono_df["pH_change"].median():.2f}',
            transform=ax.transAxes, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8), fontsize=9)

    plt.tight_layout()

    for ext in ['svg', 'png', 'pdf']:
        fig.savefig(f'{output_dir}/v3_ph_change_histogram.{ext}', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: v3_ph_change_histogram")


# =============================================================================
# VERSION 4: Stacked bar chart by pH category
# =============================================================================
def plot_version4_stacked_bars(mono_df, opt_df):
    """Stacked bar charts showing pH categories"""

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Panel A: Monoculture pH change categories
    ax1 = axes[0]

    # Define categories
    strong_acid = len(mono_df[mono_df['pH_after_15h'] < 4.5])
    moderate_acid = len(mono_df[(mono_df['pH_after_15h'] >= 4.5) & (mono_df['pH_after_15h'] < 6.0)])
    neutral = len(mono_df[(mono_df['pH_after_15h'] >= 6.0) & (mono_df['pH_after_15h'] <= 7.0)])
    alkaline = len(mono_df[mono_df['pH_after_15h'] > 7.0])

    categories = ['Strong\nAcidifier\n(<4.5)', 'Moderate\nAcidifier\n(4.5-6)',
                  'Neutral\n(6-7)', 'Alkalizer\n(>7)']
    counts = [strong_acid, moderate_acid, neutral, alkaline]
    colors = ['#d62728', '#ff7f0e', 'gray', '#1f77b4']

    bars = ax1.bar(categories, counts, color=colors, edgecolor='black', linewidth=0.8, alpha=0.8)
    ax1.set_ylabel('Number of species')
    ax1.set_title('A. Species → pH\n(Monoculture pH modification)', fontweight='bold')

    # Add count labels
    for bar, count in zip(bars, counts):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Panel B: Optimal pH categories
    ax2 = axes[1]

    acidophile = len(opt_df[opt_df['Optimal_pH'] <= 5])
    slight_acid = len(opt_df[(opt_df['Optimal_pH'] > 5) & (opt_df['Optimal_pH'] <= 6)])
    neutral_pref = len(opt_df[(opt_df['Optimal_pH'] > 6) & (opt_df['Optimal_pH'] <= 8)])
    alkaliphile = len(opt_df[opt_df['Optimal_pH'] > 8])

    categories2 = ['Acidophile\n(≤5)', 'Slight Acid\n(5-6)',
                   'Neutral\n(6-8)', 'Alkaliphile\n(>8)']
    counts2 = [acidophile, slight_acid, neutral_pref, alkaliphile]
    colors2 = ['#d62728', '#ff7f0e', 'gray', '#1f77b4']

    bars2 = ax2.bar(categories2, counts2, color=colors2, edgecolor='black', linewidth=0.8, alpha=0.8)
    ax2.set_ylabel('Number of species')
    ax2.set_title('B. pH → Species\n(Optimal growth pH)', fontweight='bold')

    # Add count labels
    for bar, count in zip(bars2, counts2):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()

    for ext in ['svg', 'png', 'pdf']:
        fig.savefig(f'{output_dir}/v4_stacked_bars.{ext}', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: v4_stacked_bars")


# =============================================================================
# VERSION 5: Combined figure with density plots
# =============================================================================
def plot_version5_density_comparison(mono_df, opt_df):
    """Density plots comparing both distributions"""

    from scipy.stats import gaussian_kde

    fig, ax = plt.subplots(figsize=(8, 5))

    # Monoculture pH (Species → pH)
    x1 = np.linspace(2, 9, 200)
    kde1 = gaussian_kde(mono_df['pH_after_15h'])
    y1 = kde1(x1)
    ax.fill_between(x1, y1, alpha=0.4, color='#4C72B0', label='pH after monoculture growth')
    ax.plot(x1, y1, color='#4C72B0', linewidth=2)

    # Optimal pH (pH → Species) - only use non-blank wells
    valid_opt = opt_df[opt_df['Optimal_OD'] > 0.05]['Optimal_pH']
    x2 = np.linspace(3, 10, 200)
    kde2 = gaussian_kde(valid_opt)
    y2 = kde2(x2)
    ax.fill_between(x2, y2, alpha=0.4, color='#55A868', label='Optimal pH for growth')
    ax.plot(x2, y2, color='#55A868', linewidth=2)

    ax.axvline(6.5, color='black', linestyle='--', linewidth=1.5, label='Initial/Neutral pH (6.5)')

    ax.set_xlabel('pH', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('Comparison: pH Modification vs pH Preference', fontweight='bold', fontsize=13)
    ax.legend(loc='upper right', fontsize=9)
    ax.set_xlim(2, 10)

    plt.tight_layout()

    for ext in ['svg', 'png', 'pdf']:
        fig.savefig(f'{output_dir}/v5_density_comparison.{ext}', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: v5_density_comparison")


# =============================================================================
# VERSION 6: Publication-ready single panel (monoculture only)
# =============================================================================
def plot_version6_publication_single(mono_df):
    """Publication-ready histogram for monoculture pH change"""

    fig, ax = plt.subplots(figsize=(4, 3))

    bins = np.arange(2.5, 8.5, 0.5)

    # Color bins by acidifier/alkalizer
    n, bin_edges, patches = ax.hist(mono_df['pH_after_15h'], bins=bins,
                                     edgecolor='black', linewidth=0.8)

    # Color patches
    for patch, left_edge in zip(patches, bin_edges[:-1]):
        if left_edge + 0.25 < 6.5:  # Acidifier (bin center < 6.5)
            patch.set_facecolor('#d62728')
            patch.set_alpha(0.7)
        else:  # Alkalizer
            patch.set_facecolor('#1f77b4')
            patch.set_alpha(0.7)

    ax.axvline(6.5, color='black', linestyle='-', linewidth=1.5)
    ax.text(6.5, ax.get_ylim()[1] * 1.02, 'Initial\npH', ha='center', va='bottom', fontsize=8)

    # Add labels
    ax.text(4.5, ax.get_ylim()[1] * 0.85, '← Acidifiers', ha='center', fontsize=9,
            color='#d62728', fontweight='bold')
    ax.text(7.2, ax.get_ylim()[1] * 0.85, 'Alkalizers →', ha='center', fontsize=9,
            color='#1f77b4', fontweight='bold')

    ax.set_xlabel('pH after 15h monoculture growth')
    ax.set_ylabel('Number of species')

    plt.tight_layout()

    for ext in ['svg', 'png', 'pdf']:
        fig.savefig(f'{output_dir}/v6_publication_monoculture.{ext}', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: v6_publication_monoculture")


def main():
    print("="*60)
    print("GENERATING pH HISTOGRAMS")
    print("="*60)
    print()

    # Load data
    print("Loading data...")
    mono_df = load_monoculture_ph_data()
    opt_df = load_optimal_ph_data()

    print(f"  Monoculture pH data: {len(mono_df)} species")
    print(f"  Optimal pH data: {len(opt_df)} species")
    print()

    # Generate all versions
    print("Generating plots...")
    plot_version1_simple_histograms(mono_df, opt_df)
    plot_version2_colored_histograms(mono_df, opt_df)
    plot_version3_ph_change_histogram(mono_df)
    plot_version4_stacked_bars(mono_df, opt_df)
    plot_version5_density_comparison(mono_df, opt_df)
    plot_version6_publication_single(mono_df)

    print()
    print("="*60)
    print(f"All plots saved to: {output_dir}/")
    print("="*60)

if __name__ == "__main__":
    main()
