#!/usr/bin/env python3
"""
Create simple plots using basic matplotlib functionality
"""

import json
import numpy as np
import os

# Try importing matplotlib with fallback
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    from scipy.ndimage import gaussian_filter
    PLOTTING_AVAILABLE = True
    print("Matplotlib loaded successfully!")
except ImportError as e:
    print(f"Matplotlib import failed: {e}")
    PLOTTING_AVAILABLE = False


def create_simple_heatmap(u_coords, v_coords, title, color, output_file, bins=30):
    """Create a simple heatmap plot"""
    
    if not PLOTTING_AVAILABLE:
        print(f"Cannot create plot {output_file} - matplotlib not available")
        return False
    
    try:
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        
        # Create 2D histogram
        H, xedges, yedges = np.histogram2d(u_coords, v_coords, bins=bins, range=[[0, 1], [0, 1]])
        
        # Simple plot without fancy smoothing
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        im = ax.imshow(H.T, extent=extent, origin='lower', cmap='Blues', aspect='equal')
        
        # Add contour lines
        X, Y = np.meshgrid(xedges[:-1], yedges[:-1])
        ax.contour(X, Y, H.T, levels=5, colors='black', alpha=0.4, linewidths=0.8)
        
        # Formatting
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel('u (contribution from community 1)', fontsize=12)
        ax.set_ylabel('v (contribution from community 2)', fontsize=12)
        ax.set_title(title, fontsize=14)
        
        # Add diagonal reference line
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=1)
        
        # Add colorbar
        plt.colorbar(im, ax=ax, label='Density')
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Successfully saved: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error creating plot {output_file}: {e}")
        return False


def create_comparison_plot(processed_data, output_file):
    """Create comparison plot across all interaction strengths"""
    
    if not PLOTTING_AVAILABLE:
        print(f"Cannot create comparison plot - matplotlib not available")
        return False
    
    try:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        u_values = ['0.3', '0.5', '0.8']
        colors = ['blue', 'orange', 'red']
        
        for idx, u in enumerate(u_values):
            ax = axes[idx]
            data = processed_data[u]
            
            u_coords = np.array(data['u_coords'])
            v_coords = np.array(data['v_coords'])
            
            if len(u_coords) > 0:
                # Create simple scatter plot
                ax.scatter(u_coords, v_coords, alpha=0.6, s=20, c=colors[idx])
                
                # Add diagonal
                ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=1)
                
                # Formatting
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.set_aspect('equal')
                ax.set_title(f'u = {u}', fontsize=14)
                ax.set_xlabel('u', fontsize=12)
                if idx == 0:
                    ax.set_ylabel('v', fontsize=12)
                
                ax.grid(True, alpha=0.3)
        
        plt.suptitle('Coalescence Outcomes Across Interaction Strengths', fontsize=16)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Successfully saved comparison plot: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error creating comparison plot: {e}")
        return False


def main():
    """Create plots from processed data"""
    
    # Load processed data
    data_file = "Analysis_Results/processed_test_data.json"
    
    if not os.path.exists(data_file):
        print(f"Error: Processed data file not found at {data_file}")
        return
    
    with open(data_file, 'r') as f:
        processed_data = json.load(f)
    
    # Create output directory
    output_dir = "Figure/VectorDecomp_48species_plots"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Creating plots in: {output_dir}")
    
    # Create individual plots for each interaction strength
    u_values = ['0.3', '0.5', '0.8']
    colors = ['blue', 'orange', 'red']
    
    plots_created = 0
    
    for u, color in zip(u_values, colors):
        data = processed_data[u]
        u_coords = np.array(data['u_coords'])
        v_coords = np.array(data['v_coords'])
        
        if len(u_coords) > 0:
            title = f"Coalescence Outcomes (u = {u}, 10 repetitions)"
            output_file = f"{output_dir}/heatmap_u{u}.png"
            
            success = create_simple_heatmap(u_coords, v_coords, title, color, output_file)
            if success:
                plots_created += 1
    
    # Create comparison plot
    comparison_file = f"{output_dir}/comparison_plot.png"
    success = create_comparison_plot(processed_data, comparison_file)
    if success:
        plots_created += 1
    
    # Summary
    print(f"\n=== PLOT CREATION SUMMARY ===")
    print(f"Plots successfully created: {plots_created}")
    print(f"Output directory: {output_dir}")
    
    if plots_created > 0:
        print(f"\nGenerated files:")
        for f in os.listdir(output_dir):
            if f.endswith('.png'):
                print(f"  - {f}")
    else:
        print("No plots were created due to matplotlib issues.")
        print("Data is available in JSON format for plotting with other tools.")


if __name__ == "__main__":
    main()