"""
plot_phase_diagram_pie.py

Purpose: Generate pie plots and stacked bar plots for synthetic coalescence data showing distribution of outcomes
Key features:
- Creates pie charts for dominance, mixing, and restructuring outcomes
- Creates stacked bar plots (vertical) for each nutrient condition separately
- Shows percentage distributions for each nutrient condition (LN, MN, HN)
- Creates stacked bar plot for simulation at mu=0.6
- Uses the same data classification as phase diagrams but displays as pie charts

Output:
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged_pie.svg
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_bar_LN.svg/.png (Nutr-)
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_bar_MN.svg/.png (Base)
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_bar_HN.svg/.png (Nutr+)
- Figure/PhaseDiagram/Fig_phase_diagram_simulation_bar_mu0.6.svg/.png (Simulation mu=0.6)
"""

from common_setup import *
from pathlib import Path
import numpy as np
import json
import matplotlib.pyplot as plt
from COLORMAP import get_phase_diagram_colors

def classify_outcomes(u_values, v_values, k_values):
    """
    Classify coalescence outcomes based on u, v, k values using the same logic as phase diagrams.

    Returns counts of:
    - Dominance (class 0)
    - Mixing (class 1)
    - Restructuring (class 2)
    """
    dominance_count = 0
    mixing_count = 0
    restructuring_count = 0

    for u, v, k in zip(u_values, v_values, k_values):
        # Use the same classification logic as in common_setup.py
        x = np.sqrt(u**2 + v**2)
        y = np.abs(np.abs(np.arctan(u/(v + 1e-8))) - np.pi/4) / (np.pi/4)

        # characterize_case logic
        if (x**2 > 0.5) * (y > 0.5):
            dominance_count += 1  # Class 0
        elif (x**2 > 0.5) * (y < 0.5):
            mixing_count += 1     # Class 1
        elif (x**2 < 0.5):
            restructuring_count += 1  # Class 2

    return dominance_count, mixing_count, restructuring_count


def create_single_stacked_bar_no_axis(data, colors, output_basename, show_counts=True):
    """
    Create a single vertical stacked bar plot without axis annotations.
    Only shows % and optionally (count/total) annotations.

    Parameters:
    -----------
    data : dict
        Dict with 'Dominance', 'Mixing', 'Restructuring' counts
    colors : list
        Colors for each category
    output_basename : str
        Base filename for output (without extension)
    show_counts : bool
        Whether to show (count/total) annotations (default True)
    """
    fig, ax = plt.subplots(figsize=(2.5, 4))

    total = data['Dominance'] + data['Mixing'] + data['Restructuring']

    if total == 0:
        plt.close()
        return

    # Calculate percentages
    cls_pct = data['Dominance'] / total * 100
    mix_pct = data['Mixing'] / total * 100
    rest_pct = data['Restructuring'] / total * 100

    bar_width = 0.5
    x = 0

    # Create stacked bars
    ax.bar(x, cls_pct, bar_width, label='CLS', color=colors[0], edgecolor='white', linewidth=0.5)
    ax.bar(x, mix_pct, bar_width, bottom=cls_pct, label='Mixing', color=colors[1], edgecolor='white', linewidth=0.5)
    ax.bar(x, rest_pct, bar_width, bottom=cls_pct + mix_pct, label='Restructuring', color=colors[2], edgecolor='white', linewidth=0.5)

    # Annotation fontsize (x1.5)
    annotation_fontsize = 15

    # Add annotations (black text) - % and optionally (count/total)
    # CLS annotation (bottom section)
    if cls_pct > 8:
        y_pos = cls_pct / 2
        if show_counts:
            text = f"{cls_pct:.0f}%\n({data['Dominance']}/{total})"
        else:
            text = f"{cls_pct:.0f}%"
        ax.text(x, y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, fontweight='bold', color='black')

    # Mixing annotation (middle section)
    if mix_pct > 8:
        y_pos = cls_pct + mix_pct / 2
        if show_counts:
            text = f"{mix_pct:.0f}%\n({data['Mixing']}/{total})"
        else:
            text = f"{mix_pct:.0f}%"
        ax.text(x, y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, fontweight='bold', color='black')

    # Restructuring annotation (top section)
    if rest_pct > 8:
        y_pos = cls_pct + mix_pct + rest_pct / 2
        if show_counts:
            text = f"{rest_pct:.0f}%\n({data['Restructuring']}/{total})"
        else:
            text = f"{rest_pct:.0f}%"
        ax.text(x, y_pos, text, ha='center', va='center', fontsize=annotation_fontsize, fontweight='bold', color='black')

    # Remove all axis elements
    ax.set_ylim(0, 100)
    ax.set_xlim(-0.5, 0.5)
    ax.axis('off')  # Remove all axes

    plt.tight_layout()

    # Save as SVG and PNG
    fig.savefig(f"{output_basename}.svg", format='svg', dpi=300, bbox_inches='tight', transparent=True)
    fig.savefig(f"{output_basename}.png", format='png', dpi=300, bbox_inches='tight', transparent=True)
    plt.close()

    print(f"  ✓ Created: {output_basename}.svg and .png")


def generate_simulation_bar_mu06():
    """Generate stacked bar plot for simulation at mu=0.6."""

    print("\nGenerating simulation bar plot for μ=0.6...")

    # Load simulation data from 48species_200reps_fine
    data_file = Path("Simulation_Data/48species_200reps_fine/Community_200reps_fine.json")

    if not data_file.exists():
        print(f"  Warning: Simulation data file not found: {data_file}")
        return None

    with open(data_file, 'r') as f:
        sim_data = json.load(f)

    # Find mu=0.6 data
    mu_str = "0.60"
    dominance = mixing = restructuring = 0

    if mu_str in sim_data:
        mu_data = sim_data[mu_str]
        for rep_key, rep_data in mu_data.items():
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            for cc_key, c_mix in cc_list.items():
                idx1, idx2 = cc_key.split('_')
                c1 = np.array(sc_list[idx1])
                c2 = np.array(sc_list[idx2])
                c_mix = np.array(c_mix)

                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)[:3]
                    dom, mix, rest = classify_outcomes([u], [v], [k])
                    dominance += dom
                    mixing += mix
                    restructuring += rest
                except:
                    continue

    data = {
        'Dominance': dominance,
        'Mixing': mixing,
        'Restructuring': restructuring
    }

    colors = get_phase_diagram_colors()
    output_basename = "Figure/PhaseDiagram/Fig_phase_diagram_simulation_bar_mu0.6"
    create_single_stacked_bar_no_axis(data, colors, output_basename, show_counts=False)

    total = dominance + mixing + restructuring
    print(f"  Simulation μ=0.6: CLS={dominance} ({dominance/total*100:.1f}%), Mixing={mixing} ({mixing/total*100:.1f}%), Rest={restructuring} ({restructuring/total*100:.1f}%), n={total}")

    return data


def main():
    """Main function to generate pie plots and bar plots for synthetic merged data."""

    # Create output directory
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating plots for synthetic coalescence data...")

    # Collect data for each nutrient level across all species pool sizes
    nutrient_levels = ['LN', 'MN', 'HN']
    nutrient_labels = {'LN': 'Nutr-', 'MN': 'Base', 'HN': 'Nutr+'}
    pie_data = {}

    for nutrient_level in nutrient_levels:
        data1_combined = []
        data2_combined = []
        data3_combined = []

        # Combine data from all pool sizes
        for pool_size in ['6', '12', '24']:
            type_name = f'{nutrient_level}_{pool_size}'

            if type_name in Syn_Coal_IDX:
                IDX_list = Syn_Coal_IDX[type_name]
                idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
                idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
                idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
                idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
                idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
                idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
                idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])

                for i in range(len(idx)):
                    c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                    c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                    c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                    c_1 = c_1 * (c_1 > 1e-4)
                    c_2 = c_2 * (c_2 > 1e-4)
                    u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                    data1_combined.append(u)
                    data2_combined.append(v)
                    data3_combined.append(k)

        # Classify outcomes
        dominance, mixing, restructuring = classify_outcomes(data1_combined, data2_combined, data3_combined)
        pie_data[nutrient_level] = {
            'Dominance': dominance,
            'Mixing': mixing,
            'Restructuring': restructuring
        }

    # Get colors
    colors = get_phase_diagram_colors()

    # ==========================================================================
    # Generate separate stacked bar plots for each nutrient condition (no axis)
    # ==========================================================================
    print("\nGenerating stacked bar plots (no axis annotations)...")

    for nutrient_level in nutrient_levels:
        output_basename = f"Figure/PhaseDiagram/Fig_phase_diagram_synthetic_bar_{nutrient_level}"
        create_single_stacked_bar_no_axis(pie_data[nutrient_level], colors, output_basename)

    # ==========================================================================
    # Also create combined horizontal stacked bar plot (original format)
    # ==========================================================================
    print("\nGenerating combined horizontal bar plot...")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for idx, (nutrient_level, ax) in enumerate(zip(nutrient_levels, axes)):
        data = pie_data[nutrient_level]
        values = [data['Dominance'], data['Mixing'], data['Restructuring']]
        labels = ['Dominance', 'Mixing', 'Restructuring']

        # Calculate total
        total = sum(values)

        # Create horizontal stacked bar chart
        left = 0
        for i, (value, label) in enumerate(zip(values, labels)):
            percentage = value / total * 100 if total > 0 else 0
            bar = ax.barh(0, percentage, left=left, color=colors[i],
                         alpha=0.85, height=0.5, edgecolor='white', linewidth=2)

            # Add text label with (n/total) format
            if percentage > 5:  # Only show label if segment is large enough
                ax.text(left + percentage/2, 0, f'{value}/{total}',
                       ha='center', va='center', fontsize=14, fontweight='bold',
                       color='black')

            left += percentage

        # Set axis properties
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel('Percentage (%)', fontsize=12)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add title
        ax.set_title(f'{nutrient_labels[nutrient_level]}', fontsize=14, fontweight='bold', pad=20)

    # Adjust layout
    plt.tight_layout()

    # Save figure
    output_filename = "Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged_pie.svg"
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_filename}")

    # ==========================================================================
    # Generate simulation bar plot for mu=0.6
    # ==========================================================================
    generate_simulation_bar_mu06()

    # Print summary statistics
    print("\nSummary Statistics:")
    print("-" * 50)
    for nutrient_level in nutrient_levels:
        data = pie_data[nutrient_level]
        values_list = list(data.values())
        total_count = sum(values_list)
        print(f"\n{nutrient_labels[nutrient_level]} ({nutrient_level}) Medium (n={total_count}):")
        for outcome, count in data.items():
            if total_count > 0:
                percentage = count/total_count * 100
                print(f"  {outcome}: {count} ({percentage:.1f}%)")
            else:
                print(f"  {outcome}: {count} (0.0%)")

if __name__ == "__main__":
    main()