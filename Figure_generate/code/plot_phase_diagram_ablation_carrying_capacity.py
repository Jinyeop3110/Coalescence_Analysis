#!/usr/bin/env python
"""
Plot Phase Diagrams for Carrying Capacity Ablation Studies

This script creates phase diagrams from the carrying capacity ablation study simulation data.
- k_std01: K_i ~ N(1, 0.1^2) carrying capacity distribution
- k_std02: K_i ~ N(1, 0.2^2) carrying capacity distribution

Inputs:
- Simulation_Data/48species_ablation_k_std01/Community_ablation_k_std01.json
- Simulation_Data/48species_ablation_k_std02/Community_ablation_k_std02.json

Outputs:
- Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_k_std01.svg/png/pdf
- Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_k_std02.svg/png/pdf

Usage:
python plot_phase_diagram_ablation_carrying_capacity.py
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


def process_json_simulation_data(json_file_path):
    """Process JSON simulation data and extract vector decomposition coefficients."""

    with open(json_file_path, 'r') as f:
        simulation_data = json.load(f)

    types_to_plot = []
    data1, data2, data3 = {}, {}, {}

    for mu_str, mu_data in simulation_data.items():
        if len(mu_data) == 0:
            continue

        types_to_plot.append(mu_str)
        mu_data1, mu_data2, mu_data3 = [], [], []

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

                    u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
                    mu_data1.append(u)
                    mu_data2.append(v)
                    mu_data3.append(k)
                except:
                    continue

        data1[mu_str] = mu_data1
        data2[mu_str] = mu_data2
        data3[mu_str] = mu_data3

    types_to_plot.sort(key=lambda x: float(x))
    return types_to_plot, data1, data2, data3


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ablation_sessions = [
        {
            "name": "k_std01",
            "json_file": "Simulation_Data/48species_ablation_k_std01/Community_ablation_k_std01.json",
            "output_base": "Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_k_std01",
            "description": "Carrying capacity K ~ N(1, 0.1^2)"
        },
        {
            "name": "k_std02",
            "json_file": "Simulation_Data/48species_ablation_k_std02/Community_ablation_k_std02.json",
            "output_base": "Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_k_std02",
            "description": "Carrying capacity K ~ N(1, 0.2^2)"
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
            print(f"  Run simulation first: python run_ablation_carrying_capacity_{session['name']}.py", flush=True)
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
