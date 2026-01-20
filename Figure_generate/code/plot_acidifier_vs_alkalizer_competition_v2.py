#!/usr/bin/env python3
"""
plot_acidifier_vs_alkalizer_competition_v2.py

When an acidic community (pH < 7) competes against an alkaline community (pH > 7),
who wins? Show win rate based on parent community pH.

This version uses community-level pH (measured after growth) rather than
individual species classification.

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


def analyze_acidic_vs_alkaline_community_competition():
    """
    For each coalescence event where one parent community is acidic (pH < 7)
    and the other is alkaline (pH > 7), determine who wins.
    """
    print("="*60)
    print("ACIDIC vs ALKALINE COMMUNITY COMPETITION")
    print("="*60)

    colors = get_medium_colors()
    results = {}

    for medium in ['L', 'M', 'H']:
        results[medium] = {
            'acidic_wins': 0,
            'alkaline_wins': 0,
            'tie': 0,
            'total': 0,
            'events': [],
            'ph_diffs': [],  # pH difference (acidic - alkaline parent)
            'pdis': []       # PDI values
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

            # Get parent community pH
            parent1_comm = Communities_data[Communities_data['SampleIDX'] == parent1_idx]
            parent2_comm = Communities_data[Communities_data['SampleIDX'] == parent2_idx]

            if len(parent1_comm) == 0 or len(parent2_comm) == 0:
                continue

            ph1 = parent1_comm['fieldPH7'].values[0]
            ph2 = parent2_comm['fieldPH7'].values[0]

            if np.isnan(ph1) or np.isnan(ph2):
                continue

            # Only consider events where one is acidic and one is alkaline
            neutral_zone = 0.5  # pH 6.5 to 7.5 is neutral zone
            if not ((ph1 < 7 - neutral_zone and ph2 > 7 + neutral_zone) or
                    (ph1 > 7 + neutral_zone and ph2 < 7 - neutral_zone)):
                continue

            # Get PDI (similarity to parent 1)
            pdi = coal_event['SimilarityTo1_BC_5'].values[0]
            if np.isnan(pdi):
                continue

            # Determine winner
            if ph1 < ph2:
                # Parent 1 is more acidic
                acidic_parent = 1
                ph_diff = ph2 - ph1  # positive = parent 2 is more alkaline
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
                # Parent 2 is more acidic
                acidic_parent = 2
                ph_diff = ph1 - ph2  # positive = parent 1 is more alkaline
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


def plot_win_rate_stacked(results):
    """Plot stacked bar chart of win rates"""

    fig, ax = plt.subplots(figsize=(90*mm, 70*mm), dpi=150)

    media = ['L', 'M', 'H']
    media_labels = ['Nutr$-$', 'Base', 'Nutr$+$']
    colors_media = get_medium_colors()

    acidic_rates = []
    alkaline_rates = []
    tie_rates = []
    totals = []

    for medium in media:
        total = results[medium]['total']
        if total > 0:
            acidic_rates.append(results[medium]['acidic_wins'] / total * 100)
            alkaline_rates.append(results[medium]['alkaline_wins'] / total * 100)
            tie_rates.append(results[medium]['tie'] / total * 100)
        else:
            acidic_rates.append(0)
            alkaline_rates.append(0)
            tie_rates.append(0)
        totals.append(total)

    x = np.arange(len(media))
    width = 0.6

    # Stacked bars
    bars1 = ax.bar(x, acidic_rates, width, label='Acidic community wins',
                   color='#d62728', alpha=0.8, edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x, tie_rates, width, bottom=acidic_rates, label='Tie/Mixed',
                   color='gray', alpha=0.5, edgecolor='black', linewidth=0.5)
    bars3 = ax.bar(x, alkaline_rates, width,
                   bottom=[a+t for a, t in zip(acidic_rates, tie_rates)],
                   label='Alkaline community wins', color='#1f77b4', alpha=0.8,
                   edgecolor='black', linewidth=0.5)

    # Add 50% reference line
    ax.axhline(50, color='black', linestyle='--', linewidth=1, alpha=0.7)

    # Add percentage labels inside bars
    for i, (acid, tie, alk, total) in enumerate(zip(acidic_rates, tie_rates, alkaline_rates, totals)):
        if total > 0:
            # Acidic label
            if acid > 8:
                ax.text(i, acid/2, f'{acid:.0f}%', ha='center', va='center',
                       fontsize=10, color='white', fontweight='bold')
            # Tie label
            if tie > 8:
                ax.text(i, acid + tie/2, f'{tie:.0f}%', ha='center', va='center',
                       fontsize=9, color='black')
            # Alkaline label
            if alk > 8:
                ax.text(i, acid + tie + alk/2, f'{alk:.0f}%', ha='center', va='center',
                       fontsize=10, color='white', fontweight='bold')
            # Total count
            ax.text(i, 102, f'n={total}', ha='center', va='bottom', fontsize=8)

    ax.set_ylabel('Fraction of Outcomes (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(media_labels)
    ax.set_ylim(0, 115)
    ax.legend(loc='upper right', fontsize=7, bbox_to_anchor=(1.0, 0.95))
    ax.set_title('Acidic vs Alkaline Community:\nWho Wins in Coalescence?', fontweight='bold')

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_acidic_vs_alkaline_winrate_stacked.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_acidic_vs_alkaline_winrate_stacked.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_acidic_vs_alkaline_winrate_stacked.pdf', bbox_inches='tight')
    plt.close()

    print(f"✓ Saved: {output_dir}/Fig_acidic_vs_alkaline_winrate_stacked.[svg/png/pdf]")


def plot_ph_diff_vs_outcome(results):
    """Plot pH difference vs coalescence outcome (scatter)"""

    fig, axes = plt.subplots(1, 3, figsize=(180*mm, 60*mm), dpi=150)
    colors_media = get_medium_colors()
    media = ['L', 'M', 'H']
    media_labels = ['Nutr$-$', 'Base', 'Nutr$+$']

    for idx, medium in enumerate(media):
        ax = axes[idx]

        ph_diffs = results[medium]['ph_diffs']
        pdis = results[medium]['pdis']  # PDI relative to acidic parent

        if len(ph_diffs) > 3:
            ax.scatter(ph_diffs, pdis, alpha=0.6, s=30, color=colors_media[idx])

            # Add regression line
            if len(set(ph_diffs)) > 1:
                slope, intercept, r, p, se = stats.linregress(ph_diffs, pdis)
                x_line = np.array([min(ph_diffs), max(ph_diffs)])
                y_line = slope * x_line + intercept
                ax.plot(x_line, y_line, color='black', linewidth=1.5, linestyle='--')

                ax.annotate(f'R² = {r**2:.2f}\np = {p:.3f}',
                           xy=(0.05, 0.95), xycoords='axes fraction',
                           verticalalignment='top', fontsize=8)

        ax.axhline(0.5, color='gray', linestyle=':', alpha=0.5)
        ax.set_xlabel('pH Difference\n(alkaline − acidic parent)')
        ax.set_ylabel('Similarity to Acidic Parent')
        ax.set_ylim(0, 1)
        ax.set_title(media_labels[idx], fontweight='bold', color=colors_media[idx])

        # Add shading for winner regions
        ax.axhspan(0.6, 1.0, alpha=0.1, color='red', label='Acidic wins')
        ax.axhspan(0.0, 0.4, alpha=0.1, color='blue', label='Alkaline wins')

    axes[0].legend(fontsize=7, loc='lower right')

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_pH_diff_vs_outcome_scatter.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_pH_diff_vs_outcome_scatter.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_pH_diff_vs_outcome_scatter.pdf', bbox_inches='tight')
    plt.close()

    print(f"✓ Saved: {output_dir}/Fig_pH_diff_vs_outcome_scatter.[svg/png/pdf]")


def plot_combined_figure(results):
    """Combined figure: bar + scatter for Nutr+ only"""

    fig = plt.figure(figsize=(160*mm, 65*mm), dpi=150)
    colors_media = get_medium_colors()

    # Panel A: Stacked bar for all media
    ax1 = fig.add_subplot(121)

    media = ['L', 'M', 'H']
    media_labels = ['Nutr$-$', 'Base', 'Nutr$+$']

    acidic_rates = []
    alkaline_rates = []
    tie_rates = []
    totals = []

    for medium in media:
        total = results[medium]['total']
        if total > 0:
            acidic_rates.append(results[medium]['acidic_wins'] / total * 100)
            alkaline_rates.append(results[medium]['alkaline_wins'] / total * 100)
            tie_rates.append(results[medium]['tie'] / total * 100)
        else:
            acidic_rates.append(0)
            alkaline_rates.append(0)
            tie_rates.append(0)
        totals.append(total)

    x = np.arange(len(media))
    width = 0.6

    bars1 = ax1.bar(x, acidic_rates, width, label='Acidic wins',
                    color='#d62728', alpha=0.8, edgecolor='black', linewidth=0.5)
    bars2 = ax1.bar(x, tie_rates, width, bottom=acidic_rates, label='Mixed',
                    color='gray', alpha=0.5, edgecolor='black', linewidth=0.5)
    bars3 = ax1.bar(x, alkaline_rates, width,
                    bottom=[a+t for a, t in zip(acidic_rates, tie_rates)],
                    label='Alkaline wins', color='#1f77b4', alpha=0.8,
                    edgecolor='black', linewidth=0.5)

    ax1.axhline(50, color='black', linestyle='--', linewidth=1, alpha=0.7)

    for i, (acid, tie, alk, total) in enumerate(zip(acidic_rates, tie_rates, alkaline_rates, totals)):
        if total > 0 and acid > 8:
            ax1.text(i, acid/2, f'{acid:.0f}%', ha='center', va='center',
                    fontsize=9, color='white', fontweight='bold')
        if total > 0 and alk > 8:
            ax1.text(i, acid + tie + alk/2, f'{alk:.0f}%', ha='center', va='center',
                    fontsize=9, color='white', fontweight='bold')
        if total > 0:
            ax1.text(i, 102, f'n={total}', ha='center', va='bottom', fontsize=7)

    ax1.set_ylabel('Outcome Fraction (%)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(media_labels)
    ax1.set_ylim(0, 115)
    ax1.legend(fontsize=7, loc='upper left')
    ax1.set_title('A', fontweight='bold', loc='left', fontsize=12)

    # Panel B: Scatter for Nutr+ only
    ax2 = fig.add_subplot(122)

    medium = 'H'
    ph_diffs = results[medium]['ph_diffs']
    pdis = results[medium]['pdis']

    if len(ph_diffs) > 3:
        ax2.scatter(ph_diffs, pdis, alpha=0.6, s=40, color=colors_media[2])

        if len(set(ph_diffs)) > 1:
            slope, intercept, r, p, se = stats.linregress(ph_diffs, pdis)
            x_line = np.array([min(ph_diffs), max(ph_diffs)])
            y_line = slope * x_line + intercept
            ax2.plot(x_line, y_line, color='black', linewidth=2, linestyle='--')

            ax2.annotate(f'R² = {r**2:.2f}\np = {p:.3f}',
                        xy=(0.05, 0.95), xycoords='axes fraction',
                        verticalalignment='top', fontsize=9)

    ax2.axhline(0.5, color='gray', linestyle=':', alpha=0.5)
    ax2.axhspan(0.6, 1.0, alpha=0.1, color='red')
    ax2.axhspan(0.0, 0.4, alpha=0.1, color='blue')

    ax2.set_xlabel('pH Difference (alkaline − acidic parent)')
    ax2.set_ylabel('Similarity to Acidic Parent')
    ax2.set_ylim(0, 1)
    ax2.set_title('B (Nutr$+$)', fontweight='bold', loc='left', fontsize=12)

    # Add winner labels
    ax2.text(0.95, 0.85, 'Acidic\nwins', transform=ax2.transAxes, ha='right',
            fontsize=8, color='#d62728', fontweight='bold')
    ax2.text(0.95, 0.15, 'Alkaline\nwins', transform=ax2.transAxes, ha='right',
            fontsize=8, color='#1f77b4', fontweight='bold')

    plt.tight_layout()

    # Save
    fig.savefig(f'{output_dir}/Fig_acidic_vs_alkaline_combined.svg', bbox_inches='tight')
    fig.savefig(f'{output_dir}/Fig_acidic_vs_alkaline_combined.png', bbox_inches='tight', dpi=300)
    fig.savefig(f'{output_dir}/Fig_acidic_vs_alkaline_combined.pdf', bbox_inches='tight')
    plt.close()

    print(f"✓ Saved: {output_dir}/Fig_acidic_vs_alkaline_combined.[svg/png/pdf]")


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
        print(f"  Total acidic vs alkaline matchups: {total}")

        if total > 0:
            acid_rate = r['acidic_wins'] / total * 100
            alk_rate = r['alkaline_wins'] / total * 100
            tie_rate = r['tie'] / total * 100

            print(f"  Acidic community wins: {r['acidic_wins']} ({acid_rate:.1f}%)")
            print(f"  Alkaline community wins: {r['alkaline_wins']} ({alk_rate:.1f}%)")
            print(f"  Tie/Mixed: {r['tie']} ({tie_rate:.1f}%)")

            # Binomial test
            if r['acidic_wins'] + r['alkaline_wins'] > 0:
                from scipy.stats import binomtest
                n_decisive = r['acidic_wins'] + r['alkaline_wins']
                result = binomtest(r['acidic_wins'], n_decisive, p=0.5, alternative='greater')
                print(f"  Binomial test (acidic > 50%): p = {result.pvalue:.4f}")

                # Chi-square test
                observed = [r['acidic_wins'], r['alkaline_wins']]
                expected = [n_decisive/2, n_decisive/2]
                chi2, p_chi = stats.chisquare(observed, expected)
                print(f"  Chi-square test: χ² = {chi2:.2f}, p = {p_chi:.4f}")


def main():
    """Main function"""

    # Analyze competition outcomes
    results = analyze_acidic_vs_alkaline_community_competition()

    # Print detailed results
    print_detailed_results(results)

    # Generate plots
    print("\n" + "="*60)
    print("GENERATING FIGURES")
    print("="*60)

    plot_win_rate_stacked(results)
    plot_ph_diff_vs_outcome(results)
    plot_combined_figure(results)

    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"\nOutput directory: {output_dir}")
    print("\nGenerated files:")
    print("  - Fig_acidic_vs_alkaline_winrate_stacked.[svg/png/pdf]")
    print("  - Fig_pH_diff_vs_outcome_scatter.[svg/png/pdf]")
    print("  - Fig_acidic_vs_alkaline_combined.[svg/png/pdf]")


if __name__ == "__main__":
    main()
