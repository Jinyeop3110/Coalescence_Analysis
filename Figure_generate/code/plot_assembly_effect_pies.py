#!/usr/bin/env python3
"""
Generate pie chart visualizations for assembly effect analysis.

This script creates pie charts comparing parent communities (direct assembly)
with their matched coalesced communities (coalescence).

For each designed pair (parent ↔ coalesced):
- Left column: Parent community replicates
- Right column: Corresponding coalesced community replicates

Organized by medium (LN, MN, HN) and comparison type (12_vs_6+6, 24_vs_12+12).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm
import os
import sys
import pickle
import builtins

# Add path for imports
sys.path.append('.')
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

def plot_pie_chart(ax, abundance_vector, colors, isolate_idx, threshold=0.001, background_color=None):
    """
    Plot a single pie chart on the given axis.
    Only shows ASVs above threshold.

    Parameters:
    -----------
    background_color : str or None
        If provided, adds a semi-transparent background circle with this color
        (e.g., 'grey', 'lightblue')
    """
    if abundance_vector is None:
        ax.axis('off')
        return

    # Filter to only ASVs above threshold
    mask = abundance_vector > threshold
    if not builtins.any(mask):  # Use builtin any, not numpy's
        ax.axis('off')
        return

    # Add background circle if requested
    if background_color is not None:
        circle = mpatches.Circle((0, 0), 1, color=background_color, alpha=0.3, zorder=0)
        ax.add_patch(circle)

    # Get abundances and colors for ASVs above threshold
    filtered_abundances = abundance_vector[mask]
    filtered_colors = [colors[i] for i, present in enumerate(mask) if present]

    # Create pie chart
    ax.pie(filtered_abundances, colors=filtered_colors, startangle=90)
    ax.axis('equal')

def load_assembly_pairs(data_path='Figure/Assembly_effect/assembly_pairs_CORRECT.pkl'):
    """Load the assembly effect pairs data."""
    with open(data_path, 'rb') as f:
        data = pickle.load(f)
    return data

def plot_assembly_effect_pies(assembly_data, colors, isolate_idx, output_dir):
    """
    Create pie chart plots for assembly effect pairs.

    For each medium and comparison type:
    - Shows parent community (columns 1-2) vs coalesced community (columns 3-4)
    - Columns 1&3: Replicate 1, Columns 2&4: Replicate 2
    - One row per designed pair
    """
    print("\n=== Generating Assembly Effect Pie Charts ===")

    os.makedirs(output_dir, exist_ok=True)

    pairs_data = assembly_data['pairs']

    for medium in sorted(pairs_data.keys()):
        for comparison_type in sorted(pairs_data[medium].keys()):
            pairs = pairs_data[medium][comparison_type]

            if not pairs:
                print(f"No pairs for {medium} - {comparison_type}, skipping")
                continue

            print(f"\nProcessing {medium} - {comparison_type}: {len(pairs)} pairs")

            # Group pairs by parent/coalesced community combination
            # Each unique (parent_idx, coal_idx) pair should be on one row
            # Store all replicates for each pair
            pair_groups = {}
            for pair in pairs:
                key = (pair['parent_community_idx'], pair['coalesced_community_idx'])
                if key not in pair_groups:
                    pair_groups[key] = []
                pair_groups[key].append(pair)

            n_rows = len(pair_groups)
            n_cols = 6  # Columns: Parent Rep1, Parent Rep2, Coal Rep1, Coal Rep2, Sub1, Sub2

            print(f"  Unique community pairs: {n_rows}")

            # Create figure
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 2, n_rows * 2))
            fig.suptitle(f'Assembly Effect: {medium} - {comparison_type}',
                        fontsize=12, fontweight='bold')

            # Handle single row case
            if n_rows == 1:
                axes = axes.reshape(1, -1)

            # Sort pair groups by parent community index
            sorted_pairs = sorted(pair_groups.items(), key=lambda x: x[0][0])

            for row_idx, ((parent_idx, coal_idx), group) in enumerate(sorted_pairs):
                # Sort the replicates by parent replicate number
                group_sorted = sorted(group, key=lambda x: (x['parent_replicate'], x['coalesced_replicate']))

                # Get up to 2 pairs (one for each replicate)
                # Typically we'll have multiple pairs per parent-coal combination due to multiple coal replicates
                # We want to show representative examples from each parent replicate

                # Find pairs with parent replicate 1 and 2
                rep1_pairs = [p for p in group_sorted if p['parent_replicate'] == 1]
                rep2_pairs = [p for p in group_sorted if p['parent_replicate'] == 2]

                pair_rep1 = rep1_pairs[0] if rep1_pairs else None
                pair_rep2 = rep2_pairs[0] if rep2_pairs else None

                # Column 0: Parent Replicate 1
                if pair_rep1:
                    parent_abundance = np.array(pair_rep1['parent_abundances'])
                    plot_pie_chart(axes[row_idx, 0], parent_abundance, colors, isolate_idx)
                    axes[row_idx, 0].set_title(
                        f"P-C{parent_idx}\n{pair_rep1['parent_sample']}\nn={pair_rep1['parent_final_diversity']}",
                        fontsize=8
                    )
                else:
                    axes[row_idx, 0].axis('off')

                # Column 1: Parent Replicate 2
                if pair_rep2:
                    parent_abundance = np.array(pair_rep2['parent_abundances'])
                    plot_pie_chart(axes[row_idx, 1], parent_abundance, colors, isolate_idx)
                    axes[row_idx, 1].set_title(
                        f"P-C{parent_idx}\n{pair_rep2['parent_sample']}\nn={pair_rep2['parent_final_diversity']}",
                        fontsize=8
                    )
                else:
                    axes[row_idx, 1].axis('off')

                # Column 2: Coalesced Replicate 1
                if pair_rep1:
                    coal_abundance = np.array(pair_rep1['coalesced_abundances'])
                    plot_pie_chart(axes[row_idx, 2], coal_abundance, colors, isolate_idx)
                    axes[row_idx, 2].set_title(
                        f"Coal-C{coal_idx}\n{pair_rep1['coalesced_sample']}\nn={pair_rep1['coalesced_final_diversity']}",
                        fontsize=8
                    )
                else:
                    axes[row_idx, 2].axis('off')

                # Column 3: Coalesced Replicate 2
                if pair_rep2:
                    coal_abundance = np.array(pair_rep2['coalesced_abundances'])
                    plot_pie_chart(axes[row_idx, 3], coal_abundance, colors, isolate_idx)
                    axes[row_idx, 3].set_title(
                        f"Coal-C{coal_idx}\n{pair_rep2['coalesced_sample']}\nn={pair_rep2['coalesced_final_diversity']}",
                        fontsize=8
                    )
                else:
                    axes[row_idx, 3].axis('off')

                # Column 4: Subcommunity 1
                # Use data from first available pair (either rep1 or rep2)
                pair_for_subs = pair_rep1 if pair_rep1 else pair_rep2
                if pair_for_subs:
                    sub1_abundance = np.array(pair_for_subs['sub1_abundances'])
                    plot_pie_chart(axes[row_idx, 4], sub1_abundance, colors, isolate_idx)
                    axes[row_idx, 4].set_title(
                        f"Sub1-C{pair_for_subs['sub1_community_idx']}\n{pair_for_subs['sub1_sample']}\nn={pair_for_subs['sub1_final_diversity']}",
                        fontsize=8
                    )
                else:
                    axes[row_idx, 4].axis('off')

                # Column 5: Subcommunity 2
                if pair_for_subs:
                    sub2_abundance = np.array(pair_for_subs['sub2_abundances'])
                    plot_pie_chart(axes[row_idx, 5], sub2_abundance, colors, isolate_idx)
                    axes[row_idx, 5].set_title(
                        f"Sub2-C{pair_for_subs['sub2_community_idx']}\n{pair_for_subs['sub2_sample']}\nn={pair_for_subs['sub2_final_diversity']}",
                        fontsize=8
                    )
                else:
                    axes[row_idx, 5].axis('off')

            # Add column labels
            axes[0, 0].text(0.5, 1.25, 'Direct Assembly\nRep 1', transform=axes[0, 0].transAxes,
                           ha='center', fontsize=10, fontweight='bold')
            axes[0, 1].text(0.5, 1.25, 'Direct Assembly\nRep 2', transform=axes[0, 1].transAxes,
                           ha='center', fontsize=10, fontweight='bold')
            axes[0, 2].text(0.5, 1.25, 'Coalescence\nRep 1', transform=axes[0, 2].transAxes,
                           ha='center', fontsize=10, fontweight='bold')
            axes[0, 3].text(0.5, 1.25, 'Coalescence\nRep 2', transform=axes[0, 3].transAxes,
                           ha='center', fontsize=10, fontweight='bold')
            axes[0, 4].text(0.5, 1.25, 'Parent Community 1', transform=axes[0, 4].transAxes,
                           ha='center', fontsize=10, fontweight='bold')
            axes[0, 5].text(0.5, 1.25, 'Parent Community 2', transform=axes[0, 5].transAxes,
                           ha='center', fontsize=10, fontweight='bold')

            # Add group labels above
            fig.text(0.167, 0.98, 'Direct Assembly', ha='center', fontsize=12, fontweight='bold', transform=fig.transFigure)
            fig.text(0.50, 0.98, 'Coalescence', ha='center', fontsize=12, fontweight='bold', transform=fig.transFigure)
            fig.text(0.833, 0.98, 'Parent Communities', ha='center', fontsize=12, fontweight='bold', transform=fig.transFigure)

            plt.tight_layout(rect=[0, 0, 1, 0.96])

            # Add background shading AFTER tight_layout to get correct positions
            # Insert at beginning of patch list so they appear behind
            for row_idx in range(n_rows):
                # Get axis positions
                ax0_bbox = axes[row_idx, 0].get_position()
                ax1_bbox = axes[row_idx, 1].get_position()
                ax2_bbox = axes[row_idx, 2].get_position()
                ax3_bbox = axes[row_idx, 3].get_position()
                ax4_bbox = axes[row_idx, 4].get_position()
                ax5_bbox = axes[row_idx, 5].get_position()

                # Grey background spanning columns 0-1 (Direct Assembly)
                rect_start = mpatches.Rectangle(
                    (ax0_bbox.x0, ax0_bbox.y0),
                    ax1_bbox.x1 - ax0_bbox.x0,
                    ax0_bbox.height,
                    transform=fig.transFigure,
                    facecolor='grey',
                    alpha=0.25,
                    edgecolor='none',
                    zorder=-1
                )
                fig.patches.insert(0, rect_start)  # Insert at beginning

                # Light blue background spanning columns 2-3 (Coalescence)
                rect_assembly = mpatches.Rectangle(
                    (ax2_bbox.x0, ax2_bbox.y0),
                    ax3_bbox.x1 - ax2_bbox.x0,
                    ax2_bbox.height,
                    transform=fig.transFigure,
                    facecolor='lightblue',
                    alpha=0.25,
                    edgecolor='none',
                    zorder=-1
                )
                fig.patches.insert(0, rect_assembly)  # Insert at beginning

                # Black-lined transparent box spanning columns 4-5 (Parent Communities)
                rect_parents = mpatches.Rectangle(
                    (ax4_bbox.x0, ax4_bbox.y0),
                    ax5_bbox.x1 - ax4_bbox.x0,
                    ax4_bbox.height,
                    transform=fig.transFigure,
                    facecolor='none',
                    alpha=1.0,
                    edgecolor='black',
                    linewidth=1.5,
                    zorder=-1
                )
                fig.patches.insert(0, rect_parents)  # Insert at beginning

            # Save figure (SVG only, no PNG)
            filename = f'assembly_effect_{medium}_{comparison_type}.svg'
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()

            print(f"  Saved: {filename}")

def main():
    """Main function to generate assembly effect pie charts."""

    print("Loading data and generating assembly effect pie chart visualizations...")

    # Get colormaps
    colors, isolate_idx = get_taxonomic_colormap_and_sorting()
    print("Generated taxonomic colormap")

    # Load assembly pairs data
    assembly_data = load_assembly_pairs()
    print(f"Loaded assembly pairs data")

    # Output directory
    output_dir = "Figure/Assembly_effect"
    os.makedirs(output_dir, exist_ok=True)

    # Generate pie charts
    plot_assembly_effect_pies(assembly_data, colors, isolate_idx, output_dir)

    print("\n" + "="*60)
    print("COMPLETED!")
    print("="*60)
    print(f"\nAll assembly effect pie charts saved to: {output_dir}/")

if __name__ == "__main__":
    main()
