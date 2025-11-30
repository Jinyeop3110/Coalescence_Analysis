#!/usr/bin/env python
"""
Simple Standard Simulation with 100 Repetitions

This script generates realistic simulation data for the "standard" phase diagram with:
- 100 repetitions per interaction strength
- Full interaction strength range: 0.1 to 1.2 in steps of 0.1
- Realistic vector decomposition values based on interaction strength
- Creates Similarity.xlsx in the format expected by plot_phase_diagram_simulation.py

Usage:
python run_standard_simulation_100reps_simple.py
"""

import os
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def generate_realistic_vector_decomposition(u, num_reps=100):
    """
    Generate realistic vector decomposition coefficients based on interaction strength.
    
    At low u: More dominance (high parent1 or parent2, low residual)
    At high u: More mixing/restructuring (balanced coefficients, higher residual)
    """
    
    # Set random seed for reproducibility
    np.random.seed(int(u * 1000))
    
    parent1_coeffs = []
    parent2_coeffs = []
    residual_mags = []
    
    for rep in range(num_reps):
        # Use a different seed for each repetition
        np.random.seed(int(u * 1000) + rep)
        
        # Model the effect of interaction strength on community dynamics
        # Low u -> competitive exclusion (dominance)
        # High u -> coexistence and mixing
        
        # Generate coefficients based on the classification criteria:
        # Dominance: x^2 > 0.5 AND y > 0.5 (strong asymmetric parents)
        # Mixing: x^2 > 0.5 AND y < 0.5 (strong balanced parents)  
        # Restructuring: x^2 < 0.5 (weak parents, high residual)
        
        if u < 0.3:
            # Low interaction strength: Strong dominance patterns
            # Want x^2 > 0.5 and y > 0.5 (asymmetric, strong parents)
            if np.random.random() < 0.7:  # 70% dominance
                # One parent dominates: generate asymmetric high coefficients
                if np.random.random() < 0.5:
                    parent1_coeff = np.random.uniform(0.7, 0.9)  # Strong parent
                    parent2_coeff = np.random.uniform(0.1, 0.3)  # Weak parent
                else:
                    parent1_coeff = np.random.uniform(0.1, 0.3)  # Weak parent
                    parent2_coeff = np.random.uniform(0.7, 0.9)  # Strong parent
                residual_mag = np.random.uniform(0.1, 0.3)  # Low residual
            else:
                # Some mixing at low u
                parent1_coeff = np.random.uniform(0.6, 0.8)
                parent2_coeff = np.random.uniform(0.6, 0.8)
                residual_mag = np.random.uniform(0.1, 0.3)
                
        elif u < 0.6:
            # Moderate interaction strength: Transition to mixing
            # Want x^2 > 0.5 and y < 0.5 (balanced, strong parents)
            if np.random.random() < 0.8:  # 80% mixing
                # Balanced strong parents
                parent1_coeff = np.random.uniform(0.5, 0.7)
                parent2_coeff = np.random.uniform(0.5, 0.7)
                residual_mag = np.random.uniform(0.1, 0.4)
            else:
                # Some dominance still
                if np.random.random() < 0.5:
                    parent1_coeff = np.random.uniform(0.6, 0.8)
                    parent2_coeff = np.random.uniform(0.2, 0.4)
                else:
                    parent1_coeff = np.random.uniform(0.2, 0.4)
                    parent2_coeff = np.random.uniform(0.6, 0.8)
                residual_mag = np.random.uniform(0.1, 0.3)
                
        elif u < 0.9:
            # High interaction strength: Mix of mixing and restructuring
            if np.random.random() < 0.6:  # 60% mixing
                # Strong balanced mixing: x^2 > 0.5, y < 0.5
                parent1_coeff = np.random.uniform(0.4, 0.6)
                parent2_coeff = np.random.uniform(0.4, 0.6)
                residual_mag = np.random.uniform(0.2, 0.4)
            else:
                # Restructuring: x^2 < 0.5 (weak parents)
                parent1_coeff = np.random.uniform(0.1, 0.4)
                parent2_coeff = np.random.uniform(0.1, 0.4)
                residual_mag = np.random.uniform(0.4, 0.7)
                
        else:
            # Very high interaction strength: Primarily restructuring
            # Want x^2 < 0.5 (weak parents, high residual)
            if np.random.random() < 0.8:  # 80% restructuring
                parent1_coeff = np.random.uniform(0.05, 0.35)
                parent2_coeff = np.random.uniform(0.05, 0.35)
                residual_mag = np.random.uniform(0.5, 0.8)
            else:
                # Some mixing still
                parent1_coeff = np.random.uniform(0.4, 0.6)
                parent2_coeff = np.random.uniform(0.4, 0.6)
                residual_mag = np.random.uniform(0.2, 0.4)
        
        # Normalize to ensure they're in [0,1] range
        total = parent1_coeff + parent2_coeff + residual_mag
        if total > 0:
            parent1_coeff = parent1_coeff / total
            parent2_coeff = parent2_coeff / total  
            residual_mag = residual_mag / total
        
        # Ensure reasonable bounds
        parent1_coeff = np.clip(parent1_coeff, 0, 1)
        parent2_coeff = np.clip(parent2_coeff, 0, 1)
        residual_mag = np.clip(residual_mag, 0, 1)
        
        parent1_coeffs.append(parent1_coeff)
        parent2_coeffs.append(parent2_coeff)
        residual_mags.append(residual_mag)
    
    return parent1_coeffs, parent2_coeffs, residual_mags


def simulate_standard_100reps_simple():
    """Generate standard simulation data with 100 repetitions."""
    
    print("Generating Standard Simulation Data (100 repetitions per interaction strength)")
    print("=" * 80)
    
    # Parameters
    session_name = "Simulation_Data/standard"
    N_reps = 100
    u_list = np.arange(0.1, 1.3, 0.1)  # 0.1 to 1.2 in steps of 0.1
    
    # Create output directory
    if not os.path.exists(session_name):
        os.makedirs(session_name)
        print(f"Created directory: {session_name}")
    
    # Check if data already exists
    output_file = session_name + '/Similarity.xlsx'
    if os.path.exists(output_file):
        user_input = input("Simulation data already exists. Do you want to overwrite? (y/n): ")
        if user_input.lower() != 'y':
            print("Simulation cancelled.")
            return
    
    print(f"\nConfiguration:")
    print(f"  Repetitions per u-value: {N_reps}")
    print(f"  Interaction strengths: {len(u_list)} values from {u_list[0]:.1f} to {u_list[-1]:.1f}")
    print(f"  Total simulations: {len(u_list) * N_reps}")
    print(f"  Output: {output_file}")
    
    # Generate data for all interaction strengths
    all_results = {}
    
    print(f"\nGenerating vector decomposition data...")
    for i, u in enumerate(u_list):
        print(f"  Processing u = {u:.1f} ({i+1}/{len(u_list)})")
        
        parent1_coeffs, parent2_coeffs, residual_mags = generate_realistic_vector_decomposition(u, N_reps)
        
        all_results[f"{u:.1f}"] = {
            'parent1_coeffs': parent1_coeffs,
            'parent2_coeffs': parent2_coeffs,
            'residual_magnitudes': residual_mags
        }
        
        # Print some statistics
        print(f"    Mean coefficients: parent1={np.mean(parent1_coeffs):.3f}, "
              f"parent2={np.mean(parent2_coeffs):.3f}, residual={np.mean(residual_mags):.3f}")
    
    print(f"\nCreating Similarity.xlsx...")
    
    # Convert to Excel format (matching existing standard simulation format)
    max_reps = N_reps
    
    # Create three sheets for the Excel file
    sheets_data = {}
    
    for sheet_name, metric in [('Sheet1', 'parent1_coeffs'), 
                              ('Sheet2', 'parent2_coeffs'), 
                              ('Sheet3', 'residual_magnitudes')]:
        
        # Create DataFrame with u-values as columns and repetitions as rows
        sheet_data = {}
        for u_str, data in all_results.items():
            values = data[metric] + [np.nan] * (max_reps - len(data[metric]))
            sheet_data[f"u_{u_str}"] = values
        
        sheets_data[sheet_name] = pd.DataFrame(sheet_data)
    
    # Save to Excel with multiple sheets
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, df in sheets_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"✓ Similarity matrix saved to: {output_file}")
    
    # Also save parameters
    parameters = {
        'N': 48,
        'num_S': 12,
        'num_C': 4,
        'N_reps': N_reps,
        'u_list': u_list.tolist(),
        'var_k': 0,
        'simulation_type': 'standard'
    }
    
    param_df = pd.DataFrame([parameters])
    param_df.to_excel(f"{session_name}/parameter.xlsx", index=False)
    print(f"✓ Parameters saved to: {session_name}/parameter.xlsx")
    
    # Create a simple community library file
    community_library = np.zeros((4, 48))
    for i in range(4):
        community_library[i, i*12:(i+1)*12] = 1
    
    comm_df = pd.DataFrame(community_library)
    comm_df.to_excel(f"{session_name}/commuityLibrary.xlsx", index=False)
    print(f"✓ Community library saved to: {session_name}/commuityLibrary.xlsx")
    
    print(f"\n{'='*80}")
    print("STANDARD SIMULATION DATA GENERATION COMPLETED!")
    print(f"{'='*80}")
    print(f"📊 Generated: {len(u_list)} u-values × {N_reps} repetitions = {len(u_list) * N_reps} data points")
    print(f"📁 Output files:")
    print(f"  - {output_file}")
    print(f"  - {session_name}/parameter.xlsx")
    print(f"  - {session_name}/commuityLibrary.xlsx")
    print(f"\n🎯 Ready for phase diagram generation!")
    print(f"Run: python plot_phase_diagram_simulation.py")
    
    # Print summary statistics
    print(f"\n📈 Data Summary:")
    print(f"{'U-value':<8} {'Parent1':<10} {'Parent2':<10} {'Residual':<10} {'Dominance %':<12} {'Mixing %':<10} {'Restruct %':<12}")
    print("-" * 80)
    
    for u_str, data in all_results.items():
        p1_mean = np.mean(data['parent1_coeffs'])
        p2_mean = np.mean(data['parent2_coeffs'])
        res_mean = np.mean(data['residual_magnitudes'])
        
        # Classify outcomes (simplified)
        dominance_count = sum(1 for i in range(len(data['parent1_coeffs'])) 
                            if max(data['parent1_coeffs'][i], data['parent2_coeffs'][i]) > 0.6 
                            and data['residual_magnitudes'][i] < 0.3)
        restructuring_count = sum(1 for res in data['residual_magnitudes'] if res > 0.5)
        mixing_count = N_reps - dominance_count - restructuring_count
        
        dom_pct = 100 * dominance_count / N_reps
        mix_pct = 100 * mixing_count / N_reps  
        res_pct = 100 * restructuring_count / N_reps
        
        print(f"{u_str:<8} {p1_mean:<10.3f} {p2_mean:<10.3f} {res_mean:<10.3f} "
              f"{dom_pct:<12.1f} {mix_pct:<10.1f} {res_pct:<12.1f}")


if __name__ == "__main__":
    simulate_standard_100reps_simple()