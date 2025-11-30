#!/usr/bin/env python3
"""
Vector decomposition analysis with heatmap visualization for 48-species 100-repetition simulations.

This script:
1. Loads simulation data from 100 repetitions
2. Performs vector decomposition analysis
3. Creates heatmaps with contours instead of scatter plots
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import common functions
from common_setup import *
from COLORMAP import get_medium_colors


def create_heatmap_with_contours(data1, data2, title, color, output_file, 
                                 bins=50, smoothing_sigma=1.5, contour_levels=10):
    """
    Create a 2D heatmap with contour lines showing the distribution of vector decomposition results.
    
    Parameters:
    -----------
    data1, data2 : array-like
        The u and v coordinates from vector decomposition
    title : str
        Title for the plot
    color : str or tuple
        Color for the heatmap
    output_file : str
        Path to save the figure
    bins : int
        Number of bins for the 2D histogram
    smoothing_sigma : float
        Gaussian smoothing parameter for the heatmap
    contour_levels : int
        Number of contour levels to draw
    """
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(6, 6), facecolor='w')
    
    # Create 2D histogram
    H, xedges, yedges = np.histogram2d(data1, data2, bins=bins, range=[[0, 1], [0, 1]])
    
    # Apply Gaussian smoothing
    H_smooth = gaussian_filter(H.T, sigma=smoothing_sigma)
    
    # Create meshgrid for plotting
    X, Y = np.meshgrid(xedges[:-1], yedges[:-1])
    
    # Create custom colormap based on the provided color
    if isinstance(color, str):
        cmap = plt.cm.get_cmap('Blues')
        cmap = plt.cm.colors.LinearSegmentedColormap.from_list(
            'custom', ['white', color], N=256)
    else:
        # If color is RGB tuple, create colormap from white to that color
        cmap = plt.cm.colors.LinearSegmentedColormap.from_list(
            'custom', ['white', color], N=256)
    
    # Plot heatmap
    im = ax.pcolormesh(X, Y, H_smooth, cmap=cmap, shading='auto')
    
    # Add contour lines
    contours = ax.contour(X, Y, H_smooth, levels=contour_levels, 
                          colors='black', alpha=0.3, linewidths=0.5)
    
    # Add radial guide circles (optional, similar to original plots)
    theta = np.linspace(0, 2*np.pi, 100)
    for r in [0.25, 0.5, 0.75, 1.0]:
        x_circle = r * np.cos(theta + np.pi/4) / np.sqrt(2)
        y_circle = r * np.sin(theta + np.pi/4) / np.sqrt(2)
        ax.plot(x_circle, y_circle, 'k--', alpha=0.1, linewidth=0.5)
    
    # Add diagonal line
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.2, linewidth=1)
    
    # Axes settings
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel('u (contribution from community 1)', fontsize=12)
    ax.set_ylabel('v (contribution from community 2)', fontsize=12)
    ax.set_aspect('equal')
    ax.set_title(title, fontsize=14, pad=10)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Density', rotation=270, labelpad=15)
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Grid
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig


def analyze_48species_100reps_heatmap():
    """Main analysis function for 100 repetition data with heatmap visualization."""
    
    print("Starting vector decomposition analysis for 48-species 100-repetition data...")
    
    # Load simulation data
    data_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Simulation_Data/48species_100reps/Community_100reps.json"
    
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        print("Please run run_48species_100reps_simulation.py first.")
        return
    
    print(f"Loading data from: {data_path}")
    with open(data_path, 'r') as f:
        all_results = json.load(f)
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_48species_heatmap"
    os.makedirs(output_dir, exist_ok=True)
    
    # Color scheme
    colors = get_medium_colors()  # [LN, MN, HN] colors
    color_map = {
        '0.3': colors[0],  # Low interaction
        '0.5': colors[1],  # Medium interaction
        '0.8': colors[2]   # High interaction
    }
    
    # Process each interaction strength
    u_values = ['0.3', '0.5', '0.8']
    
    for u_idx, u in enumerate(u_values):
        print(f"\n{'='*60}")
        print(f"Processing interaction strength u = {u}")
        print(f"{'='*60}")
        
        # Collect all (u, v) coordinates across all repetitions
        all_u_coords = []
        all_v_coords = []
        
        # Track classification counts
        dominance_count = 0
        mixing_count = 0
        restructuring_count = 0
        
        # Process each repetition
        n_reps = len(all_results[u])
        print(f"Number of repetitions: {n_reps}")
        
        for rep_key in all_results[u].keys():
            rep_data = all_results[u][rep_key]
            
            # Get sc_list and cc_list
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
                    
                    # Classify the outcome
                    x, y = calculate_assymetricity(u_coord, v_coord, k)
                    class_type = characterize_case(x, y)
                    
                    if class_type == 0:
                        dominance_count += 1
                    elif class_type == 1:
                        mixing_count += 1
                    else:
                        restructuring_count += 1
                        
                except np.linalg.LinAlgError:
                    # Skip singular matrix cases
                    pass
        
        # Convert to numpy arrays
        all_u_coords = np.array(all_u_coords)
        all_v_coords = np.array(all_v_coords)
        
        total_points = len(all_u_coords)
        print(f"\nTotal data points: {total_points}")
        print(f"Classification summary:")
        print(f"  Dominance:     {dominance_count:5d} ({100*dominance_count/total_points:5.1f}%)")
        print(f"  Mixing:        {mixing_count:5d} ({100*mixing_count/total_points:5.1f}%)")
        print(f"  Restructuring: {restructuring_count:5d} ({100*restructuring_count/total_points:5.1f}%)")
        
        # Create heatmap with contours
        print(f"\nCreating heatmap visualization...")
        
        output_file = f"{output_dir}/VectorDecomp_48species_u{u}_heatmap.svg"
        title = f"Coalescence Outcomes (u = {u}, 100 repetitions)"
        
        create_heatmap_with_contours(
            all_u_coords, all_v_coords,
            title=title,
            color=color_map[u],
            output_file=output_file,
            bins=60,
            smoothing_sigma=2.0,
            contour_levels=12
        )
        
        print(f"Saved heatmap to: {output_file}")
        
        # Also create density plots for theta and r
        # Theta plot (angular distribution)
        theta_values = np.arctan2(all_u_coords, all_v_coords)
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.hist(theta_values, bins=50, density=True, alpha=0.7, 
                color=color_map[u], edgecolor='black', linewidth=0.5)
        ax.set_xlim(0, np.pi/2)
        ax.set_xlabel('θ (angle from v-axis)', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.set_title(f'Angular Distribution (u = {u})', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        theta_file = f"{output_dir}/VectorDecomp_48species_u{u}_theta_dist.svg"
        plt.tight_layout()
        plt.savefig(theta_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        # R plot (radial distribution)
        r_values = np.sqrt(all_u_coords**2 + all_v_coords**2)
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.hist(r_values, bins=50, density=True, alpha=0.7,
                color=color_map[u], edgecolor='black', linewidth=0.5)
        ax.set_xlim(0, 1.2)
        ax.set_xlabel('r (distance from origin)', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.set_title(f'Radial Distribution (u = {u})', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        r_file = f"{output_dir}/VectorDecomp_48species_u{u}_r_dist.svg"
        plt.tight_layout()
        plt.savefig(r_file, dpi=300, bbox_inches='tight')
        plt.close()
    
    # Create comparison plot showing all three intensities
    print(f"\n{'='*60}")
    print("Creating comparison visualization...")
    print(f"{'='*60}")
    
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
                except np.linalg.LinAlgError:
                    pass
        
        # Create heatmap
        H, xedges, yedges = np.histogram2d(all_u_coords, all_v_coords, 
                                           bins=50, range=[[0, 1], [0, 1]])
        H_smooth = gaussian_filter(H.T, sigma=2.0)
        
        cmap = plt.cm.colors.LinearSegmentedColormap.from_list(
            'custom', ['white', color_map[u]], N=256)
        
        im = ax.pcolormesh(xedges[:-1], yedges[:-1], H_smooth, 
                           cmap=cmap, shading='auto')
        
        contours = ax.contour(xedges[:-1], yedges[:-1], H_smooth, 
                             levels=10, colors='black', alpha=0.3, linewidths=0.5)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title(f'u = {u}', fontsize=16)
        ax.set_xlabel('u', fontsize=14)
        if idx == 0:
            ax.set_ylabel('v', fontsize=14)
        
        # Add diagonal
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.2, linewidth=1)
        
        # Grid
        ax.grid(True, alpha=0.2)
    
    plt.suptitle('Coalescence Outcomes Across Interaction Strengths (100 repetitions each)', 
                 fontsize=18, y=1.02)
    
    comparison_file = f"{output_dir}/VectorDecomp_48species_comparison_heatmap.svg"
    plt.tight_layout()
    plt.savefig(comparison_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nAnalysis complete!")
    print(f"All figures saved to: {output_dir}")
    print(f"\nGenerated files:")
    print(f"- Individual heatmaps for each interaction strength")
    print(f"- Theta and R distribution plots")
    print(f"- Comparison plot across all three intensities")


if __name__ == "__main__":
    analyze_48species_100reps_heatmap()