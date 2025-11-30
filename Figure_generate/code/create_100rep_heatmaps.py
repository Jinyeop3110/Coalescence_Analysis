#!/usr/bin/env python3
"""
Create discrete heatmaps using the 100-repetition data (not test data)
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

def process_100rep_data():
    """Process 100-repetition data"""
    
    data_file = 'Simulation_Data/48species_100reps_final/Community_100reps_final.json'
    
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
        
        print(f"  Total data points: {len(all_u_coords)}")
        
        # Store processed data
        processed_data[u] = {
            'u_coords': all_u_coords,
            'v_coords': all_v_coords
        }
    
    return processed_data

def create_svg_heatmap(data1, data2, title, color_hex, output_file, bins=25):
    """Create a discrete SVG heatmap using 100-rep data"""
    
    print(f"Creating discrete heatmap: {os.path.basename(output_file)}")
    
    # Create 2D histogram
    H, xedges, yedges = np.histogram2d(data1, data2, bins=bins, range=[[0, 1], [0, 1]])
    
    # SVG parameters
    width, height = 500, 500
    margin = 60
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    
    # Normalize histogram for color intensity
    max_count = np.max(H) if np.max(H) > 0 else 1
    
    # Start SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width + 100}" height="{height + 100}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title {{ font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; text-anchor: middle; }}
      .axis-label {{ font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; }}
      .tick-label {{ font-family: Arial, sans-serif; font-size: 10px; text-anchor: middle; }}
    </style>
  </defs>
  
  <!-- Background -->
  <rect x="0" y="0" width="{width + 100}" height="{height + 100}" fill="white"/>
  
  <!-- Title -->
  <text x="{(width + 100) / 2}" y="30" class="title">{title} (100 Repetitions)</text>
  
  <!-- Plot area -->
  <rect x="{margin}" y="{margin}" width="{plot_width}" height="{plot_height}" 
        fill="none" stroke="black" stroke-width="1"/>
'''
    
    # Draw heatmap cells
    cell_width = plot_width / bins
    cell_height = plot_height / bins
    
    for i in range(bins):
        for j in range(bins):
            count = H[i, j]
            if count > 0:
                # Calculate opacity based on count
                opacity = count / max_count
                
                # Convert color hex to RGB for opacity
                color_rgb = f"rgb({int(color_hex[1:3], 16)}, {int(color_hex[3:5], 16)}, {int(color_hex[5:7], 16)})"
                
                x = margin + i * cell_width
                y = margin + (bins - 1 - j) * cell_height  # Flip y-axis
                
                svg_content += f'''  <rect x="{x:.1f}" y="{y:.1f}" width="{cell_width:.1f}" height="{cell_height:.1f}" 
        fill="{color_rgb}" opacity="{opacity:.3f}"/>\n'''
    
    # Add diagonal reference line
    x1, y1 = margin, margin + plot_height
    x2, y2 = margin + plot_width, margin
    svg_content += f'''  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
        stroke="gray" stroke-width="1" stroke-dasharray="5,5" opacity="0.7"/>
'''
    
    # Add axes
    # X-axis
    svg_content += f'''  <line x1="{margin}" y1="{margin + plot_height}" x2="{margin + plot_width}" y2="{margin + plot_height}" 
        stroke="black" stroke-width="1"/>
'''
    
    # Y-axis  
    svg_content += f'''  <line x1="{margin}" y1="{margin}" x2="{margin}" y2="{margin + plot_height}" 
        stroke="black" stroke-width="1"/>
'''
    
    # X-axis ticks and labels
    for i in range(6):  # 0, 0.2, 0.4, 0.6, 0.8, 1.0
        x = margin + i * plot_width / 5
        y_tick = margin + plot_height
        value = i / 5
        
        svg_content += f'''  <line x1="{x}" y1="{y_tick}" x2="{x}" y2="{y_tick + 5}" stroke="black" stroke-width="1"/>
  <text x="{x}" y="{y_tick + 20}" class="tick-label">{value:.1f}</text>
'''
    
    # Y-axis ticks and labels
    for i in range(6):  # 0, 0.2, 0.4, 0.6, 0.8, 1.0
        y = margin + plot_height - i * plot_height / 5
        x_tick = margin
        value = i / 5
        
        svg_content += f'''  <line x1="{x_tick - 5}" y1="{y}" x2="{x_tick}" y2="{y}" stroke="black" stroke-width="1"/>
  <text x="{x_tick - 15}" y="{y + 4}" class="tick-label">{value:.1f}</text>
'''
    
    # Axis labels
    svg_content += f'''  <text x="{margin + plot_width / 2}" y="{height + 50}" class="axis-label">u (contribution from community 1)</text>
  <text x="20" y="{margin + plot_height / 2}" class="axis-label" transform="rotate(-90, 20, {margin + plot_height / 2})">v (contribution from community 2)</text>
'''
    
    # Add simple legend
    legend_x = width - 50
    legend_y = margin + 20
    
    svg_content += f'''  <!-- Legend -->
  <text x="{legend_x}" y="{legend_y}" class="axis-label">Density</text>
  <rect x="{legend_x - 10}" y="{legend_y + 10}" width="15" height="15" fill="{color_hex}" opacity="0.3"/>
  <text x="{legend_x + 10}" y="{legend_y + 22}" style="font-family: Arial; font-size: 8px;">Low</text>
  <rect x="{legend_x - 10}" y="{legend_y + 30}" width="15" height="15" fill="{color_hex}" opacity="1.0"/>
  <text x="{legend_x + 10}" y="{legend_y + 42}" style="font-family: Arial; font-size: 8px;">High</text>
'''
    
    # Close SVG
    svg_content += '</svg>'
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    return True

def main():
    """Create updated discrete heatmaps using 100-repetition data"""
    
    print("="*80)
    print("CREATING DISCRETE HEATMAPS FROM 100-REPETITION DATA")
    print("="*80)
    
    # Process 100-repetition data
    processed_data = process_100rep_data()
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Create discrete heatmaps
    u_values = ['0.3', '0.5', '0.8']
    colors = ['#1f77b4', '#ff7f0e', '#d62728']  # Blue, Orange, Red
    labels = ['Low Interaction', 'Medium Interaction', 'High Interaction']
    
    plots_created = 0
    
    print(f"\n📊 Creating discrete heatmaps from 100-repetition data...")
    
    for u, color, label in zip(u_values, colors, labels):
        data = processed_data[u]
        u_coords = data['u_coords']
        v_coords = data['v_coords']
        
        if len(u_coords) > 0:
            title = f"Coalescence Outcomes: {label} (u = {u})"
            output_file = f"{output_dir}/VectorDecomp_100rep_u{u}_discrete.svg"
            
            success = create_svg_heatmap(u_coords, v_coords, title, color, output_file, bins=30)
            if success:
                print(f"✅ Created: VectorDecomp_100rep_u{u}_discrete.svg")
                plots_created += 1
    
    # Final summary
    print(f"\n" + "="*80)
    print(f"DISCRETE HEATMAPS FROM 100-REP DATA COMPLETE!")
    print(f"="*80)
    print(f"📊 Plots created: {plots_created}")
    print(f"📁 Output directory: {output_dir}")
    
    print(f"\n🔍 Now compare:")
    print(f"   OLD (10-rep test): VectorDecomp_48species_u0.5_heatmap.svg")
    print(f"   NEW (100-rep):     VectorDecomp_100rep_u0.5_discrete.svg")
    print(f"   SMOOTH (100-rep):  VectorDecomp_smooth_u0.5_contour.svg")

if __name__ == "__main__":
    main()