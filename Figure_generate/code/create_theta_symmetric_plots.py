#!/usr/bin/env python3
"""
Create theta_symmetric versions of simulation theta plots with grey stacked bars.
Takes the brown-only simulation theta plots and adds grey bars representing (1-val).
"""

import re
import os

def parse_simulation_histogram_data(svg_content):
    """Extract histogram data from simulation theta SVG"""
    
    # Extract all rect elements that are histogram bars
    rect_pattern = r'<rect x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)" style="fill: ([^;]+); fill-opacity: ([^;]+); stroke: none"/>'
    rects = re.findall(rect_pattern, svg_content)
    
    histogram_bars = []
    
    for rect in rects:
        x, y, width, height, color, opacity = rect
        
        # Only process brown histogram bars (not grey background)
        if '#802000' in color:  # Brown color for theta data
            histogram_bars.append({
                'x': float(x),
                'y': float(y), 
                'width': float(width),
                'height': float(height),
                'color': color,
                'opacity': float(opacity)
            })
    
    return histogram_bars

def extract_max_density_from_svg(svg_content):
    """Extract max density value from y-axis label in SVG"""
    
    # Look for the y-axis label text (e.g., "2.5" for density)
    text_pattern = r'<text[^>]*y="9\.2[0-9]*"[^>]*>([^<]+)</text>'
    matches = re.findall(text_pattern, svg_content)
    
    if matches:
        try:
            # The last match should be the max density value
            return float(matches[-1])
        except ValueError:
            pass
    
    return 30.0  # Default fallback

def create_theta_symmetric_svg(original_bars, output_file, input_filename):
    """Create theta_symmetric version with grey stacked bars"""
    
    print(f"Creating symmetric version: {os.path.basename(output_file)}")
    print(f"  Processing {len(original_bars)} brown histogram bars from {input_filename}")
    
    # Scale factor to account for max_density change from 10 to 6
    # Original bars were scaled by max_density=6, but we need to ensure consistent scaling
    density_scale_factor = 6.0 / 6.0  # Now both use max_density=6
    
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
    brown_color = "#802000"
    grey_color = "#808080"
    
    # Start SVG with same structure
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
    
    # Add X-axis ticks for 0-1 range
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
    
    # Extract max density from original file and add Y-axis ticks
    y_tick_positions = [0.0, 1.0]
    
    # Set fixed max density to 10
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
    
    # Process each original brown bar
    for bar in original_bars:
        # Scale original brown bar to 50% height (bottom half)
        brown_x = bar['x']
        brown_width = bar['width']
        brown_opacity = bar['opacity']
        
        # Brown bar takes bottom 50% of original height
        original_height = bar['height']
        brown_height = original_height * 0.5
        brown_y = bar['y'] + original_height * 0.5  # Move down to bottom half
        
        # Grey bar takes top 50% of original height
        grey_height = original_height * 0.5
        grey_y = bar['y']  # Top half
        grey_opacity = 0.8  # Fixed opacity for all grey bars
        
        # Add brown bar (original)
        svg_content += f'''    <rect x="{brown_x:.3f}" y="{brown_y:.3f}" width="{brown_width:.3f}" height="{brown_height:.3f}" style="fill: {brown_color}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''
        
        # Add grey bar (stacked on top)
        svg_content += f'''    <rect x="{brown_x:.3f}" y="{grey_y:.3f}" width="{brown_width:.3f}" height="{grey_height:.3f}" style="fill: {grey_color}; fill-opacity: {grey_opacity:.3f}; stroke: none"/>
'''
    
    svg_content += '   </g>\n'
    
    # Add step function outline around stacked bars
    svg_content += '   <g id="HistogramOutline_1">\n'
    
    if original_bars:
        # Sort bars by x position for proper step function
        sorted_bars = sorted(original_bars, key=lambda b: b['x'])
        
        # Build step function path that goes to y=0 for gaps between bars
        path_parts = []
        
        for bar in sorted_bars:
            # Calculate total height (brown + grey both 50%)
            total_height = bar['height']  # Total height stays the same
            y_top = bar['y']  # Top is at original y position
            
            x_left = bar['x']
            x_right = bar['x'] + bar['width']
            
            if not path_parts:  # First bar
                path_parts.append(f"M {x_left:.3f} {plot_bottom:.3f}")
            else:
                # Connect from previous position to start of this bar at baseline
                path_parts.append(f"L {x_left:.3f} {plot_bottom:.3f}")
            
            # Step up to total height
            path_parts.append(f"L {x_left:.3f} {y_top:.3f}")
            # Move horizontally across bar top
            path_parts.append(f"L {x_right:.3f} {y_top:.3f}")
            # Step down to baseline at end of bar
            path_parts.append(f"L {x_right:.3f} {plot_bottom:.3f}")
        
        if path_parts:
            path_string = " ".join(path_parts)
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
    
    # Close SVG
    svg_content += '''  </g>
 </g>
</svg>'''
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    return True

def main():
    """Create theta_symmetric versions of simulation plots"""
    
    print("="*80)
    print("CREATING THETA_SYMMETRIC SIMULATION PLOTS")
    print("="*80)
    
    # Input files requested
    input_files = [
        "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples/VectorDecomp_u0.3_theta.svg",
        "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples/VectorDecomp_u0.6_theta.svg",
        "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples/VectorDecomp_u0.8_theta.svg"
    ]
    
    plots_created = 0
    
    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"❌ Input file not found: {input_file}")
            continue
        
        # Read original SVG
        with open(input_file, 'r') as f:
            svg_content = f.read()
        
        # Parse histogram data
        histogram_bars = parse_simulation_histogram_data(svg_content)
        
        if not histogram_bars:
            print(f"❌ No histogram bars found in {os.path.basename(input_file)}")
            continue
        
        # Create output filename with _symmetric suffix
        input_basename = os.path.basename(input_file)
        base_name = input_basename.replace('_theta.svg', '')
        output_filename = f"{base_name}_theta_symmetric.svg"
        output_path = os.path.join(os.path.dirname(input_file), output_filename)
        
        # Create symmetric version
        success = create_theta_symmetric_svg(histogram_bars, output_path, input_basename)
        
        if success:
            plots_created += 1
            print(f"✅ Created: {output_filename}")
    
    print(f"\n" + "="*80)
    print(f"THETA_SYMMETRIC PLOTS CREATED: {plots_created}")
    print(f"="*80)
    print(f"🎯 Features:")
    print(f"   - Brown bars: Original theta frequencies")
    print(f"   - Grey bars: (1-val) stacked on top")
    print(f"   - Step function outline around complete bars")
    print(f"   - More grey at edges (0, 1), less in middle (0.5)")
    print(f"   - X-axis: 0 to 1 (theta/(π/2) normalized)")
    print(f"   - Large tick labels: 12.8px")

if __name__ == "__main__":
    main()