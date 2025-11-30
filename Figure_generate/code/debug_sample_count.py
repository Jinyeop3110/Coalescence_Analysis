#!/usr/bin/env python3
"""
Debug why we have 94 samples per medium
"""

import pandas as pd

def debug_sample_count():
    """Debug the sample count breakdown"""
    
    print("DEBUGGING SAMPLE COUNT")
    print("=" * 40)
    
    # Load coalescence recipe
    recipe = pd.read_excel("../../Postprocessed/CoalescenceRecipe.xlsx")
    print(f"1. Coalescence recipe events: {len(recipe)}")
    print("   First few events:")
    print(recipe.head())
    
    # Load and check communities
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    print(f"\n2. Total community records: {len(communities_data)}")
    print(f"   CoalescenceType breakdown:")
    if 'CoalescenceType' in communities_data.columns:
        print(communities_data['CoalescenceType'].value_counts())
    
    print(f"   Medium breakdown:")
    if 'Medium' in communities_data.columns:
        print(communities_data['Medium'].value_counts())
    
    # Check parent communities specifically
    parent_communities = communities_data[communities_data['CoalescenceType'] == 'S']
    print(f"\n3. Parent communities: {len(parent_communities)}")
    print("   Parent communities by medium:")
    print(parent_communities['Medium'].value_counts())
    
    # Check coalesced communities
    coalesced_communities = communities_data[communities_data['CoalescenceType'] == 'C']
    print(f"\n4. Coalesced communities: {len(coalesced_communities)}")
    print("   Coalesced communities by medium:")
    print(coalesced_communities['Medium'].value_counts())
    
    # Check unique CommunityIDX values
    print(f"\n5. Unique parent CommunityIDX: {parent_communities['CommunityIDX'].nunique()}")
    print(f"   Unique coalesced CommunityIDX: {coalesced_communities['CommunityIDX'].nunique()}")
    
    # Show how linking works
    print(f"\n6. LINKING PROCESS:")
    print(f"   Recipe has {len(recipe)} coalescence events")
    print(f"   Each event uses 2 parents → creates 2 parent records per event")
    print(f"   For 3 media (H/L/M): 2 parents × {len(recipe)} events × 3 media = {2 * len(recipe) * 3}")
    
    # Check actual linking
    successful_links = 0
    for medium in ['H', 'L', 'M']:
        medium_links = 0
        for _, row in recipe.iterrows():
            coal_idx = row['CommunityIDX_Coal']
            sub1_idx = row['CommunityIDX_Sub1'] 
            sub2_idx = row['CommunityIDX_Sub2']
            
            # Check if all communities exist in this medium
            coal_exists = len(coalesced_communities[(coalesced_communities['CommunityIDX'] == coal_idx) & 
                                                  (coalesced_communities['Medium'] == medium)]) > 0
            sub1_exists = len(parent_communities[(parent_communities['CommunityIDX'] == sub1_idx) & 
                                               (parent_communities['Medium'] == medium)]) > 0
            sub2_exists = len(parent_communities[(parent_communities['CommunityIDX'] == sub2_idx) & 
                                               (parent_communities['Medium'] == medium)]) > 0
            
            if coal_exists and sub1_exists and sub2_exists:
                medium_links += 2  # 2 parents per successful coalescence event
                successful_links += 2
        
        print(f"   Medium {medium}: {medium_links} linked parent records")
    
    print(f"   Total successful links: {successful_links}")
    
    # Check pH data availability
    print(f"\n7. pH DATA AVAILABILITY:")
    coalesced_with_pH = coalesced_communities[~coalesced_communities['fieldPH7'].isna()]
    print(f"   Coalesced communities with pH data: {len(coalesced_with_pH)}")
    print("   By medium:")
    print(coalesced_with_pH['Medium'].value_counts())

if __name__ == "__main__":
    debug_sample_count()