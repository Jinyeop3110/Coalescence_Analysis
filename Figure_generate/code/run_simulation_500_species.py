#!/usr/bin/env python
"""
Large Species Pool Simulation (500 Species)

This script runs Lotka-Volterra simulations with:
- 500 total species
- 50 species per community  
- Constant carrying capacity (var_k = 0)
- Varying interaction strengths (u from 0 to 1.2)

Run this script with:
conda activate coalescence
python run_simulation_500_species.py
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathos.multiprocessing import ProcessingPool as Pool
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from InitializeSpeciesPool import InitializeSpeciesPool
from LV import run_lotka_volterra
from VariousMetrics import *


def uniform_distribution(u, o):
    """Generate uniform random interaction strength."""
    return (2*u + 2*o) * np.random.random() - o


def InitializeRandomCommunityPool_500(N, num_C, num_S, I, g, k, save_path="Data/test"):
    """
    Initialize random non-overlapping communities for large species pool.
    
    Parameters:
    - N: Total number of species (500)
    - num_C: Number of communities to create
    - num_S: Number of species per community (50)
    - I, g, k: Interaction matrix, growth rates, carrying capacities
    - save_path: Where to save the community library
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
            # If we run out of species, wrap around or handle as needed
            print(f"Warning: Not enough species for community {i}")
            break
    
    # Save community library
    df1 = pd.DataFrame(CommunitiesLibrary)
    with pd.ExcelWriter(save_path + '/communityLibrary.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Sheet1')
    
    return CommunitiesLibrary


def simulate_task_500(task):
    """Run simulation for one parameter combination."""
    i, itt, u, session_name, t, N, o, threshold, num_C, num_S, f_k = task
    
    # Set random seed for reproducibility
    np.random.seed(itt + i * 1000)  # Different seed for each task
    
    # Initialize interaction function
    f_interaction = lambda: uniform_distribution(u, o)
    
    # Initialize species pool
    I, g, k = InitializeSpeciesPool(N, f_interaction, 
                                    f_g=lambda: np.ones(1),
                                    f_k=f_k, 
                                    is_diagonal_one=True, 
                                    save_path=session_name)
    
    # Create random communities
    CommunitiesLibrary = InitializeRandomCommunityPool_500(N, num_C, num_S, I, g, k, 
                                                           save_path=session_name)
    
    # Initialize with small random abundances
    y = np.random.rand(N) * 0.1
    
    # Run single community simulations
    sc_list = {}
    for idx in range(num_C):
        # Run to steady state
        y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
        y1[y1 < threshold] = 0
        sc_list[idx] = y1.tolist()
    
    # Run coalescence simulations (pairwise)
    cc_list = {}
    for idx in range(num_C):
        for jdx in range(idx + 1, num_C):
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
    
    return (u, itt, sc_list, cc_list)


def main():
    """Main simulation function."""
    # Simulation parameters for 500 species
    session_name = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500"
    
    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")
    
    # Parameters
    N_simul = 4  # Number of simulation replicates (reduced due to larger size)
    N = 500  # Total species pool
    num_S = 50  # Species per community
    num_C = 10  # Number of communities (500/50 = 10 max non-overlapping)
    u_list = np.arange(0, 1.3, 0.1)  # Interaction strength range
    o = 0  # Offset parameter
    t = [0, 5000]  # Time span
    threshold = 1e-3  # Extinction threshold
    
    # Fixed carrying capacity (var_k = 0)
    var_k = 0
    f_k = lambda: 1  # Constant carrying capacity
    
    print(f"\nSimulation Configuration:")
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Simulation replicates: {N_simul}")
    print(f"Interaction strengths: {u_list}")
    print(f"Carrying capacity variance: {var_k} (constant)")
    
    # Check if we need to run the simulation
    Intention_to_reset = True
    
    if Intention_to_reset or not os.path.isfile(session_name + '/Community.json'):
        print("\nStarting simulation...")
        start_time = time.time()
        
        # Prepare tasks for parallel processing
        tasks = []
        for i, u in enumerate(u_list):
            for itt in range(N_simul):
                tasks.append((i, itt, u, session_name, t, N, o, threshold, num_C, num_S, f_k))
        
        print(f"Total number of tasks: {len(tasks)}")
        
        # Run simulations in parallel
        print("\nRunning simulations in parallel...")
        with Pool(processes=4) as pool:  # Use fewer processes due to memory constraints
            results = list(tqdm(pool.imap(simulate_task_500, tasks), total=len(tasks)))
        
        # Aggregate results
        print("\nAggregating results...")
        all_results = {}
        for u, itt, sc_list, cc_list in results:
            if u not in all_results:
                all_results[u] = {}
            all_results[u][f"community_{itt}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list
            }
        
        # Save results
        print("\nSaving results...")
        with open(session_name + '/Community.json', 'w') as f:
            json.dump(all_results, f, indent=4)
        
        end_time = time.time()
        print(f"\nSimulation completed successfully!")
        print(f"Total time: {end_time - start_time:.2f} seconds")
        print(f"Data saved to: {session_name}/Community.json")
        
    else:
        print(f"\nSimulation data already exists at: {session_name}/Community.json")
        print("Set Intention_to_reset = True to rerun simulation.")
    
    # Verify output
    if os.path.exists(session_name + '/Community.json'):
        with open(session_name + '/Community.json', 'r') as f:
            loaded_results = json.load(f)
        
        print("\nData structure:")
        print(f"Interaction strengths: {list(loaded_results.keys())}")
        
        # Check one example
        first_u = list(loaded_results.keys())[0]
        first_community = list(loaded_results[first_u].keys())[0]
        
        print(f"\nExample data for u={first_u}, {first_community}:")
        print(f"Number of single communities: {len(loaded_results[first_u][first_community]['sc_list'])}")
        print(f"Number of coalescence pairs: {len(loaded_results[first_u][first_community]['cc_list'])}")
        
        # Check species richness
        example_sc = loaded_results[first_u][first_community]['sc_list']['0']
        species_present = sum(1 for x in example_sc if x > threshold)
        print(f"\nExample community 0:")
        print(f"Species present: {species_present} / {num_S} initial")
        print(f"Total abundance: {sum(example_sc):.4f}")


if __name__ == "__main__":
    main()