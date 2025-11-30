#!/usr/bin/env python
"""
Monitor progress of both running simulations
"""

import json
import time
import os
from pathlib import Path

def check_simulation_progress(name, json_file, expected_total):
    """Check progress of a single simulation"""
    
    if not Path(json_file).exists():
        return f"❌ {name}: File not found"
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        file_size = os.path.getsize(json_file)
        mod_time = os.path.getmtime(json_file)
        
        total_reps = sum(len(data[u_key]) for u_key in data.keys())
        progress_pct = (total_reps / expected_total) * 100
        
        status = "✅ COMPLETE" if progress_pct >= 100 else "🟡 RUNNING"
        
        return f"""📊 {name}:
   File size: {file_size:,} bytes
   Modified: {time.ctime(mod_time)}
   Progress: {total_reps}/{expected_total} reps ({progress_pct:.1f}%)
   Status: {status}
   Intensities: {list(data.keys())}"""
        
    except json.JSONDecodeError:
        return f"⚠️ {name}: File being written (simulation active)"
    except Exception as e:
        return f"❌ {name}: Error - {e}"

def monitor_simulations():
    """Monitor both simulations"""
    
    print("🔍 DUAL SIMULATION MONITORING")
    print("=" * 50)
    print(f"⏰ Check time: {time.ctime()}")
    print()
    
    # 500 reps simulation (3 intensities: 0.3, 0.5, 0.8)
    sim1_result = check_simulation_progress(
        "48species_500reps",
        "Simulation_Data/48species_500reps/Community_500reps.json",
        500 * 3  # 1500 total
    )
    
    # Fine interval simulation (24 intensities: 0.05-1.2, 200 reps each)
    sim2_result = check_simulation_progress(
        "48species_200reps_fine", 
        "Simulation_Data/48species_200reps_fine/Community_200reps_fine.json",
        200 * 24  # 4800 total
    )
    
    print(sim1_result)
    print()
    print(sim2_result)
    print()
    
    print("🎯 Expected Final Output:")
    print("   • 48species_500reps: 1,500 total repetitions (500×3)")
    print("   • 48species_200reps_fine: 4,800 total repetitions (200×24)")
    print("   • Both will generate full JSON data for phase diagram analysis")

if __name__ == "__main__":
    monitor_simulations()