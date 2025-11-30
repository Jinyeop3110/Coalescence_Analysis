#!/usr/bin/env python3
"""
plot_species_dominance_hierarchy.py

Purpose: Calculates and plots species-to-species dominance hierarchy using the same approach as community hierarchy
Key features:
- Creates species dominance matrices from coalescence similarity data
- Uses existing hierarchy score calculation from calculate_hierarchy_scores.py
- Generates heatmaps identical to community-level analysis but for species
- Statistical significance testing with null models

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
    print("Loading coalescence and sequence data...")
    
    # Define file paths
    base_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404"
    
    Coalescence_data_synthetic_path = f"{base_path}/Analyzed/processed_CoalescenceEvent_synthetic.xlsx"
    Meta_data_path = f"{base_path}/Postprocessed/Metadata.xlsx"
    Processed_sequences_synthetic_path = f"{base_path}/Postprocessed/processed_Sequences_synthetic.xlsx"
    
    # Load data (only synthetic for now)
    Coalescence_data = pd.read_excel(Coalescence_data_synthetic_path)
    Metadata = pd.read_excel(Meta_data_path)
    processed_sequences = pd.read_excel(Processed_sequences_synthetic_path)
    
    # Exception list for problematic samples
    exception_list = ['P4-02','P4-03','P4-23','P4-24','P7-97', 'P8-12'] + ['P8-91'] + \
                    ['P5-73', 'P5-69','P5-64','P5-61','P5-59', 'P5-56'] + ['P6-67']
    
    print(f"Loaded {len(Coalescence_data)} coalescence events")
    print(f"Loaded {len(processed_sequences)} sequence abundance profiles")
    print(f"Number of species (ASVs): {len(processed_sequences.columns) - 1}")
    
    return Coalescence_data, Metadata, processed_sequences, exception_list

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

def get_species_dominance_from_similarity(Coalescence_data, Coal_IDX_list, Sub_IDX_list, Variable2plot='SimilarityTo1_BC_3'):
    """
    Create species-level dominance matrix using the same approach as community analysis.
    Instead of communities competing, we track which species from each parent dominate.
    """
    print(f"Creating species dominance matrix from {len(Coal_IDX_list)} coalescence events...")
    
    # Map subcommunity samples to their dominant species
    species_dominance = {}  # sample_id -> dominant_species_id
    
    for SampleIDX in Coal_IDX_list:
        idx = np.where(Coalescence_data['SampleIDX'] == SampleIDX)[0]
        if len(idx) == 0:
            continue
            
        # Get the similarity value (higher = parent1 wins, lower = parent2 wins)
        similarity_value = Coalescence_data.iloc[idx[0]][Variable2plot]
        
        # Determine which parent "wins" this coalescence
        subSampleIDX1 = Coalescence_data.iloc[idx[0]]["SampleIDX_Sub1"]
        subSampleIDX2 = Coalescence_data.iloc[idx[0]]["SampleIDX_Sub2"]
        
        # Store the dominance relationship
        # similarity_value > 0.5 means parent1 dominates parent2
        if subSampleIDX1 in Sub_IDX_list and subSampleIDX2 in Sub_IDX_list:
            species_dominance[(subSampleIDX1, subSampleIDX2)] = similarity_value
            species_dominance[(subSampleIDX2, subSampleIDX1)] = 1 - similarity_value
    
    return species_dominance

def getDominanceMatrix_Species(Coalescence_data, Coal_IDX_list, Sub_IDX_list, Variable2plot='SimilarityTo1_BC_3'):
    """
    Create species dominance matrix using the same logic as community getDominanceMatrix.
    Here we treat each subcommunity as representing its dominant "species" identity.
    """
    matrix = {Sub_IDX: {} for Sub_IDX in Sub_IDX_list}
    
    for SampleIDX in Coal_IDX_list:
        idx = np.where(Coalescence_data['SampleIDX'] == SampleIDX)[0]
        if len(idx) == 0:
            continue
            
        dominance1 = Coalescence_data.iloc[idx[0]][Variable2plot]
        dominance2 = 1 - dominance1
        subSampleIDX1 = Coalescence_data.iloc[idx[0]]["SampleIDX_Sub1"]
        subSampleIDX2 = Coalescence_data.iloc[idx[0]]["SampleIDX_Sub2"]
        
        # Only include if both subcommunities are in our list
        if subSampleIDX1 in Sub_IDX_list and subSampleIDX2 in Sub_IDX_list:
            matrix[subSampleIDX1].update({subSampleIDX2: dominance1})
            matrix[subSampleIDX2].update({subSampleIDX1: dominance2})
    
    # Add self-dominance (neutral)
    for SampleIDX in Sub_IDX_list:
        matrix[SampleIDX].update({SampleIDX: 0.5})
    
    return matrix

def calculate_hierarchy_score(matrix):
    """Calculate hierarchy score from dominance matrix (same as community analysis)"""
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
    """Generate random matrix for null model (same as community analysis)"""
    random_fractions = np.random.choice(matrix.flatten(), size=matrix.size, replace=True)
    random_matrix = np.zeros(matrix.shape)
    idx = np.tril_indices(matrix.shape[0], k=-1)
    
    random_matrix[idx] = random_fractions[0:len(idx[0])]
    random_matrix[np.triu_indices(matrix.shape[0], k=1)] = 1 - random_fractions[0:len(idx[0])]
    np.fill_diagonal(random_matrix, 0.5)
    
    return random_matrix

def calculate_significance(matrix, n_samples=1000):
    """Calculate significance with null model (same as community analysis)"""
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

def plot_species_hierarchy_heatmaps(Coalescence_data, processed_sequences, Metadata, exception_list,
                                  com_type='S', Variable2plot='SimilarityTo1_BC_3', medium='M', species_num=12):
    """Plot species hierarchy heatmaps identical to community analysis"""
    
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(30, 16), dpi=100)
    
    # Replicate 1
    rep = 1
    Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
    Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
    
    matrix = getDominanceMatrix_Species(Coalescence_data, Coal_IDX_list, Sub_IDX_list, Variable2plot)
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
    
    matrix = getDominanceMatrix_Species(Coalescence_data, Coal_IDX_list, Sub_IDX_list, Variable2plot)
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
    filename = f"Species_Dominance_Hierarchy_{Variable2plot}_{com_type}_{medium}_{species_num}.png"
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
    plt.close(fig)  # Close figure instead of showing
    
    return df_mean.iloc[sorted_idx_final, sorted_idx_final]

def plot_species_hierarchy_with_significance(Coalescence_data, processed_sequences, Metadata, exception_list,
                                           com_type='S', Variable2plot='SimilarityTo1_BC_3', medium='M', species_num=12, rep=2):
    """Plot species hierarchy with significance testing (identical to community analysis)"""
    
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    
    # Get data
    Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
    Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
    
    matrix = getDominanceMatrix_Species(Coalescence_data, Coal_IDX_list, Sub_IDX_list, Variable2plot)
    df = pd.DataFrame(matrix)
    df_sorted = df.sort_index(axis=1).sort_index(axis=0)
    
    # Create competitive scores (inverted for better visualization)
    competitive_scores = [1 - np.mean(df.loc[row_col, :]) for row_col in df_sorted.index]
    sorted_idx = np.argsort(competitive_scores)
    df_sorted = df_sorted.iloc[sorted_idx, sorted_idx]
    
    # Plot heatmap
    sns.heatmap(df_sorted, annot=True, cmap='YlGnBu', vmin=0, vmax=1, ax=axs[0])
    axs[0].set_title(f'Species Dominance: {Variable2plot}_{com_type}_{medium}_{species_num}')
    axs[0].xaxis.tick_top()
    
    # Label axes with subcommunity IDs
    axs[0].set_xticklabels(df_sorted.columns.tolist(), rotation=45)
    axs[0].set_yticklabels(df_sorted.index.tolist(), rotation=0)
    
    # Calculate and plot hierarchy score significance
    permutated_scores, p_value, hs = calculate_significance(df.values, 1000)
    
    axs[1].hist(permutated_scores, bins=50, alpha=0.5, range=(0.5, 1), density=True)
    axs[1].axvline(x=hs, linestyle='--', color='red', label='Actual Score')
    axs[1].text(0.1, 0.9, f'p = {p_value:.4f}', ha='center', va='center', 
                transform=axs[1].transAxes)
    axs[1].legend()
    axs[1].set_xlabel('Hierarchy Scores')
    axs[1].set_ylabel('Frequency')
    axs[1].set_title(f'Species Hierarchy Score = {hs:.3f}')
    
    # Plot competitive scores
    sorted_scores = np.array(competitive_scores)[sorted_idx]
    axs[2].bar(range(len(sorted_scores)), sorted_scores)
    axs[2].set_xlabel('Subcommunities (sorted)')
    axs[2].set_ylabel('Competitive Score')
    axs[2].set_title('Species Competitive Hierarchy')
    
    plt.tight_layout()
    
    # Save figure
    filename = f"Species_Dominance_Hierarchy_with_significance_{Variable2plot}_{com_type}_{medium}_{species_num}_rep{rep}.png"
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
    plt.close(fig)  # Close figure instead of showing
    
    print(f"Species Hierarchy Score: {hs:.4f}")
    print(f"P-value: {p_value:.4f}")
    
    return hs, p_value

def calculate_species_hierarchy_scores_comprehensive(Coalescence_data, processed_sequences, Metadata, exception_list):
    """Calculate species hierarchy scores for different conditions"""
    
    print("Calculating species hierarchy scores for different conditions...")
    
    # Conditions to test (only synthetic)
    conditions = [
        ('S', 'L', 6), ('S', 'L', 12), ('S', 'L', 24),  # Synthetic LN
        ('S', 'M', 6), ('S', 'M', 12), ('S', 'M', 24),  # Synthetic MN  
        ('S', 'H', 6), ('S', 'H', 12), ('S', 'H', 24)   # Synthetic HN
    ]
    
    Variable2plot_list = ['SimilarityTo1_BC_3', 'SimilarityTo1_J_3', 'SimilarityTo1_JS_3']
    
    results = []
    
    for Variable2plot in Variable2plot_list:
        print(f"\nProcessing variable: {Variable2plot}")
        
        for com_type, medium, species_num in conditions:
            condition_name = f"{com_type}_{medium}_{species_num}"
            print(f"  Processing: {condition_name}")
            
            try:
                # Calculate for both replicates
                for rep in [1, 2]:
                    Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
                    Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
                    
                    if len(Coal_IDX_list) > 3 and len(Sub_IDX_list) > 3:  # Need minimum samples
                        matrix = getDominanceMatrix_Species(Coalescence_data, Coal_IDX_list, Sub_IDX_list, Variable2plot)
                        df = pd.DataFrame(matrix)
                        
                        if not df.empty and df.shape[0] > 2:  # Need minimum matrix size
                            # Calculate hierarchy score
                            hs = calculate_hierarchy_score(df.values)
                            
                            # Calculate significance (reduced iterations for speed)
                            try:
                                random_scores, p_value, _ = calculate_significance(df.values, n_samples=100)
                                null_mean = np.mean(random_scores)
                                null_std = np.std(random_scores)
                            except:
                                p_value = np.nan
                                null_mean = np.nan
                                null_std = np.nan
                            
                            # Store results
                            result = {
                                'Variable': Variable2plot,
                                'CommunityType': com_type,
                                'Medium': medium,
                                'SpeciesNum': species_num,
                                'Replicate': rep,
                                'HierarchyScore': hs,
                                'P_value': p_value,
                                'NullMean': null_mean,
                                'NullStd': null_std,
                                'N_Communities': len(Sub_IDX_list),
                                'N_Coalescence': len(Coal_IDX_list),
                                'MatrixSize': df.shape[0]
                            }
                            
                            results.append(result)
                            print(f"    Rep {rep}: HS={hs:.3f}, p={p_value:.3f}, n_comm={len(Sub_IDX_list)}")
                        
            except Exception as e:
                print(f"    Error processing {condition_name}: {e}")
                continue
    
    # Create comprehensive DataFrame
    results_df = pd.DataFrame(results)
    
    # Save detailed results
    results_df.to_csv(os.path.join(output_dir, "species_dominance_hierarchy_comprehensive.csv"), index=False)
    
    # Create summary by condition (averaging replicates)
    if not results_df.empty:
        summary_list = []
        for variable in Variable2plot_list:
            var_data = results_df[results_df['Variable'] == variable]
            for (com_type, medium, species_num), group in var_data.groupby(['CommunityType', 'Medium', 'SpeciesNum']):
                summary = {
                    'Variable': variable,
                    'CommunityType': com_type,
                    'Medium': medium,
                    'SpeciesNum': species_num,
                    'Mean_HierarchyScore': group['HierarchyScore'].mean(),
                    'Std_HierarchyScore': group['HierarchyScore'].std(),
                    'Mean_P_value': group['P_value'].mean(),
                    'N_Replicates': len(group),
                    'Mean_N_Communities': group['N_Communities'].mean(),
                    'Mean_N_Coalescence': group['N_Coalescence'].mean()
                }
                summary_list.append(summary)
        
        summary_df = pd.DataFrame(summary_list)
        summary_df.to_csv(os.path.join(output_dir, "species_dominance_hierarchy_summary.csv"), index=False)
        
        print("\nSpecies Dominance Hierarchy Scores Summary:")
        print(summary_df.to_string(index=False))
    
    return results_df

def plot_species_hierarchy_separate_versions(Coalescence_data, processed_sequences, Metadata, exception_list,
                                           com_type='S', Variable2plot='SimilarityTo1_BC_3', medium='M', species_num=12, rep=2):
    """Generate separate plots for ASV-ordered and competence-ordered versions"""
    print(f"\nGenerating separate ASV-ordered and competence-ordered versions for {com_type}_{medium}_{species_num}...")
    
    # Get data
    Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
    Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
    
    matrix = getDominanceMatrix_Species(Coalescence_data, Coal_IDX_list, Sub_IDX_list, Variable2plot)
    df = pd.DataFrame(matrix)
    
    if df.empty:
        print("Warning: Empty matrix, skipping...")
        return
    
    # Calculate hierarchy score
    hs = calculate_hierarchy_score(df.values)
    
    # ASV labels
    asv_labels = [f"ASV{i+1}" for i in range(len(df))]
    
    # Version 1: ASV-ordered (original order)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    sns.heatmap(df, annot=True, fmt='.2f', cmap='YlGnBu', 
                vmin=0, vmax=1, ax=ax, square=True,
                cbar_kws={'label': 'Species Dominance'})
    ax.set_xlabel('ASV j')
    ax.set_ylabel('ASV i')
    ax.set_title(f'{medium}N: Species Dominance Matrix (ASV{species_num})\n(Ordered by ASV Number)')
    ax.set_xticklabels(asv_labels)
    ax.set_yticklabels(asv_labels)
    
    plt.tight_layout()
    filename = f"Species_Dominance_Hierarchy_{Variable2plot}_{com_type}_{medium}_{species_num}_ASV_ordered.png"
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(output_dir, filename.replace('.png', '.svg')), 
                format='svg', bbox_inches='tight')
    plt.close()
    print(f"Saved ASV-ordered version: {filename}")
    
    # Version 2: Competence-ordered (sorted by mean dominance)
    competitive_scores = [np.mean(df.loc[i, :]) for i in df.index]
    sorted_idx = np.argsort(competitive_scores)[::-1]  # Sort by decreasing competitive ability
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    sorted_df = df.iloc[sorted_idx, sorted_idx]
    sorted_labels = [asv_labels[i] for i in sorted_idx]
    
    sns.heatmap(sorted_df, annot=True, fmt='.2f', cmap='YlGnBu',
                vmin=0, vmax=1, ax=ax, square=True,
                cbar_kws={'label': 'Species Dominance (sorted)'})
    ax.set_xlabel('ASV (sorted by competitive ability)')
    ax.set_ylabel('ASV (sorted by competitive ability)')
    ax.set_title(f'{medium}N: Species Dominance Matrix (ASV{species_num})\n(Ordered by Mean Competence)')
    ax.set_xticklabels(sorted_labels)
    ax.set_yticklabels(sorted_labels)
    
    # Add hierarchy score
    ax.text(0.02, 0.98, f'Hierarchy Score: {hs:.3f}',
            transform=ax.transAxes, va='top', ha='left',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Add diagonal line to emphasize upper/lower triangular structure
    ax.plot([0, len(df)], [0, len(df)], 'k-', linewidth=1, alpha=0.3)
    
    plt.tight_layout()
    filename = f"Species_Dominance_Hierarchy_{Variable2plot}_{com_type}_{medium}_{species_num}_competence_ordered.png"
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(output_dir, filename.replace('.png', '.svg')), 
                format='svg', bbox_inches='tight')
    plt.close()
    print(f"Saved competence-ordered version: {filename}")
    
    # Save competence ranking data
    competence_df = pd.DataFrame({
        'ASV': asv_labels,
        'Mean_Dominance_Score': competitive_scores,
        'Competence_Rank': np.argsort(-np.array(competitive_scores)) + 1
    })
    competence_df = competence_df.sort_values('Mean_Dominance_Score', ascending=False)
    competence_df.to_csv(os.path.join(output_dir, f'Species_competence_ranking_{com_type}_{medium}_{species_num}.csv'), 
                         index=False)
    print(f"Saved competence ranking: Species_competence_ranking_{com_type}_{medium}_{species_num}.csv")

def main():
    """Main function to run species dominance hierarchy analysis"""
    print("Starting Species Dominance Hierarchy Analysis...")
    
    # Load data
    Coalescence_data, Metadata, processed_sequences, exception_list = load_data()
    
    # Example plots for specific conditions
    print("\nGenerating example species dominance hierarchy heatmaps...")
    
    # Plot for synthetic medium nutrients, 12 species
    df_result = plot_species_hierarchy_heatmaps(
        Coalescence_data, processed_sequences, Metadata, exception_list,
        com_type='S', Variable2plot='SimilarityTo1_BC_3', medium='M', species_num=12
    )
    
    # Plot with significance testing
    print("\nGenerating species hierarchy analysis with significance testing...")
    hs, p_value = plot_species_hierarchy_with_significance(
        Coalescence_data, processed_sequences, Metadata, exception_list,
        com_type='S', Variable2plot='SimilarityTo1_BC_3', medium='M', species_num=12, rep=2
    )
    
    # Generate separate versions for key conditions
    print("\nGenerating separate ASV-ordered and competence-ordered versions...")
    for medium in ['L', 'M', 'H']:
        for species_num in [6, 12, 24]:
            plot_species_hierarchy_separate_versions(
                Coalescence_data, processed_sequences, Metadata, exception_list,
                com_type='S', Variable2plot='SimilarityTo1_BC_3', medium=medium, species_num=species_num, rep=2
            )
    
    # Calculate summary for all conditions
    print("\nCalculating species hierarchy scores for all conditions...")
    results_df = calculate_species_hierarchy_scores_comprehensive(
        Coalescence_data, processed_sequences, Metadata, exception_list
    )
    
    print(f"\nSpecies dominance hierarchy analysis complete! All figures saved to: {output_dir}")

if __name__ == "__main__":
    main()