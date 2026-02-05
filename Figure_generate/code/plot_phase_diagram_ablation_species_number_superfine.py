#!/usr/bin/env python
"""
Plot Phase Diagrams for Species Number Ablation Studies - SUPERFINE VERSION
High-resolution version with 59 interaction strengths (step 0.02)

This script creates phase diagrams for different species per community configurations.

Usage:
python plot_phase_diagram_ablation_species_number_superfine.py
python plot_phase_diagram_ablation_species_number_superfine.py --smooth 2.0
"""

import os
import sys
import json
import argparse
import numpy as np
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common_setup import *


def process_json_simulation_data(json_file_path, session_name):
    """Process JSON simulation data and extract vector decomposition coefficients."""
    print(f"Processing JSON simulation data: {session_name}")

    if not Path(json_file_path).exists():
        print(f"Warning: File not found: {json_file_path}")
        return None, None, None, None

    try:
        with open(json_file_path, 'r') as f:
            simulation_data = json.load(f)

        print(f"  Loaded JSON data with {len(simulation_data)} interaction strengths")

        types_to_plot = []
        data1, data2, data3 = {}, {}, {}

        for mu_str, mu_data in simulation_data.items():
            if len(mu_data) == 0:
                continue

            types_to_plot.append(mu_str)
            mu_data1, mu_data2, mu_data3 = [], [], []

            for rep_key, rep_data in mu_data.items():
                try:
                    sc_list = rep_data.get('sc_list', {})
                    cc_list = rep_data.get('cc_list', {})

                    if not sc_list or not cc_list:
                        continue

                    for cc_key, cmix in cc_list.items():
                        try:
                            parts = cc_key.split('_')
                            c1_key = int(parts[0])
                            c2_key = int(parts[1])
                        except:
                            continue

                        c1 = np.array(sc_list.get(str(c1_key), sc_list.get(c1_key, [])))
                        c2 = np.array(sc_list.get(str(c2_key), sc_list.get(c2_key, [])))
                        cmix = np.array(cmix)

                        try:
                            u_coeff, v_coeff, k_coeff = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
                            mu_data1.append(u_coeff)
                            mu_data2.append(v_coeff)
                            mu_data3.append(k_coeff)
                        except:
                            continue
                except:
                    continue

            data1[mu_str] = mu_data1
            data2[mu_str] = mu_data2
            data3[mu_str] = mu_data3

        try:
            types_to_plot.sort(key=lambda x: float(x))
        except:
            types_to_plot.sort()

        total_points = sum(len(data1.get(t, [])) for t in types_to_plot)
        print(f"  Successfully processed {len(types_to_plot)} interaction strengths, {total_points:,} data points")

        return types_to_plot, data1, data2, data3

    except Exception as e:
        print(f"Error processing {json_file_path}: {e}")
        return None, None, None, None


def plot_species_number_phase_diagram_superfine(config, smooth_sigma=2.0, u_step=0.02):
    """Generate a phase diagram for species number ablation."""

    config_name = config['name']
    json_file = config['json_file']
    num_s = config['num_S']

    print(f"\n{'='*70}")
    print(f"Processing {config_name}: {num_s} species per community")
    print(f"{'='*70}")

    if not Path(json_file).exists():
        print(f"  File not found: {json_file}")
        return False

    types_to_plot, data1, data2, data3 = process_json_simulation_data(json_file, config_name)

    if types_to_plot is None or len(types_to_plot) == 0:
        print(f"  Skipping {config_name} due to data processing error")
        return False

    # For superfine data
    expected_mu_values = [f"{mu:.2f}" for mu in np.arange(0.05, 1.20 + u_step, u_step)]
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

    # Pad data
    padded_data1, padded_data2, padded_data3 = {}, {}, {}
    for mu in expected_mu_values:
        padded_data1[mu] = data1.get(mu, [])
        padded_data2[mu] = data2.get(mu, [])
        padded_data3[mu] = data3.get(mu, [])

    # Generate outputs
    output_base_superfine = f"Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_{config_name}_superfine"
    output_base_replace = f"Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_{config_name}"

    try:
        # Create superfine versions
        for fmt in ['svg', 'png', 'pdf']:
            # Superfine version
            create_phase_diagram(
                expected_mu_values,
                padded_data1, padded_data2, padded_data3,
                custom_x_ticks, custom_x_labels,
                output_filename=f"{output_base_superfine}.{fmt}",
                plot_boundary=False
            )
            # Replace old plots
            create_phase_diagram(
                expected_mu_values,
                padded_data1, padded_data2, padded_data3,
                custom_x_ticks, custom_x_labels,
                output_filename=f"{output_base_replace}.{fmt}",
                plot_boundary=False
            )

        print(f"  Created: {output_base_superfine}.[svg,png,pdf]")
        print(f"  Updated: {output_base_replace}.[svg,png,pdf]")
        return True

    except Exception as e:
        print(f"  Failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate species number ablation phase diagrams (superfine)')
    parser.add_argument('--smooth', type=float, default=2.0,
                        help='Gaussian smoothing sigma (default: 2.0)')
    parser.add_argument('--step', type=float, default=0.02,
                        help='Step size for interaction strengths (default: 0.02)')
    args = parser.parse_args()

    Path("Figure/PhaseDiagram_ablation").mkdir(parents=True, exist_ok=True)

    # Species number configurations
    configs = [
        {"name": "4percomm", "N": 16, "num_C": 4, "num_S": 4},
        {"name": "6percomm", "N": 24, "num_C": 4, "num_S": 6},
        {"name": "9percomm", "N": 36, "num_C": 4, "num_S": 9},
        {"name": "12percomm", "N": 48, "num_C": 4, "num_S": 12},
        {"name": "24percomm", "N": 96, "num_C": 4, "num_S": 24},
        {"name": "48percomm", "N": 192, "num_C": 4, "num_S": 48},
    ]

    for cfg in configs:
        cfg['json_file'] = f"Simulation_Data/{cfg['num_S']}percomm_ablation_species_number_superfine/Community_ablation_{cfg['name']}_superfine.json"

    print("\n" + "="*70)
    print("GENERATING PHASE DIAGRAMS FOR SPECIES NUMBER ABLATION (SUPERFINE)")
    print("="*70)

    print("\nChecking available simulation data...")
    available = []
    for cfg in configs:
        if Path(cfg['json_file']).exists():
            try:
                with open(cfg['json_file'], 'r') as f:
                    data = json.load(f)
                total = sum(len(data[k]) for k in data.keys())
                print(f"  {cfg['name']}: {total:,} simulations")
                available.append(cfg)
            except:
                print(f"  {cfg['name']}: Cannot read")
        else:
            print(f"  {cfg['name']}: Not found")

    if not available:
        print("\nNo simulation data available.")
        return

    successful = 0
    for cfg in available:
        if plot_species_number_phase_diagram_superfine(cfg, args.smooth, args.step):
            successful += 1

    print(f"\n{'='*70}")
    print(f"COMPLETE! Generated {successful} phase diagrams.")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
