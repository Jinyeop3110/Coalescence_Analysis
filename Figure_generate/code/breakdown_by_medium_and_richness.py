#!/usr/bin/env python3
"""
Show breakdown by medium (L/M/H) and try to find richness information
"""

import pandas as pd

def analyze_breakdown():
    """Show sample breakdown by medium and richness if available"""
    
    # Load all data
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    # Merge abundance data with metadata (including Medium)
    merged_data = abundance_data.merge(
        communities_data[['SampleIDX', 'Medium', 'fieldPH1', 'fieldPH7', 'CommunityOrigin']], 
        on='SampleIDX', 
        how='inner'
    )
    
    print("SAMPLE BREAKDOWN ANALYSIS")
    print("=" * 50)
    print(f"Total samples in multivariate regression: {len(merged_data[~merged_data['fieldPH7'].isna()])}")
    
    # 1. Medium breakdown
    print("\n1. BREAKDOWN BY MEDIUM:")
    medium_counts = merged_data['Medium'].value_counts().sort_index()
    for medium, count in medium_counts.items():
        percentage = count / len(merged_data) * 100
        print(f"   {medium}: {count} samples ({percentage:.1f}%)")
    
    # 2. Community Origin breakdown  
    print("\n2. BREAKDOWN BY COMMUNITY ORIGIN:")
    origin_counts = merged_data['CommunityOrigin'].value_counts()
    for origin, count in origin_counts.items():
        percentage = count / len(merged_data) * 100
        print(f"   {origin}: {count} samples ({percentage:.1f}%)")
    
    # 3. Combined breakdown
    print("\n3. COMBINED BREAKDOWN (Medium × Origin):")
    combined = pd.crosstab(merged_data['Medium'], merged_data['CommunityOrigin'], margins=True)
    print(combined)
    
    # 4. Try to infer richness from data patterns
    print("\n4. ATTEMPTING TO INFER RICHNESS LEVELS:")
    
    # Count non-zero species abundances per sample
    abundance_cols = [col for col in merged_data.columns if col.startswith('NormalizedAbundance')]
    print(f"   Total species columns available: {len(abundance_cols)}")
    
    # For each sample, count how many species have >0 abundance
    non_zero_species_counts = []
    for _, row in merged_data.iterrows():
        non_zero_count = sum(1 for col in abundance_cols if row[col] > 0.001)  # >0.1% abundance
        non_zero_species_counts.append(non_zero_count)
    
    merged_data['ObservedRichness'] = non_zero_species_counts
    
    print("\n   OBSERVED SPECIES RICHNESS DISTRIBUTION:")
    richness_dist = pd.Series(non_zero_species_counts).value_counts().sort_index()
    for richness, count in richness_dist.head(15).items():  # Show top 15
        print(f"   {richness} species: {count} samples")
    
    # Look for patterns that might indicate s6/s12/s24
    print("\n5. POSSIBLE RICHNESS GROUPS:")
    # Group by ranges that might correspond to s6, s12, s24
    low_richness = merged_data[merged_data['ObservedRichness'] <= 8]   # Likely s6
    mid_richness = merged_data[(merged_data['ObservedRichness'] > 8) & (merged_data['ObservedRichness'] <= 16)]  # Likely s12
    high_richness = merged_data[merged_data['ObservedRichness'] > 16]   # Likely s24
    
    print(f"   Low richness (≤8 species, likely s6): {len(low_richness)} samples")
    print(f"   Mid richness (9-16 species, likely s12): {len(mid_richness)} samples") 
    print(f"   High richness (>16 species, likely s24): {len(high_richness)} samples")
    
    # Show medium breakdown for each richness group
    print("\n6. MEDIUM BREAKDOWN BY INFERRED RICHNESS:")
    print("\n   Low richness (≤8 species):")
    print(low_richness['Medium'].value_counts().sort_index())
    print("\n   Mid richness (9-16 species):")
    print(mid_richness['Medium'].value_counts().sort_index())
    print("\n   High richness (>16 species):")
    print(high_richness['Medium'].value_counts().sort_index())

if __name__ == "__main__":
    analyze_breakdown()