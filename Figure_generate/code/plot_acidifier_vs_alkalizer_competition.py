#!/usr/bin/env python3
"""
plot_acidifier_vs_alkalizer_competition.py

When acidifier-dominated community competes against alkalizer-dominated community,
who wins? Show win rate of acidifiers vs alkalizers across nutrient conditions.

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

# Define acidifiers and alkalizers based on monoculture pH after 15h
# Acidifiers: species that lower pH (monoculture pH < 6.5)
# Alkalizers: species that raise pH (monoculture pH > 6.5)

# Load monoculture pH data
def load_monoculture_ph():
    """Load monoculture pH data to classify species as acidifiers/alkalizers"""
    try:
        ph_file = "../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/230623_pH.xlsx"
        df = pd.read_excel(ph_file, sheet_name='after 15h', header=None)

        # Find data start
        data_start = None
        for i in range(len(df)):
            if df.iloc[i, 0] == 'A':
                data_start = i
                break

        if data_start is None:
            return None

        # Map well positions to ASV indices (A1=ASV1, A2=ASV2, etc.)
        # Assuming plate layout corresponds to ASV order
        species_ph = {}
        asv_idx = 0
        for row_idx, row_label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            if data_start + row_idx >= len(df):
                break
            row_data = df.iloc[data_start + row_idx, 1:13]
            for col_idx, ph_val in enumerate(row_data):
                if pd.notna(ph_val) and isinstance(ph_val, (int, float)):
                    # Convert raw value to pH (assuming raw is pH * 10)
                    actual_ph = float(ph_val) / 10.0 if ph_val > 14 else float(ph_val)
                    species_ph[asv_idx] = actual_ph
                asv_idx += 1

        return species_ph
    except Exception as e:
        print(f"Error loading monoculture pH: {e}")
        return None


def classify_community_by_dominant_species_ph(abundance, species_ph, threshold=0.1):
    """
    Classify a community as acidifier-dominated or alkalizer-dominated
    based on the pH modification ability of its dominant species.

    Returns: 'acidifier', 'alkalizer', or 'neutral'
    """
    abundance = np.array(abundance)

    # Find dominant species (highest abundance)
    dominant_idx = np.argmax(abundance)
    dominant_abundance = abundance[dominant_idx]

    # Only classify if dominant species has substantial abundance
    if dominant_abundance < threshold:
        return 'neutral', dominant_idx, None

    # Get pH of dominant species
    if dominant_idx in species_ph:
        dom_ph = species_ph[dominant_idx]
        if dom_ph < 6.0:  # Strong acidifier
            return 'acidifier', dominant_idx, dom_ph
        elif dom_ph > 7.0:  # Strong alkalizer
            return 'alkalizer', dominant_idx, dom_ph
        else:
            return 'neutral', dominant_idx, dom_ph

    return 'unknown', dominant_idx, None


def analyze_acidifier_vs_alkalizer_competition():
    """
    For each coalescence event where one parent is acidifier-dominated
    and the other is alkalizer-dominated, determine who wins.
    """
    print("="*60)
    print("ACIDIFIER vs ALKALIZER COMPETITION ANALYSIS")
    print("="*60)

    # Load monoculture pH data
    species_ph = load_monoculture_ph()
    if species_ph is None:
        print("Could not load monoculture pH data, using correlation-based classification")
        # Fallback: use correlation with community pH as proxy
        # Acidifiers: ASV3, ASV12, ASV13 (negative correlation)
        # Alkalizers: ASV1, ASV2, ASV10 (positive correlation)
        species_ph = {
            0: 7.5,   # ASV1 - alkalizer
            1: 7.5,   # ASV2 - alkalizer
            2: 5.0,   # ASV3 - acidifier
            9: 7.5,   # ASV10 - alkalizer
            11: 5.0,  # ASV12 - acidifier
            12: 5.0,  # ASV13 - acidifier
        }

    print(f"\nLoaded pH data for {len(species_ph)} species")

    # Classify species
    acidifiers = [idx for idx, ph in species_ph.items() if ph < 6.0]
    alkalizers = [idx for idx, ph in species_ph.items() if ph > 7.0]
    print(f"Acidifiers (pH < 6.0): ASV {[i+1 for i in acidifiers]}")
    print(f"Alkalizers (pH > 7.0): ASV {[i+1 for i in alkalizers]}")

    colors = get_medium_colors()
    results = {}

    for medium in ['L', 'M', 'H']:
        results[medium] = {
            'acidifier_wins': 0,
            'alkalizer_wins': 0,
            'tie': 0,
            'total': 0,
            'events': []
        }

        # Get all coalescence events
        coal_idx_list = []
        for pool in [6, 12, 24]:
            coal_idx_list.extend(Community_PermutateList("F", "S", medium, "C", pool))

        for coal_idx in coal_idx_list:
            # Get coalescence event
            coal_event = Coalescence_data[Coalescence_data['SampleIDX'] == coal_idx]
            if len(coal_event) == 0:
                continue

            # Get parent community indices
            parent1_idx = coal_event['SampleIDX_Sub1'].values[0]
            parent2_idx = coal_event['SampleIDX_Sub2'].values[0]

            # Get parent abundances
            parent1_abundance = getAbundance(Processed_sequences_synthetic, parent1_idx)
            parent2_abundance = getAbundance(Processed_sequences_synthetic, parent2_idx)

            if parent1_abundance is None or parent2_abundance is None:
                continue

            # Classify parents
            type1, dom1_idx, dom1_ph = classify_community_by_dominant_species_ph(parent1_abundance, species_ph)
            type2, dom2_idx, dom2_ph = classify_community_by_dominant_species_ph(parent2_abundance, species_ph)

            # Only consider events where one is acidifier and one is alkalizer
            if not ((type1 == 'acidifier' and type2 == 'alkalizer') or
                    (type1 == 'alkalizer' and type2 == 'acidifier')):
                continue

            # Get PDI (similarity to parent 1)
            pdi = coal_event['SimilarityTo1_BC_5'].values[0]

            # Determine winner
            if type1 == 'acidifier':
                # Parent 1 is acidifier
                if pdi > 0.6:
                    results[medium]['acidifier_wins'] += 1
                    winner = 'acidifier'
                elif pdi < 0.4:
                    results[medium]['alkalizer_wins'] += 1
                    winner = 'alkalizer'
                else:
                    results[medium]['tie'] += 1
                    winner = 'tie'
            else:
                # Parent 2 is acidifier
                if pdi < 0.4:
                    results[medium]['acidifier_wins'] += 1
                    winner = 'acidifier'
                elif pdi > 0.6:
                    results[medium]['alkalizer_wins'] += 1
                    winner = 'alkalizer'
                else:
                    results[medium]['tie'] += 1
                    winner = 'tie'

            results[medium]['total'] += 1
            results[medium]['events'].append({
                'coal_idx': coal_idx,
                'parent1_type': type1,
                'parent2_type': type2,
                'pdi': pdi,
                'winner': winner
            })

    return results, species_ph


def plot_win_rate_bar(results):
    """Plot bar chart of acidifier vs alkalizer win rates"""

    colors = get_medium_colors()

    fig, ax = plt.subplots(figsize=(100*mm, 80*mm), dpi=150)

    media = ['L', 'M', 'H']
    media_labels = ['Nutr$-$', 'Base', 'Nutr$+$']

    acidifier_rates = []
    alkalizer_rates = []
    tie_rates = []
    totals = []

    for medium in media:
        total = results[medium]['total']
        if total > 0:
            acidifier_rates.append(results[medium]['acidifier_wins'] / total * 100)
            alkalizer_rates.append(results[medium]['alkalizer_wins'] / total * 100)
            tie_rates.append(results[medium]['tie'] / total * 100)
        else:
            acidifier_rates.append(0)
            alkalizer_rates.append(0)
            tie_rates.append(0)
        totals.append(total)

    x = np.arange(len(media))
    width = 0.25

    bars1 = ax.bar(x - width, acidifier_rates, width, label='Acidifier wins',
                   color='#d62728', alpha=0.8, edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x, tie_rates, width, label='Tie/Mixed',
                   color='gray', alpha=0.6, edgecolor='black', linewidth=0.5)
    bars3 = ax.bar(x + width, alkalizer_rates, width, label='Alkalizer wins',
                   color='#1f77b4', alpha=0.8, edgecolor='black', linewidth=0.5)

    # Add 50% reference line
    ax.axhline(50, color='black', linestyle='--', linewidth=1, alpha=0.5)

    # Add count labels on bars
    for i, (bar, total) in enumerate(zip(bars1, totals)):
        if total > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                   f'n={total}', ha='center', va='bottom', fontsize=7)

    ax.set_ylabel('Win Rate (%)')
    ax.set_xlabel('Nutrient Condition')
    ax.set_xticks(x)
    ax.set_xticklabels(media_labels)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper left', fontsize=8)
    ax.set_title('Acidifier vs Alkalizer Competition Outcomes', fontweight='bold')

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_acidifier_vs_alkalizer_winrate.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_acidifier_vs_alkalizer_winrate.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_acidifier_vs_alkalizer_winrate.pdf', bbox_inches='tight')
    plt.close()

    print(f"\n✓ Saved: {output_dir}/Fig_acidifier_vs_alkalizer_winrate.[svg/png/pdf]")


def plot_win_rate_stacked(results):
    """Plot stacked bar chart of win rates"""

    colors = get_medium_colors()

    fig, ax = plt.subplots(figsize=(90*mm, 70*mm), dpi=150)

    media = ['L', 'M', 'H']
    media_labels = ['Nutr$-$', 'Base', 'Nutr$+$']

    acidifier_rates = []
    alkalizer_rates = []
    tie_rates = []
    totals = []

    for medium in media:
        total = results[medium]['total']
        if total > 0:
            acidifier_rates.append(results[medium]['acidifier_wins'] / total * 100)
            alkalizer_rates.append(results[medium]['alkalizer_wins'] / total * 100)
            tie_rates.append(results[medium]['tie'] / total * 100)
        else:
            acidifier_rates.append(0)
            alkalizer_rates.append(0)
            tie_rates.append(0)
        totals.append(total)

    x = np.arange(len(media))
    width = 0.6

    # Stacked bars
    bars1 = ax.bar(x, acidifier_rates, width, label='Acidifier wins',
                   color='#d62728', alpha=0.8, edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x, tie_rates, width, bottom=acidifier_rates, label='Tie/Mixed',
                   color='gray', alpha=0.6, edgecolor='black', linewidth=0.5)
    bars3 = ax.bar(x, alkalizer_rates, width,
                   bottom=[a+t for a, t in zip(acidifier_rates, tie_rates)],
                   label='Alkalizer wins', color='#1f77b4', alpha=0.8,
                   edgecolor='black', linewidth=0.5)

    # Add 50% reference line
    ax.axhline(50, color='black', linestyle='--', linewidth=1, alpha=0.7)

    # Add percentage labels inside bars
    for i, (acid, tie, alk, total) in enumerate(zip(acidifier_rates, tie_rates, alkalizer_rates, totals)):
        if total > 0:
            # Acidifier label
            if acid > 10:
                ax.text(i, acid/2, f'{acid:.0f}%', ha='center', va='center',
                       fontsize=9, color='white', fontweight='bold')
            # Tie label
            if tie > 10:
                ax.text(i, acid + tie/2, f'{tie:.0f}%', ha='center', va='center',
                       fontsize=8, color='black')
            # Alkalizer label
            if alk > 10:
                ax.text(i, acid + tie + alk/2, f'{alk:.0f}%', ha='center', va='center',
                       fontsize=9, color='white', fontweight='bold')
            # Total count
            ax.text(i, 102, f'n={total}', ha='center', va='bottom', fontsize=8)

    ax.set_ylabel('Fraction of Outcomes (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(media_labels)
    ax.set_ylim(0, 115)
    ax.legend(loc='upper right', fontsize=7, bbox_to_anchor=(1.0, 0.95))
    ax.set_title('Acidifier vs Alkalizer:\nWho Wins in Coalescence?', fontweight='bold')

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_acidifier_vs_alkalizer_winrate_stacked.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_acidifier_vs_alkalizer_winrate_stacked.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_acidifier_vs_alkalizer_winrate_stacked.pdf', bbox_inches='tight')
    plt.close()

    print(f"✓ Saved: {output_dir}/Fig_acidifier_vs_alkalizer_winrate_stacked.[svg/png/pdf]")


def print_detailed_results(results):
    """Print detailed statistics"""

    print("\n" + "="*60)
    print("DETAILED RESULTS")
    print("="*60)

    media_labels = {'L': 'Nutr-', 'M': 'Base', 'H': 'Nutr+'}

    for medium in ['L', 'M', 'H']:
        r = results[medium]
        total = r['total']

        print(f"\n{media_labels[medium]}:")
        print(f"  Total acidifier vs alkalizer matchups: {total}")

        if total > 0:
            acid_rate = r['acidifier_wins'] / total * 100
            alk_rate = r['alkalizer_wins'] / total * 100
            tie_rate = r['tie'] / total * 100

            print(f"  Acidifier wins: {r['acidifier_wins']} ({acid_rate:.1f}%)")
            print(f"  Alkalizer wins: {r['alkalizer_wins']} ({alk_rate:.1f}%)")
            print(f"  Tie/Mixed: {r['tie']} ({tie_rate:.1f}%)")

            # Binomial test: is acidifier win rate significantly > 50%?
            if r['acidifier_wins'] + r['alkalizer_wins'] > 0:
                from scipy.stats import binomtest
                n_decisive = r['acidifier_wins'] + r['alkalizer_wins']
                result = binomtest(r['acidifier_wins'], n_decisive, p=0.5, alternative='greater')
                print(f"  Binomial test (acidifier > 50%): p = {result.pvalue:.4f}")


def main():
    """Main function"""

    # Analyze competition outcomes
    results, species_ph = analyze_acidifier_vs_alkalizer_competition()

    # Print detailed results
    print_detailed_results(results)

    # Generate plots
    print("\n" + "="*60)
    print("GENERATING FIGURES")
    print("="*60)

    plot_win_rate_bar(results)
    plot_win_rate_stacked(results)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  - Fig_acidifier_vs_alkalizer_winrate.[svg/png/pdf]")
    print("  - Fig_acidifier_vs_alkalizer_winrate_stacked.[svg/png/pdf]")


if __name__ == "__main__":
    main()
