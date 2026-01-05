"""
Test script to verify V3 and V4 null model implementations
"""
import numpy as np
import sys
import os

# Add the Figure_generate/code directory to Python path
sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

from AsymmetricityNullModelAnalysis import (
    generate_random_selection_null_v3,
    generate_random_selection_null_v4
)

def create_test_data():
    """Create simple test data to verify null model behavior"""
    # Parent 1: Species [0, 1, 2] present
    parent1 = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
    
    # Parent 2: Species [2, 3, 4] present (species 2 overlaps with parent1)
    parent2 = np.array([0.0, 0.0, 1.0, 1.0, 1.0, 0.0])
    
    # Offspring: 2 species survived ([1, 3])
    offspring = np.array([0.0, 1.0, 0.0, 1.0, 0.0, 0.0])
    
    return parent1, parent2, offspring

def test_species_pool_construction():
    """Test that V3 and V4 construct species pools correctly"""
    print("=== Testing Species Pool Construction ===")
    
    parent1, parent2, offspring = create_test_data()
    
    threshold = 1e-4
    
    # Identify species in each parent
    parent1_present = parent1 > threshold  # [True, True, True, False, False, False]
    parent2_present = parent2 > threshold  # [False, False, True, True, True, False]
    
    print(f"Parent 1 species: {np.where(parent1_present)[0]}")  # [0, 1, 2]
    print(f"Parent 2 species: {np.where(parent2_present)[0]}")  # [2, 3, 4]
    print(f"Overlapping species: {np.where(parent1_present & parent2_present)[0]}")  # [2]
    
    # V3 species pool (excluding overlaps)
    parent1_unique = parent1_present & ~parent2_present  # [True, True, False, False, False, False]
    parent2_unique = parent2_present & ~parent1_present  # [False, False, False, True, True, False]
    v3_pool = parent1_unique | parent2_unique  # [True, True, False, True, True, False]
    
    print(f"V3 species pool (excluding overlaps): {np.where(v3_pool)[0]}")  # [0, 1, 3, 4]
    
    # V4 species pool (including overlaps)
    v4_pool = parent1_present | parent2_present  # [True, True, True, True, True, False]
    
    print(f"V4 species pool (including overlaps): {np.where(v4_pool)[0]}")  # [0, 1, 2, 3, 4]
    
    return v3_pool, v4_pool

def test_fixed_n_sampling():
    """Test that both models sample exactly N species matching experimental data"""
    print("\n=== Testing Fixed-N Sampling ===")
    
    parent1, parent2, offspring = create_test_data()
    
    # Count survivors in experimental data
    threshold = 1e-4
    n_survivors = np.sum(offspring > threshold)
    print(f"Experimental survivors: {n_survivors}")
    print(f"Survivor species: {np.where(offspring > threshold)[0]}")
    
    # Test data setup
    parent1_list = [parent1]
    parent2_list = [parent2]
    offspring_list = [offspring]
    nutrient_conditions = ['LN']
    species_numbers = [6]
    data_types = ['S']
    
    # Generate V3 null models
    print("\n--- Testing V3 (excluding overlaps) ---")
    v3_results = generate_random_selection_null_v3(
        parent1_list, parent2_list, nutrient_conditions, species_numbers,
        n_permutations=10, data_types=data_types, offspring_list=offspring_list
    )
    
    v3_offspring, v3_parent1, v3_parent2, v3_conditions, v3_species = v3_results
    
    print(f"Generated {len(v3_offspring)} V3 null samples")
    
    # Check survivor counts for V3
    v3_survivor_counts = [np.sum(null_off > threshold) for null_off in v3_offspring]
    print(f"V3 survivor counts: {v3_survivor_counts}")
    print(f"All V3 samples have {n_survivors} survivors: {all(count == n_survivors for count in v3_survivor_counts)}")
    
    # Show first few V3 samples
    for i, null_off in enumerate(v3_offspring[:3]):
        survivors = np.where(null_off > threshold)[0]
        print(f"V3 sample {i+1} survivors: {survivors}")
    
    # Generate V4 null models
    print("\n--- Testing V4 (including overlaps) ---")
    v4_results = generate_random_selection_null_v4(
        parent1_list, parent2_list, nutrient_conditions, species_numbers,
        n_permutations=10, data_types=data_types, offspring_list=offspring_list
    )
    
    v4_offspring, v4_parent1, v4_parent2, v4_conditions, v4_species = v4_results
    
    print(f"Generated {len(v4_offspring)} V4 null samples")
    
    # Check survivor counts for V4
    v4_survivor_counts = [np.sum(null_off > threshold) for null_off in v4_offspring]
    print(f"V4 survivor counts: {v4_survivor_counts}")
    print(f"All V4 samples have {n_survivors} survivors: {all(count == n_survivors for count in v4_survivor_counts)}")
    
    # Show first few V4 samples
    for i, null_off in enumerate(v4_offspring[:3]):
        survivors = np.where(null_off > threshold)[0]
        print(f"V4 sample {i+1} survivors: {survivors}")
    
    return v3_results, v4_results

def analyze_sampling_behavior():
    """Analyze the sampling behavior over many iterations"""
    print("\n=== Analyzing Sampling Behavior ===")
    
    parent1, parent2, offspring = create_test_data()
    
    # Test data setup
    parent1_list = [parent1]
    parent2_list = [parent2]
    offspring_list = [offspring]
    nutrient_conditions = ['LN']
    species_numbers = [6]
    data_types = ['S']
    
    # Generate many samples
    n_samples = 1000
    
    print(f"Generating {n_samples} samples for each model...")
    
    # V3 analysis
    v3_results = generate_random_selection_null_v3(
        parent1_list, parent2_list, nutrient_conditions, species_numbers,
        n_permutations=n_samples, data_types=data_types, offspring_list=offspring_list
    )
    
    v3_offspring = v3_results[0]
    
    # Count species frequency in V3
    species_counts_v3 = np.zeros(6)
    for null_off in v3_offspring:
        species_counts_v3 += (null_off > 1e-4).astype(int)
    
    print(f"\nV3 Species Selection Frequencies (out of {n_samples} samples):")
    for i, count in enumerate(species_counts_v3):
        print(f"Species {i}: {count} times ({count/n_samples:.3f})")
    
    # V4 analysis  
    v4_results = generate_random_selection_null_v4(
        parent1_list, parent2_list, nutrient_conditions, species_numbers,
        n_permutations=n_samples, data_types=data_types, offspring_list=offspring_list
    )
    
    v4_offspring = v4_results[0]
    
    # Count species frequency in V4
    species_counts_v4 = np.zeros(6)
    for null_off in v4_offspring:
        species_counts_v4 += (null_off > 1e-4).astype(int)
    
    print(f"\nV4 Species Selection Frequencies (out of {n_samples} samples):")
    for i, count in enumerate(species_counts_v4):
        print(f"Species {i}: {count} times ({count/n_samples:.3f})")
    
    # Expected frequencies
    print(f"\nExpected V3 frequency: {2/4:.3f} for species in pool [0,1,3,4]")
    print(f"Expected V4 frequency: {2/5:.3f} for species in pool [0,1,2,3,4]")
    
    # Verify species 2 (overlap) behavior
    print(f"\nSpecies 2 (overlap) selected:")
    print(f"V3: {species_counts_v3[2]} times (should be 0 - excluded from pool)")
    print(f"V4: {species_counts_v4[2]} times (should be ~{2*n_samples/5:.0f} - included in pool)")

def test_edge_cases():
    """Test edge cases like empty parents or no survivors"""
    print("\n=== Testing Edge Cases ===")
    
    # Case 1: Empty offspring (no survivors)
    parent1 = np.array([1.0, 1.0, 0.0, 0.0])
    parent2 = np.array([0.0, 1.0, 1.0, 0.0])
    offspring_empty = np.array([0.0, 0.0, 0.0, 0.0])  # No survivors
    
    print("Testing with empty offspring (0 survivors)...")
    
    parent1_list = [parent1]
    parent2_list = [parent2]
    offspring_list = [offspring_empty]
    nutrient_conditions = ['LN']
    species_numbers = [4]
    data_types = ['S']
    
    try:
        v3_results = generate_random_selection_null_v3(
            parent1_list, parent2_list, nutrient_conditions, species_numbers,
            n_permutations=5, data_types=data_types, offspring_list=offspring_list
        )
        
        print(f"V3 with 0 survivors: Generated {len(v3_results[0])} samples")
        for i, null_off in enumerate(v3_results[0]):
            survivors = np.sum(null_off > 1e-4)
            print(f"  Sample {i+1}: {survivors} survivors")
            
    except Exception as e:
        print(f"V3 failed with empty offspring: {e}")
    
    # Case 2: All species overlap
    parent1_overlap = np.array([1.0, 1.0, 0.0, 0.0])
    parent2_overlap = np.array([1.0, 1.0, 0.0, 0.0])  # Same as parent1
    offspring_overlap = np.array([1.0, 0.0, 0.0, 0.0])  # 1 survivor
    
    print("\nTesting with complete overlap between parents...")
    
    parent1_list = [parent1_overlap]
    parent2_list = [parent2_overlap]
    offspring_list = [offspring_overlap]
    
    try:
        v3_results = generate_random_selection_null_v3(
            parent1_list, parent2_list, nutrient_conditions, species_numbers,
            n_permutations=5, data_types=data_types, offspring_list=offspring_list
        )
        
        print(f"V3 with complete overlap: Generated {len(v3_results[0])} samples")
        print("(Should generate 0 samples because V3 excludes overlaps, leaving empty pool)")
        
    except Exception as e:
        print(f"V3 failed with complete overlap: {e}")

if __name__ == "__main__":
    print("Testing V3 and V4 Null Model Implementations")
    print("=" * 50)
    
    # Run all tests
    test_species_pool_construction()
    test_fixed_n_sampling()
    analyze_sampling_behavior()
    test_edge_cases()
    
    print("\n" + "=" * 50)
    print("Testing completed!")