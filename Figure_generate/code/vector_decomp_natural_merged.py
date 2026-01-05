#!/usr/bin/env python3
"""
Vector decomposition analysis for natural coalescence events with merged plots.
Matching the style of vector_decomp_experimental_merged.py but without species pools.
Natural data doesn't have initial pools - all data is analyzed together per medium.
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
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_natural"
os.makedirs(output_dir, exist_ok=True)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

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

def print_class_fractions(data1, data2, type_name=None):
    class1_count = 0  # Dominance
    class2_count = 0  # Mixing
    class3_count = 0  # Restructuring

    for j in range(len(data1)):
        # Calculate asymmetricity
        x, y = calculate_assymetricity(data1[j], data2[j], 0)

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
    theta = np.abs(theta)
    theta = np.minimum(theta, np.pi/2)
    theta_normalized = theta / (np.pi/2)
    return theta_normalized

def create_theta_histogram_svg(theta_values, output_file, medium_name):
    """Create theta distribution plot matching reference style"""

    print(f"Creating theta plot: {os.path.basename(output_file)}")

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

    # Create histogram
    n_bins = 20
    hist_orig, bin_edges = np.histogram(theta_values, bins=n_bins, range=(0, 1), density=True)

    # Set fixed max density to 10 for consistent scaling
    max_density = 10.0
    hist_orig_norm = hist_orig / max_density

    # Import colors for media-specific coloring
    from COLORMAP import get_medium_color
    data_color = get_medium_color(medium_name)

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
        brown_height = hist_orig_norm[i] * plot_height

        if brown_height > 0:
            y_brown = plot_bottom - brown_height
            brown_opacity = 0.3 + 0.7 * min(hist_orig_norm[i], 1.0)

            svg_content += f'''    <rect x="{x_left:.3f}" y="{y_brown:.3f}" width="{bin_width:.3f}" height="{brown_height:.3f}" style="fill: {data_color}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''

    svg_content += '   </g>\n'

    # Add step function outline
    svg_content += '   <g id="HistogramOutline_1">\n'

    path_parts = []

    for i in range(n_bins):
        x_left = plot_left + i * bin_width
        x_right = x_left + bin_width
        brown_height = hist_orig_norm[i] * plot_height

        if brown_height > 0:
            y_top = plot_bottom - brown_height

            if not path_parts:
                path_parts.append(f"M {x_left:.3f} {plot_bottom:.3f}")
            else:
                path_parts.append(f"L {x_left:.3f} {plot_bottom:.3f}")

            path_parts.append(f"L {x_left:.3f} {y_top:.3f}")
            path_parts.append(f"L {x_right:.3f} {y_top:.3f}")
            path_parts.append(f"L {x_right:.3f} {plot_bottom:.3f}")

    if path_parts:
        path_string = " ".join(path_parts)
        svg_content += f'''    <path d="{path_string}" style="fill: none; stroke: #333333; stroke-width: 0.8"/>
'''

    svg_content += '   </g>\n'

    # Add box frame
    svg_content += f'''   <g id="axes_frame">
    <path d="M {plot_left} {plot_bottom}
L {plot_right} {plot_bottom}
L {plot_right} {plot_top}
L {plot_left} {plot_top}
L {plot_left} {plot_bottom}" style="fill: none; stroke: #262626; stroke-width: 0.8"/>
   </g>
'''

    svg_content += '''  </g>
 </g>
</svg>'''

    with open(output_file, 'w') as f:
        f.write(svg_content)

    return True, max_density

def parse_theta_histogram_data(svg_content):
    """Extract histogram data from theta SVG for symmetric version"""
    import re

    rect_pattern = r'<rect x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)" style="fill: ([^;]+); fill-opacity: ([^;]+); stroke: none"/>'
    rects = re.findall(rect_pattern, svg_content)

    histogram_bars = []

    for rect in rects:
        x, y, width, height, color, opacity = rect

        # Only process histogram bars (media-specific colors)
        if color in ['#A7216A', '#802000', '#E24912']:
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

    # Reference dimensions
    width_pt = 167.330938
    height_pt = 63.93
    plot_left = 19.5975
    plot_right = 157.810937
    plot_top = 7.2
    plot_bottom = 43.23
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top

    from COLORMAP import get_medium_color
    data_color = get_medium_color(medium_name) if medium_name else "#802000"
    grey_color = "#808080"

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

    # Add X-axis ticks (stroke-width reduced to half: 0.5 -> 0.25)
    x_tick_positions = [0, 0.5, 1.0]
    x_tick_labels = ['0', '0.5', '1']
    tick_length = 3.5

    for i, (tick_val, label) in enumerate(zip(x_tick_positions, x_tick_labels)):
        x_pos = plot_left + tick_val * plot_width
        svg_content += f'''   <g id="xtick_{i+1}">
    <g id="line2d_{i+1}">
     <path d="M 0 0
L 0 -{tick_length}
" style="stroke: #262626; stroke-width: 0.25" transform="translate({x_pos}, {plot_bottom})"/>
    </g>
    <g id="text_{i+1}">
     <text x="{x_pos}" y="{plot_bottom + 12}" style="font-family: Arial; font-size: 12.8px; text-anchor: middle; fill: #262626">{label}</text>
    </g>
   </g>
'''

    # Add Y-axis ticks (stroke-width reduced to half: 0.5 -> 0.25)
    y_tick_positions = [0.0, 1.0]
    y_tick_labels = ['0', '10']
    for i, (tick_val, label) in enumerate(zip(y_tick_positions, y_tick_labels)):
        y_pos = plot_bottom - tick_val * plot_height
        svg_content += f'''   <g id="ytick_{i+1}">
    <g id="line2d_{i+4}">
     <path d="M 0 0
L {tick_length} 0
" style="stroke: #262626; stroke-width: 0.25" transform="translate({plot_left}, {y_pos})"/>
    </g>
    <g id="text_{i+4}">
     <text x="{plot_left - 5}" y="{y_pos + 2}" style="font-family: Arial; font-size: 12.8px; text-anchor: end; fill: #262626">{label}</text>
    </g>
   </g>
'''

    # Add stacked histogram bars
    svg_content += '   <g id="HistogramCollection_1">\n'

    for bar in original_bars:
        brown_x = bar['x']
        brown_y = bar['y']
        brown_width = bar['width']
        brown_height = bar['height']
        brown_opacity = bar['opacity']

        rel_x = (brown_x - plot_left) / plot_width
        center_distance = abs(rel_x - 0.5) * 2
        grey_scale_factor = 0.3 + 0.7 * center_distance

        grey_height = brown_height * grey_scale_factor * 0.5
        grey_opacity = 0.8

        brown_height_norm = brown_height * 0.5
        grey_height_norm = grey_height * 0.5
        brown_y_norm = plot_bottom - brown_height_norm
        grey_y_norm = brown_y_norm - grey_height_norm

        svg_content += f'''    <rect x="{brown_x:.3f}" y="{brown_y_norm:.3f}" width="{brown_width:.3f}" height="{brown_height_norm:.3f}" style="fill: {data_color}; fill-opacity: {brown_opacity:.3f}; stroke: none"/>
'''
        svg_content += f'''    <rect x="{brown_x:.3f}" y="{grey_y_norm:.3f}" width="{brown_width:.3f}" height="{grey_height_norm:.3f}" style="fill: {grey_color}; fill-opacity: {grey_opacity:.3f}; stroke: none"/>
'''

    svg_content += '   </g>\n'

    # Add step function outline
    svg_content += '   <g id="HistogramOutline_1">\n'

    if original_bars:
        sorted_bars = sorted(original_bars, key=lambda b: b['x'])
        path_parts = []

        for bar in sorted_bars:
            rel_x = (bar['x'] - plot_left) / plot_width
            center_distance = abs(rel_x - 0.5) * 2
            grey_scale_factor = 0.3 + 0.7 * center_distance
            grey_height = bar['height'] * grey_scale_factor * 0.5
            brown_height_norm = bar['height'] * 0.5
            grey_height_norm = grey_height * 0.5
            total_height = brown_height_norm + grey_height_norm
            y_top = plot_bottom - total_height

            x_left = bar['x']
            x_right = bar['x'] + bar['width']

            if not path_parts:
                path_parts.append(f"M {x_left:.3f} {plot_bottom:.3f}")
            else:
                path_parts.append(f"L {x_left:.3f} {plot_bottom:.3f}")

            path_parts.append(f"L {x_left:.3f} {y_top:.3f}")
            path_parts.append(f"L {x_right:.3f} {y_top:.3f}")
            path_parts.append(f"L {x_right:.3f} {plot_bottom:.3f}")

        if path_parts:
            path_string = " ".join(path_parts)
            svg_content += f'''    <path d="{path_string}" style="fill: none; stroke: #333333; stroke-width: 0.4"/>
'''

    svg_content += '   </g>\n'

    # Add box frame (stroke-width reduced to half: 0.8 -> 0.4)
    svg_content += f'''   <g id="axes_frame">
    <path d="M {plot_left} {plot_bottom}
L {plot_right} {plot_bottom}
L {plot_right} {plot_top}
L {plot_left} {plot_top}
L {plot_left} {plot_bottom}" style="fill: none; stroke: #262626; stroke-width: 0.4"/>
   </g>
'''

    svg_content += '''  </g>
 </g>
</svg>'''

    with open(output_file, 'w') as f:
        f.write(svg_content)

    return True

def plot_class_fraction_comparison_merged(all_class_data, colors):
    """Create merged class fraction bar plot for all media"""
    mm = 1 / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(210*mm, 60*mm))

    class_names = ["Mixing", "Dominance", "Restructuring"]
    class_indices = [1, 0, 2]  # Reordering indices

    for idx, (medium_name, ax) in enumerate(zip(['LN', 'MN', 'HN'], axes)):
        x = np.arange(3)
        bar_width = 0.6  # Wider bars since no species pool comparison

        if medium_name in all_class_data:
            data = all_class_data[medium_name]

            # Reorder counts
            counts_real = [data['real_counts'][i] for i in class_indices]
            proportions_real = [counts_real[i] / data['real_total'] for i in range(3)]

            # Wilson CI
            ci_low_real = []
            for i in range(3):
                low_r, high_r = wilson_conf_int(counts_real[i], data['real_total'])
                ci_low_real.append(max(0, low_r))

            errors_real = [max(0, p - l) for p, l in zip(proportions_real, ci_low_real)]

            # Plot bars
            ax.bar(x, proportions_real, bar_width, yerr=errors_real,
                  capsize=0, alpha=0.7, edgecolor='none',
                  error_kw={'elinewidth': .5, 'capthick': 0},
                  color=colors[idx])

        # Axis settings
        ax.set_xticks(x)
        ax.set_xticklabels(class_names)
        ax.set_ylim(0, 1)
        if idx == 0:
            ax.set_ylabel("Fraction")
        ax.set_title(f'{medium_name}')

    plt.tight_layout()
    return fig

def load_natural_coalescence_data():
    """Load natural coalescence data"""
    print("Loading natural coalescence data...")

    offspring_list = []
    parent1_list = []
    parent2_list = []
    nutrient_conditions = []

    for idx, row in Coalescence_data.iterrows():
        try:
            if row.get('CommunityOrigin') != 'N':
                continue

            mixture_id = row['SampleIDX']
            parent1_id = row['SampleIDX_Sub1']
            parent2_id = row['SampleIDX_Sub2']

            # Get abundance vectors
            mixture_rows_syn = Processed_sequences_synthetic[Processed_sequences_synthetic['SampleIDX'] == mixture_id]
            mixture_rows_nat = Processed_sequences_natural[Processed_sequences_natural['SampleIDX'] == mixture_id]
            mixture_rows = pd.concat([mixture_rows_syn, mixture_rows_nat])

            parent1_rows_syn = Processed_sequences_synthetic[Processed_sequences_synthetic['SampleIDX'] == parent1_id]
            parent1_rows_nat = Processed_sequences_natural[Processed_sequences_natural['SampleIDX'] == parent1_id]
            parent1_rows = pd.concat([parent1_rows_syn, parent1_rows_nat])

            parent2_rows_syn = Processed_sequences_synthetic[Processed_sequences_synthetic['SampleIDX'] == parent2_id]
            parent2_rows_nat = Processed_sequences_natural[Processed_sequences_natural['SampleIDX'] == parent2_id]
            parent2_rows = pd.concat([parent2_rows_syn, parent2_rows_nat])

            if mixture_rows.empty or parent1_rows.empty or parent2_rows.empty:
                continue

            # Extract abundance vectors
            mixture_vector = mixture_rows.iloc[0, 1:44].values.astype(float)
            parent1_vector = parent1_rows.iloc[0, 1:44].values.astype(float)
            parent2_vector = parent2_rows.iloc[0, 1:44].values.astype(float)

            # Handle NaN values
            mixture_vector = np.nan_to_num(mixture_vector, 0)
            parent1_vector = np.nan_to_num(parent1_vector, 0)
            parent2_vector = np.nan_to_num(parent2_vector, 0)

            # Normalize
            if np.sum(mixture_vector) > 0:
                mixture_vector = mixture_vector / np.sum(mixture_vector)
            if np.sum(parent1_vector) > 0:
                parent1_vector = parent1_vector / np.sum(parent1_vector)
            if np.sum(parent2_vector) > 0:
                parent2_vector = parent2_vector / np.sum(parent2_vector)

            # Determine nutrient condition
            nutrient_condition = determine_nutrient_condition_from_metadata(mixture_id)

            if (np.sum(mixture_vector) > 0 and
                np.sum(parent1_vector) > 0 and
                np.sum(parent2_vector) > 0):

                offspring_list.append(mixture_vector)
                parent1_list.append(parent1_vector)
                parent2_list.append(parent2_vector)
                nutrient_conditions.append(nutrient_condition)

        except Exception as e:
            continue

    print(f"Successfully loaded {len(offspring_list)} natural coalescence events")
    if len(offspring_list) > 0:
        print(f"Nutrient distribution: LN={nutrient_conditions.count('LN')}, MN={nutrient_conditions.count('MN')}, HN={nutrient_conditions.count('HN')}")

    return offspring_list, parent1_list, parent2_list, nutrient_conditions

def determine_nutrient_condition_from_metadata(sample_id):
    """Determine nutrient condition from metadata or sample ID pattern"""
    metadata_rows = Metadata[Metadata['SampleIDX'] == sample_id]

    if not metadata_rows.empty:
        medium = metadata_rows.iloc[0]['Medium']
        if medium == 'H':
            return 'HN'
        elif medium == 'M':
            return 'MN'
        elif medium == 'L':
            return 'LN'

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
    """Main analysis function for natural community merged plots"""
    print("Starting vector decomposition analysis for natural community data (merged plots)...")

    # Color scheme
    from COLORMAP import get_medium_colors
    colors = get_medium_colors()  # [LN, MN, HN] colors

    # Load natural coalescence data
    offspring_list, parent1_list, parent2_list, nutrient_conditions = load_natural_coalescence_data()

    if len(offspring_list) == 0:
        print("No natural coalescence data found!")
        return

    # Storage for all data
    all_data = {}  # {medium: {'real': (data1, data2)}}
    all_class_data = {}  # {medium: {'real_counts': [], 'real_total': int}}

    # Process each medium type
    for c_i, medium in enumerate(['LN', 'MN', 'HN']):
        print(f"\nProcessing {medium} natural communities...")

        # Filter data for this condition
        condition_indices = [i for i, c in enumerate(nutrient_conditions) if c == medium]

        if len(condition_indices) == 0:
            print(f"No data found for {medium}")
            continue

        print(f"Found {len(condition_indices)} events for {medium}")

        # Initialize data lists
        data1, data2 = [], []

        # Process each sample
        for i in condition_indices:
            try:
                c_mix = offspring_list[i]
                c_1 = parent1_list[i]
                c_2 = parent2_list[i]

                # Filter small values
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)

                # Calculate metrics for real data
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                data1.append(u)
                data2.append(v)

            except np.linalg.LinAlgError:
                pass

        if len(data1) == 0:
            print(f"No valid data for {medium} after processing")
            continue

        # Store data
        all_data[medium] = {'real': (data1, data2)}

        # Calculate class fractions
        print(f"\nClass Fractions for {medium} Natural:")
        real_class1_frac, real_class2_frac, real_class3_frac = print_class_fractions(data1, data2, "Real Data")
        real_total = len(data1)
        real_counts = [int(real_class1_frac * real_total),
                      int(real_class2_frac * real_total),
                      int(real_class3_frac * real_total)]

        all_class_data[medium] = {
            'real_counts': real_counts,
            'real_total': real_total
        }

    # Create merged plots
    print("\nCreating merged plots...")

    # Merged class fraction comparison
    fig = plot_class_fraction_comparison_merged(all_class_data, colors)
    fig.savefig(f'{output_dir}/ClassFractions_all_natural_merged_GroupedBarPlot.svg', bbox_inches='tight')
    plt.close()
    print(f"✅ Created: ClassFractions_all_natural_merged_GroupedBarPlot.svg")

    # Create combined polarized plot (all media together)
    mm = 1 / 25.4
    f, axes = plt.subplots(1, 3, figsize=(180*mm, 60*mm), facecolor='w', edgecolor='k')

    for c_i, medium in enumerate(['LN', 'MN', 'HN']):
        ax = axes[c_i]

        if medium in all_data:
            data1, data2 = all_data[medium]['real']
            ax.scatter(data1, data2, s=25, color=colors[c_i], marker='o',
                      alpha=0.7, linewidths=0)
            ax.scatter(data2, data1, s=25, color='grey', marker='o',
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

        titles = ['Low Nutrient', 'Medium Nutrient', 'High Nutrient']
        ax.set_title(titles[c_i])

    plt.tight_layout()
    f.savefig(f'{output_dir}/Metric_metric3_all_natural_merged_Polarized.svg', bbox_inches='tight')
    plt.close()
    print(f"✅ Created: Metric_metric3_all_natural_merged_Polarized.svg")

    # Create individual polarized plots for each medium
    for c_i, medium in enumerate(['LN', 'MN', 'HN']):
        if medium not in all_data:
            continue

        mm = 1 / 25.4
        f, ax = plt.subplots(1, 1, figsize=(80*mm, 80*mm), facecolor='w', edgecolor='k')

        data1, data2 = all_data[medium]['real']
        ax.scatter(data1, data2, s=30, color=colors[c_i], marker='o',
                  alpha=0.7, linewidths=0)
        ax.scatter(data2, data1, s=30, color='grey', marker='o',
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

        # Add title to match experimental style dimensions
        ax.set_title(f'{medium} - Natural')

        f.savefig(f'{output_dir}/Metric_metric3_{medium}_natural_Polarized.svg', bbox_inches='tight')
        plt.close()
        print(f"✅ Created: Metric_metric3_{medium}_natural_Polarized.svg")

    # Create theta distribution plots
    print("\nCreating theta distribution plots...")

    theta_plots_created = 0

    for c_i, medium in enumerate(['LN', 'MN', 'HN']):
        if medium not in all_data:
            continue

        data1, data2 = all_data[medium]['real']

        if len(data1) > 0 and len(data2) > 0:
            # Convert to theta values
            all_u_coords = np.array(data1)
            all_v_coords = np.array(data2)
            theta_values = uv_to_theta_normalized(all_u_coords, all_v_coords)

            # Create theta plot
            theta_file = f"{output_dir}/VectorDecomp_natural_{medium}_merged_theta.svg"

            success, max_density = create_theta_histogram_svg(theta_values, theta_file, medium)
            if success:
                theta_plots_created += 1
                print(f"✅ Created: VectorDecomp_natural_{medium}_merged_theta.svg")

                # Create symmetric version
                try:
                    with open(theta_file, 'r') as f:
                        svg_content = f.read()

                    histogram_bars = parse_theta_histogram_data(svg_content)

                    if histogram_bars:
                        symmetric_file = f"{output_dir}/VectorDecomp_natural_{medium}_merged_theta_symmetric.svg"
                        input_filename = f"VectorDecomp_natural_{medium}_merged_theta.svg"

                        success_symmetric = create_theta_symmetric_svg(histogram_bars, symmetric_file, input_filename, max_density, medium)
                        if success_symmetric:
                            theta_plots_created += 1
                            print(f"✅ Created: VectorDecomp_natural_{medium}_merged_theta_symmetric.svg")
                except Exception as e:
                    print(f"❌ Failed to create symmetric version for {medium}: {e}")

    print(f"\nTheta plots created: {theta_plots_created}")
    print(f"\nAnalysis complete! All figures saved to {output_dir}")

if __name__ == "__main__":
    main()
