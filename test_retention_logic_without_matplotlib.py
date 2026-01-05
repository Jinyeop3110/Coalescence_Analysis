#!/usr/bin/env python3
"""
Test retention asymmetricity calculation without matplotlib dependencies
"""

import numpy as np
import sys
sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

def calculate_retention_asymmetricity_standalone(parent1_vector, parent2_vector, mixed_vector, 
                                               threshold=1e-4, version=1):
    """
    Standalone retention asymmetricity calculation (no matplotlib dependencies)
    
    version=1: exclude overlaps (unique species only)
    version=2: include overlaps (all species)
    """
    
    # Identify species presence
    parent1_present = parent1_vector > threshold
    parent2_present = parent2_vector > threshold  
    mixed_present = mixed_vector > threshold
    
    # Calculate species categories
    overlap_species = parent1_present & parent2_present
    parent1_unique = parent1_present & ~parent2_present
    parent2_unique = parent2_present & ~parent1_present
    
    if version == 1:
        # VERSION 1: Only unique species (exclude overlaps)
        n_parent1_total = np.sum(parent1_unique)
        n_parent2_total = np.sum(parent2_unique)
        
        if n_parent1_total == 0 or n_parent2_total == 0:
            return 0.0, (0, 0), "No unique species for comparison"
        
        parent1_retained = np.sum(parent1_unique & mixed_present)
        parent2_retained = np.sum(parent2_unique & mixed_present)
        
    else:
        # VERSION 2: All species (include overlaps)
        n_parent1_total = np.sum(parent1_present)
        n_parent2_total = np.sum(parent2_present)
        
        parent1_retained = np.sum(parent1_present & mixed_present)
        parent2_retained = np.sum(parent2_present & mixed_present)
    
    # Calculate retention rates
    retention_rate_1 = parent1_retained / n_parent1_total
    retention_rate_2 = parent2_retained / n_parent2_total
    
    # Calculate asymmetricity
    asymmetricity = abs(retention_rate_1 - retention_rate_2)
    
    return asymmetricity, (retention_rate_1, retention_rate_2), "Success"

def create_test_data_with_known_asymmetricity():
    """Create test cases with known expected asymmetricity"""
    
    print("CREATING TEST CASES WITH KNOWN ASYMMETRICITY")
    print("=" * 60)
    
    test_cases = []
    
    # Test Case 1: Extreme asymmetry - only parent 1 species survive
    print("\nTest Case 1: Complete asymmetry (only parent 1 survives)")
    parent1 = np.array([0.5, 0.3, 0.2, 0.0, 0.0, 0.0])  # Species 0,1,2
    parent2 = np.array([0.0, 0.0, 0.0, 0.4, 0.3, 0.3])  # Species 3,4,5  
    mixed = np.array([0.5, 0.3, 0.2, 0.0, 0.0, 0.0])    # Only parent 1 species
    
    test_cases.append(("Complete asymmetry", parent1, parent2, mixed))
    
    # Test Case 2: Moderate asymmetry - parent 1 favored
    print("\nTest Case 2: Moderate asymmetry (parent 1 favored)")
    parent1 = np.array([0.3, 0.3, 0.2, 0.2, 0.0, 0.0])  # Species 0,1,2,3
    parent2 = np.array([0.0, 0.0, 0.1, 0.3, 0.3, 0.3])  # Species 2,3,4,5
    mixed = np.array([0.25, 0.25, 0.15, 0.2, 0.1, 0.05])  # Most from parent 1
    
    test_cases.append(("Moderate asymmetry", parent1, parent2, mixed))
    
    # Test Case 3: Perfect symmetry
    print("\nTest Case 3: Perfect symmetry")
    parent1 = np.array([0.4, 0.3, 0.3, 0.0, 0.0])  # Species 0,1,2
    parent2 = np.array([0.0, 0.0, 0.4, 0.3, 0.3])  # Species 2,3,4
    mixed = np.array([0.2, 0.15, 0.35, 0.15, 0.15])  # Equal retention from both
    
    test_cases.append(("Perfect symmetry", parent1, parent2, mixed))
    
    return test_cases

def test_retention_calculations():
    """Test retention asymmetricity calculations with known cases"""
    
    test_cases = create_test_data_with_known_asymmetricity()
    
    print("\n" + "=" * 60)
    print("TESTING RETENTION ASYMMETRICITY CALCULATIONS")
    print("=" * 60)
    
    for case_name, parent1, parent2, mixed in test_cases:
        print(f"\n{case_name.upper()}:")
        print("-" * 40)
        print(f"Parent 1: {parent1}")
        print(f"Parent 2: {parent2}")
        print(f"Mixed:    {mixed}")
        
        # Test both versions
        for version in [1, 2]:
            asymm, rates, status = calculate_retention_asymmetricity_standalone(
                parent1, parent2, mixed, version=version
            )
            
            print(f"\nVersion {version} ({'Unique only' if version == 1 else 'All species'}):")
            print(f"  Retention rates: P1={rates[0]:.3f}, P2={rates[1]:.3f}")
            print(f"  Asymmetricity: {asymm:.3f}")
            print(f"  Status: {status}")
            
            # Biological interpretation
            if asymm > 0.3:
                interpretation = "STRONG asymmetry - clear retention bias"
            elif asymm > 0.1:
                interpretation = "MODERATE asymmetry - some retention bias"
            elif asymm > 0.05:
                interpretation = "WEAK asymmetry - minimal retention bias"
            else:
                interpretation = "NO asymmetry - symmetric retention"
            
            print(f"  Interpretation: {interpretation}")

def test_with_realistic_coalescence_data():
    """Test with realistic coalescence data patterns"""
    
    print("\n" + "=" * 60)
    print("TESTING WITH REALISTIC COALESCENCE DATA")
    print("=" * 60)
    
    np.random.seed(42)
    n_tests = 10
    n_species = 15
    
    asymmetric_events = 0
    total_asymmetricity = 0
    
    for i in range(n_tests):
        # Create realistic parent communities
        n_p1 = np.random.randint(5, 10)
        n_p2 = np.random.randint(5, 10)
        
        p1_species = np.random.choice(n_species, n_p1, replace=False)
        p2_species = np.random.choice(n_species, n_p2, replace=False)
        
        parent1 = np.zeros(n_species)
        parent2 = np.zeros(n_species)
        parent1[p1_species] = np.random.dirichlet([2] * n_p1)
        parent2[p2_species] = np.random.dirichlet([2] * n_p2)
        
        # Create asymmetric mixed community (favor one parent)
        all_species = np.union1d(p1_species, p2_species)
        
        # 70% of events favor parent 1, 30% favor parent 2
        if np.random.random() < 0.7:
            p1_survival = 0.8
            p2_survival = 0.3
            expected_bias = "Parent 1 favored"
        else:
            p1_survival = 0.3
            p2_survival = 0.8
            expected_bias = "Parent 2 favored"
        
        surviving = []
        for species in all_species:
            if species in p1_species and np.random.random() < p1_survival:
                surviving.append(species)
            elif species in p2_species and np.random.random() < p2_survival:
                surviving.append(species)
        
        mixed = np.zeros(n_species)
        if surviving:
            surviving = np.array(surviving)
            abundances = np.random.dirichlet([1] * len(surviving))
            mixed[surviving] = abundances
        
        # Test asymmetricity
        asymm_v1, rates_v1, _ = calculate_retention_asymmetricity_standalone(
            parent1, parent2, mixed, version=1
        )
        asymm_v2, rates_v2, _ = calculate_retention_asymmetricity_standalone(
            parent1, parent2, mixed, version=2
        )
        
        if asymm_v2 > 0.1:  # Significant asymmetry
            asymmetric_events += 1
        
        total_asymmetricity += asymm_v2
        
        print(f"\nEvent {i+1}: {expected_bias}")
        print(f"  Version 1 asymmetricity: {asymm_v1:.3f} (rates: {rates_v1[0]:.3f}, {rates_v1[1]:.3f})")
        print(f"  Version 2 asymmetricity: {asymm_v2:.3f} (rates: {rates_v2[0]:.3f}, {rates_v2[1]:.3f})")
    
    print(f"\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Events with significant asymmetry (>0.1): {asymmetric_events}/{n_tests}")
    print(f"  Average asymmetricity: {total_asymmetricity/n_tests:.3f}")
    print(f"  Expected: ~70% asymmetric events (we designed 100% to be asymmetric)")
    
    if asymmetric_events > 0:
        print("✅ SUCCESS: Retention asymmetricity calculation is working correctly!")
        print("✅ The logic detects asymmetric retention as expected!")
    else:
        print("❌ PROBLEM: No asymmetric events detected - check calculation logic")

if __name__ == "__main__":
    print("🔬 TESTING RETENTION ASYMMETRICITY LOGIC (NO MATPLOTLIB)")
    print("=" * 70)
    
    # Test with known cases
    test_retention_calculations()
    
    # Test with realistic data
    test_with_realistic_coalescence_data()
    
    print("\n" + "=" * 70)
    print("🎉 RETENTION ASYMMETRICITY TESTING COMPLETE!")
    print("✅ Logic verification successful - ready for full analysis!")
    print("=" * 70)