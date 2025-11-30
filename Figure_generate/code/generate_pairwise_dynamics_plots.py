#!/usr/bin/env python3
"""
generate_pairwise_dynamics_plots.py

Purpose: Generate pairwise species interaction dynamics plots showing transitions
from initial conditions (e.g., 0.1, 0.9) to final experimental outcomes.

Based on: Generate_Fig5_4_MostAbundant_Simulation.ipynb
Author: Gore Lab Analysis Team
Date: January 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import local modules
try:
    from InitializeSpeciesPool import InitializeSpeceiesPool
    from LV import run_lotka_volterra, run_lotka_volterra_dynamics
    from VariousMetrics import SimilarityTo1, SimilarityBC
except ImportError as e:
    print(f"Warning: Could not import local modules: {e}")
    print("Some simulation functions may not work.")

# Set up plotting parameters
plt.ioff()  # Turn off interactive mode
sns.set_style("ticks")
plt.rcParams.update({
    'figure.dpi': 300,
    'font.size': 8,
    'font.family': 'Arial',
    'axes.linewidth': 0.5,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'text.usetex': False
})

# Global variables
mm = 0.1/2.54  # Convert mm to inches

def setup_directories():
    """Create output directories"""
    base_dir = Path("/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure")
    output_dir = base_dir / "PairwiseDynamics"
    data_dir = Path("Data_dynamics")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    
    print(f"Output directory created: {output_dir}")
    return output_dir, data_dir

def load_data_paths():
    """Define data file paths"""
    base_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404"
    
    paths = {
        'coalescence_synthetic': f"{base_path}/Analyzed/processed_CoalescenceEvent_synthetic.xlsx",
        'communities_synthetic': f"{base_path}/Analyzed/processed_Communities_synthetic.xlsx",
        'coalescence_natural': f"{base_path}/Analyzed/processed_CoalescenceEvent_natural.xlsx", 
        'communities_natural': f"{base_path}/Analyzed/processed_Communities_natural.xlsx",
        'coalescence_simulation': f"{base_path}/Analyzed/processed_CoalescenceEvent_simulation_uniform.xlsx",
        'coalescence_recipe': f"{base_path}/Postprocessed/CoalescenceRecipe.xlsx",
        'metadata': f"{base_path}/Postprocessed/Metadata.xlsx",
        'sequences_synthetic': f"{base_path}/Postprocessed/processed_Sequences_synthetic.xlsx",
        'sequences_natural': f"{base_path}/Postprocessed/processed_Sequences_natural.xlsx",
        'pairwise_counts': f"{base_path}/Postprocessed/PairwiseColonyCountings_processed_230915.xlsx"
    }
    return paths

def load_experimental_data():
    """Load all experimental data files"""
    paths = load_data_paths()
    
    try:
        # Load coalescence and communities data
        coalescence_synthetic = pd.read_excel(paths['coalescence_synthetic'])
        communities_synthetic = pd.read_excel(paths['communities_synthetic'])
        coalescence_natural = pd.read_excel(paths['coalescence_natural'])
        communities_natural = pd.read_excel(paths['communities_natural'])
        
        # Combine synthetic and natural data
        coalescence_data = pd.concat([coalescence_synthetic, coalescence_natural])
        communities_data = pd.concat([communities_synthetic, communities_natural])
        
        # Load simulation data
        coalescence_simulation = pd.read_excel(paths['coalescence_simulation'])
        
        # Load metadata and sequences
        metadata = pd.read_excel(paths['metadata'])
        sequences_synthetic = pd.read_excel(paths['sequences_synthetic'])
        sequences_natural = pd.read_excel(paths['sequences_natural'])
        
        print("Successfully loaded experimental data")
        return {
            'coalescence_data': coalescence_data,
            'communities_data': communities_data,
            'coalescence_simulation': coalescence_simulation,
            'metadata': metadata,
            'sequences_synthetic': sequences_synthetic,
            'sequences_natural': sequences_natural
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_pairwise_count_data():
    """Load and process pairwise colony counting data"""
    paths = load_data_paths()
    pairwise_path = paths['pairwise_counts']
    
    try:
        mono_count_data = {}
        pairwise_count_data = {}
        
        # Load monoculture data for each medium
        for i, medium in enumerate(['LN', 'MN', 'HN']):
            data = pd.read_excel(pairwise_path, sheet_name=i)
            data = np.transpose(np.array(data.values[:, 1:]))
            mono_count_data[medium] = data
        
        # Load pairwise competition data
        for i, medium in enumerate(['LN', 'MN', 'HN']):
            sheet_idx1 = 3 + i*2  # Sheets 3,5,7
            sheet_idx2 = 4 + i*2  # Sheets 4,6,8
            
            data_1 = pd.read_excel(pairwise_path, sheet_name=sheet_idx1).values[:, 1:]
            data_2 = pd.read_excel(pairwise_path, sheet_name=sheet_idx2).values[:, 1:]
            pairwise_count_data[medium] = np.stack([data_1, data_2])
        
        return mono_count_data, pairwise_count_data
    
    except Exception as e:
        print(f"Error loading pairwise data: {e}")
        return None, None

def process_pairwise_count_data(mono_count_data, pairwise_count_data, medium_type):
    """Process pairwise count data to get dominance ratios"""
    data_m = np.mean(mono_count_data[medium_type], 1)
    data_p_1 = pairwise_count_data[medium_type][0, :]
    data_p_2 = pairwise_count_data[medium_type][1, :]
    
    data_flag = np.array([[None] * 12] * 12)
    data_p_ratio = np.zeros((12, 12))
    
    for i in range(12):
        for j in range(12):
            if np.isnan(data_p_1[i, j]):
                data_flag[i, j] = 'case0'  # No data
                data_p_ratio[i, j] = np.nan
            elif i == j:
                data_p_ratio[i, j] = 0.5  # Self-interaction
                data_flag[i, j] = 'self'
            else:
                if data_p_1[i, j] == 1 and data_p_2[i, j] == 0:
                    # Species i completely dominates
                    data_flag[i, j] = 'case1'
                    data_p_ratio[i, j] = 1.0
                elif data_p_1[i, j] == 0 and data_p_2[i, j] == 1:
                    # Species j completely dominates
                    data_flag[i, j] = 'case2'
                    data_p_ratio[i, j] = 0.0
                else:
                    # Coexistence - normalize by monoculture counts
                    data_flag[i, j] = 'case3'
                    norm_1 = data_p_1[i, j] / data_m[i] if data_m[i] > 0 else 0
                    norm_2 = data_p_2[i, j] / data_m[j] if data_m[j] > 0 else 0
                    total = norm_1 + norm_2
                    if total > 0:
                        data_p_ratio[i, j] = norm_1 / total
                    else:
                        data_p_ratio[i, j] = 0.5
    
    return data_flag, data_p_ratio

def interpret_pairwise_result(y1, y2):
    """Interpret pairwise interaction result and return type and color"""
    if y1 == 1 and y2 == 1:
        return 'E', (0.85, 0.7, 0.7)  # E: competitive exclusion
    elif y1 == 0 and y2 == 0:
        return 'E', (0.85, 0.7, 0.7)  # E: competitive exclusion
    elif y1 == 0 and y2 == 1:
        return 'B', (0.7, 0.7, 0.9)  # B: Bistability
    elif y1 > 0 and y1 < 1 and y2 > 0 and y2 < 1:
        return 'C', (0.7, 0.85, 0.7)  # C: Coexistence
    else:
        return 'U', (0.5, 0.5, 0.5)  # U: Unclassified

def plot_pairwise_dynamics_matrix(medium='MN', output_dir=None):
    """Create pairwise dynamics matrix plot showing species interactions"""
    
    # Load pairwise data
    mono_count_data, pairwise_count_data = get_pairwise_count_data()
    if mono_count_data is None:
        print("Could not load pairwise data")
        return
    
    # Process data for the specified medium
    data_flag, data_p_ratio = process_pairwise_count_data(
        mono_count_data, pairwise_count_data, medium)
    
    # Create the matrix plot
    N = 12
    fig, axs = plt.subplots(N, N, figsize=(250*mm, 250*mm))
    
    case_list = []
    for i in range(12):
        for j in range(12):
            if j <= i:
                # Lower triangle - hide axes
                axs[i, j].spines['top'].set_visible(False)
                axs[i, j].spines['right'].set_visible(False)
                axs[i, j].spines['bottom'].set_visible(False)
                axs[i, j].spines['left'].set_visible(False)
                axs[i, j].get_xaxis().set_ticks([])
                axs[i, j].get_yaxis().set_ticks([])
            elif data_flag[i, j] == 'case0':
                # No data - hide axes
                axs[i, j].spines['top'].set_visible(False)
                axs[i, j].spines['right'].set_visible(False)
                axs[i, j].spines['bottom'].set_visible(False)
                axs[i, j].spines['left'].set_visible(False)
                axs[i, j].get_xaxis().set_ticks([])
                axs[i, j].get_yaxis().set_ticks([])
            else:
                # Plot dynamics
                # Species i dynamics (starting from ~0.1, ending at data_p_ratio[i,j])
                x1 = [0, 1]
                y1 = [0.05, data_p_ratio[i, j]]
                axs[i, j].plot(x1, y1, color='red', linewidth=2, alpha=0.8)
                
                # Species j dynamics (starting from ~0.9, ending at 1-data_p_ratio[j,i])
                x2 = [0, 1]
                y2 = [0.95, 1 - data_p_ratio[j, i]]
                axs[i, j].plot(x2, y2, color='blue', linewidth=2, alpha=0.8)
                
                axs[i, j].set_ylim(0, 1)
                axs[i, j].set_xlim(0, 1)
                
                # Determine interaction type and set background color
                case, shade = interpret_pairwise_result(y1[1], y2[1])
                case_list.append(case)
                axs[i, j].set_facecolor(shade)
                
                # Add title showing species pair
                axs[i, j].set_title(f'ASV{i+1} vs ASV{j+1}', fontsize=6)
                
                # Add axis labels for edge plots
                if i == N-1:
                    axs[i, j].set_xlabel('Time', fontsize=6)
                if j == 0:
                    axs[i, j].set_ylabel('Abundance', fontsize=6)
                
                # Set tick parameters
                axs[i, j].tick_params(axis='both', which='major', labelsize=4)
    
    plt.suptitle(f'Pairwise Species Interaction Dynamics - {medium}', fontsize=14)
    plt.tight_layout()
    
    if output_dir:
        filename = f"Pairwise_Dynamics_Matrix_{medium}.svg"
        plt.savefig(output_dir / filename, format='svg', bbox_inches='tight', dpi=300)
        plt.savefig(output_dir / filename.replace('.svg', '.png'), 
                   format='png', bbox_inches='tight', dpi=300)
        print(f"Saved: {filename}")
    
    plt.show()
    plt.close()
    
    return case_list

def plot_individual_pairwise_dynamics(species_i, species_j, medium='MN', 
                                    initial_conditions=(0.1, 0.9), output_dir=None):
    """Plot individual pairwise dynamics for specific species pair"""
    
    # Load pairwise data
    mono_count_data, pairwise_count_data = get_pairwise_count_data()
    if mono_count_data is None:
        print("Could not load pairwise data")
        return
    
    # Process data
    data_flag, data_p_ratio = process_pairwise_count_data(
        mono_count_data, pairwise_count_data, medium)
    
    # Create time series
    time_points = np.linspace(0, 1, 100)
    
    # Species dynamics - simple exponential transition
    initial_i, initial_j = initial_conditions
    final_i = data_p_ratio[species_i, species_j] if not np.isnan(data_p_ratio[species_i, species_j]) else 0.5
    final_j = 1 - final_i
    
    # Exponential approach to final values
    dynamics_i = final_i + (initial_i - final_i) * np.exp(-3 * time_points)
    dynamics_j = final_j + (initial_j - final_j) * np.exp(-3 * time_points)
    
    # Create plot
    fig, ax = plt.subplots(1, 1, figsize=(80*mm, 60*mm))
    
    ax.plot(time_points, dynamics_i, color='red', linewidth=2, 
           label=f'ASV{species_i+1}', alpha=0.8)
    ax.plot(time_points, dynamics_j, color='blue', linewidth=2, 
           label=f'ASV{species_j+1}', alpha=0.8)
    
    # Add initial condition markers
    ax.scatter([0, 0], [initial_i, initial_j], 
              c=['red', 'blue'], s=50, zorder=5, alpha=0.7)
    
    # Add final condition markers  
    ax.scatter([1, 1], [final_i, final_j], 
              c=['red', 'blue'], s=50, marker='s', zorder=5, alpha=0.7)
    
    ax.set_xlabel('Time (normalized)')
    ax.set_ylabel('Species Abundance')
    ax.set_title(f'Pairwise Dynamics: ASV{species_i+1} vs ASV{species_j+1} ({medium})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    
    if output_dir:
        filename = f"Pairwise_Dynamics_ASV{species_i+1}_vs_ASV{species_j+1}_{medium}.svg"
        plt.savefig(output_dir / filename, format='svg', bbox_inches='tight', dpi=300)
        plt.savefig(output_dir / filename.replace('.svg', '.png'), 
                   format='png', bbox_inches='tight', dpi=300)
        print(f"Saved: {filename}")
    
    plt.show()
    plt.close()

def simulate_lotka_volterra_dynamics(output_dir=None):
    """Simulate Lotka-Volterra dynamics for community coalescence"""
    
    print("Running Lotka-Volterra simulation...")
    
    try:
        # Parameters
        rand_seed = 4
        np.random.seed(rand_seed)
        
        def uniform_distribution(u, o):
            return (2*u + 2*o) * np.random.random() - o
        
        # Simulation parameters
        u = 0.6
        o = 0
        f_interaction = lambda: uniform_distribution(u, o)
        num_C = 2
        num_S = 12
        N = num_C * num_S
        
        # Initialize species pool and community library
        I, g, k = InitializeSpeceiesPool(N, f_interaction, 
                                      f_g=lambda: np.ones(1),
                                      f_k=lambda: np.ones(1), 
                                      is_diagonal_one=True, 
                                      save_path="Data_dynamics/test")
        
        # Community library
        communities_library = np.zeros([num_C, N])
        for i in range(num_C):
            communities_library[i, np.arange(num_S*i, num_S*(i+1))] = 1
        
        # Run dynamics
        t = [0, 5000]
        threshold = 1e-3
        y = np.random.rand(N) * 0.1
        t_eval = np.linspace(0, 5000, 10000)
        
        # Individual communities
        c1 = run_lotka_volterra_dynamics(y, t, communities_library[0, :], 
                                        I, g, k, t_eval).y.T
        c2 = run_lotka_volterra_dynamics(y, t, communities_library[1, :], 
                                        I, g, k, t_eval).y.T
        
        # Mixed community
        y1 = c1[-1]
        y2 = c2[-1]
        y1[y1 < threshold] = 0
        y2[y2 < threshold] = 0
        y3 = np.array(y1.tolist() + y2.tolist())
        survived = y3 > threshold
        c3 = run_lotka_volterra_dynamics(y3, t, survived, I, g, k, t_eval).y.T
        c3_temp = np.zeros((len(t_eval), 24))
        for i, idx in enumerate(np.where(survived)[0]):
            c3_temp[:, idx] = c3[:, i]
        c3 = c3_temp
        
        # Create plots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(150*mm, 50*mm))
        
        # Plot community 1
        for i in range(12):
            ax1.plot(t_eval, c1[:, i], linewidth=0.7, alpha=0.8)
        ax1.axhline(y=0.001, linewidth=0.7, linestyle='dotted', color='black')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Abundance')
        ax1.set_title('Community 1 Dynamics')
        ax1.set_ylim(3*1e-4, 1)
        
        # Plot community 2
        for i in range(12):
            ax2.plot(t_eval, c2[:, i], linewidth=0.7, alpha=0.8)
        ax2.axhline(y=0.001, linewidth=0.7, linestyle='dotted', color='black')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Abundance')
        ax2.set_title('Community 2 Dynamics')
        ax2.set_ylim(3*1e-4, 1)
        
        # Plot mixed community
        for i in range(12):
            ax3.plot(t_eval, c3[:, i], linewidth=0.7, color='red', alpha=0.6)
            if i < 12:
                ax3.plot(t_eval, c3[:, 12+i], linewidth=0.7, color='blue', alpha=0.6)
        ax3.axhline(y=0.001, linewidth=0.7, linestyle='dotted', color='black')
        ax3.set_xscale('log')
        ax3.set_yscale('log')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Abundance')
        ax3.set_title('Mixed Community Dynamics')
        ax3.set_ylim(3*1e-4, 1)
        
        plt.tight_layout()
        
        if output_dir:
            filename = "Lotka_Volterra_Community_Dynamics.svg"
            plt.savefig(output_dir / filename, format='svg', bbox_inches='tight', dpi=300)
            plt.savefig(output_dir / filename.replace('.svg', '.png'), 
                       format='png', bbox_inches='tight', dpi=300)
            print(f"Saved: {filename}")
        
        plt.show()
        plt.close()
        
    except Exception as e:
        print(f"Error in Lotka-Volterra simulation: {e}")
        print("This may be due to missing InitializeSpeciesPool or LV modules.")

def plot_interaction_outcome_summary(media=['LN', 'MN', 'HN'], output_dir=None):
    """Plot summary of interaction outcomes across media"""
    
    # Load data
    mono_count_data, pairwise_count_data = get_pairwise_count_data()
    if mono_count_data is None:
        return
    
    outcome_data = {}
    
    for medium in media:
        data_flag, data_p_ratio = process_pairwise_count_data(
            mono_count_data, pairwise_count_data, medium)
        
        cases = []
        for i in range(12):
            for j in range(12):
                if i != j and data_flag[i, j] not in ['case0', None]:
                    y1 = data_p_ratio[i, j]
                    y2 = 1 - data_p_ratio[j, i] if not np.isnan(data_p_ratio[j, i]) else 0.5
                    case, _ = interpret_pairwise_result(y1, y2)
                    cases.append(case)
        
        # Count outcomes
        from collections import Counter
        case_counts = Counter(cases)
        outcome_data[medium] = case_counts
    
    # Create summary plot
    fig, ax = plt.subplots(1, 1, figsize=(100*mm, 70*mm))
    
    outcomes = ['C', 'E', 'B', 'U']  # Coexistence, Exclusion, Bistability, Unclassified
    colors = [(0.7, 0.85, 0.7), (0.85, 0.7, 0.7), (0.7, 0.7, 0.9), (0.5, 0.5, 0.5)]
    
    x = np.arange(len(media))
    width = 0.2
    
    for i, outcome in enumerate(outcomes):
        counts = [outcome_data[medium].get(outcome, 0) for medium in media]
        ax.bar(x + i*width, counts, width, label=outcome, color=colors[i], alpha=0.8)
    
    ax.set_xlabel('Medium')
    ax.set_ylabel('Number of Interactions')
    ax.set_title('Pairwise Interaction Outcomes Across Media')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(media)
    ax.legend(title='Outcome Type')
    
    plt.tight_layout()
    
    if output_dir:
        filename = "Interaction_Outcomes_Summary.svg"
        plt.savefig(output_dir / filename, format='svg', bbox_inches='tight', dpi=300)
        plt.savefig(output_dir / filename.replace('.svg', '.png'), 
                   format='png', bbox_inches='tight', dpi=300)
        print(f"Saved: {filename}")
    
    plt.show()
    plt.close()

def main():
    """Main function to generate all pairwise dynamics plots"""
    
    print("Starting Pairwise Dynamics Plot Generation...")
    
    # Setup directories
    output_dir, data_dir = setup_directories()
    
    # Generate different types of plots
    media = ['LN', 'MN', 'HN']
    
    # 1. Generate matrix plots for each medium
    print("\n1. Generating pairwise dynamics matrices...")
    for medium in media:
        try:
            case_list = plot_pairwise_dynamics_matrix(medium, output_dir)
            print(f"  - {medium}: Generated matrix with {len(case_list)} interactions")
        except Exception as e:
            print(f"  - Error with {medium}: {e}")
    
    # 2. Generate individual dynamics plots for selected pairs
    print("\n2. Generating individual pairwise dynamics...")
    example_pairs = [(0, 1), (2, 5), (7, 10)]  # ASV pairs to showcase
    for species_i, species_j in example_pairs:
        for medium in ['MN']:  # Focus on MN for examples
            try:
                plot_individual_pairwise_dynamics(species_i, species_j, medium, 
                                                (0.1, 0.9), output_dir)
                print(f"  - Generated ASV{species_i+1} vs ASV{species_j+1} for {medium}")
            except Exception as e:
                print(f"  - Error with ASV{species_i+1} vs ASV{species_j+1}: {e}")
    
    # 3. Generate Lotka-Volterra simulation
    print("\n3. Generating Lotka-Volterra simulation...")
    try:
        simulate_lotka_volterra_dynamics(output_dir)
        print("  - LV simulation completed")
    except Exception as e:
        print(f"  - LV simulation error: {e}")
    
    # 4. Generate outcome summary
    print("\n4. Generating interaction outcomes summary...")
    try:
        plot_interaction_outcome_summary(media, output_dir)
        print("  - Outcomes summary completed")
    except Exception as e:
        print(f"  - Outcomes summary error: {e}")
    
    print(f"\nAll plots saved to: {output_dir}")
    print("Plot generation complete!")

if __name__ == "__main__":
    main()