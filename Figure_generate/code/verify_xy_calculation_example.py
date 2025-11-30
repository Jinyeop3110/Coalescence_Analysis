#!/usr/bin/env python3
"""
Concrete example showing how x and y are calculated for one coalescence event
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
    """Calculate species-level dominance using Lotka-Volterra equilibrium."""

    # Case 1: Both alphas > 1 - competitive exclusion
    if alpha_12 > 1.0 and alpha_21 > 1.0:
        return 0.5

    # Case 2: alpha_12 > 1 and alpha_21 < 1 - species 1 wins
    elif alpha_12 > 1.0 and alpha_21 < 1.0:
        return 1.0

    # Case 3: alpha_12 < 1 and alpha_21 > 1 - species 2 wins
    elif alpha_12 < 1.0 and alpha_21 > 1.0:
        return 0.0

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

# Load actual data
print("="*80)
print("CONCRETE EXAMPLE: How x and y are Calculated")
print("="*80)

with open('Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json', 'r') as f:
    data = json.load(f)

# Get first replicate at intensity 0.20
rep_data = data['0.20']['rep_000']
interaction_matrix = np.array(rep_data['parameters']['interaction_matrix'])
sc_list = rep_data['sc_list']
cc_list = rep_data['cc_list']

# Get communities
c1 = np.array(sc_list['c1'])
c2 = np.array(sc_list['c2'])
c_mix = np.array(cc_list['c1_c2'])

# Normalize
c1_norm = c1 / (np.sum(c1) + 1e-8)
c2_norm = c2 / (np.sum(c2) + 1e-8)
c_mix_norm = c_mix / (np.sum(c_mix) + 1e-8)

print("\n" + "="*80)
print("STEP 1: Identify Most Abundant Species")
print("="*80)

C1 = np.argmax(c1_norm)
C2 = np.argmax(c2_norm)

print(f"\nCommunity c1 (48 species):")
print(f"  Most abundant species: {C1}")
print(f"  Abundance: {c1_norm[C1]:.4f}")
print(f"  Top 3 species: {np.argsort(c1_norm)[-3:][::-1]} with abundances {c1_norm[np.argsort(c1_norm)[-3:][::-1]]}")

print(f"\nCommunity c2 (48 species):")
print(f"  Most abundant species: {C2}")
print(f"  Abundance: {c2_norm[C2]:.4f}")
print(f"  Top 3 species: {np.argsort(c2_norm)[-3:][::-1]} with abundances {c2_norm[np.argsort(c2_norm)[-3:][::-1]]}")

print(f"\nCoalescence outcome c_mix (48 species):")
c_mix_top3 = np.argsort(c_mix_norm)[-3:][::-1]
print(f"  Top 3 species: {c_mix_top3} with abundances {c_mix_norm[c_mix_top3]}")

print("\n" + "="*80)
print("STEP 2: Extract Interaction Coefficients")
print("="*80)

alpha_12 = interaction_matrix[C1, C2]
alpha_21 = interaction_matrix[C2, C1]

print(f"\nInteraction matrix is 48x48, diagonal = 1.0 (intraspecific competition)")
print(f"\nalpha_12 = interaction_matrix[{C1}, {C2}] = {alpha_12:.4f}")
print(f"  Interpretation: Effect of species {C2} on species {C1}")
print(f"\nalpha_21 = interaction_matrix[{C2}, {C1}] = {alpha_21:.4f}")
print(f"  Interpretation: Effect of species {C1} on species {C2}")
print(f"\nMatrix is asymmetric: alpha_12 ≠ alpha_21? {alpha_12 != alpha_21}")

print("\n" + "="*80)
print("STEP 3: Calculate x (Species-Level Dominance from LV Equilibrium)")
print("="*80)

print(f"\nLotka-Volterra analysis:")
print(f"  alpha_12 = {alpha_12:.4f} ({'>' if alpha_12 > 1 else '<'} 1)")
print(f"  alpha_21 = {alpha_21:.4f} ({'>' if alpha_21 > 1 else '<'} 1)")
print(f"  sum = {alpha_12 + alpha_21:.4f} ({'>' if alpha_12 + alpha_21 > 2 else '<'} 2)")

if alpha_12 < 1.0 and alpha_21 < 1.0 and alpha_12 + alpha_21 < 2.0:
    print(f"\n→ Case: Stable coexistence (both < 1, sum < 2)")
    print(f"\nLV equilibrium formula:")
    print(f"  N1*/(N1*+N2*) = (1 - alpha_12) / (2 - alpha_12 - alpha_21)")
    print(f"                = (1 - {alpha_12:.4f}) / (2 - {alpha_12:.4f} - {alpha_21:.4f})")
    print(f"                = {1 - alpha_12:.4f} / {2 - alpha_12 - alpha_21:.4f}")
    species_dominance = calculate_lv_equilibrium_dominance(alpha_12, alpha_21)
    print(f"                = {species_dominance:.4f}")
else:
    species_dominance = calculate_lv_equilibrium_dominance(alpha_12, alpha_21)
    print(f"\n→ Other case, species dominance = {species_dominance:.4f}")

x = species_dominance

print(f"\n{'*'*80}")
print(f"x = {x:.4f}")
print(f"{'*'*80}")
print(f"Interpretation: Species {C1} has predicted dominance of {x:.1%} at LV equilibrium")
print(f"                Species {C2} has predicted dominance of {1-x:.1%}")

print("\n" + "="*80)
print("STEP 4: Calculate y (Community-Level Dominance from Vector Decomposition)")
print("="*80)

try:
    u, v, k = metric_VectorDecomposition_onlyPositive(c1_norm, c2_norm, c_mix_norm)

    print(f"\nVector decomposition: c_mix ≈ u·c1 + v·c2 + k·(orthogonal)")
    print(f"  u = {u:.4f} (contribution from c1)")
    print(f"  v = {v:.4f} (contribution from c2)")
    print(f"  k = {k:.4f} (restructuring/orthogonal component)")
    print(f"\nNormalization check: u² + v² + k² = {u**2 + v**2 + k**2:.4f} (should be ≈ 1.0)")

    mixing_strength = u**2 + v**2
    print(f"\nMixing strength: u² + v² = {u**2:.4f} + {v**2:.4f} = {mixing_strength:.4f}")
    print(f"Filter threshold: {mixing_strength:.4f} > 0.66? {mixing_strength > 0.66}")

    if mixing_strength <= 0.66:
        print(f"→ FILTERED OUT: Too much restructuring (k² = {k**2:.4f})")
        y = None
    else:
        print(f"→ PASSES FILTER: Mixing dominates over restructuring")

        ratio = u / (v + 1e-8)
        arctan_value = np.arctan(ratio)
        community_dominance = arctan_value / (np.pi / 2)

        print(f"\nArctan normalization:")
        print(f"  ratio = u/v = {u:.4f}/{v:.4f} = {ratio:.4f}")
        print(f"  arctan({ratio:.4f}) = {arctan_value:.4f} radians")
        print(f"  normalized = {arctan_value:.4f} / (π/2) = {arctan_value:.4f} / {np.pi/2:.4f} = {community_dominance:.4f}")

        y = community_dominance

        print(f"\n{'*'*80}")
        print(f"y = {y:.4f}")
        print(f"{'*'*80}")
        print(f"Interpretation: Community c1 has observed dominance of {y:.1%} in coalescence")
        print(f"                Community c2 has observed dominance of {1-y:.1%}")

except Exception as e:
    print(f"Error in vector decomposition: {e}")
    y = None

print("\n" + "="*80)
print("STEP 5: Data Point Duplication")
print("="*80)

if y is not None:
    print(f"\nOriginal data point:")
    print(f"  (x, y) = ({x:.4f}, {y:.4f})")

    print(f"\nDuplicated (symmetric) data point:")
    print(f"  (1-x, 1-y) = ({1-x:.4f}, {1-y:.4f})")

    print(f"\nBoth points are added to the scatter plot to create symmetry around (0.5, 0.5)")

print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

if y is not None:
    print(f"\nFor coalescence c1 + c2 → c_mix:")
    print(f"  Most abundant species: {C1} (c1) vs {C2} (c2)")
    print(f"  Interaction: α₁₂={alpha_12:.4f}, α₂₁={alpha_21:.4f}")
    print(f"  ")
    print(f"  x (Species LV Dominance)     = {x:.4f}")
    print(f"  y (Community Dominance)      = {y:.4f}")
    print(f"  ")
    print(f"  Data points added to plot: ({x:.4f}, {y:.4f}) and ({1-x:.4f}, {1-y:.4f})")

    if abs(x - y) < 0.1:
        print(f"\n→ Good agreement: Species-level competition predicts community outcome")
    else:
        print(f"\n→ Poor agreement: Community dynamics differ from pairwise predictions")
        print(f"  Difference: |x - y| = {abs(x-y):.4f}")
else:
    print(f"\nThis coalescence event was FILTERED OUT (too much restructuring)")

print("\n" + "="*80)
