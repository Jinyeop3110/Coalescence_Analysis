#!/usr/bin/env python
"""
Run Lotka-Volterra simulation with k_gaussian_0.25 parameters.
This creates a simulation similar to the existing k_gaussian_0.25 data but new.
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from InitializeSpeciesPool import InitializeSpeciesPool
from LV import run_lotka_volterra
from VariousMetrics import *

def gaussian_distribution(u, sigma=0.25):
    """Generate Gaussian random interaction strength with mean u and std sigma."""
    return np.random.normal(u, sigma)

def run_k_gaussian_025_simulation():
    """Run k_gaussian_0.25 simulation similar to existing data."""
    
    print("Running k_gaussian_0.25 Lotka-Volterra simulation...")
    
    # Parameters matching k_gaussian_0.25
    N = 48  # Number of species
    num_C = 8  # Number of communities 
    num_S = 12  # Species per community (overlapping)
    threshold = 1e-5  # Extinction threshold
    u_values = np.arange(0.1, 1.3, 0.1)  # Interaction strengths 0.1 to 1.2
    n_iterations = 100  # Number of coalescence events per u-value
    
    session_name = "Simulation_Data/k_gaussian_0.25_new"
    os.makedirs(session_name, exist_ok=True)
    
    # Initialize species pool with Gaussian interaction distribution
    print(f"Initializing species pool with N={N} species...")
    
    # Create interaction function with Gaussian distribution (sigma = 0.25)
    f_interaction = lambda: gaussian_distribution(0.5, 0.25)  # Mean interaction strength
    
    # Initialize with constant growth rates and carrying capacities
    I, g, k = InitializeSpeciesPool(N, f_interaction, 
                                    f_g=lambda: np.ones(1),  # Constant growth rate = 1
                                    f_k=lambda: np.ones(1),  # Constant carrying capacity = 1
                                    is_diagonal_one=True,    # Self-interaction = 1
                                    save_path=session_name)
    
    print(f"Interaction matrix shape: {I.shape}")
    print(f"Mean interaction strength: {np.mean(I[I != 1]):.3f} ± {np.std(I[I != 1]):.3f}")
    
    # Create community library (overlapping communities for standard simulation)
    print(f"Creating {num_C} communities with {num_S} species each (overlapping)...")
    CommunitiesLibrary = np.zeros([num_C, N])
    
    # Create overlapping communities
    species_per_community = num_S
    for i in range(num_C):
        # Select species for this community (with overlap)
        available_species = list(range(N))
        selected_species = np.random.choice(available_species, species_per_community, replace=False)
        CommunitiesLibrary[i, selected_species] = 1
    
    # Save community library
    df_communities = pd.DataFrame(CommunitiesLibrary)
    with pd.ExcelWriter(f'{session_name}/commuityLibrary.xlsx') as writer:
        df_communities.to_excel(writer, sheet_name='Sheet1')
    
    print(f"Community overlap: {np.mean(CommunitiesLibrary.sum(axis=0)):.2f} communities per species")
    
    # Run simulations for different interaction strengths
    print(f"Running simulations for {len(u_values)} interaction strength values...")
    
    # Storage for results
    all_similarities = {
        'data1': [],  # Parent 1 coefficients (a)
        'data2': [],  # Parent 2 coefficients (b) 
        'data3': []   # Residual magnitudes (c)
    }
    
    # Integration time span
    t_span = (0, 100)  # Simulate for 100 time units
    
    for u_idx, u in enumerate(tqdm(u_values, desc="Interaction strengths")):
        print(f"\nProcessing u={u:.1f}...")
        
        type_data1, type_data2, type_data3 = [], [], []
        
        for iteration in tqdm(range(n_iterations), desc=f"u={u:.1f} iterations", leave=False):
            # Set random seed for reproducibility
            np.random.seed(iteration + u_idx * 1000)
            
            try:
                # Select two random communities for coalescence
                community_indices = np.random.choice(num_C, 2, replace=False)
                comm1_idx, comm2_idx = community_indices
                
                # Get community compositions
                comm1 = CommunitiesLibrary[comm1_idx] > 0
                comm2 = CommunitiesLibrary[comm2_idx] > 0
                
                # Initial abundances (small random values)
                y0_1 = np.random.uniform(0.01, 0.1, N) * comm1
                y0_2 = np.random.uniform(0.01, 0.1, N) * comm2
                y0_mixed = (y0_1 + y0_2) / 2  # Mixed community
                
                # Run Lotka-Volterra simulations to equilibrium
                y_final_1 = run_lotka_volterra(y0_1, t_span, comm1, I, g, k)
                y_final_2 = run_lotka_volterra(y0_2, t_span, comm2, I, g, k)
                y_final_mixed = run_lotka_volterra(y0_mixed, comm1 | comm2, I, g, k)
                
                # Apply extinction threshold
                y_final_1[y_final_1 < threshold] = 0
                y_final_2[y_final_2 < threshold] = 0
                y_final_mixed[y_final_mixed < threshold] = 0
                
                # Normalize to relative abundances
                if np.sum(y_final_1) > 0:
                    y_final_1 = y_final_1 / np.sum(y_final_1)
                if np.sum(y_final_2) > 0:
                    y_final_2 = y_final_2 / np.sum(y_final_2)
                if np.sum(y_final_mixed) > 0:
                    y_final_mixed = y_final_mixed / np.sum(y_final_mixed)
                
                # Vector decomposition: y_mixed = a*y1 + b*y2 + c*residual
                # Solve least squares: min ||[y1 y2] * [a; b] - y_mixed||^2
                A = np.column_stack([y_final_1, y_final_2])
                
                # Handle edge cases
                if np.sum(y_final_1) == 0 or np.sum(y_final_2) == 0:
                    a, b, residual_norm = 0, 0, 1
                else:
                    try:
                        # Solve least squares
                        coeffs, residuals, rank, s = np.linalg.lstsq(A, y_final_mixed, rcond=None)
                        a, b = coeffs if len(coeffs) == 2 else [0, 0]
                        
                        # Calculate residual
                        y_predicted = a * y_final_1 + b * y_final_2
                        residual = y_final_mixed - y_predicted
                        residual_norm = np.linalg.norm(residual)
                        
                    except np.linalg.LinAlgError:
                        a, b, residual_norm = 0, 0, 1
                
                # Store results
                type_data1.append(a)
                type_data2.append(b)
                type_data3.append(residual_norm)
                
            except Exception as e:
                print(f"Error in iteration {iteration}: {e}")
                # Store default values for failed simulations
                type_data1.append(0)
                type_data2.append(0)
                type_data3.append(1)
        
        # Add to overall results
        all_similarities['data1'].append(type_data1)
        all_similarities['data2'].append(type_data2)
        all_similarities['data3'].append(type_data3)
        
        # Print statistics
        if type_data1:
            print(f"  Results - a: {np.mean(type_data1):.3f}±{np.std(type_data1):.3f}, "
                  f"b: {np.mean(type_data2):.3f}±{np.std(type_data2):.3f}, "
                  f"c: {np.mean(type_data3):.3f}±{np.std(type_data3):.3f}")
    
    # Convert results to DataFrame format (transpose for Excel compatibility)
    print("Converting results to Excel format...")
    
    # Create DataFrames with u-values as columns
    max_length = max(len(data) for data in all_similarities['data1'])
    
    # Pad shorter lists with NaN
    df_data1 = {}
    df_data2 = {}
    df_data3 = {}
    
    for i, u in enumerate(u_values):
        col_name = f"Type_{i}"  # Standard format for simulation data
        
        data1_padded = all_similarities['data1'][i] + [np.nan] * (max_length - len(all_similarities['data1'][i]))
        data2_padded = all_similarities['data2'][i] + [np.nan] * (max_length - len(all_similarities['data2'][i]))
        data3_padded = all_similarities['data3'][i] + [np.nan] * (max_length - len(all_similarities['data3'][i]))
        
        df_data1[col_name] = data1_padded
        df_data2[col_name] = data2_padded
        df_data3[col_name] = data3_padded
    
    # Create DataFrames
    df1 = pd.DataFrame(df_data1)
    df2 = pd.DataFrame(df_data2)
    df3 = pd.DataFrame(df_data3)
    
    # Save to Excel file
    excel_path = f"{session_name}/Similarity.xlsx"
    with pd.ExcelWriter(excel_path) as writer:
        df1.to_excel(writer, sheet_name='Sheet1', index=True)
        df2.to_excel(writer, sheet_name='Sheet2', index=True)
        df3.to_excel(writer, sheet_name='Sheet3', index=True)
    
    print(f"\n✅ Simulation complete!")
    print(f"   📁 Results saved to: {session_name}/")
    print(f"   📊 Excel file: {excel_path}")
    print(f"   🧬 Species pool: {N} species, {num_C} communities")
    print(f"   📈 Interaction strengths: {len(u_values)} values from {u_values[0]:.1f} to {u_values[-1]:.1f}")
    print(f"   🔁 Iterations per u-value: {n_iterations}")
    print(f"   📋 Total simulations: {len(u_values) * n_iterations}")
    
    return session_name

if __name__ == "__main__":
    print("🧪 Starting k_gaussian_0.25 Lotka-Volterra simulation...")
    print("=" * 60)
    
    start_time = time.time()
    session_name = run_k_gaussian_025_simulation()
    end_time = time.time()
    
    print(f"\n🎉 Simulation completed in {end_time - start_time:.2f} seconds")
    print(f"📁 Data saved to: {session_name}")
    print("=" * 60)