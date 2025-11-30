"""
Comparison of Old vs New Diversity Asymmetricity Formulas
"""

import numpy as np
from AsymmetricityAnalysis import calculate_diversity_asymmetricity_type1, calculate_diversity_asymmetricity_type2
from DiversityAsymmetricityAnalysis import (
    calculate_diversity_asymmetricity_v1_origin_tracking,
    calculate_diversity_asymmetricity_v2_origin_tracking,
    analyze_species_origins
)

def compare_formulas():
    """Compare old and new diversity asymmetricity formulas"""
    print("Diversity Asymmetricity Formula Comparison")
    print("=" * 50)
    
    # Test case: Realistic coalescence example
    print("\nTest case: Realistic coalescence scenario")
    parent1 = np.array([12, 8, 6, 4, 0, 0, 2, 0])  # Species 0,1,2,3,6 (5 species)
    parent2 = np.array([0, 3, 5, 8, 7, 4, 0, 1])   # Species 1,2,3,4,5,7 (6 species)
    offspring = np.array([6, 5, 4, 6, 2, 0, 1, 0]) # Species 0,1,2,3,4,6 (6 species)
    
    # Species origins analysis
    origins = analyze_species_origins(parent1, parent2, offspring, threshold=1e-4)
    print(f"Parent 1 species: {np.sum(parent1 > 1e-4)} (indices: {np.where(parent1 > 1e-4)[0].tolist()})")
    print(f"Parent 2 species: {np.sum(parent2 > 1e-4)} (indices: {np.where(parent2 > 1e-4)[0].tolist()})")
    print(f"Offspring species: {np.sum(offspring > 1e-4)} (indices: {np.where(offspring > 1e-4)[0].tolist()})")
    print(f"Species from parent 1 only: {origins['from_parent1_only']} (species 0)")
    print(f"Species from parent 2 only: {origins['from_parent2_only']} (species 4)")
    print(f"Species from both parents: {origins['from_both_parents']} (species 1,2,3)")
    print(f"Novel species: {origins['novel_species']} (species 6)")
    
    # Calculate with old formulas
    div1 = np.sum(parent1 > 1e-4)
    div2 = np.sum(parent2 > 1e-4) 
    div_off = np.sum(offspring > 1e-4)
    
    old_type1 = calculate_diversity_asymmetricity_type1(div1, div2, div_off)
    old_type2 = calculate_diversity_asymmetricity_type2(div1, div2, div_off)
    
    # Calculate with new formulas
    new_type1 = calculate_diversity_asymmetricity_v1_origin_tracking(parent1, parent2, offspring)
    new_type2 = calculate_diversity_asymmetricity_v2_origin_tracking(parent1, parent2, offspring)
    
    print(f"\nOLD FORMULAS:")
    print(f"Type 1 (old): {old_type1:.3f}")
    print(f"  Formula: |min({div1},{div_off}) - min({div2},{div_off})| / {div_off}")
    print(f"  Calculation: |min(5,6) - min(6,6)| / 6 = |5-6|/6 = {old_type1:.3f}")
    
    print(f"Type 2 (old): {old_type2:.3f}")
    print(f"  Formula: |min({div1},{div_off}) - min({div2},{div_off})| / ({div_off} - min({div1},{div2}))")
    print(f"  Calculation: |5-6| / (6-5) = 1/1 = {old_type2:.3f}")
    
    print(f"\nNEW FORMULAS (Origin-Tracking):")
    print(f"Type 1 (new): {new_type1:.3f}")
    print(f"  Formula: |spp_from_p1_only - spp_from_p2_only| / (spp_from_p1_only + spp_from_p2_only)")
    print(f"  Calculation: |1 - 1| / (1 + 1) = 0/2 = {new_type1:.3f}")
    
    print(f"Type 2 (new): {new_type2:.3f}")
    print(f"  Formula: |spp_from_p1_total - spp_from_p2_total| / (spp_from_p1_total + spp_from_p2_total)")
    print(f"  Calculation: |(1+3) - (1+3)| / (1+3 + 1+3) = |4-4|/8 = {new_type2:.3f}")
    
    print(f"\nINTERPRETATION:")
    print(f"Old formulas: Focus on diversity counts with min() constraints")
    print(f"New formulas: Focus on species origin asymmetry")
    print(f"- Type 1 (new): Symmetric retention of unique species (1 from each parent)")
    print(f"- Type 2 (new): Symmetric total retention (4 species traced to each parent)")

if __name__ == "__main__":
    compare_formulas()