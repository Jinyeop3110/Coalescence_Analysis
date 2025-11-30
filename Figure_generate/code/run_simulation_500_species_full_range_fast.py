#!/usr/bin/env python
"""
Fast 500 Species Simulation with Full U-Range

This script runs Lotka-Volterra simulations with:
- 500 total species
- 50 species per community  
- Full interaction strength range (0.1 to 1.2)
- Reduced parameters for faster execution

Usage:
conda activate coalescence
python run_simulation_500_species_full_range_fast.py
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from InitializeSpeciesPool import InitializeSpeceiesPool
from LV import run_lotka_volterra
from VariousMetrics import *


def uniform_distribution(u, o):
    """Generate uniform random interaction strength."""
    return (2*u + 2*o) * np.random.random() - o


def InitializeRandomCommunityPool_500(N, num_C, num_S, I, g, k, save_path="Data/test"):
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
        species_indices = all_species[start_idx:end_idx]
        
        # Set abundance for selected species
        CommunitiesLibrary[i, species_indices] = 1.0
    
    # Normalize communities
    for i in range(num_C):
        total = np.sum(CommunitiesLibrary[i])
        if total > 0:
            CommunitiesLibrary[i] = CommunitiesLibrary[i] / total
    
    return CommunitiesLibrary


def main():
    print("="*60)
    print("500-SPECIES SIMULATION - FULL U-RANGE (FAST VERSION)")
    print("="*60)
    
    # Create session directory  
    session_name = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full"
    if not os.path.isdir(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")
    
    # Fast parameters for testing
    N_simul = 1  # Single replicate for speed
    N = 500  # Total species pool
    num_S = 50  # Species per community
    num_C = 8  # Reduced communities for faster coalescence
    u_list = np.arange(0.1, 1.3, 0.1)  # Full interaction strength range
    o = 0  # Offset parameter
    t = [0, 2000]  # Reduced time span for speed
    threshold = 1e-3  # Extinction threshold
    var_k = 0  # Constant carrying capacity
    
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Simulation replicates: {N_simul}")
    print(f"Interaction strengths: {len(u_list)} values from {u_list[0]:.1f} to {u_list[-1]:.1f}")
    print(f"Time span: {t[0]} to {t[1]}")
    print(f"Carrying capacity variance: {var_k} (constant)")
    
    # Check if we need to run the simulation
    if os.path.isfile(session_name + '/Community.json'):
        print("\\nSimulation data already exists.")
        print("Delete Community.json to rerun simulation.")
        return
    
    print(f"\\nStarting simulation...")
    print(f"Total tasks: {len(u_list)} × {N_simul} = {len(u_list) * N_simul}")
    
    # Run simulation
    all_results = {}
    total_tasks = len(u_list) * N_simul
    task_count = 0
    
    start_time = time.time()
    
    for i, u in enumerate(u_list):
        print(f"\\n[{i+1}/{len(u_list)}] Processing u = {u:.1f}")
        
        u_results = {}
        
        for itt in range(N_simul):
            task_count += 1
            elapsed = time.time() - start_time
            print(f"  Rep {itt+1}/{N_simul} (Task {task_count}/{total_tasks}) - {elapsed:.1f}s elapsed")
            
            # Set random seed for reproducibility
            np.random.seed(itt + i * 1000)
            
            # Initialize interaction matrix and parameters
            I = uniform_distribution(u, o) * (np.random.random([N, N]) - 0.5) / N
            np.fill_diagonal(I, 0)  # No self-interaction
            
            # Growth rates  
            g = np.ones(N)
            
            # Carrying capacities
            if var_k == 0:
                k = np.ones(N)
            else:
                k = abs(np.random.normal(1, var_k, N))
            
            # Initialize random communities
            CommunitiesLibrary = InitializeRandomCommunityPool_500(N, num_C, num_S, I, g, k)
            
            # Simulate coalescence events
            sc_list = {}
            cc_list = {}
            
            # Store single communities
            for community_idx in range(num_C):
                sc_list[str(community_idx)] = CommunitiesLibrary[community_idx].tolist()
            
            # Simulate pairwise coalescence
            coalescence_count = 0
            for c1 in range(num_C):
                for c2 in range(c1 + 1, num_C):
                    # Initial combined abundance
                    y0 = (CommunitiesLibrary[c1] + CommunitiesLibrary[c2]) / 2
                    
                    # Run Lotka-Volterra simulation
                    try:
                        sol = run_lotka_volterra(y0, t, I, g, k, threshold)
                        final_abundance = sol[:, -1]  # Final time point
                        
                        # Normalize and store
                        if np.sum(final_abundance) > 0:
                            final_abundance = final_abundance / np.sum(final_abundance)
                        
                        key = f"{c1}_{c2}"
                        cc_list[key] = final_abundance.tolist()
                        coalescence_count += 1
                        
                    except Exception as e:
                        print(f"    Warning: Coalescence {c1}-{c2} failed: {e}")
                        continue
            
            print(f"    → Generated {coalescence_count} coalescence events")
            
            # Store results
            u_results[f'community_{itt}'] = {
                'sc_list': sc_list,
                'cc_list': cc_list
            }
        
        all_results[f'{u:.1f}'] = u_results
        
        # Progress update
        elapsed = time.time() - start_time
        remaining_u = len(u_list) - (i + 1)
        avg_time_per_u = elapsed / (i + 1)
        est_remaining = remaining_u * avg_time_per_u
        print(f"  ✓ u={u:.1f} complete. Est. {est_remaining:.1f}s remaining")
    
    # Save results
    print(f"\\nSaving results to {session_name}/Community.json...")
    with open(session_name + '/Community.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    total_time = time.time() - start_time
    print(f"\\n🎉 Simulation complete!")
    print(f"   Total time: {total_time:.1f} seconds")
    print(f"   Total u-values: {len(u_list)}")
    print(f"   Output saved to: {session_name}/Community.json")


if __name__ == "__main__":
    main()