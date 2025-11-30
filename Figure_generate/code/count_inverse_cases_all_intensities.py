#!/usr/bin/env python3
"""
Count inverse vs non-inverse cases across all intensities
"""

import json
import numpy as np

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

def calculate_lv_equilibrium_dominance(alpha_12, alpha_21):
    """Calculate species-level dominance using CORRECTED Lotka-Volterra equilibrium."""

    # Case 1: Both alphas > 1 - competitive exclusion
    if alpha_12 > 1.0 and alpha_21 > 1.0:
        return 0.5

    # Case 2: alpha_12 > 1 and alpha_21 < 1 - species 2 wins (CORRECTED)
    elif alpha_12 > 1.0 and alpha_21 < 1.0:
        return 0.0

    # Case 3: alpha_12 < 1 and alpha_21 > 1 - species 1 wins (CORRECTED)
    elif alpha_12 < 1.0 and alpha_21 > 1.0:
        return 1.0

    # Case 4a: Both alphas < 1 AND sum < 2 - stable coexistence
    elif alpha_12 < 1.0 and alpha_21 < 1.0:
        if alpha_12 + alpha_21 < 2.0:
            denominator = 2 - alpha_12 - alpha_21
            if abs(denominator) < 1e-10:
                return 0.5
            return (1 - alpha_12) / denominator
        else:
            # Case 4b: Bistability
            return 0.5
    else:
        return 0.5

def analyze_intensity(data, intensity_key):
    """Analyze inverse cases for a given intensity."""

    intensity_data = data[intensity_key]

    inverse_cases = []
    non_inverse_cases = []
    exclusion_cases = []
    coexistence_cases = []
    bistability_cases = []
    both_alpha_gt_1_filtered = 0

    total_processed = 0

    for rep_key in intensity_data.keys():
        rep_data = intensity_data[rep_key]
        rep_interaction_matrix = np.array(rep_data['parameters']['interaction_matrix'])
        sc_list = rep_data['sc_list']
        cc_list = rep_data['cc_list']

        communities = {}
        most_abundant_indices = {}

        for comm_key in sorted(sc_list.keys()):
            community = np.array(sc_list[comm_key])
            communities[comm_key] = community
            most_abundant_indices[comm_key] = np.argmax(community)

        comm_keys = sorted(sc_list.keys())

        for i in range(len(comm_keys)):
            for j in range(i+1, len(comm_keys)):
                coal_key = f"{comm_keys[i]}_{comm_keys[j]}"
                if coal_key not in cc_list:
                    continue

                c_mix = np.array(cc_list[coal_key])
                c_1 = np.array(communities[comm_keys[i]])
                c_2 = np.array(communities[comm_keys[j]])

                # Normalize
                c_mix = c_mix / (np.sum(c_mix) + 1e-8)
                c_1 = c_1 / (np.sum(c_1) + 1e-8)
                c_2 = c_2 / (np.sum(c_2) + 1e-8)

                # Apply threshold
                c_1_thresh = c_1 * (c_1 > 1e-4)
                c_2_thresh = c_2 * (c_2 > 1e-4)

                if np.sum(c_1_thresh) == 0 or np.sum(c_2_thresh) == 0:
                    continue

                # Vector decomposition
                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

                    if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                        continue

                    mixing_strength = u**2 + v**2
                    if mixing_strength <= 0.66:
                        continue

                    community_dominance = np.arctan(u / (v + 1e-8)) / (np.pi / 2)

                    if np.isnan(community_dominance) or np.isinf(community_dominance):
                        continue
                except:
                    continue

                # Get species
                C1 = most_abundant_indices[comm_keys[i]]
                C2 = most_abundant_indices[comm_keys[j]]

                if C1 >= rep_interaction_matrix.shape[0] or C2 >= rep_interaction_matrix.shape[0]:
                    continue

                alpha_12 = rep_interaction_matrix[C1, C2]
                alpha_21 = rep_interaction_matrix[C2, C1]

                # FILTER: Exclude both alpha > 1
                if alpha_12 > 1.0 and alpha_21 > 1.0:
                    both_alpha_gt_1_filtered += 1
                    continue

                # Calculate species dominance
                species_dominance_raw = calculate_lv_equilibrium_dominance(alpha_12, alpha_21)
                ratio = species_dominance_raw / (1 - species_dominance_raw + 1e-8)
                species_dominance = np.arctan(ratio) / (np.pi / 2)

                total_processed += 1

                # Classify by LV case
                if alpha_12 < 1.0 and alpha_21 > 1.0:
                    exclusion_cases.append(('sp1_wins', species_dominance, community_dominance))
                elif alpha_12 > 1.0 and alpha_21 < 1.0:
                    exclusion_cases.append(('sp2_wins', species_dominance, community_dominance))
                elif alpha_12 < 1.0 and alpha_21 < 1.0:
                    if alpha_12 + alpha_21 < 2.0:
                        coexistence_cases.append((species_dominance, community_dominance))
                    else:
                        bistability_cases.append((species_dominance, community_dominance))

                # Determine if inverse
                x_side = 'c1' if species_dominance > 0.5 else 'c2'
                y_side = 'c1' if community_dominance > 0.5 else 'c2'

                is_inverse = (x_side != y_side)

                if is_inverse:
                    inverse_cases.append({
                        'alpha_12': alpha_12,
                        'alpha_21': alpha_21,
                        'x': species_dominance,
                        'y': community_dominance
                    })
                else:
                    non_inverse_cases.append({
                        'alpha_12': alpha_12,
                        'alpha_21': alpha_21,
                        'x': species_dominance,
                        'y': community_dominance
                    })

    return {
        'total': total_processed,
        'inverse': len(inverse_cases),
        'non_inverse': len(non_inverse_cases),
        'exclusion': len(exclusion_cases),
        'coexistence': len(coexistence_cases),
        'bistability': len(bistability_cases),
        'both_alpha_gt_1_filtered': both_alpha_gt_1_filtered
    }

# Load data
with open('Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json', 'r') as f:
    data = json.load(f)

print("="*80)
print("INVERSE RATE ACROSS ALL INTENSITIES")
print("="*80)

intensities = ['0.20', '0.40', '0.60', '0.80', '1.00', '1.20']

results = {}
for intensity in intensities:
    if intensity in data:
        results[intensity] = analyze_intensity(data, intensity)

# Print table
print(f"\n{'Intensity':<12} {'Total':<8} {'Inverse':<10} {'Non-inv':<10} {'Inv Rate':<12} {'Exclusion':<12} {'Coexist':<10} {'Bistab':<10} {'Filtered':<10}")
print("-" * 120)

for intensity in intensities:
    if intensity in results:
        r = results[intensity]
        inv_rate = (r['inverse'] / r['total'] * 100) if r['total'] > 0 else 0
        print(f"I={intensity:<8} {r['total']:<8} {r['inverse']:<10} {r['non_inverse']:<10} {inv_rate:>5.1f}%{'':<6} {r['exclusion']:<12} {r['coexistence']:<10} {r['bistability']:<10} {r['both_alpha_gt_1_filtered']:<10}")

print("\n" + "="*80)
print("KEY OBSERVATIONS")
print("="*80)

# Calculate trend
inv_rates = [(float(i), results[i]['inverse'] / results[i]['total'] * 100)
             for i in intensities if i in results and results[i]['total'] > 0]

print(f"\nInverse rate vs. competition intensity:")
for i_val, rate in inv_rates:
    bar = "#" * int(rate / 2)  # Scale to fit
    print(f"  I={i_val:.2f}: {rate:5.1f}% {bar}")

# Calculate change
if len(inv_rates) >= 2:
    initial_rate = inv_rates[0][1]
    final_rate = inv_rates[-1][1]
    change = final_rate - initial_rate
    print(f"\nChange from I=0.20 to I=1.20: {change:+.1f} percentage points")

    if change > 0:
        print(f"TREND: Inverse rate INCREASES with competition intensity")
    else:
        print(f"TREND: Inverse rate DECREASES with competition intensity")

# Case type breakdown
print(f"\n{'='*80}")
print("CASE TYPE BREAKDOWN BY INTENSITY")
print(f"{'='*80}")
print(f"\n{'Intensity':<12} {'Exclusion %':<15} {'Coexistence %':<15} {'Bistability %':<15}")
print("-" * 60)

for intensity in intensities:
    if intensity in results:
        r = results[intensity]
        total = r['exclusion'] + r['coexistence'] + r['bistability']
        if total > 0:
            excl_pct = r['exclusion'] / total * 100
            coex_pct = r['coexistence'] / total * 100
            bist_pct = r['bistability'] / total * 100
            print(f"I={intensity:<8} {excl_pct:>6.1f}%{'':<8} {coex_pct:>6.1f}%{'':<8} {bist_pct:>6.1f}%")

print(f"\n{'='*80}")
print("INTERPRETATION")
print(f"{'='*80}")
print("""
The inverse rate shows how often the Lotka-Volterra pairwise model fails to
predict the correct winner in community coalescence events.

- At LOW competition: Fewer species dominate, LV predictions more reliable
- At HIGH competition: More exclusion events, but multi-species effects stronger
- Exclusion cases: LV clearly predicts one species wins (x≈0 or x≈1)
- Coexistence cases: LV predicts stable coexistence (intermediate x)
- Bistability cases: LV predicts outcome depends on initial conditions

Note: Cases with both α>1 are filtered out (competitive exclusion/bistability).
These represent true bistability where initial conditions matter.
""")
