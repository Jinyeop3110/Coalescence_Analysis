#!/usr/bin/env python
"""
Debug script to understand why 500-species classification is showing all mixing.
Examine the actual vector decomposition values to understand the data distribution.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def examine_vector_decomposition_data():
    """Examine the actual vector decomposition values to understand why all mixing."""
    
    print("Debugging 500-species vector decomposition classification...")
    
    # Load the Excel data
    file_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full/Similarity.xlsx"
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        return
    
    # Read the simulation data
    data1 = pd.read_excel(file_path, sheet_name=0)  # Parent 1 coefficients
    data2 = pd.read_excel(file_path, sheet_name=1)  # Parent 2 coefficients  
    data3 = pd.read_excel(file_path, sheet_name=2)  # Residual magnitudes
    
    print(f"Data shapes: {data1.shape}, {data2.shape}, {data3.shape}")
    print(f"Columns in data1: {list(data1.columns)}")
    
    # Extract u-values from column names
    u_values = []
    for col in data1.columns:
        if col.startswith('u_'):
            u_val = float(col.split('_')[1])
            u_values.append(u_val)
    u_values = sorted(u_values)
    
    print(f"Found u-values: {u_values}")
    
    # Examine data for a few representative u-values
    test_u_values = [0.3, 0.7, 1.0, 1.2] if len(u_values) > 4 else u_values[:3]
    
    for u_val in test_u_values:
        col_name = f"u_{u_val}"
        if col_name in data1.columns:
            print(f"\n--- Examining u={u_val:.1f} ---")
            
            a_values = data1[col_name].dropna().values
            b_values = data2[col_name].dropna().values
            c_values = data3[col_name].dropna().values
            
            min_length = min(len(a_values), len(b_values), len(c_values))
            a_values = a_values[:min_length]
            b_values = b_values[:min_length]
            c_values = c_values[:min_length]
            
            print(f"Sample size: {min_length}")
            
            # Statistics on raw values
            print(f"Raw values:")
            print(f"  a (parent1): mean={np.mean(a_values):.4f}, std={np.std(a_values):.4f}, range=[{np.min(a_values):.4f}, {np.max(a_values):.4f}]")
            print(f"  b (parent2): mean={np.mean(b_values):.4f}, std={np.std(b_values):.4f}, range=[{np.min(b_values):.4f}, {np.max(b_values):.4f}]")
            print(f"  c (residual): mean={np.mean(c_values):.4f}, std={np.std(c_values):.4f}, range=[{np.min(c_values):.4f}, {np.max(c_values):.4f}]")
            
            # Examine normalized values
            totals = a_values + b_values + c_values
            valid_idx = totals > 0
            
            if np.sum(valid_idx) > 0:
                a_norm = a_values[valid_idx] / totals[valid_idx]
                b_norm = b_values[valid_idx] / totals[valid_idx]
                c_norm = c_values[valid_idx] / totals[valid_idx]
                
                print(f"Normalized values (valid samples: {np.sum(valid_idx)}):")
                print(f"  a_norm: mean={np.mean(a_norm):.4f}, std={np.std(a_norm):.4f}, range=[{np.min(a_norm):.4f}, {np.max(a_norm):.4f}]")
                print(f"  b_norm: mean={np.mean(b_norm):.4f}, std={np.std(b_norm):.4f}, range=[{np.min(b_norm):.4f}, {np.max(b_norm):.4f}]")
                print(f"  c_norm: mean={np.mean(c_norm):.4f}, std={np.std(c_norm):.4f}, range=[{np.min(c_norm):.4f}, {np.max(c_norm):.4f}]")
                
                # Check classification metrics
                abs_diff = np.abs(a_norm - b_norm)
                print(f"  |a_norm - b_norm|: mean={np.mean(abs_diff):.4f}, std={np.std(abs_diff):.4f}, range=[{np.min(abs_diff):.4f}, {np.max(abs_diff):.4f}]")
                
                # Test different classification thresholds
                print(f"Classification tests:")
                
                # Current thresholds (from standard pipeline)
                c_threshold = 0.5
                diff_threshold = 0.3
                
                n_high_residual = np.sum(c_norm > c_threshold)
                n_high_diff = np.sum(abs_diff > diff_threshold)
                n_mixing = np.sum((c_norm <= c_threshold) & (abs_diff <= diff_threshold))
                
                print(f"  Current thresholds (c>0.5, |diff|>0.3): Res={n_high_residual}, Dom={n_high_diff}, Mix={n_mixing}")
                
                # Try more sensitive thresholds
                c_thresholds = [0.4, 0.3, 0.2, 0.1]
                diff_thresholds = [0.2, 0.15, 0.1, 0.05]
                
                for c_thresh in c_thresholds:
                    for diff_thresh in diff_thresholds:
                        n_res = np.sum(c_norm > c_thresh)
                        remaining = (c_norm <= c_thresh)
                        n_dom = np.sum(remaining & (abs_diff > diff_thresh))
                        n_mix = np.sum(remaining & (abs_diff <= diff_thresh))
                        
                        print(f"  Thresholds (c>{c_thresh:.1f}, |diff|>{diff_thresh:.2f}): Res={n_res}, Dom={n_dom}, Mix={n_mix}")
                        
                        if n_res > 0 or n_dom > 0:  # Stop when we find some non-mixing
                            break
                    if n_res > 0 or n_dom > 0:
                        break
                
                # Show some example data points
                print(f"  Example data points (first 10):")
                for i in range(min(10, len(a_norm))):
                    print(f"    Point {i+1}: a={a_norm[i]:.4f}, b={b_norm[i]:.4f}, c={c_norm[i]:.4f}, |diff|={abs_diff[i]:.4f}")

def compare_with_other_simulations():
    """Compare with data from other simulations to understand typical ranges."""
    
    print("\n" + "="*60)
    print("COMPARING WITH OTHER SIMULATION DATA")
    print("="*60)
    
    # Try to load one of the standard simulation files for comparison
    test_sessions = ["k_gaussian_0.25", "k_gaussian_0.15", "standard"]
    
    for session in test_sessions:
        file_path = f"Simulation_Data/{session}/Similarity.xlsx"
        if Path(file_path).exists():
            print(f"\n--- Comparing with {session} ---")
            
            try:
                data1 = pd.read_excel(file_path, sheet_name=0)
                data2 = pd.read_excel(file_path, sheet_name=1)
                data3 = pd.read_excel(file_path, sheet_name=2)
                
                # Remove first column if it's index
                if data1.columns[0] == 'Unnamed: 0' or str(data1.columns[0]).startswith('Unnamed'):
                    data1 = data1.drop(data1.columns[0], axis=1)
                    data2 = data2.drop(data2.columns[0], axis=1)
                    data3 = data3.drop(data3.columns[0], axis=1)
                
                # Transpose if needed (standard format has types as columns)
                if data1.shape[1] > data1.shape[0]:
                    data1 = data1.transpose()
                    data2 = data2.transpose() 
                    data3 = data3.transpose()
                
                print(f"Data shapes: {data1.shape}, {data2.shape}, {data3.shape}")
                
                # Examine first few columns/types
                n_types = min(3, data1.shape[1])
                for type_idx in range(n_types):
                    print(f"\n  Type {type_idx}:")
                    
                    a_vals = data1.iloc[:, type_idx].dropna().values
                    b_vals = data2.iloc[:, type_idx].dropna().values
                    c_vals = data3.iloc[:, type_idx].dropna().values
                    
                    min_len = min(len(a_vals), len(b_vals), len(c_vals))
                    if min_len > 0:
                        a_vals = a_vals[:min_len]
                        b_vals = b_vals[:min_len]
                        c_vals = c_vals[:min_len]
                        
                        totals = a_vals + b_vals + c_vals
                        valid_idx = totals > 0
                        
                        if np.sum(valid_idx) > 0:
                            a_norm = a_vals[valid_idx] / totals[valid_idx]
                            b_norm = b_vals[valid_idx] / totals[valid_idx]
                            c_norm = c_vals[valid_idx] / totals[valid_idx]
                            abs_diff = np.abs(a_norm - b_norm)
                            
                            print(f"    a_norm: mean={np.mean(a_norm):.4f}, range=[{np.min(a_norm):.4f}, {np.max(a_norm):.4f}]")
                            print(f"    b_norm: mean={np.mean(b_norm):.4f}, range=[{np.min(b_norm):.4f}, {np.max(b_norm):.4f}]")
                            print(f"    c_norm: mean={np.mean(c_norm):.4f}, range=[{np.min(c_norm):.4f}, {np.max(c_norm):.4f}]")
                            print(f"    |diff|: mean={np.mean(abs_diff):.4f}, range=[{np.min(abs_diff):.4f}, {np.max(abs_diff):.4f}]")
                
                break  # Found working data, stop
                
            except Exception as e:
                print(f"Error loading {session}: {e}")
                continue
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    examine_vector_decomposition_data()
    compare_with_other_simulations()