#!/usr/bin/env python3

import numpy as np
import pandas as pd
from pathlib import Path
import json
from plot_phase_diagram_simulation import read_simulation_excel, create_phase_diagram

def test_500_species_phase_diagram():
    """Test the 500-species phase diagram generation."""
    
    print("="*60)
    print("TESTING 500-SPECIES PHASE DIAGRAM GENERATION")
    print("="*60)
    
    # Session name for 500 species
    session_name = "new_k_gamma_0_defined_pool_nooverlap_50from500_natural"
    data_path = f"Simulation_Data/{session_name}"
    
    try:
        # Load JSON data structure
        json_file = f"{data_path}/Community.json"
        with open(json_file, 'r') as f:
            raw_data = json.load(f)
        
        u_values = [float(k) for k in raw_data.keys()]
        u_values.sort()
        print(f"✓ Interaction strengths: {u_values}")
        
        # Load Excel data
        excel_file = f"{data_path}/Similarity.xlsx"
        excel_data = read_simulation_excel(excel_file)
        data1, data2, data3 = excel_data
        
        print(f"✓ Excel sheets loaded: {data1.shape}, {data2.shape}, {data3.shape}")
        print(f"✓ Column names: {list(data1.columns)}")
        
        # Process data properly
        data1_dict = {}
        data2_dict = {}  
        data3_dict = {}
        
        for i, u_val in enumerate(u_values):
            type_key = np.int64(i)
            col_name = f"u_{u_val}"
            
            if col_name in data1.columns:
                type_data1 = data1[col_name].dropna().tolist()
                type_data2 = data2[col_name].dropna().tolist()
                type_data3 = data3[col_name].dropna().tolist()
                
                min_length = min(len(type_data1), len(type_data2), len(type_data3))
                data1_dict[type_key] = type_data1[:min_length]
                data2_dict[type_key] = type_data2[:min_length]
                data3_dict[type_key] = type_data3[:min_length]
                
                print(f"✓ u={u_val:.1f}: {min_length} data points")
        
        types_to_plot = list(data1_dict.keys())
        print(f"✓ Types to plot: {types_to_plot}")
        
        # Calculate summary statistics
        for type_key in types_to_plot:
            dom_avg = np.mean(data1_dict[type_key]) if data1_dict[type_key] else 0
            mix_avg = np.mean(data2_dict[type_key]) if data2_dict[type_key] else 0  
            rest_avg = np.mean(data3_dict[type_key]) if data3_dict[type_key] else 0
            u_val = u_values[int(type_key)]
            print(f"   u={u_val:.1f}: Dom={dom_avg:.3f}, Mix={mix_avg:.3f}, Rest={rest_avg:.3f}")
        
        # Set up plotting parameters
        custom_x_ticks = np.array([0, 2, 4, 6, 8, 10])  # Full range ticks
        custom_x_labels = ["0.1", "0.3", "0.5", "0.7", "0.9", "1.1"]  # Full range labels
        
        # Create output directory
        output_dir = Path("Figure/PhaseDiagram")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filename = output_dir / "Fig_phase_diagram_Simul_50from500.svg"
        
        print(f"\n🎨 Creating phase diagram...")
        print(f"   Output: {output_filename}")
        
        # Generate phase diagram
        create_phase_diagram(
            types_to_plot,
            data1_dict, data2_dict, data3_dict, 
            custom_x_ticks, 
            custom_x_labels, 
            output_filename=str(output_filename),
            plot_boundary=False
        )
        
        # Verify output
        if output_filename.exists():
            file_size = output_filename.stat().st_size
            print(f"✓ Phase diagram created successfully!")
            print(f"✓ File size: {file_size:,} bytes")
            return True
        else:
            print("✗ Output file was not created")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_500_species_phase_diagram()
    print(f"\n{'✓ SUCCESS' if success else '✗ FAILED'}")