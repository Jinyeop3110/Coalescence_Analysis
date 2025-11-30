#!/usr/bin/env python3
"""
Modified retention asymmetricity analysis comparing DISTRIBUTIONS between experimental and null models
instead of event-wise significance testing.
"""

import numpy as np
from scipy import stats
import sys
import os

sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

def calculate_retention_asymmetricity_simple(parent1_vector, parent2_vector, mixed_vector, 
                                           threshold=1e-4, version=1):
    """
    Calculate retention asymmetricity WITHOUT permutation testing.
    Just returns the asymmetricity value for distribution comparison.
    """
    # Identify present species
    parent1_present = parent1_vector > threshold
    parent2_present = parent2_vector > threshold
    mixed_present = mixed_vector > threshold
    
    # Calculate based on version
    if version == 1:  # Unique species only
        parent1_unique = parent1_present & ~parent2_present
        parent2_unique = parent2_present & ~parent1_present
        
        n_parent1_total = np.sum(parent1_unique)
        n_parent2_total = np.sum(parent2_unique)
        
        if n_parent1_total == 0 or n_parent2_total == 0:
            return np.nan  # Skip events with no unique species
            
        parent1_retained = np.sum(parent1_unique & mixed_present)
        parent2_retained = np.sum(parent2_unique & mixed_present)
        
    else:  # All species
        n_parent1_total = np.sum(parent1_present)
        n_parent2_total = np.sum(parent2_present)
        
        if n_parent1_total == 0 or n_parent2_total == 0:
            return np.nan
            
        parent1_retained = np.sum(parent1_present & mixed_present)
        parent2_retained = np.sum(parent2_present & mixed_present)
    
    # Calculate retention rates
    retention_1 = parent1_retained / n_parent1_total
    retention_2 = parent2_retained / n_parent2_total
    
    # Return asymmetricity
    return abs(retention_1 - retention_2)

def compare_distributions(exp_values, null_values, test_name="Experimental vs Null"):
    """
    Compare two distributions using multiple statistical tests.
    
    Returns:
        dict: Statistical test results including p-values and effect sizes
    """
    # Remove NaN values
    exp_values = [v for v in exp_values if not np.isnan(v)]
    null_values = [v for v in null_values if not np.isnan(v)]
    
    if len(exp_values) < 3 or len(null_values) < 3:
        return {
            'error': 'Insufficient data for comparison',
            'n_exp': len(exp_values),
            'n_null': len(null_values)
        }
    
    results = {
        'n_exp': len(exp_values),
        'n_null': len(null_values),
        'exp_mean': np.mean(exp_values),
        'exp_std': np.std(exp_values),
        'null_mean': np.mean(null_values),
        'null_std': np.std(null_values),
    }
    
    # 1. Mann-Whitney U test (non-parametric)
    u_stat, u_pval = stats.mannwhitneyu(exp_values, null_values, alternative='two-sided')
    results['mann_whitney_u'] = {
        'statistic': u_stat,
        'p_value': u_pval,
        'significant': u_pval < 0.05
    }
    
    # 2. Kolmogorov-Smirnov test (tests if distributions are different)
    ks_stat, ks_pval = stats.ks_2samp(exp_values, null_values)
    results['kolmogorov_smirnov'] = {
        'statistic': ks_stat,
        'p_value': ks_pval,
        'significant': ks_pval < 0.05
    }
    
    # 3. Effect size (Cohen's d)
    pooled_std = np.sqrt((np.std(exp_values)**2 + np.std(null_values)**2) / 2)
    if pooled_std > 0:
        cohens_d = (np.mean(exp_values) - np.mean(null_values)) / pooled_std
    else:
        cohens_d = 0
    
    results['effect_size'] = {
        'cohens_d': cohens_d,
        'interpretation': 'Small' if abs(cohens_d) < 0.5 else 'Medium' if abs(cohens_d) < 0.8 else 'Large'
    }
    
    # 4. Permutation test for mean difference
    observed_diff = np.mean(exp_values) - np.mean(null_values)
    all_values = exp_values + null_values
    n_permutations = 10000
    perm_diffs = []
    
    np.random.seed(42)
    for _ in range(n_permutations):
        np.random.shuffle(all_values)
        perm_exp = all_values[:len(exp_values)]
        perm_null = all_values[len(exp_values):]
        perm_diffs.append(np.mean(perm_exp) - np.mean(perm_null))
    
    perm_pval = sum(1 for d in perm_diffs if abs(d) >= abs(observed_diff)) / n_permutations
    
    results['permutation_test'] = {
        'observed_difference': observed_diff,
        'p_value': perm_pval,
        'significant': perm_pval < 0.05
    }
    
    return results

def analyze_retention_distributions_with_null_models(offspring_list, parent1_list, parent2_list,
                                                   nutrient_conditions, species_numbers=None):
    """
    Analyze retention asymmetricity by comparing DISTRIBUTIONS between experimental and null models.
    """
    print("\n=== RETENTION ASYMMETRICITY DISTRIBUTION ANALYSIS ===")
    print("Comparing experimental vs null model DISTRIBUTIONS (not individual events)")
    
    conditions = ['LN', 'MN', 'HN']
    species_pools = [6, 12, 24] if species_numbers else [None]
    
    # Calculate experimental asymmetricity values
    print("\nCalculating experimental asymmetricity distributions...")
    exp_results = {}
    
    for ret_type in [1, 2]:
        exp_results[f'type{ret_type}'] = {}
        
        for condition in conditions:
            exp_results[f'type{ret_type}'][condition] = {}
            
            # Get indices for this condition
            condition_indices = [i for i, c in enumerate(nutrient_conditions) if c == condition]
            
            if species_numbers:
                # Break down by species pool
                for sp_num in species_pools:
                    sp_indices = [i for i in condition_indices if species_numbers[i] == sp_num]
                    
                    # Calculate asymmetricity for each event
                    asymm_values = []
                    for idx in sp_indices:
                        asymm = calculate_retention_asymmetricity_simple(
                            parent1_list[idx], parent2_list[idx], offspring_list[idx], 
                            version=ret_type
                        )
                        if not np.isnan(asymm):
                            asymm_values.append(asymm)
                    
                    exp_results[f'type{ret_type}'][condition][f'pool_{sp_num}'] = asymm_values
            else:
                # All data for this condition
                asymm_values = []
                for idx in condition_indices:
                    asymm = calculate_retention_asymmetricity_simple(
                        parent1_list[idx], parent2_list[idx], offspring_list[idx],
                        version=ret_type
                    )
                    if not np.isnan(asymm):
                        asymm_values.append(asymm)
                
                exp_results[f'type{ret_type}'][condition]['all'] = asymm_values
    
    # Generate null models and calculate their distributions
    print("\nGenerating null model distributions...")
    
    # Import null model generation functions
    from AsymmetricityNullModelAnalysis import (
        generate_neutral_mixing_null,
        generate_random_selection_null_v1,
        generate_random_selection_null_v2
    )
    
    null_results = {}
    
    # Generate each type of null model
    null_models = {
        'neutral_mixing': generate_neutral_mixing_null(
            parent1_list, parent2_list, nutrient_conditions, species_numbers, len(offspring_list)
        ),
        'random_selection_v1': generate_random_selection_null_v1(
            parent1_list, parent2_list, nutrient_conditions, species_numbers, len(offspring_list)
        ),
        'random_selection_v2': generate_random_selection_null_v2(
            parent1_list, parent2_list, nutrient_conditions, species_numbers, len(offspring_list)
        )
    }
    
    # Calculate null model distributions
    for null_name, null_data in null_models.items():
        print(f"  Analyzing {null_name} null model...")
        
        if len(null_data) == 5:
            null_offspring, null_parent1, null_parent2, null_conditions, null_species = null_data
        else:
            null_offspring, null_parent1, null_parent2 = null_data
            null_conditions = nutrient_conditions[:len(null_offspring)]
            null_species = species_numbers[:len(null_offspring)] if species_numbers else None
        
        null_results[null_name] = {}
        
        for ret_type in [1, 2]:
            null_results[null_name][f'type{ret_type}'] = {}
            
            for condition in conditions:
                null_results[null_name][f'type{ret_type}'][condition] = {}
                
                # Get indices for this condition
                condition_indices = [i for i, c in enumerate(null_conditions) if c == condition]
                
                if null_species:
                    # Break down by species pool
                    for sp_num in species_pools:
                        sp_indices = [i for i in condition_indices if null_species[i] == sp_num]
                        
                        # Calculate asymmetricity for each null event
                        asymm_values = []
                        for idx in sp_indices:
                            asymm = calculate_retention_asymmetricity_simple(
                                null_parent1[idx], null_parent2[idx], null_offspring[idx],
                                version=ret_type
                            )
                            if not np.isnan(asymm):
                                asymm_values.append(asymm)
                        
                        null_results[null_name][f'type{ret_type}'][condition][f'pool_{sp_num}'] = asymm_values
                else:
                    # All data for this condition
                    asymm_values = []
                    for idx in condition_indices:
                        asymm = calculate_retention_asymmetricity_simple(
                            null_parent1[idx], null_parent2[idx], null_offspring[idx],
                            version=ret_type
                        )
                        if not np.isnan(asymm):
                            asymm_values.append(asymm)
                    
                    null_results[null_name][f'type{ret_type}'][condition]['all'] = asymm_values
    
    # Compare distributions
    print("\n=== STATISTICAL COMPARISON OF DISTRIBUTIONS ===")
    
    comparison_results = {}
    
    for ret_type in [1, 2]:
        print(f"\n--- Retention Type {ret_type} ---")
        comparison_results[f'type{ret_type}'] = {}
        
        for condition in conditions:
            print(f"\n{condition} Condition:")
            comparison_results[f'type{ret_type}'][condition] = {}
            
            # Determine keys to compare
            keys = exp_results[f'type{ret_type}'][condition].keys()
            
            for key in keys:
                exp_values = exp_results[f'type{ret_type}'][condition][key]
                
                if len(exp_values) > 0:
                    print(f"\n  {key}:")
                    print(f"    Experimental: n={len(exp_values)}, mean={np.mean(exp_values):.3f}, std={np.std(exp_values):.3f}")
                    
                    comparison_results[f'type{ret_type}'][condition][key] = {}
                    
                    # Compare with each null model
                    for null_name in null_results:
                        null_values = null_results[null_name][f'type{ret_type}'][condition].get(key, [])
                        
                        if len(null_values) > 0:
                            print(f"    {null_name}: n={len(null_values)}, mean={np.mean(null_values):.3f}, std={np.std(null_values):.3f}")
                            
                            # Statistical comparison
                            comp = compare_distributions(exp_values, null_values, 
                                                       f"Exp vs {null_name}")
                            
                            comparison_results[f'type{ret_type}'][condition][key][null_name] = comp
                            
                            # Print key results
                            print(f"      Mann-Whitney U p-value: {comp['mann_whitney_u']['p_value']:.4f} {'*' if comp['mann_whitney_u']['significant'] else ''}")
                            print(f"      Kolmogorov-Smirnov p-value: {comp['kolmogorov_smirnov']['p_value']:.4f} {'*' if comp['kolmogorov_smirnov']['significant'] else ''}")
                            print(f"      Effect size (Cohen's d): {comp['effect_size']['cohens_d']:.3f} ({comp['effect_size']['interpretation']})")
    
    return {
        'experimental': exp_results,
        'null_models': null_results,
        'comparisons': comparison_results
    }

def plot_distribution_comparisons(results, save_dir="Figure/AsymmetricityNullModelAnalysis"):
    """
    Create plots comparing experimental vs null model distributions with p-values.
    """
    import matplotlib.pyplot as plt
    import os
    
    os.makedirs(save_dir, exist_ok=True)
    
    conditions = ['LN', 'MN', 'HN']
    colors = {
        'experimental': 'darkblue',
        'neutral_mixing': 'orange',
        'random_selection_v1': 'purple', 
        'random_selection_v2': 'brown'
    }
    
    # Create plots for each retention type
    for ret_type in [1, 2]:
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle(f'Retention Asymmetricity Type {ret_type} - Distribution Comparison\n'
                    f'Experimental vs Null Models with Statistical Tests', fontsize=16)
        
        for i, condition in enumerate(conditions):
            ax = axes[i]
            
            # Get all data for this condition (combine species pools if they exist)
            all_exp = []
            for key in results['experimental'][f'type{ret_type}'][condition]:
                all_exp.extend(results['experimental'][f'type{ret_type}'][condition][key])
            
            # Plot experimental distribution
            if all_exp:
                ax.hist(all_exp, bins=20, alpha=0.5, label=f'Experimental (n={len(all_exp)})', 
                       color=colors['experimental'], density=True)
            
            # Plot null model distributions
            for null_name in results['null_models']:
                all_null = []
                for key in results['null_models'][null_name][f'type{ret_type}'][condition]:
                    all_null.extend(results['null_models'][null_name][f'type{ret_type}'][condition][key])
                
                if all_null:
                    ax.hist(all_null, bins=20, alpha=0.5, 
                           label=f'{null_name.replace("_", " ").title()} (n={len(all_null)})',
                           color=colors[null_name], density=True)
            
            # Add statistical test results as text
            y_pos = 0.95
            for null_name in ['neutral_mixing', 'random_selection_v1', 'random_selection_v2']:
                if null_name in results['comparisons'][f'type{ret_type}'][condition].get('all', {}):
                    comp = results['comparisons'][f'type{ret_type}'][condition]['all'][null_name]
                    
                    mw_p = comp['mann_whitney_u']['p_value']
                    ks_p = comp['kolmogorov_smirnov']['p_value']
                    
                    text = f"vs {null_name.replace('_', ' ')}: MW p={mw_p:.3f}"
                    if mw_p < 0.05:
                        text += " *"
                    
                    ax.text(0.98, y_pos, text, transform=ax.transAxes, 
                           fontsize=10, ha='right', va='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                    y_pos -= 0.08
            
            ax.set_title(f'{condition} Condition')
            ax.set_xlabel('Retention Asymmetricity')
            ax.set_ylabel('Density')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{save_dir}/retention_type{ret_type}_distribution_comparison.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    print(f"\nDistribution comparison plots saved to {save_dir}/")

if __name__ == "__main__":
    print("Distribution-based retention asymmetricity analysis")
    print("This compares DISTRIBUTIONS, not individual events")