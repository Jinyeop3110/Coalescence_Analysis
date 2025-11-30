#!/usr/bin/env python
"""
Standalone 500 Species Simulation with Full U-Range

This script runs Lotka-Volterra simulations without matplotlib dependencies:
- 500 total species
- 50 species per community  
- Full interaction strength range (0.1 to 1.2)
- Standalone implementation to avoid import issues

Usage:
python run_simulation_500_species_standalone.py
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

from LV import run_lotka_volterra
from VariousMetrics import *


def uniform_distribution(u, o):
    """Generate uniform random interaction strength."""
    return (2*u + 2*o) * np.random.random() - o


def initialize_species_pool_standalone(N, f_interaction, save_path="Data/test"):
    """
    Initialize species pool without matplotlib dependencies.
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Folder '{save_path}' created.")
    
    # Initialize interaction matrix
    I = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            I[i, j] = f_interaction()
    
    # Set diagonal to 1 (self-interaction)
    for i in range(N):
        I[i, i] = 1
              
    # Initialize growth rates (all ones)
    g = np.ones(N)
        
    # Initialize carrying capacities (all ones)
    k = np.ones(N)
        
    # Save parameters to Excel
    df1 = pd.DataFrame({'g': g, 'k': k})
    df2 = pd.DataFrame(I)

    with pd.ExcelWriter(save_path + '/parameter.xlsx') as writer:  
        df1.to_excel(writer, sheet_name='Sheet1')
        df2.to_excel(writer, sheet_name='Sheet2')

    return I, g, k


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
    
    # Parameters
    N_simul = 3  # Number of simulation replicates
    N = 500  # Total species pool
    num_S = 50  # Species per community
    num_C = 10  # Number of communities
    u_list = np.arange(0.1, 1.3, 0.1)  # Full interaction strength range: 0.1, 0.2, ..., 1.2
    o = 0  # Offset parameter
    t = [0, 5000]  # Time span
    threshold = 1e-3  # Extinction threshold
    
    # Fixed carrying capacity (var_k = 0)
    var_k = 0
    
    print(f"500-SPECIES SIMULATION - FULL U-RANGE")
    print(f"="*50)
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Simulation replicates: {N_simul}")
    print(f"Interaction strengths: {len(u_list)} values from {u_list[0]:.1f} to {u_list[-1]:.1f}")
    print(f"Time span: {t[0]} to {t[1]}")
    print(f"Carrying capacity variance: {var_k} (constant)")
    
    # Check if we need to run the simulation
    if os.path.isfile(session_name + '/Community.json'):
        print(f"\nSimulation data already exists at: {session_name}/Community.json")
        print("Delete the file to rerun simulation.")
        return
    
    print(f"\nStarting simulation...")
    print(f"Total tasks: {len(u_list)} × {N_simul} = {len(u_list) * N_simul}")
    start_time = time.time()
    
    # Run simulation without multiprocessing
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
            
            # Initialize species pool without matplotlib dependencies
            print("    Initializing species pool...")
            I, g, k = initialize_species_pool_standalone(N, 
                                                       lambda: uniform_distribution(u, o),
                                                       save_path=session_name)
            
            # Create random communities
            print("    Creating communities...")
            CommunitiesLibrary = InitializeRandomCommunityPool_500(N, num_C, num_S, I, g, k, 
                                                                   save_path=session_name)
            
            # Initialize with small random abundances
            y = np.random.rand(N) * 0.1
            
            # Run single community simulations
            print("    Running single community simulations...")
            sc_list = {}
            for idx in range(num_C):
                if idx % 3 == 0:  # Progress indicator
                    print(f"      Community {idx+1}/{num_C}")
                y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
                y1[y1 < threshold] = 0
                sc_list[idx] = y1.tolist()
            
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
                    y1 = np.array(sc_list[idx])
                    y2 = np.array(sc_list[jdx])
                    
                    # Mix communities
                    y3 = (y1 + y2) / 2
                    
                    # Run to new steady state
                    survived = y3 > threshold
                    y3 = run_lotka_volterra(y3, t, survived, I, g, k)
                    y3[y3 < threshold] = 0
                    
                    cc_list[f"{idx}_{jdx}"] = y3.tolist()
            
            print(f"    → Generated {len(sc_list)} single communities and {len(cc_list)} coalescence pairs")
            
            # Store results
            if str(u) not in all_results:
                all_results[str(u)] = {}
            all_results[str(u)][f"community_{itt}"] = {
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
    
    # Check species richness
    example_sc = loaded_results[first_u][first_community]['sc_list']['0']
    species_present = sum(1 for x in example_sc if x > threshold)
    print(f"  - Species present in example: {species_present} / {num_S} initial")
    print(f"  - Total abundance: {sum(example_sc):.4f}")


if __name__ == "__main__":
    simulate_500_species()