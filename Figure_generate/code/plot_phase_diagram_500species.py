#!/usr/bin/env python
"""
plot_phase_diagram_500species.py

Purpose: Generate phase diagram for 500-species simulation data across full u-range
Key features:
- Creates phase diagram for 500-species coalescence simulation
- Shows distribution of dominance, mixing, and restructuring outcomes across u-values 0.1 to 1.2
- Uses vector decomposition to classify simulation coalescence events
- Processes data with u-values as columns

Outputs:
- Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500_full_range.svg
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path


def classify_vector_decomposition(a, b, c):
    """
    Classify coalescence outcome based on vector decomposition coefficients.
    
    Args:
        a, b: Coefficients for parent contributions
        c: Residual/restructuring magnitude
    
    Returns:
        0: Dominance, 1: Mixing, 2: Restructuring
    """
    # Normalize to handle different scales
    total = a + b + c
    if total > 0:
        a_norm = a / total
        b_norm = b / total
        c_norm = c / total
    else:
        return 2  # Default to restructuring
    
    # Classification rules based on vector decomposition
    if c_norm > 0.5:
        return 2  # Restructuring
    elif abs(a_norm - b_norm) > 0.3:
        return 0  # Dominance (one parent dominates)
    else:
        return 1  # Mixing


def create_500species_phase_diagram(data1, data2, data3, u_values, 
                                   output_filename="Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500_full_range.svg"):
    """
    Create phase diagram for 500-species simulation data.
    
    Args:
        data1, data2, data3: DataFrames with u-values as columns
        u_values: List of u-values
        output_filename: Output file path
    """
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Colors for each outcome type
    colors = ['#FF6B6B', '#9B59B6', '#2ECC71']  # Red, Purple, Green
    type_names = ['Dominance', 'Mixing', 'Restructuring']
    
    # Initialize data for stacked bar plot
    dominance_fractions = []
    mixing_fractions = []
    restructuring_fractions = []
    
    x_positions = []
    x_labels = []
    
    print(f"Processing {len(u_values)} u-values...")
    
    for i, u_val in enumerate(u_values):
        col_name = f"u_{u_val}"
        
        if col_name in data1.columns:
            # Get data for this u-value
            a_values = data1[col_name].dropna().values
            b_values = data2[col_name].dropna().values
            c_values = data3[col_name].dropna().values
            
            # Ensure all arrays have the same length
            min_length = min(len(a_values), len(b_values), len(c_values))
            if min_length == 0:
                print(f"  Warning: No data for u={u_val}")
                continue
                
            a_values = a_values[:min_length]
            b_values = b_values[:min_length]
            c_values = c_values[:min_length]
            
            # Classify each data point
            classifications = []
            for j in range(min_length):
                cls = classify_vector_decomposition(a_values[j], b_values[j], c_values[j])
                classifications.append(cls)
            
            # Count each classification type
            classifications = np.array(classifications)
            n_dominance = np.sum(classifications == 0)
            n_mixing = np.sum(classifications == 1)
            n_restructuring = np.sum(classifications == 2)
            total = n_dominance + n_mixing + n_restructuring
            
            if total > 0:
                # Calculate fractions
                dominance_frac = n_dominance / total
                mixing_frac = n_mixing / total
                restructuring_frac = n_restructuring / total
                
                dominance_fractions.append(dominance_frac)
                mixing_fractions.append(mixing_frac)
                restructuring_fractions.append(restructuring_frac)
                
                x_positions.append(i)
                x_labels.append(f"{u_val:.1f}")
                
                print(f"  u={u_val:.1f}: {n_dominance}D + {n_mixing}M + {n_restructuring}R = {total} total")
                print(f"    → {dominance_frac:.1%} dominance, {mixing_frac:.1%} mixing, {restructuring_frac:.1%} restructuring")
    
    if len(x_positions) == 0:
        print("Error: No valid data found!")
        return
    
    # Create stacked bar plot
    width = 0.6
    
    # Create the bars
    p1 = ax.bar(x_positions, dominance_fractions, width, 
                color=colors[0], alpha=0.8, label=type_names[0])
    
    p2 = ax.bar(x_positions, mixing_fractions, width, 
                bottom=dominance_fractions, color=colors[1], alpha=0.8, label=type_names[1])
    
    p3 = ax.bar(x_positions, restructuring_fractions, width, 
                bottom=np.array(dominance_fractions) + np.array(mixing_fractions), 
                color=colors[2], alpha=0.8, label=type_names[2])
    
    # Customize the plot
    ax.set_xlabel('Interaction Strength (u)', fontsize=14)
    ax.set_ylabel('Fraction of Coalescence Events', fontsize=14)
    ax.set_title('500-Species Coalescence Phase Diagram\n(Full Interaction Strength Range)', fontsize=16, pad=20)
    
    # Set x-axis
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, rotation=45)
    ax.set_xlim(-0.5, len(x_positions) - 0.5)
    
    # Set y-axis to 0-1
    ax.set_ylim(0, 1)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.set_yticklabels([f"{y:.1f}" for y in np.arange(0, 1.1, 0.1)])
    
    # Add legend
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    
    # Add grid
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)
    
    # Improve layout
    plt.tight_layout()
    
    # Save the figure
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save in multiple formats
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', format='svg')
    plt.savefig(output_filename.replace('.svg', '.png'), dpi=300, bbox_inches='tight', format='png')
    
    plt.show()
    
    print(f"✓ Phase diagram saved to: {output_filename}")
    print(f"✓ PNG version saved to: {output_filename.replace('.svg', '.png')}")


def main():
    """Main function to generate 500-species phase diagram."""
    
    print("Generating phase diagram for 500-species simulation data...")
    print("🎨 Using colormap: Red (Dominance), Purple (Mixing), Green (Restructuring)")
    
    # Path to the 500-species data
    file_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full/Similarity.xlsx"
    
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        return
    
    print(f"Reading data from: {file_path}")
    
    # Read the Excel data
    try:
        data1 = pd.read_excel(file_path, sheet_name=0)  # Parent 1 coefficients
        data2 = pd.read_excel(file_path, sheet_name=1)  # Parent 2 coefficients  
        data3 = pd.read_excel(file_path, sheet_name=2)  # Residual magnitudes
        
        print(f"Data shapes: {data1.shape}, {data2.shape}, {data3.shape}")
        print(f"Columns: {list(data1.columns)}")
        
        # Extract u-values from column names
        u_values = []
        for col in data1.columns:
            if col.startswith('u_'):
                u_val = float(col.split('_')[1])
                u_values.append(u_val)
        
        u_values = sorted(u_values)
        print(f"Found u-values: {u_values}")
        
        # Create the phase diagram
        create_500species_phase_diagram(data1, data2, data3, u_values)
        
        print(f"\n🎉 500-species phase diagram generation complete!")
        
    except Exception as e:
        print(f"Error processing data: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()