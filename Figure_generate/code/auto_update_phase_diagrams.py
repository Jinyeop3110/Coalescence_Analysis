#!/usr/bin/env python
"""
Auto-update phase diagrams as simulation data becomes available
"""

import time
import subprocess
import json
from pathlib import Path

def check_simulation_progress():
    """Check progress of both simulations"""
    
    progress = {}
    
    # Check 500reps simulation
    json_500 = "Simulation_Data/48species_500reps/Community_500reps.json"
    if Path(json_500).exists():
        try:
            with open(json_500, 'r') as f:
                data_500 = json.load(f)
            total_500 = sum(len(data_500[u_key]) for u_key in data_500.keys())
            progress['500reps'] = {
                'current': total_500,
                'target': 1500,
                'percent': (total_500 / 1500) * 100,
                'intensities': len(data_500)
            }
        except:
            progress['500reps'] = {'current': 0, 'target': 1500, 'percent': 0, 'intensities': 0}
    else:
        progress['500reps'] = {'current': 0, 'target': 1500, 'percent': 0, 'intensities': 0}
    
    # Check fine simulation  
    json_fine = "Simulation_Data/48species_200reps_fine/Community_200reps_fine.json"
    if Path(json_fine).exists():
        try:
            with open(json_fine, 'r') as f:
                data_fine = json.load(f)
            total_fine = sum(len(data_fine[u_key]) for u_key in data_fine.keys())
            progress['fine'] = {
                'current': total_fine,
                'target': 4800,
                'percent': (total_fine / 4800) * 100,
                'intensities': len(data_fine)
            }
        except:
            progress['fine'] = {'current': 0, 'target': 4800, 'percent': 0, 'intensities': 0}
    else:
        progress['fine'] = {'current': 0, 'target': 4800, 'percent': 0, 'intensities': 0}
    
    return progress

def update_phase_diagrams():
    """Update phase diagrams with latest data"""
    
    print("🔄 Updating phase diagrams with latest simulation data...")
    
    try:
        result = subprocess.run(['python', 'plot_phase_diagram_json_simulations.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Phase diagrams updated successfully!")
            return True
        else:
            print(f"❌ Error updating phase diagrams: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running update: {e}")
        return False

def main():
    """Monitor simulations and update phase diagrams periodically"""
    
    print("🔍 AUTOMATIC PHASE DIAGRAM UPDATER")
    print("=" * 40)
    print("This script will monitor simulation progress and update phase diagrams")
    print("Press Ctrl+C to stop")
    print()
    
    last_500_reps = 0
    last_fine_reps = 0
    update_count = 0
    
    try:
        while True:
            # Check current progress
            progress = check_simulation_progress()
            
            current_time = time.strftime("%H:%M:%S")
            print(f"⏰ {current_time} - Progress Check:")
            print(f"   48species_500reps: {progress['500reps']['current']}/{progress['500reps']['target']} "
                  f"({progress['500reps']['percent']:.1f}%) - {progress['500reps']['intensities']} intensities")
            print(f"   48species_fine: {progress['fine']['current']}/{progress['fine']['target']} "
                  f"({progress['fine']['percent']:.1f}%) - {progress['fine']['intensities']} intensities")
            
            # Check if we have new data
            new_500_data = progress['500reps']['current'] > last_500_reps
            new_fine_data = progress['fine']['current'] > last_fine_reps
            
            if new_500_data or new_fine_data:
                print("   📈 New data detected! Updating phase diagrams...")
                
                if update_phase_diagrams():
                    update_count += 1
                    print(f"   ✅ Update #{update_count} completed")
                    
                    # Update our tracking variables
                    last_500_reps = progress['500reps']['current']
                    last_fine_reps = progress['fine']['current']
                else:
                    print("   ❌ Update failed")
            else:
                print("   📊 No new data, keeping current diagrams")
            
            # Check if simulations are complete
            if (progress['500reps']['percent'] >= 100 and progress['fine']['percent'] >= 100):
                print("\n🎉 Both simulations complete! Final update...")
                update_phase_diagrams()
                print("✅ All phase diagrams are final and complete!")
                break
            
            print("   ⏳ Waiting 60 seconds for next check...\n")
            time.sleep(60)  # Wait 1 minute between checks
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
        print(f"📊 Total updates performed: {update_count}")
        print("💡 You can run 'python plot_phase_diagram_json_simulations.py' manually anytime")

if __name__ == "__main__":
    main()