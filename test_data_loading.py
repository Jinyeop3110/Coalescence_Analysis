#!/usr/bin/env python3
"""
Test the data loading function without matplotlib dependencies
"""

import numpy as np
import pandas as pd
import sys
import os

def load_real_coalescence_data():
    """
    Load real experimental coalescence data using the existing common_setup infrastructure.
    
    Returns:
        Tuple of (offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers)
    """
    # Import existing data from common_setup
    from common_setup import Coalescence_data
    
    # Load processed sequences data directly (contains actual ASV abundance data)
    Processed_sequences_synthetic_path ="../../Postprocessed/processed_Sequences_synthetic.xlsx"
    Processed_sequences_natural_path ="../../Postprocessed/processed_Sequences_natural.xlsx"
    
    sequences_synthetic = pd.read_excel(Processed_sequences_synthetic_path)
    sequences_natural = pd.read_excel(Processed_sequences_natural_path)
    processed_sequences = pd.concat([sequences_synthetic, sequences_natural])
    
    offspring_list = []
    parent1_list = []
    parent2_list = []
    nutrient_conditions = []
    species_numbers = []
    
    print("Loading real coalescence data using processed sequences...")
    print(f"Coalescence data shape: {Coalescence_data.shape}")
    print(f"Processed sequences shape: {processed_sequences.shape}")
    print(f"Processed sequences columns: {list(processed_sequences.columns[:10])}...")  # Show first 10 columns
    
    # Iterate through coalescence data and get abundance vectors from processed sequences
    processed_events = 0
    skipped_events = 0
    
    for _, row in Coalescence_data.iterrows():
        try:
            # Get medium and convert to our format
            medium = row['Medium']
            nutrient_mapping = {'L': 'LN', 'M': 'MN', 'H': 'HN'}
            nutrient_condition = nutrient_mapping.get(medium)
            
            if nutrient_condition is None:
                skipped_events += 1
                continue
            
            # Get sample IDs
            mixture_sample_id = row['SampleIDX']
            parent1_sample_id = row['SampleIDX_Sub1']
            parent2_sample_id = row['SampleIDX_Sub2']
            
            # Find corresponding rows in processed sequences data (contains actual abundances)
            mixture_rows = processed_sequences[processed_sequences['SampleIDX'] == mixture_sample_id]
            parent1_rows = processed_sequences[processed_sequences['SampleIDX'] == parent1_sample_id]
            parent2_rows = processed_sequences[processed_sequences['SampleIDX'] == parent2_sample_id]
            
            # Skip if any data is missing
            if mixture_rows.empty or parent1_rows.empty or parent2_rows.empty:
                skipped_events += 1
                continue
                
            # Check if DataFrames have enough columns (SampleIDX + at least 1 species column)
            if (len(mixture_rows.columns) < 2 or 
                len(parent1_rows.columns) < 2 or 
                len(parent2_rows.columns) < 2):
                skipped_events += 1
                continue
            
            # Extract community vectors (columns 1 onwards, since column 0 is SampleIDX)
            mixture_vector = mixture_rows.iloc[0, 1:].values.astype(float)
            parent1_vector = parent1_rows.iloc[0, 1:].values.astype(float)
            parent2_vector = parent2_rows.iloc[0, 1:].values.astype(float)
            
            # Clean and normalize
            mixture_vector = np.nan_to_num(mixture_vector, 0)
            parent1_vector = np.nan_to_num(parent1_vector, 0)
            parent2_vector = np.nan_to_num(parent2_vector, 0)
            
            # Apply threshold and normalize as in the notebook
            threshold = 1e-4
            mixture_vector = mixture_vector * (mixture_vector > threshold)
            parent1_vector = parent1_vector * (parent1_vector > threshold)
            parent2_vector = parent2_vector * (parent2_vector > threshold)
            
            # Normalize
            if np.sum(mixture_vector) > 0:
                mixture_vector = mixture_vector / np.sum(mixture_vector)
            if np.sum(parent1_vector) > 0:
                parent1_vector = parent1_vector / np.sum(parent1_vector)
            if np.sum(parent2_vector) > 0:
                parent2_vector = parent2_vector / np.sum(parent2_vector)
            
            # Count final observed species (for validation)
            n_observed_species = np.sum(mixture_vector > 0)
            
            # Get experimental design species pool number from CommunityIDX
            # This applies only to synthetic coalescence data (CommunityOrigin == 'S')
            experimental_species_pool = None
            if row['CommunityOrigin'] == 'S' and row['CoalescenceType'] == 'C':
                community_idx = row['CommunityIDX']
                # Apply mapping from common_setup.py:
                # species_pool_num == 6: communityIDX <= 14
                # species_pool_num == 12: communityIDX > 14 & <= 41  
                # species_pool_num == 24: communityIDX > 41 & <= 47
                if community_idx <= 14:
                    experimental_species_pool = 6
                elif community_idx <= 41:
                    experimental_species_pool = 12
                elif community_idx <= 47:
                    experimental_species_pool = 24
            
            # Include valid samples with minimum diversity threshold
            if (n_observed_species >= 3 and 
                np.sum(mixture_vector) > 0 and 
                np.sum(parent1_vector) > 0 and 
                np.sum(parent2_vector) > 0):
                
                offspring_list.append(mixture_vector)
                parent1_list.append(parent1_vector)
                parent2_list.append(parent2_vector)
                nutrient_conditions.append(nutrient_condition)
                # Use experimental species pool number if available
                species_numbers.append(experimental_species_pool if experimental_species_pool is not None else n_observed_species)
                processed_events += 1
            else:
                skipped_events += 1
        
        except Exception as e:
            print(f"Error processing row: {e}")
            skipped_events += 1
            continue
    
    print(f"Successfully loaded {processed_events} coalescence events")
    print(f"Skipped {skipped_events} events due to missing/invalid data")
    
    if len(offspring_list) > 0:
        print(f"Nutrient distribution: LN={nutrient_conditions.count('LN')}, MN={nutrient_conditions.count('MN')}, HN={nutrient_conditions.count('HN')}")
        print(f"Species range: {min(species_numbers)} - {max(species_numbers)}")
    
    return offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers

if __name__ == "__main__":
    try:
        offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers = load_real_coalescence_data()
        print(f"\nData loading successful!")
        print(f"Total events loaded: {len(offspring_list)}")
        
        if len(offspring_list) > 0:
            print(f"Sample vector length: {len(offspring_list[0])}")
            print(f"First few species numbers: {species_numbers[:10]}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()