#!/usr/bin/env python
"""
Run 48-species coalescence simulations with independent mean and std control
PARALLELIZED VERSION for faster execution with 500 reps

This script uses multiprocessing to run simulations in parallel across multiple CPU cores.
Significant speedup on multi-core machines (e.g., 8 cores → ~8x faster).

Key changes from serial version:
- Uses multiprocessing.Pool for parallel execution
- Processes multiple (mean, std, rep) combinations simultaneously
- Periodic checkpointing to avoid data loss
- Automatic core detection (uses all available cores by default)
"""

import numpy as np
import json
from scipy.integrate import odeint
from scipy.stats import truncnorm
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

# Parameter grid
mean_values = np.arange(0.1, 1.21, 0.1)  # 0.1, 0.2, ..., 1.2 (12 values)
std_values = np.linspace(0, 0.3464, 10)  # 10 uniform points from 0 to 0.3464

N_reps = 50  # Number of repetitions per (mean, std) combination
base_seed = 10000

# Integration parameters
t_start = 0
t_end = 2000
num_points = 500

# Extinction threshold
extinction_threshold = 1e-4


def truncated_normal_distribution(mean, std):
    """
    Sample from truncated normal distribution N(mean, std²) with support [0, ∞)
    """
    if std <= 0:
        return mean  # Degenerate case

    # Truncated normal: truncate at 0 (lower bound), no upper bound
    a = -mean / std  # Lower bound in standardized units
    b = np.inf  # No upper bound

    return truncnorm.rvs(a, b, loc=mean, scale=std)


def run_single_simulation(mean, std, rep, seed):
    """Run a single simulation with given parameters"""
    np.random.seed(seed)

    # Initialize interaction matrix with diagonal = 1.0
    I = np.eye(N)

    # Fill off-diagonal elements with truncated normal distribution
    for i in range(N):
        for j in range(N):
            if i != j:
                I[i, j] = truncated_normal_distribution(mean, std)

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
            "target_std": float(std),
            "target_cv": float(std / mean) if mean > 0 else 0,
            "distribution": "truncated_normal",
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
    mean, std, rep, seed = args
    key = f"mean{mean:.2f}_std{std:.2f}"
    rep_key = f"rep_{rep:03d}"

    result = run_single_simulation(mean, std, rep, seed)

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
    print("48-Species Coalescence Simulation - Mean × Std Grid (PARALLELIZED)")
    print("Distribution: Truncated Normal N(mean, std²) with support [0, ∞)")
    print("="*70)

    # Determine number of cores to use
    num_cores = mp.cpu_count()
    print(f"\nSystem information:")
    print(f"  Available CPU cores: {num_cores}")
    print(f"  Using {num_cores} cores for parallel execution")

    print(f"\nParameter Grid:")
    print(f"  Mean values: {len(mean_values)} values from {mean_values[0]:.1f} to {mean_values[-1]:.1f}")
    print(f"  Std values:  {len(std_values)} values from {std_values[0]:.2f} to {std_values[-1]:.2f}")
    print(f"  Grid size: {len(mean_values)} × {len(std_values)} = {len(mean_values) * len(std_values)} combinations")
    print(f"  Repetitions per combination: {N_reps}")

    total_sims = len(mean_values) * len(std_values) * N_reps
    print(f"\nTotal simulations: {total_sims:,}")
    print(f"Expected speedup: ~{num_cores}x faster than serial execution")
    print(f"Estimated time: ~{total_sims * 2 / 3600 / num_cores:.1f} hours (at 2 sec/simulation)")
    print(f"Base seed: {base_seed}\n")

    # Create output directory
    output_dir = f"Simulation_Data/mean_std_grid_{N_reps}reps"
    os.makedirs(output_dir, exist_ok=True)

    # Check if data already exists
    output_file = os.path.join(output_dir, f"Community_mean_std_grid_{N_reps}reps.json")
    if os.path.exists(output_file):
        print(f"⚠️  WARNING: Output file already exists: {output_file}")
        response = input("Do you want to overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("Exiting without running simulation.")
            return

    # Prepare all tasks (mean, std, rep, seed)
    print("Preparing simulation tasks...")
    tasks = []
    current_sim = 0
    for mean in mean_values:
        for std in std_values:
            for rep in range(N_reps):
                seed = base_seed + current_sim
                tasks.append((mean, std, rep, seed))
                current_sim += 1

    print(f"✓ Prepared {len(tasks)} tasks")

    # Initialize results dictionary
    all_results = {}
    for mean in mean_values:
        for std in std_values:
            key = f"mean{mean:.2f}_std{std:.2f}"
            all_results[key] = {}

    # Run simulations in parallel
    print(f"\n{'='*70}")
    print("Running simulations in parallel...")
    print(f"{'='*70}\n")

    start_time = time.time()
    completed = 0
    checkpoint_interval = 500  # Save checkpoint every 500 simulations

    with mp.Pool(processes=num_cores) as pool:
        # Use imap_unordered for better progress tracking
        for key, rep_key, result in pool.imap_unordered(run_simulation_wrapper, tasks, chunksize=10):
            # Store result
            all_results[key][rep_key] = result

            completed += 1

            # Progress reporting
            if completed % 50 == 0 or completed == total_sims:
                elapsed = time.time() - start_time
                avg_time = elapsed / completed
                remaining = (total_sims - completed) * avg_time
                percent = 100 * completed / total_sims

                print(f"Progress: {completed}/{total_sims} ({percent:.1f}%) | "
                      f"Elapsed: {elapsed/60:.1f} min | "
                      f"Remaining: {remaining/60:.1f} min | "
                      f"Speed: {completed/elapsed:.1f} sims/sec")

            # Periodic checkpointing
            if completed % checkpoint_interval == 0:
                print(f"\n  💾 Saving checkpoint at {completed} simulations...")
                checkpoint_file, file_size = save_checkpoint(all_results, output_dir, completed)
                print(f"     Saved: {checkpoint_file} ({file_size:.1f} MB)\n")

    total_time = time.time() - start_time

    # Save final results
    print("\n" + "="*70)
    print("Saving final results...")

    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"✓ Saved to: {output_file}")
    print(f"✓ File size: {file_size_mb:.1f} MB")

    # Save parameters summary
    params_data = []
    for mean in mean_values:
        for std in std_values:
            for rep in range(N_reps):
                seed = base_seed + len(params_data)
                params_data.append({
                    "mean": mean,
                    "std": std,
                    "cv": std / mean if mean > 0 else 0,
                    "rep": rep,
                    "seed": seed,
                    "distribution": "truncated_normal",
                    "support": "[0, ∞)"
                })

    params_df = pd.DataFrame(params_data)
    params_file = os.path.join(output_dir, "simulation_parameters.xlsx")
    params_df.to_excel(params_file, index=False)
    print(f"✓ Parameters saved to: {params_file}")

    # Create parameter grid summary
    grid_summary = []
    for mean in mean_values:
        for std in std_values:
            grid_summary.append({
                "mean": mean,
                "std": std,
                "cv": std / mean if mean > 0 else 0,
                "n_reps": N_reps
            })

    grid_df = pd.DataFrame(grid_summary)
    grid_file = os.path.join(output_dir, "parameter_grid.xlsx")
    grid_df.to_excel(grid_file, index=False)
    print(f"✓ Grid summary saved to: {grid_file}")

    # Print final summary
    print("\n" + "="*70)
    print("SIMULATION COMPLETE!")
    print("="*70)
    print(f"Total simulations run: {total_sims:,}")
    print(f"Total time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
    print(f"Average time per simulation: {total_time/total_sims:.2f} seconds")
    print(f"Effective speedup: ~{(total_sims * 2) / total_time:.1f}x")
    print(f"Throughput: {total_sims / total_time:.2f} simulations/second")
    print("="*70)


if __name__ == "__main__":
    # Ensure proper multiprocessing behavior on macOS
    mp.set_start_method('fork', force=True)
    main()
