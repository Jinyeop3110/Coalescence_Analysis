"""
Diversity Asymmetricity Analysis - Species Origin Tracking

Implements diversity asymmetricity calculations that track which species in the offspring
come from which parent, similar to retention probability analysis.

Two versions:
- Type 1: Excludes overlapping species (present in both parents)
- Type 2: Includes overlapping species (counted once)
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any

def analyze_species_origins(parent1: np.ndarray, parent2: np.ndarray, offspring: np.ndarray, 
                           threshold: float = 1e-4) -> Dict[str, Any]:
    """
    Analyze which species in offspring come from which parent.
    
    Args:
        parent1: Parent 1 abundance vector
        parent2: Parent 2 abundance vector
        offspring: Offspring abundance vector
        threshold: Abundance threshold for considering species present
        
    Returns:
        Dictionary with species origin analysis
    """
    # Convert to binary presence/absence
    p1_present = parent1 > threshold
    p2_present = parent2 > threshold
    off_present = offspring > threshold
    
    # Find species origins in offspring
    from_p1_only = off_present & p1_present & ~p2_present  # Only in parent1
    from_p2_only = off_present & p2_present & ~p1_present  # Only in parent2
    from_both = off_present & p1_present & p2_present      # In both parents (overlapping)
    novel = off_present & ~p1_present & ~p2_present        # Novel species (not in either parent)
    
    # Count species
    n_from_p1_only = np.sum(from_p1_only)
    n_from_p2_only = np.sum(from_p2_only)
    n_from_both = np.sum(from_both)
    n_novel = np.sum(novel)
    
    return {
        'from_parent1_only': n_from_p1_only,
        'from_parent2_only': n_from_p2_only,
        'from_both_parents': n_from_both,
        'novel_species': n_novel,
        'total_offspring_species': np.sum(off_present),
        'parent1_species': np.sum(p1_present),
        'parent2_species': np.sum(p2_present),
        'overlap_in_parents': np.sum(p1_present & p2_present)
    }

def calculate_diversity_asymmetricity_v1_origin_tracking(parent1: np.ndarray, parent2: np.ndarray, 
                                                        offspring: np.ndarray, threshold: float = 1e-4) -> float:
    """
    Diversity asymmetricity Type 1: Excluding overlapping species
    
    Formula: |species_from_p1_only - species_from_p2_only| / (species_from_p1_only + species_from_p2_only)
    
    This excludes species that were present in both parents from both numerator and denominator.
    
    Args:
        parent1: Parent 1 abundance vector
        parent2: Parent 2 abundance vector
        offspring: Offspring abundance vector
        threshold: Abundance threshold for considering species present
        
    Returns:
        Asymmetricity value [0, 1]
    """
    origins = analyze_species_origins(parent1, parent2, offspring, threshold)
    
    n_from_p1 = origins['from_parent1_only']
    n_from_p2 = origins['from_parent2_only']
    
    denominator = n_from_p1 + n_from_p2
    
    if denominator == 0:
        return 0.0  # No non-overlapping species retained
    
    numerator = abs(n_from_p1 - n_from_p2)
    
    return numerator / denominator

def calculate_diversity_asymmetricity_v2_origin_tracking(parent1: np.ndarray, parent2: np.ndarray, 
                                                        offspring: np.ndarray, threshold: float = 1e-4) -> float:
    """
    Diversity asymmetricity Type 2: Including overlapping species
    
    Formula: |species_from_p1_total - species_from_p2_total| / (species_from_p1_total + species_from_p2_total)
    
    Where:
    - species_from_p1_total = from_p1_only + from_both (overlapping counted for both)
    - species_from_p2_total = from_p2_only + from_both (overlapping counted for both)
    
    Args:
        parent1: Parent 1 abundance vector
        parent2: Parent 2 abundance vector
        offspring: Offspring abundance vector
        threshold: Abundance threshold for considering species present
        
    Returns:
        Asymmetricity value [0, 1]
    """
    origins = analyze_species_origins(parent1, parent2, offspring, threshold)
    
    n_from_p1_total = origins['from_parent1_only'] + origins['from_both_parents']
    n_from_p2_total = origins['from_parent2_only'] + origins['from_both_parents']
    # Fix: denominator should not double-count overlap
    denominator = origins['from_parent1_only'] + origins['from_parent2_only'] + origins['from_both_parents']
    if denominator == 0:
        return 0.0  # No species retained from either parent
    numerator = abs(n_from_p1_total - n_from_p2_total)
    return numerator / denominator

def test_diversity_asymmetricity_formulas():
    """Test the new diversity asymmetricity formulas with example data."""
    
    print("Testing Origin-Tracking Diversity Asymmetricity Formulas")
    print("=" * 60)
    
    # Test case 1: No overlap
    print("\nTest 1: No overlap between parents")
    p1 = np.array([10, 8, 0, 0, 5])  # Species 0,1,4
    p2 = np.array([0, 0, 6, 4, 0])   # Species 2,3
    off = np.array([5, 4, 3, 0, 2])  # Species 0,1,2,4 (0,1,4 from p1; 2 from p2)
    
    origins = analyze_species_origins(p1, p2, off)
    print(f"From P1 only: {origins['from_parent1_only']} (species 0,1,4)")
    print(f"From P2 only: {origins['from_parent2_only']} (species 2)")
    print(f"From both: {origins['from_both_parents']}")
    
    v1 = calculate_diversity_asymmetricity_v1_origin_tracking(p1, p2, off)
    v2 = calculate_diversity_asymmetricity_v2_origin_tracking(p1, p2, off)
    print(f"Type 1 (excluding overlap): {v1:.3f}")
    print(f"Type 2 (including overlap): {v2:.3f}")
    print(f"Expected: |3-1|/(3+1) = 0.5 for both")
    
    # Test case 2: With overlap
    print("\nTest 2: With overlap between parents")
    p1 = np.array([10, 8, 6, 0, 0])  # Species 0,1,2
    p2 = np.array([0, 4, 7, 5, 3])   # Species 1,2,3,4 (overlap: 1,2)
    off = np.array([5, 6, 4, 2, 0])  # Species 0,1,2,3 
    # Species origins: 0 from p1_only, 1,2 from both, 3 from p2_only
    
    origins = analyze_species_origins(p1, p2, off)
    print(f"From P1 only: {origins['from_parent1_only']} (species 0)")
    print(f"From P2 only: {origins['from_parent2_only']} (species 3)")
    print(f"From both: {origins['from_both_parents']} (species 1,2)")
    
    v1 = calculate_diversity_asymmetricity_v1_origin_tracking(p1, p2, off)
    v2 = calculate_diversity_asymmetricity_v2_origin_tracking(p1, p2, off)
    print(f"Type 1 (excluding overlap): {v1:.3f}")
    print(f"Type 2 (including overlap): {v2:.3f}")
    print(f"Type 1 expected: |1-1|/(1+1) = 0.0")
    print(f"Type 2 expected: |(1+2)-(1+2)|/(1+2+1+2) = 0.0")
    
    # Test case 3: Asymmetric retention
    print("\nTest 3: Asymmetric retention")
    p1 = np.array([10, 8, 6, 0, 0])  # Species 0,1,2
    p2 = np.array([0, 4, 7, 5, 3])   # Species 1,2,3,4
    off = np.array([5, 6, 4, 0, 0])  # Species 0,1,2 (mostly from p1)
    # Species origins: 0 from p1_only, 1,2 from both, 0 from p2_only
    
    origins = analyze_species_origins(p1, p2, off)
    print(f"From P1 only: {origins['from_parent1_only']} (species 0)")
    print(f"From P2 only: {origins['from_parent2_only']} (none)")
    print(f"From both: {origins['from_both_parents']} (species 1,2)")
    
    v1 = calculate_diversity_asymmetricity_v1_origin_tracking(p1, p2, off)
    v2 = calculate_diversity_asymmetricity_v2_origin_tracking(p1, p2, off)
    print(f"Type 1 (excluding overlap): {v1:.3f}")
    print(f"Type 2 (including overlap): {v2:.3f}")
    print(f"Type 1 expected: |1-0|/(1+0) = 1.0")
    print(f"Type 2 expected: |(1+2)-(0+2)|/(1+2+0+2) = |3-2|/5 = 0.2")

if __name__ == "__main__":
    test_diversity_asymmetricity_formulas()