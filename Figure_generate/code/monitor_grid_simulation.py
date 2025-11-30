#!/usr/bin/env python
"""
Monitor progress of mean-std grid simulation

This script checks the latest checkpoint or final output file
and reports progress statistics.
"""

import os
import json
import glob
from datetime import datetime

def monitor_simulation(n_reps=500):
    """Monitor simulation progress"""

    output_dir = f"Simulation_Data/mean_std_grid_{n_reps}reps"

    if not os.path.exists(output_dir):
        print(f"❌ Directory not found: {output_dir}")
        print(f"   Simulation has not been started yet.")
        return

    print("="*70)
    print(f"MONITORING: {output_dir}")
    print("="*70)

    # Check for final output
    final_file = os.path.join(output_dir, f"Community_mean_std_grid_{n_reps}reps.json")

    if os.path.exists(final_file):
        print(f"\n✅ SIMULATION COMPLETE!")
        file_size = os.path.getsize(final_file) / (1024**3)
        mod_time = datetime.fromtimestamp(os.path.getmtime(final_file))

        print(f"\n📁 Final output:")
        print(f"   File: {final_file}")
        print(f"   Size: {file_size:.2f} GB")
        print(f"   Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Analyze completeness
        with open(final_file, 'r') as f:
            data = json.load(f)

        n_combinations = len(data)
        total_reps = sum(len([k for k in combo.keys() if k.startswith('rep_')])
                        for combo in data.values())

        expected_combinations = 12 * 6  # 12 means × 6 stds
        expected_total = expected_combinations * n_reps

        print(f"\n📊 Data summary:")
        print(f"   Combinations: {n_combinations}/{expected_combinations}")
        print(f"   Total reps: {total_reps:,}/{expected_total:,}")
        print(f"   Completeness: {100*total_reps/expected_total:.1f}%")

        return

    # Check for checkpoints
    checkpoints = glob.glob(os.path.join(output_dir, "checkpoint_*.json"))

    if not checkpoints:
        print(f"\n⚠️  No checkpoints or final output found")
        print(f"   Simulation may not have started or no progress saved yet")
        return

    # Find latest checkpoint
    latest_checkpoint = max(checkpoints, key=os.path.getmtime)
    checkpoint_num = int(latest_checkpoint.split('_')[-1].replace('.json', ''))

    file_size = os.path.getsize(latest_checkpoint) / (1024**2)
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_checkpoint))

    print(f"\n🔄 SIMULATION IN PROGRESS")
    print(f"\n📁 Latest checkpoint:")
    print(f"   File: {os.path.basename(latest_checkpoint)}")
    print(f"   Size: {file_size:.1f} MB")
    print(f"   Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Analyze progress
    with open(latest_checkpoint, 'r') as f:
        data = json.load(f)

    n_combinations = len(data)
    total_reps = sum(len([k for k in combo.keys() if k.startswith('rep_')])
                    for combo in data.values())

    expected_combinations = 12 * 6
    expected_total = expected_combinations * n_reps

    progress_pct = 100 * total_reps / expected_total

    print(f"\n📊 Progress:")
    print(f"   Combinations: {n_combinations}/{expected_combinations}")
    print(f"   Total simulations: {total_reps:,}/{expected_total:,}")
    print(f"   Progress: {progress_pct:.1f}%")
    print(f"   Remaining: {expected_total - total_reps:,} simulations")

    # Estimate time remaining (rough)
    if total_reps > 0:
        elapsed_time = (datetime.now() - mod_time).total_seconds()
        if elapsed_time < 300:  # Only if checkpoint is recent (< 5 min old)
            print(f"\n⏱️  Note: Checkpoint is recent ({elapsed_time/60:.1f} min old)")
            print(f"   Simulation is likely still running")

    print("\n" + "="*70)


if __name__ == "__main__":
    import sys

    n_reps = 500
    if len(sys.argv) > 1:
        n_reps = int(sys.argv[1])

    monitor_simulation(n_reps)
