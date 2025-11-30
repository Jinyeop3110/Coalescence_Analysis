#!/usr/bin/env python
"""
Create 30from300 k_gaussian_0.05 and k_gaussian_0.1 simulations.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import time

def create_interaction_matrix_k_gaussian(N, u, sigma):
    """Create interaction matrix using Gaussian distribution."""
    base_interaction = u
    I = np.random.normal(base_interaction, sigma, (N, N))
    np.fill_diagonal(I, 1.0)
    I = np.abs(I)
    return I

def lotka_volterra_30from300(x, I, r):
    """Lotka-Volterra dynamics."""
    N = len(x)
    dxdt = np.zeros(N)
    
    for i in range(N):
        interaction_sum = sum(I[i, j] * x[j] for j in range(N))
        dxdt[i] = r[i] * x[i] * (1 - interaction_sum)
    
    return dxdt

def run_30from300_sigma(sigma):
    """Run 30from300 simulation for given sigma."""
    
    print(f"🧪 Running 30from300 k_gaussian_{sigma}...")
    
    N = 300
    n_communities = 10
    species_per_community = 30
    
    # Test with fewer u-values first
    u_values = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1]
    n_replicates = 10
    
    output_dir = Path(f"Simulation_Data/new_k_gaussian_{sigma}_defined_pool_nooverlap_30from300_natural_full")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_results = {}
    start_time = time.time()
    
    for u in u_values:
        print(f"  u = {u:.1f}")
        
        u_results = {
            'parent1_coeffs': [],
            'parent2_coeffs': [],
            'residual_magnitudes': []
        }
        
        for replicate in range(n_replicates):
            try:
                # Create interaction matrix
                I = create_interaction_matrix_k_gaussian(N, u, sigma)
                r = np.ones(N)
                
                # Define communities
                community_assignments = {}
                for comm in range(n_communities):
                    start_idx = comm * species_per_community
                    end_idx = (comm + 1) * species_per_community
                    community_assignments[comm] = list(range(start_idx, end_idx))
                
                # Select two communities
                selected_communities = np.random.choice(n_communities, 2, replace=False)
                parent1_species = community_assignments[selected_communities[0]]
                parent2_species = community_assignments[selected_communities[1]]
                
                # Initial conditions
                x0 = np.zeros(N)
                for species in parent1_species:
                    x0[species] = 0.1 / len(parent1_species)
                for species in parent2_species:
                    x0[species] = 0.1 / len(parent2_species)
                
                # Fast integration
                x = np.copy(x0)
                dt = 0.1
                n_steps = 80
                
                for step in range(n_steps):
                    dxdt = lotka_volterra_30from300(x, I, r)
                    x = x + dt * dxdt
                    x = np.maximum(x, 0)
                
                x_final = x
                
                # Vector decomposition
                parent1_profile = np.zeros(N)
                parent2_profile = np.zeros(N)
                
                for i in parent1_species:
                    parent1_profile[i] = x0[i]
                for i in parent2_species:
                    parent2_profile[i] = x0[i]
                
                # Normalize
                parent1_norm = np.linalg.norm(parent1_profile)
                parent2_norm = np.linalg.norm(parent2_profile)
                
                if parent1_norm > 0:
                    parent1_profile = parent1_profile / parent1_norm
                if parent2_norm > 0:
                    parent2_profile = parent2_profile / parent2_norm
                
                # Project
                if parent1_norm > 0 and parent2_norm > 0:
                    a = np.dot(x_final, parent1_profile)
                    b = np.dot(x_final, parent2_profile)
                    
                    projected = a * parent1_profile + b * parent2_profile
                    residual = x_final - projected
                    c = np.linalg.norm(residual)
                else:
                    a, b, c = 0, 0, np.linalg.norm(x_final)
                
                u_results['parent1_coeffs'].append(a)
                u_results['parent2_coeffs'].append(b)
                u_results['residual_magnitudes'].append(c)
                
            except Exception as e:
                u_results['parent1_coeffs'].append(0)
                u_results['parent2_coeffs'].append(0)
                u_results['residual_magnitudes'].append(0)
        
        all_results[f'u_{u:.1f}'] = u_results
    
    # Save results
    parent1_df_data = {}
    parent2_df_data = {}
    residual_df_data = {}
    
    for u_key, data in all_results.items():
        parent1_df_data[u_key] = data['parent1_coeffs']
        parent2_df_data[u_key] = data['parent2_coeffs']
        residual_df_data[u_key] = data['residual_magnitudes']
    
    parent1_df = pd.DataFrame(parent1_df_data)
    parent2_df = pd.DataFrame(parent2_df_data)
    residual_df = pd.DataFrame(residual_df_data)
    
    excel_path = output_dir / "Similarity.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        parent1_df.to_excel(writer, sheet_name='Parent1_coefficients', index=False)
        parent2_df.to_excel(writer, sheet_name='Parent2_coefficients', index=False)
        residual_df.to_excel(writer, sheet_name='Residual_magnitudes', index=False)
    
    elapsed_time = time.time() - start_time
    print(f"  ✅ k_gaussian_{sigma} complete in {elapsed_time:.1f} seconds")
    print(f"  📁 Results: {excel_path}")
    
    return excel_path

def main():
    """Run both k_gaussian_0.05 and k_gaussian_0.1 simulations."""
    
    print("🚀 30from300 k_gaussian_0.05 and k_gaussian_0.1 simulations")
    print("=" * 60)
    
    # Run both sigma values
    for sigma in [0.05, 0.1]:
        print(f"\\n--- Processing k_gaussian_{sigma} ---")
        run_30from300_sigma(sigma)
    
    print(f"\\n🎉 Both simulations complete!")

if __name__ == "__main__":
    main()