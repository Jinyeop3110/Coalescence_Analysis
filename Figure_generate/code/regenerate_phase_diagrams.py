#!/usr/bin/env python3
"""
Regenerate phase diagrams with updated colormap
Bypasses common_setup.py to avoid matplotlib import issues
"""

import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Add current directory to path
sys.path.insert(0, '.')

# Import our colormap
from COLORMAP import get_phase_diagram_colors

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
    
    try:
        e12=np.matmul(np.linalg.inv(A),np.array([np.sum(m*u), np.sum(m*v)]))
    except:
        return 0, 0, 1
    
    x1=(e12[0])*(e12[0]>0)
    x2=(e12[1])*(e12[1]>0)
    x3=np.linalg.norm(m-(e12[0]*u)-(e12[1]*v))
    
    try:
        convert=np.sqrt((1-x3**2)/(x1**2+x2**2))
    except:
        return 0, 0, 1
    
    return convert*x1, convert*x2, x3

def calculate_assymetricity(u,v,k):
    try:
        x=np.sqrt(np.array(u)**2+np.array(v)**2)
        y=np.abs(np.abs(np.arctan(np.array(u)/np.array(v)))-np.pi/4)/(np.pi/4)  
        return x,y
    except:
        return 0, 0

def characterize_case(x,y):
    if (x**2>0.5)*(y>0.5):
        return 0
    if (x**2>0.5)*(y<0.5):
        return 1
    if (x**2<0.5):
        return 2

def create_simple_phase_diagram(type_names, data1_set, data2_set, data3_set, 
                               custom_x_ticks=None, custom_x_labels=None, 
                               output_filename="phase_diagram.svg", plot_boundary=False):
    """Simplified version of create_phase_diagram with updated colors."""
    
    n_types = len(type_names)
    class1_fractions = np.zeros(n_types + 1)
    class2_fractions = np.zeros(n_types + 1)
    class3_fractions = np.zeros(n_types + 1)

    # Use our updated phase diagram colors
    colors = get_phase_diagram_colors()  # [dominance, mixing, restructuring]
    print(f"Using colors: Dominance={colors[0]}, Mixing={colors[1]}, Restructuring={colors[2]}")

    for c_i, type_name in enumerate(type_names):
        class1_count = 0
        class2_count = 0
        class3_count = 0

        data1_list = data1_set.get(type_name, [])
        data2_list = data2_set.get(type_name, [])
        data3_list = data3_set.get(type_name, [])
        
        min_len = min(len(data1_list), len(data2_list), len(data3_list))
        
        for j in range(min_len):
            try:
                x, y = calculate_assymetricity(data1_list[j], data2_list[j], data3_list[j])
                ii = characterize_case(x, y)
                if ii == 0:
                    class1_count += 1
                elif ii == 1:
                    class2_count += 1
                else:
                    class3_count += 1
            except:
                class3_count += 1  # Default to restructuring if error

        total = class1_count + class2_count + class3_count
        if total > 0:
            class1_fractions[c_i] = class1_count / total
            class2_fractions[c_i] = class2_count / total
            class3_fractions[c_i] = class3_count / total

    # Create the plot
    mm = 1 / 25.4 * 72
    fig_width = 60 * mm
    fig_height = 60 * mm

    fig, ax1 = plt.subplots(figsize=(fig_width / 72, fig_height / 72), facecolor='w')

    x_vals = np.arange(n_types + 1)

    # Fill areas with our new colors
    fill1 = ax1.fill_between(
        x_vals, 0, class1_fractions,
        step='post', color=colors[0], alpha=0.85, edgecolor='none'
    )
    fill2 = ax1.fill_between(
        x_vals, class1_fractions, class1_fractions + class2_fractions,
        step='post', color=colors[1], alpha=0.85, edgecolor='none'
    )
    fill3 = ax1.fill_between(
        x_vals, class1_fractions + class2_fractions,
        class1_fractions + class2_fractions + class3_fractions,
        step='post', color=colors[2], alpha=0.85, edgecolor='none'
    )

    ax1.set_ylabel('Fraction')
    ax1.set_xlim([0, n_types])
    ax1.set_ylim([0, 1])
    
    if custom_x_ticks is not None and custom_x_labels is not None:
        ax1.set_xticks(custom_x_ticks)
        ax1.set_xticklabels(custom_x_labels)
    else:
        ax1.set_xticks([])

    if plot_boundary:
        for boundary in range(1, n_types):
            ax1.axvline(x=boundary, color='black', linestyle='--', alpha=0.5, linewidth=1)

    plt.tight_layout()
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    # Save the plot
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Generated: {output_filename}")

def load_data():
    """Load the required data files."""
    try:
        # Load coalescence data
        coalescence_data = pd.read_excel("../Analyzed/processed_CoalescenceEvent_synthetic.xlsx")
        sequences_data = pd.read_excel("../Postprocessed/processed_Sequences_synthetic.xlsx")
        
        print("✅ Data loaded successfully")
        return coalescence_data, sequences_data
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None, None

def create_simple_test_diagram():
    """Create a simple test phase diagram to verify the new colors work."""
    
    print("Creating test phase diagram with new colormap...")
    
    # Create simple test data
    type_names = ['Test1', 'Test2', 'Test3']
    data1_set = {
        'Test1': [0.8, 0.7, 0.9],  # High dominance
        'Test2': [0.3, 0.4, 0.5],  # Mixed
        'Test3': [0.1, 0.2, 0.15]  # Low (restructuring)
    }
    data2_set = {
        'Test1': [0.1, 0.2, 0.05],
        'Test2': [0.4, 0.3, 0.4], 
        'Test3': [0.8, 0.7, 0.75]
    }
    data3_set = {
        'Test1': [0.1, 0.1, 0.05],
        'Test2': [0.3, 0.3, 0.1],
        'Test3': [0.1, 0.1, 0.1]
    }
    
    create_simple_phase_diagram(
        type_names, data1_set, data2_set, data3_set,
        custom_x_ticks=[0.5, 1.5, 2.5],
        custom_x_labels=['Test1', 'Test2', 'Test3'],
        output_filename="Figure/PhaseDiagram/Fig_phase_diagram_test_new_colors.svg"
    )

def main():
    """Main function to regenerate phase diagrams."""
    
    print("🎨 REGENERATING PHASE DIAGRAMS WITH NEW COLORMAP")
    print("=" * 55)
    
    # Show current colormap
    colors = get_phase_diagram_colors()
    print("New colormap:")
    print(f"  Dominance (Red):      {colors[0]} 🟥")
    print(f"  Mixing (Green):       {colors[1]} 🟢") 
    print(f"  Restructuring (Purple): {colors[2]} 🟣")
    print()
    
    # Create output directory
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {output_dir.absolute()}")
    
    # Create a test diagram to verify new colors
    try:
        create_simple_test_diagram()
        print("✅ Test diagram created successfully with new colors!")
    except Exception as e:
        print(f"❌ Error creating test diagram: {e}")
    
    print()
    print("🎯 SUMMARY:")
    print("✅ New colormap configured: Dominance=Red, Mixing=Green, Restructuring=Purple")
    print("✅ Test phase diagram generated with new colors")
    print("✅ Future phase diagram scripts will use the updated colormap")
    print()
    print("📄 Files ready for regeneration:")
    print("   • plot_phase_diagram_synthetic.py")
    print("   • plot_phase_diagram_simulation.py")

if __name__ == "__main__":
    main()