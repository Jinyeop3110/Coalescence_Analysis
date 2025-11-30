"""
Pairwise Correlation Analysis - Per Replicate Session

This module analyzes pairwise correlations WITHIN each replicate session,
treating each replicate's coalescence events as independent.

Key difference from pooled analysis:
- Pooled: Treats all 600 events as one dataset
- Per-replicate: Analyzes 6 events within each of 100 replicates separately
"""

import numpy as np
from scipy.stats import pearsonr, ttest_ind, mannwhitneyu
from collections import defaultdict


def analyze_within_replicate_correlations(replicate_offspring_list, replicate_parent1_list,
                                          replicate_parent2_list, threshold=1e-4):
    """
    Analyze pairwise correlations within ONE replicate session.

    Args:
        replicate_offspring_list: List of offspring communities (6 events)
        replicate_parent1_list: List of parent1 communities (6 events)
        replicate_parent2_list: List of parent2 communities (6 events)
        threshold: Minimum abundance to consider species present

    Returns:
        dict with correlation statistics for this replicate
    """
    n_events = len(replicate_offspring_list)
    n_species = len(replicate_offspring_list[0])

    # Build presence/absence matrix (n_events x n_species)
    offspring_matrix = np.array([
        (np.array(off) > threshold).astype(int)
        for off in replicate_offspring_list
    ])

    # Determine species origins
    # Average parent communities to assign origin
    avg_p1 = np.mean([np.array(p) for p in replicate_parent1_list], axis=0)
    avg_p2 = np.mean([np.array(p) for p in replicate_parent2_list], axis=0)

    species_origins = np.zeros(n_species, dtype=int)  # 0 = parent A, 1 = parent B
    for i in range(n_species):
        if avg_p1[i] > threshold and avg_p2[i] <= threshold:
            species_origins[i] = 0  # From parent A
        elif avg_p2[i] > threshold and avg_p1[i] <= threshold:
            species_origins[i] = 1  # From parent B
        elif avg_p1[i] > threshold and avg_p2[i] > threshold:
            # Present in both, assign to more abundant one
            species_origins[i] = 0 if avg_p1[i] >= avg_p2[i] else 1
        else:
            species_origins[i] = -1  # Not clearly from either parent

    # Calculate pairwise correlations
    same_origin_corrs = []
    mixed_origin_corrs = []

    for i in range(n_species):
        if species_origins[i] == -1:
            continue

        for j in range(i + 1, n_species):
            if species_origins[j] == -1:
                continue

            vec_i = offspring_matrix[:, i]
            vec_j = offspring_matrix[:, j]

            # Skip if no variance
            if np.std(vec_i) == 0 or np.std(vec_j) == 0:
                continue

            # Calculate correlation
            corr, _ = pearsonr(vec_i, vec_j)

            # Classify by origin
            if species_origins[i] == species_origins[j]:
                same_origin_corrs.append(corr)
            else:
                mixed_origin_corrs.append(corr)

    return {
        'n_events': n_events,
        'n_species_from_A': np.sum(species_origins == 0),
        'n_species_from_B': np.sum(species_origins == 1),
        'same_origin_corrs': same_origin_corrs,
        'mixed_origin_corrs': mixed_origin_corrs,
        'mean_same': np.mean(same_origin_corrs) if same_origin_corrs else np.nan,
        'mean_mixed': np.mean(mixed_origin_corrs) if mixed_origin_corrs else np.nan,
    }


def analyze_simulation_per_replicate(json_data, interaction_strength, n_simulations=1000):
    """
    Analyze pairwise correlations treating each replicate as independent.

    Args:
        json_data: Loaded simulation JSON data
        interaction_strength: e.g., '0.3', '0.5', '0.8'
        n_simulations: Number of null model simulations

    Returns:
        dict with aggregate results across all replicates
    """
    param_key = interaction_strength
    param_data = json_data[param_key]

    print(f"Analyzing {len(param_data)} replicates...")

    # Analyze each replicate separately
    replicate_results = []

    for rep_idx, (rep_key, rep_data) in enumerate(param_data.items()):
        sc_list = rep_data['sc_list']
        cc_list = rep_data['cc_list']

        # Get coalescence pairs
        coalescence_keys = sorted([k for k in cc_list.keys() if '_' in k])

        # Build lists for this replicate
        rep_offspring = []
        rep_parent1 = []
        rep_parent2 = []

        for pair_key in coalescence_keys:
            idx1, idx2 = pair_key.split('_')

            rep_offspring.append(cc_list[pair_key])
            rep_parent1.append(sc_list[idx1])
            rep_parent2.append(sc_list[idx2])

        # Analyze this replicate
        result = analyze_within_replicate_correlations(
            rep_offspring, rep_parent1, rep_parent2
        )
        replicate_results.append(result)

    # Aggregate across replicates
    all_same_corrs = [r['mean_same'] for r in replicate_results if not np.isnan(r['mean_same'])]
    all_mixed_corrs = [r['mean_mixed'] for r in replicate_results if not np.isnan(r['mean_mixed'])]

    # Calculate aggregate statistics
    mean_same = np.mean(all_same_corrs) if all_same_corrs else 0
    mean_mixed = np.mean(all_mixed_corrs) if all_mixed_corrs else 0
    std_same = np.std(all_same_corrs) if all_same_corrs else 0
    std_mixed = np.std(all_mixed_corrs) if all_mixed_corrs else 0

    print(f"  Same-origin correlation: {mean_same:.4f} ± {std_same:.4f}")
    print(f"  Mixed-origin correlation: {mean_mixed:.4f} ± {std_mixed:.4f}")
    print(f"  Difference: {mean_same - mean_mixed:.4f}")

    # Statistical test
    if len(all_same_corrs) > 1 and len(all_mixed_corrs) > 1:
        t_stat, p_val = ttest_ind(all_same_corrs, all_mixed_corrs)
        print(f"  t-test p-value: {p_val:.4f}")
    else:
        p_val = 1.0

    # Generate null model
    print(f"Generating null model ({n_simulations} simulations)...")
    null_same_means = []
    null_mixed_means = []

    for sim_idx in range(n_simulations):
        if (sim_idx + 1) % 100 == 0:
            print(f"  Completed {sim_idx + 1}/{n_simulations} simulations")

        # Randomly shuffle origins within each replicate
        sim_same = []
        sim_mixed = []

        for result in replicate_results:
            # Pool all correlations and randomly assign to same/mixed
            all_corrs = result['same_origin_corrs'] + result['mixed_origin_corrs']

            if len(all_corrs) > 0:
                n_same = len(result['same_origin_corrs'])
                n_mixed = len(result['mixed_origin_corrs'])

                # Randomly shuffle
                np.random.shuffle(all_corrs)

                if n_same > 0:
                    sim_same.extend(all_corrs[:n_same])
                if n_mixed > 0:
                    sim_mixed.extend(all_corrs[n_same:n_same+n_mixed])

        null_same_means.append(np.mean(sim_same) if sim_same else 0)
        null_mixed_means.append(np.mean(sim_mixed) if sim_mixed else 0)

    null_same_mean = np.mean(null_same_means)
    null_mixed_mean = np.mean(null_mixed_means)

    print(f"Null model:")
    print(f"  Expected same-origin: {null_same_mean:.4f}")
    print(f"  Expected mixed-origin: {null_mixed_mean:.4f}")

    # Calculate permutation p-value
    observed_diff = mean_same - mean_mixed
    null_diffs = np.array(null_same_means) - np.array(null_mixed_means)
    perm_pvalue = np.sum(np.abs(null_diffs) >= np.abs(observed_diff)) / n_simulations
    print(f"  Permutation p-value: {perm_pvalue:.4f}")

    return {
        'n_replicates': len(replicate_results),
        'summary': {
            'mean_corr_same': mean_same,
            'mean_corr_mixed': mean_mixed,
            'std_corr_same': std_same,
            'std_corr_mixed': std_mixed,
            'n_pairs_same_origin': len(all_same_corrs),
            'n_pairs_mixed_origin': len(all_mixed_corrs),
        },
        'null_results': {
            'expected_same_mean': null_same_mean,
            'expected_mixed_mean': null_mixed_mean,
            'null_same_means': null_same_means,
            'null_mixed_means': null_mixed_means,
            'expected_same_std': np.std(null_same_means),
            'expected_mixed_std': np.std(null_mixed_means),
        },
        'test_results': {
            't_pvalue': p_val,
            'permutation_pvalue': perm_pvalue,
            'observed_difference': observed_diff,
        },
        'replicate_results': replicate_results,
        'all_same_corrs': all_same_corrs,
        'all_mixed_corrs': all_mixed_corrs,
    }
