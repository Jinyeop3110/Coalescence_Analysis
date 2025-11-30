#!/usr/bin/env python3
"""
Quick Summary of Assembly Effect Pairs
======================================

Shows basic statistics about the identified pairs.
"""

import pickle
import numpy as np
import pandas as pd

# Load data
with open('Figure/Assembly_effect/all_assembly_pairs.pkl', 'rb') as f:
    data = pickle.load(f)

print("="*80)
print("ASSEMBLY EFFECT ANALYSIS - QUICK SUMMARY")
print("="*80)

# Overall statistics
total_pairs = sum(len(pairs) for medium_data in data['pairs'].values()
                 for pairs in medium_data.values())
print(f"\nTotal pairs: {total_pairs:,}")

# By medium and comparison
print("\n" + "-"*80)
print("Pairs by Medium and Comparison Type:")
print("-"*80)

for medium, comparisons in data['pairs'].items():
    print(f"\n{medium}:")
    for comp_type, pairs in comparisons.items():
        print(f"  {comp_type}: {len(pairs):,} pairs")

# Sample statistics for each comparison type
print("\n" + "="*80)
print("SPECIES DIVERSITY STATISTICS")
print("="*80)

for medium, comparisons in data['pairs'].items():
    print(f"\n{medium} Medium:")

    for comp_type, pairs in comparisons.items():
        if len(pairs) == 0:
            continue

        print(f"\n  {comp_type}:")

        # Parent diversity
        parent_divs = [p['parent_num_species'] for p in pairs]
        print(f"    Parent communities:")
        print(f"      Mean diversity: {np.mean(parent_divs):.2f} ± {np.std(parent_divs):.2f}")
        print(f"      Range: {np.min(parent_divs)} - {np.max(parent_divs)}")

        # Coalesced diversity
        coal_divs = [p['coalesced_num_species'] for p in pairs]
        print(f"    Coalesced communities:")
        print(f"      Mean diversity: {np.mean(coal_divs):.2f} ± {np.std(coal_divs):.2f}")
        print(f"      Range: {np.min(coal_divs)} - {np.max(coal_divs)}")

        # Difference
        diffs = np.array(parent_divs) - np.array(coal_divs)
        print(f"    Difference (Parent - Coalesced):")
        print(f"      Mean: {np.mean(diffs):.2f} ± {np.std(diffs):.2f}")
        print(f"      % with Parent > Coalesced: {100*np.sum(diffs > 0)/len(diffs):.1f}%")
        print(f"      % with Parent < Coalesced: {100*np.sum(diffs < 0)/len(diffs):.1f}%")
        print(f"      % with Parent = Coalesced: {100*np.sum(diffs == 0)/len(diffs):.1f}%")

        # Overlap
        overlaps = [p['overlap_fraction'] for p in pairs]
        print(f"    Species pool overlap:")
        print(f"      Mean: {np.mean(overlaps):.2%} ± {np.std(overlaps):.2%}")
        print(f"      Range: {np.min(overlaps):.2%} - {np.max(overlaps):.2%}")

# Create summary table
print("\n" + "="*80)
print("SUMMARY TABLE")
print("="*80 + "\n")

summary_data = []
for medium, comparisons in data['pairs'].items():
    for comp_type, pairs in comparisons.items():
        if len(pairs) == 0:
            continue

        parent_divs = [p['parent_num_species'] for p in pairs]
        coal_divs = [p['coalesced_num_species'] for p in pairs]
        diffs = np.array(parent_divs) - np.array(coal_divs)
        overlaps = [p['overlap_fraction'] for p in pairs]

        summary_data.append({
            'Medium': medium,
            'Comparison': comp_type,
            'N_pairs': len(pairs),
            'Parent_diversity_mean': f"{np.mean(parent_divs):.2f}",
            'Parent_diversity_std': f"{np.std(parent_divs):.2f}",
            'Coalesced_diversity_mean': f"{np.mean(coal_divs):.2f}",
            'Coalesced_diversity_std': f"{np.std(coal_divs):.2f}",
            'Diversity_diff_mean': f"{np.mean(diffs):.2f}",
            'Diversity_diff_std': f"{np.std(diffs):.2f}",
            'Overlap_mean': f"{np.mean(overlaps):.2%}",
            'Overlap_std': f"{np.std(overlaps):.2%}"
        })

df = pd.DataFrame(summary_data)
print(df.to_string(index=False))

# Save to CSV
output_csv = 'Figure/Assembly_effect/assembly_pairs_statistics.csv'
df.to_csv(output_csv, index=False)
print(f"\nSummary statistics saved to: {output_csv}")

print("\n" + "="*80)
print("Analysis complete!")
print("="*80)
