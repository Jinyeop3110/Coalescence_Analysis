#!/usr/bin/env python3
"""
Check metadata columns for richness and medium information
"""

import pandas as pd

def check_metadata():
    """Check what metadata is available"""
    
    print("METADATA COLUMN ANALYSIS")
    print("=" * 40)
    
    # Check communities files for metadata
    print("1. SYNTHETIC COMMUNITIES METADATA:")
    try:
        communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
        print(f"   Columns: {list(communities_synthetic.columns)}")
        print(f"   Sample size: {len(communities_synthetic)}")
        
        # Look for richness/medium related columns
        relevant_cols = [col for col in communities_synthetic.columns 
                        if any(x in col.lower() for x in ['rich', 'medium', 'pool', 'initial', 's6', 's12', 's24', 'treatment', 'condition'])]
        if relevant_cols:
            print(f"   Relevant columns: {relevant_cols}")
            for col in relevant_cols:
                unique_vals = communities_synthetic[col].unique()
                print(f"     {col}: {unique_vals}")
    except Exception as e:
        print(f"   Error reading synthetic communities: {e}")
    
    print("\n2. NATURAL COMMUNITIES METADATA:")
    try:
        communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
        print(f"   Columns: {list(communities_natural.columns)}")
        print(f"   Sample size: {len(communities_natural)}")
        
        relevant_cols = [col for col in communities_natural.columns 
                        if any(x in col.lower() for x in ['rich', 'medium', 'pool', 'initial', 's6', 's12', 's24', 'treatment', 'condition'])]
        if relevant_cols:
            print(f"   Relevant columns: {relevant_cols}")
            for col in relevant_cols:
                unique_vals = communities_natural[col].unique()
                print(f"     {col}: {unique_vals}")
    except Exception as e:
        print(f"   Error reading natural communities: {e}")
    
    print("\n3. POSTPROCESSED METADATA:")
    try:
        metadata = pd.read_excel("../../Postprocessed/Metadata.xlsx")
        print(f"   Columns: {list(metadata.columns)}")
        print(f"   Sample size: {len(metadata)}")
        
        relevant_cols = [col for col in metadata.columns 
                        if any(x in col.lower() for x in ['rich', 'medium', 'pool', 'initial', 's6', 's12', 's24', 'treatment', 'condition'])]
        if relevant_cols:
            print(f"   Relevant columns: {relevant_cols}")
            for col in relevant_cols:
                unique_vals = metadata[col].unique()
                print(f"     {col}: {unique_vals[:10]}")  # Show first 10 unique values
    except Exception as e:
        print(f"   Error reading metadata: {e}")

if __name__ == "__main__":
    check_metadata()