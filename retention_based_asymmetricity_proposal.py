#!/usr/bin/env python3
"""
Proposal for Retention-Based Asymmetricity Analysis

This addresses the fundamental flaws in diversity-based measures by focusing on
retention probabilities and statistically comparing them between parent communities.
"""

import numpy as np
from scipy import stats
import pandas as pd

def explain_retention_based_approach():
    """
    Comprehensive proposal for retention-based asymmetricity analysis
    """
    
    print("RETENTION-BASED ASYMMETRICITY ANALYSIS")
    print("=" * 60)
    
    print("\n🧬 CORE BIOLOGICAL QUESTION:")
    print("-" * 50)
    print("Instead of asking: 'How many species did each parent lose?'")
    print("We should ask: 'Did the two parents have significantly different")  
    print("                 species retention probabilities?'")
    print()
    print("This focuses on the MECHANISM rather than just the OUTCOME.")
    
    print(f"\n📊 RETENTION-BASED FRAMEWORK:")
    print("-" * 50)
    
    print("For each coalescence event, calculate:")
    print("1. Parent 1 retention rate: R1 = (P1 species in mixed) / (P1 total species)")
    print("2. Parent 2 retention rate: R2 = (P2 species in mixed) / (P2 total species)")  
    print("3. Test: Is |R1 - R2| significantly different from expected?")
    print()
    print("This approach:")
    print("✓ Controls for initial diversity differences")
    print("✓ Accounts for species identity and overlap")
    print("✓ Provides statistical significance testing")
    print("✓ Distinguishes biological from mathematical effects")

def demonstrate_retention_calculation():
    """Show how to calculate retention rates properly"""
    
    print(f"\n🔢 RETENTION RATE CALCULATION:")
    print("-" * 50)
    
    print("Example coalescence event:")
    print("Parent 1 species: {A, B, C, D, E} (5 species)")
    print("Parent 2 species: {C, D, F, G} (4 species)") 
    print("Mixed community: {A, C, D, F} (4 species)")
    print()
    
    # Define the communities
    parent1_species = {'A', 'B', 'C', 'D', 'E'}
    parent2_species = {'C', 'D', 'F', 'G'}  
    mixed_species = {'A', 'C', 'D', 'F'}
    
    print("Species classifications:")
    overlap = parent1_species & parent2_species
    p1_unique = parent1_species - parent2_species
    p2_unique = parent2_species - parent1_species
    
    print(f"• Overlap species: {overlap}")
    print(f"• Parent 1 unique: {p1_unique}")  
    print(f"• Parent 2 unique: {p2_unique}")
    print()
    
    # Calculate retention
    p1_retained = len(mixed_species & parent1_species)
    p2_retained = len(mixed_species & parent2_species)
    
    p1_retention = p1_retained / len(parent1_species)
    p2_retention = p2_retained / len(parent2_species)
    
    print("Retention analysis:")
    print(f"• Parent 1: {p1_retained}/{len(parent1_species)} species retained = {p1_retention:.2f}")
    print(f"• Parent 2: {p2_retained}/{len(parent2_species)} species retained = {p2_retention:.2f}")
    print(f"• Retention difference: {abs(p1_retention - p2_retention):.2f}")
    
    # Breakdown by species type
    p1_overlap_retained = len(overlap & mixed_species)
    p1_unique_retained = len(p1_unique & mixed_species)
    p2_overlap_retained = len(overlap & mixed_species)  
    p2_unique_retained = len(p2_unique & mixed_species)
    
    print(f"\nDetailed breakdown:")
    print(f"• Parent 1 overlap retention: {p1_overlap_retained}/{len(overlap)} = {p1_overlap_retained/len(overlap) if overlap else 0:.2f}")
    print(f"• Parent 1 unique retention: {p1_unique_retained}/{len(p1_unique)} = {p1_unique_retained/len(p1_unique) if p1_unique else 0:.2f}")
    print(f"• Parent 2 overlap retention: {p2_overlap_retained}/{len(overlap)} = {p2_overlap_retained/len(overlap) if overlap else 0:.2f}")  
    print(f"• Parent 2 unique retention: {p2_unique_retained}/{len(p2_unique)} = {p2_unique_retained/len(p2_unique) if p2_unique else 0:.2f}")

def propose_statistical_framework():
    """Propose statistical framework for retention-based asymmetricity"""
    
    print(f"\n📈 STATISTICAL FRAMEWORK:")
    print("-" * 50)
    
    print("LEVEL 1: Per-Event Retention Asymmetricity")
    print("• Calculate R1 and R2 for each coalescence event")
    print("• Define asymmetricity: A = |R1 - R2|")  
    print("• Range: [0, 1] where 0 = equal retention, 1 = complete asymmetricity")
    print()
    
    print("LEVEL 2: Statistical Significance Testing") 
    print("• Null hypothesis: R1 = R2 (symmetric retention)")
    print("• Test statistic: |R1 - R2|")
    print("• P-value from permutation test or bootstrap")
    print("• Multiple testing correction across events")
    print()
    
    print("LEVEL 3: Population-Level Analysis")
    print("• Aggregate retention asymmetricity by condition (LN/MN/HN)")
    print("• Test: Do conditions differ in retention asymmetricity?")
    print("• ANOVA or Kruskal-Wallis across nutrient conditions")
    print("• Effect size estimation and confidence intervals")

def propose_advanced_measures():
    """Propose more sophisticated retention-based measures"""
    
    print(f"\n🚀 ADVANCED RETENTION-BASED MEASURES:")
    print("-" * 50)
    
    print("1. SPECIES-TYPE-SPECIFIC RETENTION ASYMMETRICITY:")
    print("   • Overlap species asymmetricity: |R1_overlap - R2_overlap|") 
    print("   • Unique species asymmetricity: |R1_unique - R2_unique|")
    print("   • Hypothesis: Overlap vs unique species have different dynamics")
    print()
    
    print("2. ABUNDANCE-WEIGHTED RETENTION ASYMMETRICITY:")
    print("   • Weight retention by species' original abundances")
    print("   • R1_weighted = Σ(retained_abundance_i) / Σ(original_abundance_i)")
    print("   • Tests: Do abundant species have different retention patterns?")
    print()
    
    print("3. PHYLOGENETIC RETENTION ASYMMETRICITY:")
    print("   • Weight by phylogenetic diversity retained")  
    print("   • Account for evolutionary relationships")
    print("   • Test: Is phylogenetic diversity retained asymmetrically?")
    print()
    
    print("4. FUNCTIONAL RETENTION ASYMMETRICITY:")
    print("   • Group species by functional traits/pathways")
    print("   • Calculate retention rates per functional group") 
    print("   • Test: Are specific functions retained asymmetrically?")

def propose_implementation():
    """Propose how to implement this in the existing codebase"""
    
    print(f"\n💻 IMPLEMENTATION IN EXISTING CODEBASE:")
    print("-" * 50)
    
    print("NEW FUNCTION STRUCTURE:")
    print()
    print("def calculate_retention_asymmetricity(parent1_vector, parent2_vector, mixed_vector,")
    print("                                    threshold=1e-4, method='basic'):")
    print("    '''")
    print("    Calculate retention-based asymmetricity between two parent communities")
    print("    ")
    print("    Args:")
    print("        parent1_vector: Abundance vector for parent 1")
    print("        parent2_vector: Abundance vector for parent 2") 
    print("        mixed_vector: Abundance vector for mixed community")
    print("        threshold: Minimum abundance to consider species 'present'")
    print("        method: 'basic', 'weighted', 'species_specific'")
    print("    ")
    print("    Returns:")
    print("        dict with retention rates, asymmetricity score, and statistics")
    print("    '''")
    print()
    
    print("INTEGRATION WITH EXISTING ANALYSIS:")
    print("• Add retention_asymmetricity to AsymmetricityAnalysis.py")
    print("• Modify analyze_single_coalescence_event() to include retention measures")
    print("• Add retention-based plotting functions")  
    print("• Include retention asymmetricity in null model comparisons")
    print()
    
    print("NULL MODEL ENHANCEMENT:")
    print("• Compare experimental retention asymmetricity to null model predictions")
    print("• Test: Is observed retention asymmetricity > random expectation?")
    print("• Use same retention-based measures on null model communities")

def demonstrate_null_hypothesis_testing():
    """Show how to test statistical significance of retention asymmetricity"""
    
    print(f"\n🎯 NULL HYPOTHESIS TESTING EXAMPLE:")
    print("-" * 50)
    
    print("Observed coalescence event:")
    print("• Parent 1: 10 species → 7 retained (70% retention)")
    print("• Parent 2: 8 species → 4 retained (50% retention)")
    print("• Observed asymmetricity: |0.70 - 0.50| = 0.20")
    print()
    
    print("NULL HYPOTHESIS: Equal retention probabilities")
    print("• H0: Both parents have the same underlying retention rate")
    print("• H1: Parents have significantly different retention rates")
    print()
    
    print("PERMUTATION TEST:")
    print("1. Pool all species from both parents")
    print("2. Randomly assign species to 'parent 1' and 'parent 2' groups")
    print("3. Calculate retention rates for permuted groups")
    print("4. Repeat 1000+ times to build null distribution")
    print("5. P-value = fraction of permutations with |R1-R2| ≥ 0.20")
    print()
    
    # Simulate permutation test
    print("SIMULATED PERMUTATION TEST:")
    np.random.seed(42)
    
    # True data: 17 species total, 11 retained
    total_species = 18  # 10 + 8
    total_retained = 11  # 7 + 4
    p1_size, p2_size = 10, 8
    
    null_asymmetries = []
    for _ in range(1000):
        # Randomly assign species to parents
        all_retained = [1] * total_retained + [0] * (total_species - total_retained)
        np.random.shuffle(all_retained)
        
        p1_retained = sum(all_retained[:p1_size])
        p2_retained = sum(all_retained[p1_size:])
        
        r1_null = p1_retained / p1_size
        r2_null = p2_retained / p2_size  
        null_asymmetries.append(abs(r1_null - r2_null))
    
    observed_asymmetry = 0.20
    p_value = sum(1 for x in null_asymmetries if x >= observed_asymmetry) / 1000
    
    print(f"• Null distribution mean: {np.mean(null_asymmetries):.3f}")
    print(f"• Null distribution std: {np.std(null_asymmetries):.3f}")
    print(f"• Observed asymmetricity: {observed_asymmetry:.3f}")
    print(f"• P-value: {p_value:.3f}")
    print(f"• Result: {'Significant' if p_value < 0.05 else 'Not significant'} asymmetricity")

if __name__ == "__main__":
    explain_retention_based_approach()
    demonstrate_retention_calculation()
    propose_statistical_framework()
    propose_advanced_measures()
    propose_implementation()
    demonstrate_null_hypothesis_testing()
    
    print(f"\n🏆 SUMMARY:")
    print("=" * 60)
    print("Retention-based asymmetricity analysis provides:")
    print("✓ Unbiased comparison across different diversity levels") 
    print("✓ Statistical significance testing")
    print("✓ Mechanistic biological interpretation")
    print("✓ Species-identity and overlap awareness")
    print("✓ Integration with existing null model framework")
    print("✓ Multiple levels of analysis (per-event, population-level)")
    print()
    print("This approach transforms asymmetricity analysis from a descriptive")
    print("measure into a rigorous statistical test of biological mechanisms.")