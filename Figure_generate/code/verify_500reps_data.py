#!/usr/bin/env python
"""
Verify the 48species_500reps simulation data
"""

import json
import pandas as pd

def verify_500reps_data():
    """Verify the existing 500 reps simulation data"""
    
    data_dir = "Simulation_Data/48species_500reps"
    json_file = f"{data_dir}/Community_500reps.json"
    
    print("VERIFYING 48SPECIES_500REPS DATA")
    print("=" * 40)
    
    try:
        # Read the JSON data
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        print(f"✓ Successfully loaded: {json_file}")
        print(f"📊 Top-level keys: {list(data.keys())}")
        
        # Check each interaction strength
        for u_key in data.keys():
            u_data = data[u_key]
            print(f"\n🎯 Interaction strength {u_key}:")
            print(f"   Number of repetitions: {len(u_data)}")
            
            # Check first repetition structure
            first_rep = list(u_data.keys())[0]
            rep_data = u_data[first_rep]
            
            print(f"   Single communities: {len(rep_data.get('sc_list', {}))}")
            print(f"   Coalescence pairs: {len(rep_data.get('cc_list', {}))}")
            
            # Sample data structure
            if 'sc_list' in rep_data:
                sc_example = list(rep_data['sc_list'].keys())[:3]
                print(f"   SC keys (sample): {sc_example}")
            
            if 'cc_list' in rep_data:
                cc_example = list(rep_data['cc_list'].keys())[:3]
                print(f"   CC keys (sample): {cc_example}")
        
        total_reps = sum(len(data[u_key]) for u_key in data.keys())
        print(f"\n📈 SUMMARY:")
        print(f"   Total repetitions across all u-values: {total_reps}")
        print(f"   Expected (500 × 3): {500 * 3}")
        print(f"   Data completeness: {'✅ COMPLETE' if total_reps == 1500 else '❌ INCOMPLETE'}")
        
        # Check parameter file
        param_file = f"{data_dir}/parameter.xlsx"
        params = pd.read_excel(param_file)
        print(f"\n⚙️  PARAMETERS:")
        for col in params.columns:
            value = params[col].iloc[0]
            print(f"   {col}: {value}")
            
        print(f"\n✅ Data verification complete!")
        print(f"🎯 This data is ready for phase diagram generation")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

if __name__ == "__main__":
    verify_500reps_data()