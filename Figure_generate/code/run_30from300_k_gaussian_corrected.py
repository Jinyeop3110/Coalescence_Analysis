#!/usr/bin/env python
"""
CORRECTED 30from300 k_gaussian simulations with proper Lotka-Volterra dynamics.
Matches the dynamics used in 50from500 simulations.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import time
from scipy.integrate import solve_ivp
import warnings
warnings.filterwarnings('ignore')

def gLV_dynamics(t, y, I, g, k):
    """Generalized Lotka-Volterra dynamics with carrying capacity."""
    dydt = np.zeros_like(y)
    for i in range(len(y)):
        if y[i] > 1e-10:
            interaction_sum = np.sum(I[i, :] * y)
            dydt[i] = g[i] * y[i] * (1 - interaction_sum / k[i])
    return dydt

def run_simulation_to_equilibrium(y0, I, g, k, t_max=50):
    """Run simulation to equilibrium using scipy's ODE solver."""
    # Only simulate species with non-zero initial abundance
    active_indices = np.where(y0 > 1e-10)[0]
    
    if len(active_indices) == 0:
        return np.zeros_like(y0)
    
    # Extract subsystem
    y0_active = y0[active_indices]
    I_active = I[np.ix_(active_indices, active_indices)]
    g_active = g[active_indices]
    k_active = k[active_indices]
    
    def dynamics(t, y):
        return gLV_dynamics(t, y, I_active, g_active, k_active)
    
    try:
        sol = solve_ivp(dynamics, [0, t_max], y0_active, 
                       method='RK45', rtol=1e-8, atol=1e-10)
        
        if sol.success:
            y_final = np.zeros_like(y0)
            y_final[active_indices] = np.maximum(sol.y[:, -1], 0)
            return y_final
        else:
            return np.zeros_like(y0)
    except:
        return np.zeros_like(y0)

def create_interaction_matrix_k_gaussian(N, u, sigma, base_interaction=0.5):
    """
    Create interaction matrix using Gaussian distribution.
    Matches 50from500 approach: base interaction scaled by u.
    """
    # Generate base matrix with Gaussian distribution
    I = np.random.normal(base_interaction, sigma, (N, N))
    
    # Scale by u
    I = I * u
    
    # Set diagonal to 1 (self-interaction)
    np.fill_diagonal(I, 1.0)
    
    # Ensure positive interactions
    I = np.abs(I)
    
    return I

def run_corrected_30from300_k_gaussian(sigma):
    """Run corrected 30from300 simulation with proper dynamics."""
    
    print(f"🔧 Running CORRECTED 30from300 k_gaussian_{sigma} simulation")
    print(f"Using proper gLV dynamics with carrying capacity")
    print("=" * 60)
    
    # Parameters
    N = 300  # Total species pool
    n_communities = 10  # Number of communities
    species_per_community = 30  # Species per community
    base_interaction = 0.5  # Base interaction strength (matching 50from500)
    
    # Full u-range
    u_values = np.arange(0.1, 1.3, 0.1)  # 0.1 to 1.2
    n_replicates = 20  # Number of replicates
    
    print(f"Parameters:")
    print(f"  Species pool: {N}")
    print(f"  Communities: {n_communities} × {species_per_community} species")
    print(f"  Gaussian σ: {sigma}")
    print(f"  Base interaction: {base_interaction}")
    print(f"  U-values: {u_values[0]:.1f} to {u_values[-1]:.1f}")
    print(f"  Replicates: {n_replicates}")
    
    # Create output directory
    output_dir = Path(f"Simulation_Data/corrected_k_gaussian_{sigma}_defined_pool_nooverlap_30from300_natural_full")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate growth rates and carrying capacities
    g = np.random.uniform(0.8, 1.2, N)  # Growth rates
    k = np.ones(N)  # Carrying capacities (normalized to 1)
    
    # Define non-overlapping communities
    communities = np.zeros((n_communities, N))
    all_species = np.arange(N)
    for i in range(n_communities):
        start_idx = i * species_per_community
        end_idx = (i + 1) * species_per_community
        communities[i, all_species[start_idx:end_idx]] = 1
    
    # Storage for results
    all_results = {}
    start_time = time.time()
    
    for u_idx, u in enumerate(u_values):
        print(f"\nProcessing u = {u:.1f} ({u_idx + 1}/{len(u_values)})")
        
        u_results = {
            'parent1_coeffs': [],
            'parent2_coeffs': [],
            'residual_magnitudes': []
        }
        
        # Create interaction matrix for this u value
        I = create_interaction_matrix_k_gaussian(N, u, sigma, base_interaction)
        
        for replicate in range(n_replicates):
            try:
                # Select two random communities
                selected = np.random.choice(n_communities, 2, replace=False)
                comm1_mask = communities[selected[0]] > 0
                comm2_mask = communities[selected[1]] > 0
                
                # Initial conditions (matching 50from500 approach)
                y0 = np.zeros(N)
                y0[comm1_mask] = np.random.uniform(0.05, 0.2, np.sum(comm1_mask))
                y0[comm2_mask] = np.random.uniform(0.05, 0.2, np.sum(comm2_mask))
                
                # Mixed initial condition (average of parents)
                y0_mixed = y0 * 0.5
                
                # Run to equilibrium
                y_final = run_simulation_to_equilibrium(y0_mixed, I, g, k)
                
                # Also run parents separately for comparison
                y0_parent1 = np.zeros(N)
                y0_parent1[comm1_mask] = y0[comm1_mask] * 2  # Restore full abundance
                y_parent1 = run_simulation_to_equilibrium(y0_parent1, I, g, k)
                
                y0_parent2 = np.zeros(N)
                y0_parent2[comm2_mask] = y0[comm2_mask] * 2  # Restore full abundance
                y_parent2 = run_simulation_to_equilibrium(y0_parent2, I, g, k)
                
                # Vector decomposition analysis
                # Normalize parent profiles
                parent1_norm = np.linalg.norm(y_parent1)
                parent2_norm = np.linalg.norm(y_parent2)
                
                if parent1_norm > 0 and parent2_norm > 0:
                    parent1_profile = y_parent1 / parent1_norm
                    parent2_profile = y_parent2 / parent2_norm
                    
                    # Project final state
                    a = np.dot(y_final, parent1_profile)
                    b = np.dot(y_final, parent2_profile)
                    
                    # Calculate residual
                    projected = a * parent1_profile + b * parent2_profile
                    residual = y_final - projected
                    c = np.linalg.norm(residual)
                else:
                    a, b, c = 0, 0, np.linalg.norm(y_final)
                
                u_results['parent1_coeffs'].append(a)
                u_results['parent2_coeffs'].append(b)
                u_results['residual_magnitudes'].append(c)
                
                if (replicate + 1) % 5 == 0:
                    print(f"  Completed {replicate + 1}/{n_replicates} replicates")
                    
            except Exception as e:
                print(f"  Error in replicate {replicate}: {e}")
                u_results['parent1_coeffs'].append(0)
                u_results['parent2_coeffs'].append(0)
                u_results['residual_magnitudes'].append(0)
        
        all_results[f'u_{u:.1f}'] = u_results
    
    # Save results to Excel
    print("\n💾 Saving results...")
    
    # Create DataFrames
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
    
    # Save to Excel
    excel_path = output_dir / "Similarity.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        parent1_df.to_excel(writer, sheet_name='Parent1_coefficients', index=False)
        parent2_df.to_excel(writer, sheet_name='Parent2_coefficients', index=False)
        residual_df.to_excel(writer, sheet_name='Residual_magnitudes', index=False)
    
    elapsed_time = time.time() - start_time
    print(f"\n✅ CORRECTED simulation complete!")
    print(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
    print(f"📁 Results: {excel_path}")
    print(f"🔬 Using proper gLV dynamics: dx/dt = g*x*(1 - Σ(I*x)/k)")
    
    return excel_path

def main():
    """Run corrected simulations for all three sigma values."""
    
    print("🚀 CORRECTED 30from300 k_gaussian simulations")
    print("Fixing dynamics to match 50from500 system")
    print("=" * 70)
    
    sigma_values = [0.05, 0.1, 0.15]
    
    for sigma in sigma_values:
        print(f"\n{'='*20} k_gaussian_{sigma} {'='*20}")
        run_corrected_30from300_k_gaussian(sigma)
        print()
    
    print("\n🎉 All corrected simulations complete!")
    print("📊 Ready to generate phase diagrams with proper dynamics")

if __name__ == "__main__":
    main()