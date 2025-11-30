#!/usr/bin/env python
"""
Regenerate All Phase Diagrams with Old Classification System

This script regenerates phase diagrams for:
1. 48species_20reps_narrow_uniform
2. 48species_20reps_wide_uniform
3. Natural communities (LN, MN, HN)

All use the OLD asymmetricity-based classification boundaries.
"""

from common_setup import *
from pathlib import Path
import json
import numpy as np

def process_uniform_simulation(json_file, output_name, description):
    """Process narrow/wide uniform simulation data."""

    print(f"\n{'='*70}")
    print(f"Processing {output_name}")
    print(f"Description: {description}")
    print(f"{'='*70}")

    if not Path(json_file).exists():
        print(f"✗ File not found: {json_file}")
        return False

    try:
        # Load JSON data
        with open(json_file, 'r') as f:
            simulation_data = json.load(f)

        print(f"✓ Loaded JSON data with {len(simulation_data)} interaction strengths")

        # Initialize data structures
        types_to_plot = []
        data1 = {}  # Parent1 coefficients
        data2 = {}  # Parent2 coefficients
        data3 = {}  # Residual magnitudes

        # Process each interaction strength
        for u_str, u_data in simulation_data.items():
            print(f"  Processing u = {u_str} ({len(u_data)} repetitions)")

            if len(u_data) == 0:
                continue

            types_to_plot.append(u_str)

            # Initialize lists for this u-value
            u_data1 = []
            u_data2 = []
            u_data3 = []

            # Process each repetition
            for rep_key, rep_data in u_data.items():
                try:
                    sc_list = rep_data.get('sc_list', {})
                    cc_list = rep_data.get('cc_list', {})

                    if not sc_list or not cc_list:
                        continue

                    # Process each coalescence pair
                    for cc_key, cmix in cc_list.items():
                        try:
                            # Parse coalescence key
                            parts = cc_key.split('_')
                            c1_key = parts[0]  # e.g., "c1"
                            c2_key = parts[1]  # e.g., "c2"
                        except:
                            continue

                        # Get parent community data
                        if c1_key not in sc_list or c2_key not in sc_list:
                            continue

                        c1 = np.array(sc_list[c1_key])
                        c2 = np.array(sc_list[c2_key])
                        cmix = np.array(cmix)

                        # Apply vector decomposition
                        try:
                            u_coeff, v_coeff, k_coeff = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
                            u_data1.append(u_coeff)
                            u_data2.append(v_coeff)
                            u_data3.append(k_coeff)
                        except:
                            continue

                except Exception as e:
                    continue

            # Store data for this u-value
            data1[u_str] = u_data1
            data2[u_str] = u_data2
            data3[u_str] = u_data3

            print(f"    ✓ {len(u_data1)} coalescence events")

        # Sort by numerical u-value
        try:
            types_to_plot.sort(key=lambda x: float(x))
        except:
            types_to_plot.sort()

        # Set up x-axis ticks
        custom_x_ticks = np.arange(len(types_to_plot) + 1)
        custom_x_labels = [f"{float(t):.2f}" for t in types_to_plot] + [""]

        # Generate output filename
        output_filename = f"Figure/PhaseDiagram/Fig_phase_diagram_{output_name}.svg"

        # Create the phase diagram
        create_phase_diagram(
            types_to_plot,
            data1, data2, data3,
            custom_x_ticks,
            custom_x_labels,
            output_filename=output_filename,
            plot_boundary=False
        )

        print(f"✓ Created: {output_filename}")

        # Print statistics
        total_points = sum(len(data1.get(t, [])) for t in types_to_plot)
        print(f"  Total data points: {total_points}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def process_natural_communities():
    """Process natural community coalescence data."""

    print(f"\n{'='*70}")
    print(f"Processing natural communities")
    print(f"Media: LN, MN, HN")
    print(f"{'='*70}")

    try:
        data1_set = {}
        data2_set = {}
        data3_set = {}

        type_names = ['LN', 'MN', 'HN']

        # Process natural communities across nutrient levels
        for medium in type_names:
            if medium not in Nat_Coal_IDX:
                print(f"Warning: {medium} not found in Nat_Coal_IDX")
                data1_set[medium] = []
                data2_set[medium] = []
                data3_set[medium] = []
                continue

            IDX_list = Nat_Coal_IDX[medium]

            if len(IDX_list) == 0:
                print(f"Warning: No data found for {medium}")
                data1_set[medium] = []
                data2_set[medium] = []
                data3_set[medium] = []
                continue

            # Get coalescence event indices
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            if len(idx) == 0:
                data1_set[medium] = []
                data2_set[medium] = []
                data3_set[medium] = []
                continue

            # Get parent community indices
            idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1 = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in idx_1])

            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2 = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in idx_2])

            # Get mixed community indices
            idx = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in IDX_list])

            data1 = []
            data2 = []
            data3 = []

            print(f"  Processing {len(idx)} coalescence events for {medium}")

            for i in range(len(idx)):
                try:
                    # Get abundance vectors
                    c_mix = Processed_sequences_natural.iloc[idx[i]].values.tolist()[1:]
                    c_1 = np.array(Processed_sequences_natural.iloc[idx_1[i]].values.tolist()[1:])
                    c_2 = np.array(Processed_sequences_natural.iloc[idx_2[i]].values.tolist()[1:])

                    # Apply threshold filtering
                    c_1 = c_1 * (c_1 > 1e-4)
                    c_2 = c_2 * (c_2 > 1e-4)

                    # Calculate vector decomposition
                    u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                    data1.append(u)
                    data2.append(v)
                    data3.append(k)

                except Exception as e:
                    continue

            data1_set[medium] = data1
            data2_set[medium] = data2
            data3_set[medium] = data3

            print(f"    ✓ {len(data1)} events processed")

        # Set up x-axis ticks and labels
        custom_x_ticks = np.arange(len(type_names) + 1)
        custom_x_labels = type_names + [""]

        # Generate output filename
        output_filename = "Figure/PhaseDiagram/Fig_phase_diagram_natural.svg"

        # Create the phase diagram
        create_phase_diagram(
            type_names,
            data1_set, data2_set, data3_set,
            custom_x_ticks,
            custom_x_labels,
            output_filename=output_filename,
            plot_boundary=False
        )

        print(f"✓ Created: {output_filename}")

        # Print statistics
        total_points = sum(len(data1_set.get(t, [])) for t in type_names)
        print(f"  Total data points: {total_points}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to regenerate all phase diagrams."""

    print("\n" + "="*70)
    print("REGENERATING ALL PHASE DIAGRAMS WITH OLD CLASSIFICATION")
    print("="*70)
    print("Classification: Asymmetricity-based boundaries")
    print("  - Dominance: x² > 0.5 AND y > 0.5")
    print("  - Mixing: x² > 0.5 AND y < 0.5")
    print("  - Restructuring: x² < 0.5")
    print("="*70)

    # Ensure output directory exists
    Path("Figure/PhaseDiagram").mkdir(parents=True, exist_ok=True)

    successful = 0
    failed = 0

    # 1. Narrow uniform distribution
    if process_uniform_simulation(
        "Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json",
        "20reps_narrow_uniform",
        "20 reps, Uniform[0.5μ, 1.5μ], CV≈0.289"
    ):
        successful += 1
    else:
        failed += 1

    # 2. Wide uniform distribution
    if process_uniform_simulation(
        "Simulation_Data/48species_20reps_wide_uniform/Community_20reps_wide_uniform.json",
        "20reps_wide_uniform",
        "20 reps, Uniform[0, 2μ], CV≈0.577"
    ):
        successful += 1
    else:
        failed += 1

    # 3. Natural communities
    if process_natural_communities():
        successful += 1
    else:
        failed += 1

    # Summary
    print(f"\n{'='*70}")
    print("REGENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"📁 Output directory: Figure/PhaseDiagram/")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
