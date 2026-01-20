"""
Generate_Fig5_4_MostAbundant_experimental.py

Purpose: Analyzes the relationship between most abundant species in communities and coalescence outcomes
Key features:
- Calculates fraction of most abundant species in communities
- Creates histograms of most abundant species fractions across media conditions
- Compares species-level pairwise interactions with community-level outcomes
- Creates scatter plots showing correlation between species dominance and community dominance (combined pools only)
- Creates M+H combined plot with colored regression lines
- Creates M+H combined plot with most abundant species REMOVED (tests subdominant species interactions)
- Creates M+H combined plot with Y-AXIS = dominant species fraction in coalesced community
- Uses experimental pairwise count data from colony counting experiments

Saving paths:
- 'Figure/TopDownAnaylsis/Fig_Abundant_Parent.svg'
- 'Figure/TopDownAnaylsis/Fig_Abundant_Coalesced.svg'
- 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_{medium}_Combined.svg' (combines S6, S12, S24)
- 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_M_H_Combined.svg' (combines M and H media)
- 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_M_H_Combined_AbundantRemoved.svg' (with abundant species removed)
- 'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_M_H_Combined_DominantFraction.svg' (y-axis = dominant fraction in coalesced)
- 'Figure/TopDownAnaylsis/Fig_5-7_MostAbundanceSpeciesFraction_{medium}N.svg'
- 'Figure/TopDownAnaylsis/Fig_5-7_MostAbundanceSpeciesFraction_{medium}N_Coal.svg'
"""

from common_setup import *

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

def calculate_assymetricity(u,v,k):
    x=np.sqrt(np.array(u)**2+np.array(v)**2)
    y=np.abs(np.abs(np.arctan(np.array(u)/np.array(v)))-np.pi/4)/(np.pi/4)  
    return x,y

def calculate_assymetricity_direction(u,v,k):
    x=np.sqrt(np.array(u)**2+np.array(v)**2)
    y=np.sign(np.array(u)-np.array(v))*np.abs(np.abs(np.arctan(np.array(u)/np.array(v)))-np.pi/4)/(np.pi/4)  
    return x,y

def characterize_case(x,y):
    if (x**2>0.5)*(y>0.5):
        return 0
    if (x**2>0.5)*(y<0.5):
        return 1
    if (x**2<0.5):
        return 2

def getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list):
    N = len(Sub_IDX_list)
    matrix = {Sub_IDX: {} for Sub_IDX in Sub_IDX_list}
    for SampleIDX in Coal_IDX_list:
        idx = np.where(Coalescence_data['SampleIDX']==SampleIDX)
        dominance1 = Coalescence_data.iloc[idx][Variable2plot].tolist()[0]
        dominance2 = 1-dominance1
        subSampleIDX1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()[0]
        subSampleIDX2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()[0]
        
        matrix[subSampleIDX1].update({subSampleIDX2: dominance1})
        matrix[subSampleIDX2].update({subSampleIDX1: dominance2})
    
    for SampleIDX in Sub_IDX_list:
        matrix[SampleIDX].update({SampleIDX: 0.5})
    
    return matrix

def getPairwiseCountData():
    """Load pairwise colony counting data from Excel file."""
    Pairwise_Count_data_path = "../../Postprocessed/PairwiseColonyCountings_processed_230915.xlsx"
    
    Mono_Count_data = {}
    Pairwise_Count_data = {}
    
    # Load monoculture data
    for i, medium in enumerate(["LN", "MN", "HN"]):
        Data = pd.read_excel(Pairwise_Count_data_path, sheet_name=i)
        Data = np.transpose(np.array(Data.values[:,1:]))
        Mono_Count_data[medium] = Data
    
    # Load pairwise data
    for i, medium in enumerate(["LN", "MN", "HN"]):
        sheet1 = 3 + i*2
        sheet2 = 4 + i*2
        Data_1 = pd.read_excel(Pairwise_Count_data_path, sheet_name=sheet1)
        Data_1 = np.array(Data_1.values[:,1:])
        Data_2 = pd.read_excel(Pairwise_Count_data_path, sheet_name=sheet2)
        Data_2 = np.array(Data_2.values[:,1:])
        Data = np.stack([Data_1, Data_2])
        Pairwise_Count_data[medium] = Data
    
    return Mono_Count_data, Pairwise_Count_data

def getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium_type):
    """Process pairwise count data to calculate ratios."""
    data_m = np.mean(Mono_Count_data[medium_type], 1)
    data_p_1 = Pairwise_Count_data[medium_type][0,:]
    data_p_2 = Pairwise_Count_data[medium_type][1,:]
    data_flag = np.array([[None] * 12]*12)
    data_p_1_converted = np.array([[None] * 12]*12)
    data_p_2_converted = np.array([[None] * 12]*12)
    data_p_ratio = np.array([[None] * 12]*12)

    for i in range(12):
        for j in range(12):
            if np.isnan(data_p_1[i,j]):
                data_flag[i,j] = 'case0'  # No data
            else:
                if data_p_1[i,j]==1 and data_p_2[i,j]==0:
                    data_flag[i,j] = 'case1'
                    data_p_1_converted[i,j] = 1
                    data_p_2_converted[i,j] = 0
                    data_p_ratio[i,j] = 1
                elif data_p_1[i,j]==0 and data_p_2[i,j]==1:
                    data_flag[i,j] = 'case2'
                    data_p_1_converted[i,j] = 0
                    data_p_2_converted[i,j] = 1
                    data_p_ratio[i,j] = 0
                else:
                    data_flag[i,j] = 'case3'
                    data_p_1_converted[i,j] = data_p_1[i,j]/data_m[i]
                    data_p_2_converted[i,j] = data_p_2[i,j]/data_m[j]
                    if data_p_1_converted[i,j] + data_p_2_converted[i,j] > 0:
                        data_p_ratio[i,j] = data_p_1_converted[i,j]/(data_p_1_converted[i,j]+data_p_2_converted[i,j])
                    else:
                        data_p_ratio[i,j] = None
    
    return data_p_1, data_p_2, data_flag, data_p_ratio

def plot_most_abundant_fraction():
    """Plot fraction of most abundant species across media conditions."""
    from COLORMAP import get_medium_colors
    colors_points = get_medium_colors()  # [LN, MN, HN] colors
    
    data = {}
    
    for c_i, medium in enumerate(['L', 'M', 'H']):   
        IDX_list = np.sort(Community_PermutateList("F", "S", medium, "S", 12, -1))
        IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
        df = Processed_sequences_synthetic.iloc[IDX_list_]
        index = np.argmax(np.array(df.values[:,1:]), 1) + 1
        val = [df.values[i,index[i]] for i in range(len(df))]
        data[c_i] = val
    
    fig = plt.figure(figsize=(35*mm, 40*mm))

    x = [0, 1, 2]
    y = np.nan_to_num([np.mean(data[i]) for i in data.keys()])
    yerr = np.nan_to_num([np.std(data[i])/np.sqrt(len(data[i])) for i in data.keys()])

    for i in range(3):
        if len(data[i]) == 0:
            continue
        random_component = (0.1*(np.random.rand(len(data[i]))-0.5))
        plt.scatter([x[i]]*len(data[i])+random_component, data[i], s=0.4, color=colors_points[i], alpha=0.3)

    bars = plt.bar(x, y, color=colors_points, alpha=0.3, linewidth=0.5)

    # Add error bars with matching colors
    for i in range(3):
        plt.errorbar(x[i], y[i], yerr=yerr[i], fmt='none',
                     ecolor=colors_points[i], elinewidth=1.2, capsize=3, capthick=1.2, alpha=0.5)

    # Add text labels to the bars (integer percentages)
    for bar, value in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f'{int(round(value*100))}%',
                ha='center', fontsize=6, va='bottom')

    plt.xticks([0, 1, 2], ['LN', 'MN', 'HN'])
    plt.xlim(-0.5, 2.5)
    plt.ylim(0, 1)

    plt.savefig('Figure/TopDownAnaylsis/Fig_Abundant_Parent.svg', bbox_inches='tight')
    plt.close()

def plot_most_abundant_fraction_coalesced():
    """Plot fraction of most abundant species across media conditions for coalesced communities."""
    from COLORMAP import get_medium_colors
    colors_points = get_medium_colors()  # [LN, MN, HN] colors

    data = {}

    for c_i, medium in enumerate(['L', 'M', 'H']):
        IDX_list = np.sort(Community_PermutateList("F", "S", medium, "C", 12, -1))
        IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
        df = Processed_sequences_synthetic.iloc[IDX_list_]
        index = np.argmax(np.array(df.values[:,1:]), 1) + 1
        val = [df.values[i,index[i]] for i in range(len(df))]
        data[c_i] = val

    fig = plt.figure(figsize=(35*mm, 40*mm))

    x = [0, 1, 2]
    y = np.nan_to_num([np.mean(data[i]) for i in data.keys()])
    yerr = np.nan_to_num([np.std(data[i])/np.sqrt(len(data[i])) for i in data.keys()])

    for i in range(3):
        if len(data[i]) == 0:
            continue
        random_component = (0.1*(np.random.rand(len(data[i]))-0.5))
        plt.scatter([x[i]]*len(data[i])+random_component, data[i], s=0.4, color=colors_points[i], alpha=0.3)

    bars = plt.bar(x, y, color=colors_points, alpha=0.3, linewidth=0.5)

    # Add error bars with matching colors
    for i in range(3):
        plt.errorbar(x[i], y[i], yerr=yerr[i], fmt='none',
                     ecolor=colors_points[i], elinewidth=1.2, capsize=3, capthick=1.2, alpha=0.5)

    # Add text labels to the bars (integer percentages)
    for bar, value in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f'{int(round(value*100))}%',
                ha='center', fontsize=6, va='bottom')

    plt.xticks([0, 1, 2], ['LN', 'MN', 'HN'])
    plt.xlim(-0.5, 2.5)
    plt.ylim(0, 1)

    plt.savefig('Figure/TopDownAnaylsis/Fig_Abundant_Coalesced.svg', bbox_inches='tight')
    plt.close()

def plot_most_abundant_histograms():
    """Plot histograms of most abundant species fractions for subcommunities and coalescence."""
    from COLORMAP import get_medium_colors
    colors = get_medium_colors()  # [LN, MN, HN] colors
    
    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        # Subcommunities
        fig = plt.figure(figsize=(60*mm, 40*mm))
        
        IDX_list = np.sort(Community_PermutateList("F", "S", medium, "S", 12, -1))
        IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
        df = Processed_sequences_synthetic.iloc[IDX_list_]
        index = np.argmax(np.array(df.values[:,1:]), 1) + 1
        val = [df.values[i,index[i]] for i in range(len(df))]
        
        plt.hist(val, bins=np.arange(0, 1, 0.05), density=False, color=colors[medium_idx], alpha=0.7)
        plt.xlim(0, 1)
        plt.xlabel('Most Abundant Species Fraction')
        plt.ylabel('Count')
        plt.title(f"{medium}N, Most Abundant Species Abundance")
        
        plt.savefig(f'Figure/TopDownAnaylsis/Fig_5-7_MostAbundanceSpeciesFraction_{medium}N.svg', bbox_inches='tight')
        plt.close()
        
        # Coalescence communities
        fig = plt.figure(figsize=(60*mm, 40*mm))
        
        IDX_list = np.sort(Community_PermutateList("F", "S", medium, "C", 12, -1))
        IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
        df = Processed_sequences_synthetic.iloc[IDX_list_]
        index = np.argmax(np.array(df.values[:,1:]), 1) + 1
        val = [df.values[i,index[i]] for i in range(len(df))]
        
        plt.hist(val, bins=np.arange(0, 1, 0.05), density=False, color=colors[medium_idx], alpha=0.7)
        plt.xlim(0, 1)
        plt.xlabel('Most Abundant Species Fraction')
        plt.ylabel('Count')
        plt.title(f"{medium}N, Most Abundant Species Abundance (Coalescence)")
        
        plt.savefig(f'Figure/TopDownAnaylsis/Fig_5-7_MostAbundanceSpeciesFraction_{medium}N_Coal.svg', bbox_inches='tight')
        plt.close()

# REMOVED: plot_species_vs_community_dominance_single_pool() function
# This function generated individual pool size plots that are no longer needed
# Only the combined plots (plot_species_vs_community_dominance_combined) are used now

def plot_species_vs_community_dominance_combined(medium='H'):
    """Plot correlation combining all species pool sizes."""
    from matplotlib.colors import Normalize
    from matplotlib.cm import ScalarMappable
    from COLORMAP import get_medium_colors, map_medium_to_index
    
    # Load pairwise count data
    Mono_Count_data, Pairwise_Count_data = getPairwiseCountData()
    data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium+'N')

    # Get coalescence data for all species pool sizes (6, 12, 24)
    data_label = []
    data_community = []
    data_abspecies = []
    data_pool_size = []  # Track pool size for each data point

    # Loop through all species pool sizes
    for pool_size in [6, 12, 24]:
        type_name = medium + f'N_{pool_size}'
        IDX_list = Syn_Coal_IDX[type_name]
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
        idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
        idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
        idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])

        # Process each coalescence event for this pool size
        for i in range(len(idx)):
            c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
            c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
            c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
            c_1 = c_1*(c_1>1e-4)
            c_2 = c_2*(c_2>1e-4)
            u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

            # Vector similarity approach: use the directional asymmetricity as community dominance measure
            x_val, y_val = calculate_assymetricity(u, v, k)
            ii = characterize_case(x_val, y_val)

            # Get directional asymmetricity for community-level dominance
            x_val, y_val = calculate_assymetricity_direction(u, v, k)

            # Calculate vector similarity-based relative competition score
            # Convert u, v components to a relative dominance measure
            # Use arctan(u/v) - π/4, range from -π/4 to π/4
            vector_similarity_score = np.arctan(u / (v + 1e-8)) - np.pi / 4

            # FILTER: Only include mixing events (u²+v² > 0.5)
            mixing_strength = u**2 + v**2
            if mixing_strength <= 0.5:
                continue

            C1 = c_1
            C1 = np.argmax(C1)
            C2 = c_2
            C2 = np.argmax(C2)

            # Check if both species are within the pairwise data matrix bounds (12x12)
            if C1 >= 12 or C2 >= 12:
                continue

            if data_p_ratio[C1, C2] == None:
                continue

            data_label.append(ii)
            # Use vector similarity-based score instead of y_val from asymmetricity
            data_community.append(vector_similarity_score)
            data_abspecies.append(np.mean([1-data_p_ratio[C1,C2], data_p_ratio[C2,C1]]))
            data_pool_size.append(pool_size)  # Track which pool size this data point is from
    
    # Process data following the style
    x_raw = 1 - np.array(data_abspecies)

    # Apply arctan normalization to x-axis (species dominance)
    # Convert from proportion (0-1) to arctan normalized form
    # If raw dominance = p, then ratio = p/(1-p), then arctan(ratio)/(π/2)
    ratio = x_raw / (1 - x_raw + 1e-8)
    x = np.arctan(ratio) / (np.pi / 2)

    # Vector similarity score is now in [-π/4, π/4] range
    y = np.array(data_community)
    data_label = np.array(data_label)
    data_pool_size = np.array(data_pool_size)

    # Store original data before duplication
    x_original = x.copy()
    y_original = y.copy()
    pool_size_original = data_pool_size.copy()

    # Duplicate data points (as in the reference style)
    duplicate = True
    if duplicate:
        x = np.concatenate((x, 1-x))
        y = np.concatenate((y, -y))
        data_label = np.concatenate((data_label, data_label))
        data_pool_size = np.concatenate((data_pool_size, data_pool_size))

    # Color setup - using centralized COLORMAP
    colors = get_medium_colors()  # [LN, MN, HN] colors
    c_i = map_medium_to_index(medium)

    # Create figure with specified style (90% of original size)
    f, ax = plt.subplots(1, 1, figsize=(45*mm, 45*mm), facecolor='w', edgecolor='k')

    # Calculate regression using ALL points (including duplicates)
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # Define markers for different pool sizes
    markers = ['o', 's', '^']  # circle, square, triangle for pool sizes 6, 12, 24
    pool_size_to_marker = {6: markers[0], 12: markers[1], 24: markers[2]}

    # Plot duplicated points first (grey, transparent) - these are the reflected points
    x_duplicated = 1 - x_original
    y_duplicated = -y_original
    for pool_size in [6, 12, 24]:
        mask = pool_size_original == pool_size
        if np.any(mask):
            plt.scatter(x_duplicated[mask], y_duplicated[mask],
                       color='grey', s=4, alpha=0.2, zorder=1,
                       marker=pool_size_to_marker[pool_size])

    # Plot original points on top (colored) with different markers
    for pool_size in [6, 12, 24]:
        mask = pool_size_original == pool_size
        if np.any(mask):
            plt.scatter(x_original[mask], y_original[mask],
                       color=colors[c_i], s=4, alpha=0.5, zorder=2,
                       marker=pool_size_to_marker[pool_size],
                       label=f'Pool {pool_size}')
    
    # Add linear regression line
    plt.plot([0, 1], slope * np.array([0, 1]) + intercept, alpha=0.8, linewidth=0.5, color='black')

    # Add heatmap overlay
    section_size = 1.0/3 + 1e-8
    sections_x = np.arange(0, 1.1, section_size)
    sections_y = np.arange(-np.pi/4, np.pi/4 + (np.pi/2)/3, (np.pi/2)/3)
    count_matrix = np.zeros((len(sections_x) - 1, len(sections_y) - 1))

    # Count points in each section
    for i in range(len(sections_x) - 1):
        for j in range(len(sections_y) - 1):
            x_min, x_max = sections_x[i], sections_x[i + 1]
            y_min, y_max = sections_y[j], sections_y[j + 1]
            count_matrix[i, j] = np.sum((x >= x_min) & (x < x_max) & (y >= y_min) & (y < y_max))

    # Create heatmap (without text annotations)
    plt.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)

    # Add R-squared annotation at bottom right
    plt.annotate('$R^2$ = {:.2f}'.format(r_squared), xy=(0.95, 0.05), xycoords='axes fraction', fontsize=11, color='black', ha='right', va='bottom')

    # Set axis properties
    plt.xlim(-0.05, 1.05)
    plt.ylim(-np.pi/4 - 0.05, np.pi/4 + 0.05)
    custom_ticks_x = [0, 1]
    custom_ticks_y = [-np.pi/4, 0, np.pi/4]
    plt.xticks(custom_ticks_x, custom_ticks_x)
    plt.yticks(custom_ticks_y, [r'$-\pi/4$', '0', r'$\pi/4$'])

    # Count aligned points for reporting
    aligned_mask = ((x > 0.5) & (y > 0)) | ((x < 0.5) & (y < 0))
    num_aligned = np.sum(aligned_mask)
    total_points_check = len(x)
    fraction_aligned = num_aligned / total_points_check

    print(f'Medium {medium} (Combined): Aligned points: {num_aligned} / {total_points_check} = {fraction_aligned:.3f}')
    
    plt.savefig(f'Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_{medium}_Combined.svg', bbox_inches='tight')
    plt.close()

def plot_species_vs_community_dominance_M_H_combined():
    """Plot correlation combining M and H medium data (all pool sizes for both media)."""
    from matplotlib.colors import Normalize
    from matplotlib.cm import ScalarMappable
    from COLORMAP import get_medium_colors, map_medium_to_index

    # Get colors for M and H
    colors = get_medium_colors()  # [LN, MN, HN] colors
    color_M = colors[1]  # MN color
    color_H = colors[2]  # HN color

    # Load pairwise count data
    Mono_Count_data, Pairwise_Count_data = getPairwiseCountData()

    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(50*mm, 50*mm), facecolor='w', edgecolor='k')

    # Collect data for both M and H media
    data_by_medium = {}

    for medium in ['M', 'H']:
        data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium+'N')


        data_label = []
        data_community = []
        data_abspecies = []
        data_pool_size = []  # Track pool size for each data point

        # Loop through all species pool sizes
        for pool_size in [6, 12, 24]:
            type_name = medium + f'N_{pool_size}'
            IDX_list = Syn_Coal_IDX[type_name]
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
            idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])

            # Process each coalescence event for this pool size
            for i in range(len(idx)):
                c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                c_1 = c_1*(c_1>1e-4)
                c_2 = c_2*(c_2>1e-4)
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

                # Vector similarity approach
                x_val, y_val = calculate_assymetricity(u, v, k)
                ii = characterize_case(x_val, y_val)

                # Get directional asymmetricity for community-level dominance
                x_val, y_val = calculate_assymetricity_direction(u, v, k)

                # Calculate vector similarity-based relative competition score
                # Use arctan(u/v) - π/4, range from -π/4 to π/4
                vector_similarity_score = np.arctan(u / (v + 1e-8)) - np.pi / 4

                # FILTER: Only include mixing events (u²+v² > 0.5)
                mixing_strength = u**2 + v**2
                if mixing_strength <= 0.5:
                    continue

                C1 = c_1
                C1 = np.argmax(C1)
                C2 = c_2
                C2 = np.argmax(C2)

                # Check if both species are within the pairwise data matrix bounds (12x12)
                if C1 >= 12 or C2 >= 12:
                    continue

                if data_p_ratio[C1, C2] == None:
                    continue

                data_label.append(ii)
                data_community.append(vector_similarity_score)
                data_abspecies.append(np.mean([1-data_p_ratio[C1,C2], data_p_ratio[C2,C1]]))
                data_pool_size.append(pool_size)  # Track which pool size this data point is from

        # Process data
        x_raw = 1 - np.array(data_abspecies)

        # Apply arctan normalization to x-axis (species dominance)
        # Convert from proportion (0-1) to arctan normalized form
        # If raw dominance = p, then ratio = p/(1-p), then arctan(ratio)/(π/2)
        ratio = x_raw / (1 - x_raw + 1e-8)
        x = np.arctan(ratio) / (np.pi / 2)

        y = np.array(data_community)
        data_label = np.array(data_label)
        data_pool_size = np.array(data_pool_size)

        # Store original data before duplication
        x_original = x.copy()
        y_original = y.copy()
        pool_size_original = data_pool_size.copy()

        # Duplicate data points
        duplicate = True
        if duplicate:
            x = np.concatenate((x, 1-x))
            y = np.concatenate((y, -y))
            data_label = np.concatenate((data_label, data_label))
            data_pool_size = np.concatenate((data_pool_size, data_pool_size))

        data_by_medium[medium] = {
            'x': x, 'y': y, 'data_label': data_label,
            'x_original': x_original, 'y_original': y_original,
            'pool_size_original': pool_size_original
        }

    # Combine all data for heatmap overlay
    all_x = np.concatenate([data_by_medium['M']['x'], data_by_medium['H']['x']])
    all_y = np.concatenate([data_by_medium['M']['y'], data_by_medium['H']['y']])

    # Add heatmap overlay (without percentage labels)
    section_size_x = 1.0/3 + 1e-8
    section_size_y = (np.pi/2)/3 + 1e-8
    sections_x = np.arange(0, 1.1, section_size_x)
    sections_y = np.arange(-np.pi/4, np.pi/4 + section_size_y, section_size_y)
    count_matrix = np.zeros((len(sections_x) - 1, len(sections_y) - 1))

    # Count points in each section (using combined M+H data)
    for i in range(len(sections_x) - 1):
        for j in range(len(sections_y) - 1):
            x_min, x_max = sections_x[i], sections_x[i + 1]
            y_min, y_max = sections_y[j], sections_y[j + 1]
            count_matrix[i, j] = np.sum((all_x >= x_min) & (all_x < x_max) & (all_y >= y_min) & (all_y < y_max))

    # Create heatmap (no percentage labels)
    plt.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)

    # Define markers for different pool sizes
    markers = ['o', 's', '^']  # circle, square, triangle for pool sizes 6, 12, 24
    pool_size_to_marker = {6: markers[0], 12: markers[1], 24: markers[2]}

    # Plot M and H data with separate colors and regression lines
    for medium in ['M', 'H']:
        x = data_by_medium[medium]['x']
        y = data_by_medium[medium]['y']
        x_original = data_by_medium[medium]['x_original']
        y_original = data_by_medium[medium]['y_original']
        pool_size_original = data_by_medium[medium]['pool_size_original']

        # Choose color
        color = color_M if medium == 'M' else color_H

        # Calculate regression
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        # Plot duplicated points first (grey, behind) with different markers
        x_duplicated = 1 - x_original
        y_duplicated = -y_original
        for pool_size in [6, 12, 24]:
            mask = pool_size_original == pool_size
            if np.any(mask):
                plt.scatter(x_duplicated[mask], y_duplicated[mask],
                           color='grey', s=4, alpha=0.2, zorder=1,
                           marker=pool_size_to_marker[pool_size])

        # Plot original points on top (colored) with different markers
        for pool_idx, pool_size in enumerate([6, 12, 24]):
            mask = pool_size_original == pool_size
            if np.any(mask):
                label = f'{medium}N Pool {pool_size}' if pool_idx == 0 or medium == 'M' else f'Pool {pool_size}'
                plt.scatter(x_original[mask], y_original[mask],
                           color=color, s=4, alpha=0.5, zorder=2,
                           marker=pool_size_to_marker[pool_size],
                           label=label)

        # Add colored regression line
        plt.plot([0, 1], slope * np.array([0, 1]) + intercept, alpha=0.8, linewidth=1.5, color=color)

        # Add R-squared annotation
        y_offset = 0.55 if medium == 'M' else 0.45
        plt.annotate(f'{medium}N: $R^2$ = {r_squared:.2f}',
                    xy=(0.05, y_offset), xycoords='axes fraction',
                    fontsize=8, color=color)

        # Count aligned points for reporting
        aligned_mask = ((x > 0.5) & (y > 0)) | ((x < 0.5) & (y < 0))
        num_aligned = np.sum(aligned_mask)
        total_points = len(x)
        fraction_aligned = num_aligned / total_points
        print(f'{medium}N: R² = {r_squared:.3f}, slope = {slope:.3f}, aligned = {fraction_aligned:.3f} ({num_aligned}/{total_points})')

    # Set axis properties
    plt.xlim(-0.05, 1.05)
    plt.ylim(-np.pi/4 - 0.05, np.pi/4 + 0.05)
    custom_ticks_x = [0, 1]
    custom_ticks_y = [-np.pi/4, 0, np.pi/4]
    plt.xticks(custom_ticks_x, custom_ticks_x)
    plt.yticks(custom_ticks_y, [r'$-\pi/4$', '0', r'$\pi/4$'])

    # Add legend for pool sizes and media
    plt.legend(loc='upper left', fontsize=5, ncol=2)

    plt.savefig('Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_M_H_Combined.svg', bbox_inches='tight')
    plt.close()

    print(f"Combined M+H plot saved!")

def plot_species_vs_community_dominance_M_H_combined_remove_abundant():
    """Plot correlation combining M and H medium data with most abundant species removed."""
    from matplotlib.colors import Normalize
    from matplotlib.cm import ScalarMappable
    from COLORMAP import get_medium_colors, map_medium_to_index

    # Get colors for M and H
    colors = get_medium_colors()  # [LN, MN, HN] colors
    color_M = colors[1]  # MN color
    color_H = colors[2]  # HN color

    # Load pairwise count data
    Mono_Count_data, Pairwise_Count_data = getPairwiseCountData()

    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(50*mm, 50*mm), facecolor='w', edgecolor='k')

    # Collect data for both M and H media
    data_by_medium = {}

    for medium in ['M', 'H']:
        data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium+'N')


        data_label = []
        data_community = []
        data_abspecies = []
        data_pool_size = []  # Track pool size for each data point

        # Loop through all species pool sizes
        for pool_size in [6, 12, 24]:
            type_name = medium + f'N_{pool_size}'
            IDX_list = Syn_Coal_IDX[type_name]
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
            idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])

            # Process each coalescence event for this pool size
            for i in range(len(idx)):
                c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                c_1 = c_1*(c_1>1e-4)
                c_2 = c_2*(c_2>1e-4)

                # Identify most abundant species in each subcommunity
                C1_idx = np.argmax(c_1)  # Most abundant in community 1
                C2_idx = np.argmax(c_2)  # Most abundant in community 2

                # Store original most abundant species for pairwise comparison
                C1 = C1_idx
                C2 = C2_idx

                # Remove most abundant species from all three communities
                c_1_removed = c_1.copy()
                c_2_removed = c_2.copy()
                c_mix_removed = np.array(c_mix.copy())

                # Set abundances of most abundant species to zero
                c_1_removed[C1_idx] = 0
                c_1_removed[C2_idx] = 0
                c_2_removed[C1_idx] = 0
                c_2_removed[C2_idx] = 0
                c_mix_removed[C1_idx] = 0
                c_mix_removed[C2_idx] = 0

                # Renormalize to sum to 1
                if np.sum(c_1_removed) > 0:
                    c_1_removed = c_1_removed / np.sum(c_1_removed)
                if np.sum(c_2_removed) > 0:
                    c_2_removed = c_2_removed / np.sum(c_2_removed)
                if np.sum(c_mix_removed) > 0:
                    c_mix_removed = c_mix_removed / np.sum(c_mix_removed)

                # Skip if any community becomes empty after removal
                if np.sum(c_1_removed) == 0 or np.sum(c_2_removed) == 0 or np.sum(c_mix_removed) == 0:
                    continue

                # Run vector decomposition on the modified communities
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1_removed, c_2_removed, c_mix_removed)

                # Vector similarity approach
                x_val, y_val = calculate_assymetricity(u, v, k)
                ii = characterize_case(x_val, y_val)

                # Get directional asymmetricity for community-level dominance
                x_val, y_val = calculate_assymetricity_direction(u, v, k)

                # Calculate vector similarity-based relative competition score
                # Use arctan(u/v) - π/4, range from -π/4 to π/4
                vector_similarity_score = np.arctan(u / (v + 1e-8)) - np.pi / 4


                # FILTER: Only include mixing events (u²+v² > 0.5)
                mixing_strength = u**2 + v**2
                if mixing_strength <= 0.5:
                    continue

                # Skip if vector decomposition resulted in NaN or inf
                if np.isnan(vector_similarity_score) or np.isinf(vector_similarity_score):
                    continue
                if np.isnan(u) or np.isnan(v) or np.isnan(k):
                    continue

                # Check if both species are within the pairwise data matrix bounds (12x12)
                if C1 >= 12 or C2 >= 12:
                    continue

                if data_p_ratio[C1, C2] == None:
                    continue

                data_label.append(ii)
                data_community.append(vector_similarity_score)
                data_abspecies.append(np.mean([1-data_p_ratio[C1,C2], data_p_ratio[C2,C1]]))
                data_pool_size.append(pool_size)  # Track which pool size this data point is from

        # Process data
        x_raw = 1 - np.array(data_abspecies)

        # Apply arctan normalization to x-axis (species dominance)
        # Convert from proportion (0-1) to arctan normalized form
        # If raw dominance = p, then ratio = p/(1-p), then arctan(ratio)/(π/2)
        ratio = x_raw / (1 - x_raw + 1e-8)
        x = np.arctan(ratio) / (np.pi / 2)

        y = np.array(data_community)
        data_label = np.array(data_label)
        data_pool_size = np.array(data_pool_size)

        # Store original data before duplication
        x_original = x.copy()
        y_original = y.copy()
        pool_size_original = data_pool_size.copy()

        # Duplicate data points
        duplicate = True
        if duplicate:
            x = np.concatenate((x, 1-x))
            y = np.concatenate((y, -y))
            data_label = np.concatenate((data_label, data_label))
            data_pool_size = np.concatenate((data_pool_size, data_pool_size))

        data_by_medium[medium] = {
            'x': x, 'y': y, 'data_label': data_label,
            'x_original': x_original, 'y_original': y_original,
            'pool_size_original': pool_size_original
        }

    # Combine all data for heatmap overlay
    all_x = np.concatenate([data_by_medium['M']['x'], data_by_medium['H']['x']])
    all_y = np.concatenate([data_by_medium['M']['y'], data_by_medium['H']['y']])

    # Add heatmap overlay (without percentage labels)
    section_size_x = 1.0/3 + 1e-8
    section_size_y = (np.pi/2)/3 + 1e-8
    sections_x = np.arange(0, 1.1, section_size_x)
    sections_y = np.arange(-np.pi/4, np.pi/4 + section_size_y, section_size_y)
    count_matrix = np.zeros((len(sections_x) - 1, len(sections_y) - 1))

    # Count points in each section (using combined M+H data)
    for i in range(len(sections_x) - 1):
        for j in range(len(sections_y) - 1):
            x_min, x_max = sections_x[i], sections_x[i + 1]
            y_min, y_max = sections_y[j], sections_y[j + 1]
            count_matrix[i, j] = np.sum((all_x >= x_min) & (all_x < x_max) & (all_y >= y_min) & (all_y < y_max))

    # Create heatmap (no percentage labels)
    plt.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)

    # Define markers for different pool sizes
    markers = ['o', 's', '^']  # circle, square, triangle for pool sizes 6, 12, 24
    pool_size_to_marker = {6: markers[0], 12: markers[1], 24: markers[2]}

    # Plot M and H data with separate colors and regression lines
    for medium in ['M', 'H']:
        x = data_by_medium[medium]['x']
        y = data_by_medium[medium]['y']
        x_original = data_by_medium[medium]['x_original']
        y_original = data_by_medium[medium]['y_original']
        pool_size_original = data_by_medium[medium]['pool_size_original']

        # Choose color
        color = color_M if medium == 'M' else color_H

        # Calculate regression
        if len(x) > 0 and np.std(y) > 1e-10:  # Check if there's variance in y
            slope, intercept = np.polyfit(x, y, 1)
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            if ss_tot > 0:
                r_squared = 1 - (ss_res / ss_tot)
            else:
                r_squared = 0.0
                slope = 0.0
                intercept = np.mean(y) if len(y) > 0 else 0.5
        else:
            # Not enough variance for regression
            slope = 0.0
            intercept = np.mean(y) if len(y) > 0 else 0.5
            r_squared = 0.0

        # Plot duplicated points first (grey, behind) with different markers
        x_duplicated = 1 - x_original
        y_duplicated = -y_original
        for pool_size in [6, 12, 24]:
            mask = pool_size_original == pool_size
            if np.any(mask):
                plt.scatter(x_duplicated[mask], y_duplicated[mask],
                           color='grey', s=4, alpha=0.2, zorder=1,
                           marker=pool_size_to_marker[pool_size])

        # Plot original points on top (colored) with different markers
        for pool_idx, pool_size in enumerate([6, 12, 24]):
            mask = pool_size_original == pool_size
            if np.any(mask):
                label = f'{medium}N Pool {pool_size}' if pool_idx == 0 or medium == 'M' else f'Pool {pool_size}'
                plt.scatter(x_original[mask], y_original[mask],
                           color=color, s=4, alpha=0.5, zorder=2,
                           marker=pool_size_to_marker[pool_size],
                           label=label)

        # Add colored regression line
        plt.plot([0, 1], slope * np.array([0, 1]) + intercept, alpha=0.8, linewidth=1.5, color=color)

        # Add R-squared annotation
        y_offset = 0.55 if medium == 'M' else 0.45
        plt.annotate(f'{medium}N: $R^2$ = {r_squared:.2f}',
                    xy=(0.05, y_offset), xycoords='axes fraction',
                    fontsize=8, color=color)

        # Count aligned points for reporting
        aligned_mask = ((x > 0.5) & (y > 0)) | ((x < 0.5) & (y < 0))
        num_aligned = np.sum(aligned_mask)
        total_points = len(x)
        fraction_aligned = num_aligned / total_points
        print(f'{medium}N (abundant removed): R² = {r_squared:.3f}, slope = {slope:.3f}, aligned = {fraction_aligned:.3f} ({num_aligned}/{total_points})')

    # Set axis properties
    plt.xlim(-0.05, 1.05)
    plt.ylim(-np.pi/4 - 0.05, np.pi/4 + 0.05)
    custom_ticks_x = [0, 1]
    custom_ticks_y = [-np.pi/4, 0, np.pi/4]
    plt.xticks(custom_ticks_x, custom_ticks_x)
    plt.yticks(custom_ticks_y, [r'$-\pi/4$', '0', r'$\pi/4$'])

    # Add legend for pool sizes and media
    plt.legend(loc='upper left', fontsize=5, ncol=2)

    plt.savefig('Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_M_H_Combined_AbundantRemoved.svg', bbox_inches='tight')
    plt.close()

    print(f"Combined M+H plot (abundant species removed) saved!")

def plot_species_vs_dominant_fraction_M_H_combined():
    """Plot correlation with y-axis = relative fraction of dominant species in coalesced community."""
    from matplotlib.colors import Normalize
    from matplotlib.cm import ScalarMappable
    from COLORMAP import get_medium_colors, map_medium_to_index

    # Get colors for M and H
    colors = get_medium_colors()  # [LN, MN, HN] colors
    color_M = colors[1]  # MN color
    color_H = colors[2]  # HN color

    # Load pairwise count data
    Mono_Count_data, Pairwise_Count_data = getPairwiseCountData()

    # Create figure
    f, ax = plt.subplots(1, 1, figsize=(50*mm, 50*mm), facecolor='w', edgecolor='k')

    # Collect data for both M and H media
    data_by_medium = {}
    same_dominant_count = {'M': 0, 'H': 0}
    total_count = {'M': 0, 'H': 0}

    for medium in ['M', 'H']:
        data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium+'N')


        data_label = []
        data_dominant_fraction = []  # y-axis: fraction of dominant species in coalesced community
        data_abspecies = []  # x-axis: pairwise species dominance
        data_pool_size = []  # Track pool size for each data point

        # Loop through all species pool sizes
        for pool_size in [6, 12, 24]:
            type_name = medium + f'N_{pool_size}'
            IDX_list = Syn_Coal_IDX[type_name]
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
            idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])

            # Process each coalescence event for this pool size
            for i in range(len(idx)):
                total_count[medium] += 1

                c_mix = np.array(Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:])
                c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                c_1 = c_1*(c_1>1e-4)
                c_2 = c_2*(c_2>1e-4)

                # Identify most abundant species in each subcommunity
                C1_idx = np.argmax(c_1)  # Most abundant in community 1
                C2_idx = np.argmax(c_2)  # Most abundant in community 2

                # Skip if both subcommunities have the same dominant species
                if C1_idx == C2_idx:
                    same_dominant_count[medium] += 1
                    continue

                # Store original most abundant species for pairwise comparison
                C1 = C1_idx
                C2 = C2_idx

                # Vector similarity approach for classification
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                x_val, y_val = calculate_assymetricity(u, v, k)
                ii = characterize_case(x_val, y_val)

                # FILTER: Only include mixing events (u²+v² > 0.5)
                mixing_strength = u**2 + v**2
                if mixing_strength <= 0.5:
                    continue

                # Calculate relative fraction of the two dominant species in coalesced community
                frac_C1_in_mix = c_mix[C1_idx]
                frac_C2_in_mix = c_mix[C2_idx]

                # Relative fraction: what fraction of the combined dominants does C1 represent?
                # This will be in range [0, 1] where 0.5 means equal, >0.5 means C1 dominates
                total_dominant_fraction = frac_C1_in_mix + frac_C2_in_mix
                if total_dominant_fraction > 0:
                    relative_dominant_fraction = frac_C1_in_mix / total_dominant_fraction
                else:
                    continue

                # Check if both species are within the pairwise data matrix bounds (12x12)
                if C1 >= 12 or C2 >= 12:
                    continue

                if data_p_ratio[C1, C2] == None:
                    continue

                data_label.append(ii)
                data_dominant_fraction.append(relative_dominant_fraction)
                data_abspecies.append(np.mean([1-data_p_ratio[C1,C2], data_p_ratio[C2,C1]]))

        # Process data
        x_raw = 1 - np.array(data_abspecies)

        # Apply arctan normalization to x-axis (species dominance)
        # Convert from proportion (0-1) to arctan normalized form
        # If raw dominance = p, then ratio = p/(1-p), then arctan(ratio)/(π/2)
        ratio = x_raw / (1 - x_raw + 1e-8)
        x = np.arctan(ratio) / (np.pi / 2)

        y = np.array(data_dominant_fraction)
        data_label = np.array(data_label)
        data_pool_size = np.array(data_pool_size)

        # Store original data before duplication
        x_original = x.copy()
        y_original = y.copy()
        pool_size_original = data_pool_size.copy()

        # Duplicate data points
        duplicate = True
        if duplicate:
            x = np.concatenate((x, 1-x))
            y = np.concatenate((y, -y))
            data_label = np.concatenate((data_label, data_label))
            data_pool_size = np.concatenate((data_pool_size, data_pool_size))

        data_by_medium[medium] = {
            'x': x, 'y': y, 'data_label': data_label,
            'x_original': x_original, 'y_original': y_original,
            'pool_size_original': pool_size_original
        }

        # Print same-dominant statistics
        print(f'{medium}N: Same dominant species in both subcommunities: {same_dominant_count[medium]}/{total_count[medium]} ({100*same_dominant_count[medium]/total_count[medium]:.1f}%) - EXCLUDED')

    # Combine all data for heatmap overlay
    all_x = np.concatenate([data_by_medium['M']['x'], data_by_medium['H']['x']])
    all_y = np.concatenate([data_by_medium['M']['y'], data_by_medium['H']['y']])

    # Add heatmap overlay (without percentage labels)
    section_size_x = 1.0/3 + 1e-8
    section_size_y = (np.pi/2)/3 + 1e-8
    sections_x = np.arange(0, 1.1, section_size_x)
    sections_y = np.arange(-np.pi/4, np.pi/4 + section_size_y, section_size_y)
    count_matrix = np.zeros((len(sections_x) - 1, len(sections_y) - 1))

    # Count points in each section (using combined M+H data)
    for i in range(len(sections_x) - 1):
        for j in range(len(sections_y) - 1):
            x_min, x_max = sections_x[i], sections_x[i + 1]
            y_min, y_max = sections_y[j], sections_y[j + 1]
            count_matrix[i, j] = np.sum((all_x >= x_min) & (all_x < x_max) & (all_y >= y_min) & (all_y < y_max))

    # Create heatmap (no percentage labels)
    plt.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)

    # Define markers for different pool sizes
    markers = ['o', 's', '^']  # circle, square, triangle for pool sizes 6, 12, 24
    pool_size_to_marker = {6: markers[0], 12: markers[1], 24: markers[2]}

    # Plot M and H data with separate colors and regression lines
    for medium in ['M', 'H']:
        x = data_by_medium[medium]['x']
        y = data_by_medium[medium]['y']
        x_original = data_by_medium[medium]['x_original']
        y_original = data_by_medium[medium]['y_original']
        pool_size_original = data_by_medium[medium]['pool_size_original']

        # Choose color
        color = color_M if medium == 'M' else color_H

        # Calculate regression
        if len(x) > 0 and np.std(y) > 1e-10:
            slope, intercept = np.polyfit(x, y, 1)
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            if ss_tot > 0:
                r_squared = 1 - (ss_res / ss_tot)
            else:
                r_squared = 0.0
                slope = 0.0
                intercept = np.mean(y) if len(y) > 0 else 0.5
        else:
            slope = 0.0
            intercept = np.mean(y) if len(y) > 0 else 0.5
            r_squared = 0.0

        # Plot duplicated points first (grey, behind) with different markers
        x_duplicated = 1 - x_original
        y_duplicated = -y_original
        for pool_size in [6, 12, 24]:
            mask = pool_size_original == pool_size
            if np.any(mask):
                plt.scatter(x_duplicated[mask], y_duplicated[mask],
                           color='grey', s=4, alpha=0.2, zorder=1,
                           marker=pool_size_to_marker[pool_size])

        # Plot original points on top (colored) with different markers
        for pool_idx, pool_size in enumerate([6, 12, 24]):
            mask = pool_size_original == pool_size
            if np.any(mask):
                label = f'{medium}N Pool {pool_size}' if pool_idx == 0 or medium == 'M' else f'Pool {pool_size}'
                plt.scatter(x_original[mask], y_original[mask],
                           color=color, s=4, alpha=0.5, zorder=2,
                           marker=pool_size_to_marker[pool_size],
                           label=label)

        # Add colored regression line
        plt.plot([0, 1], slope * np.array([0, 1]) + intercept, alpha=0.8, linewidth=1.5, color=color)

        # Add R-squared annotation
        y_offset = 0.55 if medium == 'M' else 0.45
        plt.annotate(f'{medium}N: $R^2$ = {r_squared:.2f}',
                    xy=(0.05, y_offset), xycoords='axes fraction',
                    fontsize=8, color=color)

        # Count aligned points for reporting
        aligned_mask = ((x > 0.5) & (y > 0)) | ((x < 0.5) & (y < 0))
        num_aligned = np.sum(aligned_mask)
        total_points = len(x)
        fraction_aligned = num_aligned / total_points
        print(f'{medium}N (dominant fraction): R² = {r_squared:.3f}, slope = {slope:.3f}, aligned = {fraction_aligned:.3f} ({num_aligned}/{total_points})')

    # Set axis properties
    plt.xlim(-0.05, 1.05)
    plt.ylim(-np.pi/4 - 0.05, np.pi/4 + 0.05)
    custom_ticks_x = [0, 1]
    custom_ticks_y = [-np.pi/4, 0, np.pi/4]
    plt.xticks(custom_ticks_x, custom_ticks_x)
    plt.yticks(custom_ticks_y, [r'$-\pi/4$', '0', r'$\pi/4$'])

    # Add legend for pool sizes and media
    plt.legend(loc='upper left', fontsize=5, ncol=2)

    plt.savefig('Figure/TopDownAnaylsis/Fig_MostAbundant_Correlation_M_H_Combined_DominantFraction.svg', bbox_inches='tight')
    plt.close()

    print(f"Combined M+H plot (dominant fraction y-axis) saved!")

def main():
    """Main function to run all analyses."""
    # Create output directories
    if not os.path.exists('Figure/TopDownAnaylsis'):
        os.makedirs('Figure/TopDownAnaylsis')
    if not os.path.exists('Figure'):
        os.makedirs('Figure')
    
    # Run analyses
    print("Plotting most abundant species fraction...")
    plot_most_abundant_fraction()

    print("Plotting most abundant species fraction (coalesced)...")
    plot_most_abundant_fraction_coalesced()

    print("Plotting most abundant species histograms...")
    plot_most_abundant_histograms()
    
    # Individual pool size plots removed - only using combined plots
    # print("Plotting species vs community dominance for individual pool sizes...")
    # for medium in ['L', 'M', 'H']:
    #     for pool_size in [6, 12, 24]:
    #         plot_species_vs_community_dominance_single_pool(medium, pool_size)

    print("Plotting species vs community dominance for combined pools...")
    for medium in ['L', 'M', 'H']:
        plot_species_vs_community_dominance_combined(medium)

    print("Plotting M+H combined correlation plot...")
    plot_species_vs_community_dominance_M_H_combined()

    print("Plotting M+H combined correlation plot (abundant species removed)...")
    plot_species_vs_community_dominance_M_H_combined_remove_abundant()

    print("Plotting M+H combined with dominant fraction y-axis...")
    plot_species_vs_dominant_fraction_M_H_combined()

    print("Analysis complete!")

if __name__ == "__main__":
    main()