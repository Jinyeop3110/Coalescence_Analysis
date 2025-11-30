#!/usr/bin/env python3
"""
Explore data files to find parent community information
"""

import pandas as pd
import os

def explore_coalescence_data():
    """Explore available data files for parent community info"""
    
    print("EXPLORING DATA FILES FOR PARENT COMMUNITIES")
    print("=" * 60)
    
    # 1. Check CoalescenceRecipe.xlsx
    print("1. COALESCENCE RECIPE:")
    try:
        recipe = pd.read_excel("../../Postprocessed/CoalescenceRecipe.xlsx")
        print(f"   Columns: {list(recipe.columns)}")
        print(f"   Sample size: {len(recipe)}")
        print(f"   First few rows:")
        print(recipe.head())
    except Exception as e:
        print(f"   Error: {e}")
    
    # 2. Check if there are timepoint=0 or initial conditions in communities data
    print("\n2. CHECKING FOR INITIAL CONDITIONS IN COMMUNITIES DATA:")
    try:
        communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
        print(f"   Timepoint column exists: {'Timepoint' in communities_synthetic.columns}")
        if 'Timepoint' in communities_synthetic.columns:
            timepoints = communities_synthetic['Timepoint'].unique()
            print(f"   Available timepoints: {sorted(timepoints)}")
            
            # Check if timepoint 0 or 1 exists (initial conditions)
            initial_timepoints = [t for t in timepoints if t in [0, 1]]
            if initial_timepoints:
                print(f"   Potential initial timepoints: {initial_timepoints}")
                for tp in initial_timepoints:
                    count = len(communities_synthetic[communities_synthetic['Timepoint'] == tp])
                    print(f"     Timepoint {tp}: {count} samples")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 3. Check processed sequences for timepoint info
    print("\n3. CHECKING PROCESSED SEQUENCES FOR INITIAL DATA:")
    try:
        sequences = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
        print(f"   Columns: {list(sequences.columns)}")
        
        # Look for timepoint or initial condition indicators
        timepoint_cols = [col for col in sequences.columns if 'time' in col.lower() or 'initial' in col.lower() or 'parent' in col.lower()]
        if timepoint_cols:
            print(f"   Potential timepoint columns: {timepoint_cols}")
            for col in timepoint_cols:
                unique_vals = sequences[col].unique()
                print(f"     {col}: {unique_vals}")
        
        # Check if there might be parent community identifiers
        if 'CommunityIDX' in sequences.columns:
            print(f"   CommunityIDX values: {sorted(sequences['CommunityIDX'].unique())}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # 4. Check metadata for parent/initial info
    print("\n4. CHECKING METADATA:")
    try:
        metadata = pd.read_excel("../../Postprocessed/Metadata.xlsx")
        print(f"   Columns: {list(metadata.columns)}")
        
        # Look for coalescence type or parent info
        coalescence_cols = [col for col in metadata.columns if any(x in col.lower() for x in ['coalescence', 'parent', 'initial', 'before'])]
        if coalescence_cols:
            print(f"   Coalescence-related columns: {coalescence_cols}")
            for col in coalescence_cols:
                unique_vals = metadata[col].unique()
                print(f"     {col}: {unique_vals}")
                
        if 'CoalescenceType' in metadata.columns:
            print(f"   CoalescenceType breakdown:")
            print(metadata['CoalescenceType'].value_counts())
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # 5. Check if parent communities are identified by community origin or type
    print("\n5. ANALYZING COALESCENCE PATTERNS:")
    try:
        communities = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
        
        if 'CoalescenceType' in communities.columns:
            print(f"   CoalescenceType values: {communities['CoalescenceType'].unique()}")
            
        if 'CommunityOrigin' in communities.columns:
            print(f"   CommunityOrigin values: {communities['CommunityOrigin'].unique()}")
            
        # Look for patterns that might indicate parent vs coalesced
        if 'Replicate' in communities.columns:
            print(f"   Replicate range: {communities['Replicate'].min()} - {communities['Replicate'].max()}")
            
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    explore_coalescence_data()