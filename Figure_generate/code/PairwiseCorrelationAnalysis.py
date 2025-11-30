#!/usr/bin/env python3
"""
Pairwise Correlation Analysis for Same-Origin vs Mixed-Origin Species

Tests whether species pairs from the same parent community show higher
presence/absence correlations across replicates compared to mixed-origin pairs.

Method:
1. For each species pair (i,j), calculate Pearson correlation of their
   presence/absence patterns across all replicates
2. Group pairs by origin: same-origin (A-A, B-B) vs mixed-origin (A-B)
3. Compare mean correlations between groups using statistical tests

Author: Gore Lab Coalescence Analysis Team
Date: November 2025
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any
from scipy import stats
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')


def determine_species_origins(parent1_list: List[np.ndarray],
                              parent2_list: List[np.ndarray],
                              threshold: float = 1e-4) -> np.ndarray:
    """
    Determine which parent each species originates from.

    Returns:
        Array where 0 = Parent A, 1 = Parent B
    """
    n_species = len(parent1_list[0])
    species_origins = np.zeros(n_species, dtype=int)

    for s in range(n_species):
        # Average abundance across replicates
        avg_p1 = np.mean([p1[s] for p1 in parent1_list])
        avg_p2 = np.mean([p2[s] for p2 in parent2_list])

        present_in_p1 = avg_p1 > threshold
        present_in_p2 = avg_p2 > threshold

        if present_in_p1 and not present_in_p2:
            species_origins[s] = 0  # Parent A
        elif present_in_p2 and not present_in_p1:
            species_origins[s] = 1  # Parent B
        elif present_in_p1 and present_in_p2:
            # Assign to parent with higher average abundance
            species_origins[s] = 0 if avg_p1 >= avg_p2 else 1
        else:
            species_origins[s] = 0  # Default to Parent A

    return species_origins


def calculate_pairwise_correlations(offspring_list: List[np.ndarray],
                                    species_origins: np.ndarray,
                                    threshold: float = 1e-4,
                                    min_variance_pairs: int = 3) -> Tuple[List[Dict], Dict]:
    """
    Calculate pairwise presence/absence correlations for all species pairs.

    Args:
        offspring_list: List of offspring abundance vectors
        species_origins: Origin labels (0 = A, 1 = B)
        threshold: Abundance threshold for presence
        min_variance_pairs: Minimum number of replicates where at least one species
                           in the pair varies (not always present or always absent)

    Returns:
        pair_data: List of dictionaries with correlation info for each pair
        summary: Summary statistics
    """
    n_replicates = len(offspring_list)
    n_species = len(offspring_list[0])

    # Create presence/absence matrix: (n_replicates x n_species)
    presence_matrix = np.zeros((n_replicates, n_species))
    for r, offspring in enumerate(offspring_list):
        presence_matrix[r, :] = (offspring > threshold).astype(int)

    # Calculate correlations for all pairs
    pair_data = []

    for i, j in combinations(range(n_species), 2):
        # Get presence patterns for species i and j
        presence_i = presence_matrix[:, i]
        presence_j = presence_matrix[:, j]

        # Check if there's sufficient variation
        # Skip pairs where both species are always present or always absent
        if np.std(presence_i) < 1e-10 or np.std(presence_j) < 1e-10:
            continue

        # Count replicates where at least one species varies
        varies = (presence_i != presence_i[0]) | (presence_j != presence_j[0])
        if np.sum(varies) < min_variance_pairs:
            continue

        # Calculate Pearson correlation
        corr, p_value = stats.pearsonr(presence_i, presence_j)

        # Determine pair type
        origin_i = species_origins[i]
        origin_j = species_origins[j]

        if origin_i == origin_j:
            pair_type = 'same_origin'
            if origin_i == 0:
                pair_subtype = 'A-A'
            else:
                pair_subtype = 'B-B'
        else:
            pair_type = 'mixed_origin'
            pair_subtype = 'A-B'

        # Calculate concordance metrics
        both_present = np.sum((presence_i == 1) & (presence_j == 1))
        both_absent = np.sum((presence_i == 0) & (presence_j == 0))
        concordant = both_present + both_absent
        discordant = n_replicates - concordant

        pair_data.append({
            'species_i': i,
            'species_j': j,
            'origin_i': origin_i,
            'origin_j': origin_j,
            'pair_type': pair_type,
            'pair_subtype': pair_subtype,
            'correlation': corr,
            'p_value': p_value,
            'n_replicates': n_replicates,
            'both_present': both_present,
            'both_absent': both_absent,
            'concordant': concordant,
            'discordant': discordant,
            'concordance_rate': concordant / n_replicates
        })

    # Calculate summary statistics
    same_origin_corrs = [p['correlation'] for p in pair_data if p['pair_type'] == 'same_origin']
    mixed_origin_corrs = [p['correlation'] for p in pair_data if p['pair_type'] == 'mixed_origin']
    AA_corrs = [p['correlation'] for p in pair_data if p['pair_subtype'] == 'A-A']
    BB_corrs = [p['correlation'] for p in pair_data if p['pair_subtype'] == 'B-B']
    AB_corrs = [p['correlation'] for p in pair_data if p['pair_subtype'] == 'A-B']

    summary = {
        'n_pairs_total': len(pair_data),
        'n_pairs_same_origin': len(same_origin_corrs),
        'n_pairs_mixed_origin': len(mixed_origin_corrs),
        'n_pairs_AA': len(AA_corrs),
        'n_pairs_BB': len(BB_corrs),
        'n_pairs_AB': len(AB_corrs),
        'mean_corr_same': np.mean(same_origin_corrs) if same_origin_corrs else np.nan,
        'mean_corr_mixed': np.mean(mixed_origin_corrs) if mixed_origin_corrs else np.nan,
        'mean_corr_AA': np.mean(AA_corrs) if AA_corrs else np.nan,
        'mean_corr_BB': np.mean(BB_corrs) if BB_corrs else np.nan,
        'mean_corr_AB': np.mean(AB_corrs) if AB_corrs else np.nan,
        'median_corr_same': np.median(same_origin_corrs) if same_origin_corrs else np.nan,
        'median_corr_mixed': np.median(mixed_origin_corrs) if mixed_origin_corrs else np.nan,
        'std_corr_same': np.std(same_origin_corrs) if same_origin_corrs else np.nan,
        'std_corr_mixed': np.std(mixed_origin_corrs) if mixed_origin_corrs else np.nan,
    }

    return pair_data, summary


def perform_statistical_tests(pair_data: List[Dict]) -> Dict[str, Any]:
    """
    Perform statistical tests comparing same-origin vs mixed-origin correlations.

    Tests:
    1. Two-sample t-test (parametric)
    2. Mann-Whitney U test (non-parametric)
    3. Permutation test (10,000 permutations)

    Returns:
        Dictionary with test results
    """
    same_origin_corrs = np.array([p['correlation'] for p in pair_data if p['pair_type'] == 'same_origin'])
    mixed_origin_corrs = np.array([p['correlation'] for p in pair_data if p['pair_type'] == 'mixed_origin'])

    # 1. Two-sample t-test
    t_stat, t_pval = stats.ttest_ind(same_origin_corrs, mixed_origin_corrs)

    # 2. Mann-Whitney U test
    u_stat, u_pval = stats.mannwhitneyu(same_origin_corrs, mixed_origin_corrs, alternative='two-sided')

    # 3. Permutation test
    observed_diff = np.mean(same_origin_corrs) - np.mean(mixed_origin_corrs)

    n_permutations = 10000
    permuted_diffs = []

    all_corrs = np.concatenate([same_origin_corrs, mixed_origin_corrs])
    n_same = len(same_origin_corrs)

    rng = np.random.RandomState(42)

    for _ in range(n_permutations):
        # Shuffle labels
        shuffled = rng.permutation(all_corrs)
        perm_same = shuffled[:n_same]
        perm_mixed = shuffled[n_same:]
        perm_diff = np.mean(perm_same) - np.mean(perm_mixed)
        permuted_diffs.append(perm_diff)

    permuted_diffs = np.array(permuted_diffs)

    # Two-sided p-value
    perm_pval = np.mean(np.abs(permuted_diffs) >= np.abs(observed_diff))

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((np.std(same_origin_corrs)**2 + np.std(mixed_origin_corrs)**2) / 2)
    cohens_d = observed_diff / pooled_std if pooled_std > 0 else 0.0

    return {
        'observed_difference': observed_diff,
        'cohens_d': cohens_d,
        't_statistic': t_stat,
        't_pvalue': t_pval,
        'u_statistic': u_stat,
        'u_pvalue': u_pval,
        'permutation_pvalue': perm_pval,
        'permuted_diffs': permuted_diffs,
        'n_same_origin': len(same_origin_corrs),
        'n_mixed_origin': len(mixed_origin_corrs)
    }


def generate_null_model_correlations(offspring_list: List[np.ndarray],
                                    species_origins: np.ndarray,
                                    threshold: float = 1e-4,
                                    min_variance_pairs: int = 3,
                                    n_simulations: int = 1000,
                                    random_seed: int = 42) -> Dict[str, Any]:
    """
    Generate null model by randomizing species origin labels.

    This preserves the actual presence/absence patterns but breaks the
    association between species origins and correlations.

    Returns:
        Dictionary with null distribution of mean correlations
    """
    rng = np.random.RandomState(random_seed)
    n_species = len(offspring_list[0])

    null_same_means = []
    null_mixed_means = []

    print(f"\nGenerating null model ({n_simulations} simulations)...")

    for sim in range(n_simulations):
        # Randomize origin labels
        shuffled_origins = rng.permutation(species_origins)

        # Calculate correlations with shuffled labels
        pair_data_null, summary_null = calculate_pairwise_correlations(
            offspring_list, shuffled_origins, threshold, min_variance_pairs
        )

        # Only append if not NaN
        if not np.isnan(summary_null['mean_corr_same']):
            null_same_means.append(summary_null['mean_corr_same'])
        if not np.isnan(summary_null['mean_corr_mixed']):
            null_mixed_means.append(summary_null['mean_corr_mixed'])

        if (sim + 1) % 100 == 0:
            print(f"  Completed {sim + 1}/{n_simulations} simulations")

    # Use nanmean to handle any remaining NaN values
    return {
        'null_same_means': np.array(null_same_means),
        'null_mixed_means': np.array(null_mixed_means),
        'expected_same_mean': np.nanmean(null_same_means) if len(null_same_means) > 0 else np.nan,
        'expected_mixed_mean': np.nanmean(null_mixed_means) if len(null_mixed_means) > 0 else np.nan,
        'expected_same_std': np.nanstd(null_same_means) if len(null_same_means) > 0 else np.nan,
        'expected_mixed_std': np.nanstd(null_mixed_means) if len(null_mixed_means) > 0 else np.nan
    }


def analyze_pairwise_correlations(offspring_list: List[np.ndarray],
                                 parent1_list: List[np.ndarray],
                                 parent2_list: List[np.ndarray],
                                 threshold: float = 1e-4,
                                 min_variance_pairs: int = 3,
                                 n_simulations: int = 1000) -> Dict[str, Any]:
    """
    Main analysis function.

    Returns:
        Dictionary with all results including null model
    """
    print(f"\nAnalyzing {len(offspring_list)} replicates...")

    # Determine species origins
    species_origins = determine_species_origins(parent1_list, parent2_list, threshold)
    n_from_A = np.sum(species_origins == 0)
    n_from_B = np.sum(species_origins == 1)

    print(f"Species origins: {n_from_A} from Parent A, {n_from_B} from Parent B")

    # Calculate pairwise correlations
    pair_data, summary = calculate_pairwise_correlations(
        offspring_list, species_origins, threshold, min_variance_pairs
    )

    print(f"\nPairwise correlations calculated:")
    print(f"  Total pairs: {summary['n_pairs_total']}")
    print(f"  Same-origin pairs: {summary['n_pairs_same_origin']} (AA: {summary['n_pairs_AA']}, BB: {summary['n_pairs_BB']})")
    print(f"  Mixed-origin pairs: {summary['n_pairs_mixed_origin']}")
    print(f"\nMean correlations:")
    print(f"  Same-origin: {summary['mean_corr_same']:.4f}")
    print(f"  Mixed-origin: {summary['mean_corr_mixed']:.4f}")
    print(f"  Difference: {summary['mean_corr_same'] - summary['mean_corr_mixed']:.4f}")

    # Perform statistical tests
    test_results = perform_statistical_tests(pair_data)

    print(f"\nStatistical Tests:")
    print(f"  t-test: t = {test_results['t_statistic']:.4f}, p = {test_results['t_pvalue']:.4f}")
    print(f"  Mann-Whitney U: U = {test_results['u_statistic']:.1f}, p = {test_results['u_pvalue']:.4f}")
    print(f"  Permutation test: p = {test_results['permutation_pvalue']:.4f}")
    print(f"  Effect size (Cohen's d): {test_results['cohens_d']:.4f}")

    # Generate null model
    null_results = generate_null_model_correlations(
        offspring_list, species_origins, threshold, min_variance_pairs, n_simulations
    )

    print(f"\nNull Model Results:")
    print(f"  Expected same-origin: {null_results['expected_same_mean']:.4f}")
    print(f"  Expected mixed-origin: {null_results['expected_mixed_mean']:.4f}")
    print(f"  Expected difference: {null_results['expected_same_mean'] - null_results['expected_mixed_mean']:.4f}")

    return {
        'pair_data': pair_data,
        'summary': summary,
        'test_results': test_results,
        'null_results': null_results,
        'species_origins': species_origins,
        'n_replicates': len(offspring_list)
    }
