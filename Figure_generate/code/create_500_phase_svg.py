#!/usr/bin/env python
"""
Create SVG phase diagram for 500-species simulation without matplotlib.
Generates: Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500.svg
"""

import numpy as np
import pandas as pd
from pathlib import Path


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


def create_svg_phase_diagram():
    """Create SVG phase diagram manually."""
    
    print("Creating 500-species phase diagram SVG...")
    
    # Load data
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
                a_values = a_values[:min_length]
                b_values = b_values[:min_length] 
                c_values = c_values[:min_length]
                
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
    
    # Create SVG
    width, height = 800, 600
    margin = 80
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    
    # Colors
    colors = {
        'dominance': '#FF6B6B',     # Red
        'mixing': '#9B59B6',        # Purple  
        'restructuring': '#2ECC71'  # Green
    }
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .axis-text {{ font-family: Arial, sans-serif; font-size: 12px; }}
      .title-text {{ font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; }}
      .legend-text {{ font-family: Arial, sans-serif; font-size: 11px; }}
    </style>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="white"/>
  
  <!-- Grid lines -->'''
    
    # Add horizontal grid lines
    for i in range(6):  # 0, 0.2, 0.4, 0.6, 0.8, 1.0
        y = margin + plot_height - (i * plot_height / 5)
        svg_content += f'\n  <line x1="{margin}" y1="{y}" x2="{margin + plot_width}" y2="{y}" stroke="#E0E0E0" stroke-width="1"/>'
        # Y-axis labels
        label = f"{i * 0.2:.1f}"
        svg_content += f'\n  <text x="{margin - 10}" y="{y + 4}" text-anchor="end" class="axis-text">{label}</text>'
    
    # Add bars
    bar_width = plot_width / len(fractions_data) * 0.8
    bar_spacing = plot_width / len(fractions_data)
    
    for i, data_point in enumerate(fractions_data):
        x = margin + i * bar_spacing + bar_spacing * 0.1
        
        # Stack the bars (bottom to top: dominance, mixing, restructuring)
        y_bottom = margin + plot_height
        
        # Dominance bar (bottom)
        dom_height = data_point['dominance'] * plot_height
        if dom_height > 0:
            svg_content += f'\n  <rect x="{x}" y="{y_bottom - dom_height}" width="{bar_width}" height="{dom_height}" fill="{colors["dominance"]}" stroke="white" stroke-width="1"/>'
        
        # Mixing bar (middle)
        mix_height = data_point['mixing'] * plot_height
        if mix_height > 0:
            y_mix = y_bottom - dom_height - mix_height
            svg_content += f'\n  <rect x="{x}" y="{y_mix}" width="{bar_width}" height="{mix_height}" fill="{colors["mixing"]}" stroke="white" stroke-width="1"/>'
        
        # Restructuring bar (top)
        res_height = data_point['restructuring'] * plot_height
        if res_height > 0:
            y_res = y_bottom - dom_height - mix_height - res_height
            svg_content += f'\n  <rect x="{x}" y="{y_res}" width="{bar_width}" height="{res_height}" fill="{colors["restructuring"]}" stroke="white" stroke-width="1"/>'
        
        # X-axis labels
        label_x = x + bar_width / 2
        label_y = margin + plot_height + 20
        svg_content += f'\n  <text x="{label_x}" y="{label_y}" text-anchor="middle" class="axis-text">{data_point["u"]:.1f}</text>'
    
    # Axes
    svg_content += f'''
  <!-- Axes -->
  <line x1="{margin}" y1="{margin}" x2="{margin}" y2="{margin + plot_height}" stroke="black" stroke-width="2"/>
  <line x1="{margin}" y1="{margin + plot_height}" x2="{margin + plot_width}" y2="{margin + plot_height}" stroke="black" stroke-width="2"/>
  
  <!-- Axis labels -->
  <text x="{margin + plot_width / 2}" y="{height - 20}" text-anchor="middle" class="title-text">Interaction Strength (u)</text>
  <text x="20" y="{margin + plot_height / 2}" text-anchor="middle" class="title-text" transform="rotate(-90, 20, {margin + plot_height / 2})">Fraction of Events</text>
  
  <!-- Title -->
  <text x="{width / 2}" y="30" text-anchor="middle" class="title-text">500-Species Coalescence Phase Diagram</text>
  
  <!-- Legend -->
  <rect x="{width - 180}" y="60" width="160" height="80" fill="none" stroke="black" stroke-width="1"/>
  <rect x="{width - 170}" y="75" width="15" height="15" fill="{colors['dominance']}"/>
  <text x="{width - 150}" y="87" class="legend-text">Dominance</text>
  <rect x="{width - 170}" y="95" width="15" height="15" fill="{colors['mixing']}"/>
  <text x="{width - 150}" y="107" class="legend-text">Mixing</text>
  <rect x="{width - 170}" y="115" width="15" height="15" fill="{colors['restructuring']}"/>
  <text x="{width - 150}" y="127" class="legend-text">Restructuring</text>
  
</svg>'''
    
    # Create output directory and save
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "Fig_phase_diagram_Simul_50from500.svg"
    
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"✅ SVG phase diagram created: {output_file}")
    print(f"   Size: {width}×{height} pixels")
    print(f"   Shows {len(fractions_data)} u-values from {u_values[0]:.1f} to {u_values[-1]:.1f}")


if __name__ == "__main__":
    create_svg_phase_diagram()