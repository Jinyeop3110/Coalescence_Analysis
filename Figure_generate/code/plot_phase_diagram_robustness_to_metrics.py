"""
plot_phase_diagram_robustness_to_metrics.py

Purpose: Test robustness of coalescence outcome classification to different distance metrics
Key features:
- Uses only MN (Medium Nutrient) condition with all pool sizes (6, 12, 24) merged
- Tests multiple distance/similarity metrics: Vector Decomposition, Jaccard, Jensen-Shannon, Bray-Curtis, Euclidean
- Generates pie plots for each metric showing outcome distributions
- Compares how metric choice affects classification into Dominance, Mixing, and Restructuring

Output:
- Figure/PhaseDiagram_robustness_to_metrics/Fig_robustness_*_MN_merged.svg (one per metric)
- Figure/PhaseDiagram_robustness_to_metrics/Fig_robustness_comparison_MN_merged.svg (combined comparison)
"""

from common_setup import *
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from COLORMAP import get_phase_diagram_colors
from scipy.spatial.distance import jensenshannon, euclidean, braycurtis
from scipy.stats import entropy


def normalize(v):
    """Normalize a vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """
    Original vector decomposition metric.
    Returns u_component, v_component, restructuring_component, and orthogonal_vector.
    """
    u = normalize(u)
    v = normalize(v)
    m = normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))

    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)

    # Calculate orthogonal component (restructured community vector)
    orthogonal_vec = m - (e12[0]*u) - (e12[1]*v)
    x3 = np.linalg.norm(orthogonal_vec)
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2 + 1e-10))

    return convert*x1, convert*x2, x3, orthogonal_vec


def metric_Jaccard(c1, c2, c_mix, orthogonal_vec):
    """
    Jaccard-based metric.
    Measures presence/absence similarity.
    Uses orthogonal vector from Vector Decomposition to calculate k.
    Returns: similarity to c1, similarity to c2, similarity to orthogonal component.
    """
    threshold = 1e-4
    c1_binary = (c1 > threshold).astype(float)
    c2_binary = (c2 > threshold).astype(float)
    c_mix_binary = (c_mix > threshold).astype(float)
    orthogonal_binary = (orthogonal_vec > threshold).astype(float)

    # Jaccard similarity
    def jaccard_similarity(a, b):
        intersection = np.sum(np.minimum(a, b))
        union = np.sum(np.maximum(a, b))
        if union == 0:
            return 0
        return intersection / union

    sim_to_c1 = jaccard_similarity(c_mix_binary, c1_binary)
    sim_to_c2 = jaccard_similarity(c_mix_binary, c2_binary)
    sim_to_orth = jaccard_similarity(c_mix_binary, orthogonal_binary)

    # Normalize so that u^2 + v^2 + k^2 = 1
    norm = np.sqrt(sim_to_c1**2 + sim_to_c2**2 + sim_to_orth**2)
    if norm > 0:
        u = sim_to_c1 / norm
        v = sim_to_c2 / norm
        k = sim_to_orth / norm
    else:
        u, v, k = 0, 0, 0

    return u, v, k


def metric_JensenShannon(c1, c2, c_mix, orthogonal_vec):
    """
    Jensen-Shannon divergence-based metric.
    Measures information-theoretic distance.
    Uses orthogonal vector from Vector Decomposition to calculate k.
    Returns: inverse divergence to c1, inverse divergence to c2, divergence to orthogonal component.
    """
    # Normalize to probability distributions
    # For Jensen-Shannon, we need non-negative values, so apply max(orthogonal_vec, 0)
    c1_norm = np.array(c1) / (np.sum(c1) + 1e-10)
    c2_norm = np.array(c2) / (np.sum(c2) + 1e-10)
    c_mix_norm = np.array(c_mix) / (np.sum(c_mix) + 1e-10)
    orth_positive = np.maximum(orthogonal_vec, 0)
    orth_norm = orth_positive / (np.sum(orth_positive) + 1e-10)

    # Jensen-Shannon divergence (returns distance, so we convert to similarity)
    js_c1 = jensenshannon(c_mix_norm, c1_norm)
    js_c2 = jensenshannon(c_mix_norm, c2_norm)
    js_orth = jensenshannon(c_mix_norm, orth_norm)

    # Convert to similarities (1 - distance, bounded)
    sim_to_c1 = max(0, 1 - js_c1)
    sim_to_c2 = max(0, 1 - js_c2)
    sim_to_orth = max(0, 1 - js_orth)

    # Normalize so that u^2 + v^2 + k^2 = 1
    norm = np.sqrt(sim_to_c1**2 + sim_to_c2**2 + sim_to_orth**2)
    if norm > 0:
        u = sim_to_c1 / norm
        v = sim_to_c2 / norm
        k = sim_to_orth / norm
    else:
        u, v, k = 0, 0, 0

    return u, v, k


def metric_BrayCurtis(c1, c2, c_mix, orthogonal_vec):
    """
    Bray-Curtis dissimilarity-based metric.
    Ecological distance metric sensitive to abundance differences.
    Uses orthogonal vector from Vector Decomposition to calculate k.
    Returns: inverse distance to c1, inverse distance to c2, distance to orthogonal component.
    """
    c1_arr = np.array(c1)
    c2_arr = np.array(c2)
    c_mix_arr = np.array(c_mix)
    orth_arr = np.array(orthogonal_vec)

    # Bray-Curtis distance
    bc_c1 = braycurtis(c_mix_arr, c1_arr)
    bc_c2 = braycurtis(c_mix_arr, c2_arr)
    bc_orth = braycurtis(c_mix_arr, orth_arr)

    # Convert to similarities
    sim_to_c1 = max(0, 1 - bc_c1)
    sim_to_c2 = max(0, 1 - bc_c2)
    sim_to_orth = max(0, 1 - bc_orth)

    # Normalize so that u^2 + v^2 + k^2 = 1
    norm = np.sqrt(sim_to_c1**2 + sim_to_c2**2 + sim_to_orth**2)
    if norm > 0:
        u = sim_to_c1 / norm
        v = sim_to_c2 / norm
        k = sim_to_orth / norm
    else:
        u, v, k = 0, 0, 0

    return u, v, k


def metric_Euclidean(c1, c2, c_mix, orthogonal_vec):
    """
    Euclidean distance-based metric.
    Simple L2 distance in abundance space.
    Uses orthogonal vector from Vector Decomposition to calculate k.
    Returns: inverse distance to c1, inverse distance to c2, distance to orthogonal component.
    """
    c1_norm = normalize(np.array(c1))
    c2_norm = normalize(np.array(c2))
    c_mix_norm = normalize(np.array(c_mix))
    orth_norm = normalize(np.array(orthogonal_vec))

    # Euclidean distances
    dist_c1 = euclidean(c_mix_norm, c1_norm)
    dist_c2 = euclidean(c_mix_norm, c2_norm)
    dist_orth = euclidean(c_mix_norm, orth_norm)

    # Convert distances to similarities (inverse with normalization)
    max_dist = np.sqrt(2)  # Max possible distance for normalized vectors
    sim_to_c1 = max(0, 1 - dist_c1 / max_dist)
    sim_to_c2 = max(0, 1 - dist_c2 / max_dist)
    sim_to_orth = max(0, 1 - dist_orth / max_dist)

    # Normalize so that u^2 + v^2 + k^2 = 1
    norm = np.sqrt(sim_to_c1**2 + sim_to_c2**2 + sim_to_orth**2)
    if norm > 0:
        u = sim_to_c1 / norm
        v = sim_to_c2 / norm
        k = sim_to_orth / norm
    else:
        u, v, k = 0, 0, 0

    return u, v, k


def classify_outcomes_generic(u_values, v_values, k_values):
    """
    Generic classification for any metric that returns (u, v, k) triplets.
    Uses the same classification logic as original phase diagrams.

    Returns counts of:
    - Dominance (class 0)
    - Mixing (class 1)
    - Restructuring (class 2)
    """
    dominance_count = 0
    mixing_count = 0
    restructuring_count = 0

    for u, v, k in zip(u_values, v_values, k_values):
        # Same classification logic as common_setup.py
        x = np.sqrt(u**2 + v**2)
        y = np.abs(np.abs(np.arctan(u / (v + 1e-8))) - np.pi/4) / (np.pi/4)

        # characterize_case logic
        if (x**2 > 0.5) * (y > 0.5):
            dominance_count += 1  # Class 0
        elif (x**2 > 0.5) * (y < 0.5):
            mixing_count += 1     # Class 1
        elif (x**2 < 0.5):
            restructuring_count += 1  # Class 2

    return dominance_count, mixing_count, restructuring_count


def analyze_with_metric(metric_func, metric_name):
    """
    Analyze coalescence data using a specific metric.

    Parameters:
    -----------
    metric_func : function
        Function that takes (c1, c2, c_mix) and returns (u, v, k)
    metric_name : str
        Name of the metric for display

    Returns:
    --------
    dict with keys 'Dominance', 'Mixing', 'Restructuring'
    """
    print(f"  Analyzing with {metric_name} metric...")

    data1_combined = []
    data2_combined = []
    data3_combined = []

    # Use MN medium with all pool sizes (6, 12, 24) merged
    nutrient_level = 'MN'
    pool_sizes = ['6', '12', '24']

    for pool_size in pool_sizes:
        type_name = f'{nutrient_level}_{pool_size}'

        if type_name in Syn_Coal_IDX:
            IDX_list = Syn_Coal_IDX[type_name]
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX'] == x) for x in IDX_list])
            idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x) for x in idx_1])
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX'] == x) for x in IDX_list])
            idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x) for x in idx_2])
            idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x) for x in IDX_list])

            for i in range(len(idx)):
                c_mix = np.array(Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:])
                c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)

                try:
                    # First, get orthogonal vector from Vector Decomposition
                    if metric_name == 'Vector Decomposition':
                        u, v, k, _ = metric_func(c_1, c_2, c_mix)
                    else:
                        # For alternative metrics, first compute orthogonal vector
                        _, _, _, orthogonal_vec = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                        u, v, k = metric_func(c_1, c_2, c_mix, orthogonal_vec)

                    data1_combined.append(u)
                    data2_combined.append(v)
                    data3_combined.append(k)
                except Exception as e:
                    print(f"    Warning: Error computing metric for pool size {pool_size}, sample {i}: {e}")
                    continue

    # Classify outcomes
    dominance, mixing, restructuring = classify_outcomes_generic(
        data1_combined, data2_combined, data3_combined
    )

    return {
        'Dominance': dominance,
        'Mixing': mixing,
        'Restructuring': restructuring,
        'u_values': data1_combined,
        'v_values': data2_combined,
        'k_values': data3_combined
    }


def create_individual_pie_plot(results, metric_name, output_dir):
    """Create individual pie plot for a single metric."""
    fig, ax = plt.subplots(figsize=(3, 3))
    colors = get_phase_diagram_colors()

    values = [results['Dominance'], results['Mixing'], results['Restructuring']]
    labels = ['Dominance', 'Mixing', 'Restructuring']

    total = sum(values)

    # Check if we have any data
    if total == 0:
        print(f"  ⚠ Warning: No valid data for {metric_name} metric, skipping plot")
        plt.close()
        return

    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,
        colors=colors,
        autopct=lambda pct: f'{int(pct*total/100)} / {total}' if pct > 0 else '',
        startangle=90,
        pctdistance=0.7
    )

    # Adjust appearance
    for wedge in wedges:
        wedge.set_alpha(0.85)

    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(16)
        autotext.set_fontweight('bold')

    ax.set_title(f'{metric_name}\nMN Medium (All Pool Sizes)',
                 fontsize=14, fontweight='bold', pad=20)

    # Add total count
    ax.text(0, -1.2, f'n = {total}', ha='center', fontsize=10)

    # Save
    output_filename = output_dir / f"Fig_robustness_{metric_name.replace(' ', '_')}_MN_merged.svg"
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_filename}")

    # Print statistics
    print(f"    Dominance: {results['Dominance']} ({results['Dominance']/total*100:.1f}%)")
    print(f"    Mixing: {results['Mixing']} ({results['Mixing']/total*100:.1f}%)")
    print(f"    Restructuring: {results['Restructuring']} ({results['Restructuring']/total*100:.1f}%)")


def create_comparison_plot(all_results, output_dir):
    """Create combined comparison plot showing all metrics."""
    n_metrics = len(all_results)
    fig, axes = plt.subplots(2, 3, figsize=(9, 6))
    axes = axes.flatten()

    colors = get_phase_diagram_colors()

    for idx, (metric_name, results) in enumerate(all_results.items()):
        ax = axes[idx]

        values = [results['Dominance'], results['Mixing'], results['Restructuring']]
        total = sum(values)

        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,
            colors=colors,
            autopct=lambda pct: f'{int(pct*total/100)}' if pct > 0 else '',
            startangle=90,
            pctdistance=0.7
        )

        for wedge in wedges:
            wedge.set_alpha(0.85)

        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')

        ax.set_title(f'{metric_name}\nn = {total}', fontsize=12, fontweight='bold', pad=10)

    # Hide unused subplot
    if n_metrics < len(axes):
        for idx in range(n_metrics, len(axes)):
            axes[idx].axis('off')

    plt.tight_layout()

    # Save
    output_filename = output_dir / "Fig_robustness_comparison_MN_merged.svg"
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n✓ Created comparison plot: {output_filename}")


def main():
    """Main function to test robustness to different metrics."""

    print("="*70)
    print("Testing Robustness of Coalescence Classification to Metric Choice")
    print("="*70)
    print(f"Condition: MN Medium, All Pool Sizes (6, 12, 24) Merged")
    print()

    # Create output directory
    output_dir = Path("Figure/PhaseDiagram_robustness_to_metrics")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define metrics to test (ordered as requested)
    from collections import OrderedDict
    metrics = OrderedDict([
        ('Vector Decomposition', metric_VectorDecomposition_onlyPositive),
        ('Euclidean', metric_Euclidean),
        ('Bray-Curtis', metric_BrayCurtis),
        ('Jensen-Shannon', metric_JensenShannon),
        ('Jaccard', metric_Jaccard)
    ])

    # Analyze with each metric
    all_results = {}

    for metric_name, metric_func in metrics.items():
        print(f"\n{metric_name} Metric:")
        print("-" * 50)
        results = analyze_with_metric(metric_func, metric_name)
        all_results[metric_name] = results

        # Create individual plot
        create_individual_pie_plot(results, metric_name, output_dir)

    # Create comparison plot
    create_comparison_plot(all_results, output_dir)

    # Summary table
    print("\n" + "="*70)
    print("SUMMARY: Outcome Distribution Across Metrics")
    print("="*70)
    print(f"{'Metric':<25} {'Dominance':<12} {'Mixing':<12} {'Restructuring':<15}")
    print("-" * 70)

    for metric_name, results in all_results.items():
        total = results['Dominance'] + results['Mixing'] + results['Restructuring']
        dom_pct = results['Dominance'] / total * 100
        mix_pct = results['Mixing'] / total * 100
        rest_pct = results['Restructuring'] / total * 100

        print(f"{metric_name:<25} {dom_pct:>5.1f}% ({results['Dominance']:>2}) "
              f"{mix_pct:>5.1f}% ({results['Mixing']:>2}) "
              f"{rest_pct:>5.1f}% ({results['Restructuring']:>2})")

    print("="*70)
    print("\nAnalysis complete! All figures saved to:")
    print(f"  {output_dir}/")
    print()


if __name__ == "__main__":
    main()
