#!/usr/bin/env python
"""
Run 48-species coalescence simulations with uniform distribution
PARALLELIZED VERSION for faster execution with 500 reps

Distribution: Uniform[0, 2*u] where u is the mean interaction strength
This gives a uniform distribution with mean = u and support [0, 2u]

Key parameters:
- Mean values (u): 0.0 to 1.2 in 0.1 increments (13 values)
- Each interaction drawn from Uniform[0, 2u]
"""

import numpy as np
import json
from scipy.integrate import odeint
import sys
import os
from datetime import datetime
import pandas as pd
import multiprocessing as mp
from functools import partial
import time

# Add current directory to path to import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from LV import gLV
from common_setup import metric_VectorDecomposition_onlyPositive

# ===== SIMULATION PARAMETERS =====
N = 48  # Total number of species
num_per_community = 12  # Species per community
N_communities = 4  # Number of communities

# Parameter grid - mean values from 0.0 to 1.2
mean_values = np.arange(0.0, 1.21, 0.1)  # 0.0, 0.1, 0.2, ..., 1.2 (13 values)

N_reps = 100  # Number of repetitions per mean value
base_seed = 10000

# Integration parameters
t_start = 0
t_end = 2000
num_points = 500

# Extinction threshold
extinction_threshold = 1e-4


def uniform_interaction_strength(mean):
    """
    Sample from uniform distribution [0, 2*mean]
    This gives E[X] = mean and support [0, 2*mean]
    """
    if mean <= 0:
        return 0
    return np.random.uniform(0, 2 * mean)


def run_single_simulation(mean, rep, seed):
    """Run a single simulation with given parameters"""
    np.random.seed(seed)

    # Initialize interaction matrix with diagonal = 1.0
    I = np.eye(N)

    # Fill off-diagonal elements with uniform distribution [0, 2*mean]
    for i in range(N):
        for j in range(N):
            if i != j:
                I[i, j] = uniform_interaction_strength(mean)

    # Growth rates and carrying capacities (all 1.0)
    g = np.ones(N)
    k = np.ones(N)

    # Time points
    t = np.linspace(t_start, t_end, num_points)

    # Store results for different community combinations
    sc_list = {}  # Single community outcomes
    cc_list = {}  # Coalescence outcomes (pairwise)

    # === Single Community Simulations ===
    for comm_idx in range(N_communities):
        start_idx = comm_idx * num_per_community
        end_idx = start_idx + num_per_community

        # Initial condition: only this community present
        y0 = np.zeros(N)
        y0[start_idx:end_idx] = np.random.rand(num_per_community) * 0.1

        # Run simulation
        sol = odeint(gLV, y0, t, args=(I, g, k))
        y_final = sol[-1, :]

        # Apply extinction threshold
        y_final[y_final < extinction_threshold] = 0

        sc_list[f"c{comm_idx+1}"] = y_final.tolist()

    # === Coalescence Simulations (all pairwise) ===
    for i in range(N_communities):
        for j in range(i + 1, N_communities):
            # Get final states of both communities
            y1 = np.array(sc_list[f"c{i+1}"])
            y2 = np.array(sc_list[f"c{j+1}"])

            # Mix communities (equal proportions)
            y_mix = (y1 + y2) / 2

            # Determine which species survive the mixing
            survived = y_mix > extinction_threshold

            # Run to new steady state
            sol = odeint(gLV, y_mix, t, args=(I, g, k))
            y_final = sol[-1, :]

            # Apply extinction threshold
            y_final[y_final < extinction_threshold] = 0

            cc_list[f"c{i+1}_c{j+1}"] = y_final.tolist()

    # Calculate empirical statistics of the interaction matrix
    off_diag = I[np.triu_indices(N, k=1)]
    empirical_mean = np.mean(off_diag)
    empirical_std = np.std(off_diag)
    empirical_cv = empirical_std / empirical_mean if empirical_mean > 0 else 0

    return {
        "sc_list": sc_list,
        "cc_list": cc_list,
        "parameters": {
            "seed": int(seed),
            "target_mean": float(mean),
            "distribution": "uniform",
            "distribution_support": f"[0, {2*mean:.2f}]",
            "interaction_matrix": I.tolist(),
            "growth_rates": g.tolist(),
            "carrying_capacities": k.tolist(),
            "interaction_matrix_stats": {
                "empirical_mean": float(empirical_mean),
                "empirical_std": float(empirical_std),
                "empirical_cv": float(empirical_cv),
                "min": float(np.min(off_diag)),
                "max": float(np.max(off_diag))
            }
        }
    }


def run_simulation_wrapper(args):
    """
    Wrapper function for parallel execution.
    Returns: (key, rep_key, result)
    """
    mean, rep, seed = args
    key = f"mean{mean:.2f}"
    rep_key = f"rep_{rep:03d}"

    result = run_single_simulation(mean, rep, seed)

    return (key, rep_key, result)


def save_checkpoint(all_results, output_dir, checkpoint_num):
    """Save intermediate checkpoint"""
    checkpoint_file = os.path.join(output_dir, f"checkpoint_{checkpoint_num}.json")
    with open(checkpoint_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    file_size_mb = os.path.getsize(checkpoint_file) / (1024 * 1024)
    return checkpoint_file, file_size_mb


def main():
    print("="*70)
    print("48-Species Coalescence Simulation - Mean Grid (PARALLELIZED)")
    print("Distribution: Uniform[0, 2u] where u is the mean")
    print("="*70)

    # Determine number of cores to use
    num_cores = mp.cpu_count()
    print(f"\nSystem information:")
    print(f"  Available CPU cores: {num_cores}")
    print(f"  Using {num_cores} cores for parallel execution")

    print(f"\nParameter Grid:")
    print(f"  Mean values: {len(mean_values)} values from {mean_values[0]:.1f} to {mean_values[-1]:.1f}")
    print(f"  Grid size: {len(mean_values)} combinations")
    print(f"  Repetitions per combination: {N_reps}")

    total_sims = len(mean_values) * N_reps
    print(f"\nTotal simulations: {total_sims:,}")
    print(f"Expected speedup: ~{num_cores}x faster than serial execution")
    print(f"Estimated time: ~{total_sims * 2 / 3600 / num_cores:.1f} hours (at 2 sec/simulation)")
    print(f"Base seed: {base_seed}\n")

    # Create output directory
    output_dir = f"Simulation_Data/mean_uniform_grid_{N_reps}reps"
    os.makedirs(output_dir, exist_ok=True)

    # Check if data already exists
    output_file = os.path.join(output_dir, f"Community_mean_uniform_grid_{N_reps}reps.json")
    if os.path.exists(output_file):
        print(f"⚠️  WARNING: Output file already exists: {output_file}")
        print("Exiting without running simulation.")
        return

    # Prepare all tasks (mean, rep, seed)
    print("Preparing simulation tasks...")
    tasks = []
    current_sim = 0
    for mean in mean_values:
        for rep in range(N_reps):
            seed = base_seed + current_sim
            tasks.append((mean, rep, seed))
            current_sim += 1

    print(f"✓ Prepared {len(tasks)} tasks")

    # Initialize results dictionary
    all_results = {}
    for mean in mean_values:
        key = f"mean{mean:.2f}"
        all_results[key] = {}

    # Run simulations in parallel
    print(f"\n{'='*70}")
    print("Running simulations in parallel...")
    print(f"{'='*70}\n")

    start_time = time.time()
    completed = 0

    with mp.Pool(processes=num_cores) as pool:
        for key, rep_key, result in pool.imap_unordered(run_simulation_wrapper, tasks):
            all_results[key][rep_key] = result
            completed += 1

            # Progress update every 100 simulations
            if completed % 100 == 0 or completed == total_sims:
                elapsed_sec = time.time() - start_time
                elapsed_min = elapsed_sec / 60
                rate = completed / elapsed_sec if elapsed_sec > 0 else 0
                remaining = total_sims - completed
                eta_min = remaining / rate / 60 if rate > 0 else 0

                print(f"Progress: {completed}/{total_sims} ({100*completed/total_sims:.1f}%) | "
                      f"Elapsed: {elapsed_min:.1f} min | Remaining: {eta_min:.1f} min | "
                      f"Speed: {rate:.1f} sims/sec")

            # Save checkpoint every 1000 simulations (reduced to save disk space)
            if completed % 1000 == 0:
                print(f"\n  💾 Saving checkpoint at {completed} simulations...")
                checkpoint_file, file_size = save_checkpoint(all_results, output_dir, completed)
                print(f"     Saved: {checkpoint_file} ({file_size:.1f} MB)\n")

    # Save final results
    print(f"\n{'='*70}")
    print("Saving final results...")
    print(f"{'='*70}\n")

    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    total_time_min = (time.time() - start_time) / 60

    print(f"✓ Results saved to: {output_file}")
    print(f"✓ File size: {file_size_mb:.1f} MB")
    print(f"✓ Total time: {total_time_min:.1f} minutes")
    print(f"✓ Average time per simulation: {total_time_min * 60 / total_sims:.2f} seconds")

    print(f"\n{'='*70}")
    print("✓✓✓ SIMULATION COMPLETE! ✓✓✓")
    print(f"{'='*70}\n")

    # Print summary statistics
    print("Summary Statistics:")
    print(f"  Total mean values tested: {len(mean_values)}")
    print(f"  Repetitions per mean: {N_reps}")
    print(f"  Total simulations: {total_sims:,}")
    print(f"  Distribution: Uniform[0, 2u]")
    print(f"  Mean range: [{mean_values[0]:.1f}, {mean_values[-1]:.1f}]")


if __name__ == "__main__":
    main()
