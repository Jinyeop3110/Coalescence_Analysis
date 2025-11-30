#!/usr/bin/env python3
"""
Co-occurrence Null Model Analysis - Simulation-Based Approach

This implements a simulation-based null model that works even with limited replicates.
Instead of testing each pair individually, we test whether same-origin vs mixed-origin
co-presence is over-represented beyond what would be expected from independent species
invasion probabilities.

Key Idea:
1. Estimate each species' independent invasion probability p_i
2. Generate synthetic communities by sampling x_i ~ Bernoulli(p_i)
3. Count same-origin (AA, BB) and mixed-origin (AB) co-present pairs in synthetic communities
4. Compare observed counts to null distribution to get z-scores and p-values

Author: Gore Lab Coalescence Analysis Team
Date: November 2025
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


def estimate_species_invasion_probabilities(offspring_list: List[np.ndarray],
                                           parent1_list: List[np.ndarray],
                                           parent2_list: List[np.ndarray],
                                           threshold: float = 1e-4) -> np.ndarray:
    """
    Estimate each species' independent invasion probability.

    p_i = (# replicates where species i is present in offspring) / (total replicates)

    Args:
        offspring_list: List of offspring abundance vectors
        parent1_list: List of parent1 abundance vectors
        parent2_list: List of parent2 abundance vectors
        threshold: Abundance threshold for presence

    Returns:
        Array of invasion probabilities for each species
    """
    n_replicates = len(offspring_list)
    n_species = len(offspring_list[0])

    # Count presence across all replicates
    presence_counts = np.zeros(n_species)

    for offspring in offspring_list:
        present = offspring > threshold
        presence_counts += present.astype(int)

    # Calculate probabilities
    invasion_probs = presence_counts / n_replicates

    return invasion_probs


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


def count_copresent_pairs(presence_vector: np.ndarray,
                          species_origins: np.ndarray) -> Dict[str, float]:
    """
    Count same-origin (AA, BB) and mixed-origin (AB) co-present pairs.
    Returns both raw counts and fractions (out of all possible pairs of that type).

    Args:
        presence_vector: Binary vector (1 = present, 0 = absent)
        species_origins: Origin labels (0 = A, 1 = B)

    Returns:
        Dictionary with counts and fractions
    """
    # Get indices of present species
    present_species = np.where(presence_vector > 0)[0]

    # Count species by origin
    present_from_A = [s for s in present_species if species_origins[s] == 0]
    present_from_B = [s for s in present_species if species_origins[s] == 1]

    k_A = len(present_from_A)
    k_B = len(present_from_B)

    # Count pairs (combinations) that are CO-PRESENT
    T_AA = k_A * (k_A - 1) // 2  # C(k_A, 2)
    T_BB = k_B * (k_B - 1) // 2  # C(k_B, 2)
    T_AB = k_A * k_B             # All cross-origin pairs

    # Total number of species by origin in the ENTIRE dataset
    n_species_A = np.sum(species_origins == 0)
    n_species_B = np.sum(species_origins == 1)

    # Total POSSIBLE pairs of each type
    max_AA = n_species_A * (n_species_A - 1) // 2  # All possible A-A pairs
    max_BB = n_species_B * (n_species_B - 1) // 2  # All possible B-B pairs
    max_AB = n_species_A * n_species_B              # All possible A-B pairs

    # Calculate fractions
    frac_AA = T_AA / max_AA if max_AA > 0 else 0.0
    frac_BB = T_BB / max_BB if max_BB > 0 else 0.0
    frac_AB = T_AB / max_AB if max_AB > 0 else 0.0
    frac_same = (T_AA + T_BB) / (max_AA + max_BB) if (max_AA + max_BB) > 0 else 0.0

    return {
        'T_AA': T_AA,
        'T_BB': T_BB,
        'T_AB': T_AB,
        'T_same': T_AA + T_BB,
        'frac_AA': frac_AA,
        'frac_BB': frac_BB,
        'frac_AB': frac_AB,
        'frac_same': frac_same,
        'k_A': k_A,
        'k_B': k_B,
        'total_present': k_A + k_B,
        'max_AA': max_AA,
        'max_BB': max_BB,
        'max_AB': max_AB
    }


def generate_synthetic_community(invasion_probs: np.ndarray,
                                 random_state: np.random.RandomState = None) -> np.ndarray:
    """
    Generate a synthetic community by independent Bernoulli sampling.

    For each species i: x_i ~ Bernoulli(p_i)

    Args:
        invasion_probs: Species-specific invasion probabilities
        random_state: Random state for reproducibility

    Returns:
        Binary presence/absence vector
    """
    if random_state is None:
        random_state = np.random.RandomState()

    # Sample presence/absence independently for each species
    presence = random_state.binomial(1, invasion_probs)

    return presence


def run_null_model_simulation(invasion_probs: np.ndarray,
                              species_origins: np.ndarray,
                              n_simulations: int = 10000,
                              random_seed: int = 42) -> pd.DataFrame:
    """
    Run null model simulations to generate distribution of pair counts and fractions.

    Args:
        invasion_probs: Species invasion probabilities
        species_origins: Species origin labels
        n_simulations: Number of synthetic communities to generate
        random_seed: Random seed for reproducibility

    Returns:
        DataFrame with counts and fractions for each simulation
    """
    rng = np.random.RandomState(random_seed)

    results = []

    for b in range(n_simulations):
        # Generate synthetic community
        presence = generate_synthetic_community(invasion_probs, rng)

        # Count pairs and calculate fractions
        counts = count_copresent_pairs(presence, species_origins)

        results.append({
            'sim_id': b,
            'T_AA': counts['T_AA'],
            'T_BB': counts['T_BB'],
            'T_AB': counts['T_AB'],
            'T_same': counts['T_same'],
            'frac_AA': counts['frac_AA'],
            'frac_BB': counts['frac_BB'],
            'frac_AB': counts['frac_AB'],
            'frac_same': counts['frac_same'],
            'k_A': counts['k_A'],
            'k_B': counts['k_B'],
            'total_present': counts['total_present']
        })

    return pd.DataFrame(results)


def calculate_enrichment_statistics_null(observed_counts: Dict[str, float],
                                        null_distribution: pd.DataFrame,
                                        alpha: float = 0.05) -> Dict[str, Any]:
    """
    Calculate enrichment statistics by comparing observed to null distribution.
    Works with both counts and fractions.

    Args:
        observed_counts: Observed pair counts and fractions
        null_distribution: DataFrame with null model simulations
        alpha: Significance level

    Returns:
        Dictionary with statistics and p-values
    """
    # Extract observed values (counts and fractions)
    T_AA_obs = observed_counts['T_AA']
    T_BB_obs = observed_counts['T_BB']
    T_AB_obs = observed_counts['T_AB']
    T_same_obs = observed_counts['T_same']

    frac_AA_obs = observed_counts['frac_AA']
    frac_BB_obs = observed_counts['frac_BB']
    frac_AB_obs = observed_counts['frac_AB']
    frac_same_obs = observed_counts['frac_same']

    # Null distribution statistics (counts)
    T_AA_null = null_distribution['T_AA'].values
    T_BB_null = null_distribution['T_BB'].values
    T_AB_null = null_distribution['T_AB'].values
    T_same_null = null_distribution['T_same'].values

    # Null distribution statistics (fractions)
    frac_AA_null = null_distribution['frac_AA'].values
    frac_BB_null = null_distribution['frac_BB'].values
    frac_AB_null = null_distribution['frac_AB'].values
    frac_same_null = null_distribution['frac_same'].values

    # Calculate z-scores for FRACTIONS (more interpretable)
    z_AA = (frac_AA_obs - np.mean(frac_AA_null)) / (np.std(frac_AA_null) + 1e-10)
    z_BB = (frac_BB_obs - np.mean(frac_BB_null)) / (np.std(frac_BB_null) + 1e-10)
    z_AB = (frac_AB_obs - np.mean(frac_AB_null)) / (np.std(frac_AB_null) + 1e-10)
    z_same = (frac_same_obs - np.mean(frac_same_null)) / (np.std(frac_same_null) + 1e-10)

    # Calculate empirical p-values (two-sided) using FRACTIONS
    p_AA = np.mean(np.abs(frac_AA_null - np.mean(frac_AA_null)) >= np.abs(frac_AA_obs - np.mean(frac_AA_null)))
    p_BB = np.mean(np.abs(frac_BB_null - np.mean(frac_BB_null)) >= np.abs(frac_BB_obs - np.mean(frac_BB_null)))
    p_AB = np.mean(np.abs(frac_AB_null - np.mean(frac_AB_null)) >= np.abs(frac_AB_obs - np.mean(frac_AB_null)))
    p_same = np.mean(np.abs(frac_same_null - np.mean(frac_same_null)) >= np.abs(frac_same_obs - np.mean(frac_same_null)))

    # One-sided p-values (greater than null) using FRACTIONS
    p_AA_greater = np.mean(frac_AA_null >= frac_AA_obs)
    p_BB_greater = np.mean(frac_BB_null >= frac_BB_obs)
    p_AB_greater = np.mean(frac_AB_null >= frac_AB_obs)
    p_same_greater = np.mean(frac_same_null >= frac_same_obs)

    # Calculate enrichment ratio using FRACTIONS
    if np.mean(frac_AB_null) > 0:
        enrichment_ratio = frac_same_obs / frac_AB_obs if frac_AB_obs > 0 else np.inf
        enrichment_ratio_null = np.mean(frac_same_null) / np.mean(frac_AB_null)
        relative_enrichment = enrichment_ratio / enrichment_ratio_null
    else:
        enrichment_ratio = np.nan
        enrichment_ratio_null = np.nan
        relative_enrichment = np.nan

    return {
        'observed': {
            'T_AA': T_AA_obs,
            'T_BB': T_BB_obs,
            'T_AB': T_AB_obs,
            'T_same': T_same_obs,
            'frac_AA': frac_AA_obs,
            'frac_BB': frac_BB_obs,
            'frac_AB': frac_AB_obs,
            'frac_same': frac_same_obs,
            'k_A': observed_counts['k_A'],
            'k_B': observed_counts['k_B']
        },
        'expected': {
            'T_AA_mean': np.mean(T_AA_null),
            'T_AA_std': np.std(T_AA_null),
            'T_BB_mean': np.mean(T_BB_null),
            'T_BB_std': np.std(T_BB_null),
            'T_AB_mean': np.mean(T_AB_null),
            'T_AB_std': np.std(T_AB_null),
            'T_same_mean': np.mean(T_same_null),
            'T_same_std': np.std(T_same_null),
            'frac_AA_mean': np.mean(frac_AA_null),
            'frac_AA_std': np.std(frac_AA_null),
            'frac_BB_mean': np.mean(frac_BB_null),
            'frac_BB_std': np.std(frac_BB_null),
            'frac_AB_mean': np.mean(frac_AB_null),
            'frac_AB_std': np.std(frac_AB_null),
            'frac_same_mean': np.mean(frac_same_null),
            'frac_same_std': np.std(frac_same_null)
        },
        'z_scores': {
            'z_AA': z_AA,
            'z_BB': z_BB,
            'z_AB': z_AB,
            'z_same': z_same
        },
        'p_values_two_sided': {
            'p_AA': p_AA,
            'p_BB': p_BB,
            'p_AB': p_AB,
            'p_same': p_same
        },
        'p_values_greater': {
            'p_AA_greater': p_AA_greater,
            'p_BB_greater': p_BB_greater,
            'p_AB_greater': p_AB_greater,
            'p_same_greater': p_same_greater
        },
        'enrichment': {
            'enrichment_ratio': enrichment_ratio,
            'enrichment_ratio_null': enrichment_ratio_null,
            'relative_enrichment': relative_enrichment
        },
        'alpha': alpha
    }


def analyze_cooccurrence_with_null_model(offspring_list: List[np.ndarray],
                                         parent1_list: List[np.ndarray],
                                         parent2_list: List[np.ndarray],
                                         threshold: float = 1e-4,
                                         n_simulations: int = 10000,
                                         random_seed: int = 42) -> Dict[str, Any]:
    """
    Main function to analyze co-occurrence using simulation-based null model.

    Args:
        offspring_list: List of offspring abundance vectors
        parent1_list: List of parent1 abundance vectors
        parent2_list: List of parent2 abundance vectors
        threshold: Abundance threshold for presence/absence
        n_simulations: Number of null model simulations
        random_seed: Random seed

    Returns:
        Dictionary with analysis results
    """
    print(f"Analyzing {len(offspring_list)} coalescence replicates with null model...")

    # Step 1: Estimate invasion probabilities
    print("Step 1: Estimating species invasion probabilities...")
    invasion_probs = estimate_species_invasion_probabilities(
        offspring_list, parent1_list, parent2_list, threshold
    )

    print(f"  Species with p > 0: {np.sum(invasion_probs > 0)} / {len(invasion_probs)}")
    print(f"  Mean invasion probability: {np.mean(invasion_probs[invasion_probs > 0]):.3f}")

    # Step 2: Determine species origins
    print("Step 2: Determining species origins...")
    species_origins = determine_species_origins(parent1_list, parent2_list, threshold)

    n_from_A = np.sum(species_origins == 0)
    n_from_B = np.sum(species_origins == 1)
    print(f"  Parent A species: {n_from_A}")
    print(f"  Parent B species: {n_from_B}")

    # Step 3: Count observed pairs (across all replicates)
    print("Step 3: Counting observed co-present pairs...")
    observed_counts_list = []

    for offspring in offspring_list:
        presence = (offspring > threshold).astype(int)
        counts = count_copresent_pairs(presence, species_origins)
        observed_counts_list.append(counts)

    # Average across replicates
    observed_counts_avg = {
        'T_AA': np.mean([c['T_AA'] for c in observed_counts_list]),
        'T_BB': np.mean([c['T_BB'] for c in observed_counts_list]),
        'T_AB': np.mean([c['T_AB'] for c in observed_counts_list]),
        'T_same': np.mean([c['T_same'] for c in observed_counts_list]),
        'frac_AA': np.mean([c['frac_AA'] for c in observed_counts_list]),
        'frac_BB': np.mean([c['frac_BB'] for c in observed_counts_list]),
        'frac_AB': np.mean([c['frac_AB'] for c in observed_counts_list]),
        'frac_same': np.mean([c['frac_same'] for c in observed_counts_list]),
        'k_A': np.mean([c['k_A'] for c in observed_counts_list]),
        'k_B': np.mean([c['k_B'] for c in observed_counts_list])
    }

    print(f"  Observed T_AA (avg): {observed_counts_avg['T_AA']:.1f}")
    print(f"  Observed T_BB (avg): {observed_counts_avg['T_BB']:.1f}")
    print(f"  Observed T_AB (avg): {observed_counts_avg['T_AB']:.1f}")
    print(f"  Observed T_same (avg): {observed_counts_avg['T_AA'] + observed_counts_avg['T_BB']:.1f}")

    # Step 4: Run null model simulations
    print(f"Step 4: Running {n_simulations} null model simulations...")
    null_distribution = run_null_model_simulation(
        invasion_probs, species_origins, n_simulations, random_seed
    )

    print(f"  Expected T_AA (mean): {null_distribution['T_AA'].mean():.1f}")
    print(f"  Expected T_BB (mean): {null_distribution['T_BB'].mean():.1f}")
    print(f"  Expected T_AB (mean): {null_distribution['T_AB'].mean():.1f}")
    print(f"  Expected T_same (mean): {null_distribution['T_same'].mean():.1f}")

    # Step 5: Calculate statistics
    print("Step 5: Calculating enrichment statistics...")
    stats_results = calculate_enrichment_statistics_null(
        observed_counts_avg, null_distribution
    )

    return {
        'invasion_probabilities': invasion_probs,
        'species_origins': species_origins,
        'observed_counts': observed_counts_list,
        'observed_counts_avg': observed_counts_avg,
        'null_distribution': null_distribution,
        'statistics': stats_results,
        'n_replicates': len(offspring_list),
        'n_species': len(invasion_probs)
    }


def print_null_model_summary(results: Dict[str, Any]):
    """Print summary of null model analysis results."""
    stats = results['statistics']

    print("\n" + "="*80)
    print("CO-OCCURRENCE NULL MODEL ANALYSIS SUMMARY")
    print("="*80)

    print(f"\nData:")
    print(f"  Replicates: {results['n_replicates']}")
    print(f"  Species: {results['n_species']}")

    print(f"\nObserved Pair Fractions (averaged across replicates):")
    print(f"  frac_AA (A-A pairs): {stats['observed']['frac_AA']:.4f}")
    print(f"  frac_BB (B-B pairs): {stats['observed']['frac_BB']:.4f}")
    print(f"  frac_AB (A-B pairs): {stats['observed']['frac_AB']:.4f}")
    print(f"  frac_same (AA + BB): {stats['observed']['frac_same']:.4f}")

    print(f"\nExpected Pair Fractions (from null model):")
    print(f"  frac_AA: {stats['expected']['frac_AA_mean']:.4f} ± {stats['expected']['frac_AA_std']:.4f}")
    print(f"  frac_BB: {stats['expected']['frac_BB_mean']:.4f} ± {stats['expected']['frac_BB_std']:.4f}")
    print(f"  frac_AB: {stats['expected']['frac_AB_mean']:.4f} ± {stats['expected']['frac_AB_std']:.4f}")
    print(f"  frac_same: {stats['expected']['frac_same_mean']:.4f} ± {stats['expected']['frac_same_std']:.4f}")

    print(f"\nEnrichment Ratio:")
    print(f"  Observed: {stats['enrichment']['enrichment_ratio']:.3f}")
    print(f"  Expected (null): {stats['enrichment']['enrichment_ratio_null']:.3f}")
    print(f"  Relative enrichment: {stats['enrichment']['relative_enrichment']:.3f}")

    print(f"\nZ-scores (based on fractions):")
    print(f"  z_AA: {stats['z_scores']['z_AA']:.3f}")
    print(f"  z_BB: {stats['z_scores']['z_BB']:.3f}")
    print(f"  z_AB: {stats['z_scores']['z_AB']:.3f}")
    print(f"  z_same: {stats['z_scores']['z_same']:.3f}")

    print(f"\nP-values (empirical, two-sided, based on fractions):")
    print(f"  p_AA: {stats['p_values_two_sided']['p_AA']:.4f}")
    print(f"  p_BB: {stats['p_values_two_sided']['p_BB']:.4f}")
    print(f"  p_AB: {stats['p_values_two_sided']['p_AB']:.4f}")
    print(f"  p_same: {stats['p_values_two_sided']['p_same']:.4f}")

    # Interpret z_same
    z_same = stats['z_scores']['z_same']
    p_same = stats['p_values_two_sided']['p_same']

    print(f"\nInterpretation:")
    if p_same < 0.001:
        sig = "***"
    elif p_same < 0.01:
        sig = "**"
    elif p_same < 0.05:
        sig = "*"
    else:
        sig = "ns"

    if z_same > 2:
        print(f"  Same-origin pairs are OVER-REPRESENTED (z={z_same:.2f}, p={p_same:.4f} {sig})")
        print(f"  → Species from the same parent tend to co-occur more than expected")
    elif z_same < -2:
        print(f"  Same-origin pairs are UNDER-REPRESENTED (z={z_same:.2f}, p={p_same:.4f} {sig})")
        print(f"  → Species from different parents tend to co-occur more than expected")
    else:
        print(f"  Same-origin pairs match null expectations (z={z_same:.2f}, p={p_same:.4f} {sig})")
        print(f"  → Co-occurrence is consistent with independent invasion probabilities")


if __name__ == "__main__":
    print("Co-occurrence Null Model Analysis Module")
    print("Use run_cooccurrence_null_model_analysis.py to analyze real data")
