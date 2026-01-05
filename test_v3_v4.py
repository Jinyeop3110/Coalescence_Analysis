#!/usr/bin/env python3

# Simple test to check V3/V4 generation
import sys
sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

from AsymmetricityNullModelAnalysis import load_real_coalescence_data, generate_random_selection_null_v3

print("Testing V3/V4 null model generation...")

# Load data
offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers, data_types = load_real_coalescence_data()

if offspring_list is None:
    print("ERROR: Could not load data")
    sys.exit(1)

print(f"Loaded {len(offspring_list)} experimental events")
print(f"Conditions: {set(nutrient_conditions)}")
print(f"Data types: {set(data_types)}")

# Test V3 generation with small sample
try:
    print("\nTesting V3 generation...")
    v3_results = generate_random_selection_null_v3(
        parent1_list[:5], parent2_list[:5], nutrient_conditions[:5], 
        species_numbers[:5], n_permutations=2, data_types=data_types[:5], 
        offspring_list=offspring_list[:5]
    )
    
    null_offspring_list, null_parent1_list, null_parent2_list, null_conditions, null_species_numbers = v3_results
    print(f"V3 generated {len(null_offspring_list)} null samples")
    
except Exception as e:
    print(f"ERROR in V3 generation: {e}")
    import traceback
    traceback.print_exc()