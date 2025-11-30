#!/usr/bin/env python
"""
Create 500-species phase diagram using the standard simulation pipeline.
This uses the same approach as plot_phase_diagram_simulation.py but adapted for 500-species data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from common_setup_simulation_fix import create_phase_diagram_for_simulation

def read_500species_simulation_excel(file_path):
    """Read 500-species simulation data from Excel file with multiple sheets."""
    data_sheets = []
    try:
        for sheet_name in range(3):
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            data_sheets.append(df)
        return data_sheets
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def process_500species_simulation():
    """Process 500-species simulation data using the standard pipeline."""
    
    print("Processing 500-species simulation data using standard pipeline...")
    
    # Use the full dataset path
    file_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full/Similarity.xlsx"
    
    if not Path(file_path).exists():
        print(f"Warning: File not found: {file_path}")
        return None, None, None, None, None
    
    # Read the simulation data
    excel_data = read_500species_simulation_excel(file_path)
    if excel_data is None:
        return None, None, None, None, None
    
    data1, data2, data3 = excel_data
    print(f"Loaded Excel sheets with shapes: {data1.shape}, {data2.shape}, {data3.shape}")
    
    # Extract u-values from column names
    u_values = []
    for col in data1.columns:
        if col.startswith('u_'):
            u_val = float(col.split('_')[1])
            u_values.append(u_val)
    u_values = sorted(u_values)
    
    print(f"Found u-values: {u_values}")
    
    # Convert to dictionary format expected by create_phase_diagram_for_simulation
    data1_dict = {}
    data2_dict = {}
    data3_dict = {}
    
    # Map u-values to type indices (0, 1, 2, ...)
    types_to_plot = list(range(len(u_values)))
    
    for i, u_val in enumerate(u_values):
        col_name = f"u_{u_val}"
        if col_name in data1.columns:
            # Extract data for this u-value (remove NaN values)
            type_data1 = data1[col_name].dropna().tolist()
            type_data2 = data2[col_name].dropna().tolist()
            type_data3 = data3[col_name].dropna().tolist()
            
            # Ensure all arrays have the same length
            min_length = min(len(type_data1), len(type_data2), len(type_data3))
            type_data1 = type_data1[:min_length]
            type_data2 = type_data2[:min_length]
            type_data3 = type_data3[:min_length]
            
            data1_dict[i] = type_data1
            data2_dict[i] = type_data2
            data3_dict[i] = type_data3
            
            print(f"  u={u_val:.1f} -> type {i}: {min_length} data points")
        else:
            # Fill missing types with empty lists
            data1_dict[i] = []
            data2_dict[i] = []
            data3_dict[i] = []
    
    return types_to_plot, data1_dict, data2_dict, data3_dict, u_values

def main():
    """Main function to generate 500-species phase diagram using standard pipeline."""
    
    # Create output directory
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating 500-species phase diagram using standard simulation pipeline...")
    print("🎨 Using standard colors: Red (Dominance), Green (Mixing), Purple (Restructuring)")
    
    # Process the 500-species simulation data
    result = process_500species_simulation()
    if result[0] is None:
        print("✗ Failed to process 500-species simulation data")
        return
    
    types_to_plot, data1, data2, data3, u_values = result
    
    print(f"\n--- Processing 500-species simulation ---")
    print(f"Found {len(types_to_plot)} data types for u-values: {u_values}")
    
    # Set up plotting parameters for the full range
    # Even though we only have data for [0.1, 0.2, ... 1.2], we'll map them correctly
    custom_x_ticks = np.arange(len(u_values))  # 0, 1, 2, ..., len(u_values)-1
    custom_x_labels = [f"{u:.1f}" for u in u_values]  # Actual u-values as labels
    
    # Generate output filename
    output_filename = "Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500.svg"
    
    try:
        # Create the phase diagram using the standard function
        create_phase_diagram_for_simulation(
            types_to_plot, 
            data1, data2, data3, 
            custom_x_ticks, 
            custom_x_labels, 
            output_filename=output_filename,
            plot_boundary=False,  # No boundary for simulation plots
            u_values=u_values     # Pass u_values for proper handling
        )
        
        print(f"✓ Created: {output_filename}")
        
        # Print some statistics about the data
        total_points = sum(len(data1.get(t, [])) for t in types_to_plot)
        print(f"  Data points processed: {total_points}")
        
        # Verify the file was created
        if Path(output_filename).exists():
            file_size = Path(output_filename).stat().st_size
            print(f"  File size: {file_size:,} bytes")
            print(f"✓ Successfully generated 500-species phase diagram!")
        else:
            print(f"✗ Output file was not created: {output_filename}")
            
    except Exception as e:
        print(f"✗ Error creating {output_filename}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()