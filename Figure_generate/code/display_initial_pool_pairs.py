#!/usr/bin/env python3
"""
Display Assembly Effect Pairs - Matched by Initial Pool
========================================================

Shows the 6 pairs identified by matching initial species pools.
"""

import pickle
import pandas as pd
import numpy as np

# Load data
with open('Figure/Assembly_effect/assembly_pairs_initial_pool.pkl', 'rb') as f:
    data = pickle.load(f)

print("="*80)
print("ASSEMBLY EFFECT PAIRS - MATCHED BY INITIAL SPECIES POOL")
print("="*80)
print("\nMethod: Match communities with ≥80% Jaccard similarity in INITIAL pools")
print("Initial pool inferred from observed species in parent communities")

total_pairs = sum(len(pairs) for medium_data in data['pairs'].values()
                 for pairs in medium_data.values())
print(f"\nTotal pairs: {total_pairs}")

# Detailed pair information
for medium, comparisons in data['pairs'].items():
    print(f"\n{'='*80}")
    print(f"MEDIUM: {medium}")
    print(f"{'='*80}")

    for comp_type, pairs in comparisons.items():
        print(f"\n{comp_type.upper().replace('_', ' ')}:")
        print("-"*80)

        if len(pairs) == 0:
            print("  No pairs found.")
            continue

        for i, pair in enumerate(pairs, 1):
            print(f"\nPair {i}:")
            print(f"  Parent Community {pair['parent_community_idx']} (Sample: {pair['parent_sample']})")
            print(f"    Initial pool size: {pair['parent_initial_pool_size']} species")
            print(f"    Initial pool: {pair['parent_initial_pool']}")
            print(f"    Final diversity: {pair['parent_final_diversity']} species")
            print(f"    Final species: {pair['parent_final_species']}")

            print(f"\n  Coalesced Community {pair['coalesced_community_idx']} (Sample: {pair['coalesced_sample']})")
            print(f"    Formed from: Sub{pair['sub1_community_idx']} + Sub{pair['sub2_community_idx']}")
            print(f"    Sub1 sample: {pair['sub1_sample']}")
            print(f"    Sub2 sample: {pair['sub2_sample']}")
            print(f"    Initial pool size: {pair['coalesced_initial_pool_size']} species")
            print(f"    Initial pool: {pair['coalesced_initial_pool']}")
            print(f"    Final diversity: {pair['coalesced_final_diversity']} species")
            print(f"    Final species: {pair['coalesced_final_species']}")

            print(f"\n  Initial Pool Match:")
            print(f"    Jaccard similarity: {pair['initial_pool_jaccard']:.1%}")
            print(f"    Overlapping species: {pair['initial_pool_overlap']}")

            print(f"\n  Assembly Effect:")
            div_diff = pair['parent_final_diversity'] - pair['coalesced_final_diversity']
            print(f"    Diversity difference (Parent - Coalesced): {div_diff}")
            if div_diff > 0:
                print(f"    → Parent has MORE species (+{div_diff})")
            elif div_diff < 0:
                print(f"    → Coalesced has MORE species ({div_diff})")
            else:
                print(f"    → Same final diversity")

# Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

summary_data = []
for medium, comparisons in data['pairs'].items():
    for comp_type, pairs in comparisons.items():
        if len(pairs) == 0:
            continue

        parent_init = [p['parent_initial_pool_size'] for p in pairs]
        coal_init = [p['coalesced_initial_pool_size'] for p in pairs]
        parent_final = [p['parent_final_diversity'] for p in pairs]
        coal_final = [p['coalesced_final_diversity'] for p in pairs]
        div_diffs = np.array(parent_final) - np.array(coal_final)
        jaccards = [p['initial_pool_jaccard'] for p in pairs]

        summary_data.append({
            'Medium': medium,
            'Comparison': comp_type,
            'N_pairs': len(pairs),
            'Parent_initial_mean': f"{np.mean(parent_init):.1f}",
            'Coalesced_initial_mean': f"{np.mean(coal_init):.1f}",
            'Parent_final_mean': f"{np.mean(parent_final):.1f}",
            'Coalesced_final_mean': f"{np.mean(coal_final):.1f}",
            'Diversity_diff_mean': f"{np.mean(div_diffs):.2f}",
            'Initial_pool_jaccard_mean': f"{np.mean(jaccards):.1%}"
        })

df = pd.DataFrame(summary_data)
print("\n" + df.to_string(index=False))

# Save to CSV
output_csv = 'Figure/Assembly_effect/initial_pool_pairs_summary.csv'
df.to_csv(output_csv, index=False)
print(f"\n\nSummary saved to: {output_csv}")

print("\n" + "="*80)
print("Recommendation: Use these 6 pairs for assembly effect analysis")
print("="*80)
