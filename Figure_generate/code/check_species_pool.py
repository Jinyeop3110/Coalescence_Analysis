#!/usr/bin/env python3
"""Check which ASVs are actually in each species pool"""

import pandas as pd
import numpy as np

# Load metadata to understand species pool setup
metadata_path = '/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Postprocessed/Metadata.xlsx'
sequences_path = '/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Postprocessed/processed_Sequences_synthetic.xlsx'

metadata = pd.read_excel(metadata_path)
sequences = pd.read_excel(sequences_path)

# Check samples for different species pools
pools = {
    '6-species': (1, 9),
    '12-species': (10, 18),
    '24-species': (19, 30)
}

asv_cols = [col for col in sequences.columns if col != 'SampleIDX']

for pool_name, (start_idx, end_idx) in pools.items():
    pool_samples = metadata[(metadata['CommunityOrigin'] == 'S') & 
                           (metadata['CommunityIDX'].astype(int) >= start_idx) & 
                           (metadata['CommunityIDX'].astype(int) <= end_idx) &
                           (metadata['CoalescenceType'] == 'S')]
    
    print(f'\n{pool_name} pool analysis:')
    print(f'Number of samples: {len(pool_samples)}')
    
    # Collect all ASVs that appear in this pool
    all_asvs_in_pool = set()
    
    for sample_id in pool_samples['SampleIDX'].tolist():
        sample_data = sequences[sequences['SampleIDX'] == sample_id]
        if not sample_data.empty:
            abundances = sample_data[asv_cols].iloc[0]
            present_asvs = abundances[abundances > 0.01].index.tolist()
            all_asvs_in_pool.update(present_asvs)
    
    # Extract ASV numbers and sort
    asv_numbers = []
    for asv in all_asvs_in_pool:
        try:
            num = int(asv.replace('NormalizedAbundance', ''))
            asv_numbers.append(num)
        except:
            pass
    
    asv_numbers = sorted(asv_numbers)
    print(f'ASVs present in {pool_name} pool: {asv_numbers}')
    print(f'Total unique ASVs: {len(asv_numbers)}')
    
    # Show some example samples
    print(f'\nExample samples from {pool_name} pool:')
    for i, (idx, row) in enumerate(pool_samples.head(3).iterrows()):
        sample_id = row['SampleIDX']
        sample_data = sequences[sequences['SampleIDX'] == sample_id]
        if not sample_data.empty:
            abundances = sample_data[asv_cols].iloc[0]
            present_asvs = abundances[abundances > 0.01]
            asv_nums = [int(col.replace('NormalizedAbundance', '')) for col in present_asvs.index]
            print(f'  {sample_id}: ASVs {sorted(asv_nums)}')