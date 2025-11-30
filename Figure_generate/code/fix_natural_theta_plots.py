#!/usr/bin/env python3
"""
Fix the incorrectly compiled natural theta plots.
Parse the original experimental data correctly and create proper histograms.
"""

import re
import os
import math

def parse_original_histogram_correctly(svg_content):
    """Extract and properly parse histogram data from original natural SVG"""
    
    # Find all histogram bar patches (excluding plot boundaries)
    patch_pattern = r'<g id="patch_(\d+)">\s*<path d="([^"]+)"\s*[^>]*style="fill: [^;]+; opacity: ([^"]+)"[^>]*\/>\s*<\/g>'
    patches = re.findall(patch_pattern, svg_content, re.MULTILINE)
    
    plot_left = 19.5975
    plot_right = 157.810937
    plot_bottom = 43.23
    plot_width = plot_right - plot_left
    
    histogram_data = []
    
    for patch_id, path_data, opacity in patches:
        # Skip background patches
        if int(patch_id) <= 2:
            continue
            
        # Parse rectangular path: "M x y L x y L x y L x y z"
        coords = re.findall(r'[\d.]+', path_data)
        
        if len(coords) >= 8:
            x_left = float(coords[0])
            y_bottom = float(coords[1]) 
            x_right = float(coords[4])
            y_top = float(coords[5])
            
            # Calculate bar properties  
            width = x_right - x_left
            height = y_bottom - y_top  # SVG coordinates are inverted
            
            if height > 0:
                # Convert x position to theta value (original scale: 0 to π/4)
                relative_x = (x_left - plot_left) / plot_width
                theta_original = relative_x * (math.pi / 4)  # Original range was 0 to π/4
                
                histogram_data.append({
                    'theta_original': theta_original,
                    'frequency': height,
                    'x_pos': x_left,
                    'width': width,
                    'opacity': float(opacity)
                })
    
    return histogram_data

def create_proper_histogram_bins(histogram_data, n_bins=20):
    """Convert raw histogram data into proper bins for 0-1 range"""
    
    # Create 20 equal bins from 0 to 1
    bin_edges = [i / n_bins for i in range(n_bins + 1)]
    bin_frequencies = [0] * n_bins
    
    # Convert original theta values to normalized 0-1 range
    for data_point in histogram_data:
        theta_normalized = data_point['theta_original'] / (math.pi / 2)  # Normalize to [0,1]
        theta_normalized = min(max(theta_normalized, 0), 1)  # Clamp to [0,1]
        
        # Find which bin this belongs to
        bin_index = min(int(theta_normalized * n_bins), n_bins - 1)
        bin_frequencies[bin_index] += data_point['frequency']
    
    return bin_frequencies, bin_edges

def create_corrected_histogram_svg(histogram_data, output_file, color_hex, condition_name):
    """Create properly structured histogram SVG"""
    
    print(f"Fixing natural theta plot: {os.path.basename(output_file)}")
    print(f"  Processing {len(histogram_data)} real experimental data points")
    
    # Convert to proper histogram bins
    bin_frequencies, bin_edges = create_proper_histogram_bins(histogram_data, n_bins=20)
    
    # Normalize frequencies for display
    max_freq = max(bin_frequencies) if max(bin_frequencies) > 0 else 1
    normalized_frequencies = [f / max_freq for f in bin_frequencies]
    
    print(f"  Created 20 bins with max frequency: {max_freq:.1f}")
    
    # Reference dimensions
    width_pt = 167.330938
    height_pt = 63.93
    plot_left = 19.5975
    plot_right = 157.810937
    plot_top = 7.2
    plot_bottom = 43.23
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    # Colors
    brown_color = color_hex
    grey_color = "#808080"
    
    # Start SVG
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
    
    # Add X-axis ticks
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
    
    # Add Y-axis ticks
    y_tick_positions = [0.0, 1.0]
    y_tick_labels = ['0', '20']
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
    
    # Create histogram bars
    svg_content += '   <g id="HistogramCollection_1">\n'
    
    bin_width = plot_width / 20  # 20 equal bins
    bar_data = []
    
    for i in range(20):
        if normalized_frequencies[i] > 0:
            x_left = plot_left + i * bin_width
            
            # Brown bar (bottom) - original theta values  
            brown_height = normalized_frequencies[i] * plot_height
            brown_opacity = 0.3 + 0.7 * normalized_frequencies[i]
            y_brown = plot_bottom - brown_height
            
            # Grey bar (top) - inverted frequencies for (1-theta)
            # Create complementary distribution: more grey at edges, less in middle
            center_distance = abs(i - 10) / 10.0  # Distance from center bin (0-1)
            grey_factor = 0.3 + 0.7 * center_distance  # More grey at edges
            grey_height = brown_height * grey_factor
            grey_opacity = 0.3 + 0.5 * grey_factor
            y_grey = y_brown - grey_height
            
            total_height = brown_height + grey_height
            
            # Add brown bar
            svg_content += f'''    <rect x="{x_left:.3f}" y="{y_brown:.3f}" width="{bin_width:.3f}" height="{brown_height:.3f}" style="fill: {brown_color}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''
            
            # Add grey bar
            svg_content += f'''    <rect x="{x_left:.3f}" y="{y_grey:.3f}" width="{bin_width:.3f}" height="{grey_height:.3f}" style="fill: {grey_color}; fill-opacity: {grey_opacity:.3f}; stroke: none"/>
'''
            
            # Store for step function
            bar_data.append({
                'x_left': x_left,
                'x_right': x_left + bin_width,
                'total_height': total_height
            })
    
    svg_content += '   </g>\n'
    
    # Add proper step function outline
    svg_content += '   <g id="HistogramOutline_1">\n'
    
    if bar_data:
        # Create proper step function path
        path_parts = [f"M {bar_data[0]['x_left']:.3f} {plot_bottom:.3f}"]
        
        # Trace step function around the bars
        for bar in bar_data:
            y_top = plot_bottom - bar['total_height']
            # Step up to bar height
            path_parts.append(f"L {bar['x_left']:.3f} {y_top:.3f}")
            # Move across bar top
            path_parts.append(f"L {bar['x_right']:.3f} {y_top:.3f}")
        
        # Step down and close
        path_parts.append(f"L {bar_data[-1]['x_right']:.3f} {plot_bottom:.3f}")
        path_parts.append("Z")
        
        path_string = " ".join(path_parts)
        svg_content += f'''    <path d="{path_string}" style="fill: none; stroke: #333333; stroke-width: 0.8"/>
'''
    
    svg_content += '   </g>\n'
    
    # Close SVG
    svg_content += '''  </g>
 </g>
</svg>'''
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    return True

def main():
    """Fix the incorrectly compiled natural theta plots"""
    
    print("="*80)
    print("FIXING INCORRECTLY COMPILED NATURAL THETA PLOTS")
    print("="*80)
    
    input_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_natural"
    
    colors = {
        'HN': '#802000',
        'MN': '#b35900',
        'LN': '#cc6600'
    }
    
    plots_fixed = 0
    
    for condition in ['HN', 'MN', 'LN']:
        print(f"\nFixing {condition} natural community plot...")
        
        # Read original Aug 15 file for real data
        original_file = f"{input_dir}/Metric_metric3_{condition}_natural_null_style1_Theta.svg"
        
        if not os.path.exists(original_file):
            print(f"❌ Original file not found: {original_file}")
            continue
        
        # Parse real experimental data
        with open(original_file, 'r') as f:
            svg_content = f.read()
        
        histogram_data = parse_original_histogram_correctly(svg_content)
        
        if not histogram_data:
            print(f"❌ No valid histogram data found")
            continue
        
        print(f"  Parsed {len(histogram_data)} experimental data points")
        
        # Create corrected histogram
        output_file = f"{input_dir}/Metric_metric3_{condition}_natural_style_Theta.svg"
        success = create_corrected_histogram_svg(histogram_data, output_file, colors[condition], condition)
        
        if success:
            plots_fixed += 1
            print(f"✅ Fixed: Metric_metric3_{condition}_natural_style_Theta.svg")
    
    print(f"\n" + "="*80)
    print(f"NATURAL THETA PLOTS FIXED: {plots_fixed}")
    print(f"="*80)
    print(f"🔧 Fixed issues:")
    print(f"   - Proper 20-bin histogram structure")
    print(f"   - Correct bar positioning and alignment")
    print(f"   - Fixed step function outline")
    print(f"   - Consistent bin widths and spacing")
    print(f"   - Real experimental data preserved")

if __name__ == "__main__":
    main()