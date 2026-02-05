#!/usr/bin/env python
"""
Plot Phase Diagrams for Ablation Studies - ANNOTATED VERSION
With vertical lines at mu=0.3, 0.6, 0.8 and percentage annotations.

This script creates phase diagrams with:
- Vertical marker lines at specific mu values (0.3, 0.6, 0.8)
- Percentage annotations showing the fraction of each outcome at those points
- Y-axis labeled as "Coalescence outcome fraction"

Usage:
python plot_phase_diagram_ablation_annotated.py
python plot_phase_diagram_ablation_annotated.py --ablation gaussian
"""

import os
import sys
import json
import argparse
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend - no popup
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

        print(f"  Loaded JSON data with {len(simulation_data)} interaction strengths")

        types_to_plot = []
        data1 = {}
        data2 = {}
        data3 = {}

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
        import traceback
        traceback.print_exc()
        return None, None, None, None


def create_phase_diagram_annotated(
    type_names,
    data1_set,
    data2_set,
    data3_set,
    custom_x_ticks=None,
    custom_x_labels=None,
    output_filename="Fig_phase_diagram_annotated.svg",
    annotation_mu_values=[0.3, 0.6, 0.8],
):
    """
    Creates a stacked-filled bar plot with annotations at specific mu values.

    Parameters:
    - annotation_mu_values: List of mu values where to add vertical lines and % annotations
    """
    n_types = len(type_names)
    class1_fractions = np.zeros(n_types + 1)
    class2_fractions = np.zeros(n_types + 1)
    class3_fractions = np.zeros(n_types + 1)

    colors = get_phase_diagram_colors()  # [dominance, mixing, restructuring]

    # Calculate fractions for each mu value
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

    # Figure setup - SAME SIZE as original create_phase_diagram
    mm = 1 / 25.4 * 72
    fig_width = 60 * mm  # Same as original
    fig_height = 60 * mm

    fig, ax1 = plt.subplots(figsize=(fig_width / 72, fig_height / 72), facecolor='w')

    x_vals = np.arange(n_types + 1)

    # Create stacked area plot
    fill1 = ax1.fill_between(
        x_vals, 0, class1_fractions,
        step='post', color=colors[0], alpha=0.85, edgecolor='none',
        label='Dominance'
    )
    fill2 = ax1.fill_between(
        x_vals, class1_fractions, class1_fractions + class2_fractions,
        step='post', color=colors[1], alpha=0.85, edgecolor='none',
        label='Mixing'
    )
    fill3 = ax1.fill_between(
        x_vals, class1_fractions + class2_fractions,
        class1_fractions + class2_fractions + class3_fractions,
        step='post', color=colors[2], alpha=0.85, edgecolor='none',
        label='Restructuring'
    )

    # Set axis labels
    ax1.set_ylabel('Coalescence outcome fraction')
    ax1.set_xlabel(r'Interaction strength $\mu$')
    ax1.set_xlim([0, n_types])
    ax1.set_ylim([0, 1])

    # Set x-axis ticks
    if custom_x_ticks is not None and custom_x_labels is not None:
        ax1.set_xticks(custom_x_ticks)
        ax1.set_xticklabels(custom_x_labels)

    # Set y-axis ticks
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['0', '1'])

    # Add vertical lines and annotations at specified mu values
    annotation_font_size = 6

    for mu_target in annotation_mu_values:
        # Try multiple string formats to find the matching mu value
        mu_formats = [f"{mu_target:.2f}", f"{mu_target:.1f}", f"{mu_target}"]

        pos = None
        for mu_str in mu_formats:
            if mu_str in type_names:
                pos = type_names.index(mu_str)
                break

        # Also try finding closest match
        if pos is None:
            try:
                type_floats = [float(t) for t in type_names]
                closest_idx = np.argmin(np.abs(np.array(type_floats) - mu_target))
                if np.abs(type_floats[closest_idx] - mu_target) < 0.01:
                    pos = closest_idx
            except:
                pass

        if pos is not None:
            # Get fractions at this position
            dom_frac = class1_fractions[pos]
            mix_frac = class2_fractions[pos]
            rest_frac = class3_fractions[pos]

            # Draw vertical dashed line at the CENTER of the bar
            ax1.axvline(x=pos + 0.5, color='black', linestyle='--', alpha=0.9, linewidth=1.0)

            # Calculate y positions for text (center of each region)
            y_dom = dom_frac / 2
            y_mix = dom_frac + mix_frac / 2
            y_rest = dom_frac + mix_frac + rest_frac / 2

            # Add percentage annotations (only if fraction > 5%)
            x_text = pos + 1.5  # To the right of the line

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

            # Add mu label at top (round to 1 decimal for cleaner display)
            mu_display = round(mu_target, 1)
            ax1.text(pos + 0.5, 1.02, f'$\\mu$={mu_display}',
                    ha='center', va='bottom', fontsize=annotation_font_size,
                    color='black')

            print(f"  mu={mu_target} (pos={pos}): Dominance={dom_frac*100:.1f}%, Mixing={mix_frac*100:.1f}%, Restructuring={rest_frac*100:.1f}%")
        else:
            print(f"  WARNING: mu={mu_target} not found in type_names. Available: {type_names[:5]}...{type_names[-3:]}")

    plt.tight_layout()
    fig.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close(fig)


def plot_ablation_phase_diagram_annotated(session_config, u_step=0.02, annotation_mu=[0.3, 0.6, 0.8]):
    """Generate an annotated phase diagram for a single ablation study."""

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

    # Output files
    output_base = f"Figure/PhaseDiagram_ablation/Fig_phase_diagram_{output_suffix}_annotated"

    try:
        for fmt in ['svg', 'png', 'pdf']:
            output_filename = f"{output_base}.{fmt}"
            create_phase_diagram_annotated(
                expected_mu_values,
                padded_data1, padded_data2, padded_data3,
                custom_x_ticks,
                custom_x_labels,
                output_filename=output_filename,
                annotation_mu_values=annotation_mu
            )

        print(f"  Created: {output_base}.[svg,png,pdf]")
        return True

    except Exception as e:
        print(f"  Failed to create {output_base}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate annotated ablation study phase diagrams')
    parser.add_argument('--ablation', type=str, default=None,
                        help='Specific ablation to plot (gaussian, gamma, growth_std01, growth_std02, k_std01, k_std02)')
    parser.add_argument('--step', type=float, default=0.02,
                        help='Step size for interaction strengths (default: 0.02)')
    parser.add_argument('--mu', type=str, default='0.31,0.61,0.81',
                        help='Comma-separated mu values for annotations (default: 0.31,0.61,0.81 for step=0.02 from 0.05)')
    args = parser.parse_args()

    # Parse annotation mu values
    annotation_mu = [float(x.strip()) for x in args.mu.split(',')]

    # Ensure output directory exists
    Path("Figure/PhaseDiagram_ablation").mkdir(parents=True, exist_ok=True)

    # Define all ablation sessions
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
    print("GENERATING ANNOTATED PHASE DIAGRAMS FOR ABLATION STUDIES")
    print("="*70)
    print(f"Annotation mu values: {annotation_mu}")
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
        success = plot_ablation_phase_diagram_annotated(
            session,
            u_step=args.step,
            annotation_mu=annotation_mu
        )
        if success:
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*70}")
    print("ANNOTATED PHASE DIAGRAM GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f"Successful plots: {successful}")
    print(f"Failed/Skipped plots: {failed}")
    print(f"Output directory: Figure/PhaseDiagram_ablation/")


if __name__ == "__main__":
    main()
