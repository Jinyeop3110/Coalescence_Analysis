#!/usr/bin/env python3
"""
plot_species_species_hierarchy.py

Purpose: Calculates and plots species-to-species competitive hierarchy heatmaps
Key features:
- Creates dominance matrices showing which species beat which other species
- Generates hierarchy heatmaps similar to community-level analysis but for individual species
- Calculates species-level hierarchy scores with statistical significance testing
- Uses species abundance data to determine competitive outcomes

Author: Gore Lab Coalescence Analysis Team
Date: January 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from collections import defaultdict
import os
import warnings
warnings.filterwarnings('ignore')

# Import the analysis modules
import VariousMetrics as vm

# Set up plotting style
sns.set_style("ticks")
plt.rcParams.update({
    'legend.fontsize': 'large',
    'figure.figsize': (15, 5),
    'axes.labelsize': 'large',
    'axes.titlesize': 'large',
    'xtick.labelsize': 'medium',
    'ytick.labelsize': 'medium'
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

def get_abundance_vector(processed_sequences, sample_id, threshold=1e-4):
    """Get abundance vector for a sample"""
    sample_rows = processed_sequences[processed_sequences['SampleIDX'] == sample_id]
    
    if sample_rows.empty:
        return None
    
    # Extract abundance vector (skip first column which is SampleIDX)
    abundance_vector = sample_rows.iloc[0, 1:].values.astype(float)
    
    # Clean and normalize
    abundance_vector = np.nan_to_num(abundance_vector, 0)
    abundance_vector = abundance_vector * (abundance_vector > threshold)
    
    # Normalize
    if np.sum(abundance_vector) > 0:
        abundance_vector = abundance_vector / np.sum(abundance_vector)
    
    return abundance_vector

def calculate_species_dominance_matrix(Coalescence_data, processed_sequences, Coal_IDX_list, 
                                     threshold=1e-4, min_abundance=0.01):
    """
    Calculate species-to-species dominance matrix from coalescence experiments.
    
    For each coalescence event, determine which species from parent1 vs parent2 
    are more successful in the offspring community.
    """
    print(f"Processing {len(Coal_IDX_list)} coalescence events for species dominance...")
    
    # Get all species indices
    species_names = processed_sequences.columns[1:].tolist()  # Skip SampleIDX column
    n_species = len(species_names)
    
    # Initialize dominance tracking
    species_encounters = defaultdict(lambda: defaultdict(list))  # species_i -> species_j -> [dominance_scores]
    
    processed_events = 0
    
    for coal_sample_id in Coal_IDX_list:
        # Get coalescence event data
        coal_row = Coalescence_data[Coalescence_data['SampleIDX'] == coal_sample_id]
        
        if coal_row.empty:
            continue
            
        parent1_id = coal_row['SampleIDX_Sub1'].iloc[0]
        parent2_id = coal_row['SampleIDX_Sub2'].iloc[0]
        
        # Get abundance vectors
        parent1_vector = get_abundance_vector(processed_sequences, parent1_id, threshold)
        parent2_vector = get_abundance_vector(processed_sequences, parent2_id, threshold)
        mixed_vector = get_abundance_vector(processed_sequences, coal_sample_id, threshold)
        
        if (parent1_vector is None or parent2_vector is None or mixed_vector is None):
            continue
        
        # Find species that are present in parents and abundant enough
        parent1_present = (parent1_vector > min_abundance)
        parent2_present = (parent2_vector > min_abundance) 
        mixed_present = (mixed_vector > min_abundance)
        
        # For each pair of species where one comes from parent1 and one from parent2
        for i in range(n_species):
            for j in range(n_species):
                if i == j:
                    continue  # Skip same species
                
                # Check if species i is from parent1 and species j is from parent2
                if parent1_present[i] and parent2_present[j]:
                    # Calculate relative success in offspring
                    parent1_contribution = mixed_vector[i] if mixed_present[i] else 0
                    parent2_contribution = mixed_vector[j] if mixed_present[j] else 0
                    
                    # Calculate dominance score: > 0.5 means species i (parent1) dominates species j (parent2)
                    total_contribution = parent1_contribution + parent2_contribution
                    if total_contribution > 0:
                        dominance_score = parent1_contribution / total_contribution
                        species_encounters[i][j].append(dominance_score)
                        # Also record the reverse relationship
                        species_encounters[j][i].append(1 - dominance_score)
        
        processed_events += 1
    
    print(f"Successfully processed {processed_events} coalescence events")
    
    # Convert to dominance matrix
    dominance_matrix = np.full((n_species, n_species), np.nan)
    encounter_counts = np.zeros((n_species, n_species))
    
    for i in range(n_species):
        dominance_matrix[i, i] = 0.5  # Self-dominance is neutral
        for j in range(n_species):
            if i != j and len(species_encounters[i][j]) > 0:
                dominance_matrix[i, j] = np.mean(species_encounters[i][j])
                encounter_counts[i, j] = len(species_encounters[i][j])
    
    # Filter matrix to include only species with sufficient encounters
    min_encounters = 3
    species_with_data = []
    
    for i in range(n_species):
        total_encounters = np.sum(encounter_counts[i, :]) + np.sum(encounter_counts[:, i])
        if total_encounters >= min_encounters:
            species_with_data.append(i)
    
    if len(species_with_data) < 3:
        print(f"Warning: Only {len(species_with_data)} species with sufficient data")
        return None, None, None
    
    # Create filtered matrix
    filtered_matrix = dominance_matrix[np.ix_(species_with_data, species_with_data)]
    filtered_species_names = [species_names[i] for i in species_with_data]
    filtered_encounter_counts = encounter_counts[np.ix_(species_with_data, species_with_data)]
    
    print(f"Species dominance matrix: {filtered_matrix.shape[0]} species with sufficient data")
    
    return filtered_matrix, filtered_species_names, filtered_encounter_counts

def calculate_hierarchy_score(matrix):
    """Calculate hierarchy score from dominance matrix"""
    # Remove NaN values and get valid entries
    valid_mask = ~np.isnan(matrix)
    if np.sum(valid_mask) == 0:
        return 0.5
    
    # Get mean of each row and sort indices
    row_means = np.nanmean(matrix, axis=1)
    mean_indices = np.argsort(-row_means)
    
    # Get mean of each column and sort indices  
    col_means = np.nanmean(matrix, axis=0)
    col_mean_indices = np.argsort(col_means)
    
    # Create sorted matrix
    sorted_matrix = matrix[mean_indices][:, col_mean_indices]
    
    # Get lower triangle mask
    mask = np.tril(np.ones_like(sorted_matrix), k=-1).astype(bool)
    valid_lower = ~np.isnan(sorted_matrix) & mask
    
    if np.sum(valid_lower) == 0:
        return 0.5
    
    non_nan_values = sorted_matrix[valid_lower]
    
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
    valid_mask = ~np.isnan(matrix)
    valid_values = matrix[valid_mask]
    
    if len(valid_values) == 0:
        return matrix.copy()
    
    random_matrix = np.full_like(matrix, np.nan)
    
    # Fill diagonal with 0.5
    np.fill_diagonal(random_matrix, 0.5)
    
    # Fill off-diagonal elements randomly
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if i != j and valid_mask[i, j]:
                random_matrix[i, j] = np.random.choice(valid_values)
    
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
    valid_random_scores = random_scores[~np.isnan(random_scores)]
    
    if len(valid_random_scores) == 0:
        p_value = 1.0
    else:
        p_value = (valid_random_scores >= hierarchy_score).sum() / len(valid_random_scores)
    
    return valid_random_scores, p_value, hierarchy_score

def plot_species_hierarchy_heatmap(dominance_matrix, species_names, encounter_counts, 
                                 condition_name, save_path):
    """
    Plot species-to-species dominance heatmap similar to community-level analysis
    """
    if dominance_matrix is None:
        print(f"No data to plot for {condition_name}")
        return None
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    # Calculate competitive scores and sort
    competitive_scores = np.nanmean(dominance_matrix, axis=1)
    sorted_idx = np.argsort(competitive_scores)[::-1]
    
    # Create sorted matrix and labels
    sorted_matrix = dominance_matrix[sorted_idx][:, sorted_idx]
    sorted_species = [species_names[i] for i in sorted_idx]
    sorted_encounters = encounter_counts[sorted_idx][:, sorted_idx]
    
    # Plot 1: Dominance heatmap
    mask = np.isnan(sorted_matrix)
    
    sns.heatmap(sorted_matrix, annot=True, fmt='.2f', cmap='RdYlBu_r', center=0.5,
                vmin=0, vmax=1, mask=mask, ax=axes[0],
                xticklabels=sorted_species, yticklabels=sorted_species,
                cbar_kws={'label': 'Dominance Score'})
    axes[0].set_title(f'Species Dominance Matrix\n{condition_name}')
    axes[0].set_xlabel('Species (Columns)')
    axes[0].set_ylabel('Species (Rows)')
    
    # Rotate labels for better readability
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].tick_params(axis='y', rotation=0)
    
    # Plot 2: Encounter counts heatmap
    sns.heatmap(sorted_encounters, annot=True, fmt='.0f', cmap='Greys',
                ax=axes[1], xticklabels=sorted_species, yticklabels=sorted_species,
                cbar_kws={'label': 'Number of Encounters'})
    axes[1].set_title(f'Species Encounter Counts\n{condition_name}')
    axes[1].set_xlabel('Species (Columns)')
    axes[1].set_ylabel('Species (Rows)')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].tick_params(axis='y', rotation=0)
    
    # Plot 3: Hierarchy significance
    random_scores, p_value, hs = calculate_significance(dominance_matrix, 500)
    
    if len(random_scores) > 0:
        axes[2].hist(random_scores, bins=30, alpha=0.7, density=True, 
                    color='lightblue', edgecolor='black')
        axes[2].axvline(x=hs, color='red', linestyle='--', linewidth=2, 
                       label=f'Observed Score = {hs:.3f}')
        axes[2].set_xlabel('Hierarchy Scores')
        axes[2].set_ylabel('Density')
        axes[2].set_title(f'Species Hierarchy Significance\np = {p_value:.3f}')
        axes[2].legend()
        
        # Add text with statistics
        axes[2].text(0.05, 0.95, f'Hierarchy Score: {hs:.3f}\nP-value: {p_value:.3f}\nN species: {len(species_names)}', 
                    transform=axes[2].transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Species Hierarchy Score: {hs:.3f}, P-value: {p_value:.3f}")
    
    return hs, p_value

def analyze_species_hierarchy_by_condition(Coalescence_data, Metadata, processed_sequences, exception_list):
    """
    Analyze species-to-species hierarchy across different conditions
    """
    print("Starting species-to-species hierarchy analysis...")
    
    # Test conditions (only synthetic)
    conditions = [
        ('Synthetic LN-6', 'S', 'L', 6),
        ('Synthetic LN-12', 'S', 'L', 12), 
        ('Synthetic LN-24', 'S', 'L', 24),
        ('Synthetic MN-6', 'S', 'M', 6),
        ('Synthetic MN-12', 'S', 'M', 12),
        ('Synthetic MN-24', 'S', 'M', 24),
        ('Synthetic HN-6', 'S', 'H', 6),
        ('Synthetic HN-12', 'S', 'H', 12),
        ('Synthetic HN-24', 'S', 'H', 24),
    ]
    
    results = []
    
    for condition_name, com_type, medium, species_num in conditions:
        print(f"\nProcessing condition: {condition_name}")
        
        # Get coalescence events for this condition  
        Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, 
                                               species_num, -1, exception_list)
        
        if len(Coal_IDX_list) < 10:
            print(f"  Insufficient coalescence events for {condition_name} (n={len(Coal_IDX_list)})")
            continue
        
        # Calculate species dominance matrix
        dominance_matrix, species_names, encounter_counts = calculate_species_dominance_matrix(
            Coalescence_data, processed_sequences, Coal_IDX_list
        )
        
        if dominance_matrix is not None:
            # Generate plot
            plot_path = os.path.join(output_dir, f"Species_Species_Hierarchy_{condition_name.replace(' ', '_').replace('-', '_')}.png")
            hs, p_value = plot_species_hierarchy_heatmap(
                dominance_matrix, species_names, encounter_counts, 
                condition_name, plot_path
            )
            
            # Store results
            results.append({
                'Condition': condition_name,
                'CommunityType': com_type,
                'Medium': medium,
                'SpeciesNum': species_num,
                'N_Species': len(species_names),
                'N_CoalescenceEvents': len(Coal_IDX_list),
                'HierarchyScore': hs,
                'P_value': p_value,
                'Significant': p_value < 0.05,
                'Mean_Encounters': np.mean(encounter_counts[encounter_counts > 0]),
                'Total_Encounters': np.sum(encounter_counts)
            })
    
    # Save results summary
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv(os.path.join(output_dir, "species_species_hierarchy_summary.csv"), index=False)
        
        print("\n" + "="*80)
        print("SPECIES-TO-SPECIES HIERARCHY ANALYSIS SUMMARY")
        print("="*80)
        print(results_df.to_string(index=False))
        
        # Create comparison plot
        plot_condition_comparison(results_df)
    
    return results

def plot_condition_comparison(results_df):
    """Plot comparison of hierarchy scores across conditions"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Hierarchy scores by medium and species number
    mediums = ['L', 'M', 'H']
    species_nums = [6, 12, 24]
    
    for i, medium in enumerate(mediums):
        medium_data = results_df[results_df['Medium'] == medium]
        if not medium_data.empty:
            x_pos = range(len(medium_data))
            axes[0, 0].bar([x + i*0.25 for x in x_pos], medium_data['HierarchyScore'], 
                          width=0.25, label=f'{medium}N', alpha=0.8)
    
    axes[0, 0].set_xlabel('Conditions')
    axes[0, 0].set_ylabel('Species Hierarchy Score')
    axes[0, 0].set_title('Species Hierarchy Scores by Nutrient Condition')
    axes[0, 0].legend()
    
    # Plot 2: P-values
    conditions = results_df['Condition'].tolist()
    p_values = results_df['P_value'].tolist()
    colors = ['red' if p < 0.05 else 'blue' for p in p_values]
    
    axes[0, 1].bar(range(len(conditions)), p_values, color=colors, alpha=0.7)
    axes[0, 1].axhline(y=0.05, color='red', linestyle='--', alpha=0.5, label='p=0.05')
    axes[0, 1].set_xlabel('Conditions')
    axes[0, 1].set_ylabel('P-value')
    axes[0, 1].set_title('Statistical Significance of Species Hierarchy')
    axes[0, 1].set_xticks(range(len(conditions)))
    axes[0, 1].set_xticklabels(conditions, rotation=45, ha='right')
    axes[0, 1].legend()
    
    # Plot 3: Number of species vs hierarchy score
    axes[1, 0].scatter(results_df['N_Species'], results_df['HierarchyScore'], 
                      c=results_df['SpeciesNum'], cmap='viridis', alpha=0.7)
    axes[1, 0].set_xlabel('Number of Species in Analysis')
    axes[1, 0].set_ylabel('Hierarchy Score')
    axes[1, 0].set_title('Species Diversity vs Hierarchy Strength')
    cbar = plt.colorbar(axes[1, 0].collections[0], ax=axes[1, 0])
    cbar.set_label('Species Pool Size')
    
    # Plot 4: Hierarchy score vs total encounters
    axes[1, 1].scatter(results_df['Total_Encounters'], results_df['HierarchyScore'], 
                      alpha=0.7)
    for i, condition in enumerate(results_df['Condition']):
        axes[1, 1].annotate(condition, 
                           (results_df['Total_Encounters'].iloc[i], 
                            results_df['HierarchyScore'].iloc[i]), 
                           fontsize=8, alpha=0.7)
    axes[1, 1].set_xlabel('Total Species Encounters')
    axes[1, 1].set_ylabel('Hierarchy Score')
    axes[1, 1].set_title('Data Quantity vs Hierarchy Score')
    
    plt.suptitle('Species-to-Species Hierarchy: Cross-Condition Analysis', fontsize=16)
    plt.tight_layout()
    
    comparison_path = os.path.join(output_dir, "Species_Species_Hierarchy_Comparison.png")
    plt.savefig(comparison_path, dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main function to run species-to-species hierarchy analysis"""
    print("Starting Species-to-Species Hierarchy Analysis...")
    
    # Load data
    Coalescence_data, Metadata, processed_sequences, exception_list = load_data()
    
    # Run analysis
    results = analyze_species_hierarchy_by_condition(
        Coalescence_data, Metadata, processed_sequences, exception_list
    )
    
    print(f"\nSpecies-to-species hierarchy analysis complete!")
    print(f"Results saved to: {output_dir}")
    print("Files created:")
    print("  - species_species_hierarchy_summary.csv")
    print("  - Individual condition heatmaps: Species_Species_Hierarchy_[Condition].png")
    print("  - Cross-condition comparison: Species_Species_Hierarchy_Comparison.png")

if __name__ == "__main__":
    main()