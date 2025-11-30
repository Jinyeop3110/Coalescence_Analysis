#!/usr/bin/env python3
"""
Count inverse vs non-inverse cases at I=1.2 after LV fix
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

# Load data
with open('Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json', 'r') as f:
    data = json.load(f)

print("="*80)
print("COUNTING INVERSE VS NON-INVERSE CASES AT I=1.2")
print("="*80)

intensity_data = data['1.20']

inverse_cases = []
non_inverse_cases = []
exclusion_cases = []  # Track α₁₂ < 1, α₂₁ > 1 OR α₁₂ > 1, α₂₁ < 1
coexistence_cases = []  # Track both α < 1, sum < 2
bistability_cases = []  # Track both α < 1, sum > 2

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
            # Inverse = predicted opposite sides of 0.5
            # species_dominance > 0.5 predicts sp1 wins (c1 wins)
            # community_dominance > 0.5 means c1 wins
            # So inverse if (x>0.5 and y<0.5) or (x<0.5 and y>0.5)

            x_side = 'c1' if species_dominance > 0.5 else 'c2'
            y_side = 'c1' if community_dominance > 0.5 else 'c2'

            is_inverse = (x_side != y_side)

            case_info = {
                'rep': rep_key,
                'coal': coal_key,
                'C1': C1,
                'C2': C2,
                'alpha_12': alpha_12,
                'alpha_21': alpha_21,
                'x': species_dominance,
                'y': community_dominance,
                'x_side': x_side,
                'y_side': y_side
            }

            if is_inverse:
                inverse_cases.append(case_info)
            else:
                non_inverse_cases.append(case_info)

print(f"\nTotal cases processed (after all filters): {total_processed}")
print(f"\n{'='*80}")
print("OVERALL BREAKDOWN")
print(f"{'='*80}")
print(f"Inverse cases:     {len(inverse_cases):3d} ({len(inverse_cases)/total_processed*100:.1f}%)")
print(f"Non-inverse cases: {len(non_inverse_cases):3d} ({len(non_inverse_cases)/total_processed*100:.1f}%)")

print(f"\n{'='*80}")
print("BREAKDOWN BY LV CASE TYPE")
print(f"{'='*80}")
print(f"Exclusion cases (α₁₂<1, α₂₁>1 or α₁₂>1, α₂₁<1): {len(exclusion_cases)}")
print(f"Coexistence cases (both α<1, sum<2):           {len(coexistence_cases)}")
print(f"Bistability cases (both α<1, sum>2):           {len(bistability_cases)}")

# Analyze inverse cases by type
inverse_exclusion = [c for c in inverse_cases if
                     (c['alpha_12'] < 1.0 and c['alpha_21'] > 1.0) or
                     (c['alpha_12'] > 1.0 and c['alpha_21'] < 1.0)]
inverse_coexistence = [c for c in inverse_cases if
                       c['alpha_12'] < 1.0 and c['alpha_21'] < 1.0 and
                       c['alpha_12'] + c['alpha_21'] < 2.0]
inverse_bistability = [c for c in inverse_cases if
                       c['alpha_12'] < 1.0 and c['alpha_21'] < 1.0 and
                       c['alpha_12'] + c['alpha_21'] >= 2.0]

print(f"\n{'='*80}")
print("INVERSE CASES BY TYPE")
print(f"{'='*80}")
if len(exclusion_cases) > 0:
    print(f"Exclusion:    {len(inverse_exclusion):3d} / {len(exclusion_cases):3d} ({len(inverse_exclusion)/len(exclusion_cases)*100:.1f}% of exclusion cases are inverse)")
if len(coexistence_cases) > 0:
    print(f"Coexistence:  {len(inverse_coexistence):3d} / {len(coexistence_cases):3d} ({len(inverse_coexistence)/len(coexistence_cases)*100:.1f}% of coexistence cases are inverse)")
if len(bistability_cases) > 0:
    print(f"Bistability:  {len(inverse_bistability):3d} / {len(bistability_cases):3d} ({len(inverse_bistability)/len(bistability_cases)*100:.1f}% of bistability cases are inverse)")
else:
    print(f"Bistability:  {len(inverse_bistability):3d} /   0 (no bistability cases after filtering both α>1)")

print(f"\n{'='*80}")
print("DETAILED INVERSE CASES")
print(f"{'='*80}")

for idx, case in enumerate(inverse_cases[:5], 1):
    print(f"\nInverse Case {idx}:")
    print(f"  {case['rep']} - {case['coal']}")
    print(f"  Most abundant: sp{case['C1']} (c1) vs sp{case['C2']} (c2)")
    print(f"  α₁₂={case['alpha_12']:.3f}, α₂₁={case['alpha_21']:.3f}, sum={case['alpha_12']+case['alpha_21']:.3f}")
    print(f"  LV predicts: {case['x_side']} wins (x={case['x']:.3f})")
    print(f"  Reality:     {case['y_side']} wins (y={case['y']:.3f})")

    # Determine case type
    if case['alpha_12'] < 1.0 and case['alpha_21'] > 1.0:
        case_type = "Exclusion (sp1 wins)"
    elif case['alpha_12'] > 1.0 and case['alpha_21'] < 1.0:
        case_type = "Exclusion (sp2 wins)"
    elif case['alpha_12'] < 1.0 and case['alpha_21'] < 1.0:
        if case['alpha_12'] + case['alpha_21'] < 2.0:
            case_type = "Coexistence"
        else:
            case_type = "Bistability"
    else:
        case_type = "Unknown"
    print(f"  Case type: {case_type}")

print(f"\n{'='*80}")
print("COMPARISON TO BEFORE LV FIX")
print(f"{'='*80}")
print("BEFORE FIX (with backwards LV logic):")
print("  Inverse cases: 31/50 (62%)")
print("  Non-inverse:   19/50 (38%)")
print("")
print("AFTER FIX (with corrected LV logic):")
print(f"  Inverse cases: {len(inverse_cases)}/{total_processed} ({len(inverse_cases)/total_processed*100:.1f}%)")
print(f"  Non-inverse:   {len(non_inverse_cases)}/{total_processed} ({len(non_inverse_cases)/total_processed*100:.1f}%)")
print("")
print(f"IMPROVEMENT: {62 - len(inverse_cases)/total_processed*100:.1f} percentage point reduction in inverse cases!")
