#!/usr/bin/env python3
"""
Display Assembly Effect Pairs
==============================

This script loads and displays the identified comparable pairs from the
assembly effect analysis in a clean, readable format.
"""

import pickle
import pandas as pd

def load_pairs(pickle_path='Figure/Assembly_effect/comparable_pairs.pkl'):
    """Load the comparable pairs from pickle file."""
    with open(pickle_path, 'rb') as f:
        pairs = pickle.load(f)
    return pairs

def display_pairs(pairs):
    """Display pairs in a clean format."""
    print("\n" + "="*80)
    print("ASSEMBLY EFFECT ANALYSIS - COMPARABLE PAIRS")
    print("="*80)

    total_pairs = 0

    for medium, comparisons in pairs.items():
        print(f"\n{'='*80}")
        print(f"MEDIUM: {medium}")
        print(f"{'='*80}")

        for comparison_type, pair_list in comparisons.items():
            print(f"\n{comparison_type.upper().replace('_', ' ')}")
            print(f"-" * 80)

            if len(pair_list) == 0:
                print("  No comparable pairs found.")
                continue

            # Group by unique pairs (to avoid duplicates from replicates)
            unique_pairs = {}
            for pair in pair_list:
                key = (pair['parent_community_idx'], pair['coalesced_community_idx'])
                if key not in unique_pairs:
                    unique_pairs[key] = []
                unique_pairs[key].append(pair)

            for i, (key, replicates) in enumerate(unique_pairs.items(), 1):
                pair = replicates[0]  # Take first replicate for display
                print(f"\nPair {i}:")
                print(f"  Parent Community {pair['parent_community_idx']}:")
                print(f"    Pool Size: {pair['parent_pool_size']}")
                print(f"    Sample ID: {pair['parent_sample']}")
                print(f"    # Species present: {len(pair['parent_species'])}")
                print(f"    Species: {pair['parent_species'][:10]}{'...' if len(pair['parent_species']) > 10 else ''}")

                print(f"\n  Coalesced Community {pair['coalesced_community_idx']}:")
                print(f"    Formed from: Sub{pair['sub1_community_idx']} + Sub{pair['sub2_community_idx']}")
                print(f"    Each parent pool size: {pair['coalesced_pool_size']}")
                print(f"    Sample ID: {pair['coalesced_sample']}")
                print(f"    Sub1 sample: {pair['sub1_sample']}")
                print(f"    Sub2 sample: {pair['sub2_sample']}")
                print(f"    # Species in Sub1: {len(pair['sub1_species'])}")
                print(f"    # Species in Sub2: {len(pair['sub2_species'])}")
                print(f"    # Species combined: {len(pair['combined_species'])}")
                print(f"    Combined species: {pair['combined_species'][:10]}{'...' if len(pair['combined_species']) > 10 else ''}")

                print(f"\n  Species Pool Overlap:")
                print(f"    Overlap fraction: {pair['overlap_fraction']:.1%}")
                print(f"    Overlapping species: {pair['species_pool_overlap'][:10]}{'...' if len(pair['species_pool_overlap']) > 10 else ''}")

                print(f"\n  Replicates: {len(replicates)}")

                total_pairs += 1

    print("\n" + "="*80)
    print(f"TOTAL UNIQUE COMPARABLE PAIRS: {total_pairs}")
    print("="*80 + "\n")

def create_summary_table(pairs):
    """Create a summary table of all pairs."""
    data = []

    for medium, comparisons in pairs.items():
        for comparison_type, pair_list in comparisons.items():
            # Group by unique pairs
            unique_pairs = {}
            for pair in pair_list:
                key = (pair['parent_community_idx'], pair['coalesced_community_idx'])
                if key not in unique_pairs:
                    unique_pairs[key] = []
                unique_pairs[key].append(pair)

            for key, replicates in unique_pairs.items():
                pair = replicates[0]
                data.append({
                    'Medium': medium,
                    'Comparison': comparison_type,
                    'Parent_Comm': pair['parent_community_idx'],
                    'Parent_Sample': pair['parent_sample'],
                    'Parent_PoolSize': pair['parent_pool_size'],
                    'Parent_NumSpecies': len(pair['parent_species']),
                    'Coalesced_Comm': pair['coalesced_community_idx'],
                    'Coalesced_Sample': pair['coalesced_sample'],
                    'Sub1': pair['sub1_community_idx'],
                    'Sub2': pair['sub2_community_idx'],
                    'Sub1_Sample': pair['sub1_sample'],
                    'Sub2_Sample': pair['sub2_sample'],
                    'Sub1_NumSpecies': len(pair['sub1_species']),
                    'Sub2_NumSpecies': len(pair['sub2_species']),
                    'Combined_NumSpecies': len(pair['combined_species']),
                    'Overlap_Fraction': f"{pair['overlap_fraction']:.1%}",
                    'Num_Replicates': len(replicates)
                })

    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    # Load pairs
    pairs = load_pairs()

    # Display pairs
    display_pairs(pairs)

    # Create summary table
    summary_df = create_summary_table(pairs)

    print("\nSUMMARY TABLE:")
    print("="*80)
    print(summary_df.to_string(index=False))
    print("\n")

    # Save to CSV
    output_csv = 'Figure/Assembly_effect/comparable_pairs_summary.csv'
    summary_df.to_csv(output_csv, index=False)
    print(f"Summary table saved to: {output_csv}")
