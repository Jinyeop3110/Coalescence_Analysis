#!/usr/bin/env python
"""
Create phase diagram for 500-species simulation with full u-range
Uses existing infrastructure but properly handles the 500-species data structure
"""

import numpy as np
import pandas as pd
from pathlib import Path

def classify_vector_decomposition(a, b, c):
    """
    Classify coalescence outcome based on vector decomposition coefficients.
    Adjusted thresholds for non-overlapping community data.
    """
    # Normalize to handle different scales
    total = a + b + c
    if total > 0:
        a_norm = a / total
        b_norm = b / total
        c_norm = c / total
    else:
        return 2  # Default to restructuring
    
    # More sensitive thresholds for non-overlapping communities
    # Use quantile-based approach
    abs_diff = abs(a_norm - b_norm)
    
    # Classification rules - much more sensitive thresholds
    if c_norm > 0.0004:  # Top ~25% of residuals -> restructuring
        return 2  # Restructuring
    elif abs_diff > 0.0008:  # Top ~25% of differences -> dominance
        return 0  # Dominance (one parent dominates)
    else:
        return 1  # Mixing

def create_500species_phase_diagram():
    """Create phase diagram for 500-species simulation data using existing infrastructure."""
    
    print("Creating 500-species phase diagram with full u-range...")
    
    # Read the Excel data
    file_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full/Similarity.xlsx"
    
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        return
    
    try:
        data1 = pd.read_excel(file_path, sheet_name=0)  # Parent 1 coefficients
        data2 = pd.read_excel(file_path, sheet_name=1)  # Parent 2 coefficients  
        data3 = pd.read_excel(file_path, sheet_name=2)  # Residual magnitudes
        
        print(f"Data shapes: {data1.shape}, {data2.shape}, {data3.shape}")
        
        # Extract u-values from column names
        u_values = []
        for col in data1.columns:
            if col.startswith('u_'):
                u_val = float(col.split('_')[1])
                u_values.append(u_val)
        
        u_values = sorted(u_values)
        print(f"Found u-values: {u_values}")
        
        # Process data and convert to format expected by existing system
        data1_dict = {}
        data2_dict = {}  
        data3_dict = {}
        
        for i, u_val in enumerate(u_values):
            col_name = f"u_{u_val}"
            
            if col_name in data1.columns:
                # Get data for this u-value
                type_data1 = data1[col_name].dropna().tolist()
                type_data2 = data2[col_name].dropna().tolist()
                type_data3 = data3[col_name].dropna().tolist()
                
                # Ensure all arrays have the same length
                min_length = min(len(type_data1), len(type_data2), len(type_data3))
                if min_length > 0:
                    type_data1 = type_data1[:min_length]
                    type_data2 = type_data2[:min_length]
                    type_data3 = type_data3[:min_length]
                    
                    data1_dict[i] = type_data1
                    data2_dict[i] = type_data2
                    data3_dict[i] = type_data3
                    
                    print(f"  u={u_val:.1f}: {min_length} data points")
        
        # Now let me try importing common_setup and use it
        try:
            from common_setup_simulation_fix import create_phase_diagram_for_simulation
            
            # Create the phase diagram
            type_names = list(range(len(u_values)))
            
            # Set up x-axis for full range
            custom_x_ticks = list(range(len(u_values)))
            custom_x_labels = [f"{u:.1f}" for u in u_values]
            
            output_filename = "Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500_full_range.svg"
            
            create_phase_diagram_for_simulation(
                type_names,
                data1_dict,
                data2_dict, 
                data3_dict,
                custom_x_ticks=custom_x_ticks,
                custom_x_labels=custom_x_labels,
                output_filename=output_filename,
                plot_boundary=False,
                u_values=u_values
            )
            
            print(f"✓ Phase diagram created: {output_filename}")
            
        except ImportError as e:
            print(f"Cannot import common_setup_simulation_fix: {e}")
            print("Creating a simple text-based summary instead...")
            
            # Create text summary
            print("\n" + "="*60)
            print("500-SPECIES COALESCENCE PHASE DIAGRAM SUMMARY")
            print("="*60)
            print(f"{'u-value':<8} {'Dominance':<12} {'Mixing':<12} {'Restructuring':<15} {'Total':<8}")
            print("-"*60)
            
            for i, u_val in enumerate(u_values):
                if i in data1_dict:
                    a_values = np.array(data1_dict[i])
                    b_values = np.array(data2_dict[i])
                    c_values = np.array(data3_dict[i])
                    
                    # Classify each data point
                    classifications = []
                    for j in range(len(a_values)):
                        cls = classify_vector_decomposition(a_values[j], b_values[j], c_values[j])
                        classifications.append(cls)
                    
                    classifications = np.array(classifications)
                    n_dominance = np.sum(classifications == 0)
                    n_mixing = np.sum(classifications == 1)
                    n_restructuring = np.sum(classifications == 2)
                    total = len(classifications)
                    
                    dom_pct = n_dominance / total * 100 if total > 0 else 0
                    mix_pct = n_mixing / total * 100 if total > 0 else 0
                    res_pct = n_restructuring / total * 100 if total > 0 else 0
                    
                    print(f"{u_val:<8.1f} {dom_pct:<12.1f} {mix_pct:<12.1f} {res_pct:<15.1f} {total:<8}")
            
            print("-"*60)
            print("\nPercentages show the fraction of coalescence events in each category.")
            print("Data based on vector decomposition analysis of Lotka-Volterra simulations.")
            
    except Exception as e:
        print(f"Error processing data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_500species_phase_diagram()