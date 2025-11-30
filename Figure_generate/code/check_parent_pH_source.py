#!/usr/bin/env python3
"""
Check how pH is measured for parent communities
"""

import pandas as pd

def check_parent_pH_data():
    """Check the source of pH data for parent communities"""
    
    print("CHECKING PARENT COMMUNITY pH DATA SOURCE")
    print("=" * 50)
    
    # Load all data
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    metadata = pd.read_excel("../../Postprocessed/Metadata.xlsx")
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    # Merge to get parent communities with pH
    full_data = abundance_data.merge(
        metadata[['SampleIDX', 'CoalescenceType', 'Medium', 'CommunityIDX']], 
        on='SampleIDX', how='inner'
    ).merge(
        communities_data[['SampleIDX', 'fieldPH1', 'fieldPH7']], 
        on='SampleIDX', how='inner'
    )
    
    # Filter parent communities
    parent_communities = full_data[full_data['CoalescenceType'] == 'S'].copy()
    
    print("1. PARENT COMMUNITY pH DATA:")
    print(f"   Total parent community records: {len(parent_communities)}")
    print(f"   Records with fieldPH1: {(~parent_communities['fieldPH1'].isna()).sum()}")
    print(f"   Records with fieldPH7: {(~parent_communities['fieldPH7'].isna()).sum()}")
    
    # Check pH ranges
    print(f"\n2. pH VALUE RANGES:")
    if (~parent_communities['fieldPH1'].isna()).sum() > 0:
        print(f"   fieldPH1 range: {parent_communities['fieldPH1'].min():.2f} - {parent_communities['fieldPH1'].max():.2f}")
    if (~parent_communities['fieldPH7'].isna()).sum() > 0:
        print(f"   fieldPH7 range: {parent_communities['fieldPH7'].min():.2f} - {parent_communities['fieldPH7'].max():.2f}")
    
    # Check by medium
    print(f"\n3. pH BY MEDIUM (fieldPH7):")
    for medium in ['H', 'L', 'M']:
        medium_data = parent_communities[parent_communities['Medium'] == medium]
        pH_data = medium_data['fieldPH7'].dropna()
        if len(pH_data) > 0:
            print(f"   Medium {medium}: {len(pH_data)} communities, pH {pH_data.min():.2f} - {pH_data.max():.2f}")
        else:
            print(f"   Medium {medium}: No pH data")
    
    # Show some example records
    print(f"\n4. EXAMPLE PARENT COMMUNITY RECORDS:")
    example_parents = parent_communities[['SampleIDX', 'CommunityIDX', 'Medium', 'fieldPH1', 'fieldPH7']].head(10)
    print(example_parents.to_string(index=False))
    
    # Check what fieldPH1 and fieldPH7 represent
    print(f"\n5. pH FIELD MEANINGS:")
    print("   Based on column names:")
    print("   - fieldPH1: likely initial pH measurement")  
    print("   - fieldPH7: likely final pH measurement (after incubation)")
    print("   Note: Need to verify what these timepoints represent")
    
    # Check if parent communities should have their own pH measurements
    print(f"\n6. INTERPRETATION:")
    print("   Parent communities (CoalescenceType='S') are single communities")
    print("   They should have their own pH measurements before coalescence")
    print("   fieldPH7 likely represents the pH of each parent community")
    print("   after their individual growth/incubation period")
    
    # Check for unique vs duplicate communities
    print(f"\n7. COMMUNITY REPLICATION:")
    unique_communities = parent_communities.groupby(['CommunityIDX', 'Medium']).size()
    print(f"   Unique (CommunityIDX, Medium) combinations: {len(unique_communities)}")
    print(f"   Communities appearing multiple times:")
    duplicates = unique_communities[unique_communities > 1]
    if len(duplicates) > 0:
        print(f"   {len(duplicates)} community-medium pairs have multiple records")
        print("   This suggests multiple samples/replicates per community")
    else:
        print("   No duplicates found")

if __name__ == "__main__":
    check_parent_pH_data()