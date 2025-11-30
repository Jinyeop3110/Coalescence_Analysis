#!/usr/bin/env python3
"""
Create two-panel figure with shared pH axis:
- Top panel: Clean pH histogram 
- Bottom panel: ASV positions at their final pH values
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Set Arial font for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

def load_ph_change_data():
    """Load pH change data after 15 hours"""
    file_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/230623_pH.xlsx'
    
    try:
        df = pd.read_excel(file_path, sheet_name='after 15h', header=None)
        
        # Find data start
        data_start = None
        for i in range(len(df)):
            if df.iloc[i, 0] == 'A':
                data_start = i
                break
        
        if data_start is None:
            return pd.DataFrame()
        
        all_data = []
        
        for row_idx, row_label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            if data_start + row_idx >= len(df):
                break
                
            row_data = df.iloc[data_start + row_idx, 1:13]
            
            for col_idx, ph_change in enumerate(row_data):
                if pd.notna(ph_change) and isinstance(ph_change, (int, float)):
                    all_data.append({
                        'Well': f"{row_label}{col_idx+1}",
                        'pH_final': float(ph_change) / 10.0,
                        'Species': f"{row_label}{col_idx+1}"
                    })
        
        return pd.DataFrame(all_data)
        
    except Exception as e:
        print(f"Error loading pH change data: {e}")
        return pd.DataFrame()

def create_two_panel_ph_figure(df_change, output_dir):
    """Create two-panel figure with histogram on top and ASV positions below"""
    
    # Create figure with two subplots sharing x-axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 2), height_ratios=[3, 1], 
                                   sharex=True, gridspec_kw={'hspace': 0.1})
    
    # Define pH range and bins
    ph_range = (2.5, 8.5)
    bins = np.arange(2.5, 8.5, 0.5)
    
    # TOP PANEL: Clean histogram
    n, bin_edges, patches = ax1.hist(df_change['pH_final'], 
                                    bins=bins,
                                    edgecolor='none', 
                                    linewidth=0,
                                    alpha=0.8,
                                    color='gray')
    
    # Style top panel
    ax1.set_ylabel('Number of Species', fontsize=9)
    ax1.tick_params(labelsize=7)
    ax1.set_xlim(ph_range)
    
    # Add initial pH reference line
    ax1.axvline(x=6.5, color='black', linestyle='-', linewidth=1.0, alpha=0.8)
    ax1.text(6.5, ax1.get_ylim()[1] * 0.95, 'Initial pH', ha='center', va='bottom', 
            fontsize=8, color='black')
    
    # Add acidifier and alkalizer labels
    y_pos = ax1.get_ylim()[1] * 0.8
    ax1.text(5.8, y_pos, '← Acidifiers', ha='right', va='center', 
            fontsize=8, color='red', fontweight='bold')
    ax1.text(7.2, y_pos, 'Alkalizers →', ha='left', va='center', 
            fontsize=8, color='blue', fontweight='bold')
    
    # Remove x-axis labels from top panel
    ax1.tick_params(labelbottom=False)
    
    # BOTTOM PANEL: ASV positions
    # ASV data with exact pH values from the data
    asv_wells = {
        'ASV12': 'B5',  # pH 3.2
        'ASV3': 'D7',   # pH 3.8  
        'ASV8': 'A1',   # pH 4.2
        'ASV9': 'B1',   # pH 5.5
        'ASV11': 'A4'   # pH 6.8
    }
    
    asv_data = []
    for asv_name, well in asv_wells.items():
        well_data = df_change[df_change['Well'] == well]
        if not well_data.empty:
            ph_value = well_data['pH_final'].iloc[0]
            asv_data.append({
                'name': asv_name,
                'ph': ph_value,
                'well': well
            })
    
    # Define colors for each ASV
    asv_colors = {
        'ASV12': {'color': 'orange', 'bgcolor': 'peachpuff'},
        'ASV3': {'color': 'red', 'bgcolor': 'yellow'},
        'ASV8': {'color': 'green', 'bgcolor': 'lightgreen'},
        'ASV9': {'color': 'purple', 'bgcolor': 'plum'},
        'ASV11': {'color': 'blue', 'bgcolor': 'lightblue'}
    }
    
    # Plot ASV positions as solid colored circles
    y_pos = 0.5  # Middle of the bottom panel
    circle_size = 40  # Further reduced size of scatter points
    
    for asv in asv_data:
        color_info = asv_colors[asv['name']]
        
        # Plot solid colored circle at pH position (no edges)
        ax2.scatter(asv['ph'], y_pos, s=circle_size, 
                   c=color_info['color'], alpha=0.8, zorder=3)
    
    # Add ASV labels with smart positioning to avoid overlaps
    # Sort ASVs by pH for positioning
    asv_data.sort(key=lambda x: x['ph'])
    
    label_positions = []
    min_separation = 0.8
    
    for i, asv in enumerate(asv_data):
        # Try to place label at original pH position
        best_x = asv['ph']
        
        # Check for overlaps and adjust if needed
        for prev_pos in label_positions:
            if abs(best_x - prev_pos) < min_separation:
                # Shift to avoid overlap
                if best_x < prev_pos:
                    best_x = prev_pos - min_separation
                else:
                    best_x = prev_pos + min_separation
        
        # Ensure within plot bounds
        best_x = max(ph_range[0] + 0.3, min(ph_range[1] - 0.3, best_x))
        label_positions.append(best_x)
        
        # Alternate label positions above and below
        label_y = 0.8 if i % 2 == 0 else 0.2
        
        # Add label
        ax2.text(best_x, label_y, asv['name'], ha='center', va='center',
                fontsize=7, fontweight='bold', 
                bbox=dict(boxstyle='round,pad=0.15', 
                         facecolor='lightgray',
                         edgecolor='gray',
                         alpha=0.8, linewidth=0.8))
        
        # Add connection line if label is moved
        if abs(best_x - asv['ph']) > 0.1:
            ax2.plot([asv['ph'], best_x], [y_pos, label_y], 
                    color=asv_colors[asv['name']]['color'], 
                    linewidth=1, alpha=0.6, linestyle='-')
    
    # Style bottom panel
    ax2.set_xlim(ph_range)
    ax2.set_ylim(0, 1)
    ax2.set_ylabel('ASV', fontsize=8)
    ax2.tick_params(labelsize=7)
    ax2.set_xticks([3, 4, 5, 6, 7, 8])
    ax2.set_yticks([])  # Remove y-axis ticks for cleaner look
    
    # Add initial pH reference line to bottom panel
    ax2.axvline(x=6.5, color='black', linestyle='-', linewidth=1.0, alpha=0.8)
    
    # Remove spines for cleaner look
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    # Ensure consistent styling
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # Save figure
    fig.savefig(f"{output_dir}/two_panel_ph_asv_figure.svg", bbox_inches='tight', dpi=300)
    fig.savefig(f"{output_dir}/two_panel_ph_asv_figure.png", bbox_inches='tight', dpi=300)
    
    return fig

def main():
    """Create two-panel pH figure"""
    
    # Create output directory
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Creating two-panel pH figure...")
    
    # Load data
    df_change = load_ph_change_data()
    
    if df_change.empty:
        print("Error: No pH change data found!")
        return
    
    # Create figure
    fig = create_two_panel_ph_figure(df_change, output_dir)
    print("✓ Created two_panel_ph_asv_figure.svg/png")
    
    print("✓ Two-panel figure complete!")

if __name__ == "__main__":
    main()