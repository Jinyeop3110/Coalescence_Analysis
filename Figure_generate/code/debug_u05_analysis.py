#!/usr/bin/env python3
"""
Debug u=0.5 analysis to understand the polarization pattern
"""

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

def debug_u05():
    with open('Simulation_Data/48species_100reps_final/Community_100reps_final.json', 'r') as f:
        data = json.load(f)
    
    print("Debugging u=0.5 analysis:")
    print("=" * 50)
    
    u_coords = []
    v_coords = []
    problem_cases = []
    
    # Analyze first few reps in detail
    rep_count = 0
    for rep_key in sorted(data['0.5'].keys())[:5]:  # First 5 reps
        rep_data = data['0.5'][rep_key]
        rep_count += 1
        
        print(f"\nRep {rep_count} ({rep_key}):")
        
        sc_list = rep_data['sc_list']
        cc_list = rep_data['cc_list']
        
        # Check single communities first
        for idx in range(4):
            c = np.array(sc_list[str(idx)])
            alive = np.sum(c > 1e-4)
            total_biomass = np.sum(c)
            print(f"  Community {idx}: {alive} alive, total biomass = {total_biomass:.3f}")
        
        # Check coalescence pairs
        for pair_key, c_mix in cc_list.items():
            idx, jdx = map(int, pair_key.split('_'))
            
            c_1 = np.array(sc_list[str(idx)])
            c_2 = np.array(sc_list[str(jdx)])
            c_mix = np.array(c_mix)
            
            # Filter small values
            c_1 = c_1 * (c_1 > 1e-4)
            c_2 = c_2 * (c_2 > 1e-4)
            
            c1_alive = np.sum(c_1 > 0)
            c2_alive = np.sum(c_2 > 0)
            cmix_alive = np.sum(c_mix > 0)
            
            print(f"    Pair {pair_key}: C1({c1_alive} alive), C2({c2_alive} alive) → Mix({cmix_alive} alive)")
            print(f"      Biomass: C1={np.sum(c_1):.3f}, C2={np.sum(c_2):.3f}, Mix={np.sum(c_mix):.3f}")
            
            if c1_alive > 0 and c2_alive > 0 and cmix_alive > 0:
                try:
                    u_coord, v_coord, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                    
                    print(f"      Vector decomp: u={u_coord:.3f}, v={v_coord:.3f}, k={k:.3f}")
                    
                    if not (np.isnan(u_coord) or np.isnan(v_coord)):
                        u_coords.append(u_coord)
                        v_coords.append(v_coord)
                        
                        # Check for extreme values
                        if u_coord < 0.1 and v_coord < 0.1:
                            problem_cases.append({
                                'rep': rep_key,
                                'pair': pair_key, 
                                'coords': (u_coord, v_coord),
                                'c1_alive': c1_alive,
                                'c2_alive': c2_alive,
                                'cmix_alive': cmix_alive,
                                'c1_biomass': np.sum(c_1),
                                'c2_biomass': np.sum(c_2),
                                'cmix_biomass': np.sum(c_mix)
                            })
                    else:
                        print(f"      WARNING: NaN coordinates!")
                        
                except Exception as e:
                    print(f"      ERROR in vector decomposition: {e}")
            else:
                print(f"      SKIPPED: Missing communities")
    
    print(f"\n" + "=" * 50)
    print(f"Summary from first 5 reps:")
    print(f"Total valid coordinates: {len(u_coords)}")
    print(f"Problem cases (u<0.1, v<0.1): {len(problem_cases)}")
    
    if problem_cases:
        print(f"\nProblem case analysis:")
        for case in problem_cases[:3]:  # Show first 3
            print(f"  {case['rep']} {case['pair']}: coords=({case['coords'][0]:.3f}, {case['coords'][1]:.3f})")
            print(f"    Alive: C1={case['c1_alive']}, C2={case['c2_alive']}, Mix={case['cmix_alive']}")
            print(f"    Biomass: C1={case['c1_biomass']:.3f}, C2={case['c2_biomass']:.3f}, Mix={case['cmix_biomass']:.3f}")
    
    # Overall statistics
    if u_coords:
        u_array = np.array(u_coords)
        v_array = np.array(v_coords)
        print(f"\nCoordinate statistics (first 5 reps):")
        print(f"u: min={np.min(u_array):.3f}, max={np.max(u_array):.3f}, mean={np.mean(u_array):.3f}")
        print(f"v: min={np.min(v_array):.3f}, max={np.max(v_array):.3f}, mean={np.mean(v_array):.3f}")

if __name__ == "__main__":
    debug_u05()