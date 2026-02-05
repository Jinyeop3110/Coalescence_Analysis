#!/usr/bin/env python3
"""
Generate pie chart visualizations for subcommunities and coalesced communities.

This script creates:
1. Subcommunity pie charts - one plot per medium + species pool showing all subcommunities
2. Coalesced community matrix pie charts - N×N matrices where each cell shows the
   coalesced community from parent i and parent j
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm
import os
import sys

# Import the common setup functions
from common_setup import *

def get_taxonomic_colormap_and_sorting():
    """Generate taxonomy-based colormap and isolate sorting index."""
    # Taxonomy data from the timeseries notebook
    data = [
        ["ASV1", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Enterobacteriaceae", "Pluralibacter"],
        ["ASV2", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Enterobacteriaceae", "Raoultella"],
        ["ASV3", "Bacteria", "Firmicutes", "Bacilli", "Lactobacillales", "Streptococcaceae", "Lactococcus"],
        ["ASV4", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Xanthomonadales", "Xanthomonadaceae", "Stenotrophomonas"],
        ["ASV5", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Aeromonadales", "Aeromonadaceae", "Aeromonas"],
        ["ASV6", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Pseudomonadales", "Moraxellaceae", "Acinetobacter"],
        ["ASV7", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Enterobacteriaceae", "Klebsiella"],
        ["ASV8", "Bacteria", "Bacteroidota", "Bacteroidia", "Sphingobacteriales", "Sphingobacteriaceae", "Pedobacter"],
        ["ASV9", "Bacteria", "Bacteroidota", "Bacteroidia", "Flavobacteriales", "Weeksellaceae", "Chryseobacterium"],
        ["ASV10", "Bacteria", "Firmicutes", "Bacilli", "Bacillales", "Bacillaceae", "Bacillus"],
        ["ASV11", "Bacteria", "Firmicutes", "Bacilli", "Exiguobacterales", "Exiguobacteraceae", "Exiguobacterium"],
        ["ASV12", "Bacteria", "Firmicutes", "Bacilli", "Lactobacillales", "Leuconostocaceae", "Leuconostoc"],
        ["ASV13", "Bacteria", "Bacteroidota", "Bacteroidia", "Bacteroidales", "Porphyromonadaceae", "Porphyromonas"],
        ["ASV14", "Bacteria", "Firmicutes", "Bacilli", "Bacillales", "Planococcaceae", "Lysinibacillus"],
        ["ASV15", "Bacteria", "Bacteroidota", "Bacteroidia", "Sphingobacteriales", "Sphingobacteriaceae", "Sphingobacterium"],
        ["ASV16", "Bacteria", "Firmicutes", "Bacilli", "Staphylococcales", "Staphylococcaceae", "Staphylococcus"],
        ["ASV17", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Enterobacteriaceae", "NA"],
        ["ASV18", "Bacteria", "Bacteroidota", "Bacteroidia", "Flavobacteriales", "Weeksellaceae", "Empedobacter"],
        ["ASV19", "Bacteria", "Proteobacteria", "Alphaproteobacteria", "Rhizobiales", "Rhizobiaceae", "Ochrobactrum"],
        ["ASV20", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Burkholderiales", "Comamonadaceae", "Acidovorax"],
        ["ASV21", "Bacteria", "Bacteroidota", "Bacteroidia", "Cytophagales", "Spirosomaceae", "Flectobacillus"],
        ["ASV22", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Xanthomonadales", "Xanthomonadaceae", "Stenotrophomonas"],
        ["ASV23", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "NA", "NA"],
        ["ASV24", "Bacteria", "Firmicutes", "Bacilli", "Bacillales", "Planococcaceae", "NA"],
        ["ASV25", "Bacteria", "Bacteroidota", "Bacteroidia", "Bacteroidales", "Bacteroidaceae", "Bacteroides"],
        ["ASV26", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Erwiniaceae", "Pantoea"],
        ["ASV27", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Pseudomonadales", "Pseudomonadaceae", "Pseudomonas"],
        ["ASV28", "Bacteria", "Firmicutes", "Bacilli", "Lactobacillales", "Streptococcaceae", "Lactococcus"],
        ["ASV29", "Bacteria", "Firmicutes", "Bacilli", "Staphylococcales", "Staphylococcaceae", "Staphylococcus"],
        ["ASV30", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Enterobacteriaceae", "Citrobacter"],
        ["ASV31", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Erwiniaceae", "Pantoea"],
        ["ASV32", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Pseudomonadales", "Pseudomonadaceae", "Pseudomonas"],
        ["ASV33", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Pseudomonadales", "Pseudomonadaceae", "Pseudomonas"],
        ["ASV34", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Burkholderiales", "Oxalobacteraceae", "Herbaspirillum"],
        ["ASV35", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Pseudomonadales", "Pseudomonadaceae", "Pseudomonas"],
        ["ASV36", "Bacteria", "Firmicutes", "Bacilli", "Staphylococcales", "Staphylococcaceae", "Staphylococcus"],
        ["ASV37", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Pseudomonadales", "Pseudomonadaceae", "Pseudomonas"],
        ["ASV38", "Bacteria", "Bacteroidota", "Bacteroidia", "Flavobacteriales", "Flavobacteriaceae", "Flavobacterium"],
        ["ASV39", "Bacteria", "Firmicutes", "Bacilli", "Bacillales", "Bacillaceae", "Bacillus"],
        ["ASV40", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Enterobacteriaceae", "Citrobacter"],
        ["ASV41", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Enterobacteriaceae", "Klebsiella"],
        ["ASV42", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Enterobacteriaceae", "Escherichia/Shigella"],
        ["ASV43", "Bacteria", "Proteobacteria", "Gammaproteobacteria", "Enterobacterales", "Yersiniaceae", "Yersinia"]
    ]

    # Sort isolates by phylogeny
    sorted_data = sorted(data, key=lambda x: x[2:])
    isolate_idx = [data.index(row) for row in sorted_data]

    # Generate colormap - using newer matplotlib API
    np.random.seed(4)
    try:
        inferno = plt.colormaps.get_cmap('inferno').resampled(43)
    except AttributeError:
        inferno = cm.get_cmap('inferno', 43)
    colors = [inferno(i)[:3] for i in range(43)]
    np.random.shuffle(colors)

    return colors, isolate_idx

def get_abundance_vector(sample_id):
    """Extract abundance vector for a given sample ID."""
    # Check both synthetic and natural data
    sample_rows_syn = Processed_sequences_synthetic[Processed_sequences_synthetic['SampleIDX'] == sample_id]
    sample_rows_nat = Processed_sequences_natural[Processed_sequences_natural['SampleIDX'] == sample_id]

    sample_rows = pd.concat([sample_rows_syn, sample_rows_nat])

    if sample_rows.empty:
        return None

    # Get abundance values (columns 1-43, skipping SampleIDX)
    abundance_vector = sample_rows.iloc[0, 1:44].values.astype(float)
    abundance_vector = np.nan_to_num(abundance_vector, 0)

    # Normalize
    if abundance_vector.sum() > 0:
        abundance_vector = abundance_vector / abundance_vector.sum()

    return abundance_vector

def plot_pie_chart(ax, abundance_vector, colors, isolate_idx, threshold=0.001):
    """
    Plot a single pie chart on the given axis.
    Only shows ASVs above threshold.
    """
    if abundance_vector is None:
        ax.axis('off')
        return

    # Filter to only ASVs above threshold
    mask = abundance_vector > threshold
    if not np.any(mask):
        ax.axis('off')
        return

    # Get abundances and colors for ASVs above threshold
    filtered_abundances = abundance_vector[mask]
    filtered_colors = [colors[i] for i, present in enumerate(mask) if present]

    # Create pie chart
    ax.pie(filtered_abundances, colors=filtered_colors, startangle=90)
    ax.axis('equal')

def get_subcommunities_by_medium_and_pool(metadata_df, sequences_df):
    """
    Get all subcommunities organized by medium, species pool, and replicate.
    Returns: dict[medium][species_pool][replicate] = list of sample_ids
    """
    subcommunities = {}

    # Filter for subcommunities (CoalescenceType == 'S')
    subcomm_metadata = metadata_df[metadata_df['CoalescenceType'] == 'S'].copy()

    for _, row in subcomm_metadata.iterrows():
        sample_id = row['SampleIDX']
        medium = row['Medium']
        replicate = int(row['Replicate'])

        # Map medium codes to names
        medium_name = {'H': 'Nutr+', 'M': 'Base', 'L': 'Nutr-'}.get(medium, medium)

        # Determine species pool from CommunityIDX
        community_idx = int(row['CommunityIDX'])
        if community_idx <= 9:
            species_pool = 6
        elif community_idx <= 18:
            species_pool = 12
        elif community_idx <= 30:
            species_pool = 24
        else:
            continue  # Skip if out of expected range

        # Initialize nested dict structure
        if medium_name not in subcommunities:
            subcommunities[medium_name] = {}
        if species_pool not in subcommunities[medium_name]:
            subcommunities[medium_name][species_pool] = {}
        if replicate not in subcommunities[medium_name][species_pool]:
            subcommunities[medium_name][species_pool][replicate] = []

        subcommunities[medium_name][species_pool][replicate].append(sample_id)

    return subcommunities

def plot_subcommunity_pies(subcommunities, colors, isolate_idx, output_dir):
    """
    Create pie chart plots for all subcommunities.
    One plot per medium + species pool combination, with rep1 on left and rep2 on right.
    Ordered by community index to match coalescence matrices.
    """
    print("\n=== Generating Subcommunity Pie Charts ===")

    os.makedirs(output_dir, exist_ok=True)

    for medium in sorted(subcommunities.keys()):
        for species_pool in sorted(subcommunities[medium].keys()):
            rep_data = subcommunities[medium][species_pool]

            # Get replicate 1 and 2 samples and sort by community index
            def sort_by_community_idx(sample_list):
                """Sort samples by CommunityIDX, then by SampleIDX"""
                samples_with_idx = []
                for sample_id in sample_list:
                    subcomm_meta = Metadata[Metadata['SampleIDX'] == sample_id]
                    if not subcomm_meta.empty:
                        comm_idx = int(subcomm_meta.iloc[0]['CommunityIDX'])
                        samples_with_idx.append((sample_id, comm_idx))
                samples_with_idx.sort(key=lambda x: (x[1], x[0]))
                return [s[0] for s in samples_with_idx]

            rep1_samples = sort_by_community_idx(rep_data.get(1, []))
            rep2_samples = sort_by_community_idx(rep_data.get(2, []))

            n_samples_per_rep = max(len(rep1_samples), len(rep2_samples))

            print(f"Processing {medium} - s{species_pool}: Rep1={len(rep1_samples)}, Rep2={len(rep2_samples)}")

            # Calculate grid dimensions (rows for subcommunities, 2 columns for replicates)
            n_rows = n_samples_per_rep
            n_cols = 2  # Left column: rep1, Right column: rep2

            # Create figure
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 1.5, n_rows * 1.5))
            fig.suptitle(f'{medium} - Parentals (N_species = {species_pool})',
                        fontsize=12, fontweight='bold', y=1.02)

            # Handle single row case
            if n_rows == 1:
                axes = axes.reshape(1, -1)

            # Plot replicate 1 (left column)
            for idx, sample_id in enumerate(rep1_samples):
                abundance_vector = get_abundance_vector(sample_id)
                plot_pie_chart(axes[idx, 0], abundance_vector, colors, isolate_idx)

                # Add community index to label
                subcomm_meta = Metadata[Metadata['SampleIDX'] == sample_id]
                if not subcomm_meta.empty:
                    comm_idx = int(subcomm_meta.iloc[0]['CommunityIDX'])
                    axes[idx, 0].set_title(f'{sample_id} (C{comm_idx})', fontsize=9)
                else:
                    axes[idx, 0].set_title(f'{sample_id}', fontsize=9)

            # Hide unused plots in rep1 column
            for idx in range(len(rep1_samples), n_rows):
                axes[idx, 0].axis('off')

            # Plot replicate 2 (right column)
            for idx, sample_id in enumerate(rep2_samples):
                abundance_vector = get_abundance_vector(sample_id)
                plot_pie_chart(axes[idx, 1], abundance_vector, colors, isolate_idx)

                # Add community index to label
                subcomm_meta = Metadata[Metadata['SampleIDX'] == sample_id]
                if not subcomm_meta.empty:
                    comm_idx = int(subcomm_meta.iloc[0]['CommunityIDX'])
                    axes[idx, 1].set_title(f'{sample_id} (C{comm_idx})', fontsize=9)
                else:
                    axes[idx, 1].set_title(f'{sample_id}', fontsize=9)

            # Hide unused plots in rep2 column
            for idx in range(len(rep2_samples), n_rows):
                axes[idx, 1].axis('off')

            # Add column labels
            axes[0, 0].text(0.5, 1.25, 'Replicate 1', transform=axes[0, 0].transAxes,
                           ha='center', fontsize=13, fontweight='bold')
            axes[0, 1].text(0.5, 1.25, 'Replicate 2', transform=axes[0, 1].transAxes,
                           ha='center', fontsize=13, fontweight='bold')

            plt.tight_layout()

            # Save figure
            filename = f'subcommunities_{medium}_s{species_pool}.png'
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.savefig(filepath.replace('.png', '.svg'), dpi=150, bbox_inches='tight')
            plt.close()

            print(f"  Saved: {filename}")

def get_coalescence_matrix_data(metadata_df, coalescence_df):
    """
    Organize coalescence data into matrices by medium, species pool, and replicate.
    Uses the same ordering logic as NbyNcomposition from common_setup.py.
    Returns: dict[medium][species_pool][replicate] = {
        'subcommunity_ids': list of subcommunity IDs in order from Community_PermutateList,
        'matrix': dict[(parent1_idx, parent2_idx)] = coalesced_sample_id
    }
    """
    coal_matrices = {}

    # Map medium codes
    medium_map = {'H': 'Nutr+', 'M': 'Base', 'L': 'Nutr-'}

    # Process each combination of medium, species pool, and replicate
    for medium_code in ['H', 'M', 'L']:
        medium_name = medium_map[medium_code]
        for species_pool in [6, 12, 24]:
            for replicate in [1, 2]:
                # Get the ordered lists from Community_PermutateList (same as create_coalescence_pie_visualization.py)
                coal_samples = Community_PermutateList("F", "S", medium_code, "C", species_pool, replicate)
                sub_samples = Community_PermutateList("F", "S", medium_code, "S", species_pool, replicate)

                if not coal_samples or not sub_samples:
                    continue

                # Initialize structure
                if medium_name not in coal_matrices:
                    coal_matrices[medium_name] = {}
                if species_pool not in coal_matrices[medium_name]:
                    coal_matrices[medium_name][species_pool] = {}
                if replicate not in coal_matrices[medium_name][species_pool]:
                    coal_matrices[medium_name][species_pool][replicate] = {
                        'subcommunity_ids': sub_samples,  # Use the ordered list from Community_PermutateList
                        'matrix': {}
                    }

                # Build the matrix using position indices (like NbyNcomposition does)
                for offspring_id in coal_samples:
                    # Get parent IDs
                    coal_row = coalescence_df[coalescence_df['SampleIDX'] == offspring_id]
                    if coal_row.empty:
                        continue

                    parent1_id = coal_row.iloc[0]['SampleIDX_Sub1']
                    parent2_id = coal_row.iloc[0]['SampleIDX_Sub2']

                    if pd.isna(parent1_id) or pd.isna(parent2_id):
                        continue

                    # Find positions of parents in sub_samples list
                    try:
                        parent1_pos = sub_samples.index(parent1_id)
                        parent2_pos = sub_samples.index(parent2_id)
                    except ValueError:
                        # Parent not in subcommunity list for this combination
                        continue

                    # Store with position indices (i, j) like NbyNcomposition
                    i = min(parent1_pos, parent2_pos)
                    j = max(parent1_pos, parent2_pos)
                    coal_matrices[medium_name][species_pool][replicate]['matrix'][(i, j)] = offspring_id

    return coal_matrices

def plot_coalescence_matrices(coal_matrices, colors, isolate_idx, output_dir):
    """
    Create N×N matrices of pie charts for coalesced communities.
    One plot per medium + species pool combination, with rep1 on left and rep2 on right.
    Rows and columns are ordered by position in Community_PermutateList (same as NbyNcomposition).
    """
    print("\n=== Generating Coalescence Matrix Pie Charts ===")

    os.makedirs(output_dir, exist_ok=True)

    for medium in sorted(coal_matrices.keys()):
        for species_pool in sorted(coal_matrices[medium].keys()):
            rep_data = coal_matrices[medium][species_pool]

            # Get replicate 1 and 2 data
            rep1_data = rep_data.get(1, {'subcommunity_ids': [], 'matrix': {}})
            rep2_data = rep_data.get(2, {'subcommunity_ids': [], 'matrix': {}})

            n1 = len(rep1_data['subcommunity_ids'])
            n2 = len(rep2_data['subcommunity_ids'])

            print(f"Processing {medium} - s{species_pool}: Rep1={n1}×{n1}, Rep2={n2}×{n2}")

            # Create figure with two matrix panels side by side
            # Total width = n1 + n2 (both matrices), with larger scaling factor for readability
            fig = plt.figure(figsize=((n1 + n2 + 1) * 1.2, max(n1, n2) * 1.2))
            fig.suptitle(f'{medium} - Coalescence Outcomes (N_species = {species_pool})',
                        fontsize=14, fontweight='bold')

            # Create gridspec for side-by-side matrices
            gs = fig.add_gridspec(1, 2, width_ratios=[n1, n2], wspace=0.1)

            # Plot replicate 1 matrix (left)
            if n1 > 0:
                gs_left = gs[0].subgridspec(n1, n1, hspace=0.05, wspace=0.05)

                # Get labels for subcommunities
                rep1_labels = []
                for idx, sample_id in enumerate(rep1_data['subcommunity_ids']):
                    subcomm_meta = Metadata[Metadata['SampleIDX'] == sample_id]
                    if not subcomm_meta.empty:
                        comm_idx = int(subcomm_meta.iloc[0]['CommunityIDX'])
                        rep1_labels.append(f'{idx+1}\n{sample_id}')
                    else:
                        rep1_labels.append(f'{idx+1}\n{sample_id}')

                # Iterate over matrix positions (i, j) - only upper triangle where j >= i
                for i in range(n1):
                    for j in range(n1):
                        ax = fig.add_subplot(gs_left[i, j])

                        # Only plot upper triangle (j >= i)
                        if j >= i:
                            # Get coalesced community ID using position indices
                            # Matrix is stored with (min, max) indexing
                            min_ij = min(i, j)
                            max_ij = max(i, j)
                            offspring_id = rep1_data['matrix'].get((min_ij, max_ij), None)

                            if offspring_id is not None:
                                # Plot the pie chart
                                abundance_vector = get_abundance_vector(offspring_id)
                                plot_pie_chart(ax, abundance_vector, colors, isolate_idx)
                            else:
                                # Empty cell
                                ax.axis('off')
                        else:
                            # Lower triangle - turn off
                            ax.axis('off')

                        # Remove ticks
                        ax.set_xticks([])
                        ax.set_yticks([])

                        # Add row labels on left edge
                        if j == 0:
                            ax.set_ylabel(rep1_labels[i], fontsize=9, rotation=0,
                                         ha='right', va='center', labelpad=5)

                        # Add column labels on top edge
                        if i == 0:
                            ax.set_title(rep1_labels[j], fontsize=9, pad=2)

                # Add replicate label
                fig.text(0.25, 0.95, 'Replicate 1', ha='center', fontsize=14, fontweight='bold')

            # Plot replicate 2 matrix (right)
            if n2 > 0:
                gs_right = gs[1].subgridspec(n2, n2, hspace=0.05, wspace=0.05)

                # Get labels for subcommunities
                rep2_labels = []
                for idx, sample_id in enumerate(rep2_data['subcommunity_ids']):
                    subcomm_meta = Metadata[Metadata['SampleIDX'] == sample_id]
                    if not subcomm_meta.empty:
                        comm_idx = int(subcomm_meta.iloc[0]['CommunityIDX'])
                        rep2_labels.append(f'{idx+1}\n{sample_id}')
                    else:
                        rep2_labels.append(f'{idx+1}\n{sample_id}')

                # Iterate over matrix positions (i, j) - only upper triangle where j >= i
                for i in range(n2):
                    for j in range(n2):
                        ax = fig.add_subplot(gs_right[i, j])

                        # Only plot upper triangle (j >= i)
                        if j >= i:
                            # Get coalesced community ID using position indices
                            # Matrix is stored with (min, max) indexing
                            min_ij = min(i, j)
                            max_ij = max(i, j)
                            offspring_id = rep2_data['matrix'].get((min_ij, max_ij), None)

                            if offspring_id is not None:
                                # Plot the pie chart
                                abundance_vector = get_abundance_vector(offspring_id)
                                plot_pie_chart(ax, abundance_vector, colors, isolate_idx)
                            else:
                                # Empty cell
                                ax.axis('off')
                        else:
                            # Lower triangle - turn off
                            ax.axis('off')

                        # Remove ticks
                        ax.set_xticks([])
                        ax.set_yticks([])

                        # Add row labels on left edge
                        if j == 0:
                            ax.set_ylabel(rep2_labels[i], fontsize=9, rotation=0,
                                         ha='right', va='center', labelpad=5)

                        # Add column labels on top edge
                        if i == 0:
                            ax.set_title(rep2_labels[j], fontsize=9, pad=2)

                # Add replicate label
                fig.text(0.75, 0.95, 'Replicate 2', ha='center', fontsize=14, fontweight='bold')

            # Save figure
            filename = f'coalescence_matrix_{medium}_s{species_pool}.png'
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.savefig(filepath.replace('.png', '.pdf'), bbox_inches='tight')
            plt.savefig(filepath.replace('.png', '.svg'), dpi=150, bbox_inches='tight')
            plt.close()

            print(f"  Saved: {filename}")

def main():
    """Main function to generate all pie chart plots."""

    print("Loading data and generating pie chart visualizations...")

    # Get colormaps
    colors, isolate_idx = get_taxonomic_colormap_and_sorting()
    print("Generated taxonomic colormap")

    # Base output directory
    base_output_dir = "Figure/PieCharts"
    os.makedirs(base_output_dir, exist_ok=True)

    # 1. Generate subcommunity pie charts
    print("\n" + "="*60)
    print("PART 1: SUBCOMMUNITY PIE CHARTS")
    print("="*60)

    subcommunities = get_subcommunities_by_medium_and_pool(Metadata, Processed_sequences_synthetic)
    subcomm_output_dir = os.path.join(base_output_dir, "Subcommunities")
    plot_subcommunity_pies(subcommunities, colors, isolate_idx, subcomm_output_dir)

    # 2. Generate coalescence matrix pie charts
    print("\n" + "="*60)
    print("PART 2: COALESCENCE MATRIX PIE CHARTS")
    print("="*60)

    coal_matrices = get_coalescence_matrix_data(Metadata, Coalescence_data)
    coal_output_dir = os.path.join(base_output_dir, "CoalescenceMatrices")
    plot_coalescence_matrices(coal_matrices, colors, isolate_idx, coal_output_dir)

    print("\n" + "="*60)
    print("COMPLETED!")
    print("="*60)
    print(f"\nAll pie charts saved to: {base_output_dir}/")
    print(f"  - Subcommunity plots: {subcomm_output_dir}/")
    print(f"  - Coalescence matrices: {coal_output_dir}/")

if __name__ == "__main__":
    main()
