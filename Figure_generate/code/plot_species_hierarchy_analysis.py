#!/usr/bin/env python3
"""
plot_species_hierarchy_analysis.py

Purpose: Calculates and plots species-level hierarchy scores using vector similarity metrics
Key features:
- Species-level competitive hierarchy analysis using abundance vectors
- Uses vector similarity functions from AsymmetricityAnalysis.py and VariousMetrics.py
- Calculates retention probabilities and species dominance hierarchies
- Generates heatmaps and hierarchy plots for species competitive relationships
- Performs statistical significance testing

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
from AsymmetricityAnalysis import calculate_vector_asymmetricity, calculate_retention_asymmetricity_base

# Set up plotting style
sns.set_style("ticks")
plt.rcParams.update({
    'legend.fontsize': 'large',
    'figure.figsize': (12, 8),
    'axes.labelsize': 'large',
    'axes.titlesize': 'large',
    'xtick.labelsize': 'medium',
    'ytick.labelsize': 'medium'
})

# Create output directory
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Hiearchy"
os.makedirs(output_dir, exist_ok=True)

def load_sequence_data():
    """Load processed sequence abundance data"""
    print("Loading sequence abundance data...")
    
    # Define file paths
    base_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404"
    
    Processed_sequences_synthetic_path = f"{base_path}/Postprocessed/processed_Sequences_synthetic.xlsx"
    Processed_sequences_natural_path = f"{base_path}/Postprocessed/processed_Sequences_natural.xlsx"
    
    # Load sequence data
    sequences_synthetic = pd.read_excel(Processed_sequences_synthetic_path)
    sequences_natural = pd.read_excel(Processed_sequences_natural_path)
    processed_sequences = pd.concat([sequences_synthetic, sequences_natural])
    
    print(f"Loaded {len(processed_sequences)} sequence abundance profiles")
    print(f"Number of species (ASVs): {len(processed_sequences.columns) - 1}")
    
    return processed_sequences

def load_coalescence_data():
    """Load coalescence experiment data"""
    print("Loading coalescence data...")
    
    base_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404"
    
    Coalescence_data_synthetic_path = f"{base_path}/Analyzed/processed_CoalescenceEvent_synthetic.xlsx"
    Coalescence_data_natural_path = f"{base_path}/Analyzed/processed_CoalescenceEvent_natural.xlsx"
    Meta_data_path = f"{base_path}/Postprocessed/Metadata.xlsx"
    
    # Load data
    Coalescence_data = pd.concat([
        pd.read_excel(Coalescence_data_synthetic_path),
        pd.read_excel(Coalescence_data_natural_path)
    ])
    
    Metadata = pd.read_excel(Meta_data_path)
    
    # Exception list
    exception_list = ['P4-02','P4-03','P4-23','P4-24','P7-97', 'P8-12'] + ['P8-91'] + \
                    ['P5-73', 'P5-69','P5-64','P5-61','P5-59', 'P5-56'] + ['P6-67']
    
    print(f"Loaded {len(Coalescence_data)} coalescence events")
    
    return Coalescence_data, Metadata, exception_list

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

def calculate_species_competitive_hierarchy(parent1_vector, parent2_vector, mixed_vector, threshold=1e-4):
    """
    Calculate species-level competitive hierarchy score using retention probabilities
    and vector similarities
    """
    # Calculate retention asymmetricity (core species hierarchy metric)
    retention_analysis = calculate_retention_asymmetricity_base(
        parent1_vector, parent2_vector, mixed_vector, 
        threshold=threshold, n_permutations=100, version=1
    )
    
    # Calculate vector similarities using VariousMetrics functions
    parent1_to_mixed_bc = vm.SimilarityBC(parent1_vector, mixed_vector, threshold)
    parent2_to_mixed_bc = vm.SimilarityBC(parent2_vector, mixed_vector, threshold)
    parent1_to_mixed_js = vm.SimilarityJS(parent1_vector, mixed_vector, threshold)
    parent2_to_mixed_js = vm.SimilarityJS(parent2_vector, mixed_vector, threshold)
    
    # Calculate which parent "wins" (higher similarity to offspring)
    bc_advantage = parent1_to_mixed_bc - parent2_to_mixed_bc  # > 0 means parent1 wins
    js_advantage = parent1_to_mixed_js - parent2_to_mixed_js
    
    # Calculate diversity measures for each community
    div1_richness = vm.Diversity1(parent1_vector, threshold)
    div2_richness = vm.Diversity1(parent2_vector, threshold)
    mixed_richness = vm.Diversity1(mixed_vector, threshold)
    
    div1_shannon = vm.Diversity2(parent1_vector, threshold)
    div2_shannon = vm.Diversity2(parent2_vector, threshold)
    mixed_shannon = vm.Diversity2(mixed_vector, threshold)
    
    # Calculate species dominance patterns
    parent1_dominant_species = np.argmax(parent1_vector)
    parent2_dominant_species = np.argmax(parent2_vector)
    mixed_dominant_species = np.argmax(mixed_vector)
    
    # Determine hierarchical outcome
    if abs(bc_advantage) > 0.1:  # Strong hierarchy
        hierarchy_strength = abs(bc_advantage)
        dominant_parent = 1 if bc_advantage > 0 else 2
    else:  # Weak hierarchy
        hierarchy_strength = abs(bc_advantage)
        dominant_parent = 0  # Coexistence
    
    return {
        'retention_asymmetricity': retention_analysis['asymmetricity'],
        'retention_p_value': retention_analysis['p_value'],
        'bc_advantage': bc_advantage,
        'js_advantage': js_advantage,
        'hierarchy_strength': hierarchy_strength,
        'dominant_parent': dominant_parent,
        'parent1_bc_sim': parent1_to_mixed_bc,
        'parent2_bc_sim': parent2_to_mixed_bc,
        'parent1_js_sim': parent1_to_mixed_js,
        'parent2_js_sim': parent2_to_mixed_js,
        'div1_richness': div1_richness,
        'div2_richness': div2_richness,
        'mixed_richness': mixed_richness,
        'div1_shannon': div1_shannon,
        'div2_shannon': div2_shannon,
        'mixed_shannon': mixed_shannon,
        'parent1_dominant_species': parent1_dominant_species,
        'parent2_dominant_species': parent2_dominant_species,
        'mixed_dominant_species': mixed_dominant_species,
        'retention_rates': retention_analysis['retention_rates']
    }

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

def calculate_species_hierarchy_matrix(Coalescence_data, processed_sequences, Coal_IDX_list, threshold=1e-4):
    """
    Calculate species-level hierarchy matrix for all coalescence events
    """
    hierarchy_results = []
    
    print(f"Processing {len(Coal_IDX_list)} coalescence events...")
    
    for i, coal_sample_id in enumerate(Coal_IDX_list):
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
        
        if (parent1_vector is not None and parent2_vector is not None and 
            mixed_vector is not None):
            
            # Calculate species hierarchy metrics
            hierarchy_metrics = calculate_species_competitive_hierarchy(
                parent1_vector, parent2_vector, mixed_vector, threshold
            )
            
            # Add sample identifiers
            hierarchy_metrics.update({
                'coalescence_id': coal_sample_id,
                'parent1_id': parent1_id,
                'parent2_id': parent2_id,
                'event_index': i
            })
            
            hierarchy_results.append(hierarchy_metrics)
    
    print(f"Successfully processed {len(hierarchy_results)} coalescence events")
    
    return hierarchy_results

def plot_species_hierarchy_summary(hierarchy_results, condition_name, save_path):
    """
    Plot summary of species-level hierarchy analysis
    """
    if not hierarchy_results:
        print(f"No results to plot for {condition_name}")
        return
    
    # Convert to DataFrame for easier plotting
    df = pd.DataFrame(hierarchy_results)
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Plot 1: Hierarchy strength distribution
    axes[0, 0].hist(df['hierarchy_strength'], bins=20, alpha=0.7, edgecolor='black')
    axes[0, 0].set_xlabel('Hierarchy Strength')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Distribution of Hierarchy Strength')
    
    # Plot 2: BC Advantage vs Retention Asymmetricity
    axes[0, 1].scatter(df['bc_advantage'], df['retention_asymmetricity'], alpha=0.6)
    axes[0, 1].set_xlabel('BC Similarity Advantage (Parent1 - Parent2)')
    axes[0, 1].set_ylabel('Retention Asymmetricity')
    axes[0, 1].set_title('Vector vs Retention Asymmetricity')
    axes[0, 1].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[0, 1].axvline(x=0, color='red', linestyle='--', alpha=0.5)
    
    # Plot 3: Parent similarity comparison
    axes[0, 2].scatter(df['parent1_bc_sim'], df['parent2_bc_sim'], alpha=0.6)
    axes[0, 2].set_xlabel('Parent 1 BC Similarity to Offspring')
    axes[0, 2].set_ylabel('Parent 2 BC Similarity to Offspring')
    axes[0, 2].set_title('Parent Similarities to Offspring')
    # Add diagonal line for equal similarity
    lims = [0, max(axes[0, 2].get_xlim()[1], axes[0, 2].get_ylim()[1])]
    axes[0, 2].plot(lims, lims, 'r--', alpha=0.5)
    
    # Plot 4: Diversity retention analysis
    div_retention = []
    for _, row in df.iterrows():
        initial_div = (row['div1_shannon'] + row['div2_shannon']) / 2
        final_div = row['mixed_shannon']
        if initial_div > 0:
            retention_ratio = final_div / initial_div
            div_retention.append(retention_ratio)
    
    if div_retention:
        axes[1, 0].hist(div_retention, bins=20, alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Diversity Retention Ratio (Final/Initial)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Shannon Diversity Retention')
        axes[1, 0].axvline(x=1, color='red', linestyle='--', alpha=0.5, label='No Change')
        axes[1, 0].legend()
    
    # Plot 5: Dominant parent outcomes
    dominant_counts = df['dominant_parent'].value_counts().sort_index()
    labels = ['Coexistence', 'Parent 1 Wins', 'Parent 2 Wins']
    colors = ['green', 'blue', 'orange']
    
    # Ensure we have data for all categories
    plot_values = []
    plot_labels = []
    plot_colors = []
    for i in range(3):
        if i in dominant_counts.index:
            plot_values.append(dominant_counts[i])
            plot_labels.append(labels[i])
            plot_colors.append(colors[i])
    
    if plot_values:
        axes[1, 1].pie(plot_values, labels=plot_labels, colors=plot_colors, autopct='%1.1f%%')
        axes[1, 1].set_title('Competitive Outcomes')
    
    # Plot 6: Hierarchy strength vs p-value
    valid_pvals = df['retention_p_value'].dropna()
    valid_hierarchy = df.loc[valid_pvals.index, 'hierarchy_strength']
    
    if len(valid_pvals) > 0:
        axes[1, 2].scatter(valid_hierarchy, valid_pvals, alpha=0.6)
        axes[1, 2].set_xlabel('Hierarchy Strength')
        axes[1, 2].set_ylabel('Retention Asymmetricity P-value')
        axes[1, 2].set_title('Hierarchy vs Statistical Significance')
        axes[1, 2].axhline(y=0.05, color='red', linestyle='--', alpha=0.5, label='p=0.05')
        axes[1, 2].legend()
    
    plt.suptitle(f'Species-Level Hierarchy Analysis: {condition_name}', fontsize=16)
    plt.tight_layout()
    
    # Save plot
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary statistics
    print(f"\n=== Species Hierarchy Summary for {condition_name} ===")
    print(f"Number of coalescence events: {len(df)}")
    print(f"Mean hierarchy strength: {df['hierarchy_strength'].mean():.3f} ± {df['hierarchy_strength'].std():.3f}")
    print(f"Mean retention asymmetricity: {df['retention_asymmetricity'].mean():.3f} ± {df['retention_asymmetricity'].std():.3f}")
    
    if len(valid_pvals) > 0:
        significant_events = np.sum(valid_pvals < 0.05)
        print(f"Statistically significant events: {significant_events}/{len(valid_pvals)} ({100*significant_events/len(valid_pvals):.1f}%)")
    
    # Competitive outcomes
    total_events = len(df)
    if total_events > 0:
        coexist_pct = 100 * (dominant_counts.get(0, 0) / total_events)
        parent1_pct = 100 * (dominant_counts.get(1, 0) / total_events)
        parent2_pct = 100 * (dominant_counts.get(2, 0) / total_events)
        print(f"Outcomes: Coexistence {coexist_pct:.1f}%, Parent1 wins {parent1_pct:.1f}%, Parent2 wins {parent2_pct:.1f}%")

def analyze_species_hierarchy_comprehensive(Coalescence_data, Metadata, processed_sequences, exception_list):
    """
    Comprehensive species-level hierarchy analysis across conditions
    """
    print("Starting comprehensive species-level hierarchy analysis...")
    
    # Test conditions
    conditions = [
        ('Natural LN', 'N', 'L', 0),
        ('Natural MN', 'N', 'M', 0),
        ('Natural HN', 'N', 'H', 0),
        ('Synthetic LN-12', 'S', 'L', 12),
        ('Synthetic MN-12', 'S', 'M', 12),
        ('Synthetic HN-12', 'S', 'H', 12),
        ('Synthetic HN-6', 'S', 'H', 6),
        ('Synthetic HN-24', 'S', 'H', 24),
    ]
    
    all_condition_results = {}
    summary_stats = []
    
    for condition_name, com_type, medium, species_num in conditions:
        print(f"\nProcessing condition: {condition_name}")
        
        # Get coalescence events for this condition
        Coal_IDX_list = Community_PermutateList("F", com_type, medium, "C", Metadata, 
                                               species_num, -1, exception_list)
        
        if len(Coal_IDX_list) < 3:
            print(f"  Insufficient data for {condition_name} (n={len(Coal_IDX_list)})")
            continue
        
        # Calculate hierarchy metrics
        hierarchy_results = calculate_species_hierarchy_matrix(
            Coalescence_data, processed_sequences, Coal_IDX_list
        )
        
        if hierarchy_results:
            all_condition_results[condition_name] = hierarchy_results
            
            # Calculate summary statistics
            df = pd.DataFrame(hierarchy_results)
            summary_stats.append({
                'Condition': condition_name,
                'CommunityType': com_type,
                'Medium': medium,
                'SpeciesNum': species_num,
                'N_Events': len(hierarchy_results),
                'Mean_HierarchyStrength': df['hierarchy_strength'].mean(),
                'Std_HierarchyStrength': df['hierarchy_strength'].std(),
                'Mean_RetentionAsymmetricity': df['retention_asymmetricity'].mean(),
                'Std_RetentionAsymmetricity': df['retention_asymmetricity'].std(),
                'Mean_BC_Advantage': df['bc_advantage'].mean(),
                'Fraction_Parent1_Wins': (df['dominant_parent'] == 1).mean(),
                'Fraction_Parent2_Wins': (df['dominant_parent'] == 2).mean(),
                'Fraction_Coexistence': (df['dominant_parent'] == 0).mean(),
                'Mean_P_Value': df['retention_p_value'].mean(),
                'Fraction_Significant': (df['retention_p_value'] < 0.05).mean()
            })
            
            # Generate individual condition plot
            plot_path = os.path.join(output_dir, f"Species_Hierarchy_{condition_name.replace(' ', '_').replace('-', '_')}.png")
            plot_species_hierarchy_summary(hierarchy_results, condition_name, plot_path)
    
    # Save comprehensive results
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv(os.path.join(output_dir, "species_hierarchy_comprehensive_summary.csv"), index=False)
    
    # Print overall comparison
    print("\n" + "="*80)
    print("SPECIES-LEVEL HIERARCHY COMPARISON ACROSS CONDITIONS")
    print("="*80)
    print(summary_df.to_string(index=False))
    
    return all_condition_results, summary_df

def main():
    """Main function to run species hierarchy analysis"""
    print("Starting Species-Level Hierarchy Analysis...")
    
    # Load data
    processed_sequences = load_sequence_data()
    Coalescence_data, Metadata, exception_list = load_coalescence_data()
    
    # Run comprehensive analysis
    print("\nRunning comprehensive species hierarchy analysis...")
    condition_results, summary_df = analyze_species_hierarchy_comprehensive(
        Coalescence_data, Metadata, processed_sequences, exception_list
    )
    
    # Create comparison plot across conditions
    if not summary_df.empty:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Hierarchy strength comparison
        natural_data = summary_df[summary_df['CommunityType'] == 'N']
        synthetic_data = summary_df[summary_df['CommunityType'] == 'S']
        
        if not natural_data.empty and not synthetic_data.empty:
            # Plot 1: Hierarchy strength by medium (Natural vs Synthetic)
            x_pos = np.arange(len(natural_data))
            width = 0.35
            
            axes[0, 0].bar(x_pos - width/2, natural_data['Mean_HierarchyStrength'], width, 
                          label='Natural', alpha=0.8, yerr=natural_data['Std_HierarchyStrength'])
            axes[0, 0].bar(x_pos + width/2, synthetic_data['Mean_HierarchyStrength'][:len(natural_data)], width,
                          label='Synthetic', alpha=0.8, yerr=synthetic_data['Std_HierarchyStrength'][:len(natural_data)])
            axes[0, 0].set_xlabel('Medium')
            axes[0, 0].set_ylabel('Hierarchy Strength')
            axes[0, 0].set_title('Hierarchy Strength: Natural vs Synthetic')
            axes[0, 0].set_xticks(x_pos)
            axes[0, 0].set_xticklabels(natural_data['Medium'])
            axes[0, 0].legend()
        
        # Plot 2: Competitive outcomes by condition
        conditions = summary_df['Condition'].tolist()
        coexist_fractions = summary_df['Fraction_Coexistence'].tolist()
        parent1_fractions = summary_df['Fraction_Parent1_Wins'].tolist()
        parent2_fractions = summary_df['Fraction_Parent2_Wins'].tolist()
        
        x_pos = np.arange(len(conditions))
        
        axes[0, 1].bar(x_pos, coexist_fractions, label='Coexistence', alpha=0.8)
        axes[0, 1].bar(x_pos, parent1_fractions, bottom=coexist_fractions, label='Parent 1 Wins', alpha=0.8)
        axes[0, 1].bar(x_pos, parent2_fractions, 
                      bottom=np.array(coexist_fractions) + np.array(parent1_fractions), 
                      label='Parent 2 Wins', alpha=0.8)
        axes[0, 1].set_xlabel('Condition')
        axes[0, 1].set_ylabel('Fraction of Events')
        axes[0, 1].set_title('Competitive Outcomes by Condition')
        axes[0, 1].set_xticks(x_pos)
        axes[0, 1].set_xticklabels(conditions, rotation=45, ha='right')
        axes[0, 1].legend()
        
        # Plot 3: Retention asymmetricity vs hierarchy strength
        axes[1, 0].scatter(summary_df['Mean_HierarchyStrength'], summary_df['Mean_RetentionAsymmetricity'])
        for i, condition in enumerate(summary_df['Condition']):
            axes[1, 0].annotate(condition, 
                               (summary_df['Mean_HierarchyStrength'].iloc[i], 
                                summary_df['Mean_RetentionAsymmetricity'].iloc[i]), 
                               fontsize=8, alpha=0.7)
        axes[1, 0].set_xlabel('Mean Hierarchy Strength')
        axes[1, 0].set_ylabel('Mean Retention Asymmetricity')
        axes[1, 0].set_title('Hierarchy Strength vs Retention Asymmetricity')
        
        # Plot 4: Statistical significance by condition
        axes[1, 1].bar(x_pos, summary_df['Fraction_Significant'])
        axes[1, 1].set_xlabel('Condition')
        axes[1, 1].set_ylabel('Fraction of Significant Events')
        axes[1, 1].set_title('Statistical Significance of Species Hierarchy')
        axes[1, 1].set_xticks(x_pos)
        axes[1, 1].set_xticklabels(conditions, rotation=45, ha='right')
        axes[1, 1].axhline(y=0.05, color='red', linestyle='--', alpha=0.5, label='Expected by chance')
        axes[1, 1].legend()
        
        plt.suptitle('Species-Level Hierarchy Analysis: Cross-Condition Comparison', fontsize=16)
        plt.tight_layout()
        
        comparison_path = os.path.join(output_dir, "Species_Hierarchy_Cross_Condition_Comparison.png")
        plt.savefig(comparison_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    print(f"\nSpecies hierarchy analysis complete!")
    print(f"Results saved to: {output_dir}")
    print("Files created:")
    print("  - species_hierarchy_comprehensive_summary.csv")
    print("  - Individual condition plots: Species_Hierarchy_[Condition].png")
    print("  - Cross-condition comparison: Species_Hierarchy_Cross_Condition_Comparison.png")

if __name__ == "__main__":
    main()