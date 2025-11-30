#!/usr/bin/env python3
"""
Final 100-repetition 48-species coalescence simulation
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

def simulate_100_reps():
    """Run the full 100 repetitions simulation"""
    
    # Simulation parameters
    session_name = "Simulation_Data/48species_100reps_final"
    
    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")
    
    # Parameters
    N_reps = 100  # Full 100 repetitions
    N = 48  # Total species pool
    num_S = 12  # Species per community
    num_C = 4  # Number of communities (48/12 = 4)
    u_list = [0.3, 0.6, 0.8]  # Three interaction strengths
    o = 0  # Offset parameter
    t = [0, 2000]  # Time span
    threshold = 1e-3  # Extinction threshold
    
    print(f"\n{'='*80}")
    print(f"RUNNING 100-REPETITION 48-SPECIES COALESCENCE SIMULATION")
    print(f"{'='*80}")
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Repetitions per intensity: {N_reps}")
    print(f"Interaction strengths: {u_list}")
    print(f"Expected runtime: ~10 minutes")
    
    output_file = session_name + '/Community_100reps_final.json'
    
    print(f"\nStarting simulation...")
    overall_start_time = time.time()
    
    # Run simulation
    all_results = {}
    total_tasks = len(u_list) * N_reps
    task_count = 0
    
    for i, u in enumerate(u_list):
        print(f"\n{'='*50}")
        print(f"Processing interaction strength u = {u:.1f} ({i+1}/{len(u_list)})")
        print(f"{'='*50}")
        
        intensity_start_time = time.time()
        all_results[str(u)] = {}
        
        for rep in range(N_reps):
            task_count += 1
            
            if rep % 10 == 0:
                elapsed = time.time() - overall_start_time
                remaining_tasks = total_tasks - task_count
                rate = task_count / elapsed if elapsed > 0 else 0
                eta = remaining_tasks / rate if rate > 0 else 0
                print(f"  Rep {rep+1:3d}/{N_reps} | Progress: {task_count:3d}/{total_tasks} | ETA: {eta/60:.1f} min")
            
            # Set unique random seed
            seed = int(u * 1000) + rep * 10000 + 12345  # Add offset to avoid collision with test data
            np.random.seed(seed)
            
            # Initialize species pool
            I, g, k = initialize_species_pool(N, lambda: uniform_distribution(u, o))
            
            # Create communities
            CommunitiesLibrary = initialize_random_communities(N, num_C, num_S)
            
            # Initialize abundances
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
        
        intensity_end_time = time.time()
        print(f"  Intensity u={u} completed in {(intensity_end_time - intensity_start_time)/60:.1f} minutes")
        
        # Save intermediate results
        print(f"  Saving intermediate results...")
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2)
    
    # Save final results
    print(f"\nSaving final results...")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    overall_end_time = time.time()
    total_time = overall_end_time - overall_start_time
    
    print(f"\n{'='*80}")
    print(f"SIMULATION COMPLETED SUCCESSFULLY!")
    print(f"{'='*80}")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Rate: {total_tasks/(total_time/60):.1f} simulations per minute")
    print(f"Data saved to: {output_file}")
    
    # Quick verification
    print(f"\nVerification:")
    for u in u_list:
        reps = len(all_results[str(u)])
        example_rep = all_results[str(u)]['rep_000']
        communities = len(example_rep['sc_list'])
        pairs = len(example_rep['cc_list'])
        print(f"  u = {u}: {reps} repetitions, {communities} communities, {pairs} coalescence pairs each")
    
    total_coalescence_events = len(u_list) * N_reps * 6  # 6 pairs per rep
    print(f"\nTotal coalescence events: {total_coalescence_events}")
    print(f"Ready for analysis and visualization!")
    
    return output_file

if __name__ == "__main__":
    simulate_100_reps()