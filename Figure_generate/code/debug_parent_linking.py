#!/usr/bin/env python3
"""
Debug parent community linking issues
"""

import pandas as pd

def debug_community_data():
    """Debug the community data structure"""
    
    # Load data
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    metadata = pd.read_excel("../../Postprocessed/Metadata.xlsx")
    
    # Merge abundance with metadata
    full_data = abundance_data.merge(
        metadata[['SampleIDX', 'CoalescenceType', 'Medium', 'CommunityIDX']], 
        on='SampleIDX', 
        how='inner'
    )
    
    print("DEBUGGING COMMUNITY DATA")
    print("=" * 40)
    
    # Check for duplicates
    print("1. CHECKING FOR DUPLICATE CommunityIDX VALUES:")
    parent_communities = full_data[full_data['CoalescenceType'] == 'S'].copy()
    coalesced_communities = full_data[full_data['CoalescenceType'] == 'C'].copy()
    
    print(f"   Parent communities: {len(parent_communities)}")
    print(f"   Unique parent CommunityIDX: {parent_communities['CommunityIDX'].nunique()}")
    
    parent_duplicates = parent_communities['CommunityIDX'].value_counts()
    parent_duplicates = parent_duplicates[parent_duplicates > 1]
    if len(parent_duplicates) > 0:
        print(f"   Duplicate parent CommunityIDX: {len(parent_duplicates)} values")
        print(f"   Examples: {parent_duplicates.head()}")
    
    print(f"   Coalesced communities: {len(coalesced_communities)}")
    print(f"   Unique coalesced CommunityIDX: {coalesced_communities['CommunityIDX'].nunique()}")
    
    coal_duplicates = coalesced_communities['CommunityIDX'].value_counts()
    coal_duplicates = coal_duplicates[coal_duplicates > 1]
    if len(coal_duplicates) > 0:
        print(f"   Duplicate coalesced CommunityIDX: {len(coal_duplicates)} values")
        print(f"   Examples: {coal_duplicates.head()}")
    
    # Check what causes duplicates - likely replicates or different samples from same community
    print("\\n2. ANALYZING DUPLICATE STRUCTURE:")
    if len(parent_duplicates) > 0:
        example_idx = parent_duplicates.index[0]
        duplicate_rows = parent_communities[parent_communities['CommunityIDX'] == example_idx]
        print(f"   Example duplicate (CommunityIDX {example_idx}):")
        print(duplicate_rows[['SampleIDX', 'CommunityIDX', 'Medium', 'CoalescenceType']].to_string())
        
        # Check if these are different samples from same community
        print(f"   Different SampleIDX? {duplicate_rows['SampleIDX'].nunique() > 1}")
        print(f"   Different Media? {duplicate_rows['Medium'].nunique() > 1}")
    
    # Check coalescence recipe
    print("\\n3. COALESCENCE RECIPE ANALYSIS:")
    recipe = pd.read_excel("../../Postprocessed/CoalescenceRecipe.xlsx")
    print(f"   Coalescence events: {len(recipe)}")
    print(f"   Unique coalesced communities: {recipe['CommunityIDX_Coal'].nunique()}")
    print(f"   Unique parent1 communities: {recipe['CommunityIDX_Sub1'].nunique()}")
    print(f"   Unique parent2 communities: {recipe['CommunityIDX_Sub2'].nunique()}")
    
    # Show some examples
    print(f"\\n   Example coalescence events:")
    print(recipe.head().to_string())

if __name__ == "__main__":
    debug_community_data()