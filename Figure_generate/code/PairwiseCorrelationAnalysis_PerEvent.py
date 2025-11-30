#!/usr/bin/env python3
"""
Per-Event Pairwise Correlation Analysis

For EACH coalescence event independently:
1. Identify species origins from that event's parent pair
2. Calculate same-origin correlation (among M species + among N species)
3. Calculate mixed-origin correlation (between M and N species)

Then average across all events.

This is fundamentally different from the cross-replicate approach!
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any
from scipy import stats
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')


def determine_species_origins_single_event(parent1: np.ndarray,
                                           parent2: np.ndarray,
                                           threshold: float = 1e-4) -> np.ndarray:
    """
    Determine which parent each species originates from for a SINGLE event.

    Args:
        parent1: Abundance vector for Parent A
        parent2: Abundance vector for Parent B
        threshold: Presence threshold

    Returns:
        Array where 0 = Parent A, 1 = Parent B, -1 = neither/both equally
    """
    n_species = len(parent1)
    species_origins = np.full(n_species, -1, dtype=int)

    for s in range(n_species):
        present_in_p1 = parent1[s] > threshold
        present_in_p2 = parent2[s] > threshold

        if present_in_p1 and not present_in_p2:
            species_origins[s] = 0  # Parent A
        elif present_in_p2 and not present_in_p1:
            species_origins[s] = 1  # Parent B
        elif present_in_p1 and present_in_p2:
            # Assign to parent with higher abundance
            species_origins[s] = 0 if parent1[s] >= parent2[s] else 1
        else:
            species_origins[s] = -1  # Not present in either

    return species_origins


def calculate_correlation_single_event(offspring: np.ndarray,
                                       parent1: np.ndarray,
                                       parent2: np.ndarray,
                                       threshold: float = 1e-4) -> Dict:
    """
    Calculate same-origin and mixed-origin correlations for a SINGLE event.

    The correlation here is based on co-occurrence patterns among species pairs
    within this single offspring community.

    Returns:
        Dictionary with same_origin_corr, mixed_origin_corr, and counts
    """
    # Determine species origins
    species_origins = determine_species_origins_single_event(parent1, parent2, threshold)

    # Get offspring presence
    offspring_presence = (offspring > threshold).astype(int)

    # Find species from each parent
    species_A = np.where(species_origins == 0)[0]
    species_B = np.where(species_origins == 1)[0]

    n_species_A = len(species_A)
    n_species_B = len(species_B)

    # Need at least 2 species from same origin to calculate correlation
    if n_species_A < 2 and n_species_B < 2:
        # Cannot calculate same-origin correlation
        return None

    if n_species_A < 1 or n_species_B < 1:
        # Cannot calculate mixed-origin correlation
        return None

    # Calculate same-origin correlation
    # This is the correlation between co-occurrence patterns
    # For species pairs from same origin, do they tend to co-occur or co-absent?

    same_origin_concordances = []

    # Pairs from Parent A
    if n_species_A >= 2:
        for i, j in combinations(species_A, 2):
            pi = offspring_presence[i]
            pj = offspring_presence[j]
            # Concordant if both present (1,1) or both absent (0,0)
            concordant = (pi == pj)
            same_origin_concordances.append(int(concordant))

    # Pairs from Parent B
    if n_species_B >= 2:
        for i, j in combinations(species_B, 2):
            pi = offspring_presence[i]
            pj = offspring_presence[j]
            concordant = (pi == pj)
            same_origin_concordances.append(int(concordant))

    # Calculate mixed-origin concordances
    mixed_origin_concordances = []
    for i in species_A:
        for j in species_B:
            pi = offspring_presence[i]
            pj = offspring_presence[j]
            concordant = (pi == pj)
            mixed_origin_concordances.append(int(concordant))

    # Convert concordance to correlation-like metric
    # Concordance rate: fraction of (1,1) or (0,0) outcomes
    # This is analogous to positive correlation
    # We can convert: correlation = 2 * concordance_rate - 1
    # This gives: concordance_rate=1 -> corr=1, concordance_rate=0.5 -> corr=0, concordance_rate=0 -> corr=-1

    n_same = len(same_origin_concordances)
    n_mixed = len(mixed_origin_concordances)

    if n_same == 0 or n_mixed == 0:
        return None

    concordance_same = np.mean(same_origin_concordances)
    concordance_mixed = np.mean(mixed_origin_concordances)

    # Convert to correlation-like metric
    corr_same = 2 * concordance_same - 1
    corr_mixed = 2 * concordance_mixed - 1

    return {
        'same_origin_corr': corr_same,
        'mixed_origin_corr': corr_mixed,
        'n_same_pairs': n_same,
        'n_mixed_pairs': n_mixed,
        'n_species_A': n_species_A,
        'n_species_B': n_species_B,
        'concordance_same': concordance_same,
        'concordance_mixed': concordance_mixed
    }


def analyze_pairwise_correlations_per_event(offspring_list: List[np.ndarray],
                                            parent1_list: List[np.ndarray],
                                            parent2_list: List[np.ndarray],
                                            threshold: float = 1e-4,
                                            n_simulations: int = 1000) -> Dict:
    """
    Analyze pairwise correlations calculating per-event, then averaging.

    Args:
        offspring_list: List of offspring abundance vectors (one per event)
        parent1_list: List of Parent A abundance vectors (one per event)
        parent2_list: List of Parent B abundance vectors (one per event)
        threshold: Presence threshold
        n_simulations: Number of null model simulations

    Returns:
        Dictionary with results
    """
    n_events = len(offspring_list)

    print(f"\nAnalyzing {n_events} coalescence events...")

    event_results = []

    for i in range(n_events):
        result = calculate_correlation_single_event(
            offspring_list[i],
            parent1_list[i],
            parent2_list[i],
            threshold
        )

        if result is not None:
            event_results.append(result)

    n_valid_events = len(event_results)
    print(f"Valid events with sufficient species: {n_valid_events}/{n_events}")

    if n_valid_events == 0:
        raise ValueError("No valid events found!")

    # Extract correlations
    same_origin_corrs = [r['same_origin_corr'] for r in event_results]
    mixed_origin_corrs = [r['mixed_origin_corr'] for r in event_results]

    # Summary statistics
    mean_same = np.mean(same_origin_corrs)
    mean_mixed = np.mean(mixed_origin_corrs)
    std_same = np.std(same_origin_corrs)
    std_mixed = np.std(mixed_origin_corrs)

    print(f"\nPer-event correlations calculated:")
    print(f"  Mean same-origin: {mean_same:.4f} ± {std_same:.4f}")
    print(f"  Mean mixed-origin: {mean_mixed:.4f} ± {std_mixed:.4f}")
    print(f"  Difference: {mean_same - mean_mixed:.4f}")

    # Statistical test: paired t-test
    # (each event has both same and mixed correlation)
    t_stat, t_pval = stats.ttest_rel(same_origin_corrs, mixed_origin_corrs)

    print(f"\nPaired t-test:")
    print(f"  t = {t_stat:.4f}, p = {t_pval:.4f}")

    # Null model: shuffle species origins within each event
    print(f"\nGenerating null model ({n_simulations} simulations)...")

    null_same_means = []
    null_mixed_means = []

    for sim in range(n_simulations):
        if (sim + 1) % 100 == 0:
            print(f"  Completed {sim + 1}/{n_simulations} simulations")

        sim_same = []
        sim_mixed = []

        for i in range(n_events):
            # Shuffle species origins
            species_origins_orig = determine_species_origins_single_event(
                parent1_list[i], parent2_list[i], threshold
            )

            # Only shuffle among species present in at least one parent
            valid_species = np.where(species_origins_orig >= 0)[0]

            if len(valid_species) < 3:
                continue

            shuffled_origins = species_origins_orig.copy()
            shuffled_labels = species_origins_orig[valid_species].copy()
            np.random.shuffle(shuffled_labels)
            shuffled_origins[valid_species] = shuffled_labels

            # Recalculate with shuffled origins
            offspring_presence = (offspring_list[i] > threshold).astype(int)
            species_A = np.where(shuffled_origins == 0)[0]
            species_B = np.where(shuffled_origins == 1)[0]

            if len(species_A) < 1 or len(species_B) < 1:
                continue

            # Same-origin concordances
            same_conc = []
            if len(species_A) >= 2:
                for ii, jj in combinations(species_A, 2):
                    same_conc.append(int(offspring_presence[ii] == offspring_presence[jj]))
            if len(species_B) >= 2:
                for ii, jj in combinations(species_B, 2):
                    same_conc.append(int(offspring_presence[ii] == offspring_presence[jj]))

            # Mixed-origin concordances
            mixed_conc = []
            for ii in species_A:
                for jj in species_B:
                    mixed_conc.append(int(offspring_presence[ii] == offspring_presence[jj]))

            if len(same_conc) > 0 and len(mixed_conc) > 0:
                sim_same.append(2 * np.mean(same_conc) - 1)
                sim_mixed.append(2 * np.mean(mixed_conc) - 1)

        if len(sim_same) > 0:
            null_same_means.append(np.mean(sim_same))
            null_mixed_means.append(np.mean(sim_mixed))

    null_same_means = np.array(null_same_means)
    null_mixed_means = np.array(null_mixed_means)

    # Permutation p-value
    observed_diff = mean_same - mean_mixed
    null_diffs = null_same_means - null_mixed_means
    perm_pval = np.mean(np.abs(null_diffs) >= np.abs(observed_diff))

    print(f"\nNull Model Results:")
    print(f"  Expected same-origin: {np.mean(null_same_means):.4f}")
    print(f"  Expected mixed-origin: {np.mean(null_mixed_means):.4f}")
    print(f"  Permutation p-value: {perm_pval:.4f}")

    return {
        'n_events': n_events,
        'n_valid_events': n_valid_events,
        'event_results': event_results,
        'same_origin_corrs': same_origin_corrs,
        'mixed_origin_corrs': mixed_origin_corrs,
        'summary': {
            'mean_corr_same': mean_same,
            'mean_corr_mixed': mean_mixed,
            'std_corr_same': std_same,
            'std_corr_mixed': std_mixed,
            'n_pairs_same_origin': np.sum([r['n_same_pairs'] for r in event_results]),
            'n_pairs_mixed_origin': np.sum([r['n_mixed_pairs'] for r in event_results]),
        },
        'test_results': {
            't_statistic': t_stat,
            't_pvalue': t_pval,
            'observed_difference': observed_diff,
            'permutation_pvalue': perm_pval,
        },
        'null_results': {
            'null_same_means': null_same_means,
            'null_mixed_means': null_mixed_means,
            'expected_same_mean': np.mean(null_same_means),
            'expected_mixed_mean': np.mean(null_mixed_means),
            'expected_same_std': np.std(null_same_means),
            'expected_mixed_std': np.std(null_mixed_means),
        }
    }
