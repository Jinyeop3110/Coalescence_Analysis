#!/usr/bin/env python3
"""
Fixed phase diagram creation function for simulation data.
This should be integrated into common_setup.py or used as a replacement.
"""

import numpy as np
import matplotlib.pyplot as plt
from COLORMAP import get_phase_diagram_colors

def create_phase_diagram_for_simulation(
    type_names,
    data1_set,  # a coefficients (parent 1) 
    data2_set,  # b coefficients (parent 2)
    data3_set,  # c residuals (restructuring)
    custom_x_ticks=None,
    custom_x_labels=None,
    output_filename="Figure/PhaseDiagram/Fig_phase_diagram.svg",
    plot_boundary=False,
    u_values=None,  # Add parameter for actual u-values
):
    """
    Creates a phase diagram specifically for simulation data.
    
    This function properly handles vector decomposition coefficients
    without incorrectly passing them through calculate_assymetricity.
    
    Args:
        type_names: List of type indices
        data1_set: Dict of parent 1 coefficients by type
        data2_set: Dict of parent 2 coefficients by type  
        data3_set: Dict of residual magnitudes by type
    """
    # For 500-species, use full range like standard simulations
    if u_values is not None and len(u_values) == 3 and max(u_values) <= 0.7:
        # This is 500-species data - use full range 0.1 to 1.2
        full_u_range = np.arange(0.1, 1.3, 0.1)
        n_full_range = len(full_u_range)
        
        class1_fractions = np.zeros(n_full_range)
        class2_fractions = np.zeros(n_full_range)
        class3_fractions = np.zeros(n_full_range)
        
        # Map u-values to correct positions in full range
        u_to_idx = {}
        for i, u_val in enumerate(u_values):
            for j, u_full in enumerate(full_u_range):
                if abs(u_full - u_val) < 0.05:
                    u_to_idx[i] = j
                    break
    else:
        # Standard simulation data
        n_types = len(type_names)
        n_full_range = n_types
        class1_fractions = np.zeros(n_types)
        class2_fractions = np.zeros(n_types)
        class3_fractions = np.zeros(n_types)
        u_to_idx = {i: i for i in range(n_types)}
    
    colors = get_phase_diagram_colors()
    
    for c_i, type_name in enumerate(type_names):
        if type_name not in data1_set:
            continue
            
        class1_count = 0  # Dominance
        class2_count = 0  # Mixing
        class3_count = 0  # Restructuring
        
        # Get vector decomposition data
        a_vals = data1_set[type_name]
        b_vals = data2_set[type_name]
        c_vals = data3_set[type_name]
        
        # Ensure same length
        min_len = min(len(a_vals), len(b_vals), len(c_vals))
        
        for j in range(min_len):
            a = a_vals[j]
            b = b_vals[j]
            c = c_vals[j]
            
            # Normalize for classification
            total = a + b + c
            if total <= 0:
                class3_count += 1  # Default to restructuring
                continue
                
            a_norm = a / total
            b_norm = b / total
            c_norm = c / total
            
            # Classify based on normalized coefficients
            if c_norm > 0.5:
                # High residual -> Restructuring
                class3_count += 1
            elif abs(a_norm - b_norm) > 0.3:
                # One parent dominates -> Dominance
                class1_count += 1
            else:
                # Similar contributions -> Mixing
                class2_count += 1
        
        total = class1_count + class2_count + class3_count
        if total > 0:
            idx = u_to_idx.get(c_i, c_i)
            class1_fractions[idx] = class1_count / total
            class2_fractions[idx] = class2_count / total
            class3_fractions[idx] = class3_count / total
    
    # Create plot
    mm = 1 / 25.4 * 72
    fig_width = 60 * mm
    fig_height = 60 * mm
    
    fig, ax1 = plt.subplots(1, 1, figsize=(fig_width/72, fig_height/72))
    
    # Set x-axis positions
    x_positions = np.arange(n_full_range)
    
    # Plot stacked bars
    width = 0.8
    
    p1 = ax1.bar(x_positions, class1_fractions, width,
                 color=colors[0], edgecolor='none')
    p2 = ax1.bar(x_positions, class2_fractions, width,
                 bottom=class1_fractions,
                 color=colors[1], edgecolor='none')
    p3 = ax1.bar(x_positions, class3_fractions, width,
                 bottom=class1_fractions + class2_fractions,
                 color=colors[2], edgecolor='none')
    
    # Customize axes
    ax1.set_ylim([0, 1])
    ax1.set_ylabel('Fraction', fontsize=9)
    ax1.set_xlabel('Interaction strength', fontsize=9)
    
    # Set x-axis limits and ticks  
    ax1.set_xlim([-0.5, n_full_range - 0.5])
    
    if u_values is not None and len(u_values) == 3 and max(u_values) <= 0.7:
        # 500-species: show full range with ticks at every other position
        ax1.set_xticks(np.arange(0, n_full_range, 2))
        ax1.set_xticklabels([f"{u:.1f}" for u in full_u_range[::2]])
    elif custom_x_ticks is not None and custom_x_labels is not None:
        ax1.set_xticks(custom_x_ticks)
        ax1.set_xticklabels(custom_x_labels)
    else:
        ax1.set_xticks(x_positions)
        ax1.set_xticklabels([str(t) for t in type_names])
    
    ax1.tick_params(axis='both', which='major', labelsize=7)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig