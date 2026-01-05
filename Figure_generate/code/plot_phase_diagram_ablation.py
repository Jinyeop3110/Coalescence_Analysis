#!/usr/bin/env python
"""
Plot Phase Diagrams for Ablation Studies (Gaussian and Gamma Distributions)

This script creates phase diagrams from the ablation study simulation data.
Both distributions have CV = 1/sqrt(3) ≈ 0.577.

Inputs:
- Simulation_Data/48species_ablation_gaussian/Community_ablation_gaussian.json
- Simulation_Data/48species_ablation_gamma/Community_ablation_gamma.json

Outputs:
- Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_gaussian.svg
- Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_gamma.svg

Usage:
python plot_phase_diagram_ablation.py
"""

from common_setup import *
from pathlib import Path
import json
import pandas as pd
import numpy as np


def process_json_simulation_data(json_file_path, session_name):
    """
    Process JSON simulation data and extract vector decomposition coefficients.

    Parameters:
    json_file_path: Path to the JSON file with simulation data
    session_name: Name of the simulation session

    Returns:
    types_to_plot: List of mu-values (mean interaction strengths)
    data1: Parent1 coefficients
    data2: Parent2 coefficients
    data3: Residual magnitudes
    """

    print(f"Processing JSON simulation data: {session_name}")

    if not Path(json_file_path).exists():
        print(f"Warning: File not found: {json_file_path}")
        return None, None, None, None

    try:
        # Load JSON data
        with open(json_file_path, 'r') as f:
            simulation_data = json.load(f)

        print(f"  Loaded JSON data with {len(simulation_data)} interaction strengths")

        # Initialize data structures
        types_to_plot = []
        data1 = {}  # Parent1 coefficients
        data2 = {}  # Parent2 coefficients
        data3 = {}  # Residual magnitudes

        # Process each interaction strength
        for mu_str, mu_data in simulation_data.items():
            if len(mu_data) == 0:
                print(f"    Skipping mu = {mu_str} (no data)")
                continue

            types_to_plot.append(mu_str)

            # Initialize lists for this mu-value
            mu_data1 = []  # Parent1 coefficients
            mu_data2 = []  # Parent2 coefficients
            mu_data3 = []  # Residual magnitudes

            # Process each repetition
            processed_reps = 0
            for rep_key, rep_data in mu_data.items():
                try:
                    # Get single communities and coalescence results
                    sc_list = rep_data.get('sc_list', {})
                    cc_list = rep_data.get('cc_list', {})

                    if not sc_list or not cc_list:
                        continue

                    # Process each coalescence pair
                    for cc_key, cmix in cc_list.items():
                        try:
                            parts = cc_key.split('_')
                            c1_key = parts[0]
                            c2_key = parts[1]
                        except:
                            continue

                        # Get parent community data (keys are integers in sc_list)
                        c1_key_int = int(c1_key)
                        c2_key_int = int(c2_key)

                        if str(c1_key_int) not in sc_list and c1_key_int not in sc_list:
                            continue
                        if str(c2_key_int) not in sc_list and c2_key_int not in sc_list:
                            continue

                        # Handle both string and int keys
                        c1 = np.array(sc_list.get(str(c1_key_int), sc_list.get(c1_key_int, [])))
                        c2 = np.array(sc_list.get(str(c2_key_int), sc_list.get(c2_key_int, [])))
                        cmix = np.array(cmix)

                        # Apply vector decomposition
                        try:
                            u_coeff, v_coeff, k_coeff = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)

                            # Store coefficients
                            mu_data1.append(u_coeff)
                            mu_data2.append(v_coeff)
                            mu_data3.append(k_coeff)

                        except Exception as decomp_error:
                            continue

                    processed_reps += 1

                except Exception as rep_error:
                    continue

            # Store data for this mu-value
            data1[mu_str] = mu_data1
            data2[mu_str] = mu_data2
            data3[mu_str] = mu_data3

            print(f"    mu = {mu_str}: {len(mu_data1)} coalescence events")

        print(f"  Successfully processed {len(types_to_plot)} interaction strengths")

        # Sort by numerical mu-value for proper ordering
        try:
            types_to_plot.sort(key=lambda x: float(x))
        except:
            types_to_plot.sort()

        return types_to_plot, data1, data2, data3

    except Exception as e:
        print(f"Error processing {json_file_path}: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None


def plot_ablation_phase_diagrams():
    """Generate phase diagrams for ablation study simulations."""

    print("\n" + "="*70)
    print("GENERATING PHASE DIAGRAMS FOR ABLATION STUDIES")
    print("="*70)

    # List of simulation sessions to process
    ablation_sessions = [
        {
            "name": "gaussian",
            "json_file": "Simulation_Data/48species_ablation_gaussian/Community_ablation_gaussian.json",
            "description": "Gaussian N(mu, (mu/sqrt(3))^2), CV=0.577",
            "output_suffix": "ablation_gaussian"
        },
        {
            "name": "gamma",
            "json_file": "Simulation_Data/48species_ablation_gamma/Community_ablation_gamma.json",
            "description": "Gamma(k=3, theta=mu/3), CV=0.577",
            "output_suffix": "ablation_gamma"
        }
    ]

    successful_plots = 0
    failed_plots = 0

    for session in ablation_sessions:
        print(f"\n{'='*70}")
        print(f"Processing {session['name']} distribution")
        print(f"Description: {session['description']}")
        print(f"{'='*70}")

        # Check if file exists
        if not Path(session['json_file']).exists():
            print(f"  File not found: {session['json_file']}")
            print(f"  Run simulation first: python run_ablation_{session['name']}.py")
            failed_plots += 1
            continue

        # Process the JSON simulation data
        types_to_plot, data1, data2, data3 = process_json_simulation_data(
            session['json_file'], session['name']
        )

        if types_to_plot is None or len(types_to_plot) == 0:
            print(f"  Skipping {session['name']} due to data processing error or no data")
            failed_plots += 1
            continue

        # Set up plotting parameters
        # For fine interval data (24 intensities: 0.05 to 1.2 in steps of 0.05)
        expected_mu_values = [f"{mu:.2f}" for mu in np.arange(0.05, 1.25, 0.05)]
        n_expected = len(expected_mu_values)  # 24 values

        # Show custom tick labels: 0.4, 0.8, 1.2
        custom_x_ticks = []
        custom_x_labels = []

        target_labels = [0.4, 0.8, 1.2]
        for target in target_labels:
            target_str = f"{target:.2f}"
            if target_str in expected_mu_values:
                pos = expected_mu_values.index(target_str)
                custom_x_ticks.append(pos)
                custom_x_labels.append(f"{target:.1f}")

        # Add the end position with empty label
        custom_x_ticks.append(n_expected)
        custom_x_labels.append("")

        # Pad data to match expected range
        padded_data1, padded_data2, padded_data3 = {}, {}, {}
        for mu in expected_mu_values:
            padded_data1[mu] = data1.get(mu, [])
            padded_data2[mu] = data2.get(mu, [])
            padded_data3[mu] = data3.get(mu, [])

        plot_types = expected_mu_values
        plot_data1, plot_data2, plot_data3 = padded_data1, padded_data2, padded_data3

        # Generate output filename
        output_filename = f"Figure/PhaseDiagram_ablation/Fig_phase_diagram_{session['output_suffix']}.svg"

        try:
            # Create the phase diagram
            create_phase_diagram(
                plot_types,
                plot_data1, plot_data2, plot_data3,
                custom_x_ticks,
                custom_x_labels,
                output_filename=output_filename,
                plot_boundary=False
            )

            print(f"  Created: {output_filename}")
            successful_plots += 1

            # Print statistics about the data
            total_points = sum(len(data1.get(t, [])) for t in types_to_plot)
            print(f"  Data points processed: {total_points}")

        except Exception as e:
            print(f"  Failed to create {output_filename}: {e}")
            import traceback
            traceback.print_exc()
            failed_plots += 1
            continue

    print(f"\n{'='*70}")
    print("PHASE DIAGRAM GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"Successful plots: {successful_plots}")
    print(f"Failed/Skipped plots: {failed_plots}")
    print(f"Output directory: Figure/PhaseDiagram_ablation/")


def main():
    """Main function to run the phase diagram generation."""

    # Ensure output directory exists
    Path("Figure/PhaseDiagram_ablation").mkdir(parents=True, exist_ok=True)

    # Check current simulation data availability
    print("Checking available simulation data...")

    # Check Gaussian data
    json_gaussian = "Simulation_Data/48species_ablation_gaussian/Community_ablation_gaussian.json"
    if Path(json_gaussian).exists():
        try:
            with open(json_gaussian, 'r') as f:
                data_gaussian = json.load(f)
            total_gaussian = sum(len(data_gaussian[mu_key]) for mu_key in data_gaussian.keys())
            print(f"  Gaussian data: {total_gaussian} simulations available")
        except:
            print(f"  Gaussian data: File exists but cannot read")
    else:
        print(f"  Gaussian data: Not found (run run_ablation_gaussian.py first)")

    # Check Gamma data
    json_gamma = "Simulation_Data/48species_ablation_gamma/Community_ablation_gamma.json"
    if Path(json_gamma).exists():
        try:
            with open(json_gamma, 'r') as f:
                data_gamma = json.load(f)
            total_gamma = sum(len(data_gamma[mu_key]) for mu_key in data_gamma.keys())
            print(f"  Gamma data: {total_gamma} simulations available")
        except:
            print(f"  Gamma data: File exists but cannot read")
    else:
        print(f"  Gamma data: Not found (run run_ablation_gamma.py first)")

    print()

    # Generate phase diagrams with available data
    plot_ablation_phase_diagrams()


if __name__ == "__main__":
    main()
