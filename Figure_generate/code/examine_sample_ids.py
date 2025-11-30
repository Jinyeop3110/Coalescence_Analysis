#!/usr/bin/env python3
"""
Examine SampleIDX patterns to identify richness levels
"""

import pandas as pd
import re

def examine_sample_patterns():
    """Examine SampleIDX patterns"""
    
    # Load abundance data
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    # Load pH data
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    ph_data = communities_data[['SampleIDX', 'fieldPH1', 'fieldPH7']].copy()
    
    # Merge data
    merged_data = abundance_data.merge(ph_data, on='SampleIDX', how='inner')
    
    print("SAMPLE ID PATTERNS")
    print("=" * 30)
    
    # Show first 20 sample IDs
    sample_ids = merged_data['SampleIDX'].astype(str).tolist()
    print("First 20 Sample IDs:")
    for i, sid in enumerate(sample_ids[:20], 1):
        print(f"  {i:2d}. {sid}")
    
    # Look for various patterns
    patterns_to_check = [
        r's(\d+)',     # s6, s12, s24
        r'S(\d+)',     # S6, S12, S24
        r'(\d+)s',     # 6s, 12s, 24s
        r'rich(\d+)',  # rich6, rich12, rich24
        r'r(\d+)',     # r6, r12, r24
        r'pool(\d+)',  # pool6, pool12, pool24
        r'_(\d+)_',    # _6_, _12_, _24_
        r'-(\d+)-',    # -6-, -12-, -24-
    ]
    
    print("\nPattern Analysis:")
    for pattern in patterns_to_check:
        matches = merged_data['SampleIDX'].astype(str).str.extract(pattern, expand=False)
        unique_matches = matches.dropna().unique()
        if len(unique_matches) > 0:
            print(f"\nPattern '{pattern}' found:")
            print(f"  Unique values: {sorted(unique_matches)}")
            print(f"  Counts: {matches.value_counts().sort_index().to_dict()}")
    
    # Check if there are any numeric patterns
    print("\nAll unique numeric substrings in SampleIDX:")
    all_numbers = set()
    for sid in sample_ids:
        numbers = re.findall(r'\d+', str(sid))
        all_numbers.update(numbers)
    
    sorted_numbers = sorted(all_numbers, key=lambda x: int(x) if x.isdigit() else 0)
    print(f"Found numbers: {sorted_numbers}")
    
    # Look for 6, 12, 24 specifically
    richness_counts = {'6': 0, '12': 0, '24': 0}
    for sid in sample_ids:
        if '6' in str(sid):
            richness_counts['6'] += 1
        if '12' in str(sid):
            richness_counts['12'] += 1
        if '24' in str(sid):
            richness_counts['24'] += 1
    
    print(f"\nSamples containing richness indicators:")
    for richness, count in richness_counts.items():
        print(f"  Contains '{richness}': {count} samples")

if __name__ == "__main__":
    examine_sample_patterns()