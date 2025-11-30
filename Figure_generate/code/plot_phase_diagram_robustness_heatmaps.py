"""
plot_phase_diagram_robustness_heatmaps.py

Purpose: Generate vector heatmaps (u, v) for different distance metrics
Key features:
- Creates polarized plots showing (u, v) coordinates for each metric
- Uses only MN (Medium Nutrient) condition with all pool sizes (6, 12, 24) merged
- Tests multiple distance/similarity metrics: Vector Decomposition, Euclidean, Bray-Curtis, Jensen-Shannon, Jaccard
- Shows how different metrics map communities into (u, v) space

Output:
- Figure/PhaseDiagram_robustness_to_metrics/Fig_robustness_heatmap_MN_merged.svg
"""

from common_setup import *
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import jensenshannon, euclidean, braycurtis
from collections import OrderedDict


def normalize(v):
    """Normalize a vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """Original vector decomposition metric."""
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
    """Jaccard-based metric."""
    threshold = 1e-4
    c1_binary = (c1 > threshold).astype(float)
    c2_binary = (c2 > threshold).astype(float)
    c_mix_binary = (c_mix > threshold).astype(float)
    orthogonal_binary = (orthogonal_vec > threshold).astype(float)

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
    """Jensen-Shannon divergence-based metric."""
    c1_norm = np.array(c1) / (np.sum(c1) + 1e-10)
    c2_norm = np.array(c2) / (np.sum(c2) + 1e-10)
    c_mix_norm = np.array(c_mix) / (np.sum(c_mix) + 1e-10)
    orth_positive = np.maximum(orthogonal_vec, 0)
    orth_norm = orth_positive / (np.sum(orth_positive) + 1e-10)

    js_c1 = jensenshannon(c_mix_norm, c1_norm)
    js_c2 = jensenshannon(c_mix_norm, c2_norm)
    js_orth = jensenshannon(c_mix_norm, orth_norm)

    sim_to_c1 = max(0, 1 - js_c1)
    sim_to_c2 = max(0, 1 - js_c2)
    sim_to_orth = max(0, 1 - js_orth)

    norm = np.sqrt(sim_to_c1**2 + sim_to_c2**2 + sim_to_orth**2)
    if norm > 0:
        u = sim_to_c1 / norm
        v = sim_to_c2 / norm
        k = sim_to_orth / norm
    else:
        u, v, k = 0, 0, 0

    return u, v, k


def metric_BrayCurtis(c1, c2, c_mix, orthogonal_vec):
    """Bray-Curtis dissimilarity-based metric."""
    c1_arr = np.array(c1)
    c2_arr = np.array(c2)
    c_mix_arr = np.array(c_mix)
    orth_arr = np.array(orthogonal_vec)

    bc_c1 = braycurtis(c_mix_arr, c1_arr)
    bc_c2 = braycurtis(c_mix_arr, c2_arr)
    bc_orth = braycurtis(c_mix_arr, orth_arr)

    sim_to_c1 = max(0, 1 - bc_c1)
    sim_to_c2 = max(0, 1 - bc_c2)
    sim_to_orth = max(0, 1 - bc_orth)

    norm = np.sqrt(sim_to_c1**2 + sim_to_c2**2 + sim_to_orth**2)
    if norm > 0:
        u = sim_to_c1 / norm
        v = sim_to_c2 / norm
        k = sim_to_orth / norm
    else:
        u, v, k = 0, 0, 0

    return u, v, k


def metric_Euclidean(c1, c2, c_mix, orthogonal_vec):
    """Euclidean distance-based metric."""
    c1_norm = normalize(np.array(c1))
    c2_norm = normalize(np.array(c2))
    c_mix_norm = normalize(np.array(c_mix))
    orth_norm = normalize(np.array(orthogonal_vec))

    dist_c1 = euclidean(c_mix_norm, c1_norm)
    dist_c2 = euclidean(c_mix_norm, c2_norm)
    dist_orth = euclidean(c_mix_norm, orth_norm)

    max_dist = np.sqrt(2)
    sim_to_c1 = max(0, 1 - dist_c1 / max_dist)
    sim_to_c2 = max(0, 1 - dist_c2 / max_dist)
    sim_to_orth = max(0, 1 - dist_orth / max_dist)

    norm = np.sqrt(sim_to_c1**2 + sim_to_c2**2 + sim_to_orth**2)
    if norm > 0:
        u = sim_to_c1 / norm
        v = sim_to_c2 / norm
        k = sim_to_orth / norm
    else:
        u, v, k = 0, 0, 0

    return u, v, k


def collect_uv_data(metric_func, metric_name):
    """Collect (u, v) coordinates for a specific metric."""
    u_values = []
    v_values = []

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
                    if metric_name == 'Vector Decomposition':
                        u, v, k, _ = metric_func(c_1, c_2, c_mix)
                    else:
                        _, _, _, orthogonal_vec = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                        u, v, k = metric_func(c_1, c_2, c_mix, orthogonal_vec)

                    u_values.append(u)
                    v_values.append(v)
                except Exception as e:
                    continue

    return u_values, v_values


def create_heatmap_comparison(all_uv_data, output_dir):
    """Create combined heatmap showing (u, v) for all metrics."""
    mm = 1 / 25.4
    fig, axes = plt.subplots(2, 3, figsize=(180*mm, 120*mm), facecolor='w')
    axes = axes.flatten()

    for idx, (metric_name, uv_data) in enumerate(all_uv_data.items()):
        ax = axes[idx]
        u_values, v_values = uv_data

        # Plot data points (using color #802000 to match experimental plots)
        ax.scatter(u_values, v_values, s=25, color='#802000', alpha=0.7,
                  linewidths=0, edgecolors='none')
        ax.scatter(v_values, u_values, s=25, color='#808080', alpha=0.2,
                  linewidths=0, edgecolors='none')

        # Define the grid and contours
        x = np.linspace(-0.15, 1.2, 500)
        y = np.linspace(-0.15, 1.2, 500)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(abs(X**2 + Y**2))

        ax.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                  alpha=0.2, linewidths=0.5)

        # Add auxiliary lines
        ax.axhline(0, color='k', linestyle='--', linewidth=0.8)
        ax.axvline(0, color='k', linestyle='--', linewidth=0.8)

        # Set plot limits and labels
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xticks([0, 0.5, 1.0])
        ax.set_yticks([0, 0.5, 1.0])

        # Remove the outer box (spines)
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Add title with sample count
        n_samples = len(u_values)
        ax.set_title(f'{metric_name}\nn = {n_samples}', fontsize=10, fontweight='bold')

    # Hide unused subplot
    if len(all_uv_data) < len(axes):
        for idx in range(len(all_uv_data), len(axes)):
            axes[idx].axis('off')

    plt.tight_layout()
    return fig


def main():
    """Main function to generate heatmaps."""

    print("="*70)
    print("Generating Vector Heatmaps for Metric Robustness Analysis")
    print("="*70)
    print(f"Condition: MN Medium, All Pool Sizes (6, 12, 24) Merged")
    print()

    # Create output directory
    output_dir = Path("Figure/PhaseDiagram_robustness_to_metrics")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define metrics (ordered as requested)
    metrics = OrderedDict([
        ('Vector Decomposition', metric_VectorDecomposition_onlyPositive),
        ('Euclidean', metric_Euclidean),
        ('Bray-Curtis', metric_BrayCurtis),
        ('Jensen-Shannon', metric_JensenShannon),
        ('Jaccard', metric_Jaccard)
    ])

    # Collect (u, v) data for each metric
    all_uv_data = OrderedDict()

    for metric_name, metric_func in metrics.items():
        print(f"Collecting (u, v) data for {metric_name}...")
        u_values, v_values = collect_uv_data(metric_func, metric_name)
        all_uv_data[metric_name] = (u_values, v_values)
        print(f"  Collected {len(u_values)} data points")

    # Create heatmap comparison
    print("\nGenerating heatmap comparison plot...")
    fig = create_heatmap_comparison(all_uv_data, output_dir)

    output_filename = output_dir / "Fig_robustness_heatmap_MN_merged.svg"
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Created: {output_filename}")
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
