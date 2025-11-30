#!/usr/bin/env python
"""
Create 500-species phase diagram SVG matching the exact style of existing phase diagrams.
Replicates: Fig_phase_diagram_Simul_k_gaussian_0.25.svg format
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime


def classify_vector_decomposition(a, b, c):
    """Classify coalescence outcome."""
    total = a + b + c
    if total > 0:
        a_norm = a / total
        b_norm = b / total
        c_norm = c / total
    else:
        return 2
    
    abs_diff = abs(a_norm - b_norm)
    if c_norm > 0.0004:
        return 2  # Restructuring
    elif abs_diff > 0.0008:
        return 0  # Dominance
    else:
        return 1  # Mixing


def create_matplotlib_style_svg():
    """Create SVG matching matplotlib output exactly."""
    
    print("Creating matplotlib-style 500-species phase diagram...")
    
    # Load and process data
    file_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural_full/Similarity.xlsx"
    data1 = pd.read_excel(file_path, sheet_name=0)
    data2 = pd.read_excel(file_path, sheet_name=1)  
    data3 = pd.read_excel(file_path, sheet_name=2)
    
    # Extract u-values
    u_values = []
    for col in data1.columns:
        if col.startswith('u_'):
            u_val = float(col.split('_')[1])
            u_values.append(u_val)
    u_values = sorted(u_values)
    
    # Process data and calculate fractions
    fractions_data = []
    
    for u_val in u_values:
        col_name = f"u_{u_val}"
        if col_name in data1.columns:
            a_values = data1[col_name].dropna().values
            b_values = data2[col_name].dropna().values
            c_values = data3[col_name].dropna().values
            
            min_length = min(len(a_values), len(b_values), len(c_values))
            if min_length > 0:
                # Classify
                classifications = [classify_vector_decomposition(a_values[j], b_values[j], c_values[j]) 
                                 for j in range(min_length)]
                classifications = np.array(classifications)
                
                n_dominance = np.sum(classifications == 0)
                n_mixing = np.sum(classifications == 1)
                n_restructuring = np.sum(classifications == 2)
                total = len(classifications)
                
                dom_frac = n_dominance / total if total > 0 else 0
                mix_frac = n_mixing / total if total > 0 else 0
                res_frac = n_restructuring / total if total > 0 else 0
                
                fractions_data.append({
                    'u': u_val,
                    'dominance': dom_frac,
                    'mixing': mix_frac,
                    'restructuring': res_frac
                })
    
    # Matplotlib-style dimensions (matching reference)
    width_pt = 177.58425
    height_pt = 158.917775
    
    # Plot area coordinates (from reference)
    plot_left = 33.13625
    plot_right = 164.82425
    plot_bottom = 140.901525
    plot_top = 10.063125
    
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    # Colors matching the reference (with opacity)
    colors = {
        'dominance': '#e57373',      # Red from reference
        'mixing': '#ba68c8',         # Purple from reference  
        'restructuring': '#81c784'   # Green from reference
    }
    
    # Create matplotlib-style SVG
    current_time = datetime.now().isoformat()
    
    svg_content = f'''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns:xlink="http://www.w3.org/1999/xlink" width="{width_pt}pt" height="{height_pt}pt" viewBox="0 0 {width_pt} {height_pt}" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <metadata>
  <rdf:RDF xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <cc:Work>
    <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>
    <dc:date>{current_time}</dc:date>
    <dc:format>image/svg+xml</dc:format>
    <dc:creator>
     <cc:Agent>
      <dc:title>500-species phase diagram (Claude generated)</dc:title>
     </cc:Agent>
    </cc:creator>
   </cc:Work>
  </rdf:RDF>
 </metadata>
 <defs>
  <style type="text/css">*{{stroke-linejoin: round; stroke-linecap: butt}}</style>
  <clipPath id="p500species">
   <rect x="{plot_left}" y="{plot_top}" width="{plot_width}" height="{plot_height}"/>
  </clipPath>
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
   </g>'''
    
    # X-axis ticks and labels
    n_bars = len(fractions_data)
    bar_width = plot_width / n_bars
    
    svg_content += '\n   <g id="matplotlib.axis_1">'
    
    for i, data_point in enumerate(fractions_data):
        x_center = plot_left + (i + 0.5) * bar_width
        
        # X-tick
        svg_content += f'''
    <g id="xtick_{i+1}">
     <g id="line2d_{i+1}">
      <defs>
       <path id="tick_{i+1}" d="M 0 0 
L 0 -3.5 
" style="stroke: #262626; stroke-width: 0.5"/>
      </defs>
      <g>
       <use xlink:href="#tick_{i+1}" x="{x_center}" y="{plot_bottom}" style="fill: #262626; stroke: #262626; stroke-width: 0.5"/>
      </g>
     </g>
     <g id="text_{i+1}">
      <text x="{x_center}" y="{plot_bottom + 15}" text-anchor="middle" style="font-family: Arial, sans-serif; font-size: 10px; fill: #262626">{data_point['u']:.1f}</text>
     </g>
    </g>'''
    
    # Y-axis ticks
    for j in range(6):  # 0.0 to 1.0
        y_val = j * 0.2
        y_pos = plot_bottom - (y_val * plot_height)
        
        svg_content += f'''
    <g id="ytick_{j+1}">
     <g>
      <path d="M 0 0 L 3.5 0" x="{plot_left}" y="{y_pos}" style="stroke: #262626; stroke-width: 0.5; fill: none"/>
     </g>
     <g>
      <text x="{plot_left - 8}" y="{y_pos + 3}" text-anchor="end" style="font-family: Arial, sans-serif; font-size: 10px; fill: #262626">{y_val:.1f}</text>
     </g>
    </g>'''
    
    svg_content += '\n   </g>'
    
    # Plot the stacked bars
    for i, data_point in enumerate(fractions_data):
        x_left = plot_left + i * bar_width
        x_right = plot_left + (i + 1) * bar_width
        
        # Calculate heights
        dom_height = data_point['dominance'] * plot_height
        mix_height = data_point['mixing'] * plot_height
        res_height = data_point['restructuring'] * plot_height
        
        # Stack from bottom: dominance, mixing, restructuring
        y_bottom = plot_bottom
        
        # Dominance bar (bottom, red)
        if dom_height > 0:
            y_top = y_bottom - dom_height
            svg_content += f'''
   <g id="patch_dominance_{i}">
    <path d="M {x_left} {y_bottom} 
L {x_right} {y_bottom} 
L {x_right} {y_top} 
L {x_left} {y_top} 
z
" clip-path="url(#p500species)" style="fill: {colors['dominance']}; fill-opacity: 0.85"/>
   </g>'''
            y_bottom = y_top
        
        # Mixing bar (middle, purple)
        if mix_height > 0:
            y_top = y_bottom - mix_height
            svg_content += f'''
   <g id="patch_mixing_{i}">
    <path d="M {x_left} {y_bottom} 
L {x_right} {y_bottom} 
L {x_right} {y_top} 
L {x_left} {y_top} 
z
" clip-path="url(#p500species)" style="fill: {colors['mixing']}; fill-opacity: 0.85"/>
   </g>'''
            y_bottom = y_top
        
        # Restructuring bar (top, green)
        if res_height > 0:
            y_top = y_bottom - res_height
            svg_content += f'''
   <g id="patch_restructuring_{i}">
    <path d="M {x_left} {y_bottom} 
L {x_right} {y_bottom} 
L {x_right} {y_top} 
L {x_left} {y_top} 
z
" clip-path="url(#p500species)" style="fill: {colors['restructuring']}; fill-opacity: 0.85"/>
   </g>'''
    
    # Axis borders (matching reference style)
    svg_content += f'''
   <g id="patch_left">
    <path d="M {plot_left} {plot_bottom} 
L {plot_left} {plot_top} 
" style="fill: none; stroke: #262626; stroke-width: 0.5; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_right">
    <path d="M {plot_right} {plot_bottom} 
L {plot_right} {plot_top} 
" style="fill: none; stroke: #262626; stroke-width: 0.5; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_bottom">
    <path d="M {plot_left} {plot_bottom} 
L {plot_right} {plot_bottom} 
" style="fill: none; stroke: #262626; stroke-width: 0.5; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_top">
    <path d="M {plot_left} {plot_top} 
L {plot_right} {plot_top} 
" style="fill: none; stroke: #262626; stroke-width: 0.5; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
</svg>'''
    
    # Save the file
    output_file = Path("Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500.svg")
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"✅ Matplotlib-style SVG created: {output_file}")
    print(f"   Dimensions: {width_pt:.1f} × {height_pt:.1f} pt")
    print(f"   Colors: Red (dominance), Purple (mixing), Green (restructuring)")
    print(f"   Style: Matches Fig_phase_diagram_Simul_k_gaussian_0.25.svg format")


if __name__ == "__main__":
    create_matplotlib_style_svg()