#!/usr/bin/env python3
"""
calculate_hierarchy_scores.py

Purpose: Calculates hierarchy scores for coalescence experiments (without plotting)
Key features:
- Calculates hierarchy scores from dominance matrices
- Performs statistical significance testing with null models
- Saves results to CSV files

Converted from Figure_generation_Hiearchy.ipynb
Author: Gore Lab Coalescence Analysis Team
Date: January 2025
"""

import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

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

def calculate_hierarchy_scores_comprehensive(Coalescence_data, Communities_data, Metadata, exception_list):
    """Calculate hierarchy scores for all conditions with significance testing"""
    
    print("Calculating hierarchy scores for all conditions...")
    
    # Variables to test
    Variable2plot_list = ['SimilarityTo1_BC_3', 'SimilarityTo1_J_3', 'SimilarityTo1_JS_3']
    
    # Conditions to test
    conditions = [
        ('N', 'L', 0), ('N', 'M', 0), ('N', 'H', 0),  # Natural communities
        ('S', 'L', 6), ('S', 'L', 12), ('S', 'L', 24),  # Synthetic LN
        ('S', 'M', 6), ('S', 'M', 12), ('S', 'M', 24),  # Synthetic MN  
        ('S', 'H', 6), ('S', 'H', 12), ('S', 'H', 24)   # Synthetic HN
    ]
    
    all_results = []
    
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
                        matrix = getDominanceMatrix(Variable2plot, Coalescence_data, Coal_IDX_list, Sub_IDX_list)
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
                            
                            all_results.append(result)
                            print(f"    Rep {rep}: HS={hs:.3f}, p={p_value:.3f}, n_comm={len(Sub_IDX_list)}")
                        
            except Exception as e:
                print(f"    Error processing {condition_name}: {e}")
                continue
    
    # Create comprehensive DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Save detailed results
    results_df.to_csv(os.path.join(output_dir, "hierarchy_scores_comprehensive.csv"), index=False)
    
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
        summary_df.to_csv(os.path.join(output_dir, "hierarchy_scores_summary.csv"), index=False)
        
        print("\nHierarchy Scores Summary (top 20 rows):")
        print(summary_df.head(20).to_string(index=False))
        
        # Print some key comparisons
        print("\n" + "="*80)
        print("KEY COMPARISONS")
        print("="*80)
        
        # Natural vs Synthetic (BC similarity metric)
        bc_data = summary_df[summary_df['Variable'] == 'SimilarityTo1_BC_3']
        if not bc_data.empty:
            print("\nNatural Communities (BC similarity):")
            nat_data = bc_data[bc_data['CommunityType'] == 'N'].sort_values('Medium')
            for _, row in nat_data.iterrows():
                print(f"  {row['Medium']}: {row['Mean_HierarchyScore']:.3f} ± {row['Std_HierarchyScore']:.3f}")
            
            print("\nSynthetic Communities - 12 species (BC similarity):")
            syn_data = bc_data[(bc_data['CommunityType'] == 'S') & (bc_data['SpeciesNum'] == 12)].sort_values('Medium')
            for _, row in syn_data.iterrows():
                print(f"  {row['Medium']}: {row['Mean_HierarchyScore']:.3f} ± {row['Std_HierarchyScore']:.3f}")
    
    else:
        print("No results generated!")
    
    return results_df

def main():
    """Main function to run hierarchy analysis"""
    print("Starting Hierarchy Score Calculation...")
    
    # Load data
    Coalescence_data, Communities_data, Metadata, exception_list = load_data()
    
    # Calculate comprehensive hierarchy scores
    print("\nCalculating comprehensive hierarchy scores...")
    results_df = calculate_hierarchy_scores_comprehensive(
        Coalescence_data, Communities_data, Metadata, exception_list
    )
    
    print(f"\nAnalysis complete! Results saved to: {output_dir}")
    print("Files created:")
    print("  - hierarchy_scores_comprehensive.csv (detailed results)")
    print("  - hierarchy_scores_summary.csv (summary by condition)")
    
    return results_df

if __name__ == "__main__":
    main()