"""
CalculateEmpiricalRetentionProbabilities.py - Calculate empirical species retention probabilities

This module calculates empirical species retention probabilities from experimental data
for different nutrient conditions (LN, MN, HN) and species pool sizes (6, 12, 24).

The retention probability represents the fraction of species from the parent communities
that survive in the offspring community after coalescence.

Author: Gore Lab Coalescence Analysis Team
Date: January 2025
"""

import numpy as np
import pandas as pd
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Import common setup for data loading (avoiding matplotlib import from AsymmetricityAnalysis)
import sys
sys.path.append('.')

def load_real_coalescence_data():
    """
    Load real experimental coalescence data directly from common_setup.
    """
    try:
        # Import existing data from common_setup
        from common_setup import Coalescence_data
        
        # Load processed sequences data directly
        import pandas as pd
        Processed_sequences_synthetic_path ="../../Postprocessed/processed_Sequences_synthetic.xlsx"
        Processed_sequences_natural_path ="../../Postprocessed/processed_Sequences_natural.xlsx"
        
        sequences_synthetic = pd.read_excel(Processed_sequences_synthetic_path)
        sequences_natural = pd.read_excel(Processed_sequences_natural_path)
        processed_sequences = pd.concat([sequences_synthetic, sequences_natural])
        
    except ImportError as e:
        print(f"Error importing data: {e}")
        return None, None, None, None, None
    except Exception as e:
        print(f"Error loading processed sequences: {e}")
        return None, None, None, None, None
    
    offspring_list = []
    parent1_list = []
    parent2_list = []
    nutrient_conditions = []
    species_numbers = []
    
    print("Loading real coalescence data using processed sequences...")
    
    # Iterate through coalescence data and get abundance vectors from processed sequences
    # FILTER: Only process synthetic coalescence data (controlled species pools)
    for idx, row in Coalescence_data.iterrows():
        try:
            # Skip non-synthetic data
            if row['CommunityOrigin'] != 'S' or row['CoalescenceType'] != 'C':
                continue
                
            # Get medium and convert to our format
            medium = row['Medium']
            nutrient_mapping = {'L': 'LN', 'M': 'MN', 'H': 'HN'}
            nutrient_condition = nutrient_mapping.get(medium)
            
            if nutrient_condition is None:
                continue
            
            # Get sample IDs
            mixture_sample_id = row['SampleIDX']
            parent1_sample_id = row['SampleIDX_Sub1']
            parent2_sample_id = row['SampleIDX_Sub2']
            
            # Find corresponding rows in processed sequences data
            mixture_rows = processed_sequences[processed_sequences['SampleIDX'] == mixture_sample_id]
            parent1_rows = processed_sequences[processed_sequences['SampleIDX'] == parent1_sample_id]
            parent2_rows = processed_sequences[processed_sequences['SampleIDX'] == parent2_sample_id]
            
            if mixture_rows.empty or parent1_rows.empty or parent2_rows.empty:
                continue
            
            # Extract community vectors
            mixture_vector = mixture_rows.iloc[0, 1:].values.astype(float)
            parent1_vector = parent1_rows.iloc[0, 1:].values.astype(float)
            parent2_vector = parent2_rows.iloc[0, 1:].values.astype(float)
            
            # Clean and normalize
            mixture_vector = np.nan_to_num(mixture_vector, 0)
            parent1_vector = np.nan_to_num(parent1_vector, 0)
            parent2_vector = np.nan_to_num(parent2_vector, 0)
            
            # Apply threshold and normalize
            threshold = 1e-4
            mixture_vector = mixture_vector * (mixture_vector > threshold)
            parent1_vector = parent1_vector * (parent1_vector > threshold)
            parent2_vector = parent2_vector * (parent2_vector > threshold)
            
            # Normalize
            if np.sum(mixture_vector) > 0:
                mixture_vector = mixture_vector / np.sum(mixture_vector)
            if np.sum(parent1_vector) > 0:
                parent1_vector = parent1_vector / np.sum(parent1_vector)
            if np.sum(parent2_vector) > 0:
                parent2_vector = parent2_vector / np.sum(parent2_vector)
            
            # Count final observed species
            n_observed_species = np.sum(mixture_vector > 0)
            
            # Get experimental design species pool number (guaranteed to exist for synthetic data)
            community_idx = row['CommunityIDX']
            if community_idx <= 14:
                experimental_species_pool = 6
            elif community_idx <= 41:
                experimental_species_pool = 12
            elif community_idx <= 47:
                experimental_species_pool = 24
            else:
                # Skip if community_idx is outside expected range
                continue
            
            # Only include valid samples
            if (n_observed_species >= 3 and 
                np.sum(mixture_vector) > 0 and 
                np.sum(parent1_vector) > 0 and 
                np.sum(parent2_vector) > 0):
                
                offspring_list.append(mixture_vector)
                parent1_list.append(parent1_vector)
                parent2_list.append(parent2_vector)
                nutrient_conditions.append(nutrient_condition)
                species_numbers.append(experimental_species_pool)
            
        except Exception as e:
            continue
    
    print(f"Successfully loaded {len(offspring_list)} coalescence events")
    if len(offspring_list) > 0:
        print(f"Nutrient distribution: LN={nutrient_conditions.count('LN')}, MN={nutrient_conditions.count('MN')}, HN={nutrient_conditions.count('HN')}")
        print(f"Species range: {min(species_numbers)} - {max(species_numbers)}")
    
    return offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers

def calculate_species_retention_probability_v1(parent1, parent2, offspring, threshold=1e-4):
    """
    Calculate retention probability VERSION 1: Exclude overlapping species from both numerator and denominator.
    
    Retention probability = (# non-overlapping species retained in offspring) / (# non-overlapping species in parents)
    
    This excludes overlapping species between parents since they are guaranteed to be "retained".
    We only measure retention of species that are unique to one parent or the other.
    
    Args:
        parent1, parent2: Parent community abundance vectors
        offspring: Offspring community abundance vector
        threshold: Abundance threshold for presence/absence
    
    Returns:
        retention_probability: Fraction of non-overlapping parent species retained in offspring
        n_nonoverlapping_parents: Number of non-overlapping species in parent communities
        n_nonoverlapping_offspring: Number of non-overlapping species retained in offspring
    """
    # Determine species presence/absence
    parent1_present = parent1 > threshold
    parent2_present = parent2 > threshold
    offspring_present = offspring > threshold
    
    # Find non-overlapping species (unique to one parent)
    parent1_unique = parent1_present & (~parent2_present)
    parent2_unique = parent2_present & (~parent1_present)
    nonoverlapping_parents = parent1_unique | parent2_unique
    
    n_nonoverlapping_parents = np.sum(nonoverlapping_parents)
    
    # Find non-overlapping species that are retained in offspring
    nonoverlapping_retained = nonoverlapping_parents & offspring_present
    n_nonoverlapping_offspring = np.sum(nonoverlapping_retained)
    
    # Calculate retention probability based on non-overlapping species only
    if n_nonoverlapping_parents > 0:
        retention_probability = n_nonoverlapping_offspring / n_nonoverlapping_parents
    else:
        retention_probability = 1.0  # All species retained by default
    
    return retention_probability, n_nonoverlapping_parents, n_nonoverlapping_offspring

def calculate_species_retention_probability_v2(parent1, parent2, offspring, threshold=1e-4):
    """
    Calculate retention probability VERSION 2: Include overlapping species in both numerator and denominator,
    but count them only once (not twice).
    
    Retention probability = (# total unique species retained in offspring) / (# total unique species in parents)
    
    This includes all species but counts overlapping species only once in both numerator and denominator.
    
    Args:
        parent1, parent2: Parent community abundance vectors
        offspring: Offspring community abundance vector
        threshold: Abundance threshold for presence/absence
    
    Returns:
        retention_probability: Fraction of total unique parent species retained in offspring
        n_total_parents: Total number of unique species in parent communities (union)
        n_total_offspring: Total number of species in offspring
    """
    # Determine species presence/absence
    parent1_present = parent1 > threshold
    parent2_present = parent2 > threshold
    offspring_present = offspring > threshold
    
    # Find total unique species in parents (union - counts overlapping species only once)
    total_parent_species = parent1_present | parent2_present
    n_total_parents = np.sum(total_parent_species)
    
    # Find total species in offspring
    n_total_offspring = np.sum(offspring_present)
    
    # Calculate retention probability based on total unique species
    if n_total_parents > 0:
        retention_probability = n_total_offspring / n_total_parents
    else:
        retention_probability = 0.0  # No species to retain
    
    return retention_probability, n_total_parents, n_total_offspring

def calculate_species_retention_probability_parentwise_v1(parent1, parent2, offspring, threshold=1e-4):
    """
    Calculate retention probability PARENT-WISE VERSION 1: Calculate retention for each parent separately,
    excluding overlapping species from each parent, then average the two retention probabilities.
    
    P1_retention = |P1 unique species retained| / |P1 unique species|
    P2_retention = |P2 unique species retained| / |P2 unique species|
    Final P = (P1_retention + P2_retention) / 2
    
    Args:
        parent1, parent2: Parent community abundance vectors
        offspring: Offspring community abundance vector
        threshold: Abundance threshold for presence/absence
    
    Returns:
        retention_probability: Average of P1 and P2 retention probabilities
        n_p1_unique: Number of unique species in parent1
        n_p2_unique: Number of unique species in parent2
        p1_retention: Individual retention probability for parent1
        p2_retention: Individual retention probability for parent2
    """
    # Determine species presence/absence
    parent1_present = parent1 > threshold
    parent2_present = parent2 > threshold
    offspring_present = offspring > threshold
    
    # Find unique species for each parent (excluding overlaps)
    parent1_unique = parent1_present & (~parent2_present)
    parent2_unique = parent2_present & (~parent1_present)
    
    n_p1_unique = np.sum(parent1_unique)
    n_p2_unique = np.sum(parent2_unique)
    
    # Calculate retention for each parent separately
    if n_p1_unique > 0:
        p1_retained = np.sum(parent1_unique & offspring_present)
        p1_retention = p1_retained / n_p1_unique
    else:
        p1_retention = 1.0  # No unique species to lose
    
    if n_p2_unique > 0:
        p2_retained = np.sum(parent2_unique & offspring_present)
        p2_retention = p2_retained / n_p2_unique
    else:
        p2_retention = 1.0  # No unique species to lose
    
    # Average the two retention probabilities
    retention_probability = (p1_retention + p2_retention) / 2
    
    return retention_probability, n_p1_unique, n_p2_unique, p1_retention, p2_retention

def calculate_species_retention_probability_parentwise_v2(parent1, parent2, offspring, threshold=1e-4):
    """
    Calculate retention probability PARENT-WISE VERSION 2: Calculate retention for each parent separately,
    including all species in each parent (overlaps counted in both), then average the two retention probabilities.
    
    P1_retention = |P1 species retained| / |P1 total species|
    P2_retention = |P2 species retained| / |P2 total species|
    Final P = (P1_retention + P2_retention) / 2
    
    Args:
        parent1, parent2: Parent community abundance vectors
        offspring: Offspring community abundance vector
        threshold: Abundance threshold for presence/absence
    
    Returns:
        retention_probability: Average of P1 and P2 retention probabilities
        n_p1_total: Total number of species in parent1
        n_p2_total: Total number of species in parent2
        p1_retention: Individual retention probability for parent1
        p2_retention: Individual retention probability for parent2
    """
    # Determine species presence/absence
    parent1_present = parent1 > threshold
    parent2_present = parent2 > threshold
    offspring_present = offspring > threshold
    
    n_p1_total = np.sum(parent1_present)
    n_p2_total = np.sum(parent2_present)
    
    # Calculate retention for each parent separately
    if n_p1_total > 0:
        p1_retained = np.sum(parent1_present & offspring_present)
        p1_retention = p1_retained / n_p1_total
    else:
        p1_retention = 0.0  # No species to retain
    
    if n_p2_total > 0:
        p2_retained = np.sum(parent2_present & offspring_present)
        p2_retention = p2_retained / n_p2_total
    else:
        p2_retention = 0.0  # No species to retain
    
    # Average the two retention probabilities
    retention_probability = (p1_retention + p2_retention) / 2
    
    return retention_probability, n_p1_total, n_p2_total, p1_retention, p2_retention

def calculate_species_retention_probability(parent1, parent2, offspring, threshold=1e-4, version=1, parentwise=False):
    """
    Calculate species retention probability using specified version.
    
    Args:
        parent1, parent2: Parent community abundance vectors
        offspring: Offspring community abundance vector
        threshold: Abundance threshold for presence/absence
        version: 1 for excluding overlaps, 2 for including overlaps (counted once)
        parentwise: If True, use parent-wise calculation (calculate for each parent separately then average)
    
    Returns:
        Tuple of (retention_probability, n_parent_species, n_offspring_species)
        For parentwise=True, returns (retention_probability, n_p1_species, n_p2_species, p1_retention, p2_retention)
    """
    if parentwise:
        if version == 1:
            return calculate_species_retention_probability_parentwise_v1(parent1, parent2, offspring, threshold)
        elif version == 2:
            return calculate_species_retention_probability_parentwise_v2(parent1, parent2, offspring, threshold)
        else:
            raise ValueError("Version must be 1 or 2")
    else:
        if version == 1:
            return calculate_species_retention_probability_v1(parent1, parent2, offspring, threshold)
        elif version == 2:
            return calculate_species_retention_probability_v2(parent1, parent2, offspring, threshold)
        else:
            raise ValueError("Version must be 1 or 2")

def calculate_empirical_probabilities_by_condition(offspring_list, parent1_list, parent2_list,
                                                  nutrient_conditions, species_numbers,
                                                  threshold=1e-4, version=1, parentwise=False):
    """
    Calculate empirical retention probabilities grouped by nutrient condition and species pool size.
    
    Args:
        version: 1 for excluding overlaps, 2 for including overlaps (counted once)
        parentwise: If True, use parent-wise calculation (calculate for each parent separately then average)
    
    Returns:
        Dictionary with structure:
        {
            ('LN', 6): {'probabilities': [...], 'mean': x, 'std': y, 'n': z},
            ('LN', 12): {...},
            ...
        }
    """
    if parentwise:
        results = defaultdict(lambda: {'probabilities': [], 'parent1_species': [], 'parent2_species': [], 'p1_retentions': [], 'p2_retentions': []})
    else:
        results = defaultdict(lambda: {'probabilities': [], 'parent_species': [], 'offspring_species': []})
    
    # Process each coalescence event
    for i, (offspring, parent1, parent2, nutrient, sp_num) in enumerate(
        zip(offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers)):
        
        # Calculate retention probability
        if parentwise:
            retention_prob, n_p1_species, n_p2_species, p1_retention, p2_retention = calculate_species_retention_probability(
                parent1, parent2, offspring, threshold, version, parentwise=True
            )
            
            # Store by condition and species number
            key = (nutrient, sp_num)
            results[key]['probabilities'].append(retention_prob)
            results[key]['parent1_species'].append(n_p1_species)
            results[key]['parent2_species'].append(n_p2_species)
            results[key]['p1_retentions'].append(p1_retention)
            results[key]['p2_retentions'].append(p2_retention)
        else:
            retention_prob, n_parent_species, n_offspring_species = calculate_species_retention_probability(
                parent1, parent2, offspring, threshold, version, parentwise=False
            )
            
            # Store by condition and species number
            key = (nutrient, sp_num)
            results[key]['probabilities'].append(retention_prob)
            results[key]['parent_species'].append(n_parent_species)
            results[key]['offspring_species'].append(n_offspring_species)
    
    # Calculate summary statistics
    summary = {}
    for key, data in results.items():
        probabilities = np.array(data['probabilities'])
        base_summary = {
            'probabilities': probabilities,
            'mean': np.mean(probabilities),
            'std': np.std(probabilities),
            'median': np.median(probabilities),
            'n': len(probabilities)
        }
        
        if parentwise:
            base_summary.update({
                'parent1_species_mean': np.mean(data['parent1_species']),
                'parent2_species_mean': np.mean(data['parent2_species']),
                'p1_retention_mean': np.mean(data['p1_retentions']),
                'p2_retention_mean': np.mean(data['p2_retentions']),
                'p1_retention_std': np.std(data['p1_retentions']),
                'p2_retention_std': np.std(data['p2_retentions'])
            })
        else:
            base_summary.update({
                'parent_species_mean': np.mean(data['parent_species']),
                'offspring_species_mean': np.mean(data['offspring_species'])
            })
        
        summary[key] = base_summary
    
    return summary

def plot_retention_probabilities(empirical_probs, save_path=None):
    """
    Plot empirical retention probabilities by condition and species pool size.
    Note: Plotting temporarily disabled due to matplotlib compatibility issues.
    """
    print("Plotting temporarily disabled due to matplotlib compatibility issues.")
    print("Empirical probabilities calculated successfully - see summary table below.")

def create_probability_lookup_table(empirical_probs):
    """
    Create a lookup table for easy access to retention probabilities.
    
    Returns:
        Dictionary with (nutrient, species_pool) as keys and mean probability as values
    """
    lookup = {}
    for key, stats in empirical_probs.items():
        lookup[key] = stats['mean']
    
    # Also create a default lookup with just nutrient conditions (averaging across species pools)
    nutrient_defaults = defaultdict(list)
    for (nutrient, sp_num), stats in empirical_probs.items():
        nutrient_defaults[nutrient].extend(stats['probabilities'])
    
    for nutrient, probs in nutrient_defaults.items():
        lookup[(nutrient, 'default')] = np.mean(probs)
    
    return lookup

def save_probability_results(empirical_probs, lookup_table, save_dir='./'):
    """
    Save the calculated probabilities to files for later use.
    """
    import os
    import json
    
    # Create save directory if needed
    os.makedirs(save_dir, exist_ok=True)
    
    # Save detailed results as CSV
    detailed_data = []
    for (nutrient, sp_num), stats in empirical_probs.items():
        base_data = {
            'Nutrient': nutrient,
            'Species_Pool': sp_num,
            'Mean_Probability': stats['mean'],
            'Std_Probability': stats['std'],
            'Median_Probability': stats['median'],
            'N_Samples': stats['n']
        }
        
        # Add parent-wise specific columns if available
        if 'parent1_species_mean' in stats:
            base_data.update({
                'Mean_Parent1_Species': stats['parent1_species_mean'],
                'Mean_Parent2_Species': stats['parent2_species_mean'],
                'P1_Retention_Mean': stats['p1_retention_mean'],
                'P2_Retention_Mean': stats['p2_retention_mean'],
                'P1_Retention_Std': stats['p1_retention_std'],
                'P2_Retention_Std': stats['p2_retention_std']
            })
        else:
            base_data.update({
                'Mean_Parent_Species': stats['parent_species_mean'],
                'Mean_Offspring_Species': stats['offspring_species_mean']
            })
        
        detailed_data.append(base_data)
    
    detailed_df = pd.DataFrame(detailed_data)
    detailed_df.to_csv(f'{save_dir}/empirical_retention_probabilities_summary.csv', index=False)
    
    # Save lookup table as JSON for easy loading
    # Convert tuple keys to strings for JSON serialization
    json_lookup = {}
    for (nutrient, sp_num), prob in lookup_table.items():
        key_str = f"{nutrient}_{sp_num}"
        json_lookup[key_str] = prob
    
    with open(f'{save_dir}/retention_probability_lookup.json', 'w') as f:
        json.dump(json_lookup, f, indent=2)
    
    print(f"Saved probability results to {save_dir}")
    print(f"  - Summary CSV: empirical_retention_probabilities_summary.csv")
    print(f"  - Lookup JSON: retention_probability_lookup.json")

def print_probability_summary(empirical_probs):
    """
    Print a summary table of retention probabilities.
    """
    print("\n" + "="*80)
    print("EMPIRICAL SPECIES RETENTION PROBABILITIES")
    print("="*80)
    
    # Organize by nutrient condition
    nutrients = ['LN', 'MN', 'HN']
    species_pools = sorted(set(sp for _, sp in empirical_probs.keys()))
    
    # Print header
    header = "Condition" + "".join(f"\t{sp}sp" for sp in species_pools)
    print(header)
    print("-" * 80)
    
    # Print data
    for nutrient in nutrients:
        row = f"{nutrient}"
        for sp in species_pools:
            key = (nutrient, sp)
            if key in empirical_probs:
                mean_prob = empirical_probs[key]['mean']
                std_prob = empirical_probs[key]['std']
                n_samples = empirical_probs[key]['n']
                row += f"\t{mean_prob:.3f}±{std_prob:.3f} (n={n_samples})"
            else:
                row += "\t-"
        print(row)
    
    print("\n" + "="*80)

def run_empirical_probability_analysis(save_plots=True, save_results=True, version=1, parentwise=False):
    """
    Main function to run the complete empirical probability analysis.
    
    Args:
        version: 1 for excluding overlaps, 2 for including overlaps (counted once)
        parentwise: If True, use parent-wise calculation (calculate for each parent separately then average)
    """
    print("Loading experimental coalescence data...")
    offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers = load_real_coalescence_data()
    
    if not offspring_list:
        print("No data found!")
        return None
    
    print(f"Loaded {len(offspring_list)} coalescence events")
    
    # Calculate empirical probabilities for specified version
    version_name = "excluding_overlaps" if version == 1 else "including_overlaps"
    method_name = "parent-wise" if parentwise else "union-based"
    print(f"Calculating empirical retention probabilities (Version {version}: {version_name}, Method: {method_name})...")
    
    empirical_probs = calculate_empirical_probabilities_by_condition(
        offspring_list, parent1_list, parent2_list,
        nutrient_conditions, species_numbers,
        threshold=1e-4, version=version, parentwise=parentwise
    )
    
    # Create lookup table
    lookup_table = create_probability_lookup_table(empirical_probs)
    
    # Print summary
    print_probability_summary(empirical_probs)
    
    # Plot results
    if save_plots:
        plot_retention_probabilities(empirical_probs, 
                                   save_path=f'Figure/AsymmetricityAnalysis/empirical_retention_probabilities_v{version}.png')
    
    # Save results
    if save_results:
        save_probability_results(empirical_probs, lookup_table, 
                               save_dir=f'Figure/AsymmetricityAnalysis/version_{version}')
    
    return empirical_probs, lookup_table

def run_parentwise_vs_union_comparison(version=1, save_plots=False, save_results=False):
    """
    Compare parent-wise vs union-based calculation methods for a given version.
    
    Args:
        version: 1 for excluding overlaps, 2 for including overlaps
        save_plots: Whether to save plots
        save_results: Whether to save results to files
    """
    print("="*80)
    print(f"COMPARING PARENT-WISE vs UNION-BASED METHODS (Version {version})")
    print("="*80)
    
    # Union-based calculation (current method)
    print(f"\nUnion-based V{version} calculation:")
    empirical_probs_union, lookup_union = run_empirical_probability_analysis(
        save_plots=save_plots, save_results=save_results, version=version, parentwise=False
    )
    
    # Parent-wise calculation (new method)
    print(f"\nParent-wise V{version} calculation:")
    empirical_probs_parentwise, lookup_parentwise = run_empirical_probability_analysis(
        save_plots=save_plots, save_results=save_results, version=version, parentwise=True
    )
    
    # Compare results
    print("\n" + "="*80)
    print("COMPARISON RESULTS")
    print("="*80)
    print(f"{'Condition':<15} {'Union-based':<12} {'Parent-wise':<12} {'Difference':<12} {'% Change':<10}")
    print("-" * 70)
    
    for key in sorted(empirical_probs_union.keys()):
        union_mean = empirical_probs_union[key]['mean']
        parentwise_mean = empirical_probs_parentwise[key]['mean']
        diff = parentwise_mean - union_mean
        pct_change = (diff / union_mean) * 100 if union_mean != 0 else 0
        
        print(f"{str(key):<15} {union_mean:<12.4f} {parentwise_mean:<12.4f} {diff:<+12.4f} {pct_change:<+10.1f}%")
    
    return (empirical_probs_union, lookup_union), (empirical_probs_parentwise, lookup_parentwise)

def run_both_versions_analysis(save_plots=True, save_results=True):
    """
    Run analysis for both versions of retention probability calculation.
    """
    print("="*80)
    print("RUNNING EMPIRICAL PROBABILITY ANALYSIS - BOTH VERSIONS")
    print("="*80)
    
    # Version 1: Exclude overlaps
    print("\n" + "="*60)
    print("VERSION 1: EXCLUDING OVERLAPPING SPECIES")
    print("="*60)
    
    empirical_probs_v1, lookup_table_v1 = run_empirical_probability_analysis(
        save_plots=save_plots, save_results=save_results, version=1
    )
    
    # Version 2: Include overlaps (counted once)
    print("\n" + "="*60)
    print("VERSION 2: INCLUDING OVERLAPPING SPECIES (COUNTED ONCE)")
    print("="*60)
    
    empirical_probs_v2, lookup_table_v2 = run_empirical_probability_analysis(
        save_plots=save_plots, save_results=save_results, version=2
    )
    
    # Compare results
    print("\n" + "="*80)
    print("COMPARISON OF BOTH VERSIONS")
    print("="*80)
    
    # Print comparison for key conditions
    key_conditions = [('LN', 6), ('LN', 12), ('LN', 24), 
                      ('MN', 6), ('MN', 12), ('MN', 24),
                      ('HN', 6), ('HN', 12), ('HN', 24)]
    
    print(f"{'Condition':<10} {'Version 1':<12} {'Version 2':<12} {'Difference':<12}")
    print("-" * 50)
    
    for key in key_conditions:
        if key in empirical_probs_v1 and key in empirical_probs_v2:
            v1_mean = empirical_probs_v1[key]['mean']
            v2_mean = empirical_probs_v2[key]['mean']
            diff = v2_mean - v1_mean
            condition_name = f"{key[0]}-{key[1]}sp"
            print(f"{condition_name:<10} {v1_mean:<12.3f} {v2_mean:<12.3f} {diff:<12.3f}")
    
    # Save comparison to Excel file
    save_comparison_to_excel(empirical_probs_v1, empirical_probs_v2, 
                            save_path='Figure/AsymmetricityAnalysis/retention_probability_comparison.xlsx')
    
    return {
        'version_1': {'probabilities': empirical_probs_v1, 'lookup': lookup_table_v1},
        'version_2': {'probabilities': empirical_probs_v2, 'lookup': lookup_table_v2}
    }

def save_comparison_to_excel(empirical_probs_v1, empirical_probs_v2, save_path):
    """
    Save comparison of both versions to Excel file.
    """
    import pandas as pd
    import os
    
    # Create directory if needed
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Prepare comparison data
    comparison_data = []
    
    # Get all unique conditions
    all_conditions = set(list(empirical_probs_v1.keys()) + list(empirical_probs_v2.keys()))
    
    for condition in sorted(all_conditions):
        nutrient, species_pool = condition
        
        row = {
            'Nutrient': nutrient,
            'Species_Pool': species_pool,
            'Version_1_Mean': empirical_probs_v1.get(condition, {}).get('mean', 'N/A'),
            'Version_1_Std': empirical_probs_v1.get(condition, {}).get('std', 'N/A'),
            'Version_1_N': empirical_probs_v1.get(condition, {}).get('n', 'N/A'),
            'Version_2_Mean': empirical_probs_v2.get(condition, {}).get('mean', 'N/A'),
            'Version_2_Std': empirical_probs_v2.get(condition, {}).get('std', 'N/A'),
            'Version_2_N': empirical_probs_v2.get(condition, {}).get('n', 'N/A'),
        }
        
        # Calculate difference if both versions have data
        if (condition in empirical_probs_v1 and condition in empirical_probs_v2):
            row['Difference'] = empirical_probs_v2[condition]['mean'] - empirical_probs_v1[condition]['mean']
            row['Percent_Increase'] = (row['Difference'] / empirical_probs_v1[condition]['mean']) * 100
        else:
            row['Difference'] = 'N/A'
            row['Percent_Increase'] = 'N/A'
        
        comparison_data.append(row)
    
    # Create DataFrame
    comparison_df = pd.DataFrame(comparison_data)
    
    try:
        # Write to Excel with multiple sheets
        with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
            # Main comparison sheet
            comparison_df.to_excel(writer, sheet_name='Comparison', index=False)
            
            # Version 1 detailed sheet
            v1_detailed = []
            for condition, data in empirical_probs_v1.items():
                nutrient, species_pool = condition
                v1_detailed.append({
                    'Nutrient': nutrient,
                    'Species_Pool': species_pool,
                    'Mean': data['mean'],
                    'Std': data['std'],
                    'Median': data['median'],
                    'N_Samples': data['n'],
                    'Parent_Species_Mean': data['parent_species_mean'],
                    'Offspring_Species_Mean': data['offspring_species_mean']
                })
            pd.DataFrame(v1_detailed).to_excel(writer, sheet_name='Version_1_Excluding_Overlaps', index=False)
            
            # Version 2 detailed sheet
            v2_detailed = []
            for condition, data in empirical_probs_v2.items():
                nutrient, species_pool = condition
                v2_detailed.append({
                    'Nutrient': nutrient,
                    'Species_Pool': species_pool,
                    'Mean': data['mean'],
                    'Std': data['std'],
                    'Median': data['median'],
                    'N_Samples': data['n'],
                    'Parent_Species_Mean': data['parent_species_mean'],
                    'Offspring_Species_Mean': data['offspring_species_mean']
                })
            pd.DataFrame(v2_detailed).to_excel(writer, sheet_name='Version_2_Including_Overlaps', index=False)
        
        print(f"\nSaved retention probability comparison to: {save_path}")
        
    except Exception as e:
        print(f"Error saving Excel file: {e}")
        print("Attempting to save as CSV instead...")
        csv_path = save_path.replace('.xlsx', '.csv')
        comparison_df.to_csv(csv_path, index=False)
        print(f"Saved as CSV: {csv_path}")

if __name__ == "__main__":
    # Run both versions of the analysis
    results = run_both_versions_analysis()
    
    # Example of how to use the lookup tables
    print("\nExample usage of lookup tables:")
    
    lookup_table_v1 = results['version_1']['lookup']
    lookup_table_v2 = results['version_2']['lookup']
    
    print("\nVersion 1 (excluding overlaps):")
    print(f"LN condition with 6 species pool: p = {lookup_table_v1.get(('LN', 6), 'Not found'):.3f}")
    print(f"MN condition with 12 species pool: p = {lookup_table_v1.get(('MN', 12), 'Not found'):.3f}")
    print(f"HN condition (default): p = {lookup_table_v1.get(('HN', 'default'), 'Not found'):.3f}")
    
    print("\nVersion 2 (including overlaps, counted once):")
    print(f"LN condition with 6 species pool: p = {lookup_table_v2.get(('LN', 6), 'Not found'):.3f}")
    print(f"MN condition with 12 species pool: p = {lookup_table_v2.get(('MN', 12), 'Not found'):.3f}")
    print(f"HN condition (default): p = {lookup_table_v2.get(('HN', 'default'), 'Not found'):.3f}")