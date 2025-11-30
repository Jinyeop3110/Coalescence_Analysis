#!/usr/bin/env python
"""
Compare Coalescence vs Direct Assembly

Two assembly methods:
1. Coalescence: c1 alone → c2 alone → mix → final state
2. Direct Assembly: start with c1+c2 initial pool together → final state

Parameters match the updated mean_std_grid:
- Mean: 12 values from 0.1 to 1.2
- Std: 10 uniform points from 0 to 0.3464
- Reps: 50 per combination
- Total: 12 × 10 × 50 = 6000 simulations per method
"""

import numpy as np
import json
from scipy.integrate import odeint
from scipy.stats import truncnorm
import sys
import os
from datetime import datetime
import multiprocessing as mp
from functools import partial
import time

# Add current directory to path
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
    """Sample from truncated normal distribution N(mean, std²) with support [0, ∞)"""
    if std <= 0:
        return mean  # Degenerate case

    # Truncated normal: truncate at 0 (lower bound), no upper bound
    a = -mean / std  # Lower bound in standardized units
    b = np.inf  # No upper bound

    return truncnorm.rvs(a, b, loc=mean, scale=std)


def run_single_simulation(mean, std, rep, seed, method='coalescence'):
    """
    Run a single simulation with given parameters

    Parameters:
    -----------
    mean : float
        Mean of interaction strength distribution
    std : float
        Standard deviation of interaction strength distribution
    rep : int
        Replicate number
    seed : int
        Random seed
    method : str
        'coalescence' or 'direct'

    Returns:
    --------
    dict with results for both single communities and coalescence/direct assembly
    """
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

    # Store results
    sc_list = {}  # Single community outcomes
    cc_list = {}  # Coalescence or direct assembly outcomes

    # === Single Community Simulations (same for both methods) ===
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

    # === Pairwise Assembly (method-dependent) ===
    for i in range(N_communities):
        for j in range(i + 1, N_communities):

            if method == 'coalescence':
                # COALESCENCE: Grow separately, then mix
                # Get final states of both communities (already grown separately)
                y1 = np.array(sc_list[f"c{i+1}"])
                y2 = np.array(sc_list[f"c{j+1}"])

                # Mix communities (equal proportions)
                y_mix = (y1 + y2) / 2

                # Run to new steady state after mixing
                sol = odeint(gLV, y_mix, t, args=(I, g, k))
                y_final = sol[-1, :]

            elif method == 'direct':
                # DIRECT ASSEMBLY: Start with initial pool of both communities together
                start_idx_i = i * num_per_community
                end_idx_i = start_idx_i + num_per_community
                start_idx_j = j * num_per_community
                end_idx_j = start_idx_j + num_per_community

                # Initial condition: both communities present from the start
                y0_direct = np.zeros(N)
                # Use same random initial abundances as single community runs
                # but combine them directly
                np.random.seed(seed + i * 1000)  # Reproducible random for c_i
                y0_direct[start_idx_i:end_idx_i] = np.random.rand(num_per_community) * 0.1

                np.random.seed(seed + j * 1000)  # Reproducible random for c_j
                y0_direct[start_idx_j:end_idx_j] = np.random.rand(num_per_community) * 0.1

                # Run simulation from mixed initial state
                sol = odeint(gLV, y0_direct, t, args=(I, g, k))
                y_final = sol[-1, :]

            else:
                raise ValueError(f"Unknown method: {method}")

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
            "assembly_method": method,
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
    """Wrapper function for parallel execution"""
    mean, std, rep, seed, method = args
    key = f"mean{mean:.2f}_std{std:.4f}"
    rep_key = f"rep_{rep:03d}"

    result = run_single_simulation(mean, std, rep, seed, method)

    return (key, rep_key, result)


def save_checkpoint(all_results, output_dir, checkpoint_num, method):
    """Save intermediate checkpoint"""
    checkpoint_file = os.path.join(output_dir, f"checkpoint_{method}_{checkpoint_num}.json")
    with open(checkpoint_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    file_size_mb = os.path.getsize(checkpoint_file) / (1024 * 1024)
    return checkpoint_file, file_size_mb


def run_simulations_for_method(method):
    """Run all simulations for a given method"""

    print(f"\n{'='*70}")
    print(f"Running {method.upper()} simulations")
    print(f"{'='*70}")

    # Determine number of cores to use
    num_cores = mp.cpu_count()
    print(f"\nSystem information:")
    print(f"  Available CPU cores: {num_cores}")
    print(f"  Using {num_cores} cores for parallel execution")

    print(f"\nParameter Grid:")
    print(f"  Mean values: {len(mean_values)} values from {mean_values[0]:.2f} to {mean_values[-1]:.2f}")
    print(f"  Std values:  {len(std_values)} values from {std_values[0]:.4f} to {std_values[-1]:.4f}")
    print(f"  Grid size: {len(mean_values)} × {len(std_values)} = {len(mean_values) * len(std_values)} combinations")
    print(f"  Repetitions per combination: {N_reps}")

    total_sims = len(mean_values) * len(std_values) * N_reps
    print(f"\nTotal simulations: {total_sims:,}")
    print(f"Expected speedup: ~{num_cores}x faster than serial execution")
    print(f"Estimated time: ~{total_sims * 2 / 3600 / num_cores:.1f} hours (at 2 sec/simulation)")

    # Create output directory
    output_dir = f"Simulation_Data/coalescence_vs_direct_{N_reps}reps"
    os.makedirs(output_dir, exist_ok=True)

    # Check if data already exists
    output_file = os.path.join(output_dir, f"Community_{method}_{N_reps}reps.json")
    if os.path.exists(output_file):
        print(f"\n⚠️  WARNING: Output file already exists: {output_file}")
        response = input("Overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("Skipping this method.")
            return

    # Prepare all tasks
    print("\nPreparing simulation tasks...")
    tasks = []
    current_sim = 0
    for mean in mean_values:
        for std in std_values:
            for rep in range(N_reps):
                seed = base_seed + current_sim
                tasks.append((mean, std, rep, seed, method))
                current_sim += 1

    print(f"✓ Prepared {len(tasks)} tasks")

    # Initialize results dictionary
    all_results = {}
    for mean in mean_values:
        for std in std_values:
            key = f"mean{mean:.2f}_std{std:.4f}"
            all_results[key] = {}

    # Run simulations in parallel
    print(f"\n{'='*70}")
    print(f"Running {method} simulations in parallel...")
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

            # Save checkpoint every 500 simulations
            if completed % 500 == 0:
                print(f"\n  💾 Saving checkpoint at {completed} simulations...")
                checkpoint_file, file_size = save_checkpoint(all_results, output_dir, completed, method)
                print(f"     Saved: {checkpoint_file} ({file_size:.1f} MB)\n")

    # Save final results
    print(f"\n{'='*70}")
    print(f"Saving final results for {method}...")
    print(f"{'='*70}\n")

    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    total_time_min = (time.time() - start_time) / 60

    print(f"✓ Results saved to: {output_file}")
    print(f"✓ File size: {file_size_mb:.1f} MB")
    print(f"✓ Total time: {total_time_min:.1f} minutes")
    print(f"✓ Average time per simulation: {total_time_min * 60 / total_sims:.2f} seconds")


def main():
    print("="*70)
    print("48-Species Coalescence vs Direct Assembly Comparison")
    print("="*70)
    print("\nTwo assembly methods:")
    print("  1. COALESCENCE: c1 alone → c2 alone → mix → final state")
    print("  2. DIRECT: start with c1+c2 pool together → final state")
    print("="*70)

    # Run both methods
    run_simulations_for_method('coalescence')
    run_simulations_for_method('direct')

    print(f"\n{'='*70}")
    print("✓✓✓ ALL SIMULATIONS COMPLETE! ✓✓✓")
    print(f"{'='*70}\n")

    print("Output files:")
    output_dir = f"Simulation_Data/coalescence_vs_direct_{N_reps}reps"
    print(f"  Coalescence: {output_dir}/Community_coalescence_{N_reps}reps.json")
    print(f"  Direct:      {output_dir}/Community_direct_{N_reps}reps.json")


if __name__ == "__main__":
    main()
