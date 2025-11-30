#!/usr/bin/env python3
"""
plot_true_species_hierarchy.py

Purpose: Calculates and plots TRUE species-to-species (ASV-to-ASV) dominance hierarchy
Key features:
- Creates ASV dominance matrices from coalescence abundance data
- Tracks which ASVs win/lose in coalescence events
- Uses actual ASV IDs (NormalizedAbundance1, etc.) as row/column labels
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
    'xtick.labelsize': 'large',
    'ytick.labelsize': 'large'
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
    
    # Get ASV column names
    asv_columns = [col for col in processed_sequences.columns if col != 'SampleIDX']
    print(f"Number of ASVs: {len(asv_columns)}")
    
    return Coalescence_data, Metadata, processed_sequences, asv_columns, exception_list

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

def get_dominant_asvs(processed_sequences, sample_ids, top_n=5, min_abundance=0.05):
    """
    Get the most abundant ASVs for each sample.
    Returns dict: {sample_id: [list of dominant ASV names]}
    """
    asv_columns = [col for col in processed_sequences.columns if col != 'SampleIDX']
    sample_dominant_asvs = {}
    
    for sample_id in sample_ids:
        sample_data = processed_sequences[processed_sequences['SampleIDX'] == sample_id]
        if sample_data.empty:
            continue
            
        # Get abundances for this sample
        abundances = sample_data[asv_columns].iloc[0]
        
        # Filter ASVs above minimum abundance threshold
        abundant_asvs = abundances[abundances >= min_abundance]
        
        # Sort by abundance and take top N
        top_asvs = abundant_asvs.nlargest(top_n).index.tolist()
        sample_dominant_asvs[sample_id] = top_asvs
    
    return sample_dominant_asvs

def calculate_asv_dominance_from_coalescence(Coalescence_data, processed_sequences, 
                                           Coal_IDX_list, Sub_IDX_list, 
                                           Variable2plot='SimilarityTo1_BC_3'):
    """
    Calculate ASV-to-ASV dominance based on coalescence outcomes.
    
    Logic:
    1. For each coalescence event, identify dominant ASVs in parent communities
    2. Use similarity score to determine which parent "wins"
    3. Track which ASVs from winning parent dominate ASVs from losing parent
    """
    
    print(f"Calculating ASV dominance from {len(Coal_IDX_list)} coalescence events...")
    
    # Get dominant ASVs for each subcommunity (parent)
    parent_dominant_asvs = get_dominant_asvs(processed_sequences, Sub_IDX_list, top_n=3, min_abundance=0.1)
    
    # Get all unique ASVs that appear as dominant
    all_dominant_asvs = set()
    for asvs in parent_dominant_asvs.values():
        all_dominant_asvs.update(asvs)
    all_dominant_asvs = sorted(list(all_dominant_asvs))
    
    print(f"Found {len(all_dominant_asvs)} dominant ASVs across all subcommunities")
    
    # Initialize dominance matrix
    asv_dominance_matrix = {}
    for asv1 in all_dominant_asvs:
        asv_dominance_matrix[asv1] = {}
        for asv2 in all_dominant_asvs:
            asv_dominance_matrix[asv1][asv2] = []  # List to store dominance values
    
    # Process each coalescence event
    successful_events = 0
    for SampleIDX in Coal_IDX_list:
        idx = np.where(Coalescence_data['SampleIDX'] == SampleIDX)[0]
        if len(idx) == 0:
            continue
            
        # Get coalescence information
        similarity_value = Coalescence_data.iloc[idx[0]][Variable2plot]
        subSampleIDX1 = Coalescence_data.iloc[idx[0]]["SampleIDX_Sub1"]
        subSampleIDX2 = Coalescence_data.iloc[idx[0]]["SampleIDX_Sub2"]
        
        # Check if both parents have dominant ASV data
        if subSampleIDX1 not in parent_dominant_asvs or subSampleIDX2 not in parent_dominant_asvs:
            continue
            
        parent1_asvs = parent_dominant_asvs[subSampleIDX1]
        parent2_asvs = parent_dominant_asvs[subSampleIDX2]
        
        if len(parent1_asvs) == 0 or len(parent2_asvs) == 0:
            continue
        
        # similarity_value > 0.5 means parent1 dominates parent2
        dominance_strength = similarity_value
        
        # Record dominance relationships between ASVs
        for asv1 in parent1_asvs:
            for asv2 in parent2_asvs:
                if asv1 in asv_dominance_matrix and asv2 in asv_dominance_matrix[asv1]:
                    asv_dominance_matrix[asv1][asv2].append(dominance_strength)
                    asv_dominance_matrix[asv2][asv1].append(1 - dominance_strength)
        
        successful_events += 1
    
    print(f"Successfully processed {successful_events} coalescence events for ASV dominance")
    
    # Convert lists to mean values
    final_matrix = {}
    for asv1 in all_dominant_asvs:
        final_matrix[asv1] = {}
        for asv2 in all_dominant_asvs:
            if asv1 == asv2:
                final_matrix[asv1][asv2] = 0.5  # Self-dominance is neutral
            else:
                dominance_values = asv_dominance_matrix[asv1][asv2]
                if len(dominance_values) > 0:
                    final_matrix[asv1][asv2] = np.mean(dominance_values)
                else:
                    final_matrix[asv1][asv2] = np.nan  # No data available
    
    return final_matrix, all_dominant_asvs

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
    # Only use non-NaN values for generating random values
    non_nan_values = matrix[~np.isnan(matrix)]
    if len(non_nan_values) == 0:
        return matrix.copy()
        
    random_matrix = np.zeros(matrix.shape)
    idx = np.tril_indices(matrix.shape[0], k=-1)
    
    # Fill lower triangle with random values from the original matrix
    random_values = np.random.choice(non_nan_values, size=len(idx[0]), replace=True)
    random_matrix[idx] = random_values
    random_matrix[np.triu_indices(matrix.shape[0], k=1)] = 1 - random_values
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

def plot_asv_hierarchy_with_significance(Coalescence_data, processed_sequences, Metadata, exception_list,
                                       com_type='S', Variable2plot='SimilarityTo1_BC_3', medium='M', species_num=12, rep=2):
    """Plot ASV hierarchy with significance testing"""
    
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    
    # Get data
    Sub_IDX_list = Community_PermutateList("F", com_type, medium, "S", Metadata, species_num, rep, exception_list)
    Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, species_num, rep, exception_list)
    
    print(f"Found {len(Sub_IDX_list)} subcommunities and {len(Coal_IDX_list)} coalescence events")
    
    # Calculate ASV dominance matrix
    asv_matrix, dominant_asvs = calculate_asv_dominance_from_coalescence(
        Coalescence_data, processed_sequences, Coal_IDX_list, Sub_IDX_list, Variable2plot)
    
    if len(dominant_asvs) < 2:
        print("Not enough dominant ASVs found for analysis")
        return np.nan, np.nan
    
    # Convert to DataFrame
    df = pd.DataFrame(asv_matrix, index=dominant_asvs, columns=dominant_asvs)
    
    # Check for sufficient data
    non_nan_count = (~df.isna()).sum().sum()
    if non_nan_count < 4:
        print(f"Insufficient data: only {non_nan_count} non-NaN values")
        return np.nan, np.nan
    
    # Create competitive scores and sort
    row_means = df.mean(axis=1, skipna=True)
    sorted_idx = row_means.argsort()[::-1]  # Sort descending by competitive ability
    df_sorted = df.iloc[sorted_idx, sorted_idx]
    
    # Plot heatmap
    mask = df_sorted.isna()
    sns.heatmap(df_sorted, annot=True, cmap='YlGnBu', vmin=0, vmax=1, 
                ax=axs[0], mask=mask, fmt='.2f')
    axs[0].set_title(f'ASV Dominance: {Variable2plot}_{com_type}_{medium}_{species_num}')
    axs[0].set_xlabel('ASVs (sorted by competitive ability)')
    axs[0].set_ylabel('ASVs (sorted by competitive ability)')
    
    # Simplify ASV labels for readability
    simplified_labels = [f"ASV{col.replace('NormalizedAbundance', '')}" for col in df_sorted.columns]
    axs[0].set_xticklabels(simplified_labels, rotation=45)
    axs[0].set_yticklabels(simplified_labels, rotation=0)
    
    # Calculate and plot hierarchy score significance
    matrix_values = df.values
    permutated_scores, p_value, hs = calculate_significance(matrix_values, 100)
    
    axs[1].hist(permutated_scores, bins=30, alpha=0.5, density=True)
    axs[1].axvline(x=hs, linestyle='--', color='red', label='Actual Score')
    axs[1].text(0.1, 0.9, f'p = {p_value:.3f}', ha='center', va='center', 
                transform=axs[1].transAxes, fontsize=12)
    axs[1].legend()
    axs[1].set_xlabel('Hierarchy Scores')
    axs[1].set_ylabel('Frequency')
    axs[1].set_title(f'ASV Hierarchy Score = {hs:.3f}')
    
    # Plot competitive scores
    competitive_scores = row_means.iloc[sorted_idx].values
    axs[2].bar(range(len(competitive_scores)), competitive_scores)
    axs[2].set_xlabel('ASVs (sorted)')
    axs[2].set_ylabel('Mean Dominance Score')
    axs[2].set_title('ASV Competitive Ranking')
    axs[2].set_xticks(range(len(simplified_labels)))
    axs[2].set_xticklabels(simplified_labels, rotation=45)
    
    plt.tight_layout()
    
    # Save figure
    filename = f"TRUE_ASV_Hierarchy_{Variable2plot}_{com_type}_{medium}_{species_num}_rep{rep}.png"
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    print(f"ASV Hierarchy Score: {hs:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Number of dominant ASVs: {len(dominant_asvs)}")
    
    return hs, p_value

def main():
    """Main function to run true ASV hierarchy analysis"""
    print("Starting TRUE ASV (Species) Hierarchy Analysis...")
    
    # Load data
    Coalescence_data, Metadata, processed_sequences, asv_columns, exception_list = load_data()
    
    # Test with different conditions
    test_conditions = [
        ('S', 'SimilarityTo1_BC_3', 'H', 12, 1),
        ('S', 'SimilarityTo1_BC_3', 'H', 12, 2),
        ('S', 'SimilarityTo1_BC_3', 'M', 12, 1),
        ('S', 'SimilarityTo1_BC_3', 'L', 12, 1),
    ]
    
    results = []
    for com_type, variable, medium, species_num, rep in test_conditions:
        print(f"\n=== Processing: {com_type} {medium} {species_num} species, rep {rep} ===")
        
        try:
            hs, p_value = plot_asv_hierarchy_with_significance(
                Coalescence_data, processed_sequences, Metadata, exception_list,
                com_type=com_type, Variable2plot=variable, medium=medium, 
                species_num=species_num, rep=rep
            )
            
            results.append({
                'CommunityType': com_type,
                'Variable': variable,
                'Medium': medium,
                'SpeciesNum': species_num,
                'Replicate': rep,
                'HierarchyScore': hs,
                'P_value': p_value
            })
            
        except Exception as e:
            print(f"Error processing {com_type} {medium} {species_num} rep {rep}: {e}")
            continue
    
    # Save results
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(os.path.join(output_dir, "TRUE_ASV_hierarchy_results.csv"), index=False)
        print("\nTRUE ASV Hierarchy Results:")
        print(results_df.to_string(index=False))
    
    print(f"\nTrue ASV hierarchy analysis complete! Results saved to: {output_dir}")

if __name__ == "__main__":
    main()