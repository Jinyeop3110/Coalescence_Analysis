#!/usr/bin/env python3
"""
Create final radial smooth contour plots with sigma=8.0 and consistent colormaps
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

def create_radial_density_field(u_coords, v_coords, r_bins=50, theta_bins=50, smoothing_sigma=8.0):
    """Create smooth density field using radial coordinates with sigma=8.0"""
    
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

def create_svg_radial_contour(u_coords, v_coords, title, interaction_level, output_file):
    """Create radial-smoothed contour plot with consistent colormap"""
    
    print(f"Creating final radial contour: {os.path.basename(output_file)}")
    
    # Create radial density field with sigma=8.0
    H_radial, r_edges, theta_edges = create_radial_density_field(
        u_coords, v_coords, 
        r_bins=50, theta_bins=50, 
        smoothing_sigma=8.0
    )
    
    # Convert back to u-v space
    density_uv = create_cartesian_density_from_radial(H_radial, r_edges, theta_edges, uv_bins=80)
    
    # Create SVG with consistent colormap
    success = create_svg_from_density(density_uv, title, interaction_level, output_file)
    return success

def create_svg_from_density(density, title, interaction_level, output_file):
    """Create SVG from density field with consistent colormap"""
    
    # SVG parameters
    width, height = 600, 600
    margin = 80
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    bins = density.shape[0]
    
    # Consistent colormap for all interaction levels
    # Using a single viridis-like colormap that works for all cases
    colormap = {
        'gradient_id': 'densityGradient',
        'colors': ['#440154', '#31688e', '#35b779', '#fde725', '#ff6b35'],
        'background': '#fafafa',
        'contour_color': '#2c2c54'
    }
    
    # Start SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width + 120}" height="{height + 120}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title {{ font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; }}
      .axis-label {{ font-family: Arial, sans-serif; font-size: 14px; text-anchor: middle; }}
      .tick-label {{ font-family: Arial, sans-serif; font-size: 11px; text-anchor: middle; }}
    </style>
    
    <!-- Consistent gradient for all plots -->
    <linearGradient id="{colormap['gradient_id']}" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:{colormap['colors'][0]};stop-opacity:0.3"/>
      <stop offset="25%" style="stop-color:{colormap['colors'][1]};stop-opacity:0.5"/>
      <stop offset="50%" style="stop-color:{colormap['colors'][2]};stop-opacity:0.7"/>
      <stop offset="75%" style="stop-color:{colormap['colors'][3]};stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:{colormap['colors'][4]};stop-opacity:0.9"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect x="0" y="0" width="{width + 120}" height="{height + 120}" fill="white"/>
  
  <!-- Title -->
  <text x="{(width + 120) / 2}" y="40" class="title">{title}</text>
  
  <!-- Plot area background -->
  <rect x="{margin}" y="{margin}" width="{plot_width}" height="{plot_height}" 
        fill="{colormap['background']}" stroke="none"/>
'''
    
    # Create smooth density visualization
    cell_width = plot_width / bins
    cell_height = plot_height / bins
    threshold = 0.03  # Lower threshold for more visible structure
    
    for i in range(bins):
        for j in range(bins):
            density_val = density[j, i]
            
            if density_val > threshold:
                x_center = margin + (i + 0.5) * cell_width
                y_center = margin + (bins - 1 - j + 0.5) * cell_height
                
                # Circle size and color based on density
                max_radius = min(cell_width, cell_height) * 0.9
                radius = max_radius * math.sqrt(density_val)
                
                # Use consistent colormap for all interaction levels
                opacity = 0.3 + 0.7 * density_val
                color_idx = min(4, int(density_val * 4))
                color = colormap['colors'][color_idx]
                
                svg_content += f'''  <circle cx="{x_center:.1f}" cy="{y_center:.1f}" r="{radius:.1f}" 
        fill="{color}" opacity="{opacity:.3f}" stroke="none"/>
'''
    
    # Add diagonal reference line
    x1, y1 = margin, margin + plot_height
    x2, y2 = margin + plot_width, margin
    svg_content += f'''  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
        stroke="{colormap['contour_color']}" stroke-width="2" stroke-dasharray="8,4" opacity="0.6"/>
'''
    
    # Add coordinate grid
    grid_lines = 5
    for i in range(grid_lines + 1):
        # Vertical grid lines
        x = margin + i * plot_width / grid_lines
        svg_content += f'''  <line x1="{x}" y1="{margin}" x2="{x}" y2="{margin + plot_height}" 
        stroke="#dddddd" stroke-width="0.5" opacity="0.7"/>
'''
        
        # Horizontal grid lines
        y = margin + i * plot_height / grid_lines
        svg_content += f'''  <line x1="{margin}" y1="{y}" x2="{margin + plot_width}" y2="{y}" 
        stroke="#dddddd" stroke-width="0.5" opacity="0.7"/>
'''
    
    # Add plot border
    svg_content += f'''  <rect x="{margin}" y="{margin}" width="{plot_width}" height="{plot_height}" 
        fill="none" stroke="black" stroke-width="2"/>
'''
    
    # Add axes ticks and labels
    tick_values = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    
    for i, value in enumerate(tick_values):
        # X-axis ticks
        x = margin + i * plot_width / (len(tick_values) - 1)
        y_tick = margin + plot_height
        
        svg_content += f'''  <line x1="{x}" y1="{y_tick}" x2="{x}" y2="{y_tick + 8}" 
        stroke="black" stroke-width="1"/>
  <text x="{x}" y="{y_tick + 25}" class="tick-label">{value:.1f}</text>
'''
        
        # Y-axis ticks
        y = margin + plot_height - i * plot_height / (len(tick_values) - 1)
        x_tick = margin
        
        svg_content += f'''  <line x1="{x_tick - 8}" y1="{y}" x2="{x_tick}" y2="{y}" 
        stroke="black" stroke-width="1"/>
  <text x="{x_tick - 20}" y="{y + 4}" class="tick-label">{value:.1f}</text>
'''
    
    # Axis labels
    svg_content += f'''  <text x="{margin + plot_width / 2}" y="{height + 80}" class="axis-label">
    u (contribution from community 1)</text>
  <text x="30" y="{margin + plot_height / 2}" class="axis-label" 
        transform="rotate(-90, 30, {margin + plot_height / 2})">
    v (contribution from community 2)</text>
'''
    
    # Add legend/colorbar
    legend_x = width + 20
    legend_y = margin + 50
    legend_height = 200
    
    svg_content += f'''  <!-- Legend -->
  <text x="{legend_x + 30}" y="{legend_y - 10}" class="axis-label">Density</text>
  
  <rect x="{legend_x}" y="{legend_y}" width="20" height="{legend_height}" 
        fill="url(#{colormap['gradient_id']})" stroke="black" stroke-width="1"/>
  
  <text x="{legend_x + 25}" y="{legend_y + 10}" style="font-family: Arial; font-size: 10px;">High</text>
  <text x="{legend_x + 25}" y="{legend_y + legend_height - 5}" style="font-family: Arial; font-size: 10px;">Low</text>
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
    """Create final clean plots with sigma=8.0 and consistent colormaps"""
    
    print("="*80)
    print("CREATING FINAL RADIAL CONTOUR PLOTS (σ=8.0, CONSISTENT COLORMAP)")
    print("="*80)
    
    # Process data
    data_file = "Simulation_Data/48species_100reps_final/Community_100reps_final.json"
    processed_data = process_100rep_data(data_file)
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")

    # Create final plots
    u_values = ['0.3', '0.6', '0.8']
    labels = ['Low Interaction', 'Medium Interaction', 'High Interaction']
    
    plots_created = 0
    
    print(f"\n📊 Creating final radial contour plots with σ=8.0...")
    
    for u, label in zip(u_values, labels):
        data = processed_data[u]
        u_coords = data['u_coords']
        v_coords = data['v_coords']
        
        if len(u_coords) > 0:
            title = f"Coalescence Outcomes: {label} (u = {u})"
            output_file = f"{output_dir}/VectorDecomp_u{u}_radial_sigma8.svg"
            
            success = create_svg_radial_contour(u_coords, v_coords, title, u, output_file)
            if success:
                plots_created += 1
                print(f"✅ Created: VectorDecomp_u{u}_radial_sigma8.svg")
    
    print(f"\n" + "="*80)
    print(f"FINAL PLOTS COMPLETE!")
    print(f"="*80)
    print(f"📊 Plots created: {plots_created}")
    print(f"🎯 Features:")
    print(f"   - Radial-based smoothing (σ=8.0)")
    print(f"   - Consistent colormap across all interaction strengths")
    print(f"   - Geometrically correct for vector decomposition")
    print(f"   - Clean, publication-ready appearance")

if __name__ == "__main__":
    main()