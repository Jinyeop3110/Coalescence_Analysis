#!/usr/bin/env python3
"""
plot_assembly_effect_separate_pies.py

Modified from plot_assembly_effect_simulation.py to generate 10 separate pie chart figures
instead of one combined figure.

Generates:
- 5 coalescence pie charts (one per interaction strength: 0.2, 0.4, 0.6, 0.8, 1.0)
- 5 direct assembly pie charts (one per interaction strength)

Total: 10 separate SVG files

Output directory: Figure/Assembly_effect_simulation/
"""

from common_setup import *
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import json
from COLORMAP import get_phase_diagram_colors

# Create output directory
output_dir = Path("Figure/Assembly_effect_simulation")
output_dir.mkdir(parents=True, exist_ok=True)

# Interaction strengths to analyze
INTERACTION_STRENGTHS = [0.2, 0.4, 0.6, 0.8, 1.0]


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """Vector decomposition to get (u, v, k) components"""
    def normalize(vec):
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    u = normalize(u)
    v = normalize(v)
    m = normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))

    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)

    orthogonal_vec = m - (e12[0]*u) - (e12[1]*v)
    x3 = np.linalg.norm(orthogonal_vec)
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2 + 1e-10))

    return convert*x1, convert*x2, x3


def classify_outcome(u, v, k):
    """
    Classify outcome into Dominance, Mixing, or Restructuring.
    Returns: 0 (Dominance), 1 (Mixing), 2 (Restructuring)
    """
    x = np.sqrt(u**2 + v**2)
    y = np.abs(np.abs(np.arctan(u / (v + 1e-8))) - np.pi/4) / (np.pi/4)

    if (x**2 > 0.5) * (y > 0.5):
        return 0  # Dominance
    elif (x**2 > 0.5) * (y < 0.5):
        return 1  # Mixing
    elif (x**2 < 0.5):
        return 2  # Restructuring
    else:
        return 1  # Default to mixing


def analyze_simulation_data(coalescence_file, direct_file):
    """
    Analyze both coalescence and direct assembly simulation data.

    Returns:
    --------
    dict with keys for each interaction strength, containing:
        - 'coalescence': {outcomes, u_values, v_values}
        - 'direct': {outcomes, u_values, v_values}
    """
    print("\n=== Loading Simulation Data ===")

    with open(coalescence_file, 'r') as f:
        coal_data = json.load(f)

    with open(direct_file, 'r') as f:
        direct_data = json.load(f)

    print(f"Loaded coalescence data: {len(coal_data)} combinations")
    print(f"Loaded direct assembly data: {len(direct_data)} combinations")

    results = {}

    for mean_val in INTERACTION_STRENGTHS:
        key = str(mean_val)

        results[mean_val] = {
            'coalescence': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0,
                           'u_values': [], 'v_values': []},
            'direct': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0,
                      'u_values': [], 'v_values': []}
        }

        # Process coalescence data - aggregate across all std values for this mean
        for combo_key in coal_data.keys():
            if f'mean{mean_val:.2f}_' not in combo_key:
                continue

            combo = coal_data[combo_key]
            for rep_key in combo.keys():
                rep_data = combo[rep_key]

                # Get c1, c2 from single communities and c1_c2 from coalescence
                c1 = np.array(rep_data['sc_list']['c1'])
                c2 = np.array(rep_data['sc_list']['c2'])
                c_mix = np.array(rep_data['cc_list']['c1_c2'])

                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)

                    if not (np.isnan(u) or np.isnan(v) or np.isnan(k)):
                        # Classify
                        outcome = classify_outcome(u, v, k)
                        if outcome == 0:
                            results[mean_val]['coalescence']['Dominance'] += 1
                        elif outcome == 1:
                            results[mean_val]['coalescence']['Mixing'] += 1
                        else:
                            results[mean_val]['coalescence']['Restructuring'] += 1

                        # Store u, v for plotting
                        results[mean_val]['coalescence']['u_values'].append(u)
                        results[mean_val]['coalescence']['v_values'].append(v)
                except:
                    continue

        # Process direct assembly data - aggregate across all std values for this mean
        for combo_key in direct_data.keys():
            if f'mean{mean_val:.2f}_' not in combo_key:
                continue

            combo = direct_data[combo_key]
            for rep_key in combo.keys():
                rep_data = combo[rep_key]

                # For direct assembly, we still have c1 and c2 as single communities
                # but c1_c2 is the direct assembly result
                c1 = np.array(rep_data['sc_list']['c1'])
                c2 = np.array(rep_data['sc_list']['c2'])
                c_direct = np.array(rep_data['cc_list']['c1_c2'])

                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, c_direct)

                    if not (np.isnan(u) or np.isnan(v) or np.isnan(k)):
                        # Classify
                        outcome = classify_outcome(u, v, k)
                        if outcome == 0:
                            results[mean_val]['direct']['Dominance'] += 1
                        elif outcome == 1:
                            results[mean_val]['direct']['Mixing'] += 1
                        else:
                            results[mean_val]['direct']['Restructuring'] += 1

                        # Store u, v for plotting
                        results[mean_val]['direct']['u_values'].append(u)
                        results[mean_val]['direct']['v_values'].append(v)
                except:
                    continue

    return results


def plot_single_pie_chart(counts, mean_val, method_name, output_dir):
    """
    Create a single pie chart for one interaction strength and method.

    Parameters:
    -----------
    counts : list
        [Dominance_count, Mixing_count, Restructuring_count]
    mean_val : float
        Interaction strength (e.g., 0.2, 0.4, 0.6, 0.8, 1.0)
    method_name : str
        'coalescence' or 'direct'
    output_dir : Path
        Output directory
    """
    mm = 1 / 25.4
    fig, ax = plt.subplots(1, 1, figsize=(50*mm, 50*mm), facecolor='w', edgecolor='k')

    colors = get_phase_diagram_colors()  # Use standardized phase diagram colors
    labels = ['Dominance', 'Mixing', 'Restructuring']

    total = sum(counts)

    if total > 0:
        ax.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 8})

        if method_name == 'coalescence':
            title = f'Coalescence\nμ={mean_val}\n(n={total})'
        else:
            title = f'Direct Assembly\nμ={mean_val}\n(n={total})'

        ax.set_title(title, fontsize=9, fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center',
                transform=ax.transAxes)
        if method_name == 'coalescence':
            ax.set_title(f'Coalescence μ={mean_val}', fontsize=9)
        else:
            ax.set_title(f'Direct Assembly μ={mean_val}', fontsize=9)

    plt.tight_layout()

    # Create filename
    method_short = 'coal' if method_name == 'coalescence' else 'direct'
    output_file = output_dir / f"Fig_assembly_effect_{method_short}_u{mean_val}.svg"

    try:
        fig.savefig(str(output_file), format='svg', dpi=300, bbox_inches='tight')
        print(f"  ✓ Created: {output_file.name}")
    except Exception as e:
        print(f"  ✗ ERROR saving {output_file}: {e}")
    finally:
        plt.close()

    return output_file


def main():
    print("="*70)
    print("Assembly Effect Analysis - Separate Pie Charts")
    print("="*70)
    print("Generating 10 separate figures (5 coalescence + 5 direct)")

    # File paths
    coalescence_file = "Simulation_Data/coalescence_vs_direct_50reps/Community_coalescence_50reps.json"
    direct_file = "Simulation_Data/coalescence_vs_direct_50reps/Community_direct_50reps.json"

    # Check if files exist
    if not Path(coalescence_file).exists():
        print(f"ERROR: Coalescence file not found: {coalescence_file}")
        return
    if not Path(direct_file).exists():
        print(f"ERROR: Direct assembly file not found: {direct_file}")
        return

    # Analyze data
    results = analyze_simulation_data(coalescence_file, direct_file)

    # Generate separate pie charts
    print("\n=== Generating Separate Pie Charts ===")

    files_created = []

    for mean_val in INTERACTION_STRENGTHS:
        # Coalescence pie chart
        coal_counts = [results[mean_val]['coalescence']['Dominance'],
                      results[mean_val]['coalescence']['Mixing'],
                      results[mean_val]['coalescence']['Restructuring']]

        output_file = plot_single_pie_chart(coal_counts, mean_val, 'coalescence', output_dir)
        files_created.append(output_file.name)

        # Direct assembly pie chart
        direct_counts = [results[mean_val]['direct']['Dominance'],
                        results[mean_val]['direct']['Mixing'],
                        results[mean_val]['direct']['Restructuring']]

        output_file = plot_single_pie_chart(direct_counts, mean_val, 'direct', output_dir)
        files_created.append(output_file.name)

    print("\n" + "="*70)
    print("✓✓✓ PLOTTING COMPLETE! ✓✓✓")
    print("="*70)
    print(f"\nOutput directory: {output_dir}/")
    print(f"\nGenerated {len(files_created)} separate pie chart files:")
    for filename in sorted(files_created):
        print(f"  - {filename}")


if __name__ == "__main__":
    main()
