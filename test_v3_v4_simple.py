"""
Simple test script to verify V3 and V4 null model logic without importing full module
"""
import numpy as np

def generate_random_selection_null_fixed_n_test(parent1, parent2, offspring, exclude_overlaps=True, n_permutations=10):
    """
    Simplified version of the fixed-N null model generation for testing
    """
    threshold = 1e-4
    null_offspring_list = []
    
    # Count surviving species in original experimental data
    n_survivors = np.sum(offspring > threshold)
    print(f"Experimental survivors: {n_survivors}")
    
    for perm in range(n_permutations):
        # Get species present in each parent
        parent1_present = parent1 > threshold
        parent2_present = parent2 > threshold
        
        # Create species pool
        if exclude_overlaps:
            # V3: Only unique species (excluding overlaps)
            parent1_unique = parent1_present & ~parent2_present
            parent2_unique = parent2_present & ~parent1_present
            available_species = parent1_unique | parent2_unique
            model_name = "V3"
        else:
            # V4: All species (including overlaps)
            available_species = parent1_present | parent2_present
            model_name = "V4"
        
        available_indices = np.where(available_species)[0]
        print(f"{model_name} available species pool: {available_indices}")
        
        if len(available_indices) == 0 or n_survivors == 0:
            # Create empty null offspring
            null_offspring = np.zeros_like(parent1)
        else:
            # Randomly select exactly N species (matching experimental survivors)
            n_to_select = min(n_survivors, len(available_indices))
            selected_indices = np.random.choice(available_indices, 
                                              size=n_to_select, 
                                              replace=False)
            
            # Create null offspring vector
            null_offspring = np.zeros_like(parent1)
            null_offspring[selected_indices] = 1.0  # Binary presence
        
        null_offspring_list.append(null_offspring)
        
        # Show first few samples in detail
        if perm < 3:
            selected_species = np.where(null_offspring > threshold)[0]
            print(f"{model_name} Sample {perm+1}: Selected species {selected_species} (count: {len(selected_species)})")
    
    return null_offspring_list

def test_species_pool_construction():
    """Test that V3 and V4 construct species pools correctly"""
    print("=== Testing Species Pool Construction ===")
    
    # Parent 1: Species [0, 1, 2] present
    parent1 = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
    
    # Parent 2: Species [2, 3, 4] present (species 2 overlaps with parent1)
    parent2 = np.array([0.0, 0.0, 1.0, 1.0, 1.0, 0.0])
    
    # Offspring: 2 species survived ([1, 3])
    offspring = np.array([0.0, 1.0, 0.0, 1.0, 0.0, 0.0])
    
    threshold = 1e-4
    
    # Identify species in each parent
    parent1_present = parent1 > threshold
    parent2_present = parent2 > threshold
    
    print(f"Parent 1 species: {np.where(parent1_present)[0]}")
    print(f"Parent 2 species: {np.where(parent2_present)[0]}")
    print(f"Overlapping species: {np.where(parent1_present & parent2_present)[0]}")
    print(f"Experimental offspring species: {np.where(offspring > threshold)[0]}")
    
    # V3 species pool (excluding overlaps)
    parent1_unique = parent1_present & ~parent2_present
    parent2_unique = parent2_present & ~parent1_present
    v3_pool = parent1_unique | parent2_unique
    
    print(f"V3 species pool (excluding overlaps): {np.where(v3_pool)[0]}")
    
    # V4 species pool (including overlaps)
    v4_pool = parent1_present | parent2_present
    
    print(f"V4 species pool (including overlaps): {np.where(v4_pool)[0]}")
    
    return parent1, parent2, offspring

def test_fixed_n_sampling():
    """Test that both models sample exactly N species matching experimental data"""
    print("\n=== Testing Fixed-N Sampling ===")
    
    parent1, parent2, offspring = test_species_pool_construction()
    
    # Test V3
    print("\n--- Testing V3 (excluding overlaps) ---")
    np.random.seed(42)  # For reproducible results
    v3_samples = generate_random_selection_null_fixed_n_test(
        parent1, parent2, offspring, exclude_overlaps=True, n_permutations=5
    )
    
    # Verify all samples have correct number of survivors
    threshold = 1e-4
    expected_survivors = np.sum(offspring > threshold)
    actual_survivors = [np.sum(sample > threshold) for sample in v3_samples]
    print(f"V3 survivor counts: {actual_survivors}")
    print(f"All V3 samples have {expected_survivors} survivors: {all(count == expected_survivors for count in actual_survivors)}")
    
    # Test V4
    print("\n--- Testing V4 (including overlaps) ---")
    np.random.seed(42)  # For reproducible results
    v4_samples = generate_random_selection_null_fixed_n_test(
        parent1, parent2, offspring, exclude_overlaps=False, n_permutations=5
    )
    
    # Verify all samples have correct number of survivors
    actual_survivors = [np.sum(sample > threshold) for sample in v4_samples]
    print(f"V4 survivor counts: {actual_survivors}")
    print(f"All V4 samples have {expected_survivors} survivors: {all(count == expected_survivors for count in actual_survivors)}")

def test_large_scale_behavior():
    """Test behavior over many samples to check selection frequencies"""
    print("\n=== Testing Large-Scale Behavior ===")
    
    parent1 = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])  # Species [0,1,2]
    parent2 = np.array([0.0, 0.0, 1.0, 1.0, 1.0, 0.0])  # Species [2,3,4]
    offspring = np.array([0.0, 1.0, 0.0, 1.0, 0.0, 0.0])  # 2 survivors
    
    n_samples = 1000
    threshold = 1e-4
    
    print(f"Generating {n_samples} samples for statistical analysis...")
    
    # V3 analysis
    np.random.seed(123)
    v3_samples = generate_random_selection_null_fixed_n_test(
        parent1, parent2, offspring, exclude_overlaps=True, n_permutations=n_samples
    )
    
    species_counts_v3 = np.zeros(6)
    for sample in v3_samples:
        species_counts_v3 += (sample > threshold).astype(int)
    
    print(f"\nV3 Species Selection Frequencies (out of {n_samples} samples):")
    for i, count in enumerate(species_counts_v3):
        print(f"Species {i}: {count} times ({count/n_samples:.3f})")
    
    # V4 analysis
    np.random.seed(123)
    v4_samples = generate_random_selection_null_fixed_n_test(
        parent1, parent2, offspring, exclude_overlaps=False, n_permutations=n_samples
    )
    
    species_counts_v4 = np.zeros(6)
    for sample in v4_samples:
        species_counts_v4 += (sample > threshold).astype(int)
    
    print(f"\nV4 Species Selection Frequencies (out of {n_samples} samples):")
    for i, count in enumerate(species_counts_v4):
        print(f"Species {i}: {count} times ({count/n_samples:.3f})")
    
    # Analysis
    print(f"\nAnalysis:")
    print(f"V3 pool size: 4 species [0,1,3,4], selecting 2")
    print(f"Expected V3 frequency per species: {2/4:.3f} = 0.500")
    print(f"V4 pool size: 5 species [0,1,2,3,4], selecting 2") 
    print(f"Expected V4 frequency per species: {2/5:.3f} = 0.400")
    
    print(f"\nSpecies 2 (overlap) behavior:")
    print(f"V3: {species_counts_v3[2]} selections (should be 0 - excluded)")
    print(f"V4: {species_counts_v4[2]} selections (should be ~{0.4*n_samples:.0f} - included)")

def test_edge_cases():
    """Test edge cases"""
    print("\n=== Testing Edge Cases ===")
    
    # Case 1: No survivors
    parent1 = np.array([1.0, 1.0, 0.0, 0.0])
    parent2 = np.array([0.0, 1.0, 1.0, 0.0])
    offspring_empty = np.array([0.0, 0.0, 0.0, 0.0])
    
    print("Testing with 0 survivors...")
    v3_empty = generate_random_selection_null_fixed_n_test(
        parent1, parent2, offspring_empty, exclude_overlaps=True, n_permutations=3
    )
    
    print("V3 with 0 survivors completed")
    
    # Case 2: Complete overlap
    parent1_overlap = np.array([1.0, 1.0, 0.0, 0.0])
    parent2_overlap = np.array([1.0, 1.0, 0.0, 0.0])  # Same as parent1
    offspring_overlap = np.array([1.0, 0.0, 0.0, 0.0])  # 1 survivor
    
    print("\nTesting with complete overlap...")
    v3_overlap = generate_random_selection_null_fixed_n_test(
        parent1_overlap, parent2_overlap, offspring_overlap, exclude_overlaps=True, n_permutations=3
    )
    
    print("V3 with complete overlap completed")

if __name__ == "__main__":
    print("Testing V3 and V4 Null Model Logic")
    print("=" * 50)
    
    test_species_pool_construction()
    test_fixed_n_sampling()
    test_large_scale_behavior()
    test_edge_cases()
    
    print("\n" + "=" * 50)
    print("Testing completed!")