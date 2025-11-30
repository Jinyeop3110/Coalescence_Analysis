#!/usr/bin/env python3

import json
import numpy as np
from pathlib import Path

def debug_500_species_data():
    print("="*60)
    print("DEBUGGING 500-SPECIES DATA STRUCTURE")  
    print("="*60)
    
    # Check raw JSON structure
    session_name = "new_k_gamma_0_defined_pool_nooverlap_50from500_natural"
    json_file = f"Simulation_Data/{session_name}/Community.json"
    
    print(f"\n📁 Loading: {json_file}")
    
    if not Path(json_file).exists():
        print(f"❌ File not found: {json_file}")
        return
        
    with open(json_file, 'r') as f:
        raw_data = json.load(f)
    
    print(f"\n📊 Raw JSON structure:")
    print(f"   Keys: {list(raw_data.keys())}")
    print(f"   Total entries: {len(raw_data)}")
    
    # Sample a few entries
    sample_keys = list(raw_data.keys())[:3]
    for key in sample_keys:
        entry = raw_data[key]
        print(f"\n   Entry '{key}':")
        if isinstance(entry, dict):
            print(f"      Keys: {list(entry.keys())}")
            if 'interaction_strength' in entry:
                print(f"      interaction_strength: {entry['interaction_strength']}")
        else:
            print(f"      Value: {entry}")
    
    print(f"\n🔍 Checking JSON data interaction strengths...")
    try:
        # Check what interaction strengths are present
        u_values = []
        for key, entry in raw_data.items():
            if isinstance(entry, dict) and 'interaction_strength' in entry:
                u = entry['interaction_strength'] 
                if u not in u_values:
                    u_values.append(u)
        
        u_values.sort()
        print(f"   Found interaction strengths: {u_values}")
        print(f"   Number of unique u values: {len(u_values)}")
        
        # Count entries per u value
        for u in u_values:
            count = sum(1 for entry in raw_data.values() 
                       if isinstance(entry, dict) and entry.get('interaction_strength') == u)
            print(f"   u = {u}: {count} entries")
                
    except Exception as e:
        print(f"   ❌ Error in analysis: {e}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_500_species_data()