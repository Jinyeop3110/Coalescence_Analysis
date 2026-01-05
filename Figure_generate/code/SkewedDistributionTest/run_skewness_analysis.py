#!/usr/bin/env python3
"""
Run Skewness Analysis for Coalescence Asymmetricity

This script runs the complete analysis testing whether observed high asymmetricity
in coalescence outcomes is due to skewed relative abundance distributions in
parental communities.

Two null models are tested:
1. Abundance-Weighted Random Selection (Approach 2)
2. Shuffled Abundance Null Model (Approach 5)

Usage:
    python run_skewness_analysis.py

Output:
    - Figures saved to Figure/SkewedDistributionTest/
    - Statistical results printed to console and saved to JSON

Author: Gore Lab Coalescence Analysis
Date: November 2025
"""

import numpy as np
import json
import os
import sys

# Add parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skewed_distribution_null_models import (
    load_coalescence_data,
    calculate_asymmetricity_distribution,
    generate_abundance_weighted_null_batch,
    generate_shuffled_abundance_null_batch,
    compare_distributions,
    analyze_skewness_asymmetricity_correlation,
    calculate_vector_asymmetricity
)

from visualization import (
    plot_asymmetricity_comparison,
    plot_asymmetricity_by_condition,
    plot_skewness_correlation,
    plot_distribution_histograms,
    create_summary_figure
)


def run_complete_analysis(data_type='synthetic', n_permutations=1000, save_dir=None):
    """
    Run complete skewness analysis.

    Args:
        data_type: 'synthetic', 'natural', or 'both'
        n_permutations: Number of null model permutations
        save_dir: Directory to save results

    Returns:
        dict: Complete analysis results
    """
    print("=" * 70)
    print("SKEWED DISTRIBUTION TEST FOR COALESCENCE ASYMMETRICITY")
    print("=" * 70)
    print(f"\nData type: {data_type}")
    print(f"Number of permutations: {n_permutations}")

    # Set up save directory
    if save_dir is None:
        save_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Figure", "SkewedDistributionTest"
        )
    os.makedirs(save_dir, exist_ok=True)
    print(f"Output directory: {save_dir}")

    # =========================================================================
    # STEP 1: Load experimental data
    # =========================================================================
    print("\n" + "-" * 50)
    print("STEP 1: Loading experimental coalescence data...")
    print("-" * 50)

    offspring_list, parent1_list, parent2_list, metadata = load_coalescence_data(data_type)

    if len(offspring_list) == 0:
        print("ERROR: No data loaded!")
        return None

    print(f"Loaded {len(offspring_list)} coalescence events")

    # =========================================================================
    # STEP 2: Calculate experimental asymmetricity and skewness metrics
    # =========================================================================
    print("\n" + "-" * 50)
    print("STEP 2: Calculating experimental asymmetricity...")
    print("-" * 50)

    exp_asymm, skewness_metrics = calculate_asymmetricity_distribution(
        offspring_list, parent1_list, parent2_list
    )

    valid_count = np.sum(~np.isnan(exp_asymm))
    print(f"Valid asymmetricity values: {valid_count}/{len(exp_asymm)}")
    print(f"Experimental asymmetricity: mean={np.nanmean(exp_asymm):.3f}, "
          f"median={np.nanmedian(exp_asymm):.3f}, std={np.nanstd(exp_asymm):.3f}")
    print(f"Mean parental Gini coefficient: {np.nanmean(skewness_metrics['mean_gini']):.3f}")

    # =========================================================================
    # STEP 3: Generate Abundance-Weighted Null Model
    # =========================================================================
    print("\n" + "-" * 50)
    print("STEP 3: Generating Abundance-Weighted Random Selection null model...")
    print("-" * 50)

    # Use observed retention rate from experimental data
    # Estimate: fraction of combined species pool that survives
    retention_rates = []
    for off, p1, p2 in zip(offspring_list, parent1_list, parent2_list):
        combined_species = np.sum((np.array(p1) > 1e-4) | (np.array(p2) > 1e-4))
        offspring_species = np.sum(np.array(off) > 1e-4)
        if combined_species > 0:
            retention_rates.append(offspring_species / combined_species)

    mean_retention = np.mean(retention_rates) if retention_rates else 0.5
    print(f"Estimated mean retention rate: {mean_retention:.3f}")

    null_offspring_aw, null_p1_aw, null_p2_aw = generate_abundance_weighted_null_batch(
        parent1_list, parent2_list,
        n_permutations=n_permutations,
        retention_rate=mean_retention
    )

    # Calculate null asymmetricity
    null_asymm_aw = []
    for off, p1, p2 in zip(null_offspring_aw, null_p1_aw, null_p2_aw):
        asym, _ = calculate_vector_asymmetricity(p1, p2, off)
        null_asymm_aw.append(asym)
    null_asymm_aw = np.array(null_asymm_aw)

    print(f"Abundance-Weighted Null: mean={np.nanmean(null_asymm_aw):.3f}, "
          f"median={np.nanmedian(null_asymm_aw):.3f}, std={np.nanstd(null_asymm_aw):.3f}")

    # =========================================================================
    # STEP 4: Generate Shuffled Abundance Null Model
    # =========================================================================
    print("\n" + "-" * 50)
    print("STEP 4: Generating Shuffled Abundance null model...")
    print("-" * 50)

    null_offspring_sh, null_p1_sh, null_p2_sh = generate_shuffled_abundance_null_batch(
        parent1_list, parent2_list, offspring_list,
        n_permutations=n_permutations
    )

    # Calculate null asymmetricity
    null_asymm_sh = []
    for off, p1, p2 in zip(null_offspring_sh, null_p1_sh, null_p2_sh):
        asym, _ = calculate_vector_asymmetricity(p1, p2, off)
        null_asymm_sh.append(asym)
    null_asymm_sh = np.array(null_asymm_sh)

    print(f"Shuffled Null: mean={np.nanmean(null_asymm_sh):.3f}, "
          f"median={np.nanmedian(null_asymm_sh):.3f}, std={np.nanstd(null_asymm_sh):.3f}")

    # =========================================================================
    # STEP 5: Statistical comparisons
    # =========================================================================
    print("\n" + "-" * 50)
    print("STEP 5: Statistical comparisons...")
    print("-" * 50)

    comparison_stats = {}

    # Compare with Abundance-Weighted null
    comparison_stats['abundance_weighted'] = compare_distributions(
        exp_asymm, null_asymm_aw, "Exp vs Abundance-Weighted"
    )

    print("\nAbundance-Weighted Null Model Comparison:")
    aw_stats = comparison_stats['abundance_weighted']
    print(f"  Experimental mean: {aw_stats['exp_mean']:.3f}")
    print(f"  Null mean: {aw_stats['null_mean']:.3f}")
    print(f"  Mann-Whitney U p-value: {aw_stats['mann_whitney_u']['p_value']:.2e} "
          f"({'SIGNIFICANT' if aw_stats['mann_whitney_u']['significant'] else 'not significant'})")
    print(f"  K-S test p-value: {aw_stats['kolmogorov_smirnov']['p_value']:.2e}")
    print(f"  Effect size (Cohen's d): {aw_stats['effect_size']['cohens_d']:.3f} "
          f"({aw_stats['effect_size']['interpretation']})")

    # Compare with Shuffled null
    comparison_stats['shuffled'] = compare_distributions(
        exp_asymm, null_asymm_sh, "Exp vs Shuffled"
    )

    print("\nShuffled Abundance Null Model Comparison:")
    sh_stats = comparison_stats['shuffled']
    print(f"  Experimental mean: {sh_stats['exp_mean']:.3f}")
    print(f"  Null mean: {sh_stats['null_mean']:.3f}")
    print(f"  Mann-Whitney U p-value: {sh_stats['mann_whitney_u']['p_value']:.2e} "
          f"({'SIGNIFICANT' if sh_stats['mann_whitney_u']['significant'] else 'not significant'})")
    print(f"  K-S test p-value: {sh_stats['kolmogorov_smirnov']['p_value']:.2e}")
    print(f"  Effect size (Cohen's d): {sh_stats['effect_size']['cohens_d']:.3f} "
          f"({sh_stats['effect_size']['interpretation']})")

    # =========================================================================
    # STEP 6: Correlation analysis
    # =========================================================================
    print("\n" + "-" * 50)
    print("STEP 6: Correlation between skewness and asymmetricity...")
    print("-" * 50)

    correlation_results = analyze_skewness_asymmetricity_correlation(
        exp_asymm, skewness_metrics
    )

    print("\nCorrelation Analysis (Parental Skewness vs Offspring Asymmetricity):")
    for metric_name, corr in correlation_results.items():
        print(f"\n  {metric_name}:")
        print(f"    Pearson r: {corr['pearson_r']:.3f} (p = {corr['pearson_p']:.2e})")
        print(f"    Spearman r: {corr['spearman_r']:.3f} (p = {corr['spearman_p']:.2e})")
        if corr['significant']:
            print(f"    ** SIGNIFICANT correlation **")

    # =========================================================================
    # STEP 7: Generate figures
    # =========================================================================
    print("\n" + "-" * 50)
    print("STEP 7: Generating figures...")
    print("-" * 50)

    null_results = {
        'abundance_weighted': null_asymm_aw,
        'shuffled': null_asymm_sh
    }

    # Main comparison figure
    plot_asymmetricity_comparison(
        exp_asymm, null_results, comparison_stats,
        save_path=os.path.join(save_dir, f"asymmetricity_comparison_{data_type}.png")
    )

    # By-condition plots
    plot_asymmetricity_by_condition(
        exp_asymm, null_asymm_aw, metadata['nutrient_conditions'],
        "Abundance-Weighted Null",
        save_path=os.path.join(save_dir, f"asymmetricity_by_condition_aw_{data_type}.png")
    )

    plot_asymmetricity_by_condition(
        exp_asymm, null_asymm_sh, metadata['nutrient_conditions'],
        "Shuffled Abundance Null",
        save_path=os.path.join(save_dir, f"asymmetricity_by_condition_sh_{data_type}.png")
    )

    # Correlation plots
    plot_skewness_correlation(
        exp_asymm, skewness_metrics, correlation_results,
        save_path=os.path.join(save_dir, f"skewness_correlation_{data_type}.png")
    )

    # Distribution histograms
    plot_distribution_histograms(
        exp_asymm, null_results,
        save_path=os.path.join(save_dir, f"distribution_histograms_{data_type}.png")
    )

    # Summary figure
    create_summary_figure(
        exp_asymm, null_results, comparison_stats,
        skewness_metrics, correlation_results,
        save_path=os.path.join(save_dir, f"summary_figure_{data_type}.png")
    )

    # =========================================================================
    # STEP 8: Save results to JSON
    # =========================================================================
    print("\n" + "-" * 50)
    print("STEP 8: Saving results...")
    print("-" * 50)

    # Prepare results for JSON (convert numpy types)
    def convert_to_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(v) for v in obj]
        return obj

    results = {
        'data_type': data_type,
        'n_events': len(offspring_list),
        'n_permutations': n_permutations,
        'experimental': {
            'asymmetricity_mean': float(np.nanmean(exp_asymm)),
            'asymmetricity_median': float(np.nanmedian(exp_asymm)),
            'asymmetricity_std': float(np.nanstd(exp_asymm)),
            'mean_gini': float(np.nanmean(skewness_metrics['mean_gini'])),
            'mean_retention_rate': float(mean_retention)
        },
        'null_models': {
            'abundance_weighted': {
                'mean': float(np.nanmean(null_asymm_aw)),
                'median': float(np.nanmedian(null_asymm_aw)),
                'std': float(np.nanstd(null_asymm_aw))
            },
            'shuffled': {
                'mean': float(np.nanmean(null_asymm_sh)),
                'median': float(np.nanmedian(null_asymm_sh)),
                'std': float(np.nanstd(null_asymm_sh))
            }
        },
        'statistical_comparisons': convert_to_serializable(comparison_stats),
        'correlations': convert_to_serializable(correlation_results)
    }

    results_path = os.path.join(save_dir, f"analysis_results_{data_type}.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {results_path}")

    # =========================================================================
    # STEP 9: Print conclusions
    # =========================================================================
    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)

    # Interpretation for Abundance-Weighted Null
    print("\n1. ABUNDANCE-WEIGHTED RANDOM SELECTION NULL MODEL:")
    aw_sig = comparison_stats['abundance_weighted']['mann_whitney_u']['significant']
    aw_diff = aw_stats['exp_mean'] - aw_stats['null_mean']

    if aw_sig:
        if aw_diff > 0:
            print("   -> Experimental asymmetricity is HIGHER than expected from skewness alone")
            print("   -> CONCLUSION: Skewed abundances do NOT fully explain the observed asymmetricity")
            print("   -> Ecological factors (competition, niche differences) likely contribute")
        else:
            print("   -> Experimental asymmetricity is LOWER than expected from skewness alone")
            print("   -> CONCLUSION: Real outcomes are more symmetric than predicted by abundance skewness")
    else:
        print("   -> No significant difference between experimental and null")
        print("   -> CONCLUSION: Skewed abundances MAY explain the observed asymmetricity pattern")

    # Interpretation for Shuffled Null
    print("\n2. SHUFFLED ABUNDANCE NULL MODEL:")
    sh_sig = comparison_stats['shuffled']['mann_whitney_u']['significant']

    if sh_sig:
        print("   -> Shuffling parental abundances significantly changes asymmetricity")
        print("   -> CONCLUSION: Specific species having high abundance MATTERS for asymmetricity")
        print("   -> Identity-dependent effects (which species is dominant) are important")
    else:
        print("   -> Shuffling parental abundances does NOT significantly change asymmetricity")
        print("   -> CONCLUSION: Asymmetricity is not sensitive to which specific species are dominant")

    # Correlation interpretation
    print("\n3. SKEWNESS-ASYMMETRICITY CORRELATION:")
    gini_corr = correlation_results.get('gini_difference', {})
    if gini_corr and gini_corr.get('significant', False):
        r = gini_corr['pearson_r']
        print(f"   -> Gini difference correlates with asymmetricity (r = {r:.3f})")
        if r > 0:
            print("   -> CONCLUSION: Greater parental inequality difference predicts higher asymmetricity")
        else:
            print("   -> CONCLUSION: Greater parental inequality difference predicts lower asymmetricity")
    else:
        print("   -> No significant correlation between Gini difference and asymmetricity")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run skewness analysis for coalescence asymmetricity')
    parser.add_argument('--data', type=str, default='synthetic',
                       choices=['synthetic', 'natural', 'both'],
                       help='Data type to analyze')
    parser.add_argument('--permutations', type=int, default=1000,
                       help='Number of null model permutations')
    parser.add_argument('--output', type=str, default=None,
                       help='Output directory for results')

    args = parser.parse_args()

    results = run_complete_analysis(
        data_type=args.data,
        n_permutations=args.permutations,
        save_dir=args.output
    )
