#!/usr/bin/env python3
"""
Final Day Community Composition Plotter
========================================

This script creates stacked bar plots showing the final day composition of parent 
and child communities for all coalescence experiments, using the same plotting 
style as the timeseries notebook.

Features:
- Loads data for all medium conditions (LN/MN/HN) and species pools (6/12/24)
- Creates side-by-side plots showing parent communities and their coalescence offspring
- Uses consistent color schemes and taxonomy-based sorting from timeseries plots
- Saves plots organized by condition and experiment type

Usage:
    python plot_final_day_communities.py
"""

import os
import sys
import numpy as np
import pandas as pd

# Add path for imports
sys.path.append('.')

# Import existing setup that has working matplotlib configuration
from common_setup import *
from matplotlib import cm

def load_coalescence_data():
    """
    Load coalescence data from common_setup module.
    Returns coalescence experiments and processed sequence data.
    """
    try:
        # Data should already be loaded from common_setup import
        # Combine synthetic and natural sequence data
        processed_sequences = pd.concat([
            Processed_sequences_synthetic, 
            Processed_sequences_natural
        ], ignore_index=True)
        
        return Coalescence_data, processed_sequences
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def get_taxonomic_colormap_and_sorting():
    """
    Generate taxonomy-based colormap and isolate sorting index.
    Based on the taxonomy data from new_Plot_timeseries.ipynb
    """
    # Taxonomy data from the notebook
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
    
    # Sort isolates by phylogeny (same as notebook)
    sorted_data = sorted(data, key=lambda x: x[2:])
    isolate_idx = [data.index(row) for row in sorted_data]
    
    # Generate colormap (inferno with shuffling, same seed as notebook)
    np.random.seed(4)
    inferno = cm.get_cmap('inferno', 43)
    colors = [inferno(i)[:3] for i in range(43)]
    np.random.shuffle(colors)
    
    return colors, isolate_idx

def get_colormap_for_subcommunities():
    """
    Get red and blue colormaps for subcommunities (same as notebook).
    """
    def get_colormap(name='inferno', n=43):
        cmap = cm.get_cmap(name, n)
        return [cmap(i)[:3] for i in range(n)]

    # Blue gradient for sub1, Red gradient for sub2
    colormap_sub1 = get_colormap('Reds', 53)[5:-5] 
    colormap_sub2 = get_colormap('Blues', 53)[5:-5]
    
    return colormap_sub1, colormap_sub2

def get_abundance_vector(processed_sequences, sample_id):
    """
    Extract abundance vector for a given sample ID.
    """
    sample_rows = processed_sequences[processed_sequences['SampleIDX'] == sample_id]
    if sample_rows.empty:
        return None
    
    # Get abundance values (columns 1-43, skipping SampleIDX)
    abundance_vector = sample_rows.iloc[0, 1:44].values.astype(float)
    abundance_vector = np.nan_to_num(abundance_vector, 0)
    
    # Normalize
    if abundance_vector.sum() > 0:
        abundance_vector = abundance_vector / abundance_vector.sum()
    
    return abundance_vector

def create_community_bar_plot(abundance_vectors, labels, colors, isolate_idx, title="", 
                            figsize=(12, 6), save_path=None):
    """
    Create a stacked bar plot showing community composition.
    
    Parameters:
        abundance_vectors: List of abundance vectors
        labels: List of sample labels  
        colors: Color map for ASVs
        isolate_idx: Sorting index for ASVs
        title: Plot title
        figsize: Figure size
        save_path: Path to save figure
    """
    mm = 0.1/2.54  # Convert to mm like in notebook
    n_samples = len(abundance_vectors)
    
    fig, ax = plt.subplots(1, figsize=(n_samples * 6 * mm * 10, 8 * 4 * mm * 10), 
                          facecolor='w', edgecolor='k')
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    
    x_scale = 4
    bar_positions = np.array(range(n_samples))
    bottom = np.zeros(n_samples)
    
    # Plot in taxonomic order
    for i in range(43):
        asv_idx = isolate_idx[i]  # Get the actual ASV index
        color = colors[i]
        
        # Get abundances for this ASV across all samples
        abundances = [vec[asv_idx] if vec is not None else 0 for vec in abundance_vectors]
        abundances = np.array(abundances)
        
        # Only plot if there's some abundance
        if np.any(abundances > 0):
            ax.bar(bar_positions * x_scale, abundances, width=0.8 * x_scale, 
                  bottom=bottom, color=color, linewidth=0, 
                  label=f'ASV{asv_idx + 1}')
            bottom += abundances
    
    # Formatting
    ax.set_xticks(bar_positions * x_scale)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=6)
    ax.set_ylabel('Relative Abundance', fontsize=8)
    ax.set_title(title, fontsize=10, fontweight='bold')
    
    # Remove spines and ticks (consistent with notebook style)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(left=False, bottom=False)
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight', format='svg')
        plt.savefig(save_path.replace('.svg', '.png'), dpi=300, bbox_inches='tight')
        print(f"Saved plot: {save_path}")
    
    plt.close()

def extract_experiment_info(row):
    """
    Extract experiment information from coalescence data row.
    """
    # Map medium to nutrient condition
    medium_mapping = {'L': 'LN', 'M': 'MN', 'H': 'HN'}
    nutrient_condition = medium_mapping.get(row['Medium'])
    
    # Get species pool size
    species_pool = row.get('SpeciesPool', 12)  # Default to 12 if not specified
    
    # Determine data type (synthetic vs natural)
    data_type = 'synthetic' if 'P' in row['SampleIDX'] else 'natural'
    
    return nutrient_condition, species_pool, data_type

def main():
    """
    Main function to create all final day community plots.
    """
    print("Loading coalescence data...")
    coalescence_data, processed_sequences = load_coalescence_data()
    
    if coalescence_data is None or processed_sequences is None:
        print("Failed to load data. Exiting.")
        return
    
    print("Getting colormap and taxonomy sorting...")
    colors, isolate_idx = get_taxonomic_colormap_and_sorting()
    colormap_sub1, colormap_sub2 = get_colormap_for_subcommunities()
    
    # Create output directory
    output_dir = "Figure/FinalDayPlots"
    os.makedirs(output_dir, exist_ok=True)
    
    # Group experiments by condition
    experiments_by_condition = {}
    
    print("Processing coalescence experiments...")
    for idx, row in coalescence_data.iterrows():
        try:
            # Extract experiment info
            nutrient_condition, species_pool, data_type = extract_experiment_info(row)
            
            if nutrient_condition is None:
                continue
            
            # Get sample IDs
            mixture_sample_id = row['SampleIDX']
            parent1_sample_id = row['SampleIDX_Sub1']
            parent2_sample_id = row['SampleIDX_Sub2']
            
            # Get abundance vectors
            mixture_vector = get_abundance_vector(processed_sequences, mixture_sample_id)
            parent1_vector = get_abundance_vector(processed_sequences, parent1_sample_id)
            parent2_vector = get_abundance_vector(processed_sequences, parent2_sample_id)
            
            if mixture_vector is None or parent1_vector is None or parent2_vector is None:
                print(f"Missing data for experiment: {mixture_sample_id}")
                continue
            
            # Create experiment key
            exp_key = f"{nutrient_condition}_{species_pool}_{data_type}"
            
            if exp_key not in experiments_by_condition:
                experiments_by_condition[exp_key] = []
            
            experiments_by_condition[exp_key].append({
                'mixture_id': mixture_sample_id,
                'parent1_id': parent1_sample_id,
                'parent2_id': parent2_sample_id,
                'mixture_vector': mixture_vector,
                'parent1_vector': parent1_vector,
                'parent2_vector': parent2_vector,
                'row_data': row
            })
            
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue
    
    print(f"Found {len(experiments_by_condition)} experimental conditions:")
    for key, experiments in experiments_by_condition.items():
        print(f"  {key}: {len(experiments)} experiments")
    
    # Create plots for each condition
    for condition_key, experiments in experiments_by_condition.items():
        print(f"\nCreating plots for {condition_key}...")
        
        for i, exp in enumerate(experiments):
            # Create individual experiment plot
            abundance_vectors = [
                exp['parent1_vector'],
                exp['parent2_vector'], 
                exp['mixture_vector']
            ]
            
            labels = [
                f"Parent1\n({exp['parent1_id']})",
                f"Parent2\n({exp['parent2_id']})",
                f"Offspring\n({exp['mixture_id']})"
            ]
            
            title = f"{condition_key} - Experiment {i+1}"
            
            save_path = os.path.join(output_dir, condition_key, 
                                   f"experiment_{i+1:02d}_{exp['mixture_id']}.svg")
            
            create_community_bar_plot(
                abundance_vectors, labels, colors, isolate_idx,
                title=title, save_path=save_path
            )
        
        # Create summary plot for all experiments in this condition
        if len(experiments) > 1:
            print(f"Creating summary plot for {condition_key}...")
            
            all_vectors = []
            all_labels = []
            
            for i, exp in enumerate(experiments):
                all_vectors.extend([
                    exp['parent1_vector'],
                    exp['parent2_vector'],
                    exp['mixture_vector']
                ])
                all_labels.extend([
                    f"P1-{i+1}",
                    f"P2-{i+1}",
                    f"O-{i+1}"
                ])
            
            save_path = os.path.join(output_dir, condition_key, f"summary_{condition_key}.svg")
            
            create_community_bar_plot(
                all_vectors, all_labels, colors, isolate_idx,
                title=f"{condition_key} - All Experiments", save_path=save_path
            )
    
    print(f"\nAll plots saved to: {output_dir}")
    print("Done!")

if __name__ == "__main__":
    main()