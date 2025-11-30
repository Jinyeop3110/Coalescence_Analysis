#!/usr/bin/env python3
"""
Create a corrected phase diagram for 500-species simulation data.

The issue with the current implementation is that it passes vector decomposition
coefficients through calculate_assymetricity, which is incorrect. The vector
decomposition already provides the classification information we need.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from COLORMAP import get_phase_diagram_colors

def classify_vector_decomposition(a, b, c):
    """
    Classify coalescence outcome based on vector decomposition coefficients.
    
    Args:
        a: Coefficient for parent 1
        b: Coefficient for parent 2  
        c: Residual magnitude (restructuring)
    
    Returns:
        0: Dominance (one parent strongly dominates)
        1: Mixing (both parents contribute similarly)
        2: Restructuring (large residual component)
    """
    # Normalize to ensure fair comparison
    total = a + b + c
    if total > 0:
        a_norm = a / total
        b_norm = b / total
        c_norm = c / total
    else:
        return 2  # Default to restructuring if all zeros
    
    # Classification based on normalized values
    if c_norm > 0.5:  # High residual -> restructuring
        return 2
    elif abs(a_norm - b_norm) > 0.3:  # Large difference -> dominance
        return 0
    else:  # Similar contributions -> mixing
        return 1

def create_corrected_phase_diagram():
    """Create phase diagram using proper vector decomposition classification."""
    
    print("="*60)
    print("CREATING CORRECTED 500-SPECIES PHASE DIAGRAM")
    print("="*60)
    
    # Load data
    session_name = "new_k_gamma_0_defined_pool_nooverlap_50from500_natural"
    excel_path = f"Simulation_Data/{session_name}/Similarity.xlsx"
    
    # Read the three sheets
    sheet0 = pd.read_excel(excel_path, sheet_name='0')  # a values
    sheet1 = pd.read_excel(excel_path, sheet_name='1')  # b values
    sheet2 = pd.read_excel(excel_path, sheet_name='2')  # c values
    
    u_values = [0.3, 0.5, 0.7]
    
    # Calculate class fractions for each u-value
    class_fractions = {0: [], 1: [], 2: []}  # dominance, mixing, restructuring
    
    for i, u_val in enumerate(u_values):
        col_name = f"u_{u_val}"
        
        if col_name not in sheet0.columns:
            print(f"Warning: Column {col_name} not found")
            continue
            
        # Get vector decomposition values
        a_vals = sheet0[col_name].dropna()
        b_vals = sheet1[col_name].dropna()
        c_vals = sheet2[col_name].dropna()
        
        # Ensure same length
        min_len = min(len(a_vals), len(b_vals), len(c_vals))
        a_vals = a_vals[:min_len]
        b_vals = b_vals[:min_len]
        c_vals = c_vals[:min_len]
        
        # Classify each event
        class_counts = {0: 0, 1: 0, 2: 0}
        for a, b, c in zip(a_vals, b_vals, c_vals):
            class_idx = classify_vector_decomposition(a, b, c)
            class_counts[class_idx] += 1
        
        # Calculate fractions
        total = sum(class_counts.values())
        if total > 0:
            for class_idx in range(3):
                class_fractions[class_idx].append(class_counts[class_idx] / total)
        else:
            for class_idx in range(3):
                class_fractions[class_idx].append(0.0)
        
        print(f"\nu = {u_val}:")
        print(f"  Total events: {total}")
        print(f"  Dominance: {class_counts[0]} ({class_fractions[0][-1]:.1%})")
        print(f"  Mixing: {class_counts[1]} ({class_fractions[1][-1]:.1%})")
        print(f"  Restructuring: {class_counts[2]} ({class_fractions[2][-1]:.1%})")
    
    # Create the plot
    print("\n🎨 Creating phase diagram...")
    
    colors = get_phase_diagram_colors()  # [dominance_red, mixing_purple, restructuring_green]
    
    # Set up figure
    mm = 1 / 25.4 * 72
    fig_width = 60 * mm
    fig_height = 60 * mm
    fig, ax = plt.subplots(1, 1, figsize=(fig_width/72, fig_height/72))
    
    # X-axis positions for u = [0.3, 0.5, 0.7]
    # Map to positions 1, 2, 3 on scale from 0.1 to 1.1
    x_positions = [1, 2, 3]  
    
    # Plot stacked bars
    width = 0.8
    
    # Plot each class
    bottom = np.zeros(len(u_values))
    
    # Dominance (red)
    ax.bar(x_positions, class_fractions[0], width, 
           bottom=bottom, color=colors[0], label='Dominance')
    bottom += class_fractions[0]
    
    # Mixing (purple)
    ax.bar(x_positions, class_fractions[1], width,
           bottom=bottom, color=colors[1], label='Mixing')
    bottom += class_fractions[1]
    
    # Restructuring (green)
    ax.bar(x_positions, class_fractions[2], width,
           bottom=bottom, color=colors[2], label='Restructuring')
    
    # Customize plot
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 1)
    
    # Set custom x-axis
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ax.set_xticklabels(['0.1', '0.3', '0.5', '0.7', '0.9', '1.1', '1.3', '1.5', '1.7', '1.9', '2.1'])
    
    ax.set_xlabel('Interaction strength (u)', fontsize=9)
    ax.set_ylabel('Fraction', fontsize=9)
    ax.tick_params(axis='both', labelsize=7)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Save figure
    output_path = "Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500_corrected.svg"
    plt.tight_layout()
    plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight')
    print(f"✓ Saved corrected phase diagram to: {output_path}")
    
    # Also save as PNG for quick viewing
    output_png = output_path.replace('.svg', '.png')
    plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight')
    print(f"✓ Also saved as PNG: {output_png}")
    
    plt.close()

if __name__ == "__main__":
    create_corrected_phase_diagram()