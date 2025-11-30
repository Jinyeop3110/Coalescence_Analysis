#!/usr/bin/env python3
"""
Create a separate colorbar SVG file for radial plots
"""

import os

def create_radial_colorbar_svg(output_file, orientation='vertical'):
    """Create colorbar SVG for radial plots"""
    
    print(f"Creating radial plot colorbar: {os.path.basename(output_file)}")
    
    # Actual colormap from radial contour plots (dark red to light peach)
    colors = ['#802000', '#9a4a30', '#c08674', '#e4c0b6', '#ffebe6']
    
    if orientation == 'vertical':
        # Vertical colorbar dimensions
        width = 60
        height = 200
        bar_width = 20
        bar_height = height - 40
        bar_x = 20
        bar_y = 20
        
        # Title and labels
        title_x = width / 2
        title_y = 15
        
        # Tick positions for vertical bar
        tick_positions = [0, 0.25, 0.5, 0.75, 1.0]
        tick_labels = ['0', '0.25', '0.5', '0.75', '1']
        
    else:  # horizontal
        # Horizontal colorbar dimensions
        width = 200
        height = 60
        bar_width = width - 40
        bar_height = 20
        bar_x = 20
        bar_y = 20
        
        # Title and labels
        title_x = width / 2
        title_y = 15
        
        # Tick positions for horizontal bar
        tick_positions = [0, 0.25, 0.5, 0.75, 1.0]
        tick_labels = ['0', '0.25', '0.5', '0.75', '1']
    
    # Start SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title {{ font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; fill: #333; }}
      .tick-label {{ font-family: Arial, sans-serif; font-size: 10px; text-anchor: middle; fill: #333; }}
    </style>
    
    <!-- Colorbar gradient -->
    <linearGradient id="colorbarGradient" x1="{0 if orientation == 'vertical' else 0}%" y1="{100 if orientation == 'vertical' else 0}%" x2="{0 if orientation == 'vertical' else 100}%" y2="{0 if orientation == 'vertical' else 0}%">
      <stop offset="0%" style="stop-color:{colors[0]};stop-opacity:1"/>
      <stop offset="25%" style="stop-color:{colors[1]};stop-opacity:1"/>
      <stop offset="50%" style="stop-color:{colors[2]};stop-opacity:1"/>
      <stop offset="75%" style="stop-color:{colors[3]};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:{colors[4]};stop-opacity:1"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  
  
  <!-- Colorbar rectangle -->
  <rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="{bar_height}" 
        fill="url(#colorbarGradient)" stroke="#333" stroke-width="0.5"/>
'''
    
    # Add ticks and labels
    if orientation == 'vertical':
        for i, (tick_pos, label) in enumerate(zip(tick_positions, tick_labels)):
            y_pos = bar_y + bar_height - (tick_pos * bar_height)
            tick_x = bar_x + bar_width
            label_x = tick_x + 5
            
            svg_content += f'''  <!-- Tick {i} -->
  <line x1="{tick_x}" y1="{y_pos}" x2="{tick_x + 3}" y2="{y_pos}" stroke="#333" stroke-width="0.5"/>
  <text x="{label_x}" y="{y_pos + 3}" class="tick-label" text-anchor="start">{label}</text>
'''
    else:  # horizontal
        for i, (tick_pos, label) in enumerate(zip(tick_positions, tick_labels)):
            x_pos = bar_x + (tick_pos * bar_width)
            tick_y = bar_y + bar_height
            label_y = tick_y + 15
            
            svg_content += f'''  <!-- Tick {i} -->
  <line x1="{x_pos}" y1="{tick_y}" x2="{x_pos}" y2="{tick_y + 3}" stroke="#333" stroke-width="0.5"/>
  <text x="{x_pos}" y="{label_y}" class="tick-label">{label}</text>
'''
    
    # Close SVG
    svg_content += '''
</svg>'''
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    return True

def main():
    """Create both vertical and horizontal colorbars"""
    
    print("="*60)
    print("CREATING RADIAL PLOT COLORBARS")
    print("="*60)
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim_heatmaps_moresamples"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create vertical colorbar
    vertical_file = f"{output_dir}/radial_colorbar_vertical.svg"
    success_v = create_radial_colorbar_svg(vertical_file, orientation='vertical')
    
    # Create horizontal colorbar  
    horizontal_file = f"{output_dir}/radial_colorbar_horizontal.svg"
    success_h = create_radial_colorbar_svg(horizontal_file, orientation='horizontal')
    
    print(f"\n📁 Output directory: {output_dir}")
    
    colorbars_created = 0
    if success_v:
        colorbars_created += 1
        print(f"✅ Created: radial_colorbar_vertical.svg")
    if success_h:
        colorbars_created += 1
        print(f"✅ Created: radial_colorbar_horizontal.svg")
    
    print(f"\n" + "="*60)
    print(f"RADIAL COLORBARS CREATED: {colorbars_created}")
    print("="*60)
    print("🎯 Features:")
    print("   - Colormap: viridis-like (#440154 → #ff6b35)")
    print("   - Range: 0 to 1 (normalized density)")
    print("   - Available: vertical and horizontal orientations")
    print("   - Style: matches radial plot aesthetics")

if __name__ == "__main__":
    main()