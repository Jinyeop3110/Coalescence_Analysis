#!/usr/bin/env python3
"""
Create theta (angle) distribution plots matching the reference style
Shows the angular distribution of vector decomposition coordinates
"""

import json
import numpy as np
import os
import math

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

def uv_to_theta_normalized(u_coords, v_coords):
    """Convert u,v coordinates to theta/(π/2) ranging from 0 to 1"""
    theta = np.arctan2(v_coords, u_coords)
    # Ensure theta is in [0, π/2] range
    theta = np.abs(theta)
    theta = np.minimum(theta, np.pi/2)
    
    # Normalize by π/2 to get range [0, 1]
    theta_normalized = theta / (np.pi/2)
    return theta_normalized

def create_theta_histogram_svg(theta_values, output_file):
    """Create theta distribution plot matching reference style"""
    
    print(f"Creating theta plot: {os.path.basename(output_file)}")
    
    # Reference dimensions for theta plot (from Metric_metric3_MN_natural_null_style1_Theta.svg)
    width_pt = 167.330938
    height_pt = 63.93
    
    # Plot area coordinates (from reference)
    plot_left = 19.5975
    plot_right = 157.810937
    plot_top = 7.2
    plot_bottom = 43.23
    
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    # Create single histogram for brown bars only
    n_bins = 20
    
    # Original histogram as density (brown bars only)
    hist_orig, bin_edges = np.histogram(theta_values, bins=n_bins, range=(0, 1), density=True)
    
    # Set fixed max density to 6 for consistent scaling
    max_density = 6.0
    hist_orig_norm = hist_orig / max_density
    
    # Colors for stacked bars
    brown_color = "#802000"  # Dark red/brown for original data
    grey_color = "#808080"   # Grey for inverted data
    
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
" style="fill: #ffffff"/>
   </g>
'''
    
    # Add X-axis ticks for normalized range [0, 1]
    x_tick_positions = [0, 0.5, 1.0]
    x_tick_labels = ['0', '0.5', '1']
    tick_length = 3.5
    
    for i, (tick_val, label) in enumerate(zip(x_tick_positions, x_tick_labels)):
        x_pos = plot_left + tick_val * plot_width
        svg_content += f'''   <g id="xtick_{i+1}">
    <g id="line2d_{i+1}">
     <path d="M 0 0 
L 0 -{tick_length} 
" style="stroke: #262626; stroke-width: 0.5" transform="translate({x_pos}, {plot_bottom})"/>
    </g>
    <g id="text_{i+1}">
     <text x="{x_pos}" y="{plot_bottom + 12}" style="font-family: Arial; font-size: 12.8px; text-anchor: middle; fill: #262626">{label}</text>
    </g>
   </g>
'''
    
    # Add Y-axis ticks for density
    y_tick_positions = [0.0, 1.0]
    y_tick_labels = ['0', '10']
    for i, (tick_val, label) in enumerate(zip(y_tick_positions, y_tick_labels)):
        y_pos = plot_bottom - tick_val * plot_height
        svg_content += f'''   <g id="ytick_{i+1}">
    <g id="line2d_{i+4}">
     <path d="M 0 0 
L {tick_length} 0 
" style="stroke: #262626; stroke-width: 0.5" transform="translate({plot_left}, {y_pos})"/>
    </g>
    <g id="text_{i+4}">
     <text x="{plot_left - 5}" y="{y_pos + 2}" style="font-family: Arial; font-size: 12.8px; text-anchor: end; fill: #262626">{label}</text>
    </g>
   </g>
'''
    
    # Add stacked histogram bars
    svg_content += '   <g id="HistogramCollection_1">\n'
    
    bin_width = plot_width / n_bins
    
    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        
        # Calculate bar height (brown only)
        brown_height = hist_orig_norm[i] * plot_height
        
        # Only draw bars if there's data
        if brown_height > 0:
            y_brown = plot_bottom - brown_height
            # Opacity varies with frequency, clamped to valid range
            brown_opacity = 0.3 + 0.7 * min(hist_orig_norm[i], 1.0)
            
            svg_content += f'''    <rect x="{x_left:.3f}" y="{y_brown:.3f}" width="{bin_width:.3f}" height="{brown_height:.3f}" style="fill: {brown_color}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''
            
    
    svg_content += '   </g>\n'
    
    # Add step function outline around entire histogram
    svg_content += '   <g id="HistogramOutline_1">\n'
    
    # Build step function path that goes to y=0 for empty bars
    path_parts = []
    
    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        x_right = x_left + bin_width
        brown_height = hist_orig_norm[i] * plot_height
        
        if brown_height > 0:
            y_top = plot_bottom - brown_height
            
            if not path_parts:  # First bar
                path_parts.append(f"M {x_left:.3f} {plot_bottom:.3f}")
            else:
                # Connect from previous position to start of this bar at baseline
                path_parts.append(f"L {x_left:.3f} {plot_bottom:.3f}")
            
            # Step up to bar height
            path_parts.append(f"L {x_left:.3f} {y_top:.3f}")
            # Move horizontally across bar top
            path_parts.append(f"L {x_right:.3f} {y_top:.3f}")
            # Step down to baseline at end of bar
            path_parts.append(f"L {x_right:.3f} {plot_bottom:.3f}")
    
    if path_parts:
        path_string = " ".join(path_parts)
        
        # Add step function outline
        svg_content += f'''    <path d="{path_string}" style="fill: none; stroke: #333333; stroke-width: 0.4"/>
'''
    
    svg_content += '   </g>\n'
    
    # Add box frame around plot area
    svg_content += f'''   <g id="axes_frame">
    <path d="M {plot_left} {plot_bottom} 
L {plot_right} {plot_bottom} 
L {plot_right} {plot_top} 
L {plot_left} {plot_top} 
L {plot_left} {plot_bottom}" style="fill: none; stroke: #262626; stroke-width: 0.4"/>
   </g>
'''
    
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
        
        # Convert to numpy arrays and calculate normalized theta
        all_u_coords = np.array(all_u_coords)
        all_v_coords = np.array(all_v_coords)
        theta_values = uv_to_theta_normalized(all_u_coords, all_v_coords)
        
        total_points = len(all_u_coords)
        print(f"  Total data points: {total_points}")
        print(f"  Theta/(π/2) range: [{np.min(theta_values):.3f}, {np.max(theta_values):.3f}]")
        
        # Store processed data
        processed_data[u] = {
            'u_coords': all_u_coords,
            'v_coords': all_v_coords,
            'theta_values': theta_values
        }
    
    return processed_data

def main():
    """Create theta distribution plots"""
    
    print("="*80)
    print("CREATING THETA DISTRIBUTION PLOTS")
    print("="*80)
    
    # Process data
    data_file = "Simulation_Data/48species_100reps_final/Community_100reps_final.json"
    processed_data = process_100rep_data(data_file)
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Create theta plots
    u_values = ['0.3', '0.6', '0.8']

    plots_created = 0
    
    print(f"\n📊 Creating theta distribution plots...")
    
    for u in u_values:
        data = processed_data[u]
        theta_values = data['theta_values']
        
        if len(theta_values) > 0:
            output_file = f"{output_dir}/VectorDecomp_u{u}_theta.svg"
            
            success = create_theta_histogram_svg(theta_values, output_file)
            if success:
                plots_created += 1
                print(f"✅ Created: VectorDecomp_u{u}_theta.svg")
    
    print(f"\n" + "="*80)
    print(f"THETA DISTRIBUTION PLOTS COMPLETE!")
    print(f"="*80)
    print(f"📊 Plots created: {plots_created}")
    print(f"🎯 Features:")
    print(f"   - Angular distribution of vector decomposition")
    print(f"   - Reference style: 167.330938pt × 63.93pt")
    print(f"   - Single color: #802000 with varying opacity")
    print(f"   - X-axis: 0 to 1 (theta/(π/2) normalized)")
    print(f"   - 0 = θ=0 (pure u), 1 = θ=π/2 (pure v)")
    print(f"   - Shows mixing vs dominance angular preferences")

if __name__ == "__main__":
    main()