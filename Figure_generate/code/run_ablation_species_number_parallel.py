#!/usr/bin/env python
"""
Ablation Study: Species per Community Variation - PARALLELIZED SUPERFINE
High-resolution version with 59 interaction strengths (step 0.02)

This script runs Lotka-Volterra simulations with varying species per community:
- 4 species/comm:  16 total (4 communities × 4 species each)
- 6 species/comm:  24 total (4 communities × 6 species each)
- 9 species/comm:  36 total (4 communities × 9 species each)
- 12 species/comm: 48 total (4 communities × 12 species each) - baseline
- 24 species/comm: 96 total (4 communities × 24 species each)
- 48 species/comm: 192 total (4 communities × 48 species each)

Parameters:
- 400 independent repetitions per interaction strength (default)
- 59 interaction strengths: 0.05 to 1.21 in steps of 0.02 (default)
- Uniform distribution U(0, 2*mu) for interaction strengths (CV = 1/sqrt(3))
- Parallel execution using multiprocessing

Usage:
python run_ablation_species_number_parallel.py
python run_ablation_species_number_parallel.py --n_cores 10
python run_ablation_species_number_parallel.py --n_reps 400 --u_step 0.02
"""

import os
import sys
import json
import time
import argparse
import numpy as np
import pandas as pd
import multiprocessing as mp
import warnings
import glob

warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scipy.integrate import odeint


def gLV_vectorized(y, t, I, g, k):
    """Vectorized Generalized Lotka-Volterra dynamics."""
    y = np.maximum(y, 0)
    dydt = y * g * (1 - np.dot(I, y) / k)
    return dydt


def run_lotka_volterra_local(y0, t, s_idx, I, g, k):
    """Run Lotka-Volterra simulation for a subset of species."""
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
    """Generate uniform random interaction strength with mean mu."""
    if mu <= 0:
        return 0.0
    return np.random.uniform(0, 2 * mu)


def run_single_simulation(args):
    """Run a single simulation with given parameters."""
    config_name, N, num_C, num_S, mu, rep, seed = args

    np.random.seed(seed)

    # Initialize interaction matrix
    I = np.eye(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                I[i, j] = uniform_distribution(mu)

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

    t = [0, 5000]
    threshold = 1e-3
    y0 = np.random.rand(N) * 0.1

    # Run single community simulations
    sc_list = {}
    for idx in range(num_C):
        y1 = run_lotka_volterra_local(y0, t, CommunitiesLibrary[idx, :], I, g, k)
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
            y3 = run_lotka_volterra_local(y3, t, survived, I, g, k)
            y3[y3 < threshold] = 0
            cc_list[f"{idx}_{jdx}"] = y3.tolist()

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
                "std": float(np.std(off_diag))
            }
        }
    }

    mu_str = f"{mu:.2f}"
    rep_key = f"rep_{rep:03d}"

    return (config_name, mu_str, rep_key, result)


def run_species_ablation(n_cores=None, n_reps=400, u_step=0.02):
    """Run the ablation study with different species numbers."""

    if n_cores is None:
        n_cores = max(1, mp.cpu_count() - 1)

    # Configuration for different species per community
    configs = [
        {"name": "4percomm", "N": 16, "num_C": 4, "num_S": 4},
        {"name": "6percomm", "N": 24, "num_C": 4, "num_S": 6},
        {"name": "9percomm", "N": 36, "num_C": 4, "num_S": 9},
        {"name": "12percomm", "N": 48, "num_C": 4, "num_S": 12},  # baseline
        {"name": "24percomm", "N": 96, "num_C": 4, "num_S": 24},
        {"name": "48percomm", "N": 192, "num_C": 4, "num_S": 48},
    ]

    # Super-fine mu values
    mu_list = np.arange(0.05, 1.20 + u_step, u_step)
    mu_list = np.round(mu_list, 3)

    print("=" * 70)
    print("ABLATION STUDY: SPECIES NUMBER VARIATION - PARALLELIZED SUPERFINE")
    print("=" * 70)
    print(f"\nConfigurations:")
    for cfg in configs:
        print(f"  {cfg['name']}: {cfg['N']} species = {cfg['num_C']} communities × {cfg['num_S']} species")
    print(f"\nParameters:")
    print(f"  Distribution: U(0, 2*mu) with CV = 1/sqrt(3)")
    print(f"  Repetitions per intensity: {n_reps}")
    print(f"  Interaction strength range: {mu_list[0]:.3f} to {mu_list[-1]:.3f}")
    print(f"  Number of intensity values: {len(mu_list)}")
    print(f"  Step size: {u_step}")
    print(f"\nSystem:")
    print(f"  Using {n_cores} cores for parallel execution")

    total_sims_per_config = len(mu_list) * n_reps
    total_sims = total_sims_per_config * len(configs)
    print(f"\nTotal simulations: {total_sims:,} ({total_sims_per_config:,} per config)")
    print("=" * 70)

    # Process each configuration
    for cfg in configs:
        config_name = cfg["name"]
        N = cfg["N"]
        num_C = cfg["num_C"]
        num_S = cfg["num_S"]

        session_name = f"Simulation_Data/{num_S}percomm_ablation_species_number_superfine"
        os.makedirs(session_name, exist_ok=True)

        output_file = f"{session_name}/Community_ablation_{config_name}_superfine.json"

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
            'N_reps': n_reps,
            'mu_list': mu_list.tolist(),
            'u_step': u_step,
            'distribution_type': 'uniform',
            'distribution_formula': 'U(0, 2*mu)',
            'CV': 1/np.sqrt(3),
            'n_cores': n_cores
        }
        param_df = pd.DataFrame([params_dict])
        param_df.to_excel(f"{session_name}/parameter.xlsx", index=False)

        # Prepare all tasks
        tasks = []
        base_seed = hash(config_name + "_superfine") % 1000000

        for mu_idx, mu in enumerate(mu_list):
            for rep in range(n_reps):
                seed = base_seed + mu_idx * 10000 + rep
                tasks.append((config_name, N, num_C, num_S, mu, rep, seed))

        print(f"  Prepared {len(tasks):,} tasks")

        # Initialize results
        all_results = {f"{mu:.2f}": {} for mu in mu_list}

        # Run in parallel
        start_time = time.time()
        completed = 0

        with mp.Pool(processes=n_cores) as pool:
            for config_name_out, mu_str, rep_key, result in pool.imap_unordered(run_single_simulation, tasks, chunksize=10):
                all_results[mu_str][rep_key] = result
                completed += 1

                if completed % 500 == 0 or completed == len(tasks):
                    elapsed = time.time() - start_time
                    percent = 100 * completed / len(tasks)
                    speed = completed / elapsed if elapsed > 0 else 0
                    remaining = (len(tasks) - completed) / speed if speed > 0 else 0

                    print(f"  Progress: {completed}/{len(tasks)} ({percent:.1f}%) | "
                          f"Speed: {speed:.1f} sims/sec | "
                          f"ETA: {remaining/60:.1f} min")

                # Checkpoint every 2000 simulations
                if completed % 2000 == 0:
                    checkpoint_file = f"{session_name}/checkpoint_{config_name}_{completed}.json"
                    with open(checkpoint_file, 'w') as f:
                        json.dump(all_results, f)

        # Save final results
        with open(output_file, 'w') as f:
            json.dump(all_results, f)

        elapsed = time.time() - start_time
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

        print(f"\n  Completed {config_name}!")
        print(f"  Time: {elapsed/60:.1f} minutes ({elapsed/3600:.2f} hours)")
        print(f"  File size: {file_size_mb:.1f} MB")
        print(f"  Saved to: {output_file}")

        # Clean up checkpoints
        for checkpoint in glob.glob(f"{session_name}/checkpoint_{config_name}_*.json"):
            os.remove(checkpoint)
            print(f"  Removed checkpoint: {checkpoint}")

    print("\n" + "=" * 70)
    print("SPECIES NUMBER ABLATION COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    for cfg in configs:
        output_file = f"Simulation_Data/{cfg['num_S']}percomm_ablation_species_number_superfine/Community_ablation_{cfg['name']}_superfine.json"
        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"  {cfg['name']}: {size_mb:.1f} MB")


if __name__ == "__main__":
    mp.set_start_method('fork', force=True)
    parser = argparse.ArgumentParser(description='Run parallel Species Number ablation simulations')
    parser.add_argument('--n_cores', type=int, default=None,
                        help='Number of CPU cores to use (default: all-1)')
    parser.add_argument('--n_reps', type=int, default=400,
                        help='Number of repetitions per intensity (default: 400)')
    parser.add_argument('--u_step', type=float, default=0.02,
                        help='Interaction strength step size (default: 0.02)')
    args = parser.parse_args()

    run_species_ablation(n_cores=args.n_cores, n_reps=args.n_reps, u_step=args.u_step)
