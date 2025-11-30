#!/usr/bin/env python3
"""
Vector decomposition analysis for simulated coalescence events.
Converted from new_Plot_vectorDecomp_simulation.ipynb
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
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/VectorDecomp_sim"
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

def PolarizedPlot(data1,data2, c_i, colors):
    f, ax = plt.subplots(1,1, figsize=(60*mm,60*mm),facecolor='w', edgecolor='k')
    ax.scatter(data1,data2, s=30,color=colors[c_i], marker='.', alpha=0.7,linewidths=0)
    ax.scatter(data2,data1, s=30,color='grey', marker='.', alpha=0.2,linewidths=0)

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
    mm = 1 / 25.4  # millimeter to inch conversion

    # Compute folded theta
    theta = np.arctan2(data1, data2)

    # Create figure
    f, ax = plt.subplots(figsize=(60 * mm, 25 * mm))

    # KDE smoothing
    kde = gaussian_kde(theta, bw_method=smoothing)
    theta_vals = np.linspace(0, np.pi / 4, 500)
    kde_vals = kde(theta_vals)

    # Plot histogram
    ax.hist(theta, bins=20, range=(0, np.pi/2), color=color, edgecolor='none',  alpha=0.7, density=True)
    ax.hist(np.pi/2-theta, bins=20, range=(0, np.pi/2), color='grey', edgecolor='none',  alpha=0.7, density=True)

    # Axis settings
    ax.set_xlim(0, np.pi / 2)
    ax.set_ylim(0, 5)
    ax.set_xticks([0, np.pi/4, np.pi/2])
    ax.set_xticklabels(['0', r'$\frac{\pi}{8}$', r'$\frac{\pi}{4}$'])

    plt.tight_layout()
    return f

def PolarizedThetaPlot(data1, data2, c_i, colors):
    mm = 1 / 25.4
    f, ax = plt.subplots(1, 1, figsize=(60 * mm, 60 * mm), facecolor='w', edgecolor='k')
    ax.scatter(data1, data2, s=30, color=colors[c_i], marker='.', alpha=0.7, linewidths=0)
    ax.scatter(data2, data1, s=30, color='grey', marker='.', alpha=0.2, linewidths=0)

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
    ax.hist(r, bins=20, range=(0, 1), color=color, edgecolor='none',  alpha=0.7, density=True)
    
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
    
    errors_real = [p - l for p, l in zip(proportions_real, ci_low_real)]
    errors_null = [p - l for p, l in zip(proportions_null, ci_low_null)]

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

def main():
    """Main analysis function"""
    print("Starting vector decomposition analysis for simulation data...")
    
    # Load simulation data
    path="/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_12from48"
    loaded_results=json.load(open(path+"/Community.json"))
    
    # Color scheme - using centralized COLORMAP
    from COLORMAP import get_medium_colors
    colors = get_medium_colors()  # [LN, MN, HN] colors

    typeofplot = 'swarmpoint' 
    to_plot_null = False  # Turned off null model generation
    to_plot_subperturb = True

    # Plotting real data
    for c_i, type_intensity in enumerate([3, 5, 8]):
        type_name=f"Simul_{type_intensity}"
        print(f"Processing {type_name}...")
        
        # Use 4 communities instead of 2 to double the data points
        communities_to_use = [1, 3, 5, 7]
        X1_list, X2_list, y_list = [], [], []
        
        for community_idx in communities_to_use:
            X1_temp, X2_temp, y_temp = prepare_X1_X2_y(loaded_results, community_idx, type_intensity, eps=1e-3)
            X1_list.append(X1_temp)
            X2_list.append(X2_temp)
            y_list.append(y_temp)

        # Merge all communities
        X1 = np.concatenate(X1_list, axis=0)
        X2 = np.concatenate(X2_list, axis=0)
        y = np.concatenate(y_list, axis=0)
        
        # Limit to exactly 92 data points
        X1 = X1[:92, :]
        X2 = X2[:92, :]
        y = y[:92, :]
        
        # Initialize data lists
        data1, data2, data_null_model_1, data_null_model_2, data_subperturb_1, data_subperturb_2 = [], [], [], [], [], []
        species_num = len(np.zeros(48))  # Get species number from data
        Null_model_rep=1
        
        # Process each sample
        for i in range(len(X1)):
            for _ in range(Null_model_rep):
                # Get composition data
                c_mix = y[i]
                c_1 = X1[i]
                c_2 = X2[i]
                
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
                    try:
                        # Create mock mixtures for null model
                        mix_label = (np.random.rand(species_num) > 0.5).astype(int)
                        moc_c1 = (mix_label) * c_1 + (1 - mix_label) * c_2
                        moc_c2 = (1 - mix_label) * c_1 + (mix_label) * c_2
                        moc_c_mix = c_mix
                        # Normalize
                        moc_c1 = moc_c1 / (np.sum(moc_c1) + 1e-9)
                        moc_c2 = moc_c2 / (np.sum(moc_c2) + 1e-9)

                        # Calculate F1 and F2 metrics
                        u, v, k = metric_VectorDecomposition_onlyPositive(moc_c1, moc_c2, moc_c_mix)

                        F1 = np.sum(np.minimum(moc_c1, c_mix))
                        F2 = np.sum(np.minimum(moc_c2, c_mix))
                        
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
                            print(type_name)
                            print(u, v, k)
                    except np.linalg.LinAlgError:
                        # Skip this case if matrix is singular
                        pass

        # Print the class fractions for each data type
        print(f"\n===== Class Fractions for {type_name} =====")
        # Get fractions for real data
        real_class1_frac, real_class2_frac, real_class3_frac = print_class_fractions(data1, data2, "Real Data")
        real_total = len(data1)
        real_counts = [int(real_class1_frac * real_total), int(real_class2_frac * real_total), int(real_class3_frac * real_total)]

        null_counts = []
        null_total = 0
        if to_plot_null:
            # Get fractions for null model
            null_class1_frac, null_class2_frac, null_class3_frac = print_class_fractions(data_null_model_1, data_null_model_2, "Null Model")
            null_total = len(data_null_model_1)
            null_counts = [int(null_class1_frac * null_total), int(null_class2_frac * null_total), int(null_class3_frac * null_total)]

        if to_plot_subperturb:
            subperturb_class1_frac, subperturb_class2_frac, subperturb_class3_frac = print_class_fractions(data_subperturb_1, data_subperturb_2, "Subperturb Model")

        # Always generate main plots
        f=PolarizedPlot(data1,data2, c_i, colors)
        f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_style_Polarized.svg',bbox_inches='tight')

        f=PolarizedThetaPlot(data1,data2, c_i, colors)
        f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_style_PolarizedTheta.svg',bbox_inches='tight')

        f=thetaplot(data1, data2, colors[c_i])
        f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_style_Theta.svg',bbox_inches='tight')
        
        f=rplot(data1, data2, color=colors[c_i])
        f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_style_R.svg',bbox_inches='tight')

        # Plot comparison between real and null model (only if null model is enabled)
        if to_plot_null and len(null_counts) > 0:
            fig = plot_class_fraction_comparison(
                real_counts, 
                null_counts, 
                real_total, 
                null_total,
                color= colors[c_i],
            )
            fig.savefig(f"{output_dir}/ClassFractions_{type_name}_sim_GroupedBarPlot.svg", bbox_inches='tight')

            f= PolarizedPlot(data_null_model_1,data_null_model_2, c_i, colors)
            f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_null_style1_Polarized.svg',bbox_inches='tight')

            f = thetaplot(data_null_model_1, data_null_model_2, colors[c_i])
            f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_null_style1_Theta.svg', bbox_inches='tight')
            
            f = rplot(data_null_model_1, data_null_model_2, color=colors[c_i])
            f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_null_style1_R.svg', bbox_inches='tight')

        # Generate subpertub plots (only if subperturb model is enabled)
        if to_plot_subperturb:
            f= PolarizedPlot(data_subperturb_1,data_subperturb_2, c_i, colors)
            f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_subperturb_style1_Polarized.svg',bbox_inches='tight')

            f = thetaplot(data_subperturb_1,data_subperturb_2, colors[c_i])
            f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_subperturb_style1_Theta.svg', bbox_inches='tight')
            
            f = rplot(data_subperturb_1, data_subperturb_2, color=colors[c_i])
            f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_subperturb_style1_R.svg', bbox_inches='tight')
            
        plt.close('all')
    
    print(f"Analysis complete! All figures saved to {output_dir}")


if __name__ == "__main__":
    main()
    
    # Run analysis for 500 species data
    print("\nStarting vector decomposition analysis for 500 species simulation data...")
    
    # Load simulation data for 500 species
    path="/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural"
    
    # Check if the file exists
    if not os.path.exists(path + "/Community.json"):
        print(f"Warning: {path}/Community.json not found. Please run the simulation first.")
    else:
        loaded_results=json.load(open(path+"/Community.json"))
        
        # Color scheme - using centralized COLORMAP
        from COLORMAP import get_medium_colors
        colors = get_medium_colors()  # [LN, MN, HN] colors

        typeofplot = 'swarmpoint' 
        to_plot_null = False  # Turned off null model generation for 500-species too
        to_plot_subperturb = True

        # Plotting real data - using interaction strengths 0, 1, 2 (indices in 500-species u_list: 0.3, 0.5, 0.7)
        u_values = [0.3, 0.5, 0.7]
        for c_i, type_intensity in enumerate([0, 1, 2]):
            u_value = u_values[c_i]
            type_name=f"Simul_50from500_{u_value}"
            print(f"Processing {type_name}...")
            
            # Use 4 communities instead of 2 to double the data points for 500-species simulation
            communities_to_use_500 = [0, 1, 2, 3]  # Using communities 0-3 for 500-species
            X1_list_500, X2_list_500, y_list_500 = [], [], []
            
            for community_idx in communities_to_use_500:
                X1_temp, X2_temp, y_temp = prepare_X1_X2_y(loaded_results, community_idx, type_intensity, eps=1e-3)
                X1_list_500.append(X1_temp)
                X2_list_500.append(X2_temp)
                y_list_500.append(y_temp)

            # Merge all communities for 500-species simulation
            X1 = np.concatenate(X1_list_500, axis=0)
            X2 = np.concatenate(X2_list_500, axis=0)
            y = np.concatenate(y_list_500, axis=0)
            
            # Limit 500-species simulation to 92 data points as well
            X1 = X1[:92, :]
            X2 = X2[:92, :]
            y = y[:92, :]
            
            # Initialize data lists
            data1, data2, data_null_model_1, data_null_model_2, data_subperturb_1, data_subperturb_2 = [], [], [], [], [], []
            species_num = 500  # 500 species total
            Null_model_rep=1
            
            # Process each sample
            for i in range(len(X1)):
                for _ in range(Null_model_rep):
                    # Get composition data
                    c_mix = y[i]
                    c_1 = X1[i]
                    c_2 = X2[i]
                    
                    # Filter small values
                    c_1 = c_1 * (c_1 > 1e-4)
                    c_2 = c_2 * (c_2 > 1e-4)
                    
                    # Null model calculations
                    if to_plot_null:
                        try:
                            # Prepare for null model
                            c_1_positive = c_1[c_1 > 0]
                            c_2_positive = c_2[c_2 > 0]
                            N_1 = len(c_1_positive)
                            N_2 = len(c_2_positive)
                            
                            # Null model: Random sampling
                            num_samples_from_c1 = int(N_1 * N_1 / (N_1 + N_2))
                            num_samples_from_c2 = int(N_2 * N_2 / (N_1 + N_2))
                            
                            c_mix_simulated = np.zeros_like(c_mix)
                            idx_in_c1 = np.where(c_1 > 0)[0]
                            idx_in_c2 = np.where(c_2 > 0)[0]
                            
                            sampled_idx_c1 = np.random.choice(idx_in_c1, num_samples_from_c1, replace=False)
                            sampled_idx_c2 = np.random.choice(idx_in_c2, num_samples_from_c2, replace=False)
                            
                            for idx in sampled_idx_c1:
                                c_mix_simulated[idx] = c_1[idx]
                            for idx in sampled_idx_c2:
                                c_mix_simulated[idx] = c_2[idx]
                                
                            # Calculate metrics for null model
                            u_n, v_n, k_n = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix_simulated)
                            data_null_model_1.append(u_n)
                            data_null_model_2.append(v_n)
                        except (np.linalg.LinAlgError, ValueError) as e:
                            # Skip this case if matrix is singular
                            pass
                    
                    # Calculate metrics for real data
                    if _ == 0:
                        try:
                            u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                            data1.append(u)
                            data2.append(v)
                            
                            # Debug output for unusual cases
                            if u > 0.6 and v > 0.6:
                                print(type_name)
                                print(u, v, k)
                        except np.linalg.LinAlgError:
                            # Skip this case if matrix is singular
                            pass

            # Print the class fractions for each data type
            print(f"\n===== Class Fractions for {type_name} =====")
            # Get fractions for real data
            real_class1_frac, real_class2_frac, real_class3_frac = print_class_fractions(data1, data2, "Real Data")
            real_total = len(data1)
            real_counts = [int(real_class1_frac * real_total), int(real_class2_frac * real_total), int(real_class3_frac * real_total)]

            null_counts = []
            null_total = 0
            if to_plot_null:
                # Get fractions for null model
                null_class1_frac, null_class2_frac, null_class3_frac = print_class_fractions(data_null_model_1, data_null_model_2, "Null Model")
                null_total = len(data_null_model_1)
                null_counts = [int(null_class1_frac * null_total), int(null_class2_frac * null_total), int(null_class3_frac * null_total)]

            # Plot comparison between real and null model
            if to_plot_null and len(null_counts) > 0:
                fig = plot_class_fraction_comparison(
                    real_counts, 
                    null_counts, 
                    real_total, 
                    null_total,
                    color= colors[c_i],
                )
                fig.savefig(f"{output_dir}/ClassFractions_{type_name}_sim_GroupedBarPlot.svg", bbox_inches='tight')
                
                f=PolarizedPlot(data1,data2, c_i, colors)
                f.savefig(f'{output_dir}/Metric_metric3_{type_name}_sim_style_Polarized.svg',bbox_inches='tight')

        # Note: Combined plot function not available for 500-species data yet
        
        print("\nVector decomposition analysis for 500 species completed!")
        print(f"Results saved in {output_dir}/")