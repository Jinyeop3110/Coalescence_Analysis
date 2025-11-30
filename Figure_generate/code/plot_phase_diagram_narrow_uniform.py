"""
Plot phase diagram for narrow uniform distribution simulations
"""

import numpy as np
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
    create_phase_diagram
)

def process_json_simulation_data(json_file_path, session_name):
    """
    Process JSON simulation data and extract coalescence outcomes

    Returns:
        types_to_plot: dict with u values as keys
        data1, data2, data3: arrays for Dominance, Mixing, Restructuring counts
    """
    print(f"Loading data from: {json_file_path}")

    with open(json_file_path, 'r') as f:
        all_results = json.load(f)

    # Get all u values and sort them
    u_values = sorted([float(u) for u in all_results.keys()])
    print(f"Found {len(u_values)} interaction strengths")

    # Initialize counters for each outcome type
    types_to_plot = {}

    for u in u_values:
        u_key = f"{u:.2f}"
        reps = all_results[u_key]

        # Count outcome types for this u value
        outcome_counts = {0: 0, 1: 0, 2: 0}  # 0=Dominance, 1=Mixing, 2=Restructuring
        total_coalescence_events = 0

        for rep_key, rep_data in reps.items():
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            # Process each coalescence event (pairwise community combination)
            for cc_key, cmix in cc_list.items():
                # Extract community indices from key like "c1_c2"
                parts = cc_key.split('_')
                c1_idx = int(parts[0][1:]) - 1  # Convert "c1" to index 0
                c2_idx = int(parts[1][1:]) - 1  # Convert "c2" to index 1

                c1 = sc_list[f"c{c1_idx+1}"]
                c2 = sc_list[f"c{c2_idx+1}"]

                # Apply vector decomposition
                try:
                    u_coeff, v_coeff, k_coeff = metric_VectorDecomposition_onlyPositive(
                        np.array(c1), np.array(c2), np.array(cmix)
                    )

                    # Calculate asymmetricity
                    assym = calculate_assymetricity(u_coeff, v_coeff)

                    # Characterize the case
                    case_type = characterize_case(u_coeff, v_coeff, k_coeff)

                    outcome_counts[case_type] += 1
                    total_coalescence_events += 1

                except Exception as e:
                    print(f"Warning: Error processing {cc_key} in {rep_key} at u={u}: {e}")
                    continue

        # Store results for this u value
        types_to_plot[u] = {
            'dominance': outcome_counts[0],
            'mixing': outcome_counts[1],
            'restructuring': outcome_counts[2],
            'total': total_coalescence_events
        }

        print(f"u={u:.2f}: Dom={outcome_counts[0]}, Mix={outcome_counts[1]}, "
              f"Rest={outcome_counts[2]}, Total={total_coalescence_events}")

    # Prepare data for plotting
    data1 = np.array([types_to_plot[u]['dominance'] for u in u_values])
    data2 = np.array([types_to_plot[u]['mixing'] for u in u_values])
    data3 = np.array([types_to_plot[u]['restructuring'] for u in u_values])

    return types_to_plot, data1, data2, data3


def main():
    print("="*70)
    print("Phase Diagram Generation - Narrow Uniform Distribution")
    print("Distribution: Uniform[mean*0.5, mean*1.5]")
    print("Theoretical CV: 0.289 (vs 0.577 for wide uniform)")
    print("="*70)

    # Input file
    json_file = "Simulation_Data/48species_10reps_narrow_uniform/Community_10reps_narrow_uniform.json"

    if not os.path.exists(json_file):
        print(f"ERROR: File not found: {json_file}")
        return

    # Process data
    types_to_plot, data1, data2, data3 = process_json_simulation_data(
        json_file,
        "narrow_uniform_10reps"
    )

    # Create output directory
    output_dir = "Figure/PhaseDiagram"
    os.makedirs(output_dir, exist_ok=True)

    # Generate phase diagram
    output_file = os.path.join(output_dir, "Fig_phase_diagram_narrow_uniform_10reps.svg")

    print("\n" + "="*70)
    print("Creating phase diagram...")

    create_phase_diagram(
        types_to_plot=types_to_plot,
        data1=data1,
        data2=data2,
        data3=data3,
        output_file=output_file,
        title="Phase Diagram: Narrow Uniform [0.5μ, 1.5μ] (CV≈0.289)"
    )

    print(f"✓ Phase diagram saved to: {output_file}")
    print("="*70)

    # Print summary statistics
    print("\nSummary Statistics:")
    print("-" * 70)
    total_dom = np.sum(data1)
    total_mix = np.sum(data2)
    total_rest = np.sum(data3)
    total_all = total_dom + total_mix + total_rest

    print(f"Total Dominance events:     {total_dom:4d} ({100*total_dom/total_all:.1f}%)")
    print(f"Total Mixing events:        {total_mix:4d} ({100*total_mix/total_all:.1f}%)")
    print(f"Total Restructuring events: {total_rest:4d} ({100*total_rest/total_all:.1f}%)")
    print(f"Total events:               {total_all:4d}")
    print("="*70)


if __name__ == "__main__":
    main()
