#!/usr/bin/env python3

import pandas as pd
import numpy as np

def debug_data_values():
    """Debug the actual data values in the 500-species Excel file."""
    
    print("="*60)
    print("DEBUGGING 500-SPECIES DATA VALUES")
    print("="*60)
    
    excel_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural/Similarity.xlsx"
    
    # Read all three sheets
    for sheet_idx in range(3):
        print(f"\n📊 Sheet {sheet_idx} Analysis:")
        df = pd.read_excel(excel_path, sheet_name=str(sheet_idx))
        
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        
        # Analyze each column
        for col in df.columns:
            data = df[col].dropna()
            if len(data) > 0:
                print(f"\n   Column '{col}':")
                print(f"      Count: {len(data)}")
                print(f"      Mean: {data.mean():.4f}")
                print(f"      Min: {data.min():.4f}")
                print(f"      Max: {data.max():.4f}")
                print(f"      First 5 values: {data.head().tolist()}")
                
                # Check for specific issues
                zeros = (data == 0).sum()
                ones = (data == 1).sum()
                print(f"      Zeros: {zeros}")
                print(f"      Ones: {ones}")
            else:
                print(f"\n   Column '{col}': NO DATA")
    
    print("\n" + "="*60)
    print("CHECKING PHASE DIAGRAM LOGIC")
    print("="*60)
    
    # Check what happens with the vector decomposition
    sheet0 = pd.read_excel(excel_path, sheet_name='0')
    sheet1 = pd.read_excel(excel_path, sheet_name='1')
    sheet2 = pd.read_excel(excel_path, sheet_name='2')
    
    print("\n📈 Vector Decomposition Interpretation:")
    print("   Sheet 0: Dominance metric (a)")
    print("   Sheet 1: Mixing metric (b)")
    print("   Sheet 2: Restructuring metric (c)")
    
    # Calculate fractions for each u-value
    for col in sheet0.columns:
        print(f"\n   {col}:")
        a_vals = sheet0[col].dropna()
        b_vals = sheet1[col].dropna()
        c_vals = sheet2[col].dropna()
        
        if len(a_vals) > 0:
            # These are the actual metric values, not fractions
            # Need to understand how they map to dominance/mixing/restructuring
            print(f"      Metric a: mean={a_vals.mean():.3f}, std={a_vals.std():.3f}")
            print(f"      Metric b: mean={b_vals.mean():.3f}, std={b_vals.std():.3f}")
            print(f"      Metric c: mean={c_vals.mean():.3f}, std={c_vals.std():.3f}")
            
            # Check the distribution
            print(f"      a > 0.5: {(a_vals > 0.5).sum()} events")
            print(f"      b > 0.5: {(b_vals > 0.5).sum()} events")
            print(f"      c > 0.5: {(c_vals > 0.5).sum()} events")

if __name__ == "__main__":
    debug_data_values()