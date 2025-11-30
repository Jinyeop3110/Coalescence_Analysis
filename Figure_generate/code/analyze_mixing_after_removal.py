#!/usr/bin/env python3
"""
Analyze how many coalescence pairs remain as mixtures after removing dominant taxa
"""

import numpy as np
import pandas as pd
from common_setup import *

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

def metric_VectorDecomposition_onlyPositive(u,v,m):
    u=normalize(u)
    v=normalize(v)
    m=normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    e12=np.matmul(np.linalg.inv(A),np.array([np.sum(m*u), np.sum(m*v)]))

    x1=(e12[0])*(e12[0]>0)
    x2=(e12[1])*(e12[1]>0)
    x3=np.linalg.norm(m-(e12[0]*u)-(e12[1]*v))
    convert=np.sqrt((1-x3**2)/(x1**2+x2**2))

    return convert*x1, convert*x2, x3

print("="*80)
print("ANALYZING MIXING STRENGTH BEFORE AND AFTER DOMINANT TAXA REMOVAL")
print("="*80)

# Track statistics for each medium
results_by_medium = {}

for medium in ['L', 'M', 'H']:
    print(f"\n{'='*80}")
    print(f"MEDIUM: {medium}N")
    print(f"{'='*80}")

    total_events = 0
    mixing_before_removal = 0
    mixing_after_removal = 0
    restructuring_before = 0
    restructuring_after = 0

    mixing_lost = 0  # Was mixing before, not after
    mixing_gained = 0  # Was not mixing before, but is after
    mixing_maintained = 0  # Mixing both before and after

    before_mixing_strengths = []
    after_mixing_strengths = []

    # Loop through all species pool sizes
    for pool_size in [6, 12, 24]:
        type_name = medium + f'N_{pool_size}'
        IDX_list = Syn_Coal_IDX[type_name]
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
        idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
        idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
        idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])

        # Process each coalescence event
        for i in range(len(idx)):
            c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
            c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
            c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
            c_1 = c_1*(c_1>1e-4)
            c_2 = c_2*(c_2>1e-4)

            # Vector decomposition BEFORE removal
            try:
                u_before, v_before, k_before = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

                if np.isnan(u_before) or np.isnan(v_before) or np.isnan(k_before):
                    continue
                if np.isinf(u_before) or np.isinf(v_before) or np.isinf(k_before):
                    continue

                mixing_strength_before = u_before**2 + v_before**2
                is_mixing_before = mixing_strength_before > 0.66
            except:
                continue

            # Identify most abundant species
            C1_idx = np.argmax(c_1)
            C2_idx = np.argmax(c_2)

            # Remove most abundant species
            c_1_removed = c_1.copy()
            c_2_removed = c_2.copy()
            c_mix_removed = np.array(c_mix.copy())

            c_1_removed[C1_idx] = 0
            c_1_removed[C2_idx] = 0
            c_2_removed[C1_idx] = 0
            c_2_removed[C2_idx] = 0
            c_mix_removed[C1_idx] = 0
            c_mix_removed[C2_idx] = 0

            # Renormalize
            if np.sum(c_1_removed) > 0:
                c_1_removed = c_1_removed / np.sum(c_1_removed)
            if np.sum(c_2_removed) > 0:
                c_2_removed = c_2_removed / np.sum(c_2_removed)
            if np.sum(c_mix_removed) > 0:
                c_mix_removed = c_mix_removed / np.sum(c_mix_removed)

            # Skip if any community becomes empty
            if np.sum(c_1_removed) == 0 or np.sum(c_2_removed) == 0 or np.sum(c_mix_removed) == 0:
                continue

            # Vector decomposition AFTER removal
            try:
                u_after, v_after, k_after = metric_VectorDecomposition_onlyPositive(c_1_removed, c_2_removed, c_mix_removed)

                if np.isnan(u_after) or np.isnan(v_after) or np.isnan(k_after):
                    continue
                if np.isinf(u_after) or np.isinf(v_after) or np.isinf(k_after):
                    continue

                mixing_strength_after = u_after**2 + v_after**2
                is_mixing_after = mixing_strength_after > 0.66
            except:
                continue

            # Count valid events
            total_events += 1
            before_mixing_strengths.append(mixing_strength_before)
            after_mixing_strengths.append(mixing_strength_after)

            if is_mixing_before:
                mixing_before_removal += 1
            else:
                restructuring_before += 1

            if is_mixing_after:
                mixing_after_removal += 1
            else:
                restructuring_after += 1

            # Track transitions
            if is_mixing_before and is_mixing_after:
                mixing_maintained += 1
            elif is_mixing_before and not is_mixing_after:
                mixing_lost += 1
            elif not is_mixing_before and is_mixing_after:
                mixing_gained += 1

    # Store results
    results_by_medium[medium] = {
        'total': total_events,
        'mixing_before': mixing_before_removal,
        'mixing_after': mixing_after_removal,
        'restructuring_before': restructuring_before,
        'restructuring_after': restructuring_after,
        'mixing_maintained': mixing_maintained,
        'mixing_lost': mixing_lost,
        'mixing_gained': mixing_gained,
        'before_strengths': before_mixing_strengths,
        'after_strengths': after_mixing_strengths
    }

    # Print results
    print(f"\nTotal coalescence events processed: {total_events}")
    print(f"\n{'BEFORE Dominant Taxa Removal:':<40}")
    print(f"  Mixing events (u²+v² > 0.66):     {mixing_before_removal:4d} ({mixing_before_removal/total_events*100:5.1f}%)")
    print(f"  Restructuring events (u²+v² ≤ 0.66): {restructuring_before:4d} ({restructuring_before/total_events*100:5.1f}%)")

    print(f"\n{'AFTER Dominant Taxa Removal:':<40}")
    print(f"  Mixing events (u²+v² > 0.66):     {mixing_after_removal:4d} ({mixing_after_removal/total_events*100:5.1f}%)")
    print(f"  Restructuring events (u²+v² ≤ 0.66): {restructuring_after:4d} ({restructuring_after/total_events*100:5.1f}%)")

    print(f"\n{'TRANSITIONS:':<40}")
    print(f"  Mixing → Mixing (maintained):    {mixing_maintained:4d} ({mixing_maintained/total_events*100:5.1f}%)")
    print(f"  Mixing → Restructuring (lost):   {mixing_lost:4d} ({mixing_lost/total_events*100:5.1f}%)")
    print(f"  Restructuring → Mixing (gained): {mixing_gained:4d} ({mixing_gained/total_events*100:5.1f}%)")

    print(f"\n{'MIXING STRENGTH STATISTICS:':<40}")
    print(f"  Before removal - Mean: {np.mean(before_mixing_strengths):.3f}, Median: {np.median(before_mixing_strengths):.3f}")
    print(f"  After removal  - Mean: {np.mean(after_mixing_strengths):.3f}, Median: {np.median(after_mixing_strengths):.3f}")

    # Net change
    net_change = mixing_after_removal - mixing_before_removal
    print(f"\n{'NET CHANGE:':<40}")
    print(f"  Mixing events: {net_change:+4d} ({net_change/total_events*100:+5.1f} percentage points)")

# Summary table
print(f"\n{'='*80}")
print("SUMMARY TABLE")
print(f"{'='*80}")
print(f"\n{'Medium':<10} {'Total':<8} {'Before Mix':<12} {'After Mix':<12} {'Maintained':<12} {'Lost':<8} {'Gained':<8}")
print("-" * 80)

for medium in ['L', 'M', 'H']:
    r = results_by_medium[medium]
    print(f"{medium+'N':<10} {r['total']:<8} {r['mixing_before']:<4} ({r['mixing_before']/r['total']*100:4.1f}%) "
          f"{r['mixing_after']:<4} ({r['mixing_after']/r['total']*100:4.1f}%) "
          f"{r['mixing_maintained']:<4} ({r['mixing_maintained']/r['total']*100:4.1f}%) "
          f"{r['mixing_lost']:<8} {r['mixing_gained']:<8}")

print(f"\n{'='*80}")
print("INTERPRETATION")
print(f"{'='*80}")
print("""
- "Mixing maintained": Events that were mixing before AND after removal
  → Subdominant species also show mixing pattern

- "Mixing lost": Events that were mixing before but became restructuring after removal
  → Dominant species were driving the mixing; subdominants restructured

- "Mixing gained": Events that were restructuring before but became mixing after removal
  → Dominant species were causing restructuring; removing them reveals mixing

The AbundantRemoved plot uses the AFTER removal data (mixing_after_removal events).
This tests whether subdominant species dynamics follow the same patterns as dominant species.
""")
