#!/usr/bin/env python
"""
Create all three 30from300 k_gaussian simulations (0.05, 0.1, 0.15) and their phase diagrams.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

def create_interaction_matrix_k_gaussian(N, u, sigma):
    """Create interaction matrix using Gaussian distribution."""
    base_interaction = u
    I = np.random.normal(base_interaction, sigma, (N, N))
    np.fill_diagonal(I, 1.0)
    I = np.abs(I)
    return I

def lotka_volterra_30from300(x, I, r):
    """Lotka-Volterra dynamics for 30from300 system."""
    N = len(x)
    dxdt = np.zeros(N)
    
    for i in range(N):
        interaction_sum = sum(I[i, j] * x[j] for j in range(N))
        dxdt[i] = r[i] * x[i] * (1 - interaction_sum)
    
    return dxdt

def run_30from300_k_gaussian_simulation(sigma):
    """Run 30from300 simulation for given sigma value."""
    
    print(f"🧪 Running 30from300 k_gaussian_{sigma} simulation...")
    
    N = 300
    n_communities = 10
    species_per_community = 30
    
    # Full u-value range
    u_values = np.arange(0.1, 1.3, 0.1)  # 0.1 to 1.2
    n_replicates = 15  # Moderate number for reasonable runtime
    
    output_dir = Path(f"Simulation_Data/new_k_gaussian_{sigma}_defined_pool_nooverlap_30from300_natural_full")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_results = {}
    start_time = time.time()
    
    for u_idx, u in enumerate(u_values):
        print(f"  u = {u:.1f} ({u_idx + 1}/{len(u_values)})")
        
        u_results = {
            'parent1_coeffs': [],
            'parent2_coeffs': [],
            'residual_magnitudes': []
        }
        
        for replicate in range(n_replicates):
            try:
                # Create interaction matrix
                I = create_interaction_matrix_k_gaussian(N, u, sigma)
                r = np.ones(N)
                
                # Define non-overlapping communities
                community_assignments = {}
                for comm in range(n_communities):
                    start_idx = comm * species_per_community
                    end_idx = (comm + 1) * species_per_community
                    community_assignments[comm] = list(range(start_idx, end_idx))
                
                # Select two random communities
                selected_communities = np.random.choice(n_communities, 2, replace=False)
                parent1_species = community_assignments[selected_communities[0]]
                parent2_species = community_assignments[selected_communities[1]]
                
                # Initial conditions
                x0 = np.zeros(N)
                for species in parent1_species:
                    x0[species] = 0.1 / len(parent1_species)
                for species in parent2_species:
                    x0[species] = 0.1 / len(parent2_species)
                
                # Time integration (optimized for speed)
                x = np.copy(x0)
                dt = 0.1
                n_steps = 100
                
                for step in range(n_steps):
                    dxdt = lotka_volterra_30from300(x, I, r)
                    x = x + dt * dxdt
                    x = np.maximum(x, 0)
                
                x_final = x
                
                # Vector decomposition
                parent1_profile = np.zeros(N)
                parent2_profile = np.zeros(N)
                
                for i in parent1_species:
                    parent1_profile[i] = x0[i]
                for i in parent2_species:
                    parent2_profile[i] = x0[i]
                
                # Normalize
                parent1_norm = np.linalg.norm(parent1_profile)
                parent2_norm = np.linalg.norm(parent2_profile)
                
                if parent1_norm > 0:
                    parent1_profile = parent1_profile / parent1_norm
                if parent2_norm > 0:
                    parent2_profile = parent2_profile / parent2_norm
                
                # Project final state
                if parent1_norm > 0 and parent2_norm > 0:
                    a = np.dot(x_final, parent1_profile)
                    b = np.dot(x_final, parent2_profile)
                    
                    projected = a * parent1_profile + b * parent2_profile
                    residual = x_final - projected
                    c = np.linalg.norm(residual)
                else:
                    a, b, c = 0, 0, np.linalg.norm(x_final)
                
                u_results['parent1_coeffs'].append(a)
                u_results['parent2_coeffs'].append(b)
                u_results['residual_magnitudes'].append(c)
                
            except Exception as e:
                print(f"    Error in replicate {replicate}: {e}")
                u_results['parent1_coeffs'].append(0)
                u_results['parent2_coeffs'].append(0)
                u_results['residual_magnitudes'].append(0)
        
        all_results[f'u_{u:.1f}'] = u_results
    
    # Save results
    parent1_df_data = {}
    parent2_df_data = {}
    residual_df_data = {}
    
    max_replicates = max(len(data['parent1_coeffs']) for data in all_results.values())
    
    for u_key, data in all_results.items():
        # Pad with NaN if needed
        parent1_coeffs = data['parent1_coeffs'] + [np.nan] * (max_replicates - len(data['parent1_coeffs']))
        parent2_coeffs = data['parent2_coeffs'] + [np.nan] * (max_replicates - len(data['parent2_coeffs']))
        residual_magnitudes = data['residual_magnitudes'] + [np.nan] * (max_replicates - len(data['residual_magnitudes']))
        
        parent1_df_data[u_key] = parent1_coeffs
        parent2_df_data[u_key] = parent2_coeffs
        residual_df_data[u_key] = residual_magnitudes
    
    parent1_df = pd.DataFrame(parent1_df_data)
    parent2_df = pd.DataFrame(parent2_df_data)
    residual_df = pd.DataFrame(residual_df_data)
    
    excel_path = output_dir / "Similarity.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        parent1_df.to_excel(writer, sheet_name='Parent1_coefficients', index=False)
        parent2_df.to_excel(writer, sheet_name='Parent2_coefficients', index=False)
        residual_df.to_excel(writer, sheet_name='Residual_magnitudes', index=False)
    
    elapsed_time = time.time() - start_time
    print(f"  ✅ k_gaussian_{sigma} complete in {elapsed_time:.1f} seconds")
    print(f"  📁 Results: {excel_path}")
    
    return excel_path

def classify_vector_decomposition_k_gaussian_30from300(a, b, c, sigma):
    """Classify coalescence outcome for 30from300 k_gaussian data."""
    # Normalize for classification
    total = a + b + c
    if total <= 0:
        return 2  # Default to restructuring
        
    a_norm = a / total
    b_norm = b / total
    c_norm = c / total
    
    # Classification thresholds adjusted based on sigma for 30from300
    if sigma <= 0.05:
        c_threshold = 0.05
        diff_threshold = 0.15
    elif sigma <= 0.1:
        c_threshold = 0.08
        diff_threshold = 0.2
    else:  # σ=0.15
        c_threshold = 0.15
        diff_threshold = 0.25
    
    if c_norm > c_threshold:
        return 2  # Restructuring
    elif abs(a_norm - b_norm) > diff_threshold:
        return 0  # Dominance
    else:
        return 1  # Mixing

def create_30from300_phase_diagram(sigma, data_path, output_path):
    """Create phase diagram for 30from300 k_gaussian simulation."""
    
    if not Path(data_path).exists():
        print(f"❌ Data file not found: {data_path}")
        return False
    
    # Read data
    data1 = pd.read_excel(data_path, sheet_name=0)
    data2 = pd.read_excel(data_path, sheet_name=1)
    data3 = pd.read_excel(data_path, sheet_name=2)
    
    # Extract u-values
    u_values = []
    for col in data1.columns:
        if col.startswith('u_'):
            u_val = float(col.split('_')[1])
            u_values.append(u_val)
    u_values = sorted(u_values)
    
    # Process fractions
    fractions_data = []
    
    for u_val in u_values:
        col_name = f"u_{u_val}"
        if col_name in data1.columns:
            a_values = data1[col_name].dropna().values
            b_values = data2[col_name].dropna().values
            c_values = data3[col_name].dropna().values
            
            min_length = min(len(a_values), len(b_values), len(c_values))
            if min_length > 0:
                classifications = [classify_vector_decomposition_k_gaussian_30from300(a_values[j], b_values[j], c_values[j], sigma) 
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
    
    # Create SVG (same format as before)
    width_pt = 177.58425
    height_pt = 158.917775
    plot_left = 33.13625
    plot_right = 164.82425
    plot_bottom = 140.901525
    plot_top = 10.063125
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    colors = {
        'dominance': '#e57373',
        'mixing': '#81c784',
        'restructuring': '#ba68c8'
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
      <dc:title>30from300 k_gaussian_{sigma} phase diagram</dc:title>
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
    
    # Add axis elements and bars (similar structure as previous implementation)
    n_bars = len(fractions_data)
    bar_width = plot_width / n_bars
    
    # X-axis ticks
    for i, data_point in enumerate(fractions_data):
        x_center = plot_left + (i + 0.5) * bar_width
        svg_content += f'''
    <g id="xtick_{i+1}">
     <g id="line2d_{i+1}">
      <defs>
       <path id="tick{i+1}" d="M 0 0 L 0 -3.5 " style="stroke: #262626; stroke-width: 0.5"/>
      </defs>
      <g>
       <use xlink:href="#tick{i+1}" x="{x_center}" y="{plot_bottom}" style="fill: #262626; stroke: #262626; stroke-width: 0.5"/>
      </g>
     </g>
     <g id="text_{i+1}">
      <text x="{x_center}" y="{plot_bottom + 15}" text-anchor="middle" style="font-family: DejaVu Sans, sans-serif; font-size: 8px; fill: #262626">{data_point['u']:.1f}</text>
     </g>
    </g>'''
    
    # Y-axis ticks
    for j in range(6):
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
    
    # Stacked bars
    for i, data_point in enumerate(fractions_data):
        x_left = plot_left + i * bar_width
        x_right = plot_left + (i + 1) * bar_width
        
        dom_height = data_point['dominance'] * plot_height
        mix_height = data_point['mixing'] * plot_height
        res_height = data_point['restructuring'] * plot_height
        
        y_bottom = plot_bottom
        
        # Dominance
        if dom_height > 0:
            y_top = y_bottom - dom_height
            svg_content += f'''
   <g id="patch_dom_{i}">
    <path d="M {x_left} {y_bottom} L {x_right} {y_bottom} L {x_right} {y_top} L {x_left} {y_top} z" style="fill: {colors['dominance']}"/>
   </g>'''
            y_bottom = y_top
        
        # Mixing
        if mix_height > 0:
            y_top = y_bottom - mix_height
            svg_content += f'''
   <g id="patch_mix_{i}">
    <path d="M {x_left} {y_bottom} L {x_right} {y_bottom} L {x_right} {y_top} L {x_left} {y_top} z" style="fill: {colors['mixing']}"/>
   </g>'''
            y_bottom = y_top
        
        # Restructuring
        if res_height > 0:
            y_top = y_bottom - res_height
            svg_content += f'''
   <g id="patch_res_{i}">
    <path d="M {x_left} {y_bottom} L {x_right} {y_bottom} L {x_right} {y_top} L {x_left} {y_top} z" style="fill: {colors['restructuring']}"/>
   </g>'''
    
    # Labels and spines
    svg_content += f'''
   <g id="text_xlabel">
    <text x="{plot_left + plot_width/2}" y="{plot_bottom + 30}" text-anchor="middle" style="font-family: DejaVu Sans, sans-serif; font-size: 8px; fill: #262626">Interaction strength</text>
   </g>
   <g id="text_ylabel">
    <text x="{plot_left - 25}" y="{plot_top + plot_height/2}" text-anchor="middle" transform="rotate(-90, {plot_left - 25}, {plot_top + plot_height/2})" style="font-family: DejaVu Sans, sans-serif; font-size: 8px; fill: #262626">Fraction</text>
   </g>
   <g id="patch_spine_left">
    <path d="M {plot_left} {plot_bottom} L {plot_left} {plot_top} " style="fill: none; stroke: #262626; stroke-width: 0.5; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_spine_bottom">
    <path d="M {plot_left} {plot_bottom} L {plot_right} {plot_bottom} " style="fill: none; stroke: #262626; stroke-width: 0.5; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
</svg>'''
    
    # Save file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"  📊 Phase diagram: {output_file}")
    return True

def main():
    """Run all 30from300 k_gaussian simulations and create phase diagrams."""
    
    print("🚀 30from300 k_gaussian simulation suite")
    print("=" * 60)
    
    sigma_values = [0.05, 0.1, 0.15]
    total_start_time = time.time()
    
    for sigma in sigma_values:
        print(f"\\n--- Processing k_gaussian_{sigma} ---")
        
        # Run simulation
        data_path = run_30from300_k_gaussian_simulation(sigma)
        
        # Create phase diagram
        output_path = f"Figure/PhaseDiagram/Fig_phase_diagram_Simul_30from300_k_gaussian_{sigma}.svg"
        create_30from300_phase_diagram(sigma, data_path, output_path)
    
    total_time = time.time() - total_start_time
    print(f"\\n🎉 All 30from300 k_gaussian simulations complete!")
    print(f"⏱️  Total time: {total_time/60:.1f} minutes")
    print(f"📁 Phase diagrams in: Figure/PhaseDiagram/")
    
    for sigma in sigma_values:
        svg_path = Path(f"Figure/PhaseDiagram/Fig_phase_diagram_Simul_30from300_k_gaussian_{sigma}.svg")
        if svg_path.exists():
            file_size = svg_path.stat().st_size
            print(f"  • k_gaussian_{sigma} → {svg_path.name} ({file_size:,} bytes)")

if __name__ == "__main__":
    main()