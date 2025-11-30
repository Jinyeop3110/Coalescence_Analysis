#!/usr/bin/env python
"""
Minimal Converter: 500 species Community.json to Similarity.xlsx format

This script converts the 500-species simulation data from JSON format
to the Excel format expected by the phase diagram scripts, with minimal dependencies.
"""

import json
import pandas as pd
import numpy as np


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """
    Minimal vector decomposition for coalescence analysis.
    
    This function decomposes the mixed outcome m as:
    m = a*u + b*v + c*residual
    
    Where:
    - a, b are coefficients for parent contributions
    - c is the magnitude of residual/restructuring
    
    Args:
        u, v: Parent abundance vectors
        m: Mixed outcome vector
    
    Returns:
        Tuple of (a, b, c)
    """
    # Ensure inputs are numpy arrays
    u = np.array(u)
    v = np.array(v)
    m = np.array(m)
    
    # Normalize inputs to unit vectors for consistent scaling
    u_sum = np.sum(u) + 1e-10
    v_sum = np.sum(v) + 1e-10
    m_sum = np.sum(m) + 1e-10
    
    u_norm = u / u_sum
    v_norm = v / v_sum
    m_norm = m / m_sum
    
    # Set up least squares problem: m = a*u + b*v + residual
    # We want to minimize ||m - a*u - b*v||^2
    A_matrix = np.column_stack([u_norm, v_norm])
    
    try:
        # Solve least squares: min ||A*x - m||^2
        coeffs, residuals, rank, s = np.linalg.lstsq(A_matrix, m_norm, rcond=None)
        
        a = max(0, coeffs[0])  # Coefficient for parent 1
        b = max(0, coeffs[1])  # Coefficient for parent 2
        
        # Calculate residual
        predicted = a * u_norm + b * v_norm
        residual = m_norm - predicted
        c = np.linalg.norm(residual)  # Magnitude of residual
        
        return a, b, c
        
    except np.linalg.LinAlgError:
        # If matrix is singular, return defaults
        return 0.5, 0.5, 0.5


def convert_json_to_excel():
    """Convert Community.json to Similarity.xlsx format."""
    
    json_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full/Community.json"
    excel_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full/Similarity.xlsx"
    
    print("Loading 500-species simulation data...")
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Initialize data structure organized by interaction strength
    # Each sheet will have columns for each u-value
    u_values = sorted([float(k) for k in data.keys()])
    print(f"Found u-values in data: {u_values}")
    sheet_data = {0: {u: [] for u in u_values}, 
                  1: {u: [] for u in u_values}, 
                  2: {u: [] for u in u_values}}
    
    print("Converting data to Excel format...")
    
    # Process each interaction strength and replicate
    for u_str, replicates in data.items():
        u_val = float(u_str)
        print(f"  Processing u = {u_val}")
        
        for rep_key, rep_data in replicates.items():
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']
            
            # Process each coalescence pair
            for cc_key, cc_values in cc_list.items():
                # Parse community indices from key like "0_1"
                idx1, idx2 = map(int, cc_key.split('_'))
                
                # Get the individual community compositions
                y1 = np.array(sc_list[str(idx1)])
                y2 = np.array(sc_list[str(idx2)])
                y3 = np.array(cc_values)
                
                # Calculate vector decomposition metrics
                try:
                    a, b, c = metric_VectorDecomposition_onlyPositive(y1, y2, y3)
                    sheet_data[0][u_val].append(a)  # Sheet 1
                    sheet_data[1][u_val].append(b)  # Sheet 2  
                    sheet_data[2][u_val].append(c)  # Sheet 3
                except:
                    # If calculation fails, add NaN
                    sheet_data[0][u_val].append(np.nan)
                    sheet_data[1][u_val].append(np.nan)
                    sheet_data[2][u_val].append(np.nan)
    
    # Convert to DataFrames and save to Excel  
    print("Saving to Excel format...")
    
    # Find the maximum number of data points for any u-value
    max_len = 0
    total_points = 0
    for sheet_idx in range(3):
        for u_val in u_values:
            max_len = max(max_len, len(sheet_data[sheet_idx][u_val]))
            if sheet_idx == 0:  # Count only once
                total_points += len(sheet_data[sheet_idx][u_val])
    
    print(f"  Max data points per u-value: {max_len}")
    print(f"  Total data points: {total_points}")
    
    with pd.ExcelWriter(excel_path) as writer:
        for sheet_idx in range(3):
            # Create DataFrame with u-values as columns
            df_dict = {}
            for u_val in u_values:
                data_col = sheet_data[sheet_idx][u_val].copy()
                
                # Pad with NaN to match max_len
                while len(data_col) < max_len:
                    data_col.append(np.nan)
                
                df_dict[f"u_{u_val}"] = data_col
            
            # Create DataFrame with columns for each u-value
            df = pd.DataFrame(df_dict)
            df.to_excel(writer, sheet_name=str(sheet_idx), index=False)
            
            print(f"  Sheet {sheet_idx}: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print(f"✓ Converted {total_points} data points")
    print(f"✓ Saved to: {excel_path}")
    
    # Verify the conversion
    print("\nVerifying conversion...")
    verify_df = pd.read_excel(excel_path, sheet_name=0)
    print(f"  Sheet 0 shape: {verify_df.shape}")
    print(f"  Column names: {list(verify_df.columns)}")
    if verify_df.shape[0] > 0 and verify_df.shape[1] > 0:
        print(f"  Sample values from first column: {verify_df.iloc[:5, 0].values}")


if __name__ == "__main__":
    convert_json_to_excel()