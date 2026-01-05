#!/usr/bin/env python3
"""
plot_assembly_effect_simulation.py

Purpose: Generate assembly effect plots for simulation data comparing
         coalescence vs direct assembly methods.

Generates:
1. Pie charts comparing outcome distributions (Dominance/Mixing/Restructuring)
2. Theta (polarized) plots showing (u, v) coordinates for different interaction strengths

Uses data from:
- Simulation_Data/coalescence_vs_direct_50reps/Community_coalescence_50reps.json
- Simulation_Data/coalescence_vs_direct_50reps/Community_direct_50reps.json

Output directory: Figure/Assembly_effect_simulation/

Interaction strengths to plot: 0.2, 0.4, 0.6, 0.8, 1.0
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
        print(f"\nProcessing mean interaction strength = {mean_val}")

        results[mean_val] = {
            'coalescence': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0,
                          'u_values': [], 'v_values': []},
            'direct': {'Dominance': 0, 'Mixing': 0, 'Restructuring': 0,
                      'u_values': [], 'v_values': []}
        }

        # Process coalescence data
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

        # Process direct assembly data
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

        # Print summary
        coal_total = (results[mean_val]['coalescence']['Dominance'] +
                     results[mean_val]['coalescence']['Mixing'] +
                     results[mean_val]['coalescence']['Restructuring'])
        direct_total = (results[mean_val]['direct']['Dominance'] +
                       results[mean_val]['direct']['Mixing'] +
                       results[mean_val]['direct']['Restructuring'])

        print(f"  Coalescence: {coal_total} events")
        print(f"    Dominance: {results[mean_val]['coalescence']['Dominance']}")
        print(f"    Mixing: {results[mean_val]['coalescence']['Mixing']}")
        print(f"    Restructuring: {results[mean_val]['coalescence']['Restructuring']}")

        print(f"  Direct: {direct_total} events")
        print(f"    Dominance: {results[mean_val]['direct']['Dominance']}")
        print(f"    Mixing: {results[mean_val]['direct']['Mixing']}")
        print(f"    Restructuring: {results[mean_val]['direct']['Restructuring']}")

    return results


def plot_pie_charts(results, output_dir):
    """Create pie charts comparing coalescence vs direct assembly outcomes"""

    print("\n=== Generating Pie Charts ===")

    n_strengths = len(INTERACTION_STRENGTHS)

    fig, axes = plt.subplots(2, n_strengths, figsize=(10, 5),
                            facecolor='w', edgecolor='k')

    colors = get_phase_diagram_colors()  # Use standardized phase diagram colors

    for idx, mean_val in enumerate(INTERACTION_STRENGTHS):
        # Coalescence (top row)
        ax_coal = axes[0, idx]
        coal_counts = [results[mean_val]['coalescence']['Dominance'],
                      results[mean_val]['coalescence']['Mixing'],
                      results[mean_val]['coalescence']['Restructuring']]
        total_coal = sum(coal_counts)

        if total_coal > 0:
            wedges, texts, autotexts = ax_coal.pie(
                coal_counts,
                labels=None,
                colors=colors,
                autopct=lambda pct: f'{pct:.0f}%' if pct > 0 else '',
                startangle=90,
                pctdistance=0.6,
                wedgeprops={'linewidth': 0.5, 'edgecolor': 'white'}
            )
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontsize(9)
            ax_coal.text(0, -1.25, f'n={total_coal}', ha='center', fontsize=9)
            ax_coal.set_title(f'μ={mean_val}', fontsize=11, fontweight='bold', pad=8)
        else:
            ax_coal.text(0.5, 0.5, 'No data', ha='center', va='center',
                        transform=ax_coal.transAxes, fontsize=10)
            ax_coal.set_title(f'μ={mean_val}', fontsize=11, fontweight='bold', pad=8)

        # Direct assembly (bottom row)
        ax_direct = axes[1, idx]
        direct_counts = [results[mean_val]['direct']['Dominance'],
                        results[mean_val]['direct']['Mixing'],
                        results[mean_val]['direct']['Restructuring']]
        total_direct = sum(direct_counts)

        if total_direct > 0:
            wedges, texts, autotexts = ax_direct.pie(
                direct_counts,
                labels=None,
                colors=colors,
                autopct=lambda pct: f'{pct:.0f}%' if pct > 0 else '',
                startangle=90,
                pctdistance=0.6,
                wedgeprops={'linewidth': 0.5, 'edgecolor': 'white'}
            )
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontsize(9)
            ax_direct.text(0, -1.25, f'n={total_direct}', ha='center', fontsize=9)
        else:
            ax_direct.text(0.5, 0.5, 'No data', ha='center', va='center',
                          transform=ax_direct.transAxes, fontsize=10)

    # Add row labels on the left side
    axes[0, 0].text(-0.35, 0.5, 'Coalescence', rotation=90, fontsize=11,
                   fontweight='bold', va='center', ha='center',
                   transform=axes[0, 0].transAxes)
    axes[1, 0].text(-0.35, 0.5, 'Direct Assembly', rotation=90, fontsize=11,
                   fontweight='bold', va='center', ha='center',
                   transform=axes[1, 0].transAxes)

    # Add legend with CLS instead of Dominance
    fig.legend(
        labels=['CLS', 'Mixing', 'Restructuring'],
        loc='upper center',
        bbox_to_anchor=(0.5, 0.98),
        ncol=3,
        fontsize=10,
        frameon=False
    )

    plt.tight_layout(rect=[0.05, 0, 1, 0.93])

    output_file = output_dir / "Fig_assembly_effect_parent_vs_coalesced.svg"
    try:
        fig.savefig(str(output_file), format='svg', dpi=300, bbox_inches='tight')
        print(f"  ✓ Created: {output_file}")
    except Exception as e:
        print(f"  ✗ ERROR saving {output_file}: {e}")
    finally:
        plt.close()


def plot_theta_single(mean_val, coal_data, direct_data, output_dir):
    """Create side-by-side theta plot for a single interaction strength"""

    mm = 1 / 25.4
    fig, axes = plt.subplots(1, 2, figsize=(160*mm, 80*mm), facecolor='w', edgecolor='k')

    coal_u = np.array(coal_data['u_values'])
    coal_v = np.array(coal_data['v_values'])
    direct_u = np.array(direct_data['u_values'])
    direct_v = np.array(direct_data['v_values'])

    # Define contour grid
    x = np.linspace(-0.15, 1.2, 500)
    y = np.linspace(-0.15, 1.2, 500)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)

    color = '#3498db'  # Blue

    # ===== LEFT: Direct Assembly =====
    ax_direct = axes[0]

    if len(direct_u) > 0:
        ax_direct.scatter(direct_u, direct_v, s=40, color=color, marker='o',
                         alpha=0.6, linewidths=0, edgecolors='none')
        ax_direct.scatter(direct_v, direct_u, s=40, color='grey', marker='o',
                         alpha=0.2, linewidths=0, edgecolors='none')

    ax_direct.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                     alpha=0.3, linewidths=0.5)
    ax_direct.axhline(0, color='k', linestyle='--', linewidth=0.8)
    ax_direct.axvline(0, color='k', linestyle='--', linewidth=0.8)

    ax_direct.set_xlim(-0.05, 1.05)
    ax_direct.set_ylim(-0.05, 1.05)
    ax_direct.set_xticks([0, 0.5, 1.0])
    ax_direct.set_yticks([0, 0.5, 1.0])
    ax_direct.set_xlabel('u (Parent 1 contribution)', fontsize=10)
    ax_direct.set_ylabel('v (Parent 2 contribution)', fontsize=10)

    for spine in ax_direct.spines.values():
        spine.set_visible(False)

    ax_direct.set_title('Direct Assembly', fontsize=11, fontweight='bold')
    ax_direct.text(0.02, 0.98, f'n={len(direct_u)}',
                  transform=ax_direct.transAxes, fontsize=9,
                  verticalalignment='top', fontweight='bold')

    # ===== RIGHT: Coalescence =====
    ax_coal = axes[1]

    if len(coal_u) > 0:
        ax_coal.scatter(coal_u, coal_v, s=40, color=color, marker='o',
                       alpha=0.6, linewidths=0, edgecolors='none')
        ax_coal.scatter(coal_v, coal_u, s=40, color='grey', marker='o',
                       alpha=0.2, linewidths=0, edgecolors='none')

    ax_coal.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                   alpha=0.3, linewidths=0.5)
    ax_coal.axhline(0, color='k', linestyle='--', linewidth=0.8)
    ax_coal.axvline(0, color='k', linestyle='--', linewidth=0.8)

    ax_coal.set_xlim(-0.05, 1.05)
    ax_coal.set_ylim(-0.05, 1.05)
    ax_coal.set_xticks([0, 0.5, 1.0])
    ax_coal.set_yticks([0, 0.5, 1.0])
    ax_coal.set_xlabel('u (Parent 1 contribution)', fontsize=10)
    ax_coal.set_ylabel('v (Parent 2 contribution)', fontsize=10)

    for spine in ax_coal.spines.values():
        spine.set_visible(False)

    ax_coal.set_title('Coalescence', fontsize=11, fontweight='bold')
    ax_coal.text(0.02, 0.98, f'n={len(coal_u)}',
                transform=ax_coal.transAxes, fontsize=9,
                verticalalignment='top', fontweight='bold')

    # Overall title
    fig.suptitle(f'μ = {mean_val}', fontsize=13, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    output_file = output_dir / f"Fig_assembly_effect_theta_mean{mean_val:.1f}.svg"
    try:
        fig.savefig(str(output_file), format='svg', dpi=300, bbox_inches='tight')
    except Exception as e:
        print(f"  ✗ ERROR saving {output_file}: {e}")
    finally:
        plt.close()

    return output_file


def plot_theta_merged(results, output_dir):
    """Create merged theta plot: 2 rows × 5 columns (5 interaction strengths)"""

    print("\n=== Generating Merged Theta Plot ===")

    mm = 1 / 25.4
    fig, axes = plt.subplots(2, len(INTERACTION_STRENGTHS),
                            figsize=(50*len(INTERACTION_STRENGTHS)*mm, 100*mm),
                            facecolor='w', edgecolor='k')

    # Define contour grid
    x = np.linspace(-0.15, 1.2, 500)
    y = np.linspace(-0.15, 1.2, 500)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)

    color = '#3498db'

    for col_idx, mean_val in enumerate(INTERACTION_STRENGTHS):
        coal_u = np.array(results[mean_val]['coalescence']['u_values'])
        coal_v = np.array(results[mean_val]['coalescence']['v_values'])
        direct_u = np.array(results[mean_val]['direct']['u_values'])
        direct_v = np.array(results[mean_val]['direct']['v_values'])

        # ===== TOP ROW: Direct Assembly =====
        ax_direct = axes[0, col_idx]

        if len(direct_u) > 0:
            ax_direct.scatter(direct_u, direct_v, s=30, color=color, marker='o',
                             alpha=0.6, linewidths=0, edgecolors='none')
            ax_direct.scatter(direct_v, direct_u, s=30, color='grey', marker='o',
                             alpha=0.2, linewidths=0, edgecolors='none')

        ax_direct.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                         alpha=0.3, linewidths=0.5)
        ax_direct.axhline(0, color='k', linestyle='--', linewidth=0.8)
        ax_direct.axvline(0, color='k', linestyle='--', linewidth=0.8)

        ax_direct.set_xlim(-0.05, 1.05)
        ax_direct.set_ylim(-0.05, 1.05)
        ax_direct.set_xticks([0, 0.5, 1.0])
        ax_direct.set_yticks([0, 0.5, 1.0])

        if col_idx == 0:
            ax_direct.set_ylabel('v', fontsize=9)

        ax_direct.set_xlabel('')

        for spine in ax_direct.spines.values():
            spine.set_visible(False)

        ax_direct.set_title(f'μ={mean_val}', fontsize=10, fontweight='bold')
        ax_direct.text(0.02, 0.98, f'n={len(direct_u)}',
                      transform=ax_direct.transAxes, fontsize=8,
                      verticalalignment='top', fontweight='bold')

        # ===== BOTTOM ROW: Coalescence =====
        ax_coal = axes[1, col_idx]

        if len(coal_u) > 0:
            ax_coal.scatter(coal_u, coal_v, s=30, color=color, marker='o',
                           alpha=0.6, linewidths=0, edgecolors='none')
            ax_coal.scatter(coal_v, coal_u, s=30, color='grey', marker='o',
                           alpha=0.2, linewidths=0, edgecolors='none')

        ax_coal.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                       alpha=0.3, linewidths=0.5)
        ax_coal.axhline(0, color='k', linestyle='--', linewidth=0.8)
        ax_coal.axvline(0, color='k', linestyle='--', linewidth=0.8)

        ax_coal.set_xlim(-0.05, 1.05)
        ax_coal.set_ylim(-0.05, 1.05)
        ax_coal.set_xticks([0, 0.5, 1.0])
        ax_coal.set_yticks([0, 0.5, 1.0])

        if col_idx == 0:
            ax_coal.set_ylabel('v', fontsize=9)

        ax_coal.set_xlabel('u', fontsize=9)

        for spine in ax_coal.spines.values():
            spine.set_visible(False)

        ax_coal.text(0.02, 0.98, f'n={len(coal_u)}',
                    transform=ax_coal.transAxes, fontsize=8,
                    verticalalignment='top', fontweight='bold')

    # Add row labels
    axes[0, 0].text(-0.3, 0.5, 'Direct Assembly', rotation=90, fontsize=11,
                   fontweight='bold', va='center', ha='center',
                   transform=axes[0, 0].transAxes)
    axes[1, 0].text(-0.3, 0.5, 'Coalescence', rotation=90, fontsize=11,
                   fontweight='bold', va='center', ha='center',
                   transform=axes[1, 0].transAxes)

    plt.tight_layout()

    output_file = output_dir / "Fig_assembly_effect_theta_merged.svg"
    try:
        fig.savefig(str(output_file), format='svg', dpi=300, bbox_inches='tight')
        print(f"  ✓ Created: {output_file}")
    except Exception as e:
        print(f"  ✗ ERROR saving {output_file}: {e}")
    finally:
        plt.close()


def main():
    print("="*70)
    print("Assembly Effect Analysis - Simulation Data")
    print("="*70)

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

    # Generate plots
    print("\n=== Generating Plots ===")

    # Pie charts
    plot_pie_charts(results, output_dir)

    # Individual theta plots for each interaction strength
    print("\n=== Generating Individual Theta Plots ===")
    for mean_val in INTERACTION_STRENGTHS:
        output_file = plot_theta_single(mean_val,
                                        results[mean_val]['coalescence'],
                                        results[mean_val]['direct'],
                                        output_dir)
        print(f"  ✓ Created: {output_file}")

    # Merged theta plot
    plot_theta_merged(results, output_dir)

    print("\n" + "="*70)
    print("✓✓✓ PLOTTING COMPLETE! ✓✓✓")
    print("="*70)
    print(f"\nOutput directory: {output_dir}/")
    print("\nGenerated files:")
    print("  - Fig_assembly_effect_parent_vs_coalesced.svg (pie charts)")
    print("  - Fig_assembly_effect_theta_mean*.svg (individual theta plots)")
    print("  - Fig_assembly_effect_theta_merged.svg (merged theta plot)")


if __name__ == "__main__":
    main()
