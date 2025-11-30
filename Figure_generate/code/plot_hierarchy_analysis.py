#!/usr/bin/env python3
"""
plot_hierarchy_analysis.py

Purpose: Calculates and plots hierarchy scores for coalescence experiments
Key features:
- Calculates hierarchy scores from dominance matrices
- Generates heatmaps of competitive relationships
- Performs statistical significance testing with null models
- Saves plots to Figure/Hiearchy directory

Converted from Figure_generation_Hiearchy.ipynb
Author: Gore Lab Coalescence Analysis Team
Date: January 2025
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent popups
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from collections import defaultdict
import os
import warnings
warnings.filterwarnings('ignore')
plt.ioff()  # Turn off interactive mode

# Set up plotting style
sns.set_style("ticks")
plt.rcParams.update({
    'legend.fontsize': 'x-large',
    'figure.figsize': (15, 5),
    'axes.labelsize': 'x-large',
    'axes.titlesize': 'x-large',
    'xtick.labelsize': 'x-large',
    'ytick.labelsize': 'x-large'
})

# Create output directory
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Hiearchy"
os.makedirs(output_dir, exist_ok=True)

def load_data():
    """Load all required datasets"""
    print("Loading coalescence and community data...")
    
    # Define file paths
    base_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404"
    
    Coalescence_data_synthetic_path = f"{base_path}/Analyzed/processed_CoalescenceEvent_synthetic.xlsx"
    Communities_data_synthetic_path = f"{base_path}/Analyzed/processed_Communities_synthetic.xlsx"
    Coalescence_data_natural_path = f"{base_path}/Analyzed/processed_CoalescenceEvent_natural.xlsx"
    Communities_data_natural_path = f"{base_path}/Analyzed/processed_Communities_natural.xlsx"
    Meta_data_path = f"{base_path}/Postprocessed/Metadata.xlsx"
    
    # Load and combine data
    Coalescence_data = pd.concat([
        pd.read_excel(Coalescence_data_synthetic_path),
        pd.read_excel(Coalescence_data_natural_path)
    ])
    
    Communities_data = pd.concat([
        pd.read_excel(Communities_data_synthetic_path),
        pd.read_excel(Communities_data_natural_path)
    ])
    
    Metadata = pd.read_excel(Meta_data_path)
    
    # Exception list for problematic samples
    exception_list = ['P4-02','P4-03','P4-23','P4-24','P7-97', 'P8-12'] + ['P8-91'] + \
                    ['P5-73', 'P5-69','P5-64','P5-61','P5-59', 'P5-56'] + ['P6-67']
    
    print(f"Loaded {len(Coalescence_data)} coalescence events")
    print(f"Loaded {len(Communities_data)} community samples")
    print(f"Loaded {len(Metadata)} metadata entries")
    
    return Coalescence_data, Communities_data, Metadata, exception_list

def Community_PermutateList(Timepoint, CommunityOrigin, Medium, CoalescenceType, 
                           Metadata, species_pool_num=0, Replicate=-1, exception_list=None):
    """Get list of sample IDs based on experimental conditions"""
    if exception_list is None:
        exception_list = []
    
    if Replicate == -1:
        idx = (Metadata['Timepoint'] == Timepoint) & \
              (Metadata['CommunityOrigin'] == CommunityOrigin) & \
              (Metadata['Medium'] == Medium) & \
              (Metadata['CoalescenceType'] == CoalescenceType)
    elif Replicate in [1, 2]:
        idx = (Metadata['Timepoint'] == Timepoint) & \
              (Metadata['CommunityOrigin'] == CommunityOrigin) & \
              (Metadata['Medium'] == Medium) & \
              (Metadata['CoalescenceType'] == CoalescenceType) & \
              (Metadata['Replicate'] == Replicate)
    else:
        raise ValueError("Invalid replicate input")

    if CommunityOrigin == 'S':
        communityIDX = np.array([int(x) for x in Metadata['CommunityIDX']])
        if CoalescenceType == 'S':
            if species_pool_num == 6:
                idx = idx & (communityIDX <= 9)
            elif species_pool_num == 12:
                idx = idx & ((communityIDX > 9) & (communityIDX <= 18))
            elif species_pool_num == 24:
                idx = idx & ((communityIDX > 18) & (communityIDX <= 30))
        elif CoalescenceType == 'C':
            if species_pool_num == 6:
                idx = idx & (communityIDX <= 14)
            elif species_pool_num == 12:
                idx = idx & ((communityIDX > 14) & (communityIDX <= 41))
            elif species_pool_num == 24:
                idx = idx & ((communityIDX > 41) & (communityIDX <= 47))

    O = Metadata['SampleIDX'][idx].tolist()
    O = list(set(O) - set(exception_list))
    return O

def getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list):
    """Create dominance matrix from coalescence data"""
    matrix = {Sub_IDX: {} for Sub_IDX in Sub_IDX_list}
    
    for SampleIDX in Coal_IDX_list:
        idx = np.where(Coalescence_data['SampleIDX'] == SampleIDX)[0]
        if len(idx) == 0:
            continue
            
        dominance1 = Coalescence_data.iloc[idx[0]][Variable2plot]
        dominance2 = 1 - dominance1
        subSampleIDX1 = Coalescence_data.iloc[idx[0]]["SampleIDX_Sub1"]
        subSampleIDX2 = Coalescence_data.iloc[idx[0]]["SampleIDX_Sub2"]
        
        matrix[subSampleIDX1].update({subSampleIDX2: dominance1})
        matrix[subSampleIDX2].update({subSampleIDX1: dominance2})
    
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
    
    random_matrix[idx] = random_fractions[0:len(idx[0])]
    random_matrix[np.triu_indices(matrix.shape[0], k=1)] = 1 - random_fractions[0:len(idx[0])]
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

def plot_hierarchy_heatmaps(Coalescence_data, Communities_data, Metadata, exception_list,
                           com_type='S', Variable2plot='SimilarityTo1_BC_3', medium='M', species_num=12):
    """Plot hierarchy heatmaps for different replicates"""
    
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(30, 16), dpi=100)
    
    # Replicate 1
    rep = 1
    Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
    Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
    
    matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
    df = pd.DataFrame(matrix)
    df_sorted = df.sort_index(axis=1).sort_index(axis=0)
    
    # Create competitive scores and sort
    competitive_scores = [np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
    sorted_idx = np.argsort(competitive_scores)[::-1]
    df_sorted = df_sorted.iloc[sorted_idx, sorted_idx]
    df1 = df_sorted
    
    # Plot replicate 1
    sns.heatmap(df1, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[0, 0])
    axs[0, 0].set_title("rep 1")
    
    # Replicate 2
    rep = 2
    Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
    Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
    
    matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
    df = pd.DataFrame(matrix)
    df_sorted = df.sort_index(axis=1).sort_index(axis=0)
    
    # Calculate competitive scores for rep 2
    competitive_scores2 = [np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
    sorted_idx2 = np.argsort(competitive_scores2)[::-1]
    df_sorted = df_sorted.iloc[sorted_idx2, sorted_idx2]
    df2 = df_sorted
    
    # Plot replicate 2
    sns.heatmap(df2, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[0, 1])
    axs[0, 1].set_title("rep 2")
    
    # Combined data - only if both dataframes have same shape
    if df1.shape == df2.shape and all(df1.index == df2.index) and all(df1.columns == df2.columns):
        mat = np.nanmean(np.array([df1.to_numpy(), df2.to_numpy()]), axis=0)
        df_mean = pd.DataFrame(mat, index=df1.index, columns=df1.columns)
        has_combined = True
    else:
        # If shapes don't match, use df1 as the mean
        df_mean = df1.copy()
        has_combined = False
    
    title_suffix = "rep1 + rep 2" if has_combined else "rep1 only"
    sns.heatmap(df_mean, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[0, 2])
    axs[0, 2].set_title(title_suffix)
    
    # Resort based on combined/mean data
    competitive_scores_final = [np.mean(df_mean.loc[row_col, :]) for row_col in df_mean.index]
    sorted_idx_final = np.argsort(competitive_scores_final)[::-1]
    
    # Plot with new sorting - only use indices that exist in each dataframe
    if len(sorted_idx_final) <= len(df1.index) and len(sorted_idx_final) <= len(df1.columns):
        sns.heatmap(df1.iloc[sorted_idx_final, sorted_idx_final], annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[1, 0])
        axs[1, 0].set_title("rep 1 (sorted by final)")
    else:
        sns.heatmap(df1, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[1, 0])
        axs[1, 0].set_title("rep 1")
    
    if has_combined and len(sorted_idx_final) <= len(df2.index) and len(sorted_idx_final) <= len(df2.columns):
        sns.heatmap(df2.iloc[sorted_idx_final, sorted_idx_final], annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[1, 1])
        axs[1, 1].set_title("rep 2 (sorted by final)")
    else:
        sns.heatmap(df2, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[1, 1])
        axs[1, 1].set_title("rep 2")
    
    sns.heatmap(df_mean.iloc[sorted_idx_final, sorted_idx_final], annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[1, 2])
    axs[1, 2].set_title(f"{title_suffix} (sorted)")
    
    plt.tight_layout()
    
    # Save figure
    filename = f"Hierarchy_Analysis_{Variable2plot}_{com_type}_{medium}_{species_num}.png"
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
    plt.close(fig)  # Close figure instead of showing
    
    return df_mean.iloc[sorted_idx_final, sorted_idx_final]

def plot_hierarchy_with_significance(Coalescence_data, Communities_data, Metadata, exception_list,
                                   com_type='S', Variable2plot='SimilarityTo1_BC_5', medium='M', species_num=12, rep=2):
    """Plot hierarchy with significance testing"""
    
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    
    # Get data
    Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
    Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
    
    matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
    df = pd.DataFrame(matrix)
    df_sorted = df.sort_index(axis=1).sort_index(axis=0)
    
    # Create competitive scores (inverted for better visualization)
    competitive_scores = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
    sorted_idx = np.argsort(competitive_scores)
    df_sorted = df_sorted.iloc[sorted_idx, sorted_idx]
    
    # Plot heatmap
    sns.heatmap(df_sorted, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[0])
    axs[0].set_title(f'{Variable2plot}_{com_type}_{medium}_{species_num}')
    axs[0].xaxis.tick_top()
    
    # Try to get community data for labeling
    try:
        com_columns = Communities_data[Communities_data['SampleIDX'].isin(df_sorted.columns.tolist())]
        if not com_columns.empty:
            axs[0].set_xticklabels(com_columns['SampleIDX'].tolist())
            axs[0].set_yticklabels(com_columns['SampleIDX'].tolist())
    except:
        pass  # Keep default labels if community data unavailable
    
    # Calculate and plot hierarchy score significance
    permutated_scores, p_value, hs = calculate_significance(df.values, 1000)
    
    axs[1].hist(permutated_scores, bins=50, alpha=0.5, range=(0.5, 1), density=True)
    axs[1].axvline(x=hs, linestyle='--', color='red', label='Actual Score')
    axs[1].text(0.1, 0.9, f'p = {p_value:.4f}', ha='center', va='center', 
                transform=axs[1].transAxes)
    axs[1].legend()
    axs[1].set_xlabel('Hierarchy Scores')
    axs[1].set_ylabel('Frequency')
    axs[1].set_title(f'Hierarchy Score = {hs:.3f}')
    
    # Plot competitive scores
    sorted_scores = np.array(competitive_scores)[sorted_idx]
    axs[2].bar(range(len(sorted_scores)), sorted_scores)
    axs[2].set_xlabel('Communities (sorted)')
    axs[2].set_ylabel('Competitive Score')
    axs[2].set_title('Competitive Hierarchy')
    
    plt.tight_layout()
    
    # Save figure
    filename = f"Hierarchy_Analysis_with_significance_{Variable2plot}_{com_type}_{medium}_{species_num}_rep{rep}.png"
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
    plt.close(fig)  # Close figure instead of showing
    
    print(f"Hierarchy Score: {hs:.4f}")
    print(f"P-value: {p_value:.4f}")
    
    return hs, p_value

def calculate_hierarchy_scores_summary(Coalescence_data, Communities_data, Metadata, exception_list):
    """Calculate hierarchy scores for different conditions"""
    
    print("Calculating hierarchy scores for different conditions...")
    
    # Conditions to test
    conditions = [
        ('N', 'L', 0), ('N', 'M', 0), ('N', 'H', 0),  # Natural communities
        ('S', 'L', 6), ('S', 'L', 12), ('S', 'L', 24),  # Synthetic LN
        ('S', 'M', 6), ('S', 'M', 12), ('S', 'M', 24),  # Synthetic MN  
        ('S', 'H', 6), ('S', 'H', 12), ('S', 'H', 24)   # Synthetic HN
    ]
    
    Variable2plot = 'SimilarityTo1_BC_3'
    results = []
    
    for com_type, medium, species_num in conditions:
        print(f"Processing: {com_type} {medium} {species_num}")
        
        try:
            # Calculate for both replicates
            rep1_scores = []
            rep2_scores = []
            
            for rep in [1, 2]:
                Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
                Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
                
                if len(Coal_IDX_list) > 0 and len(Sub_IDX_list) > 0:
                    matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
                    df = pd.DataFrame(matrix)
                    
                    if not df.empty:
                        hs = calculate_hierarchy_score(df.values)
                        if rep == 1:
                            rep1_scores.append(hs)
                        else:
                            rep2_scores.append(hs)
            
            # Store results
            rep1_mean = np.mean(rep1_scores) if rep1_scores else np.nan
            rep2_mean = np.mean(rep2_scores) if rep2_scores else np.nan
            
            results.append({
                'CommunityType': com_type,
                'Medium': medium,
                'SpeciesNum': species_num,
                'Rep1_HierarchyScore': rep1_mean,
                'Rep2_HierarchyScore': rep2_mean,
                'Mean_HierarchyScore': np.nanmean([rep1_mean, rep2_mean])
            })
            
        except Exception as e:
            print(f"Error processing {com_type} {medium} {species_num}: {e}")
            continue
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(results)
    
    # Save results
    summary_df.to_csv(os.path.join(output_dir, "hierarchy_scores_summary.csv"), index=False)
    
    print("\nHierarchy Scores Summary:")
    print(summary_df.to_string(index=False))
    
    return summary_df

def plot_hierarchy_scores_comparison(summary_df):
    """Plot comparison of hierarchy scores across conditions"""
    
    # Filter for specific conditions to compare
    natural_data = summary_df[summary_df['CommunityType'] == 'N']
    synthetic_data = summary_df[summary_df['CommunityType'] == 'S']
    
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot natural communities
    if not natural_data.empty:
        conditions = natural_data['Medium'].tolist()
        rep1_scores = natural_data['Rep1_HierarchyScore'].tolist()
        rep2_scores = natural_data['Rep2_HierarchyScore'].tolist()
        
        x = np.arange(len(conditions))
        width = 0.35
        
        axs[0].bar(x - width/2, rep1_scores, width, label='Rep 1', alpha=0.8)
        axs[0].bar(x + width/2, rep2_scores, width, label='Rep 2', alpha=0.8)
        
        axs[0].set_xlabel('Medium')
        axs[0].set_ylabel('Hierarchy Score')
        axs[0].set_title('Natural Communities')
        axs[0].set_xticks(x)
        axs[0].set_xticklabels(conditions)
        axs[0].legend()
        axs[0].set_ylim([0.5, 1.0])
    
    # Plot synthetic communities (group by medium, show species pool effect)
    if not synthetic_data.empty:
        mediums = ['L', 'M', 'H']
        species_pools = [6, 12, 24]
        
        x = np.arange(len(mediums))
        width = 0.25
        
        for i, sp_num in enumerate(species_pools):
            sp_data = synthetic_data[synthetic_data['SpeciesNum'] == sp_num]
            if not sp_data.empty:
                scores = []
                for medium in mediums:
                    medium_data = sp_data[sp_data['Medium'] == medium]
                    if not medium_data.empty:
                        scores.append(medium_data['Mean_HierarchyScore'].iloc[0])
                    else:
                        scores.append(0)
                
                axs[1].bar(x + i*width - width, scores, width, 
                          label=f'{sp_num} species', alpha=0.8)
        
        axs[1].set_xlabel('Medium')
        axs[1].set_ylabel('Hierarchy Score')
        axs[1].set_title('Synthetic Communities')
        axs[1].set_xticks(x)
        axs[1].set_xticklabels(mediums)
        axs[1].legend()
        axs[1].set_ylim([0.5, 1.0])
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "hierarchy_scores_comparison.png"), bbox_inches='tight', dpi=300)
    plt.close()  # Close figure instead of showing

def main():
    """Main function to run hierarchy analysis"""
    print("Starting Hierarchy Analysis...")
    
    # Load data
    Coalescence_data, Communities_data, Metadata, exception_list = load_data()
    
    # Example plots for specific conditions
    print("\nGenerating example hierarchy heatmaps...")
    
    # Plot for synthetic medium nutrients, 12 species
    df_result = plot_hierarchy_heatmaps(
        Coalescence_data, Communities_data, Metadata, exception_list,
        com_type='S', Variable2plot='SimilarityTo1_BC_3', medium='M', species_num=12
    )
    
    # Plot with significance testing
    print("\nGenerating hierarchy analysis with significance testing...")
    hs, p_value = plot_hierarchy_with_significance(
        Coalescence_data, Communities_data, Metadata, exception_list,
        com_type='S', Variable2plot='SimilarityTo1_BC_5', medium='M', species_num=12, rep=2
    )
    
    # Calculate summary for all conditions
    print("\nCalculating hierarchy scores for all conditions...")
    summary_df = calculate_hierarchy_scores_summary(
        Coalescence_data, Communities_data, Metadata, exception_list
    )
    
    # Plot comparison
    print("\nGenerating hierarchy scores comparison plot...")
    plot_hierarchy_scores_comparison(summary_df)
    
    print(f"\nAnalysis complete! All figures saved to: {output_dir}")

if __name__ == "__main__":
    main()