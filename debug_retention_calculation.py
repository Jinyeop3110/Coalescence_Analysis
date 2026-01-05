#!/usr/bin/env python3
"""
Debug retention asymmetricity calculation to find why it gives zeros
"""

import numpy as np

def debug_retention_calculation():
    """Debug step by step what happens in retention calculation"""
    
    print("DEBUGGING RETENTION ASYMMETRICITY CALCULATION")
    print("=" * 60)
    
    # Create realistic test data
    print("\n1. CREATING TEST DATA:")
    print("-" * 30)
    
    # Parent 1: 4 species present
    parent1 = np.array([0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0])
    # Parent 2: 4 different species present (with 1 overlap)  
    parent2 = np.array([0.0, 0.0, 0.1, 0.3, 0.3, 0.3, 0.0, 0.0])
    # Mixed: Some species from both parents survive
    mixed = np.array([0.2, 0.1, 0.15, 0.2, 0.15, 0.2, 0.0, 0.0])
    
    threshold = 1e-4
    
    print(f"Parent 1: {parent1}")
    print(f"Parent 2: {parent2}")
    print(f"Mixed:    {mixed}")
    print(f"Threshold: {threshold}")
    
    print(f"\nSpecies presence:")
    parent1_present = parent1 > threshold
    parent2_present = parent2 > threshold  
    mixed_present = mixed > threshold
    
    print(f"Parent 1 present: {parent1_present}")
    print(f"Parent 2 present: {parent2_present}")
    print(f"Mixed present:    {mixed_present}")
    
    # Calculate species counts
    print(f"\n2. SPECIES ANALYSIS:")
    print("-" * 30)
    
    overlap_species = parent1_present & parent2_present
    parent1_unique = parent1_present & ~parent2_present
    parent2_unique = parent2_present & ~parent1_present
    
    print(f"Overlap species:     {overlap_species}")
    print(f"Parent 1 unique:     {parent1_unique}")
    print(f"Parent 2 unique:     {parent2_unique}")
    
    n_overlap = np.sum(overlap_species)
    n_p1_unique = np.sum(parent1_unique)
    n_p2_unique = np.sum(parent2_unique)
    
    print(f"\nCounts:")
    print(f"Overlap species:     {n_overlap}")
    print(f"Parent 1 unique:     {n_p1_unique}")  
    print(f"Parent 2 unique:     {n_p2_unique}")
    
    # VERSION 1 CALCULATION (exclude overlaps)
    print(f"\n3. VERSION 1 (EXCLUDE OVERLAPS):")
    print("-" * 40)
    
    n_parent1_total_v1 = n_p1_unique
    n_parent2_total_v1 = n_p2_unique
    parent1_retained_v1 = np.sum(parent1_unique & mixed_present)
    parent2_retained_v1 = np.sum(parent2_unique & mixed_present)
    
    print(f"Parent 1 total (unique only): {n_parent1_total_v1}")
    print(f"Parent 2 total (unique only): {n_parent2_total_v1}")
    print(f"Parent 1 retained: {parent1_retained_v1}")
    print(f"Parent 2 retained: {parent2_retained_v1}")
    
    if n_parent1_total_v1 > 0 and n_parent2_total_v1 > 0:
        retention_1_v1 = parent1_retained_v1 / n_parent1_total_v1
        retention_2_v1 = parent2_retained_v1 / n_parent2_total_v1
        asymmetricity_v1 = abs(retention_1_v1 - retention_2_v1)
        
        print(f"Parent 1 retention rate: {retention_1_v1:.3f}")
        print(f"Parent 2 retention rate: {retention_2_v1:.3f}")
        print(f"Asymmetricity: {asymmetricity_v1:.3f}")
    else:
        print("⚠️ One parent has no unique species - asymmetricity = 0")
    
    # VERSION 2 CALCULATION (include overlaps)
    print(f"\n4. VERSION 2 (INCLUDE OVERLAPS):")
    print("-" * 40)
    
    n_parent1_total_v2 = np.sum(parent1_present)
    n_parent2_total_v2 = np.sum(parent2_present)
    parent1_retained_v2 = np.sum(parent1_present & mixed_present)
    parent2_retained_v2 = np.sum(parent2_present & mixed_present)
    
    print(f"Parent 1 total (all species): {n_parent1_total_v2}")
    print(f"Parent 2 total (all species): {n_parent2_total_v2}")
    print(f"Parent 1 retained: {parent1_retained_v2}")
    print(f"Parent 2 retained: {parent2_retained_v2}")
    
    retention_1_v2 = parent1_retained_v2 / n_parent1_total_v2
    retention_2_v2 = parent2_retained_v2 / n_parent2_total_v2
    asymmetricity_v2 = abs(retention_1_v2 - retention_2_v2)
    
    print(f"Parent 1 retention rate: {retention_1_v2:.3f}")
    print(f"Parent 2 retention rate: {retention_2_v2:.3f}")
    print(f"Asymmetricity: {asymmetricity_v2:.3f}")
    
    # POTENTIAL ISSUES
    print(f"\n5. POTENTIAL ISSUES THAT COULD CAUSE ZEROS:")
    print("-" * 50)
    
    print("❓ Issue 1: Threshold too high?")
    for thresh in [1e-4, 1e-3, 1e-2, 0.01]:
        p1_count = np.sum(parent1 > thresh)
        p2_count = np.sum(parent2 > thresh)
        m_count = np.sum(mixed > thresh)
        print(f"   Threshold {thresh}: P1={p1_count}, P2={p2_count}, Mixed={m_count}")
    
    print(f"\n❓ Issue 2: No species overlap causing division by zero?")
    print(f"   Overlap exists: {n_overlap > 0}")
    print(f"   Parent 1 unique exists: {n_p1_unique > 0}")
    print(f"   Parent 2 unique exists: {n_p2_unique > 0}")
    
    print(f"\n❓ Issue 3: All species retained (no loss)?")
    all_p1_retained = parent1_retained_v2 == n_parent1_total_v2
    all_p2_retained = parent2_retained_v2 == n_parent2_total_v2
    print(f"   All P1 species retained: {all_p1_retained}")
    print(f"   All P2 species retained: {all_p2_retained}")
    print(f"   If both = True, asymmetricity = 0")
    
    print(f"\n❓ Issue 4: Real data has different structure?")
    print("   Check if real data:")
    print("   - Has very sparse vectors (mostly zeros)")
    print("   - Uses different abundance scales") 
    print("   - Has different threshold requirements")
    
    return {
        'asymmetricity_v1': asymmetricity_v1 if 'asymmetricity_v1' in locals() else 0,
        'asymmetricity_v2': asymmetricity_v2,
        'retention_rates': {
            'v1': (retention_1_v1, retention_2_v1) if 'retention_1_v1' in locals() else (0, 0),
            'v2': (retention_1_v2, retention_2_v2)
        }
    }

def test_with_extreme_cases():
    """Test with cases that should definitely give non-zero asymmetricity"""
    
    print(f"\n6. TESTING EXTREME CASES:")
    print("-" * 30)
    
    # Case 1: Complete asymmetry (only parent 1 species survive)
    parent1 = np.array([0.5, 0.3, 0.2, 0.0, 0.0])
    parent2 = np.array([0.0, 0.0, 0.3, 0.4, 0.3])
    mixed_asymmetric = np.array([0.5, 0.3, 0.2, 0.0, 0.0])  # Only P1 species
    
    print("Case 1 - Complete Asymmetry (only P1 survives):")
    print(f"Parent 1: {parent1}")
    print(f"Parent 2: {parent2}")
    print(f"Mixed:    {mixed_asymmetric}")
    
    # Manual calculation
    p1_total = np.sum(parent1 > 0)
    p2_total = np.sum(parent2 > 0) 
    p1_retained = np.sum((parent1 > 0) & (mixed_asymmetric > 0))
    p2_retained = np.sum((parent2 > 0) & (mixed_asymmetric > 0))
    
    retention_1 = p1_retained / p1_total
    retention_2 = p2_retained / p2_total
    asymmetry = abs(retention_1 - retention_2)
    
    print(f"P1 retention: {p1_retained}/{p1_total} = {retention_1:.3f}")
    print(f"P2 retention: {p2_retained}/{p2_total} = {retention_2:.3f}")
    print(f"Expected asymmetricity: {asymmetry:.3f}")
    
    if asymmetry == 0:
        print("🚨 ERROR: Even extreme case gives zero asymmetricity!")
    else:
        print("✅ Extreme case gives non-zero asymmetricity as expected")
    
    return asymmetry

if __name__ == "__main__":
    debug_result = debug_retention_calculation()
    extreme_result = test_with_extreme_cases()
    
    print(f"\n" + "="*60)
    print("DEBUGGING SUMMARY:")
    print(f"Basic test asymmetricity V1: {debug_result['asymmetricity_v1']:.3f}")
    print(f"Basic test asymmetricity V2: {debug_result['asymmetricity_v2']:.3f}")
    print(f"Extreme case asymmetricity: {extreme_result:.3f}")
    
    if debug_result['asymmetricity_v2'] == 0 and extreme_result == 0:
        print("🚨 PROBLEM: Even simple cases give zero asymmetricity")
        print("📋 CHECK: Implementation logic in the actual function")
    else:
        print("✅ Basic logic works - issue might be with real data or function implementation")
    print("="*60)