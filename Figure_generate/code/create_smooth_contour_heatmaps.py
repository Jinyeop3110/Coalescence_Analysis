#!/usr/bin/env python3
"""
Create smooth, continuous contour-style heatmaps from 100-repetition simulation data
Uses SVG with smooth gradient fills and contour lines for publication-quality visualization
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


def calculate_assymetricity(u, v, k):
    """Calculate asymmetricity measures"""
    x = np.sqrt(np.array(u)**2 + np.array(v)**2)
    if v == 0:
        y = 1.0
    else:
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
    return 1  # Default to mixing


def create_smooth_density_field(u_coords, v_coords, bins=50, smoothing_sigma=3.0):
    """Create a smooth density field using Gaussian filtering"""
    
    # Create high-resolution 2D histogram
    H, xedges, yedges = np.histogram2d(u_coords, v_coords, bins=bins, range=[[0, 1], [0, 1]])
    
    # Apply strong Gaussian smoothing for continuous appearance
    H_smooth = gaussian_filter(H.T, sigma=smoothing_sigma)
    
    # Normalize to 0-1 range
    H_norm = H_smooth / np.max(H_smooth) if np.max(H_smooth) > 0 else H_smooth
    
    return H_norm, xedges, yedges


def create_svg_contour_heatmap(u_coords, v_coords, title, color_scheme, output_file, bins=60):
    """Create smooth contour-style SVG heatmap with continuous gradients"""
    
    print(f"Creating smooth contour heatmap: {os.path.basename(output_file)}")
    
    # Create smooth density field with high sigma for maximum smoothness
    density, xedges, yedges = create_smooth_density_field(u_coords, v_coords, bins=bins, smoothing_sigma=8.0)
    
    # SVG parameters
    width, height = 600, 600
    margin = 80
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    
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
    
    # Start SVG with definitions
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width + 120}" height="{height + 120}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title {{ font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; }}
      .axis-label {{ font-family: Arial, sans-serif; font-size: 14px; text-anchor: middle; }}
      .tick-label {{ font-family: Arial, sans-serif; font-size: 11px; text-anchor: middle; }}
    </style>
    
    <!-- Radial gradient for smooth density representation -->
    <radialGradient id="{scheme['gradient_id']}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:{scheme['colors'][4]};stop-opacity:0.9"/>
      <stop offset="30%" style="stop-color:{scheme['colors'][3]};stop-opacity:0.7"/>
      <stop offset="60%" style="stop-color:{scheme['colors'][2]};stop-opacity:0.5"/>
      <stop offset="80%" style="stop-color:{scheme['colors'][1]};stop-opacity:0.3"/>
      <stop offset="100%" style="stop-color:{scheme['colors'][0]};stop-opacity:0.1"/>
    </radialGradient>
  </defs>
  
  <!-- Background -->
  <rect x="0" y="0" width="{width + 120}" height="{height + 120}" fill="white"/>
  
  <!-- Title -->
  <text x="{(width + 120) / 2}" y="40" class="title">{title}</text>
  
  <!-- Plot area background -->
  <rect x="{margin}" y="{margin}" width="{plot_width}" height="{plot_height}" 
        fill="#fafafa" stroke="none"/>
'''
    
    # Create smooth density visualization using circles with gradients
    cell_width = plot_width / bins
    cell_height = plot_height / bins
    
    # Find peaks for circle placement
    threshold = 0.1  # Only show circles above this density threshold
    
    for i in range(bins):
        for j in range(bins):
            density_val = density[j, i]  # Note: j,i because density is transposed
            
            if density_val > threshold:
                # Calculate position
                x_center = margin + (i + 0.5) * cell_width
                y_center = margin + (bins - 1 - j + 0.5) * cell_height
                
                # Circle size based on density
                max_radius = min(cell_width, cell_height) * 0.8
                radius = max_radius * math.sqrt(density_val)
                
                # Color intensity based on density
                opacity = 0.3 + 0.7 * density_val
                color_idx = min(4, int(density_val * 4))
                color = scheme['colors'][color_idx]
                
                svg_content += f'''  <circle cx="{x_center:.1f}" cy="{y_center:.1f}" r="{radius:.1f}" 
        fill="{color}" opacity="{opacity:.3f}" stroke="none"/>
'''
    
    # Add contour lines (simplified)
    contour_levels = [0.2, 0.4, 0.6, 0.8]
    
    for level in contour_levels:
        # Find approximate contour paths (simplified approach)
        level_points = []
        
        for i in range(0, bins-1, 3):  # Sample every 3rd point for performance
            for j in range(0, bins-1, 3):
                if abs(density[j, i] - level) < 0.1:
                    x = margin + (i + 0.5) * cell_width
                    y = margin + (bins - 1 - j + 0.5) * cell_height
                    level_points.append((x, y))
        
        # Draw contour points as small circles
        if level_points:
            for x, y in level_points[::2]:  # Use every other point
                svg_content += f'''  <circle cx="{x:.1f}" cy="{y:.1f}" r="1" 
        fill="{scheme['contour_color']}" opacity="0.4"/>
'''
    
    # Add diagonal reference line
    x1, y1 = margin, margin + plot_height
    x2, y2 = margin + plot_width, margin
    svg_content += f'''  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
        stroke="#666666" stroke-width="2" stroke-dasharray="8,4" opacity="0.6"/>
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
    
    # Add legend/colorbar representation
    legend_x = width + 20
    legend_y = margin + 50
    legend_height = 200
    
    svg_content += f'''  <!-- Legend -->
  <text x="{legend_x + 30}" y="{legend_y - 10}" class="axis-label">Density</text>
  
  <!-- Gradient legend -->
  <defs>
    <linearGradient id="legendGradient" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:{scheme['colors'][0]};stop-opacity:0.3"/>
      <stop offset="25%" style="stop-color:{scheme['colors'][1]};stop-opacity:0.5"/>
      <stop offset="50%" style="stop-color:{scheme['colors'][2]};stop-opacity:0.7"/>
      <stop offset="75%" style="stop-color:{scheme['colors'][3]};stop-opacity:0.8"/>
      <stop offset="100%" style="stop-color:{scheme['colors'][4]};stop-opacity:0.9"/>
    </linearGradient>
  </defs>
  
  <rect x="{legend_x}" y="{legend_y}" width="20" height="{legend_height}" 
        fill="url(#legendGradient)" stroke="black" stroke-width="1"/>
  
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
        
        # Skip if this interaction strength data doesn't exist yet
        if u not in all_results:
            print(f"  Skipping u = {u} (data not available yet)")
            processed_data[u] = {
                'u_coords': np.array([]),
                'v_coords': np.array([]),
                'classification': {'dominance': 0, 'mixing': 0, 'restructuring': 0, 'total': 0},
                'statistics': {'u_mean': 0, 'u_std': 0, 'v_mean': 0, 'v_std': 0}
            }
            continue
        
        all_u_coords = []
        all_v_coords = []
        
        # Classification counters
        dominance_count = 0
        mixing_count = 0
        restructuring_count = 0
        
        # Process each repetition
        rep_count = 0
        valid_pairs = 0
        
        for rep_key in all_results[u].keys():
            rep_data = all_results[u][rep_key]
            rep_count += 1
            
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
                            valid_pairs += 1
                            
                            # Classify outcome
                            x, y = calculate_assymetricity(u_coord, v_coord, k)
                            class_type = characterize_case(x, y)
                            
                            if class_type == 0:
                                dominance_count += 1
                            elif class_type == 1:
                                mixing_count += 1
                            else:
                                restructuring_count += 1
                                
                    except Exception as e:
                        # Skip problematic cases
                        pass
        
        # Convert to numpy arrays
        all_u_coords = np.array(all_u_coords)
        all_v_coords = np.array(all_v_coords)
        
        total_points = len(all_u_coords)
        
        print(f"  Repetitions processed: {rep_count}")
        print(f"  Valid coalescence pairs: {valid_pairs}")
        print(f"  Total data points: {total_points}")
        
        if total_points > 0:
            print(f"  Classification:")
            print(f"    Dominance:     {dominance_count:4d} ({100*dominance_count/total_points:5.1f}%)")
            print(f"    Mixing:        {mixing_count:4d} ({100*mixing_count/total_points:5.1f}%)")
            print(f"    Restructuring: {restructuring_count:4d} ({100*restructuring_count/total_points:5.1f}%)")
            
            # Statistics
            print(f"  Coordinate statistics:")
            print(f"    u: mean={np.mean(all_u_coords):.3f}, std={np.std(all_u_coords):.3f}")
            print(f"    v: mean={np.mean(all_v_coords):.3f}, std={np.std(all_v_coords):.3f}")
        
        # Store processed data
        processed_data[u] = {
            'u_coords': all_u_coords,
            'v_coords': all_v_coords,
            'classification': {
                'dominance': dominance_count,
                'mixing': mixing_count,
                'restructuring': restructuring_count,
                'total': total_points
            },
            'statistics': {
                'u_mean': float(np.mean(all_u_coords)) if total_points > 0 else 0,
                'u_std': float(np.std(all_u_coords)) if total_points > 0 else 0,
                'v_mean': float(np.mean(all_v_coords)) if total_points > 0 else 0,
                'v_std': float(np.std(all_v_coords)) if total_points > 0 else 0
            }
        }
    
    return processed_data


def main():
    """Main function to create smooth contour heatmaps"""
    
    print("="*80)
    print("CREATING SMOOTH CONTOUR HEATMAPS FROM 100-REPETITION DATA")
    print("="*80)
    
    # Look for 100-repetition data file
    data_files = [
        "Simulation_Data/48species_100reps_final/Community_100reps_final.json",
        "Simulation_Data/48species_100reps/Community_100reps.json"
    ]
    
    data_file = None
    for f in data_files:
        if os.path.exists(f):
            data_file = f
            break
    
    if data_file is None:
        print("❌ No 100-repetition data found. Using test data instead...")
        data_file = "Analysis_Results/processed_test_data.json"
        
        if not os.path.exists(data_file):
            print("❌ No data available for plotting")
            return
        
        # Load test data directly
        with open(data_file, 'r') as f:
            processed_data = json.load(f)
        
        # Convert to expected format
        for u in processed_data:
            processed_data[u]['u_coords'] = np.array(processed_data[u]['u_coords'])
            processed_data[u]['v_coords'] = np.array(processed_data[u]['v_coords'])
    else:
        # Process 100-repetition data
        processed_data = process_100rep_data(data_file)
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")

    # Create smooth contour heatmaps
    u_values = ['0.3', '0.6', '0.8']
    colors = ['blue', 'orange', 'red']
    labels = ['Low Interaction', 'Medium Interaction', 'High Interaction']
    
    plots_created = 0
    
    print(f"\n📊 Creating smooth contour heatmaps...")
    
    for u, color, label in zip(u_values, colors, labels):
        data = processed_data[u]
        u_coords = data['u_coords']
        v_coords = data['v_coords']
        
        if len(u_coords) > 0:
            title = f"Coalescence Outcomes: {label} (u = {u}) - High Sigma"
            output_file = f"{output_dir}/VectorDecomp_smooth_u{u}_highsigma.svg"
            
            success = create_svg_contour_heatmap(u_coords, v_coords, title, color, output_file, bins=80)
            if success:
                plots_created += 1
                print(f"✅ Created high sigma plot: VectorDecomp_smooth_u{u}_highsigma.svg")
        else:
            print(f"⏳ No data for u = {u} (simulation still running or not started yet)")
    
    # Create summary
    summary_file = f"{output_dir}/SMOOTH_CONTOUR_SUMMARY.txt"
    with open(summary_file, 'w') as f:
        f.write("SMOOTH CONTOUR HEATMAPS - 100 REPETITION ANALYSIS\n")
        f.write("=" * 55 + "\n\n")
        
        f.write("VISUALIZATION FEATURES:\n")
        f.write("- Smooth, continuous density representation\n")
        f.write("- Gaussian-filtered density fields\n")
        f.write("- Contour-style appearance with gradients\n")
        f.write("- High-resolution bins for smooth appearance\n\n")
        
        f.write("RESULTS SUMMARY:\n")
        f.write(f"{'Strength':>8} {'Dominance':>10} {'Mixing':>10} {'Restructuring':>12} {'Total':>8}\n")
        f.write("-" * 55 + "\n")
        
        for u in u_values:
            data = processed_data[u]
            cls = data['classification']
            total = cls['total']
            if total > 0:
                dom_pct = 100 * cls['dominance'] / total
                mix_pct = 100 * cls['mixing'] / total
                res_pct = 100 * cls['restructuring'] / total
                
                f.write(f"u = {u:>4} {dom_pct:>8.1f}% {mix_pct:>8.1f}% {res_pct:>10.1f}% {total:>6d}\n")
    
    print(f"✅ Created summary: {summary_file}")
    
    # Final summary
    print(f"\n" + "="*80)
    print(f"SMOOTH CONTOUR HEATMAPS COMPLETE!")
    print(f"="*80)
    print(f"📊 Plots created: {plots_created}")
    print(f"📁 Output directory: {output_dir}")
    
    print(f"\n✅ Generated smooth contour files:")
    for filename in sorted(os.listdir(output_dir)):
        if 'smooth' in filename or 'contour' in filename:
            print(f"   - {filename}")
    
    print(f"\n🎯 Features of smooth contour plots:")
    print(f"   - Continuous density gradients")
    print(f"   - Smooth contour-like appearance")
    print(f"   - High-resolution visualization")
    print(f"   - Publication-ready SVG format")


if __name__ == "__main__":
    main()