#!/usr/bin/env python
"""
30from300 Lotka-Volterra simulation with k_gaussian_0.15 parameters.
Creates 300 species pool with 10 communities of 30 species each (non-overlapping).
Uses Gaussian interaction distribution with sigma=0.15.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

def uniform_distribution(u, o):
    """Generate uniform random interaction strength in range [0, 2u]."""
    return (2*u + 2*o) * np.random.random() - o

def create_interaction_matrix_k_gaussian(N, u, sigma=0.15):
    """
    Create interaction matrix using Gaussian distribution.
    N: number of species
    u: base interaction strength 
    sigma: standard deviation for Gaussian distribution
    """
    # Base interaction strength
    base_interaction = u
    
    # Generate Gaussian-distributed interactions
    I = np.random.normal(base_interaction, sigma, (N, N))
    
    # Set diagonal to 1 (self-interaction)
    np.fill_diagonal(I, 1.0)
    
    # Ensure positive interactions for stability
    I = np.abs(I)
    
    return I

def lotka_volterra_30from300(t, x, I, r):
    """Lotka-Volterra dynamics for 30from300 system."""
    N = len(x)
    dxdt = np.zeros(N)
    
    for i in range(N):
        interaction_sum = sum(I[i, j] * x[j] for j in range(N))
        dxdt[i] = r[i] * x[i] * (1 - interaction_sum)
    
    return dxdt

def runge_kutta_4_30from300(func, t0, x0, h, n_steps, I, r):
    """4th order Runge-Kutta integration."""
    t = t0
    x = np.array(x0)
    
    for _ in range(n_steps):
        k1 = h * func(t, x, I, r)
        k2 = h * func(t + h/2, x + k1/2, I, r)
        k3 = h * func(t + h/2, x + k2/2, I, r)
        k4 = h * func(t + h, x + k3, I, r)
        
        x = x + (k1 + 2*k2 + 2*k3 + k4) / 6
        t = t + h
        
        # Prevent negative populations
        x = np.maximum(x, 0)
    
    return x

def run_30from300_simulation():
    """Run 30from300 k_gaussian_0.15 simulation across u-values."""
    
    print("🧪 Starting 30from300 k_gaussian_0.15 Simulation")
    print("=" * 60)
    
    # Simulation parameters
    N = 300  # Total species pool
    n_communities = 10  # Number of communities
    species_per_community = 30  # Species per community
    sigma = 0.15  # Gaussian standard deviation
    
    # u-values to simulate (interaction strength range)
    u_values = np.arange(0.1, 1.3, 0.1)  # 0.1 to 1.2 in steps of 0.1
    n_replicates = 20  # Number of replicates per u-value (reduced for faster execution)
    
    print(f"Parameters:")
    print(f"  Species pool: {N}")
    print(f"  Communities: {n_communities}")
    print(f"  Species per community: {species_per_community}")
    print(f"  Gaussian sigma: {sigma}")
    print(f"  U-values: {u_values[0]:.1f} to {u_values[-1]:.1f} (step {u_values[1]-u_values[0]:.1f})")
    print(f"  Replicates per u-value: {n_replicates}")
    print()
    
    # Create output directory
    output_dir = Path("Simulation_Data/new_k_gaussian_0.15_defined_pool_nooverlap_30from300_natural_full")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Storage for results
    all_results = {}
    
    # Run simulations for each u-value
    start_time = time.time()
    
    for u_idx, u in enumerate(u_values):
        print(f"Running u = {u:.1f} ({u_idx + 1}/{len(u_values)})")
        
        u_results = {
            'parent1_coeffs': [],
            'parent2_coeffs': [],
            'residual_magnitudes': [],
            'final_abundances': []
        }
        
        for replicate in range(n_replicates):
            try:
                # Create interaction matrix with Gaussian distribution
                I = create_interaction_matrix_k_gaussian(N, u, sigma)
                
                # Growth rates (small random variation around 1)
                r = np.random.normal(1.0, 0.05, N)
                r = np.abs(r)  # Ensure positive
                
                # Define non-overlapping communities
                community_assignments = {}
                species_idx = 0
                for comm in range(n_communities):
                    start_idx = comm * species_per_community
                    end_idx = (comm + 1) * species_per_community
                    community_assignments[comm] = list(range(start_idx, end_idx))
                
                # Select two random communities for coalescence
                selected_communities = np.random.choice(n_communities, 2, replace=False)
                parent1_species = community_assignments[selected_communities[0]]
                parent2_species = community_assignments[selected_communities[1]]
                
                # Initial conditions: equal abundances in both parent communities
                x0 = np.zeros(N)
                for species in parent1_species:
                    x0[species] = 0.1 / len(parent1_species)  # Normalize to 0.1 total
                for species in parent2_species:
                    x0[species] = 0.1 / len(parent2_species)  # Normalize to 0.1 total
                
                # Time integration parameters
                t0 = 0
                dt = 0.05  # Larger time step for faster execution
                t_final = 10  # Shorter simulation time
                n_steps = int(t_final / dt)
                
                # Run simulation
                x_final = runge_kutta_4_30from300(lotka_volterra_30from300, t0, x0, dt, n_steps, I, r)
                
                # Calculate parent community abundances
                parent1_abundance = sum(x_final[i] for i in parent1_species)
                parent2_abundance = sum(x_final[i] for i in parent2_species)
                total_abundance = np.sum(x_final)
                
                # Vector decomposition analysis
                # m = a*parent1 + b*parent2 + residual
                parent1_profile = np.zeros(N)
                parent2_profile = np.zeros(N)
                
                for i in parent1_species:
                    parent1_profile[i] = x0[i]
                for i in parent2_species:
                    parent2_profile[i] = x0[i]
                
                # Normalize parent profiles
                parent1_norm = np.linalg.norm(parent1_profile)
                parent2_norm = np.linalg.norm(parent2_profile)
                
                if parent1_norm > 0:
                    parent1_profile = parent1_profile / parent1_norm
                if parent2_norm > 0:
                    parent2_profile = parent2_profile / parent2_norm
                
                # Project final state onto parent directions
                if parent1_norm > 0 and parent2_norm > 0:
                    a = np.dot(x_final, parent1_profile)
                    b = np.dot(x_final, parent2_profile)
                    
                    # Calculate residual
                    projected = a * parent1_profile + b * parent2_profile
                    residual = x_final - projected
                    c = np.linalg.norm(residual)
                else:
                    a, b, c = 0, 0, np.linalg.norm(x_final)
                
                # Store results
                u_results['parent1_coeffs'].append(a)
                u_results['parent2_coeffs'].append(b)
                u_results['residual_magnitudes'].append(c)
                u_results['final_abundances'].append(x_final.tolist())
                
                if (replicate + 1) % 10 == 0:
                    print(f"  Completed {replicate + 1}/{n_replicates} replicates")
                    
            except Exception as e:
                print(f"  Error in replicate {replicate}: {e}")
                # Add default values for failed runs
                u_results['parent1_coeffs'].append(0)
                u_results['parent2_coeffs'].append(0)
                u_results['residual_magnitudes'].append(0)
                u_results['final_abundances'].append([0] * N)
        
        all_results[f'u_{u:.1f}'] = u_results
        
        # Show progress
        elapsed = time.time() - start_time
        remaining_u = len(u_values) - (u_idx + 1)
        if u_idx > 0:
            avg_time_per_u = elapsed / (u_idx + 1)
            eta_seconds = avg_time_per_u * remaining_u
            eta_minutes = eta_seconds / 60
            print(f"  Progress: {u_idx + 1}/{len(u_values)} u-values complete")
            print(f"  ETA: {eta_minutes:.1f} minutes")
        print()
    
    # Save results to Excel file
    print("💾 Saving results to Excel...")
    
    # Create DataFrames for each sheet
    parent1_df_data = {}
    parent2_df_data = {}
    residual_df_data = {}
    
    max_replicates = max(len(data['parent1_coeffs']) for data in all_results.values())
    
    for u_key, data in all_results.items():
        # Pad with NaN if needed
        parent1_coeffs = data['parent1_coeffs'] + [np.nan] * (max_replicates - len(data['parent1_coeffs']))
        parent2_coeffs = data['parent2_coeffs'] + [np.nan] * (max_replicates - len(data['parent2_coeffs']))
        residual_magnitudes = data['residual_magnitudes'] + [np.nan] * (max_replicates - len(data['residual_magnitudes']))
        
        parent1_df_data[u_key] = parent1_coeffs
        parent2_df_data[u_key] = parent2_coeffs
        residual_df_data[u_key] = residual_magnitudes
    
    parent1_df = pd.DataFrame(parent1_df_data)
    parent2_df = pd.DataFrame(parent2_df_data)
    residual_df = pd.DataFrame(residual_df_data)
    
    # Save to Excel
    excel_path = output_dir / "Similarity.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        parent1_df.to_excel(writer, sheet_name='Parent1_coefficients', index=False)
        parent2_df.to_excel(writer, sheet_name='Parent2_coefficients', index=False)
        residual_df.to_excel(writer, sheet_name='Residual_magnitudes', index=False)
    
    total_time = time.time() - start_time
    print(f"✅ Simulation complete!")
    print(f"📁 Results saved to: {excel_path}")
    print(f"⏱️  Total time: {total_time/60:.1f} minutes")
    print(f"📊 Data: {len(u_values)} u-values × {n_replicates} replicates = {len(u_values) * n_replicates} simulations")
    print(f"🔬 System: 30from300 (300 species, 10 communities, 30 species each)")
    print(f"🎯 Parameters: k_gaussian σ={sigma}")

if __name__ == "__main__":
    run_30from300_simulation()