"""
Visualize the dynamics of parent communities and coalescence over time
Shows how abundances change from initial conditions to equilibrium
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LV import gLV

# Load an example from the data
with open('Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json', 'r') as f:
    data = json.load(f)

# Use the mixing example we found
example = data['0.30']['rep_000']
I = np.array(example['parameters']['interaction_matrix'])
g = np.array(example['parameters']['growth_rates'])
k = np.array(example['parameters']['carrying_capacities'])

# Time points for detailed trajectory
t = np.linspace(0, 2000, 500)

# Get equilibrium states
c1_eq = np.array(example['sc_list']['c1'])
c2_eq = np.array(example['sc_list']['c2'])

print("="*70)
print("SIMULATION DYNAMICS VISUALIZATION")
print("="*70)
print(f"Example: mean=0.30, rep_000 (Mixing case)")
print(f"Distribution: Narrow Uniform [0.15, 0.45]")
print()

# === Parent Community 1 Dynamics ===
print("1. Parent Community 1 (species 0-11) - Growing alone")
print("-" * 70)

y0_c1 = np.zeros(48)
y0_c1[:12] = 0.01  # Initial condition

sol_c1 = odeint(gLV, y0_c1, t, args=(I, g, k))

print(f"Initial: Total abundance = {np.sum(y0_c1):.4f}")
print(f"Final:   Total abundance = {np.sum(sol_c1[-1, :]):.4f}")
print(f"Surviving species: {np.sum(sol_c1[-1, :12] > 1e-6)} / 12")
print(f"Time to settle: ~{t[np.argmax(np.abs(np.diff(np.sum(sol_c1[:, :12], axis=1))) < 0.001)]:.0f} time units")

# === Parent Community 2 Dynamics ===
print("\n2. Parent Community 2 (species 12-23) - Growing alone")
print("-" * 70)

y0_c2 = np.zeros(48)
y0_c2[12:24] = 0.01

sol_c2 = odeint(gLV, y0_c2, t, args=(I, g, k))

print(f"Initial: Total abundance = {np.sum(y0_c2):.4f}")
print(f"Final:   Total abundance = {np.sum(sol_c2[-1, :]):.4f}")
print(f"Surviving species: {np.sum(sol_c2[-1, 12:24] > 1e-6)} / 12")

# === Coalescence Dynamics ===
print("\n3. Coalescence (0.5 × c1_equilibrium + 0.5 × c2_equilibrium)")
print("-" * 70)

y0_coal = 0.5 * c1_eq + 0.5 * c2_eq

sol_coal = odeint(gLV, y0_coal, t, args=(I, g, k))

print(f"Initial:")
print(f"  From c1 species: {np.sum(y0_coal[:12]):.4f}")
print(f"  From c2 species: {np.sum(y0_coal[12:24]):.4f}")
print(f"  Total: {np.sum(y0_coal):.4f}")

print(f"Final:")
print(f"  From c1 species: {np.sum(sol_coal[-1, :12]):.4f} ({np.sum(sol_coal[-1, :12]>1e-6)} species)")
print(f"  From c2 species: {np.sum(sol_coal[-1, 12:24]):.4f} ({np.sum(sol_coal[-1, 12:24]>1e-6)} species)")
print(f"  Total: {np.sum(sol_coal[-1, :]):.4f}")

c1_frac = np.sum(sol_coal[-1, :12]) / np.sum(sol_coal[-1, :])
c2_frac = np.sum(sol_coal[-1, 12:24]) / np.sum(sol_coal[-1, :])
print(f"\nOutcome: c1={c1_frac:.1%}, c2={c2_frac:.1%} → MIXING")

# === Create Visualization ===
print("\n" + "="*70)
print("Creating visualization...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Community 1 alone
ax = axes[0, 0]
for i in range(12):
    if sol_c1[-1, i] > 1e-6:
        ax.plot(t, sol_c1[:, i], label=f'sp{i}', alpha=0.7)
ax.set_xlabel('Time')
ax.set_ylabel('Abundance')
ax.set_title('Community 1 Alone (species 0-11)')
ax.grid(True, alpha=0.3)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# Plot 2: Community 2 alone
ax = axes[0, 1]
for i in range(12, 24):
    if sol_c2[-1, i] > 1e-6:
        ax.plot(t, sol_c2[:, i], label=f'sp{i}', alpha=0.7)
ax.set_xlabel('Time')
ax.set_ylabel('Abundance')
ax.set_title('Community 2 Alone (species 12-23)')
ax.grid(True, alpha=0.3)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# Plot 3: Coalescence - c1 species
ax = axes[1, 0]
for i in range(12):
    if sol_coal[-1, i] > 1e-6 or y0_coal[i] > 1e-6:
        ax.plot(t, sol_coal[:, i], label=f'sp{i}', alpha=0.7)
ax.set_xlabel('Time')
ax.set_ylabel('Abundance')
ax.set_title('Coalescence: c1 species (0-11)')
ax.grid(True, alpha=0.3)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# Plot 4: Coalescence - c2 species
ax = axes[1, 1]
for i in range(12, 24):
    if sol_coal[-1, i] > 1e-6 or y0_coal[i] > 1e-6:
        ax.plot(t, sol_coal[:, i], label=f'sp{i}', alpha=0.7)
ax.set_xlabel('Time')
ax.set_ylabel('Abundance')
ax.set_title('Coalescence: c2 species (12-23)')
ax.grid(True, alpha=0.3)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

plt.tight_layout()
plt.savefig('dynamics_visualization.png', dpi=150, bbox_inches='tight')
print("✓ Saved to: dynamics_visualization.png")

# === Create summary plot ===
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

# Total abundance over time
ax.plot(t, np.sum(sol_c1[:, :12], axis=1), 'b-', linewidth=2, label='c1 alone', alpha=0.7)
ax.plot(t, np.sum(sol_c2[:, 12:24], axis=1), 'r-', linewidth=2, label='c2 alone', alpha=0.7)
ax.plot(t, np.sum(sol_coal[:, :12], axis=1), 'b--', linewidth=2, label='c1 in coalescence', alpha=0.7)
ax.plot(t, np.sum(sol_coal[:, 12:24], axis=1), 'r--', linewidth=2, label='c2 in coalescence', alpha=0.7)
ax.plot(t, np.sum(sol_coal[:, :], axis=1), 'k-', linewidth=2, label='Total in coalescence', alpha=0.7)

ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Total Abundance', fontsize=12)
ax.set_title('Community Dynamics: Parent vs Coalescence', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('dynamics_summary.png', dpi=150, bbox_inches='tight')
print("✓ Saved to: dynamics_summary.png")

print("\n" + "="*70)
print("DONE!")
print("="*70)
print("\nKey observations:")
print("1. Parent communities reach equilibrium from initial 0.01")
print("2. Coalescence starts from 0.5 × equilibrium of each parent")
print("3. Competition during coalescence can change species abundances")
print("4. Final outcome depends on interaction strengths")
print("\nVisualization files:")
print("  - dynamics_visualization.png (4 subplots showing all species)")
print("  - dynamics_summary.png (total abundances over time)")
print("="*70)
