#!/usr/bin/env python3
"""
Detailed analysis of generate_random_selection_null_base function
"""

import numpy as np

def analyze_null_generation():
    """
    Step-by-step analysis of the null model generation
    """
    print("ANALYSIS OF generate_random_selection_null_base")
    print("=" * 60)
    
    print("\n1. FUNCTION SIGNATURE AND INPUTS:")
    print("-" * 40)
    print("def generate_random_selection_null_base(parent1_list, parent2_list,")
    print("                                      nutrient_conditions, species_numbers,") 
    print("                                      n_permutations=1000, version=1)")
    print()
    print("Expected inputs:")
    print("- parent1_list: List of parent1 abundance vectors from experiments")
    print("- parent2_list: List of parent2 abundance vectors from experiments") 
    print("- nutrient_conditions: ['LN', 'MN', 'HN', ...] from experiments")
    print("- species_numbers: [6, 12, 24, ...] experimental design species pools")
    print("- n_permutations: How many null samples to generate")
    print("- version: 1 (exclude overlaps) or 2 (include overlaps)")
    
    print("\n2. STEP-BY-STEP ANALYSIS:")
    print("-" * 40)
    
    print("\nSTEP 1: Load lookup table")
    print("  lookup_table = load_empirical_probabilities(version=version)")
    print("  ✅ CORRECT: Loads version-specific probabilities")
    print("  ⚠️  ISSUE: Currently returns None (files don't exist)")
    
    print("\nSTEP 2: Generate null samples in loop")
    print("  for _ in range(n_permutations):")
    print("    ✅ CORRECT: Creates n_permutations null samples")
    
    print("\nSTEP 3: Randomly select experimental event")  
    print("    idx = np.random.randint(0, len(parent1_list))")
    print("    p1 = parent1_list[idx].copy()")
    print("    p2 = parent2_list[idx].copy()")
    print("    condition = nutrient_conditions[idx]")
    print("    sp_num = species_numbers[idx]")
    print("    ✅ CORRECT: Randomly samples from real experimental data")
    print("    ✅ CORRECT: Preserves condition and species pool from that experiment")
    
    print("\nSTEP 4: Get retention probability")
    print("    selection_prob = get_empirical_probability(condition, sp_num, lookup_table)")
    print("    ✅ CORRECT: Uses condition+species-specific probability")
    print("    ⚠️  CURRENTLY: Always returns 0.5 (no lookup table)")
    
    print("\nSTEP 5: Cap probability")
    print("    selection_prob = min(1.0, max(0.0, selection_prob))")
    print("    ✅ CORRECT: Ensures valid probability range [0,1]")
    
    print("\nSTEP 6: Combine parent communities")
    print("    combined = p1 + p2") 
    print("    ❓ POTENTIAL ISSUE: What does this addition mean?")
    
    # Simulate this step
    print("\n    SIMULATION:")
    p1 = np.array([0.5, 0.3, 0.2, 0.0])  # Parent 1: species 0,1,2 present
    p2 = np.array([0.0, 0.4, 0.0, 0.6])  # Parent 2: species 1,3 present
    combined = p1 + p2
    print(f"    p1 = {p1}")
    print(f"    p2 = {p2}") 
    print(f"    combined = {combined}")
    print(f"    ✅ INTERPRETATION: Creates species pool with all species from both parents")
    print(f"    ✅ CORRECT: Species present in both get higher values")
    
    print("\nSTEP 7: Random species selection")
    print("    n_species = len(combined)")
    print("    selection_mask = np.random.binomial(1, selection_prob, n_species)")
    print("    ❓ CRITICAL QUESTION: Is this the right selection logic?")
    
    # Simulate this step
    np.random.seed(42)
    selection_prob = 0.7
    n_species = len(combined)
    selection_mask = np.random.binomial(1, selection_prob, n_species).astype(bool)
    print(f"\n    SIMULATION (selection_prob = {selection_prob}):")
    print(f"    n_species = {n_species}")
    print(f"    selection_mask = {selection_mask}")
    print(f"    Selected species indices: {np.where(selection_mask)[0]}")
    print(f"    ✅ CORRECT: Each species independently selected with probability p")
    
    print("\nSTEP 8: Create offspring abundances")
    print("    offspring = np.zeros(n_species)")
    print("    if np.any(selection_mask):")
    print("        offspring[selection_mask] = np.random.exponential(1, np.sum(selection_mask))")
    print("        offspring = offspring / np.sum(offspring)")
    
    # Simulate this step
    offspring = np.zeros(n_species)
    if np.any(selection_mask):
        np.random.seed(42)
        offspring[selection_mask] = np.random.exponential(1, np.sum(selection_mask))
        offspring = offspring / np.sum(offspring)
    
    print(f"\n    SIMULATION:")
    print(f"    Raw exponential values: {offspring[selection_mask] * np.sum(offspring) if np.any(selection_mask) else 'None'}")
    print(f"    Final normalized offspring: {offspring}")
    print(f"    ✅ CORRECT: Selected species get random abundances, normalized to sum=1")
    
    print("\nSTEP 9: Store results") 
    print("    null_offspring_list.append(offspring)")
    print("    null_parent1_list.append(p1)")  
    print("    null_parent2_list.append(p2)")
    print("    ✅ CORRECT: Stores null offspring with original parents")
    print("    ❌ MISSING: Should also store condition and species_number!")
    
    print("\n3. OVERALL ASSESSMENT:")
    print("-" * 40)
    print("✅ STRENGTHS:")
    print("  - Uses real experimental parent communities")
    print("  - Correctly looks up condition+species-specific probabilities")  
    print("  - Proper random species selection with binomial distribution")
    print("  - Reasonable abundance assignment (exponential + normalization)")
    print("  - Preserves original parent information")
    
    print("\n❌ ISSUES IDENTIFIED:")
    print("  1. MAJOR: Doesn't return condition/species info → lost for analysis!")
    print("  2. Currently all probabilities = 0.5 (missing lookup tables)")
    print("  3. Combined = p1 + p2 might not reflect real species pool biology")
    
    print("\n🔍 BIOLOGICAL INTERPRETATION:")
    print("  The null model asks: 'What if species retention was purely random")
    print("  at empirically-observed rates, starting from real parent communities?'")
    print("  - Uses real parent compositions (preserves parent-specific effects)")
    print("  - Uses real retention rates (preserves condition-specific effects)")  
    print("  - Randomizes only WHICH species are retained (tests selectivity)")
    
    print("\n⚠️  CRITICAL MISSING PIECE:")
    print("  Function should return (offspring_list, parent1_list, parent2_list, conditions, species_nums)")
    print("  Currently only returns first 3, so condition info is LOST!")

if __name__ == "__main__":
    analyze_null_generation()