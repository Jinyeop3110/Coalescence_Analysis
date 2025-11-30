"""
Run 48-species coalescence simulations with independent mean and std control
Uses Normal distribution truncated at [0, ∞) for interaction matrices

This allows exploring the 2D parameter space:
- Mean: 0.1 to 1.2
- Std: 0.05 to 0.6
"""

import numpy as np
import json
from scipy.integrate import odeint
from scipy.stats import truncnorm
import sys
import os
from datetime import datetime
import pandas as pd
import itertools

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
std_values = np.arange(0.1, 0.61, 0.1)  # 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 (6 values)

N_reps = 100  # Number of repetitions per (mean, std) combination
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

    This ensures interaction strengths are non-negative while allowing
    independent control of mean and std.

    Properties:
    - Support: [0, ∞)
    - Target mean: mean
    - Target std: std
    - Actual mean/std will be slightly different due to truncation at 0
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

    # Calculate empirical statistics from the interaction matrix
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


def main():
    print("="*70)
    print("48-Species Coalescence Simulation - Mean × Std Grid")
    print("Distribution: Truncated Normal N(mean, std²) with support [0, ∞)")
    print("="*70)

    print(f"\nParameter Grid:")
    print(f"  Mean values: {len(mean_values)} values from {mean_values[0]:.1f} to {mean_values[-1]:.1f}")
    print(f"  Std values:  {len(std_values)} values from {std_values[0]:.2f} to {std_values[-1]:.2f}")
    print(f"  Grid size: {len(mean_values)} × {len(std_values)} = {len(mean_values) * len(std_values)} combinations")
    print(f"  Repetitions per combination: {N_reps}")

    total_sims = len(mean_values) * len(std_values) * N_reps
    print(f"\nTotal simulations: {total_sims:,}")
    print(f"Estimated time: ~{total_sims * 2 / 3600:.1f} hours (at 2 sec/simulation)")
    print(f"Base seed: {base_seed}\n")

    # Create output directory
    output_dir = f"Simulation_Data/mean_std_grid_{N_reps}reps"
    os.makedirs(output_dir, exist_ok=True)

    # Store all results organized by (mean, std)
    all_results = {}

    # Track progress
    current_sim = 0
    start_time = datetime.now()

    # Iterate through all (mean, std) combinations
    for mean in mean_values:
        for std in std_values:
            key = f"mean{mean:.2f}_std{std:.2f}"

            print(f"\n{'='*70}")
            print(f"Running mean={mean:.2f}, std={std:.2f}, CV={std/mean:.3f}")
            print(f"{'='*70}")

            all_results[key] = {}

            for rep in range(N_reps):
                seed = base_seed + current_sim
                current_sim += 1

                print(f"  Rep {rep+1}/{N_reps} (seed={seed})... ", end="", flush=True)

                result = run_single_simulation(mean, std, rep, seed)
                all_results[key][f"rep_{rep:03d}"] = result

                # Progress
                elapsed = (datetime.now() - start_time).total_seconds()
                avg_time = elapsed / current_sim
                remaining = (total_sims - current_sim) * avg_time

                print(f"✓ ({current_sim}/{total_sims}, ~{remaining/3600:.1f} hr remaining)")

                # Save intermediate results every 100 simulations
                if current_sim % 100 == 0:
                    print(f"\n  💾 Saving intermediate results...")
                    temp_file = os.path.join(output_dir, f"temp_checkpoint_{current_sim}.json")
                    with open(temp_file, 'w') as f:
                        json.dump(all_results, f, indent=2)

    # Save final results
    print("\n" + "="*70)
    print("Saving final results...")

    output_file = os.path.join(output_dir, f"Community_mean_std_grid_{N_reps}reps.json")
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
    print(f"✓ Parameter grid saved to: {grid_file}")

    # Final statistics
    total_time = (datetime.now() - start_time).total_seconds()
    print("\n" + "="*70)
    print("SIMULATION COMPLETE!")
    print("="*70)
    print(f"Total time: {total_time/3600:.1f} hours")
    print(f"Average time per simulation: {total_time/total_sims:.1f} seconds")
    print(f"Total simulations: {total_sims:,}")
    print(f"Parameter combinations: {len(mean_values) * len(std_values)}")
    print(f"Output directory: {output_dir}")
    print("="*70)

    # Clean up checkpoint files
    print("\nCleaning up checkpoint files...")
    for file in os.listdir(output_dir):
        if file.startswith("temp_checkpoint_"):
            os.remove(os.path.join(output_dir, file))
            print(f"  Removed: {file}")

    print("\n✅ All done!")


if __name__ == "__main__":
    main()
