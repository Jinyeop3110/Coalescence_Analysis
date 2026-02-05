"""
plot_phase_diagram_synthetic_merged_annotated.py

Purpose: Generate annotated phase diagram for synthetic/experimental coalescence data
         (merged across all species pool sizes) with percentage annotations per bar.

Outputs:
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged_annotated.svg
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged_annotated.png
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged_annotated.pdf
"""

from common_setup import *
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from COLORMAP import get_phase_diagram_colors


def create_phase_diagram_annotated(
    type_names,
    data1_set,
    data2_set,
    data3_set,
    custom_x_ticks=None,
    custom_x_labels=None,
    output_filename="Fig_phase_diagram_annotated.svg",
):
    """Creates a stacked-filled bar plot with percentage annotations in each bar segment."""
    n_types = len(type_names)
    class1_fractions = np.zeros(n_types + 1)
    class2_fractions = np.zeros(n_types + 1)
    class3_fractions = np.zeros(n_types + 1)

    colors = get_phase_diagram_colors()

    for c_i, type_name in enumerate(type_names):
        class1_count = 0
        class2_count = 0
        class3_count = 0

        for j in range(len(data1_set.get(type_name, []))):
            u = data1_set[type_name][j]
            v = data2_set[type_name][j]
            k = data3_set[type_name][j]

            x, y = calculate_assymetricity(u, v, k)
            ii = characterize_case(x, y)

            if ii == 0:
                class1_count += 1
            elif ii == 1:
                class2_count += 1
            else:
                class3_count += 1

        total = class1_count + class2_count + class3_count
        if total > 0:
            class1_fractions[c_i] = class1_count / total
            class2_fractions[c_i] = class2_count / total
            class3_fractions[c_i] = class3_count / total

    # Figure setup - SAME SIZE as original
    mm = 1 / 25.4 * 72
    fig_width = 60 * mm
    fig_height = 60 * mm

    fig, ax1 = plt.subplots(figsize=(fig_width / 72, fig_height / 72), facecolor='w')

    x_vals = np.arange(n_types + 1)

    # Create stacked area plot
    ax1.fill_between(x_vals, 0, class1_fractions,
                     step='post', color=colors[0], alpha=0.85, edgecolor='none')
    ax1.fill_between(x_vals, class1_fractions, class1_fractions + class2_fractions,
                     step='post', color=colors[1], alpha=0.85, edgecolor='none')
    ax1.fill_between(x_vals, class1_fractions + class2_fractions,
                     class1_fractions + class2_fractions + class3_fractions,
                     step='post', color=colors[2], alpha=0.85, edgecolor='none')

    ax1.set_ylabel('Coalescence outcome fraction')
    ax1.set_xlim([0, n_types])
    ax1.set_ylim([0, 1])

    if custom_x_ticks is not None and custom_x_labels is not None:
        ax1.set_xticks(custom_x_ticks)
        ax1.set_xticklabels(custom_x_labels)

    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['0', '1'])

    # Add boundary lines between bars
    for boundary in range(1, n_types):
        ax1.axvline(x=boundary, color='black', linestyle='--', alpha=0.5, linewidth=1)

    # Add percentage annotations inside each bar segment
    annotation_font_size = 6

    for pos in range(n_types):
        dom_frac = class1_fractions[pos]
        mix_frac = class2_fractions[pos]
        rest_frac = class3_fractions[pos]

        x_center = pos + 0.5

        # Dominance (bottom segment)
        if dom_frac > 0.05:
            y_dom = dom_frac / 2
            ax1.text(x_center, y_dom, f'{dom_frac*100:.0f}%',
                    ha='center', va='center', fontsize=annotation_font_size,
                    color='white', weight='bold')

        # Mixing (middle segment)
        if mix_frac > 0.05:
            y_mix = dom_frac + mix_frac / 2
            ax1.text(x_center, y_mix, f'{mix_frac*100:.0f}%',
                    ha='center', va='center', fontsize=annotation_font_size,
                    color='black', weight='bold')

        # Restructuring (top segment)
        if rest_frac > 0.05:
            y_rest = dom_frac + mix_frac + rest_frac / 2
            ax1.text(x_center, y_rest, f'{rest_frac*100:.0f}%',
                    ha='center', va='center', fontsize=annotation_font_size,
                    color='black', weight='bold')

        print(f"  {type_names[pos]}: Dom={dom_frac*100:.1f}%, Mix={mix_frac*100:.1f}%, Rest={rest_frac*100:.1f}%")

    plt.tight_layout()
    fig.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close(fig)


def main():
    """Main function to generate annotated merged phase diagram."""
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating annotated merged phase diagram for synthetic coalescence data...")

    # Combine data for each nutrient level across all species pool sizes
    data1_set_merged = {}
    data2_set_merged = {}
    data3_set_merged = {}

    for nutrient_level in ['LN', 'MN', 'HN']:
        data1_combined = []
        data2_combined = []
        data3_combined = []

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

        data1_set_merged[nutrient_level] = data1_combined
        data2_set_merged[nutrient_level] = data2_combined
        data3_set_merged[nutrient_level] = data3_combined

    types_to_plot_merged = ['LN', 'MN', 'HN']
    custom_x_ticks = [0.5, 1.5, 2.5]
    custom_x_labels = ['Nutr$-$', 'Base', 'Nutr$+$']

    for fmt in ['svg', 'png', 'pdf']:
        output_filename = f"Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged_annotated.{fmt}"

        create_phase_diagram_annotated(
            types_to_plot_merged,
            data1_set_merged, data2_set_merged, data3_set_merged,
            custom_x_ticks, custom_x_labels,
            output_filename=output_filename,
        )
        print(f"Created: {output_filename}")

    print("\nDone!")


if __name__ == "__main__":
    main()
