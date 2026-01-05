#!/usr/bin/env python3
"""
Concrete example showing what the null model now returns
"""

import numpy as np

def demonstrate_null_model_outcome():
    """Show exactly what the fixed null model returns"""
    
    print("NULL MODEL RETURN VALUES - CONCRETE EXAMPLE")
    print("=" * 60)
    
    print("\n1. EXAMPLE EXPERIMENTAL DATA INPUT:")
    print("-" * 40)
    
    # Simulate what gets passed to the null model
    experimental_data = {
        'parent1_list': [
            np.array([0.5, 0.3, 0.2, 0.0]),  # Event 1: LN 12
            np.array([0.4, 0.6, 0.0, 0.0]),  # Event 2: MN 6  
            np.array([0.3, 0.2, 0.3, 0.2]),  # Event 3: HN 24
            np.array([0.6, 0.2, 0.2, 0.0]),  # Event 4: LN 12
        ],
        'parent2_list': [
            np.array([0.2, 0.4, 0.3, 0.1]),  # Event 1
            np.array([0.3, 0.7, 0.0, 0.0]),  # Event 2
            np.array([0.4, 0.3, 0.2, 0.1]),  # Event 3  
            np.array([0.3, 0.5, 0.1, 0.1]),  # Event 4
        ],
        'nutrient_conditions': ['LN', 'MN', 'HN', 'LN'],
        'species_numbers': [12, 6, 24, 12]
    }
    
    for i, (p1, p2, condition, sp_num) in enumerate(zip(
        experimental_data['parent1_list'],
        experimental_data['parent2_list'], 
        experimental_data['nutrient_conditions'],
        experimental_data['species_numbers']
    )):
        print(f"  Event {i+1}: {condition} {sp_num} - Parent1={p1} Parent2={p2}")
    
    print(f"\nTotal experimental events: {len(experimental_data['parent1_list'])}")
    
    print("\n2. NULL MODEL GENERATION PROCESS:")
    print("-" * 40)
    
    # Simulate the null model generation process
    np.random.seed(42)  # For reproducible example
    n_permutations = 8
    
    print(f"Generating {n_permutations} null samples...")
    print("\nFor each null sample, the model:")
    print("  1. Randomly selects one experimental event") 
    print("  2. Uses THAT event's condition (LN/MN/HN) and species pool (6/12/24)")
    print("  3. Looks up the retention probability for that specific condition")
    print("  4. Generates null offspring using random species selection")
    print("  5. PRESERVES the original condition and species pool information")
    
    # Simulate what happens in each iteration
    simulated_results = {
        'null_offspring_list': [],
        'null_parent1_list': [],
        'null_parent2_list': [],
        'null_conditions': [],
        'null_species_numbers': []
    }
    
    print(f"\n3. SIMULATED NULL SAMPLE GENERATION:")
    print("-" * 40)
    
    for perm in range(n_permutations):
        # This is what happens in the real function
        idx = np.random.randint(0, len(experimental_data['parent1_list']))
        
        selected_condition = experimental_data['nutrient_conditions'][idx]
        selected_species_num = experimental_data['species_numbers'][idx]
        selected_p1 = experimental_data['parent1_list'][idx]
        selected_p2 = experimental_data['parent2_list'][idx]
        
        print(f"  Null sample {perm+1}: Selected experimental event {idx+1} → {selected_condition} {selected_species_num}")
        
        # Simulate retention probability lookup
        prob_lookup = {
            ('LN', 12): 0.70, ('MN', 6): 0.45, ('HN', 24): 0.70,
            ('LN', 6): 0.65, ('MN', 12): 0.55, ('HN', 12): 0.60
        }
        retention_prob = prob_lookup.get((selected_condition, selected_species_num), 0.50)
        print(f"    → Uses retention probability: {retention_prob}")
        
        # Create a mock null offspring (simplified)
        mock_offspring = np.array([0.4, 0.3, 0.3, 0.0])  # Just for illustration
        
        # This is what gets stored
        simulated_results['null_offspring_list'].append(mock_offspring)
        simulated_results['null_parent1_list'].append(selected_p1)
        simulated_results['null_parent2_list'].append(selected_p2)
        simulated_results['null_conditions'].append(selected_condition)
        simulated_results['null_species_numbers'].append(selected_species_num)
    
    print(f"\n4. FINAL NULL MODEL RETURN VALUES:")
    print("-" * 40)
    print("The function now returns a 5-tuple:")
    print()
    print("📦 RETURNED TUPLE:")
    print("  (null_offspring_list, null_parent1_list, null_parent2_list,")
    print("   null_conditions, null_species_numbers)")
    print()
    print("📋 CONTENTS:")
    print(f"  • null_offspring_list: {len(simulated_results['null_offspring_list'])} null community vectors")
    print(f"  • null_parent1_list: {len(simulated_results['null_parent1_list'])} parent1 vectors (for comparison)")
    print(f"  • null_parent2_list: {len(simulated_results['null_parent2_list'])} parent2 vectors (for comparison)") 
    print(f"  • null_conditions: {simulated_results['null_conditions']}")
    print(f"  • null_species_numbers: {simulated_results['null_species_numbers']}")
    
    print(f"\n5. KEY IMPROVEMENTS:")
    print("-" * 40)
    print("🔥 BEFORE (broken):")
    print("  • Function returned: (offspring, parent1, parent2)")
    print("  • Condition info was LOST after generation")
    print("  • Statistical analysis used dummy 'NULL' conditions")  
    print("  • Couldn't do condition-matched comparisons")
    print()
    print("✅ AFTER (fixed):")
    print("  • Function returns: (offspring, parent1, parent2, conditions, species_nums)")
    print("  • Condition info is PRESERVED throughout analysis")
    print("  • Statistical analysis can compare LN-exp vs LN-null, MN-exp vs MN-null, etc.")
    print("  • Proper condition-matched hypothesis testing")
    
    print(f"\n6. STATISTICAL ANALYSIS IMPACT:")
    print("-" * 40)
    
    # Show condition distribution
    condition_counts = {}
    for condition in simulated_results['null_conditions']:
        condition_counts[condition] = condition_counts.get(condition, 0) + 1
    
    print("Null sample condition distribution:")
    for condition, count in condition_counts.items():
        print(f"  • {condition}: {count} samples ({count/len(simulated_results['null_conditions']):.1%})")
    
    print()
    print("This enables proper statistical tests like:")
    print("  • Mann-Whitney U test: LN experimental vs LN null")
    print("  • Mann-Whitney U test: MN experimental vs MN null") 
    print("  • Mann-Whitney U test: HN experimental vs HN null")
    print("  • Instead of meaningless: ALL experimental vs ALL null")

if __name__ == "__main__":
    demonstrate_null_model_outcome()