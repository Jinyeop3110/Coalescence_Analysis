#!/usr/bin/env python3
"""
Simple Final Day Community Plotter (Minimal Dependencies)
==========================================================

A simplified version that creates CSV data files and basic plots for final day 
community compositions, designed to work with the existing environment constraints.
"""

import os
import sys
import numpy as np
import pandas as pd

def load_data_simple():
    """Load data using direct file paths to avoid matplotlib import issues."""
    try:
        # Load files directly
        coalescence_synthetic_path = "../../Analyzed/processed_CoalescenceEvent_synthetic.xlsx"
        coalescence_natural_path = "../../Analyzed/processed_CoalescenceEvent_natural.xlsx"
        sequences_synthetic_path = "../../Postprocessed/processed_Sequences_synthetic.xlsx"
        sequences_natural_path = "../../Postprocessed/processed_Sequences_natural.xlsx"
        
        # Load coalescence data
        coalescence_synthetic = pd.read_excel(coalescence_synthetic_path)
        coalescence_natural = pd.read_excel(coalescence_natural_path)
        coalescence_data = pd.concat([coalescence_synthetic, coalescence_natural])
        
        # Load sequence data
        sequences_synthetic = pd.read_excel(sequences_synthetic_path)
        sequences_natural = pd.read_excel(sequences_natural_path)
        processed_sequences = pd.concat([sequences_synthetic, sequences_natural])
        
        print(f"Loaded {len(coalescence_data)} coalescence experiments")
        print(f"Loaded {len(processed_sequences)} sequence samples")
        
        return coalescence_data, processed_sequences
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def get_abundance_vector(processed_sequences, sample_id):
    """Extract abundance vector for a given sample ID."""
    sample_rows = processed_sequences[processed_sequences['SampleIDX'] == sample_id]
    if sample_rows.empty:
        return None
    
    # Get abundance values (skip SampleIDX column)
    abundance_vector = sample_rows.iloc[0, 1:].values.astype(float)
    abundance_vector = np.nan_to_num(abundance_vector, 0)
    
    # Normalize to sum to 1
    if abundance_vector.sum() > 0:
        abundance_vector = abundance_vector / abundance_vector.sum()
    
    return abundance_vector

def analyze_coalescence_experiments():
    """Analyze all coalescence experiments and create data summaries."""
    print("Loading coalescence data...")
    coalescence_data, processed_sequences = load_data_simple()
    
    if coalescence_data is None or processed_sequences is None:
        print("Failed to load data. Exiting.")
        return
    
    # Create output directory
    output_dir = "Figure/FinalDayAnalysis"
    os.makedirs(output_dir, exist_ok=True)
    
    # Collect experiment data
    experiment_results = []
    
    print("Processing experiments...")
    for idx, row in coalescence_data.iterrows():
        try:
            # Extract basic info
            medium = row.get('Medium', '')
            species_pool = row.get('SpeciesPool', 'unknown')
            
            # Map medium to nutrient condition
            medium_mapping = {'L': 'LN', 'M': 'MN', 'H': 'HN'}
            nutrient_condition = medium_mapping.get(medium, medium)
            
            # Get sample IDs
            mixture_sample_id = row['SampleIDX']
            parent1_sample_id = row['SampleIDX_Sub1']
            parent2_sample_id = row['SampleIDX_Sub2']
            
            # Get abundance vectors
            mixture_vector = get_abundance_vector(processed_sequences, mixture_sample_id)
            parent1_vector = get_abundance_vector(processed_sequences, parent1_sample_id)
            parent2_vector = get_abundance_vector(processed_sequences, parent2_sample_id)
            
            if mixture_vector is None or parent1_vector is None or parent2_vector is None:
                print(f"Missing data for: {mixture_sample_id}")
                continue
            
            # Determine data type
            data_type = 'synthetic' if 'P' in mixture_sample_id else 'natural'
            
            # Calculate some basic metrics
            parent1_richness = np.sum(parent1_vector > 0)
            parent2_richness = np.sum(parent2_vector > 0)  
            mixture_richness = np.sum(mixture_vector > 0)
            
            # Store results
            result = {
                'mixture_id': mixture_sample_id,
                'parent1_id': parent1_sample_id,
                'parent2_id': parent2_sample_id,
                'nutrient_condition': nutrient_condition,
                'species_pool': species_pool,
                'data_type': data_type,
                'parent1_richness': parent1_richness,
                'parent2_richness': parent2_richness,
                'mixture_richness': mixture_richness,
                'parent1_vector': parent1_vector,
                'parent2_vector': parent2_vector,
                'mixture_vector': mixture_vector
            }
            experiment_results.append(result)
            
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue
    
    print(f"Successfully processed {len(experiment_results)} experiments")
    
    # Create summary DataFrame
    summary_data = []
    for result in experiment_results:
        summary_data.append({
            'mixture_id': result['mixture_id'],
            'parent1_id': result['parent1_id'],
            'parent2_id': result['parent2_id'],
            'nutrient_condition': result['nutrient_condition'],
            'species_pool': result['species_pool'],
            'data_type': result['data_type'],
            'parent1_richness': result['parent1_richness'],
            'parent2_richness': result['parent2_richness'],
            'mixture_richness': result['mixture_richness']
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_path = os.path.join(output_dir, "experiment_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"Saved summary to: {summary_path}")
    
    # Group by condition and create detailed data files
    conditions = summary_df.groupby(['nutrient_condition', 'species_pool', 'data_type'])
    
    for (nutrient, pool, dtype), group in conditions:
        condition_name = f"{nutrient}_{pool}_{dtype}"
        condition_dir = os.path.join(output_dir, condition_name)
        os.makedirs(condition_dir, exist_ok=True)
        
        print(f"Processing condition: {condition_name} ({len(group)} experiments)")
        
        # Save detailed abundance data for this condition
        abundance_data = []
        
        for _, exp_summary in group.iterrows():
            # Find the corresponding result
            exp_result = next(r for r in experiment_results if r['mixture_id'] == exp_summary['mixture_id'])
            
            # Create abundance records
            for asv_idx in range(len(exp_result['parent1_vector'])):
                abundance_data.append({
                    'mixture_id': exp_result['mixture_id'],
                    'sample_type': 'parent1',
                    'sample_id': exp_result['parent1_id'],
                    'asv_idx': asv_idx + 1,
                    'abundance': exp_result['parent1_vector'][asv_idx]
                })
                abundance_data.append({
                    'mixture_id': exp_result['mixture_id'],
                    'sample_type': 'parent2', 
                    'sample_id': exp_result['parent2_id'],
                    'asv_idx': asv_idx + 1,
                    'abundance': exp_result['parent2_vector'][asv_idx]
                })
                abundance_data.append({
                    'mixture_id': exp_result['mixture_id'],
                    'sample_type': 'offspring',
                    'sample_id': exp_result['mixture_id'],
                    'asv_idx': asv_idx + 1,
                    'abundance': exp_result['mixture_vector'][asv_idx]
                })
        
        # Save abundance data
        abundance_df = pd.DataFrame(abundance_data)
        abundance_path = os.path.join(condition_dir, "abundance_data.csv")
        abundance_df.to_csv(abundance_path, index=False)
        
        # Save condition summary
        condition_summary_path = os.path.join(condition_dir, "condition_summary.csv")
        group.to_csv(condition_summary_path, index=False)
        
        print(f"  Saved {len(abundance_data)} abundance records")
    
    print(f"\nAll data saved to: {output_dir}")
    
    # Print summary statistics
    print("\nSUMMARY STATISTICS:")
    print("===================")
    condition_counts = summary_df.groupby(['nutrient_condition', 'data_type']).size()
    for (nutrient, dtype), count in condition_counts.items():
        print(f"{nutrient} {dtype}: {count} experiments")
    
    print(f"\nRichness statistics:")
    print(f"Parent1 richness: {summary_df['parent1_richness'].mean():.1f} ± {summary_df['parent1_richness'].std():.1f}")
    print(f"Parent2 richness: {summary_df['parent2_richness'].mean():.1f} ± {summary_df['parent2_richness'].std():.1f}")
    print(f"Mixture richness: {summary_df['mixture_richness'].mean():.1f} ± {summary_df['mixture_richness'].std():.1f}")

def create_simple_plot_script():
    """Create a simple R or Python plotting script that can be run separately."""
    script_content = """
# Simple plotting script for final day community data
# Run this after plot_final_day_simple.py generates the data files

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def create_simple_bar_plots():
    output_dir = "Figure/FinalDayAnalysis"
    
    # Read experiment summary
    summary_df = pd.read_csv(os.path.join(output_dir, "experiment_summary.csv"))
    
    # Create richness comparison plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot richness by condition
    conditions = summary_df['nutrient_condition'].unique()
    
    for i, richness_type in enumerate(['parent1_richness', 'parent2_richness', 'mixture_richness']):
        ax = axes[i]
        means = []
        stds = []
        
        for condition in conditions:
            data = summary_df[summary_df['nutrient_condition'] == condition][richness_type]
            means.append(data.mean())
            stds.append(data.std())
        
        ax.bar(conditions, means, yerr=stds, capsize=5)
        ax.set_title(richness_type.replace('_', ' ').title())
        ax.set_ylabel('Species Richness')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "richness_comparison.png"), dpi=300)
    print("Created richness comparison plot")

if __name__ == "__main__":
    create_simple_bar_plots()
"""
    
    script_path = "Figure/FinalDayAnalysis/create_plots.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"Created plotting script: {script_path}")
    print("Run this script separately to create plots once matplotlib issues are resolved.")

def main():
    """Main function."""
    print("Final Day Community Analysis")
    print("============================")
    
    analyze_coalescence_experiments()
    create_simple_plot_script()
    
    print("\nDone! Data files created for further analysis and plotting.")

if __name__ == "__main__":
    main()