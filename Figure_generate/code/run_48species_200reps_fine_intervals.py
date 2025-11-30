#!/usr/bin/env python
"""
48 Species Simulation with 200 Repetitions and Fine Intensity Intervals

This script runs Lotka-Volterra simulations with:
- 48 total species
- 12 species per community  
- 200 independent repetitions per interaction strength
- 24 interaction strengths: 0.05 to 1.2 in steps of 0.05
- Each repetition initializes a new species pool

Usage:
python run_48species_200reps_fine_intervals.py
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


def InitializeRandomCommunityPool_48(N, num_C, num_S, save_path="Data/test"):
    """
    Initialize random non-overlapping communities for 48 species pool.
    Creates 4 communities of 12 species each.
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


def simulate_48_species_200reps_fine():
    """Run the 48 species simulation with 200 repetitions and fine intensity intervals."""
    
    # Simulation parameters for 48 species - 200 repetitions, fine intervals
    session_name = "Simulation_Data/48species_200reps_fine"
    
    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")
    
    # Parameters
    N_reps = 200  # Number of repetitions per interaction strength
    N = 48  # Total species pool
    num_S = 12  # Species per community
    num_C = 4  # Number of communities (48/12 = 4)
    
    # Fine intensity intervals: 0.05 to 1.2 in steps of 0.05
    u_list = np.arange(0.05, 1.25, 0.05)  # 0.05, 0.10, 0.15, ..., 1.20
    u_list = np.round(u_list, 2)  # Round to avoid floating point precision issues
    
    o = 0  # Offset parameter
    t = [0, 5000]  # Time span
    threshold = 1e-3  # Extinction threshold
    
    print(f"\nFINE INTERVAL SIMULATION CONFIGURATION:")
    print(f"=" * 50)
    print(f"Total species: {N}")
    print(f"Species per community: {num_S}")
    print(f"Number of communities: {num_C}")
    print(f"Repetitions per intensity: {N_reps}")
    print(f"Interaction strength range: {u_list[0]:.2f} to {u_list[-1]:.2f}")
    print(f"Number of intensity values: {len(u_list)}")
    print(f"Intensity step size: 0.05")
    print(f"Total simulations: {len(u_list) * N_reps}")
    print(f"=" * 50)
    
    # Check if we need to run the simulation
    output_file = session_name + '/Community_200reps_fine.json'
    if os.path.isfile(output_file):
        print(f"\nSimulation data already exists at: {output_file}")
        user_input = input("Do you want to overwrite? (y/n): ")
        if user_input.lower() != 'y':
            print("Exiting without running simulation.")
            return
    
    # Save parameters
    params_dict = {
        'N': N,
        'num_S': num_S,
        'num_C': num_C,
        'N_reps': N_reps,
        'u_list': u_list.tolist(),
        'u_range': f'{u_list[0]:.2f} to {u_list[-1]:.2f}',
        'u_step': 0.05,
        'o': o,
        't': t,
        'threshold': threshold,
        'simulation_type': 'fine_intervals'
    }
    
    param_df = pd.DataFrame([params_dict])
    param_df.to_excel(f"{session_name}/parameter.xlsx", index=False)
    print(f"✓ Parameters saved to: {session_name}/parameter.xlsx")
    
    print("\nStarting simulation...")
    start_time = time.time()
    
    # Run simulation
    all_results = {}
    total_tasks = len(u_list) * N_reps
    task_count = 0
    
    for i, u in enumerate(u_list):
        print(f"\n{'='*60}")
        print(f"Processing interaction strength u = {u:.2f} ({i+1}/{len(u_list)})")
        print(f"{'='*60}")
        
        all_results[f"{u:.2f}"] = {}
        
        for rep in range(N_reps):
            task_count += 1
            rep_start_time = time.time()
            
            print(f"\n  Rep {rep+1}/{N_reps} (Overall: {task_count}/{total_tasks}, {100*task_count/total_tasks:.1f}%)")
            
            # Set unique random seed for each repetition
            seed = int(u * 10000) + rep * 100000
            np.random.seed(seed)
            
            # Initialize NEW species pool for each repetition
            print("    Initializing new species pool...")
            I, g, k = InitializeSpeceiesPool(N, 
                                           lambda: uniform_distribution(u, o),
                                           f_g=lambda: np.ones(1),
                                           f_k=lambda: 1,
                                           is_diagonal_one=True, 
                                           save_path=session_name)
            
            # Create random communities
            print("    Creating communities...")
            CommunitiesLibrary = InitializeRandomCommunityPool_48(N, num_C, num_S, 
                                                                  save_path=session_name)
            
            # Initialize with small random abundances
            y = np.random.rand(N) * 0.1
            
            # Run single community simulations
            print("    Running single community simulations...")
            sc_list = {}
            for idx in range(num_C):
                y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
                y1[y1 < threshold] = 0
                sc_list[idx] = y1.tolist()
            
            # Run coalescence simulations (all pairwise combinations)
            print("    Running coalescence simulations...")
            cc_list = {}
            
            for idx in range(num_C):
                for jdx in range(idx + 1, num_C):
                    # Get steady states of individual communities
                    y1 = np.array(sc_list[idx])
                    y2 = np.array(sc_list[jdx])
                    
                    # Mix communities (equal proportions)
                    y3 = (y1 + y2) / 2
                    
                    # Run to new steady state
                    survived = y3 > threshold
                    y3 = run_lotka_volterra(y3, t, survived, I, g, k)
                    y3[y3 < threshold] = 0
                    
                    cc_list[f"{idx}_{jdx}"] = y3.tolist()
            
            # Store results for this repetition
            all_results[f"{u:.2f}"][f"rep_{rep:03d}"] = {
                "sc_list": sc_list,
                "cc_list": cc_list,
                "parameters": {
                    "seed": seed,
                    "u": u,
                    "interaction_matrix_stats": {
                        "mean": float(np.mean(I[np.triu_indices(N, k=1)])),
                        "std": float(np.std(I[np.triu_indices(N, k=1)]))
                    }
                }
            }
            
            rep_end_time = time.time()
            print(f"    Repetition completed in {rep_end_time - rep_start_time:.2f} seconds")
            
            # Save intermediate results every 20 repetitions
            if (rep + 1) % 20 == 0:
                print(f"\n  💾 Saving intermediate results (rep {rep+1})...")
                with open(output_file, 'w') as f:
                    json.dump(all_results, f, indent=2)
        
        # Save after each intensity
        print(f"\n💾 Saving results after completing u = {u:.2f}...")
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2)
    
    # Save final results
    print("\n💾 Saving final results...")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    end_time = time.time()
    print(f"\n🎉 SIMULATION COMPLETED SUCCESSFULLY!")
    print(f"⏱️  Total time: {(end_time - start_time)/60:.2f} minutes")
    print(f"📁 Data saved to: {output_file}")
    
    # Verify output and print summary statistics
    with open(output_file, 'r') as f:
        loaded_results = json.load(f)
    
    print("\n" + "="*60)
    print("FINE INTERVAL SIMULATION SUMMARY")
    print("="*60)
    
    print(f"📊 Data structure:")
    print(f"  • Intensity values: {len(loaded_results)} (from {u_list[0]:.2f} to {u_list[-1]:.2f})")
    print(f"  • Repetitions per intensity: {N_reps}")
    print(f"  • Total data points: {len(loaded_results) * N_reps}")
    
    # Sample statistics from a few intensities
    sample_intensities = [u_list[0], u_list[len(u_list)//2], u_list[-1]]
    
    for u in sample_intensities:
        u_key = f"{u:.2f}"
        if u_key in loaded_results:
            print(f"\n📈 Sample stats for u = {u:.2f}:")
            print(f"  Number of repetitions: {len(loaded_results[u_key])}")
            
            # Check one example
            first_rep = list(loaded_results[u_key].keys())[0]
            example_data = loaded_results[u_key][first_rep]
            
            print(f"  Number of single communities: {len(example_data['sc_list'])}")
            print(f"  Number of coalescence pairs: {len(example_data['cc_list'])}")
            
            # Check species richness across all reps
            richness_values = []
            for rep_key in loaded_results[u_key].keys():
                for comm_idx in loaded_results[u_key][rep_key]['sc_list'].keys():
                    sc = loaded_results[u_key][rep_key]['sc_list'][comm_idx]
                    species_present = sum(1 for x in sc if x > threshold)
                    richness_values.append(species_present)
            
            print(f"  Average species richness: {np.mean(richness_values):.2f} ± {np.std(richness_values):.2f}")
    
    print(f"\n📋 Data structure saved:")
    print(f"  • Top level: interaction strengths ({u_list[0]:.2f}, {u_list[1]:.2f}, ..., {u_list[-1]:.2f})")
    print(f"  • Second level: repetitions (rep_000 to rep_{N_reps-1:03d})")
    print(f"  • Third level: 'sc_list' (single communities), 'cc_list' (coalescence), 'parameters'")
    
    print(f"\n🎯 Ready for phase diagram generation!")
    print(f"   This data can be used with plot_phase_diagram_simulation.py")


if __name__ == "__main__":
    simulate_48_species_200reps_fine()