"""
Analyze why the mean×variance heatmaps show stochastic/noisy patterns
"""

import numpy as np
import json
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_setup import metric_VectorDecomposition_onlyPositive

# Load data
data_file = "Simulation_Data/mean_std_grid_100reps/Community_mean_std_grid_100reps.json"
print("="*70)
print("ANALYZING HEATMAP NOISE/STOCHASTICITY")
print("="*70)

with open(data_file, 'r') as f:
    data = json.load(f)

# Grid parameters
mean_values = np.arange(0.1, 1.21, 0.1)
std_values = np.arange(0.1, 0.61, 0.1)

print(f"\nGrid: {len(mean_values)} means × {len(std_values)} stds = {len(mean_values) * len(std_values)} combinations")
print(f"Mean values: {mean_values}")
print(f"Std values: {std_values}")

# Analyze a few specific points
print("\n" + "="*70)
print("ANALYZING SPECIFIC GRID POINTS")
print("="*70)

test_points = [
    (0.3, 0.1),  # Low mean, low std
    (0.3, 0.6),  # Low mean, high std
    (1.0, 0.1),  # High mean, low std
    (1.0, 0.6),  # High mean, high std
]

for mean, std in test_points:
    key = f"mean{mean:.2f}_std{std:.2f}"

    if key not in data:
        continue

    print(f"\n{'='*70}")
    print(f"Point: mean={mean:.2f}, std={std:.2f}")
    print(f"{'='*70}")

    # Count outcomes for this point
    dom_count = 0
    mix_count = 0
    res_count = 0
    total_count = 0

    # Also track variability across reps
    rep_outcomes = []

    for rep_key, rep_data in data[key].items():
        if not rep_key.startswith('rep_'):
            continue

        rep_dom = 0
        rep_mix = 0
        rep_res = 0

        sc_list = rep_data['sc_list']
        cc_list = rep_data['cc_list']

        for cc_key, cc_final in cc_list.items():
            parts = cc_key.split('_')
            c1_key = parts[0]
            c2_key = parts[1]

            c1_final = sc_list[c1_key]
            c2_final = sc_list[c2_key]

            try:
                x1, x2, x3 = metric_VectorDecomposition_onlyPositive(
                    c1_final, c2_final, cc_final
                )

                if x1 > 0.7 or x2 > 0.7:
                    dom_count += 1
                    rep_dom += 1
                elif x3 > 0.7:
                    res_count += 1
                    rep_res += 1
                else:
                    mix_count += 1
                    rep_mix += 1

                total_count += 1
            except:
                pass

        # Store this rep's outcome distribution (6 coalescence events per rep)
        rep_total = rep_dom + rep_mix + rep_res
        if rep_total > 0:
            rep_outcomes.append({
                'dom_frac': rep_dom / rep_total,
                'mix_frac': rep_mix / rep_total,
                'res_frac': rep_res / rep_total
            })

    # Calculate overall fractions
    if total_count > 0:
        dom_frac = dom_count / total_count
        mix_frac = mix_count / total_count
        res_frac = res_count / total_count

        print(f"\nOverall fractions (across all {len(rep_outcomes)} reps):")
        print(f"  Dominance:     {dom_frac:.3f}")
        print(f"  Mixing:        {mix_frac:.3f}")
        print(f"  Restructuring: {res_frac:.3f}")
        print(f"  Total events:  {total_count}")

        # Calculate variability across reps
        if len(rep_outcomes) > 0:
            dom_fracs = [r['dom_frac'] for r in rep_outcomes]
            mix_fracs = [r['mix_frac'] for r in rep_outcomes]
            res_fracs = [r['res_frac'] for r in rep_outcomes]

            print(f"\nVariability across reps (std dev of fractions):")
            print(f"  Dominance std:     {np.std(dom_fracs):.3f}")
            print(f"  Mixing std:        {np.std(mix_fracs):.3f}")
            print(f"  Restructuring std: {np.std(res_fracs):.3f}")

            print(f"\nPer-rep fraction ranges:")
            print(f"  Dominance:     [{min(dom_fracs):.3f}, {max(dom_fracs):.3f}]")
            print(f"  Mixing:        [{min(mix_fracs):.3f}, {max(mix_fracs):.3f}]")
            print(f"  Restructuring: [{min(res_fracs):.3f}, {max(res_fracs):.3f}]")

# Now analyze neighboring points to see if they're truly different or just noise
print("\n" + "="*70)
print("COMPARING NEIGHBORING GRID POINTS")
print("="*70)

# Compare points at same std, different means
print("\nAt std=0.3, comparing different means:")
std_fixed = 0.3
for i in range(len(mean_values)-1):
    mean1 = mean_values[i]
    mean2 = mean_values[i+1]

    key1 = f"mean{mean1:.2f}_std{std_fixed:.2f}"
    key2 = f"mean{mean2:.2f}_std{std_fixed:.2f}"

    if key1 not in data or key2 not in data:
        continue

    # Calculate fractions for both points
    fractions = []
    for key in [key1, key2]:
        dom = 0
        mix = 0
        res = 0
        total = 0

        for rep_key, rep_data in data[key].items():
            if not rep_key.startswith('rep_'):
                continue

            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            for cc_key, cc_final in cc_list.items():
                parts = cc_key.split('_')
                c1_key = parts[0]
                c2_key = parts[1]

                c1_final = sc_list[c1_key]
                c2_final = sc_list[c2_key]

                try:
                    x1, x2, x3 = metric_VectorDecomposition_onlyPositive(
                        c1_final, c2_final, cc_final
                    )

                    if x1 > 0.7 or x2 > 0.7:
                        dom += 1
                    elif x3 > 0.7:
                        res += 1
                    else:
                        mix += 1

                    total += 1
                except:
                    pass

        if total > 0:
            fractions.append((dom/total, mix/total, res/total))
        else:
            fractions.append((0, 0, 0))

    if len(fractions) == 2:
        diff_dom = abs(fractions[1][0] - fractions[0][0])
        diff_mix = abs(fractions[1][1] - fractions[0][1])
        diff_res = abs(fractions[1][2] - fractions[0][2])

        print(f"  mean {mean1:.2f} → {mean2:.2f}: Δdom={diff_dom:.3f}, Δmix={diff_mix:.3f}, Δres={diff_res:.3f}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
Potential reasons for stochastic/noisy heatmaps:

1. **High intrinsic stochasticity**: Each grid point has ~600 coalescence events
   (100 reps × 6 pairwise combinations). If outcomes are highly variable even
   with the same interaction matrix, we'll see noise.

2. **Different interaction matrices per rep**: Each rep generates a NEW random
   interaction matrix from the distribution. So we're averaging over different
   realizations of the interaction matrix, not just different initial conditions.

3. **Insufficient averaging**: 100 reps × 6 coalescence events = ~600 events per
   grid point. This might not be enough to smooth out the noise if the system
   is highly sensitive to the specific interaction matrix realization.

4. **Sensitive dynamics**: Small differences in interaction strengths may lead to
   qualitatively different outcomes (dominance vs mixing vs restructuring).

5. **Threshold effects**: The classification uses thresholds (x1>0.7, etc.), so
   outcomes near boundaries can flip randomly.
""")
