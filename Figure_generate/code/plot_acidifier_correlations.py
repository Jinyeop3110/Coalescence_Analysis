#!/usr/bin/env python3
"""
Create small plots showing negative correlations for acidifier species
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

def load_parent_data():
    """Load parent community data"""
    # Load abundance data
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    # Load metadata and communities data
    metadata = pd.read_excel("../../Postprocessed/Metadata.xlsx")
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    # Merge all data
    full_data = abundance_data.merge(
        metadata[['SampleIDX', 'CoalescenceType', 'Medium', 'CommunityIDX']], 
        on='SampleIDX', how='inner'
    ).merge(
        communities_data[['SampleIDX', 'fieldPH1', 'fieldPH7']], 
        on='SampleIDX', how='inner'
    )
    
    # Filter for parent communities only
    parent_communities = full_data[full_data['CoalescenceType'] == 'S'].copy()
    parent_communities = parent_communities[~parent_communities['fieldPH7'].isna()].copy()
    
    return parent_communities

def create_acidifier_plot_by_medium(medium_type):
    """Create small plot for acidifier species (3, 8, 12) for specific medium"""
    parent_data = load_parent_data()
    
    # Filter by medium
    medium_data = parent_data[parent_data['Medium'] == medium_type]
    
    acidifier_species = ['NormalizedAbundance3', 'NormalizedAbundance8', 'NormalizedAbundance12']
    asv_labels = ['ASV 3', 'ASV 8', 'ASV 12']
    color = 'red' if medium_type == 'H' else 'darkred'
    
    fig, axes = plt.subplots(1, 3, figsize=(6, 2))
    
    for idx, (species, asv_label) in enumerate(zip(acidifier_species, asv_labels)):
        ax = axes[idx]
        
        x = medium_data[species].values
        y = medium_data['fieldPH7'].values
        
        # Remove missing values
        valid_mask = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[valid_mask]
        y_clean = y[valid_mask]
        
        if len(x_clean) > 5:
            # Calculate correlation
            r, p = stats.pearsonr(x_clean, y_clean)
            
            # Plot scatter
            ax.scatter(x_clean, y_clean, alpha=0.4, s=8, color=color)
            
            # Add trendline
            z = np.polyfit(x_clean, y_clean, 1)
            p_trend = np.poly1d(z)
            x_trend = np.linspace(x_clean.min(), x_clean.max(), 50)
            ax.plot(x_trend, p_trend(x_trend), color=color, linestyle='-', linewidth=1.5)
        
        # Add subplot label
        ax.text(0.95, 0.95, asv_label, transform=ax.transAxes, fontsize=12, fontweight='bold',
                verticalalignment='top', horizontalalignment='right')
        
        ax.tick_params(labelsize=8)
        ax.set_xlim(left=0)
        ax.set_ylim(3.5, 9.5)
    
    plt.tight_layout()
    
    # Save plot
    output_dir = "Figure/pH_Analysis"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    plt.savefig(f'{output_dir}/acidifiers_{medium_type}_medium.svg', bbox_inches='tight')
    
    print(f"✓ Acidifier plot saved for medium {medium_type}:")
    print(f"  - {output_dir}/acidifiers_{medium_type}_medium.svg")

def create_alkalizer_plot_by_medium(medium_type):
    """Create small plot for alkalizer species (9, 11) for specific medium"""
    parent_data = load_parent_data()
    
    # Filter by medium
    medium_data = parent_data[parent_data['Medium'] == medium_type]
    
    alkalizer_species = ['NormalizedAbundance9', 'NormalizedAbundance11']
    asv_labels = ['ASV 9', 'ASV 11']
    color = 'blue' if medium_type == 'H' else 'darkblue'
    
    fig, axes = plt.subplots(1, 2, figsize=(4, 2))
    
    for idx, (species, asv_label) in enumerate(zip(alkalizer_species, asv_labels)):
        ax = axes[idx]
        
        x = medium_data[species].values
        y = medium_data['fieldPH7'].values
        
        # Remove missing values
        valid_mask = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[valid_mask]
        y_clean = y[valid_mask]
        
        if len(x_clean) > 5:
            # Calculate correlation
            r, p = stats.pearsonr(x_clean, y_clean)
            
            # Plot scatter
            ax.scatter(x_clean, y_clean, alpha=0.4, s=8, color=color)
            
            # Add trendline
            z = np.polyfit(x_clean, y_clean, 1)
            p_trend = np.poly1d(z)
            x_trend = np.linspace(x_clean.min(), x_clean.max(), 50)
            ax.plot(x_trend, p_trend(x_trend), color=color, linestyle='-', linewidth=1.5)
        
        # Add subplot label
        ax.text(0.95, 0.95, asv_label, transform=ax.transAxes, fontsize=12, fontweight='bold',
                verticalalignment='top', horizontalalignment='right')
        
        ax.tick_params(labelsize=8)
        ax.set_xlim(left=0)
        ax.set_ylim(3.5, 9.5)
    
    plt.tight_layout()
    
    # Save plot
    output_dir = "Figure/pH_Analysis"
    
    plt.savefig(f'{output_dir}/alkalizers_{medium_type}_medium.svg', bbox_inches='tight')
    
    print(f"✓ Alkalizer plot saved for medium {medium_type}:")
    print(f"  - {output_dir}/alkalizers_{medium_type}_medium.svg")

def print_correlation_stats():
    """Print correlation statistics for all analyzed species"""
    parent_data = load_parent_data()
    species_to_analyze = ['NormalizedAbundance3', 'NormalizedAbundance12', 'NormalizedAbundance8', 
                         'NormalizedAbundance9', 'NormalizedAbundance11']
    
    print("\nCORRELATION STATISTICS:")
    print("=" * 50)
    
    for species in species_to_analyze:
        print(f"\n{species}:")
        
        for medium in ['H', 'M', 'L']:
            medium_data = parent_data[parent_data['Medium'] == medium]
            
            if len(medium_data) > 5:
                x = medium_data[species].values
                y = medium_data['fieldPH7'].values
                
                valid_mask = ~(np.isnan(x) | np.isnan(y))
                x_clean = x[valid_mask]
                y_clean = y[valid_mask]
                
                if len(x_clean) > 5:
                    r, p = stats.pearsonr(x_clean, y_clean)
                    sig = "*" if p < 0.05 else " "
                    print(f"  Medium {medium}: r = {r:6.3f}{sig}, p = {p:.4f}, n = {len(x_clean)}")

if __name__ == "__main__":
    print("Creating correlation plots for H and M media...")
    
    print("1. Acidifier species (3, 8, 12):")
    print("   H medium:")
    create_acidifier_plot_by_medium('H')
    print("   M medium:")
    create_acidifier_plot_by_medium('M')
    
    print("\n2. Alkalizer species (9, 11):")
    print("   H medium:")
    create_alkalizer_plot_by_medium('H')
    print("   M medium:")
    create_alkalizer_plot_by_medium('M')
    
    print("\n3. Correlation statistics:")
    print_correlation_stats()