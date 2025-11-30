#!/usr/bin/env python3
"""
Assembly Effect Analysis - Pair Identification (CORRECTED VERSION)
==================================================================

This script identifies ALL pairs of communities for assembly effect comparison.

KEY INSIGHT: We don't need to match species pools - we compare ALL parent communities
of a given pool size with ALL coalesced communities from the corresponding smaller pools.

The comparison groups are:
1. Parent pool-12 vs ALL coalesced 6+6 (within same medium)
2. Parent pool-24 vs ALL coalesced 12+12 (within same medium)

The species composition overlap is a DATA OUTCOME to be measured, not a selection criterion!

Author: Assembly Effect Analysis (Corrected)
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

def identify_all_assembly_pairs():
    """
    Identify ALL comparable pairs for assembly effect analysis.

    Returns a dictionary organized by medium and comparison type, containing
    information about parent communities, coalesced communities, and their
    sub-communities.
    """

    mediums = ['L', 'M', 'H']
    results = {
        'metadata': {
            'description': 'Assembly effect pairs - comparing direct assembly vs coalescence',
            'comparison_types': {
                '12_vs_6+6': 'Parent community pool-12 vs Coalesced from two pool-6',
                '24_vs_12+12': 'Parent community pool-24 vs Coalesced from two pool-12'
            }
        },
        'pairs': {}
    }

    # Combine processed sequences
    processed_sequences = pd.concat([
        Processed_sequences_synthetic,
        Processed_sequences_natural
    ], ignore_index=True)

    for medium in mediums:
        medium_name = medium + 'N'
        results['pairs'][medium_name] = {
            '12_vs_6+6': [],
            '24_vs_12+12': []
        }

        print(f"\n{'='*80}")
        print(f"Analyzing Medium: {medium_name}")
        print(f"{'='*80}")

        # ======================================================================
        # PART 1: Pool 12 (Parent) vs 6+6 (Coalesced)
        # ======================================================================
        print(f"\n--- Pool Size 12 (Parent) vs 6+6 (Coalesced) ---")

        # Get ALL parent communities with pool size 12 in this medium
        parent_12_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'S') &
            (Metadata['CommunityIDX'] > 9) &
            (Metadata['CommunityIDX'] <= 18)
        ]

        # Get ALL coalesced communities from pool size 6 (6+6) in this medium
        coalesced_6_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'C') &
            (Metadata['CommunityIDX'] <= 14)
        ]

        print(f"Parent pool-12 communities: {len(parent_12_communities)} samples")
        print(f"  Community IDs: {sorted(parent_12_communities['CommunityIDX'].unique())}")
        print(f"Coalesced 6+6 communities: {len(coalesced_6_communities)} samples")
        print(f"  Community IDs: {sorted(coalesced_6_communities['CommunityIDX'].unique())}")

        # Create all pairwise comparisons
        pair_count = 0
        for _, parent_row in parent_12_communities.iterrows():
            parent_idx = parent_row['CommunityIDX']
            parent_sample = parent_row['SampleIDX']

            # Get parent abundance
            parent_abundance = getAbundance(processed_sequences, parent_sample)
            if parent_abundance is None:
                continue
            parent_abundance = np.array(parent_abundance, dtype=float)
            if parent_abundance.sum() > 0:
                parent_abundance = parent_abundance / parent_abundance.sum()
            parent_species = set(np.where(parent_abundance > 0.001)[0])

            for _, coal_row in coalesced_6_communities.iterrows():
                coal_idx = coal_row['CommunityIDX']
                coal_sample = coal_row['SampleIDX']

                # Get sub-communities
                recipe_row = Coalescence_recipe[Coalescence_recipe['CommunityIDX_Coal'] == coal_idx]
                if recipe_row.empty:
                    continue

                sub1_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub1'])
                sub2_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub2'])

                # Get sub community samples
                sub1_sample_rows = Metadata[
                    (Metadata['CommunityIDX'] == sub1_idx) &
                    (Metadata['Timepoint'] == 'F') &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Medium'] == medium)
                ]['SampleIDX'].values

                sub2_sample_rows = Metadata[
                    (Metadata['CommunityIDX'] == sub2_idx) &
                    (Metadata['Timepoint'] == 'F') &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Medium'] == medium)
                ]['SampleIDX'].values

                if len(sub1_sample_rows) == 0 or len(sub2_sample_rows) == 0:
                    continue

                sub1_sample = sub1_sample_rows[0]
                sub2_sample = sub2_sample_rows[0]

                # Get abundances
                sub1_abundance = getAbundance(processed_sequences, sub1_sample)
                sub2_abundance = getAbundance(processed_sequences, sub2_sample)
                coal_abundance = getAbundance(processed_sequences, coal_sample)

                if sub1_abundance is None or sub2_abundance is None or coal_abundance is None:
                    continue

                sub1_abundance = np.array(sub1_abundance, dtype=float)
                sub2_abundance = np.array(sub2_abundance, dtype=float)
                coal_abundance = np.array(coal_abundance, dtype=float)

                if sub1_abundance.sum() > 0:
                    sub1_abundance = sub1_abundance / sub1_abundance.sum()
                if sub2_abundance.sum() > 0:
                    sub2_abundance = sub2_abundance / sub2_abundance.sum()
                if coal_abundance.sum() > 0:
                    coal_abundance = coal_abundance / coal_abundance.sum()

                sub1_species = set(np.where(sub1_abundance > 0.001)[0])
                sub2_species = set(np.where(sub2_abundance > 0.001)[0])
                coal_species = set(np.where(coal_abundance > 0.001)[0])
                combined_sub_species = sub1_species.union(sub2_species)

                # Calculate overlap (for reference, not filtering)
                overlap = parent_species.intersection(combined_sub_species)
                if len(parent_species.union(combined_sub_species)) > 0:
                    overlap_fraction = len(overlap) / len(parent_species.union(combined_sub_species))
                else:
                    overlap_fraction = 0.0

                # Store the pair (ALL pairs, no filtering by overlap)
                pair = {
                    'parent_community_idx': int(parent_idx),
                    'parent_pool_size': 12,
                    'parent_sample': parent_sample,
                    'parent_species': sorted([int(x) for x in parent_species]),
                    'parent_num_species': len(parent_species),
                    'coalesced_community_idx': int(coal_idx),
                    'coalesced_pool_size': 6,  # each parent
                    'coalesced_sample': coal_sample,
                    'coalesced_species': sorted([int(x) for x in coal_species]),
                    'coalesced_num_species': len(coal_species),
                    'sub1_community_idx': int(sub1_idx),
                    'sub2_community_idx': int(sub2_idx),
                    'sub1_sample': sub1_sample,
                    'sub2_sample': sub2_sample,
                    'sub1_species': sorted([int(x) for x in sub1_species]),
                    'sub1_num_species': len(sub1_species),
                    'sub2_species': sorted([int(x) for x in sub2_species]),
                    'sub2_num_species': len(sub2_species),
                    'combined_sub_species': sorted([int(x) for x in combined_sub_species]),
                    'combined_sub_num_species': len(combined_sub_species),
                    'species_pool_overlap': sorted([int(x) for x in overlap]),
                    'overlap_fraction': float(overlap_fraction)
                }
                results['pairs'][medium_name]['12_vs_6+6'].append(pair)
                pair_count += 1

        print(f"Total 12 vs 6+6 pairs: {pair_count}")

        # ======================================================================
        # PART 2: Pool 24 (Parent) vs 12+12 (Coalesced)
        # ======================================================================
        print(f"\n--- Pool Size 24 (Parent) vs 12+12 (Coalesced) ---")

        # Get ALL parent communities with pool size 24 in this medium
        parent_24_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'S') &
            (Metadata['CommunityIDX'] > 18) &
            (Metadata['CommunityIDX'] <= 30)
        ]

        # Get ALL coalesced communities from pool size 12 (12+12) in this medium
        coalesced_12_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'C') &
            (Metadata['CommunityIDX'] > 14) &
            (Metadata['CommunityIDX'] <= 41)
        ]

        print(f"Parent pool-24 communities: {len(parent_24_communities)} samples")
        print(f"  Community IDs: {sorted(parent_24_communities['CommunityIDX'].unique())}")
        print(f"Coalesced 12+12 communities: {len(coalesced_12_communities)} samples")
        print(f"  Community IDs: {sorted(coalesced_12_communities['CommunityIDX'].unique())}")

        # Create all pairwise comparisons
        pair_count = 0
        for _, parent_row in parent_24_communities.iterrows():
            parent_idx = parent_row['CommunityIDX']
            parent_sample = parent_row['SampleIDX']

            # Get parent abundance
            parent_abundance = getAbundance(processed_sequences, parent_sample)
            if parent_abundance is None:
                continue
            parent_abundance = np.array(parent_abundance, dtype=float)
            if parent_abundance.sum() > 0:
                parent_abundance = parent_abundance / parent_abundance.sum()
            parent_species = set(np.where(parent_abundance > 0.001)[0])

            for _, coal_row in coalesced_12_communities.iterrows():
                coal_idx = coal_row['CommunityIDX']
                coal_sample = coal_row['SampleIDX']

                # Get sub-communities
                recipe_row = Coalescence_recipe[Coalescence_recipe['CommunityIDX_Coal'] == coal_idx]
                if recipe_row.empty:
                    continue

                sub1_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub1'])
                sub2_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub2'])

                # Get sub community samples
                sub1_sample_rows = Metadata[
                    (Metadata['CommunityIDX'] == sub1_idx) &
                    (Metadata['Timepoint'] == 'F') &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Medium'] == medium)
                ]['SampleIDX'].values

                sub2_sample_rows = Metadata[
                    (Metadata['CommunityIDX'] == sub2_idx) &
                    (Metadata['Timepoint'] == 'F') &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Medium'] == medium)
                ]['SampleIDX'].values

                if len(sub1_sample_rows) == 0 or len(sub2_sample_rows) == 0:
                    continue

                sub1_sample = sub1_sample_rows[0]
                sub2_sample = sub2_sample_rows[0]

                # Get abundances
                sub1_abundance = getAbundance(processed_sequences, sub1_sample)
                sub2_abundance = getAbundance(processed_sequences, sub2_sample)
                coal_abundance = getAbundance(processed_sequences, coal_sample)

                if sub1_abundance is None or sub2_abundance is None or coal_abundance is None:
                    continue

                sub1_abundance = np.array(sub1_abundance, dtype=float)
                sub2_abundance = np.array(sub2_abundance, dtype=float)
                coal_abundance = np.array(coal_abundance, dtype=float)

                if sub1_abundance.sum() > 0:
                    sub1_abundance = sub1_abundance / sub1_abundance.sum()
                if sub2_abundance.sum() > 0:
                    sub2_abundance = sub2_abundance / sub2_abundance.sum()
                if coal_abundance.sum() > 0:
                    coal_abundance = coal_abundance / coal_abundance.sum()

                sub1_species = set(np.where(sub1_abundance > 0.001)[0])
                sub2_species = set(np.where(sub2_abundance > 0.001)[0])
                coal_species = set(np.where(coal_abundance > 0.001)[0])
                combined_sub_species = sub1_species.union(sub2_species)

                # Calculate overlap (for reference, not filtering)
                overlap = parent_species.intersection(combined_sub_species)
                if len(parent_species.union(combined_sub_species)) > 0:
                    overlap_fraction = len(overlap) / len(parent_species.union(combined_sub_species))
                else:
                    overlap_fraction = 0.0

                # Store the pair (ALL pairs, no filtering by overlap)
                pair = {
                    'parent_community_idx': int(parent_idx),
                    'parent_pool_size': 24,
                    'parent_sample': parent_sample,
                    'parent_species': sorted([int(x) for x in parent_species]),
                    'parent_num_species': len(parent_species),
                    'coalesced_community_idx': int(coal_idx),
                    'coalesced_pool_size': 12,  # each parent
                    'coalesced_sample': coal_sample,
                    'coalesced_species': sorted([int(x) for x in coal_species]),
                    'coalesced_num_species': len(coal_species),
                    'sub1_community_idx': int(sub1_idx),
                    'sub2_community_idx': int(sub2_idx),
                    'sub1_sample': sub1_sample,
                    'sub2_sample': sub2_sample,
                    'sub1_species': sorted([int(x) for x in sub1_species]),
                    'sub1_num_species': len(sub1_species),
                    'sub2_species': sorted([int(x) for x in sub2_species]),
                    'sub2_num_species': len(sub2_species),
                    'combined_sub_species': sorted([int(x) for x in combined_sub_species]),
                    'combined_sub_num_species': len(combined_sub_species),
                    'species_pool_overlap': sorted([int(x) for x in overlap]),
                    'overlap_fraction': float(overlap_fraction)
                }
                results['pairs'][medium_name]['24_vs_12+12'].append(pair)
                pair_count += 1

        print(f"Total 24 vs 12+12 pairs: {pair_count}")

    return results

def save_results(results, output_path='Figure/Assembly_effect/all_assembly_pairs.pkl'):
    """Save results to a pickle file."""
    import pickle
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(results, f)
    print(f"\nResults saved to: {output_path}")

def print_summary(results):
    """Print a summary of all pairs."""
    print("\n" + "="*80)
    print("SUMMARY OF ALL ASSEMBLY EFFECT PAIRS")
    print("="*80)

    total_pairs = 0

    for medium, comparisons in results['pairs'].items():
        print(f"\n{medium} Medium:")
        for comparison_type, pairs in comparisons.items():
            print(f"  {comparison_type}: {len(pairs)} pairs")
            total_pairs += len(pairs)

    print(f"\nTOTAL PAIRS: {total_pairs}")

if __name__ == '__main__':
    print("="*80)
    print("Assembly Effect Analysis - ALL Pairs Identification")
    print("="*80)
    print("\nThis analysis identifies ALL pairs for assembly effect comparison:")
    print("  1. Parent pool-12 vs ALL coalesced 6+6 (same medium)")
    print("  2. Parent pool-24 vs ALL coalesced 12+12 (same medium)")
    print("\nNo filtering by species overlap - that's an outcome to measure!\n")

    # Identify all pairs
    results = identify_all_assembly_pairs()

    # Print summary
    print_summary(results)

    # Save results
    save_results(results)

    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)
