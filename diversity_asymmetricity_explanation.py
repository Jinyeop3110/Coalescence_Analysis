#!/usr/bin/env python3
"""
Comprehensive explanation of Diversity-Based Asymmetricity Type 1 vs Type 2
"""

import numpy as np

def explain_diversity_asymmetricity():
    """
    Detailed explanation of the two types of diversity-based asymmetricity measures
    """
    
    print("DIVERSITY-BASED ASYMMETRICITY: TYPE 1 vs TYPE 2")
    print("=" * 60)
    
    print("\n📊 WHAT IS DIVERSITY-BASED ASYMMETRICITY?")
    print("-" * 50)
    print("Diversity-based asymmetricity measures how differently the two parent")
    print("communities contribute their species diversity to the mixed community.")
    print("It asks: 'Did one parent lose more species than the other during coalescence?'")
    print()
    print("Key variables:")
    print("• div1_subcom: Species richness of Parent 1")
    print("• div2_subcom: Species richness of Parent 2") 
    print("• div_mixedcom: Species richness of Mixed community (offspring)")
    
    print(f"\n🔬 CONCRETE EXAMPLE:")
    print("-" * 50)
    
    # Example data
    examples = [
        {
            'name': 'Symmetric Loss',
            'div1': 8, 'div2': 6, 'mixed': 10,
            'description': 'Both parents contribute equally'
        },
        {
            'name': 'Asymmetric Loss', 
            'div1': 10, 'div2': 4, 'mixed': 8,
            'description': 'Parent 1 dominates, Parent 2 suppressed'
        },
        {
            'name': 'No Loss (Additive)',
            'div1': 5, 'div2': 5, 'mixed': 10, 
            'description': 'Perfect species addition'
        },
        {
            'name': 'Extreme Asymmetry',
            'div1': 12, 'div2': 2, 'mixed': 6,
            'description': 'Strong competitive exclusion'
        }
    ]
    
    print("\nExample scenarios:")
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex['name']}: Parent1={ex['div1']} species, Parent2={ex['div2']} species → Mixed={ex['mixed']} species")
        print(f"     ({ex['description']})")
    
    print(f"\n📐 TYPE 1 vs TYPE 2 FORMULAS:")
    print("-" * 50)
    
    print("TYPE 1 FORMULA:")
    print("  Asymmetricity = |min(div1, div_mixed) - min(div2, div_mixed)| / div_mixed")
    print("  ")
    print("  Interpretation: How much do the parents differ in their RETAINED diversity")
    print("  relative to the total mixed community diversity")
    print("  ")
    print("  • Numerator: Difference in how much each parent 'survives' in mixture") 
    print("  • Denominator: Total diversity in mixture (absolute scale)")
    print("  • Range: [0, 1] where 0 = symmetric, 1 = completely asymmetric")
    
    print("\nTYPE 2 FORMULA:")
    print("  Asymmetricity = |min(div1, div_mixed) - min(div2, div_mixed)| / ")
    print("                  (div_mixed - min(div1, div2))")
    print("  ")
    print("  Interpretation: How much do the parents differ in their RETAINED diversity")  
    print("  relative to the NOVEL diversity gained through coalescence")
    print("  ")
    print("  • Numerator: Same as Type 1 (difference in retention)")
    print("  • Denominator: Novel species gained = mixed_diversity - smaller_parent")
    print("  • Range: [0, ∞] but typically [0, 1] in practice")
    
    print(f"\n🧮 CALCULATIONS FOR ALL EXAMPLES:")
    print("-" * 50)
    
    for i, ex in enumerate(examples, 1):
        div1, div2, mixed = ex['div1'], ex['div2'], ex['mixed']
        
        print(f"\n{i}. {ex['name']} (Parent1={div1}, Parent2={div2}, Mixed={mixed}):")
        
        # Type 1 calculation
        min1 = min(div1, mixed)
        min2 = min(div2, mixed)
        numerator = abs(min1 - min2)
        type1 = numerator / mixed if mixed > 0 else 0
        
        print(f"   TYPE 1:")
        print(f"   • min(div1, mixed) = min({div1}, {mixed}) = {min1}")
        print(f"   • min(div2, mixed) = min({div2}, {mixed}) = {min2}")
        print(f"   • |{min1} - {min2}| / {mixed} = {numerator} / {mixed} = {type1:.3f}")
        
        # Type 2 calculation  
        min_subs = min(div1, div2)
        denominator = mixed - min_subs
        type2 = numerator / denominator if denominator > 0 else 0
        
        print(f"   TYPE 2:")
        print(f"   • Numerator: {numerator} (same as Type 1)")
        print(f"   • Denominator: {mixed} - min({div1}, {div2}) = {mixed} - {min_subs} = {denominator}")
        print(f"   • {numerator} / {denominator} = {type2:.3f}" if denominator > 0 else "   • Division by zero → 0.000")
        
        print(f"   INTERPRETATION: Type1={type1:.3f}, Type2={type2:.3f}")
    
    print(f"\n🔍 KEY DIFFERENCES:")
    print("-" * 50)
    
    print("TYPE 1 (Absolute Scale):")
    print("✓ Always bounded [0, 1]")
    print("✓ Easy to interpret: fraction of total mixed diversity") 
    print("✓ Compares asymmetricity across different diversity levels")
    print("✗ May underestimate asymmetricity in high-diversity mixtures")
    print("✗ Denominator includes all mixed community diversity")
    
    print("\nTYPE 2 (Novel Diversity Scale):") 
    print("✓ Focuses on 'emergent' diversity from coalescence")
    print("✓ More sensitive to asymmetricity when little novel diversity appears")
    print("✓ Better for detecting subtle competitive effects") 
    print("✗ Can be unstable when denominator is small")
    print("✗ Not bounded (can exceed 1, though rare)")
    print("✗ Undefined when mixed diversity ≤ smaller parent diversity")
    
    print(f"\n🧬 BIOLOGICAL INTERPRETATION:")
    print("-" * 50)
    
    print("TYPE 1 asks: 'How asymmetric is species retention relative to total diversity?'")
    print("• High Type 1 = One parent strongly dominates the community composition")
    print("• Low Type 1 = Both parents contribute roughly equally to final diversity") 
    print("• Good for: Comparing asymmetricity across experiments with different diversity levels")
    
    print("\nTYPE 2 asks: 'How asymmetric is species retention relative to novel diversity gained?'")
    print("• High Type 2 = Asymmetric retention despite little novel species emergence")
    print("• Low Type 2 = Symmetric retention when many new species appear")  
    print("• Good for: Detecting competitive exclusion vs facilitation effects")
    print("• Problematic: When mixed diversity ≤ individual parent diversity (no novelty)")
    
    print(f"\n⚖️  WHEN TO USE WHICH:")
    print("-" * 50)
    
    print("Use TYPE 1 when:")
    print("• You want a standardized [0,1] asymmetricity measure")
    print("• Comparing across experiments with different diversity scales") 
    print("• You care about overall community dominance patterns")
    print("• You want robust, interpretable results")
    
    print("\nUse TYPE 2 when:")
    print("• You want to emphasize novel diversity effects")
    print("• You suspect subtle competitive interactions")
    print("• Mixed communities consistently have higher diversity than parents")
    print("• You're willing to handle edge cases and potential instability")
    
    print(f"\n🎯 RESEARCH CONTEXT:")
    print("-" * 50)
    print("In coalescence experiments:")
    print("• TYPE 1 better captures overall community assembly asymmetricity")
    print("• TYPE 2 better captures species-level interaction asymmetricity") 
    print("• Both provide complementary information about microbial community dynamics")
    print("• Choice depends on your specific biological hypothesis")

def demonstrate_edge_cases():
    """Show problematic edge cases for both measures"""
    
    print(f"\n\n⚠️  EDGE CASES AND PROBLEMS:")
    print("=" * 60)
    
    edge_cases = [
        {'name': 'Zero Mixed Diversity', 'div1': 5, 'div2': 3, 'mixed': 0},
        {'name': 'Mixed < Both Parents', 'div1': 8, 'div2': 6, 'mixed': 4},  
        {'name': 'Mixed = Smaller Parent', 'div1': 10, 'div2': 4, 'mixed': 4},
        {'name': 'One Parent = 0', 'div1': 0, 'div2': 8, 'mixed': 5},
    ]
    
    for case in edge_cases:
        div1, div2, mixed = case['div1'], case['div2'], case['mixed']
        print(f"\n{case['name']}: Parent1={div1}, Parent2={div2}, Mixed={mixed}")
        
        # Type 1
        if mixed == 0:
            type1 = 0
            print(f"  TYPE 1: 0 (division by zero handled)")
        else:
            min1, min2 = min(div1, mixed), min(div2, mixed)
            type1 = abs(min1 - min2) / mixed
            print(f"  TYPE 1: {type1:.3f}")
        
        # Type 2
        min_subs = min(div1, div2)
        denominator = mixed - min_subs
        if denominator <= 0:
            type2 = 0
            print(f"  TYPE 2: 0 (denominator ≤ 0)")
        else:
            min1, min2 = min(div1, mixed), min(div2, mixed)
            type2 = abs(min1 - min2) / denominator 
            print(f"  TYPE 2: {type2:.3f}")
    
    print(f"\n📝 SUMMARY:")
    print("Both measures handle edge cases but with different sensitivities.")
    print("Type 1 is more robust, Type 2 is more sensitive but less stable.")

if __name__ == "__main__":
    explain_diversity_asymmetricity()
    demonstrate_edge_cases()