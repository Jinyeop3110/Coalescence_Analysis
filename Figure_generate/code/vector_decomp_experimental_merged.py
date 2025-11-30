#!/usr/bin/env python3
"""
Vector decomposition analysis for experimental coalescence events with merged plots for species pools 6, 12, and 24.
Extended from vector_decomp_experimental.py to handle multiple species pools.
"""

from common_setup import *
from pathlib import Path
import json
import os
from scipy.stats import binomtest
from scipy.stats import gaussian_kde
import matplotlib.patches as mpatches

# Alternative to statsmodels for confidence intervals
def wilson_conf_int(x, n, alpha=0.05):
    """Wilson score confidence interval for binomial proportion"""
    z = 1.96  # 95% confidence interval
    p = x / n
    denominator = 1 + z**2 / n
    centre_adjusted_probability = (p + z**2 / (2*n)) / denominator
    adjustment = z * np.sqrt((p * (1 - p) + z**2 / (4*n)) / n) / denominator
    lower_bound = centre_adjusted_probability - adjustment
    upper_bound = centre_adjusted_probability + adjustment
    return lower_bound, upper_bound

# Create output directory
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_exp_merged"
os.makedirs(output_dir, exist_ok=True)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def metric1(u,v,m):
    u=normalize(u)
    v=normalize(v)
    m=normalize(m)
    
    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])

    e12=np.matmul(np.linalg.inv(A),np.array([np.sum(m*u), np.sum(m*v)]))
    return np.linalg.norm(m-(e12[0]*u)-(e12[1]*v))**2
    
def metric2(u,v,m):
    u=normalize(u)
    v=normalize(v)
    m=normalize(m)
    
    return abs(np.sum(m*u)-np.sum(m*v))

def metric3(u,v,m):
    u=normalize(u)
    v=normalize(v)
    m=normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])

    e12=np.matmul(np.linalg.inv(A),np.array([np.sum(m*u), np.sum(m*v)]))
    return (e12[0]),(e12[1]), np.linalg.norm(m-(e12[0]*u)-(e12[1]*v))

def metric4(u,v,m,):
    return np.sum(np.minimum(u,m)), np.sum(np.minimum(v,m))

def metric5(u,v,m):
    return SimilarityJS(u,m), SimilarityJS(v,m)

def metric6(u,v,m):
    return SimilarityJS(u,m,1e-4), SimilarityJS(v,m,1e-4)

def metric7(u,v,m):
    return np.sum(np.minimum(u,m))/np.sum(np.maximum(u,m)), np.sum(np.minimum(v,m))/np.sum(np.maximum(v,m))

def drawPairwiseChange(i, j, x):
    return np.sin(i*x) + np.cos(j*x)

def InterpretPairwiseResult(y1,y2):
    if y1==1 and y2==1:
        return 'E',(0.85, 0.7, 0.7) #E : competitive exclusion
    elif y1==0 and y2==0:
        return 'E',(0.85, 0.7, 0.7) #E : competitive exclusion
    elif y1==0 and y2==1:
        return 'B',(0.7, 0.7, 0.9) #B : Bistability
    elif y1>0 and y1<1 and y2>0 and y2<1:
        return 'C',(0.7, 0.85, 0.7) #C : Coexistence
    else:
        return 'U',(0.5, 0.5, 0.5) #U : Unclassified

def mask_equal(u,v,m):
    u_m=np.array(u)>0
    v_m=np.array(v)>0
    shared=u_m*v_m
    mask1=u_m-shared*(np.array(v)/(np.array(u)+np.array(v)+1e-8))
    mask2=1-mask1
    return mask1, mask2

def NbyNcomposition(Coalescence_data, Coal_IDX_list, Sub_IDX_list):
    N=len(Sub_IDX_list)
    Coal_matrix={}
    Coal_keys={}
    Coal_mask1={}
    Coal_mask2={}
    Sub_keys={}
    Sub_matrix={}
    for SampleIDX in Coal_IDX_list:
        idx=np.where(Coalescence_data['SampleIDX']==SampleIDX)
        subSampleIDX1=Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()[0]
        subSampleIDX2=Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()[0]
        subSampleIDX1=np.where(Sub_IDX_list==subSampleIDX1)[0][0]
        subSampleIDX2=np.where(Sub_IDX_list==subSampleIDX2)[0][0]
        IDX_list_=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in [SampleIDX]])
        df=Processed_sequences_synthetic.iloc[IDX_list_]
        c_mix=df.values[1:].tolist()
        ID_mix=df.values[0]
        
        SampleIDX=Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()[0]
        IDX_list_=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in [SampleIDX]])
        if (IDX_list_.size==0):
            continue
        df=Processed_sequences_synthetic.iloc[IDX_list_]
        c_1=df.values[1:].tolist()
        ID_1=df.values[0]   
        
        SampleIDX=Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()[0]
        IDX_list_=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in [SampleIDX]])
        if (IDX_list_.size==0):
            continue
        df=Processed_sequences_synthetic.iloc[IDX_list_]
        c_2=df.values[1:].tolist()
        ID_2=df.values[0]          
        
        mask_1,mask_2=mask_equal(c_1,c_2,c_mix)
        
        i=min(subSampleIDX1,subSampleIDX2)
        j=max(subSampleIDX1,subSampleIDX2)
        Coal_matrix[i,j]=c_mix
        Coal_keys[i,j]=ID_mix
        Coal_mask1[i,j]=mask_1
        Coal_mask2[i,j]=mask_2
        
    for SampleIDX in Sub_IDX_list:
        IDX_list_=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in [SampleIDX]])
        if (IDX_list_.size==0):
            continue
        df=Processed_sequences_synthetic.iloc[IDX_list_]
        i=np.where(Sub_IDX_list==SampleIDX)[0][0]
        Sub_matrix[i]=df.values[1:].tolist()
        Sub_keys[i]=df.values[0]
        
    return Coal_matrix, Sub_matrix, Coal_keys, Sub_keys,Coal_mask1,Coal_mask2

def metric_VectorDecomposition_onlyPositive(u,v,m):
    u=normalize(u)
    v=normalize(v)
    m=normalize(m)
    
    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])

    e12=np.matmul(np.linalg.inv(A),np.array([np.sum(m*u), np.sum(m*v)]))
    
    x1=(e12[0])*(e12[0]>0)
    x2=(e12[1])*(e12[1]>0)
    x3=np.linalg.norm(m-(e12[0]*u)-(e12[1]*v))
    convert=np.sqrt((1-x3**2)/(x1**2+x2**2))
    
    return convert*x1, convert*x2, x3

def PolarizedPlot_merged(all_data, colors, species_pools):
    mm = 1 / 25.4
    f, axes = plt.subplots(1, 3, figsize=(180*mm, 60*mm), facecolor='w', edgecolor='k')
    
    for idx, (medium_data, ax) in enumerate(zip(all_data, axes)):
        # Plot data for all species pools
        for pool_idx, (pool_size, pool_data) in enumerate(medium_data.items()):
            data1, data2 = pool_data['real']
            # Use different markers for different pools
            markers = ['o', 's', '^']
            ax.scatter(data1, data2, s=25, color=colors[idx], marker=markers[pool_idx], 
                      alpha=0.7, linewidths=0, label=f'Pool {pool_size}')
            ax.scatter(data2, data1, s=25, color='grey', marker=markers[pool_idx], 
                      alpha=0.2, linewidths=0)

        # Define the grid of points
        x = np.linspace(-0.15, 1.2, 500)
        y = np.linspace(-0.15, 1.2, 500)
        X, Y = np.meshgrid(x, y)

        # Calculate the radius from the origin
        R = np.sqrt(abs(X**2 + Y**2))
        contour = ax.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey', 
                           alpha=0.2, linewidths=0.5)
        
        # Add auxiliary lines at x=0 and y=0
        ax.axhline(0, color='k', linestyle='--', linewidth=.8)
        ax.axvline(0, color='k', linestyle='--', linewidth=.8)

        # Set plot limits and labels
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xticks([0, 0.5, 1.0])
        ax.set_yticks([0, 0.5, 1.0])
        
        # Remove the outer box (spines)
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        # Add title
        titles = ['Low Nutrient', 'Medium Nutrient', 'High Nutrient']
        ax.set_title(titles[idx])
        
        # Add legend to first subplot
        if idx == 0:
            ax.legend(loc='upper right', fontsize=8)
    
    plt.tight_layout()
    return f

def plot_class_fraction_comparison_merged(all_class_data, colors):
    mm = 1 / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(210*mm, 60*mm))
    
    class_names = ["Mixing", "Dominance", "Restructuring"]
    class_indices = [1, 0, 2]  # Reordering indices
    
    for idx, (medium_name, ax) in enumerate(zip(['LN', 'MN', 'HN'], axes)):
        x = np.arange(3)
        bar_width = 0.25
        
        # Plot bars for each species pool
        for pool_idx, pool_size in enumerate([6, 12, 24]):
            if pool_size in all_class_data[medium_name]:
                data = all_class_data[medium_name][pool_size]
                
                # Reorder counts
                counts_real = [data['real_counts'][i] for i in class_indices]
                proportions_real = [counts_real[i] / data['real_total'] for i in range(3)]
                
                # Wilson CI
                ci_low_real = []
                ci_high_real = []
                for i in range(3):
                    low_r, high_r = wilson_conf_int(counts_real[i], data['real_total'])
                    ci_low_real.append(max(0, low_r))  # Ensure non-negative
                    ci_high_real.append(min(1, high_r))  # Ensure ≤ 1
                
                errors_real = [max(0, p - l) for p, l in zip(proportions_real, ci_low_real)]
                
                # Plot bars
                offset = (pool_idx - 1) * bar_width
                ax.bar(x + offset, proportions_real, bar_width, yerr=errors_real, 
                      capsize=0, alpha=0.7, edgecolor='none', 
                      error_kw={'elinewidth': .5, 'capthick': 0},
                      label=f'Pool {pool_size}', color=colors[idx])
        
        # Axis settings
        ax.set_xticks(x)
        ax.set_xticklabels(class_names)
        ax.set_ylim(0, 1)
        if idx == 0:
            ax.set_ylabel("Fraction")
        ax.set_title(f'{medium_name}')
        if idx == 0:
            ax.legend()
    
    plt.tight_layout()
    return fig

def print_class_fractions(data1, data2, type_name=None):
    class1_count = 0  # Dominance
    class2_count = 0  # Mixing
    class3_count = 0  # Restructuring
    
    for j in range(len(data1)):
        # Calculate asymmetricity
        x, y = calculate_assymetricity(data1[j], data2[j], 0)  # Pass 0 for k as it's not used
        
        # Determine class
        class_type = characterize_case(x, y)
        if class_type == 0:
            class1_count += 1
        elif class_type == 1:
            class2_count += 1
        else:
            class3_count += 1
    
    total_count = class1_count + class2_count + class3_count
    
    if total_count > 0:
        class1_fraction = class1_count / total_count
        class2_fraction = class2_count / total_count
        class3_fraction = class3_count / total_count
        
        label = f"{type_name} " if type_name else ""
        print(f"{label}Class Fractions:")
        print(f"  Dominance:    {class1_fraction:.2f} ({class1_count}/{total_count})")
        print(f"  Mixing:       {class2_fraction:.2f} ({class2_count}/{total_count})")
        print(f"  Restructuring: {class3_fraction:.2f} ({class3_count}/{total_count})")
        print("")
        
        return class1_fraction, class2_fraction, class3_fraction
    else:
        print(f"No data points to classify")
        return 0, 0, 0

def uv_to_theta_normalized(u_coords, v_coords):
    """Convert u,v coordinates to theta/(π/2) ranging from 0 to 1"""
    theta = np.arctan2(v_coords, u_coords)
    # Ensure theta is in [0, π/2] range
    theta = np.abs(theta)
    theta = np.minimum(theta, np.pi/2)
    
    # Normalize by π/2 to get range [0, 1]
    theta_normalized = theta / (np.pi/2)
    return theta_normalized

def create_theta_histogram_svg(theta_values, output_file, medium_name):
    """Create theta distribution plot matching reference style"""
    
    print(f"Creating theta plot: {os.path.basename(output_file)}")
    
    # Reference dimensions for theta plot (from simulation code)
    width_pt = 167.330938
    height_pt = 63.93
    
    # Plot area coordinates (from reference)
    plot_left = 19.5975
    plot_right = 157.810937
    plot_top = 7.2
    plot_bottom = 43.23
    
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    # Create single histogram for brown bars only
    n_bins = 20
    
    # Original histogram as density (brown bars only)
    hist_orig, bin_edges = np.histogram(theta_values, bins=n_bins, range=(0, 1), density=True)
    
    # Set fixed max density to 10 for consistent scaling
    max_density = 10.0
    hist_orig_norm = hist_orig / max_density
    
    # Import colors for media-specific coloring
    from COLORMAP import get_medium_color
    
    # Colors for bars - media-specific
    data_color = get_medium_color(medium_name)  # LN, MN, or HN specific color
    
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
    
    # Add Y-axis ticks for density
    y_tick_positions = [0.0, 1.0]
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
    
    # Add histogram bars
    svg_content += '   <g id="HistogramCollection_1">\n'
    
    bin_width = plot_width / n_bins
    
    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        
        # Calculate bar height (brown only)
        brown_height = hist_orig_norm[i] * plot_height
        
        # Only draw bars if there's data
        if brown_height > 0:
            y_brown = plot_bottom - brown_height
            # Opacity varies with frequency, clamped to valid range
            brown_opacity = 0.3 + 0.7 * min(hist_orig_norm[i], 1.0)
            
            svg_content += f'''    <rect x="{x_left:.3f}" y="{y_brown:.3f}" width="{bin_width:.3f}" height="{brown_height:.3f}" style="fill: {data_color}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''
            
    
    svg_content += '   </g>\n'
    
    # Add step function outline around entire histogram
    svg_content += '   <g id="HistogramOutline_1">\n'
    
    # Build step function path that goes to y=0 for empty bars
    path_parts = []
    
    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        x_right = x_left + bin_width
        brown_height = hist_orig_norm[i] * plot_height
        
        if brown_height > 0:
            y_top = plot_bottom - brown_height
            
            if not path_parts:  # First bar
                path_parts.append(f"M {x_left:.3f} {plot_bottom:.3f}")
            else:
                # Connect from previous position to start of this bar at baseline
                path_parts.append(f"L {x_left:.3f} {plot_bottom:.3f}")
            
            # Step up to bar height
            path_parts.append(f"L {x_left:.3f} {y_top:.3f}")
            # Move horizontally across bar top
            path_parts.append(f"L {x_right:.3f} {y_top:.3f}")
            # Step down to baseline at end of bar
            path_parts.append(f"L {x_right:.3f} {plot_bottom:.3f}")
    
    if path_parts:
        path_string = " ".join(path_parts)
        
        # Add step function outline
        svg_content += f'''    <path d="{path_string}" style="fill: none; stroke: #333333; stroke-width: 0.8"/>
'''
    
    svg_content += '   </g>\n'
    
    # Add box frame around plot area
    svg_content += f'''   <g id="axes_frame">
    <path d="M {plot_left} {plot_bottom} 
L {plot_right} {plot_bottom} 
L {plot_right} {plot_top} 
L {plot_left} {plot_top} 
L {plot_left} {plot_bottom}" style="fill: none; stroke: #262626; stroke-width: 0.8"/>
   </g>
'''
    
    # Close SVG structure
    svg_content += '''  </g>
 </g>
</svg>'''
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    return True, max_density

def parse_theta_histogram_data(svg_content):
    """Extract histogram data from theta SVG for symmetric version"""
    import re
    
    # Extract all rect elements that are histogram bars
    rect_pattern = r'<rect x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)" style="fill: ([^;]+); fill-opacity: ([^;]+); stroke: none"/>'
    rects = re.findall(rect_pattern, svg_content)
    
    histogram_bars = []
    
    for rect in rects:
        x, y, width, height, color, opacity = rect
        
        # Only process histogram bars (any media color, not grey background)
        if color in ['#A7216A', '#802000', '#E24912']:  # Media-specific colors
            histogram_bars.append({
                'x': float(x),
                'y': float(y), 
                'width': float(width),
                'height': float(height),
                'color': color,
                'opacity': float(opacity)
            })
    
    return histogram_bars

def create_theta_symmetric_svg(original_bars, output_file, input_filename, max_density=None, medium_name=None):
    """Create theta_symmetric version with grey stacked bars"""
    
    print(f"Creating symmetric version: {os.path.basename(output_file)}")
    print(f"  Processing {len(original_bars)} brown histogram bars from {input_filename}")
    
    # Reference dimensions
    width_pt = 167.330938
    height_pt = 63.93
    plot_left = 19.5975
    plot_right = 157.810937
    plot_top = 7.2
    plot_bottom = 43.23
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top
    
    # Import colors for media-specific coloring
    from COLORMAP import get_medium_color
    
    # Colors - media-specific data color
    data_color = get_medium_color(medium_name) if medium_name else "#802000"
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
    
    # Add Y-axis ticks for density
    y_tick_positions = [0.0, 1.0]
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
        # Keep original brown bar (bottom)
        brown_x = bar['x']
        brown_y = bar['y']
        brown_width = bar['width']
        brown_height = bar['height']
        brown_opacity = bar['opacity']
        
        # Calculate relative position for grey bar sizing
        rel_x = (brown_x - plot_left) / plot_width  # Position from 0 to 1
        
        # Create grey bar on top - more grey at edges (0 and 1), less in middle (0.5)
        center_distance = abs(rel_x - 0.5) * 2  # 0 at center, 1 at edges
        grey_scale_factor = 0.3 + 0.7 * center_distance  # More grey at edges
        
        grey_height = brown_height * grey_scale_factor * 0.5
        grey_y = brown_y - grey_height
        grey_opacity = 0.8  # Fixed opacity for all grey bars
        
        # Reduce both bars to half for normalization
        brown_height_norm = brown_height * 0.5
        grey_height_norm = grey_height * 0.5
        brown_y_norm = plot_bottom - brown_height_norm
        grey_y_norm = brown_y_norm - grey_height_norm
        
        # Add brown bar (original, normalized)
        svg_content += f'''    <rect x="{brown_x:.3f}" y="{brown_y_norm:.3f}" width="{brown_width:.3f}" height="{brown_height_norm:.3f}" style="fill: {data_color}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''
        
        # Add grey bar (stacked on top, normalized)
        svg_content += f'''    <rect x="{brown_x:.3f}" y="{grey_y_norm:.3f}" width="{brown_width:.3f}" height="{grey_height_norm:.3f}" style="fill: {grey_color}; fill-opacity: {grey_opacity:.3f}; stroke: none"/>
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
            # Calculate total height (brown + grey), both normalized to half
            rel_x = (bar['x'] - plot_left) / plot_width
            center_distance = abs(rel_x - 0.5) * 2
            grey_scale_factor = 0.3 + 0.7 * center_distance
            grey_height = bar['height'] * grey_scale_factor * 0.5
            # Both bars reduced to half
            brown_height_norm = bar['height'] * 0.5
            grey_height_norm = grey_height * 0.5
            total_height = brown_height_norm + grey_height_norm
            y_top = plot_bottom - total_height
            
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
            svg_content += f'''    <path d="{path_string}" style="fill: none; stroke: #333333; stroke-width: 0.8"/>
'''
    
    svg_content += '   </g>\n'
    
    # Add box frame around plot area
    svg_content += f'''   <g id="axes_frame">
    <path d="M {plot_left} {plot_bottom} 
L {plot_right} {plot_bottom} 
L {plot_right} {plot_top} 
L {plot_left} {plot_top} 
L {plot_left} {plot_bottom}" style="fill: none; stroke: #262626; stroke-width: 0.8"/>
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
    """Main analysis function for merged plots"""
    print("Starting vector decomposition analysis for experimental data (merged species pools)...")
    
    # Color scheme - using centralized COLORMAP
    from COLORMAP import get_medium_colors
    colors = get_medium_colors()  # [LN, MN, HN] colors

    typeofplot = 'swarmpoint' 
    to_plot_null = True
    to_plot_subperturb = False  # Simplified for merged plots

    # Storage for all data across species pools
    all_data = []  # Will be list of dicts for each medium
    all_class_data = {'LN': {}, 'MN': {}, 'HN': {}}
    
    # Process each medium type
    for c_i, medium in enumerate(['LN', 'MN', 'HN']):
        print(f"\nProcessing {medium}...")
        medium_data = {}
        
        # Process each species pool
        for species_num in [6, 12, 24]:
            type_name = f'{medium}_{species_num}'
            print(f"  Processing {type_name}...")
            
            # Skip if data doesn't exist
            if type_name not in Syn_Coal_IDX:
                print(f"    Warning: {type_name} not found in Syn_Coal_IDX, skipping...")
                continue
            
            Null_model_rep = 1
            
            # Get indices for the current type
            IDX_list = Syn_Coal_IDX[type_name]
            
            # Get parent sample indices
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            
            # Get indices for the first components
            idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
            
            # Get indices for the second components
            idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
            
            # Get indices for the mixture
            idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
            
            # Initialize data lists
            data1, data2, data_null_model_1, data_null_model_2 = [], [], [], []
            
            # Determine species number based on pool
            if species_num == 6:
                species_count = 23  # Adjust based on your actual data
            elif species_num == 12:
                species_count = 43
            else:  # 24
                species_count = 79  # Adjust based on your actual data
                
            # Process each sample
            for i in range(len(idx)):
                for _ in range(Null_model_rep):
                    # Get composition data
                    c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                    c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                    c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                    
                    # Filter small values
                    c_1 = c_1 * (c_1 > 1e-4)
                    c_2 = c_2 * (c_2 > 1e-4)
                    
                    if to_plot_null and _ == 0:
                        try:
                            # Create mock mixtures for null model
                            mix_label = (np.random.rand(len(c_1)))
                            moc_c1 = c_1
                            moc_c2 = c_2
                            
                            # Normalize
                            moc_c_mix = (mix_label) * c_1 + mix_label * c_2
                            moc_c_mix = moc_c_mix / (np.sum(moc_c_mix) + 1e-9)
                            
                            # Calculate F1 and F2 metrics
                            u, v, k = metric_VectorDecomposition_onlyPositive(moc_c1, moc_c2, moc_c_mix)
                            
                            data_null_model_1.append(u)
                            data_null_model_2.append(v)
                        except np.linalg.LinAlgError:
                            pass
                    
                    if _ == 0:
                        try:
                            # Calculate metrics for real data
                            u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                            data1.append(u)
                            data2.append(v)
                        except np.linalg.LinAlgError:
                            pass
            
            # Store data for this species pool
            medium_data[species_num] = {
                'real': (data1, data2),
                'null': (data_null_model_1, data_null_model_2)
            }
            
            # Calculate class fractions
            print(f"\n    Class Fractions for {type_name}:")
            real_class1_frac, real_class2_frac, real_class3_frac = print_class_fractions(data1, data2, "Real Data")
            real_total = len(data1)
            real_counts = [int(real_class1_frac * real_total), 
                          int(real_class2_frac * real_total), 
                          int(real_class3_frac * real_total)]
            
            # Store class data
            all_class_data[medium][species_num] = {
                'real_counts': real_counts,
                'real_total': real_total
            }
            
            if to_plot_null and len(data_null_model_1) > 0:
                null_class1_frac, null_class2_frac, null_class3_frac = print_class_fractions(
                    data_null_model_1, data_null_model_2, "Null Model")
                null_total = len(data_null_model_1)
                null_counts = [int(null_class1_frac * null_total), 
                              int(null_class2_frac * null_total), 
                              int(null_class3_frac * null_total)]
                
                all_class_data[medium][species_num]['null_counts'] = null_counts
                all_class_data[medium][species_num]['null_total'] = null_total
        
        all_data.append(medium_data)
    
    # Create merged plots
    print("\nCreating merged plots...")
    
    # Merged polarized plot
    f = PolarizedPlot_merged(all_data, colors, [6, 12, 24])
    f.savefig(f'{output_dir}/Metric_metric3_all_exp_merged_Polarized.svg', bbox_inches='tight')
    plt.close()
    
    # Merged class fraction comparison
    fig = plot_class_fraction_comparison_merged(all_class_data, colors)
    fig.savefig(f'{output_dir}/ClassFractions_all_exp_merged_GroupedBarPlot.svg', bbox_inches='tight')
    plt.close()
    
    # Create individual plots for each medium with all species pools
    for c_i, medium in enumerate(['LN', 'MN', 'HN']):
        if c_i >= len(all_data) or not all_data[c_i]:
            continue
            
        # Combined plot for this medium
        mm = 1 / 25.4
        f, ax = plt.subplots(1, 1, figsize=(80*mm, 80*mm), facecolor='w', edgecolor='k')
        
        # Plot data for all species pools
        markers = ['o', 's', '^']
        alphas = [0.5, 0.7, 0.9]
        
        for pool_idx, pool_size in enumerate([6, 12, 24]):
            if pool_size in all_data[c_i]:
                data1, data2 = all_data[c_i][pool_size]['real']
                ax.scatter(data1, data2, s=30, color=colors[c_i], marker=markers[pool_idx], 
                          alpha=alphas[pool_idx], linewidths=0, label=f'Pool {pool_size}')
                ax.scatter(data2, data1, s=30, color='grey', marker=markers[pool_idx], 
                          alpha=0.2, linewidths=0)
        
        # Background
        x = np.linspace(-0.15, 1.2, 500)
        y = np.linspace(-0.15, 1.2, 500)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(abs(X**2 + Y**2))
        ax.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey', 
                  alpha=0.2, linewidths=0.5)
        
        ax.axhline(0, color='k', linestyle='--', linewidth=.8)
        ax.axvline(0, color='k', linestyle='--', linewidth=.8)
        
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xticks([0, 0.5, 1.0])
        ax.set_yticks([0, 0.5, 1.0])
        
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.set_title(f'{medium} - All Species Pools')
        ax.legend(loc='upper right', fontsize=8)
        
        f.savefig(f'{output_dir}/Metric_metric3_{medium}_all_pools_exp_Polarized.svg', 
                 bbox_inches='tight')
        plt.close()
    
    # Create merged theta distribution plots (combining all species pools for each medium)
    print("\nCreating merged theta distribution plots...")
    
    theta_plots_created = 0
    
    for c_i, medium in enumerate(['LN', 'MN', 'HN']):
        if c_i >= len(all_data) or not all_data[c_i]:
            continue
            
        # Combine data from all species pools for this medium
        all_u_merged = []
        all_v_merged = []
        
        for pool_size in [6, 12, 24]:
            if pool_size in all_data[c_i]:
                data1, data2 = all_data[c_i][pool_size]['real']
                all_u_merged.extend(data1)
                all_v_merged.extend(data2)
        
        if len(all_u_merged) > 0 and len(all_v_merged) > 0:
            # Convert to theta values
            all_u_coords = np.array(all_u_merged)
            all_v_coords = np.array(all_v_merged)
            theta_values = uv_to_theta_normalized(all_u_coords, all_v_coords)
            
            # Create merged theta plot
            theta_file = f"{output_dir}/VectorDecomp_exp_{medium}_merged_theta.svg"
            
            success, max_density = create_theta_histogram_svg(theta_values, theta_file, medium)
            if success:
                theta_plots_created += 1
                print(f"✅ Created: VectorDecomp_exp_{medium}_merged_theta.svg")
                
                # Create symmetric version
                try:
                    # Read the original SVG file
                    with open(theta_file, 'r') as f:
                        svg_content = f.read()
                    
                    # Parse histogram data
                    histogram_bars = parse_theta_histogram_data(svg_content)
                    
                    if histogram_bars:
                        # Create symmetric version
                        symmetric_file = f"{output_dir}/VectorDecomp_exp_{medium}_merged_theta_symmetric.svg"
                        input_filename = f"VectorDecomp_exp_{medium}_merged_theta.svg"
                        
                        success_symmetric = create_theta_symmetric_svg(histogram_bars, symmetric_file, input_filename, max_density, medium)
                        if success_symmetric:
                            theta_plots_created += 1
                            print(f"✅ Created: VectorDecomp_exp_{medium}_merged_theta_symmetric.svg")
                except Exception as e:
                    print(f"❌ Failed to create symmetric version for {medium}_merged: {e}")
    
    print(f"\nTheta plots created: {theta_plots_created}")
    print(f"\nAnalysis complete! All figures saved to {output_dir}")
    print(f"🎯 New theta plot features:")
    print(f"   - Angular distribution of experimental vector decomposition")
    print(f"   - Reference style: 167.330938pt × 63.93pt")
    print(f"   - Brown bars: Original theta frequencies")
    print(f"   - Symmetric versions: Grey bars stacked on top")
    print(f"   - X-axis: 0 to 1 (theta/(π/2) normalized)")
    print(f"   - Merged plots only: All species pools combined per medium")

if __name__ == "__main__":
    main()