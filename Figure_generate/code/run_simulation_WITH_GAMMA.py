#!/usr/bin/env python
"""
Simulation with Gamma-Distributed Interaction Matrices

This script allows flexible control of both mean AND variance of interaction strengths
using the gamma distribution.

Usage:
conda activate coalescence
python run_simulation_WITH_GAMMA.py --mean 0.5 --cv 0.5 --reps 10
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import argparse
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from InitializeSpeciesPool import InitializeSpeceiesPool
from LV import run_lotka_volterra
from VariousMetrics import *


def gamma_distribution_mean_cv(mean, cv):
    """
    Generate gamma-distributed interaction strength.

    Parameters:
    -----------
    mean : float
        Desired mean of distribution (interaction strength)
    cv : float
        Coefficient of variation (std/mean)
        cv = 0.2 → low variability (tight around mean)
        cv = 0.5 → moderate variability
        cv = 1.0 → high variability
        cv = 1.5 → very high variability

    Returns:
    --------
    float
        Random sample from Gamma(k, θ)

    Properties:
    -----------
    - Mean = mean
    - Variance = (mean × cv)²
    - Std = mean × cv
    """
    k = 1.0 / (cv**2)            # shape parameter
    theta = mean * (cv**2)       # scale parameter
    return np.random.gamma(shape=k, scale=theta)


def gamma_distribution_mean_var(mean, variance):
    """
    Generate gamma-distributed interaction strength.

    Parameters:
    -----------
    mean : float
        Desired mean of distribution
    variance : float
        Desired variance of distribution

    Returns:
    --------
    float
        Random sample from Gamma(k, θ)
    """
    k = mean**2 / variance       # shape parameter
    theta = variance / mean      # scale parameter
    return np.random.gamma(shape=k, scale=theta)


def uniform_distribution(u, o=0):
    """Original uniform distribution for comparison."""
    return (2*u + 2*o) * np.random.random() - o


def InitializeRandomCommunityPool_48(N, num_C, num_S, save_path="Data/test"):
    """Initialize random non-overlapping communities."""
    CommunitiesLibrary = np.zeros([num_C, N])
    all_species = np.random.permutation(N)

    for i in range(num_C):
        start_idx = i * num_S
        end_idx = start_idx + num_S
        if end_idx <= N:
            selected_species = all_species[start_idx:end_idx]
            CommunitiesLibrary[i, selected_species] = 1

    df1 = pd.DataFrame(CommunitiesLibrary)
    with pd.ExcelWriter(save_path + '/communityLibrary.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Sheet1')

    return CommunitiesLibrary


def run_simulation_gamma(mean_values, cv_values, n_reps=10, distribution='gamma'):
    """
    Run simulation with gamma-distributed interactions.

    Parameters:
    -----------
    mean_values : list
        List of mean interaction strengths to test
    cv_values : list
        List of CV values to test (one per mean)
    n_reps : int
        Number of repetitions per parameter combination
    distribution : str
        'gamma' or 'uniform'
    """

    session_name = f"Simulation_Data/gamma_mean{mean_values[0]:.2f}_cv{cv_values[0]:.2f}_{n_reps}reps"
    os.makedirs(session_name, exist_ok=True)

    # Parameters
    N = 48
    num_S = 12
    num_C = 4
    t = [0, 5000]
    threshold = 1e-3

    print(f"\n{'='*70}")
    print(f"SIMULATION WITH {distribution.upper()} DISTRIBUTION")
    print(f"{'='*70}")
    print(f"Species: {N}")
    print(f"Communities: {num_C} (12 species each)")
    print(f"Repetitions per parameter: {n_reps}")
    print(f"Parameter combinations: {len(mean_values)}")

    if distribution == 'gamma':
        print(f"\nGamma distribution parameters:")
        for mean, cv in zip(mean_values, cv_values):
            variance = (mean * cv)**2
            k = 1.0 / (cv**2)
            print(f"  Mean={mean:.2f}, CV={cv:.2f} → Variance={variance:.4f}, Shape={k:.2f}")
    else:
        print(f"\nUniform distribution: [0, 2×mean]")

    print(f"{'='*70}\n")

    # Save parameters
    params_dict = {
        'N': N,
        'num_S': num_S,
        'num_C': num_C,
        'N_reps': n_reps,
        'distribution': distribution,
        'mean_values': mean_values,
        'cv_values': cv_values if distribution == 'gamma' else None,
        't': t,
        'threshold': threshold
    }

    param_df = pd.DataFrame([params_dict])
    param_df.to_excel(f"{session_name}/simulation_parameters.xlsx", index=False)

    # Run simulation
    output_file = session_name + f'/Community_{distribution}.json'
    all_results = {}
    start_time = time.time()

    for i, (mean, cv) in enumerate(zip(mean_values, cv_values)):
        param_key = f"mean{mean:.2f}_cv{cv:.2f}" if distribution == 'gamma' else f"u{mean:.2f}"

        print(f"\n{'='*70}")
        print(f"Parameter {i+1}/{len(mean_values)}: {param_key}")
        print(f"{'='*70}")

        all_results[param_key] = {}

        for rep in range(n_reps):
            print(f"  Rep {rep+1}/{n_reps}...", end=" ")
            rep_start = time.time()

            seed = int(mean * 10000) + int(cv * 1000) + rep * 100000
            np.random.seed(seed)

            # Define distribution function
            if distribution == 'gamma':
                f_interaction = lambda: gamma_distribution_mean_cv(mean, cv)
            else:
                f_interaction = lambda: uniform_distribution(mean, 0)

            # Initialize species pool
            I, g, k = InitializeSpeceiesPool(N,
                                           f_interaction,
                                           f_g=lambda: np.ones(1),
                                           f_k=lambda: 1,
                                           is_diagonal_one=True,
                                           save_path=session_name)

            # Create communities
            CommunitiesLibrary = InitializeRandomCommunityPool_48(N, num_C, num_S,
                                                                  save_path=session_name)

            # Initialize abundances
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

            # Store results with full interaction matrix
            all_results[param_key][f"rep_{rep:03d}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list,
                "parameters": {
                    "seed": seed,
                    "mean": mean,
                    "cv": cv if distribution == 'gamma' else None,
                    "distribution": distribution,
                    "interaction_matrix": I.tolist(),
                    "growth_rates": g.tolist(),
                    "carrying_capacities": k.tolist(),
                    "interaction_matrix_stats": {
                        "mean": float(np.mean(I[np.triu_indices(N, k=1)])),
                        "std": float(np.std(I[np.triu_indices(N, k=1)])),
                        "min": float(np.min(I[np.triu_indices(N, k=1)])),
                        "max": float(np.max(I[np.triu_indices(N, k=1)])),
                        "cv": float(np.std(I[np.triu_indices(N, k=1)]) / np.mean(I[np.triu_indices(N, k=1)]))
                    }
                }
            }

            print(f"✓ {time.time() - rep_start:.1f}s")

        # Save after each parameter
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2)

        file_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"  Saved: {file_size:.1f} MB")

    end_time = time.time()
    print(f"\n{'='*70}")
    print(f"✅ SIMULATION COMPLETE!")
    print(f"{'='*70}")
    print(f"Total time: {(end_time - start_time)/60:.1f} minutes")
    print(f"Output: {output_file}")
    print(f"Size: {os.path.getsize(output_file) / (1024 * 1024):.1f} MB")

    return output_file


def main():
    parser = argparse.ArgumentParser(description='Run simulation with gamma-distributed interactions')

    parser.add_argument('--distribution', type=str, default='gamma',
                       choices=['gamma', 'uniform'],
                       help='Distribution type (default: gamma)')

    parser.add_argument('--means', type=float, nargs='+', default=[0.3, 0.5, 0.8],
                       help='Mean interaction strengths (default: 0.3 0.5 0.8)')

    parser.add_argument('--cvs', type=float, nargs='+', default=None,
                       help='CV values for gamma (default: 0.5 for all means)')

    parser.add_argument('--reps', type=int, default=10,
                       help='Number of repetitions (default: 10)')

    args = parser.parse_args()

    # Set up CV values
    if args.cvs is None:
        args.cvs = [0.5] * len(args.means)
    elif len(args.cvs) == 1:
        args.cvs = args.cvs * len(args.means)
    elif len(args.cvs) != len(args.means):
        raise ValueError("Number of CVs must match number of means")

    print("\n" + "="*70)
    print("SIMULATION PARAMETERS")
    print("="*70)
    print(f"Distribution: {args.distribution}")
    print(f"Mean values: {args.means}")
    if args.distribution == 'gamma':
        print(f"CV values: {args.cvs}")
    print(f"Repetitions: {args.reps}")
    print("="*70)

    run_simulation_gamma(args.means, args.cvs, args.reps, args.distribution)


if __name__ == "__main__":
    # Example usage:
    # python run_simulation_WITH_GAMMA.py --means 0.5 --cvs 0.3 --reps 10
    # python run_simulation_WITH_GAMMA.py --means 0.5 0.5 0.5 --cvs 0.2 0.5 1.0 --reps 10
    # python run_simulation_WITH_GAMMA.py --distribution uniform --means 0.3 0.5 0.8 --reps 10

    main()
