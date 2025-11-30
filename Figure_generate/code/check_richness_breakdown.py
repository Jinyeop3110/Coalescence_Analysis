#!/usr/bin/env python3
"""
Check breakdown of samples by initial species richness (s6, s12, s24)
"""

import pandas as pd

def check_richness_breakdown():
    """Check how many samples from each initial richness level"""
    
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
    
    print("SAMPLE BREAKDOWN BY INITIAL SPECIES RICHNESS")
    print("=" * 50)
    
    # Check what columns might indicate richness
    print("Available columns:")
    for col in merged_data.columns:
        if any(x in col.lower() for x in ['rich', 'species', 's6', 's12', 's24', 'pool', 'initial']):
            print(f"  - {col}")
    
    print(f"\nTotal samples: {len(merged_data)}")
    
    # Try to find richness indicator
    richness_cols = [col for col in merged_data.columns if any(x in col.lower() for x in ['rich', 'species', 'pool', 'initial'])]
    
    if richness_cols:
        print(f"\nPossible richness columns: {richness_cols}")
        for col in richness_cols[:3]:  # Check first few
            print(f"\n{col} breakdown:")
            print(merged_data[col].value_counts().sort_index())
    else:
        print("\nNo obvious richness columns found. Checking SampleIDX patterns...")
        # Look for patterns in SampleIDX
        sample_patterns = merged_data['SampleIDX'].astype(str).str.extract(r'(s\d+)', expand=False)
        if sample_patterns.notna().any():
            print("SampleIDX patterns (s6/s12/s24):")
            print(sample_patterns.value_counts())

if __name__ == "__main__":
    check_richness_breakdown()