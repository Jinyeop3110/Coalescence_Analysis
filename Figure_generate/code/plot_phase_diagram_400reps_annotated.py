#!/usr/bin/env python
"""
Plot Phase Diagram for 400 reps superfine data with annotations.
Adds vertical lines at mu=0.3, 0.6, 0.8 with percentage text annotations.
"""

import os
import sys
import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case
)
from COLORMAP import get_phase_diagram_colors


def process_json_simulation_data(json_file_path, session_name):
    """Process JSON simulation data and extract vector decomposition coefficients."""
    print(f"Processing JSON simulation data: {session_name}")

    if not Path(json_file_path).exists():
        print(f"Warning: File not found: {json_file_path}")
        return None, None, None, None

    try:
        with open(json_file_path, 'r') as f:
            simulation_data = json.load(f)

        print(f"Loaded JSON data with {len(simulation_data)} interaction strengths")

        types_to_plot = []
        data1, data2, data3 = {}, {}, {}

        for u_str, u_data in simulation_data.items():
            if len(u_data) == 0:
                continue

            types_to_plot.append(u_str)
            u_data1, u_data2, u_data3 = [], [], []

            for rep_key, rep_data in u_data.items():
                try:
                    sc_list = rep_data.get('sc_list', {})
                    cc_list = rep_data.get('cc_list', {})

                    if not sc_list or not cc_list:
                        continue

                    for cc_key, cmix in cc_list.items():
                        try:
                            c1_idx, c2_idx = cc_key.split('_')
                            c1_idx, c2_idx = int(c1_idx), int(c2_idx)
                        except:
                            continue

                        if str(c1_idx) not in sc_list or str(c2_idx) not in sc_list:
                            if c1_idx not in sc_list or c2_idx not in sc_list:
                                continue
                            c1 = np.array(sc_list[c1_idx])
                            c2 = np.array(sc_list[c2_idx])
                        else:
                            c1 = np.array(sc_list[str(c1_idx)])
                            c2 = np.array(sc_list[str(c2_idx)])

                        cmix = np.array(cmix)

                        try:
                            u_coeff, v_coeff, k_coeff = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
                            u_data1.append(u_coeff)
                            u_data2.append(v_coeff)
                            u_data3.append(k_coeff)
                        except:
                            continue
                except:
                    continue

            data1[u_str] = u_data1
            data2[u_str] = u_data2
            data3[u_str] = u_data3

        try:
            types_to_plot.sort(key=lambda x: float(x))
        except:
            types_to_plot.sort()

        total_points = sum(len(data1.get(t, [])) for t in types_to_plot)
        print(f"Successfully processed {len(types_to_plot)} interaction strengths, {total_points:,} data points")

        return types_to_plot, data1, data2, data3

    except Exception as e:
        print(f"Error processing {json_file_path}: {e}")
        return None, None, None, None


def create_phase_diagram_annotated(
    type_names,
    data1_set,
    data2_set,
    data3_set,
    custom_x_ticks=None,
    custom_x_labels=None,
    output_filename="Fig_phase_diagram_annotated.svg",
    annotation_mu_values=[0.31, 0.61, 0.81],
):
    """Creates a stacked-filled bar plot with annotations at specific mu values."""
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
    ax1.set_xlabel(r'Interaction strength $\mu$')
    ax1.set_xlim([0, n_types])
    ax1.set_ylim([0, 1])

    if custom_x_ticks is not None and custom_x_labels is not None:
        ax1.set_xticks(custom_x_ticks)
        ax1.set_xticklabels(custom_x_labels)

    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['0', '1'])

    # Add annotations
    annotation_font_size = 6

    for mu_target in annotation_mu_values:
        mu_str = f"{mu_target:.2f}"
        pos = None

        if mu_str in type_names:
            pos = type_names.index(mu_str)
        else:
            # Find closest match
            try:
                type_floats = [float(t) for t in type_names]
                closest_idx = np.argmin(np.abs(np.array(type_floats) - mu_target))
                if np.abs(type_floats[closest_idx] - mu_target) < 0.02:
                    pos = closest_idx
            except:
                pass

        if pos is not None:
            dom_frac = class1_fractions[pos]
            mix_frac = class2_fractions[pos]
            rest_frac = class3_fractions[pos]

            # Vertical dashed line
            ax1.axvline(x=pos + 0.5, color='black', linestyle='--', alpha=0.9, linewidth=1.0)

            y_dom = dom_frac / 2
            y_mix = dom_frac + mix_frac / 2
            y_rest = dom_frac + mix_frac + rest_frac / 2

            x_text = pos + 1.5

            if dom_frac > 0.05:
                ax1.text(x_text, y_dom, f'{dom_frac*100:.0f}%',
                        ha='left', va='center', fontsize=annotation_font_size,
                        color='white', weight='bold')

            if mix_frac > 0.05:
                ax1.text(x_text, y_mix, f'{mix_frac*100:.0f}%',
                        ha='left', va='center', fontsize=annotation_font_size,
                        color='black', weight='bold')

            if rest_frac > 0.05:
                ax1.text(x_text, y_rest, f'{rest_frac*100:.0f}%',
                        ha='left', va='center', fontsize=annotation_font_size,
                        color='black', weight='bold')

            # Mu label at top (display as rounded value)
            mu_display = round(mu_target, 1)
            ax1.text(pos + 0.5, 1.02, f'$\\mu$={mu_display}',
                    ha='center', va='bottom', fontsize=annotation_font_size,
                    color='black')

            print(f"  mu={mu_display} (actual {mu_target}): Dom={dom_frac*100:.1f}%, Mix={mix_frac*100:.1f}%, Rest={rest_frac*100:.1f}%")

    plt.tight_layout()
    fig.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close(fig)


def main():
    Path("Figure/PhaseDiagram").mkdir(parents=True, exist_ok=True)

    json_file = "Simulation_Data/48species_400reps_superfine/Community_400reps_superfine.json"

    if not Path(json_file).exists():
        # Try the 500reps superfine
        json_file = "Simulation_Data/48species_500reps_superfine/Community_500reps_superfine.json"

    session_name = "48species_400reps_superfine"

    print(f"\n{'='*70}")
    print("Generating annotated 400 reps superfine phase diagram")
    print(f"{'='*70}")

    types_to_plot, data1, data2, data3 = process_json_simulation_data(json_file, session_name)

    if types_to_plot is None or len(types_to_plot) == 0:
        print("Error: No data found")
        return

    n_values = len(types_to_plot)

    custom_x_ticks = []
    custom_x_labels = []
    target_labels = [0.4, 0.8, 1.2]

    for target in target_labels:
        target_str = f"{target:.2f}"
        if target_str in types_to_plot:
            pos = types_to_plot.index(target_str)
            custom_x_ticks.append(pos)
            custom_x_labels.append(f"{target:.1f}")

    custom_x_ticks.append(n_values)
    custom_x_labels.append("")

    # Use mu values that exist in data (0.31, 0.61, 0.81)
    annotation_mu = [0.31, 0.61, 0.81]

    for fmt in ['svg', 'png', 'pdf']:
        output_filename = f"Figure/PhaseDiagram/Fig_phase_diagram_{session_name}_annotated.{fmt}"

        create_phase_diagram_annotated(
            types_to_plot,
            data1, data2, data3,
            custom_x_ticks,
            custom_x_labels,
            output_filename=output_filename,
            annotation_mu_values=annotation_mu
        )

    print(f"\nCreated: Figure/PhaseDiagram/Fig_phase_diagram_{session_name}_annotated.[svg,png,pdf]")


if __name__ == "__main__":
    main()
