#!/usr/bin/env python
"""
Plot Phase Diagram for 400 reps superfine data using the SAME STYLE as 200reps_fine.

This script uses the exact same create_phase_diagram function from common_setup.py
to ensure visual consistency with the 200reps_fine figure.

Output:
- Figure/PhaseDiagram/Fig_phase_diagram_48species_400reps_superfine.svg (matches 200reps_fine style)
"""

from common_setup import *
from pathlib import Path
import json
import numpy as np


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
        data1 = {}
        data2 = {}
        data3 = {}

        for u_str, u_data in simulation_data.items():
            if len(u_data) == 0:
                continue

            types_to_plot.append(u_str)
            u_data1 = []
            u_data2 = []
            u_data3 = []

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


def main():
    """Generate phase diagram for 400 reps superfine data with 200reps_fine style."""

    Path("Figure/PhaseDiagram").mkdir(parents=True, exist_ok=True)

    json_file = "Simulation_Data/48species_400reps_superfine/Community_400reps_superfine.json"
    session_name = "48species_400reps_superfine"

    print(f"\n{'='*70}")
    print("Generating 400 reps superfine phase diagram (200reps_fine style)")
    print(f"{'='*70}")

    types_to_plot, data1, data2, data3 = process_json_simulation_data(json_file, session_name)

    if types_to_plot is None or len(types_to_plot) == 0:
        print("Error: No data found")
        return

    # Set up tick labels same as 200reps_fine (0.4, 0.8, 1.2)
    # For 59 values from 0.05 to 1.21 in steps of 0.02
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

    # Add end position with empty label (like 200reps_fine)
    custom_x_ticks.append(n_values)
    custom_x_labels.append("")

    # Generate output using ORIGINAL create_phase_diagram from common_setup.py
    # This ensures exact style match with 200reps_fine
    for fmt in ['svg', 'png', 'pdf']:
        output_filename = f"Figure/PhaseDiagram/Fig_phase_diagram_{session_name}.{fmt}"

        create_phase_diagram(
            types_to_plot,
            data1, data2, data3,
            custom_x_ticks,
            custom_x_labels,
            output_filename=output_filename,
            plot_boundary=False
        )

    print(f"\nCreated: Figure/PhaseDiagram/Fig_phase_diagram_{session_name}.[svg,png,pdf]")
    print("Style matches 200reps_fine (stepped bars, same tick format)")


if __name__ == "__main__":
    main()
