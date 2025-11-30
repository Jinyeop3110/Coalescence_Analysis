"""
Debug script to check natural community data loading and classification
"""

from common_setup import *
import numpy as np
import pandas as pd

def debug_data_loading():
    """Debug the data loading process for natural communities."""
    
    print("=" * 80)
    print("DEBUGGING NATURAL COMMUNITY DATA LOADING")
    print("=" * 80)
    
    # Check what's in Nat_Coal_IDX
    print("\n1. Checking Nat_Coal_IDX contents:")
    print(f"Keys in Nat_Coal_IDX: {list(Nat_Coal_IDX.keys())}")
    for key, value in Nat_Coal_IDX.items():
        print(f"  {key}: {len(value)} samples - {value[:5]}..." if len(value) > 5 else f"  {key}: {len(value)} samples - {value}")
    
    # Check Coalescence_data structure
    print("\n2. Checking Coalescence_data structure:")
    print(f"Coalescence_data shape: {Coalescence_data.shape}")
    print(f"Coalescence_data columns: {list(Coalescence_data.columns)}")
    print(f"First few rows:\n{Coalescence_data.head()}")
    
    # Check Processed_sequences_natural structure
    print("\n3. Checking Processed_sequences_natural structure:")
    print(f"Processed_sequences_natural shape: {Processed_sequences_natural.shape}")
    print(f"First few columns: {list(Processed_sequences_natural.columns[:10])}")
    
    # Let's trace through one example for each nutrient level
    for nutrient_level in ['LN', 'MN', 'HN']:
        print(f"\n{'='*60}")
        print(f"DETAILED CHECK FOR {nutrient_level}")
        print(f"{'='*60}")
        
        if nutrient_level not in Nat_Coal_IDX:
            print(f"ERROR: {nutrient_level} not in Nat_Coal_IDX")
            continue
            
        IDX_list = Nat_Coal_IDX[nutrient_level]
        if len(IDX_list) == 0:
            print(f"ERROR: No samples for {nutrient_level}")
            continue
            
        # Take first sample as example
        sample_idx = IDX_list[0]
        print(f"\nExample sample: {sample_idx}")
        
        # Find in Coalescence_data
        coal_idx = np.where(Coalescence_data['SampleIDX'] == sample_idx)[0]
        if len(coal_idx) == 0:
            print(f"ERROR: Sample {sample_idx} not found in Coalescence_data")
            continue
            
        coal_row = Coalescence_data.iloc[coal_idx[0]]
        print(f"\nCoalescence data for sample {sample_idx}:")
        print(f"  SampleIDX_Sub1: {coal_row['SampleIDX_Sub1']}")
        print(f"  SampleIDX_Sub2: {coal_row['SampleIDX_Sub2']}")
        
        # Find parent communities
        sub1_idx = np.where(Processed_sequences_natural['SampleIDX'] == coal_row['SampleIDX_Sub1'])[0]
        sub2_idx = np.where(Processed_sequences_natural['SampleIDX'] == coal_row['SampleIDX_Sub2'])[0]
        mix_idx = np.where(Processed_sequences_natural['SampleIDX'] == sample_idx)[0]
        
        print(f"\nIndices in Processed_sequences_natural:")
        print(f"  Sub1 ({coal_row['SampleIDX_Sub1']}): {'Found' if len(sub1_idx) > 0 else 'NOT FOUND'}")
        print(f"  Sub2 ({coal_row['SampleIDX_Sub2']}): {'Found' if len(sub2_idx) > 0 else 'NOT FOUND'}")
        print(f"  Mix ({sample_idx}): {'Found' if len(mix_idx) > 0 else 'NOT FOUND'}")
        
        if len(sub1_idx) > 0 and len(sub2_idx) > 0 and len(mix_idx) > 0:
            # Get abundance vectors
            c_1 = np.array(Processed_sequences_natural.iloc[sub1_idx[0]].values.tolist()[1:])
            c_2 = np.array(Processed_sequences_natural.iloc[sub2_idx[0]].values.tolist()[1:])
            c_mix = np.array(Processed_sequences_natural.iloc[mix_idx[0]].values.tolist()[1:])
            
            print(f"\nAbundance vector stats:")
            print(f"  c_1: shape={c_1.shape}, sum={np.sum(c_1):.6f}, non-zero={np.sum(c_1 > 0)}")
            print(f"  c_2: shape={c_2.shape}, sum={np.sum(c_2):.6f}, non-zero={np.sum(c_2 > 0)}")
            print(f"  c_mix: shape={c_mix.shape}, sum={np.sum(c_mix):.6f}, non-zero={np.sum(c_mix > 0)}")
            
            # Apply threshold
            c_1_thresh = c_1 * (c_1 > 1e-4)
            c_2_thresh = c_2 * (c_2 > 1e-4)
            
            print(f"\nAfter threshold (1e-4):")
            print(f"  c_1: non-zero={np.sum(c_1_thresh > 0)}")
            print(f"  c_2: non-zero={np.sum(c_2_thresh > 0)}")
            
            # Calculate metrics
            try:
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1_thresh, c_2_thresh, c_mix)
                print(f"\nVector decomposition results:")
                print(f"  u = {u:.4f}")
                print(f"  v = {v:.4f}")
                print(f"  k = {k:.4f}")
                
                # Classification
                x = np.sqrt(u**2 + v**2)
                y = np.abs(np.abs(np.arctan(u/(v + 1e-8))) - np.pi/4) / (np.pi/4)
                
                print(f"\nClassification variables:")
                print(f"  x = {x:.4f}")
                print(f"  y = {y:.4f}")
                
                # Determine class
                if (x**2 > 0.5) * (y > 0.5):
                    outcome = "Dominance"
                elif (x**2 > 0.5) * (y < 0.5):
                    outcome = "Mixing"
                elif (x**2 < 0.5):
                    outcome = "Restructuring"
                else:
                    outcome = "Unknown"
                
                print(f"  Outcome: {outcome}")
                
            except Exception as e:
                print(f"\nERROR in vector decomposition: {e}")

def check_classification_consistency():
    """Check if classification is consistent between different scripts."""
    
    print("\n" + "=" * 80)
    print("CHECKING CLASSIFICATION CONSISTENCY")
    print("=" * 80)
    
    # Test some edge cases
    test_cases = [
        (0.8, 0.8),   # Should be dominance
        (0.8, 0.1),   # Should be mixing
        (0.1, 0.1),   # Should be restructuring
    ]
    
    for u, v in test_cases:
        x = np.sqrt(u**2 + v**2)
        y = np.abs(np.abs(np.arctan(u/(v + 1e-8))) - np.pi/4) / (np.pi/4)
        
        print(f"\nTest case: u={u}, v={v}")
        print(f"  x = {x:.4f}, x^2 = {x**2:.4f}")
        print(f"  y = {y:.4f}")
        
        # Check conditions
        print(f"  x^2 > 0.5: {x**2 > 0.5}")
        print(f"  y > 0.5: {y > 0.5}")
        print(f"  y < 0.5: {y < 0.5}")
        
        if (x**2 > 0.5) * (y > 0.5):
            outcome = "Dominance"
        elif (x**2 > 0.5) * (y < 0.5):
            outcome = "Mixing"
        elif (x**2 < 0.5):
            outcome = "Restructuring"
        else:
            outcome = "Unknown"
            
        print(f"  Classification: {outcome}")

if __name__ == "__main__":
    debug_data_loading()
    check_classification_consistency()