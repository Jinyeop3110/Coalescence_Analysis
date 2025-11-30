#!/usr/bin/env python3
"""
Species-pH Visualization Script
Creates scientific publication-quality plots for species-pH analysis
"""

import numpy as np
import pandas as pd
import os

# Set matplotlib backend to avoid display issues
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Set scientific plotting style
plt.style.use('default')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['font.family'] = 'Arial'

def load_analysis_results():
    """Load the results from the species-pH analysis"""
    print("Loading analysis results...")
    
    # Load the correlation results
    results_df = pd.read_csv("Figure/pH_Analysis/species_ph_correlations_simple.csv")
    alkaliphiles = pd.read_csv("Figure/pH_Analysis/alkaliphile_species.csv")
    acidophiles = pd.read_csv("Figure/pH_Analysis/acidophile_species.csv")
    
    # Load original data for plotting
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    ph_data = communities_data[['SampleIDX', 'fieldPH1', 'fieldPH7']].copy()
    merged_data = abundance_data.merge(ph_data, on='SampleIDX', how='inner')
    
    print(f"✓ Loaded {len(results_df)} species correlation results")
    print(f"✓ Loaded {len(merged_data)} samples for plotting")
    
    return results_df, alkaliphiles, acidophiles, merged_data

def plot_correlation_overview(results_df, output_dir):
    """Plot 1: Overview of all species-pH correlations"""
    print("Creating correlation overview plot...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1A: Histogram of correlations
    correlations = results_df['Correlation_with_pH'].values
    
    ax1.hist(correlations, bins=30, alpha=0.7, color='steelblue', edgecolor='black', linewidth=0.5)
    ax1.axvline(x=0, color='red', linestyle='--', alpha=0.7, linewidth=1)
    ax1.axvline(x=0.2, color='blue', linestyle='--', alpha=0.7, linewidth=1, label='Alkaliphile threshold')
    ax1.axvline(x=-0.2, color='orange', linestyle='--', alpha=0.7, linewidth=1, label='Acidophile threshold')
    
    ax1.set_xlabel('Species-pH Correlation (r)')
    ax1.set_ylabel('Number of Species')
    ax1.set_title('Distribution of Species-pH Correlations')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 1B: Correlation vs Presence Rate
    ax2.scatter(results_df['Presence_Rate'], results_df['Correlation_with_pH'], 
                alpha=0.6, s=30, color='steelblue')
    
    # Highlight significant species
    alkaliphile_mask = results_df['Correlation_with_pH'] > 0.2
    acidophile_mask = results_df['Correlation_with_pH'] < -0.2
    
    if alkaliphile_mask.any():
        ax2.scatter(results_df[alkaliphile_mask]['Presence_Rate'], 
                   results_df[alkaliphile_mask]['Correlation_with_pH'],
                   color='blue', s=60, alpha=0.8, label='Alkaliphiles', edgecolor='white', linewidth=1)
    
    if acidophile_mask.any():
        ax2.scatter(results_df[acidophile_mask]['Presence_Rate'], 
                   results_df[acidophile_mask]['Correlation_with_pH'],
                   color='red', s=60, alpha=0.8, label='Acidophiles', edgecolor='white', linewidth=1)
    
    ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    ax2.axhline(y=0.2, color='blue', linestyle='--', alpha=0.7)
    ax2.axhline(y=-0.2, color='red', linestyle='--', alpha=0.7)
    
    ax2.set_xlabel('Species Presence Rate')
    ax2.set_ylabel('pH Correlation (r)')
    ax2.set_title('Correlation vs Species Prevalence')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/1_correlation_overview.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved correlation overview plot")

def plot_top_species_scatter(results_df, merged_data, output_dir):
    """Plot 2: Scatter plots for top pH-associated species"""
    print("Creating top species scatter plots...")
    
    # Get top 12 most correlated species (by absolute correlation)
    top_species = results_df.head(12)
    
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    axes = axes.flatten()
    
    for i, (_, row) in enumerate(top_species.iterrows()):
        if i >= 12:
            break
            
        ax = axes[i]
        species = row['Species']
        correlation = row['Correlation_with_pH']
        
        # Get data for this species
        x = merged_data[species].values
        y = merged_data['fieldPH7'].values
        
        # Remove NaN values
        mask = ~(np.isnan(x) | np.isnan(y))
        x_clean = x[mask]
        y_clean = y[mask]
        
        # Color points by abundance
        colors = np.log10(x_clean + 1e-6)  # Log transform for better visualization
        
        scatter = ax.scatter(x_clean, y_clean, c=colors, cmap='viridis', 
                           alpha=0.6, s=15, edgecolors='none')
        
        # Add trend line
        if len(x_clean) > 10:
            z = np.polyfit(x_clean, y_clean, 1)
            p = np.poly1d(z)
            x_trend = np.linspace(x_clean.min(), x_clean.max(), 100)
            ax.plot(x_trend, p(x_trend), "r-", alpha=0.8, linewidth=2)
        
        # Labels and formatting
        species_num = species.replace('NormalizedAbundance', 'Species ')
        ax.set_title(f'{species_num}\\nr = {correlation:.3f}', fontsize=9)
        ax.set_xlabel('Abundance', fontsize=8)
        ax.set_ylabel('Final pH', fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3)
        
        # Set appropriate axis limits
        if x_clean.max() > 0:
            ax.set_xlim(0, x_clean.max() * 1.1)
    
    # Remove empty subplots
    for i in range(len(top_species), 12):
        fig.delaxes(axes[i])
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/2_top_species_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved top species scatter plots")

def plot_alkaliphiles_vs_acidophiles(alkaliphiles, acidophiles, output_dir):
    """Plot 3: Bar plot comparing alkaliphiles vs acidophiles"""
    print("Creating alkaliphiles vs acidophiles comparison...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 3A: Correlation strengths
    all_significant = pd.concat([alkaliphiles, acidophiles])
    
    species_names = [s.replace('NormalizedAbundance', 'Sp.') for s in all_significant['Species']]
    correlations = all_significant['Correlation_with_pH'].values
    colors = ['blue' if r > 0 else 'red' for r in correlations]
    
    bars = ax1.barh(range(len(species_names)), correlations, color=colors, alpha=0.7)
    
    ax1.set_yticks(range(len(species_names)))
    ax1.set_yticklabels(species_names, fontsize=9)
    ax1.set_xlabel('Species-pH Correlation (r)')
    ax1.set_title('pH-Associated Species\\n(Blue: Alkaliphiles, Red: Acidophiles)')
    ax1.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Add correlation values as text
    for i, (bar, corr) in enumerate(zip(bars, correlations)):
        width = bar.get_width()
        ax1.text(width + (0.02 if width > 0 else -0.02), bar.get_y() + bar.get_height()/2, 
                f'{corr:.3f}', ha='left' if width > 0 else 'right', va='center', fontsize=8)
    
    # Plot 3B: Presence rates
    presence_rates = all_significant['Presence_Rate'].values * 100  # Convert to percentage
    
    bars2 = ax2.barh(range(len(species_names)), presence_rates, color=colors, alpha=0.7)
    
    ax2.set_yticks(range(len(species_names)))
    ax2.set_yticklabels(species_names, fontsize=9)
    ax2.set_xlabel('Species Presence Rate (%)')
    ax2.set_title('Species Prevalence in Samples')
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Add percentage values as text
    for i, (bar, rate) in enumerate(zip(bars2, presence_rates)):
        width = bar.get_width()
        ax2.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f'{rate:.1f}%', ha='left', va='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/3_alkaliphiles_vs_acidophiles.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved alkaliphiles vs acidophiles comparison")

def plot_ph_distributions(results_df, merged_data, output_dir):
    """Plot 4: pH distributions for different species groups"""
    print("Creating pH distribution plots...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Get pH data
    ph_values = merged_data['fieldPH7'].dropna()
    
    # Plot 4A: Overall pH distribution
    ax1.hist(ph_values, bins=30, alpha=0.7, color='gray', edgecolor='black', linewidth=0.5)
    ax1.set_xlabel('Final pH')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Overall pH Distribution')
    ax1.grid(True, alpha=0.3)
    
    # Add statistics
    ax1.axvline(ph_values.mean(), color='red', linestyle='--', alpha=0.7, 
               label=f'Mean: {ph_values.mean():.2f}')
    ax1.axvline(ph_values.median(), color='blue', linestyle='--', alpha=0.7, 
               label=f'Median: {ph_values.median():.2f}')
    ax1.legend()
    
    # Plot 4B: pH for high abundance vs low abundance samples
    # Get top acidophile for demonstration
    top_acidophile = results_df.iloc[0]['Species']  # Most negative correlation
    
    high_abundance_mask = merged_data[top_acidophile] > merged_data[top_acidophile].quantile(0.75)
    low_abundance_mask = merged_data[top_acidophile] < merged_data[top_acidophile].quantile(0.25)
    
    high_ph = merged_data[high_abundance_mask]['fieldPH7'].dropna()
    low_ph = merged_data[low_abundance_mask]['fieldPH7'].dropna()
    
    ax2.hist(low_ph, bins=20, alpha=0.7, color='lightblue', label='Low abundance', 
            edgecolor='black', linewidth=0.5)
    ax2.hist(high_ph, bins=20, alpha=0.7, color='salmon', label='High abundance',
            edgecolor='black', linewidth=0.5)
    
    species_name = top_acidophile.replace('NormalizedAbundance', 'Species ')
    ax2.set_xlabel('Final pH')
    ax2.set_ylabel('Frequency')
    ax2.set_title(f'pH Distribution by {species_name} Abundance\\n(Top Acidophile)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 4C: Species richness vs pH
    # Calculate species richness (number of species with >0.1% abundance)
    abundance_cols = [col for col in merged_data.columns if col.startswith('NormalizedAbundance')]
    richness = (merged_data[abundance_cols] > 0.001).sum(axis=1)  # >0.1% abundance threshold
    
    ph_clean = merged_data['fieldPH7'].dropna()
    richness_clean = richness.loc[ph_clean.index]
    
    ax3.scatter(richness_clean, ph_clean, alpha=0.5, s=20, color='green')
    
    # Add trend line
    z = np.polyfit(richness_clean, ph_clean, 1)
    p = np.poly1d(z)
    x_trend = np.linspace(richness_clean.min(), richness_clean.max(), 100)
    ax3.plot(x_trend, p(x_trend), "r-", alpha=0.8, linewidth=2)
    
    # Calculate correlation
    richness_ph_corr = np.corrcoef(richness_clean, ph_clean)[0, 1]
    
    ax3.set_xlabel('Species Richness')
    ax3.set_ylabel('Final pH') 
    ax3.set_title(f'Species Richness vs pH\\nr = {richness_ph_corr:.3f}')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4D: Abundance-weighted pH preferences
    # For each species, calculate mean pH where it's present
    species_ph_preferences = []
    species_names = []
    
    for species in abundance_cols[:20]:  # Top 20 most abundant species
        species_data = merged_data[merged_data[species] > 0.01]  # Present at >1% abundance
        if len(species_data) > 10:  # Need sufficient data
            mean_ph = species_data['fieldPH7'].mean()
            species_ph_preferences.append(mean_ph)
            species_names.append(species.replace('NormalizedAbundance', 'Sp.'))
    
    if species_ph_preferences:
        colors_pref = ['red' if ph < 6.5 else 'blue' if ph > 7.5 else 'gray' 
                      for ph in species_ph_preferences]
        
        ax4.barh(range(len(species_names)), species_ph_preferences, color=colors_pref, alpha=0.7)
        ax4.set_yticks(range(len(species_names)))
        ax4.set_yticklabels(species_names, fontsize=8)
        ax4.set_xlabel('Mean pH Preference')
        ax4.set_title('Species pH Preferences\\n(Red: Acidic, Blue: Alkaline)')
        ax4.axvline(x=7.0, color='black', linestyle='--', alpha=0.5, label='Neutral')
        ax4.grid(True, alpha=0.3, axis='x')
        ax4.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/4_ph_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved pH distribution plots")

def plot_correlation_heatmap(results_df, output_dir):
    """Plot 5: Heatmap of species correlations"""
    print("Creating correlation heatmap...")
    
    # Prepare data for heatmap - select top 30 most correlated species
    top_30 = results_df.head(30).copy()
    
    # Create matrix for heatmap
    species_names = [s.replace('NormalizedAbundance', 'Sp.') for s in top_30['Species']]
    correlations = top_30['Correlation_with_pH'].values.reshape(-1, 1)
    
    fig, ax = plt.subplots(figsize=(8, 12))
    
    # Create heatmap
    im = ax.imshow(correlations, cmap='RdBu_r', aspect='auto', vmin=-0.6, vmax=0.6)
    
    # Set ticks and labels
    ax.set_yticks(range(len(species_names)))
    ax.set_yticklabels(species_names, fontsize=8)
    ax.set_xticks([0])
    ax.set_xticklabels(['pH Correlation'])
    ax.set_title('Species-pH Correlations\\n(Red: Acidophiles, Blue: Alkaliphiles)', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Correlation Coefficient (r)', rotation=270, labelpad=20)
    
    # Add correlation values as text
    for i, corr in enumerate(correlations.flatten()):
        text_color = 'white' if abs(corr) > 0.3 else 'black'
        ax.text(0, i, f'{corr:.3f}', ha='center', va='center', 
               color=text_color, fontweight='bold', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/5_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved correlation heatmap")

def create_summary_figure(results_df, alkaliphiles, acidophiles, output_dir):
    """Create a comprehensive summary figure"""
    print("Creating comprehensive summary figure...")
    
    fig = plt.figure(figsize=(16, 10))
    
    # Create a 3x3 grid with different subplot sizes
    gs = fig.add_gridspec(3, 3, width_ratios=[1, 1, 1], height_ratios=[1, 1, 1])
    
    # Summary statistics panel
    ax_summary = fig.add_subplot(gs[0, :])
    ax_summary.axis('off')
    
    # Add summary text
    total_species = len(results_df)
    n_alkaliphiles = len(alkaliphiles)
    n_acidophiles = len(acidophiles)
    n_neutral = total_species - n_alkaliphiles - n_acidophiles
    
    summary_text = f'''
    SPECIES-pH CORRELATION ANALYSIS SUMMARY
    
    📊 Dataset Overview:
    • Total species analyzed: {total_species}
    • Samples with pH data: 580
    • Analysis method: Pearson correlation
    
    🔵 Alkaliphiles (pH increasers, r > 0.2): {n_alkaliphiles} species
    🔴 Acidophiles (pH decreasers, r < -0.2): {n_acidophiles} species  
    ⚪ Neutral species (|r| ≤ 0.2): {n_neutral} species
    
    ⭐ Strongest pH-associated species:
    • Most alkaliphilic: {alkaliphiles.iloc[0]['Species'] if len(alkaliphiles) > 0 else 'None'} (r = {alkaliphiles.iloc[0]['Correlation_with_pH']:.3f if len(alkaliphiles) > 0 else 'N/A'})
    • Most acidophilic: {acidophiles.iloc[0]['Species']} (r = {acidophiles.iloc[0]['Correlation_with_pH']:.3f})
    '''
    
    ax_summary.text(0.05, 0.95, summary_text, transform=ax_summary.transAxes, 
                   fontsize=11, verticalalignment='top', fontfamily='monospace',
                   bbox=dict(boxstyle="round,pad=1", facecolor="lightgray", alpha=0.8))
    
    # Small correlation histogram
    ax_hist = fig.add_subplot(gs[1, 0])
    correlations = results_df['Correlation_with_pH'].values
    ax_hist.hist(correlations, bins=20, alpha=0.7, color='steelblue', edgecolor='black')
    ax_hist.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    ax_hist.set_xlabel('pH Correlation')
    ax_hist.set_ylabel('Count')
    ax_hist.set_title('Correlation Distribution')
    ax_hist.grid(True, alpha=0.3)
    
    # Top species bar plot
    ax_bar = fig.add_subplot(gs[1, 1:])
    top_10 = results_df.head(10)
    species_names = [s.replace('NormalizedAbundance', 'Sp.') for s in top_10['Species']]
    colors = ['red' if r < 0 else 'blue' for r in top_10['Correlation_with_pH']]
    
    bars = ax_bar.barh(range(len(species_names)), top_10['Correlation_with_pH'], 
                       color=colors, alpha=0.7)
    ax_bar.set_yticks(range(len(species_names)))
    ax_bar.set_yticklabels(species_names)
    ax_bar.set_xlabel('pH Correlation (r)')
    ax_bar.set_title('Top 10 pH-Associated Species')
    ax_bar.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax_bar.grid(True, alpha=0.3, axis='x')
    
    # Presence vs correlation scatter
    ax_scatter = fig.add_subplot(gs[2, :2])
    ax_scatter.scatter(results_df['Presence_Rate'], results_df['Correlation_with_pH'], 
                      alpha=0.6, s=30, color='gray')
    
    # Highlight significant species
    if len(alkaliphiles) > 0:
        ax_scatter.scatter(alkaliphiles['Presence_Rate'], alkaliphiles['Correlation_with_pH'],
                          color='blue', s=80, alpha=0.9, label='Alkaliphiles', 
                          edgecolor='white', linewidth=1)
    
    if len(acidophiles) > 0:
        ax_scatter.scatter(acidophiles['Presence_Rate'], acidophiles['Correlation_with_pH'],
                          color='red', s=80, alpha=0.9, label='Acidophiles',
                          edgecolor='white', linewidth=1)
    
    ax_scatter.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    ax_scatter.set_xlabel('Species Presence Rate')
    ax_scatter.set_ylabel('pH Correlation (r)')
    ax_scatter.set_title('Species Prevalence vs pH Association')
    ax_scatter.legend()
    ax_scatter.grid(True, alpha=0.3)
    
    # Classification pie chart
    ax_pie = fig.add_subplot(gs[2, 2])
    sizes = [n_alkaliphiles, n_acidophiles, n_neutral]
    labels = ['Alkaliphiles', 'Acidophiles', 'Neutral']
    colors_pie = ['blue', 'red', 'lightgray']
    
    ax_pie.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
    ax_pie.set_title('Species Classification')
    
    plt.suptitle('Species-pH Correlation Analysis', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/0_comprehensive_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved comprehensive summary figure")

def main():
    """Main function to create all visualizations"""
    print("=" * 60)
    print("SPECIES-pH VISUALIZATION GENERATION")
    print("=" * 60)
    
    # Load data
    results_df, alkaliphiles, acidophiles, merged_data = load_analysis_results()
    
    output_dir = "Figure/pH_Analysis"
    
    # Create all visualizations
    create_summary_figure(results_df, alkaliphiles, acidophiles, output_dir)
    plot_correlation_overview(results_df, output_dir)
    plot_top_species_scatter(results_df, merged_data, output_dir)
    plot_alkaliphiles_vs_acidophiles(alkaliphiles, acidophiles, output_dir)
    plot_ph_distributions(results_df, merged_data, output_dir)
    plot_correlation_heatmap(results_df, output_dir)
    
    print(f"\n🎉 ALL VISUALIZATIONS COMPLETE!")
    print(f"📁 Saved to: {output_dir}/")
    print("📊 Generated plots:")
    print("  0. 0_comprehensive_summary.png - Overview of all results")
    print("  1. 1_correlation_overview.png - Correlation distribution & prevalence")
    print("  2. 2_top_species_scatter.png - Individual species vs pH scatter plots")
    print("  3. 3_alkaliphiles_vs_acidophiles.png - Comparison of pH-associated species")
    print("  4. 4_ph_distributions.png - pH distributions and patterns")
    print("  5. 5_correlation_heatmap.png - Correlation strength visualization")
    print("\n✅ Ready for scientific publication!")

if __name__ == "__main__":
    main()