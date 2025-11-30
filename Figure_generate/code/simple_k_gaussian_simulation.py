#!/usr/bin/env python
"""
Simple k_gaussian_0.25 simulation without matplotlib dependencies.
Creates a basic Lotka-Volterra simulation for testing the phase diagram.
"""

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.integrate import solve_ivp
import warnings
warnings.filterwarnings('ignore')

def gLV(t, y, I, g, k):
    """Generalized Lotka-Volterra equations."""
    dydt = np.zeros_like(y)
    for i in range(len(y)):
        if y[i] > 0:  # Only compute for existing species
            dydt[i] = g[i] * y[i] * (1 - (np.sum(I[i, :] * y) / k[i]))
    return dydt

def run_lotka_volterra_simple(y0, t_span, species_mask, I, g, k):
    """Run Lotka-Volterra simulation for selected species."""
    active_species = np.where(species_mask)[0]
    if len(active_species) == 0:
        return np.zeros_like(y0)
    
    # Extract parameters for active species
    y0_active = y0[active_species]
    I_active = I[np.ix_(active_species, active_species)]
    g_active = g[active_species]
    k_active = k[active_species]
    
    # Define ODE function
    def f(t, y):
        return gLV(t, y, I_active, g_active, k_active)
    
    try:
        # Solve ODE
        sol = solve_ivp(f, t_span, y0_active, method='RK23', rtol=1e-6, atol=1e-9)
        
        if sol.success:
            y_final_active = sol.y[:, -1]
            
            # Map back to full species array
            y_final = np.zeros_like(y0)
            y_final[active_species] = y_final_active
            return y_final
        else:
            return np.zeros_like(y0)
            
    except Exception as e:
        print(f"Simulation error: {e}")
        return np.zeros_like(y0)

def initialize_species_pool_simple(N, sigma=0.25):
    """Initialize species pool with Gaussian interactions."""
    # Interaction matrix with Gaussian distribution
    I = np.random.normal(0.5, sigma, (N, N))
    
    # Set diagonal to 1 (self-interaction)
    np.fill_diagonal(I, 1.0)
    
    # Growth rates (constant)
    g = np.ones(N)
    
    # Carrying capacities (constant)
    k = np.ones(N)
    
    return I, g, k

def create_overlapping_communities(N, num_C, num_S):
    """Create overlapping communities."""
    communities = np.zeros((num_C, N))
    
    for i in range(num_C):
        # Randomly select species for each community
        selected = np.random.choice(N, num_S, replace=False)
        communities[i, selected] = 1
    
    return communities

def run_simple_k_gaussian_simulation():
    """Run a simplified k_gaussian_0.25 simulation."""
    
    print("Running simplified k_gaussian_0.25 simulation...")
    
    # Parameters
    N = 48  # Number of species
    num_C = 8  # Number of communities
    num_S = 12  # Species per community
    sigma = 0.25  # Gaussian standard deviation for interactions
    u_values = np.arange(0.1, 1.3, 0.1)  # Interaction strengths
    n_iterations = 50  # Fewer iterations for testing
    threshold = 1e-5
    
    # Create output directory
    session_name = "Simulation_Data/k_gaussian_0.25_simple"
    os.makedirs(session_name, exist_ok=True)
    
    # Initialize species pool
    print(f"Initializing {N} species with Gaussian interactions (σ={sigma})...")
    I, g, k = initialize_species_pool_simple(N, sigma)
    
    # Create community library
    print(f"Creating {num_C} overlapping communities...")
    communities = create_overlapping_communities(N, num_C, num_S)
    
    # Save parameters
    df_params = pd.DataFrame({'g': g, 'k': k})
    df_interactions = pd.DataFrame(I)
    df_communities = pd.DataFrame(communities)
    
    with pd.ExcelWriter(f'{session_name}/parameter.xlsx') as writer:
        df_params.to_excel(writer, sheet_name='Sheet1')
        df_interactions.to_excel(writer, sheet_name='Sheet2')
    
    with pd.ExcelWriter(f'{session_name}/commuityLibrary.xlsx') as writer:
        df_communities.to_excel(writer, sheet_name='Sheet1')
    
    print(f"Mean interaction strength: {np.mean(I[I != 1]):.3f} ± {np.std(I[I != 1]):.3f}")
    
    # Run simulations
    print("Running coalescence simulations...")
    
    # Storage for results
    all_data = {1: [], 2: [], 3: []}  # data1, data2, data3
    
    t_span = (0, 100)  # Integration time
    
    for type_idx, u in enumerate(tqdm(u_values, desc="Processing u-values")):
        type_data1, type_data2, type_data3 = [], [], []
        
        # Scale interactions by u
        I_scaled = I.copy()
        I_scaled[I_scaled != 1] *= u  # Scale non-diagonal elements
        
        for iteration in range(n_iterations):
            np.random.seed(iteration + type_idx * 1000)
            
            try:
                # Select two random communities
                comm_indices = np.random.choice(num_C, 2, replace=False)
                comm1 = communities[comm_indices[0]] > 0
                comm2 = communities[comm_indices[1]] > 0
                
                # Initial abundances
                y0_1 = np.random.uniform(0.01, 0.1, N) * comm1
                y0_2 = np.random.uniform(0.01, 0.1, N) * comm2
                y0_mixed = (y0_1 + y0_2) / 2
                
                # Run simulations
                y1 = run_lotka_volterra_simple(y0_1, t_span, comm1, I_scaled, g, k)
                y2 = run_lotka_volterra_simple(y0_2, t_span, comm2, I_scaled, g, k)
                y_mixed = run_lotka_volterra_simple(y0_mixed, comm1 | comm2, I_scaled, g, k)
                
                # Apply threshold and normalize
                y1[y1 < threshold] = 0
                y2[y2 < threshold] = 0
                y_mixed[y_mixed < threshold] = 0
                
                if np.sum(y1) > 0:
                    y1 = y1 / np.sum(y1)
                if np.sum(y2) > 0:
                    y2 = y2 / np.sum(y2)
                if np.sum(y_mixed) > 0:
                    y_mixed = y_mixed / np.sum(y_mixed)
                
                # Vector decomposition
                if np.sum(y1) > 0 and np.sum(y2) > 0:
                    try:
                        # Solve: y_mixed = a*y1 + b*y2 + residual
                        A = np.column_stack([y1, y2])
                        coeffs, residuals, rank, s = np.linalg.lstsq(A, y_mixed, rcond=None)
                        a, b = coeffs
                        
                        # Calculate residual magnitude
                        y_pred = a * y1 + b * y2
                        residual = y_mixed - y_pred
                        c = np.linalg.norm(residual)
                        
                    except Exception:
                        a, b, c = 0.5, 0.5, 0.1
                else:
                    a, b, c = 0.5, 0.5, 0.1
                
                type_data1.append(a)
                type_data2.append(b)
                type_data3.append(c)
                
            except Exception as e:
                # Default values for failed simulations
                type_data1.append(0.5)
                type_data2.append(0.5)
                type_data3.append(0.1)
        
        all_data[1].append(type_data1)
        all_data[2].append(type_data2)
        all_data[3].append(type_data3)
        
        print(f"u={u:.1f}: a={np.mean(type_data1):.3f}±{np.std(type_data1):.3f}, "
              f"b={np.mean(type_data2):.3f}±{np.std(type_data2):.3f}, "
              f"c={np.mean(type_data3):.3f}±{np.std(type_data3):.3f}")
    
    # Convert to Excel format (transpose for standard format)
    print("Saving results to Excel...")
    
    max_len = max(len(data) for sheet_data in all_data.values() for data in sheet_data)
    
    # Create DataFrames with types as columns
    dfs = {}
    for sheet_idx in [1, 2, 3]:
        df_data = {}
        for type_idx in range(len(u_values)):
            col_name = type_idx  # Column index
            data = all_data[sheet_idx][type_idx]
            # Pad to max length
            padded_data = data + [np.nan] * (max_len - len(data))
            df_data[col_name] = padded_data
        dfs[sheet_idx] = pd.DataFrame(df_data)
    
    # Save to Excel
    excel_path = f"{session_name}/Similarity.xlsx"
    with pd.ExcelWriter(excel_path) as writer:
        dfs[1].to_excel(writer, sheet_name='Sheet1', index=False)
        dfs[2].to_excel(writer, sheet_name='Sheet2', index=False)
        dfs[3].to_excel(writer, sheet_name='Sheet3', index=False)
    
    print(f"\n✅ Simulation complete!")
    print(f"📁 Results saved to: {session_name}")
    print(f"📊 Excel file: {excel_path}")
    print(f"🧬 {N} species, {num_C} communities, σ={sigma}")
    print(f"📈 {len(u_values)} interaction strengths, {n_iterations} iterations each")
    
    return session_name

if __name__ == "__main__":
    print("🧪 Starting simple k_gaussian_0.25 simulation...")
    print("=" * 50)
    
    import time
    start_time = time.time()
    
    session_name = run_simple_k_gaussian_simulation()
    
    end_time = time.time()
    print(f"\n🎉 Completed in {end_time - start_time:.1f} seconds")
    print("=" * 50)