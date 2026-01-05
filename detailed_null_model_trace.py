#!/usr/bin/env python3
"""
Detailed trace of null model probability usage to verify LN 12 logic
"""

import numpy as np

def detailed_null_model_trace():
    """
    Trace through the null model logic step by step
    """
    print("DETAILED NULL MODEL TRACE")
    print("=" * 50)
    
    # Simulate the experimental data structure that would be loaded
    print("1. SIMULATED EXPERIMENTAL DATA:")
    print("-" * 30)
    
    # Example: 3 events for LN 12, 2 events for MN 6, etc.
    experimental_data = [
        # Format: (parent1_vector, parent2_vector, condition, species_pool_number)
        (np.array([0.5, 0.3, 0.2]), np.array([0.4, 0.4, 0.2]), 'LN', 12),  # LN with 12-species design
        (np.array([0.6, 0.4]), np.array([0.3, 0.7]), 'MN', 6),                # MN with 6-species design  
        (np.array([0.3, 0.3, 0.4]), np.array([0.5, 0.2, 0.3]), 'LN', 12),    # Another LN 12
        (np.array([0.2, 0.8]), np.array([0.6, 0.4]), 'HN', 6),                # HN with 6-species design
    ]
    
    # Unpack into lists (as the real code does)
    parent1_list = [item[0] for item in experimental_data]
    parent2_list = [item[1] for item in experimental_data]  
    nutrient_conditions = [item[2] for item in experimental_data]
    species_numbers = [item[3] for item in experimental_data]
    
    print(f"parent1_list: {len(parent1_list)} entries")
    print(f"nutrient_conditions: {nutrient_conditions}")
    print(f"species_numbers: {species_numbers}")
    
    print("\n2. LOOKUP TABLE (simulated):")
    print("-" * 30)
    lookup_table = {
        'LN_6': 0.65,  'LN_12': 0.70,  'LN_24': 0.75,
        'MN_6': 0.45,  'MN_12': 0.55,  'MN_24': 0.65,  
        'HN_6': 0.50,  'HN_12': 0.60,  'HN_24': 0.70,
    }
    
    for key, value in sorted(lookup_table.items()):
        print(f"  {key}: {value:.2f}")
    
    print("\n3. PROBABILITY LOOKUP FUNCTION:")
    print("-" * 30)
    
    def get_empirical_probability(nutrient_condition, species_pool_size, lookup_table):
        """Replicate the exact lookup logic"""
        print(f"    Looking up: nutrient='{nutrient_condition}', species_pool={species_pool_size}")
        
        if lookup_table is None:
            print(f"    -> No lookup table, return 0.5")
            return 0.5
        
        # Try exact match first  
        key = f"{nutrient_condition}_{species_pool_size}"
        print(f"    -> Trying key: '{key}'")
        if key in lookup_table:
            result = lookup_table[key]
            print(f"    -> Found! Returning {result}")
            return result
        
        # Try nutrient condition default
        default_key = f"{nutrient_condition}_default"  
        print(f"    -> Key not found, trying default: '{default_key}'")
        if default_key in lookup_table:
            result = lookup_table[default_key]
            print(f"    -> Found default! Returning {result}")
            return result
        
        # Ultimate fallback
        print(f"    -> No default found, returning fallback 0.5")
        return 0.5
    
    print("\n4. NULL MODEL GENERATION TRACE:")
    print("-" * 30)
    
    # Simulate a few iterations of the null model
    np.random.seed(42)  # For reproducible results
    n_permutations = 5
    
    for iteration in range(n_permutations):
        print(f"\n  ITERATION {iteration + 1}:")
        print(f"  {'=' * 20}")
        
        # This is the key line from the null model:
        idx = np.random.randint(0, len(parent1_list))
        print(f"  -> Random index selected: {idx}")
        
        # Get the data for this index
        p1 = parent1_list[idx].copy()
        p2 = parent2_list[idx].copy() 
        condition = nutrient_conditions[idx]
        sp_num = species_numbers[idx]
        
        print(f"  -> condition = '{condition}'")
        print(f"  -> sp_num = {sp_num}")
        print(f"  -> p1 shape: {p1.shape}, p2 shape: {p2.shape}")
        
        # Get probability
        selection_prob = get_empirical_probability(condition, sp_num, lookup_table)
        
        # Cap probability  
        selection_prob = min(1.0, max(0.0, selection_prob))
        print(f"  -> Final selection_prob = {selection_prob}")
        
        # Show what would happen to species selection
        combined = p1 + p2
        n_species = len(combined)
        print(f"  -> Combined vector length: {n_species}")
        
        # Simulate binomial selection (show a few random draws)
        np.random.seed(42 + iteration)  # Different seed for each iteration
        selection_mask = np.random.binomial(1, selection_prob, n_species).astype(bool)
        n_selected = np.sum(selection_mask)
        print(f"  -> Species selected: {n_selected}/{n_species} ({n_selected/n_species:.1%})")
    
    print("\n5. CRITICAL ANALYSIS:")
    print("-" * 30)
    
    print("✅ The null model DOES correctly use condition-specific probabilities:")
    print("   - LN 12 events use LN_12 probability (0.70)")
    print("   - MN 6 events use MN_6 probability (0.45)")  
    print("   - Each iteration gets the right probability for its condition")
    
    print("\n❓ POTENTIAL ISSUES TO VERIFY:")
    print("   1. Are species_numbers correctly assigned in data loading?")
    print("   2. Does species_numbers[idx] actually represent the DESIGNED species pool?")
    print("   3. Or does it represent the OBSERVED species count in that sample?")
    print("   4. Are lookup tables actually available (not just falling back to 0.5)?")
    
    print("\n🔍 KEY QUESTION:")
    print("   When the code says 'species pool 12', does it mean:")
    print("   A) The experiment was designed with a 12-species pool, OR")
    print("   B) This particular sample happens to have 12 observed species?")
    print("   The answer determines if we're using the right probabilities!")

if __name__ == "__main__":
    detailed_null_model_trace()