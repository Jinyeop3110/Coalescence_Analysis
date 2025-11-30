#!/usr/bin/env python3
"""
generate_fig4_hierarchy_ph_analysis.py

Purpose: Generate Figure 4 plots including dominance hierarchy matrices and pH vs competitive score analysis
Key features:
- Creates dominance hierarchy matrices for different nutrient conditions
- Calculates competitive scores and hierarchy significance testing
- Plots pH vs competitive score relationships with linear regression
- Generates both regular and competence-ordered heatmaps

This is the Python version of Main_Fig_4/Generate_Fig4_1.ipynb with updated color scheme.

Author: Gore Lab Coalescence Analysis Team  
Date: January 2025
"""

from common_setup import *
from COLORMAP import get_medium_colors, get_medium_color_by_index
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent popups
import warnings
warnings.filterwarnings('ignore')
plt.ioff()  # Turn off interactive mode

# Create output directory
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Hiearchy_pH"
os.makedirs(output_dir, exist_ok=True)

def getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list):
    """Create dominance matrix from coalescence similarity data"""
    N = len(Sub_IDX_list)
    matrix = {Sub_IDX : {} for Sub_IDX in Sub_IDX_list}
    
    for SampleIDX in Coal_IDX_list:
        idx = np.where(Coalescence_data['SampleIDX']==SampleIDX)
        if len(idx[0]) == 0:
            continue
            
        dominance1 = Coalescence_data.iloc[idx][Variable2plot].tolist()[0]
        dominance2 = 1 - dominance1
        subSampleIDX1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()[0]
        subSampleIDX2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()[0]

        if subSampleIDX1 in Sub_IDX_list and subSampleIDX2 in Sub_IDX_list:
            matrix[subSampleIDX1].update({subSampleIDX2: dominance1})
            matrix[subSampleIDX2].update({subSampleIDX1: dominance2})
    
    # Add self-dominance (neutral)
    for SampleIDX in Sub_IDX_list:
        matrix[SampleIDX].update({SampleIDX: 0.5})
    
    return matrix

def calculate_hierarchy_score(matrix):
    """Calculate hierarchy score from dominance matrix"""
    # Get mean of each row and sort indices
    mean_indices = np.argsort(-np.nanmean(matrix, axis=1))
    # Get mean of each column and sort indices  
    col_mean_indices = np.argsort(np.nanmean(matrix, axis=0))
    
    # Create sorted matrix based on sorted row and column indices
    sorted_matrix = matrix[mean_indices][:, col_mean_indices]
    
    # Get lower triangle mask
    mask = np.tril(np.ones_like(sorted_matrix), k=-1).astype(bool)
    non_nan_values = sorted_matrix[mask][~np.isnan(sorted_matrix[mask])]
    
    # Calculate hierarchy score
    if len(non_nan_values) > 0:
        sum_non_nan = np.sum(non_nan_values)
        num_non_nan = len(non_nan_values)
        hierarchy_score = 1 - sum_non_nan / num_non_nan
    else:
        hierarchy_score = 0.5
    
    return hierarchy_score

def generate_random_matrix(matrix):
    """Generate random matrix for null model"""
    random_fractions = np.random.choice(matrix.flatten(), size=matrix.size, replace=True)
    random_matrix = np.zeros(matrix.shape)
    idx = np.tril_indices(matrix.shape[0], k=-1)
    flip_index = 2 * (np.random.rand(len(idx[0])) > 0.5) - 1

    random_matrix[np.tril_indices(matrix.shape[0], k=-1)] = 0.5 + (random_fractions[0:len(idx[0])] - 0.5) * flip_index
    random_matrix[np.triu_indices(matrix.shape[0], k=1)] = 0.5 - (random_fractions[0:len(idx[0])] - 0.5) * flip_index
    np.fill_diagonal(random_matrix, 0.5)
    
    return random_matrix

def calculate_significance(matrix, n_samples=1000):
    """Calculate significance with null model"""
    hierarchy_score = calculate_hierarchy_score(matrix)
    
    # Generate random matrices and calculate hierarchy scores
    random_scores = []
    for i in range(n_samples):
        random_matrix = generate_random_matrix(matrix)
        random_scores.append(calculate_hierarchy_score(random_matrix))
    
    # Calculate p-value
    random_scores = np.array(random_scores)
    p_value = (random_scores >= hierarchy_score).sum() / n_samples
    
    return random_scores, p_value, hierarchy_score

def plot_dominance_matrices(Variable2plot='SimilarityTo1_BC_5', species_num=12, com_type="S"):
    """Plot dominance matrices for all nutrient conditions"""
    
    for medium in ["L", "M", "H"]:
        print(f"\nGenerating dominance matrices for {medium}N...")
        
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(300*mm, 250*mm), dpi=100)

        for rep_idx, rep in enumerate([1, 2]):
            Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", species_num, rep)
            Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, rep)

            matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
            df = pd.DataFrame(matrix)
            df_sorted = df.sort_index(axis=1).sort_index(axis=0)
            
            # Unsorted matrix
            sns.heatmap(df_sorted, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[rep_idx, 0])
            axs[rep_idx, 0].set_title(f"Unsorted, rep {rep}")
            
            # Create competitive scores and sort
            competitive_scores = [np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
            sorted_idx = np.argsort(competitive_scores)[::-1]
            df_sorted = df_sorted.iloc[sorted_idx, sorted_idx]

            # Sorted matrix
            sns.heatmap(df_sorted, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[rep_idx, 1])
            axs[rep_idx, 1].set_title(f"Sorted, rep {rep}")

        plt.tight_layout()
        plt.savefig(f'{output_dir}/Fig_4-1_MatrixPlot_medium_{medium}_S{species_num}.svg', bbox_inches='tight')
        plt.close()

def plot_hierarchy_significance(Variable2plot='SimilarityTo1_BC_5', species_num=12, com_type="S"):
    """Plot hierarchy significance testing for all nutrient conditions"""
    
    # Use COLORMAP colors for nutrient conditions
    colors = get_medium_colors()
    
    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        print(f"Calculating hierarchy significance for {medium}N...")
        
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(60*mm, 60*mm), dpi=100)
        
        # Calculate hierarchy scores for both replicates
        hs_values = []
        p_values = []
        permutated_scores_all = []
        
        for rep in [1, 2]:
            Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", species_num, rep)
            Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, rep)

            matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
            df = pd.DataFrame(matrix)
            
            if not df.empty:
                permutated_scores, p_value, hs = calculate_significance(df.values, 10000)
                hs_values.append(hs)
                p_values.append(p_value)
                permutated_scores_all.extend(permutated_scores)

        if hs_values:
            # Plot histogram of shuffled scores
            plt.hist(permutated_scores_all, bins=50, alpha=0.5, range=(0.5, 0.9), 
                    label='Shuffled', linewidth=0, density=True, color='lightgray')
            
            # Plot actual scores
            for i, hs in enumerate(hs_values):
                line_style = '--' if i == 0 else '-.'
                plt.axvline(x=hs, linestyle=line_style, color=colors[medium_idx], 
                          label=f'Rep {i+1}', linewidth=2)

            combined_p = 1 - (1 - p_values[0]) * (1 - p_values[1]) if len(p_values) > 1 else p_values[0]
            print(f"{medium}N: HS1={hs_values[0]:.3f}, HS2={hs_values[1] if len(hs_values)>1 else 'N/A':.3f}, " +
                  f"p1={p_values[0]:.3f}, p2={p_values[1] if len(p_values)>1 else 'N/A':.3f}, " + 
                  f"combined_p={combined_p:.3f}")

            plt.xlabel('Hierarchy Scores')
            plt.ylabel('Frequency')
            plt.title(f'{medium}N Hierarchy Significance')
            plt.legend()
            plt.savefig(f'{output_dir}/Fig_4-2_HS_medium_{medium}_S{species_num}.svg', bbox_inches='tight')
            plt.close()

def plot_ph_vs_competitive_scores(Variable2plot='SimilarityTo1_BC_3', species_num=12, com_type="S"):
    """Plot pH vs average competitive score relationships"""
    
    # Use COLORMAP colors for nutrient conditions
    colors = get_medium_colors()
    
    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        print(f"Generating pH vs competitive score plot for {medium}N...")
        
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(70*mm, 70*mm), dpi=100)

        Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", species_num, -1)  # All replicates
        Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, -1)

        matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
        df = pd.DataFrame(matrix)
        
        if df.empty:
            print(f"Warning: No data for {medium}N")
            plt.close()
            continue
            
        df_sorted = df.sort_index(axis=1).sort_index(axis=0)
        competitive_scores = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]

        # Sort rows and columns by competitive score
        sorted_idx = np.argsort(competitive_scores)
        df_sorted = df_sorted.iloc[sorted_idx, sorted_idx]

        # Get pH data from metadata
        try:
            communities_data = getCommunities(Communities_data, df_sorted.columns.tolist())
            if 'fieldPH7' in communities_data.columns:
                ph_values = communities_data['fieldPH7'].tolist()
            else:
                print(f"Warning: fieldPH7 not found for {medium}N, using fieldPH1")
                ph_values = communities_data['fieldPH1'].tolist()
                
            competitive_scores_final = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
            
            # Remove NaN values
            valid_pairs = [(cs, ph) for cs, ph in zip(competitive_scores_final, ph_values) 
                          if not (np.isnan(cs) or np.isnan(ph))]
            
            if len(valid_pairs) < 3:
                print(f"Warning: Not enough valid data points for {medium}N")
                plt.close()
                continue
                
            x_values = [pair[0] for pair in valid_pairs]  # competitive scores
            y_values = [pair[1] for pair in valid_pairs]  # pH values
            
            # Linear regression
            model = LinearRegression()
            x_array = np.array(x_values).reshape(-1, 1)
            y_array = np.array(y_values)
            model.fit(x_array, y_array)
            
            slope = model.coef_[0]
            intercept = model.intercept_
            r_squared = r2_score(y_array, model.predict(x_array))

            # Create scatter plot
            plt.scatter(x_values, y_values, color=colors[medium_idx], s=4, alpha=0.7)
            
            # Add regression line
            x_line = np.array([0, 1])
            y_line = slope * x_line + intercept
            plt.plot(x_line, y_line, color=colors[medium_idx], alpha=0.8, linewidth=2)
            
            # Add R-squared annotation
            plt.annotate(f'$R^2$ = {r_squared:.2f}', 
                        xy=(0.65, 0.15), xycoords='axes fraction', 
                        fontsize=12, color=colors[medium_idx])

            plt.xlabel('Average Competitive Score')
            plt.ylabel('Final pH')
            plt.title(f'{medium}N: pH vs Competitive Score')
            plt.xlim(0, 1)
            plt.ylim(3.5, 9.5)
            
            plt.savefig(f'{output_dir}/Fig_4-2_pH_vs_CompetitiveScore_{medium}N_S{species_num}.svg', 
                       bbox_inches='tight')
            plt.close()
            
            print(f"{medium}N: R² = {r_squared:.3f}, slope = {slope:.3f}")
            
        except Exception as e:
            print(f"Error processing pH data for {medium}N: {e}")
            plt.close()
            continue

def plot_competitive_score_vs_ph(Variable2plot='SimilarityTo1_BC_3', species_num=12, com_type="S"):
    """Plot competitive score vs pH (reversed axes)"""
    
    # Use COLORMAP colors for nutrient conditions
    colors = get_medium_colors()
    
    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        print(f"Generating competitive score vs pH plot for {medium}N...")
        
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(70*mm, 70*mm), dpi=100)

        Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", species_num, -1)
        Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, -1)

        matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
        df = pd.DataFrame(matrix)
        
        if df.empty:
            print(f"Warning: No data for {medium}N")
            plt.close()
            continue
            
        df_sorted = df.sort_index(axis=1).sort_index(axis=0)
        competitive_scores = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]

        # Sort by competitive score
        sorted_idx = np.argsort(competitive_scores)
        df_sorted = df_sorted.iloc[sorted_idx, sorted_idx]

        try:
            communities_data = getCommunities(Communities_data, df_sorted.columns.tolist())
            if 'fieldPH7' in communities_data.columns:
                ph_values = communities_data['fieldPH7'].tolist()
            else:
                ph_values = communities_data['fieldPH1'].tolist()
                
            competitive_scores_final = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
            
            # Remove NaN values
            valid_pairs = [(cs, ph) for cs, ph in zip(competitive_scores_final, ph_values) 
                          if not (np.isnan(cs) or np.isnan(ph))]
            
            if len(valid_pairs) < 3:
                print(f"Warning: Not enough valid data points for {medium}N")
                plt.close()
                continue
                
            x_values = [pair[1] for pair in valid_pairs]  # pH values (x-axis)
            y_values = [pair[0] for pair in valid_pairs]  # competitive scores (y-axis)
            
            # Linear regression
            model = LinearRegression()
            x_array = np.array(x_values).reshape(-1, 1)
            y_array = np.array(y_values)
            model.fit(x_array, y_array)
            
            slope = model.coef_[0]
            intercept = model.intercept_
            r_squared = r2_score(y_array, model.predict(x_array))

            # Create scatter plot
            plt.scatter(x_values, y_values, color=colors[medium_idx], s=4, alpha=0.7)
            
            # Add regression line
            x_line = np.array([3.5, 9.5])
            y_line = slope * x_line + intercept
            plt.plot(x_line, y_line, color=colors[medium_idx], alpha=0.8, linewidth=2)
            
            # Add R-squared annotation
            plt.annotate(f'$R^2$ = {r_squared:.2f}', 
                        xy=(0.15, 0.85), xycoords='axes fraction', 
                        fontsize=12, color=colors[medium_idx])

            # Remove title and axis labels
            plt.ylim(0, 1)
            plt.xlim(3.5, 9.5)
            
            plt.savefig(f'{output_dir}/Fig_4-2_CompetitiveScore_vs_pH_{medium}N_S{species_num}_reverted.svg', 
                       bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(f"Error processing reversed pH plot for {medium}N: {e}")
            plt.close()
            continue

def plot_individual_coalescence_ph_difference(Variable2plot='SimilarityTo1_BC_3', species_num=12, com_type="S"):
    """Plot individual coalescence events: pH difference vs community competition (TopDownAnalysis style)"""
    
    # Use COLORMAP colors for nutrient conditions
    colors = get_medium_colors()
    
    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        print(f"Generating individual coalescence pH difference plot for {medium}N...")
        
        # Get coalescence data for specific pool size
        Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, -1)
        
        if len(Coal_IDX_list) == 0:
            print(f"Warning: No coalescence data for {medium}N")
            continue
        
        # Get coalescence event indices
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in Coal_IDX_list])
        if len(idx) == 0:
            print(f"Warning: No matching coalescence events for {medium}N")
            continue
            
        # Get parent community indices
        idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
        idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
        
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in Coal_IDX_list])
        idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
        idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
        
        # Get mixed community indices
        idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in Coal_IDX_list])
        
        data_ph_diff = []  # pH difference (community A - community B)
        data_community_competition = []  # Community competition score
        
        print(f"Processing {len(idx)} coalescence events for {medium}N...")
        
        for i in range(len(idx)):
            try:
                # Get abundance vectors
                c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                
                # Apply threshold filtering
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                # Calculate vector decomposition for community competition
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                
                # Calculate vector similarity-based relative competition score
                # Convert u, v components to a relative dominance measure
                vector_similarity_score = u / (u + v + 1e-8)  # Relative contribution of community 1
                
                # Get pH values for both parent communities
                # Get community IDs from the coalescence data for this specific event  
                coal_event_idx = np.where(Coalescence_data['SampleIDX'] == Coal_IDX_list[i])[0][0]
                community1_id = Coalescence_data.iloc[coal_event_idx]["SampleIDX_Sub1"]
                community2_id = Coalescence_data.iloc[coal_event_idx]["SampleIDX_Sub2"]
                
                # Find pH data for these communities in Communities_data
                comm1_idx = np.where(Communities_data['SampleIDX'] == community1_id)[0]
                comm2_idx = np.where(Communities_data['SampleIDX'] == community2_id)[0]
                
                if len(comm1_idx) == 0 or len(comm2_idx) == 0:
                    continue
                
                comm1_data = Communities_data.iloc[comm1_idx[0]]
                comm2_data = Communities_data.iloc[comm2_idx[0]]
                
                # Try fieldPH7 first, then fieldPH1
                ph_column = 'fieldPH7' if 'fieldPH7' in Communities_data.columns else 'fieldPH1'
                
                if ph_column not in Communities_data.columns:
                    continue
                
                ph1 = comm1_data[ph_column]
                ph2 = comm2_data[ph_column]
                
                if np.isnan(ph1) or np.isnan(ph2):
                    continue
                
                # Calculate pH difference (community A - community B)
                ph_difference = ph1 - ph2
                
                data_ph_diff.append(ph_difference)
                data_community_competition.append(vector_similarity_score)
                
            except Exception as e:
                print(f"Error processing event {i} for {medium}N: {e}")
                continue
        
        if len(data_ph_diff) < 3:
            print(f"Warning: Not enough valid data points for {medium}N ({len(data_ph_diff)} points)")
            continue
            
        # Convert to numpy arrays
        x = np.array(data_ph_diff)
        y = np.array(data_community_competition)
        
        # Duplicate data points (as in the reference TopDownAnalysis style)
        duplicate = True
        if duplicate:
            x = np.concatenate((x, -x))  # Flip pH difference
            y = np.concatenate((y, 1-y))  # Flip community competition
        
        # Calculate linear regression
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Create figure with 2.3x2.2 inch size
        f, ax = plt.subplots(1, 1, figsize=(2.3, 2.2), facecolor='w', edgecolor='k')
        
        # Create scatter plot with color
        plt.scatter(x, y, color=colors[medium_idx], s=4, alpha=0.5)
        
        # Add linear regression line
        x_line = np.array([np.min(x), np.max(x)])
        y_line = slope * x_line + intercept
        plt.plot(x_line, y_line, alpha=0.8, linewidth=0.5, color='black')
        
        # Add R-squared annotation (positioned like in reference)
        plt.annotate('R² = {:.2f}'.format(r_squared), xy=(0.05+0.7, 0.55), 
                    xycoords='axes fraction', fontsize=8, color='black')
        
        # Add heatmap overlay (3x3 grid)
        x_min, x_max = np.min(x), np.max(x)
        y_min, y_max = np.min(y), np.max(y)
        
        # Extend ranges slightly to ensure all points are captured
        x_range = x_max - x_min
        y_range = y_max - y_min
        x_min -= 0.05 * x_range
        x_max += 0.05 * x_range
        y_min -= 0.05 * y_range
        y_max += 0.05 * y_range
        
        section_size_x = (x_max - x_min) / 3
        section_size_y = (y_max - y_min) / 3
        sections_x = np.linspace(x_min, x_max, 4)
        sections_y = np.linspace(y_min, y_max, 4)
        count_matrix = np.zeros((3, 3))
        
        # Count points in each section
        for i in range(3):
            for j in range(3):
                x_section_min, x_section_max = sections_x[i], sections_x[i + 1]
                y_section_min, y_section_max = sections_y[j], sections_y[j + 1]
                count_matrix[i, j] = np.sum((x >= x_section_min) & (x < x_section_max) & 
                                           (y >= y_section_min) & (y < y_section_max))
        
        total_points = np.sum(count_matrix)
        percentage_matrix = (count_matrix / total_points) * 100
        
        # Create heatmap overlay
        plt.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)
        
        # Add percentage annotations for sections with >10% of points
        for i in range(3):
            for j in range(3):
                if percentage_matrix[i, j] > 10:
                    x_center = sections_x[i] + section_size_x/2
                    y_center = sections_y[j] + section_size_y/2
                    plt.text(x_center, y_center, f'{percentage_matrix[i, j]:.1f}%', 
                            color='black', size=8, alpha=0.7, ha='center', va='center')
        
        # Set axis properties
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        
        # Set up custom ticks (similar to reference style)
        custom_ticks = [x_min, x_max]
        plt.xticks(custom_ticks, [f'{x_min:.1f}', f'{x_max:.1f}'])
        plt.yticks([0, 1], ['0', '1'])
        
        # Remove axis labels
        
        plt.savefig(f'{output_dir}/Fig_4-4_pHDiff_vs_CommunityCompetition_{medium}N_S{species_num}.svg', 
                   bbox_inches='tight')
        plt.close()
        
        print(f"{medium}N individual coalescence: R² = {r_squared:.3f}, slope = {slope:.3f}, n_points = {len(data_ph_diff)}")

def plot_individual_coalescence_ph_difference_combined(Variable2plot='SimilarityTo1_BC_3', com_type="S", exclude_mixtures=False):
    """Plot individual coalescence events combining all species pool sizes (6, 12, 24)

    Parameters:
    -----------
    exclude_mixtures : bool
        If True, exclude coalescence events where either parent community was itself a mixture
    """

    # Use COLORMAP colors for nutrient conditions
    colors = get_medium_colors()

    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        suffix = "_NoMixtures" if exclude_mixtures else "_Combined"
        print(f"Generating combined pH difference plot for {medium}N (combining S6, S12, S24){' [excluding mixtures]' if exclude_mixtures else ''}...")

        data_ph_diff = []  # pH difference (community A - community B)
        data_community_competition = []  # Community competition score

        # Loop through all species pool sizes (6, 12, 24)
        for species_num in [6, 12, 24]:
            print(f"  Processing {medium}N S{species_num}...")

            # Get coalescence data for specific pool size
            Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, -1)

            if len(Coal_IDX_list) == 0:
                print(f"    Warning: No coalescence data for {medium}N S{species_num}")
                continue

            # Get coalescence event indices
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in Coal_IDX_list])
            if len(idx) == 0:
                print(f"    Warning: No matching coalescence events for {medium}N S{species_num}")
                continue

            # Get parent community indices
            idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])

            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in Coal_IDX_list])
            idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])

            # Get mixed community indices
            idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in Coal_IDX_list])

            # Get parent community IDs for filtering
            parent_community_ids = []
            for i in range(len(idx)):
                coal_event_idx = np.where(Coalescence_data['SampleIDX'] == Coal_IDX_list[i])[0][0]
                community1_id = Coalescence_data.iloc[coal_event_idx]["SampleIDX_Sub1"]
                community2_id = Coalescence_data.iloc[coal_event_idx]["SampleIDX_Sub2"]
                parent_community_ids.append((community1_id, community2_id))

            print(f"    Processing {len(idx)} coalescence events for {medium}N S{species_num}...")

            for i in range(len(idx)):
                try:
                    # If exclude_mixtures is True, check if parent communities are single communities
                    if exclude_mixtures:
                        community1_id, community2_id = parent_community_ids[i]

                        # Check if parent communities are single communities (CoalescenceType == 'S')
                        comm1_meta = Metadata[Metadata['SampleIDX'] == community1_id]
                        comm2_meta = Metadata[Metadata['SampleIDX'] == community2_id]

                        if len(comm1_meta) == 0 or len(comm2_meta) == 0:
                            continue

                        # Skip if either parent is a mixture (CoalescenceType == 'C')
                        if comm1_meta.iloc[0]['CoalescenceType'] == 'C' or comm2_meta.iloc[0]['CoalescenceType'] == 'C':
                            continue

                    # Get abundance vectors
                    c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                    c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                    c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])

                    # Apply threshold filtering
                    c_1 = c_1 * (c_1 > 1e-4)
                    c_2 = c_2 * (c_2 > 1e-4)

                    # Calculate vector decomposition for community competition
                    u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)

                    # Calculate vector similarity-based relative competition score
                    # Convert u, v components to a relative dominance measure
                    vector_similarity_score = u / (u + v + 1e-8)  # Relative contribution of community 1

                    # Get pH values for both parent communities
                    # Get community IDs from the coalescence data for this specific event
                    coal_event_idx = np.where(Coalescence_data['SampleIDX'] == Coal_IDX_list[i])[0][0]
                    community1_id = Coalescence_data.iloc[coal_event_idx]["SampleIDX_Sub1"]
                    community2_id = Coalescence_data.iloc[coal_event_idx]["SampleIDX_Sub2"]

                    # Find pH data for these communities in Communities_data
                    comm1_idx = np.where(Communities_data['SampleIDX'] == community1_id)[0]
                    comm2_idx = np.where(Communities_data['SampleIDX'] == community2_id)[0]

                    if len(comm1_idx) == 0 or len(comm2_idx) == 0:
                        continue

                    comm1_data = Communities_data.iloc[comm1_idx[0]]
                    comm2_data = Communities_data.iloc[comm2_idx[0]]

                    # Try fieldPH7 first, then fieldPH1
                    ph_column = 'fieldPH7' if 'fieldPH7' in Communities_data.columns else 'fieldPH1'

                    if ph_column not in Communities_data.columns:
                        continue

                    ph1 = comm1_data[ph_column]
                    ph2 = comm2_data[ph_column]

                    if np.isnan(ph1) or np.isnan(ph2):
                        continue

                    # Calculate pH difference (community A - community B)
                    ph_difference = ph1 - ph2

                    data_ph_diff.append(ph_difference)
                    data_community_competition.append(vector_similarity_score)

                except Exception as e:
                    print(f"    Error processing event {i} for {medium}N S{species_num}: {e}")
                    continue
        
        if len(data_ph_diff) < 3:
            print(f"Warning: Not enough valid data points for {medium}N combined ({len(data_ph_diff)} points)")
            continue
            
        # Convert to numpy arrays
        x = np.array(data_ph_diff)
        y = np.array(data_community_competition)
        
        # Duplicate data points (as in the reference TopDownAnalysis style)
        duplicate = True
        if duplicate:
            x = np.concatenate((x, -x))  # Flip pH difference
            y = np.concatenate((y, 1-y))  # Flip community competition
        
        # Calculate linear regression
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Create figure with 2.3x2.2 inch size
        f, ax = plt.subplots(1, 1, figsize=(2.3, 2.2), facecolor='w', edgecolor='k')
        
        # Create scatter plot with color
        plt.scatter(x, y, color=colors[medium_idx], s=4, alpha=0.5)
        
        # Add linear regression line
        x_line = np.array([np.min(x), np.max(x)])
        y_line = slope * x_line + intercept
        plt.plot(x_line, y_line, alpha=0.8, linewidth=0.5, color='black')
        
        # Add R-squared annotation (positioned like in reference)
        plt.annotate('R² = {:.2f}'.format(r_squared), xy=(0.05+0.7, 0.55), 
                    xycoords='axes fraction', fontsize=8, color='black')
        
        # Add heatmap overlay (3x3 grid)
        x_min, x_max = np.min(x), np.max(x)
        y_min, y_max = np.min(y), np.max(y)
        
        # Extend ranges slightly to ensure all points are captured
        x_range = x_max - x_min
        y_range = y_max - y_min
        x_min -= 0.05 * x_range
        x_max += 0.05 * x_range
        y_min -= 0.05 * y_range
        y_max += 0.05 * y_range
        
        section_size_x = (x_max - x_min) / 3
        section_size_y = (y_max - y_min) / 3
        sections_x = np.linspace(x_min, x_max, 4)
        sections_y = np.linspace(y_min, y_max, 4)
        count_matrix = np.zeros((3, 3))
        
        # Count points in each section
        for i in range(3):
            for j in range(3):
                x_section_min, x_section_max = sections_x[i], sections_x[i + 1]
                y_section_min, y_section_max = sections_y[j], sections_y[j + 1]
                count_matrix[i, j] = np.sum((x >= x_section_min) & (x < x_section_max) & 
                                           (y >= y_section_min) & (y < y_section_max))
        
        total_points = np.sum(count_matrix)
        percentage_matrix = (count_matrix / total_points) * 100
        
        # Create heatmap overlay
        plt.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)
        
        # Add percentage annotations for sections with >10% of points
        for i in range(3):
            for j in range(3):
                if percentage_matrix[i, j] > 10:
                    x_center = sections_x[i] + section_size_x/2
                    y_center = sections_y[j] + section_size_y/2
                    plt.text(x_center, y_center, f'{percentage_matrix[i, j]:.1f}%', 
                            color='black', size=8, alpha=0.7, ha='center', va='center')
        
        # Set axis properties
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        
        # Set up custom ticks (similar to reference style)
        custom_ticks = [x_min, x_max]
        plt.xticks(custom_ticks, [f'{x_min:.1f}', f'{x_max:.1f}'])
        plt.yticks([0, 1], ['0', '1'])
        
        # Remove axis labels

        plt.savefig(f'{output_dir}/Fig_4-5_pHDiff_vs_CommunityCompetition_{medium}N{suffix}.svg',
                   bbox_inches='tight')
        plt.close()

        mixture_status = " (no mixtures)" if exclude_mixtures else ""
        print(f"{medium}N combined (S6+S12+S24){mixture_status}: R² = {r_squared:.3f}, slope = {slope:.3f}, n_points = {len(data_ph_diff)}")

def plot_ph_vs_competitive_scores_heatmap_style(Variable2plot='SimilarityTo1_BC_3', species_num=12, com_type="S"):
    """Plot pH vs average competitive score with TopDownAnalysis heatmap style"""
    
    # Use COLORMAP colors for nutrient conditions
    colors = get_medium_colors()
    
    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        print(f"Generating heatmap-style pH vs competitive score plot for {medium}N...")
        
        Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", species_num, -1)
        Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, -1)

        matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
        df = pd.DataFrame(matrix)
        
        if df.empty:
            print(f"Warning: No data for {medium}N")
            continue
            
        df_sorted = df.sort_index(axis=1).sort_index(axis=0)
        competitive_scores = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]

        # Sort by competitive score
        sorted_idx = np.argsort(competitive_scores)
        df_sorted = df_sorted.iloc[sorted_idx, sorted_idx]

        try:
            communities_data = getCommunities(Communities_data, df_sorted.columns.tolist())
            if 'fieldPH7' in communities_data.columns:
                ph_values = communities_data['fieldPH7'].tolist()
            else:
                ph_values = communities_data['fieldPH1'].tolist()
                
            competitive_scores_final = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
            
            # Remove NaN values
            valid_pairs = [(ph, cs) for cs, ph in zip(competitive_scores_final, ph_values) 
                          if not (np.isnan(cs) or np.isnan(ph))]
            
            if len(valid_pairs) < 3:
                print(f"Warning: Not enough valid data points for {medium}N")
                continue
                
            x_values = [pair[0] for pair in valid_pairs]  # pH values (x-axis)
            y_values = [pair[1] for pair in valid_pairs]  # competitive scores (y-axis)
            
            # Convert to numpy arrays
            x = np.array(x_values)
            y = np.array(y_values)
            
            # Linear regression
            slope, intercept = np.polyfit(x, y, 1)
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            # Create figure with TopDownAnalysis style (70mm x 70mm)
            mm = 0.1/2.54  # mm to inches conversion
            f, ax = plt.subplots(1, 1, figsize=(70*mm, 70*mm), facecolor='w', edgecolor='k')
            
            # Create scatter plot with color
            plt.scatter(x, y, color=colors[medium_idx], s=4, alpha=0.5)
            
            # Add linear regression line
            x_line = np.array([np.min(x), np.max(x)])
            y_line = slope * x_line + intercept
            plt.plot(x_line, y_line, alpha=0.8, linewidth=0.5, color='black')
            
            # Add R-squared annotation (positioned like in reference)
            plt.annotate('$R^2$ = {:.2f}'.format(r_squared), xy=(0.05+0.7, 0.55), 
                        xycoords='axes fraction', fontsize=8, color='black')
            
            # Add heatmap overlay (3x3 grid)
            x_min, x_max = np.min(x), np.max(x)
            y_min, y_max = np.min(y), np.max(y)
            
            # Extend ranges slightly to ensure all points are captured
            x_range = x_max - x_min
            y_range = y_max - y_min
            x_min -= 0.05 * x_range
            x_max += 0.05 * x_range
            y_min -= 0.05 * y_range
            y_max += 0.05 * y_range
            
            section_size_x = (x_max - x_min) / 3
            section_size_y = (y_max - y_min) / 3
            sections_x = np.linspace(x_min, x_max, 4)
            sections_y = np.linspace(y_min, y_max, 4)
            count_matrix = np.zeros((3, 3))
            
            # Count points in each section
            for i in range(3):
                for j in range(3):
                    x_section_min, x_section_max = sections_x[i], sections_x[i + 1]
                    y_section_min, y_section_max = sections_y[j], sections_y[j + 1]
                    count_matrix[i, j] = np.sum((x >= x_section_min) & (x < x_section_max) & 
                                               (y >= y_section_min) & (y < y_section_max))
            
            total_points = np.sum(count_matrix)
            percentage_matrix = (count_matrix / total_points) * 100
            
            # Create heatmap overlay
            plt.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)
            
            # Add percentage annotations for sections with >10% of points
            for i in range(3):
                for j in range(3):
                    if percentage_matrix[i, j] > 10:
                        x_center = sections_x[i] + section_size_x/2
                        y_center = sections_y[j] + section_size_y/2
                        plt.text(x_center, y_center, f'{percentage_matrix[i, j]:.1f}%', 
                                color='black', size=8, alpha=0.7, ha='center', va='center')
            
            # Set axis properties
            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)
            
            # Set up custom ticks (similar to reference style)
            x_ticks = [x_min, x_max]
            y_ticks = [y_min, y_max]
            plt.xticks([round(x_min, 1), round(x_max, 1)], [round(x_min, 1), round(x_max, 1)])
            plt.yticks([round(y_min, 2), round(y_max, 2)], [round(y_min, 2), round(y_max, 2)])
            
            plt.xlabel('Final pH')
            plt.ylabel('Average Competitive Score')
            
            plt.savefig(f'{output_dir}/Fig_4-3_pH_vs_CompetitiveScore_Heatmap_{medium}N_S{species_num}.svg', 
                       bbox_inches='tight')
            plt.close()
            
            print(f"{medium}N heatmap style: R² = {r_squared:.3f}, slope = {slope:.3f}")
            
        except Exception as e:
            print(f"Error processing heatmap style pH plot for {medium}N: {e}")
            continue

def plot_ph_vs_competitive_scores_combined(Variable2plot='SimilarityTo1_BC_3', com_type="S"):
    """Plot pH vs competitive scores combining all species pool sizes (6, 12, 24)"""
    
    # Use COLORMAP colors for nutrient conditions
    colors = get_medium_colors()
    
    for medium_idx, medium in enumerate(['L', 'M', 'H']):
        print(f"Generating combined pH vs competitive score plot for {medium}N (combining S6, S12, S24)...")
        
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(70*mm, 70*mm), dpi=100)

        all_ph_values = []
        all_competitive_scores = []
        
        # Loop through all species pool sizes (6, 12, 24)
        for species_num in [6, 12, 24]:
            print(f"  Processing {medium}N S{species_num}...")
            
            Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", species_num, -1)
            Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, -1)

            matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
            df = pd.DataFrame(matrix)
            
            if df.empty:
                print(f"    Warning: No data for {medium}N S{species_num}")
                continue
                
            df_sorted = df.sort_index(axis=1).sort_index(axis=0)
            competitive_scores = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]

            # Sort by competitive score
            sorted_idx = np.argsort(competitive_scores)
            df_sorted = df_sorted.iloc[sorted_idx, sorted_idx]

            try:
                communities_data = getCommunities(Communities_data, df_sorted.columns.tolist())
                if 'fieldPH7' in communities_data.columns:
                    ph_values = communities_data['fieldPH7'].tolist()
                else:
                    print(f"    Warning: fieldPH7 not found for {medium}N S{species_num}, using fieldPH1")
                    ph_values = communities_data['fieldPH1'].tolist()
                    
                competitive_scores_final = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
                
                # Remove NaN values and collect valid data
                valid_pairs = [(ph, cs) for cs, ph in zip(competitive_scores_final, ph_values) 
                              if not (np.isnan(cs) or np.isnan(ph))]
                
                if len(valid_pairs) >= 3:
                    ph_vals = [pair[0] for pair in valid_pairs]
                    cs_vals = [pair[1] for pair in valid_pairs]
                    all_ph_values.extend(ph_vals)
                    all_competitive_scores.extend(cs_vals)
                    print(f"    Added {len(valid_pairs)} data points from S{species_num}")
                else:
                    print(f"    Warning: Not enough valid data points for {medium}N S{species_num}")
                    
            except Exception as e:
                print(f"    Error processing pH data for {medium}N S{species_num}: {e}")
                continue
        
        if len(all_ph_values) < 3:
            print(f"Warning: Not enough combined valid data points for {medium}N ({len(all_ph_values)} points)")
            plt.close()
            continue
            
        # Convert to numpy arrays
        x_values = np.array(all_ph_values)  # pH values
        y_values = np.array(all_competitive_scores)  # competitive scores
        
        # Normalize competitive scores to 0-1 range within this medium
        y_min, y_max = np.min(y_values), np.max(y_values)
        if y_max > y_min:
            y_values = (y_values - y_min) / (y_max - y_min)
        
        # Linear regression
        model = LinearRegression()
        x_array = x_values.reshape(-1, 1)
        model.fit(x_array, y_values)
        
        slope = model.coef_[0]
        intercept = model.intercept_
        r_squared = r2_score(y_values, model.predict(x_array))

        # Create scatter plot
        plt.scatter(x_values, y_values, color=colors[medium_idx], s=4, alpha=0.7)
        
        # Add regression line
        x_line = np.array([3.5, 9.5])
        y_line = slope * x_line + intercept
        plt.plot(x_line, y_line, color=colors[medium_idx], alpha=0.8, linewidth=2)
        
        # Add R-squared annotation
        plt.annotate(f'$R^2$ = {r_squared:.2f}', 
                    xy=(0.65, 0.15), xycoords='axes fraction', 
                    fontsize=12, color=colors[medium_idx])

        plt.xlabel('Final pH')
        plt.ylabel('Average Competitive Score (Normalized)')
        plt.title(f'{medium}N: pH vs Competitive Score (Combined)')
        plt.xlim(3.5, 9.5)
        plt.ylim(0, 1)
        
        plt.savefig(f'{output_dir}/Fig_4-2_pH_vs_CompetitiveScore_{medium}N_Combined.svg', 
                   bbox_inches='tight')
        plt.close()
        
        print(f"{medium}N combined (S6+S12+S24): R² = {r_squared:.3f}, slope = {slope:.3f}, n_points = {len(all_ph_values)}")

def main():
    """Main function to generate all Figure 4 plots"""
    print("Starting Figure 4 Hierarchy and pH Analysis...")
    print("=" * 50)
    
    print(f"Data loaded from common_setup.py:")
    print(f"  Coalescence events: {len(Coalescence_data)}")
    print(f"  Community measurements: {len(Communities_data)}")
    print(f"  Metadata entries: {len(Metadata)}")
    
    # Set analysis parameters
    Variable2plot = 'SimilarityTo1_BC_5'  # For hierarchy analysis
    Variable2plot_pH = 'SimilarityTo1_BC_3'  # For pH analysis (as in original notebook)
    species_num = 12
    com_type = "S"
    
    print(f"\nUsing colors from COLORMAP:")
    colors = get_medium_colors()
    for i, medium in enumerate(['LN', 'MN', 'HN']):
        print(f"  {medium}: {colors[i]}")
    
    # Generate dominance matrix plots
    print(f"\n{'='*50}")
    print("1. Generating dominance hierarchy matrices...")
    plot_dominance_matrices(Variable2plot, species_num, com_type)
    
    # Generate hierarchy significance plots  
    print(f"\n{'='*50}")
    print("2. Calculating hierarchy significance...")
    plot_hierarchy_significance(Variable2plot, species_num, com_type)
    
    # Generate pH vs competitive score plots
    print(f"\n{'='*50}")
    print("3. Generating pH vs competitive score plots...")
    plot_ph_vs_competitive_scores(Variable2plot_pH, species_num, com_type)
    
    # Generate combined pH vs competitive score plots (S6 + S12 + S24)
    print(f"\n{'='*50}")
    print("4. Generating combined pH vs competitive score plots (S6+S12+S24)...")
    plot_ph_vs_competitive_scores_combined(Variable2plot_pH, com_type)
    
    # Generate competitive score vs pH plots (reversed axes)
    print(f"\n{'='*50}")  
    print("5. Generating competitive score vs pH plots...")
    plot_competitive_score_vs_ph(Variable2plot_pH, species_num, com_type)
    
    # Generate pH vs competitive score plots with heatmap style
    print(f"\n{'='*50}")
    print("6. Generating pH vs competitive score plots with heatmap overlay...")
    plot_ph_vs_competitive_scores_heatmap_style(Variable2plot_pH, species_num, com_type)
    
    # Generate individual coalescence pH difference plots
    print(f"\n{'='*50}")
    print("7. Generating individual coalescence pH difference vs community competition plots...")
    plot_individual_coalescence_ph_difference(Variable2plot_pH, species_num, com_type)
    
    # Generate combined coalescence pH difference plots (S6 + S12 + S24)
    print(f"\n{'='*50}")
    print("8. Generating combined pH difference vs community competition plots (S6+S12+S24)...")
    plot_individual_coalescence_ph_difference_combined(Variable2plot_pH, com_type, exclude_mixtures=False)

    # Generate combined coalescence pH difference plots WITHOUT mixtures (S6 + S12 + S24)
    print(f"\n{'='*50}")
    print("9. Generating combined pH difference plots WITHOUT mixtures (S6+S12+S24)...")
    plot_individual_coalescence_ph_difference_combined(Variable2plot_pH, com_type, exclude_mixtures=True)

    print(f"\n{'='*50}")
    print(f"Figure 4 analysis complete! All plots saved to:")
    print(f"  {output_dir}")
    print("Generated files:")
    print("  - Fig_4-1_MatrixPlot_medium_[L/M/H]_S12.svg")
    print("  - Fig_4-2_HS_medium_[L/M/H]_S12.svg")
    print("  - Fig_4-2_pH_vs_CompetitiveScore_[L/M/H]N_S12.svg")
    print("  - Fig_4-2_pH_vs_CompetitiveScore_[L/M/H]N_Combined.svg")
    print("  - Fig_4-2_CompetitiveScore_vs_pH_[L/M/H]N_S12_reverted.svg")
    print("  - Fig_4-3_pH_vs_CompetitiveScore_Heatmap_[L/M/H]N_S12.svg")
    print("  - Fig_4-4_pHDiff_vs_CommunityCompetition_[L/M/H]N_S12.svg")
    print("  - Fig_4-5_pHDiff_vs_CommunityCompetition_[L/M/H]N_Combined.svg")
    print("  - Fig_4-5_pHDiff_vs_CommunityCompetition_[L/M/H]N_NoMixtures.svg")

if __name__ == "__main__":
    main()