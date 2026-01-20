#!/usr/bin/env python
"""
48 Species Simulation with 1000 Repetitions and Super-Fine Intensity Intervals

This script runs Lotka-Volterra simulations with:
- 48 total species
- 12 species per community
- 1000 independent repetitions per interaction strength
- 47 interaction strengths: 0.05 to 1.2 in steps of 0.025
- Each repetition initializes a new species pool

Time estimate: ~9.8x longer than 200reps_fine version
(47,000 simulations vs 4,800 simulations)

Usage:
python run_48species_1000reps_superfine.py
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


def simulate_48_species_1000reps_superfine():
    """Run the 48 species simulation with 1000 repetitions and super-fine intensity intervals."""

    # Simulation parameters for 48 species - 1000 repetitions, super-fine intervals
    session_name = "Simulation_Data/48species_1000reps_superfine"

    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")

    # Parameters
    N_reps = 1000  # Number of repetitions per interaction strength
    N = 48  # Total species pool
    num_S = 12  # Species per community
    num_C = 4  # Number of communities (48/12 = 4)

    # Super-fine intensity intervals: 0.05 to 1.2 in steps of 0.025
    u_list = np.arange(0.05, 1.225, 0.025)  # 0.05, 0.075, 0.10, ..., 1.20
    u_list = np.round(u_list, 3)  # Round to avoid floating point precision issues

    o = 0  # Offset parameter
    t = [0, 5000]  # Time span
    threshold = 1e-3  # Extinction threshold

    total_simulations = len(u_list) * N_reps

    print(f"\nSUPER-FINE INTERVAL SIMULATION CONFIGURATION:")
    print(f"=" * 60)
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Repetitions per intensity: {N_reps}")
    print(f"Interaction strength range: {u_list[0]:.3f} to {u_list[-1]:.3f}")
    print(f"Number of intensity values: {len(u_list)}")
    print(f"Intensity step size: 0.025")
    print(f"Total simulations: {total_simulations:,}")
    print(f"=" * 60)
    print(f"\nEstimated time: ~9.8x longer than 200reps_fine version")
    print(f"(If 200reps_fine took X hours, this will take ~10X hours)")

    # Check if we need to run the simulation
    output_file = session_name + '/Community_1000reps_superfine.json'

    # Check for existing checkpoint
    checkpoint_file = session_name + '/checkpoint.json'
    start_u_idx = 0
    start_rep = 0
    all_results = {}

    if os.path.isfile(checkpoint_file):
        print(f"\nFound checkpoint file: {checkpoint_file}")
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        start_u_idx = checkpoint.get('u_idx', 0)
        start_rep = checkpoint.get('rep', 0)
        print(f"Resuming from u_idx={start_u_idx} ({u_list[start_u_idx]:.3f}), rep={start_rep}")

        # Load existing results
        if os.path.isfile(output_file):
            with open(output_file, 'r') as f:
                all_results = json.load(f)
            print(f"Loaded {len(all_results)} existing intensity values")
    elif os.path.isfile(output_file):
        print(f"\nSimulation data already exists at: {output_file}")
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
        'u_range': f'{u_list[0]:.3f} to {u_list[-1]:.3f}',
        'u_step': 0.025,
        'o': o,
        't': t,
        'threshold': threshold,
        'simulation_type': 'superfine_intervals'
    }

    param_df = pd.DataFrame([params_dict])
    param_df.to_excel(f"{session_name}/parameter.xlsx", index=False)
    print(f"Parameters saved to: {session_name}/parameter.xlsx")

    print("\nStarting simulation...")
    start_time = time.time()

    # Run simulation
    total_tasks = len(u_list) * N_reps
    task_count = start_u_idx * N_reps + start_rep

    for i in range(start_u_idx, len(u_list)):
        u = u_list[i]
        u_key = f"{u:.3f}"

        print(f"\n{'='*70}")
        print(f"Processing interaction strength u = {u:.3f} ({i+1}/{len(u_list)})")
        print(f"{'='*70}")

        if u_key not in all_results:
            all_results[u_key] = {}

        # Determine starting rep for this u value
        rep_start = start_rep if i == start_u_idx else 0

        for rep in range(rep_start, N_reps):
            task_count += 1
            rep_start_time = time.time()

            # Progress indicator (less verbose for 1000 reps)
            if rep % 50 == 0 or rep == N_reps - 1:
                elapsed = time.time() - start_time
                rate = task_count / elapsed if elapsed > 0 else 0
                remaining = (total_tasks - task_count) / rate if rate > 0 else 0
                print(f"  Rep {rep+1}/{N_reps} | Overall: {task_count:,}/{total_tasks:,} ({100*task_count/total_tasks:.1f}%) | ETA: {remaining/3600:.1f}h")

            # Set unique random seed for each repetition
            seed = int(u * 100000) + rep * 1000000
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
            all_results[u_key][f"rep_{rep:04d}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list,
                "parameters": {
                    "seed": seed,
                    "u": u,
                    "interaction_matrix_stats": {
                        "mean": float(np.mean(I[np.triu_indices(N, k=1)])),
                        "std": float(np.std(I[np.triu_indices(N, k=1)]))
                    }
                }
            }

            # Save checkpoint every 100 repetitions
            if (rep + 1) % 100 == 0:
                # Save checkpoint
                with open(checkpoint_file, 'w') as f:
                    json.dump({'u_idx': i, 'rep': rep + 1}, f)

                # Save intermediate results
                with open(output_file, 'w') as f:
                    json.dump(all_results, f)

                if rep % 500 == 0:
                    print(f"    Checkpoint saved at rep {rep+1}")

        # Save after each intensity and clear checkpoint rep
        print(f"  Saving results after completing u = {u:.3f}...")
        with open(output_file, 'w') as f:
            json.dump(all_results, f)

        # Update checkpoint
        with open(checkpoint_file, 'w') as f:
            json.dump({'u_idx': i + 1, 'rep': 0}, f)

        # Reset start_rep for next u value
        start_rep = 0

    # Save final results
    print("\nSaving final results...")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    # Remove checkpoint file
    if os.path.isfile(checkpoint_file):
        os.remove(checkpoint_file)
        print("Checkpoint file removed.")

    end_time = time.time()
    total_time_hours = (end_time - start_time) / 3600

    print(f"\n{'='*70}")
    print(f"SIMULATION COMPLETED SUCCESSFULLY!")
    print(f"{'='*70}")
    print(f"Total time: {total_time_hours:.2f} hours ({(end_time - start_time)/60:.1f} minutes)")
    print(f"Data saved to: {output_file}")

    # Verify output and print summary statistics
    with open(output_file, 'r') as f:
        loaded_results = json.load(f)

    print(f"\nSUPER-FINE INTERVAL SIMULATION SUMMARY:")
    print(f"  Intensity values: {len(loaded_results)}")
    print(f"  Repetitions per intensity: {N_reps}")
    print(f"  Total data points: {len(loaded_results) * N_reps:,}")

    print(f"\nReady for phase diagram generation!")
    print(f"Use plot_phase_diagram_json_simulations.py with this data")


if __name__ == "__main__":
    simulate_48_species_1000reps_superfine()
