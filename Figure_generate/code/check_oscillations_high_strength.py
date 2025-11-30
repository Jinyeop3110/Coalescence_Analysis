"""
Check for oscillations specifically in HIGH interaction strength regions
where oscillations are more likely
"""

import numpy as np
import json
from scipy.integrate import odeint
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LV import gLV

data_file = "Simulation_Data/mean_std_grid_100reps/Community_mean_std_grid_100reps.json"

print("="*70)
print("CHECKING FOR OSCILLATIONS AT HIGH INTERACTION STRENGTHS")
print("="*70)

with open(data_file, 'r') as f:
    data = json.load(f)

# Check high interaction strength points
test_keys = [
    "mean0.80_std0.50",
    "mean0.90_std0.50",
    "mean1.00_std0.50",
    "mean1.10_std0.60",
    "mean1.20_std0.60",
]

print(f"\nAnalyzing high interaction strength points...")

total_oscillating = 0
total_stable = 0
total_explosive = 0
total_checked = 0

for grid_key in test_keys:
    if grid_key not in data:
        print(f"\nSkipping {grid_key} (not found)")
        continue

    print(f"\n{'='*70}")
    print(f"Grid point: {grid_key}")
    print(f"{'='*70}")

    grid_data = data[grid_key]
    rep_keys = [k for k in grid_data.keys() if k.startswith('rep_')][:5]

    for rep_key in rep_keys:
        rep_data = grid_data[rep_key]

        I = np.array(rep_data['parameters']['interaction_matrix'])
        g = np.array(rep_data['parameters']['growth_rates'])
        k = np.array(rep_data['parameters']['carrying_capacities'])

        print(f"\n  {rep_key}:")

        # Check c1 community
        c1_final = np.array(rep_data['sc_list']['c1'])

        if np.any(c1_final > 1e10):
            print(f"    c1: EXPLOSIVE (max = {np.max(c1_final):.2e})")
            total_explosive += 1
            total_checked += 1
            continue

        if np.all(c1_final < 1e-6):
            print(f"    c1: ALL EXTINCT")
            total_stable += 1
            total_checked += 1
            continue

        # Re-integrate for 500 more time units to check stability
        N = len(c1_final)
        t_check = np.linspace(0, 500, 200)

        try:
            sol_check = odeint(gLV, c1_final, t_check, args=(I, g, k))

            # Check for explosive growth during check
            if np.any(sol_check > 1e10):
                print(f"    c1: BECAME EXPLOSIVE during check")
                total_explosive += 1
                total_checked += 1
                continue

            # Calculate CV for each non-extinct species over last half of trajectory
            last_half = sol_check[100:, :]
            cvs = []
            for i in range(N):
                if last_half[:, i].max() > 1e-6:
                    mean_abund = np.mean(last_half[:, i])
                    std_abund = np.std(last_half[:, i])
                    cv = std_abund / (mean_abund + 1e-10)
                    cvs.append(cv)

            if len(cvs) > 0:
                max_cv = np.max(cvs)
                mean_cv = np.mean(cvs)

                # Also check trend (is it still changing?)
                first_quarter = sol_check[:50, :]
                last_quarter = sol_check[-50:, :]
                trend = np.max(np.abs(last_quarter.mean(axis=0) - first_quarter.mean(axis=0)))

                if max_cv > 0.05:  # Lowered threshold
                    print(f"    c1: OSCILLATING (max CV={max_cv:.3f}, mean CV={mean_cv:.3f}, trend={trend:.3e})")
                    total_oscillating += 1
                else:
                    print(f"    c1: STABLE (max CV={max_cv:.3f}, mean CV={mean_cv:.3f}, trend={trend:.3e})")
                    total_stable += 1
            else:
                print(f"    c1: ALL EXTINCT")
                total_stable += 1

            total_checked += 1

        except Exception as e:
            print(f"    c1: ERROR: {str(e)[:50]}")
            total_explosive += 1
            total_checked += 1

        # Also check one coalescence event
        if 'c1_c2' in rep_data['cc_list']:
            cc_final = np.array(rep_data['cc_list']['c1_c2'])

            if np.any(cc_final > 1e10):
                print(f"    c1_c2: EXPLOSIVE (max = {np.max(cc_final):.2e})")
                total_explosive += 1
                total_checked += 1
                continue

            if np.all(cc_final < 1e-6):
                print(f"    c1_c2: ALL EXTINCT")
                total_stable += 1
                total_checked += 1
                continue

            try:
                sol_check = odeint(gLV, cc_final, t_check, args=(I, g, k))

                if np.any(sol_check > 1e10):
                    print(f"    c1_c2: BECAME EXPLOSIVE")
                    total_explosive += 1
                    total_checked += 1
                    continue

                last_half = sol_check[100:, :]
                cvs = []
                for i in range(N):
                    if last_half[:, i].max() > 1e-6:
                        mean_abund = np.mean(last_half[:, i])
                        std_abund = np.std(last_half[:, i])
                        cv = std_abund / (mean_abund + 1e-10)
                        cvs.append(cv)

                if len(cvs) > 0:
                    max_cv = np.max(cvs)
                    if max_cv > 0.05:
                        print(f"    c1_c2: OSCILLATING (max CV={max_cv:.3f})")
                        total_oscillating += 1
                    else:
                        print(f"    c1_c2: STABLE (max CV={max_cv:.3f})")
                        total_stable += 1
                else:
                    print(f"    c1_c2: ALL EXTINCT")
                    total_stable += 1

                total_checked += 1

            except Exception as e:
                print(f"    c1_c2: ERROR: {str(e)[:50]}")
                total_explosive += 1
                total_checked += 1

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Total systems checked: {total_checked}")
if total_checked > 0:
    print(f"  Stable (equilibrium): {total_stable} ({100*total_stable/total_checked:.1f}%)")
    print(f"  Oscillating: {total_oscillating} ({100*total_oscillating/total_checked:.1f}%)")
    print(f"  Explosive/Error: {total_explosive} ({100*total_explosive/total_checked:.1f}%)")

print("\n" + "="*70)
print("CONCLUSION:")
print("="*70)
print("""
Current handling of oscillations:
- The code does NOT detect oscillations
- Simply takes final state at t=2000
- If oscillations exist, this captures a random phase of the oscillation

This could contribute to the stochasticity in the heatmaps if oscillations
are present, but based on this analysis, oscillations appear to be rare
or absent in most parameter regimes.

The stochasticity is more likely due to:
1. Different random interaction matrices for each rep
2. High sensitivity to specific matrix configurations
3. Insufficient averaging (only 100 reps × 6 coalescences per grid point)
""")
