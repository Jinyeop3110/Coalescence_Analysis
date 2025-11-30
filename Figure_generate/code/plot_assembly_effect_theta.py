"""
plot_assembly_effect_theta.py

Purpose: Create theta (polarized) plots comparing parent (direct assembly) vs coalesced (coalescence)
         communities using vector decomposition coordinates (u, v).

Similar to: vector_decomp_experimental_merged.py polarized plots

Output:
- Figure/Assembly_effect/Fig_assembly_effect_theta_LN.svg
- Figure/Assembly_effect/Fig_assembly_effect_theta_MN.svg
- Figure/Assembly_effect/Fig_assembly_effect_theta_HN.svg
- Figure/Assembly_effect/Fig_assembly_effect_theta_merged.svg
"""

from common_setup import *
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pickle


def metric_VectorDecomposition_onlyPositive(u, v, m):
    """
    Original vector decomposition metric.
    Returns u_component, v_component, restructuring_component, and orthogonal_vector.
    """
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

    # Calculate orthogonal component (restructured community vector)
    orthogonal_vec = m - (e12[0]*u) - (e12[1]*v)
    x3 = np.linalg.norm(orthogonal_vec)
    convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2 + 1e-10))

    return convert*x1, convert*x2, x3, orthogonal_vec


def getAbundance_fixed(Processed_sequences, IDX):
    """Fixed version of getAbundance that correctly handles samples at index 0."""
    SampleIdx = np.flatnonzero([x == IDX for x in Processed_sequences['SampleIDX']])
    if len(SampleIdx) == 0:
        return None
    else:
        O = Processed_sequences.iloc[SampleIdx[0]].values.tolist()[1:]
        return O


def create_polarized_plot_single(parent_data, coalesced_data, medium, color, output_dir):
    """
    Create two subplots: one for parent (direct assembly) and one for coalesced (coalescence).

    Parameters:
    -----------
    parent_data : tuple of (u_values, v_values)
    coalesced_data : tuple of (u_values, v_values)
    medium : str (e.g., 'LN', 'MN', 'HN')
    color : str (matplotlib color)
    output_dir : Path
    """
    mm = 1 / 25.4
    fig, axes = plt.subplots(1, 2, figsize=(160*mm, 80*mm), facecolor='w', edgecolor='k')

    parent_u, parent_v = parent_data
    coal_u, coal_v = coalesced_data

    medium_names = {'LN': 'Nutr-', 'MN': 'Base', 'HN': 'Nutr+'}

    # Define the grid of points for contours (shared)
    x = np.linspace(-0.15, 1.2, 500)
    y = np.linspace(-0.15, 1.2, 500)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(abs(X**2 + Y**2))

    # ===== LEFT SUBPLOT: Parent (Direct Assembly) =====
    ax_parent = axes[0]

    # Plot parent communities
    ax_parent.scatter(parent_u, parent_v, s=40, color=color, marker='o',
                     alpha=0.6, linewidths=0, edgecolors='none')
    # Mirror points
    ax_parent.scatter(parent_v, parent_u, s=40, color='grey', marker='o',
                     alpha=0.2, linewidths=0, edgecolors='none')

    # Contours
    ax_parent.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                     alpha=0.3, linewidths=0.5)

    # Auxiliary lines
    ax_parent.axhline(0, color='k', linestyle='--', linewidth=0.8)
    ax_parent.axvline(0, color='k', linestyle='--', linewidth=0.8)

    # Set plot limits and labels
    ax_parent.set_xlim(-0.05, 1.05)
    ax_parent.set_ylim(-0.05, 1.05)
    ax_parent.set_xticks([0, 0.5, 1.0])
    ax_parent.set_yticks([0, 0.5, 1.0])
    ax_parent.set_xlabel('u (Parent 1 contribution)', fontsize=10)
    ax_parent.set_ylabel('v (Parent 2 contribution)', fontsize=10)

    # Remove spines
    for spine in ax_parent.spines.values():
        spine.set_visible(False)

    # Title
    ax_parent.set_title(f'Direct Assembly',
                       fontsize=11, fontweight='bold')

    # Sample count
    ax_parent.text(0.02, 0.98, f'n={len(parent_u)}',
                  transform=ax_parent.transAxes, fontsize=9,
                  verticalalignment='top', fontweight='bold')

    # ===== RIGHT SUBPLOT: Coalesced (Coalescence) =====
    ax_coal = axes[1]

    # Plot coalesced communities
    ax_coal.scatter(coal_u, coal_v, s=40, color=color, marker='o',
                   alpha=0.6, linewidths=0, edgecolors='none')
    # Mirror points
    ax_coal.scatter(coal_v, coal_u, s=40, color='grey', marker='o',
                   alpha=0.2, linewidths=0, edgecolors='none')

    # Contours
    ax_coal.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                   alpha=0.3, linewidths=0.5)

    # Auxiliary lines
    ax_coal.axhline(0, color='k', linestyle='--', linewidth=0.8)
    ax_coal.axvline(0, color='k', linestyle='--', linewidth=0.8)

    # Set plot limits and labels
    ax_coal.set_xlim(-0.05, 1.05)
    ax_coal.set_ylim(-0.05, 1.05)
    ax_coal.set_xticks([0, 0.5, 1.0])
    ax_coal.set_yticks([0, 0.5, 1.0])
    ax_coal.set_xlabel('u (Parent 1 contribution)', fontsize=10)
    ax_coal.set_ylabel('v (Parent 2 contribution)', fontsize=10)

    # Remove spines
    for spine in ax_coal.spines.values():
        spine.set_visible(False)

    # Title
    ax_coal.set_title(f'Coalescence',
                     fontsize=11, fontweight='bold')

    # Sample count
    ax_coal.text(0.02, 0.98, f'n={len(coal_u)}',
                transform=ax_coal.transAxes, fontsize=9,
                verticalalignment='top', fontweight='bold')

    # Add overall title for the medium
    fig.suptitle(medium_names[medium], fontsize=13, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Save with new naming convention
    medium_file_names = {'LN': 'Nutr-', 'MN': 'Base', 'HN': 'Nutr+'}
    output_filename = output_dir / f"Fig_assembly_effect_theta_{medium_file_names[medium]}.svg"
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Created: {output_filename}")


def create_polarized_plot_merged(all_data, colors, output_dir):
    """
    Create merged polarized plot: 2 rows (parent vs coalesced) x 3 columns (LN, MN, HN).

    Parameters:
    -----------
    all_data : dict with keys 'LN', 'MN', 'HN', each containing:
               {'parent': (u, v), 'coalesced': (u, v)}
    colors : dict with keys 'LN', 'MN', 'HN'
    output_dir : Path
    """
    mm = 1 / 25.4
    fig, axes = plt.subplots(2, 3, figsize=(210*mm, 140*mm), facecolor='w', edgecolor='k')

    medium_order = ['LN', 'MN', 'HN']
    medium_names = {'LN': 'Nutr-', 'MN': 'Base', 'HN': 'Nutr+'}

    # Define the grid of points for contours (shared)
    x = np.linspace(-0.15, 1.2, 500)
    y = np.linspace(-0.15, 1.2, 500)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(abs(X**2 + Y**2))

    for col_idx, medium in enumerate(medium_order):
        if medium not in all_data:
            continue

        parent_u, parent_v = all_data[medium]['parent']
        coal_u, coal_v = all_data[medium]['coalesced']
        color = colors[medium]

        # ===== TOP ROW: Parent (Direct Assembly) =====
        ax_parent = axes[0, col_idx]

        # Plot parent communities
        ax_parent.scatter(parent_u, parent_v, s=30, color=color, marker='o',
                         alpha=0.6, linewidths=0, edgecolors='none')
        ax_parent.scatter(parent_v, parent_u, s=30, color='grey', marker='o',
                         alpha=0.2, linewidths=0, edgecolors='none')

        # Contours
        ax_parent.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                         alpha=0.3, linewidths=0.5)

        # Auxiliary lines
        ax_parent.axhline(0, color='k', linestyle='--', linewidth=0.8)
        ax_parent.axvline(0, color='k', linestyle='--', linewidth=0.8)

        # Set plot limits and labels
        ax_parent.set_xlim(-0.05, 1.05)
        ax_parent.set_ylim(-0.05, 1.05)
        ax_parent.set_xticks([0, 0.5, 1.0])
        ax_parent.set_yticks([0, 0.5, 1.0])

        if col_idx == 0:
            ax_parent.set_ylabel('v (Parent 2)', fontsize=9)

        # Remove bottom x-label for top row
        ax_parent.set_xlabel('')

        # Remove spines
        for spine in ax_parent.spines.values():
            spine.set_visible(False)

        # Title (only for top row)
        ax_parent.set_title(medium_names[medium], fontsize=10, fontweight='bold')

        # Sample count
        ax_parent.text(0.02, 0.98, f'n={len(parent_u)}',
                      transform=ax_parent.transAxes, fontsize=8,
                      verticalalignment='top', fontweight='bold')

        # ===== BOTTOM ROW: Coalesced (Coalescence) =====
        ax_coal = axes[1, col_idx]

        # Plot coalesced communities
        ax_coal.scatter(coal_u, coal_v, s=30, color=color, marker='o',
                       alpha=0.6, linewidths=0, edgecolors='none')
        ax_coal.scatter(coal_v, coal_u, s=30, color='grey', marker='o',
                       alpha=0.2, linewidths=0, edgecolors='none')

        # Contours
        ax_coal.contour(X, Y, R, levels=[0.25, 0.5, 0.75, 1.0], colors='grey',
                       alpha=0.3, linewidths=0.5)

        # Auxiliary lines
        ax_coal.axhline(0, color='k', linestyle='--', linewidth=0.8)
        ax_coal.axvline(0, color='k', linestyle='--', linewidth=0.8)

        # Set plot limits and labels
        ax_coal.set_xlim(-0.05, 1.05)
        ax_coal.set_ylim(-0.05, 1.05)
        ax_coal.set_xticks([0, 0.5, 1.0])
        ax_coal.set_yticks([0, 0.5, 1.0])

        if col_idx == 0:
            ax_coal.set_ylabel('v (Parent 2)', fontsize=9)

        ax_coal.set_xlabel('u (Parent 1)', fontsize=9)

        # Remove spines
        for spine in ax_coal.spines.values():
            spine.set_visible(False)

        # Sample count
        ax_coal.text(0.02, 0.98, f'n={len(coal_u)}',
                    transform=ax_coal.transAxes, fontsize=8,
                    verticalalignment='top', fontweight='bold')

    # Add row labels on the left
    fig.text(0.02, 0.75, 'Direct Assembly', fontsize=11, fontweight='bold',
            rotation=90, va='center', ha='center')
    fig.text(0.02, 0.25, 'Coalescence', fontsize=11, fontweight='bold',
            rotation=90, va='center', ha='center')

    plt.tight_layout(rect=[0.03, 0, 1, 1])

    # Save
    output_filename = output_dir / "Fig_assembly_effect_theta_merged.svg"
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n✓ Created merged plot: {output_filename}")


def main():
    """Main function to create theta (polarized) plots for assembly effect."""

    print("="*80)
    print("Assembly Effect Theta (Polarized) Plots")
    print("="*80)
    print("Creating theta plots comparing parent (direct assembly) vs coalesced (coalescence)")
    print()

    # Create output directory
    output_dir = Path("Figure/Assembly_effect")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load assembly pairs data
    pairs_file = output_dir / "assembly_pairs_CORRECT.pkl"
    print(f"Loading assembly pairs from: {pairs_file}\n")

    with open(pairs_file, 'rb') as f:
        assembly_data = pickle.load(f)

    # Get data
    pairs_data = assembly_data['pairs']

    # Colors for each medium (from COLORMAP)
    from COLORMAP import get_medium_color
    colors = {
        'LN': get_medium_color('LN'),
        'MN': get_medium_color('MN'),
        'HN': get_medium_color('HN')
    }

    # Store u, v values for each medium and type
    all_data = {}

    for medium in ['LN', 'MN', 'HN']:
        print(f"Processing {medium}...")

        parent_u_list = []
        parent_v_list = []
        coal_u_list = []
        coal_v_list = []

        # Process all comparison types for this medium
        for comparison_type in pairs_data[medium].keys():
            pairs = pairs_data[medium][comparison_type]

            for pair in pairs:
                # Only use pairs with matching replicates
                if pair['parent_replicate'] != pair['coalesced_replicate']:
                    continue

                # Get abundances with NaN handling
                def safe_array_convert(data):
                    arr = np.array(data, dtype=float)
                    arr = np.nan_to_num(arr, nan=0.0)
                    return arr

                parent_abund = safe_array_convert(pair['parent_abundances'])
                coal_abund = safe_array_convert(pair['coalesced_abundances'])
                coal_sub1_abund = safe_array_convert(pair['sub1_abundances'])
                coal_sub2_abund = safe_array_convert(pair['sub2_abundances'])

                # For PARENT: Check if it's a coalesced community
                parent_sample = pair['parent_sample']
                parent_coal_data = Coalescence_data[Coalescence_data['SampleIDX'] == parent_sample]

                if len(parent_coal_data) > 0:
                    # Parent IS a coalesced community - use its actual parents
                    parent_sub1_sample = parent_coal_data.iloc[0]['SampleIDX_Sub1']
                    parent_sub2_sample = parent_coal_data.iloc[0]['SampleIDX_Sub2']

                    # Get abundances
                    parent_sub1_abund = getAbundance_fixed(
                        pd.concat([Processed_sequences_synthetic, Processed_sequences_natural]),
                        parent_sub1_sample
                    )
                    parent_sub2_abund = getAbundance_fixed(
                        pd.concat([Processed_sequences_synthetic, Processed_sequences_natural]),
                        parent_sub2_sample
                    )

                    if parent_sub1_abund is None or parent_sub2_abund is None:
                        continue

                    parent_sub1_abund = safe_array_convert(parent_sub1_abund)
                    parent_sub2_abund = safe_array_convert(parent_sub2_abund)
                else:
                    # Parent is NOT a coalesced community - use same subs as coalesced
                    parent_sub1_abund = coal_sub1_abund.copy()
                    parent_sub2_abund = coal_sub2_abund.copy()

                # Apply threshold
                threshold = 1e-4
                parent_abund = parent_abund * (parent_abund > threshold)
                coal_abund = coal_abund * (coal_abund > threshold)
                coal_sub1_abund = coal_sub1_abund * (coal_sub1_abund > threshold)
                coal_sub2_abund = coal_sub2_abund * (coal_sub2_abund > threshold)
                parent_sub1_abund = parent_sub1_abund * (parent_sub1_abund > threshold)
                parent_sub2_abund = parent_sub2_abund * (parent_sub2_abund > threshold)

                try:
                    # Compute vector decomposition for PARENT
                    u_parent, v_parent, k_parent, _ = metric_VectorDecomposition_onlyPositive(
                        parent_sub1_abund, parent_sub2_abund, parent_abund
                    )

                    # Compute vector decomposition for COALESCED
                    u_coal, v_coal, k_coal, _ = metric_VectorDecomposition_onlyPositive(
                        coal_sub1_abund, coal_sub2_abund, coal_abund
                    )

                    # Store values
                    if not (np.isnan(u_parent) or np.isnan(v_parent)):
                        parent_u_list.append(u_parent)
                        parent_v_list.append(v_parent)

                    if not (np.isnan(u_coal) or np.isnan(v_coal)):
                        coal_u_list.append(u_coal)
                        coal_v_list.append(v_coal)

                except Exception as e:
                    continue

        # Store data for this medium
        all_data[medium] = {
            'parent': (np.array(parent_u_list), np.array(parent_v_list)),
            'coalesced': (np.array(coal_u_list), np.array(coal_v_list))
        }

        print(f"  Parent points: {len(parent_u_list)}")
        print(f"  Coalesced points: {len(coal_u_list)}")

        # Create individual plot for this medium
        create_polarized_plot_single(
            all_data[medium]['parent'],
            all_data[medium]['coalesced'],
            medium,
            colors[medium],
            output_dir
        )

    # Create merged plot with all three media
    print("\nCreating merged plot...")
    create_polarized_plot_merged(all_data, colors, output_dir)

    print("\n" + "="*80)
    print("All theta plots created!")
    print("="*80)


if __name__ == "__main__":
    main()
