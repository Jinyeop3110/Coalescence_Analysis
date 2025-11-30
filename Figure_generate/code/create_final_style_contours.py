#!/usr/bin/env python3
"""
Create radial contour plots (sigma=8.0) with reference style formatting:
- Same figure size (160.708pt x 156.05465pt)  
- Same colormap (#802000)
- No title, minimal labels
- Radial-based smoothing with sigma=8.0
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

def create_radial_density_field(u_coords, v_coords, r_bins=50, theta_bins=50, smoothing_sigma=6.0):
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

def create_cartesian_density_from_radial(H_radial, r_edges, theta_edges, uv_bins=60):
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

def interpolate_color(color1, color2, factor):
    """Interpolate between two hex colors"""
    # Convert hex to RGB
    c1_r = int(color1[1:3], 16)
    c1_g = int(color1[3:5], 16)
    c1_b = int(color1[5:7], 16)
    
    c2_r = int(color2[1:3], 16)
    c2_g = int(color2[3:5], 16)
    c2_b = int(color2[5:7], 16)
    
    # Interpolate
    r = int(c1_r + (c2_r - c1_r) * factor)
    g = int(c1_g + (c2_g - c1_g) * factor)
    b = int(c1_b + (c2_b - c1_b) * factor)
    
    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'

def generate_contour_rings(density_uv, plot_width, plot_height, n_levels=6):
    """Generate concentric rings based on density levels"""
    bins = density_uv.shape[0]
    
    # Get density statistics
    max_density = np.max(density_uv)
    print(f"  Max density: {max_density:.6f}")
    
    if max_density == 0:
        print("  No density data found")
        return []
    
    # Find peak location, but constrain to inner region of unit circle
    # Mask out regions near edges and outside unit circle
    u_grid = np.linspace(0, 1, bins)
    v_grid = np.linspace(0, 1, bins)
    U, V = np.meshgrid(u_grid, v_grid)
    R = np.sqrt(U**2 + V**2)
    
    # Create mask for reasonable peak locations
    valid_mask = (R < 0.8) & (U > 0.1) & (V > 0.1) & (U < 0.9) & (V < 0.9)
    masked_density = np.where(valid_mask, density_uv, 0)
    
    if np.max(masked_density) > 0:
        peak_idx = np.unravel_index(np.argmax(masked_density), masked_density.shape)
        peak_u = peak_idx[1] / bins
        peak_v = peak_idx[0] / bins
    else:
        # Fallback to center if no valid peak found
        peak_u = 0.5
        peak_v = 0.5
    
    print(f"  Peak at u={peak_u:.3f}, v={peak_v:.3f}")
    
    # Create contour levels based on percentiles of non-zero values
    non_zero_vals = density_uv[density_uv > 0]
    if len(non_zero_vals) == 0:
        print("  No non-zero values found")
        return []
    
    # Use percentiles for better level distribution
    percentiles = np.linspace(10, 90, n_levels)
    levels = np.percentile(non_zero_vals, percentiles)
    print(f"  Contour levels: {levels}")
    
    contour_elements = []
    
    # For each level, estimate the area of regions above this level
    for level_idx, level in enumerate(levels):
        # Count points above this level in circular regions around peak
        max_radius = 0.4  # Maximum search radius
        best_radius = 0
        
        # Try different radii to find where density drops to this level
        for test_radius in np.linspace(0.02, max_radius, 30):
            # Sample points on circle at this radius
            points_above = 0
            total_points = 0
            n_samples = 32
            
            for i in range(n_samples):
                angle = 2 * np.pi * i / n_samples
                u = peak_u + test_radius * np.cos(angle)
                v = peak_v + test_radius * np.sin(angle)
                
                # Check bounds and unit circle
                if 0 <= u < 1 and 0 <= v < 1 and np.sqrt(u**2 + v**2) < 1.0:
                    i_bin = min(int(u * bins), bins-1)
                    j_bin = min(int(v * bins), bins-1)
                    total_points += 1
                    
                    if density_uv[j_bin, i_bin] >= level:
                        points_above += 1
            
            # If roughly half the points are above threshold, this is our contour
            if total_points > 0 and 0.3 <= (points_above / total_points) <= 0.7:
                best_radius = test_radius
                break
        
        if best_radius > 0.01:  # Minimum meaningful radius
            norm_level = (level_idx + 1) / n_levels
            contour_elements.append({
                'center_u': peak_u,
                'center_v': peak_v,
                'radius': best_radius,
                'level': norm_level
            })
            print(f"  Level {level_idx}: radius={best_radius:.3f}, norm_level={norm_level:.3f}")
    
    print(f"  Generated {len(contour_elements)} contour rings")
    return contour_elements

def create_style_matched_contour_svg(u_coords, v_coords, output_file):
    """Create radial contour plot with reference style formatting"""
    
    print(f"Creating style-matched contour: {os.path.basename(output_file)}")
    
    # Create radial density field with higher resolution and more smoothing
    H_radial, r_edges, theta_edges = create_radial_density_field(
        u_coords, v_coords, 
        r_bins=80, theta_bins=80,  # Increased resolution
        smoothing_sigma=6.5  # Reduced smoothing for more detail
    )
    
    # Convert back to u-v space with higher resolution
    density_uv = create_cartesian_density_from_radial(H_radial, r_edges, theta_edges, uv_bins=100)  # Higher resolution
    
    # Exact dimensions from reference
    width_pt = 160.708
    height_pt = 156.05465
    
    # Plot area coordinates (from reference)
    plot_left = 21.82
    plot_right = 153.508  
    plot_top = 7.2
    plot_bottom = 138.0384
    
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    bins = density_uv.shape[0]
    
    # Color scheme - from light to dark red
    base_color = '#802000'  # Dark red for high density
    light_color = '#ffebe6'  # Very light red/pink for background
    
    # Start SVG with exact reference structure
    svg_content = f'''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns:xlink="http://www.w3.org/1999/xlink" width="{width_pt}pt" height="{height_pt}pt" viewBox="0 0 {width_pt} {height_pt}" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <defs>
  <style type="text/css">*{{stroke-linejoin: round; stroke-linecap: butt}}</style>
 </defs>
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 {height_pt} 
L {width_pt} {height_pt} 
L {width_pt} 0 
L 0 0 
z
" style="fill: #ffffff"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M {plot_left} {plot_bottom} 
L {plot_right} {plot_bottom} 
L {plot_right} {plot_top} 
L {plot_left} {plot_top} 
z
" style="fill: {light_color}"/>
   </g>
'''
    
    # Add axis ticks (minimal, like reference)
    tick_positions = [0.0, 0.5, 1.0]
    tick_length = 3.5
    
    # X-axis ticks
    for i, tick_val in enumerate(tick_positions):
        x_pos = plot_left + tick_val * plot_width
        svg_content += f'''   <g id="xtick_{i+1}">
    <g id="line2d_{i+1}">
     <path d="M 0 0 
L 0 -{tick_length} 
" style="stroke: #262626; stroke-width: 0.5" transform="translate({x_pos}, {plot_bottom})"/>
    </g>
    <g id="text_{i+1}">
     <text x="{x_pos}" y="{plot_bottom + 9}" style="font-family: Arial; font-size: 6.4px; text-anchor: middle; fill: #262626">{tick_val}</text>
    </g>
   </g>
'''
    
    # Y-axis ticks  
    for i, tick_val in enumerate(tick_positions):
        y_pos = plot_bottom - tick_val * plot_height
        svg_content += f'''   <g id="ytick_{i+1}">
    <g id="line2d_{i+4}">
     <path d="M 0 0 
L {tick_length} 0 
" style="stroke: #262626; stroke-width: 0.5" transform="translate({plot_left}, {y_pos})"/>
    </g>
    <g id="text_{i+4}">
     <text x="{plot_left - 5}" y="{y_pos + 2}" style="font-family: Arial; font-size: 6.4px; text-anchor: end; fill: #262626">{tick_val}</text>
    </g>
   </g>
'''
    
    # Add radial heatmap visualization with circular tiles
    svg_content += '   <g id="ContourCollection_1">\n'
    
    # Create radial grid instead of rectangular grid
    n_radial = 60  # Number of radial divisions
    n_angular = 80  # Number of angular divisions
    
    threshold = 0.0001  # Very small threshold to exclude near-zero density
    
    tiles_rendered = 0
    tiles_skipped = 0
    
    for r_idx in range(n_radial):
        for theta_idx in range(n_angular):
            # Calculate radial coordinates
            r_inner = r_idx / n_radial
            r_outer = (r_idx + 1) / n_radial
            r_mid = (r_inner + r_outer) / 2
            
            theta_start = theta_idx * (np.pi/2) / n_angular
            theta_end = (theta_idx + 1) * (np.pi/2) / n_angular
            theta_mid = (theta_start + theta_end) / 2
            
            # Render within slightly extended circle
            if r_outer <= 1.001:
                # Convert to u,v coordinates to get density
                u_mid = r_mid * np.cos(theta_mid)
                v_mid = r_mid * np.sin(theta_mid)
                
                # For boundary tiles, ensure they get rendered
                if r_inner >= 0.95:  # Boundary tiles near r=1
                    # Sample from a slightly inner point to ensure we get data
                    r_sample = min(r_mid, 0.99)
                    u_sample = r_sample * np.cos(theta_mid)
                    v_sample = r_sample * np.sin(theta_mid)
                    
                    if 0 <= u_sample < 1.0 and 0 <= v_sample < 1.0:
                        i_bin = min(int(u_sample * bins), bins-1)
                        j_bin = min(int(v_sample * bins), bins-1)
                        density_val = max(density_uv[j_bin, i_bin], 0.0001)  # Ensure minimum for boundary
                    else:
                        density_val = 0.0001  # Force render boundary tiles
                else:
                    # Normal sampling for inner tiles
                    if 0 <= u_mid < 1.0 and 0 <= v_mid < 1.0:
                        i_bin = min(int(u_mid * bins), bins-1)
                        j_bin = min(int(v_mid * bins), bins-1)
                        density_val = density_uv[j_bin, i_bin]
                    else:
                        density_val = 0.0001  # Just above threshold to ensure rendering
                
                # Render tiles above threshold
                if density_val >= threshold:
                    # Create radial sector path
                    # Convert to plot coordinates
                    x_center = plot_left
                    y_center = plot_bottom
                    
                    r_inner_plot = r_inner * min(plot_width, plot_height)
                    r_outer_plot = r_outer * min(plot_width, plot_height)
                    
                    # Calculate sector corners
                    x1_inner = x_center + r_inner_plot * np.cos(theta_start)
                    y1_inner = y_center - r_inner_plot * np.sin(theta_start)
                    x2_inner = x_center + r_inner_plot * np.cos(theta_end)
                    y2_inner = y_center - r_inner_plot * np.sin(theta_end)
                    
                    x1_outer = x_center + r_outer_plot * np.cos(theta_start)
                    y1_outer = y_center - r_outer_plot * np.sin(theta_start)
                    x2_outer = x_center + r_outer_plot * np.cos(theta_end)
                    y2_outer = y_center - r_outer_plot * np.sin(theta_end)
                    
                    # Create proper radial sector using SVG path
                    # Apply power transformation for more contrast
                    if density_val > 0:
                        adjusted_val = density_val ** 0.6
                        # Interpolate color from light to dark
                        color = interpolate_color(light_color, base_color, adjusted_val)
                    else:
                        # Use light background color for zero density
                        color = light_color
                    
                    # Create sector path - simplified approach for better reliability
                    if r_inner < 0.01:  # Very small radius - use triangular sector from center
                        path_data = f"M {x_center:.3f} {y_center:.3f} "
                        path_data += f"L {x1_outer:.3f} {y1_outer:.3f} "
                        path_data += f"A {r_outer_plot:.3f} {r_outer_plot:.3f} 0 0 1 {x2_outer:.3f} {y2_outer:.3f} "
                        path_data += "Z"
                    else:  # Normal annular sector
                        path_data = f"M {x1_inner:.3f} {y1_inner:.3f} "
                        path_data += f"L {x1_outer:.3f} {y1_outer:.3f} "
                        path_data += f"A {r_outer_plot:.3f} {r_outer_plot:.3f} 0 0 1 {x2_outer:.3f} {y2_outer:.3f} "
                        path_data += f"L {x2_inner:.3f} {y2_inner:.3f} "
                        path_data += f"A {r_inner_plot:.3f} {r_inner_plot:.3f} 0 0 0 {x1_inner:.3f} {y1_inner:.3f} "
                        path_data += "Z"
                    
                    svg_content += f'''    <path d="{path_data}" style="fill: {color}; stroke: none"/>
'''
                    tiles_rendered += 1
                else:
                    tiles_skipped += 1
    
    print(f"  Tiles rendered: {tiles_rendered}, skipped: {tiles_skipped}")
    
    svg_content += '   </g>\n'
    
    # Close SVG structure
    svg_content += '''  </g>
 </g>
</svg>'''
    
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
    """Create final radial contour plots with reference style"""
    
    print("="*80)
    print("CREATING SMOOTH RADIAL HEATMAPS (σ=6.5) WITH REFERENCE STYLE")
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

    plots_created = 0
    
    print(f"\n📊 Creating radial contour plots with reference style...")
    
    for u in u_values:
        data = processed_data[u]
        u_coords = data['u_coords']
        v_coords = data['v_coords']
        
        if len(u_coords) > 0:
            output_file = f"{output_dir}/VectorDecomp_u{u}_radial_contour.svg"
            
            success = create_style_matched_contour_svg(u_coords, v_coords, output_file)
            if success:
                plots_created += 1
                print(f"✅ Created: VectorDecomp_u{u}_radial_contour.svg")
    
    print(f"\n" + "="*80)
    print(f"RADIAL HEATMAPS COMPLETE!")
    print(f"="*80)
    print(f"📊 Plots created: {plots_created}")
    print(f"🎯 Features:")
    print(f"   - Radial-based smoothing (σ=6.5)")
    print(f"   - Radial tiling: 60×80 (r×θ) grid")
    print(f"   - Reference style: 160.708pt × 156.05465pt")
    print(f"   - Color gradient: #ffebe6 (light red) → #802000 (dark red)")
    print(f"   - Circular tiles for clean radial boundary")
    print(f"   - No boundary circle (clean edge)")
    print(f"   - Minimal design: no title, clean axes")
    print(f"   - Geometrically correct for vector decomposition")

if __name__ == "__main__":
    main()