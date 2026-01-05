#!/usr/bin/env python
"""
Ablation Study: Growth Rate Heterogeneity with std=0.1

This script runs Lotka-Volterra simulations with:
- 48 total species
- 12 species per community
- 200 independent repetitions per interaction strength
- 24 interaction strengths: 0.05 to 1.2 in steps of 0.05
- Uniform interaction distribution (same as baseline)
- Intrinsic growth rate: N(1, 0.1^2), clipped to 0 if negative
  - Mean = 1
  - Std = 0.1
  - CV = 0.1

Usage:
conda activate coalescence
python run_ablation_growth_rate_std01.py
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


def uniform_distribution(mu):
    """
    Generate Uniform random interaction strength (baseline distribution).
    Uniform[0, 2*mu] has mean = mu.
    """
    return np.random.uniform(0, 2 * mu)


def growth_rate_gaussian_std01():
    """
    Generate Gaussian random growth rate with mean=1, std=0.1.
    Clips negative values to 0.
    """
    g = np.random.normal(1.0, 0.1)
    return max(0.0, g)


def InitializeRandomCommunityPool_48(N, num_C, num_S, save_path="Data/test"):
    """
    Initialize random non-overlapping communities for 48 species pool.
    Creates 4 communities of 12 species each.
    """
    CommunitiesLibrary = np.zeros([num_C, N])
    all_species = np.random.permutation(N)

    for i in range(num_C):
        start_idx = i * num_S
        end_idx = start_idx + num_S

        if end_idx <= N:
            selected_species = all_species[start_idx:end_idx]
            CommunitiesLibrary[i, selected_species] = 1
        else:
            print(f"Warning: Not enough species for community {i}")
            break

    df1 = pd.DataFrame(CommunitiesLibrary)
    with pd.ExcelWriter(save_path + '/communityLibrary.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Sheet1')

    return CommunitiesLibrary


def simulate_ablation_growth_rate():
    """Run the ablation study with growth rate heterogeneity (std=0.1)."""

    session_name = "Simulation_Data/48species_ablation_growth_std01"

    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")

    # Parameters
    N_reps = 200
    N = 48
    num_S = 12
    num_C = 4

    mu_list = np.arange(0.05, 1.25, 0.05)
    mu_list = np.round(mu_list, 2)

    t = [0, 5000]
    threshold = 1e-3

    print(f"\n" + "="*70)
    print("ABLATION STUDY: GROWTH RATE HETEROGENEITY (std=0.1)")
    print("="*70)
    print(f"Growth rate distribution: N(1, 0.1^2), clipped to 0 if negative")
    print(f"Interaction distribution: Uniform[0, 2*mu] (baseline)")
    print(f"="*70)
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Repetitions per intensity: {N_reps}")
    print(f"Mean interaction strength range: {mu_list[0]:.2f} to {mu_list[-1]:.2f}")
    print(f"Number of intensity values: {len(mu_list)}")
    print(f"Total simulations: {len(mu_list) * N_reps}")
    print(f"="*70)

    output_file = session_name + '/Community_ablation_growth_std01.json'
    if os.path.isfile(output_file):
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
        'mu_list': mu_list.tolist(),
        'mu_range': f'{mu_list[0]:.2f} to {mu_list[-1]:.2f}',
        'mu_step': 0.05,
        't': t,
        'threshold': threshold,
        'growth_rate_distribution': 'N(1, 0.1^2)',
        'growth_rate_mean': 1.0,
        'growth_rate_std': 0.1,
        'interaction_distribution': 'Uniform[0, 2*mu]'
    }

    param_df = pd.DataFrame([params_dict])
    param_df.to_excel(f"{session_name}/simulation_parameters.xlsx", index=False)
    print(f"Parameters saved to: {session_name}/simulation_parameters.xlsx")

    print("\nStarting simulation...")
    start_time = time.time()

    all_results = {}
    total_tasks = len(mu_list) * N_reps
    task_count = 0

    for i, mu in enumerate(mu_list):
        print(f"\n{'='*70}")
        print(f"Processing mean interaction strength mu = {mu:.2f} ({i+1}/{len(mu_list)})")
        print(f"{'='*70}")

        all_results[f"{mu:.2f}"] = {}

        for rep in range(N_reps):
            task_count += 1

            if rep % 20 == 0:
                elapsed = time.time() - start_time
                avg_time_per_task = elapsed / task_count if task_count > 0 else 0
                remaining_tasks = total_tasks - task_count
                eta_seconds = avg_time_per_task * remaining_tasks
                eta_minutes = eta_seconds / 60

                print(f"\n  Rep {rep+1}/{N_reps} | Overall: {task_count}/{total_tasks} ({100*task_count/total_tasks:.1f}%)")
                print(f"    ETA: {eta_minutes:.1f} minutes")

            # Set unique random seed
            seed = int(mu * 10000) + rep * 100000 + 3000000
            np.random.seed(seed)

            # Initialize species pool with heterogeneous growth rates
            I, g, k = InitializeSpeceiesPool(N,
                                           lambda: uniform_distribution(mu),
                                           f_g=growth_rate_gaussian_std01,
                                           f_k=lambda: 1,
                                           is_diagonal_one=True,
                                           save_path=session_name)

            CommunitiesLibrary = InitializeRandomCommunityPool_48(N, num_C, num_S,
                                                                  save_path=session_name)

            y = np.random.rand(N) * 0.1

            # Run single community simulations
            sc_list = {}
            for idx in range(num_C):
                y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
                y1[y1 < threshold] = 0
                sc_list[idx] = y1.tolist()

            # Run coalescence simulations
            cc_list = {}
            for idx in range(num_C):
                for jdx in range(idx + 1, num_C):
                    y1 = np.array(sc_list[idx])
                    y2 = np.array(sc_list[jdx])
                    y3 = (y1 + y2) / 2
                    survived = y3 > threshold
                    y3 = run_lotka_volterra(y3, t, survived, I, g, k)
                    y3[y3 < threshold] = 0
                    cc_list[f"{idx}_{jdx}"] = y3.tolist()

            # Store results
            off_diag = I[np.triu_indices(N, k=1)]
            all_results[f"{mu:.2f}"][f"rep_{rep:03d}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list,
                "parameters": {
                    "seed": seed,
                    "mu": mu,
                    "growth_rate_stats": {
                        "mean": float(np.mean(g)),
                        "std": float(np.std(g)),
                        "min": float(np.min(g)),
                        "max": float(np.max(g))
                    },
                    "interaction_matrix_stats": {
                        "mean": float(np.mean(off_diag)),
                        "std": float(np.std(off_diag)),
                        "min": float(np.min(off_diag)),
                        "max": float(np.max(off_diag))
                    }
                }
            }

            if (rep + 1) % 50 == 0:
                print(f"\n  Saving intermediate results (rep {rep+1})...")
                with open(output_file, 'w') as f:
                    json.dump(all_results, f)

        print(f"\nSaving results after completing mu = {mu:.2f}...")
        with open(output_file, 'w') as f:
            json.dump(all_results, f)

    print("\nSaving final results...")
    with open(output_file, 'w') as f:
        json.dump(all_results, f)

    end_time = time.time()
    total_time = (end_time - start_time) / 60

    print(f"\n{'='*70}")
    print("GROWTH RATE ABLATION (std=0.1) SIMULATION COMPLETED!")
    print(f"{'='*70}")
    print(f"Total time: {total_time:.1f} minutes ({total_time/60:.2f} hours)")
    print(f"Data saved to: {output_file}")

    with open(output_file, 'r') as f:
        loaded_results = json.load(f)

    print(f"\nData structure:")
    print(f"  Intensity values: {len(loaded_results)}")
    print(f"  Repetitions per intensity: {N_reps}")
    print(f"  Total data points: {len(loaded_results) * N_reps}")

    print(f"\nReady for phase diagram generation!")
    print(f"Use: python plot_phase_diagram_ablation_growth_rate.py")


if __name__ == "__main__":
    simulate_ablation_growth_rate()
