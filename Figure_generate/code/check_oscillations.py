"""
Check if oscillation cases are occurring in the simulations
Analyze dynamics to see if systems reach equilibrium or oscillate
"""

import numpy as np
import json
from scipy.integrate import odeint
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LV import gLV

# Load a few simulations and check their dynamics
data_file = "Simulation_Data/mean_std_grid_100reps/Community_mean_std_grid_100reps.json"

print("="*70)
print("CHECKING FOR OSCILLATIONS IN SIMULATIONS")
print("="*70)

with open(data_file, 'r') as f:
    data = json.load(f)

# Check a few random grid points
test_keys = list(data.keys())[:5]  # First 5 grid points

print(f"\nAnalyzing {len(test_keys)} grid points...")

total_oscillating = 0
total_stable = 0
total_explosive = 0
total_checked = 0

for grid_key in test_keys:
    print(f"\n{'='*70}")
    print(f"Grid point: {grid_key}")
    print(f"{'='*70}")

    grid_data = data[grid_key]

    # Check first 3 reps
    rep_keys = [k for k in grid_data.keys() if k.startswith('rep_')][:3]

    for rep_key in rep_keys:
        rep_data = grid_data[rep_key]

        # Get interaction matrix
        I = np.array(rep_data['parameters']['interaction_matrix'])
        g = np.array(rep_data['parameters']['growth_rates'])
        k = np.array(rep_data['parameters']['carrying_capacities'])

        print(f"\n  {rep_key}:")

        # Check one parent community and one coalescence
        # Pick c1
        c1_final = np.array(rep_data['sc_list']['c1'])

        # Check if final state looks reasonable
        if np.any(c1_final > 1e10):
            print(f"    c1: EXPLOSIVE GROWTH (max abundance = {np.max(c1_final):.2e})")
            total_explosive += 1
            total_checked += 1
            continue

        # Re-integrate from a point near the end to check for oscillations
        # Use the final state as initial condition and integrate for 500 more time steps
        N = len(c1_final)
        t_check = np.linspace(0, 500, 100)

        try:
            sol_check = odeint(gLV, c1_final, t_check, args=(I, g, k))

            # Check if abundances are stable (small changes)
            max_change = np.max(np.abs(sol_check[-1, :] - sol_check[0, :]))
            rel_change = max_change / (np.max(np.abs(sol_check[0, :])) + 1e-10)

            # Check for oscillations by looking at variance over time
            # For each species, calculate coefficient of variation
            cvs = []
            for i in range(N):
                if sol_check[:, i].max() > 1e-6:  # Only check non-extinct species
                    mean_abund = np.mean(sol_check[:, i])
                    std_abund = np.std(sol_check[:, i])
                    cv = std_abund / (mean_abund + 1e-10)
                    cvs.append(cv)

            if len(cvs) > 0:
                max_cv = np.max(cvs)

                if max_cv > 0.1:
                    print(f"    c1: OSCILLATING (max CV = {max_cv:.3f}, rel_change = {rel_change:.3f})")
                    total_oscillating += 1
                else:
                    print(f"    c1: STABLE (max CV = {max_cv:.3f}, rel_change = {rel_change:.3f})")
                    total_stable += 1
            else:
                print(f"    c1: ALL EXTINCT")
                total_stable += 1

            total_checked += 1

        except Exception as e:
            print(f"    c1: ERROR during integration: {str(e)}")
            total_explosive += 1
            total_checked += 1

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Total systems checked: {total_checked}")
print(f"  Stable (equilibrium): {total_stable} ({100*total_stable/total_checked:.1f}%)")
print(f"  Oscillating: {total_oscillating} ({100*total_oscillating/total_checked:.1f}%)")
print(f"  Explosive/Error: {total_explosive} ({100*total_explosive/total_checked:.1f}%)")

print("\n" + "="*70)
print("HOW OSCILLATIONS ARE HANDLED IN CURRENT CODE:")
print("="*70)
print("""
Current approach:
1. Integrate from t=0 to t=2000 with 500 time points
2. Take the FINAL state at t=2000: final_state = sol[-1, :]
3. Apply extinction threshold: final_state[final_state < 1e-4] = 0
4. Store this as the "equilibrium" state

Problems with oscillating systems:
- If the system oscillates, the "final state" at t=2000 is just one snapshot
  of the oscillation, not a true equilibrium
- The outcome classification (dominance/mixing/restructuring) will depend on
  WHICH PHASE of the oscillation we happened to sample at t=2000
- This adds randomness to the results

Better approaches would be:
1. Detect oscillations by checking if variance over the last 25% of time is high
2. For oscillating systems, average over the last oscillation period
3. Or extend integration time until equilibrium is reached
4. Or flag oscillating systems separately in the analysis
""")
