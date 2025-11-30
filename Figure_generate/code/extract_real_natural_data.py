#!/usr/bin/env python3
"""
Extract real natural community experimental data and regenerate theta plots.
This script bypasses dependency issues by directly loading and processing the experimental data.
"""

import pandas as pd
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

def uv_to_theta_normalized(u_coords, v_coords):
    """Convert u,v coordinates to theta/(π/2) ranging from 0 to 1"""
    theta = np.arctan2(v_coords, u_coords)
    # Ensure theta is in [0, π/2] range
    theta = np.abs(theta)
    theta = np.minimum(theta, np.pi/2)
    
    # Normalize by π/2 to get range [0, 1]
    theta_normalized = theta / (np.pi/2)
    return theta_normalized

def create_natural_theta_histogram_svg(theta_values, output_file, color_hex, condition_name):
    """Create theta distribution plot matching our new style"""
    
    print(f"Creating REAL natural theta plot: {os.path.basename(output_file)}")
    print(f"  Using {len(theta_values)} actual experimental theta values")
    
    # Reference dimensions for theta plot
    width_pt = 167.330938
    height_pt = 63.93
    
    # Plot area coordinates
    plot_left = 19.5975
    plot_right = 157.810937
    plot_top = 7.2
    plot_bottom = 43.23
    
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    # Create dual histograms for stacked bars
    n_bins = 20
    
    # Original histogram (brown bars - bottom)
    hist_orig, bin_edges = np.histogram(theta_values, bins=n_bins, range=(0, 1))
    
    # Inverted histogram (grey bars - top)
    theta_inverted = 1 - theta_values
    hist_inverted, _ = np.histogram(theta_inverted, bins=n_bins, range=(0, 1))
    
    # Normalize by combined maximum for proper scaling
    max_combined = np.max(hist_orig + hist_inverted)
    hist_orig_norm = hist_orig / max_combined if max_combined > 0 else hist_orig
    hist_inverted_norm = hist_inverted / max_combined if max_combined > 0 else hist_inverted
    
    # Colors for stacked bars
    brown_color = color_hex  # Use provided color
    grey_color = "#808080"   # Grey for inverted data
    
    # Start SVG with exact reference structure
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
    
    # Add X-axis ticks for normalized range [0, 1]
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
    
    # Add Y-axis ticks (matching reference: 0, 20)
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
    
    # Add stacked histogram bars
    svg_content += '   <g id="HistogramCollection_1">\n'
    
    bin_width = plot_width / n_bins
    
    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        
        # Calculate bar heights
        brown_height = hist_orig_norm[i] * plot_height
        grey_height = hist_inverted_norm[i] * plot_height
        
        # Only draw bars if there's data
        if brown_height > 0 or grey_height > 0:
            
            # Brown bar (bottom) - original theta values
            if brown_height > 0:
                y_brown = plot_bottom - brown_height
                brown_opacity = 0.3 + 0.7 * hist_orig_norm[i]  # Opacity varies with frequency
                
                svg_content += f'''    <rect x="{x_left:.3f}" y="{y_brown:.3f}" width="{bin_width:.3f}" height="{brown_height:.3f}" style="fill: {brown_color}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''
            
            # Grey bar (top) - inverted theta values (1-val)
            if grey_height > 0:
                y_grey = plot_bottom - (brown_height + grey_height)
                grey_opacity = 0.3 + 0.7 * hist_inverted_norm[i]  # Opacity varies with frequency
                
                svg_content += f'''    <rect x="{x_left:.3f}" y="{y_grey:.3f}" width="{bin_width:.3f}" height="{grey_height:.3f}" style="fill: {grey_color}; fill-opacity: {grey_opacity:.3f}; stroke: none"/>
'''
    
    svg_content += '   </g>\n'
    
    # Add step function outline around entire histogram
    svg_content += '   <g id="HistogramOutline_1">\n'
    
    # Collect bar data for step function path
    bar_data = []
    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        brown_height = hist_orig_norm[i] * plot_height
        grey_height = hist_inverted_norm[i] * plot_height
        total_height = brown_height + grey_height
        
        if brown_height > 0 or grey_height > 0:
            bar_data.append({
                'x_left': x_left,
                'x_right': x_left + bin_width,
                'height': total_height
            })
    
    # Build step function path
    if bar_data:
        # Start path at bottom-left of first bar
        path_parts = [f"M {bar_data[0]['x_left']:.3f} {plot_bottom:.3f}"]
        
        # Trace the top outline as step function
        for bar in bar_data:
            y_top = plot_bottom - bar['height']
            # Step up to bar height
            path_parts.append(f"L {bar['x_left']:.3f} {y_top:.3f}")
            # Move horizontally across bar top
            path_parts.append(f"L {bar['x_right']:.3f} {y_top:.3f}")
        
        # Step down to baseline at end
        path_parts.append(f"L {bar_data[-1]['x_right']:.3f} {plot_bottom:.3f}")
        # Close path back to start
        path_parts.append("Z")
        
        path_string = " ".join(path_parts)
        
        # Add step function outline
        svg_content += f'''    <path d="{path_string}" style="fill: none; stroke: #333333; stroke-width: 0.8"/>
'''
    
    svg_content += '   </g>\n'
    
    # Close SVG structure
    svg_content += '''  </g>
 </g>
</svg>'''
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    return True

def load_real_natural_coalescence_data():
    """Load and process real natural coalescence data"""
    
    print("Loading REAL natural coalescence experimental data...")
    
    # Data file paths
    coalescence_natural_path = "../../Analyzed/processed_CoalescenceEvent_natural.xlsx"
    processed_sequences_natural_path = "../../Postprocessed/processed_Sequences_natural.xlsx"
    metadata_path = "../../Postprocessed/Metadata.xlsx"
    
    # Check if files exist
    for path in [coalescence_natural_path, processed_sequences_natural_path, metadata_path]:
        if not os.path.exists(path):
            print(f"ERROR: Data file not found: {path}")
            return None
    
    try:
        # Load data files
        coalescence_data = pd.read_excel(coalescence_natural_path)
        processed_sequences_natural = pd.read_excel(processed_sequences_natural_path)
        metadata = pd.read_excel(metadata_path)
        
        print(f"Loaded {len(coalescence_data)} coalescence events")
        print(f"Loaded {len(processed_sequences_natural)} natural sequence records")
        print(f"Loaded {len(metadata)} metadata records")
        
        # Process natural communities only
        offspring_list = []
        parent1_list = []
        parent2_list = []
        nutrient_conditions = []
        
        for idx, row in coalescence_data.iterrows():
            try:
                # Only process natural communities
                if row.get('CommunityOrigin') != 'N':
                    continue
                    
                mixture_id = row['SampleIDX']
                parent1_id = row['SampleIDX_Sub1']
                parent2_id = row['SampleIDX_Sub2']
                
                # Get abundance vectors
                mixture_rows = processed_sequences_natural[processed_sequences_natural['SampleIDX'] == mixture_id]
                parent1_rows = processed_sequences_natural[processed_sequences_natural['SampleIDX'] == parent1_id]
                parent2_rows = processed_sequences_natural[processed_sequences_natural['SampleIDX'] == parent2_id]
                
                if mixture_rows.empty or parent1_rows.empty or parent2_rows.empty:
                    continue
                    
                # Extract abundance vectors (columns 1-43, skipping SampleIDX)
                mixture_vector = mixture_rows.iloc[0, 1:44].values.astype(float)
                parent1_vector = parent1_rows.iloc[0, 1:44].values.astype(float) 
                parent2_vector = parent2_rows.iloc[0, 1:44].values.astype(float)
                
                # Handle NaN values
                mixture_vector = np.nan_to_num(mixture_vector, 0)
                parent1_vector = np.nan_to_num(parent1_vector, 0)
                parent2_vector = np.nan_to_num(parent2_vector, 0)
                
                # Normalize to relative abundances
                if np.sum(mixture_vector) > 0:
                    mixture_vector = mixture_vector / np.sum(mixture_vector)
                if np.sum(parent1_vector) > 0:
                    parent1_vector = parent1_vector / np.sum(parent1_vector)
                if np.sum(parent2_vector) > 0:
                    parent2_vector = parent2_vector / np.sum(parent2_vector)
                
                # Determine nutrient condition from metadata
                nutrient_condition = determine_nutrient_condition_from_metadata(mixture_id, metadata)
                
                # Only include if all vectors have non-zero abundance
                if (np.sum(mixture_vector) > 0 and 
                    np.sum(parent1_vector) > 0 and 
                    np.sum(parent2_vector) > 0):
                    
                    offspring_list.append(mixture_vector)
                    parent1_list.append(parent1_vector)
                    parent2_list.append(parent2_vector)
                    nutrient_conditions.append(nutrient_condition)
                    
            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                continue
        
        print(f"Successfully processed {len(offspring_list)} REAL natural coalescence events")
        if len(offspring_list) > 0:
            print(f"Nutrient distribution: LN={nutrient_conditions.count('LN')}, MN={nutrient_conditions.count('MN')}, HN={nutrient_conditions.count('HN')}")
        
        return offspring_list, parent1_list, parent2_list, nutrient_conditions
        
    except Exception as e:
        print(f"ERROR loading data files: {e}")
        return None

def determine_nutrient_condition_from_metadata(sample_id, metadata):
    """Determine nutrient condition from metadata or sample ID pattern"""
    # Try metadata first
    metadata_rows = metadata[metadata['SampleIDX'] == sample_id]
    
    if not metadata_rows.empty:
        medium = metadata_rows.iloc[0]['Medium']
        if medium == 'H':
            return 'HN'
        elif medium == 'M':
            return 'MN'
        elif medium == 'L':
            return 'LN'
    
    # Fallback to sample ID pattern matching
    sample_id_str = str(sample_id)
    if 'HN' in sample_id_str or sample_id_str.startswith('HN'):
        return 'HN'
    elif 'MN' in sample_id_str or sample_id_str.startswith('MN'):
        return 'MN'
    elif 'LN' in sample_id_str or sample_id_str.startswith('LN'):
        return 'LN'
    else:
        return 'unknown'

def main():
    """Main function to extract real natural data and regenerate theta plots"""
    
    print("="*80)
    print("EXTRACTING REAL NATURAL COMMUNITY EXPERIMENTAL DATA")
    print("="*80)
    
    # Load real natural coalescence data
    data_result = load_real_natural_coalescence_data()
    
    if data_result is None:
        print("❌ Failed to load real natural data")
        return
    
    offspring_list, parent1_list, parent2_list, nutrient_conditions = data_result
    
    if len(offspring_list) == 0:
        print("❌ No real natural coalescence data found")
        return
    
    # Create output directory
    output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_natural"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Color scheme matching natural conditions
    colors = {
        'HN': '#802000',  # Dark red for high nutrient
        'MN': '#b35900',  # Orange-brown for medium nutrient  
        'LN': '#cc6600'   # Orange for low nutrient
    }
    
    plots_created = 0
    
    print(f"\n📊 Creating REAL natural theta distribution plots...")
    
    for condition in ['HN', 'MN', 'LN']:
        print(f"\nProcessing {condition} natural communities...")
        
        # Filter data for this condition
        condition_indices = [i for i, c in enumerate(nutrient_conditions) if c == condition]
        
        if len(condition_indices) == 0:
            print(f"No real data found for {condition}")
            continue
            
        print(f"Found {len(condition_indices)} REAL experimental events for {condition}")
        
        # Process real experimental data
        u_coords = []
        v_coords = []
        
        for i in condition_indices:
            c_mix = offspring_list[i]
            c_1 = parent1_list[i]
            c_2 = parent2_list[i]
            
            try:
                # Calculate F1 and F2 metrics using real experimental data
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                u_coords.append(u)
                v_coords.append(v)
                
            except np.linalg.LinAlgError:
                # Skip singular cases
                continue
        
        if len(u_coords) == 0:
            print(f"No valid u,v coordinates for {condition}")
            continue
            
        # Convert to normalized theta using REAL experimental data
        u_coords = np.array(u_coords)
        v_coords = np.array(v_coords)
        theta_values = uv_to_theta_normalized(u_coords, v_coords)
        
        print(f"  Generated {len(theta_values)} REAL theta values from experimental data")
        print(f"  Theta range: {np.min(theta_values):.3f} to {np.max(theta_values):.3f}")
        
        if len(theta_values) > 0:
            output_file = f"{output_dir}/Metric_metric3_{condition}_natural_style_Theta.svg"
            
            success = create_natural_theta_histogram_svg(theta_values, output_file, colors[condition], condition)
            if success:
                plots_created += 1
                print(f"✅ Created REAL: Metric_metric3_{condition}_natural_style_Theta.svg")
    
    print(f"\n" + "="*80)
    print(f"REAL NATURAL THETA REGENERATION COMPLETE!")
    print(f"="*80)
    print(f"📊 Plots created with REAL experimental data: {plots_created}")
    print(f"🎯 Features:")
    print(f"   - Uses ACTUAL natural community experimental measurements")
    print(f"   - Stacked histograms: Brown (original) + Grey (1-val)")
    print(f"   - X-axis: 0 to 1 (theta/(π/2) normalized)")
    print(f"   - Step function boundary around complete bars")
    print(f"   - Large tick labels: 12.8px")
    print(f"   - Reference style: 167.330938pt × 63.93pt")

if __name__ == "__main__":
    main()