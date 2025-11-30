#!/usr/bin/env python3
"""
Vector decomposition analysis for natural coalescence events.
Based on natural experiment handling from AsymmetricityNullModelAnalysis.py
"""

from common_setup import *
from pathlib import Path
import json
import os
from scipy.stats import binomtest
from scipy.stats import gaussian_kde

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

def PolarizedPlot(data1,data2, c_i, colors):
    mm = 1 / 25.4
    f, ax = plt.subplots(1,1, figsize=(60*mm,60*mm),facecolor='w', edgecolor='k')
    ax.scatter(data1,data2, s=25,color=colors[c_i], marker='.', alpha=0.7,linewidths=0)
    ax.scatter(data2,data1, s=25,color='grey', marker='.', alpha=0.2,linewidths=0)

    # Define the grid of points
    x = np.linspace(-0.15, 1.2, 500)
    y = np.linspace(-0.15, 1.2, 500)
    X, Y = np.meshgrid(x, y)

    # Calculate the radius from the origin
    R = np.sqrt(abs(X**2 + Y**2))
    contour = plt.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey', alpha=0.2, linewidths=0.5)
    
    # Add auxiliary lines at x=0 and y=0
    plt.axhline(0, color='k', linestyle='--', linewidth=.8)
    plt.axvline(0, color='k', linestyle='--', linewidth=.8)

    # Set plot limits and labels
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.xticks([0, 0.5, 1.0])
    plt.yticks([0, 0.5, 1.0])
    # Remove the outer box (spines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    return f

def thetaplot(data1, data2, color, smoothing=0.1):
    mm = 1 / 25.4

    # Compute theta/(π/2) normalized to range [0, 1]
    theta = np.arctan2(data2, data1)  # Note: swapped to match our convention
    theta = np.abs(theta)
    theta = np.minimum(theta, np.pi/2)
    theta_normalized = theta / (np.pi/2)  # Normalize to [0, 1]
    
    # Compute inverted theta for stacking
    theta_inverted = 1 - theta_normalized

    # Create figure with exact reference dimensions
    f, ax = plt.subplots(figsize=(167.330938/25.4 * mm, 63.93/25.4 * mm))

    # Create histograms for stacking
    n_bins = 20
    hist_orig, bin_edges = np.histogram(theta_normalized, bins=n_bins, range=(0, 1))
    hist_inverted, _ = np.histogram(theta_inverted, bins=n_bins, range=(0, 1))
    
    # Normalize by maximum for proper scaling
    max_val = np.max(hist_orig)
    if max_val > 0:
        hist_orig_norm = hist_orig / max_val
    else:
        hist_orig_norm = hist_orig

    # Plot stacked bars (brown + grey)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = bin_edges[1] - bin_edges[0]
    
    # Normalize inverted histogram by same factor for consistent stacking
    max_combined = np.max(hist_orig + hist_inverted)
    if max_combined > 0:
        hist_orig_norm = hist_orig / max_combined
        hist_inverted_norm = hist_inverted / max_combined
    else:
        hist_orig_norm = hist_orig
        hist_inverted_norm = hist_inverted
    
    for i in range(n_bins):
        brown_height = hist_orig[i]
        grey_height = hist_inverted[i]
        
        if brown_height > 0 or grey_height > 0:
            # Brown bar (bottom)
            if brown_height > 0:
                brown_opacity = 0.3 + 0.7 * hist_orig_norm[i]
                ax.bar(bin_centers[i], brown_height, width=bin_width, color=color, alpha=brown_opacity, edgecolor='none')
            
            # Grey bar (top)
            if grey_height > 0:
                grey_opacity = 0.3 + 0.7 * hist_inverted_norm[i]
                ax.bar(bin_centers[i], grey_height, width=bin_width, bottom=brown_height, 
                       color='#808080', alpha=grey_opacity, edgecolor='none')

    # Add step function outline around combined bars
    if np.any(hist_orig + hist_inverted > 0):
        # Create step function coordinates for total height
        x_vals = []
        y_vals = []
        
        for i in range(n_bins):
            total_height = hist_orig[i] + hist_inverted[i]
            if total_height > 0:
                x_left = bin_edges[i]
                x_right = bin_edges[i+1]
                
                # Add points for step function
                x_vals.extend([x_left, x_left, x_right, x_right])
                y_vals.extend([0, total_height, total_height, 0])
        
        if x_vals:
            ax.plot(x_vals, y_vals, color='#333333', linewidth=0.8)

    # Axis settings - match our new style
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 30)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(['0', '0.5', '1'])
    
    # Increase tick label size
    ax.tick_params(axis='both', which='major', labelsize=12.8*72/25.4/2.54)  # Convert to matplotlib points

    # Remove spines for clean look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    return f

def PolarizedThetaPlot(data1, data2, c_i, colors):
    mm = 1 / 25.4
    f, ax = plt.subplots(1, 1, figsize=(60 * mm, 60 * mm), facecolor='w', edgecolor='k')
    ax.scatter(data1, data2, s=25, color=colors[c_i], marker='.', alpha=0.7, linewidths=0)
    ax.scatter(data2, data1, s=25, color='grey', marker='.', alpha=0.2, linewidths=0)

    # Background radial contours
    x = np.linspace(-0.15, 1.2, 500)
    y = np.linspace(-0.15, 1.2, 500)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    ax.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey', alpha=0.2, linewidths=0.5)

    # Axes lines
    ax.axhline(0, color='k', linestyle='--', linewidth=.8)
    ax.axvline(0, color='k', linestyle='--', linewidth=.8)

    # Add theta density curve along quarter circle
    theta = np.arctan2(data1, data2) - np.pi / 4
    theta = np.append(theta, -theta)  # Reflect for symmetry

    kde = gaussian_kde(theta, bw_method=0.1)
    theta_vals = np.linspace(-np.pi / 4, np.pi / 4, 500)
    density_vals = kde(theta_vals)

    # Convert polar to Cartesian coordinates for quarter arc
    r_base = 1.05
    r = r_base + 0.1 * density_vals
    x_theta = r * np.cos(theta_vals + np.pi / 4)
    y_theta = r * np.sin(theta_vals + np.pi / 4)

    ax.plot(x_theta, y_theta, color=colors[c_i], linewidth=1.2)
    ax.fill_betweenx(y_theta, x_theta, r_base * np.cos(theta_vals + np.pi / 4), color=colors[c_i], alpha=0.2)

    # Styling
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_yticks([0, 0.5, 1.0])
    for side in ['top', 'right', 'bottom', 'left']:
        ax.spines[side].set_visible(False)

    return f

def rplot(data1, data2, color='blue', smoothing=0.1):
    mm = 1 / 25.4
    
    # Calculate r as the Euclidean distance
    r = np.sqrt(np.array(data1)**2 + np.array(data2)**2)
    
    # Create figure
    f, ax = plt.subplots(figsize=(60*mm,30*mm))
    
    # KDE for smoothing
    kde = gaussian_kde(r, bw_method=smoothing)
    r_vals = np.linspace(r.min(), r.max(), 500)
    kde_vals = kde(r_vals)
    
    # Plot histogram
    ax.hist(r, bins=20, range=(0, np.pi/4), color=color, edgecolor='none',  alpha=0.7, density=False)
    
    # Set x-axis limits based on range of r
    ax.set_xlim(0, 1)
    
    plt.tight_layout()
    
    return f

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

def plot_class_fraction_comparison(class_counts_real, class_counts_null, total_real, total_null, color):
    mm = 1 / 25.4
    # Class order
    class_names = ["Mixing", "Dominance", "Restructuring"]
    class_indices = [1, 0, 2]  # Reordering indices for correct class order

    # Reorder counts
    counts_real = [class_counts_real[i] for i in class_indices]
    counts_null = [class_counts_null[i] for i in class_indices]

    proportions_real = [counts_real[i] / total_real for i in range(3)]
    proportions_null = [counts_null[i] / total_null for i in range(3)]

    # Compute Wilson 95% CI
    ci_low_real = []
    ci_low_null = []
    for i in range(3):
        low_r, _ = wilson_conf_int(counts_real[i], total_real)
        low_n, _ = wilson_conf_int(counts_null[i], total_null)
        ci_low_real.append(low_r)
        ci_low_null.append(low_n)
    
    errors_real = [max(0, p - l) for p, l in zip(proportions_real, ci_low_real)]  # Ensure non-negative
    errors_null = [max(0, p - l) for p, l in zip(proportions_null, ci_low_null)]  # Ensure non-negative

    # P-value testing
    p_values = [
        binomtest(counts_real[i], total_real, proportions_null[i], alternative='two-sided').pvalue
        for i in range(3)
    ]

    # Plot setup
    x = np.arange(3)
    bar_width = 0.35
    fig, ax = plt.subplots(figsize=(70 * mm, 60 * mm))

    # Null model (left bars, grey)
    ax.bar(x - bar_width/2, proportions_null, bar_width, yerr=errors_null, capsize=0, alpha=0.5, edgecolor='none', error_kw={'elinewidth': .5, 'capthick': 0},
           label='Null Model', color='grey')

    # Real data (right bars, color-coded)
    ax.bar(x + bar_width/2, proportions_real, bar_width, yerr=errors_real, capsize=0, alpha=0.7, edgecolor='none', error_kw={'elinewidth': .5, 'capthick': 0},
           label='Experiment', color=color)

    # Axis settings
    ax.set_xticks(x)
    ax.set_xticklabels(class_names)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Fraction")
    ax.legend()

    # Significance stars
    def p_to_stars(p):
        if p < 0.001:
            return '***'
        elif p < 0.01:
            return '**'
        elif p < 0.05:
            return '*'
        else:
            return 'n.s.'

    for i, p in enumerate(p_values):
        stars = p_to_stars(p)
        
        # Determine height for the line and star
        y1 = proportions_null[i] + errors_null[i]
        y2 = proportions_real[i] + errors_real[i]
        y = max(y1, y2) + 0.05  # vertical offset above the taller bar

        # Draw horizontal bracket
        ax.plot([x[i] - bar_width/2, x[i] + bar_width/2], [y, y], color='black', linewidth=0.8)
        ax.plot([x[i] - bar_width/2, x[i] - bar_width/2], [y - 0.01, y], color='black', linewidth=0.8)
        ax.plot([x[i] + bar_width/2, x[i] + bar_width/2], [y - 0.01, y], color='black', linewidth=0.8)
        
        # Add significance stars above the line
        ax.text(x[i], y + 0.01, stars, ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout()
    return fig

def load_natural_coalescence_data():
    """
    Load natural coalescence data following the approach from AsymmetricityNullModelAnalysis.py
    """
    print("Loading natural coalescence data...")
    
    offspring_list = []
    parent1_list = []
    parent2_list = []
    nutrient_conditions = []
    species_numbers = []
    
    # Process coalescence data and filter for natural communities only
    for idx, row in Coalescence_data.iterrows():
        try:
            # Only process natural communities (CommunityOrigin == 'N')
            if row.get('CommunityOrigin') != 'N':
                continue
                
            mixture_id = row['SampleIDX']
            parent1_id = row['SampleIDX_Sub1']
            parent2_id = row['SampleIDX_Sub2']
            
            # Get abundance vectors from processed sequences (both synthetic and natural)
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
            
            # Count observed species for species pool estimation
            n_observed_species = np.sum(mixture_vector > 0)
            
            # Determine nutrient condition from metadata
            nutrient_condition = determine_nutrient_condition_from_metadata(mixture_id)
            
            # Only include if all vectors have non-zero abundance
            if (np.sum(mixture_vector) > 0 and 
                np.sum(parent1_vector) > 0 and 
                np.sum(parent2_vector) > 0):
                
                offspring_list.append(mixture_vector)
                parent1_list.append(parent1_vector)
                parent2_list.append(parent2_vector)
                nutrient_conditions.append(nutrient_condition)
                species_numbers.append(n_observed_species)  # Use observed species for natural data
                
        except Exception as e:
            continue
    
    print(f"Successfully loaded {len(offspring_list)} natural coalescence events")
    if len(offspring_list) > 0:
        print(f"Nutrient distribution: LN={nutrient_conditions.count('LN')}, MN={nutrient_conditions.count('MN')}, HN={nutrient_conditions.count('HN')}")
        print(f"Species range: {min(species_numbers)} - {max(species_numbers)}")
    
    return offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers

def determine_nutrient_condition_from_metadata(sample_id):
    """Determine nutrient condition from metadata or sample ID pattern"""
    # Try metadata first
    metadata_rows = Metadata[Metadata['SampleIDX'] == sample_id]
    
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
    """Main analysis function for natural communities"""
    print("Starting vector decomposition analysis for natural community data...")
    
    # Load natural coalescence data
    offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers = load_natural_coalescence_data()
    
    if len(offspring_list) == 0:
        print("No natural coalescence data found!")
        return
    
    # Color scheme - using centralized COLORMAP
    from COLORMAP import get_medium_colors
    colors = get_medium_colors()  # [LN, MN, HN] colors

    to_plot_null = True
    to_plot_subperturb = True

    # Analyze by nutrient condition (natural data doesn't have species pool stratification)
    for c_i, condition in enumerate(['LN', 'MN', 'HN']):
        print(f"Processing {condition} natural communities...")
        
        # Filter data for this condition
        condition_indices = [i for i, c in enumerate(nutrient_conditions) if c == condition]
        
        if len(condition_indices) == 0:
            print(f"No data found for {condition}")
            continue
            
        print(f"Found {len(condition_indices)} events for {condition}")
        
        # Initialize data lists
        data1, data2, data_null_model_1, data_null_model_2, data_subperturb_1, data_subperturb_2 = [], [], [], [], [], []
        species_num = 43  # Natural communities use all 43 species
        Null_model_rep = 1
        
        # Process each sample
        for i in condition_indices:
            for _ in range(Null_model_rep):
                # Get composition data
                c_mix = offspring_list[i]
                c_1 = parent1_list[i]
                c_2 = parent2_list[i]
                
                # Filter small values
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                if to_plot_null:
                    try:
                        # Create mock mixtures for null model
                        mix_label = (np.random.rand(species_num))
                        moc_c1 = c_1
                        moc_c2 = c_2
                        
                        # Normalize
                        moc_c_mix= (mix_label) * c_1 + mix_label * c_2
                        moc_c_mix= moc_c_mix / (np.sum(moc_c_mix) + 1e-9)
                        
                        # Calculate F1 and F2 metrics
                        u, v, k = metric_VectorDecomposition_onlyPositive(moc_c1, moc_c2, moc_c_mix)
                        
                        data_null_model_1.append(u)
                        data_null_model_2.append(v)
                    except np.linalg.LinAlgError:
                        # Skip this case if matrix is singular
                        pass
                
                if to_plot_subperturb:
                    for j in range(10):  # Reduced iterations for natural data
                        try:
                            # Create mock mixtures for sub-perturbation model
                            mix_label = (np.random.rand(species_num) > 0.5).astype(int)
                            moc_c1 = (mix_label) * c_1 + (1 - mix_label) * c_2
                            moc_c2 = (1 - mix_label) * c_1 + (mix_label) * c_2
                            moc_c_mix = c_mix
                            # Normalize
                            moc_c1 = moc_c1 / (np.sum(moc_c1) + 1e-9)
                            moc_c2 = moc_c2 / (np.sum(moc_c2) + 1e-9)

                            # Calculate F1 and F2 metrics
                            u, v, k = metric_VectorDecomposition_onlyPositive(moc_c1, moc_c2, moc_c_mix)
                            
                            data_subperturb_1.append(u)
                            data_subperturb_2.append(v)
                        except np.linalg.LinAlgError:
                            # Skip this case if matrix is singular
                            pass
                
                if _ == 0:
                    try:
                        # Calculate metrics for real data
                        u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                        data1.append(u)
                        data2.append(v)
                        
                        # Debug output for unusual cases
                        if u > 0.6 and v > 0.6:
                            print(f"{condition}: High symmetry case: u={u:.3f}, v={v:.3f}, k={k:.3f}")
                    except np.linalg.LinAlgError:
                        # Skip this case if matrix is singular
                        pass

        if len(data1) == 0:
            print(f"No valid data for {condition} after processing")
            continue

        # Print the class fractions for each data type
        print(f"\n===== Class Fractions for {condition} Natural =====")
        # Get fractions for real data
        real_class1_frac, real_class2_frac, real_class3_frac = print_class_fractions(data1, data2, "Real Data")
        real_total = len(data1)
        real_counts = [int(real_class1_frac * real_total), int(real_class2_frac * real_total), int(real_class3_frac * real_total)]

        null_counts = []
        null_total = 0
        if to_plot_null and len(data_null_model_1) > 0:
            # Get fractions for null model
            null_class1_frac, null_class2_frac, null_class3_frac = print_class_fractions(data_null_model_1, data_null_model_2, "Null Model")
            null_total = len(data_null_model_1)
            null_counts = [int(null_class1_frac * null_total), int(null_class2_frac * null_total), int(null_class3_frac * null_total)]

        if to_plot_subperturb and len(data_subperturb_1) > 0:
            subperturb_class1_frac, subperturb_class2_frac, subperturb_class3_frac = print_class_fractions(data_subperturb_1, data_subperturb_2, "Subperturb Model")
            subperturb_total = len(data_subperturb_1)
            subperturb_counts = [int(subperturb_class1_frac * subperturb_total), int(subperturb_class2_frac * subperturb_total), int(subperturb_class3_frac * subperturb_total)]

        # Plot comparison between real and null model
        if to_plot_null and len(null_counts) > 0:
            fig = plot_class_fraction_comparison(
                real_counts, 
                null_counts, 
                real_total, 
                null_total,
                color= colors[c_i],
            )
            fig.savefig(f"{output_dir}/ClassFractions_{condition}_natural_GroupedBarPlot.svg", bbox_inches='tight')
            
            if to_plot_subperturb and len(subperturb_counts) > 0:
                fig = plot_class_fraction_comparison(
                    real_counts, 
                    subperturb_counts, 
                    real_total, 
                    subperturb_total,
                    color= colors[c_i],
                )
                fig.savefig(f"{output_dir}/ClassFractions_{condition}_natural_subperturb_GroupedBarPlot.svg", bbox_inches='tight')
            
            f=PolarizedPlot(data1,data2, c_i, colors)
            f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_style_Polarized.svg',bbox_inches='tight')

            f=PolarizedThetaPlot(data1,data2, c_i, colors)
            f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_style_PolarizedTheta.svg',bbox_inches='tight')

            f=thetaplot(data1, data2, colors[c_i])
            f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_style_Theta.svg',bbox_inches='tight')
            
            f=rplot(data1, data2, color=colors[c_i])
            f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_style_R.svg',bbox_inches='tight')

            f= PolarizedPlot(data_null_model_1,data_null_model_2, c_i, colors)
            f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_null_style1_Polarized.svg',bbox_inches='tight')

            f = thetaplot(data_null_model_1, data_null_model_2, colors[c_i])
            f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_null_style1_Theta.svg', bbox_inches='tight')
            
            f = rplot(data_null_model_1, data_null_model_2, color=colors[c_i])
            f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_null_style1_R.svg', bbox_inches='tight')
            
            if len(data_subperturb_1) > 0:
                f= PolarizedPlot(data_subperturb_1,data_subperturb_2, c_i, colors)
                f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_subperturb_style1_Polarized.svg',bbox_inches='tight')

                f = thetaplot(data_subperturb_1,data_subperturb_2, colors[c_i])
                f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_subperturb_style1_Theta.svg', bbox_inches='tight')
                
                f = rplot(data_subperturb_1, data_subperturb_2, color=colors[c_i])
                f.savefig(f'{output_dir}/Metric_metric3_{condition}_natural_subperturb_style1_R.svg', bbox_inches='tight')
            
            plt.close('all')

    print(f"Analysis complete! All figures saved to {output_dir}")

if __name__ == "__main__":
    main()