"""
Resume 48-Species Coalescence Simulation from Checkpoint
Continues from the last successful checkpoint after disk space failure
"""

import numpy as np
import json
import os
import multiprocessing as mp
from datetime import datetime
import time
from scipy.integrate import odeint
from scipy.stats import truncnorm
import sys

# Import existing functions from the original script
from LV import gLV

# ============================================================================
# Configuration
# ============================================================================

# Find the latest checkpoint
output_dir = "Simulation_Data/mean_std_grid_500reps"
checkpoint_files = sorted([f for f in os.listdir(output_dir) if f.startswith("checkpoint_") and f.endswith(".json")])

if not checkpoint_files:
    print("ERROR: No checkpoint files found!")
    sys.exit(1)

latest_checkpoint = os.path.join(output_dir, checkpoint_files[-1])
checkpoint_num = int(checkpoint_files[-1].replace("checkpoint_", "").replace(".json", ""))

print(f"\n{'='*70}")
print(f"RESUMING 48-Species Coalescence Simulation")
print(f"{'='*70}\n")
print(f"Latest checkpoint: {latest_checkpoint}")
print(f"Completed simulations: {checkpoint_num:,}")

# Load checkpoint
print(f"Loading checkpoint data...")
with open(latest_checkpoint, 'r') as f:
    all_results = json.load(f)

print(f"✓ Loaded {len(all_results)} parameter combinations")

# Simulation parameters (must match original)
S_number = 48
S_com = 12
mean_values = np.linspace(0.1, 1.2, 12)
std_values = np.linspace(0.10, 0.60, 6)
N_reps = 500
base_seed = 10000

# Community structure
com_labels = ['Com1', 'Com2', 'Com3', 'Com4']
com_membership = {}
for i, com in enumerate(com_labels):
    com_membership[com] = list(range(i * S_com, (i + 1) * S_com))

# Lotka-Volterra parameters
g = np.ones(S_number)
k = np.ones(S_number)
t = np.linspace(0, 200, 501)
t_thresh = 100

# ============================================================================
# Simulation Functions (copied from original)
# ============================================================================

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
    """Run a single coalescence simulation"""
    np.random.seed(seed)

    # Generate interaction matrix (diagonal = 1.0, off-diagonal from truncated normal)
    I = np.eye(S_number)
    for i in range(S_number):
        for j in range(S_number):
            if i != j:
                I[i, j] = truncated_normal_distribution(mean, std)

    # Run 4 separate communities
    community_finals = {}
    for com_name in com_labels:
        y0 = np.zeros(S_number)
        y0[com_membership[com_name]] = 0.01

        try:
            sol = odeint(gLV, y0, t, args=(I, g, k))
            y_final = sol[-1, :]
            y_final[y_final < 1e-6] = 0
            community_finals[com_name] = y_final.tolist()
        except:
            community_finals[com_name] = [0] * S_number

    # Run pairwise coalescence events
    coalescence_results = {}
    pairs = [('Com1', 'Com2'), ('Com1', 'Com3'), ('Com1', 'Com4'),
             ('Com2', 'Com3'), ('Com2', 'Com4'), ('Com3', 'Com4')]

    for com1, com2 in pairs:
        y1 = np.array(community_finals[com1])
        y2 = np.array(community_finals[com2])
        y_mix = (y1 + y2) / 2
        y_mix[y_mix < 1e-6] = 0

        try:
            sol = odeint(gLV, y_mix, t, args=(I, g, k))
            y_coal = sol[-1, :]
            y_coal[y_coal < 1e-6] = 0
            coalescence_results[f"{com1}_{com2}"] = y_coal.tolist()
        except:
            coalescence_results[f"{com1}_{com2}"] = [0] * S_number

    return {
        'communities': community_finals,
        'coalescence': coalescence_results,
        'interaction_matrix': I.tolist()
    }

def run_simulation_wrapper(args):
    """Wrapper for parallel execution"""
    mean, std, rep, seed = args
    key = f"mean_{mean:.2f}_std_{std:.2f}"
    rep_key = f"rep_{rep}"
    result = run_single_simulation(mean, std, rep, seed)
    return (key, rep_key, result)

def save_checkpoint(results, output_dir, checkpoint_num):
    """Save checkpoint to disk"""
    checkpoint_file = os.path.join(output_dir, f"checkpoint_{checkpoint_num}.json")

    with open(checkpoint_file, 'w') as f:
        json.dump(results, f, indent=2)

    file_size = os.path.getsize(checkpoint_file) / (1024**2)
    return checkpoint_file, file_size

# ============================================================================
# Determine What Simulations Still Need to Run
# ============================================================================

print(f"\nDetermining which simulations need to be completed...")

tasks_to_run = []
total_expected = len(mean_values) * len(std_values) * N_reps

for mean in mean_values:
    for std in std_values:
        key = f"mean_{mean:.2f}_std_{std:.2f}"

        # Check if this combination exists in checkpoint
        if key not in all_results:
            all_results[key] = {}

        # Check which reps are missing
        for rep in range(N_reps):
            rep_key = f"rep_{rep}"
            if rep_key not in all_results[key]:
                seed = base_seed + rep
                tasks_to_run.append((mean, std, rep, seed))

remaining = len(tasks_to_run)
print(f"\n✓ Found {checkpoint_num:,} completed simulations")
print(f"✓ Remaining simulations: {remaining:,}")
print(f"✓ Progress: {checkpoint_num}/{total_expected} ({100*checkpoint_num/total_expected:.1f}%)")

if remaining == 0:
    print("\n✓✓✓ ALL SIMULATIONS COMPLETE! ✓✓✓")
    sys.exit(0)

# ============================================================================
# Run Remaining Simulations in Parallel
# ============================================================================

num_cores = mp.cpu_count()
print(f"\nSystem information:")
print(f"  Available CPU cores: {num_cores}")
print(f"  Using {num_cores} cores for parallel execution")

print(f"\n{'='*70}")
print(f"Resuming simulations in parallel...")
print(f"{'='*70}\n")

start_time = time.time()
completed = checkpoint_num
last_checkpoint = checkpoint_num

with mp.Pool(processes=num_cores) as pool:
    for key, rep_key, result in pool.imap_unordered(run_simulation_wrapper, tasks_to_run):
        all_results[key][rep_key] = result
        completed += 1

        # Progress update every 100 simulations
        if completed % 100 == 0 or completed == total_expected:
            elapsed_min = (time.time() - start_time) / 60
            rate = (completed - checkpoint_num) / elapsed_min if elapsed_min > 0 else 0
            remaining_sims = total_expected - completed
            remaining_min = remaining_sims / rate if rate > 0 else 0

            print(f"Progress: {completed}/{total_expected} ({100*completed/total_expected:.1f}%) | "
                  f"Elapsed: {elapsed_min:.1f} min | Remaining: {remaining_min:.1f} min | "
                  f"Speed: {rate:.1f} sims/sec")

        # Save checkpoint every 1000 simulations (reduced to save disk space)
        if completed % 1000 == 0 and completed != last_checkpoint:
            print(f"\n  💾 Saving checkpoint at {completed} simulations...")
            checkpoint_file, file_size = save_checkpoint(all_results, output_dir, completed)
            print(f"     Saved: {checkpoint_file} ({file_size:.1f} MB)\n")
            last_checkpoint = completed

# ============================================================================
# Save Final Results
# ============================================================================

print(f"\n{'='*70}")
print(f"Saving final results...")
print(f"{'='*70}\n")

final_file = os.path.join(output_dir, "Community_mean_std_grid_500reps.json")
with open(final_file, 'w') as f:
    json.dump(all_results, f, indent=2)

final_size = os.path.getsize(final_file) / (1024**2)
total_time = (time.time() - start_time) / 60

print(f"✓ Final results saved: {final_file}")
print(f"✓ File size: {final_size:.1f} MB")
print(f"✓ Total time: {total_time:.1f} minutes")
print(f"\n{'='*70}")
print(f"✓✓✓ SIMULATION COMPLETE! ✓✓✓")
print(f"{'='*70}\n")
