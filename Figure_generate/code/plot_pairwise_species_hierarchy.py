#!/usr/bin/env python3
"""
plot_pairwise_species_hierarchy.py

Purpose: Plots TRUE species-to-species competition hierarchy from pairwise coculture experiments
Key features:
- Uses actual colony counting data from pairwise species competitions
- Creates dominance matrices based on experimental outcomes
- Generates hierarchy heatmaps for different nutrient conditions
- Calculates hierarchy scores from real competition data

Author: Gore Lab Coalescence Analysis Team
Date: January 2025
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent popups
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import os
import warnings
warnings.filterwarnings('ignore')
plt.ioff()  # Turn off interactive mode

# Set up plotting style
sns.set_style("ticks")
plt.rcParams.update({
    'legend.fontsize': 'x-large',
    'figure.figsize': (15, 5),
    'axes.labelsize': 'x-large',
    'axes.titlesize': 'x-large',
    'xtick.labelsize': 'large',
    'ytick.labelsize': 'large',
    'font.family': 'Arial',
    'axes.linewidth': 0.5
})

# Create output directory
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Hiearchy"
os.makedirs(output_dir, exist_ok=True)

def getPairwiseCountData():
    """Load pairwise species competition data from colony counting experiments"""
    Pairwise_Count_data_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Postprocessed/PairwiseColonyCountings_processed_230915.xlsx"
    
    Mono_Count_data = {}
    Pairwise_Count_data = {}
    
    # Load monoculture data for each medium
    # Sheet 0: LN monoculture
    Data = pd.read_excel(Pairwise_Count_data_path, sheet_name=0)
    Data = np.transpose(np.array(Data.values[:, 1:]))
    Mono_Count_data["LN"] = Data
    
    # Sheet 1: MN monoculture
    Data = pd.read_excel(Pairwise_Count_data_path, sheet_name=1)
    Data = np.transpose(np.array(Data.values[:, 1:]))
    Mono_Count_data["MN"] = Data
    
    # Sheet 2: HN monoculture
    Data = pd.read_excel(Pairwise_Count_data_path, sheet_name=2)
    Data = np.transpose(np.array(Data.values[:, 1:]))
    Mono_Count_data["HN"] = Data
    
    # Load pairwise competition data
    # Sheets 3-4: LN pairwise
    Data_1 = pd.read_excel(Pairwise_Count_data_path, sheet_name=3).values[:, 1:]
    Data_2 = pd.read_excel(Pairwise_Count_data_path, sheet_name=4).values[:, 1:]
    Pairwise_Count_data["LN"] = np.stack([Data_1, Data_2])
    
    # Sheets 5-6: MN pairwise
    Data_1 = pd.read_excel(Pairwise_Count_data_path, sheet_name=5).values[:, 1:]
    Data_2 = pd.read_excel(Pairwise_Count_data_path, sheet_name=6).values[:, 1:]
    Pairwise_Count_data["MN"] = np.stack([Data_1, Data_2])
    
    # Sheets 7-8: HN pairwise
    Data_1 = pd.read_excel(Pairwise_Count_data_path, sheet_name=7).values[:, 1:]
    Data_2 = pd.read_excel(Pairwise_Count_data_path, sheet_name=8).values[:, 1:]
    Pairwise_Count_data["HN"] = np.stack([Data_1, Data_2])
    
    return Mono_Count_data, Pairwise_Count_data

def getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium_type):
    """Process pairwise count data to get dominance ratios"""
    data_m = np.mean(Mono_Count_data[medium_type], 1)  # Mean monoculture counts
    data_p_1 = Pairwise_Count_data[medium_type][0, :]  # Species 1 in pairwise
    data_p_2 = Pairwise_Count_data[medium_type][1, :]  # Species 2 in pairwise
    
    data_flag = np.array([[None] * 12] * 12)
    data_p_ratio = np.zeros((12, 12))
    
    for i in range(12):
        for j in range(12):
            if np.isnan(data_p_1[i, j]):
                data_flag[i, j] = 'case0'  # No data
                data_p_ratio[i, j] = np.nan
            elif i == j:
                data_p_ratio[i, j] = 0.5  # Self-interaction
                data_flag[i, j] = 'self'
            else:
                if data_p_1[i, j] == 1 and data_p_2[i, j] == 0:
                    # Species i completely dominates
                    data_flag[i, j] = 'case1'
                    data_p_ratio[i, j] = 1.0
                elif data_p_1[i, j] == 0 and data_p_2[i, j] == 1:
                    # Species j completely dominates
                    data_flag[i, j] = 'case2'
                    data_p_ratio[i, j] = 0.0
                else:
                    # Coexistence - normalize by monoculture counts
                    data_flag[i, j] = 'case3'
                    norm_1 = data_p_1[i, j] / data_m[i] if data_m[i] > 0 else 0
                    norm_2 = data_p_2[i, j] / data_m[j] if data_m[j] > 0 else 0
                    total = norm_1 + norm_2
                    if total > 0:
                        data_p_ratio[i, j] = norm_1 / total
                    else:
                        data_p_ratio[i, j] = 0.5
    
    return data_flag, data_p_ratio

def calculate_hierarchy_score(matrix):
    """Calculate hierarchy score from dominance matrix"""
    # Remove NaN values for calculation
    valid_mask = ~np.isnan(matrix)
    
    # Get mean of each row (excluding NaN)
    row_means = np.nanmean(matrix, axis=1)
    valid_rows = ~np.isnan(row_means)
    
    if np.sum(valid_rows) < 2:
        return np.nan
    
    # Sort by competitive ability
    sorted_indices = np.argsort(-row_means[valid_rows])
    
    # Create sorted submatrix with only valid rows/columns
    valid_indices = np.where(valid_rows)[0][sorted_indices]
    sorted_matrix = matrix[valid_indices][:, valid_indices]
    
    # Get lower triangle mask
    mask = np.tril(np.ones_like(sorted_matrix), k=-1).astype(bool)
    valid_mask_sorted = ~np.isnan(sorted_matrix)
    combined_mask = mask & valid_mask_sorted
    
    lower_triangle_values = sorted_matrix[combined_mask]
    
    if len(lower_triangle_values) > 0:
        hierarchy_score = 1 - np.mean(lower_triangle_values)
    else:
        hierarchy_score = 0.5
    
    return hierarchy_score

def plot_pairwise_species_hierarchy(medium='MN'):
    """Plot species-to-species hierarchy from pairwise competition data"""
    
    print(f"\nProcessing {medium} pairwise species competition data...")
    
    # Load data
    Mono_Count_data, Pairwise_Count_data = getPairwiseCountData()
    
    # Process data to get dominance matrix
    data_flag, data_p_ratio = getProcessedPairwiseCountData(
        Mono_Count_data, Pairwise_Count_data, medium)
    
    # Create figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Plot 1: Dominance matrix heatmap
    mask = np.isnan(data_p_ratio)
    sns.heatmap(data_p_ratio, annot=True, fmt='.2f', cmap='YlGnBu', 
                vmin=0, vmax=1, mask=mask, ax=ax1, square=True,
                cbar_kws={'label': 'Dominance of ASV i over j'})
    ax1.set_xlabel('ASV j')
    ax1.set_ylabel('ASV i')
    ax1.set_title(f'{medium}: Pairwise Species Dominance Matrix')
    
    # Add ASV labels (1-12 instead of 0-11)
    species_labels = [str(i+1) for i in range(12)]
    ax1.set_xticklabels(species_labels)
    ax1.set_yticklabels(species_labels)
    
    # Plot 2: Sorted by competitive ability
    row_means = np.nanmean(data_p_ratio, axis=1)
    sorted_idx = np.argsort(-row_means)  # Sort by decreasing competitive ability
    
    # Create sorted matrix
    sorted_matrix = data_p_ratio[sorted_idx][:, sorted_idx]
    sorted_labels = [species_labels[i] for i in sorted_idx]
    
    mask_sorted = np.isnan(sorted_matrix)
    sns.heatmap(sorted_matrix, annot=True, fmt='.2f', cmap='YlGnBu',
                vmin=0, vmax=1, mask=mask_sorted, ax=ax2, square=True,
                cbar_kws={'label': 'Dominance (sorted)'})
    ax2.set_xlabel('ASV (sorted by ability)')
    ax2.set_ylabel('ASV (sorted by ability)')
    ax2.set_title(f'{medium}: Sorted by Competitive Ability')
    ax2.set_xticklabels(sorted_labels)
    ax2.set_yticklabels(sorted_labels)
    
    # Calculate hierarchy score
    hierarchy_score = calculate_hierarchy_score(data_p_ratio)
    ax2.text(0.02, 0.98, f'Hierarchy Score: {hierarchy_score:.3f}',
             transform=ax2.transAxes, va='top', ha='left',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 3: Competitive ranking
    ax3.bar(range(12), row_means[sorted_idx])
    ax3.set_xlabel('ASV (sorted by competitive ability)')
    ax3.set_ylabel('Mean Dominance Score')
    ax3.set_title(f'{medium}: ASV Competitive Ranking')
    ax3.set_xticks(range(12))
    ax3.set_xticklabels(sorted_labels, rotation=45)
    ax3.set_ylim([0, 1])
    
    # Add grid
    ax3.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    filename = f"Pairwise_Species_Hierarchy_{medium}.svg"
    plt.savefig(os.path.join(output_dir, filename), format='svg', bbox_inches='tight')
    plt.close()
    
    print(f"{medium} Hierarchy Score: {hierarchy_score:.3f}")
    print(f"Saved: {filename}")
    
    # Also save separate versions for ASV-ordered and competence-ordered
    plot_separate_versions(medium, data_p_ratio, species_labels, 
                          sorted_idx, sorted_labels, hierarchy_score)
    
    return hierarchy_score, data_p_ratio

def plot_separate_versions(medium, data_p_ratio, species_labels, 
                          sorted_idx, sorted_labels, hierarchy_score):
    """Generate separate plots for ASV-ordered and competence-ordered versions"""
    
    # Version 1: ASV-ordered (original order)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    mask = np.isnan(data_p_ratio)
    sns.heatmap(data_p_ratio, annot=True, fmt='.2f', cmap='YlGnBu', 
                vmin=0, vmax=1, mask=mask, ax=ax, square=True,
                cbar_kws={'label': 'Dominance of ASV i over j'})
    ax.set_xlabel('ASV j')
    ax.set_ylabel('ASV i')
    ax.set_title(f'{medium}: Pairwise Species Dominance Matrix\n(Ordered by ASV Number)')
    ax.set_xticklabels(species_labels)
    ax.set_yticklabels(species_labels)
    
    plt.tight_layout()
    filename = f"Pairwise_Species_Hierarchy_{medium}_ASV_ordered.svg"
    plt.savefig(os.path.join(output_dir, filename), format='svg', bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, filename.replace('.svg', '.png')), 
                format='png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved ASV-ordered version: {filename}")
    
    # Version 2: Competence-ordered (sorted by mean dominance)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    sorted_matrix = data_p_ratio[sorted_idx][:, sorted_idx]
    mask_sorted = np.isnan(sorted_matrix)
    
    # Create custom colormap to emphasize upper triangular structure
    # Values close to 1 (dominance) will be darker
    sns.heatmap(sorted_matrix, annot=True, fmt='.2f', cmap='YlGnBu',
                vmin=0, vmax=1, mask=mask_sorted, ax=ax, square=True,
                cbar_kws={'label': 'Dominance (sorted)'})
    ax.set_xlabel('ASV (sorted by competitive ability)')
    ax.set_ylabel('ASV (sorted by competitive ability)')
    ax.set_title(f'{medium}: Pairwise Species Dominance Matrix\n(Ordered by Mean Competence)')
    ax.set_xticklabels(sorted_labels)
    ax.set_yticklabels(sorted_labels)
    
    # Add hierarchy score
    ax.text(0.02, 0.98, f'Hierarchy Score: {hierarchy_score:.3f}',
            transform=ax.transAxes, va='top', ha='left',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Add lines to emphasize upper/lower triangular structure
    ax.plot([0, 12], [0, 12], 'k-', linewidth=1, alpha=0.3)
    
    plt.tight_layout()
    filename = f"Pairwise_Species_Hierarchy_{medium}_competence_ordered.svg"
    plt.savefig(os.path.join(output_dir, filename), format='svg', bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, filename.replace('.svg', '.png')), 
                format='png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved competence-ordered version: {filename}")
    
    # Save competence ranking data
    row_means = np.nanmean(data_p_ratio, axis=1)
    competence_df = pd.DataFrame({
        'ASV': species_labels,
        'Mean_Dominance_Score': row_means,
        'Competence_Rank': np.argsort(-row_means) + 1
    })
    competence_df = competence_df.sort_values('Mean_Dominance_Score', ascending=False)
    competence_df.to_csv(os.path.join(output_dir, f'ASV_competence_ranking_{medium}.csv'), 
                         index=False)
    print(f"Saved competence ranking: ASV_competence_ranking_{medium}.csv")

def plot_hierarchy_comparison():
    """Compare hierarchy scores across nutrient conditions"""
    
    media = ['LN', 'MN', 'HN']
    hierarchy_scores = []
    
    # Calculate hierarchy scores for each medium
    for medium in media:
        score, _ = plot_pairwise_species_hierarchy(medium)
        hierarchy_scores.append(score)
    
    # Create comparison plot
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    bars = ax.bar(media, hierarchy_scores, color=['lightblue', 'skyblue', 'steelblue'])
    ax.set_ylabel('Hierarchy Score')
    ax.set_xlabel('Nutrient Condition')
    ax.set_title('ASV Hierarchy Across Nutrient Conditions\n(From Pairwise Competition Experiments)')
    ax.set_ylim([0, 1])
    
    # Add value labels on bars
    for bar, score in zip(bars, hierarchy_scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{score:.3f}', ha='center', va='bottom')
    
    # Add grid
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    filename = "Pairwise_Species_Hierarchy_Comparison.svg"
    plt.savefig(os.path.join(output_dir, filename), format='svg', bbox_inches='tight')
    plt.close()
    
    print(f"\nSaved comparison plot: {filename}")
    
    # Save summary CSV
    summary_df = pd.DataFrame({
        'Medium': media,
        'Hierarchy_Score': hierarchy_scores
    })
    summary_df.to_csv(os.path.join(output_dir, "pairwise_species_hierarchy_summary.csv"), index=False)
    
    return summary_df

def main():
    """Main function to run pairwise species hierarchy analysis"""
    print("Starting Pairwise Species Competition Hierarchy Analysis...")
    print("Using actual colony counting data from coculture experiments")
    
    # Analyze each nutrient condition
    summary_df = plot_hierarchy_comparison()
    
    print("\n=== SUMMARY ===")
    print(summary_df.to_string(index=False))
    print(f"\nAll results saved to: {output_dir}")

if __name__ == "__main__":
    main()