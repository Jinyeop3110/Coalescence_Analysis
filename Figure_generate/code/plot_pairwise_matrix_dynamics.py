#!/usr/bin/env python3
"""
plot_pairwise_matrix_dynamics.py

Purpose: Generate pairwise species interaction matrix plot showing dynamics
from initial conditions (0.05, 0.95) to final experimental outcomes.

Based on the exact code from Generate_Fig5_4_MostAbundant_Simulation.ipynb
Author: Gore Lab Analysis Team  
Date: January 2025
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent pop-ups
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
plt.ioff()  # Turn off interactive mode

# Set up plotting parameters
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

def setup_output_directory():
    """Create output directory"""
    output_dir = Path("/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/PairwiseMatrixDynamics")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def get_pairwise_count_data():
    """Load and process pairwise colony counting data"""
    pairwise_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Postprocessed/PairwiseColonyCountings_processed_230915.xlsx"
    
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

def getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium_type):
    """Process pairwise count data exactly as in the original notebook"""
    data_m = np.mean(Mono_Count_data[medium_type], 1)
    data_p_1 = Pairwise_Count_data[medium_type][0, :]
    data_p_2 = Pairwise_Count_data[medium_type][1, :]
    data_flag = np.array([[None] * 12] * 12)
    data_p_1_converted = np.array([[None] * 12] * 12)
    data_p_2_converted = np.array([[None] * 12] * 12)
    data_p_ratio = np.array([[None] * 12] * 12)

    count = 0
    for i in range(12):
        for j in range(12):
            if np.isnan(data_p_1[i, j]):
                data_flag[i, j] = 'case0'  # No data
            else:
                if data_p_1[i, j] == 1 and data_p_2[i, j] == 0:
                    data_flag[i, j] = 'case1'  # species i dominates
                    data_p_1_converted[i, j] = 1
                    data_p_2_converted[i, j] = 0
                    data_p_ratio[i, j] = 1
                elif data_p_1[i, j] == 0 and data_p_2[i, j] == 1:
                    data_flag[i, j] = 'case2'  # species j dominates
                    data_p_1_converted[i, j] = 0
                    data_p_2_converted[i, j] = 1
                    data_p_ratio[i, j] = 0
                else:
                    data_flag[i, j] = 'case3'  # species i, j coexists
                    data_p_1_converted[i, j] = data_p_1[i, j] / data_m[i]
                    data_p_2_converted[i, j] = data_p_2[i, j] / data_m[j]
                    data_p_ratio[i, j] = data_p_1_converted[i, j] / (data_p_1_converted[i, j] + data_p_2_converted[i, j])
    
    return data_p_1, data_p_2, data_flag, data_p_ratio

def drawPairwiseChange(i, j, x):
    """Sample function from original notebook"""
    return np.sin(i*x) + np.cos(j*x)

def InterpretPairwiseResult(y1, y2):
    """Interpret pairwise interaction result exactly as in original"""
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

def create_pairwise_matrix_plot(medium='MN'):
    """Create the exact pairwise matrix plot from the notebook"""
    
    # Load pairwise data
    print(f"Loading pairwise data for {medium}...")
    Mono_Count_data, Pairwise_Count_data = get_pairwise_count_data()
    
    if Mono_Count_data is None:
        print("Could not load pairwise data")
        return
    
    # Process data exactly as in notebook
    data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData(
        Mono_Count_data, Pairwise_Count_data, medium)
    
    # Create the matrix plot exactly as in notebook
    N = 12
    fig, axs = plt.subplots(N, N, figsize=(250*mm, 250*mm))
    
    case_list = []
    for i in range(12):
        for j in range(12):
            if j <= i:
                axs[i, j].spines['top'].set_visible(False)
                axs[i, j].spines['right'].set_visible(False)
                axs[i, j].spines['bottom'].set_visible(False)
                axs[i, j].spines['left'].set_visible(False)
                axs[i, j].get_xaxis().set_ticks([])
                axs[i, j].get_yaxis().set_ticks([])
            elif data_flag[i, j] == 'case0':
                axs[i, j].spines['top'].set_visible(False)
                axs[i, j].spines['right'].set_visible(False)
                axs[i, j].spines['bottom'].set_visible(False)
                axs[i, j].spines['left'].set_visible(False)
                axs[i, j].get_xaxis().set_ticks([])
                axs[i, j].get_yaxis().set_ticks([])
            else:
                # Plot dynamics exactly as in notebook
                x1 = [0, 1]
                y1 = [0.05, data_p_ratio[i, j]]
                axs[i, j].plot(x1, y1)
                
                x2 = [0, 1]
                y2 = [0.95, 1 - data_p_ratio[j, i]]
                axs[i, j].plot(x2, y2)
                
                axs[i, j].set_ylim(0, 1)
                
                case, shade = InterpretPairwiseResult(y1[1], y2[1])
                case_list.append(case)
                axs[i, j].set_facecolor(shade)
                
                axs[i, j].set_title(f'i, j={i+1},{j+1}', fontsize=6)
    
    plt.suptitle(f'Pairwise Species Dynamics Matrix - {medium}', fontsize=12)
    plt.tight_layout()
    
    # Save the plot
    output_dir = setup_output_directory()
    filename = f"Pairwise_Matrix_Dynamics_{medium}"
    
    plt.savefig(output_dir / f"{filename}.svg", format='svg', bbox_inches='tight', dpi=300)
    plt.savefig(output_dir / f"{filename}.png", format='png', bbox_inches='tight', dpi=300)
    
    print(f"Saved: {filename}.svg and {filename}.png")
    print(f"Total interactions plotted: {len(case_list)}")
    
    # Print summary of interaction types
    from collections import Counter
    case_counts = Counter(case_list)
    print("Interaction type counts:")
    for case_type, count in case_counts.items():
        case_names = {'C': 'Coexistence', 'E': 'Exclusion', 'B': 'Bistability', 'U': 'Unclassified'}
        print(f"  {case_names.get(case_type, case_type)}: {count}")
    
    plt.close()  # Close figure to free memory
    
    return case_list

def main():
    """Main function to create pairwise matrix dynamics plots"""
    
    print("Creating Pairwise Matrix Dynamics Plots...")
    print("(No pop-ups will appear)")
    
    # Create plots for all media
    media = ['LN', 'MN', 'HN']
    
    for medium in media:
        print(f"\n--- Processing {medium} ---")
        try:
            case_list = create_pairwise_matrix_plot(medium)
            print(f"Successfully created plot for {medium}")
        except Exception as e:
            print(f"Error creating plot for {medium}: {e}")
    
    output_dir = setup_output_directory()
    print(f"\nAll plots saved to: {output_dir}")
    print("Plot generation complete!")

if __name__ == "__main__":
    main()