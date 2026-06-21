#!/usr/bin/env python3
"""
plot_stacked_bar_class_fractions.py

Purpose: Generate stacked bar plots for class fractions (Dominance, Mixture, Restructuring)
         replacing pie charts with a consistent format across all ablation/comparison figures.

Generates:
1. Fig S4: Sensitivity to metrics (5 bars: Vector Decomp, Euclidean, Bray-Curtis, Jensen-Shannon, Jaccard)
2. Fig S12: Species number ablation (6 bars: 4, 6, 9, 12, 24, 48 species per community)
3. Fig S25: Assembly effect simulation (5 bars per row for interaction strengths)
4. Fig S26: Assembly effect experimental (3 bars per row for nutrient conditions)

Format: Vertical stacked bars showing percentages with (count/total) annotations
"""

from common_setup import *
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from COLORMAP import get_phase_diagram_colors
from scipy.spatial.distance import jensenshannon, euclidean, braycurtis
import json
import pickle

# Create output directory
output_dir = Path("Figure/StackedBar_ClassFractions")
output_dir.mkdir(parents=True, exist_ok=True)

# Get consistent colors for Dominance, Mixture, Restructuring
COLORS = get_phase_diagram_colors()


def create_stacked_bar_plot(data_dict, labels, title, output_filename,
                            figsize=(8, 5), ylabel="Fraction (%)",
                            show_counts=True, legend_loc='upper right'):
    """
    Create a stacked bar plot for class fractions.

    Parameters:
    -----------
    data_dict : dict
        Keys are bar labels, values are dicts with 'Dominance', 'Mixing', 'Restructuring' counts
    labels : list
        X-axis labels for bars
    title : str
        Plot title
    output_filename : str or Path
        Output file path
    figsize : tuple
        Figure size
    ylabel : str
        Y-axis label
    show_counts : bool
        Whether to show (count/total) annotations
    legend_loc : str
        Legend location
    """
    fig, ax = plt.subplots(figsize=figsize)

    n_bars = len(labels)
    x = np.arange(n_bars)
    bar_width = 0.45  # Narrower bars

    # Calculate percentages
    cls_pcts = []
    mix_pcts = []
    rest_pcts = []
    totals = []
    counts = {'Dominance': [], 'Mixture': [], 'Restructuring': []}

    for label in labels:
        data = data_dict[label]
        total = data['Dominance'] + data['Mixing'] + data['Restructuring']
        totals.append(total)

        if total > 0:
            cls_pcts.append(data['Dominance'] / total * 100)
            mix_pcts.append(data['Mixing'] / total * 100)
            rest_pcts.append(data['Restructuring'] / total * 100)
        else:
            cls_pcts.append(0)
            mix_pcts.append(0)
            rest_pcts.append(0)

        counts['Dominance'].append(data['Dominance'])
        counts['Mixture'].append(data['Mixing'])
        counts['Restructuring'].append(data['Restructuring'])

    # Create stacked bars
    bars_cls = ax.bar(x, cls_pcts, bar_width, label='Dominance', color=COLORS[0], edgecolor='white', linewidth=0.5)
    bars_mix = ax.bar(x, mix_pcts, bar_width, bottom=cls_pcts, label='Mixture', color=COLORS[1], edgecolor='white', linewidth=0.5)
    bars_rest = ax.bar(x, rest_pcts, bar_width, bottom=np.array(cls_pcts) + np.array(mix_pcts),
                       label='Restructuring', color=COLORS[2], edgecolor='white', linewidth=0.5)

    # Add percentage and count annotations (fontsize x1.3, black text)
    annotation_fontsize = 10.4  # 8 * 1.3
    for i in range(n_bars):
        total = totals[i]
        if total == 0:
            continue

        # Dominance annotation (bottom section)
        if cls_pcts[i] > 8:  # Only show if section is large enough
            y_pos = cls_pcts[i] / 2
            if show_counts:
                text = f"{cls_pcts[i]:.0f}%\n({counts['Dominance'][i]}/{total})"
            else:
                text = f"{cls_pcts[i]:.0f}%"
            ax.text(x[i], y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, color='black')

        # Mixture annotation (middle section)
        if mix_pcts[i] > 8:
            y_pos = cls_pcts[i] + mix_pcts[i] / 2
            if show_counts:
                text = f"{mix_pcts[i]:.0f}%\n({counts['Mixture'][i]}/{total})"
            else:
                text = f"{mix_pcts[i]:.0f}%"
            ax.text(x[i], y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, color='black')

        # Restructuring annotation (top section)
        if rest_pcts[i] > 8:
            y_pos = cls_pcts[i] + mix_pcts[i] + rest_pcts[i] / 2
            if show_counts:
                text = f"{rest_pcts[i]:.0f}%\n({counts['Restructuring'][i]}/{total})"
            else:
                text = f"{rest_pcts[i]:.0f}%"
            ax.text(x[i], y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, color='black')

    # Formatting (fontsize x1.3)
    ax.set_ylabel(ylabel, fontsize=14.3)  # 11 * 1.3
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=13, rotation=0)  # 10 * 1.3
    ax.set_ylim(0, 100)
    ax.set_xlim(-0.5, n_bars - 0.5)

    # Add horizontal grid lines
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Title
    if title:
        ax.set_title(title, fontsize=15.6, pad=10)  # 12 * 1.3

    # Legend
    ax.legend(loc=legend_loc, frameon=True, fontsize=11.7)  # 9 * 1.3

    plt.tight_layout()

    # Save
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    fig.savefig(str(output_filename).replace('.svg', '.pdf'), format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_filename}")


def create_two_row_stacked_bar_plot(data_row1, data_row2, labels,
                                     row1_title, row2_title, main_title,
                                     output_filename, figsize=(10, 6)):
    """
    Create a two-row stacked bar plot (e.g., Coalescence vs Direct Assembly).

    Parameters:
    -----------
    data_row1, data_row2 : dict
        Keys are bar labels, values are dicts with 'Dominance', 'Mixing', 'Restructuring' counts
    labels : list
        X-axis labels for bars
    row1_title, row2_title : str
        Row labels
    main_title : str
        Main plot title
    output_filename : str or Path
        Output file path
    """
    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)

    n_bars = len(labels)
    x = np.arange(n_bars)
    bar_width = 0.45  # Narrower bars

    # Annotation fontsize x1.3
    annotation_fontsize = 9.1  # 7 * 1.3

    for ax_idx, (ax, data_dict, row_title) in enumerate([(axes[0], data_row1, row1_title),
                                                          (axes[1], data_row2, row2_title)]):
        # Calculate percentages
        cls_pcts = []
        mix_pcts = []
        rest_pcts = []
        totals = []
        counts = {'Dominance': [], 'Mixture': [], 'Restructuring': []}

        for label in labels:
            data = data_dict[label]
            total = data['Dominance'] + data['Mixing'] + data['Restructuring']
            totals.append(total)

            if total > 0:
                cls_pcts.append(data['Dominance'] / total * 100)
                mix_pcts.append(data['Mixing'] / total * 100)
                rest_pcts.append(data['Restructuring'] / total * 100)
            else:
                cls_pcts.append(0)
                mix_pcts.append(0)
                rest_pcts.append(0)

            counts['Dominance'].append(data['Dominance'])
            counts['Mixture'].append(data['Mixing'])
            counts['Restructuring'].append(data['Restructuring'])

        # Create stacked bars
        bars_cls = ax.bar(x, cls_pcts, bar_width, label='Dominance', color=COLORS[0], edgecolor='white', linewidth=0.5)
        bars_mix = ax.bar(x, mix_pcts, bar_width, bottom=cls_pcts, label='Mixture', color=COLORS[1], edgecolor='white', linewidth=0.5)
        bars_rest = ax.bar(x, rest_pcts, bar_width, bottom=np.array(cls_pcts) + np.array(mix_pcts),
                           label='Restructuring', color=COLORS[2], edgecolor='white', linewidth=0.5)

        # Add annotations (black text)
        for i in range(n_bars):
            total = totals[i]
            if total == 0:
                continue

            # Dominance annotation
            if cls_pcts[i] > 10:
                y_pos = cls_pcts[i] / 2
                text = f"{cls_pcts[i]:.0f}%\n({counts['Dominance'][i]}/{total})"
                ax.text(x[i], y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, color='black')

            # Mixture annotation
            if mix_pcts[i] > 10:
                y_pos = cls_pcts[i] + mix_pcts[i] / 2
                text = f"{mix_pcts[i]:.0f}%\n({counts['Mixture'][i]}/{total})"
                ax.text(x[i], y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, color='black')

            # Restructuring annotation
            if rest_pcts[i] > 10:
                y_pos = cls_pcts[i] + mix_pcts[i] + rest_pcts[i] / 2
                text = f"{rest_pcts[i]:.0f}%\n({counts['Restructuring'][i]}/{total})"
                ax.text(x[i], y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, color='black')

        # Formatting (fontsize x1.3)
        ax.set_ylabel(row_title, fontsize=14.3)  # 11 * 1.3
        ax.set_ylim(0, 100)
        ax.set_xlim(-0.5, n_bars - 0.5)
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Legend only for first row
        if ax_idx == 0:
            ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.0),
                      frameon=True, fontsize=11.7)  # 9 * 1.3

    # X-axis labels on bottom plot
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, fontsize=13)  # 10 * 1.3

    # Main title
    if main_title:
        fig.suptitle(main_title, fontsize=16.9, y=0.98)  # 13 * 1.3

    plt.tight_layout(rect=[0, 0, 0.88, 0.96])

    # Save
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    fig.savefig(str(output_filename).replace('.svg', '.pdf'), format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_filename}")


# =============================================================================
# Figure S4: Robustness to Metrics
# =============================================================================

def normalize(v):
    """Normalize a vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """Vector decomposition metric."""
    u = normalize(u)
    v = normalize(v)
    m = normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))

    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)

    orthogonal_vec = m - (e12[0]*u) - (e12[1]*v)
    x3 = np.linalg.norm(orthogonal_vec)
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2 + 1e-10))

    return convert*x1, convert*x2, x3, orthogonal_vec


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

    norm = np.sqrt(sim_to_c1**2 + sim_to_c2**2 + sim_to_orth**2)
    if norm > 0:
        u = sim_to_c1 / norm
        v = sim_to_c2 / norm
        k = sim_to_orth / norm
    else:
        u, v, k = 0, 0, 0

    return u, v, k


def classify_outcome(u, v, k):
    """Classify outcome into Dominance(0), Mixing(1), or Restructuring(2)."""
    x = np.sqrt(u**2 + v**2)
    y = np.abs(np.abs(np.arctan(u / (v + 1e-8))) - np.pi/4) / (np.pi/4)

    if (x**2 > 0.5) * (y > 0.5):
        return 0  # Dominance
    elif (x**2 > 0.5) * (y < 0.5):
        return 1  # Mixing
    elif (x**2 < 0.5):
        return 2  # Restructuring
    else:
        return 1  # Default to mixing


def generate_fig_s4_robustness():
    """Generate Fig S4: Robustness to different metrics."""
    print("\n" + "="*70)
    print("Generating Fig S4: Robustness to Metrics (Stacked Bar)")
    print("="*70)

    # Define metrics
    metrics = OrderedDict([
        ('Vector\nDecomp', metric_VectorDecomposition_onlyPositive),
        ('Euclidean', metric_Euclidean),
        ('Bray-\nCurtis', metric_BrayCurtis),
        ('Jensen-\nShannon', metric_JensenShannon),
        ('Jaccard', metric_Jaccard)
    ])

    results = {}

    for metric_name, metric_func in metrics.items():
        print(f"  Processing {metric_name.replace(chr(10), ' ')}...")

        data1_combined = []
        data2_combined = []
        data3_combined = []

        # Use MN medium with all pool sizes merged
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
                        if 'Vector' in metric_name:
                            u, v, k, _ = metric_func(c_1, c_2, c_mix)
                        else:
                            _, _, _, orthogonal_vec = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                            u, v, k = metric_func(c_1, c_2, c_mix, orthogonal_vec)

                        data1_combined.append(u)
                        data2_combined.append(v)
                        data3_combined.append(k)
                    except:
                        continue

        # Classify outcomes
        dominance = mixing = restructuring = 0
        for u, v, k in zip(data1_combined, data2_combined, data3_combined):
            outcome = classify_outcome(u, v, k)
            if outcome == 0:
                dominance += 1
            elif outcome == 1:
                mixing += 1
            else:
                restructuring += 1

        results[metric_name] = {
            'Dominance': dominance,
            'Mixing': mixing,
            'Restructuring': restructuring
        }

    # Create stacked bar plot
    labels = list(results.keys())
    output_file = output_dir / "Fig_S4_robustness_metrics_stacked_bar.svg"
    create_stacked_bar_plot(results, labels,
                           "Sensitivity of Classification to Metric Choice (Base Medium)",
                           output_file, figsize=(8, 5))

    return results


# =============================================================================
# Figure S12: Species Number Ablation
# =============================================================================

def generate_fig_s12_species_ablation():
    """Generate Fig S12: Species number ablation."""
    print("\n" + "="*70)
    print("Generating Fig S12: Species Number Ablation (Stacked Bar)")
    print("="*70)

    # Load simulation data for different species numbers
    # Data files are organized as: {n}percomm_ablation_species_number/Community_ablation_{n}percomm.json
    # Data structure: {mu_value: {rep_key: {sc_list: {c1, c2}, cc_list: {c1_c2}}}}
    species_numbers = [4, 6, 9, 12, 24, 48]
    interaction_strengths = [0.3, 0.6, 0.8]

    all_results = {}

    for mu in interaction_strengths:
        results = {}
        mu_str = f"{mu:.2f}"

        for n_species in species_numbers:
            # Correct file path
            data_file = Path(f"Simulation_Data/{n_species}percomm_ablation_species_number/Community_ablation_{n_species}percomm.json")

            if data_file.exists():
                with open(data_file, 'r') as f:
                    sim_data = json.load(f)

                dominance = mixing = restructuring = 0

                # Data is organized by mu value (as string key like "0.30")
                if mu_str in sim_data:
                    mu_data = sim_data[mu_str]
                    for rep_key, rep_data in mu_data.items():
                        sc_list = rep_data['sc_list']
                        cc_list = rep_data['cc_list']

                        # sc_list has keys like '0', '1', '2', '3'
                        # cc_list has keys like '0_1', '0_2', etc.
                        for cc_key, c_mix in cc_list.items():
                            # Parse the community pair indices
                            idx1, idx2 = cc_key.split('_')
                            c1 = np.array(sc_list[idx1])
                            c2 = np.array(sc_list[idx2])
                            c_mix = np.array(c_mix)

                            try:
                                u, v, k, _ = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)
                                outcome = classify_outcome(u, v, k)
                                if outcome == 0:
                                    dominance += 1
                                elif outcome == 1:
                                    mixing += 1
                                else:
                                    restructuring += 1
                            except:
                                continue
                else:
                    print(f"    Warning: μ={mu_str} not found in {data_file}")

                results[str(n_species)] = {
                    'Dominance': dominance,
                    'Mixing': mixing,
                    'Restructuring': restructuring
                }
                print(f"    {n_species} species, μ={mu}: Dominance={dominance}, Mixture={mixing}, Restructuring={restructuring}")
            else:
                print(f"    Warning: Data file not found: {data_file}")
                results[str(n_species)] = {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0}

        all_results[mu] = results

    # Create multi-panel figure (one panel per interaction strength)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

    labels = [str(n) for n in species_numbers]

    # Annotation fontsize x1.3
    annotation_fontsize = 7.8  # 6 * 1.3

    for ax_idx, (mu, results) in enumerate(all_results.items()):
        ax = axes[ax_idx]
        n_bars = len(labels)
        x = np.arange(n_bars)
        bar_width = 0.45  # Narrower bars

        cls_pcts = []
        mix_pcts = []
        rest_pcts = []
        totals = []
        counts = {'Dominance': [], 'Mixture': [], 'Restructuring': []}

        for label in labels:
            if label in results:
                data = results[label]
                total = data['Dominance'] + data['Mixing'] + data['Restructuring']
            else:
                total = 0
                data = {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0}

            totals.append(total)

            if total > 0:
                cls_pcts.append(data['Dominance'] / total * 100)
                mix_pcts.append(data['Mixing'] / total * 100)
                rest_pcts.append(data['Restructuring'] / total * 100)
            else:
                cls_pcts.append(0)
                mix_pcts.append(0)
                rest_pcts.append(0)

            counts['Dominance'].append(data['Dominance'])
            counts['Mixture'].append(data['Mixing'])
            counts['Restructuring'].append(data['Restructuring'])

        # Create stacked bars
        ax.bar(x, cls_pcts, bar_width, label='Dominance', color=COLORS[0], edgecolor='white', linewidth=0.5)
        ax.bar(x, mix_pcts, bar_width, bottom=cls_pcts, label='Mixture', color=COLORS[1], edgecolor='white', linewidth=0.5)
        ax.bar(x, rest_pcts, bar_width, bottom=np.array(cls_pcts) + np.array(mix_pcts),
               label='Restructuring', color=COLORS[2], edgecolor='white', linewidth=0.5)

        # Add annotations (black text, fontsize x1.3)
        for i in range(n_bars):
            total = totals[i]
            if total == 0:
                continue

            if cls_pcts[i] > 12:
                y_pos = cls_pcts[i] / 2
                ax.text(x[i], y_pos, f"{cls_pcts[i]:.0f}%\n({counts['Dominance'][i]}/{total})",
                       ha='center', va='center', fontsize=annotation_fontsize, color='black')

            if mix_pcts[i] > 12:
                y_pos = cls_pcts[i] + mix_pcts[i] / 2
                ax.text(x[i], y_pos, f"{mix_pcts[i]:.0f}%\n({counts['Mixture'][i]}/{total})",
                       ha='center', va='center', fontsize=annotation_fontsize, color='black')

            if rest_pcts[i] > 12:
                y_pos = cls_pcts[i] + mix_pcts[i] + rest_pcts[i] / 2
                ax.text(x[i], y_pos, f"{rest_pcts[i]:.0f}%\n({counts['Restructuring'][i]}/{total})",
                       ha='center', va='center', fontsize=annotation_fontsize, color='black')

        ax.set_title(f'μ = {mu}', fontsize=14.3)  # 11 * 1.3
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=11.7)  # 9 * 1.3
        ax.set_xlabel('Parental-community richness', fontsize=13)  # 10 * 1.3
        ax.set_ylim(0, 100)
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if ax_idx == 0:
            ax.set_ylabel('Fraction (%)', fontsize=14.3)  # 11 * 1.3
            ax.legend(loc='upper right', frameon=True, fontsize=10.4)  # 8 * 1.3

    plt.tight_layout()

    output_file = output_dir / "Fig_S12_species_ablation_stacked_bar.svg"
    fig.savefig(output_file, format='svg', dpi=300, bbox_inches='tight')
    fig.savefig(str(output_file).replace('.svg', '.pdf'), format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_file}")

    return all_results


# =============================================================================
# Figure S25: Assembly Effect Simulation
# =============================================================================

def generate_fig_s25_assembly_simulation():
    """Generate Fig S25: Assembly effect simulation."""
    print("\n" + "="*70)
    print("Generating Fig S25: Assembly Effect Simulation (Stacked Bar)")
    print("="*70)

    # Load simulation data
    coalescence_file = Path("Simulation_Data/coalescence_vs_direct_50reps/Community_coalescence_50reps.json")
    direct_file = Path("Simulation_Data/coalescence_vs_direct_50reps/Community_direct_50reps.json")

    if not coalescence_file.exists() or not direct_file.exists():
        print("  Warning: Simulation data files not found")
        return None

    with open(coalescence_file, 'r') as f:
        coal_data = json.load(f)
    with open(direct_file, 'r') as f:
        direct_data = json.load(f)

    interaction_strengths = [0.2, 0.4, 0.6, 0.8, 1.0]

    coal_results = {}
    direct_results = {}

    for mu in interaction_strengths:
        label = f'μ={mu}'

        # Process coalescence data
        dominance = mixing = restructuring = 0
        for combo_key in coal_data.keys():
            if f'mean{mu:.2f}_' not in combo_key:
                continue
            combo = coal_data[combo_key]
            for rep_key, rep_data in combo.items():
                c1 = np.array(rep_data['sc_list']['c1'])
                c2 = np.array(rep_data['sc_list']['c2'])
                c_mix = np.array(rep_data['cc_list']['c1_c2'])
                try:
                    u, v, k, _ = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)
                    outcome = classify_outcome(u, v, k)
                    if outcome == 0:
                        dominance += 1
                    elif outcome == 1:
                        mixing += 1
                    else:
                        restructuring += 1
                except:
                    continue

        coal_results[label] = {'Dominance': dominance, 'Mixing': mixing, 'Restructuring': restructuring}

        # Process direct assembly data
        dominance = mixing = restructuring = 0
        for combo_key in direct_data.keys():
            if f'mean{mu:.2f}_' not in combo_key:
                continue
            combo = direct_data[combo_key]
            for rep_key, rep_data in combo.items():
                c1 = np.array(rep_data['sc_list']['c1'])
                c2 = np.array(rep_data['sc_list']['c2'])
                c_mix = np.array(rep_data['cc_list']['c1_c2'])
                try:
                    u, v, k, _ = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)
                    outcome = classify_outcome(u, v, k)
                    if outcome == 0:
                        dominance += 1
                    elif outcome == 1:
                        mixing += 1
                    else:
                        restructuring += 1
                except:
                    continue

        direct_results[label] = {'Dominance': dominance, 'Mixing': mixing, 'Restructuring': restructuring}

    # Create two-row stacked bar plot
    labels = [f'μ={mu}' for mu in interaction_strengths]
    output_file = output_dir / "Fig_S25_assembly_effect_simulation_stacked_bar.svg"

    create_two_row_stacked_bar_plot(
        coal_results, direct_results, labels,
        'Coalescence', 'Direct Assembly',
        'Assembly History Effect on Coalescence Outcomes (Simulation)',
        output_file, figsize=(10, 6)
    )

    return coal_results, direct_results


# =============================================================================
# Figure S26: Assembly Effect Experimental
# =============================================================================

def generate_fig_s26_assembly_experimental():
    """Generate Fig S26: Assembly effect experimental."""
    print("\n" + "="*70)
    print("Generating Fig S26: Assembly Effect Experimental (Stacked Bar)")
    print("="*70)

    # Load assembly pairs data
    data_path = Path('Figure/Assembly_effect/assembly_pairs_CORRECT.pkl')

    if not data_path.exists():
        print("  Warning: Assembly pairs data not found")
        return None

    with open(data_path, 'rb') as f:
        assembly_data = pickle.load(f)

    media_labels = {'LN': 'Nutr-', 'MN': 'Base', 'HN': 'Nutr+'}
    media_order = ['LN', 'MN', 'HN']

    coal_results = {}
    parent_results = {}

    pairs_data = assembly_data['pairs']

    for medium in media_order:
        label = media_labels[medium]
        coal_dom = coal_mix = coal_rest = 0
        parent_dom = parent_mix = parent_rest = 0

        if medium in pairs_data:
            for comparison_type in pairs_data[medium].keys():
                pairs = pairs_data[medium][comparison_type]

                for pair in pairs:
                    if pair['parent_replicate'] != pair['coalesced_replicate']:
                        continue

                    parent_abund = np.array(pair['parent_abundances'], dtype=float)
                    coal_abund = np.array(pair['coalesced_abundances'], dtype=float)
                    sub1_abund = np.array(pair['sub1_abundances'], dtype=float)
                    sub2_abund = np.array(pair['sub2_abundances'], dtype=float)

                    parent_abund = np.nan_to_num(parent_abund, nan=0.0)
                    coal_abund = np.nan_to_num(coal_abund, nan=0.0)
                    sub1_abund = np.nan_to_num(sub1_abund, nan=0.0)
                    sub2_abund = np.nan_to_num(sub2_abund, nan=0.0)

                    threshold = 1e-4
                    parent_abund = parent_abund * (parent_abund > threshold)
                    coal_abund = coal_abund * (coal_abund > threshold)
                    sub1_abund = sub1_abund * (sub1_abund > threshold)
                    sub2_abund = sub2_abund * (sub2_abund > threshold)

                    try:
                        # Coalesced
                        u, v, k, _ = metric_VectorDecomposition_onlyPositive(sub1_abund, sub2_abund, coal_abund)
                        outcome = classify_outcome(u, v, k)
                        if outcome == 0:
                            coal_dom += 1
                        elif outcome == 1:
                            coal_mix += 1
                        else:
                            coal_rest += 1

                        # Parent (use same subs)
                        u, v, k, _ = metric_VectorDecomposition_onlyPositive(sub1_abund, sub2_abund, parent_abund)
                        outcome = classify_outcome(u, v, k)
                        if outcome == 0:
                            parent_dom += 1
                        elif outcome == 1:
                            parent_mix += 1
                        else:
                            parent_rest += 1
                    except:
                        continue

        coal_results[label] = {'Dominance': coal_dom, 'Mixing': coal_mix, 'Restructuring': coal_rest}
        parent_results[label] = {'Dominance': parent_dom, 'Mixing': parent_mix, 'Restructuring': parent_rest}

    # Create two-row stacked bar plot
    labels = [media_labels[m] for m in media_order]
    output_file = output_dir / "Fig_S26_assembly_effect_experimental_stacked_bar.svg"

    create_two_row_stacked_bar_plot(
        coal_results, parent_results, labels,
        'Coalescence', 'Direct Assembly',
        'Assembly History Effect on Coalescence Outcomes (Experimental)',
        output_file, figsize=(6, 6)
    )

    return coal_results, parent_results


# =============================================================================
# Main
# =============================================================================

def main():
    print("="*70)
    print("Generating Stacked Bar Plots for Class Fractions")
    print("="*70)
    print(f"Output directory: {output_dir}")

    # Generate all figures
    generate_fig_s4_robustness()
    generate_fig_s12_species_ablation()
    generate_fig_s25_assembly_simulation()
    generate_fig_s26_assembly_experimental()

    print("\n" + "="*70)
    print("✓ All stacked bar plots generated successfully!")
    print("="*70)
    print(f"\nOutput files saved to: {output_dir}/")


if __name__ == "__main__":
    main()
