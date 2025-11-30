#!/usr/bin/env python3
"""
Fixed version of create_phase_diagram for simulation data.

The key fix is to properly handle vector decomposition data without
incorrectly passing it through calculate_assymetricity.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def create_phase_diagram_simulation_fixed(
    type_names,
    data1_set,  # a coefficients (parent 1)
    data2_set,  # b coefficients (parent 2)
    data3_set,  # c residuals (restructuring)
    custom_x_ticks=None,
    custom_x_labels=None,
    output_filename="Figure/PhaseDiagram/Fig_phase_diagram_fixed.svg",
    plot_boundary=False,
):
    """
    Creates a phase diagram for simulation data using vector decomposition coefficients.
    
    This fixed version properly classifies based on the vector decomposition results
    rather than incorrectly transforming them through calculate_assymetricity.
    """
    from COLORMAP import get_phase_diagram_colors
    
    n_types = len(type_names)
    class1_fractions = np.zeros(n_types)  # Dominance
    class2_fractions = np.zeros(n_types)  # Mixing  
    class3_fractions = np.zeros(n_types)  # Restructuring
    
    colors = get_phase_diagram_colors()  # [dominance, mixing, restructuring]
    
    for c_i, type_name in enumerate(type_names):
        class1_count = 0
        class2_count = 0
        class3_count = 0
        
        # Get data for this type
        a_vals = data1_set[type_name]  # Parent 1 coefficients
        b_vals = data2_set[type_name]  # Parent 2 coefficients
        c_vals = data3_set[type_name]  # Residual magnitudes
        
        # Classify each coalescence event
        for j in range(len(a_vals)):
            a = a_vals[j]
            b = b_vals[j]
            c = c_vals[j]
            
            # Normalize coefficients for classification
            total = a + b + c
            if total > 0:
                a_norm = a / total
                b_norm = b / total
                c_norm = c / total
            else:
                # Default to restructuring if all zeros
                class3_count += 1
                continue
            
            # Classification logic based on vector decomposition
            if c_norm > 0.5:  
                # High residual component -> Restructuring
                class3_count += 1
            elif abs(a_norm - b_norm) > 0.3:  
                # One parent dominates -> Dominance
                class1_count += 1
            else:  
                # Similar contributions from both -> Mixing
                class2_count += 1
        
        total = class1_count + class2_count + class3_count
        if total > 0:
            class1_fractions[c_i] = class1_count / total
            class2_fractions[c_i] = class2_count / total
            class3_fractions[c_i] = class3_count / total
    
    # Create the plot
    mm = 1 / 25.4 * 72
    fig_width = 60 * mm
    fig_height = 60 * mm
    
    fig, ax = plt.subplots(1, 1, figsize=(fig_width/72, fig_height/72))
    
    # Plot stacked bars
    x_positions = np.array(type_names)
    width = 0.8
    
    # Stack the bars
    ax.bar(x_positions, class1_fractions, width, 
           color=colors[0], label='Dominance')
    ax.bar(x_positions, class2_fractions, width,
           bottom=class1_fractions, color=colors[1], label='Mixing')
    ax.bar(x_positions, class3_fractions, width,
           bottom=class1_fractions + class2_fractions, 
           color=colors[2], label='Restructuring')
    
    # Customize plot
    ax.set_ylim(0, 1)
    ax.set_ylabel('Fraction', fontsize=9)
    ax.set_xlabel('Interaction strength', fontsize=9)
    
    # Set custom x-axis if provided
    if custom_x_ticks is not None and custom_x_labels is not None:
        ax.set_xlim(custom_x_ticks[0]-0.5, custom_x_ticks[-1]+0.5)
        ax.set_xticks(custom_x_ticks)
        ax.set_xticklabels(custom_x_labels)
    
    ax.tick_params(axis='both', labelsize=7)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    plt.tight_layout()
    plt.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig

if __name__ == "__main__":
    # Test with 500-species data
    print("Testing fixed phase diagram creation...")
    
    import pandas as pd
    
    # Load 500-species data
    session_name = "new_k_gamma_0_defined_pool_nooverlap_50from500_natural"
    excel_path = f"Simulation_Data/{session_name}/Similarity.xlsx"
    
    sheet0 = pd.read_excel(excel_path, sheet_name='0')
    sheet1 = pd.read_excel(excel_path, sheet_name='1')
    sheet2 = pd.read_excel(excel_path, sheet_name='2')
    
    # Prepare data in expected format
    data1_dict = {}
    data2_dict = {}
    data3_dict = {}
    
    for i, col in enumerate(['u_0.3', 'u_0.5', 'u_0.7']):
        if col in sheet0.columns:
            data1_dict[i] = sheet0[col].dropna().tolist()
            data2_dict[i] = sheet1[col].dropna().tolist()
            data3_dict[i] = sheet2[col].dropna().tolist()
    
    types_to_plot = list(data1_dict.keys())
    custom_x_ticks = np.array([0, 2, 4, 6, 8, 10])
    custom_x_labels = ["0.1", "0.3", "0.5", "0.7", "0.9", "1.1"]
    
    create_phase_diagram_simulation_fixed(
        types_to_plot,
        data1_dict, data2_dict, data3_dict,
        custom_x_ticks, custom_x_labels,
        output_filename="Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500_fixed.svg"
    )
    
    print("✓ Created fixed phase diagram")