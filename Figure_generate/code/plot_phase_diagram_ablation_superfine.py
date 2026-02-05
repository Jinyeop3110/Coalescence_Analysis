#!/usr/bin/env python
"""
Plot Phase Diagrams for Ablation Studies - SUPERFINE VERSION
High-resolution version with 59 interaction strengths (step 0.02)

This script creates phase diagrams from the ablation study simulation data.
Supports both raw and smoothed phase diagrams.

Usage:
python plot_phase_diagram_ablation_superfine.py
python plot_phase_diagram_ablation_superfine.py --smooth 2.0
python plot_phase_diagram_ablation_superfine.py --ablation gaussian
python plot_phase_diagram_ablation_superfine.py --all
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
    """
    Process JSON simulation data and extract vector decomposition coefficients.
    """
    print(f"Processing JSON simulation data: {session_name}")

    if not Path(json_file_path).exists():
        print(f"Warning: File not found: {json_file_path}")
        return None, None, None, None

    try:
        with open(json_file_path, 'r') as f:
            simulation_data = json.load(f)

        print(f"  Loaded JSON data with {len(simulation_data)} interaction strengths")

        types_to_plot = []
        data1 = {}  # Parent1 coefficients
        data2 = {}  # Parent2 coefficients
        data3 = {}  # Residual magnitudes

        for mu_str, mu_data in simulation_data.items():
            if len(mu_data) == 0:
                continue

            types_to_plot.append(mu_str)
            mu_data1 = []
            mu_data2 = []
            mu_data3 = []

            for rep_key, rep_data in mu_data.items():
                try:
                    sc_list = rep_data.get('sc_list', {})
                    cc_list = rep_data.get('cc_list', {})

                    if not sc_list or not cc_list:
                        continue

                    for cc_key, cmix in cc_list.items():
                        try:
                            parts = cc_key.split('_')
                            c1_key = parts[0]
                            c2_key = parts[1]
                        except:
                            continue

                        c1_key_int = int(c1_key)
                        c2_key_int = int(c2_key)

                        if str(c1_key_int) not in sc_list and c1_key_int not in sc_list:
                            continue
                        if str(c2_key_int) not in sc_list and c2_key_int not in sc_list:
                            continue

                        c1 = np.array(sc_list.get(str(c1_key_int), sc_list.get(c1_key_int, [])))
                        c2 = np.array(sc_list.get(str(c2_key_int), sc_list.get(c2_key_int, [])))
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

        # Sort by numerical mu-value
        try:
            types_to_plot.sort(key=lambda x: float(x))
        except:
            types_to_plot.sort()

        total_points = sum(len(data1.get(t, [])) for t in types_to_plot)
        print(f"  Successfully processed {len(types_to_plot)} interaction strengths, {total_points:,} data points")

        return types_to_plot, data1, data2, data3

    except Exception as e:
        print(f"Error processing {json_file_path}: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None


def plot_ablation_phase_diagram_superfine(session_config, n_reps=400, u_step=0.02):
    """Generate a phase diagram for a single ablation study with superfine resolution."""

    name = session_config['name']
    json_file = session_config['json_file']
    description = session_config.get('description', name)
    output_suffix = session_config['output_suffix']

    print(f"\n{'='*70}")
    print(f"Processing {name}")
    print(f"Description: {description}")
    print(f"{'='*70}")

    if not Path(json_file).exists():
        print(f"  File not found: {json_file}")
        return False

    # Process the JSON simulation data
    types_to_plot, data1, data2, data3 = process_json_simulation_data(json_file, name)

    if types_to_plot is None or len(types_to_plot) == 0:
        print(f"  Skipping {name} due to data processing error or no data")
        return False

    # For superfine data (59 intensities: 0.05 to 1.21 in steps of 0.02)
    expected_mu_values = [f"{mu:.2f}" for mu in np.arange(0.05, 1.20 + u_step, u_step)]
    n_expected = len(expected_mu_values)

    # Custom tick labels: 0.4, 0.8, 1.2
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

    # Pad data to match expected range
    padded_data1, padded_data2, padded_data3 = {}, {}, {}
    for mu in expected_mu_values:
        padded_data1[mu] = data1.get(mu, [])
        padded_data2[mu] = data2.get(mu, [])
        padded_data3[mu] = data3.get(mu, [])

    # Output base for superfine version
    output_base = f"Figure/PhaseDiagram_ablation/Fig_phase_diagram_{output_suffix}_superfine"

    try:
        # Create superfine version
        for fmt in ['svg', 'png', 'pdf']:
            output_filename = f"{output_base}.{fmt}"
            create_phase_diagram(
                expected_mu_values,
                padded_data1, padded_data2, padded_data3,
                custom_x_ticks,
                custom_x_labels,
                output_filename=output_filename,
                plot_boundary=False
            )

        print(f"  Created: {output_base}.[svg,png,pdf]")

        # Also update the non-superfine output files (replace existing plots)
        old_output_base = f"Figure/PhaseDiagram_ablation/Fig_phase_diagram_{output_suffix}"
        for fmt in ['svg', 'png', 'pdf']:
            output_filename = f"{old_output_base}.{fmt}"
            create_phase_diagram(
                expected_mu_values,
                padded_data1, padded_data2, padded_data3,
                custom_x_ticks,
                custom_x_labels,
                output_filename=output_filename,
                plot_boundary=False
            )
        print(f"  Updated: {old_output_base}.[svg,png,pdf] (replaced with superfine data)")

        return True

    except Exception as e:
        print(f"  Failed to create {output_base}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate ablation study phase diagrams (superfine)')
    parser.add_argument('--ablation', type=str, default=None,
                        help='Specific ablation to plot (gaussian, gamma, growth_std01, growth_std02, k_std01, k_std02)')
    parser.add_argument('--all', action='store_true',
                        help='Plot all available ablation studies')
    parser.add_argument('--n_reps', type=int, default=400,
                        help='Number of repetitions (default: 400)')
    parser.add_argument('--step', type=float, default=0.02,
                        help='Step size for interaction strengths (default: 0.02)')
    args = parser.parse_args()

    # Ensure output directory exists
    Path("Figure/PhaseDiagram_ablation").mkdir(parents=True, exist_ok=True)

    # Define all ablation sessions with superfine data paths
    all_sessions = [
        {
            "name": "gaussian",
            "json_file": "Simulation_Data/48species_ablation_gaussian_superfine/Community_ablation_gaussian_superfine.json",
            "description": "Gaussian N(mu, (mu/sqrt(3))^2), CV=0.577",
            "output_suffix": "ablation_gaussian"
        },
        {
            "name": "gamma",
            "json_file": "Simulation_Data/48species_ablation_gamma_superfine/Community_ablation_gamma_superfine.json",
            "description": "Gamma(k=3, theta=mu/3), CV=0.577",
            "output_suffix": "ablation_gamma"
        },
        {
            "name": "growth_std01",
            "json_file": "Simulation_Data/48species_ablation_growth_std01_superfine/Community_ablation_growth_std01_superfine.json",
            "description": "Growth Rate N(1, 0.1^2)",
            "output_suffix": "ablation_growth_std01"
        },
        {
            "name": "growth_std02",
            "json_file": "Simulation_Data/48species_ablation_growth_std02_superfine/Community_ablation_growth_std02_superfine.json",
            "description": "Growth Rate N(1, 0.2^2)",
            "output_suffix": "ablation_growth_std02"
        },
        {
            "name": "k_std01",
            "json_file": "Simulation_Data/48species_ablation_k_std01_superfine/Community_ablation_k_std01_superfine.json",
            "description": "Carrying Capacity N(1, 0.1^2)",
            "output_suffix": "ablation_k_std01"
        },
        {
            "name": "k_std02",
            "json_file": "Simulation_Data/48species_ablation_k_std02_superfine/Community_ablation_k_std02_superfine.json",
            "description": "Carrying Capacity N(1, 0.2^2)",
            "output_suffix": "ablation_k_std02"
        }
    ]

    print("\n" + "="*70)
    print("GENERATING PHASE DIAGRAMS FOR ABLATION STUDIES (SUPERFINE)")
    print("="*70)
    print(f"Expected repetitions: {args.n_reps}")
    print(f"Step size: {args.step}")

    # Check available data
    print("\nChecking available simulation data...")
    available_sessions = []
    for session in all_sessions:
        if Path(session['json_file']).exists():
            try:
                with open(session['json_file'], 'r') as f:
                    data = json.load(f)
                total = sum(len(data[k]) for k in data.keys())
                print(f"  {session['name']}: {total:,} simulations available")
                available_sessions.append(session)
            except:
                print(f"  {session['name']}: File exists but cannot read")
        else:
            print(f"  {session['name']}: Not found")

    if not available_sessions:
        print("\nNo simulation data available. Run simulations first.")
        return

    # Determine which sessions to process
    if args.ablation:
        sessions_to_plot = [s for s in available_sessions if s['name'] == args.ablation]
        if not sessions_to_plot:
            print(f"\nAblation '{args.ablation}' not found or no data available.")
            return
    else:
        sessions_to_plot = available_sessions

    # Generate phase diagrams
    successful = 0
    failed = 0

    for session in sessions_to_plot:
        success = plot_ablation_phase_diagram_superfine(
            session,
            n_reps=args.n_reps,
            u_step=args.step
        )
        if success:
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*70}")
    print("PHASE DIAGRAM GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"Successful plots: {successful}")
    print(f"Failed/Skipped plots: {failed}")
    print(f"Output directory: Figure/PhaseDiagram_ablation/")


if __name__ == "__main__":
    main()
