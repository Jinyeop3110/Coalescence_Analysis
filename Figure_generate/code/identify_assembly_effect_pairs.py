#!/usr/bin/env python3
"""
Assembly Effect Analysis - Pair Identification
==============================================

This script identifies pairs of communities where we can compare:
1. Coalesced communities (formed by merging two parent communities)
2. Parent communities (that share the same initial species pool as the coalesced community)

The key comparison:
- Coalesced community from pool size 6+6 (total 12 species) vs Parent community with pool size 12
- Coalesced community from pool size 12+12 (total 24 species) vs Parent community with pool size 24

This allows us to quantify the "assembly effect" - how different are communities when they
are assembled directly vs. when they are formed through coalescence of smaller communities.

Author: Assembly Effect Analysis
Date: 2025
"""

import os
import sys
import numpy as np
import pandas as pd
from collections import defaultdict

# Add path for imports
sys.path.append('.')
from common_setup import *

def get_species_pool_for_community(community_idx, coalescence_type='S'):
    """
    Determine the species pool size for a given parent community.

    Based on the common_setup.py logic:
    - For CoalescenceType 'S' (parent communities):
        - CommunityIDX 1-9: pool size 6
        - CommunityIDX 10-18: pool size 12
        - CommunityIDX 19-30: pool size 24
    - For CoalescenceType 'C' (coalesced communities):
        - CommunityIDX 1-14: derived from pool size 6 (6+6)
        - CommunityIDX 15-41: derived from pool size 12 (12+12)
        - CommunityIDX 42-47: derived from pool size 24 (24+24)
    """
    if coalescence_type == 'S':
        if community_idx <= 9:
            return 6
        elif community_idx <= 18:
            return 12
        elif community_idx <= 30:
            return 24
    elif coalescence_type == 'C':
        if community_idx <= 14:
            return 6  # each parent has 6, total potential is 12
        elif community_idx <= 41:
            return 12  # each parent has 12, total potential is 24
        elif community_idx <= 47:
            return 24  # each parent has 24, total potential is 48
    return None

def get_species_composition(sample_idx_list, processed_sequences):
    """
    Get the species composition (which ASVs are present) for a list of samples.
    Returns a set of ASV indices that are present (abundance > threshold).
    """
    threshold = 0.001  # Consider species present if > 0.1% abundance

    species_sets = []
    for sample_idx in sample_idx_list:
        abundance = getAbundance(processed_sequences, sample_idx)
        if abundance is not None:
            abundance = np.array(abundance, dtype=float)
            # Normalize
            if abundance.sum() > 0:
                abundance = abundance / abundance.sum()
            present_species = set(np.where(abundance > threshold)[0])
            species_sets.append(present_species)

    return species_sets

def identify_comparable_pairs():
    """
    Identify pairs where coalesced and parent communities share the same initial species pool.

    Returns a dictionary with structure:
    {
        'medium': {
            '12_vs_6+6': [
                {
                    'parent_community_idx': int,
                    'parent_pool_size': 12,
                    'parent_samples': [list of sample IDs],
                    'coalesced_community_idx': int,
                    'coalesced_pool_size': 6,  # each parent community
                    'coalesced_samples': [list of sample IDs],
                    'sub1_community_idx': int,
                    'sub2_community_idx': int,
                    'sub1_samples': [list of sample IDs],
                    'sub2_samples': [list of sample IDs],
                    'species_pool_overlap': set of species indices
                }
            ],
            '24_vs_12+12': [...]
        }
    }
    """

    mediums = ['L', 'M', 'H']
    results = {}

    # Combine processed sequences
    processed_sequences = pd.concat([
        Processed_sequences_synthetic,
        Processed_sequences_natural
    ], ignore_index=True)

    for medium in mediums:
        medium_name = medium + 'N'
        results[medium_name] = {
            '12_vs_6+6': [],
            '24_vs_12+12': []
        }

        print(f"\n{'='*80}")
        print(f"Analyzing Medium: {medium_name}")
        print(f"{'='*80}")

        # Get all parent communities for this medium
        parent_communities_12 = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'S')
        ]

        # Filter by pool size 12 and 24
        parent_12 = parent_communities_12[
            (parent_communities_12['CommunityIDX'] > 9) &
            (parent_communities_12['CommunityIDX'] <= 18)
        ]

        parent_24 = parent_communities_12[
            (parent_communities_12['CommunityIDX'] > 18) &
            (parent_communities_12['CommunityIDX'] <= 30)
        ]

        # Get all coalesced communities for this medium
        coalesced_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'C')
        ]

        # Compare pool size 12 parent vs 6+6 coalesced
        print(f"\n--- Comparing Pool Size 12 (Parent) vs 6+6 (Coalesced) ---")
        coalesced_6 = coalesced_communities[
            (coalesced_communities['CommunityIDX'] <= 14)
        ]

        for _, parent_row in parent_12.iterrows():
            parent_idx = parent_row['CommunityIDX']
            parent_sample = parent_row['SampleIDX']

            # Get parent species composition
            parent_abundance = getAbundance(processed_sequences, parent_sample)
            if parent_abundance is None:
                continue
            parent_abundance = np.array(parent_abundance, dtype=float)
            if parent_abundance.sum() > 0:
                parent_abundance = parent_abundance / parent_abundance.sum()
            parent_species = set(np.where(parent_abundance > 0.001)[0])

            print(f"\nParent Community {parent_idx} (Sample: {parent_sample})")
            print(f"  Number of species: {len(parent_species)}")
            print(f"  Species indices: {sorted(parent_species)}")

            # Check all coalesced communities from pool size 6
            for _, coal_row in coalesced_6.iterrows():
                coal_idx = coal_row['CommunityIDX']
                coal_sample = coal_row['SampleIDX']

                # Get the two parent communities that formed this coalesced community
                recipe_row = Coalescence_recipe[Coalescence_recipe['CommunityIDX_Coal'] == coal_idx]
                if recipe_row.empty:
                    continue

                sub1_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub1'])
                sub2_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub2'])

                # Get samples for sub1 and sub2
                sub1_sample = Metadata[
                    (Metadata['CommunityIDX'] == sub1_idx) &
                    (Metadata['Timepoint'] == 'F') &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Medium'] == medium)
                ]['SampleIDX'].values

                sub2_sample = Metadata[
                    (Metadata['CommunityIDX'] == sub2_idx) &
                    (Metadata['Timepoint'] == 'F') &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Medium'] == medium)
                ]['SampleIDX'].values

                if len(sub1_sample) == 0 or len(sub2_sample) == 0:
                    continue

                sub1_sample = sub1_sample[0]
                sub2_sample = sub2_sample[0]

                # Get species in sub1 and sub2
                sub1_abundance = getAbundance(processed_sequences, sub1_sample)
                sub2_abundance = getAbundance(processed_sequences, sub2_sample)

                if sub1_abundance is None or sub2_abundance is None:
                    continue

                sub1_abundance = np.array(sub1_abundance, dtype=float)
                sub2_abundance = np.array(sub2_abundance, dtype=float)

                if sub1_abundance.sum() > 0:
                    sub1_abundance = sub1_abundance / sub1_abundance.sum()
                if sub2_abundance.sum() > 0:
                    sub2_abundance = sub2_abundance / sub2_abundance.sum()

                sub1_species = set(np.where(sub1_abundance > 0.001)[0])
                sub2_species = set(np.where(sub2_abundance > 0.001)[0])
                combined_species = sub1_species.union(sub2_species)

                # Check if parent and combined species pool overlap significantly
                overlap = parent_species.intersection(combined_species)
                overlap_fraction = len(overlap) / len(parent_species.union(combined_species))

                print(f"  Coalesced {coal_idx} (from Sub{sub1_idx}+Sub{sub2_idx}, Sample: {coal_sample})")
                print(f"    Sub1 species: {sorted(sub1_species)}")
                print(f"    Sub2 species: {sorted(sub2_species)}")
                print(f"    Combined species: {sorted(combined_species)}")
                print(f"    Overlap: {sorted(overlap)} ({len(overlap)}/{len(parent_species.union(combined_species))}, {overlap_fraction:.2%})")

                # If they share the same species pool (or very similar), record as comparable pair
                if overlap_fraction > 0.8:  # At least 80% overlap
                    pair = {
                        'parent_community_idx': int(parent_idx),
                        'parent_pool_size': 12,
                        'parent_sample': parent_sample,
                        'parent_species': sorted(parent_species),
                        'coalesced_community_idx': int(coal_idx),
                        'coalesced_pool_size': 6,
                        'coalesced_sample': coal_sample,
                        'sub1_community_idx': int(sub1_idx),
                        'sub2_community_idx': int(sub2_idx),
                        'sub1_sample': sub1_sample,
                        'sub2_sample': sub2_sample,
                        'sub1_species': sorted(sub1_species),
                        'sub2_species': sorted(sub2_species),
                        'combined_species': sorted(combined_species),
                        'species_pool_overlap': sorted(overlap),
                        'overlap_fraction': overlap_fraction
                    }
                    results[medium_name]['12_vs_6+6'].append(pair)
                    print(f"    ✓ COMPARABLE PAIR FOUND!")

        # Compare pool size 24 parent vs 12+12 coalesced
        print(f"\n--- Comparing Pool Size 24 (Parent) vs 12+12 (Coalesced) ---")
        coalesced_12 = coalesced_communities[
            (coalesced_communities['CommunityIDX'] > 14) &
            (coalesced_communities['CommunityIDX'] <= 41)
        ]

        for _, parent_row in parent_24.iterrows():
            parent_idx = parent_row['CommunityIDX']
            parent_sample = parent_row['SampleIDX']

            # Get parent species composition
            parent_abundance = getAbundance(processed_sequences, parent_sample)
            if parent_abundance is None:
                continue
            parent_abundance = np.array(parent_abundance, dtype=float)
            if parent_abundance.sum() > 0:
                parent_abundance = parent_abundance / parent_abundance.sum()
            parent_species = set(np.where(parent_abundance > 0.001)[0])

            print(f"\nParent Community {parent_idx} (Sample: {parent_sample})")
            print(f"  Number of species: {len(parent_species)}")
            print(f"  Species indices: {sorted(parent_species)}")

            # Check all coalesced communities from pool size 12
            for _, coal_row in coalesced_12.iterrows():
                coal_idx = coal_row['CommunityIDX']
                coal_sample = coal_row['SampleIDX']

                # Get the two parent communities that formed this coalesced community
                recipe_row = Coalescence_recipe[Coalescence_recipe['CommunityIDX_Coal'] == coal_idx]
                if recipe_row.empty:
                    continue

                sub1_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub1'])
                sub2_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub2'])

                # Get samples for sub1 and sub2
                sub1_sample = Metadata[
                    (Metadata['CommunityIDX'] == sub1_idx) &
                    (Metadata['Timepoint'] == 'F') &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Medium'] == medium)
                ]['SampleIDX'].values

                sub2_sample = Metadata[
                    (Metadata['CommunityIDX'] == sub2_idx) &
                    (Metadata['Timepoint'] == 'F') &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Medium'] == medium)
                ]['SampleIDX'].values

                if len(sub1_sample) == 0 or len(sub2_sample) == 0:
                    continue

                sub1_sample = sub1_sample[0]
                sub2_sample = sub2_sample[0]

                # Get species in sub1 and sub2
                sub1_abundance = getAbundance(processed_sequences, sub1_sample)
                sub2_abundance = getAbundance(processed_sequences, sub2_sample)

                if sub1_abundance is None or sub2_abundance is None:
                    continue

                sub1_abundance = np.array(sub1_abundance, dtype=float)
                sub2_abundance = np.array(sub2_abundance, dtype=float)

                if sub1_abundance.sum() > 0:
                    sub1_abundance = sub1_abundance / sub1_abundance.sum()
                if sub2_abundance.sum() > 0:
                    sub2_abundance = sub2_abundance / sub2_abundance.sum()

                sub1_species = set(np.where(sub1_abundance > 0.001)[0])
                sub2_species = set(np.where(sub2_abundance > 0.001)[0])
                combined_species = sub1_species.union(sub2_species)

                # Check if parent and combined species pool overlap significantly
                overlap = parent_species.intersection(combined_species)
                overlap_fraction = len(overlap) / len(parent_species.union(combined_species))

                print(f"  Coalesced {coal_idx} (from Sub{sub1_idx}+Sub{sub2_idx}, Sample: {coal_sample})")
                print(f"    Sub1 species: {sorted(sub1_species)}")
                print(f"    Sub2 species: {sorted(sub2_species)}")
                print(f"    Combined species: {sorted(combined_species)}")
                print(f"    Overlap: {sorted(overlap)} ({len(overlap)}/{len(parent_species.union(combined_species))}, {overlap_fraction:.2%})")

                # If they share the same species pool (or very similar), record as comparable pair
                if overlap_fraction > 0.8:  # At least 80% overlap
                    pair = {
                        'parent_community_idx': int(parent_idx),
                        'parent_pool_size': 24,
                        'parent_sample': parent_sample,
                        'parent_species': sorted(parent_species),
                        'coalesced_community_idx': int(coal_idx),
                        'coalesced_pool_size': 12,
                        'coalesced_sample': coal_sample,
                        'sub1_community_idx': int(sub1_idx),
                        'sub2_community_idx': int(sub2_idx),
                        'sub1_sample': sub1_sample,
                        'sub2_sample': sub2_sample,
                        'sub1_species': sorted(sub1_species),
                        'sub2_species': sorted(sub2_species),
                        'combined_species': sorted(combined_species),
                        'species_pool_overlap': sorted(overlap),
                        'overlap_fraction': overlap_fraction
                    }
                    results[medium_name]['24_vs_12+12'].append(pair)
                    print(f"    ✓ COMPARABLE PAIR FOUND!")

    return results

def save_results(results, output_path='Figure/Assembly_effect/comparable_pairs.pkl'):
    """Save results to a pickle file for later use."""
    import pickle
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(results, f)
    print(f"\nResults saved to: {output_path}")

def print_summary(results):
    """Print a summary of identified pairs."""
    print("\n" + "="*80)
    print("SUMMARY OF COMPARABLE PAIRS")
    print("="*80)

    for medium, comparisons in results.items():
        print(f"\n{medium} Medium:")
        for comparison_type, pairs in comparisons.items():
            print(f"  {comparison_type}: {len(pairs)} pairs found")
            for i, pair in enumerate(pairs, 1):
                print(f"    {i}. Parent {pair['parent_community_idx']} ({pair['parent_pool_size']} species) "
                      f"<-> Coalesced {pair['coalesced_community_idx']} "
                      f"(Sub{pair['sub1_community_idx']}+Sub{pair['sub2_community_idx']}, "
                      f"{pair['coalesced_pool_size']} species each) "
                      f"- Overlap: {pair['overlap_fraction']:.1%}")

if __name__ == '__main__':
    print("="*80)
    print("Assembly Effect Analysis - Identifying Comparable Pairs")
    print("="*80)
    print("\nThis analysis identifies pairs where:")
    print("  1. A parent community with pool size N")
    print("  2. A coalesced community formed from two communities with pool size N/2")
    print("  3. Both share the same (or very similar) initial species pool")
    print("\nThis allows us to quantify the 'assembly effect' - how different communities")
    print("are when assembled directly vs. through coalescence.\n")

    # Identify comparable pairs
    results = identify_comparable_pairs()

    # Print summary
    print_summary(results)

    # Save results
    save_results(results)

    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)
