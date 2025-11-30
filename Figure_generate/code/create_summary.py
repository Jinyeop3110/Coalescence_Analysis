#!/usr/bin/env python3
"""
Create the missing experiment_summary.csv file
"""

from common_setup import *
import pandas as pd
import numpy as np
import os

def get_abundance_vector(sample_id):
    """Extract abundance vector for a given sample ID."""
    # Check both synthetic and natural data
    sample_rows_syn = Processed_sequences_synthetic[Processed_sequences_synthetic['SampleIDX'] == sample_id]
    sample_rows_nat = Processed_sequences_natural[Processed_sequences_natural['SampleIDX'] == sample_id]
    
    sample_rows = pd.concat([sample_rows_syn, sample_rows_nat])
    
    if sample_rows.empty:
        return None
    
    # Get abundance values (columns 1-43, skipping SampleIDX)
    abundance_vector = sample_rows.iloc[0, 1:44].values.astype(float)
    abundance_vector = np.nan_to_num(abundance_vector, 0)
    
    # Normalize
    if abundance_vector.sum() > 0:
        abundance_vector = abundance_vector / abundance_vector.sum()
    
    return abundance_vector

def main():
    # Create output directory
    os.makedirs('Figure/FinalDayAnalysis', exist_ok=True)
    
    print('Creating experiment summary from coalescence data...')
    
    experiment_data = []
    
    # Process coalescence data
    for _, row in Coalescence_data.iterrows():
        if pd.notna(row['SampleIDX']) and pd.notna(row['SampleIDX_Sub1']) and pd.notna(row['SampleIDX_Sub2']):
            
            # Get richness information  
            parent1_vector = get_abundance_vector(row['SampleIDX_Sub1'])
            parent2_vector = get_abundance_vector(row['SampleIDX_Sub2'])
            mixture_vector = get_abundance_vector(row['SampleIDX'])
            
            parent1_richness = np.sum(parent1_vector > 0.001) if parent1_vector is not None else 0
            parent2_richness = np.sum(parent2_vector > 0.001) if parent2_vector is not None else 0
            mixture_richness = np.sum(mixture_vector > 0.001) if mixture_vector is not None else 0
            
            # Extract nutrient condition
            sample_id = row['SampleIDX']
            if 'HN' in sample_id:
                nutrient_condition = 'HN'
            elif 'MN' in sample_id:
                nutrient_condition = 'MN'
            elif 'LN' in sample_id:
                nutrient_condition = 'LN'
            else:
                nutrient_condition = 'LN'  # Default for synthetic data
            
            species_pool = row.get('SpeciesPool', 'unknown')
            
            experiment_data.append({
                'mixture_id': row['SampleIDX'],
                'parent1_id': row['SampleIDX_Sub1'], 
                'parent2_id': row['SampleIDX_Sub2'],
                'nutrient_condition': nutrient_condition,
                'species_pool': species_pool,
                'data_type': 'synthetic',
                'parent1_richness': parent1_richness,
                'parent2_richness': parent2_richness,
                'mixture_richness': mixture_richness
            })
    
    # Create DataFrame and save
    summary_df = pd.DataFrame(experiment_data)
    summary_path = 'Figure/FinalDayAnalysis/experiment_summary.csv'
    summary_df.to_csv(summary_path, index=False)
    
    print(f'SUCCESS: Created {len(summary_df)} experiments')
    print(f'Saved to: {summary_path}')
    print('Nutrient conditions:', summary_df['nutrient_condition'].value_counts().to_dict())

if __name__ == '__main__':
    main()