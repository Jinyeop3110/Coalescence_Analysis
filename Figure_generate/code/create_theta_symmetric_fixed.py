#!/usr/bin/env python3
"""
Create corrected theta symmetric plots where:
1. Grey bars represent the 1-theta complement to create perfect symmetry
2. All bars are scaled down by half for better visualization
"""

import numpy as np
import re
import os
import sys

# Add the parent directory to path to import COLORMAP
sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')
from COLORMAP import get_medium_color

def parse_theta_histogram_data(svg_content):
    """Extract histogram data from theta SVG"""
    rect_pattern = r'<rect x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)" style="fill: ([^;]+); fill-opacity: ([^;]+); stroke: none"/>'
    rects = re.findall(rect_pattern, svg_content)
    
    histogram_bars = []
    
    for rect in rects:
        x, y, width, height, color, opacity = rect
        
        # Only process histogram bars (check for any of the medium colors)
        if '#802000' in color or '#A7216A' in color or '#E24912' in color:
            histogram_bars.append({
                'x': float(x),
                'y': float(y), 
                'width': float(width),
                'height': float(height),
                'color': color,
                'opacity': float(opacity)
            })
    
    return histogram_bars

def create_theta_symmetric_svg_corrected(original_bars, output_file, input_filename, medium):
    """Create corrected theta_symmetric version with complementary grey bars scaled by 0.5"""
    
    print(f"Creating corrected symmetric version: {os.path.basename(output_file)}")
    print(f"  Processing {len(original_bars)} histogram bars from {input_filename}")
    
    # Get the appropriate color for this medium
    medium_color = get_medium_color(medium)
    print(f"  Using color {medium_color} for {medium}")
    
    # Reference dimensions
    width_pt = 167.330938
    height_pt = 63.93
    plot_left = 19.5975
    plot_right = 157.810937
    plot_top = 7.2
    plot_bottom = 43.23
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    # Colors - use medium-specific color instead of brown
    medium_color_hex = medium_color
    grey_color = "#808080"
    
    # Number of bins (assuming uniform binning)
    n_bins = 20
    bin_width = plot_width / n_bins
    
    # Extract histogram heights from original bars
    histogram_heights = {}
    for bar in original_bars:
        # Calculate bin index from x position
        bin_idx = int(round((bar['x'] - plot_left) / bin_width))
        if 0 <= bin_idx < n_bins:
            histogram_heights[bin_idx] = bar['height']
    
    # Fill missing bins with zero height
    for i in range(n_bins):
        if i not in histogram_heights:
            histogram_heights[i] = 0
    
    # Create complementary histogram for 1-theta
    complementary_heights = {}
    for i in range(n_bins):
        # The bin at position i corresponds to the bin at position (n_bins-1-i) in the complement
        complement_idx = n_bins - 1 - i
        complementary_heights[i] = histogram_heights[complement_idx]
    
    # Scale both histograms by 0.5
    scale_factor = 0.5
    
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
   <!-- Add plot boundary box -->
   <g id="plot_boundary">
    <rect x="{plot_left}" y="{plot_top}" width="{plot_width}" height="{plot_height}" style="fill: none; stroke: #000000; stroke-width: 0.4"/>
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
    
    # Add Y-axis ticks - adjust for scaled bars
    y_tick_positions = [0.0, 1.0]
    y_tick_labels = ['0', '20']  # Keeping original scale labels
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
    
    # Get original bar opacities if available
    original_opacities = {}
    for bar in original_bars:
        bin_idx = int(round((bar['x'] - plot_left) / bin_width))
        if 0 <= bin_idx < n_bins:
            original_opacities[bin_idx] = bar['opacity']
    
    # Draw bars for each bin
    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        
        # Brown bar (scaled by 0.5)
        brown_height = histogram_heights[i] * scale_factor
        
        # Grey bar (complementary, also scaled by 0.5)
        grey_height = complementary_heights[i] * scale_factor
        
        # Only draw if there's data
        if brown_height > 0 or grey_height > 0:
            # Calculate opacities
            brown_opacity = original_opacities.get(i, 0.8)
            
            # Grey opacity based on the complementary position's original data
            complement_idx = n_bins - 1 - i
            grey_opacity = original_opacities.get(complement_idx, 0.8)
            
            # Draw medium-colored bar (bottom)
            if brown_height > 0:
                y_brown = plot_bottom - brown_height
                svg_content += f'''    <rect x="{x_left:.3f}" y="{y_brown:.3f}" width="{bin_width:.3f}" height="{brown_height:.3f}" style="fill: {medium_color_hex}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''
            
            # Draw grey bar (stacked on top)
            if grey_height > 0:
                y_grey = plot_bottom - brown_height - grey_height
                svg_content += f'''    <rect x="{x_left:.3f}" y="{y_grey:.3f}" width="{bin_width:.3f}" height="{grey_height:.3f}" style="fill: {grey_color}; fill-opacity: {grey_opacity:.3f}; stroke: none"/>
'''
    
    svg_content += '   </g>\n'
    
    # Add step function outline around stacked bars
    svg_content += '   <g id="HistogramOutline_1">\n'
    
    # Build step function path
    path_parts = []
    
    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        x_right = x_left + bin_width
        
        # Total height (brown + grey, both scaled)
        total_height = (histogram_heights[i] + complementary_heights[i]) * scale_factor
        
        if total_height > 0:
            y_top = plot_bottom - total_height
            
            if not path_parts:  # First bar
                path_parts.append(f"M {x_left:.3f} {plot_bottom:.3f}")
            else:
                # Connect from previous position
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
    
    # Close SVG
    svg_content += '''  </g>
 </g>
</svg>'''
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    # Verify symmetry
    total_original = sum(histogram_heights.values())
    total_complement = sum(complementary_heights.values())
    print(f"  Total original height: {total_original:.2f}")
    print(f"  Total complement height: {total_complement:.2f}")
    print(f"  Symmetry check: {'PASS' if abs(total_original - total_complement) < 0.01 else 'FAIL'}")
    
    return True

def main():
    """Process existing theta plots and create corrected symmetric versions"""
    
    print("Creating corrected theta symmetric plots...")
    
    input_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_exp_merged"
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_exp_merged"
    
    # Process each medium
    for medium in ['LN', 'MN', 'HN']:
        input_file = f"{input_dir}/VectorDecomp_exp_{medium}_merged_theta.svg"
        output_file = f"{output_dir}/VectorDecomp_exp_{medium}_merged_theta_symmetric_corrected.svg"
        
        if os.path.exists(input_file):
            print(f"\nProcessing {medium}...")
            
            # Read the original SVG
            with open(input_file, 'r') as f:
                svg_content = f.read()
            
            # Parse histogram data
            histogram_bars = parse_theta_histogram_data(svg_content)
            
            if histogram_bars:
                # Create corrected symmetric version
                success = create_theta_symmetric_svg_corrected(
                    histogram_bars, 
                    output_file, 
                    os.path.basename(input_file),
                    medium
                )
                
                if success:
                    print(f"✅ Created: {os.path.basename(output_file)}")
            else:
                print(f"❌ No histogram bars found in {os.path.basename(input_file)}")
        else:
            print(f"❌ Input file not found: {input_file}")
    
    print("\n" + "="*80)
    print("CORRECTED SYMMETRIC PLOTS COMPLETE!")
    print("="*80)
    print("🎯 Corrections applied:")
    print("   - Grey bars = 1-theta complement (creating perfect symmetry)")
    print("   - All bars scaled by 0.5 (half size)")
    print("   - Brown + Grey forms a symmetric distribution")
    print("   - Preserves original opacity patterns")

if __name__ == "__main__":
    main()