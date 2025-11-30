#!/usr/bin/env python3
"""
Generate_Fig5_4_MostAbundant_simulation_correct_intensity.py

CORRECT VERSION: Plots mean interaction strength vs species-level dominance

Purpose: Analyzes the relationship between mean interaction strength and species-level dominance
Key features:
- Uses standard_defined_pool simulation data (gamma=0)
- Plots MEAN INTERACTION STRENGTH vs species-level dominance calculated from LV equilibrium
- Processes different mean interaction strength levels: 0.2, 0.4, 0.6, 1.0 (approximating 0.3, 0.5, 0.7, 1.0)
- Uses corrected Lotka-Volterra equilibrium equations for species dominance calculation

Saving paths:
- 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_Simulation_Standard_Intensity_{intensity}.svg'
"""

from common_setup import *
import json
import pandas as pd
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def metric_VectorDecomposition_onlyPositive(u,v,m):
    u=normalize(u)
    v=normalize(v)
    m=normalize(m)
    
    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])

    e12=np.matmul(np.linalg.inv(A),np.array([np.sum(m*u), np.sum(m*v)]))
    
    x1=(e12[0])*(e12[0]>0)
    x2=(e12[1])*(e12[1]>0)
    x3=np.linalg.norm(m-(e12[0]*u)-(e12[1]*v))
    convert=np.sqrt((1-x3**2)/(x1**2+x2**2))
    
    return convert*x1, convert*x2, x3

def calculate_assymetricity(u,v,k):
    x=np.sqrt(np.array(u)**2+np.array(v)**2)
    y=np.abs(np.abs(np.arctan(np.array(u)/np.array(v)))-np.pi/4)/(np.pi/4)  
    return x,y

def calculate_assymetricity_direction(u,v,k):
    x=np.sqrt(np.array(u)**2+np.array(v)**2)
    y=np.sign(np.array(u)-np.array(v))*np.abs(np.abs(np.arctan(np.array(u)/np.array(v)))-np.pi/4)/(np.pi/4)  
    return x,y

def characterize_case(x,y):
    if (x**2>0.5)*(y>0.5):
        return 0
    if (x**2>0.5)*(y<0.5):
        return 1
    if (x**2<0.5):
        return 2

def calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2):
    """
    Calculate species-level dominance using Lotka-Volterra equilibrium.

    Correct LV equilibrium conditions:
    - Both α > 1: competitive exclusion (unstable, return 0.5)
    - α₁₂ > 1, α₂₁ < 1: species 1 always wins (dominance = 1)
    - α₁₂ < 1, α₂₁ > 1: species 2 always wins (dominance = 0)
    - Both α < 1, sum < 2: stable coexistence (use formula: 1 - α₁₂/(2 - α₁₂ - α₂₁))
    - Both α < 1, sum > 2: bistability/priority effects (return 0.5)

    Args:
        alpha_12: Effect of species 2 on species 1 (interaction strength)
        alpha_21: Effect of species 1 on species 2 (interaction strength)
        K1, K2: Carrying capacities (not used in this implementation)

    Returns:
        Relative dominance of species 1
        Values > 0.5 indicate species 1 dominance
        Values < 0.5 indicate species 2 dominance
    """

    # Case 1: Both alphas > 1 - competitive exclusion
    if alpha_12 > 1.0 and alpha_21 > 1.0:
        return 0.5

    # Case 2: alpha_12 > 1 and alpha_21 < 1 - species 2 wins
    # Species 2 strongly affects species 1, species 1 weakly affects species 2
    elif alpha_12 > 1.0 and alpha_21 < 1.0:
        return 0.0

    # Case 3: alpha_12 < 1 and alpha_21 > 1 - species 1 wins
    # Species 1 strongly affects species 2, species 2 weakly affects species 1
    elif alpha_12 < 1.0 and alpha_21 > 1.0:
        return 1.0

    # Case 4a: Both alphas < 1 AND sum < 2 - stable coexistence
    elif alpha_12 < 1.0 and alpha_21 < 1.0:
        if alpha_12 + alpha_21 < 2.0:
            # Stable coexistence - use CORRECT equilibrium formula
            # dominance = N1*/(N1*+N2*) = (1-α₁₂)/(2-α₁₂-α₂₁)
            denominator = 2 - alpha_12 - alpha_21
            if abs(denominator) < 1e-10:
                return 0.5
            return (1 - alpha_12) / denominator  # FIXED: was "1 - alpha_12 / denominator"
        else:
            # Case 4b: Both < 1 but sum > 2 - bistability (priority effects)
            # Cannot predict from pairwise LV alone
            return 0.5

    # Edge cases where alphas equal exactly 1
    else:
        return 0.5

def load_standard_simulation_data():
    """Load standard simulation data (gamma=0)."""
    sim_dir = 'Simulation_Data/standard_defined_pool'

    # Load interaction matrix
    param_file = f'{sim_dir}/parameter.xlsx'
    interaction_matrix = pd.read_excel(param_file, sheet_name='Sheet2', index_col=0)
    print(f"Interaction matrix shape: {interaction_matrix.shape}")

    # Load carrying capacities (assuming they're in parameter.xlsx)
    try:
        carrying_capacities = pd.read_excel(param_file, sheet_name='Sheet1', index_col=0)
    except:
        # If no separate sheet, assume uniform carrying capacities
        print("Warning: No carrying capacity data found, using uniform values")
        carrying_capacities = pd.DataFrame(
            np.ones((interaction_matrix.shape[0], 1)),
            columns=['K'],
            index=interaction_matrix.index
        )

    # Load community library
    comm_file = f'{sim_dir}/commuityLibrary.xlsx'
    community_library = pd.read_excel(comm_file, sheet_name='Sheet1', index_col=0)

    # Load community composition data
    comm_data_file = f'{sim_dir}/Community.json'
    with open(comm_data_file, 'r') as f:
        community_data = json.load(f)

    return interaction_matrix, carrying_capacities, community_library, community_data

def load_48species_simulation_data():
    """Load 48species_10reps_fine_WITH_MATRICES simulation data."""
    sim_dir = 'Simulation_Data/48species_10reps_fine_WITH_MATRICES'

    # Load interaction matrix
    param_file = f'{sim_dir}/parameter.xlsx'
    interaction_matrix = pd.read_excel(param_file, sheet_name='Sheet2', index_col=0)
    print(f"Interaction matrix shape: {interaction_matrix.shape}")

    # Load carrying capacities
    try:
        carrying_capacities = pd.read_excel(param_file, sheet_name='Sheet1', index_col=0)
    except:
        print("Warning: No carrying capacity data found, using uniform values")
        carrying_capacities = pd.DataFrame(
            np.ones((interaction_matrix.shape[0], 1)),
            columns=['K'],
            index=interaction_matrix.index
        )

    # Load community library
    comm_file = f'{sim_dir}/communityLibrary.xlsx'
    community_library = pd.read_excel(comm_file, sheet_name='Sheet1', index_col=0)

    # Load community composition data
    comm_data_file = f'{sim_dir}/Community_10reps_fine_WITH_MATRICES.json'
    with open(comm_data_file, 'r') as f:
        community_data = json.load(f)

    return interaction_matrix, carrying_capacities, community_library, community_data

def get_most_abundant_species_from_simulation(community_data, intensity_key='0.0'):
    """Extract most abundant species from simulation community data."""
    communities = []
    most_abundant_indices = []

    # Use the first available intensity key if the specified one doesn't exist
    if intensity_key not in community_data:
        available_keys = list(community_data.keys())
        if available_keys:
            intensity_key = available_keys[0]
            print(f"Using intensity key: {intensity_key}")
        else:
            print("No intensity keys found in community data")
            return [], []

    for comm_id in community_data[intensity_key].keys():
        # Handle both 'community_' and 'rep_' naming conventions
        if 'community_' in comm_id or 'rep_' in comm_id:
            comm_composition = community_data[intensity_key][comm_id]['sc_list']

            # Convert to numpy array and find most abundant species
            if isinstance(comm_composition, dict):
                # Handle case where sc_list is a dictionary with nested structure
                if "0" in comm_composition:
                    # sc_list contains a dictionary with "0" key - get first community
                    species_abundances = np.array(comm_composition["0"])
                else:
                    # sc_list is directly a dictionary with species indices as keys
                    species_abundances = []
                    species_indices = []
                    for species_idx, abundance in comm_composition.items():
                        species_abundances.append(abundance)
                        species_indices.append(int(species_idx))

                    species_abundances = np.array(species_abundances)
                    species_indices = np.array(species_indices)

                    # Find most abundant species
                    max_idx = np.argmax(species_abundances)
                    most_abundant_species = species_indices[max_idx]

                    communities.append(species_abundances)
                    most_abundant_indices.append(most_abundant_species)
                    continue

                # Find most abundant species for the "0" case
                most_abundant_species = np.argmax(species_abundances)

            else:
                # Handle case where sc_list is a list
                species_abundances = np.array(comm_composition)
                most_abundant_species = np.argmax(species_abundances)

            communities.append(species_abundances)
            most_abundant_indices.append(most_abundant_species)

    return communities, most_abundant_indices

def plot_mean_interaction_strength_vs_species_dominance_combined():
    """Plot mean interaction strength vs species-level dominance on single plot."""
    
    # Load standard simulation data
    interaction_matrix, carrying_capacities, community_library, community_data = load_standard_simulation_data()
    
    # Define mean interaction strength levels (using exact keys from Community.json)
    intensity_mapping = {
        '0.2': 0.2,
        '0.4': 0.4, 
        '0.6000000000000001': 0.6,
        '0.8': 0.8,
        '1.0': 1.0
    }
    
    colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#9B59B6']  # Different colors for each intensity
    
    plt.figure(figsize=(10, 8))
    
    for color_idx, (intensity_key, mean_strength) in enumerate(intensity_mapping.items()):
        print(f"\nProcessing mean interaction strength = {mean_strength}")
        
        # Get community compositions and most abundant species for this intensity
        communities, most_abundant_indices = get_most_abundant_species_from_simulation(
            community_data, intensity_key=intensity_key
        )
        
        data_species_dominance = []
        data_community_dominance = []
        
        # Generate pairwise coalescence comparisons
        num_communities = len(communities)
        print(f"Number of communities: {num_communities}")
        
        for i in range(num_communities):
            for j in range(i+1, num_communities):
                c_1 = np.array(communities[i])
                c_2 = np.array(communities[j])
                
                # Simulate coalescence outcome
                c_mix = c_1 + c_2
                c_mix = c_mix / np.sum(c_mix)  # Normalize
                
                # Apply threshold
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                if np.sum(c_1) == 0 or np.sum(c_2) == 0:
                    continue
                
                # Vector decomposition for community-level dominance
                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

                    # Skip if any value is NaN or inf
                    if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                        continue

                    # FILTER: Only consider cases where x1² + x2² > 0.66 (substantial mixing)
                    mixing_strength = u**2 + v**2
                    if mixing_strength <= 0.66:
                        continue

                    # Use arctan(u/v) normalized from 0 to 1
                    # arctan ranges from 0 to π/2, so divide by π/2 to get 0 to 1
                    community_dominance = np.arctan(u / (v + 1e-8)) / (np.pi / 2)

                    # Skip if result is NaN or inf
                    if np.isnan(community_dominance) or np.isinf(community_dominance):
                        continue
                except:
                    continue
                
                # Get most abundant species from each community
                C1 = most_abundant_indices[i]
                C2 = most_abundant_indices[j]
                
                # Check bounds
                if C1 >= interaction_matrix.shape[0] or C2 >= interaction_matrix.shape[0]:
                    continue
                
                # Get interaction coefficients
                alpha_12 = interaction_matrix.iloc[C1, C2]
                alpha_21 = interaction_matrix.iloc[C2, C1]
                
                # Get carrying capacities
                if carrying_capacities.shape[1] > 0:
                    K1 = carrying_capacities.iloc[C1, 0]
                    K2 = carrying_capacities.iloc[C2, 0]
                else:
                    K1 = K2 = 1.0
                
                # Calculate species-level dominance using LV equilibrium
                species_dominance_raw = calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2)

                # Apply arctan normalization to species dominance
                # Convert from proportion (0-1) to arctan normalized form
                # If raw dominance = p, then ratio = p/(1-p), then arctan(ratio)/(π/2)
                ratio = species_dominance_raw / (1 - species_dominance_raw + 1e-8)
                species_dominance = np.arctan(ratio) / (np.pi / 2)

                data_species_dominance.append(species_dominance)
                data_community_dominance.append(community_dominance)
        
        if len(data_species_dominance) == 0:
            print(f"Warning: No valid data points for intensity {mean_strength}")
            continue
        
        # Convert to arrays
        x = np.array(data_species_dominance)
        y = np.array(data_community_dominance)

        print(f'  Collected {len(x)} coalescence events after filtering (u²+v²>0.66)')

        # Duplicate data points (as in experimental version)
        x = np.concatenate((x, 1-x))
        y = np.concatenate((y, 1-y))
        
        # Create scatter plot with different colors for each mean interaction strength
        plt.scatter(x, y, color=colors[color_idx], s=20, alpha=0.6, 
                   label=f'Mean I = {mean_strength}')
        
        # Calculate and plot linear regression
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Add regression line
        x_line = np.linspace(0, 1, 100)
        y_line = slope * x_line + intercept
        plt.plot(x_line, y_line, color=colors[color_idx], linestyle='--', linewidth=1, alpha=0.8)
        
        print(f'Mean interaction strength {mean_strength}: R² = {r_squared:.3f}, Data points = {len(x)}')
    
    # Set plot properties
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.xlabel('Species-level LV Equilibrium Dominance')
    plt.ylabel('Community-level Coalescence Dominance')
    plt.title('Standard Simulation (γ=0): Mean Interaction Strength vs Dominance')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add diagonal reference line
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5, linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity_Combined.svg', 
                bbox_inches='tight')
    plt.close()
    
    print("\nCombined plot complete!")

def plot_48species_mean_interaction_strength_vs_species_dominance_subplots():
    """Plot mean interaction strength vs species-level dominance for 48species_10reps_fine_WITH_MATRICES data as subplots."""

    # Load 48species simulation data
    # Note: interaction matrices are embedded in JSON per replicate, not from external file
    _, _, _, community_data = load_48species_simulation_data()

    # Define mean interaction strength levels (using exact keys from Community_10reps_fine_WITH_MATRICES.json)
    # Keys are formatted as '0.20', '0.40', etc.
    intensity_mapping = {
        '0.20': 0.2,
        '0.40': 0.4,
        '0.60': 0.6,
        '0.80': 0.8,
        '1.00': 1.0
    }

    colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#9B59B6']  # Different colors for each intensity

    # Create subplots: 2 rows x 3 columns (5 plots + 1 empty)
    fig, axes = plt.subplots(2, 3, figsize=(9, 6))
    fig.suptitle('48species 10reps WITH_MATRICES', fontsize=10, y=0.995)

    # Flatten axes for easier indexing
    axes_flat = axes.flatten()

    for plot_idx, (intensity_key, mean_strength) in enumerate(intensity_mapping.items()):
        print(f"\nProcessing mean interaction strength = {mean_strength}")

        ax = axes_flat[plot_idx]

        # Get all replicates for this intensity
        intensity_data = community_data[intensity_key]

        data_species_dominance = []
        data_community_dominance = []

        # Process each replicate
        for rep_key in intensity_data.keys():
            rep_data = intensity_data[rep_key]

            # Get rep-specific interaction matrix from JSON parameters
            rep_interaction_matrix = np.array(rep_data['parameters']['interaction_matrix'])

            # Get communities and most abundant species for this replicate
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            communities = []
            most_abundant_indices = []

            for comm_key in sorted(sc_list.keys(), key=int):
                community = np.array(sc_list[comm_key])
                communities.append(community)
                most_abundant_idx = np.argmax(community)
                most_abundant_indices.append(most_abundant_idx)

            num_communities = len(communities)

            # Generate pairwise coalescence comparisons
            for i in range(num_communities):
                for j in range(i+1, num_communities):
                    # Get coalescence key
                    coal_key = f"{i}_{j}"
                    if coal_key not in cc_list:
                        continue

                    # Use ACTUAL coalescence outcome from simulation
                    c_mix = np.array(cc_list[coal_key])
                    c_1 = np.array(communities[i])
                    c_2 = np.array(communities[j])

                    # Normalize all for consistent comparison
                    c_mix = c_mix / (np.sum(c_mix) + 1e-8)
                    c_1 = c_1 / (np.sum(c_1) + 1e-8)
                    c_2 = c_2 / (np.sum(c_2) + 1e-8)

                    # Apply threshold
                    c_1_thresh = c_1 * (c_1 > 1e-4)
                    c_2_thresh = c_2 * (c_2 > 1e-4)

                    if np.sum(c_1_thresh) == 0 or np.sum(c_2_thresh) == 0:
                        continue

                    # Vector decomposition for community-level dominance
                    try:
                        u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

                        # Skip if any value is NaN or inf
                        if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                            continue

                        # FILTER: Only consider cases where x1² + x2² > 0.66 (substantial mixing)
                        mixing_strength = u**2 + v**2
                        if mixing_strength <= 0.66:
                            continue

                        # Use arctan(u/v) normalized from 0 to 1
                        # arctan ranges from 0 to π/2, so divide by π/2 to get 0 to 1
                        community_dominance = np.arctan(u / (v + 1e-8)) / (np.pi / 2)

                        # Skip if result is NaN or inf
                        if np.isnan(community_dominance) or np.isinf(community_dominance):
                            continue
                    except:
                        continue

                    # Get most abundant species from each community
                    C1 = most_abundant_indices[i]
                    C2 = most_abundant_indices[j]

                    # Check bounds
                    if C1 >= rep_interaction_matrix.shape[0] or C2 >= rep_interaction_matrix.shape[0]:
                        continue

                    # Get interaction coefficients from CORRECT matrix (rep-specific from JSON)
                    alpha_12 = rep_interaction_matrix[C1, C2]
                    alpha_21 = rep_interaction_matrix[C2, C1]

                    # Get carrying capacities (all 1.0 in this dataset)
                    K1 = K2 = 1.0

                    # Calculate species-level dominance using LV equilibrium
                    species_dominance_raw = calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2)

                    # Apply arctan normalization to species dominance
                    # Convert from proportion (0-1) to arctan normalized form
                    # If raw dominance = p, then ratio = p/(1-p), then arctan(ratio)/(π/2)
                    ratio = species_dominance_raw / (1 - species_dominance_raw + 1e-8)
                    species_dominance = np.arctan(ratio) / (np.pi / 2)

                    data_species_dominance.append(species_dominance)
                    data_community_dominance.append(community_dominance)

        print(f"Number of data points collected: {len(data_species_dominance)}")

        if len(data_species_dominance) == 0:
            print(f"Warning: No valid data points for intensity {mean_strength}")
            continue

        # Convert to arrays
        x = np.array(data_species_dominance)
        y = np.array(data_community_dominance)

        print(f'  Collected {len(x)} coalescence events after filtering (u²+v²>0.66)')

        # Duplicate data points (as in experimental version)
        x = np.concatenate((x, 1-x))
        y = np.concatenate((y, 1-y))

        # Create scatter plot
        ax.scatter(x, y, color=colors[plot_idx], s=10, alpha=0.5)

        # Calculate and plot linear regression
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        # Add regression line
        x_line = np.linspace(0, 1, 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color=colors[plot_idx], linestyle='--', linewidth=1.5, alpha=0.8)

        # Set subplot properties
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel('Species LV Dominance', fontsize=8)
        ax.set_ylabel('Community Dominance', fontsize=8)
        ax.set_title(f'Mean I = {mean_strength} (R² = {r_squared:.3f})', fontsize=8)
        ax.grid(True, alpha=0.3, linewidth=0.5)
        ax.tick_params(labelsize=7)

        # Add diagonal reference line
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=0.5)

        print(f'Mean interaction strength {mean_strength}: R² = {r_squared:.3f}, Data points = {len(x)}')

    # Hide the last subplot (6th position) since we only have 5 plots
    axes_flat[5].set_visible(False)

    plt.tight_layout()
    plt.savefig('Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_48species_10reps_WITH_MATRICES_Subplots.svg',
                bbox_inches='tight', dpi=300)
    plt.close()

    print("\n48species WITH_MATRICES subplots complete!")

def plot_mean_interaction_strength_vs_species_dominance_subplots(k_gamma_dir='standard_defined_pool', k_value_label='γ=0'):
    """Plot mean interaction strength vs species-level dominance as separate subplots."""
    
    # Load simulation data
    sim_dir = f'Simulation_Data/{k_gamma_dir}'
    param_file = f'{sim_dir}/parameter.xlsx'
    interaction_matrix = pd.read_excel(param_file, sheet_name='Sheet2', index_col=0)
    print(f"Interaction matrix shape: {interaction_matrix.shape}")
    
    try:
        carrying_capacities = pd.read_excel(param_file, sheet_name='Sheet1', index_col=0)
    except:
        print("Warning: No carrying capacity data found, using uniform values")
        carrying_capacities = pd.DataFrame(
            np.ones((interaction_matrix.shape[0], 1)), 
            columns=['K'],
            index=interaction_matrix.index
        )
    
    comm_data_file = f'{sim_dir}/Community.json'
    with open(comm_data_file, 'r') as f:
        community_data = json.load(f)
    
    # Define mean interaction strength levels based on directory type
    if 'standard' in k_gamma_dir:
        # Standard directory has specific intensity keys
        intensity_mapping = {
            '0.2': 0.2,
            '0.4': 0.4, 
            '0.6000000000000001': 0.6,
            '0.8': 0.8,
            '1.0': 1.0
        }
    elif 'k_gamma_0.5' in k_gamma_dir:
        # K=0.5 directory 
        intensity_mapping = {
            '0.2': 0.2,
            '0.4': 0.4, 
            '0.6000000000000001': 0.6,
            '0.8': 0.8,
            '1.0': 1.0
        }
    elif 'k_gamma_1' in k_gamma_dir:
        # K=1.0 directory
        intensity_mapping = {
            '0.2': 0.2,
            '0.4': 0.4, 
            '0.6000000000000001': 0.6,
            '0.8': 0.8,
            '1.0': 1.0
        }
    elif 'new_k_gamma_0.2' in k_gamma_dir:
        # K=0.2 directory - use closest available keys
        available_keys = list(community_data.keys())
        available_keys.sort(key=float)  # Sort by numeric value
        print(f"Available intensity keys for K=0.2: {available_keys[:10]}")
        
        # Find keys closest to our target values: 0.2, 0.4, 0.6, 0.8, 1.0
        targets = [0.2, 0.4, 0.6, 0.8, 1.0]
        intensity_mapping = {}
        
        for target in targets:
            closest_key = min(available_keys, key=lambda x: abs(float(x) - target))
            intensity_mapping[closest_key] = target
    elif 'new_k_gamma_0.1' in k_gamma_dir:
        # K=0.1 directory - use closest available keys  
        available_keys = list(community_data.keys())
        available_keys.sort(key=float)  # Sort by numeric value
        print(f"Available intensity keys for K=0.1: {available_keys[:10]}")
        
        # Find keys closest to our target values: 0.2, 0.4, 0.6, 0.8, 1.0
        targets = [0.2, 0.4, 0.6, 0.8, 1.0]
        intensity_mapping = {}
        
        for target in targets:
            closest_key = min(available_keys, key=lambda x: abs(float(x) - target))
            intensity_mapping[closest_key] = target
    else:
        # Default mapping for other directories
        intensity_mapping = {
            '0.2': 0.2,
            '0.4': 0.4, 
            '0.6000000000000001': 0.6,
            '0.8': 0.8,
            '1.0': 1.0
        }
    
    # Create subplots: 2x3 grid (2 rows, 3 columns, with 5 plots)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f'Standard Simulation ({k_value_label}): Mean Interaction Strength vs Species Dominance', fontsize=16)
    
    # Flatten axes for easier indexing
    axes_flat = axes.flatten()
    
    colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#9B59B6'] * 2  # Extend colors to handle more plots
    
    for plot_idx, (intensity_key, mean_strength) in enumerate(intensity_mapping.items()):
        print(f"\nProcessing subplot {plot_idx+1}: mean interaction strength = {mean_strength}")
        
        ax = axes_flat[plot_idx]
        
        # Get community compositions and most abundant species for this intensity
        communities, most_abundant_indices = get_most_abundant_species_from_simulation(
            community_data, intensity_key=intensity_key
        )
        
        data_species_dominance = []
        data_community_dominance = []
        
        # Generate pairwise coalescence comparisons
        num_communities = len(communities)
        
        for i in range(num_communities):
            for j in range(i+1, num_communities):
                c_1 = np.array(communities[i])
                c_2 = np.array(communities[j])
                
                # Simulate coalescence outcome
                c_mix = c_1 + c_2
                c_mix = c_mix / np.sum(c_mix)
                
                # Apply threshold
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                if np.sum(c_1) == 0 or np.sum(c_2) == 0:
                    continue
                
                # Vector decomposition for community-level dominance
                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

                    # Skip if any value is NaN or inf
                    if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                        continue

                    # FILTER: Only consider cases where x1² + x2² > 0.66 (substantial mixing)
                    mixing_strength = u**2 + v**2
                    if mixing_strength <= 0.66:
                        continue

                    # Use arctan(u/v) normalized from 0 to 1
                    # arctan ranges from 0 to π/2, so divide by π/2 to get 0 to 1
                    community_dominance = np.arctan(u / (v + 1e-8)) / (np.pi / 2)

                    # Skip if result is NaN or inf
                    if np.isnan(community_dominance) or np.isinf(community_dominance):
                        continue
                except:
                    continue
                
                # Get most abundant species from each community
                C1 = most_abundant_indices[i]
                C2 = most_abundant_indices[j]
                
                # Check bounds
                if C1 >= interaction_matrix.shape[0] or C2 >= interaction_matrix.shape[0]:
                    continue
                
                # Get interaction coefficients
                alpha_12 = interaction_matrix.iloc[C1, C2]
                alpha_21 = interaction_matrix.iloc[C2, C1]
                
                # Get carrying capacities
                if carrying_capacities.shape[1] > 0:
                    K1 = carrying_capacities.iloc[C1, 0]
                    K2 = carrying_capacities.iloc[C2, 0]
                else:
                    K1 = K2 = 1.0
                
                # Calculate species-level dominance using LV equilibrium
                species_dominance_raw = calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2)

                # Apply arctan normalization to species dominance
                # Convert from proportion (0-1) to arctan normalized form
                # If raw dominance = p, then ratio = p/(1-p), then arctan(ratio)/(π/2)
                ratio = species_dominance_raw / (1 - species_dominance_raw + 1e-8)
                species_dominance = np.arctan(ratio) / (np.pi / 2)

                data_species_dominance.append(species_dominance)
                data_community_dominance.append(community_dominance)
        
        if len(data_species_dominance) == 0:
            print(f"Warning: No valid data points for intensity {mean_strength}")
            continue
        
        # Convert to arrays
        x = np.array(data_species_dominance)
        y = np.array(data_community_dominance)
        
        # Duplicate data points
        x = np.concatenate((x, 1-x))
        y = np.concatenate((y, 1-y))
        
        # Create scatter plot
        ax.scatter(x, y, color=colors[plot_idx], s=15, alpha=0.6)
        
        # Calculate and plot linear regression
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Add regression line
        x_line = np.linspace(0, 1, 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color=colors[plot_idx], linestyle='--', linewidth=1.5, alpha=0.8)
        
        # Set subplot properties
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel('Species-level LV Dominance')
        ax.set_ylabel('Community-level Dominance')
        ax.set_title(f'Mean I = {mean_strength}\nR² = {r_squared:.3f}')
        ax.grid(True, alpha=0.3)
        
        # Add diagonal reference line
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=0.5)
        
        print(f'Mean interaction strength {mean_strength}: R² = {r_squared:.3f}, Data points = {len(x)}')
    
    # Hide the last subplot (6th position) since we only have 5 plots
    axes_flat[5].set_visible(False)
    
    plt.tight_layout()
    
    # Save with appropriate filename
    k_label = k_value_label.replace('=', '').replace('.', '_')
    plt.savefig(f'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity_Subplots_{k_label}.svg', 
                bbox_inches='tight')
    plt.close()
    
    print(f"\nSubplot analysis complete for {k_value_label}!")

def main():
    """Main function to run corrected simulation analysis."""
    # Create output directories
    if not os.path.exists('Figure/TopDownAnaylsis'):
        os.makedirs('Figure/TopDownAnaylsis')
    if not os.path.exists('Figure'):
        os.makedirs('Figure')

    print("=== 48species_10reps_fine_WITH_MATRICES: Mean Interaction Strength vs Species-level Dominance ===")
    print("Processing mean interaction strengths: 0.2, 0.4, 0.6, 0.8, 1.0")

    # Plot: Subplots for 48species_10reps_fine_WITH_MATRICES
    print("\nCreating subplots for 48species_10reps_fine_WITH_MATRICES simulation...")
    plot_48species_mean_interaction_strength_vs_species_dominance_subplots()

    print("\n=== Analysis complete! ===")
    print("Generated file:")
    print("- Fig_MostAbundant_Correlation_48species_10reps_WITH_MATRICES_Subplots.svg")

if __name__ == "__main__":
    main()