#!/usr/bin/env python
"""
48 Species Simulation with 200 Repetitions and Fine Intensity Intervals
MODIFIED VERSION: Saves full interaction matrices

This script runs Lotka-Volterra simulations with:
- 48 total species
- 12 species per community
- 200 independent repetitions per interaction strength
- 24 interaction strengths: 0.05 to 1.2 in steps of 0.05
- Each repetition initializes a new species pool
- SAVES FULL INTERACTION MATRICES in the JSON output

Usage:
conda activate coalescence
python run_48species_200reps_fine_WITH_MATRICES.py
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from InitializeSpeciesPool import InitializeSpeceiesPool
from LV import run_lotka_volterra
from VariousMetrics import *


def uniform_distribution(u, o):
    """Generate uniform random interaction strength."""
    return (2*u + 2*o) * np.random.random() - o


def InitializeRandomCommunityPool_48(N, num_C, num_S, save_path="Data/test"):
    """
    Initialize random non-overlapping communities for 48 species pool.
    Creates 4 communities of 12 species each.
    """
    # Create non-overlapping communities
    CommunitiesLibrary = np.zeros([num_C, N])

    # Generate random permutation of all species
    all_species = np.random.permutation(N)

    # Assign species to communities
    for i in range(num_C):
        # Select species for this community
        start_idx = i * num_S
        end_idx = start_idx + num_S

        if end_idx <= N:
            selected_species = all_species[start_idx:end_idx]
            CommunitiesLibrary[i, selected_species] = 1
        else:
            print(f"Warning: Not enough species for community {i}")
            break

    # Save community library
    df1 = pd.DataFrame(CommunitiesLibrary)
    with pd.ExcelWriter(save_path + '/communityLibrary.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Sheet1')

    return CommunitiesLibrary


def simulate_48_species_200reps_fine_with_matrices():
    """Run the 48 species simulation with 200 repetitions and fine intensity intervals.

    MODIFIED: Saves full interaction matrices for each repetition.
    """

    # Simulation parameters for 48 species - 500 repetitions, fine intervals
    session_name = "Simulation_Data/48species_500reps_fine_WITH_MATRICES"

    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")

    # Parameters
    N_reps = 500  # Number of repetitions per interaction strength
    N = 48  # Total species pool
    num_S = 12  # Species per community
    num_C = 4  # Number of communities (48/12 = 4)

    # Fine intensity intervals: 0.05 to 1.2 in steps of 0.05
    u_list = np.arange(0.05, 1.25, 0.05)  # 0.05, 0.10, 0.15, ..., 1.20
    u_list = np.round(u_list, 2)  # Round to avoid floating point precision issues

    o = 0  # Offset parameter
    t = [0, 5000]  # Time span
    threshold = 1e-3  # Extinction threshold

    print(f"\n🔬 FINE INTERVAL SIMULATION WITH INTERACTION MATRICES")
    print(f"=" * 70)
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Repetitions per intensity: {N_reps}")
    print(f"Interaction strength range: {u_list[0]:.2f} to {u_list[-1]:.2f}")
    print(f"Number of intensity values: {len(u_list)}")
    print(f"Intensity step size: 0.05")
    print(f"Total simulations: {len(u_list) * N_reps}")
    print(f"\n⚠️  NEW: This version saves FULL interaction matrices (48×48)")
    print(f"   Expected file size: ~500-700 MB (for 500 reps vs 100 MB for 200 reps)")
    print(f"=" * 70)

    # Check if we need to run the simulation
    output_file = session_name + '/Community_500reps_fine_WITH_MATRICES.json'
    if os.path.isfile(output_file):
        print(f"\n⚠️  Simulation data already exists at: {output_file}")
        user_input = input("Do you want to overwrite? (y/n): ")
        if user_input.lower() != 'y':
            print("Exiting without running simulation.")
            return

    # Save parameters
    params_dict = {
        'N': N,
        'num_S': num_S,
        'num_C': num_C,
        'N_reps': N_reps,
        'u_list': u_list.tolist(),
        'u_range': f'{u_list[0]:.2f} to {u_list[-1]:.2f}',
        'u_step': 0.05,
        'o': o,
        't': t,
        'threshold': threshold,
        'simulation_type': 'fine_intervals_with_matrices',
        'includes_interaction_matrices': True
    }

    param_df = pd.DataFrame([params_dict])
    param_df.to_excel(f"{session_name}/simulation_parameters.xlsx", index=False)
    print(f"✓ Parameters saved to: {session_name}/simulation_parameters.xlsx")

    print("\n🚀 Starting simulation...")
    start_time = time.time()

    # Run simulation
    all_results = {}
    total_tasks = len(u_list) * N_reps
    task_count = 0

    for i, u in enumerate(u_list):
        print(f"\n{'='*70}")
        print(f"Processing interaction strength u = {u:.2f} ({i+1}/{len(u_list)})")
        print(f"{'='*70}")

        all_results[f"{u:.2f}"] = {}

        for rep in range(N_reps):
            task_count += 1
            rep_start_time = time.time()

            if rep % 10 == 0:  # Print progress every 10 reps
                elapsed = time.time() - start_time
                avg_time_per_task = elapsed / task_count if task_count > 0 else 0
                remaining_tasks = total_tasks - task_count
                eta_seconds = avg_time_per_task * remaining_tasks
                eta_minutes = eta_seconds / 60

                print(f"\n  Rep {rep+1}/{N_reps} | Overall: {task_count}/{total_tasks} ({100*task_count/total_tasks:.1f}%)")
                print(f"    ETA: {eta_minutes:.1f} minutes")

            # Set unique random seed for each repetition
            seed = int(u * 10000) + rep * 100000
            np.random.seed(seed)

            # Initialize NEW species pool for each repetition
            I, g, k = InitializeSpeceiesPool(N,
                                           lambda: uniform_distribution(u, o),
                                           f_g=lambda: np.ones(1),
                                           f_k=lambda: 1,
                                           is_diagonal_one=True,
                                           save_path=session_name)

            # Create random communities
            CommunitiesLibrary = InitializeRandomCommunityPool_48(N, num_C, num_S,
                                                                  save_path=session_name)

            # Initialize with small random abundances
            y = np.random.rand(N) * 0.1

            # Run single community simulations
            sc_list = {}
            for idx in range(num_C):
                y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
                y1[y1 < threshold] = 0
                sc_list[idx] = y1.tolist()

            # Run coalescence simulations (all pairwise combinations)
            cc_list = {}

            for idx in range(num_C):
                for jdx in range(idx + 1, num_C):
                    # Get steady states of individual communities
                    y1 = np.array(sc_list[idx])
                    y2 = np.array(sc_list[jdx])

                    # Mix communities (equal proportions)
                    y3 = (y1 + y2) / 2

                    # Run to new steady state
                    survived = y3 > threshold
                    y3 = run_lotka_volterra(y3, t, survived, I, g, k)
                    y3[y3 < threshold] = 0

                    cc_list[f"{idx}_{jdx}"] = y3.tolist()

            # Store results for this repetition
            # MODIFIED: Now includes full interaction matrix
            all_results[f"{u:.2f}"][f"rep_{rep:03d}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list,
                "parameters": {
                    "seed": seed,
                    "u": u,
                    "interaction_matrix_stats": {
                        "mean": float(np.mean(I[np.triu_indices(N, k=1)])),
                        "std": float(np.std(I[np.triu_indices(N, k=1)])),
                        "min": float(np.min(I[np.triu_indices(N, k=1)])),
                        "max": float(np.max(I[np.triu_indices(N, k=1)]))
                    },
                    "growth_rates": g.tolist(),  # All 1.0
                    "carrying_capacities": k.tolist(),  # All 1.0
                    "interaction_matrix": I.tolist()  # NEW: Full 48×48 matrix
                }
            }

            rep_end_time = time.time()
            if rep % 10 == 0:
                print(f"    Completed in {rep_end_time - rep_start_time:.2f} seconds")

            # Save intermediate results every 20 repetitions
            if (rep + 1) % 20 == 0:
                print(f"\n  💾 Saving intermediate results (rep {rep+1})...")
                with open(output_file, 'w') as f:
                    json.dump(all_results, f, indent=2)

                # Print file size
                file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"     Current file size: {file_size_mb:.1f} MB")

        # Save after each intensity
        print(f"\n💾 Saving results after completing u = {u:.2f}...")
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2)

        # Print file size
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"   File size: {file_size_mb:.1f} MB")

    # Save final results
    print("\n💾 Saving final results...")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    end_time = time.time()
    total_time = (end_time - start_time) / 60

    print(f"\n{'='*70}")
    print(f"🎉 SIMULATION COMPLETED SUCCESSFULLY!")
    print(f"{'='*70}")
    print(f"⏱️  Total time: {total_time:.1f} minutes ({total_time/60:.2f} hours)")
    print(f"📁 Data saved to: {output_file}")

    # Print final file size
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"📊 Final file size: {file_size_mb:.1f} MB")

    # Verify output and print summary statistics
    print("\n🔍 Verifying output...")
    with open(output_file, 'r') as f:
        loaded_results = json.load(f)

    print("\n" + "="*70)
    print("SIMULATION SUMMARY WITH INTERACTION MATRICES")
    print("="*70)

    print(f"\n📊 Data structure:")
    print(f"  • Intensity values: {len(loaded_results)} (from {u_list[0]:.2f} to {u_list[-1]:.2f})")
    print(f"  • Repetitions per intensity: {N_reps}")
    print(f"  • Total data points: {len(loaded_results) * N_reps}")
    print(f"  • Total interaction matrices: {len(loaded_results) * N_reps}")

    # Check first entry to verify matrices are stored
    first_u = list(loaded_results.keys())[0]
    first_rep = loaded_results[first_u]['rep_000']

    print(f"\n✓ Verification (u={first_u}, rep_000):")
    print(f"  • Single communities: {len(first_rep['sc_list'])}")
    print(f"  • Coalescence pairs: {len(first_rep['cc_list'])}")
    print(f"  • Interaction matrix shape: {len(first_rep['parameters']['interaction_matrix'])}×{len(first_rep['parameters']['interaction_matrix'][0])}")
    print(f"  • Growth rates length: {len(first_rep['parameters']['growth_rates'])}")
    print(f"  • Carrying capacities length: {len(first_rep['parameters']['carrying_capacities'])}")

    # Sample statistics
    I_example = np.array(first_rep['parameters']['interaction_matrix'])
    print(f"\n  Sample interaction matrix statistics:")
    print(f"    Diagonal (should be 1.0): {np.diag(I_example)[:5].tolist()}")
    print(f"    Off-diagonal mean: {first_rep['parameters']['interaction_matrix_stats']['mean']:.4f}")
    print(f"    Off-diagonal std: {first_rep['parameters']['interaction_matrix_stats']['std']:.4f}")

    print(f"\n📋 Data structure saved:")
    print(f"  • Top level: interaction strengths ({u_list[0]:.2f}, {u_list[1]:.2f}, ..., {u_list[-1]:.2f})")
    print(f"  • Second level: repetitions (rep_000 to rep_{N_reps-1:03d})")
    print(f"  • Third level: 'sc_list', 'cc_list', 'parameters'")
    print(f"  • Parameters now include:")
    print(f"    - interaction_matrix: 48×48 matrix")
    print(f"    - growth_rates: 48 values")
    print(f"    - carrying_capacities: 48 values")
    print(f"    - interaction_matrix_stats: mean, std, min, max")
    print(f"    - seed: for reproducibility")
    print(f"    - u: interaction strength")

    print(f"\n🎯 Ready for analysis!")
    print(f"   All interaction matrices are now stored and accessible.")


if __name__ == "__main__":
    simulate_48_species_200reps_fine_with_matrices()
