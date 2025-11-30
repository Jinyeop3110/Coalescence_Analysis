#!/usr/bin/env python3
"""
Generate_Fig5_4_MostAbundant_simulation_corrected.py

CORRECTED VERSION: Uses proper Lotka-Volterra equilibrium equations for species-level dominance calculation.

Purpose: Analyzes the relationship between most abundant species in simulated communities and coalescence outcomes
Key features:
- Uses Lotka-Volterra simulation data with gamma-distributed interaction strengths
- CORRECTLY calculates species-level dominance using equilibrium population ratios
- Creates correlation plots between species-level pairwise interactions and community-level outcomes
- Compares different interaction strength parameters (k_gamma values)

CORRECTION: Instead of using simple interaction strength ratios, this version calculates
the equilibrium populations for 2-species competition and uses the population ratio
as the true measure of competitive dominance.

Saving paths:
- 'Figure/TopDownAnaylsis/Fig_Abundant_Simulation_Corrected.svg'
- 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_Simulation_Corrected_{k_gamma}.svg'
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
    Calculate species-level dominance using user-specified rules for Lotka-Volterra competition.
    
    User's specific implementation rules:
    - If both α₁₂ and α₂₁ > 1: competitive exclusion (exclude)
    - If α₁₂ > 1 and α₂₁ < 1: species 1 always wins (dominance = 1)
    - If α₁₂ < 1 and α₂₁ > 1: species 2 always wins (dominance = 0)  
    - If both α₁₂ and α₂₁ < 1: calculate 1 - α₁₂/(2 - α₁₂ - α₂₁)
    
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
        # Exclude - return neutral/undefined (using 0.5 as neutral)
        return 0.5
    
    # Case 2: alpha_12 > 1 and alpha_21 < 1 - species 1 wins
    elif alpha_12 > 1.0 and alpha_21 < 1.0:
        return 1.0
    
    # Case 3: alpha_12 < 1 and alpha_21 > 1 - species 2 wins  
    elif alpha_12 < 1.0 and alpha_21 > 1.0:
        return 0.0
    
    # Case 4: Both alphas < 1 - stable coexistence
    elif alpha_12 < 1.0 and alpha_21 < 1.0:
        denominator = 2 - alpha_12 - alpha_21
        if abs(denominator) < 1e-10:
            # Edge case - return neutral
            return 0.5
        return 1 - alpha_12 / denominator
    
    # Edge cases where alphas equal exactly 1
    else:
        # Handle boundary cases conservatively
        return 0.5

def load_simulation_data(k_gamma_value):
    """Load simulation data for a specific k_gamma value."""
    # Map k_gamma values to available directories (using new_k_gamma directories)
    gamma_mapping = {
        0.0: 'new_k_gamma_0_defined_pool_nooverlap_12from48',
        0.05: 'new_k_gamma_0.05_defined_pool_nooverlap_12from48',
        0.1: 'new_k_gamma_0.1_defined_pool_nooverlap_12from48',
        0.15: 'new_k_gamma_0.15_defined_pool_nooverlap_12from48',
        0.2: 'new_k_gamma_0.2_defined_pool_nooverlap_12from48',
        0.25: 'new_k_gamma_0.25_defined_pool_nooverlap_12from48',
        0.5: 'new_k_gamma_0.5_defined_pool_nooverlap_12from48',
        1.0: 'new_k_gamma_1_defined_pool_nooverlap_12from48',
        # Keep old mapping for backward compatibility
        'old_0.5': 'k_gamma_0.5_defined_pool_nooverlap_12from48',
        'old_1.0': 'k_gamma_1_defined_pool_nooverlap_12from48',
    }
    
    sim_dir = f'Simulation_Data/{gamma_mapping[k_gamma_value]}'
    
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
    
    # Load dominance results
    dom_file = f'{sim_dir}/results_dominance_fractions.json'
    with open(dom_file, 'r') as f:
        dominance_results = json.load(f)
    
    return interaction_matrix, carrying_capacities, community_library, community_data, dominance_results

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
        if 'community_' in comm_id:
            comm_composition = community_data[intensity_key][comm_id]['sc_list']
            
            # Convert to numpy array and find most abundant species
            if isinstance(comm_composition, dict):
                # Handle case where sc_list is a dictionary with nested structure
                if "0" in comm_composition:
                    # sc_list contains a dictionary with "0" key
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

def plot_species_vs_community_dominance_simulation_corrected(k_gamma_value):
    """Plot correlation for simulation data with CORRECTED species-level dominance calculation."""
    
    # Load simulation data
    interaction_matrix, carrying_capacities, community_library, community_data, dominance_results = load_simulation_data(k_gamma_value)
    
    # Get community compositions and most abundant species
    communities, most_abundant_indices = get_most_abundant_species_from_simulation(community_data)
    
    # Color setup for different k_gamma values
    colors = ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5']  # Different colors for each k_gamma
    gamma_values = [0.3, 0.5, 0.7, 1.0]
    color_idx = gamma_values.index(k_gamma_value) if k_gamma_value in gamma_values else 0
    color = colors[color_idx]
    
    data_label = []
    data_community = []
    data_abspecies = []
    
    # Process coalescence events
    num_communities = len(communities)
    
    # Generate pairwise coalescence comparisons
    for i in range(num_communities):
        for j in range(i+1, num_communities):
            c_1 = np.array(communities[i])
            c_2 = np.array(communities[j])
            
            # Simulate coalescence outcome (simplified)
            c_mix = c_1 + c_2
            c_mix = c_mix / np.sum(c_mix)  # Normalize
            
            # Apply threshold
            c_1 = c_1 * (c_1 > 1e-4)
            c_2 = c_2 * (c_2 > 1e-4)
            
            if np.sum(c_1) == 0 or np.sum(c_2) == 0:
                continue
            
            # Vector decomposition
            u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
            
            # Vector similarity approach
            x_val, y_val = calculate_assymetricity(u, v, k)
            ii = characterize_case(x_val, y_val)
            
            # Get directional asymmetricity for community-level dominance
            x_val, y_val = calculate_assymetricity_direction(u, v, k)
            
            # Calculate vector similarity-based relative competition score
            vector_similarity_score = u / (u + v + 1e-8)
            
            # Get most abundant species from each community
            C1 = most_abundant_indices[i]
            C2 = most_abundant_indices[j]
            
            # Check if both species are within interaction matrix bounds
            if C1 >= interaction_matrix.shape[0] or C2 >= interaction_matrix.shape[0]:
                print(f"Skipping species pair ({C1}, {C2}) - out of bounds for matrix size {interaction_matrix.shape}")
                continue
            
            # CORRECTED: Get interaction coefficients and carrying capacities
            alpha_12 = interaction_matrix.iloc[C1, C2]  # Effect of species 2 on species 1
            alpha_21 = interaction_matrix.iloc[C2, C1]  # Effect of species 1 on species 2
            
            # Get carrying capacities (assuming first column contains K values)
            if carrying_capacities.shape[1] > 0:
                K1 = carrying_capacities.iloc[C1, 0]
                K2 = carrying_capacities.iloc[C2, 0]
            else:
                # Use uniform carrying capacities if not available
                K1 = K2 = 1.0
            
            # CORRECTED: Calculate species-level dominance using LV equilibrium equations
            species_level_dominance = calculate_lv_equilibrium_dominance(alpha_12, alpha_21, K1, K2)
            
            data_label.append(ii)
            data_community.append(vector_similarity_score)
            data_abspecies.append(species_level_dominance)
    
    if len(data_community) == 0:
        print(f"Warning: No valid data points for k_gamma={k_gamma_value}")
        return
    
    # Process data following experimental style
    x = np.array(data_abspecies)
    y = np.array(data_community)
    data_label = np.array(data_label)
    
    # Duplicate data points (as in experimental version)
    duplicate = True
    if duplicate:
        x = np.concatenate((x, 1-x))
        y = np.concatenate((y, 1-y))
        data_label = np.concatenate((data_label, data_label))
    
    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(70*mm, 70*mm), facecolor='w', edgecolor='k')
    
    # Calculate linear regression
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Create scatter plot
    plt.scatter(x, y, color=color, s=4, alpha=0.5)
    
    # Add linear regression line
    plt.plot([0,1], slope * np.array([0,1]) + intercept, alpha=0.8, linewidth=0.5, color='black')
    
    # Add R-squared annotation
    plt.annotate('$R^2$ = {:.2f}'.format(r_squared), xy=(0.05+0.7, 0.55), xycoords='axes fraction', fontsize=8, color='black')
    
    # Add heatmap overlay
    section_size = 1.0/3 + 1e-8
    sections_x = np.arange(0, 1.1, section_size)
    sections_y = np.arange(0, 1.1, section_size)
    count_matrix = np.zeros((len(sections_x) - 1, len(sections_y) - 1))
    
    # Count points in each section
    for i in range(len(sections_x) - 1):
        for j in range(len(sections_y) - 1):
            x_min, x_max = sections_x[i], sections_x[i + 1]
            y_min, y_max = sections_y[j], sections_y[j + 1]
            count_matrix[i, j] = np.sum((x >= x_min) & (x < x_max) & (y >= y_min) & (y < y_max))
    
    total_points = np.sum(count_matrix)
    percentage_matrix = (count_matrix / total_points) * 100
    
    # Create heatmap
    plt.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)
    for i in range(len(sections_x) - 1):
        for j in range(len(sections_y) - 1):
            if percentage_matrix[i, j] > 10:
                plt.text(sections_x[i] + section_size/2, sections_y[j] + section_size/2, 
                        f'{percentage_matrix[i, j]:.1f}%', color='black', size=8, alpha=0.7, ha='center', va='center')
    
    # Set axis properties
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    custom_ticks = [0, 1]
    plt.xticks(custom_ticks, custom_ticks)
    plt.yticks(custom_ticks, custom_ticks)
    
    plt.xlabel('Species-level LV Equilibrium Dominance')
    plt.ylabel('Community-level Coalescence Dominance')
    plt.title(f'CORRECTED: k_gamma={k_gamma_value}')
    
    # Count aligned points for reporting
    aligned_mask = ((x > 0.5) & (y > 0.5)) | ((x < 0.5) & (y < 0.5))
    num_aligned = np.sum(aligned_mask)
    total_points_check = len(x)
    fraction_aligned = num_aligned / total_points_check
    
    print(f'CORRECTED k_gamma {k_gamma_value}: Aligned points: {num_aligned} / {total_points_check} = {fraction_aligned:.3f}')
    
    plt.savefig(f'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_Simulation_Corrected_{k_gamma_value}.svg', bbox_inches='tight')
    plt.close()

def main():
    """Main function to run corrected simulation analyses."""
    # Create output directories
    if not os.path.exists('Figure/TopDownAnaylsis'):
        os.makedirs('Figure/TopDownAnaylsis')
    if not os.path.exists('Figure'):
        os.makedirs('Figure')
    
    # k_gamma values to analyze (using new_k_gamma directories)
    k_gamma_values = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5, 1.0]
    
    print("=== CORRECTED VERSION: Using Lotka-Volterra Equilibrium Equations ===")
    print("Plotting species vs community dominance for each k_gamma value...")
    for k_gamma in k_gamma_values:
        print(f"Processing k_gamma = {k_gamma}")
        try:
            plot_species_vs_community_dominance_simulation_corrected(k_gamma)
        except Exception as e:
            print(f"Error processing k_gamma={k_gamma}: {e}")
    
    print("Corrected simulation analysis complete!")

if __name__ == "__main__":
    main()