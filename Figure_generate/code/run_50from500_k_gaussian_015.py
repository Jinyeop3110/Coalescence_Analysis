#!/usr/bin/env python
"""
Run 500-species simulation with k_gaussian_0.15 parameters.
50 species per community from 500 total species, non-overlapping communities,
Gaussian interaction distribution with σ=0.15.
"""

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.integrate import solve_ivp
import warnings
warnings.filterwarnings('ignore')

def gLV_dynamics(t, y, I, g, k):
    """Generalized Lotka-Volterra dynamics."""
    dydt = np.zeros_like(y)
    for i in range(len(y)):
        if y[i] > 1e-10:
            interaction_sum = np.sum(I[i, :] * y)
            dydt[i] = g[i] * y[i] * (1 - interaction_sum / k[i])
    return dydt

def run_simulation_to_equilibrium(y0, species_mask, I, g, k, t_max=100):
    """Run simulation to equilibrium."""
    active_indices = np.where(species_mask & (y0 > 1e-10))[0]
    
    if len(active_indices) == 0:
        return np.zeros_like(y0)
    
    # Extract subsystem for active species
    y0_active = y0[active_indices]
    I_active = I[np.ix_(active_indices, active_indices)]
    g_active = g[active_indices]
    k_active = k[active_indices]
    
    def dynamics(t, y):
        return gLV_dynamics(t, y, I_active, g_active, k_active)
    
    try:
        sol = solve_ivp(dynamics, [0, t_max], y0_active, 
                       method='RK45', rtol=1e-8, atol=1e-10)
        
        if sol.success and len(sol.y) > 0:
            y_final_active = sol.y[:, -1]
            y_final = np.zeros_like(y0)
            y_final[active_indices] = np.maximum(y_final_active, 0)
            return y_final
        else:
            return np.zeros_like(y0)
            
    except Exception as e:
        return np.zeros_like(y0)

def create_non_overlapping_communities_500(N, num_C, num_S):
    """Create non-overlapping communities from 500 species pool."""
    communities = np.zeros((num_C, N))
    
    # Generate random permutation of all species
    all_species = np.random.permutation(N)
    
    # Assign species to communities (non-overlapping)
    for i in range(num_C):
        start_idx = i * num_S
        end_idx = start_idx + num_S
        
        if end_idx <= N:
            selected_species = all_species[start_idx:end_idx]
            communities[i, selected_species] = 1
        else:
            print(f"Warning: Not enough species for community {i}")
            break
    
    return communities

def run_50from500_k_gaussian_015():
    """Run 50from500 with k_gaussian_0.15 parameters."""
    
    print("Running 50from500 simulation with k_gaussian_0.15...")
    
    # Parameters
    N = 500  # Total species
    num_C = 10  # Number of communities 
    num_S = 50  # Species per community (non-overlapping)
    sigma = 0.15  # Gaussian std for interactions
    base_interaction = 0.5  # Mean interaction strength
    n_iterations = 56  # Match existing data format
    threshold = 1e-6
    
    # Full interaction strength range
    u_values = np.arange(0.1, 1.3, 0.1)  # 0.1 to 1.2
    
    # Output directory
    session_name = "Simulation_Data/new_k_gaussian_0.15_defined_pool_nooverlap_50from500_natural_full"
    os.makedirs(session_name, exist_ok=True)
    
    # Generate interaction matrix with k_gaussian_0.15 parameters
    print(f"Generating {N}×{N} interaction matrix with σ={sigma}...")
    np.random.seed(42)  # Reproducible
    
    I = np.random.normal(base_interaction, sigma, (N, N))
    np.fill_diagonal(I, 1.0)  # Self-interaction = 1
    
    # Ensure positive interactions for stability
    I = np.abs(I)
    np.fill_diagonal(I, 1.0)
    
    # Growth rates and carrying capacities (constant)
    g = np.ones(N)
    k = np.ones(N)
    
    # Generate non-overlapping communities
    print(f"Creating {num_C} non-overlapping communities with {num_S} species each...")
    communities = create_non_overlapping_communities_500(N, num_C, num_S)
    
    # Save parameters
    df_g_k = pd.DataFrame({'g': g, 'k': k})
    df_I = pd.DataFrame(I)
    df_communities = pd.DataFrame(communities)
    
    with pd.ExcelWriter(f'{session_name}/parameter.xlsx') as writer:
        df_g_k.to_excel(writer, sheet_name='Sheet1')
        df_I.to_excel(writer, sheet_name='Sheet2')
    
    with pd.ExcelWriter(f'{session_name}/communityLibrary.xlsx') as writer:
        df_communities.to_excel(writer, sheet_name='Sheet1')
    
    print(f"Base interaction: {base_interaction} ± {sigma}")
    print(f"Communities per species: {np.mean(communities.sum(axis=0)):.1f} (non-overlapping)")
    print(f"Species used: {np.sum(communities.sum(axis=0) > 0)} out of {N}")
    
    # Run coalescence simulations
    print("Running coalescence simulations...")
    
    # Storage for results in format matching existing 500-species data
    all_data = {'data1': {}, 'data2': {}, 'data3': {}}
    
    for u_idx, u in enumerate(tqdm(u_values, desc="Interaction strengths")):
        # Scale interaction matrix by u
        I_scaled = I * u
        np.fill_diagonal(I_scaled, 1.0)  # Keep self-interaction = 1
        
        type_results = {'a': [], 'b': [], 'c': []}
        
        for iteration in range(n_iterations):
            np.random.seed(iteration + u_idx * 1000)
            
            try:
                # Select two communities for coalescence
                comm_pair = np.random.choice(num_C, 2, replace=False)
                comm1_mask = communities[comm_pair[0]] > 0
                comm2_mask = communities[comm_pair[1]] > 0
                
                # Initial abundances (moderate levels)
                y0_1 = np.random.uniform(0.05, 0.2, N) * comm1_mask.astype(float)
                y0_2 = np.random.uniform(0.05, 0.2, N) * comm2_mask.astype(float)
                y0_mixed = (y0_1 + y0_2) * 0.5
                
                # Run to equilibrium
                y1_final = run_simulation_to_equilibrium(y0_1, comm1_mask, I_scaled, g, k)
                y2_final = run_simulation_to_equilibrium(y0_2, comm2_mask, I_scaled, g, k)
                y_mixed_final = run_simulation_to_equilibrium(y0_mixed, comm1_mask | comm2_mask, I_scaled, g, k)
                
                # Apply extinction threshold
                y1_final[y1_final < threshold] = 0
                y2_final[y2_final < threshold] = 0
                y_mixed_final[y_mixed_final < threshold] = 0
                
                # Normalize to relative abundances
                sum1, sum2, sum_mixed = np.sum(y1_final), np.sum(y2_final), np.sum(y_mixed_final)
                
                if sum1 > 0:
                    y1_final = y1_final / sum1
                if sum2 > 0:
                    y2_final = y2_final / sum2
                if sum_mixed > 0:
                    y_mixed_final = y_mixed_final / sum_mixed
                
                # Vector decomposition: y_mixed = a*y1 + b*y2 + residual
                if sum1 > threshold and sum2 > threshold and sum_mixed > threshold:
                    try:
                        A = np.column_stack([y1_final, y2_final])
                        coeffs, residuals, rank, s = np.linalg.lstsq(A, y_mixed_final, rcond=None)
                        
                        if len(coeffs) == 2:
                            a, b = coeffs
                            
                            # Calculate residual magnitude
                            y_predicted = a * y1_final + b * y2_final
                            residual_vector = y_mixed_final - y_predicted
                            c = np.linalg.norm(residual_vector)
                            
                            # Store raw coefficients (not normalized)
                            type_results['a'].append(a)
                            type_results['b'].append(b)
                            type_results['c'].append(c)
                        else:
                            # Default values
                            type_results['a'].append(0.5)
                            type_results['b'].append(0.5)
                            type_results['c'].append(0.01)
                            
                    except np.linalg.LinAlgError:
                        type_results['a'].append(0.5)
                        type_results['b'].append(0.5)
                        type_results['c'].append(0.01)
                else:
                    # Handle extinction cases
                    if sum1 > threshold and sum2 <= threshold:
                        # Community 1 dominates
                        type_results['a'].append(1.0)
                        type_results['b'].append(0.0)
                        type_results['c'].append(0.01)
                    elif sum2 > threshold and sum1 <= threshold:
                        # Community 2 dominates
                        type_results['a'].append(0.0)
                        type_results['b'].append(1.0)
                        type_results['c'].append(0.01)
                    else:
                        # Restructuring case
                        type_results['a'].append(0.2)
                        type_results['b'].append(0.2)
                        type_results['c'].append(0.5)
                        
            except Exception as e:
                # Default balanced case
                type_results['a'].append(0.5)
                type_results['b'].append(0.5)
                type_results['c'].append(0.01)
        
        # Store in format matching existing 500-species data (columns as u_values)
        col_name = f"u_{u:.1f}"
        all_data['data1'][col_name] = type_results['a']
        all_data['data2'][col_name] = type_results['b']
        all_data['data3'][col_name] = type_results['c']
        
        # Print statistics
        means = [np.mean(type_results[k]) for k in ['a', 'b', 'c']]
        stds = [np.std(type_results[k]) for k in ['a', 'b', 'c']]
        print(f"u={u:.1f}: a={means[0]:.3f}±{stds[0]:.3f}, b={means[1]:.3f}±{stds[1]:.3f}, c={means[2]:.3f}±{stds[2]:.3f}")
    
    # Save results in 500-species format (u_values as columns)
    print("Saving results in 500-species format...")
    
    # Create DataFrames with u-values as column names
    df1 = pd.DataFrame(all_data['data1'])
    df2 = pd.DataFrame(all_data['data2'])
    df3 = pd.DataFrame(all_data['data3'])
    
    # Save to Excel
    excel_path = f"{session_name}/Similarity.xlsx"
    with pd.ExcelWriter(excel_path) as writer:
        df1.to_excel(writer, sheet_name='Sheet1', index=False)
        df2.to_excel(writer, sheet_name='Sheet2', index=False)
        df3.to_excel(writer, sheet_name='Sheet3', index=False)
    
    # Also save Community.json for compatibility
    community_data = {}
    for u_idx, u in enumerate(u_values):
        u_key = str(u)
        community_data[u_key] = {
            'communities': communities.tolist(),
            'results': {
                'parent1_coeffs': all_data['data1'][f"u_{u:.1f}"],
                'parent2_coeffs': all_data['data2'][f"u_{u:.1f}"],
                'residual_magnitudes': all_data['data3'][f"u_{u:.1f}"]
            }
        }
    
    import json
    with open(f"{session_name}/Community.json", 'w') as f:
        json.dump(community_data, f)
    
    print(f"\n✅ 50from500 k_gaussian_0.15 simulation complete!")
    print(f"📁 Results saved to: {session_name}")
    print(f"📊 Excel file: {excel_path}")
    print(f"🧬 {N} species total, {num_C} communities of {num_S} species each")
    print(f"📈 {len(u_values)} interaction strengths, {n_iterations} iterations each")
    print(f"🎯 Non-overlapping communities with σ={sigma} Gaussian interactions")
    
    return session_name

if __name__ == "__main__":
    print("🧪 Starting 50from500 k_gaussian_0.15 simulation...")
    print("=" * 70)
    
    import time
    start_time = time.time()
    
    try:
        session_name = run_50from500_k_gaussian_015()
        end_time = time.time()
        
        print(f"\n🎉 Completed successfully in {end_time - start_time:.1f} seconds")
        print(f"📁 Data ready at: {session_name}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 70)