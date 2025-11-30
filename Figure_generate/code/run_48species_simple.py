#!/usr/bin/env python
"""
Simplified 48 Species Simulation with 100 Repetitions

This script runs Lotka-Volterra simulations with:
- 48 total species
- 12 species per community  
- 100 independent repetitions per interaction strength
- 3 interaction strengths: 0.3, 0.5, 0.8
"""

import os
import json
import time
import numpy as np
import pandas as pd
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
    
    y = solve_ivp(f, t, y0_simul, method='RK23')
    y = y.y[:,-1]
    y_out = np.zeros(N)
    for i in range(y.shape[0]):
        y_out[s_idx[i]] = y[i] 
    return y_out


def uniform_distribution(u, o):
    """Generate uniform random interaction strength."""
    return (2*u + 2*o) * np.random.random() - o


def initialize_species_pool(N, f_interaction, save_path=None):
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


def simulate_48_species_simple():
    """Run the simplified 48 species simulation with 100 repetitions."""
    
    # Simulation parameters
    session_name = "Simulation_Data/48species_100reps"
    
    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")
    
    # Parameters
    N_reps = 100  # Number of repetitions per interaction strength
    N = 48  # Total species pool
    num_S = 12  # Species per community
    num_C = 4  # Number of communities (48/12 = 4)
    u_list = [0.3, 0.5, 0.8]  # Three interaction strengths
    o = 0  # Offset parameter
    t = [0, 5000]  # Time span
    threshold = 1e-3  # Extinction threshold
    
    print(f"\nSimulation Configuration:")
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Repetitions per intensity: {N_reps}")
    print(f"Interaction strengths: {u_list}")
    
    # Check if we need to run the simulation
    output_file = session_name + '/Community_100reps.json'
    if os.path.isfile(output_file):
        print(f"\nSimulation data already exists at: {output_file}")
        print("Overwriting existing data...")
    
    print("\nStarting simulation...")
    start_time = time.time()
    
    # Run simulation
    all_results = {}
    total_tasks = len(u_list) * N_reps
    task_count = 0
    
    for i, u in enumerate(u_list):
        print(f"\n{'='*50}")
        print(f"Processing interaction strength u = {u:.1f} ({i+1}/{len(u_list)})")
        print(f"{'='*50}")
        
        all_results[str(u)] = {}  # Use string keys for JSON compatibility
        
        for rep in range(N_reps):
            task_count += 1
            rep_start_time = time.time()
            
            if rep % 10 == 0:
                print(f"  Repetition {rep+1}/{N_reps} (Overall progress: {task_count}/{total_tasks})")
            
            # Set unique random seed for each repetition
            seed = int(u * 1000) + rep * 10000
            np.random.seed(seed)
            
            # Initialize NEW species pool for each repetition
            I, g, k = initialize_species_pool(N, lambda: uniform_distribution(u, o))
            
            # Create random communities
            CommunitiesLibrary = initialize_random_communities(N, num_C, num_S)
            
            # Initialize with small random abundances
            y = np.random.rand(N) * 0.1
            
            # Run single community simulations
            sc_list = {}
            for idx in range(num_C):
                y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
                y1[y1 < threshold] = 0
                sc_list[str(idx)] = y1.tolist()  # Use string keys
            
            # Run coalescence simulations (all pairwise combinations)
            cc_list = {}
            
            for idx in range(num_C):
                for jdx in range(idx + 1, num_C):
                    # Get steady states of individual communities
                    y1 = np.array(sc_list[str(idx)])
                    y2 = np.array(sc_list[str(jdx)])
                    
                    # Mix communities (equal proportions)
                    y3 = (y1 + y2) / 2
                    
                    # Run to new steady state
                    survived = y3 > threshold
                    y3 = run_lotka_volterra(y3, t, survived, I, g, k)
                    y3[y3 < threshold] = 0
                    
                    cc_list[f"{idx}_{jdx}"] = y3.tolist()
            
            # Store results for this repetition
            all_results[str(u)][f"rep_{rep:03d}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list,
                "parameters": {
                    "seed": seed,
                    "interaction_matrix_stats": {
                        "mean": float(np.mean(I[np.triu_indices(N, k=1)])),
                        "std": float(np.std(I[np.triu_indices(N, k=1)]))
                    }
                }
            }
            
            # Save intermediate results every 20 repetitions
            if (rep + 1) % 20 == 0:
                print(f"    Saving intermediate results (rep {rep+1})...")
                with open(output_file, 'w') as f:
                    json.dump(all_results, f, indent=2)
    
    # Save final results
    print("\nSaving final results...")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    end_time = time.time()
    print(f"\nSimulation completed successfully!")
    print(f"Total time: {(end_time - start_time)/60:.2f} minutes")
    print(f"Data saved to: {output_file}")
    
    # Verify output and print summary statistics
    print("\n" + "="*50)
    print("SIMULATION SUMMARY")
    print("="*50)
    
    for u in u_list:
        print(f"\nInteraction strength u = {u}:")
        print(f"  Number of repetitions: {len(all_results[str(u)])}")
        
        # Check one example
        first_rep = list(all_results[str(u)].keys())[0]
        example_data = all_results[str(u)][first_rep]
        
        print(f"  Number of single communities: {len(example_data['sc_list'])}")
        print(f"  Number of coalescence pairs: {len(example_data['cc_list'])}")
        
        # Check species richness across first 5 reps
        richness_values = []
        for rep_key in list(all_results[str(u)].keys())[:5]:
            for comm_idx in all_results[str(u)][rep_key]['sc_list'].keys():
                sc = all_results[str(u)][rep_key]['sc_list'][comm_idx]
                species_present = sum(1 for x in sc if x > threshold)
                richness_values.append(species_present)
        
        if richness_values:
            print(f"  Average species richness (first 5 reps): {np.mean(richness_values):.2f} ± {np.std(richness_values):.2f}")


if __name__ == "__main__":
    simulate_48_species_simple()