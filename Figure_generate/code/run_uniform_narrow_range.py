"""
Run 48-species coalescence simulations with NARROW uniform distribution
Uniform[mean*0.5, mean*1.5] instead of [0, 2*mean]

This gives:
- Mean: still equals 'mean' parameter
- Range: [0.5*mean, 1.5*mean] (narrower than [0, 2*mean])
- Variance: (mean)^2 / 12 (smaller than uniform [0, 2*mean])
- CV: 1/(2*sqrt(3)) ≈ 0.289 (smaller than 0.577 for [0, 2*mean])
"""

import numpy as np
import json
from scipy.integrate import odeint
import sys
import os
from datetime import datetime
import pandas as pd

# Add current directory to path to import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from LV import gLV
from common_setup import metric_VectorDecomposition_onlyPositive

# ===== SIMULATION PARAMETERS =====
N = 48  # Total number of species
num_per_community = 12  # Species per community
N_communities = 4  # Number of communities

# Interaction strength means to test (same as original)
u_list = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
          0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00,
          1.05, 1.10, 1.15, 1.20]

N_reps = 20  # Number of repetitions per u value
base_seed = 5000

# Integration parameters
t_start = 0
t_end = 2000
num_points = 500

# Extinction threshold
extinction_threshold = 1e-4

# ===== NEW UNIFORM DISTRIBUTION =====
def uniform_narrow_range(mean):
    """
    Sample from Uniform[mean*0.5, mean*1.5]

    Properties:
    - Mean: mean
    - Variance: (mean)^2 / 12
    - Std: mean / (2*sqrt(3)) ≈ 0.289 * mean
    - CV: 1/(2*sqrt(3)) ≈ 0.289 (constant!)
    - Range: [0.5*mean, 1.5*mean]
    """
    return mean * 0.5 + mean * np.random.random()  # Uniform[0.5*mean, 1.5*mean]


def run_single_simulation(u, rep, seed):
    """Run a single simulation with given parameters"""
    np.random.seed(seed)

    # Initialize interaction matrix with diagonal = 1.0
    I = np.eye(N)

    # Fill off-diagonal elements with narrow uniform distribution
    for i in range(N):
        for j in range(N):
            if i != j:
                I[i, j] = uniform_narrow_range(u)

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
        y0[start_idx:end_idx] = 0.01

        # Integrate
        sol = odeint(gLV, y0, t, args=(I, g, k))
        final_state = sol[-1, :]
        final_state[final_state < extinction_threshold] = 0

        sc_list[f"c{comm_idx+1}"] = final_state.tolist()

    # === Coalescence Simulations (all pairwise combinations) ===
    for comm1_idx in range(N_communities):
        for comm2_idx in range(comm1_idx + 1, N_communities):
            # Get equilibrium states of both communities
            c1_equilibrium = np.array(sc_list[f"c{comm1_idx+1}"])
            c2_equilibrium = np.array(sc_list[f"c{comm2_idx+1}"])

            # Initial condition: 0.5 of each equilibrium community
            y0 = 0.5 * c1_equilibrium + 0.5 * c2_equilibrium

            # Integrate
            sol = odeint(gLV, y0, t, args=(I, g, k))
            final_state = sol[-1, :]
            final_state[final_state < extinction_threshold] = 0

            cc_list[f"c{comm1_idx+1}_c{comm2_idx+1}"] = final_state.tolist()

    return {
        "sc_list": sc_list,
        "cc_list": cc_list,
        "parameters": {
            "seed": int(seed),
            "u": float(u),
            "distribution": "uniform_narrow",
            "distribution_range": f"[{u*0.5:.3f}, {u*1.5:.3f}]",
            "interaction_matrix": I.tolist(),
            "growth_rates": g.tolist(),
            "carrying_capacities": k.tolist(),
            "interaction_matrix_stats": {
                "mean": float(np.mean(I[np.triu_indices(N, k=1)])),
                "std": float(np.std(I[np.triu_indices(N, k=1)])),
                "min": float(np.min(I[np.triu_indices(N, k=1)])),
                "max": float(np.max(I[np.triu_indices(N, k=1)])),
                "theoretical_cv": 1.0 / (2.0 * np.sqrt(3)),  # ≈ 0.289
                "empirical_cv": float(np.std(I[np.triu_indices(N, k=1)]) / np.mean(I[np.triu_indices(N, k=1)]))
            }
        }
    }


def main():
    print("="*70)
    print("48-Species Coalescence Simulation with Narrow Uniform Distribution")
    print("Distribution: Uniform[mean*0.5, mean*1.5]")
    print("="*70)

    # Calculate theoretical CV
    theoretical_cv = 1.0 / (2.0 * np.sqrt(3))
    print(f"\nTheoretical CV: {theoretical_cv:.4f} (≈0.289)")
    print(f"Compare to wide uniform [0, 2*mean]: CV ≈ 0.577")
    print(f"This is about HALF the variance!\n")

    print(f"Total simulations: {len(u_list)} means × {N_reps} reps = {len(u_list) * N_reps}")
    print(f"Mean values: {u_list[0]:.2f} to {u_list[-1]:.2f}")
    print(f"Base seed: {base_seed}\n")

    # Create output directory
    output_dir = "Simulation_Data/48species_20reps_narrow_uniform"
    os.makedirs(output_dir, exist_ok=True)

    # Store all results
    all_results = {}

    # Run simulations
    total_sims = len(u_list) * N_reps
    current_sim = 0

    start_time = datetime.now()

    for u in u_list:
        print(f"\n{'='*70}")
        print(f"Running u = {u:.2f} (range: [{u*0.5:.3f}, {u*1.5:.3f}])")
        print(f"{'='*70}")

        all_results[f"{u:.2f}"] = {}

        for rep in range(N_reps):
            seed = base_seed + current_sim
            current_sim += 1

            print(f"  Rep {rep+1}/{N_reps} (seed={seed})... ", end="", flush=True)

            result = run_single_simulation(u, rep, seed)
            all_results[f"{u:.2f}"][f"rep_{rep:03d}"] = result

            # Progress
            elapsed = (datetime.now() - start_time).total_seconds()
            avg_time = elapsed / current_sim
            remaining = (total_sims - current_sim) * avg_time

            print(f"✓ ({current_sim}/{total_sims}, ~{remaining/60:.1f} min remaining)")

    # Save results
    print("\n" + "="*70)
    print("Saving results...")

    output_file = os.path.join(output_dir, "Community_20reps_narrow_uniform.json")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"✓ Saved to: {output_file}")
    print(f"✓ File size: {file_size_mb:.1f} MB")

    # Save parameters summary
    params_data = []
    for u in u_list:
        for rep in range(N_reps):
            seed = base_seed + len(params_data)
            params_data.append({
                "u": u,
                "rep": rep,
                "seed": seed,
                "distribution": "uniform_narrow",
                "range": f"[{u*0.5:.3f}, {u*1.5:.3f}]",
                "theoretical_mean": u,
                "theoretical_std": u / (2 * np.sqrt(3)),
                "theoretical_cv": 1.0 / (2 * np.sqrt(3))
            })

    params_df = pd.DataFrame(params_data)
    params_file = os.path.join(output_dir, "simulation_parameters.xlsx")
    params_df.to_excel(params_file, index=False)
    print(f"✓ Parameters saved to: {params_file}")

    # Final statistics
    total_time = (datetime.now() - start_time).total_seconds()
    print("\n" + "="*70)
    print("SIMULATION COMPLETE!")
    print("="*70)
    print(f"Total time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
    print(f"Average time per simulation: {total_time/total_sims:.1f} seconds")
    print(f"Total simulations: {total_sims}")
    print(f"Output directory: {output_dir}")
    print("="*70)


if __name__ == "__main__":
    main()
