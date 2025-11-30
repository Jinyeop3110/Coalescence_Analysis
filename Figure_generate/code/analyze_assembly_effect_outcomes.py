#!/usr/bin/env python3
"""
analyze_assembly_effect_outcomes.py

Purpose: Test the hypothesis that "assembly effect" (coalescence) produces more
         dominance or restructuring compared to "direct assembly".

Method:
- For parent communities: Treat the two sub-communities of the matched coalesced
  community as c1 and c2, and the parent as the "outcome"
- For coalesced communities: Use the actual sub-communities as c1 and c2, and
  the coalesced community as the outcome
- Classify each into Dominance, Mixing, or Restructuring using vector decomposition
- Compare the distributions between parent and coalesced

Output:
- Figure/Assembly_effect/Fig_assembly_effect_outcomes_comparison.svg
- Statistical comparison of outcome distributions
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pickle
import builtins
from pathlib import Path
from collections import OrderedDict

# Add path for imports
sys.path.append('.')
from common_setup import *

def metric_VectorDecomposition_onlyPositive(u, v, m):
    """
    Original vector decomposition metric.
    Returns u_component, v_component, restructuring_component, and orthogonal_vector.
    """
    def normalize(vec):
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    u = normalize(u)
    v = normalize(v)
    m = normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))

    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)

    # Calculate orthogonal component (restructured community vector)
    orthogonal_vec = m - (e12[0]*u) - (e12[1]*v)
    x3 = np.linalg.norm(orthogonal_vec)
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2 + 1e-10))

    return convert*x1, convert*x2, x3, orthogonal_vec


def classify_outcome(u, v, k):
    """
    Classify a single outcome into Dominance, Mixing, or Restructuring.

    Returns:
    - 0: Dominance
    - 1: Mixing
    - 2: Restructuring
    """
    x = np.sqrt(u**2 + v**2)
    y = np.abs(np.abs(np.arctan(u / (v + 1e-8))) - np.pi/4) / (np.pi/4)

    if (x**2 > 0.5) * (y > 0.5):
        return 0  # Dominance
    elif (x**2 > 0.5) * (y < 0.5):
        return 1  # Mixing
    elif (x**2 < 0.5):
        return 2  # Restructuring
    else:
        return 1  # Default to mixing if unclear


def analyze_assembly_effect_outcomes(assembly_data):
    """
    Analyze parent vs coalesced communities and classify outcomes by medium.

    For parent communities: Use the same sub-communities (c1, c2) that formed
    the matched coalesced community to decompose the parent.

    For coalesced communities: Use actual sub-communities (c1, c2) to decompose.

    This tests whether "assembly effect" (coalescence pathway) produces different
    outcomes than "direct assembly" (direct assembly from same species pool).

    Returns:
    --------
    dict with keys 'parent' and 'coalesced', each containing medium-specific results
    """
    print("\n=== Analyzing Assembly Effect: Parent vs Coalesced ===\n")

    results = {
        'parent': {
            'HN': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0, 'classifications': []},
            'MN': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0, 'classifications': []},
            'LN': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0, 'classifications': []}
        },
        'coalesced': {
            'HN': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0, 'classifications': []},
            'MN': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0, 'classifications': []},
            'LN': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0, 'classifications': []}
        }
    }

    pairs_data = assembly_data['pairs']

    # Process all pairs across all media and comparison types
    for medium in sorted(pairs_data.keys()):
        for comparison_type in sorted(pairs_data[medium].keys()):
            pairs = pairs_data[medium][comparison_type]

            print(f"Processing {medium} - {comparison_type}: {len(pairs)} pairs")

            for pair in pairs:
                # IMPORTANT: Only use pairs where parent and coalesced have matching replicates
                # This ensures we're comparing communities from the same experimental replicate
                if pair['parent_replicate'] != pair['coalesced_replicate']:
                    continue

                # Get abundances for coalesced community and its subs
                # Convert to arrays, handling potential NaN values
                def safe_array_convert(data):
                    arr = np.array(data, dtype=float)
                    # Replace NaN with 0
                    arr = np.nan_to_num(arr, nan=0.0)
                    return arr

                parent_abund = safe_array_convert(pair['parent_abundances'])
                coal_abund = safe_array_convert(pair['coalesced_abundances'])
                coal_sub1_abund = safe_array_convert(pair['sub1_abundances'])
                coal_sub2_abund = safe_array_convert(pair['sub2_abundances'])

                # For PARENT community: Check if it's also a coalesced community
                # If so, use ITS sub-communities from Coalescence_data
                parent_sample = pair['parent_sample']
                parent_coal_data = Coalescence_data[Coalescence_data['SampleIDX'] == parent_sample]

                if len(parent_coal_data) > 0:
                    # Parent IS a coalesced community - use its actual parents
                    parent_sub1_sample = parent_coal_data.iloc[0]['SampleIDX_Sub1']
                    parent_sub2_sample = parent_coal_data.iloc[0]['SampleIDX_Sub2']

                    # Get abundances from Processed_sequences
                    parent_sub1_abund = getAbundance_fixed(
                        pd.concat([Processed_sequences_synthetic, Processed_sequences_natural]),
                        parent_sub1_sample
                    )
                    parent_sub2_abund = getAbundance_fixed(
                        pd.concat([Processed_sequences_synthetic, Processed_sequences_natural]),
                        parent_sub2_sample
                    )

                    if parent_sub1_abund is None or parent_sub2_abund is None:
                        continue

                    parent_sub1_abund = np.array(parent_sub1_abund)
                    parent_sub2_abund = np.array(parent_sub2_abund)
                else:
                    # Parent is NOT a coalesced community - use same subs as coalesced
                    parent_sub1_abund = coal_sub1_abund.copy()
                    parent_sub2_abund = coal_sub2_abund.copy()

                # Apply threshold (same as phase diagram code)
                threshold = 1e-4
                parent_abund = parent_abund * (parent_abund > threshold)
                coal_abund = coal_abund * (coal_abund > threshold)
                coal_sub1_abund = coal_sub1_abund * (coal_sub1_abund > threshold)
                coal_sub2_abund = coal_sub2_abund * (coal_sub2_abund > threshold)
                parent_sub1_abund = parent_sub1_abund * (parent_sub1_abund > threshold)
                parent_sub2_abund = parent_sub2_abund * (parent_sub2_abund > threshold)

                try:
                    # Analyze PARENT community (direct assembly)
                    # Use the parent's own sub-communities if it's a coalesced community
                    u_parent, v_parent, k_parent, _ = metric_VectorDecomposition_onlyPositive(
                        parent_sub1_abund, parent_sub2_abund, parent_abund
                    )
                    class_parent = classify_outcome(u_parent, v_parent, k_parent)

                    # Store by medium
                    results['parent'][medium]['classifications'].append(class_parent)

                    # Analyze COALESCED community (assembly effect)
                    # Always use its actual sub-communities
                    u_coal, v_coal, k_coal, _ = metric_VectorDecomposition_onlyPositive(
                        coal_sub1_abund, coal_sub2_abund, coal_abund
                    )
                    class_coal = classify_outcome(u_coal, v_coal, k_coal)

                    # Store by medium
                    results['coalesced'][medium]['classifications'].append(class_coal)

                except Exception as e:
                    print(f"  Warning: Error processing pair: {e}")
                    continue

    # Count classifications
    for assembly_type in ['parent', 'coalesced']:
        for medium_type in ['HN', 'MN', 'LN']:
            for class_val in results[assembly_type][medium_type]['classifications']:
                if class_val == 0:
                    results[assembly_type][medium_type]['Dominance'] += 1
                elif class_val == 1:
                    results[assembly_type][medium_type]['Mixing'] += 1
                elif class_val == 2:
                    results[assembly_type][medium_type]['Restructuring'] += 1

    return results


def create_comparison_plot(results, output_dir):
    """Create comparison plot showing parent vs coalesced for each medium.
    Layout: Row 0 = Coalescence, Row 1 = Direct Assembly
            Columns = LN, MN, HN
    """
    from COLORMAP import get_phase_diagram_colors

    fig, axes = plt.subplots(2, 3, figsize=(10, 5.3))
    colors = get_phase_diagram_colors()

    media_order = ['LN', 'MN', 'HN']
    media_labels = {
        'LN': 'Nutr-',
        'MN': 'Base',
        'HN': 'Nutr+'
    }

    for col_idx, medium in enumerate(media_order):
        # Top row: Coalescence
        ax_coal = axes[0, col_idx]
        values_coal = [
            results['coalesced'][medium]['Dominance'],
            results['coalesced'][medium]['Mixing'],
            results['coalesced'][medium]['Restructuring']
        ]
        total_coal = sum(values_coal)

        if total_coal > 0:
            wedges, texts, autotexts = ax_coal.pie(
                values_coal,
                labels=None,
                colors=colors,
                autopct=lambda pct: f'{int(pct*total_coal/100)}\n({pct:.1f}%)' if pct > 0 else '',
                startangle=90,
                pctdistance=0.65
            )
            for wedge in wedges:
                wedge.set_alpha(0.85)
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')
            ax_coal.text(0, -1.3, f'n = {total_coal}', ha='center', fontsize=10, fontweight='bold')
        else:
            ax_coal.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=12)

        ax_coal.set_title(f'{media_labels[medium]}',
                         fontsize=12, fontweight='bold', pad=10)

        # Bottom row: Direct Assembly
        ax_parent = axes[1, col_idx]
        values_parent = [
            results['parent'][medium]['Dominance'],
            results['parent'][medium]['Mixing'],
            results['parent'][medium]['Restructuring']
        ]
        total_parent = sum(values_parent)

        if total_parent > 0:
            wedges, texts, autotexts = ax_parent.pie(
                values_parent,
                labels=None,
                colors=colors,
                autopct=lambda pct: f'{int(pct*total_parent/100)}\n({pct:.1f}%)' if pct > 0 else '',
                startangle=90,
                pctdistance=0.65
            )
            for wedge in wedges:
                wedge.set_alpha(0.85)
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')
            ax_parent.text(0, -1.3, f'n = {total_parent}', ha='center', fontsize=10, fontweight='bold')
        else:
            ax_parent.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=12)

    # Add row labels on the left side
    axes[0, 0].text(-0.3, 0.5, 'Coalescence', rotation=90, fontsize=14,
                   fontweight='bold', va='center', ha='center',
                   transform=axes[0, 0].transAxes)
    axes[1, 0].text(-0.3, 0.5, 'Direct Assembly', rotation=90, fontsize=14,
                   fontweight='bold', va='center', ha='center',
                   transform=axes[1, 0].transAxes)

    # Add legend
    fig.legend(
        labels=['Dominance', 'Mixing', 'Restructuring'],
        loc='upper center',
        bbox_to_anchor=(0.5, 0.99),
        ncol=3,
        fontsize=12,
        frameon=False
    )

    plt.suptitle('Assembly Method Comparison Across Nutrient Levels',
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.98])

    # Save
    output_filename = output_dir / "Fig_assembly_effect_parent_vs_coalesced.svg"
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n✓ Created comparison plot: {output_filename}")


def print_statistical_summary(results):
    """Print statistical summary comparing parent vs coalesced."""
    print("\n" + "="*90)
    print("STATISTICAL SUMMARY: Direct Assembly vs Coalescence")
    print("="*90)

    for medium in ['LN', 'MN', 'HN']:
        print(f"\n{medium}:")
        print("-" * 90)
        print(f"{'Type':<30} {'Dominance':<20} {'Mixing':<20} {'Restructuring':<20}")
        print("-" * 90)

        for assembly_type, label in [('parent', 'Direct Assembly'), ('coalesced', 'Coalescence')]:
            total = (results[assembly_type][medium]['Dominance'] +
                     results[assembly_type][medium]['Mixing'] +
                     results[assembly_type][medium]['Restructuring'])

            if total == 0:
                print(f"{label:<30} No data")
                continue

            dom_pct = results[assembly_type][medium]['Dominance'] / total * 100
            mix_pct = results[assembly_type][medium]['Mixing'] / total * 100
            rest_pct = results[assembly_type][medium]['Restructuring'] / total * 100

            print(f"{label:<30} {dom_pct:>5.1f}% ({results[assembly_type][medium]['Dominance']:>3}) "
                  f"{mix_pct:>5.1f}% ({results[assembly_type][medium]['Mixing']:>3}) "
                  f"{rest_pct:>5.1f}% ({results[assembly_type][medium]['Restructuring']:>3})")

        # Calculate difference
        total_parent = sum([results['parent'][medium][k] for k in ['Dominance', 'Mixing', 'Restructuring']])
        total_coal = sum([results['coalesced'][medium][k] for k in ['Dominance', 'Mixing', 'Restructuring']])

        if total_parent > 0 and total_coal > 0:
            diff_dom = (results['coalesced'][medium]['Dominance']/total_coal*100 -
                       results['parent'][medium]['Dominance']/total_parent*100)
            diff_mix = (results['coalesced'][medium]['Mixing']/total_coal*100 -
                       results['parent'][medium]['Mixing']/total_parent*100)
            diff_rest = (results['coalesced'][medium]['Restructuring']/total_coal*100 -
                        results['parent'][medium]['Restructuring']/total_parent*100)

            print(f"\n{'Difference (Coal - Parent)':<30} {diff_dom:>+6.1f} pp        {diff_mix:>+6.1f} pp        {diff_rest:>+6.1f} pp")

    print("\n" + "="*90)
    print("HYPOTHESIS TEST: Does assembly effect produce more dominance/restructuring?")
    print("="*90)

    # Check each medium
    all_supported = True
    for medium in ['LN', 'MN', 'HN']:
        total_parent = sum([results['parent'][medium][k] for k in ['Dominance', 'Mixing', 'Restructuring']])
        total_coal = sum([results['coalesced'][medium][k] for k in ['Dominance', 'Mixing', 'Restructuring']])

        diff_dom = (results['coalesced'][medium]['Dominance']/total_coal*100 -
                   results['parent'][medium]['Dominance']/total_parent*100)
        diff_rest = (results['coalesced'][medium]['Restructuring']/total_coal*100 -
                    results['parent'][medium]['Restructuring']/total_parent*100)

        print(f"\n{medium}: Dominance {diff_dom:+6.1f} pp, Restructuring {diff_rest:+6.1f} pp")

        if diff_dom <= 5 and diff_rest <= 5:
            all_supported = False

    if all_supported:
        print("\n✓ HYPOTHESIS SUPPORTED:")
        print("  Coalescence shows MORE dominance/restructuring than direct assembly across all media.")
    else:
        print("\n≈ HYPOTHESIS PARTIALLY SUPPORTED:")
        print("  Assembly effect shows increased dominance/restructuring in some but not all media.")

    print("="*90)


def main():
    """Main function to analyze assembly effect outcomes."""

    print("="*80)
    print("Assembly Effect Outcome Analysis: Coalescence by Medium")
    print("="*80)
    print("Analyzing coalescence outcomes (dominance, mixing, restructuring)")
    print("across different nutrient levels (LN, MN, HN)")
    print()

    # Create output directory
    output_dir = Path("Figure/Assembly_effect")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load assembly pairs data
    data_path = 'Figure/Assembly_effect/assembly_pairs_CORRECT.pkl'
    print(f"Loading assembly pairs from: {data_path}")

    with open(data_path, 'rb') as f:
        assembly_data = pickle.load(f)

    # Analyze outcomes
    results = analyze_assembly_effect_outcomes(assembly_data)

    # Create comparison plot
    create_comparison_plot(results, output_dir)

    # Print statistical summary
    print_statistical_summary(results)

    # Save results
    results_path = output_dir / "assembly_effect_outcomes_results.pkl"
    with open(results_path, 'wb') as f:
        pickle.dump(results, f)
    print(f"\n✓ Results saved to: {results_path}")

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
