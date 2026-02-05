#!/usr/bin/env python
"""
Ablation Study: Carrying Capacity Heterogeneity with std=0.2 - PARALLELIZED
High-resolution version with 59 interaction strengths (step 0.02)

This script runs Lotka-Volterra simulations with:
- 48 total species
- 12 species per community
- 400 independent repetitions per interaction strength (default)
- 59 interaction strengths: 0.05 to 1.21 in steps of 0.02 (default)
- Uniform interaction distribution (same as baseline)
- Carrying capacity: N(1, 0.2^2), clipped to >0.01

Usage:
python run_ablation_carrying_capacity_std02_parallel.py
python run_ablation_carrying_capacity_std02_parallel.py --n_cores 10
"""

import os
import sys
import json
import time
import argparse
import numpy as np
import pandas as pd
import warnings
import multiprocessing as mp

warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from LV import run_lotka_volterra


def uniform_distribution(mu):
    """Generate Uniform random interaction strength (baseline distribution)."""
    return np.random.uniform(0, 2 * mu)


def run_single_repetition(args):
    """Run a single repetition for a given interaction strength."""
    u, rep, N, num_S, num_C, t, threshold, k_std, session_name = args

    seed = int(u * 10000) + rep * 100000 + 4500000  # Offset for carrying capacity std02
    np.random.seed(seed)

    # Initialize interaction matrix with Uniform distribution
    I = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            I[i, j] = uniform_distribution(u)
    for i in range(N):
        I[i, i] = 1

    g = np.ones(N)

    # Heterogeneous carrying capacities: N(1, k_std^2), clipped to >0.01
    k = np.random.normal(1.0, k_std, N)
    k = np.maximum(k, 0.01)

    # Create random communities
    CommunitiesLibrary = np.zeros([num_C, N])
    all_species = np.random.permutation(N)
    for i in range(num_C):
        start_idx = i * num_S
        end_idx = start_idx + num_S
        if end_idx <= N:
            selected_species = all_species[start_idx:end_idx]
            CommunitiesLibrary[i, selected_species] = 1

    y = np.random.rand(N) * 0.1

    sc_list = {}
    for idx in range(num_C):
        y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
        y1[y1 < threshold] = 0
        sc_list[idx] = y1.tolist()

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

    return {
        'u': u,
        'rep': rep,
        'sc_list': sc_list,
        'cc_list': cc_list,
        'parameters': {
            'seed': seed,
            'u': u,
            'distribution': 'uniform',
            'carrying_capacity_std': k_std,
            'carrying_capacity_stats': {
                'mean': float(np.mean(k)),
                'std': float(np.std(k))
            },
            'interaction_matrix_stats': {
                'mean': float(np.mean(I[np.triu_indices(N, k=1)])),
                'std': float(np.std(I[np.triu_indices(N, k=1)]))
            }
        }
    }


def simulate_parallel(n_cores=None, n_reps=400, u_step=0.02, k_std=0.2):
    """Run the Carrying Capacity ablation simulation with parallelization."""

    if n_cores is None:
        n_cores = max(1, mp.cpu_count() - 1)

    print(f"\nUsing {n_cores} CPU cores for parallel execution")

    session_name = f"Simulation_Data/48species_ablation_k_std02_superfine"

    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")

    N = 48
    num_S = 12
    num_C = 4
    t = [0, 5000]
    threshold = 1e-3

    u_list = np.arange(0.05, 1.20 + u_step, u_step)
    u_list = np.round(u_list, 3)

    total_simulations = len(u_list) * n_reps

    print(f"\nCARRYING CAPACITY ABLATION (std={k_std}) - PARALLELIZED SUPERFINE:")
    print(f"=" * 60)
    print(f"Carrying capacity distribution: N(1, {k_std}^2)")
    print(f"Interaction distribution: Uniform[0, 2*mu]")
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Repetitions per intensity: {n_reps}")
    print(f"Interaction strength range: {u_list[0]:.3f} to {u_list[-1]:.3f}")
    print(f"Number of intensity values: {len(u_list)}")
    print(f"Total simulations: {total_simulations:,}")
    print(f"Parallel cores: {n_cores}")
    print(f"=" * 60)

    output_file = f"{session_name}/Community_ablation_k_std02_superfine.json"

    if os.path.isfile(output_file):
        print(f"\nSimulation data already exists at: {output_file}")
        user_input = input("Do you want to overwrite? (y/n): ")
        if user_input.lower() != 'y':
            print("Exiting without running simulation.")
            return

    params_dict = {
        'N': N, 'num_S': num_S, 'num_C': num_C, 'N_reps': n_reps,
        'u_list': u_list.tolist(), 'u_step': u_step,
        'carrying_capacity_distribution': f'N(1, {k_std}^2)',
        'carrying_capacity_std': k_std,
        'interaction_distribution': 'Uniform[0, 2*mu]',
        'n_cores': n_cores
    }
    param_df = pd.DataFrame([params_dict])
    param_df.to_excel(f"{session_name}/parameter.xlsx", index=False)

    print("\nStarting parallel simulation...")
    start_time = time.time()

    all_results = {}

    for i, u in enumerate(u_list):
        u_key = f"{u:.2f}"
        print(f"\n{'='*70}")
        print(f"Processing u = {u:.3f} ({i+1}/{len(u_list)})")
        print(f"{'='*70}")

        batch_start = time.time()

        args_list = [(u, rep, N, num_S, num_C, t, threshold, k_std, session_name) for rep in range(n_reps)]

        with mp.Pool(processes=n_cores) as pool:
            results = pool.map(run_single_repetition, args_list)

        all_results[u_key] = {}
        for result in results:
            if result is not None:
                rep = result['rep']
                all_results[u_key][f"rep_{rep:03d}"] = {
                    'sc_list': result['sc_list'],
                    'cc_list': result['cc_list'],
                    'parameters': result['parameters']
                }

        batch_time = time.time() - batch_start
        elapsed = time.time() - start_time
        remaining_u = len(u_list) - i - 1
        eta = (elapsed / (i + 1)) * remaining_u if i > 0 else 0

        print(f"  Completed {n_reps} simulations in {batch_time:.1f}s")
        print(f"  Elapsed: {elapsed/60:.1f}min | ETA: {eta/60:.1f}min")

        with open(output_file, 'w') as f:
            json.dump(all_results, f)

    print("\nSaving final results...")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    total_time_hours = (time.time() - start_time) / 3600
    print(f"\n{'='*70}")
    print(f"CARRYING CAPACITY ABLATION (std={k_std}) COMPLETED! Total time: {total_time_hours:.2f} hours")
    print(f"Data saved to: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run parallel Carrying Capacity ablation simulations (std=0.2)')
    parser.add_argument('--n_cores', type=int, default=None)
    parser.add_argument('--n_reps', type=int, default=400)
    parser.add_argument('--u_step', type=float, default=0.02)
    args = parser.parse_args()
    simulate_parallel(n_cores=args.n_cores, n_reps=args.n_reps, u_step=args.u_step, k_std=0.2)
