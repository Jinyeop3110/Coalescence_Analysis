"""
Plot phase diagrams for both narrow and wide uniform distributions (20 reps each)
"""

from common_setup import *
from pathlib import Path
import json
import pandas as pd
import numpy as np


def process_json_simulation_data(json_file_path, session_name):
    """
    Process JSON simulation data and extract vector decomposition coefficients.
    """
    print(f"Processing JSON simulation data: {session_name}")

    if not Path(json_file_path).exists():
        print(f"Warning: File not found: {json_file_path}")
        return None, None, None, None

    try:
        # Load JSON data
        with open(json_file_path, 'r') as f:
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
                print(f"    Skipping u = {u_str} (no data)")
                continue

            types_to_plot.append(u_str)

            # Initialize lists for this u-value
            u_data1 = []  # Parent1 coefficients
            u_data2 = []  # Parent2 coefficients
            u_data3 = []  # Residual magnitudes

            # Process each repetition
            processed_reps = 0
            for rep_key, rep_data in u_data.items():
                try:
                    # Get single communities and coalescence results
                    sc_list = rep_data.get('sc_list', {})
                    cc_list = rep_data.get('cc_list', {})

                    if not sc_list or not cc_list:
                        continue

                    # Process each coalescence pair
                    for cc_key, cmix in cc_list.items():
                        # Parse coalescence key (format: "c1_c2", "c1_c3", etc.)
                        try:
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

                            # Store coefficients
                            u_data1.append(u_coeff)
                            u_data2.append(v_coeff)
                            u_data3.append(k_coeff)

                        except Exception as decomp_error:
                            # Handle singular matrix or other decomposition errors
                            continue

                    processed_reps += 1

                except Exception as rep_error:
                    print(f"    Warning: Error processing rep {rep_key}: {rep_error}")
                    continue

            # Store data for this u-value
            data1[u_str] = u_data1
            data2[u_str] = u_data2
            data3[u_str] = u_data3

            print(f"    ✓ Processed {processed_reps} reps, {len(u_data1)} coalescence events")

        print(f"✓ Successfully processed {len(types_to_plot)} interaction strengths")

        # Sort by numerical u-value for proper ordering
        try:
            types_to_plot.sort(key=lambda x: float(x))
        except:
            types_to_plot.sort()  # fallback to string sort

        return types_to_plot, data1, data2, data3

    except Exception as e:
        print(f"Error processing {json_file_path}: {e}")
        return None, None, None, None


def main():
    """Generate phase diagrams for both distributions."""

    print("\n" + "="*70)
    print("GENERATING PHASE DIAGRAMS FOR BOTH DISTRIBUTIONS (20 reps each)")
    print("="*70)
    print("🎨 Using colormap: Red (Dominance), Purple (Mixing), Green (Restructuring)")

    # Ensure output directory exists
    Path("Figure/PhaseDiagram").mkdir(parents=True, exist_ok=True)

    # List of simulation sessions to process
    json_sessions = [
        {
            "name": "20reps_narrow_uniform",
            "json_file": "Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json",
            "description": "20 reps × 24 intensities (0.05-1.2) Narrow Uniform [0.5μ,1.5μ] CV≈0.289",
            "output_suffix": "20reps_narrow_uniform"
        },
        {
            "name": "20reps_wide_uniform",
            "json_file": "Simulation_Data/48species_20reps_wide_uniform/Community_20reps_wide_uniform.json",
            "description": "20 reps × 24 intensities (0.05-1.2) Wide Uniform [0,2μ] CV≈0.577",
            "output_suffix": "20reps_wide_uniform"
        }
    ]

    successful_plots = 0
    failed_plots = 0

    for session in json_sessions:
        print(f"\n{'='*70}")
        print(f"Processing {session['name']}")
        print(f"Description: {session['description']}")
        print(f"{'='*70}")

        # Check if file exists
        if not Path(session['json_file']).exists():
            print(f"⚠️  File not found: {session['json_file']}")
            print(f"   Skipping this session")
            failed_plots += 1
            continue

        # Process the JSON simulation data
        types_to_plot, data1, data2, data3 = process_json_simulation_data(
            session['json_file'], session['name']
        )

        if types_to_plot is None or len(types_to_plot) == 0:
            print(f"✗ Skipping {session['name']} due to data processing error or no data")
            failed_plots += 1
            continue

        # Set up plotting parameters
        expected_u_values = [f"{u:.2f}" for u in np.arange(0.05, 1.25, 0.05)]
        n_expected = len(expected_u_values)  # 24 values

        # Show custom tick labels: 0.4, 0.8, 1.2
        custom_x_ticks = []
        custom_x_labels = []

        target_labels = [0.4, 0.8, 1.2]
        for target in target_labels:
            target_str = f"{target:.2f}"
            if target_str in expected_u_values:
                pos = expected_u_values.index(target_str)
                custom_x_ticks.append(pos)
                custom_x_labels.append(f"{target:.1f}")

        # Add the end position with empty label
        custom_x_ticks.append(n_expected)
        custom_x_labels.append("")

        # Pad data to match expected range
        padded_data1, padded_data2, padded_data3 = {}, {}, {}
        for u in expected_u_values:
            padded_data1[u] = data1.get(u, [])
            padded_data2[u] = data2.get(u, [])
            padded_data3[u] = data3.get(u, [])

        plot_types = expected_u_values
        plot_data1, plot_data2, plot_data3 = padded_data1, padded_data2, padded_data3

        # Generate output filename
        output_filename = f"Figure/PhaseDiagram/Fig_phase_diagram_{session['output_suffix']}.svg"

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

            print(f"✓ Created: {output_filename}")
            successful_plots += 1

            # Print statistics about the data
            total_points = sum(len(data1.get(t, [])) for t in types_to_plot)
            print(f"  Data points processed: {total_points}")

        except Exception as e:
            print(f"✗ Failed to create {output_filename}: {e}")
            import traceback
            traceback.print_exc()
            failed_plots += 1
            continue

    print(f"\n{'='*70}")
    print("PHASE DIAGRAM GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"✓ Successful plots: {successful_plots}")
    print(f"✗ Failed/Skipped plots: {failed_plots}")
    print(f"📁 Output directory: Figure/PhaseDiagram/")

    if successful_plots > 0:
        print(f"\n📊 Generated phase diagrams:")
        for session in json_sessions:
            output_file = f"Fig_phase_diagram_{session['output_suffix']}.svg"
            full_path = f"Figure/PhaseDiagram/{output_file}"
            if Path(full_path).exists():
                file_size = Path(full_path).stat().st_size / 1024
                print(f"  • {session['name']}")
                print(f"    → {output_file} ({file_size:.1f} KB)")
                print(f"    {session['description']}")


if __name__ == "__main__":
    main()
