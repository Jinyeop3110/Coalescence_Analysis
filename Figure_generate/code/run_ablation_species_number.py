#!/usr/bin/env python
"""
Ablation Study: Species per Community Variation (PARALLELIZED)

This script runs Lotka-Volterra simulations with varying species per community:
- 6 species/comm:  24 total (4 communities × 6 species each)
- 9 species/comm:  36 total (4 communities × 9 species each)
- 12 species/comm: 48 total (4 communities × 12 species each) - baseline
- 24 species/comm: 96 total (4 communities × 24 species each)

Parameters:
- 200 independent repetitions per interaction strength
- 24 interaction strengths: 0.05 to 1.2 in steps of 0.05
- Uniform distribution U(0, 2*mu) for interaction strengths (CV = 1/sqrt(3))
- Parallel execution using multiprocessing

Usage:
conda activate coalescence
python run_ablation_species_number.py
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import multiprocessing as mp
from functools import partial
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scipy.integrate import odeint


def gLV_vectorized(y, t, I, g, k):
    """Vectorized Generalized Lotka-Volterra dynamics - much faster."""
    y = np.maximum(y, 0)  # Prevent negative abundances (numerical stability)
    dydt = y * g * (1 - np.dot(I, y) / k)
    return dydt


def run_lotka_volterra(y0, t, s_idx, I, g, k):
    """
    Run Lotka-Volterra simulation for a subset of species.
    Uses vectorized dynamics with odeint for speed.
    Only simulates surviving species to avoid numerical issues.
    """
    s_idx = np.where(s_idx)[0].tolist()
    N = len(y0)

    if len(s_idx) == 0:
        return np.zeros(N)

    y0_simul = y0[s_idx]
    I_simul = I[np.ix_(s_idx, s_idx)]
    g_simul = g[s_idx]
    k_simul = k[s_idx]

    t_eval = np.linspace(t[0], t[-1], 500)
    sol = odeint(gLV_vectorized, y0_simul, t_eval, args=(I_simul, g_simul, k_simul))
    y = sol[-1, :]

    y_out = np.zeros(N)
    for i in range(len(s_idx)):
        y_out[s_idx[i]] = y[i]
    return y_out


def uniform_distribution(mu):
    """
    Generate uniform random interaction strength with mean mu.
    U(0, 2*mu) has mean = mu and CV = 1/sqrt(3)
    """
    if mu <= 0:
        return 0.0
    return np.random.uniform(0, 2 * mu)


def run_single_simulation(args):
    """
    Run a single simulation with given parameters.
    Returns: (config_name, mu_str, rep_key, result_dict)
    """
    config_name, N, num_C, num_S, mu, rep, seed = args

    np.random.seed(seed)

    # Initialize interaction matrix
    I = np.eye(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                I[i, j] = uniform_distribution(mu)

    # Growth rates and carrying capacities (all 1.0)
    g = np.ones(N)
    k = np.ones(N)

    # Create non-overlapping communities
    CommunitiesLibrary = np.zeros((num_C, N))
    all_species = np.random.permutation(N)
    for c in range(num_C):
        start_idx = c * num_S
        end_idx = start_idx + num_S
        if end_idx <= N:
            CommunitiesLibrary[c, all_species[start_idx:end_idx]] = 1

    # Time span and threshold (matching original)
    t = [0, 5000]
    threshold = 1e-3

    # Initial abundances
    y0 = np.random.rand(N) * 0.1

    # Run single community simulations
    sc_list = {}
    for idx in range(num_C):
        y1 = run_lotka_volterra(y0, t, CommunitiesLibrary[idx, :], I, g, k)
        y1[y1 < threshold] = 0
        sc_list[idx] = y1.tolist()

    # Run coalescence simulations (all pairwise)
    cc_list = {}
    for idx in range(num_C):
        for jdx in range(idx + 1, num_C):
            y1 = np.array(sc_list[idx])
            y2 = np.array(sc_list[jdx])

            # Mix communities (equal proportions)
            y3 = (y1 + y2) / 2

            # Run to new steady state - only simulate surviving species!
            survived = y3 > threshold
            y3 = run_lotka_volterra(y3, t, survived, I, g, k)
            y3[y3 < threshold] = 0
            cc_list[f"{idx}_{jdx}"] = y3.tolist()

    # Calculate interaction matrix statistics
    off_diag = I[np.triu_indices(N, k=1)]

    result = {
        "sc_list": sc_list,
        "cc_list": cc_list,
        "parameters": {
            "seed": int(seed),
            "mu": float(mu),
            "N": N,
            "num_C": num_C,
            "num_S": num_S,
            "distribution": "uniform",
            "interaction_matrix_stats": {
                "mean": float(np.mean(off_diag)),
                "std": float(np.std(off_diag)),
                "min": float(np.min(off_diag)),
                "max": float(np.max(off_diag))
            }
        }
    }

    mu_str = f"{mu:.2f}"
    rep_key = f"rep_{rep:03d}"

    return (config_name, mu_str, rep_key, result)


def run_species_ablation():
    """Run the ablation study with different species numbers."""

    # Configuration for different species per community (4 communities each)
    # Named by species per community for clarity
    configs = [
        {"name": "4percomm", "N": 16, "num_C": 4, "num_S": 4},
        {"name": "6percomm", "N": 24, "num_C": 4, "num_S": 6},
        {"name": "9percomm", "N": 36, "num_C": 4, "num_S": 9},
        {"name": "12percomm", "N": 48, "num_C": 4, "num_S": 12},  # baseline
        {"name": "24percomm", "N": 96, "num_C": 4, "num_S": 24},
        {"name": "48percomm", "N": 192, "num_C": 4, "num_S": 48},
    ]

    # Parameters
    N_reps = 200
    mu_list = np.arange(0.05, 1.25, 0.05)
    mu_list = np.round(mu_list, 2)

    # Determine number of cores
    num_cores = mp.cpu_count()

    print("=" * 70)
    print("ABLATION STUDY: SPECIES NUMBER VARIATION (PARALLELIZED)")
    print("=" * 70)
    print(f"\nConfigurations:")
    for cfg in configs:
        print(f"  {cfg['name']}: {cfg['N']} species = {cfg['num_C']} communities × {cfg['num_S']} species")
    print(f"\nParameters:")
    print(f"  Distribution: U(0, 2*mu) with CV = 1/sqrt(3)")
    print(f"  Repetitions per intensity: {N_reps}")
    print(f"  Interaction strength range: {mu_list[0]:.2f} to {mu_list[-1]:.2f}")
    print(f"  Number of intensity values: {len(mu_list)}")
    print(f"\nSystem:")
    print(f"  Available CPU cores: {num_cores}")
    print(f"  Using {num_cores} cores for parallel execution")

    total_sims_per_config = len(mu_list) * N_reps
    total_sims = total_sims_per_config * len(configs)
    print(f"\nTotal simulations: {total_sims:,} ({total_sims_per_config:,} per config)")
    print("=" * 70)

    # Process each configuration
    for cfg in configs:
        config_name = cfg["name"]
        N = cfg["N"]
        num_C = cfg["num_C"]
        num_S = cfg["num_S"]

        session_name = f"Simulation_Data/{num_S}percomm_ablation_species_number"
        os.makedirs(session_name, exist_ok=True)

        output_file = f"{session_name}/Community_ablation_{config_name}.json"

        print(f"\n{'=' * 70}")
        print(f"Processing: {config_name}")
        print(f"  N={N}, Communities={num_C}, Species/Community={num_S}")
        print(f"  Output: {output_file}")
        print(f"{'=' * 70}")

        # Check if already exists
        if os.path.exists(output_file):
            print(f"  File already exists. Skipping...")
            continue

        # Save parameters
        params_dict = {
            'config_name': config_name,
            'N': N,
            'num_S': num_S,
            'num_C': num_C,
            'N_reps': N_reps,
            'mu_list': mu_list.tolist(),
            'distribution_type': 'uniform',
            'distribution_formula': 'U(0, 2*mu)',
            'CV': 1/np.sqrt(3)
        }
        param_df = pd.DataFrame([params_dict])
        param_df.to_excel(f"{session_name}/simulation_parameters.xlsx", index=False)

        # Prepare all tasks
        tasks = []
        base_seed = hash(config_name) % 1000000

        for mu_idx, mu in enumerate(mu_list):
            for rep in range(N_reps):
                seed = base_seed + mu_idx * 10000 + rep
                tasks.append((config_name, N, num_C, num_S, mu, rep, seed))

        print(f"  Prepared {len(tasks)} tasks")

        # Initialize results
        all_results = {f"{mu:.2f}": {} for mu in mu_list}

        # Run in parallel
        start_time = time.time()
        completed = 0

        with mp.Pool(processes=num_cores) as pool:
            for config_name_out, mu_str, rep_key, result in pool.imap_unordered(run_single_simulation, tasks, chunksize=10):
                all_results[mu_str][rep_key] = result
                completed += 1

                if completed % 100 == 0 or completed == len(tasks):
                    elapsed = time.time() - start_time
                    percent = 100 * completed / len(tasks)
                    speed = completed / elapsed if elapsed > 0 else 0
                    remaining = (len(tasks) - completed) / speed if speed > 0 else 0

                    print(f"  Progress: {completed}/{len(tasks)} ({percent:.1f}%) | "
                          f"Speed: {speed:.1f} sims/sec | "
                          f"ETA: {remaining/60:.1f} min")

                # Checkpoint every 500 simulations
                if completed % 500 == 0:
                    checkpoint_file = f"{session_name}/checkpoint_{config_name}_{completed}.json"
                    with open(checkpoint_file, 'w') as f:
                        json.dump(all_results, f)
                    print(f"  Checkpoint saved: {checkpoint_file}")

        # Save final results
        with open(output_file, 'w') as f:
            json.dump(all_results, f)

        elapsed = time.time() - start_time
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

        print(f"\n  Completed {config_name}!")
        print(f"  Time: {elapsed/60:.1f} minutes")
        print(f"  File size: {file_size_mb:.1f} MB")
        print(f"  Saved to: {output_file}")

        # Clean up checkpoints
        import glob
        for checkpoint in glob.glob(f"{session_name}/checkpoint_{config_name}_*.json"):
            os.remove(checkpoint)
            print(f"  Removed checkpoint: {checkpoint}")

    print("\n" + "=" * 70)
    print("SPECIES NUMBER ABLATION COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    for cfg in configs:
        output_file = f"Simulation_Data/{cfg['num_S']}percomm_ablation_species_number/Community_ablation_{cfg['name']}.json"
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"  {cfg['name']}: {size_mb:.1f} MB")
    print("\nNext step: python plot_phase_diagram_ablation_species_number.py")


if __name__ == "__main__":
    mp.set_start_method('fork', force=True)
    run_species_ablation()
