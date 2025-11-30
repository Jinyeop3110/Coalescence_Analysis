#!/usr/bin/env python3
"""
Create contour line plots instead of heatmaps
"""

import json
import numpy as np
import os
import math
from scipy.ndimage import gaussian_filter
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib import cm
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

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
    
    try:
        e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))
    except np.linalg.LinAlgError:
        return 0, 0, 1
    
    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)
    x3 = np.linalg.norm(m - (e12[0]*u) - (e12[1]*v))
    
    if x1**2 + x2**2 == 0:
        return 0, 0, x3
    
    try:
        convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2))
    except:
        return x1, x2, x3
    
    return convert*x1, convert*x2, x3

def uv_to_radial(u_coords, v_coords):
    """Convert u,v coordinates to radial coordinates (r, theta)"""
    r = np.sqrt(u_coords**2 + v_coords**2)
    theta = np.arctan2(v_coords, u_coords)
    # Normalize theta to [0, π/2] for first quadrant
    theta = np.abs(theta)
    theta = np.minimum(theta, np.pi/2)
    return r, theta

def create_radial_density_field(u_coords, v_coords, r_bins=80, theta_bins=80, smoothing_sigma=8.0):
    """Create smooth density field using radial coordinates"""
    
    # Convert to radial coordinates
    r, theta = uv_to_radial(u_coords, v_coords)
    
    # Create 2D histogram in radial space
    r_max = 1.0 
    theta_max = np.pi/2
    
    H_radial, r_edges, theta_edges = np.histogram2d(
        r, theta, 
        bins=[r_bins, theta_bins], 
        range=[[0, r_max], [0, theta_max]]
    )
    
    # Apply Gaussian smoothing in radial space
    H_smooth = gaussian_filter(H_radial, sigma=smoothing_sigma)
    
    # Normalize
    H_norm = H_smooth / np.max(H_smooth) if np.max(H_smooth) > 0 else H_smooth
    
    return H_norm, r_edges, theta_edges

def create_cartesian_density_from_radial(H_radial, r_edges, theta_edges, uv_bins=100):
    """Convert radial density field back to u-v Cartesian grid"""
    
    # Create u-v grid
    u_grid = np.linspace(0, 1, uv_bins)
    v_grid = np.linspace(0, 1, uv_bins)
    U, V = np.meshgrid(u_grid, v_grid)
    
    # Convert grid to radial coordinates
    R_grid = np.sqrt(U**2 + V**2)
    Theta_grid = np.arctan2(V, U)
    
    # Initialize output density field
    density_uv = np.zeros((uv_bins, uv_bins))
    
    # Interpolate from radial histogram to u-v grid
    r_centers = (r_edges[:-1] + r_edges[1:]) / 2
    theta_centers = (theta_edges[:-1] + theta_edges[1:]) / 2
    
    for i in range(uv_bins):
        for j in range(uv_bins):
            r_val = R_grid[j, i]
            theta_val = Theta_grid[j, i]
            
            # Only process first quadrant (u>=0, v>=0) and within unit circle
            if theta_val >= 0 and theta_val <= np.pi/2 and r_val <= 1.0:
                # Find nearest radial bin
                r_idx = np.argmin(np.abs(r_centers - r_val))
                theta_idx = np.argmin(np.abs(theta_centers - theta_val))
                
                # Bounds checking
                if r_idx < H_radial.shape[0] and theta_idx < H_radial.shape[1]:
                    density_uv[j, i] = H_radial[r_idx, theta_idx]
    
    return density_uv

def create_contour_plot(u_coords, v_coords, output_file, u_value):
    """Create contour plot using matplotlib"""
    
    if not HAS_MATPLOTLIB:
        print("matplotlib not available, skipping contour plot")
        return
    
    print(f"Creating contour plot: {os.path.basename(output_file)}")
    
    # Create radial density field
    H_radial, r_edges, theta_edges = create_radial_density_field(
        u_coords, v_coords, 
        r_bins=80, theta_bins=80,
        smoothing_sigma=8.0
    )
    
    # Convert to u-v space
    density_uv = create_cartesian_density_from_radial(H_radial, r_edges, theta_edges, uv_bins=100)
    
    # Create figure with reference dimensions
    fig_width = 160.708 / 72  # Convert from pt to inches
    fig_height = 156.05465 / 72
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Create contour plot
    u_grid = np.linspace(0, 1, 100)
    v_grid = np.linspace(0, 1, 100)
    U, V = np.meshgrid(u_grid, v_grid)
    
    # Mask outside unit circle
    R = np.sqrt(U**2 + V**2)
    density_uv_masked = np.ma.masked_where(R > 1.0, density_uv)
    
    # Create contours with red colormap
    levels = 10
    contour = ax.contour(U, V, density_uv_masked, levels=levels, 
                        colors='#802000', linewidths=np.linspace(0.5, 2.0, levels))
    
    # Add filled contours with transparency
    contourf = ax.contourf(U, V, density_uv_masked, levels=levels,
                          cmap=plt.cm.Reds, alpha=0.3)
    
    # Add unit circle
    circle = patches.Circle((0, 0), 1, fill=False, edgecolor='#262626', linewidth=0.5)
    ax.add_patch(circle)
    
    # Set limits and aspect
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    
    # Minimal styling
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.tick_params(labelsize=6)
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Save
    plt.tight_layout()
    plt.savefig(output_file, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

def process_100rep_data(data_file):
    """Process 100-repetition simulation data"""
    
    print(f"Processing 100-repetition data from: {data_file}")
    
    with open(data_file, 'r') as f:
        all_results = json.load(f)
    
    processed_data = {}
    
    for u in ['0.3', '0.5', '0.8']:
        print(f"Processing u = {u}...")
        
        all_u_coords = []
        all_v_coords = []
        
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
                
                # Check if communities have surviving species
                c1_alive = np.sum(c_1 > 0)
                c2_alive = np.sum(c_2 > 0)
                cmix_alive = np.sum(c_mix > 0)
                
                if c1_alive > 0 and c2_alive > 0 and cmix_alive > 0:
                    try:
                        # Calculate vector decomposition
                        u_coord, v_coord, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                        
                        # Only include valid coordinates
                        if not (np.isnan(u_coord) or np.isnan(v_coord)):
                            all_u_coords.append(u_coord)
                            all_v_coords.append(v_coord)
                            
                    except Exception as e:
                        # Skip problematic cases
                        pass
        
        # Convert to numpy arrays
        all_u_coords = np.array(all_u_coords)
        all_v_coords = np.array(all_v_coords)
        
        total_points = len(all_u_coords)
        print(f"  Total data points: {total_points}")
        
        # Store processed data
        processed_data[u] = {
            'u_coords': all_u_coords,
            'v_coords': all_v_coords
        }
    
    return processed_data

def main():
    """Create contour plots"""
    
    print("="*80)
    print("CREATING CONTOUR PLOTS")
    print("="*80)
    
    # Process data
    data_file = "Simulation_Data/48species_100reps_final/Community_100reps_final.json"
    processed_data = process_100rep_data(data_file)
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Create contour plots
    u_values = ['0.3', '0.5', '0.8']
    
    plots_created = 0
    
    print(f"\n📊 Creating contour plots...")
    
    for u in u_values:
        data = processed_data[u]
        u_coords = data['u_coords']
        v_coords = data['v_coords']
        
        if len(u_coords) > 0:
            output_file = f"{output_dir}/VectorDecomp_u{u}_contour.svg"
            
            create_contour_plot(u_coords, v_coords, output_file, u)
            plots_created += 1
            print(f"✅ Created: VectorDecomp_u{u}_contour.svg")
    
    print(f"\n" + "="*80)
    print(f"CONTOUR PLOTS COMPLETE!")
    print(f"="*80)
    print(f"📊 Plots created: {plots_created}")

if __name__ == "__main__":
    main()