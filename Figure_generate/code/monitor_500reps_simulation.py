#!/usr/bin/env python3
"""
Monitor the progress of the 500 reps simulation with matrices
"""

import json
import os
import time
from datetime import datetime, timedelta

file_path = 'Simulation_Data/48species_500reps_fine_WITH_MATRICES/Community_500reps_fine_WITH_MATRICES.json'

def check_progress():
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        total_u = len(data)
        total_reps = sum(len(data[u_key]) for u_key in data.keys())
        matrices_count = 0

        for u_key in data.keys():
            for rep_key in data[u_key].keys():
                if 'interaction_matrix' in data[u_key][rep_key].get('parameters', {}):
                    matrices_count += 1

        expected_total = 24 * 500
        progress_pct = (total_reps / expected_total) * 100

        print(f"\n{'='*70}")
        print(f"🔬 500 REPS SIMULATION PROGRESS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        print(f"📊 Progress:")
        print(f"   Intensities completed: {total_u} / 24 ({total_u/24*100:.1f}%)")
        print(f"   Total repetitions: {total_reps} / {expected_total}")
        print(f"   Progress: {progress_pct:.1f}%")
        print(f"   Interaction matrices saved: {matrices_count}")
        print(f"\n📁 File info:")
        print(f"   Size: {file_size_mb:.1f} MB")
        print(f"   Expected final size: ~500-700 MB")

        # Estimate time remaining
        if total_reps > 50:  # Need some data for estimate
            # Assuming linear progress (rough estimate)
            remaining_reps = expected_total - total_reps
            # Very rough estimate: 1-2 hours per full run based on typical speeds
            hours_estimate = (remaining_reps / expected_total) * 8  # Adjust multiplier as needed
            eta = datetime.now() + timedelta(hours=hours_estimate)
            print(f"\n⏱️  Estimated completion: {eta.strftime('%Y-%m-%d %H:%M')}")
            print(f"   (Very rough estimate, assumes ~8 hours total)")

        # Latest intensity status
        latest_u = sorted([float(k) for k in data.keys()])[-1]
        latest_u_str = f"{latest_u:.2f}"
        latest_reps = len(data[latest_u_str])
        print(f"\n🔄 Current status:")
        print(f"   Working on u = {latest_u:.2f}")
        print(f"   Reps for this u: {latest_reps} / 500")

        # Check first entry
        first_u = list(data.keys())[0]
        first_rep = data[first_u]['rep_000']
        has_matrix = 'interaction_matrix' in first_rep.get('parameters', {})
        print(f"\n✅ Verification:")
        print(f"   Interaction matrices being saved: {has_matrix}")
        if has_matrix:
            matrix_size = len(first_rep['parameters']['interaction_matrix'])
            print(f"   Matrix dimensions: {matrix_size}×{matrix_size}")

        print(f"{'='*70}\n")

    except json.JSONDecodeError:
        print(f"⚠️  File is currently being written, file size: {file_size_mb:.1f} MB")
        print(f"   (This is normal during simulation)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        print("👀 Watching simulation progress (Ctrl+C to stop)...")
        try:
            while True:
                check_progress()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n✋ Monitoring stopped.")
    else:
        check_progress()
        print("💡 Tip: Run with --watch to monitor continuously")
