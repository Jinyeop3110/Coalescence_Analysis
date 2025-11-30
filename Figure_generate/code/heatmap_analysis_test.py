#!/usr/bin/env python3
"""
Heatmap analysis for test simulation data (48-species, 10 repetitions).
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import warnings
warnings.filterwarnings('ignore')


def normalize(v):
    """Normalize vector"""
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """Vector decomposition metric"""
    u = normalize(u)
    v = normalize(v)
    m = normalize(m)
    
    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    
    e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))
    
    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)
    x3 = np.linalg.norm(m - (e12[0]*u) - (e12[1]*v))
    
    if x1**2 + x2**2 == 0:
        return 0, 0, x3
    
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2))
    
    return convert*x1, convert*x2, x3


def calculate_assymetricity(u, v, k):
    """Calculate asymmetricity measures"""
    x = np.sqrt(np.array(u)**2 + np.array(v)**2)
    y = np.abs(np.abs(np.arctan(np.array(u)/np.array(v))) - np.pi/4) / (np.pi/4)  
    return x, y


def characterize_case(x, y):
    """Classify outcomes"""
    if (x**2 > 0.5) * (y > 0.5):
        return 0  # Dominance
    if (x**2 > 0.5) * (y < 0.5):
        return 1  # Mixing
    if (x**2 < 0.5):
        return 2  # Restructuring


def create_heatmap_with_contours(data1, data2, title, color, output_file, 
                                 bins=30, smoothing_sigma=1.0, contour_levels=8):
    """Create heatmap with contours"""
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='w')
    
    # Create 2D histogram
    H, xedges, yedges = np.histogram2d(data1, data2, bins=bins, range=[[0, 1], [0, 1]])
    
    # Apply Gaussian smoothing
    H_smooth = gaussian_filter(H.T, sigma=smoothing_sigma)
    
    # Create meshgrid for plotting
    X, Y = np.meshgrid(xedges[:-1], yedges[:-1])
    
    # Create colormap
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('custom', ['white', color], N=256)
    
    # Plot heatmap
    im = ax.pcolormesh(X, Y, H_smooth, cmap=cmap, shading='auto')
    
    # Add contour lines
    contours = ax.contour(X, Y, H_smooth, levels=contour_levels, 
                          colors='black', alpha=0.4, linewidths=0.8)
    
    # Add radial guide circles
    theta = np.linspace(0, 2*np.pi, 100)
    for r in [0.25, 0.5, 0.75, 1.0]:
        x_circle = r * np.cos(theta + np.pi/4) / np.sqrt(2)
        y_circle = r * np.sin(theta + np.pi/4) / np.sqrt(2)
        ax.plot(x_circle, y_circle, 'k--', alpha=0.15, linewidth=0.5)
    
    # Add diagonal line
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=1)
    
    # Axes settings
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel('u (contribution from community 1)', fontsize=14)
    ax.set_ylabel('v (contribution from community 2)', fontsize=14)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=16, pad=20)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Density', rotation=270, labelpad=20, fontsize=12)
    
    # Grid
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig


def analyze_test_data():
    """Analyze the test simulation data and create heatmaps"""
    
    print("Starting heatmap analysis for test data...")
    
    # Load test data
    data_path = "Simulation_Data/48species_test/Community_test.json"
    
    if not os.path.exists(data_path):
        print(f"Error: Test data file not found at {data_path}")
        return
    
    with open(data_path, 'r') as f:
        all_results = json.load(f)
    
    # Create output directory
    output_dir = "Figure/VectorDecomp_48species_heatmap_test"
    os.makedirs(output_dir, exist_ok=True)
    
    # Define colors for each interaction strength
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
    color_map = {
        '0.3': colors[0],
        '0.5': colors[1], 
        '0.8': colors[2]
    }
    
    # Process each interaction strength
    u_values = ['0.3', '0.5', '0.8']
    
    print("\nProcessing each interaction strength:")
    
    for u_idx, u in enumerate(u_values):
        print(f"\nProcessing u = {u}")
        
        # Collect all (u, v) coordinates
        all_u_coords = []
        all_v_coords = []
        
        # Classification counters
        dominance_count = 0
        mixing_count = 0
        restructuring_count = 0
        
        # Process each repetition
        for rep_key in all_results[u].keys():
            rep_data = all_results[u][rep_key]
            
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']
            
            # Process each coalescence pair
            for pair_key, c_mix in cc_list.items():
                idx, jdx = map(int, pair_key.split('_'))
                
                c_1 = np.array(sc_list[str(idx)])
                c_2 = np.array(sc_list[str(jdx)])
                c_mix = np.array(c_mix)
                
                # Filter small values
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                try:
                    # Calculate vector decomposition
                    u_coord, v_coord, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                    
                    all_u_coords.append(u_coord)
                    all_v_coords.append(v_coord)
                    
                    # Classify outcome
                    x, y = calculate_assymetricity(u_coord, v_coord, k)
                    class_type = characterize_case(x, y)
                    
                    if class_type == 0:
                        dominance_count += 1
                    elif class_type == 1:
                        mixing_count += 1
                    else:
                        restructuring_count += 1
                        
                except (np.linalg.LinAlgError, ZeroDivisionError):
                    # Skip problematic cases
                    pass
        
        # Convert to numpy arrays
        all_u_coords = np.array(all_u_coords)
        all_v_coords = np.array(all_v_coords)
        
        total_points = len(all_u_coords)
        print(f"  Total data points: {total_points}")
        
        if total_points > 0:
            print(f"  Classification:")
            print(f"    Dominance:     {dominance_count:3d} ({100*dominance_count/total_points:5.1f}%)")
            print(f"    Mixing:        {mixing_count:3d} ({100*mixing_count/total_points:5.1f}%)")
            print(f"    Restructuring: {restructuring_count:3d} ({100*restructuring_count/total_points:5.1f}%)")
            
            # Create heatmap
            output_file = f"{output_dir}/VectorDecomp_test_u{u}_heatmap.png"
            title = f"Coalescence Outcomes (u = {u}, 10 repetitions)"
            
            create_heatmap_with_contours(
                all_u_coords, all_v_coords,
                title=title,
                color=color_map[u],
                output_file=output_file,
                bins=20,
                smoothing_sigma=1.5,
                contour_levels=6
            )
            
            print(f"  Saved heatmap: {output_file}")
        else:
            print(f"  No valid data points found for u = {u}")
    
    # Create comparison plot
    print(f"\nCreating comparison plot...")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor='w')
    
    for idx, u in enumerate(u_values):
        ax = axes[idx]
        
        # Collect data for this intensity
        all_u_coords = []
        all_v_coords = []
        
        for rep_key in all_results[u].keys():
            rep_data = all_results[u][rep_key]
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']
            
            for pair_key, c_mix in cc_list.items():
                i, j = map(int, pair_key.split('_'))
                
                c_1 = np.array(sc_list[str(i)])
                c_2 = np.array(sc_list[str(j)])
                c_mix = np.array(c_mix)
                
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                try:
                    u_coord, v_coord, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                    all_u_coords.append(u_coord)
                    all_v_coords.append(v_coord)
                except (np.linalg.LinAlgError, ZeroDivisionError):
                    pass
        
        if len(all_u_coords) > 0:
            # Create heatmap
            H, xedges, yedges = np.histogram2d(all_u_coords, all_v_coords, 
                                               bins=20, range=[[0, 1], [0, 1]])
            H_smooth = gaussian_filter(H.T, sigma=1.5)
            
            from matplotlib.colors import LinearSegmentedColormap
            cmap = LinearSegmentedColormap.from_list('custom', ['white', color_map[u]], N=256)
            
            im = ax.pcolormesh(xedges[:-1], yedges[:-1], H_smooth, 
                               cmap=cmap, shading='auto')
            
            contours = ax.contour(xedges[:-1], yedges[:-1], H_smooth, 
                                 levels=6, colors='black', alpha=0.4, linewidths=0.8)
            
            # Add diagonal
            ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, linewidth=1)
        else:
            # If no data, just show empty plot
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', fontsize=16)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title(f'u = {u}', fontsize=16)
        ax.set_xlabel('u', fontsize=14)
        if idx == 0:
            ax.set_ylabel('v', fontsize=14)
        
        ax.grid(True, alpha=0.2)
    
    plt.suptitle('Coalescence Outcomes Across Interaction Strengths (Test Data)', 
                 fontsize=18, y=1.02)
    
    comparison_file = f"{output_dir}/VectorDecomp_test_comparison_heatmap.png"
    plt.tight_layout()
    plt.savefig(comparison_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nComparison plot saved: {comparison_file}")
    print(f"\nAnalysis complete! All figures saved to: {output_dir}")


if __name__ == "__main__":
    analyze_test_data()