"""
plot_interaction_strength_pie_charts.py

Purpose: Generate pie charts for coalescence outcomes at specific interaction strengths
Key features:
- Processes simulation data for u = 0.3, 0.6, 0.8
- Creates pie charts showing Dominance, Mixing, and Restructuring distributions
- Saves to VectorDecomp_sim_heatmaps_moresamples directory
- Uses standardized phase diagram colors from COLORMAP.py

Data Source:
- Simulation_Data/48species_100reps_final/Community_100reps_final.json

Outputs:
- Figure/VectorDecomp_sim_heatmaps_moresamples/pie_u0.3.svg
- Figure/VectorDecomp_sim_heatmaps_moresamples/pie_u0.6.svg
- Figure/VectorDecomp_sim_heatmaps_moresamples/pie_u0.8.svg
- Figure/VectorDecomp_sim_heatmaps_moresamples/pie_comparison_3panel.svg
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from COLORMAP import get_phase_diagram_colors


def normalize(v):
    """Normalize a vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """
    Vector decomposition metric (from common_setup.py).
    Returns u_component, v_component, restructuring_component.
    """
    u = normalize(np.array(u))
    v = normalize(np.array(v))
    m = normalize(np.array(m))

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])
    e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))

    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)

    # Calculate orthogonal component (restructured community vector)
    orthogonal_vec = m - (e12[0]*u) - (e12[1]*v)
    x3 = np.linalg.norm(orthogonal_vec)
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2 + 1e-10))

    return convert*x1, convert*x2, x3


def classify_outcome(u, v, k):
    """
    Classify coalescence outcome based on (u, v, k) coordinates.

    Returns:
    - 0: Dominance
    - 1: Mixing
    - 2: Restructuring
    """
    x = np.sqrt(u**2 + v**2)
    y = np.abs(np.abs(np.arctan(u/(v + 1e-8))) - np.pi/4) / (np.pi/4)

    if (x**2 > 0.5) * (y > 0.5):
        return 0  # Dominance
    elif (x**2 > 0.5) * (y < 0.5):
        return 1  # Mixing
    elif (x**2 < 0.5):
        return 2  # Restructuring

    return 2  # Default to restructuring if unclear


def process_interaction_strength(data, interaction_strength):
    """
    Process all coalescence events for a given interaction strength.

    Parameters:
    -----------
    data : dict
        Full simulation data loaded from JSON
    interaction_strength : float
        Interaction strength to process (0.3, 0.5, or 0.8)

    Returns:
    --------
    dict with keys 'Dominance', 'Mixing', 'Restructuring', 'total'
    """
    strength_key = str(interaction_strength)

    if strength_key not in data:
        print(f"Warning: Interaction strength {interaction_strength} not found in data")
        return None

    dominance_count = 0
    mixing_count = 0
    restructuring_count = 0
    total_events = 0

    # Process all replicates for this interaction strength
    for rep_key, rep_data in data[strength_key].items():
        if not rep_key.startswith('rep_'):
            continue

        sc_list = rep_data['sc_list']
        cc_list = rep_data['cc_list']

        # Process all coalescence pairs
        for cc_key, cc_final in cc_list.items():
            # Parse community indices from key like "0_1"
            parts = cc_key.split('_')
            c1_key = parts[0]
            c2_key = parts[1]

            c1_final = sc_list[c1_key]
            c2_final = sc_list[c2_key]

            try:
                # Calculate vector decomposition
                u, v, k = metric_VectorDecomposition_onlyPositive(
                    c1_final, c2_final, cc_final
                )

                # Classify outcome
                outcome = classify_outcome(u, v, k)

                if outcome == 0:
                    dominance_count += 1
                elif outcome == 1:
                    mixing_count += 1
                elif outcome == 2:
                    restructuring_count += 1

                total_events += 1

            except Exception as e:
                # Skip if vector decomposition fails
                continue

    return {
        'Dominance': dominance_count,
        'Mixing': mixing_count,
        'Restructuring': restructuring_count,
        'total': total_events
    }


def create_single_pie_chart(outcome_data, interaction_strength, output_filename):
    """
    Create a single pie chart for one interaction strength.

    Parameters:
    -----------
    outcome_data : dict
        Dictionary with Dominance, Mixing, Restructuring counts
    interaction_strength : float
        Interaction strength value (for title)
    output_filename : str
        Full path to save the figure
    """
    colors = get_phase_diagram_colors()

    values = [outcome_data['Dominance'], outcome_data['Mixing'], outcome_data['Restructuring']]
    total = outcome_data['total']

    # Create figure
    fig, ax = plt.subplots(figsize=(6, 6))

    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,
        colors=colors,
        autopct=lambda pct: f'{int(pct*total/100)} / {total}' if pct > 0 else '',
        startangle=90,
        pctdistance=0.7
    )

    # Style wedges (make them slightly transparent)
    for wedge in wedges:
        wedge.set_alpha(0.85)

    # Style percentage text
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(16)
        autotext.set_fontweight('bold')

    # Add title
    ax.set_title(f'Coalescence Outcomes\nInteraction Strength u = {interaction_strength}',
                 fontsize=14, fontweight='bold', pad=20)

    # Add total count
    ax.text(0, -1.2, f'n = {total}', ha='center', fontsize=12)

    # Save figure
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_filename}")

    # Print statistics
    print(f"    Dominance: {outcome_data['Dominance']} ({outcome_data['Dominance']/total*100:.1f}%)")
    print(f"    Mixing: {outcome_data['Mixing']} ({outcome_data['Mixing']/total*100:.1f}%)")
    print(f"    Restructuring: {outcome_data['Restructuring']} ({outcome_data['Restructuring']/total*100:.1f}%)")


def create_comparison_3panel(all_outcome_data, interaction_strengths, output_filename):
    """
    Create 3-panel comparison plot showing all three interaction strengths.

    Parameters:
    -----------
    all_outcome_data : list of dict
        List of outcome dictionaries for each interaction strength
    interaction_strengths : list
        List of interaction strength values
    output_filename : str
        Full path to save the figure
    """
    colors = get_phase_diagram_colors()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for idx, (outcome_data, u_val, ax) in enumerate(zip(all_outcome_data, interaction_strengths, axes)):
        values = [outcome_data['Dominance'], outcome_data['Mixing'], outcome_data['Restructuring']]
        total = outcome_data['total']

        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,
            colors=colors,
            autopct=lambda pct: f'{int(pct*total/100)}' if pct > 0 else '',
            startangle=90,
            pctdistance=0.7
        )

        # Style wedges
        for wedge in wedges:
            wedge.set_alpha(0.85)

        # Style text
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')

        # Add title
        ax.set_title(f'u = {u_val}\nn = {total}', fontsize=14, fontweight='bold', pad=10)

    plt.tight_layout()

    # Save
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created comparison: {output_filename}")


def main():
    """Main function to generate all pie charts."""

    print("="*70)
    print("GENERATING PIE CHARTS FOR INTERACTION STRENGTHS u = 0.3, 0.6, 0.8")
    print("="*70)

    # Load simulation data
    data_file = "Simulation_Data/48species_100reps_final/Community_100reps_final.json"
    print(f"\nLoading data from: {data_file}")

    with open(data_file, 'r') as f:
        data = json.load(f)

    print("✓ Data loaded successfully")

    # Define interaction strengths to process
    interaction_strengths = [0.3, 0.6, 0.8]

    # Create output directory
    output_dir = Path("Figure/VectorDecomp_sim_heatmaps_moresamples")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each interaction strength
    all_outcome_data = []

    for u_val in interaction_strengths:
        print(f"\n{'='*70}")
        print(f"Processing u = {u_val}")
        print(f"{'='*70}")

        outcome_data = process_interaction_strength(data, u_val)

        if outcome_data is None:
            print(f"✗ Failed to process u = {u_val}")
            continue

        all_outcome_data.append(outcome_data)

        # Create individual pie chart
        output_filename = output_dir / f"pie_u{u_val}.svg"
        create_single_pie_chart(outcome_data, u_val, output_filename)

    # Create comparison 3-panel plot
    print(f"\n{'='*70}")
    print("Creating 3-panel comparison plot")
    print(f"{'='*70}")

    output_filename = output_dir / "pie_comparison_3panel.svg"
    create_comparison_3panel(all_outcome_data, interaction_strengths, output_filename)

    print("\n" + "="*70)
    print("PIE CHART GENERATION COMPLETE!")
    print("="*70)
    print(f"\nGenerated files in {output_dir}/:")
    for u_val in interaction_strengths:
        print(f"  • pie_u{u_val}.svg")
    print(f"  • pie_comparison_3panel.svg")
    print("="*70)


if __name__ == "__main__":
    main()
