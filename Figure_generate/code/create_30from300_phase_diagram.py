#!/usr/bin/env python
"""
Create phase diagram for 30from300 k_gaussian_0.15 simulation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def classify_vector_decomposition_30from300(a, b, c):
    """
    Classify coalescence outcome for 30from300 data.
    Similar to 50from500 but adjusted for smaller community size.
    """
    # Normalize for classification
    total = a + b + c
    if total <= 0:
        return 2  # Default to restructuring
        
    a_norm = a / total
    b_norm = b / total
    c_norm = c / total
    
    # Classification thresholds for 30from300 system
    # Expect similar behavior to 50from500 but potentially more mixing
    c_threshold = 0.15  # Residual threshold
    diff_threshold = 0.25  # Dominance threshold
    
    if c_norm > c_threshold:
        return 2  # Restructuring
    elif abs(a_norm - b_norm) > diff_threshold:
        return 0  # Dominance
    else:
        return 1  # Mixing

def create_30from300_phase_diagram():
    """Create phase diagram for 30from300 k_gaussian_0.15 simulation."""
    
    print("📊 Creating 30from300 k_gaussian_0.15 phase diagram...")
    
    data_path = "Simulation_Data/new_k_gaussian_0.15_defined_pool_nooverlap_30from300_natural_full/Similarity.xlsx"
    output_path = "Figure/PhaseDiagram/Fig_phase_diagram_Simul_30from300_k_gaussian_0.15.svg"
    
    if not Path(data_path).exists():
        print(f"❌ Data file not found: {data_path}")
        return False
    
    # Read the Excel data
    data1 = pd.read_excel(data_path, sheet_name=0)  # Parent 1 coefficients
    data2 = pd.read_excel(data_path, sheet_name=1)  # Parent 2 coefficients  
    data3 = pd.read_excel(data_path, sheet_name=2)  # Residual magnitudes
    
    print(f"Data shapes: {data1.shape}, {data2.shape}, {data3.shape}")
    
    # Extract u-values from column names
    u_values = []
    for col in data1.columns:
        if col.startswith('u_'):
            u_val = float(col.split('_')[1])
            u_values.append(u_val)
    u_values = sorted(u_values)
    
    print(f"Found u-values: {u_values}")
    
    # Process each u-value and calculate fractions
    fractions_data = []
    
    for u_val in u_values:
        col_name = f"u_{u_val}"
        if col_name in data1.columns:
            a_values = data1[col_name].dropna().values
            b_values = data2[col_name].dropna().values
            c_values = data3[col_name].dropna().values
            
            min_length = min(len(a_values), len(b_values), len(c_values))
            if min_length > 0:
                # Classify each data point
                classifications = [classify_vector_decomposition_30from300(a_values[j], b_values[j], c_values[j]) 
                                 for j in range(min_length)]
                classifications = np.array(classifications)
                
                n_dominance = np.sum(classifications == 0)
                n_mixing = np.sum(classifications == 1)
                n_restructuring = np.sum(classifications == 2)
                total = len(classifications)
                
                dom_frac = n_dominance / total if total > 0 else 0
                mix_frac = n_mixing / total if total > 0 else 0
                res_frac = n_restructuring / total if total > 0 else 0
                
                print(f"  u={u_val:.1f}: Dom={dom_frac:.3f}, Mix={mix_frac:.3f}, Res={res_frac:.3f} ({total} points)")
                
                fractions_data.append({
                    'u': u_val,
                    'dominance': dom_frac,
                    'mixing': mix_frac,
                    'restructuring': res_frac
                })
    
    # Create matplotlib-style SVG
    width_pt = 177.58425
    height_pt = 158.917775
    
    plot_left = 33.13625
    plot_right = 164.82425
    plot_bottom = 140.901525
    plot_top = 10.063125
    
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    colors = {
        'dominance': '#e57373',      # Light red
        'mixing': '#81c784',         # Light green
        'restructuring': '#ba68c8'   # Light purple
    }
    
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
      <dc:title>30from300 k_gaussian_0.15 phase diagram</dc:title>
     </cc:Agent>
    </dc:creator>
   </cc:Work>
  </rdf:RDF>
 </metadata>
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
   </g>\\n   <g id="matplotlib.axis_1">'''
    
    # X-axis ticks and labels
    n_bars = len(fractions_data)
    bar_width = plot_width / n_bars
    
    # Add x-axis ticks
    for i, data_point in enumerate(fractions_data):
        x_center = plot_left + (i + 0.5) * bar_width
        
        svg_content += f'''
    <g id="xtick_{i+1}">
     <g id="line2d_{i+1}">
      <defs>
       <path id="tick{i+1}" d="M 0 0 
L 0 -3.5 
" style="stroke: #262626; stroke-width: 0.5"/>
      </defs>
      <g>
       <use xlink:href="#tick{i+1}" x="{x_center}" y="{plot_bottom}" style="fill: #262626; stroke: #262626; stroke-width: 0.5"/>
      </g>
     </g>
     <g id="text_{i+1}">
      <text x="{x_center}" y="{plot_bottom + 15}" text-anchor="middle" style="font-family: DejaVu Sans, sans-serif; font-size: 8px; fill: #262626">{data_point['u']:.1f}</text>
     </g>
    </g>'''
    
    # Add y-axis ticks (0.0 to 1.0)
    for j in range(6):  # 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
        y_val = j * 0.2
        y_pos = plot_bottom - (y_val * plot_height)
        
        svg_content += f'''
    <g id="ytick_{j+1}">
     <g id="line2d_y{j+1}">
      <defs>
       <path id="ytick{j+1}" d="M 0 0 L 3.5 0 " style="stroke: #262626; stroke-width: 0.5"/>
      </defs>
      <g>
       <use xlink:href="#ytick{j+1}" x="{plot_left}" y="{y_pos}" style="fill: #262626; stroke: #262626; stroke-width: 0.5"/>
      </g>
     </g>
     <g id="ytext_{j+1}">
      <text x="{plot_left - 8}" y="{y_pos + 2.8}" text-anchor="end" style="font-family: DejaVu Sans, sans-serif; font-size: 8px; fill: #262626">{y_val:.1f}</text>
     </g>
    </g>'''
    
    svg_content += '\\n   </g>'
    
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
   <g id="patch_dom_{i}">
    <path d="M {x_left} {y_bottom} 
L {x_right} {y_bottom} 
L {x_right} {y_top} 
L {x_left} {y_top} 
z
" style="fill: {colors['dominance']}"/>
   </g>'''
            y_bottom = y_top
        
        # Mixing bar (middle, green)
        if mix_height > 0:
            y_top = y_bottom - mix_height
            svg_content += f'''
   <g id="patch_mix_{i}">
    <path d="M {x_left} {y_bottom} 
L {x_right} {y_bottom} 
L {x_right} {y_top} 
L {x_left} {y_top} 
z
" style="fill: {colors['mixing']}"/>
   </g>'''
            y_bottom = y_top
        
        # Restructuring bar (top, purple)
        if res_height > 0:
            y_top = y_bottom - res_height
            svg_content += f'''
   <g id="patch_res_{i}">
    <path d="M {x_left} {y_bottom} 
L {x_right} {y_bottom} 
L {x_right} {y_top} 
L {x_left} {y_top} 
z
" style="fill: {colors['restructuring']}"/>
   </g>'''
    
    # Add axis labels
    svg_content += f'''
   <g id="text_xlabel">
    <text x="{plot_left + plot_width/2}" y="{plot_bottom + 30}" text-anchor="middle" style="font-family: DejaVu Sans, sans-serif; font-size: 8px; fill: #262626">Interaction strength</text>
   </g>
   <g id="text_ylabel">
    <text x="{plot_left - 25}" y="{plot_top + plot_height/2}" text-anchor="middle" transform="rotate(-90, {plot_left - 25}, {plot_top + plot_height/2})" style="font-family: DejaVu Sans, sans-serif; font-size: 8px; fill: #262626">Fraction</text>
   </g>'''
    
    # Axis spines
    svg_content += f'''
   <g id="patch_spine_left">
    <path d="M {plot_left} {plot_bottom} 
L {plot_left} {plot_top} 
" style="fill: none; stroke: #262626; stroke-width: 0.5; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_spine_bottom">
    <path d="M {plot_left} {plot_bottom} 
L {plot_right} {plot_bottom} 
" style="fill: none; stroke: #262626; stroke-width: 0.5; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
</svg>'''
    
    # Save the file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"✅ Phase diagram created: {output_file}")
    print(f"   30from300 k_gaussian_0.15 simulation")
    print(f"   Colors: Red (dominance), Green (mixing), Purple (restructuring)")
    
    # Print phase transition summary
    print("Phase transitions observed:")
    for data in fractions_data:
        u = data['u']
        dominant_phase = max([(k, v) for k, v in data.items() if k != 'u'], key=lambda x: x[1])
        print(f"  u={u:.1f}: {dominant_phase[0]} ({dominant_phase[1]:.1%})")
    
    return True

if __name__ == "__main__":
    create_30from300_phase_diagram()