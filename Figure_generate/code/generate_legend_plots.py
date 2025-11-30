#!/usr/bin/env python3
"""
Generate community composition plots with comprehensive legends for coalescence experiments.

This script fixes the matplotlib compatibility issues in the original notebook and 
creates stacked bar plots with detailed metadata including vector decomposition 
results and coalescence classifications.
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

def get_colormap_for_subcommunities():
    """Get red and blue colormaps for subcommunities."""
    def get_colormap(name='inferno', n=43):
        try:
            cmap = plt.colormaps.get_cmap(name).resampled(n)
        except AttributeError:
            cmap = cm.get_cmap(name, n)
        return [cmap(i)[:3] for i in range(n)]

    # Blue gradient for sub1, Red gradient for sub2
    colormap_sub1 = get_colormap('Reds', 53)[5:-5] 
    colormap_sub2 = get_colormap('Blues', 53)[5:-5]
    
    return colormap_sub1, colormap_sub2

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

def get_species_pool_number(parent1_id, parent2_id, offspring_id):
    """Extract species pool number from coalescence data."""
    # Find the coalescence event
    coal_row = Coalescence_data[
        (Coalescence_data['SampleIDX'] == offspring_id) &
        (Coalescence_data['SampleIDX_Sub1'] == parent1_id) &
        (Coalescence_data['SampleIDX_Sub2'] == parent2_id)
    ]
    
    if not coal_row.empty:
        # Try to get SpeciesPool column if it exists
        if 'SpeciesPool' in coal_row.columns:
            return coal_row.iloc[0]['SpeciesPool']
        # Otherwise infer from sample IDs or default
        else:
            return 12  # Default assumption
    return "unknown"

def plot_community_composition_with_legend(parent1_vector, parent2_vector, mixture_vector, 
                          parent1_id, parent2_id, mixture_id,
                          colors, isolate_idx, nutrient_condition,
                          save_path=None, show_plot=False):
    """
    Create a stacked bar plot with comprehensive legend using red/blue color scheme.
    Mixed community is sorted by parent origin.
    """
    # Calculate vector decomposition with error handling
    try:
        x1, x2, x3 = metric_VectorDecomposition_onlyPositive(parent1_vector, parent2_vector, mixture_vector)
        
        # Handle NaN or invalid values
        if np.isnan(x1) or np.isnan(x2) or np.isnan(x3):
            x1, x2, x3 = 0.0, 0.0, 1.0  # Default to restructuring
    except:
        x1, x2, x3 = 0.0, 0.0, 1.0  # Default to restructuring
    
    # Calculate asymmetry metrics for classification with error handling
    try:
        x_metric, y_metric = calculate_assymetricity(x1, x2, x3)
        
        # Handle NaN values
        if np.isnan(x_metric) or np.isnan(y_metric):
            x_metric, y_metric = 0.0, 0.0
            
        coal_class = characterize_case(x_metric, y_metric)
        
        # Handle None return from characterize_case
        if coal_class is None:
            coal_class = 2  # Default to restructuring
            
    except:
        x_metric, y_metric = 0.0, 0.0
        coal_class = 2  # Default to restructuring
    
    # Map class to name
    class_names = {0: "Dominance", 1: "Mixing", 2: "Restructuring"}
    coal_type = class_names[coal_class]
    
    # Get species pool number
    species_pool = get_species_pool_number(parent1_id, parent2_id, mixture_id)
    
    # Get colormaps
    colormap_sub1, colormap_sub2 = get_colormap_for_subcommunities()
    
    # Determine which species come from which parent
    parent1_mask = (parent1_vector > parent2_vector)
    parent2_mask = (parent2_vector > parent1_vector)
    
    # Create figure with extra space for legend
    fig = plt.figure(figsize=(8, 4))  # Wider to accommodate legend
    fig.patch.set_alpha(0)
    
    # Create subplot with adjusted position
    ax = plt.subplot(1, 1, 1)
    ax.patch.set_alpha(0)
    
    # Plot parameters - reduced x_scale to bring bars closer together
    x_scale = 2.5  # Reduced from 4 to 2.5 for less spacing
    bar_positions = np.array([0, 1, 2])  # Parent1, Parent2, Mixture
    bottom = np.zeros(3)
    
    # Reduced bar width: 2/3 of original size (0.8 * 2/3 ≈ 0.533)
    bar_width = 0.8 * x_scale * (2/3)
    
    # Create abundance matrix
    abundance_matrix = np.array([
        parent1_vector if parent1_vector is not None else np.zeros(43),
        parent2_vector if parent2_vector is not None else np.zeros(43),
        mixture_vector if mixture_vector is not None else np.zeros(43)
    ])
    
    # Plot parent communities and mixed community with different sorting
    # For parents, use taxonomic sorting
    for bar_idx in [0, 1]:  # Parent1 and Parent2
        for i in range(43):
            asv_idx = isolate_idx[i]
            abundances = abundance_matrix[bar_idx, asv_idx]
            
            if abundances > 0.001:
                # Use red colormap for parent1, blue for parent2
                if bar_idx == 0:
                    color = colormap_sub1[i]
                else:
                    color = colormap_sub2[i]
                
                ax.bar(bar_positions[bar_idx] * x_scale, abundances, 
                      width=bar_width, bottom=bottom[bar_idx], 
                      color=color, linewidth=0)
                bottom[bar_idx] += abundances
    
    # For mixed community, sort by parent origin
    # First plot species from parent1 (red colors)
    parent1_indices = np.where(parent1_mask)[0]
    for i, j in enumerate(isolate_idx):
        if j in parent1_indices:
            abundances = abundance_matrix[2, j]
            if abundances > 0.001:
                ax.bar(bar_positions[2] * x_scale, abundances, 
                      width=bar_width, bottom=bottom[2], 
                      color=colormap_sub1[i], linewidth=0)
                bottom[2] += abundances
    
    # Add a thin black line to separate parent origins
    ax.bar(bar_positions[2] * x_scale, 0, width=bar_width, 
          bottom=bottom[2], linewidth=0.5, edgecolor='black', color='red')
    
    # Then plot species from parent2 (blue colors)
    parent2_indices = np.where(parent2_mask)[0]
    for i, j in enumerate(isolate_idx):
        if j in parent2_indices:
            abundances = abundance_matrix[2, j]
            if abundances > 0.001:
                ax.bar(bar_positions[2] * x_scale, abundances, 
                      width=bar_width, bottom=bottom[2], 
                      color=colormap_sub2[i], linewidth=0)
                bottom[2] += abundances
    
    # Basic formatting
    ax.set_xticks(bar_positions * x_scale)
    ax.set_xticklabels(['Parent1', 'Parent2', 'Offspring'], fontsize=8)
    ax.set_ylabel('Relative Abundance', fontsize=8)
    ax.set_ylim(0, 1.05)  # Small space at top
    
    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    
    # Add comprehensive legend/annotation box with better formatting
    legend_text = [
        f"Offspring: {mixture_id}",
        f"Parent1: {parent1_id}",
        f"Parent2: {parent2_id}",
        "",
        f"Medium: {nutrient_condition}",
        f"Species pool: {species_pool}",
        "",
        "Vector decomposition:",
        f"  x1 (P1): {x1:.3f}",
        f"  x2 (P2): {x2:.3f}", 
        f"  x3 (res): {x3:.3f}",
        "",
        f"Type: {coal_type}",
        f"Coords: ({x_metric:.2f}, {y_metric:.2f})"
    ]
    
    # Create text box
    textstr = '\n'.join(legend_text)
    
    # Add text box to the right of the plot
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(1.02, 0.98, textstr, transform=ax.transAxes, fontsize=7,
            verticalalignment='top', bbox=props, family='monospace')
    
    # Title with basic info
    ax.set_title(f"{nutrient_condition}-S{species_pool}: {coal_type}", fontsize=10, fontweight='bold')
    
    # Add color legend
    red_patch = mpatches.Patch(color='red', label='Parent1 origin', alpha=0.6)
    blue_patch = mpatches.Patch(color='blue', label='Parent2 origin', alpha=0.6)
    ax.legend(handles=[red_patch, blue_patch], loc='lower right', fontsize=6)
    
    plt.tight_layout()
    
    # Adjust layout to prevent text cutoff
    plt.subplots_adjust(right=0.62)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight', format='svg')
        plt.savefig(save_path.replace('.svg', '.png'), dpi=150, bbox_inches='tight')
    
    if show_plot:
        plt.show()
    else:
        plt.close()
    
    return fig, coal_type, x1, x2, x3

def determine_species_pool_size(sample_id):
    """Determine species pool size based on CommunityIDX from Metadata."""
    # Find the sample in metadata
    metadata_rows = Metadata[Metadata['SampleIDX'] == sample_id]
    
    if not metadata_rows.empty:
        community_idx = int(metadata_rows.iloc[0]['CommunityIDX'])
        
        # For coalescence samples (CoalescenceType == 'C')
        if metadata_rows.iloc[0]['CoalescenceType'] == 'C':
            if community_idx <= 14:
                return 6
            elif community_idx > 14 and community_idx <= 41:
                return 12
            elif community_idx > 41 and community_idx <= 47:
                return 24
        
        # For subcommunity samples (CoalescenceType == 'S') 
        elif metadata_rows.iloc[0]['CoalescenceType'] == 'S':
            if community_idx <= 9:
                return 6
            elif community_idx > 9 and community_idx <= 18:
                return 12
            elif community_idx > 18 and community_idx <= 30:
                return 24
    
    return 12  # Default fallback

def determine_nutrient_condition(sample_id):
    """Determine nutrient condition from Metadata."""
    # Find the sample in metadata
    metadata_rows = Metadata[Metadata['SampleIDX'] == sample_id]
    
    if not metadata_rows.empty:
        medium = metadata_rows.iloc[0]['Medium']
        if medium == 'H':
            return 'HN'
        elif medium == 'M':
            return 'MN'
        elif medium == 'L':
            return 'LN'
    
    # Fallback logic if metadata doesn't work
    sample_id_str = str(sample_id)
    if 'HN' in sample_id_str or sample_id_str.startswith('HN'):
        return 'HN'
    elif 'MN' in sample_id_str or sample_id_str.startswith('MN'):
        return 'MN'
    elif 'LN' in sample_id_str or sample_id_str.startswith('LN'):
        return 'LN'
    else:
        # Default assumption for synthetic data patterns
        if sample_id_str.startswith('P4-') or sample_id_str.startswith('P1-'):
            return 'LN'  # Default assumption
        else:
            return 'unknown'

def main():
    """Main function to generate all plots with legends."""
    
    print("Loading data and generating community composition plots with legends...")
    
    # Create the missing experiment summary data if it doesn't exist
    summary_path = "Figure/FinalDayAnalysis/experiment_summary.csv"

    if not os.path.exists(summary_path):
        print("Creating missing experiment summary data...")
        
        # Create output directory
        os.makedirs("Figure/FinalDayAnalysis", exist_ok=True)
        
        experiment_data = []
        
        # Process synthetic data
        for _, row in Coalescence_data.iterrows():
            if pd.notna(row['SampleIDX']) and pd.notna(row['SampleIDX_Sub1']) and pd.notna(row['SampleIDX_Sub2']):
                
                # Get richness information
                parent1_vector = get_abundance_vector(row['SampleIDX_Sub1'])
                parent2_vector = get_abundance_vector(row['SampleIDX_Sub2'])
                mixture_vector = get_abundance_vector(row['SampleIDX'])
                
                parent1_richness = np.sum(parent1_vector > 0.001) if parent1_vector is not None else 0
                parent2_richness = np.sum(parent2_vector > 0.001) if parent2_vector is not None else 0
                mixture_richness = np.sum(mixture_vector > 0.001) if mixture_vector is not None else 0
                
                # Determine nutrient condition using metadata
                nutrient_condition = determine_nutrient_condition(row['SampleIDX'])
                
                # Determine species pool size using metadata
                species_pool_size = determine_species_pool_size(row['SampleIDX'])
                
                experiment_data.append({
                    'mixture_id': row['SampleIDX'],
                    'parent1_id': row['SampleIDX_Sub1'], 
                    'parent2_id': row['SampleIDX_Sub2'],
                    'nutrient_condition': nutrient_condition,
                    'species_pool': species_pool_size,
                    'data_type': 'synthetic',
                    'parent1_richness': parent1_richness,
                    'parent2_richness': parent2_richness,
                    'mixture_richness': mixture_richness
                })
        
        # Create DataFrame
        summary_df = pd.DataFrame(experiment_data)
        
        # Save the summary
        summary_df.to_csv(summary_path, index=False)
        
        print(f"Created experiment summary with {len(summary_df)} experiments")
    else:
        print("Loading existing experiment summary...")

    # Load the processed data from our analysis
    summary_df = pd.read_csv(summary_path)
    print(f"Loaded {len(summary_df)} experiments")
    print("Distribution by condition and species pool:")
    print(summary_df.groupby(['nutrient_condition', 'species_pool']).size())
    
    # Get colormaps
    colors, isolate_idx = get_taxonomic_colormap_and_sorting()
    print("Generated colormaps - Red for Parent1, Blue for Parent2")

    # Generate ALL coalescence plots organized by condition AND species pool size
    print("Generating all coalescence plots with comprehensive metadata...")
    print("Organizing by: Nutrient Condition (HN/MN/LN) → Species Pool (s6/s12/s24)")

    # Base output directory
    base_output_dir = "Figure/FinalDayPlots_with_Legend"
    os.makedirs(base_output_dir, exist_ok=True)

    # Group experiments by condition AND species pool
    condition_species_groups = summary_df.groupby(['nutrient_condition', 'species_pool'])
    total_plots = 0
    skipped_plots = 0

    # Track coalescence type statistics
    coal_type_stats = {}
    for condition in summary_df['nutrient_condition'].unique():
        for species_pool in summary_df['species_pool'].unique():
            coal_type_stats[f"{condition}_S{species_pool}"] = {"Dominance": 0, "Mixing": 0, "Restructuring": 0}

    for (condition, species_pool), group in condition_species_groups:
        print(f"\n=== Processing {condition} - Species Pool {species_pool} ===")
        print(f"Total experiments: {len(group)}")
        
        # Create nested subfolders: condition/species_pool/
        condition_dir = os.path.join(base_output_dir, condition)
        species_pool_dir = os.path.join(condition_dir, f"s{species_pool}")
        os.makedirs(species_pool_dir, exist_ok=True)
        
        condition_plots = 0
        condition_skipped = 0
        
        # Process ALL experiments in this condition-species_pool combination
        for i, (_, row) in enumerate(group.iterrows()):
            
            # Get abundance vectors
            parent1_vector = get_abundance_vector(row['parent1_id'])
            parent2_vector = get_abundance_vector(row['parent2_id'])
            mixture_vector = get_abundance_vector(row['mixture_id'])
            
            if parent1_vector is None or parent2_vector is None or mixture_vector is None:
                condition_skipped += 1
                continue
            
            # Create filename
            filename = f"{row['mixture_id']}_{row['parent1_id']}_to_{row['parent2_id']}_annotated.svg"
            save_path = os.path.join(species_pool_dir, filename)
            
            # Generate plot with legend
            fig, coal_type, x1, x2, x3 = plot_community_composition_with_legend(
                parent1_vector, parent2_vector, mixture_vector,
                row['parent1_id'], row['parent2_id'], row['mixture_id'],
                colors, isolate_idx, condition,
                save_path=save_path, show_plot=False
            )
            
            # Update statistics
            coal_type_stats[f"{condition}_S{species_pool}"][coal_type] += 1
            condition_plots += 1
            
            # Print progress every 20 plots for each condition-species combination
            if condition_plots % 20 == 0:
                print(f"  Generated {condition_plots} plots for {condition}-S{species_pool}...")
        
        print(f"✓ {condition}-S{species_pool}: Generated {condition_plots} plots, skipped {condition_skipped}")
        print(f"   Saved to: {species_pool_dir}/")
        total_plots += condition_plots
        skipped_plots += condition_skipped

    print(f"\nCOMPLETED!")
    print(f"Total plots generated: {total_plots}")
    print(f"Total plots skipped (missing data): {skipped_plots}")

    print(f"\nFolder Structure Created:")
    print(f"├── {base_output_dir}/")
    for condition in summary_df['nutrient_condition'].unique():
        print(f"│   ├── {condition}/")
        for species_pool in sorted(summary_df[summary_df['nutrient_condition'] == condition]['species_pool'].unique()):
            count = len(summary_df[(summary_df['nutrient_condition'] == condition) & 
                                   (summary_df['species_pool'] == species_pool)])
            print(f"│   │   └── s{species_pool}/ ({count} plots)")

    # Print coalescence type statistics by condition and species pool
    print("\n=== COALESCENCE TYPE STATISTICS BY SPECIES POOL ===")
    for key, stats in coal_type_stats.items():
        total = sum(stats.values())
        if total > 0:
            print(f"\n{key}:")
            for coal_type, count in stats.items():
                percentage = (count / total) * 100
                print(f"  {coal_type}: {count} ({percentage:.1f}%)")

    # Create a summary CSV with all vector decomposition results
    print("\nCreating summary CSV with vector decomposition results...")

    vector_results = []

    for _, row in summary_df.iterrows():
        # Get abundance vectors
        parent1_vector = get_abundance_vector(row['parent1_id'])
        parent2_vector = get_abundance_vector(row['parent2_id'])
        mixture_vector = get_abundance_vector(row['mixture_id'])
        
        if parent1_vector is None or parent2_vector is None or mixture_vector is None:
            continue
        
        # Calculate vector decomposition
        try:
            x1, x2, x3 = metric_VectorDecomposition_onlyPositive(parent1_vector, parent2_vector, mixture_vector)
        except:
            x1, x2, x3 = 0.0, 0.0, 1.0
        
        # Calculate classification
        try:
            x_metric, y_metric = calculate_assymetricity(x1, x2, x3)
            coal_class = characterize_case(x_metric, y_metric)
            if coal_class is None:
                coal_class = 2
        except:
            x_metric, y_metric = 0.0, 0.0
            coal_class = 2
            
        class_names = {0: "Dominance", 1: "Mixing", 2: "Restructuring"}
        coal_type = class_names[coal_class]
        
        vector_results.append({
            'mixture_id': row['mixture_id'],
            'parent1_id': row['parent1_id'],
            'parent2_id': row['parent2_id'],
            'nutrient_condition': row['nutrient_condition'],
            'species_pool': row['species_pool'],
            'x1_parent1_contribution': x1,
            'x2_parent2_contribution': x2,
            'x3_residual': x3,
            'x_metric': x_metric,
            'y_metric': y_metric,
            'coalescence_type': coal_type,
            'parent1_richness': row['parent1_richness'],
            'parent2_richness': row['parent2_richness'],
            'mixture_richness': row['mixture_richness']
        })

    # Save to CSV
    vector_df = pd.DataFrame(vector_results)
    vector_csv_path = os.path.join(base_output_dir, "vector_decomposition_results.csv")
    vector_df.to_csv(vector_csv_path, index=False)

    print(f"Saved vector decomposition results to: {vector_csv_path}")
    print(f"Total experiments analyzed: {len(vector_df)}")

    # Show summary statistics
    print("\n=== VECTOR DECOMPOSITION SUMMARY ===")
    for condition in vector_df['nutrient_condition'].unique():
        condition_data = vector_df[vector_df['nutrient_condition'] == condition]
        print(f"\n{condition} (n={len(condition_data)}):")
        print(f"  x1 (P1): {condition_data['x1_parent1_contribution'].mean():.3f} ± {condition_data['x1_parent1_contribution'].std():.3f}")
        print(f"  x2 (P2): {condition_data['x2_parent2_contribution'].mean():.3f} ± {condition_data['x2_parent2_contribution'].std():.3f}")
        print(f"  x3 (residual): {condition_data['x3_residual'].mean():.3f} ± {condition_data['x3_residual'].std():.3f}")

    print("\nAll plots and analysis completed successfully!")

if __name__ == "__main__":
    main()