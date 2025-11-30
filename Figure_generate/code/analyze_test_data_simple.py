#!/usr/bin/env python3
"""
Simple analysis of test simulation data without plotting (to avoid matplotlib issues).
This will process the data and save results that can be plotted later.
"""

import os
import json
import numpy as np


def normalize(v):
    """Normalize vector"""
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """Vector decomposition metric"""
    u = normalize(u)
    v = normalize(v)
    m = normalize(m)
    
    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    
    try:
        e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))
    except np.linalg.LinAlgError:
        return 0, 0, 1
    
    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)
    x3 = np.linalg.norm(m - (e12[0]*u) - (e12[1]*v))
    
    if x1**2 + x2**2 == 0:
        return 0, 0, x3
    
    try:
        convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2))
    except:
        return x1, x2, x3
    
    return convert*x1, convert*x2, x3


def calculate_assymetricity(u, v, k):
    """Calculate asymmetricity measures"""
    x = np.sqrt(np.array(u)**2 + np.array(v)**2)
    if v == 0:
        y = 1.0
    else:
        y = np.abs(np.abs(np.arctan(np.array(u)/np.array(v))) - np.pi/4) / (np.pi/4)  
    return x, y


def characterize_case(x, y):
    """Classify outcomes"""
    if (x**2 > 0.5) * (y > 0.5):
        return 0  # Dominance
    if (x**2 > 0.5) * (y < 0.5):
        return 1  # Mixing
    if (x**2 < 0.5):
        return 2  # Restructuring
    return 1  # Default to mixing


def analyze_test_data():
    """Analyze the test simulation data without plotting"""
    
    print("Analyzing test simulation data...")
    
    # Load test data
    data_path = "Simulation_Data/48species_test/Community_test.json"
    
    if not os.path.exists(data_path):
        print(f"Error: Test data file not found at {data_path}")
        return
    
    with open(data_path, 'r') as f:
        all_results = json.load(f)
    
    # Create output directory for processed data
    output_dir = "Analysis_Results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each interaction strength
    u_values = ['0.3', '0.5', '0.8']
    processed_data = {}
    
    print("\nProcessing each interaction strength:")
    
    for u in u_values:
        print(f"\nProcessing u = {u}")
        
        # Collect all (u, v) coordinates
        all_u_coords = []
        all_v_coords = []
        
        # Classification counters
        dominance_count = 0
        mixing_count = 0
        restructuring_count = 0
        
        # Process each repetition
        rep_count = 0
        valid_pairs = 0
        
        for rep_key in all_results[u].keys():
            rep_data = all_results[u][rep_key]
            rep_count += 1
            
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']
            
            # Process each coalescence pair
            for pair_key, c_mix in cc_list.items():
                idx, jdx = map(int, pair_key.split('_'))
                
                c_1 = np.array(sc_list[str(idx)])
                c_2 = np.array(sc_list[str(jdx)])
                c_mix = np.array(c_mix)
                
                # Filter small values
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                # Check if communities have surviving species
                c1_alive = np.sum(c_1 > 0)
                c2_alive = np.sum(c_2 > 0)
                cmix_alive = np.sum(c_mix > 0)
                
                if c1_alive > 0 and c2_alive > 0 and cmix_alive > 0:
                    try:
                        # Calculate vector decomposition
                        u_coord, v_coord, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                        
                        # Only include valid coordinates
                        if not (np.isnan(u_coord) or np.isnan(v_coord)):
                            all_u_coords.append(u_coord)
                            all_v_coords.append(v_coord)
                            valid_pairs += 1
                            
                            # Classify outcome
                            x, y = calculate_assymetricity(u_coord, v_coord, k)
                            class_type = characterize_case(x, y)
                            
                            if class_type == 0:
                                dominance_count += 1
                            elif class_type == 1:
                                mixing_count += 1
                            else:
                                restructuring_count += 1
                                
                    except Exception as e:
                        # Skip problematic cases
                        pass
        
        # Convert to numpy arrays
        all_u_coords = np.array(all_u_coords)
        all_v_coords = np.array(all_v_coords)
        
        total_points = len(all_u_coords)
        
        print(f"  Repetitions processed: {rep_count}")
        print(f"  Valid coalescence pairs: {valid_pairs}")
        print(f"  Total data points: {total_points}")
        
        if total_points > 0:
            print(f"  Classification:")
            print(f"    Dominance:     {dominance_count:3d} ({100*dominance_count/total_points:5.1f}%)")
            print(f"    Mixing:        {mixing_count:3d} ({100*mixing_count/total_points:5.1f}%)")
            print(f"    Restructuring: {restructuring_count:3d} ({100*restructuring_count/total_points:5.1f}%)")
            
            # Statistics
            print(f"  Coordinate statistics:")
            print(f"    u: mean={np.mean(all_u_coords):.3f}, std={np.std(all_u_coords):.3f}, range=[{np.min(all_u_coords):.3f}, {np.max(all_u_coords):.3f}]")
            print(f"    v: mean={np.mean(all_v_coords):.3f}, std={np.std(all_v_coords):.3f}, range=[{np.min(all_v_coords):.3f}, {np.max(all_v_coords):.3f}]")
        else:
            print(f"  No valid data points found for u = {u}")
        
        # Store processed data
        processed_data[u] = {
            'u_coords': all_u_coords.tolist(),
            'v_coords': all_v_coords.tolist(),
            'classification': {
                'dominance': dominance_count,
                'mixing': mixing_count,
                'restructuring': restructuring_count,
                'total': total_points
            },
            'statistics': {
                'u_mean': float(np.mean(all_u_coords)) if total_points > 0 else 0,
                'u_std': float(np.std(all_u_coords)) if total_points > 0 else 0,
                'v_mean': float(np.mean(all_v_coords)) if total_points > 0 else 0,
                'v_std': float(np.std(all_v_coords)) if total_points > 0 else 0
            }
        }
    
    # Save processed data
    output_file = f"{output_dir}/processed_test_data.json"
    with open(output_file, 'w') as f:
        json.dump(processed_data, f, indent=2)
    
    print(f"\nProcessed data saved to: {output_file}")
    
    # Summary across all interaction strengths
    print(f"\n{'='*60}")
    print("SUMMARY ACROSS ALL INTERACTION STRENGTHS")
    print(f"{'='*60}")
    
    for u in u_values:
        data = processed_data[u]
        total = data['classification']['total']
        if total > 0:
            dom_pct = 100 * data['classification']['dominance'] / total
            mix_pct = 100 * data['classification']['mixing'] / total
            res_pct = 100 * data['classification']['restructuring'] / total
            
            print(f"\nu = {u}:")
            print(f"  Total points: {total}")
            print(f"  Dominance: {dom_pct:5.1f}%")
            print(f"  Mixing: {mix_pct:5.1f}%")
            print(f"  Restructuring: {res_pct:5.1f}%")
    
    print(f"\nAnalysis complete!")
    return processed_data


if __name__ == "__main__":
    analyze_test_data()