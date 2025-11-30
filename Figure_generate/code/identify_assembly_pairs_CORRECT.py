#!/usr/bin/env python3
"""
Assembly Effect Analysis - CORRECT Matching (Manual Design)
============================================================

This script uses the ACTUAL designed pairs from the experiment.

The user has provided the correct matching based on experimental design:
- Parent communities 19-30 (pool-24) each have a corresponding coalesced community
- The coalesced community was formed from two pool-12 communities that together
  contain the SAME initial species pool as the parent

This is the CORRECT approach for assembly effect analysis!

Author: Assembly Effect Analysis (Correct Design)
Date: 2025
"""

import os
import sys
import numpy as np
import pandas as pd
import pickle
import builtins  # Need this because pylab imports numpy's any() which behaves differently

# Add path for imports
sys.path.append('.')
from common_setup import *

# Fixed version of getAbundance that works for index 0
def getAbundance_fixed(Processed_sequences, IDX):
    """
    Fixed version of getAbundance that correctly handles samples at index 0.
    Original getAbundance has a bug: `if not any(SampleIdx)` returns True when SampleIdx=[0]
    """
    SampleIdx = np.flatnonzero([x == IDX for x in Processed_sequences['SampleIDX']])
    if len(SampleIdx) == 0:  # Fixed: use len() instead of any()
        return None
    else:
        O = Processed_sequences.iloc[SampleIdx[0]].values.tolist()[1:]
        return O

# MANUAL MATCHING FROM EXPERIMENTAL DESIGN

# Pool-24 Parent → Coalesced (from 12+12)
DESIGNED_PAIRS_24 = {
    19: 24,  # Parent 19 ↔ Coalesced 24
    20: 39,  # Parent 20 ↔ Coalesced 39
    21: 15,  # Parent 21 ↔ Coalesced 15
    22: 37,  # Parent 22 ↔ Coalesced 37
    23: 18,  # Parent 23 ↔ Coalesced 18
    24: 34,  # Parent 24 ↔ Coalesced 34
    25: 30,  # Parent 25 ↔ Coalesced 30
    26: 22,  # Parent 26 ↔ Coalesced 22
    27: 28,  # Parent 27 ↔ Coalesced 28
    28: 25,  # Parent 28 ↔ Coalesced 25
    29: 41,  # Parent 29 ↔ Coalesced 41
    30: 32,  # Parent 30 ↔ Coalesced 32
}

# Pool-12 Parent → Coalesced (from 6+6)
DESIGNED_PAIRS_12 = {
    10: 2,   # Parent 10 ↔ Coalesced 2
    11: 6,   # Parent 11 ↔ Coalesced 6
    12: 11,  # Parent 12 ↔ Coalesced 11
    13: 9,   # Parent 13 ↔ Coalesced 9
    14: 12,  # Parent 14 ↔ Coalesced 12
    15: 10,  # Parent 15 ↔ Coalesced 10
    16: 1,   # Parent 16 ↔ Coalesced 1 (CORRECTED)
    17: 14,  # Parent 17 ↔ Coalesced 14 (CORRECTED)
    18: 5,   # Parent 18 ↔ Coalesced 5 (CORRECTED)
}

def identify_correct_assembly_pairs():
    """
    Identify assembly effect pairs using the correct experimental design.

    Returns pairs organized by medium and comparison type:
    - 12_vs_6+6: Pool-12 parents vs 6+6 coalesced
    - 24_vs_12+12: Pool-24 parents vs 12+12 coalesced
    """

    mediums = ['L', 'M', 'H']
    results = {
        'metadata': {
            'description': 'Assembly effect pairs - CORRECT experimental design',
            'method': 'Manual matching based on designed species pools',
            'total_pairs_12': len(DESIGNED_PAIRS_12),
            'total_pairs_24': len(DESIGNED_PAIRS_24)
        },
        'design': {
            '12_vs_6+6': {
                'parent_communities': list(DESIGNED_PAIRS_12.keys()),
                'coalesced_communities': list(DESIGNED_PAIRS_12.values()),
                'matching': DESIGNED_PAIRS_12
            },
            '24_vs_12+12': {
                'parent_communities': list(DESIGNED_PAIRS_24.keys()),
                'coalesced_communities': list(DESIGNED_PAIRS_24.values()),
                'matching': DESIGNED_PAIRS_24
            }
        },
        'pairs': {}
    }

    # Combine processed sequences
    processed_sequences = pd.concat([
        Processed_sequences_synthetic,
        Processed_sequences_natural
    ], ignore_index=True)

    # Use Coalescence_data for finding sub-community sample IDs
    # (Don't use Coalescence_recipe!)

    for medium in mediums:
        medium_name = medium + 'N'
        results['pairs'][medium_name] = {
            '12_vs_6+6': [],
            '24_vs_12+12': []
        }

        print(f"\n{'='*80}")
        print(f"Medium: {medium_name}")
        print(f"{'='*80}")

        # Process both comparison types
        for comparison_type, designed_pairs, pool_size in [
            ('12_vs_6+6', DESIGNED_PAIRS_12, 12),
            ('24_vs_12+12', DESIGNED_PAIRS_24, 24)
        ]:
            print(f"\n--- {comparison_type} ---")
            pair_count = 0

            # For each designed pair
            for parent_idx, coal_idx in designed_pairs.items():
                print(f"    Processing: Parent {parent_idx} ↔ Coalesced {coal_idx}")

                # Get parent community samples
                parent_samples = Metadata[
                    (Metadata['CommunityIDX'] == parent_idx) &
                    (Metadata['Medium'] == medium) &
                    (Metadata['CoalescenceType'] == 'S') &
                    (Metadata['Timepoint'] == 'F')
                ]

                # Get coalesced community samples
                coal_samples = Metadata[
                    (Metadata['CommunityIDX'] == coal_idx) &
                    (Metadata['Medium'] == medium) &
                    (Metadata['CoalescenceType'] == 'C') &
                    (Metadata['Timepoint'] == 'F')
                ]

                if len(parent_samples) == 0 or len(coal_samples) == 0:
                    print(f"      Skipping: parent={len(parent_samples)}, coal={len(coal_samples)} samples")
                    continue
                print(f"      Found: parent={len(parent_samples)}, coal={len(coal_samples)} samples")

                print(f"      Creating pairs: {len(parent_samples)} x {len(coal_samples)} = {len(parent_samples) * len(coal_samples)} potential pairs")

                # Create pairs for all replicates
                for _, parent_row in parent_samples.iterrows():
                    for _, coal_row in coal_samples.iterrows():

                        parent_sample = parent_row['SampleIDX']
                        coal_sample = coal_row['SampleIDX']

                        # Get sub-community sample IDs from Coalescence_data
                        coal_data_row = Coalescence_data[
                            (Coalescence_data['SampleIDX'] == coal_sample)
                        ]

                        if coal_data_row.empty:
                            print(f"        Skipping: coal_sample {coal_sample} not in Coalescence_data")
                            continue

                        sub1_sample = coal_data_row.iloc[0]['SampleIDX_Sub1']
                        sub2_sample = coal_data_row.iloc[0]['SampleIDX_Sub2']

                        # Get sub-community CommunityIDX from Metadata
                        sub1_meta = Metadata[Metadata['SampleIDX'] == sub1_sample]
                        sub2_meta = Metadata[Metadata['SampleIDX'] == sub2_sample]

                        if sub1_meta.empty or sub2_meta.empty:
                            print(f"        Skipping: sub-community not found in Metadata (sub1={len(sub1_meta)}, sub2={len(sub2_meta)})")
                            continue

                        sub1_idx = sub1_meta.iloc[0]['CommunityIDX']
                        sub2_idx = sub2_meta.iloc[0]['CommunityIDX']

                        print(f"        Samples: P={parent_sample}, C={coal_sample}, S1={sub1_sample}(CC{sub1_idx}), S2={sub2_sample}(CC{sub2_idx})")

                        # Get abundances
                        parent_abundance = getAbundance_fixed(processed_sequences, parent_sample)
                        coal_abundance = getAbundance_fixed(processed_sequences, coal_sample)
                        sub1_abundance = getAbundance_fixed(processed_sequences, sub1_sample)
                        sub2_abundance = getAbundance_fixed(processed_sequences, sub2_sample)

                        # Check if any abundance is None (use builtin any, not numpy's)
                        if builtins.any(x is None for x in [parent_abundance, coal_abundance, sub1_abundance, sub2_abundance]):
                            print(f"        Skipping pair due to None abundance")
                            continue

                        # Convert to arrays, replacing non-numeric values with 0
                        def convert_to_numeric_array(data):
                            """Convert data to numeric array, replacing non-numeric values with 0."""
                            arr = []
                            for val in data:
                                try:
                                    arr.append(float(val))
                                except (ValueError, TypeError):
                                    arr.append(0.0)
                            return np.array(arr)

                        parent_abundance = convert_to_numeric_array(parent_abundance)
                        coal_abundance = convert_to_numeric_array(coal_abundance)
                        sub1_abundance = convert_to_numeric_array(sub1_abundance)
                        sub2_abundance = convert_to_numeric_array(sub2_abundance)

                        # Normalize
                        if parent_abundance.sum() > 0:
                            parent_abundance = parent_abundance / parent_abundance.sum()
                        if coal_abundance.sum() > 0:
                            coal_abundance = coal_abundance / coal_abundance.sum()
                        if sub1_abundance.sum() > 0:
                            sub1_abundance = sub1_abundance / sub1_abundance.sum()
                        if sub2_abundance.sum() > 0:
                            sub2_abundance = sub2_abundance / sub2_abundance.sum()

                        # Get species lists (using standard threshold)
                        threshold = 0.001
                        parent_species = set(np.where(parent_abundance > threshold)[0])
                        coal_species = set(np.where(coal_abundance > threshold)[0])
                        sub1_species = set(np.where(sub1_abundance > threshold)[0])
                        sub2_species = set(np.where(sub2_abundance > threshold)[0])
                        combined_sub_species = sub1_species.union(sub2_species)

                        # Store pair
                        pair = {
                            'parent_community_idx': int(parent_idx),
                            'parent_pool_size': pool_size,
                            'parent_sample': parent_sample,
                            'parent_replicate': int(parent_row['Replicate']) if 'Replicate' in parent_row else None,
                            'parent_final_species': sorted([int(x) for x in parent_species]),
                            'parent_final_diversity': len(parent_species),
                            'parent_abundances': parent_abundance.tolist(),

                            'coalesced_community_idx': int(coal_idx),
                            'coalesced_pool_size': pool_size // 2,  # each parent pool size
                            'coalesced_sample': coal_sample,
                            'coalesced_replicate': int(coal_row['Replicate']) if 'Replicate' in coal_row else None,
                            'coalesced_final_species': sorted([int(x) for x in coal_species]),
                            'coalesced_final_diversity': len(coal_species),
                            'coalesced_abundances': coal_abundance.tolist(),

                            'sub1_community_idx': int(sub1_idx),
                            'sub2_community_idx': int(sub2_idx),
                            'sub1_sample': sub1_sample,
                            'sub2_sample': sub2_sample,
                            'sub1_final_species': sorted([int(x) for x in sub1_species]),
                            'sub2_final_species': sorted([int(x) for x in sub2_species]),
                            'sub1_final_diversity': len(sub1_species),
                            'sub2_final_diversity': len(sub2_species),
                            'sub1_abundances': sub1_abundance.tolist(),
                            'sub2_abundances': sub2_abundance.tolist(),
                            'combined_sub_species': sorted([int(x) for x in combined_sub_species]),
                            'combined_sub_diversity': len(combined_sub_species),

                            # Assembly effect metrics
                            'diversity_difference': len(parent_species) - len(coal_species),
                            'species_overlap': sorted([int(x) for x in parent_species.intersection(coal_species)]),
                            'species_only_in_parent': sorted([int(x) for x in parent_species - coal_species]),
                            'species_only_in_coalesced': sorted([int(x) for x in coal_species - parent_species]),
                        }

                        results['pairs'][medium_name][comparison_type].append(pair)
                        pair_count += 1

            print(f"Total {comparison_type} pairs: {pair_count}")

    return results

def save_results(results, output_path='Figure/Assembly_effect/assembly_pairs_CORRECT.pkl'):
    """Save results to pickle file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump(results, f)
    print(f"\nResults saved to: {output_path}")

def print_summary(results):
    """Print summary."""
    print("\n" + "="*80)
    print("SUMMARY - CORRECT Assembly Effect Pairs")
    print("="*80)

    total_pairs = sum(len(pairs) for medium_data in results['pairs'].values()
                     for pairs in medium_data.values())
    print(f"\nTotal pairs across all media: {total_pairs}")

    for medium, comparisons in results['pairs'].items():
        print(f"\n{medium}:")

        for comp_type, pairs in comparisons.items():
            print(f"\n  {comp_type}:")
            print(f"    Pairs: {len(pairs)}")

            if len(pairs) > 0:
                parent_divs = [p['parent_final_diversity'] for p in pairs]
                coal_divs = [p['coalesced_final_diversity'] for p in pairs]
                diffs = [p['diversity_difference'] for p in pairs]

                print(f"    Parent diversity: {np.mean(parent_divs):.1f} ± {np.std(parent_divs):.1f}")
                print(f"    Coalesced diversity: {np.mean(coal_divs):.1f} ± {np.std(coal_divs):.1f}")
                print(f"    Mean difference: {np.mean(diffs):.1f} ± {np.std(diffs):.1f}")

if __name__ == '__main__':
    print("="*80)
    print("Assembly Effect Analysis - CORRECT Experimental Design")
    print("="*80)
    print(f"\nUsing designed pairs from experimental documentation:")
    print(f"  Pool-12 vs 6+6: {len(DESIGNED_PAIRS_12)} pairs (parents 10-18)")
    print(f"  Pool-24 vs 12+12: {len(DESIGNED_PAIRS_24)} pairs (parents 19-30)")
    print(f"  Total designed pairs: {len(DESIGNED_PAIRS_12) + len(DESIGNED_PAIRS_24)}")
    print("\nEach parent shares the SAME initial species pool as its")
    print("corresponding coalesced community's two parent communities.\n")

    results = identify_correct_assembly_pairs()
    print_summary(results)
    save_results(results)

    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)
