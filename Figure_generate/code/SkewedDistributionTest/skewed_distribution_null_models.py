"""
SkewedDistributionTest - Null Models for Testing Skewness Effects on Asymmetricity

This module tests whether observed high asymmetricity in coalescence outcomes
is simply due to skewed relative abundance distributions in parental communities.

Two null models are implemented:

1. Abundance-Weighted Random Selection (Approach 2):
   - Species survival probability is proportional to their abundance in the combined pool
   - Tests: If experimental asymmetricity ~ null -> skewness explains the pattern

2. Shuffled Abundance Null Model (Approach 5):
   - Keep species identities but shuffle abundances within each parent
   - Tests: If shuffling destroys asymmetricity -> specific abundance patterns matter

Author: Gore Lab Coalescence Analysis
Date: November 2025
"""

import numpy as np
import pandas as pd
from scipy import stats
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    Coalescence_data,
    Processed_sequences_synthetic,
    Processed_sequences_natural
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def normalize_vector(v):
    """Normalize abundance vector to sum to 1."""
    v = np.array(v, dtype=float)
    v = np.nan_to_num(v, 0)
    v = np.clip(v, 0, None)  # Ensure non-negative
    total = np.sum(v)
    if total > 0:
        return v / total
    return v


def calculate_gini_coefficient(abundances):
    """
    Calculate Gini coefficient as a measure of abundance inequality/skewness.

    Gini = 0: Perfect equality (all species have same abundance)
    Gini = 1: Perfect inequality (one species has all abundance)
    """
    abundances = np.array(abundances, dtype=float)
    abundances = abundances[abundances > 0]  # Only consider present species

    if len(abundances) == 0:
        return 0

    abundances = np.sort(abundances)
    n = len(abundances)
    cumsum = np.cumsum(abundances)

    gini = (2 * np.sum((np.arange(1, n + 1) * abundances))) / (n * np.sum(abundances)) - (n + 1) / n
    return max(0, min(1, gini))


def calculate_evenness(abundances, threshold=1e-4):
    """
    Calculate Pielou's evenness index.

    J = H / H_max where H is Shannon entropy

    Returns value in [0, 1]:
    - 1 = perfectly even distribution
    - 0 = highly skewed (one dominant species)
    """
    abundances = np.array(abundances, dtype=float)
    abundances = abundances[abundances > threshold]

    if len(abundances) <= 1:
        return 1.0  # Single species is "perfectly even" by definition

    # Shannon entropy
    p = abundances / np.sum(abundances)
    H = -np.sum(p * np.log(p + 1e-10))

    # Maximum possible entropy
    H_max = np.log(len(abundances))

    if H_max == 0:
        return 1.0

    return H / H_max


def calculate_vector_asymmetricity(parent1, parent2, offspring, threshold=1e-4):
    """
    Calculate vector-based asymmetricity using the standard decomposition.

    Returns:
        asymmetricity: Value in [0, 1] where 0 = symmetric, 1 = one parent dominates
        coefficients: (u, v, k) from vector decomposition
    """
    # Normalize vectors
    p1 = normalize_vector(parent1)
    p2 = normalize_vector(parent2)
    off = normalize_vector(offspring)

    # Apply threshold
    p1 = p1 * (p1 > threshold)
    p2 = p2 * (p2 > threshold)
    off = off * (off > threshold)

    try:
        u, v, k = metric_VectorDecomposition_onlyPositive(p1, p2, off)
        x, y = calculate_assymetricity(u, v, k)
        return y, (u, v, k)
    except Exception as e:
        return np.nan, (np.nan, np.nan, np.nan)


# =============================================================================
# NULL MODEL 1: ABUNDANCE-WEIGHTED RANDOM SELECTION
# =============================================================================

def generate_abundance_weighted_null(parent1, parent2, n_species_retain=None,
                                    retention_rate=0.5, threshold=1e-4):
    """
    Generate null offspring where species survival probability is proportional
    to their abundance in the combined parental pool.

    Hypothesis: High-abundance species are more likely to survive regardless
    of which parent they came from.

    Args:
        parent1, parent2: Parental abundance vectors
        n_species_retain: Number of species to retain (if None, use retention_rate)
        retention_rate: Fraction of combined species pool to retain
        threshold: Minimum abundance to consider species present

    Returns:
        null_offspring: Generated null offspring abundance vector
    """
    p1 = normalize_vector(parent1)
    p2 = normalize_vector(parent2)

    # Combined species pool with abundances from both parents
    # Use average abundance as the "combined" abundance
    combined = (p1 + p2) / 2
    combined = combined * (combined > threshold)

    # Species present in combined pool
    present_species = np.where(combined > threshold)[0]

    if len(present_species) == 0:
        return np.zeros_like(p1)

    # Determine number of species to retain
    if n_species_retain is None:
        n_species_retain = max(1, int(len(present_species) * retention_rate))
    n_species_retain = min(n_species_retain, len(present_species))

    # Selection probability proportional to abundance
    selection_probs = combined[present_species]
    selection_probs = selection_probs / np.sum(selection_probs)

    # Select species based on abundance-weighted probabilities
    selected_indices = np.random.choice(
        present_species,
        size=n_species_retain,
        replace=False,
        p=selection_probs
    )

    # Generate offspring abundances for selected species
    # Use exponential distribution to create realistic abundance structure
    null_offspring = np.zeros_like(p1)
    null_offspring[selected_indices] = np.random.exponential(1, n_species_retain)
    null_offspring = normalize_vector(null_offspring)

    return null_offspring


def generate_abundance_weighted_null_batch(parent1_list, parent2_list,
                                          n_permutations=1000,
                                          retention_rate=0.5,
                                          threshold=1e-4):
    """
    Generate multiple null offspring using abundance-weighted selection.

    Args:
        parent1_list, parent2_list: Lists of parental abundance vectors
        n_permutations: Number of null offspring to generate
        retention_rate: Fraction of species to retain
        threshold: Minimum abundance threshold

    Returns:
        null_offspring_list: List of null offspring vectors
        null_parent1_list: Corresponding parent1 vectors
        null_parent2_list: Corresponding parent2 vectors
    """
    null_offspring_list = []
    null_parent1_list = []
    null_parent2_list = []

    n_events = len(parent1_list)

    for _ in range(n_permutations):
        # Randomly select a parent pair
        idx = np.random.randint(0, n_events)
        p1 = parent1_list[idx]
        p2 = parent2_list[idx]

        # Generate null offspring
        null_off = generate_abundance_weighted_null(
            p1, p2,
            retention_rate=retention_rate,
            threshold=threshold
        )

        null_offspring_list.append(null_off)
        null_parent1_list.append(p1)
        null_parent2_list.append(p2)

    return null_offspring_list, null_parent1_list, null_parent2_list


# =============================================================================
# NULL MODEL 2: SHUFFLED ABUNDANCE NULL MODEL
# =============================================================================

def generate_shuffled_abundance_null(parent1, parent2, offspring, threshold=1e-4):
    """
    Generate null offspring by shuffling abundances within each parent community,
    then applying neutral mixing.

    Hypothesis: If specific abundance patterns (who is dominant) matter for
    asymmetricity, shuffling should destroy the pattern.

    Args:
        parent1, parent2: Parental abundance vectors
        offspring: Real offspring (used to determine mixing coefficient)
        threshold: Minimum abundance threshold

    Returns:
        null_offspring: Generated null offspring with shuffled parent abundances
    """
    p1 = normalize_vector(parent1)
    p2 = normalize_vector(parent2)
    off = normalize_vector(offspring)

    # Get present species in each parent
    p1_present = p1 > threshold
    p2_present = p2 > threshold

    # Shuffle abundances among present species within each parent
    p1_shuffled = np.zeros_like(p1)
    p2_shuffled = np.zeros_like(p2)

    p1_present_idx = np.where(p1_present)[0]
    p2_present_idx = np.where(p2_present)[0]

    if len(p1_present_idx) > 0:
        shuffled_abundances_1 = p1[p1_present_idx].copy()
        np.random.shuffle(shuffled_abundances_1)
        p1_shuffled[p1_present_idx] = shuffled_abundances_1
        p1_shuffled = normalize_vector(p1_shuffled)

    if len(p2_present_idx) > 0:
        shuffled_abundances_2 = p2[p2_present_idx].copy()
        np.random.shuffle(shuffled_abundances_2)
        p2_shuffled[p2_present_idx] = shuffled_abundances_2
        p2_shuffled = normalize_vector(p2_shuffled)

    # Use the same mixing coefficient as inferred from real data
    # or use random mixing if preferred
    alpha = np.random.uniform(0, 1)

    # Generate null offspring via neutral mixing of shuffled parents
    null_offspring = alpha * p1_shuffled + (1 - alpha) * p2_shuffled
    null_offspring = normalize_vector(null_offspring)

    return null_offspring, p1_shuffled, p2_shuffled


def generate_shuffled_abundance_null_batch(parent1_list, parent2_list, offspring_list,
                                          n_permutations=1000,
                                          threshold=1e-4):
    """
    Generate multiple null offspring using shuffled abundance approach.

    Args:
        parent1_list, parent2_list: Lists of parental abundance vectors
        offspring_list: List of real offspring vectors
        n_permutations: Number of null offspring to generate
        threshold: Minimum abundance threshold

    Returns:
        null_offspring_list: List of null offspring vectors
        shuffled_parent1_list: Shuffled parent1 vectors
        shuffled_parent2_list: Shuffled parent2 vectors
    """
    null_offspring_list = []
    shuffled_parent1_list = []
    shuffled_parent2_list = []

    n_events = len(parent1_list)

    for _ in range(n_permutations):
        # Randomly select an event
        idx = np.random.randint(0, n_events)
        p1 = parent1_list[idx]
        p2 = parent2_list[idx]
        off = offspring_list[idx]

        # Generate null offspring with shuffled parent abundances
        null_off, p1_shuf, p2_shuf = generate_shuffled_abundance_null(
            p1, p2, off, threshold=threshold
        )

        null_offspring_list.append(null_off)
        shuffled_parent1_list.append(p1_shuf)
        shuffled_parent2_list.append(p2_shuf)

    return null_offspring_list, shuffled_parent1_list, shuffled_parent2_list


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def calculate_asymmetricity_distribution(offspring_list, parent1_list, parent2_list,
                                        threshold=1e-4):
    """
    Calculate vector asymmetricity for a list of coalescence events.

    Returns:
        asymmetricities: Array of asymmetricity values
        skewness_metrics: Dictionary with Gini and evenness for each parent
    """
    asymmetricities = []
    gini_p1_list = []
    gini_p2_list = []
    evenness_p1_list = []
    evenness_p2_list = []
    gini_diff_list = []

    for off, p1, p2 in zip(offspring_list, parent1_list, parent2_list):
        asym, _ = calculate_vector_asymmetricity(p1, p2, off, threshold)
        asymmetricities.append(asym)

        # Calculate skewness metrics for parents
        gini_p1 = calculate_gini_coefficient(p1)
        gini_p2 = calculate_gini_coefficient(p2)
        evenness_p1 = calculate_evenness(p1, threshold)
        evenness_p2 = calculate_evenness(p2, threshold)

        gini_p1_list.append(gini_p1)
        gini_p2_list.append(gini_p2)
        evenness_p1_list.append(evenness_p1)
        evenness_p2_list.append(evenness_p2)
        gini_diff_list.append(abs(gini_p1 - gini_p2))

    skewness_metrics = {
        'gini_p1': np.array(gini_p1_list),
        'gini_p2': np.array(gini_p2_list),
        'evenness_p1': np.array(evenness_p1_list),
        'evenness_p2': np.array(evenness_p2_list),
        'gini_difference': np.array(gini_diff_list),
        'mean_gini': (np.array(gini_p1_list) + np.array(gini_p2_list)) / 2
    }

    return np.array(asymmetricities), skewness_metrics


def compare_distributions(exp_values, null_values, test_name="Experimental vs Null"):
    """
    Statistical comparison of experimental vs null model distributions.

    Returns:
        dict: Statistical test results including p-values and effect sizes
    """
    # Remove NaN values
    exp_values = np.array([v for v in exp_values if not np.isnan(v)])
    null_values = np.array([v for v in null_values if not np.isnan(v)])

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
        'exp_median': np.median(exp_values),
        'null_mean': np.mean(null_values),
        'null_std': np.std(null_values),
        'null_median': np.median(null_values),
    }

    # 1. Mann-Whitney U test (non-parametric)
    u_stat, u_pval = stats.mannwhitneyu(exp_values, null_values, alternative='two-sided')
    results['mann_whitney_u'] = {
        'statistic': u_stat,
        'p_value': u_pval,
        'significant': u_pval < 0.05
    }

    # 2. Kolmogorov-Smirnov test
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

    return results


def analyze_skewness_asymmetricity_correlation(asymmetricities, skewness_metrics):
    """
    Analyze correlation between skewness measures and asymmetricity.

    Tests whether parental abundance inequality predicts offspring asymmetricity.
    """
    results = {}

    # Remove NaN values
    valid_idx = ~np.isnan(asymmetricities)
    asymm = asymmetricities[valid_idx]

    for metric_name, metric_values in skewness_metrics.items():
        metric_vals = metric_values[valid_idx]

        # Pearson correlation
        if len(asymm) > 3 and len(metric_vals) > 3:
            r, p = stats.pearsonr(asymm, metric_vals)
            spearman_r, spearman_p = stats.spearmanr(asymm, metric_vals)

            results[metric_name] = {
                'pearson_r': r,
                'pearson_p': p,
                'spearman_r': spearman_r,
                'spearman_p': spearman_p,
                'significant': p < 0.05
            }

    return results


# =============================================================================
# DATA LOADING
# =============================================================================

def load_coalescence_data(data_type='synthetic'):
    """
    Load coalescence data from processed sequences.

    Args:
        data_type: 'synthetic', 'natural', or 'both'

    Returns:
        offspring_list, parent1_list, parent2_list, metadata
    """
    offspring_list = []
    parent1_list = []
    parent2_list = []
    nutrient_conditions = []
    species_numbers = []

    # Select appropriate data sources
    if data_type == 'synthetic':
        processed_sequences = Processed_sequences_synthetic
        coal_filter = lambda row: row['CommunityOrigin'] == 'S'
    elif data_type == 'natural':
        processed_sequences = Processed_sequences_natural
        coal_filter = lambda row: row['CommunityOrigin'] == 'N'
    else:
        processed_sequences = pd.concat([Processed_sequences_synthetic, Processed_sequences_natural])
        coal_filter = lambda row: True

    threshold = 1e-3

    for idx, row in Coalescence_data.iterrows():
        try:
            if row['CoalescenceType'] != 'C':
                continue
            if not coal_filter(row):
                continue

            # Get medium
            medium = row['Medium']
            nutrient_mapping = {'L': 'LN', 'M': 'MN', 'H': 'HN'}
            nutrient_condition = nutrient_mapping.get(medium)

            if nutrient_condition is None:
                continue

            # Get sample IDs
            mixture_sample_id = row['SampleIDX']
            parent1_sample_id = row['SampleIDX_Sub1']
            parent2_sample_id = row['SampleIDX_Sub2']

            # Find corresponding rows in processed sequences
            mixture_rows = processed_sequences[processed_sequences['SampleIDX'] == mixture_sample_id]
            parent1_rows = processed_sequences[processed_sequences['SampleIDX'] == parent1_sample_id]
            parent2_rows = processed_sequences[processed_sequences['SampleIDX'] == parent2_sample_id]

            if mixture_rows.empty or parent1_rows.empty or parent2_rows.empty:
                continue

            # Extract vectors
            mixture_vector = mixture_rows.iloc[0, 1:].values.astype(float)
            parent1_vector = parent1_rows.iloc[0, 1:].values.astype(float)
            parent2_vector = parent2_rows.iloc[0, 1:].values.astype(float)

            # Clean and normalize
            mixture_vector = np.nan_to_num(mixture_vector, 0)
            parent1_vector = np.nan_to_num(parent1_vector, 0)
            parent2_vector = np.nan_to_num(parent2_vector, 0)

            # Apply threshold
            mixture_vector = mixture_vector * (mixture_vector > threshold)
            parent1_vector = parent1_vector * (parent1_vector > threshold)
            parent2_vector = parent2_vector * (parent2_vector > threshold)

            # Normalize
            mixture_vector = normalize_vector(mixture_vector)
            parent1_vector = normalize_vector(parent1_vector)
            parent2_vector = normalize_vector(parent2_vector)

            # Count observed species
            n_observed_species = np.sum(mixture_vector > 0)

            # Get species pool size
            community_idx = row['CommunityIDX']
            if row['CommunityOrigin'] == 'S':
                if community_idx <= 14:
                    experimental_species_pool = 6
                elif community_idx <= 41:
                    experimental_species_pool = 12
                elif community_idx <= 47:
                    experimental_species_pool = 24
                else:
                    continue
            else:
                experimental_species_pool = 0  # Natural communities

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

    metadata = {
        'nutrient_conditions': nutrient_conditions,
        'species_numbers': species_numbers,
        'n_events': len(offspring_list)
    }

    print(f"Loaded {len(offspring_list)} coalescence events")
    if len(offspring_list) > 0:
        print(f"Nutrient distribution: LN={nutrient_conditions.count('LN')}, "
              f"MN={nutrient_conditions.count('MN')}, HN={nutrient_conditions.count('HN')}")

    return offspring_list, parent1_list, parent2_list, metadata


if __name__ == "__main__":
    print("SkewedDistributionTest Null Models Module")
    print("=" * 50)
    print("\nThis module provides two null models:")
    print("1. Abundance-Weighted Random Selection")
    print("2. Shuffled Abundance Null Model")
    print("\nRun run_skewness_analysis.py for full analysis.")
