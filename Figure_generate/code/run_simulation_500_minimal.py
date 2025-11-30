#!/usr/bin/env python
"""
Minimal 500 Species Simulation with Full U-Range

This script runs Lotka-Volterra simulations with minimal dependencies:
- 500 total species
- 50 species per community  
- Full interaction strength range (0.1 to 1.2)
- Self-contained vector decomposition function

Usage:
python run_simulation_500_minimal.py
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import warnings
warnings.filterwarnings('ignore')


def uniform_distribution(u, o):
    """Generate uniform random interaction strength in range [0, 2u]."""
    return (2*u + 2*o) * np.random.random() - o


def run_lotka_volterra_minimal(y0, tspan, I, g, k, threshold=1e-6):
    """
    Minimal Lotka-Volterra integration function.
    """
    def derivative(t, y):
        """Derivative for generalized Lotka-Volterra equation."""
        y = np.maximum(y, 0)  # Ensure non-negative
        # dy/dt = y * (g - y/k - I*y)
        return y * (g - y/k - np.dot(I, y))
    
    # Solve the differential equation
    sol = solve_ivp(derivative, tspan, y0, method='RK45', 
                   dense_output=True, rtol=1e-6, atol=1e-9)
    
    if sol.success:
        final_state = sol.y[:, -1]
        final_state[final_state < threshold] = 0
        return final_state
    else:
        # If integration fails, return initial state
        return y0


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """
    Vector decomposition for coalescence analysis.
    
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


def InitializeRandomCommunityPool_500(N, num_C, num_S, save_path="Data/test"):
    """
    Initialize random non-overlapping communities for large species pool.
    """
    # Create non-overlapping communities
    CommunitiesLibrary = np.zeros([num_C, N])
    
    # Generate random permutation of all species
    all_species = np.random.permutation(N)
    
    # Assign species to communities
    for i in range(num_C):
        # Select species for this community
        start_idx = i * num_S
        end_idx = start_idx + num_S
        
        if end_idx <= N:
            selected_species = all_species[start_idx:end_idx]
            CommunitiesLibrary[i, selected_species] = 1
        else:
            print(f"Warning: Not enough species for community {i}")
            break
    
    # Save community library
    df1 = pd.DataFrame(CommunitiesLibrary)
    with pd.ExcelWriter(save_path + '/communityLibrary.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Sheet1')
    
    return CommunitiesLibrary


def simulate_500_species():
    """Run the 500 species simulation with full u-range."""
    
    # Simulation parameters for 500 species - Natural Communities
    session_name = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full"
    
    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")
    
    # Parameters - reduced for faster execution
    N_simul = 2  # Number of simulation replicates
    N = 500  # Total species pool
    num_S = 50  # Species per community
    num_C = 8  # Number of communities (reduced for speed)
    u_list = np.arange(0.1, 1.3, 0.1)  # Full interaction strength range: 0.1, 0.2, ..., 1.2
    o = 0  # Offset parameter
    t = [0, 3000]  # Time span (reduced for speed)
    threshold = 1e-3  # Extinction threshold
    
    print(f"500-SPECIES SIMULATION - FULL U-RANGE (MINIMAL)")
    print(f"="*55)
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Simulation replicates: {N_simul}")
    print(f"Interaction strengths: {len(u_list)} values from {u_list[0]:.1f} to {u_list[-1]:.1f}")
    print(f"Time span: {t[0]} to {t[1]}")
    
    # Check if we need to run the simulation
    if os.path.isfile(session_name + '/Community.json'):
        print(f"\nSimulation data already exists at: {session_name}/Community.json")
        print("Delete the file to rerun simulation.")
        return
    
    print(f"\nStarting simulation...")
    print(f"Total tasks: {len(u_list)} × {N_simul} = {len(u_list) * N_simul}")
    start_time = time.time()
    
    # Run simulation
    all_results = {}
    total_tasks = len(u_list) * N_simul
    task_count = 0
    
    for i, u in enumerate(u_list):
        print(f"\n[{i+1}/{len(u_list)}] Processing u = {u:.1f}")
        
        for itt in range(N_simul):
            task_count += 1
            elapsed = time.time() - start_time
            print(f"  Rep {itt+1}/{N_simul} (Task {task_count}/{total_tasks}) - {elapsed:.1f}s elapsed")
            
            # Set random seed for reproducibility
            np.random.seed(itt + i * 1000)
            
            # Initialize interaction matrix
            print("    Initializing interaction matrix...")
            I = np.zeros((N, N))
            for ii in range(N):
                for jj in range(N):
                    if ii != jj:
                        I[ii, jj] = uniform_distribution(u, o) / N
            np.fill_diagonal(I, 1.0)  # Self-interaction
            
            # Initialize growth rates and carrying capacities
            g = np.ones(N)
            k = np.ones(N)
            
            # Save parameters
            df1 = pd.DataFrame({'g': g, 'k': k})
            df2 = pd.DataFrame(I)
            with pd.ExcelWriter(session_name + '/parameter.xlsx') as writer:  
                df1.to_excel(writer, sheet_name='Sheet1')
                df2.to_excel(writer, sheet_name='Sheet2')
            
            # Create random communities
            print("    Creating communities...")
            CommunitiesLibrary = InitializeRandomCommunityPool_500(N, num_C, num_S, 
                                                                   save_path=session_name)
            
            # Run single community simulations
            print("    Running single community simulations...")
            sc_list = {}
            for idx in range(num_C):
                if idx % 3 == 0:  # Progress indicator
                    print(f"      Community {idx+1}/{num_C}")
                
                # Initial state for this community
                y_init = CommunitiesLibrary[idx, :] * np.random.rand(N) * 0.1
                y_final = run_lotka_volterra_minimal(y_init, t, I, g, k, threshold)
                
                # Normalize
                if np.sum(y_final) > 0:
                    y_final = y_final / np.sum(y_final)
                
                sc_list[str(idx)] = y_final.tolist()
            
            # Run coalescence simulations (pairwise)
            print("    Running coalescence simulations...")
            cc_list = {}
            pair_count = 0
            total_pairs = num_C * (num_C - 1) // 2
            
            for idx in range(num_C):
                for jdx in range(idx + 1, num_C):
                    pair_count += 1
                    if pair_count % 10 == 0:  # Progress indicator
                        print(f"      Pair {pair_count}/{total_pairs}")
                    
                    # Get steady states of individual communities
                    y1 = np.array(sc_list[str(idx)])
                    y2 = np.array(sc_list[str(jdx)])
                    
                    # Mix communities (50:50)
                    y_mixed = (y1 + y2) / 2
                    
                    # Run to new steady state
                    y_final = run_lotka_volterra_minimal(y_mixed, t, I, g, k, threshold)
                    
                    # Normalize
                    if np.sum(y_final) > 0:
                        y_final = y_final / np.sum(y_final)
                    
                    cc_list[f"{idx}_{jdx}"] = y_final.tolist()
            
            print(f"    → Generated {len(sc_list)} single communities and {len(cc_list)} coalescence pairs")
            
            # Store results
            if f'{u:.1f}' not in all_results:
                all_results[f'{u:.1f}'] = {}
            all_results[f'{u:.1f}'][f"community_{itt}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list
            }
        
        # Progress update
        elapsed = time.time() - start_time
        remaining_u = len(u_list) - (i + 1)
        avg_time_per_u = elapsed / (i + 1)
        est_remaining = remaining_u * avg_time_per_u
        print(f"  ✓ u={u:.1f} complete. Est. {est_remaining:.1f}s remaining")
    
    # Save results
    print(f"\nSaving results to {session_name}/Community.json...")
    with open(session_name + '/Community.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    end_time = time.time()
    print(f"\n🎉 Simulation completed successfully!")
    print(f"   Total time: {end_time - start_time:.1f} seconds")
    print(f"   Total u-values: {len(u_list)}")
    print(f"   Data saved to: {session_name}/Community.json")
    
    # Verify output
    with open(session_name + '/Community.json', 'r') as f:
        loaded_results = json.load(f)
    
    print(f"\nData structure verification:")
    print(f"  Interaction strengths: {list(loaded_results.keys())}")
    
    # Check one example
    first_u = list(loaded_results.keys())[0]
    first_community = list(loaded_results[first_u].keys())[0]
    
    print(f"  Example data for u={first_u}, {first_community}:")
    print(f"  - Single communities: {len(loaded_results[first_u][first_community]['sc_list'])}")
    print(f"  - Coalescence pairs: {len(loaded_results[first_u][first_community]['cc_list'])}")


if __name__ == "__main__":
    simulate_500_species()