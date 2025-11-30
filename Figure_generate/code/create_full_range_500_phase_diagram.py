#!/usr/bin/env python3
"""
Create a properly formatted 500-species phase diagram that matches the style
of other simulation phase diagrams with full u-range from 0.1 to 1.2.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from COLORMAP import get_phase_diagram_colors

def classify_vector_decomposition(a, b, c):
    """Classify coalescence outcome based on vector decomposition coefficients."""
    total = a + b + c
    if total > 0:
        a_norm = a / total
        b_norm = b / total
        c_norm = c / total
    else:
        return 2  # Default to restructuring
    
    if c_norm > 0.5:
        return 2  # Restructuring
    elif abs(a_norm - b_norm) > 0.3:
        return 0  # Dominance
    else:
        return 1  # Mixing

def create_full_range_500_phase_diagram():
    """Create phase diagram with full u-range like other simulations."""
    
    print("="*60)
    print("CREATING FULL-RANGE 500-SPECIES PHASE DIAGRAM")
    print("="*60)
    
    # Load 500-species data
    session_name = "new_k_gamma_0_defined_pool_nooverlap_50from500_natural"
    excel_path = f"Simulation_Data/{session_name}/Similarity.xlsx"
    
    sheet0 = pd.read_excel(excel_path, sheet_name='0')  # a values
    sheet1 = pd.read_excel(excel_path, sheet_name='1')  # b values
    sheet2 = pd.read_excel(excel_path, sheet_name='2')  # c values
    
    # Define the full range like standard simulations (0.1 to 1.2)
    full_u_range = np.arange(0.1, 1.3, 0.1)  # [0.1, 0.2, 0.3, ..., 1.2]
    n_types = len(full_u_range)
    
    print(f"Full u-range: {full_u_range}")
    print(f"Total positions: {n_types}")
    
    # Our 500-species data only exists at u = [0.3, 0.5, 0.7]
    available_u = [0.3, 0.5, 0.7]
    
    # Initialize fraction arrays for all positions
    class1_fractions = np.zeros(n_types)  # Dominance
    class2_fractions = np.zeros(n_types)  # Mixing
    class3_fractions = np.zeros(n_types)  # Restructuring
    
    # Calculate fractions only for positions where we have data
    for u_val in available_u:
        # Find the index in full_u_range that corresponds to this u_val
        u_idx = None
        for i, u_full in enumerate(full_u_range):
            if abs(u_full - u_val) < 0.05:  # Match within tolerance
                u_idx = i
                break
        
        if u_idx is None:
            print(f"Warning: u={u_val} not found in full range")
            continue
            
        col_name = f"u_{u_val}"
        
        if col_name not in sheet0.columns:
            print(f"Warning: Column {col_name} not found")
            continue
        
        # Get data for this u-value
        a_vals = sheet0[col_name].dropna()
        b_vals = sheet1[col_name].dropna() 
        c_vals = sheet2[col_name].dropna()
        
        min_len = min(len(a_vals), len(b_vals), len(c_vals))
        
        # Classify events
        class_counts = {0: 0, 1: 0, 2: 0}
        for i in range(min_len):
            class_idx = classify_vector_decomposition(a_vals.iloc[i], b_vals.iloc[i], c_vals.iloc[i])
            class_counts[class_idx] += 1
        
        # Calculate fractions and store at correct position
        total = sum(class_counts.values())
        if total > 0:
            class1_fractions[u_idx] = class_counts[0] / total
            class2_fractions[u_idx] = class_counts[1] / total 
            class3_fractions[u_idx] = class_counts[2] / total
            
            print(f"u = {u_val} (position {u_idx}):")
            print(f"  Total events: {total}")
            print(f"  Dominance: {class_counts[0]} ({class1_fractions[u_idx]:.1%})")
            print(f"  Mixing: {class_counts[1]} ({class2_fractions[u_idx]:.1%})")
            print(f"  Restructuring: {class_counts[2]} ({class3_fractions[u_idx]:.1%})")
    
    # Create the plot to match standard simulation style
    print("\n🎨 Creating full-range phase diagram...")
    
    colors = get_phase_diagram_colors()
    
    # Set up figure with same dimensions as standard simulations
    mm = 1 / 25.4 * 72
    fig_width = 60 * mm
    fig_height = 60 * mm
    
    fig, ax = plt.subplots(1, 1, figsize=(fig_width/72, fig_height/72))
    
    # X-axis positions for all u-values (0.1 to 1.2)
    x_positions = np.arange(n_types)
    width = 0.8
    
    # Plot stacked bars - only positions with data will show bars
    p1 = ax.bar(x_positions, class1_fractions, width,
                color=colors[0], edgecolor='none')
    p2 = ax.bar(x_positions, class2_fractions, width,
                bottom=class1_fractions, color=colors[1], edgecolor='none')
    p3 = ax.bar(x_positions, class3_fractions, width,
                bottom=class1_fractions + class2_fractions,
                color=colors[2], edgecolor='none')
    
    # Set axis properties to match standard simulations
    ax.set_xlim([-0.5, n_types - 0.5])
    ax.set_ylim([0, 1])
    
    # Set x-axis ticks and labels for full range
    ax.set_xticks(np.arange(0, n_types, 2))  # Every other tick (0, 2, 4, ...)
    ax.set_xticklabels([f"{u:.1f}" for u in full_u_range[::2]])  # 0.1, 0.3, 0.5, ...
    
    ax.set_xlabel('Interaction strength', fontsize=9)
    ax.set_ylabel('Fraction', fontsize=9)
    ax.tick_params(axis='both', labelsize=7)
    
    # Style to match other phase diagrams
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    plt.tight_layout()
    
    # Save the corrected phase diagram
    output_path = "Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500.svg"
    plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight')
    print(f"✓ Saved corrected full-range phase diagram: {output_path}")
    
    # Also save PNG for viewing
    output_png = output_path.replace('.svg', '.png')
    plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight')
    print(f"✓ Also saved as PNG: {output_png}")
    
    plt.close()
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Full u-range: {full_u_range[0]:.1f} to {full_u_range[-1]:.1f}")
    print(f"   Data available at: {available_u}")
    print(f"   Empty positions: {n_types - len(available_u)} out of {n_types}")

if __name__ == "__main__":
    create_full_range_500_phase_diagram()