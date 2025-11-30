#!/usr/bin/env python3
"""
Create minimal academic-style explanatory figure for ASV annotations
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Set Arial font for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

def create_asv_explanation_figure(output_dir):
    """Create histogram-style explanatory figure with ASV annotations"""
    
    # Create figure matching main histogram proportions
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Create a simplified histogram representation
    ph_values = [3.2, 3.8, 4.2, 5.5, 6.8]  # ASV pH values
    heights = [1, 1, 1, 1, 1]  # Equal height bars for visualization
    
    # Create bars at ASV positions
    bars = ax.bar(ph_values, heights, width=0.3, alpha=0.3, color='lightgray', 
                  edgecolor='gray', linewidth=0.5)
    
    # ASV data matching the main figure
    asvs = [
        {'label': 'ASV12', 'ph': 3.2, 'color': 'orange', 'bgcolor': 'peachpuff', 'type': 'Strong Acidifier'},
        {'label': 'ASV3', 'ph': 3.8, 'color': 'red', 'bgcolor': 'yellow', 'type': 'Acidifier'},
        {'label': 'ASV8', 'ph': 4.2, 'color': 'green', 'bgcolor': 'lightgreen', 'type': 'Moderate Acidifier'},
        {'label': 'ASV9', 'ph': 5.5, 'color': 'purple', 'bgcolor': 'plum', 'type': 'Weak Acidifier'},
        {'label': 'ASV11', 'ph': 6.8, 'color': 'blue', 'bgcolor': 'lightblue', 'type': 'Alkalizer'}
    ]
    
    # Smart positioning to avoid overlaps - similar to main plot algorithm
    positions = []
    min_separation = 0.8
    base_depths = [0.35, 0.55, 0.75, 0.95, 1.15]
    
    # Pre-calculate optimal positions
    optimal_positions = []
    
    for i, asv in enumerate(asvs):
        best_x = asv['ph']
        min_cost = float('inf')
        
        # Try positions around the original pH value
        for offset in np.arange(-0.8, 0.9, 0.1):
            test_x = asv['ph'] + offset
            if test_x < 2.5 or test_x > 7.5:
                continue
                
            distance_cost = abs(offset) * 2
            overlap_cost = 0
            
            for prev_pos in optimal_positions:
                if abs(test_x - prev_pos['x']) < min_separation:
                    overlap_cost += 10
            
            total_cost = distance_cost + overlap_cost
            if total_cost < min_cost:
                min_cost = total_cost
                best_x = test_x
        
        optimal_positions.append({'x': best_x, 'asv': asv, 'idx': i})
    
    # Create annotations with arrows
    for i, opt_pos in enumerate(optimal_positions):
        asv = opt_pos['asv']
        adjusted_ph = opt_pos['x']
        depth_idx = min(i, len(base_depths) - 1)
        
        # Create annotation with arrow pointing to actual pH position
        ax.annotate(asv['label'], 
                   xy=(asv['ph'], 0.1), 
                   xytext=(adjusted_ph, base_depths[depth_idx]),
                   ha='center', fontsize=9, fontweight='bold',
                   arrowprops=dict(arrowstyle='->', color=asv['color'], lw=1.5, alpha=0.8),
                   bbox=dict(boxstyle='round,pad=0.2', facecolor=asv['bgcolor'], 
                            alpha=0.8, edgecolor=asv['color'], linewidth=1))
        
        # Add pH value below annotation
        ax.text(adjusted_ph, base_depths[depth_idx] - 0.12, f'pH {asv["ph"]}', 
                ha='center', va='center', fontsize=8, color='black')
    
    # Add initial pH reference line
    ax.axvline(x=6.5, color='black', linestyle='-', linewidth=2.5, alpha=0.8)
    ax.text(6.5, 1.4, 'Initial pH\n(6.5)', ha='center', va='bottom', 
            fontsize=9, bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8))
    
    # Add acidifier and alkalizer labels
    ax.text(4.5, 1.3, '← Acidifiers', ha='right', va='center', 
            fontsize=10, color='red', fontweight='bold')
    ax.text(6.9, 1.3, 'Alkalizers →', ha='left', va='center', 
            fontsize=10, color='blue', fontweight='bold')
    
    # Set axis properties
    ax.set_xlim(2.5, 7.5)
    ax.set_ylim(0, 1.6)
    ax.set_xlabel('Final pH After 15 Hours', fontsize=10)
    ax.set_ylabel('ASV Positions', fontsize=10)
    ax.tick_params(labelsize=8)
    ax.set_xticks([3, 4, 5, 6, 7])
    
    # Remove y-axis ticks since this is just for annotation visualization
    ax.set_yticks([])
    
    # Add title
    ax.set_title('ASV pH Response Annotations', fontsize=11, fontweight='bold', pad=15)
    
    plt.tight_layout()
    
    # Save figure
    fig.savefig(f"{output_dir}/asv_explanation.svg", bbox_inches='tight', dpi=300)
    fig.savefig(f"{output_dir}/asv_explanation.png", bbox_inches='tight', dpi=300)
    
    return fig

def create_asv_legend_table(output_dir):
    """Create dot-ASV-phylogeny legend"""
    
    fig, ax = plt.subplots(figsize=(4, 2))
    
    # ASV data with genus-level identification - acidifiers first, then alkalizers
    asv_data = [
        {
            'name': 'ASV3',
            'color': 'red',
            'genus': 'Klebsiella'
        },
        {
            'name': 'ASV8', 
            'color': 'green',
            'genus': 'Lactococcus'
        },
        {
            'name': 'ASV12',
            'color': 'orange',
            'genus': 'Chryseobacter'
        },
        {
            'name': 'ASV9',
            'color': 'purple', 
            'genus': 'Pedobacter'
        },
        {
            'name': 'ASV11',
            'color': 'blue',
            'genus': 'Leuconostoc'
        }
    ]
    
    # Layout parameters
    y_positions = [0.85, 0.68, 0.51, 0.34, 0.17]  # Vertical positions for each ASV
    dot_x = 0.1  # X position for dots
    label_x = 0.2  # X position for combined ASV + genus labels
    
    # Draw each ASV entry
    for i, asv in enumerate(asv_data):
        y_pos = y_positions[i]
        
        # Draw colored dot
        ax.scatter(dot_x, y_pos, s=80, c=asv['color'], alpha=0.8, zorder=3)
        
        # Add combined ASV + genus label
        combined_label = f"{asv['name']} ({asv['genus']})"
        ax.text(label_x, y_pos, combined_label, ha='left', va='center',
                fontsize=11, fontweight='bold')
    
    # Set plot limits and styling
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Add column headers (moved up since no title)
    ax.text(dot_x, 0.95, '●', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(label_x, 0.95, 'ASV (Genus)', ha='left', va='center', fontsize=11, fontweight='bold')
    
    # Add separator line
    ax.plot([0.02, 0.98], [0.92, 0.92], color='black', linewidth=1, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    fig.savefig(f"{output_dir}/asv_summary_table.svg", bbox_inches='tight', dpi=300)
    fig.savefig(f"{output_dir}/asv_summary_table.png", bbox_inches='tight', dpi=300)
    
    return fig

def main():
    """Create ASV explanation figures"""
    
    # Create output directory
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Creating ASV explanation figures...")
    
    # Create main explanation figure
    fig1 = create_asv_explanation_figure(output_dir)
    print("✓ Created asv_explanation.svg/png")
    
    # Create summary table
    fig2 = create_asv_legend_table(output_dir)
    print("✓ Created asv_summary_table.svg/png")
    
    print("✓ ASV explanation figures complete!")

if __name__ == "__main__":
    main()