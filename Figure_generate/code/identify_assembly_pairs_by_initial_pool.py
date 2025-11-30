#!/usr/bin/env python3
"""
Assembly Effect Analysis - Matching by INITIAL Species Pool
============================================================

This script correctly identifies comparable pairs by matching INITIAL species pools.

KEY INSIGHT:
- Each CommunityIDX has a UNIQUE species pool composition
- We infer the initial pool from observed species in parent communities
- For coalesced communities: initial_pool = union of species in Sub1 + Sub2
- We match: Parent pool-N with Coalesced (pool-N/2 + pool-N/2)
  WHERE the initial pools are the SAME (or very similar)

Author: Assembly Effect Analysis (Initial Pool Version)
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

def infer_initial_pool(processed_sequences, sample_id, threshold=0.0001):
    """
    Infer the initial species pool from observed species.
    Uses a very low threshold to catch species that might be rare but present.
    """
    abundance = getAbundance(processed_sequences, sample_id)
    if abundance is None:
        return set()

    abundance = np.array(abundance, dtype=float)
    # Use low threshold to capture initial pool (some species may be rare)
    initial_pool = set(np.where(abundance > threshold)[0])
    return initial_pool

def identify_pairs_by_initial_pool():
    """
    Identify assembly effect pairs by matching initial species pools.

    For each coalesced community:
    1. Infer its initial pool from union of its two parent communities
    2. Find parent communities with similar initial pools
    3. Create pairs for those matches
    """

    mediums = ['L', 'M', 'H']
    results = {
        'metadata': {
            'description': 'Assembly effect pairs - matched by INITIAL species pool',
            'method': 'Initial pool inferred from observed species in parent communities',
            'threshold': '80% Jaccard similarity for initial pools'
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

        # Get all pool-12 parent communities
        parent_12_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'S') &
            (Metadata['CommunityIDX'] > 9) &
            (Metadata['CommunityIDX'] <= 18)
        ]

        # Infer initial pools for all parent-12 communities
        parent_12_pools = {}
        for _, row in parent_12_communities.iterrows():
            comm_idx = row['CommunityIDX']
            sample_id = row['SampleIDX']
            initial_pool = infer_initial_pool(processed_sequences, sample_id)
            parent_12_pools[comm_idx] = {
                'sample_id': sample_id,
                'initial_pool': initial_pool
            }

        print(f"Parent pool-12 communities: {len(parent_12_pools)}")

        # Get all 6+6 coalesced communities
        coalesced_6_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'C') &
            (Metadata['CommunityIDX'] <= 14)
        ]

        print(f"Coalesced 6+6 communities: {len(coalesced_6_communities)}")

        # For each coalesced community, find matching parents
        pair_count = 0
        for _, coal_row in coalesced_6_communities.iterrows():
            coal_idx = coal_row['CommunityIDX']
            coal_sample = coal_row['SampleIDX']

            # Get sub-communities
            recipe_row = Coalescence_recipe[Coalescence_recipe['CommunityIDX_Coal'] == coal_idx]
            if recipe_row.empty:
                continue

            sub1_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub1'])
            sub2_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub2'])

            # Get sub samples
            sub1_samples = Metadata[
                (Metadata['CommunityIDX'] == sub1_idx) &
                (Metadata['Timepoint'] == 'F') &
                (Metadata['CoalescenceType'] == 'S') &
                (Metadata['Medium'] == medium)
            ]['SampleIDX'].values

            sub2_samples = Metadata[
                (Metadata['CommunityIDX'] == sub2_idx) &
                (Metadata['Timepoint'] == 'F') &
                (Metadata['CoalescenceType'] == 'S') &
                (Metadata['Medium'] == medium)
            ]['SampleIDX'].values

            if len(sub1_samples) == 0 or len(sub2_samples) == 0:
                continue

            sub1_sample = sub1_samples[0]
            sub2_sample = sub2_samples[0]

            # Infer initial pools for sub-communities
            sub1_pool = infer_initial_pool(processed_sequences, sub1_sample)
            sub2_pool = infer_initial_pool(processed_sequences, sub2_sample)

            # Combined initial pool for coalesced community
            coalesced_initial_pool = sub1_pool.union(sub2_pool)

            # Find parent communities with similar initial pools
            for parent_idx, parent_data in parent_12_pools.items():
                parent_pool = parent_data['initial_pool']
                parent_sample = parent_data['sample_id']

                # Calculate Jaccard similarity
                intersection = parent_pool.intersection(coalesced_initial_pool)
                union = parent_pool.union(coalesced_initial_pool)

                if len(union) > 0:
                    jaccard = len(intersection) / len(union)
                else:
                    jaccard = 0.0

                # Only include pairs with high similarity (>=80%)
                if jaccard >= 0.8:
                    # Get final compositions for comparison
                    coal_abundance = getAbundance(processed_sequences, coal_sample)
                    parent_abundance = getAbundance(processed_sequences, parent_sample)
                    sub1_abundance = getAbundance(processed_sequences, sub1_sample)
                    sub2_abundance = getAbundance(processed_sequences, sub2_sample)

                    if all(x is not None for x in [coal_abundance, parent_abundance, sub1_abundance, sub2_abundance]):
                        # Get final species (using normal threshold)
                        parent_final = set(np.where(np.array(parent_abundance) > 0.001)[0])
                        coal_final = set(np.where(np.array(coal_abundance) > 0.001)[0])
                        sub1_final = set(np.where(np.array(sub1_abundance) > 0.001)[0])
                        sub2_final = set(np.where(np.array(sub2_abundance) > 0.001)[0])

                        pair = {
                            'parent_community_idx': int(parent_idx),
                            'parent_pool_size': 12,
                            'parent_sample': parent_sample,
                            'parent_initial_pool': sorted([int(x) for x in parent_pool]),
                            'parent_initial_pool_size': len(parent_pool),
                            'parent_final_species': sorted([int(x) for x in parent_final]),
                            'parent_final_diversity': len(parent_final),

                            'coalesced_community_idx': int(coal_idx),
                            'coalesced_pool_size': 6,
                            'coalesced_sample': coal_sample,
                            'coalesced_initial_pool': sorted([int(x) for x in coalesced_initial_pool]),
                            'coalesced_initial_pool_size': len(coalesced_initial_pool),
                            'coalesced_final_species': sorted([int(x) for x in coal_final]),
                            'coalesced_final_diversity': len(coal_final),

                            'sub1_community_idx': int(sub1_idx),
                            'sub2_community_idx': int(sub2_idx),
                            'sub1_sample': sub1_sample,
                            'sub2_sample': sub2_sample,
                            'sub1_initial_pool': sorted([int(x) for x in sub1_pool]),
                            'sub2_initial_pool': sorted([int(x) for x in sub2_pool]),
                            'sub1_final_species': sorted([int(x) for x in sub1_final]),
                            'sub2_final_species': sorted([int(x) for x in sub2_final]),

                            'initial_pool_jaccard': float(jaccard),
                            'initial_pool_overlap': sorted([int(x) for x in intersection])
                        }

                        results['pairs'][medium_name]['12_vs_6+6'].append(pair)
                        pair_count += 1

        print(f"Total 12 vs 6+6 pairs (with ≥80% initial pool similarity): {pair_count}")

        # ======================================================================
        # PART 2: Pool 24 (Parent) vs 12+12 (Coalesced)
        # ======================================================================
        print(f"\n--- Pool Size 24 (Parent) vs 12+12 (Coalesced) ---")

        # Get all pool-24 parent communities
        parent_24_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'S') &
            (Metadata['CommunityIDX'] > 18) &
            (Metadata['CommunityIDX'] <= 30)
        ]

        # Infer initial pools
        parent_24_pools = {}
        for _, row in parent_24_communities.iterrows():
            comm_idx = row['CommunityIDX']
            sample_id = row['SampleIDX']
            initial_pool = infer_initial_pool(processed_sequences, sample_id)
            parent_24_pools[comm_idx] = {
                'sample_id': sample_id,
                'initial_pool': initial_pool
            }

        print(f"Parent pool-24 communities: {len(parent_24_pools)}")

        # Get all 12+12 coalesced communities
        coalesced_12_communities = Metadata[
            (Metadata['Timepoint'] == 'F') &
            (Metadata['CommunityOrigin'] == 'S') &
            (Metadata['Medium'] == medium) &
            (Metadata['CoalescenceType'] == 'C') &
            (Metadata['CommunityIDX'] > 14) &
            (Metadata['CommunityIDX'] <= 41)
        ]

        print(f"Coalesced 12+12 communities: {len(coalesced_12_communities)}")

        # For each coalesced community, find matching parents
        pair_count = 0
        for _, coal_row in coalesced_12_communities.iterrows():
            coal_idx = coal_row['CommunityIDX']
            coal_sample = coal_row['SampleIDX']

            # Get sub-communities
            recipe_row = Coalescence_recipe[Coalescence_recipe['CommunityIDX_Coal'] == coal_idx]
            if recipe_row.empty:
                continue

            sub1_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub1'])
            sub2_idx = int(recipe_row.iloc[0]['CommunityIDX_Sub2'])

            # Get sub samples
            sub1_samples = Metadata[
                (Metadata['CommunityIDX'] == sub1_idx) &
                (Metadata['Timepoint'] == 'F') &
                (Metadata['CoalescenceType'] == 'S') &
                (Metadata['Medium'] == medium)
            ]['SampleIDX'].values

            sub2_samples = Metadata[
                (Metadata['CommunityIDX'] == sub2_idx) &
                (Metadata['Timepoint'] == 'F') &
                (Metadata['CoalescenceType'] == 'S') &
                (Metadata['Medium'] == medium)
            ]['SampleIDX'].values

            if len(sub1_samples) == 0 or len(sub2_samples) == 0:
                continue

            sub1_sample = sub1_samples[0]
            sub2_sample = sub2_samples[0]

            # Infer initial pools
            sub1_pool = infer_initial_pool(processed_sequences, sub1_sample)
            sub2_pool = infer_initial_pool(processed_sequences, sub2_sample)
            coalesced_initial_pool = sub1_pool.union(sub2_pool)

            # Find parent communities with similar initial pools
            for parent_idx, parent_data in parent_24_pools.items():
                parent_pool = parent_data['initial_pool']
                parent_sample = parent_data['sample_id']

                # Calculate Jaccard similarity
                intersection = parent_pool.intersection(coalesced_initial_pool)
                union = parent_pool.union(coalesced_initial_pool)

                if len(union) > 0:
                    jaccard = len(intersection) / len(union)
                else:
                    jaccard = 0.0

                # Only include pairs with high similarity (>=80%)
                if jaccard >= 0.8:
                    # Get final compositions
                    coal_abundance = getAbundance(processed_sequences, coal_sample)
                    parent_abundance = getAbundance(processed_sequences, parent_sample)
                    sub1_abundance = getAbundance(processed_sequences, sub1_sample)
                    sub2_abundance = getAbundance(processed_sequences, sub2_sample)

                    if all(x is not None for x in [coal_abundance, parent_abundance, sub1_abundance, sub2_abundance]):
                        parent_final = set(np.where(np.array(parent_abundance) > 0.001)[0])
                        coal_final = set(np.where(np.array(coal_abundance) > 0.001)[0])
                        sub1_final = set(np.where(np.array(sub1_abundance) > 0.001)[0])
                        sub2_final = set(np.where(np.array(sub2_abundance) > 0.001)[0])

                        pair = {
                            'parent_community_idx': int(parent_idx),
                            'parent_pool_size': 24,
                            'parent_sample': parent_sample,
                            'parent_initial_pool': sorted([int(x) for x in parent_pool]),
                            'parent_initial_pool_size': len(parent_pool),
                            'parent_final_species': sorted([int(x) for x in parent_final]),
                            'parent_final_diversity': len(parent_final),

                            'coalesced_community_idx': int(coal_idx),
                            'coalesced_pool_size': 12,
                            'coalesced_sample': coal_sample,
                            'coalesced_initial_pool': sorted([int(x) for x in coalesced_initial_pool]),
                            'coalesced_initial_pool_size': len(coalesced_initial_pool),
                            'coalesced_final_species': sorted([int(x) for x in coal_final]),
                            'coalesced_final_diversity': len(coal_final),

                            'sub1_community_idx': int(sub1_idx),
                            'sub2_community_idx': int(sub2_idx),
                            'sub1_sample': sub1_sample,
                            'sub2_sample': sub2_sample,
                            'sub1_initial_pool': sorted([int(x) for x in sub1_pool]),
                            'sub2_initial_pool': sorted([int(x) for x in sub2_pool]),
                            'sub1_final_species': sorted([int(x) for x in sub1_final]),
                            'sub2_final_species': sorted([int(x) for x in sub2_final]),

                            'initial_pool_jaccard': float(jaccard),
                            'initial_pool_overlap': sorted([int(x) for x in intersection])
                        }

                        results['pairs'][medium_name]['24_vs_12+12'].append(pair)
                        pair_count += 1

        print(f"Total 24 vs 12+12 pairs (with ≥80% initial pool similarity): {pair_count}")

    return results

def save_results(results, output_path='Figure/Assembly_effect/assembly_pairs_initial_pool.pkl'):
    """Save results to pickle file."""
    import pickle
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(results, f)
    print(f"\nResults saved to: {output_path}")

def print_summary(results):
    """Print summary."""
    print("\n" + "="*80)
    print("SUMMARY - Pairs Matched by INITIAL Species Pool")
    print("="*80)

    total_pairs = 0
    for medium, comparisons in results['pairs'].items():
        print(f"\n{medium}:")
        for comp_type, pairs in comparisons.items():
            print(f"  {comp_type}: {len(pairs)} pairs")
            total_pairs += len(pairs)

    print(f"\nTOTAL PAIRS: {total_pairs}")

if __name__ == '__main__':
    print("="*80)
    print("Assembly Effect Analysis - Matching by INITIAL Species Pool")
    print("="*80)
    print("\nThis analysis identifies pairs where the INITIAL species pools match:")
    print("  - Initial pool for parent: inferred from observed species")
    print("  - Initial pool for coalesced: union of its two parent communities")
    print("  - Pairs must have ≥80% Jaccard similarity in initial pools\n")

    results = identify_pairs_by_initial_pool()
    print_summary(results)
    save_results(results)

    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)
