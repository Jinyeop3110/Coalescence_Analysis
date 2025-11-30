#!/usr/bin/env python
"""
Check progress of running simulation without interrupting it
"""

import json
import time
import os
from pathlib import Path

def check_progress():
    """Check current simulation progress"""
    
    json_file = "Simulation_Data/48species_500reps/Community_500reps.json"
    
    if not Path(json_file).exists():
        print("❌ Simulation file not found")
        return
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        file_size = os.path.getsize(json_file)
        mod_time = os.path.getmtime(json_file)
        
        print("🔍 SIMULATION PROGRESS CHECK")
        print("=" * 30)
        print(f"📁 File: {json_file}")
        print(f"📏 Size: {file_size:,} bytes")
        print(f"⏰ Modified: {time.ctime(mod_time)}")
        print()
        
        total_reps = 0
        for u_key in data.keys():
            u_reps = len(data[u_key])
            total_reps += u_reps
            print(f"🎯 u = {u_key}: {u_reps} repetitions")
        
        expected_total = 500 * 3  # 500 reps × 3 interaction strengths
        progress_pct = (total_reps / expected_total) * 100
        
        print(f"\n📊 Overall Progress:")
        print(f"   Completed: {total_reps} / {expected_total} repetitions")
        print(f"   Progress: {progress_pct:.1f}%")
        
        if progress_pct < 100:
            print(f"   Status: 🟡 RUNNING")
        else:
            print(f"   Status: ✅ COMPLETE")
            
    except json.JSONDecodeError:
        print("⚠️ File is being written, simulation is active")
    except Exception as e:
        print(f"❌ Error checking progress: {e}")

if __name__ == "__main__":
    check_progress()