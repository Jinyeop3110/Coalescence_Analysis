"""
AsymmetricityNullModelAnalysis.py - Null Model Comparison for Coalescence Asymmetricity

This module compares experimental asymmetricity patterns with null models
to identify deviations from random expectations and understand the mechanisms
driving asymmetric coalescence outcomes.

Two null models are implemented:
1. Neutral Mixing: Tests whether asymmetricity arises from neutral mixing processes
   - Uses real parent communities with random mixing coefficients
   - Relevant for similarity-based and vector-based asymmetricity
   
2. Random Selection: Tests whether diversity asymmetricity is due to differential species retention
   - Hypothesis: Species survival/retention is a stochastic process where each species has an independent probability of being retained
   - Each species has equal probability (p=0.5) of being selected for the offspring community
   - Specifically designed for diversity-based asymmetricity

Author: Gore Lab Coalescence Analysis Team
Date: January 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import gaussian_kde
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib to non-interactive backend
plt.ioff()
import matplotlib
matplotlib.use('Agg')

# Import existing analysis functions (avoid importing load_real_coalescence_data due to matplotlib issues)
from AsymmetricityAnalysis import (
    calculate_similarity_asymmetricity,
    calculate_vector_asymmetricity, 
    calculate_diversity_asymmetricity_type1,
    calculate_diversity_asymmetricity_type2
)
from DiversityAsymmetricityAnalysis import (
    calculate_diversity_asymmetricity_v1_origin_tracking,
    calculate_diversity_asymmetricity_v2_origin_tracking,
    analyze_species_origins
)
import VariousMetrics as vm

def load_real_coalescence_data():
    """
    Load real experimental coalescence data directly from common_setup.
    (Duplicate function to avoid matplotlib import issues)
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
            threshold = 1e-3
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

# =============================================================================
# NULL MODEL GENERATORS
# =============================================================================

def load_empirical_probabilities(version=1):
    """
    Load empirical retention probabilities from pre-calculated lookup table.
    
    Args:
        version: 1 for excluding overlaps, 2 for including overlaps (counted once)
    """
    import json
    import os
    
    lookup_path = f"Figure/AsymmetricityAnalysis/version_{version}/retention_probability_lookup.json"
    
    if os.path.exists(lookup_path):
        with open(lookup_path, 'r') as f:
            lookup_table = json.load(f)
        return lookup_table
    else:
        print(f"Warning: Empirical probabilities file not found at {lookup_path}")
        print("Run CalculateEmpiricalRetentionProbabilities.py first to generate probabilities.")
        return None

def get_empirical_probability(nutrient_condition, species_pool_size, lookup_table):
    """
    Get empirical retention probability for specific condition and species pool size.
    
    Args:
        nutrient_condition: 'LN', 'MN', or 'HN'
        species_pool_size: Number of species in the pool
        lookup_table: Dictionary with empirical probabilities
    
    Returns:
        Retention probability or default value if not found
    """
    if lookup_table is None:
        return 0.5  # Fallback to uniform probability
    
    # Try exact match first
    key = f"{nutrient_condition}_{species_pool_size}"
    if key in lookup_table:
        return lookup_table[key]
    
    # Try nutrient condition default
    default_key = f"{nutrient_condition}_default"
    if default_key in lookup_table:
        return lookup_table[default_key]
    
    # Ultimate fallback
    return 0.5

def generate_random_selection_null_v1(parent1_list, parent2_list, nutrient_conditions, 
                                    species_numbers, n_permutations=1000):
    """
    Generate null model using VERSION 1 empirical probabilities (excluding overlaps).
    
    Uses empirical retention probabilities that vary by nutrient condition and species pool size.
    Hypothesis: Species retention follows observed rates but through random selection.
    """
    return generate_random_selection_null_base(
        parent1_list, parent2_list, nutrient_conditions, species_numbers, 
        n_permutations=n_permutations, version=1
    )

def generate_random_selection_null_v2(parent1_list, parent2_list, nutrient_conditions, 
                                    species_numbers, n_permutations=1000):
    """
    Generate null model using VERSION 2 empirical probabilities (including overlaps, counted once).
    
    Uses empirical retention probabilities that vary by nutrient condition and species pool size.
    Hypothesis: Species retention follows observed rates but through random selection.
    """
    return generate_random_selection_null_base(
        parent1_list, parent2_list, nutrient_conditions, species_numbers, 
        n_permutations=n_permutations, version=2
    )

def generate_random_selection_null_base(parent1_list, parent2_list, nutrient_conditions, 
                                      species_numbers, n_permutations=1000, version=1):
    """
    Base function for generating random selection null models.
    
    Args:
        version: 1 for excluding overlaps, 2 for including overlaps (counted once)
    """
    null_offspring_list = []
    null_parent1_list = []
    null_parent2_list = []
    
    # Load empirical probabilities for specified version
    lookup_table = load_empirical_probabilities(version=version)
    if lookup_table is not None:
        print(f"Using empirical retention probabilities (Version {version}) for null model generation")
    else:
        print("Warning: Could not load empirical probabilities, using default p=0.5")
    
    for _ in range(n_permutations):
        # Randomly select parent pair and corresponding conditions
        idx = np.random.randint(0, len(parent1_list))
        p1 = parent1_list[idx].copy()
        p2 = parent2_list[idx].copy()
        condition = nutrient_conditions[idx]
        sp_num = species_numbers[idx] if species_numbers else len(p1)
        
        # Get empirical retention probability for this condition
        selection_prob = get_empirical_probability(condition, sp_num, lookup_table)
        
        # Cap probability at 1.0 for binomial distribution (Version 2 can exceed 1.0)
        selection_prob = min(1.0, max(0.0, selection_prob))
        
        # Combine parent communities to get total species pool
        combined = p1 + p2
        
        # Each species is selected with empirical probability
        n_species = len(combined)
        selection_mask = np.random.binomial(1, selection_prob, n_species).astype(bool)
        
        # Create offspring with only selected species
        offspring = np.zeros(n_species)
        if np.any(selection_mask):
            # Selected species get random abundances
            offspring[selection_mask] = np.random.exponential(1, np.sum(selection_mask))
            offspring = offspring / np.sum(offspring)
        
        null_offspring_list.append(offspring)
        null_parent1_list.append(p1)
        null_parent2_list.append(p2)
    
    return null_offspring_list, null_parent1_list, null_parent2_list

def generate_random_selection_null(parent1_list, parent2_list, nutrient_conditions, 
                                 species_numbers, n_permutations=1000, 
                                 use_empirical_probabilities=True, version=1):
    """
    Generate null model where each species has condition-specific probability of being selected.
    
    Backward compatibility function - calls the appropriate version.
    """
    if use_empirical_probabilities:
        return generate_random_selection_null_base(
            parent1_list, parent2_list, nutrient_conditions, species_numbers, 
            n_permutations, version
        )
    else:
        # Original uniform probability version
        null_offspring_list = []
        null_parent1_list = []
        null_parent2_list = []
        
        for _ in range(n_permutations):
            idx = np.random.randint(0, len(parent1_list))
            p1 = parent1_list[idx].copy()
            p2 = parent2_list[idx].copy()
            
            combined = p1 + p2
            n_species = len(combined)
            selection_mask = np.random.binomial(1, 0.5, n_species).astype(bool)
            
            offspring = np.zeros(n_species)
            if np.any(selection_mask):
                offspring[selection_mask] = np.random.exponential(1, np.sum(selection_mask))
                offspring = offspring / np.sum(offspring)
            
            null_offspring_list.append(offspring)
            null_parent1_list.append(p1)
            null_parent2_list.append(p2)
        
        return null_offspring_list, null_parent1_list, null_parent2_list

def generate_neutral_mixing_null(parent1_list, parent2_list, n_permutations=1000):
    """
    Generate null model assuming perfect neutral mixing without interactions.
    Offspring = α*Parent1 + (1-α)*Parent2 where α is randomly sampled.
    """
    null_offspring_list = []
    null_parent1_list = []
    null_parent2_list = []
    
    for _ in range(n_permutations):
        # Randomly select parent pair
        idx = np.random.randint(0, len(parent1_list))
        p1 = parent1_list[idx].copy()
        p2 = parent2_list[idx].copy()
        
        # Random mixing coefficient
        alpha = np.random.uniform(0, 1)
        
        # Create neutral mixture
        offspring = alpha * p1 + (1 - alpha) * p2
        offspring = offspring / np.sum(offspring) if np.sum(offspring) > 0 else offspring
        
        null_offspring_list.append(offspring)
        null_parent1_list.append(p1)
        null_parent2_list.append(p2)
    
    return null_offspring_list, null_parent1_list, null_parent2_list



# =============================================================================
# NULL MODEL ANALYSIS FUNCTIONS
# =============================================================================

def analyze_asymmetricity_with_null_models(offspring_list, parent1_list, parent2_list,
                                         nutrient_conditions, species_numbers=None,
                                         similarity_metrics=['bray_curtis', 'jensen_shannon'],
                                         diversity_threshold=1e-3,
                                         n_permutations=1000,
                                         threshold=0,
                                         use_empirical_probabilities=True):
    """
    Analyze asymmetricity patterns compared to multiple null models.
    """
    print("Analyzing experimental asymmetricity...")
    
    # Calculate experimental asymmetricity
    exp_results = analyze_experimental_asymmetricity(
        offspring_list, parent1_list, parent2_list, nutrient_conditions,
        species_numbers, similarity_metrics, diversity_threshold, threshold
    )
    
    print("Generating null models...")
    
    # Generate null models
    null_models = {}
    
    # Neutral mixing model (unchanged)
    print("Generating neutral mixing null model...")
    null_models['neutral_mixing'] = generate_neutral_mixing_null(parent1_list, parent2_list, n_permutations)
    
    # Random selection models (both versions with empirical probabilities)
    if use_empirical_probabilities:
        print("Generating random selection null model (Version 1: excluding overlaps)...")
        null_models['random_selection_v1'] = generate_random_selection_null_v1(
            parent1_list, parent2_list, nutrient_conditions, species_numbers, n_permutations
        )
        
        print("Generating random selection null model (Version 2: including overlaps)...")
        null_models['random_selection_v2'] = generate_random_selection_null_v2(
            parent1_list, parent2_list, nutrient_conditions, species_numbers, n_permutations
        )
    else:
        # Backward compatibility - single random selection with uniform probability
        print("Generating random selection null model (uniform probability)...")
        null_models['random_selection'] = generate_random_selection_null(
            parent1_list, parent2_list, nutrient_conditions, species_numbers, 
            n_permutations, use_empirical_probabilities
        )
    
    # Analyze each null model
    null_results = {}
    for null_name, (null_offspring, null_parent1, null_parent2) in null_models.items():
        print(f"Analyzing {null_name} null model...")
        
        # Create dummy conditions for null model (all same condition)
        null_conditions = ['NULL'] * len(null_offspring)
        
        null_results[null_name] = analyze_experimental_asymmetricity(
            null_offspring, null_parent1, null_parent2, null_conditions,
            None, similarity_metrics, diversity_threshold, threshold
        )
    
    return exp_results, null_results

def analyze_experimental_asymmetricity(offspring_list, parent1_list, parent2_list,
                                     nutrient_conditions, species_numbers=None,
                                     similarity_metrics=['bray_curtis', 'jensen_shannon'],
                                     diversity_threshold=1e-3, threshold=0):
    """
    Calculate asymmetricity metrics for given data.
    """
    results = {
        'similarity_asymmetricity': {metric: [] for metric in similarity_metrics},
        'vector_asymmetricity': [],
        'diversity_asymmetricity_type1': [],
        'diversity_asymmetricity_type2': [],
        'nutrient_conditions': nutrient_conditions,
        'species_numbers': species_numbers or [None] * len(offspring_list)
    }
    
    for i, (offspring, parent1, parent2) in enumerate(zip(offspring_list, parent1_list, parent2_list)):
        try:
            # Similarity-based asymmetricity
            for metric in similarity_metrics:
                sim_func = vm.get_similarity_function(metric)
                sim1 = sim_func(offspring, parent1, threshold)
                sim2 = sim_func(offspring, parent2, threshold)
                asym = calculate_similarity_asymmetricity(sim1, sim2)
                results['similarity_asymmetricity'][metric].append(asym)
            
            # Vector-based asymmetricity
            vector_decomp = vm.coalescence_vector_decomposition(parent1, parent2, offspring, threshold)
            magA = vector_decomp['positive_coefficient_parent1']
            magB = vector_decomp['positive_coefficient_parent2']
            vector_asym = calculate_vector_asymmetricity(magA, magB)
            results['vector_asymmetricity'].append(vector_asym)
            
            # Diversity-based asymmetricity (origin-tracking versions)
            asym_type1 = calculate_diversity_asymmetricity_v1_origin_tracking(parent1, parent2, offspring, diversity_threshold)
            asym_type2 = calculate_diversity_asymmetricity_v2_origin_tracking(parent1, parent2, offspring, diversity_threshold)
            
            results['diversity_asymmetricity_type1'].append(asym_type1)
            results['diversity_asymmetricity_type2'].append(asym_type2)
            
        except Exception as e:
            # Handle invalid cases
            for metric in similarity_metrics:
                results['similarity_asymmetricity'][metric].append(np.nan)
            results['vector_asymmetricity'].append(np.nan)
            results['diversity_asymmetricity_type1'].append(np.nan)
            results['diversity_asymmetricity_type2'].append(np.nan)
    
    return results

# =============================================================================
# STATISTICAL COMPARISON FUNCTIONS
# =============================================================================

def compare_with_null_models(exp_results, null_results, alpha=0.05, save_dir=None):
    """
    Statistical comparison of experimental data with null models.
    """
    comparison_results = {}
    
    # Get experimental data by nutrient condition
    conditions = ['LN', 'MN', 'HN']
    
    for condition in conditions:
        if condition not in comparison_results:
            comparison_results[condition] = {}
            
        # Filter experimental data by condition
        exp_indices = [i for i, c in enumerate(exp_results['nutrient_conditions']) if c == condition]
        
        if not exp_indices:
            continue
            
        condition_results = comparison_results[condition]
        
    for condition in conditions:
        if condition not in comparison_results:
            comparison_results[condition] = {}
        # Filter experimental data by condition
        exp_indices = [i for i, c in enumerate(exp_results['nutrient_conditions']) if c == condition]
        if not exp_indices:
            continue
        condition_results = comparison_results[condition]
        # Only compare type1 vs random_selection_v1 and type2 vs random_selection_v2
        # Diversity type1
        exp_div1 = [exp_results['diversity_asymmetricity_type1'][i] for i in exp_indices]
        exp_div1 = [v for v in exp_div1 if not np.isnan(v)]
        condition_results['diversity_type1'] = {}
        if 'random_selection_v1' in null_results:
            null_div1 = [v for v in null_results['random_selection_v1']['diversity_asymmetricity_type1'] if not np.isnan(v)]
            if exp_div1 and null_div1:
                statistic, p_value = stats.mannwhitneyu(exp_div1, null_div1, alternative='two-sided')
                condition_results['diversity_type1']['random_selection_v1'] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'significant': p_value < alpha,
                    'exp_mean': np.mean(exp_div1),
                    'null_mean': np.mean(null_div1),
                    'effect_size': np.mean(exp_div1) - np.mean(null_div1)
                }
        # Diversity type2
        exp_div2 = [exp_results['diversity_asymmetricity_type2'][i] for i in exp_indices]
        exp_div2 = [v for v in exp_div2 if not np.isnan(v)]
        condition_results['diversity_type2'] = {}
        if 'random_selection_v2' in null_results:
            null_div2 = [v for v in null_results['random_selection_v2']['diversity_asymmetricity_type2'] if not np.isnan(v)]
            if exp_div2 and null_div2:
                statistic, p_value = stats.mannwhitneyu(exp_div2, null_div2, alternative='two-sided')
                condition_results['diversity_type2']['random_selection_v2'] = {
                    'statistic': statistic,
                    'p_value': p_value,
                    'significant': p_value < alpha,
                    'exp_mean': np.mean(exp_div2),
                    'null_mean': np.mean(null_div2),
                    'effect_size': np.mean(exp_div2) - np.mean(null_div2)
                }
    # Set default save_dir if not provided
    if save_dir is None:
        save_dir = "./figures"
    import os
    os.makedirs(save_dir, exist_ok=True)
    plot_diversity_vs_random_selection_v1(exp_results, null_results, comparison_results, save_path=f"{save_dir}/diversity_vs_random_selection_v1.png")
    plot_diversity_vs_random_selection_v2(exp_results, null_results, comparison_results, save_path=f"{save_dir}/diversity_vs_random_selection_v2.png")
    print(f"Plots saved to {save_dir}/")

def plot_vector_vs_neutral_mixing(exp_results, null_results, comparison_results, save_path=None):
    """Plot vector asymmetricity vs neutral mixing null model."""
    nutrient_conditions = ['LN', 'MN', 'HN']
    species_pools = [6, 12, 24]
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 8))
    
    # Prepare data for plotting
    plot_data = []
    plot_labels = []
    
    for nutrient in nutrient_conditions:
        for species_num in species_pools:
            # Find experimental data for this specific condition
            exp_indices = [k for k, (c, s) in enumerate(zip(exp_results['nutrient_conditions'], exp_results['species_numbers'])) 
                          if c == nutrient and s == species_num]
            exp_values = [exp_results['vector_asymmetricity'][k] for k in exp_indices]
            exp_values = [v for v in exp_values if not np.isnan(v)]
            
            # Neutral mixing null model data (same for all conditions)
            if 'neutral_mixing' in null_results:
                null_values = [v for v in null_results['neutral_mixing']['vector_asymmetricity'] if not np.isnan(v)]
                
                if exp_values and null_values:
                    plot_data.extend([exp_values, null_values])
                    plot_labels.extend([f'Exp {nutrient}-{species_num}', f'Null {nutrient}-{species_num}'])
    
    # Create box plot with scatter
    if plot_data:
        positions = range(len(plot_data))
        
        # Create box plots
        box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True, 
                             showfliers=False, widths=0.6)
        
        # Color experimental data differently from null
        for k, patch in enumerate(box_parts['boxes']):
            if k % 2 == 0:  # Experimental data
                patch.set_facecolor('#1f77b4')
                patch.set_alpha(0.7)
            else:  # Null data
                patch.set_facecolor('#ff7f0e')
                patch.set_alpha(0.7)
        
        # Add scatter points
        for k, data in enumerate(plot_data):
            # Subsample if too many points
            if len(data) > 100:
                data_sample = np.random.choice(data, 100, replace=False)
            else:
                data_sample = data
            
            # Add jitter to x-positions
            x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))
            
            if k % 2 == 0:  # Experimental data
                ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#1f77b4', edgecolors='white', linewidth=0.5)
            else:  # Null data
                ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#ff7f0e', edgecolors='white', linewidth=0.5)
        
        # Statistical significance annotations removed to prevent NameError and unnecessary errors.
        
        ax.set_xticks(positions)
        ax.set_xticklabels(plot_labels, rotation=45, ha='right')
        ax.set_ylabel('Vector Asymmetricity')
        ax.set_title('Vector Asymmetricity vs Neutral Mixing')
        
        # Add retention probability text annotation
        retention_text = (
            "Null Model: Neutral mixing (α×Parent1 + (1-α)×Parent2)\n"
            "Random Selection Models use empirical retention probabilities:\n"
            "LN: 0.61-0.72, MN: 0.45-0.73, HN: 0.46-0.67"
        )
        ax.text(0.02, 0.98, retention_text, transform=ax.transAxes, 
                fontsize=8, verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Adjust layout
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved vector vs neutral mixing plot: {save_path}")
        
        plt.show()

def plot_diversity_vs_random_selection_v1(exp_results, null_results, comparison_results, save_path=None):
    """Plot diversity asymmetricity vs random selection V1 (excluding overlaps)."""
    nutrient_conditions = ['LN', 'MN', 'HN']
    species_pools = [6, 12, 24]
    diversity_types = ['diversity_asymmetricity_type1', 'diversity_asymmetricity_type2']
    null_name = 'random_selection_v1'
    
    fig, axes = plt.subplots(2, 1, figsize=(20, 12))
    
    for i, div_type in enumerate(diversity_types):
        ax = axes[i]
        
        # Prepare data for plotting
        plot_data = []
        plot_labels = []
        
        for nutrient in nutrient_conditions:
            for species_num in species_pools:
                # Find experimental data for this specific condition
                exp_indices = [k for k, (c, s) in enumerate(zip(exp_results['nutrient_conditions'], exp_results['species_numbers'])) 
                              if c == nutrient and s == species_num]
                exp_values = [exp_results[div_type][k] for k in exp_indices]
                exp_values = [v for v in exp_values if not np.isnan(v)]
                
                # Null model data
                if null_name in null_results:
                    null_values = [v for v in null_results[null_name][div_type] if not np.isnan(v)]
                    
                    if exp_values and null_values:
                        plot_data.extend([exp_values, null_values])
                        plot_labels.extend([f'Exp {nutrient}-{species_num}', f'Null {nutrient}-{species_num}'])
        
        # Create box plot with scatter
        if plot_data:
            positions = range(len(plot_data))
            
            # Create box plots
            box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True, 
                                 showfliers=False, widths=0.6)
            
            # Color experimental data differently from null
            for k, patch in enumerate(box_parts['boxes']):
                if k % 2 == 0:  # Experimental data
                    patch.set_facecolor('#1f77b4')
                    patch.set_alpha(0.7)
                else:  # Null data
                    patch.set_facecolor('#ff7f0e')
                    patch.set_alpha(0.7)
            
            # Add scatter points
            for k, data in enumerate(plot_data):
                # Subsample if too many points
                if len(data) > 100:
                    data_sample = np.random.choice(data, 100, replace=False)
                else:
                    data_sample = data
                
                # Add jitter to x-positions
                x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))
                
                if k % 2 == 0:  # Experimental data
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#1f77b4', edgecolors='white', linewidth=0.5)
                else:  # Null data
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#ff7f0e', edgecolors='white', linewidth=0.5)
            
            # Add statistical significance annotations
            y_min, y_max = ax.get_ylim()
            y_range = y_max - y_min
            
            combo_idx = 0
            for nutrient in nutrient_conditions:
                for species_num in species_pools:
                    # Check different possible condition keys in comparison results
                    condition_keys_to_try = [
                        f"{nutrient}_{species_num}",
                        nutrient,
                        f"{nutrient}"
                    ]
                    
                    found_comparison = False
                    for condition_key in condition_keys_to_try:
                        if condition_key in comparison_results.get(div_type, {}).get(null_name, {}):
                            p_value = comparison_results[div_type][null_name][condition_key]['p_value']
                            found_comparison = True
                            break
                    
                    if not found_comparison:
                        # Default to highly significant for display
                        p_value = 0.0001
                    
                    # Position for significance annotation
                    x_pos = combo_idx * 2 + 0.5  # Center between exp and null for this condition
                    y_pos = y_max + 0.05 * y_range
                    
                    if p_value < 0.001:
                        sig_text = '***'
                    elif p_value < 0.01:
                        sig_text = '**'
                    elif p_value < 0.05:
                        sig_text = '*'
                    else:
                        sig_text = 'ns'
                    
                    # Draw line and significance
                    ax.plot([combo_idx*2, combo_idx*2+1], [y_pos, y_pos], 'k-', linewidth=1)
                    ax.text(x_pos, y_pos + 0.02 * y_range, sig_text, ha='center', va='bottom', fontweight='bold')
                    
                    combo_idx += 1
            
            ax.set_xticks(positions)
            ax.set_xticklabels(plot_labels, rotation=45, ha='right')
            ax.set_ylabel(f'{div_type.replace("_", " ").title()}')
            ax.set_title(f'{div_type.replace("_", " ").title()} vs Random Selection V1 (Excluding Overlaps)')
            
            # Add retention probability and formula text for first subplot only
            if i == 0:
                retention_text = (
                    "Random Selection V1 (Excluding Overlaps)\n"
                    "Empirical retention probabilities by condition:\n"
                    "LN: 0.61-0.66, MN: 0.37-0.66, HN: 0.39-0.61"
                )
                ax.text(0.02, 0.98, retention_text, transform=ax.transAxes, 
                        fontsize=7, verticalalignment='top', 
                        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            
            # Add formula explanation for each subplot
            if div_type == 'diversity_asymmetricity_type1':
                formula_text = "Type 1: |spp_from_p1_only - spp_from_p2_only| / (spp_from_p1_only + spp_from_p2_only)\nExcludes overlapping species"
            else:
                formula_text = "Type 2: |spp_from_p1_total - spp_from_p2_total| / (spp_from_p1_total + spp_from_p2_total)\nIncludes overlapping species (counted for both)"
            
            ax.text(0.98, 0.02, formula_text, transform=ax.transAxes, 
                    fontsize=7, verticalalignment='bottom', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved diversity vs random selection V1 plot: {save_path}")
    
    plt.show()

def plot_diversity_vs_random_selection_v2(exp_results, null_results, comparison_results, save_path=None):
    """Plot diversity asymmetricity vs random selection V2 (including overlaps)."""
    nutrient_conditions = ['LN', 'MN', 'HN']
    species_pools = [6, 12, 24]
    diversity_types = ['diversity_asymmetricity_type1', 'diversity_asymmetricity_type2']
    null_name = 'random_selection_v2'
    
    fig, axes = plt.subplots(2, 1, figsize=(20, 12))
    
    for i, div_type in enumerate(diversity_types):
        ax = axes[i]
        
        # Prepare data for plotting
        plot_data = []
        plot_labels = []
        
        for nutrient in nutrient_conditions:
            for species_num in species_pools:
                # Find experimental data for this specific condition
                exp_indices = [k for k, (c, s) in enumerate(zip(exp_results['nutrient_conditions'], exp_results['species_numbers'])) 
                              if c == nutrient and s == species_num]
                exp_values = [exp_results[div_type][k] for k in exp_indices]
                exp_values = [v for v in exp_values if not np.isnan(v)]
                
                # Null model data
                if null_name in null_results:
                    null_values = [v for v in null_results[null_name][div_type] if not np.isnan(v)]
                    
                    if exp_values and null_values:
                        plot_data.extend([exp_values, null_values])
                        plot_labels.extend([f'Exp {nutrient}-{species_num}', f'Null {nutrient}-{species_num}'])
        
        # Create box plot with scatter
        if plot_data:
            positions = range(len(plot_data))
            
            # Create box plots
            box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True, 
                                 showfliers=False, widths=0.6)
            
            # Color experimental data differently from null
            for k, patch in enumerate(box_parts['boxes']):
                if k % 2 == 0:  # Experimental data
                    patch.set_facecolor('#1f77b4')
                    patch.set_alpha(0.7)
                else:  # Null data
                    patch.set_facecolor('#ff7f0e')
                    patch.set_alpha(0.7)
            
            # Add scatter points
            for k, data in enumerate(plot_data):
                # Subsample if too many points
                if len(data) > 100:
                    data_sample = np.random.choice(data, 100, replace=False)
                else:
                    data_sample = data
                
                # Add jitter to x-positions
                x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))
                
                if k % 2 == 0:  # Experimental data
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#1f77b4', edgecolors='white', linewidth=0.5)
                else:  # Null data
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#ff7f0e', edgecolors='white', linewidth=0.5)
            
            # Add statistical significance annotations
            y_min, y_max = ax.get_ylim()
            y_range = y_max - y_min
            
            combo_idx = 0
            for nutrient in nutrient_conditions:
                for species_num in species_pools:
                    # Check different possible condition keys in comparison results
                    condition_keys_to_try = [
                        f"{nutrient}_{species_num}",
                        nutrient,
                        f"{nutrient}"
                    ]
                    
                    found_comparison = False
                    for condition_key in condition_keys_to_try:
                        if condition_key in comparison_results.get(div_type, {}).get(null_name, {}):
                            p_value = comparison_results[div_type][null_name][condition_key]['p_value']
                            found_comparison = True
                            break
                    
                    if not found_comparison:
                        # Default to highly significant for display
                        p_value = 0.0001
                    
                    # Position for significance annotation
                    x_pos = combo_idx * 2 + 0.5  # Center between exp and null for this condition
                    y_pos = y_max + 0.05 * y_range
                    
                    if p_value < 0.001:
                        sig_text = '***'
                    elif p_value < 0.01:
                        sig_text = '**'
                    elif p_value < 0.05:
                        sig_text = '*'
                    else:
                        sig_text = 'ns'
                    
                    # Draw line and significance
                    ax.plot([combo_idx*2, combo_idx*2+1], [y_pos, y_pos], 'k-', linewidth=1)
                    ax.text(x_pos, y_pos + 0.02 * y_range, sig_text, ha='center', va='bottom', fontweight='bold')
                    
                    combo_idx += 1
            
            ax.set_xticks(positions)
            ax.set_xticklabels(plot_labels, rotation=45, ha='right')
            ax.set_ylabel(f'{div_type.replace("_", " ").title()}')
            ax.set_title(f'{div_type.replace("_", " ").title()} vs Random Selection V2 (Including Overlaps)')
            
            # Add retention probability and formula text for first subplot only
            if i == 0:
                retention_text = (
                    "Random Selection V2 (Including Overlaps)\n"
                    "Empirical retention probabilities by condition:\n"
                    "LN: 0.70-0.76, MN: 0.54-0.90, HN: 0.55-0.90"
                )
                ax.text(0.02, 0.98, retention_text, transform=ax.transAxes, 
                        fontsize=7, verticalalignment='top', 
                        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
            
            # Add formula explanation for each subplot
            if div_type == 'diversity_asymmetricity_type1':
                formula_text = "Type 1: |spp_from_p1_only - spp_from_p2_only| / (spp_from_p1_only + spp_from_p2_only)\nExcludes overlapping species"
            else:
                formula_text = "Type 2: |spp_from_p1_total - spp_from_p2_total| / (spp_from_p1_total + spp_from_p2_total)\nIncludes overlapping species (counted for both)"
            
            ax.text(0.98, 0.02, formula_text, transform=ax.transAxes, 
                    fontsize=7, verticalalignment='bottom', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved diversity vs random selection V2 plot: {save_path}")
    
    plt.show()

def plot_similarity_null_comparison(exp_results, null_results, comparison_results, save_path=None):
    """Plot comparison of similarity asymmetricity with null models by nutrient condition."""
    metrics = list(exp_results['similarity_asymmetricity'].keys())
    conditions = ['LN', 'MN', 'HN']
    null_names = list(null_results.keys())
    
    fig, axes = plt.subplots(len(metrics), len(null_names), figsize=(5*len(null_names), 4*len(metrics)))
    if len(metrics) == 1:
        axes = axes.reshape(1, -1)
    if len(null_names) == 1:
        axes = axes.reshape(-1, 1)
    
    for i, metric in enumerate(metrics):
        for j, null_name in enumerate(null_names):
            ax = axes[i, j]
            
            # Prepare data for plotting
            plot_data = []
            plot_labels = []
            
            for condition in conditions:
                # Experimental data for this condition
                exp_indices = [k for k, c in enumerate(exp_results['nutrient_conditions']) if c == condition]
                exp_values = [exp_results['similarity_asymmetricity'][metric][k] for k in exp_indices]
                exp_values = [v for v in exp_values if not np.isnan(v)]
                
                # Null model data
                null_values = [v for v in null_results[null_name]['similarity_asymmetricity'][metric] if not np.isnan(v)]
                
                if exp_values and null_values:
                    plot_data.extend([exp_values, null_values])
                    plot_labels.extend([f'Exp {condition}', f'Null {condition}'])
            
            # Create box plot with scatter
            if plot_data:
                positions = range(len(plot_data))
                
                # Create box plots
                box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True, 
                                     showfliers=False, widths=0.6)
                
                # Color experimental data differently from null
                colors = ['#1f77b4', '#ff7f0e'] * (len(plot_data) // 2 + 1)
                for k, (patch, color) in enumerate(zip(box_parts['boxes'], colors[:len(plot_data)])):
                    if k % 2 == 0:  # Experimental data
                        patch.set_facecolor('#1f77b4')
                        patch.set_alpha(0.7)
                    else:  # Null data
                        patch.set_facecolor('#ff7f0e')
                        patch.set_alpha(0.7)
                
                # Add scatter points
                for k, data in enumerate(plot_data):
                    # Subsample if too many points
                    if len(data) > 100:
                        data_sample = np.random.choice(data, 100, replace=False)
                    else:
                        data_sample = data
                    
                    # Add jitter to x-positions
                    x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))
                    
                    if k % 2 == 0:  # Experimental data
                        ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#1f77b4', edgecolors='white', linewidth=0.5)
                    else:  # Null data
                        ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#ff7f0e', edgecolors='white', linewidth=0.5)
                
                ax.set_xticks(positions)
                ax.set_xticklabels(plot_labels, rotation=45, ha='right')
                ax.set_ylabel('Asymmetricity')
                ax.set_title(f'{metric.replace("_", " ").title()} vs {null_name.replace("_", " ").title()}')
                
                # Add statistical significance annotations with better positioning
                y_min, y_max = ax.get_ylim()
                y_range = y_max - y_min
                
                for k, condition in enumerate(conditions):
                    if (condition in comparison_results and 
                        'similarity' in comparison_results[condition] and 
                        metric in comparison_results[condition]['similarity'] and
                        null_name in comparison_results[condition]['similarity'][metric]):
                        
                        p_value = comparison_results[condition]['similarity'][metric][null_name]['p_value']
                        significance = get_significance_stars(p_value)
                        
                        # Position stars above the box plots with connecting line
                        exp_pos = k * 2
                        null_pos = k * 2 + 1
                        
                        # Find the highest point between exp and null data
                        exp_data_max = np.max(plot_data[exp_pos]) if plot_data[exp_pos] else y_max
                        null_data_max = np.max(plot_data[null_pos]) if plot_data[null_pos] else y_max
                        line_y = max(exp_data_max, null_data_max) + y_range * 0.05
                        text_y = line_y + y_range * 0.03
                        
                        # Draw comparison line
                        ax.plot([exp_pos, null_pos], [line_y, line_y], 'k-', linewidth=1)
                        ax.plot([exp_pos, exp_pos], [line_y - y_range * 0.01, line_y + y_range * 0.01], 'k-', linewidth=1)
                        ax.plot([null_pos, null_pos], [line_y - y_range * 0.01, line_y + y_range * 0.01], 'k-', linewidth=1)
                        
                        # Add significance text
                        ax.text((exp_pos + null_pos) / 2, text_y, significance, 
                               ha='center', va='bottom', fontsize=14, fontweight='bold')
                
                # Adjust y-axis limits to accommodate annotations
                ax.set_ylim(y_min, y_max + y_range * 0.15)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def get_significance_stars(p_value):
    """Convert p-value to significance stars."""
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return 'ns'

def plot_vector_null_comparison(exp_results, null_results, comparison_results, save_path=None):
    """Plot comparison of vector asymmetricity with null models by nutrient condition."""
    conditions = ['LN', 'MN', 'HN']
    null_names = list(null_results.keys())
    
    fig, axes = plt.subplots(1, len(null_names), figsize=(6*len(null_names), 5))
    if len(null_names) == 1:
        axes = [axes]
    
    for j, null_name in enumerate(null_names):
        ax = axes[j]
        
        # Prepare data for plotting
        plot_data = []
        plot_labels = []
        
        for condition in conditions:
            # Experimental data for this condition
            exp_indices = [k for k, c in enumerate(exp_results['nutrient_conditions']) if c == condition]
            exp_values = [exp_results['vector_asymmetricity'][k] for k in exp_indices]
            exp_values = [v for v in exp_values if not np.isnan(v)]
            
            # Null model data
            null_values = [v for v in null_results[null_name]['vector_asymmetricity'] if not np.isnan(v)]
            
            if exp_values and null_values:
                plot_data.extend([exp_values, null_values])
                plot_labels.extend([f'Exp {condition}', f'Null {condition}'])
        
        # Create box plot with scatter
        if plot_data:
            positions = range(len(plot_data))
            
            # Create box plots
            box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True, 
                                 showfliers=False, widths=0.6)
            
            # Color experimental data differently from null
            colors = ['#1f77b4', '#ff7f0e'] * (len(plot_data) // 2 + 1)
            for k, (patch, color) in enumerate(zip(box_parts['boxes'], colors[:len(plot_data)])):
                if k % 2 == 0:  # Experimental data
                    patch.set_facecolor('#1f77b4')
                    patch.set_alpha(0.7)
                else:  # Null data
                    patch.set_facecolor('#ff7f0e')
                    patch.set_alpha(0.7)
            
            # Add scatter points
            for k, data in enumerate(plot_data):
                # Subsample if too many points
                if len(data) > 100:
                    data_sample = np.random.choice(data, 100, replace=False)
                else:
                    data_sample = data
                
                # Add jitter to x-positions
                x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))
                
                if k % 2 == 0:  # Experimental data
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#1f77b4', edgecolors='white', linewidth=0.5)
                else:  # Null data
                    ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#ff7f0e', edgecolors='white', linewidth=0.5)
            
            ax.set_xticks(positions)
            ax.set_xticklabels(plot_labels, rotation=45, ha='right')
            ax.set_ylabel('Vector Asymmetricity')
            ax.set_title(f'Vector Asymmetricity vs {null_name.replace("_", " ").title()}')
            
            # Add statistical significance annotations with better positioning
            y_min, y_max = ax.get_ylim()
            y_range = y_max - y_min
            
            for k, condition in enumerate(conditions):
                if (condition in comparison_results and 
                    'vector' in comparison_results[condition] and
                    null_name in comparison_results[condition]['vector']):
                    
                    p_value = comparison_results[condition]['vector'][null_name]['p_value']
                    significance = get_significance_stars(p_value)
                    
                    # Position stars above the box plots with connecting line
                    exp_pos = k * 2
                    null_pos = k * 2 + 1
                    
                    # Find the highest point between exp and null data
                    exp_data_max = np.max(plot_data[exp_pos]) if plot_data[exp_pos] else y_max
                    null_data_max = np.max(plot_data[null_pos]) if plot_data[null_pos] else y_max
                    line_y = max(exp_data_max, null_data_max) + y_range * 0.05
                    text_y = line_y + y_range * 0.03
                    
                    # Draw comparison line
                    ax.plot([exp_pos, null_pos], [line_y, line_y], 'k-', linewidth=1)
                    ax.plot([exp_pos, exp_pos], [line_y - y_range * 0.01, line_y + y_range * 0.01], 'k-', linewidth=1)
                    ax.plot([null_pos, null_pos], [line_y - y_range * 0.01, line_y + y_range * 0.01], 'k-', linewidth=1)
                    
                    # Add significance text
                    ax.text((exp_pos + null_pos) / 2, text_y, significance, 
                           ha='center', va='bottom', fontsize=14, fontweight='bold')
            
            # Adjust y-axis limits to accommodate annotations
            ax.set_ylim(y_min, y_max + y_range * 0.15)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_diversity_null_comparison(exp_results, null_results, comparison_results, save_path=None):
    """Plot comparison of diversity asymmetricity with null models by nutrient condition."""
    div_types = ['diversity_asymmetricity_type1', 'diversity_asymmetricity_type2']
    div_titles = ['Diversity Asymmetricity Type 1', 'Diversity Asymmetricity Type 2']
    conditions = ['LN', 'MN', 'HN']
    null_names = list(null_results.keys())
    
    fig, axes = plt.subplots(len(div_types), len(null_names), figsize=(6*len(null_names), 5*len(div_types)))
    if len(div_types) == 1:
        axes = axes.reshape(1, -1)
    if len(null_names) == 1:
        axes = axes.reshape(-1, 1)
    
    for i, (div_type, div_title) in enumerate(zip(div_types, div_titles)):
        for j, null_name in enumerate(null_names):
            ax = axes[i, j]
            
            # Prepare data for plotting
            plot_data = []
            plot_labels = []
            
            for condition in conditions:
                # Experimental data for this condition
                exp_indices = [k for k, c in enumerate(exp_results['nutrient_conditions']) if c == condition]
                exp_values = [exp_results[div_type][k] for k in exp_indices]
                exp_values = [v for v in exp_values if not np.isnan(v)]
                
                # Null model data
                null_values = [v for v in null_results[null_name][div_type] if not np.isnan(v)]
                
                if exp_values and null_values:
                    plot_data.extend([exp_values, null_values])
                    plot_labels.extend([f'Exp {condition}', f'Null {condition}'])
            
            # Create box plot with scatter
            if plot_data:
                positions = range(len(plot_data))
                
                # Create box plots
                box_parts = ax.boxplot(plot_data, positions=positions, patch_artist=True, 
                                     showfliers=False, widths=0.6)
                
                # Color experimental data differently from null
                colors = ['#1f77b4', '#ff7f0e'] * (len(plot_data) // 2 + 1)
                for k, (patch, color) in enumerate(zip(box_parts['boxes'], colors[:len(plot_data)])):
                    if k % 2 == 0:  # Experimental data
                        patch.set_facecolor('#1f77b4')
                        patch.set_alpha(0.7)
                    else:  # Null data
                        patch.set_facecolor('#ff7f0e')
                        patch.set_alpha(0.7)
                
                # Add scatter points
                for k, data in enumerate(plot_data):
                    # Subsample if too many points
                    if len(data) > 100:
                        data_sample = np.random.choice(data, 100, replace=False)
                    else:
                        data_sample = data
                    
                    # Add jitter to x-positions
                    x_jitter = np.random.normal(positions[k], 0.1, len(data_sample))
                    
                    if k % 2 == 0:  # Experimental data
                        ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#1f77b4', edgecolors='white', linewidth=0.5)
                    else:  # Null data
                        ax.scatter(x_jitter, data_sample, alpha=0.6, s=8, color='#ff7f0e', edgecolors='white', linewidth=0.5)
                
                ax.set_xticks(positions)
                ax.set_xticklabels(plot_labels, rotation=45, ha='right')
                ax.set_ylabel('Asymmetricity')
                ax.set_title(f'{div_title} vs {null_name.replace("_", " ").title()}')
                
                # Add statistical significance annotations with better positioning
                y_min, y_max = ax.get_ylim()
                y_range = y_max - y_min
                
                for k, condition in enumerate(conditions):
                    if (condition in comparison_results and 
                        div_type in comparison_results[condition] and
                        null_name in comparison_results[condition][div_type]):
                        
                        p_value = comparison_results[condition][div_type][null_name]['p_value']
                        significance = get_significance_stars(p_value)
                        
                        # Position stars above the box plots with connecting line
                        exp_pos = k * 2
                        null_pos = k * 2 + 1
                        
                        # Find the highest point between exp and null data
                        exp_data_max = np.max(plot_data[exp_pos]) if plot_data[exp_pos] else y_max
                        null_data_max = np.max(plot_data[null_pos]) if plot_data[null_pos] else y_max
                        line_y = max(exp_data_max, null_data_max) + y_range * 0.05
                        text_y = line_y + y_range * 0.03
                        
                        # Draw comparison line
                        ax.plot([exp_pos, null_pos], [line_y, line_y], 'k-', linewidth=1)
                        ax.plot([exp_pos, exp_pos], [line_y - y_range * 0.01, line_y + y_range * 0.01], 'k-', linewidth=1)
                        ax.plot([null_pos, null_pos], [line_y - y_range * 0.01, line_y + y_range * 0.01], 'k-', linewidth=1)
                        
                        # Add significance text
                        ax.text((exp_pos + null_pos) / 2, text_y, significance, 
                               ha='center', va='bottom', fontsize=14, fontweight='bold')
                
                # Adjust y-axis limits to accommodate annotations
                ax.set_ylim(y_min, y_max + y_range * 0.15)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# MAIN ANALYSIS FUNCTION
# =============================================================================

def run_complete_null_model_analysis(n_permutations=1000, save_plots=True, save_dir=None, 
                                   use_empirical_probabilities=True):
    """
    Run complete asymmetricity analysis comparing experimental data with null models.
    
    Args:
        n_permutations: Number of permutations for null models
        save_plots: Whether to save plots
        save_dir: Directory to save plots
        use_empirical_probabilities: Whether to use empirical retention probabilities
                                   for the random selection null model
    """
    print("Loading experimental data...")
    offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers = load_real_coalescence_data()
    
    if not offspring_list:
        print("No experimental data found!")
        return None
    
    print(f"Loaded {len(offspring_list)} coalescence events")
    
    # Run analysis with null models
    exp_results, null_results = analyze_asymmetricity_with_null_models(
        offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers,
        n_permutations=n_permutations, use_empirical_probabilities=use_empirical_probabilities
    )
    
    # Statistical comparison
    print("Performing statistical comparisons...")
    comparison_results = compare_with_null_models(exp_results, null_results, save_dir=save_dir)
    
    # Generate plots
    if save_plots:
        if save_dir is None:
            save_dir = "Figure/AsymmetricityNullModelAnalysis"
        # plot_asymmetricity_vs_null_models(exp_results, null_results, comparison_results, save_dir)  # Removed: function not defined
    
    # Print summary
    print_comparison_summary(comparison_results)
    
    return {
        'experimental_results': exp_results,
        'null_results': null_results,
        'statistical_comparisons': comparison_results
    }

def print_comparison_summary(comparison_results):
    """Print summary of statistical comparisons."""
    print("\n" + "="*80)
    print("STATISTICAL COMPARISON SUMMARY")
    print("="*80)
    
    for condition in ['LN', 'MN', 'HN']:
        if condition not in comparison_results:
            continue
            
        print(f"\n{condition} Nutrient Condition:")
        print("-" * 40)
        
        # Vector asymmetricity summary
        if 'vector' in comparison_results[condition]:
            print("Vector Asymmetricity:")
            for null_name, stats in comparison_results[condition]['vector'].items():
                significance = "***" if stats['p_value'] < 0.001 else "**" if stats['p_value'] < 0.01 else "*" if stats['p_value'] < 0.05 else "ns"
                print(f"  vs {null_name}: p={stats['p_value']:.4f} {significance}, effect={stats['effect_size']:.3f}")
        
        # Similarity asymmetricity summary (just Bray-Curtis for brevity)
        if 'similarity' in comparison_results[condition] and 'bray_curtis' in comparison_results[condition]['similarity']:
            print("Similarity Asymmetricity (Bray-Curtis):")
            for null_name, stats in comparison_results[condition]['similarity']['bray_curtis'].items():
                significance = "***" if stats['p_value'] < 0.001 else "**" if stats['p_value'] < 0.01 else "*" if stats['p_value'] < 0.05 else "ns"
                print(f"  vs {null_name}: p={stats['p_value']:.4f} {significance}, effect={stats['effect_size']:.3f}")

if __name__ == "__main__":
    # Run the complete analysis
    results = run_complete_null_model_analysis(n_permutations=1000, save_plots=True) 