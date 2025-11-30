#!/usr/bin/env python3
"""
Create plots matching the exact style of the reference SVG:
- Same figure size (160.708pt x 156.05465pt)  
- Same colormap (#802000 with 0.7 opacity)
- No title, minimal labels
- Clean, publication style
"""

import json
import numpy as np
import os

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

def create_style_matched_svg(u_coords, v_coords, output_file):
    """Create SVG matching the exact style of the reference"""
    
    print(f"Creating style-matched plot: {os.path.basename(output_file)}")
    
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
    
    # Reference color and style
    color = "#802000"
    opacity = "0.7"
    circle_radius = 1.369306  # From reference path definition
    
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
    
    # Define circle path (from reference)
    svg_content += f'''   <defs>
    <path id="circle_marker" d="M 0 {circle_radius} 
C {0.363144 * circle_radius} {circle_radius} {0.711464 * circle_radius} {1.225028 * circle_radius} {0.968246 * circle_radius} {0.968246 * circle_radius} 
C {1.225028 * circle_radius} {0.711464 * circle_radius} {circle_radius} {0.363144 * circle_radius} {circle_radius} 0 
C {circle_radius} {-0.363144 * circle_radius} {1.225028 * circle_radius} {-0.711464 * circle_radius} {0.968246 * circle_radius} {-0.968246 * circle_radius} 
C {0.711464 * circle_radius} {-1.225028 * circle_radius} {0.363144 * circle_radius} {-circle_radius} 0 {-circle_radius} 
C {-0.363144 * circle_radius} {-circle_radius} {-0.711464 * circle_radius} {-1.225028 * circle_radius} {-0.968246 * circle_radius} {-0.968246 * circle_radius} 
C {-1.225028 * circle_radius} {-0.711464 * circle_radius} {-circle_radius} {-0.363144 * circle_radius} {-circle_radius} 0 
C {-circle_radius} {0.363144 * circle_radius} {-1.225028 * circle_radius} {0.711464 * circle_radius} {-0.968246 * circle_radius} {0.968246 * circle_radius} 
C {-0.711464 * circle_radius} {1.225028 * circle_radius} {-0.363144 * circle_radius} {circle_radius} 0 {circle_radius} 
z
"/>
   </defs>
'''
    
    # Add data points
    svg_content += '   <g id="PathCollection_1">\n'
    
    for i in range(len(u_coords)):
        u_val = u_coords[i]
        v_val = v_coords[i]
        
        # Convert to plot coordinates (note: v is flipped because SVG y increases downward)
        x_plot = plot_left + u_val * plot_width
        y_plot = plot_bottom - v_val * plot_height
        
        svg_content += f'    <use xlink:href="#circle_marker" x="{x_plot:.6f}" y="{y_plot:.6f}" style="fill: {color}; fill-opacity: {opacity}"/>\n'
    
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
    """Create style-matched plots"""
    
    print("="*80)
    print("CREATING STYLE-MATCHED PLOTS (REFERENCE STYLE)")
    print("="*80)
    
    # Process data
    data_file = "Simulation_Data/48species_100reps_final/Community_100reps_final.json"
    processed_data = process_100rep_data(data_file)
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Create style-matched plots
    u_values = ['0.3', '0.5', '0.8']
    
    plots_created = 0
    
    print(f"\n📊 Creating style-matched plots...")
    
    for u in u_values:
        data = processed_data[u]
        u_coords = data['u_coords']
        v_coords = data['v_coords']
        
        if len(u_coords) > 0:
            output_file = f"{output_dir}/VectorDecomp_u{u}_style_matched.svg"
            
            success = create_style_matched_svg(u_coords, v_coords, output_file)
            if success:
                plots_created += 1
                print(f"✅ Created: VectorDecomp_u{u}_style_matched.svg")
    
    print(f"\n" + "="*80)
    print(f"STYLE-MATCHED PLOTS COMPLETE!")
    print(f"="*80)
    print(f"📊 Plots created: {plots_created}")
    print(f"🎯 Features:")
    print(f"   - Exact figure size: 160.708pt × 156.05465pt")
    print(f"   - Reference colormap: #802000 with 0.7 opacity")
    print(f"   - Minimal design: no title, clean axes")
    print(f"   - Publication-ready style")

if __name__ == "__main__":
    main()