#!/usr/bin/env python
"""
Plot Phase Diagrams for Species per Community Ablation Studies

This script creates phase diagrams from the species per community ablation study.
- 6 species/comm:  24 total (4 communities × 6 species)
- 9 species/comm:  36 total (4 communities × 9 species)
- 12 species/comm: 48 total (4 communities × 12 species) - baseline
- 24 species/comm: 96 total (4 communities × 24 species)

Inputs:
- Simulation_Data/6percomm_ablation_species_number/Community_ablation_6percomm.json
- Simulation_Data/9percomm_ablation_species_number/Community_ablation_9percomm.json
- Simulation_Data/12percomm_ablation_species_number/Community_ablation_12percomm.json
- Simulation_Data/24percomm_ablation_species_number/Community_ablation_24percomm.json

Outputs:
- Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_6percomm.svg/png/pdf
- Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_9percomm.svg/png/pdf
- Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_12percomm.svg/png/pdf
- Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_24percomm.svg/png/pdf

Usage:
python plot_phase_diagram_ablation_species_number.py
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common_setup import metric_VectorDecomposition_onlyPositive, create_phase_diagram


def process_json_simulation_data(json_file_path, verbose=True):
    """Process JSON simulation data and extract vector decomposition coefficients."""

    with open(json_file_path, 'r') as f:
        simulation_data = json.load(f)

    types_to_plot = []
    data1, data2, data3 = {}, {}, {}
    total_skipped_empty = 0
    total_skipped_nan = 0
    total_processed = 0

    for mu_str, mu_data in simulation_data.items():
        if len(mu_data) == 0:
            continue

        types_to_plot.append(mu_str)
        mu_data1, mu_data2, mu_data3 = [], [], []
        mu_skipped_empty = 0
        mu_skipped_nan = 0

        for rep_key, rep_data in mu_data.items():
            sc_list = rep_data.get('sc_list', {})
            cc_list = rep_data.get('cc_list', {})

            if not sc_list or not cc_list:
                continue

            for cc_key, cmix in cc_list.items():
                try:
                    parts = cc_key.split('_')
                    c1_key = parts[0]
                    c2_key = parts[1]

                    c1 = np.array(sc_list.get(c1_key, sc_list.get(int(c1_key), [])))
                    c2 = np.array(sc_list.get(c2_key, sc_list.get(int(c2_key), [])))
                    cmix = np.array(cmix)

                    # Skip if any community is empty (all zeros) - causes numerical issues
                    if np.sum(c1) == 0 or np.sum(c2) == 0 or np.sum(cmix) == 0:
                        mu_skipped_empty += 1
                        continue

                    u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)

                    # Skip if results contain NaN or Inf
                    if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                        mu_skipped_nan += 1
                        continue

                    mu_data1.append(u)
                    mu_data2.append(v)
                    mu_data3.append(k)
                    total_processed += 1
                except:
                    continue

        data1[mu_str] = mu_data1
        data2[mu_str] = mu_data2
        data3[mu_str] = mu_data3
        total_skipped_empty += mu_skipped_empty
        total_skipped_nan += mu_skipped_nan

    types_to_plot.sort(key=lambda x: float(x))

    if verbose and (total_skipped_empty > 0 or total_skipped_nan > 0):
        print(f"    Data quality: {total_processed} valid, {total_skipped_empty} skipped (empty), {total_skipped_nan} skipped (NaN)")

    return types_to_plot, data1, data2, data3


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ablation_sessions = [
        {
            "name": "4percomm",
            "json_file": "Simulation_Data/4percomm_ablation_species_number/Community_ablation_4percomm.json",
            "output_base": "Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_4percomm",
            "description": "4 species/comm (16 total)"
        },
        {
            "name": "6percomm",
            "json_file": "Simulation_Data/6percomm_ablation_species_number/Community_ablation_6percomm.json",
            "output_base": "Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_6percomm",
            "description": "6 species/comm (24 total)"
        },
        {
            "name": "9percomm",
            "json_file": "Simulation_Data/9percomm_ablation_species_number/Community_ablation_9percomm.json",
            "output_base": "Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_9percomm",
            "description": "9 species/comm (36 total)"
        },
        {
            "name": "12percomm",
            "json_file": "Simulation_Data/12percomm_ablation_species_number/Community_ablation_12percomm.json",
            "output_base": "Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_12percomm",
            "description": "12 species/comm (48 total) - baseline"
        },
        {
            "name": "24percomm",
            "json_file": "Simulation_Data/24percomm_ablation_species_number/Community_ablation_24percomm.json",
            "output_base": "Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_24percomm",
            "description": "24 species/comm (96 total)"
        },
        {
            "name": "48percomm",
            "json_file": "Simulation_Data/48percomm_ablation_species_number/Community_ablation_48percomm.json",
            "output_base": "Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_48percomm",
            "description": "48 species/comm (192 total)"
        }
    ]

    os.makedirs("Figure/PhaseDiagram_ablation", exist_ok=True)

    expected_mu_values = [f"{mu:.2f}" for mu in np.arange(0.05, 1.25, 0.05)]
    n_expected = len(expected_mu_values)

    custom_x_ticks = []
    custom_x_labels = []
    target_labels = [0.4, 0.8, 1.2]
    for target in target_labels:
        target_str = f"{target:.2f}"
        if target_str in expected_mu_values:
            pos = expected_mu_values.index(target_str)
            custom_x_ticks.append(pos)
            custom_x_labels.append(f"{target:.1f}")
    custom_x_ticks.append(n_expected)
    custom_x_labels.append("")

    for session in ablation_sessions:
        print(f"\nProcessing {session['name']} ({session['description']})...", flush=True)

        if not os.path.exists(session['json_file']):
            print(f"  File not found: {session['json_file']}", flush=True)
            print(f"  Run simulation first: python run_ablation_species_number.py", flush=True)
            continue

        print(f"  Loading data...", flush=True)
        types_to_plot, data1, data2, data3 = process_json_simulation_data(session['json_file'])
        print(f"  Loaded {len(types_to_plot)} interaction strengths", flush=True)

        padded_data1, padded_data2, padded_data3 = {}, {}, {}
        for mu in expected_mu_values:
            padded_data1[mu] = data1.get(mu, [])
            padded_data2[mu] = data2.get(mu, [])
            padded_data3[mu] = data3.get(mu, [])

        # Generate plots in multiple formats
        for fmt in ['svg', 'png', 'pdf']:
            output_filename = f"{session['output_base']}.{fmt}"

            try:
                create_phase_diagram(
                    expected_mu_values,
                    padded_data1, padded_data2, padded_data3,
                    custom_x_ticks,
                    custom_x_labels,
                    output_filename=output_filename,
                    plot_boundary=False
                )
                print(f"  Created: {output_filename}", flush=True)
            except Exception as e:
                print(f"  Failed to create {output_filename}: {e}", flush=True)

    print("\nDone!", flush=True)


if __name__ == "__main__":
    main()
