#!/usr/bin/env python3
"""Test script to verify alpha_12 and alpha_21 extraction is correct"""

import json
import numpy as np

# Load data
with open('Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json', 'r') as f:
    data = json.load(f)

# Get first replicate at intensity 0.20
rep_data = data['0.20']['rep_000']
interaction_matrix = np.array(rep_data['parameters']['interaction_matrix'])

print("=== Interaction Matrix Structure ===")
print(f"Shape: {interaction_matrix.shape}")
print(f"Diagonal (should be 1.0): {interaction_matrix[0,0]}, {interaction_matrix[1,1]}, {interaction_matrix[2,2]}")
print(f"Matrix is symmetric? {np.allclose(interaction_matrix, interaction_matrix.T)}")
print(f"\nFirst 5x5 block:")
print(interaction_matrix[:5, :5])

# Get most abundant species from first two communities
sc_list = rep_data['sc_list']
c1 = np.array(sc_list['c1'])
c2 = np.array(sc_list['c2'])

C1 = np.argmax(c1)
C2 = np.argmax(c2)

print(f"\n=== Most Abundant Species ===")
print(f"Community c1: species {C1} (abundance: {c1[C1]:.4f})")
print(f"Community c2: species {C2} (abundance: {c2[C2]:.4f})")

# Extract alphas
alpha_12 = interaction_matrix[C1, C2]
alpha_21 = interaction_matrix[C2, C1]

print(f"\n=== Interaction Coefficients ===")
print(f"C1 = {C1}, C2 = {C2}")
print(f"alpha_12 = interaction_matrix[C1, C2] = interaction_matrix[{C1}, {C2}] = {alpha_12:.4f}")
print(f"  Interpretation: effect of species {C2} on species {C1}")
print(f"alpha_21 = interaction_matrix[C2, C1] = interaction_matrix[{C2}, {C1}] = {alpha_21:.4f}")
print(f"  Interpretation: effect of species {C1} on species {C2}")
print(f"\nAre they different (asymmetric)? {alpha_12 != alpha_21}")

# LV equilibrium analysis
print(f"\n=== LV Equilibrium Analysis ===")
print(f"alpha_12 = {alpha_12:.4f}, is > 1? {alpha_12 > 1.0}")
print(f"alpha_21 = {alpha_21:.4f}, is > 1? {alpha_21 > 1.0}")
print(f"sum = {alpha_12 + alpha_21:.4f}, is > 2? {alpha_12 + alpha_21 > 2.0}")

if alpha_12 < 1.0 and alpha_21 < 1.0:
    if alpha_12 + alpha_21 < 2.0:
        dominance = (1 - alpha_12) / (2 - alpha_12 - alpha_21)
        print(f"\nCase: Stable coexistence")
        print(f"Species dominance = (1 - {alpha_12:.4f}) / (2 - {alpha_12:.4f} - {alpha_21:.4f})")
        print(f"                  = {1 - alpha_12:.4f} / {2 - alpha_12 - alpha_21:.4f}")
        print(f"                  = {dominance:.4f}")
        print(f"\nThis means species {C1} has {dominance:.1%} relative abundance at equilibrium")
        print(f"and species {C2} has {1-dominance:.1%} relative abundance")
    else:
        print(f"\nCase: Bistability (both < 1 but sum > 2)")
        print(f"Cannot predict from pairwise LV alone, returning 0.5")
elif alpha_12 > 1.0 and alpha_21 < 1.0:
    print(f"\nCase: Species {C1} wins (alpha_12 > 1, alpha_21 < 1)")
elif alpha_12 < 1.0 and alpha_21 > 1.0:
    print(f"\nCase: Species {C2} wins (alpha_12 < 1, alpha_21 > 1)")
else:
    print(f"\nCase: Competitive exclusion (both > 1)")

# Now let's check the interpretation of alpha_ij
print(f"\n=== Verifying Alpha Interpretation ===")
print("In Lotka-Volterra model:")
print("  dN1/dt = r1*N1*(1 - (N1 + alpha_12*N2)/K1)")
print("  dN2/dt = r2*N2*(1 - (N2 + alpha_21*N1)/K2)")
print("")
print("Where alpha_12 is the effect of species 2 on species 1")
print("and alpha_21 is the effect of species 1 on species 2")
print("")
print(f"So alpha_12 = interaction_matrix[C1, C2] = effect of sp{C2} on sp{C1} ✓")
print(f"and alpha_21 = interaction_matrix[C2, C1] = effect of sp{C1} on sp{C2} ✓")
