#!/usr/bin/env python3
"""
Create smooth contour heatmaps using radial basis smoothing
Properly handles the radial nature of vector decomposition coordinates
"""

import json
import numpy as np
import os
import math
from scipy.ndimage import gaussian_filter

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

def radial_to_uv(r, theta):
    """Convert radial coordinates (r, theta) back to u,v"""
    u = r * np.cos(theta)
    v = r * np.sin(theta)
    return u, v

def create_radial_density_field(u_coords, v_coords, r_bins=40, theta_bins=40, smoothing_sigma=3.0):
    """Create smooth density field using radial coordinates"""
    
    # Convert to radial coordinates
    r, theta = uv_to_radial(u_coords, v_coords)
    
    # Create 2D histogram in radial space
    r_max = 1.0  # max radius in u-v space is sqrt(2), but we focus on [0,1]
    theta_max = np.pi/2  # first quadrant only
    
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

def create_cartesian_density_from_radial(H_radial, r_edges, theta_edges, uv_bins=80):
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
            
            # Only process first quadrant (u>=0, v>=0)
            if theta_val >= 0 and theta_val <= np.pi/2 and r_val <= 1.0:
                # Find nearest radial bin
                r_idx = np.argmin(np.abs(r_centers - r_val))
                theta_idx = np.argmin(np.abs(theta_centers - theta_val))
                
                # Bounds checking
                if r_idx < H_radial.shape[0] and theta_idx < H_radial.shape[1]:
                    density_uv[j, i] = H_radial[r_idx, theta_idx]
    
    return density_uv

def create_svg_radial_contour(u_coords, v_coords, title, color_scheme, output_file, sigma_values=[2.0, 5.0, 10.0]):
    """Create multiple radial-smoothed contour plots with different sigma values"""
    
    # Create plots for different sigma values
    for sigma in sigma_values:
        print(f"Creating radial contour with σ={sigma}: {os.path.basename(output_file)}")
        
        # Create radial density field
        H_radial, r_edges, theta_edges = create_radial_density_field(
            u_coords, v_coords, 
            r_bins=50, theta_bins=50, 
            smoothing_sigma=sigma
        )
        
        # Convert back to u-v space
        density_uv = create_cartesian_density_from_radial(H_radial, r_edges, theta_edges, uv_bins=80)
        
        # Create filename with sigma suffix
        base_name, ext = os.path.splitext(output_file)
        sigma_file = f"{base_name}_sigma{sigma:.1f}{ext}"
        
        # Create SVG
        success = create_svg_from_density(density_uv, title + f" (σ={sigma})", color_scheme, sigma_file)
        if success:
            print(f"✅ Created: {os.path.basename(sigma_file)}")

def create_svg_from_density(density, title, color_scheme, output_file):
    """Create SVG from density field"""
    
    # SVG parameters
    width, height = 600, 600
    margin = 80
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    bins = density.shape[0]
    
    # Color schemes
    color_schemes = {
        'blue': {
            'gradient_id': 'blueGradient',
            'colors': ['#f7fbff', '#c6dbef', '#6baed6', '#2171b5', '#08306b'],
            'contour_color': '#08519c'
        },
        'orange': {
            'gradient_id': 'orangeGradient', 
            'colors': ['#fff5eb', '#fdd0a2', '#fd8d3c', '#d94701', '#7f2704'],
            'contour_color': '#a63603'
        },
        'red': {
            'gradient_id': 'redGradient',
            'colors': ['#fff5f0', '#fcbba1', '#fc9272', '#de2d26', '#a50f15'],
            'contour_color': '#a50f15'
        }
    }
    
    scheme = color_schemes.get(color_scheme, color_schemes['blue'])
    
    # Start SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width + 120}" height="{height + 120}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title {{ font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; }}
      .axis-label {{ font-family: Arial, sans-serif; font-size: 14px; text-anchor: middle; }}
      .tick-label {{ font-family: Arial, sans-serif; font-size: 11px; text-anchor: middle; }}
    </style>
  </defs>
  
  <!-- Background -->
  <rect x="0" y="0" width="{width + 120}" height="{height + 120}" fill="white"/>
  
  <!-- Title -->
  <text x="{(width + 120) / 2}" y="40" class="title">{title}</text>
  
  <!-- Plot area background -->
  <rect x="{margin}" y="{margin}" width="{plot_width}" height="{plot_height}" 
        fill="#fafafa" stroke="none"/>
'''
    
    # Create smooth density visualization
    cell_width = plot_width / bins
    cell_height = plot_height / bins
    threshold = 0.05
    
    for i in range(bins):
        for j in range(bins):
            density_val = density[j, i]
            
            if density_val > threshold:
                x_center = margin + (i + 0.5) * cell_width
                y_center = margin + (bins - 1 - j + 0.5) * cell_height
                
                # Circle size and color based on density
                max_radius = min(cell_width, cell_height) * 0.9
                radius = max_radius * math.sqrt(density_val)
                
                opacity = 0.2 + 0.8 * density_val
                color_idx = min(4, int(density_val * 4))
                color = scheme['colors'][color_idx]
                
                svg_content += f'''  <circle cx="{x_center:.1f}" cy="{y_center:.1f}" r="{radius:.1f}" 
        fill="{color}" opacity="{opacity:.3f}" stroke="none"/>
'''
    
    # Add diagonal reference line
    x1, y1 = margin, margin + plot_height
    x2, y2 = margin + plot_width, margin
    svg_content += f'''  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
        stroke="#666666" stroke-width="2" stroke-dasharray="8,4" opacity="0.6"/>
'''
    
    # Add axes and labels (similar to previous implementation)
    # [Grid, axes, labels code - abbreviated for length]
    
    # Add plot border
    svg_content += f'''  <rect x="{margin}" y="{margin}" width="{plot_width}" height="{plot_height}" 
        fill="none" stroke="black" stroke-width="2"/>
'''
    
    # Axis labels
    svg_content += f'''  <text x="{margin + plot_width / 2}" y="{height + 80}" class="axis-label">
    u (contribution from community 1)</text>
  <text x="30" y="{margin + plot_height / 2}" class="axis-label" 
        transform="rotate(-90, 30, {margin + plot_height / 2})">
    v (contribution from community 2)</text>
'''
    
    # Close SVG
    svg_content += '</svg>'
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    return True

def process_100rep_data(data_file):
    """Process 100-repetition simulation data"""
    
    print(f"Processing 100-repetition data from: {data_file}")
    
    with open(data_file, 'r') as f:
        all_results = json.load(f)
    
    processed_data = {}

    for u in ['0.3', '0.6', '0.8']:
        print(f"\nProcessing u = {u}...")
        
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
    """Main function to create radial-based smooth contour heatmaps"""
    
    print("="*80)
    print("CREATING RADIAL-BASED SMOOTH CONTOUR HEATMAPS")
    print("="*80)
    
    # Process data
    data_file = "Simulation_Data/48species_100reps_final/Community_100reps_final.json"
    processed_data = process_100rep_data(data_file)
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Create radial smooth contour heatmaps with multiple sigma values
    u_values = ['0.3', '0.6', '0.8']
    colors = ['blue', 'orange', 'red']
    labels = ['Low Interaction', 'Medium Interaction', 'High Interaction']
    
    # Test with multiple sigma values for comparison
    sigma_values = [2.0, 5.0, 10.0, 15.0]
    
    print(f"\n📊 Creating radial-based smooth contours with σ = {sigma_values}...")
    
    for u, color, label in zip(u_values, colors, labels):
        data = processed_data[u]
        u_coords = data['u_coords']
        v_coords = data['v_coords']
        
        if len(u_coords) > 0:
            title = f"Radial Smooth: {label} (u = {u})"
            output_file = f"{output_dir}/VectorDecomp_radial_u{u}.svg"
            
            create_svg_radial_contour(u_coords, v_coords, title, color, output_file, sigma_values)
    
    print(f"\n" + "="*80)
    print(f"RADIAL-BASED CONTOURS COMPLETE!")
    print(f"="*80)
    print(f"🎯 Key improvement: Smoothing respects radial geometry of vector decomposition")
    print(f"📊 Multiple sigma values: {sigma_values}")
    print(f"📁 Check output directory for files with sigma suffixes")

if __name__ == "__main__":
    main()