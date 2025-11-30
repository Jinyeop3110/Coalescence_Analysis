"""
AsymmetricityAnalysis.py - Comprehensive Asymmetricity Analysis for Coalescence Data

This module provides functions to analyze and visualize asymmetricity in microbial 
community coalescence across different metrics and nutrient conditions (LN, MN, HN).

Three types of asymmetricity are analyzed:
1. Similarity-based: |sim1-sim2|/(sim1+sim2)
2. Vector-based: Magnitude differences from vector decomposition
3. Diversity-based: Two different formulations using diversity metrics

Author: Gore Lab Coalescence Analysis Team
Date: July 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib to non-interactive backend to prevent plot pop-ups
plt.ioff()
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Import the enhanced VariousMetrics module
import VariousMetrics as vm

# =============================================================================
# ASYMMETRICITY CALCULATION FUNCTIONS
# =============================================================================

def calculate_similarity_asymmetricity(sim1, sim2):
    """
    Calculate similarity-based asymmetricity.
    
    Args:
        sim1, sim2: Similarity values to parent 1 and parent 2
    
    Returns:
        Asymmetricity value [0, 1] where 0 = symmetric, 1 = completely asymmetric
    """
    # Ensure similarity values are non-negative (handle edge cases)
    sim1 = max(0, sim1)
    sim2 = max(0, sim2)
    
    numerator = abs(sim1 - sim2)
    denominator = sim1 + sim2
    if denominator == 0:
        return 0
    return numerator / denominator

def calculate_vector_asymmetricity(magA, magB):
    """
    Calculate vector-based asymmetricity using arctangent approach.
    
    Uses arctan(magA/magB) - π/4 to measure deviation from perfect symmetry (45°),
    normalized to range [0, 1].
    
    Args:
        magA, magB: Magnitude values from vector decomposition
    
    Returns:
        Asymmetricity value [0, 1] where 0 = symmetric, 1 = completely asymmetric
    """
    
    # Handle edge cases
    if magA == 0 and magB == 0:
        return 0
    
    if magB == 0:
        # When magB is 0, we have complete asymmetry (90° or π/2)
        return 1
    
    # Calculate the angle using arctangent
    theta = np.arctan(magA / magB)
    
    # Calculate deviation from perfect symmetry (π/4 or 45°)
    deviation = np.abs(theta - np.pi/4)
    
    # Normalize to [0, 1] by dividing by maximum possible deviation (π/4)
    asymmetricity = deviation / (np.pi/4)
    
    return min(1, asymmetricity)  # Ensure the result is capped at 1

def calculate_diversity_asymmetricity_type1(div1_subcom, div2_subcom, div_mixedcom):
    """
    Calculate diversity-based asymmetricity (Type 1).
    
    Formula: |min(div1_subcom, div_mixedcom) - min(div2_subcom, div_mixedcom)| / div_mixedcom
    
    Args:
        div1_subcom: Diversity of subcommunity 1
        div2_subcom: Diversity of subcommunity 2  
        div_mixedcom: Diversity of mixed (coalescence) community
    
    Returns:
        Asymmetricity value [0, 1]
    """
    if div_mixedcom == 0:
        return 0
    
    min1 = min(div1_subcom, div_mixedcom)
    min2 = min(div2_subcom, div_mixedcom)
    numerator = abs(min1 - min2)
    
    return numerator / div_mixedcom

def calculate_diversity_asymmetricity_type2(div1_subcom, div2_subcom, div_mixedcom):
    """
    Calculate diversity-based asymmetricity (Type 2).
    
    Formula: |min(div1_subcom, div_mixedcom) - min(div2_subcom, div_mixedcom)| / 
             (div_mixedcom - min(div1_subcom, div2_subcom))
    
    Args:
        div1_subcom: Diversity of subcommunity 1
        div2_subcom: Diversity of subcommunity 2
        div_mixedcom: Diversity of mixed (coalescence) community
    
    Returns:
        Asymmetricity value [0, 1]
    """
    min1 = min(div1_subcom, div_mixedcom)
    min2 = min(div2_subcom, div_mixedcom)
    min_subs = min(div1_subcom, div2_subcom)
    
    numerator = abs(min1 - min2)
    denominator = div_mixedcom - min_subs
    
    if denominator <= 0:
        return 0
    
    return numerator / denominator

def calculate_retention_asymmetricity_base(parent1_vector, parent2_vector, mixed_vector, 
                                         threshold=1e-4, n_permutations=1000, version=1):
    """
    Base function for calculating retention-based asymmetricity between parent communities.
    
    This addresses the fundamental bias in diversity-based measures by focusing on
    retention rates rather than absolute species counts.
    
    Args:
        parent1_vector: Abundance vector for parent community 1
        parent2_vector: Abundance vector for parent community 2  
        mixed_vector: Abundance vector for mixed (coalescence) community
        threshold: Minimum abundance to consider species 'present'
        n_permutations: Number of permutations for significance testing
        version: 1 (exclude overlap species) or 2 (include overlap species)
    
    Returns:
        dict: {
            'asymmetricity': float,           # |R1 - R2| 
            'retention_rates': dict,          # Individual retention rates
            'p_value': float,                 # Permutation test p-value
            'significant': bool,              # p < 0.05
            'effect_size': str,               # Small/Medium/Large effect
            'species_breakdown': dict,        # Analysis by species type
            'null_distribution': dict,        # Permutation test results
            'version': int                    # Version used (1 or 2)
        }
    """
    import numpy as np
    
    # Identify present species (above threshold)
    parent1_present = parent1_vector > threshold
    parent2_present = parent2_vector > threshold
    mixed_present = mixed_vector > threshold
    
    # Species breakdown analysis
    overlap_species = parent1_present & parent2_present
    parent1_unique = parent1_present & ~parent2_present
    parent2_unique = parent2_present & ~parent1_present
    
    # Calculate species counts and retention based on version
    if version == 1:  # Exclude overlap species
        n_parent1_total = np.sum(parent1_unique)
        n_parent2_total = np.sum(parent2_unique)
        parent1_retained = np.sum(parent1_unique & mixed_present)
        parent2_retained = np.sum(parent2_unique & mixed_present)
        version_description = "unique species only (excluding overlaps)"
    else:  # Include overlap species (version 2)
        n_parent1_total = np.sum(parent1_present)
        n_parent2_total = np.sum(parent2_present)
        parent1_retained = np.sum(parent1_present & mixed_present)
        parent2_retained = np.sum(parent2_present & mixed_present)
        version_description = "all species (including overlaps)"
    
    # Handle edge cases
    if n_parent1_total == 0 and n_parent2_total == 0:
        return {
            'asymmetricity': 0.0,
            'retention_rates': {'parent1': 0.0, 'parent2': 0.0},
            'p_value': 1.0,
            'significant': False,
            'effect_size': 'None',
            'species_breakdown': {},
            'null_distribution': {'mean': 0.0, 'std': 0.0}
        }
    
    # Calculate retention rates
    retention_1 = parent1_retained / n_parent1_total if n_parent1_total > 0 else 0.0
    retention_2 = parent2_retained / n_parent2_total if n_parent2_total > 0 else 0.0
    
    # Observed asymmetricity
    observed_asymmetricity = abs(retention_1 - retention_2)
    
    # Additional species breakdown for analysis
    n_overlap = np.sum(overlap_species)
    n_p1_unique = np.sum(parent1_unique)
    n_p2_unique = np.sum(parent2_unique)
    
    overlap_retained = np.sum(overlap_species & mixed_present)
    p1_unique_retained = np.sum(parent1_unique & mixed_present)
    p2_unique_retained = np.sum(parent2_unique & mixed_present)
    
    species_breakdown = {
        'overlap': {
            'total': n_overlap,
            'retained': overlap_retained,
            'retention_rate': overlap_retained / n_overlap if n_overlap > 0 else 0.0
        },
        'parent1_unique': {
            'total': n_p1_unique,
            'retained': p1_unique_retained,
            'retention_rate': p1_unique_retained / n_p1_unique if n_p1_unique > 0 else 0.0
        },
        'parent2_unique': {
            'total': n_p2_unique,
            'retained': p2_unique_retained,
            'retention_rate': p2_unique_retained / n_p2_unique if n_p2_unique > 0 else 0.0
        }
    }
    
    # Permutation test for significance
    null_asymmetries = []
    total_species = n_parent1_total + n_parent2_total
    total_retained = parent1_retained + parent2_retained
    
    if total_species > 0 and n_permutations > 0:
        np.random.seed(42)  # For reproducibility
        
        for _ in range(n_permutations):
            # Create array representing all species: 1=retained, 0=lost
            species_fates = [1] * total_retained + [0] * (total_species - total_retained)
            np.random.shuffle(species_fates)
            
            # Randomly assign to parent groups
            null_p1_retained = sum(species_fates[:n_parent1_total])
            null_p2_retained = sum(species_fates[n_parent1_total:n_parent1_total + n_parent2_total])
            
            null_r1 = null_p1_retained / n_parent1_total if n_parent1_total > 0 else 0.0
            null_r2 = null_p2_retained / n_parent2_total if n_parent2_total > 0 else 0.0
            
            null_asymmetries.append(abs(null_r1 - null_r2))
    
    # Calculate p-value
    if len(null_asymmetries) > 0:
        p_value = sum(1 for x in null_asymmetries if x >= observed_asymmetricity) / len(null_asymmetries)
        null_mean = np.mean(null_asymmetries)
        null_std = np.std(null_asymmetries)
    else:
        p_value = 1.0
        null_mean = 0.0
        null_std = 0.0
    
    # Effect size classification
    if observed_asymmetricity < 0.1:
        effect_size = 'Small'
    elif observed_asymmetricity < 0.3:
        effect_size = 'Medium'
    else:
        effect_size = 'Large'
    
    return {
        'asymmetricity': observed_asymmetricity,
        'retention_rates': {
            'parent1': retention_1,
            'parent2': retention_2
        },
        'p_value': p_value,
        'significant': p_value < 0.05,
        'effect_size': effect_size,
        'species_breakdown': species_breakdown,
        'null_distribution': {
            'mean': null_mean,
            'std': null_std,
            'values': null_asymmetries[:100] if len(null_asymmetries) > 100 else null_asymmetries  # Store first 100 for plotting
        },
        'version': version,
        'version_description': version_description
    }

def calculate_retention_asymmetricity_type1(parent1_vector, parent2_vector, mixed_vector, 
                                          threshold=1e-4, n_permutations=1000):
    """
    Calculate retention-based asymmetricity excluding overlap species (Version 1).
    
    This version focuses on unique species from each parent, similar to the
    diversity asymmetricity type 1 approach.
    """
    return calculate_retention_asymmetricity_base(parent1_vector, parent2_vector, mixed_vector,
                                                threshold, n_permutations, version=1)

def calculate_retention_asymmetricity_type2(parent1_vector, parent2_vector, mixed_vector,
                                          threshold=1e-4, n_permutations=1000):
    """
    Calculate retention-based asymmetricity including overlap species (Version 2).
    
    This version considers all species from both parents, similar to the
    diversity asymmetricity type 2 approach.
    """
    return calculate_retention_asymmetricity_base(parent1_vector, parent2_vector, mixed_vector,
                                                threshold, n_permutations, version=2)

# =============================================================================
# COMPREHENSIVE ASYMMETRICITY ANALYSIS
# =============================================================================

def analyze_single_coalescence_asymmetricity(offspring, parent1, parent2, 
                                           similarity_metrics=['bray_curtis', 'jensen_shannon'],
                                           diversity_threshold=1e-4,
                                           threshold=0):
    """
    Analyze all types of asymmetricity for a single coalescence event.
    
    Args:
        offspring: Offspring community abundance vector
        parent1, parent2: Parent community abundance vectors
        similarity_metrics: List of similarity metrics to analyze
        diversity_threshold: Threshold for counting species in diversity calculation (default 1e-4)
        threshold: Abundance threshold for similarity calculations
    
    Returns:
        Dictionary with all asymmetricity results
    """
    results = {
        'similarity_asymmetricity': {},
        'vector_asymmetricity': {},
        'diversity_asymmetricity_type1': {},
        'diversity_asymmetricity_type2': {},
        'retention_asymmetricity': {}
    }
    
    # 1. Similarity-based asymmetricity
    for metric in similarity_metrics:
        sim_func = vm.get_similarity_function(metric)
        sim1 = sim_func(offspring, parent1, threshold)
        sim2 = sim_func(offspring, parent2, threshold)
        
        asym = calculate_similarity_asymmetricity(sim1, sim2)
        results['similarity_asymmetricity'][metric] = {
            'asymmetricity': asym,
            'sim1': sim1,
            'sim2': sim2
        }
    
    # 2. Vector-based asymmetricity
    vector_decomp = vm.coalescence_vector_decomposition(parent1, parent2, offspring, threshold)
    magA = vector_decomp['positive_coefficient_parent1']
    magB = vector_decomp['positive_coefficient_parent2']
    
    vector_asym = calculate_vector_asymmetricity(magA, magB)
    results['vector_asymmetricity'] = {
        'asymmetricity': vector_asym,
        'magA': magA,
        'magB': magB,
        'residual_magnitude': vector_decomp['residual_magnitude']
    }
    
    # 3. Diversity-based asymmetricity (using only absolute diversity/richness)
    # Calculate richness (number of species above diversity_threshold)
    div1_subcom = np.sum(parent1 > diversity_threshold)
    div2_subcom = np.sum(parent2 > diversity_threshold)
    div_mixedcom = np.sum(offspring > diversity_threshold)
    
    asym_type1 = calculate_diversity_asymmetricity_type1(div1_subcom, div2_subcom, div_mixedcom)
    asym_type2 = calculate_diversity_asymmetricity_type2(div1_subcom, div2_subcom, div_mixedcom)
    
    results['diversity_asymmetricity_type1']['richness'] = {
        'asymmetricity': asym_type1,
        'div1_subcom': div1_subcom,
        'div2_subcom': div2_subcom,
        'div_mixedcom': div_mixedcom
    }
    
    results['diversity_asymmetricity_type2']['richness'] = {
        'asymmetricity': asym_type2,
        'div1_subcom': div1_subcom,
        'div2_subcom': div2_subcom,
        'div_mixedcom': div_mixedcom
    }
    
    # 4. Retention-based asymmetricity (both types)
    retention_type1 = calculate_retention_asymmetricity_type1(parent1, parent2, offspring, 
                                                            threshold=diversity_threshold)
    retention_type2 = calculate_retention_asymmetricity_type2(parent1, parent2, offspring,
                                                            threshold=diversity_threshold)
    results['retention_asymmetricity'] = {
        'type1': retention_type1,
        'type2': retention_type2
    }
    
    return results

def analyze_multiple_coalescence_asymmetricity(offspring_list, parent1_list, parent2_list,
                                             nutrient_conditions, species_numbers=None,
                                             similarity_metrics=['bray_curtis', 'jensen_shannon'],
                                             diversity_threshold=1e-4,
                                             threshold=0):
    """
    Analyze asymmetricity across multiple coalescence events with nutrient conditions and species numbers.
    
    Args:
        offspring_list: List of offspring communities
        parent1_list: List of parent1 communities
        parent2_list: List of parent2 communities
        nutrient_conditions: List of nutrient conditions ('LN', 'MN', 'HN')
        species_numbers: List of species numbers for each event
        similarity_metrics: List of similarity metrics to analyze
        diversity_threshold: Threshold for counting species in diversity calculation (default 1e-4)
        threshold: Abundance threshold for similarity calculations
    
    Returns:
        Comprehensive results dictionary organized by nutrient condition and species number
    """
    # Initialize results structure
    conditions = ['LN', 'MN', 'HN']
    results = {condition: {
        'similarity_asymmetricity': {metric: [] for metric in similarity_metrics},
        'vector_asymmetricity': [],
        'diversity_asymmetricity_type1': {'richness': []},
        'diversity_asymmetricity_type2': {'richness': []},
        'retention_asymmetricity': {
            'type1': {'asymmetricity': [], 'p_values': [], 'significant': []},
            'type2': {'asymmetricity': [], 'p_values': [], 'significant': []}
        },
        'species_numbers': []  # Add species numbers tracking
    } for condition in conditions}
    
    # Create species-specific results structure
    unique_species = sorted(set(species_numbers))
    results_by_species = {}
    for sp_num in unique_species:
        results_by_species[sp_num] = {condition: {
            'similarity_asymmetricity': {metric: [] for metric in similarity_metrics},
            'vector_asymmetricity': [],
            'diversity_asymmetricity_type1': {'richness': []},
            'diversity_asymmetricity_type2': {'richness': []},
            'retention_asymmetricity': {
                'type1': {'asymmetricity': [], 'p_values': [], 'significant': []},
                'type2': {'asymmetricity': [], 'p_values': [], 'significant': []}
            }
        } for condition in conditions}
    
    # Analyze each coalescence event
    for i, (offspring, parent1, parent2, condition) in enumerate(
        zip(offspring_list, parent1_list, parent2_list, nutrient_conditions)):
        
        if condition not in conditions:
            continue
            
        # Get species number for this event
        sp_num = species_numbers[i]
            
        # Get single event analysis
        event_results = analyze_single_coalescence_asymmetricity(
            offspring, parent1, parent2, similarity_metrics, diversity_threshold, threshold
        )
        
        # Store results by condition
        # Similarity asymmetricity
        for metric in similarity_metrics:
            asym_val = event_results['similarity_asymmetricity'][metric]['asymmetricity']
            results[condition]['similarity_asymmetricity'][metric].append(asym_val)
            
            # Store in species-specific results
            if sp_num in results_by_species:
                results_by_species[sp_num][condition]['similarity_asymmetricity'][metric].append(asym_val)
        
        # Vector asymmetricity
        vector_asym = event_results['vector_asymmetricity']['asymmetricity']
        results[condition]['vector_asymmetricity'].append(vector_asym)
        if sp_num in results_by_species:
            results_by_species[sp_num][condition]['vector_asymmetricity'].append(vector_asym)
        
        # Diversity asymmetricity (only richness)
        asym_type1 = event_results['diversity_asymmetricity_type1']['richness']['asymmetricity']
        asym_type2 = event_results['diversity_asymmetricity_type2']['richness']['asymmetricity']
        
        results[condition]['diversity_asymmetricity_type1']['richness'].append(asym_type1)
        results[condition]['diversity_asymmetricity_type2']['richness'].append(asym_type2)
        
        if sp_num in results_by_species:
            results_by_species[sp_num][condition]['diversity_asymmetricity_type1']['richness'].append(asym_type1)
            results_by_species[sp_num][condition]['diversity_asymmetricity_type2']['richness'].append(asym_type2)
        
        # Retention asymmetricity (both types)
        retention_type1 = event_results['retention_asymmetricity']['type1']
        retention_type2 = event_results['retention_asymmetricity']['type2']
        
        results[condition]['retention_asymmetricity']['type1']['asymmetricity'].append(retention_type1['asymmetricity'])
        results[condition]['retention_asymmetricity']['type1']['p_values'].append(retention_type1['p_value'])
        results[condition]['retention_asymmetricity']['type1']['significant'].append(retention_type1['significant'])
        
        results[condition]['retention_asymmetricity']['type2']['asymmetricity'].append(retention_type2['asymmetricity'])
        results[condition]['retention_asymmetricity']['type2']['p_values'].append(retention_type2['p_value'])
        results[condition]['retention_asymmetricity']['type2']['significant'].append(retention_type2['significant'])
        
        if sp_num in results_by_species:
            results_by_species[sp_num][condition]['retention_asymmetricity']['type1']['asymmetricity'].append(retention_type1['asymmetricity'])
            results_by_species[sp_num][condition]['retention_asymmetricity']['type1']['p_values'].append(retention_type1['p_value'])
            results_by_species[sp_num][condition]['retention_asymmetricity']['type1']['significant'].append(retention_type1['significant'])
            
            results_by_species[sp_num][condition]['retention_asymmetricity']['type2']['asymmetricity'].append(retention_type2['asymmetricity'])
            results_by_species[sp_num][condition]['retention_asymmetricity']['type2']['p_values'].append(retention_type2['p_value'])
            results_by_species[sp_num][condition]['retention_asymmetricity']['type2']['significant'].append(retention_type2['significant'])
        
        # Track species numbers
        results[condition]['species_numbers'].append(sp_num)
    
    # Return both overall and species-specific results
    return {'overall': results, 'by_species': results_by_species}

# =============================================================================
# PLOTTING FUNCTIONS
# =============================================================================

def plot_similarity_asymmetricity(results_dict, similarity_metrics, 
                                 figsize=(8, 6), save_path_prefix=None):
    """
    Plot similarity-based asymmetricity across nutrient conditions, creating separate plots for each metric.
    
    Args:
        results_dict: Results from analyze_multiple_coalescence_asymmetricity
        similarity_metrics: List of similarity metrics to plot
        figsize: Figure size tuple for each individual plot
        save_path_prefix: Optional path prefix to save the figures (will append metric name)
    """
    conditions = ['LN', 'MN', 'HN']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
    
    for metric in similarity_metrics:
        # Create individual plot for each metric
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        
        # Prepare data for plotting
        plot_data = []
        for condition in conditions:
            asym_values = results_dict[condition]['similarity_asymmetricity'][metric]
            for val in asym_values:
                plot_data.append({'Condition': condition, 'Asymmetricity': val})
        
        plot_df = pd.DataFrame(plot_data)
        
        # Create box plot
        sns.boxplot(data=plot_df, x='Condition', y='Asymmetricity', 
                   palette=colors, ax=ax)
        
        # Add individual points
        sns.stripplot(data=plot_df, x='Condition', y='Asymmetricity', 
                     color='black', alpha=0.5, size=3, ax=ax)
        
        ax.set_title(f'{metric.replace("_", " ").title()} Similarity Asymmetricity')
        ax.set_ylabel('Asymmetricity [0-1]')
        ax.set_ylim(0, 1)
        
        # Add statistical annotations
        for j, condition in enumerate(conditions):
            values = results_dict[condition]['similarity_asymmetricity'][metric]
            mean_val = np.mean(values)
            std_val = np.std(values)
            ax.text(j, 0.95, f'μ={mean_val:.3f}\nσ={std_val:.3f}', ha='center', va='top',
                   transform=ax.get_xaxis_transform(),
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        plt.tight_layout()
        
        # Save individual plot if path provided
        if save_path_prefix:
            save_path = f"{save_path_prefix}_{metric}_asymmetricity.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved similarity asymmetricity plot for {metric}: {save_path}")
        
        plt.close()  # Close to prevent memory issues

def plot_vector_asymmetricity(results_dict, figsize=(10, 6), save_path=None):
    """
    Plot vector-based asymmetricity across nutrient conditions.
    
    Args:
        results_dict: Results from analyze_multiple_coalescence_asymmetricity
        figsize: Figure size tuple
        save_path: Optional path to save the figure
    """
    conditions = ['LN', 'MN', 'HN']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    # Prepare data
    plot_data = []
    for condition in conditions:
        asym_values = results_dict[condition]['vector_asymmetricity']
        for val in asym_values:
            plot_data.append({'Condition': condition, 'Asymmetricity': val})
    
    plot_df = pd.DataFrame(plot_data)
    
    # Create plot
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    # Box plot
    sns.boxplot(data=plot_df, x='Condition', y='Asymmetricity', 
               palette=colors, ax=ax)
    
    # Individual points
    sns.stripplot(data=plot_df, x='Condition', y='Asymmetricity', 
                 color='black', alpha=0.5, size=4, ax=ax)
    
    ax.set_title('Vector-Based Asymmetricity Analysis')
    ax.set_ylabel('Asymmetricity [0-1]')
    ax.set_ylim(0, 1)
    
    # Add statistical annotations
    for i, condition in enumerate(conditions):
        values = results_dict[condition]['vector_asymmetricity']
        mean_val = np.mean(values)
        std_val = np.std(values)
        ax.text(i, 0.95, f'μ={mean_val:.3f}\nσ={std_val:.3f}', ha='center', va='top',
               transform=ax.get_xaxis_transform(),
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved vector asymmetricity plot: {save_path}")
    
    plt.close()  # Close to prevent memory issues

def plot_diversity_asymmetricity(results_dict, asymm_type='type1',
                                figsize=(10, 6), save_path=None):
    """
    Plot diversity-based asymmetricity across nutrient conditions (richness only).
    
    Args:
        results_dict: Results from analyze_multiple_coalescence_asymmetricity
        asymm_type: 'type1' or 'type2' for different asymmetricity formulations
        figsize: Figure size tuple
        save_path: Optional path to save the figure
    """
    conditions = ['LN', 'MN', 'HN']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    asymm_key = f'diversity_asymmetricity_{asymm_type}'
    
    # Create single plot for richness
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    # Prepare data for plotting
    plot_data = []
    for condition in conditions:
        asym_values = results_dict[condition][asymm_key]['richness']
        for val in asym_values:
            plot_data.append({'Condition': condition, 'Asymmetricity': val})
    
    plot_df = pd.DataFrame(plot_data)
    
    # Create box plot
    sns.boxplot(data=plot_df, x='Condition', y='Asymmetricity', 
               palette=colors, ax=ax)
    
    # Add individual points
    sns.stripplot(data=plot_df, x='Condition', y='Asymmetricity', 
                 color='black', alpha=0.5, size=3, ax=ax)
    
    ax.set_title(f'Richness Diversity Asymmetricity ({asymm_type.upper()})')
    ax.set_ylabel('Asymmetricity [0-1]')
    ax.set_ylim(0, 1)
    
    # Add statistical annotations
    for j, condition in enumerate(conditions):
        values = results_dict[condition][asymm_key]['richness']
        mean_val = np.mean(values)
        ax.text(j, 0.95, f'μ={mean_val:.3f}', ha='center', va='top',
               transform=ax.get_xaxis_transform(),
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved diversity asymmetricity {asymm_type} plot: {save_path}")
    
    plt.close()  # Close to prevent memory issues

def plot_comprehensive_asymmetricity_comparison(results_dict, 
                                              similarity_metrics=['bray_curtis'],
                                              figsize=(18, 12), save_path=None):
    """
    Create a comprehensive comparison plot of all asymmetricity types.
    
    Args:
        results_dict: Results from analyze_multiple_coalescence_asymmetricity
        similarity_metrics: List of similarity metrics (first one used)
        figsize: Figure size tuple
        save_path: Optional path to save the figure
    """
    conditions = ['LN', 'MN', 'HN']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    # Use first similarity metric for comparison
    sim_metric = similarity_metrics[0]
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # 1. Similarity asymmetricity
    plot_data = []
    for condition in conditions:
        values = results_dict[condition]['similarity_asymmetricity'][sim_metric]
        for val in values:
            plot_data.append({'Condition': condition, 'Asymmetricity': val, 
                            'Type': 'Similarity'})
    
    plot_df = pd.DataFrame(plot_data)
    sns.boxplot(data=plot_df, x='Condition', y='Asymmetricity', 
               palette=colors, ax=axes[0, 0])
    sns.stripplot(data=plot_df, x='Condition', y='Asymmetricity', 
                 color='black', alpha=0.5, size=3, ax=axes[0, 0])
    axes[0, 0].set_title(f'Similarity Asymmetricity ({sim_metric})')
    axes[0, 0].set_ylim(0, 1)
    
    # 2. Vector asymmetricity
    plot_data = []
    for condition in conditions:
        values = results_dict[condition]['vector_asymmetricity']
        for val in values:
            plot_data.append({'Condition': condition, 'Asymmetricity': val, 
                            'Type': 'Vector'})
    
    plot_df = pd.DataFrame(plot_data)
    sns.boxplot(data=plot_df, x='Condition', y='Asymmetricity', 
               palette=colors, ax=axes[0, 1])
    sns.stripplot(data=plot_df, x='Condition', y='Asymmetricity', 
                 color='black', alpha=0.5, size=3, ax=axes[0, 1])
    axes[0, 1].set_title('Vector Asymmetricity')
    axes[0, 1].set_ylim(0, 1)
    
    # 3. Diversity asymmetricity type 1 (richness)
    plot_data = []
    for condition in conditions:
        values = results_dict[condition]['diversity_asymmetricity_type1']['richness']
        for val in values:
            plot_data.append({'Condition': condition, 'Asymmetricity': val, 
                            'Type': 'Diversity Type1'})
    
    plot_df = pd.DataFrame(plot_data)
    sns.boxplot(data=plot_df, x='Condition', y='Asymmetricity', 
               palette=colors, ax=axes[1, 0])
    sns.stripplot(data=plot_df, x='Condition', y='Asymmetricity', 
                 color='black', alpha=0.5, size=3, ax=axes[1, 0])
    axes[1, 0].set_title('Richness Asymmetricity Type1')
    axes[1, 0].set_ylim(0, 1)
    
    # 4. Diversity asymmetricity type 2 (richness)
    plot_data = []
    for condition in conditions:
        values = results_dict[condition]['diversity_asymmetricity_type2']['richness']
        for val in values:
            plot_data.append({'Condition': condition, 'Asymmetricity': val, 
                            'Type': 'Diversity Type2'})
    
    plot_df = pd.DataFrame(plot_data)
    sns.boxplot(data=plot_df, x='Condition', y='Asymmetricity', 
               palette=colors, ax=axes[1, 1])
    sns.stripplot(data=plot_df, x='Condition', y='Asymmetricity', 
                 color='black', alpha=0.5, size=3, ax=axes[1, 1])
    axes[1, 1].set_title('Richness Asymmetricity Type2')
    axes[1, 1].set_ylim(0, 1)
    
    plt.tight_layout()
    plt.suptitle('Comprehensive Asymmetricity Comparison Across Nutrient Conditions', 
                y=1.02, fontsize=16)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved comprehensive asymmetricity plot: {save_path}")
    
    plt.close()  # Close to prevent memory issues

# =============================================================================
# STATISTICAL ANALYSIS FUNCTIONS
# =============================================================================

def perform_asymmetricity_statistical_tests(results_dict, alpha=0.05):
    """
    Perform statistical tests to compare asymmetricity across nutrient conditions.
    
    Args:
        results_dict: Results from analyze_multiple_coalescence_asymmetricity
        alpha: Significance level for tests
    
    Returns:
        Dictionary with statistical test results
    """
    conditions = ['LN', 'MN', 'HN']
    stat_results = {}
    
    # Test similarity asymmetricity
    stat_results['similarity'] = {}
    for metric in results_dict['LN']['similarity_asymmetricity'].keys():
        ln_vals = results_dict['LN']['similarity_asymmetricity'][metric]
        mn_vals = results_dict['MN']['similarity_asymmetricity'][metric]
        hn_vals = results_dict['HN']['similarity_asymmetricity'][metric]
        
        # Kruskal-Wallis test (non-parametric ANOVA)
        h_stat, p_val = stats.kruskal(ln_vals, mn_vals, hn_vals)
        
        stat_results['similarity'][metric] = {
            'kruskal_wallis_h': h_stat,
            'p_value': p_val,
            'significant': p_val < alpha
        }
    
    # Test vector asymmetricity
    ln_vals = results_dict['LN']['vector_asymmetricity']
    mn_vals = results_dict['MN']['vector_asymmetricity']
    hn_vals = results_dict['HN']['vector_asymmetricity']
    
    h_stat, p_val = stats.kruskal(ln_vals, mn_vals, hn_vals)
    stat_results['vector'] = {
        'kruskal_wallis_h': h_stat,
        'p_value': p_val,
        'significant': p_val < alpha
    }
    
    # Test diversity asymmetricity (only richness)
    for asymm_type in ['type1', 'type2']:
        asymm_key = f'diversity_asymmetricity_{asymm_type}'
        
        ln_vals = results_dict['LN'][asymm_key]['richness']
        mn_vals = results_dict['MN'][asymm_key]['richness']
        hn_vals = results_dict['HN'][asymm_key]['richness']
        
        h_stat, p_val = stats.kruskal(ln_vals, mn_vals, hn_vals)
        
        stat_results[f'diversity_{asymm_type}'] = {
            'richness': {
                'kruskal_wallis_h': h_stat,
                'p_value': p_val,
                'significant': p_val < alpha
            }
        }
    
    return stat_results

def generate_asymmetricity_summary_table(results_dict, stat_results=None):
    """
    Generate a summary table of asymmetricity results.
    
    Args:
        results_dict: Results from analyze_multiple_coalescence_asymmetricity
        stat_results: Optional statistical test results
    
    Returns:
        Pandas DataFrame with summary statistics
    """
    conditions = ['LN', 'MN', 'HN']
    summary_data = []
    
    # Similarity asymmetricity
    for metric in results_dict['LN']['similarity_asymmetricity'].keys():
        for condition in conditions:
            values = results_dict[condition]['similarity_asymmetricity'][metric]
            
            summary_data.append({
                'Asymmetricity_Type': 'Similarity',
                'Metric': metric,
                'Condition': condition,
                'Mean': np.mean(values),
                'Std': np.std(values),
                'Median': np.median(values),
                'Min': np.min(values),
                'Max': np.max(values),
                'N': len(values)
            })
    
    # Vector asymmetricity
    for condition in conditions:
        values = results_dict[condition]['vector_asymmetricity']
        
        summary_data.append({
            'Asymmetricity_Type': 'Vector',
            'Metric': 'magnitude_difference',
            'Condition': condition,
            'Mean': np.mean(values),
            'Std': np.std(values),
            'Median': np.median(values),
            'Min': np.min(values),
            'Max': np.max(values),
            'N': len(values)
        })
    
    # Diversity asymmetricity (only richness)
    for asymm_type in ['type1', 'type2']:
        asymm_key = f'diversity_asymmetricity_{asymm_type}'
        
        for condition in conditions:
            values = results_dict[condition][asymm_key]['richness']
            
            summary_data.append({
                'Asymmetricity_Type': f'Diversity_{asymm_type}',
                'Metric': 'richness',
                'Condition': condition,
                'Mean': np.mean(values),
                'Std': np.std(values),
                'Median': np.median(values),
                'Min': np.min(values),
                'Max': np.max(values),
                'N': len(values)
            })
    
    summary_df = pd.DataFrame(summary_data)
    return summary_df

# =============================================================================
# SPECIES-SPECIFIC PLOTTING FUNCTIONS
# =============================================================================

def plot_asymmetricity_by_species_single(results_dict, asymmetricity_type='similarity', 
                                        metric='bray_curtis', target_species=[6, 12, 24],
                                        figsize=(15, 5), save_path=None):
    """
    Plot asymmetricity results grouped first by nutrient condition, then by species number.
    Creates 3 subplots (one for each nutrient condition) with bars for each species number.
    
    Args:
        results_dict: Results dictionary with 'by_species' key
        asymmetricity_type: Type of asymmetricity ('similarity', 'vector', 'diversity_type1', 'diversity_type2')
        metric: Specific metric to plot (for similarity metrics)
        target_species: List of species numbers to plot [6, 12, 24]
        figsize: Figure size tuple
        save_path: Optional path to save the figure
    """
    species_data = results_dict['by_species']
    conditions = ['LN', 'MN', 'HN']
    
    # Filter to only available target species
    available_species = [sp for sp in target_species if sp in species_data]
    if not available_species:
        print(f"None of the target species {target_species} found in data.")
        return
    
    # Create figure with subplots for each nutrient condition
    fig, axes = plt.subplots(1, 3, figsize=figsize, sharey=True)
    
    # Define colors for each species
    species_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green for different species
    
    for i, condition in enumerate(conditions):
        ax = axes[i]
        
        # Prepare data for this nutrient condition
        condition_data = []
        
        for sp_num in available_species:
            sp_results = species_data[sp_num][condition]
            
            if asymmetricity_type == 'similarity':
                values = sp_results['similarity_asymmetricity'][metric]
            elif asymmetricity_type == 'vector':
                values = sp_results['vector_asymmetricity']
            elif asymmetricity_type == 'diversity_type1':
                values = sp_results['diversity_asymmetricity_type1']['richness']
            elif asymmetricity_type == 'diversity_type2':
                values = sp_results['diversity_asymmetricity_type2']['richness']
            else:
                print(f"Unknown asymmetricity type: {asymmetricity_type}")
                return
            
            for val in values:
                condition_data.append({
                    'Species_Number': sp_num,
                    'Asymmetricity': val
                })
        
        if not condition_data:
            ax.set_title(f'{condition} (No data)')
            continue
        
        condition_df = pd.DataFrame(condition_data)
        
        # Create box plot for this condition
        sns.boxplot(data=condition_df, x='Species_Number', y='Asymmetricity', 
                   palette=species_colors[:len(available_species)], ax=ax)
        
        # Add individual points
        sns.stripplot(data=condition_df, x='Species_Number', y='Asymmetricity', 
                     color='black', alpha=0.5, size=3, ax=ax)
        
        # Customize subplot
        ax.set_title(f'{condition} Condition', fontsize=12, fontweight='bold')
        ax.set_xlabel('Species Number', fontsize=10)
        if i == 0:  # Only label y-axis on the first subplot
            ax.set_ylabel('Asymmetricity [0-1]', fontsize=10)
        else:
            ax.set_ylabel('')
        ax.set_ylim(0, 1)
        
        # Add statistical annotations
        for j, sp_num in enumerate(available_species):
            species_data_subset = condition_df[condition_df['Species_Number'] == sp_num]['Asymmetricity']
            if len(species_data_subset) > 0:
                mean_val = species_data_subset.mean()
                std_val = species_data_subset.std()
                ax.text(j, 0.95, f'μ={mean_val:.3f}\nσ={std_val:.3f}', 
                       ha='center', va='top', transform=ax.get_xaxis_transform(),
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8),
                       fontsize=8)
    
    # Set overall title
    title_map = {
        'similarity': f'{metric.replace("_", " ").title()} Similarity',
        'vector': 'Vector-Based',
        'diversity_type1': 'Diversity Type 1',
        'diversity_type2': 'Diversity Type 2'
    }
    fig.suptitle(f'{title_map.get(asymmetricity_type, asymmetricity_type)} Asymmetricity by Nutrient Condition', 
                 fontsize=14, y=1.02)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved species-specific asymmetricity plot: {save_path}")
    
    plt.close()  # Close to prevent showing
    ax.set_xlabel('Species Number')
    ax.set_ylabel('Mean Asymmetricity')
    
    # Set title based on asymmetricity type
    title_map = {
        'similarity': f'{metric.replace("_", " ").title()} Similarity Asymmetricity',
        'vector': 'Vector-Based Asymmetricity',
        'diversity_type1': 'Diversity Asymmetricity (Type 1)',
        'diversity_type2': 'Diversity Asymmetricity (Type 2)'
    }
    ax.set_title(title_map.get(asymmetricity_type, asymmetricity_type))
    
def plot_all_asymmetricity_by_species(results_dict, target_species=[6, 12, 24], 
                                     save_path_prefix=None):
    """
    Plot all types of asymmetricity for specific species numbers grouped by nutrient condition.
    
    Args:
        results_dict: Results dictionary with 'by_species' key
        target_species: List of species numbers to plot [6, 12, 24]
        save_path_prefix: Optional prefix for saving plots
    """
    if 'by_species' not in results_dict:
        print("No species-specific data available. Run analysis with species_numbers parameter.")
        return
    
    # Get available similarity metrics
    sample_species = list(results_dict['by_species'].keys())[0]
    sample_condition = 'LN'
    similarity_metrics = list(results_dict['by_species'][sample_species][sample_condition]['similarity_asymmetricity'].keys())
    
    # Plot similarity asymmetricity for each metric
    for metric in similarity_metrics:
        save_path = f"{save_path_prefix}_similarity_{metric}_by_species.png"
        plot_asymmetricity_by_species_single(results_dict, 'similarity', metric, 
                                            target_species, save_path=save_path)
    
    # Plot vector asymmetricity
    save_path = f"{save_path_prefix}_vector_by_species.png"
    plot_asymmetricity_by_species_single(results_dict, 'vector', target_species=target_species,
                                        save_path=save_path)
    
    # Plot diversity asymmetricity type 1
    save_path = f"{save_path_prefix}_diversity_type1_by_species.png"
    plot_asymmetricity_by_species_single(results_dict, 'diversity_type1', target_species=target_species,
                                        save_path=save_path)
    
    # Plot diversity asymmetricity type 2
    save_path = f"{save_path_prefix}_diversity_type2_by_species.png"
    plot_asymmetricity_by_species_single(results_dict, 'diversity_type2', target_species=target_species,
                                        save_path=save_path)

def create_species_summary_barplot(results_dict, target_species=[6, 12, 24], save_path=None):
    """
    Create summary barplot showing asymmetricity trends for specific species numbers.
    
    Args:
        results_dict: Results dictionary with 'by_species' key
        target_species: List of species numbers to plot [6, 12, 24]
        save_path: Optional path to save the figure
    """
    species_data = results_dict['by_species']
    conditions = ['LN', 'MN', 'HN']
    
    # Filter to only available target species
    available_species = [sp for sp in target_species if sp in species_data]
    if not available_species:
        print(f"None of the target species {target_species} found in data.")
        return
    
    # Calculate mean asymmetricity for each species and condition
    summary_data = []
    
    for sp_num in available_species:
        for condition in conditions:
            sp_results = species_data[sp_num][condition]
            
            # Get mean values for different asymmetricity types
            if sp_results['similarity_asymmetricity']['bray_curtis']:
                sim_mean = np.mean(sp_results['similarity_asymmetricity']['bray_curtis'])
            else:
                sim_mean = 0
                
            if sp_results['vector_asymmetricity']:
                vec_mean = np.mean(sp_results['vector_asymmetricity'])
            else:
                vec_mean = 0
                
            if sp_results['diversity_asymmetricity_type1']['richness']:
                div_mean = np.mean(sp_results['diversity_asymmetricity_type1']['richness'])
            else:
                div_mean = 0
            
            summary_data.append({
                'Species_Number': sp_num,
                'Condition': condition,
                'Similarity_Asymmetricity': sim_mean,
                'Vector_Asymmetricity': vec_mean,
                'Diversity_Asymmetricity': div_mean
            })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create grouped bar plot
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    asymmetricity_types = ['Similarity_Asymmetricity', 'Vector_Asymmetricity', 'Diversity_Asymmetricity']
    titles = ['Similarity Asymmetricity (Bray-Curtis)', 'Vector Asymmetricity', 'Diversity Asymmetricity (Type 1)']
    
    for i, (asym_type, title) in enumerate(zip(asymmetricity_types, titles)):
        ax = axes[i]
        
        # Pivot data for grouped bar plot
        pivot_df = summary_df.pivot(index='Species_Number', columns='Condition', values=asym_type)
        
        # Create bar plot
        pivot_df.plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e', '#2ca02c'], 
                     alpha=0.8, width=0.8)
        
        ax.set_title(title)
        ax.set_xlabel('Species Number')
        ax.set_ylabel('Mean Asymmetricity')
        ax.set_ylim(0, max(summary_df[asym_type]) * 1.1 if summary_df[asym_type].max() > 0 else 1)
        ax.legend(title='Condition')
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved species summary barplot: {save_path}")
    
    plt.close()  # Close to prevent display

# =============================================================================
# COMPREHENSIVE ANALYSIS FUNCTION WITH SPECIES SUPPORT
# =============================================================================

def run_complete_asymmetricity_analysis(offspring_list, parent1_list, parent2_list,
                                       nutrient_conditions, species_numbers,
                                       similarity_metrics=['bray_curtis', 'jensen_shannon', 'jaccard', 'cosine', 'euclidean'],
                                       diversity_threshold=1e-4,
                                       threshold=0,
                                       create_plots=True,
                                       save_plots=True,
                                       plot_dir='/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/AsymmetricityAnalysis/',
                                       perform_stats=True,
                                       plot_by_species=True):
    """
    Complete pipeline for asymmetricity analysis with species number support.
    
    Args:
        offspring_list: List of offspring communities
        parent1_list: List of parent1 communities  
        parent2_list: List of parent2 communities
        nutrient_conditions: List of nutrient conditions
        species_numbers: List of species numbers for each event
        similarity_metrics: Similarity metrics to analyze
        diversity_threshold: Threshold for counting species in diversity calculation (default 1e-4)
        threshold: Abundance threshold for similarity calculations
        create_plots: Whether to create plots
        save_plots: Whether to save plots
        plot_dir: Directory to save plots
        perform_stats: Whether to perform statistical tests
        plot_by_species: Whether to create species-specific plots
    
    Returns:
        Dictionary with complete analysis results
    """
    print("Starting comprehensive asymmetricity analysis...")
    
    # 1. Calculate asymmetricity for all events
    print("Calculating asymmetricity metrics...")
    results = analyze_multiple_coalescence_asymmetricity(
        offspring_list, parent1_list, parent2_list, nutrient_conditions,
        species_numbers, similarity_metrics, diversity_threshold, threshold
    )
    
    # Extract overall results for compatibility with existing functions
    overall_results = results if 'overall' not in results else results['overall']
    
    # 2. Generate summary statistics
    print("Generating summary statistics...")
    summary_table = generate_asymmetricity_summary_table(overall_results)
    
    # 3. Perform statistical tests
    stat_results = None
    if perform_stats:
        print("Performing statistical tests...")
        stat_results = perform_asymmetricity_statistical_tests(overall_results)
    
    # 4. Create plots
    if create_plots:
        print("Creating plots...")
        
        # Set up save paths if needed
        save_paths = {}
        if save_plots:
            import os
            os.makedirs(plot_dir, exist_ok=True)
            save_paths = {
                'similarity': f"{plot_dir}/similarity_asymmetricity.png",
                'vector': f"{plot_dir}/vector_asymmetricity.png", 
                'diversity_type1': f"{plot_dir}/diversity_asymmetricity_type1.png",
                'diversity_type2': f"{plot_dir}/diversity_asymmetricity_type2.png",
                'comprehensive': f"{plot_dir}/comprehensive_asymmetricity.png"
            }
        
        # Create individual plots for each similarity metric
        for metric in similarity_metrics:
            plot_similarity_asymmetricity(overall_results, [metric], 
                                        save_path_prefix=f"{plot_dir}/similarity")
        
        plot_vector_asymmetricity(overall_results, 
                                save_path=save_paths.get('vector'))
        
        plot_diversity_asymmetricity(overall_results, 'type1',
                                    save_path=save_paths.get('diversity_type1'))
        
        plot_diversity_asymmetricity(overall_results, 'type2',
                                    save_path=save_paths.get('diversity_type2'))
        
        plot_comprehensive_asymmetricity_comparison(overall_results, similarity_metrics,
                                                   save_path=save_paths.get('comprehensive'))
        
        # 5. Create species-specific plots
        if plot_by_species:
            print("Creating species-specific plots...")
            
            species_save_prefix = f"{plot_dir}/species_specific"
            plot_all_asymmetricity_by_species(results, target_species=[6, 12, 24], 
                                             save_path_prefix=species_save_prefix)
            
            # Create species summary barplot
            species_summary_path = f"{plot_dir}/species_summary_barplot.png"
            create_species_summary_barplot(results, target_species=[6, 12, 24], 
                                          save_path=species_summary_path)
    
    # 6. Compile final results
    final_results = {
        'asymmetricity_results': results,
        'summary_table': summary_table,
        'statistical_tests': stat_results,
        'parameters': {
            'similarity_metrics': similarity_metrics,
            'diversity_threshold': diversity_threshold,
            'threshold': threshold,
            'species_numbers': True,
            'n_events_per_condition': {
                condition: len(overall_results[condition]['vector_asymmetricity'])
                for condition in ['LN', 'MN', 'HN']
            }
        }
    }
    
    print("Asymmetricity analysis complete!")
    return final_results

# =============================================================================
# REAL DATA LOADING FUNCTIONS
# =============================================================================

def load_real_coalescence_data():
    """
    Load real experimental coalescence data using the existing common_setup infrastructure.
    
    Returns:
        Tuple of (offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers)
    """
    # Import existing data from common_setup
    from common_setup import Coalescence_data
    
    # Load processed sequences data directly (contains actual ASV abundance data)
    import pandas as pd
    Processed_sequences_synthetic_path ="../../Postprocessed/processed_Sequences_synthetic.xlsx"
    Processed_sequences_natural_path ="../../Postprocessed/processed_Sequences_natural.xlsx"
    
    sequences_synthetic = pd.read_excel(Processed_sequences_synthetic_path)
    sequences_natural = pd.read_excel(Processed_sequences_natural_path)
    processed_sequences = pd.concat([sequences_synthetic, sequences_natural])
    
    offspring_list = []
    parent1_list = []
    parent2_list = []
    nutrient_conditions = []
    species_numbers = []
    
    print("Loading real coalescence data using processed sequences...")
    print(f"Coalescence data shape: {Coalescence_data.shape}")
    print(f"Processed sequences shape: {processed_sequences.shape}")
    print(f"Processed sequences columns: {list(processed_sequences.columns[:10])}...")  # Show first 10 columns
    
    # Iterate through coalescence data and get abundance vectors from processed sequences
    processed_events = 0
    skipped_events = 0
    
    for _, row in Coalescence_data.iterrows():
            # Get medium and convert to our format
            medium = row['Medium']
            nutrient_mapping = {'L': 'LN', 'M': 'MN', 'H': 'HN'}
            nutrient_condition = nutrient_mapping.get(medium)
            
            
            # Get sample IDs
            mixture_sample_id = row['SampleIDX']
            parent1_sample_id = row['SampleIDX_Sub1']
            parent2_sample_id = row['SampleIDX_Sub2']
            
            # Find corresponding rows in processed sequences data (contains actual abundances)
            mixture_rows = processed_sequences[processed_sequences['SampleIDX'] == mixture_sample_id]
            parent1_rows = processed_sequences[processed_sequences['SampleIDX'] == parent1_sample_id]
            parent2_rows = processed_sequences[processed_sequences['SampleIDX'] == parent2_sample_id]
            
            # Skip if any data is missing
            if mixture_rows.empty or parent1_rows.empty or parent2_rows.empty:
                skipped_events += 1
                continue
                
            # Check if DataFrames have enough columns (SampleIDX + at least 1 species column)
            if (len(mixture_rows.columns) < 2 or 
                len(parent1_rows.columns) < 2 or 
                len(parent2_rows.columns) < 2):
                skipped_events += 1
                continue
            
            # Extract community vectors (columns 1 onwards, since column 0 is SampleIDX)
            mixture_vector = mixture_rows.iloc[0, 1:].values.astype(float)
            parent1_vector = parent1_rows.iloc[0, 1:].values.astype(float)
            parent2_vector = parent2_rows.iloc[0, 1:].values.astype(float)
            
            # Clean and normalize
            mixture_vector = np.nan_to_num(mixture_vector, 0)
            parent1_vector = np.nan_to_num(parent1_vector, 0)
            parent2_vector = np.nan_to_num(parent2_vector, 0)
            
            # Apply threshold and normalize as in the notebook
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
            
            # Count final observed species (for validation)
            n_observed_species = np.sum(mixture_vector > 0)
            
            # Get experimental design species pool number from CommunityIDX
            # This applies only to synthetic coalescence data (CommunityOrigin == 'S')
            experimental_species_pool = None
            if row['CommunityOrigin'] == 'S' and row['CoalescenceType'] == 'C':
                community_idx = row['CommunityIDX']
                # Apply mapping from common_setup.py:
                # species_pool_num == 6: communityIDX <= 14
                # species_pool_num == 12: communityIDX > 14 & <= 41  
                # species_pool_num == 24: communityIDX > 41 & <= 47
                if community_idx <= 14:
                    experimental_species_pool = 6
                elif community_idx <= 41:
                    experimental_species_pool = 12
                elif community_idx <= 47:
                    experimental_species_pool = 24
            
            # Include valid samples with minimum diversity threshold
            if (n_observed_species >= 3 and 
                np.sum(mixture_vector) > 0 and 
                np.sum(parent1_vector) > 0 and 
                np.sum(parent2_vector) > 0):
                
                offspring_list.append(mixture_vector)
                parent1_list.append(parent1_vector)
                parent2_list.append(parent2_vector)
                nutrient_conditions.append(nutrient_condition)
                # Use experimental species pool number if available
                species_numbers.append(experimental_species_pool if experimental_species_pool is not None else n_observed_species)
                processed_events += 1
            else:
                skipped_events += 1
    
    print(f"Successfully loaded {processed_events} coalescence events")
    print(f"Skipped {skipped_events} events due to missing/invalid data")
    
    if len(offspring_list) > 0:
        print(f"Nutrient distribution: LN={nutrient_conditions.count('LN')}, MN={nutrient_conditions.count('MN')}, HN={nutrient_conditions.count('HN')}")
        print(f"Species range: {min(species_numbers)} - {max(species_numbers)}")
    
    return offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers

# =============================================================================
# EXAMPLE USAGE AND TESTING (UPDATED FOR REAL DATA)
# =============================================================================

def test_asymmetricity_analysis():
    """
    Test function to demonstrate asymmetricity analysis with real data.
    """
    print("Testing asymmetricity analysis with real data...")
    
    # Load real coalescence data
    offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers = load_real_coalescence_data()
    
    if not offspring_list:
        print("No offspring data found. Make sure the data is loaded correctly.")
        return
    
    # All available similarity metrics
    all_similarity_metrics = ['bray_curtis', 'jensen_shannon', 'jaccard', 'cosine', 'euclidean']
    
    # Run complete analysis
    results = run_complete_asymmetricity_analysis(
        offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers,
        similarity_metrics=all_similarity_metrics,
        diversity_threshold=1e-4,
        create_plots=True,
        save_plots=True,
        perform_stats=True,
        plot_by_species=True
    )
    
    # Print summary
    print("\nAsymmetricity Analysis Summary:")
    print("=" * 50)
    
    conditions = ['LN', 'MN', 'HN']
    
    # Print species number distribution
    if 'by_species' in results['asymmetricity_results']:
        species_nums = sorted(results['asymmetricity_results']['by_species'].keys())
        print(f"\nSpecies numbers analyzed: {species_nums}")
        print(f"Total species range: {min(species_nums)} to {max(species_nums)}")
    
    # Get overall results for summary statistics
    overall_results = results['asymmetricity_results']
    if 'overall' in overall_results:
        overall_results = overall_results['overall']
    
    # Summary for each similarity metric
    print("\nSimilarity Asymmetricity:")
    for metric in all_similarity_metrics:
        print(f"\n{metric.upper()}:")
        for condition in conditions:
            values = overall_results[condition]['similarity_asymmetricity'][metric]
            print(f"  {condition}: Mean = {np.mean(values):.3f} ± {np.std(values):.3f}")
    
    print("\nVector Asymmetricity:")
    for condition in conditions:
        values = overall_results[condition]['vector_asymmetricity']
        print(f"  {condition}: Mean = {np.mean(values):.3f} ± {np.std(values):.3f}")
    
    print("\nDiversity Asymmetricity Type1 (Richness):")
    for condition in conditions:
        values = overall_results[condition]['diversity_asymmetricity_type1']['richness']
        print(f"  {condition}: Mean = {np.mean(values):.3f} ± {np.std(values):.3f}")
    
    # Statistical significance
    if results['statistical_tests']:
        print("\nStatistical Tests (p-values):")
        for metric in all_similarity_metrics:
            p_val = results['statistical_tests']['similarity'][metric]['p_value']
            print(f"  Similarity ({metric}): p = {p_val:.4f}")
        print(f"  Vector: p = {results['statistical_tests']['vector']['p_value']:.4f}")
        print(f"  Diversity Type1 (Richness): p = {results['statistical_tests']['diversity_type1']['richness']['p_value']:.4f}")
    
    return results

# =============================================================================
# RETENTION-BASED ASYMMETRICITY PLOTTING FUNCTIONS
# =============================================================================

def plot_retention_asymmetricity(results_dict, asymm_type='type1', 
                                figsize=(10, 6), save_path=None):
    """
    Plot retention-based asymmetricity across nutrient conditions.
    
    Args:
        results_dict: Results from analyze_multiple_coalescence_asymmetricity
        asymm_type: 'type1' (exclude overlaps) or 'type2' (include overlaps)
        figsize: Figure size tuple
        save_path: Path to save the plot
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    conditions = ['LN', 'MN', 'HN']
    plot_data = []
    
    for condition in conditions:
        values = results_dict[condition]['retention_asymmetricity'][asymm_type]['asymmetricity']
        p_values = results_dict[condition]['retention_asymmetricity'][asymm_type]['p_values']
        significant = results_dict[condition]['retention_asymmetricity'][asymm_type]['significant']
        
        for val, p_val, is_sig in zip(values, p_values, significant):
            plot_data.append({
                'Condition': condition, 
                'Asymmetricity': val,
                'p_value': p_val,
                'Significant': is_sig,
                'Significance': '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'
            })
    
    plot_df = pd.DataFrame(plot_data)
    
    # Create plot
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    # Box plot
    box_parts = ax.boxplot([plot_df[plot_df['Condition'] == cond]['Asymmetricity'].values 
                           for cond in conditions],
                          positions=range(len(conditions)), 
                          patch_artist=True, showfliers=False)
    
    # Color boxes
    colors = ['lightblue', 'lightgreen', 'lightcoral']
    for patch, color in zip(box_parts['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Add individual points with significance markers
    for i, condition in enumerate(conditions):
        cond_data = plot_df[plot_df['Condition'] == condition]
        x_pos = i + np.random.normal(0, 0.02, len(cond_data))  # Add jitter
        
        # Color points by significance
        sig_colors = ['red' if sig else 'gray' for sig in cond_data['Significant']]
        ax.scatter(x_pos, cond_data['Asymmetricity'], 
                  c=sig_colors, alpha=0.6, s=20, edgecolors='black', linewidth=0.5)
    
    ax.set_xticks(range(len(conditions)))
    ax.set_xticklabels(conditions)
    ax.set_ylabel('Retention Asymmetricity')
    
    title = f'Retention-Based Asymmetricity ({asymm_type.upper()})'
    if asymm_type == 'type1':
        title += '\n(Unique species only, excluding overlaps)'
    else:
        title += '\n(All species, including overlaps)'
    ax.set_title(title)
    
    # Add legend
    ax.text(0.02, 0.98, 'Red: p < 0.05 (significant)\nGray: p ≥ 0.05 (not significant)', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved retention asymmetricity {asymm_type} plot: {save_path}")
    
    plt.close()  # Close to prevent memory issues

def plot_retention_asymmetricity_comparison(results_dict, figsize=(12, 5), save_path=None):
    """
    Compare retention asymmetricity Type 1 vs Type 2 side by side.
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    conditions = ['LN', 'MN', 'HN']
    colors = ['lightblue', 'lightgreen', 'lightcoral']
    
    for idx, asymm_type in enumerate(['type1', 'type2']):
        ax = axes[idx]
        
        # Prepare data
        plot_data = []
        for condition in conditions:
            values = results_dict[condition]['retention_asymmetricity'][asymm_type]['asymmetricity']
            significant = results_dict[condition]['retention_asymmetricity'][asymm_type]['significant']
            
            for val, is_sig in zip(values, significant):
                plot_data.append({
                    'Condition': condition,
                    'Asymmetricity': val, 
                    'Significant': is_sig
                })
        
        plot_df = pd.DataFrame(plot_data)
        
        # Box plot
        box_parts = ax.boxplot([plot_df[plot_df['Condition'] == cond]['Asymmetricity'].values 
                               for cond in conditions],
                              positions=range(len(conditions)), 
                              patch_artist=True, showfliers=False)
        
        # Color boxes
        for patch, color in zip(box_parts['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add scatter points
        for i, condition in enumerate(conditions):
            cond_data = plot_df[plot_df['Condition'] == condition]
            x_pos = i + np.random.normal(0, 0.02, len(cond_data))
            sig_colors = ['red' if sig else 'gray' for sig in cond_data['Significant']]
            ax.scatter(x_pos, cond_data['Asymmetricity'], 
                      c=sig_colors, alpha=0.6, s=20, edgecolors='black', linewidth=0.5)
        
        ax.set_xticks(range(len(conditions)))
        ax.set_xticklabels(conditions)
        ax.set_ylabel('Retention Asymmetricity')
        
        title = f'Type {asymm_type[-1]}'
        if asymm_type == 'type1':
            title += ' (Unique Species)'
        else:
            title += ' (All Species)'
        ax.set_title(title)
        
        # Set same y-axis limits for comparison
        if idx == 0:
            y_max = max([max(results_dict[c]['retention_asymmetricity']['type1']['asymmetricity'] + 
                            results_dict[c]['retention_asymmetricity']['type2']['asymmetricity']) 
                        for c in conditions])
            y_lim = (0, y_max * 1.1)
        ax.set_ylim(y_lim)
    
    fig.suptitle('Retention-Based Asymmetricity Comparison', fontsize=14)
    
    # Add overall legend
    fig.text(0.5, 0.02, 'Red points: statistically significant (p < 0.05), Gray points: not significant', 
             ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight') 
        print(f"Saved retention asymmetricity comparison plot: {save_path}")
    
    plt.close()

def plot_retention_vs_diversity_asymmetricity(results_dict, condition='LN', save_path=None):
    """
    Compare retention-based vs diversity-based asymmetricity for a given condition.
    Shows how the new method fixes the diversity bias.
    """
    import matplotlib.pyplot as plt
    
    # Extract data
    retention_type1 = results_dict[condition]['retention_asymmetricity']['type1']['asymmetricity']
    retention_type2 = results_dict[condition]['retention_asymmetricity']['type2']['asymmetricity'] 
    diversity_type1 = results_dict[condition]['diversity_asymmetricity_type1']['richness']
    diversity_type2 = results_dict[condition]['diversity_asymmetricity_type2']['richness']
    species_nums = results_dict[condition]['species_numbers']
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Retention vs Diversity Type 1 
    ax1 = axes[0]
    scatter = ax1.scatter(diversity_type1, retention_type1, c=species_nums, 
                         cmap='viridis', alpha=0.7, s=50, edgecolors='black', linewidth=0.5)
    ax1.set_xlabel('Diversity Asymmetricity Type 1')
    ax1.set_ylabel('Retention Asymmetricity Type 1')
    ax1.set_title(f'Diversity vs Retention Asymmetricity (Type 1)\nCondition: {condition}')
    
    # Add colorbar
    cbar1 = plt.colorbar(scatter, ax=ax1)
    cbar1.set_label('Species Pool Size')
    
    # Plot 2: Retention vs Diversity Type 2
    ax2 = axes[1]
    scatter2 = ax2.scatter(diversity_type2, retention_type2, c=species_nums,
                          cmap='viridis', alpha=0.7, s=50, edgecolors='black', linewidth=0.5)
    ax2.set_xlabel('Diversity Asymmetricity Type 2')
    ax2.set_ylabel('Retention Asymmetricity Type 2')
    ax2.set_title(f'Diversity vs Retention Asymmetricity (Type 2)\nCondition: {condition}')
    
    # Add colorbar
    cbar2 = plt.colorbar(scatter2, ax=ax2)
    cbar2.set_label('Species Pool Size')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved retention vs diversity comparison plot: {save_path}")
    
    plt.close()

if __name__ == "__main__":
    # Run test analysis
    test_results = test_asymmetricity_analysis()
