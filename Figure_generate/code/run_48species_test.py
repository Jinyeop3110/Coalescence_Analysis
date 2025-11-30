#!/usr/bin/env python
"""
Test version: 48 Species Simulation with 10 Repetitions for quick testing

This script runs a smaller version for testing:
- 48 total species
- 12 species per community  
- 10 repetitions per interaction strength (instead of 100)
- 3 interaction strengths: 0.3, 0.5, 0.8
"""

import os
import json
import time
import numpy as np
from scipy.integrate import solve_ivp


def gLV(y, t, I_simul, g_simul, k_simul):
    """Generalized Lotka-Volterra dynamics"""
    dydt = np.zeros_like(y)
    for i in range(len(y)):
        dydt[i] = g_simul[i] * y[i] * (1 - (np.sum(I_simul[i,:] * y) / k_simul[i]))
    return dydt


def run_lotka_volterra(y0, t, s_idx, I, g, k):
    """Run Lotka-Volterra simulation"""
    s_idx = np.where(s_idx)[0].tolist()
    N = len(y0)
    y0_simul = y0[s_idx]
    I_simul = I[s_idx,:]
    I_simul = I_simul[:,s_idx]
    g_simul = g[s_idx]
    k_simul = k[s_idx]
    
    def f(t,y): 
        return gLV(y, t, I_simul, g_simul, k_simul)
    
    # Use shorter time span for faster computation
    y = solve_ivp(f, t, y0_simul, method='RK45', rtol=1e-6)
    y = y.y[:,-1]
    y_out = np.zeros(N)
    for i in range(y.shape[0]):
        y_out[s_idx[i]] = y[i] 
    return y_out


def uniform_distribution(u, o):
    """Generate uniform random interaction strength."""
    return (2*u + 2*o) * np.random.random() - o


def initialize_species_pool(N, f_interaction):
    """Initialize species pool with interaction matrix and parameters"""
    I = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            I[i,j] = f_interaction()
    
    # Set diagonal to 1 (self-interaction)
    for i in range(N):
        I[i,i] = 1
    
    # Simple growth rates and carrying capacities
    g = np.ones(N)
    k = np.ones(N)
    
    return I, g, k


def initialize_random_communities(N, num_C, num_S):
    """Initialize random non-overlapping communities"""
    CommunitiesLibrary = np.zeros([num_C, N])
    
    # Generate random permutation of all species
    all_species = np.random.permutation(N)
    
    # Assign species to communities
    for i in range(num_C):
        start_idx = i * num_S
        end_idx = start_idx + num_S
        
        if end_idx <= N:
            selected_species = all_species[start_idx:end_idx]
            CommunitiesLibrary[i, selected_species] = 1
    
    return CommunitiesLibrary


def simulate_test():
    """Run the test simulation with 10 repetitions."""
    
    # Simulation parameters
    session_name = "Simulation_Data/48species_test"
    
    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")
    
    # Parameters - reduced for testing
    N_reps = 10  # Only 10 repetitions for testing
    N = 48  # Total species pool
    num_S = 12  # Species per community
    num_C = 4  # Number of communities (48/12 = 4)
    u_list = [0.3, 0.5, 0.8]  # Three interaction strengths
    o = 0  # Offset parameter
    t = [0, 2000]  # Shorter time span for faster computation
    threshold = 1e-3  # Extinction threshold
    
    print(f"\nTEST Simulation Configuration:")
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Repetitions per intensity: {N_reps}")
    print(f"Interaction strengths: {u_list}")
    print(f"Time span: {t}")
    
    output_file = session_name + '/Community_test.json'
    
    print("\nStarting test simulation...")
    start_time = time.time()
    
    # Run simulation
    all_results = {}
    total_tasks = len(u_list) * N_reps
    task_count = 0
    
    for i, u in enumerate(u_list):
        print(f"\nProcessing interaction strength u = {u:.1f} ({i+1}/{len(u_list)})")
        
        all_results[str(u)] = {}
        
        for rep in range(N_reps):
            task_count += 1
            print(f"  Rep {rep+1}/{N_reps} (Task {task_count}/{total_tasks})")
            
            # Set unique random seed
            seed = int(u * 1000) + rep * 10000
            np.random.seed(seed)
            
            # Initialize species pool
            I, g, k = initialize_species_pool(N, lambda: uniform_distribution(u, o))
            
            # Create communities
            CommunitiesLibrary = initialize_random_communities(N, num_C, num_S)
            
            # Initialize with small random abundances
            y = np.random.rand(N) * 0.1
            
            # Run single community simulations
            sc_list = {}
            for idx in range(num_C):
                y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
                y1[y1 < threshold] = 0
                sc_list[str(idx)] = y1.tolist()
            
            # Run coalescence simulations
            cc_list = {}
            for idx in range(num_C):
                for jdx in range(idx + 1, num_C):
                    y1 = np.array(sc_list[str(idx)])
                    y2 = np.array(sc_list[str(jdx)])
                    y3 = (y1 + y2) / 2
                    
                    survived = y3 > threshold
                    y3 = run_lotka_volterra(y3, t, survived, I, g, k)
                    y3[y3 < threshold] = 0
                    
                    cc_list[f"{idx}_{jdx}"] = y3.tolist()
            
            # Store results
            all_results[str(u)][f"rep_{rep:03d}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list,
                "parameters": {"seed": seed}
            }
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    end_time = time.time()
    print(f"\nTest simulation completed!")
    print(f"Total time: {(end_time - start_time)/60:.2f} minutes")
    print(f"Data saved to: {output_file}")
    
    # Summary
    for u in u_list:
        print(f"\nInteraction strength u = {u}:")
        print(f"  Repetitions: {len(all_results[str(u)])}")
        example_data = all_results[str(u)]["rep_000"]
        print(f"  Communities: {len(example_data['sc_list'])}")
        print(f"  Coalescence pairs: {len(example_data['cc_list'])}")


if __name__ == "__main__":
    simulate_test()