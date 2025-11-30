#!/usr/bin/env python3
"""
plot_species_ph_effects.py

Purpose: Analyze and plot species-level pH effects in microbial communities
Key features:
- Identify pH-associated species (alkaliphiles vs acidophiles)
- Species-specific pH tolerance ranges and optimal pH
- Phylogenetic patterns in pH preferences
- pH prediction from species composition
- Multi-dimensional correlation analysis

Author: Gore Lab Analysis Team
Date: January 2025
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr, spearmanr
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import warnings
import os
warnings.filterwarnings('ignore')

# Set matplotlib backend to non-interactive to avoid display issues
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Load data directly instead of from common_setup
Processed_sequences_synthetic_path="../../Postprocessed/processed_Sequences_synthetic.xlsx"
Processed_sequences_natural_path="../../Postprocessed/processed_Sequences_natural.xlsx"
Communities_data_synthetic_path ="../../Analyzed/processed_Communities_synthetic.xlsx"
Communities_data_natural_path ="../../Analyzed/processed_Communities_natural.xlsx"

# Read data
Processed_sequences_synthetic=pd.read_excel(Processed_sequences_synthetic_path)
Processed_sequences_natural=pd.read_excel(Processed_sequences_natural_path)
Communities_data_synthetic=pd.read_excel(Communities_data_synthetic_path)
Communities_data_natural=pd.read_excel(Communities_data_natural_path)
Communities_data=pd.concat([Communities_data_synthetic,Communities_data_natural])

# Set up output directory
output_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/pH_Analysis"
os.makedirs(output_dir, exist_ok=True)

def load_species_ph_data():
    """Load and merge species abundance data with pH measurements"""
    print("Loading species abundance and pH data...")
    
    # Species abundance data (43 ASVs)
    abundance_data = pd.concat([Processed_sequences_synthetic, Processed_sequences_natural], ignore_index=True)
    print(f"Abundance data shape: {abundance_data.shape}")
    print(f"Abundance columns: {abundance_data.columns.tolist()[:10]}...")  # Show first 10 columns
    
    # Community pH data 
    ph_data = Communities_data[['SampleIDX', 'fieldPH1', 'fieldPH7']].copy()
    print(f"pH data shape: {ph_data.shape}")
    print(f"pH data columns: {ph_data.columns.tolist()}")
    print(f"pH data sample: \n{ph_data.head()}")
    
    # Merge on SampleIDX
    merged_data = abundance_data.merge(ph_data, on='SampleIDX', how='inner')
    print(f"Merged data shape: {merged_data.shape}")
    print(f"Merged columns: {merged_data.columns.tolist()[:15]}...")  # Show first 15 columns
    
    print(f"✓ Loaded {len(merged_data)} samples with both species and pH data")
    print(f"✓ Species tracked: NormalizedAbundance1-NormalizedAbundance43 ({43} total)")
    print(f"✓ pH measurements: Day 1 and Day 7")
    
    return merged_data

def get_asv_taxonomy():
    """Get taxonomy information for ASVs"""
    # Taxonomy data from previous analysis (from Final_Day_Community_Plots_with_Legend.ipynb)
    taxonomy_data = [
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
    
    taxonomy_df = pd.DataFrame(taxonomy_data, columns=['ASV', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus'])
    return taxonomy_df

# ===============================
# ANALYSIS 1: SPECIES-pH CORRELATION ANALYSIS
# ===============================
def calculate_species_ph_correlations(merged_data):
    """Calculate Pearson and Spearman correlations between each species and pH"""
    print("\n=== ANALYSIS 1: Species-pH Correlations ===")
    
    asv_columns = [f'NormalizedAbundance{i}' for i in range(1, 44)]
    ph_columns = ['fieldPH1', 'fieldPH7']
    
    correlation_results = []
    
    for ph_col in ph_columns:
        print(f"\nAnalyzing correlations with {ph_col}...")
        valid_data = merged_data.dropna(subset=[ph_col])
        print(f"Valid data shape: {valid_data.shape}")
        print(f"pH column {ph_col} has {valid_data[ph_col].notna().sum()} non-null values")
        
        for asv in asv_columns:
            if asv in valid_data.columns:
                abundance = valid_data[asv]
                ph_values = valid_data[ph_col]
                
                print(f"Processing {asv}: abundance range [{abundance.min():.6f}, {abundance.max():.6f}]")
                
                # Remove zeros for more meaningful correlation
                non_zero_mask = abundance > 1e-6
                if non_zero_mask.sum() > 10:  # At least 10 non-zero samples
                    try:
                        pearson_r, pearson_p = pearsonr(abundance[non_zero_mask], ph_values[non_zero_mask])
                        spearman_r, spearman_p = spearmanr(abundance[non_zero_mask], ph_values[non_zero_mask])
                        n_nonzero = non_zero_mask.sum()
                    except Exception as e:
                        print(f"Error calculating correlation for {asv} (non-zero): {e}")
                        continue
                else:
                    # Include zeros if too few non-zero samples
                    try:
                        pearson_r, pearson_p = pearsonr(abundance, ph_values)
                        spearman_r, spearman_p = spearmanr(abundance, ph_values)
                        n_nonzero = len(ph_values)
                    except Exception as e:
                        print(f"Error calculating correlation for {asv} (all data): {e}")
                        continue
                
                correlation_results.append({
                    'ASV': asv,
                    'pH_timepoint': ph_col,
                    'pearson_r': pearson_r,
                    'pearson_p': pearson_p,
                    'spearman_r': spearman_r,
                    'spearman_p': spearman_p,
                    'n_samples': len(ph_values),
                    'n_nonzero': n_nonzero
                })
            else:
                print(f"Species {asv} not found in columns")
    
    correlation_df = pd.DataFrame(correlation_results)
    
    # Debug: print first few rows and columns
    print(f"Correlation DataFrame shape: {correlation_df.shape}")
    print(f"Columns: {correlation_df.columns.tolist()}")
    print(f"First few rows:\n{correlation_df.head()}")
    
    if len(correlation_df) > 0 and 'pearson_p' in correlation_df.columns:
        # Add significance flags
        correlation_df['pearson_significant'] = correlation_df['pearson_p'] < 0.05
        correlation_df['spearman_significant'] = correlation_df['spearman_p'] < 0.05
        correlation_df['highly_significant'] = correlation_df['pearson_p'] < 0.01
    else:
        print("Warning: No correlation data or missing pearson_p column")
    
    print(f"✓ Calculated correlations for {len(asv_columns)} species")
    return correlation_df

# ===============================
# ANALYSIS 2: pH-ASSOCIATED SPECIES IDENTIFICATION
# ===============================
def identify_ph_associated_species(correlation_df, taxonomy_df):
    """Identify strongly pH-associated species (alkaliphiles vs acidophiles)"""
    print("\n=== ANALYSIS 2: pH-Associated Species Identification ===")
    
    # Focus on final pH (fieldPH7) as it's most biologically relevant
    final_ph_corr = correlation_df[correlation_df['pH_timepoint'] == 'fieldPH7'].copy()
    
    # Define thresholds for strong associations
    strong_threshold = 0.3
    moderate_threshold = 0.2
    p_threshold = 0.05
    
    # Classify species by pH association
    final_ph_corr['pH_association'] = 'Neutral'
    final_ph_corr.loc[(final_ph_corr['pearson_r'] > strong_threshold) & 
                      (final_ph_corr['pearson_p'] < p_threshold), 'pH_association'] = 'Strong Alkaliphile'
    final_ph_corr.loc[(final_ph_corr['pearson_r'] > moderate_threshold) & 
                      (final_ph_corr['pearson_r'] <= strong_threshold) & 
                      (final_ph_corr['pearson_p'] < p_threshold), 'pH_association'] = 'Moderate Alkaliphile'
    final_ph_corr.loc[(final_ph_corr['pearson_r'] < -strong_threshold) & 
                      (final_ph_corr['pearson_p'] < p_threshold), 'pH_association'] = 'Strong Acidophile'
    final_ph_corr.loc[(final_ph_corr['pearson_r'] < -moderate_threshold) & 
                      (final_ph_corr['pearson_r'] >= -strong_threshold) & 
                      (final_ph_corr['pearson_p'] < p_threshold), 'pH_association'] = 'Moderate Acidophile'
    
    # Add taxonomy information
    final_ph_corr = final_ph_corr.merge(taxonomy_df, on='ASV', how='left')
    
    # Print results
    association_counts = final_ph_corr['pH_association'].value_counts()
    print("\npH Association Summary:")
    for association, count in association_counts.items():
        print(f"  {association}: {count} species")
    
    # Show top alkaliphiles and acidophiles
    print("\n🔵 Top Alkaliphiles (high pH lovers):")
    alkaliphiles = final_ph_corr[final_ph_corr['pearson_r'] > moderate_threshold].sort_values('pearson_r', ascending=False)
    for _, row in alkaliphiles.head(10).iterrows():
        print(f"  {row['ASV']}: r={row['pearson_r']:.3f}, p={row['pearson_p']:.3f}, {row['Genus']}")
    
    print("\n🔴 Top Acidophiles (low pH lovers):")
    acidophiles = final_ph_corr[final_ph_corr['pearson_r'] < -moderate_threshold].sort_values('pearson_r')
    for _, row in acidophiles.head(10).iterrows():
        print(f"  {row['ASV']}: r={row['pearson_r']:.3f}, p={row['pearson_p']:.3f}, {row['Genus']}")
    
    return final_ph_corr

# ===============================
# ANALYSIS 3: PHYLOGENETIC pH PATTERNS
# ===============================
def analyze_phylogenetic_ph_patterns(ph_species_data):
    """Analyze pH preferences by taxonomic groups"""
    print("\n=== ANALYSIS 3: Phylogenetic pH Patterns ===")
    
    # Group by taxonomic levels
    taxonomic_levels = ['Phylum', 'Class', 'Order', 'Family', 'Genus']
    phylo_patterns = {}
    
    for level in taxonomic_levels:
        level_stats = ph_species_data.groupby(level).agg({
            'pearson_r': ['mean', 'std', 'count'],
            'pearson_p': lambda x: (x < 0.05).sum()
        }).round(3)
        level_stats.columns = ['mean_correlation', 'std_correlation', 'n_species', 'n_significant']
        level_stats = level_stats[level_stats['n_species'] >= 2].sort_values('mean_correlation', ascending=False)
        
        phylo_patterns[level] = level_stats
        
        print(f"\n{level} pH patterns (groups with ≥2 species):")
        print(level_stats.head(10))
    
    return phylo_patterns

# ===============================
# ANALYSIS 4: pH TOLERANCE RANGES
# ===============================
def calculate_ph_tolerance_ranges(merged_data):
    """Calculate pH tolerance ranges for each species"""
    print("\n=== ANALYSIS 4: pH Tolerance Ranges ===")
    
    asv_columns = [f'NormalizedAbundance{i}' for i in range(1, 44)]
    abundance_threshold = 0.01  # 1% abundance threshold for "presence"
    
    tolerance_data = []
    
    for asv in asv_columns:
        if asv in merged_data.columns:
            # Get samples where this ASV is present (>1% abundance)
            present_samples = merged_data[merged_data[asv] > abundance_threshold]
            
            if len(present_samples) > 5:  # Need at least 5 samples
                ph_values = present_samples['fieldPH7'].dropna()
                if len(ph_values) > 0:
                    tolerance_data.append({
                        'ASV': asv,
                        'pH_min': ph_values.min(),
                        'pH_max': ph_values.max(),
                        'pH_range': ph_values.max() - ph_values.min(),
                        'pH_mean': ph_values.mean(),
                        'pH_median': ph_values.median(),
                        'pH_std': ph_values.std(),
                        'n_samples': len(ph_values),
                        'max_abundance': merged_data[asv].max()
                    })
    
    tolerance_df = pd.DataFrame(tolerance_data)
    tolerance_df = tolerance_df.sort_values('pH_range', ascending=False)
    
    print(f"✓ Calculated pH tolerance for {len(tolerance_df)} species")
    print(f"\nTop pH generalists (widest tolerance):")
    for _, row in tolerance_df.head(5).iterrows():
        print(f"  {row['ASV']}: pH {row['pH_min']:.1f}-{row['pH_max']:.1f} (range: {row['pH_range']:.1f})")
    
    print(f"\nTop pH specialists (narrowest tolerance):")
    for _, row in tolerance_df.tail(5).iterrows():
        print(f"  {row['ASV']}: pH {row['pH_min']:.1f}-{row['pH_max']:.1f} (range: {row['pH_range']:.1f})")
    
    return tolerance_df

# ===============================
# ANALYSIS 5: pH PREDICTION FROM SPECIES COMPOSITION  
# ===============================
def build_ph_prediction_models(merged_data):
    """Build machine learning models to predict pH from species composition"""
    print("\n=== ANALYSIS 5: pH Prediction Models ===")
    
    # Prepare data
    asv_columns = [f'NormalizedAbundance{i}' for i in range(1, 44)]
    valid_data = merged_data.dropna(subset=['fieldPH7'])
    
    X = valid_data[asv_columns].values
    y = valid_data['fieldPH7'].values
    
    # Apply log transform to abundance data (common for microbiome data)
    X_log = np.log10(X + 1e-6)
    
    # Train multiple models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    model_results = {}
    
    for name, model in models.items():
        model.fit(X_log, y)
        y_pred = model.predict(X_log)
        r2 = r2_score(y, y_pred)
        
        model_results[name] = {
            'model': model,
            'r2_score': r2,
            'predictions': y_pred
        }
        
        print(f"{name}: R² = {r2:.3f}")
        
        # Feature importance for Random Forest
        if name == 'Random Forest':
            feature_importance = pd.DataFrame({
                'Species': asv_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\nTop 10 most important species for pH prediction:")
            for _, row in feature_importance.head(10).iterrows():
                print(f"  {row['Species']}: {row['importance']:.3f}")
    
    return model_results, feature_importance

# ===============================
# VISUALIZATION FUNCTIONS
# ===============================
def plot_correlation_heatmap(correlation_df, taxonomy_df):
    """Plot species-pH correlation heatmap"""
    print("\nGenerating correlation heatmap...")
    
    # Pivot data for heatmap
    heatmap_data = correlation_df.pivot(index='ASV', columns='pH_timepoint', values='pearson_r')
    
    # Add taxonomy info for sorting
    heatmap_data = heatmap_data.merge(taxonomy_df[['ASV', 'Phylum', 'Genus']], 
                                      left_index=True, right_on='ASV', how='left')
    heatmap_data = heatmap_data.set_index('ASV').sort_values(['Phylum', 'Genus'])
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 12))
    
    sns.heatmap(heatmap_data[['fieldPH1', 'fieldPH7']], 
                annot=False, cmap='RdBu_r', center=0,
                vmin=-0.6, vmax=0.6, ax=ax)
    
    ax.set_title('Species-pH Correlations\n(Red = Alkaliphiles, Blue = Acidophiles)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('pH Timepoint')
    ax.set_ylabel('ASV (sorted by taxonomy)')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/species_ph_correlation_heatmap.svg', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved correlation heatmap")

def plot_ph_association_barplot(ph_species_data):
    """Plot species grouped by pH association with taxonomy colors"""
    print("\nGenerating pH association bar plot...")
    
    # Count by pH association and phylum
    association_counts = ph_species_data.groupby(['pH_association', 'Phylum']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    association_counts.plot(kind='bar', stacked=True, ax=ax, 
                           colormap='Set3', alpha=0.8)
    
    ax.set_title('Species pH Associations by Phylum', fontsize=14, fontweight='bold')
    ax.set_xlabel('pH Association Category')
    ax.set_ylabel('Number of Species')
    ax.legend(title='Phylum', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/ph_association_by_phylum.svg', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved pH association plot")

def plot_ph_tolerance_ranges(tolerance_df, taxonomy_df):
    """Plot pH tolerance ranges for species"""
    print("\nGenerating pH tolerance range plot...")
    
    # Merge with taxonomy
    tolerance_plot_data = tolerance_df.merge(taxonomy_df, on='ASV', how='left')
    tolerance_plot_data = tolerance_plot_data.sort_values('pH_mean')
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create color map by phylum
    phylums = tolerance_plot_data['Phylum'].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(phylums)))
    phylum_colors = dict(zip(phylums, colors))
    
    for i, (_, row) in enumerate(tolerance_plot_data.iterrows()):
        color = phylum_colors[row['Phylum']]
        ax.barh(i, row['pH_range'], left=row['pH_min'], 
                color=color, alpha=0.7, height=0.8)
        ax.plot(row['pH_mean'], i, 'ko', markersize=3)
    
    ax.set_yticks(range(len(tolerance_plot_data)))
    ax.set_yticklabels([f"{row['ASV']} ({row['Genus']})" 
                        for _, row in tolerance_plot_data.iterrows()], fontsize=8)
    ax.set_xlabel('pH Range')
    ax.set_title('pH Tolerance Ranges by Species\n(Black dots = mean pH)', 
                 fontsize=14, fontweight='bold')
    
    # Add legend for phylums
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=phylum_colors[p], alpha=0.7, label=p) 
                       for p in phylums]
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left', title='Phylum')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/ph_tolerance_ranges.svg', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved pH tolerance ranges plot")

def plot_species_ph_scatter(merged_data, top_species):
    """Plot scatter plots for top pH-associated species"""
    print("\nGenerating species-pH scatter plots...")
    
    n_species = min(12, len(top_species))
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    axes = axes.flatten()
    
    for i, asv in enumerate(top_species.head(n_species)['ASV']):
        ax = axes[i]
        
        x = merged_data[asv]
        y = merged_data['fieldPH7']
        
        # Remove NaN values
        mask = ~(np.isnan(x) | np.isnan(y))
        x_clean, y_clean = x[mask], y[mask]
        
        # Color by abundance (log scale)
        colors = np.log10(x_clean + 1e-6)
        scatter = ax.scatter(x_clean, y_clean, c=colors, alpha=0.6, 
                            cmap='viridis', s=20)
        
        # Add trend line
        if len(x_clean) > 10:
            z = np.polyfit(x_clean, y_clean, 1)
            p = np.poly1d(z)
            ax.plot(x_clean, p(x_clean), "r--", alpha=0.8, linewidth=1)
            
            # Add R² value
            r, _ = pearsonr(x_clean, y_clean)
            ax.text(0.05, 0.95, f'r = {r:.3f}', transform=ax.transAxes, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        ax.set_xlabel(f'{asv} Abundance')
        ax.set_ylabel('Final pH')
        ax.set_title(f'{asv}', fontsize=10)
    
    # Remove empty subplots
    for i in range(n_species, len(axes)):
        fig.delaxes(axes[i])
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/species_ph_scatter_plots.svg', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved species-pH scatter plots")

def plot_phylogenetic_ph_summary(phylo_patterns):
    """Plot phylogenetic pH pattern summary"""
    print("\nGenerating phylogenetic pH summary...")
    
    # Focus on Genus level for most specific patterns
    genus_data = phylo_patterns['Genus'].reset_index()
    genus_data = genus_data[genus_data['n_species'] >= 2].sort_values('mean_correlation')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(range(len(genus_data)), genus_data['mean_correlation'], 
                   color=['red' if x < 0 else 'blue' for x in genus_data['mean_correlation']],
                   alpha=0.7)
    
    # Add error bars
    ax.errorbar(genus_data['mean_correlation'], range(len(genus_data)), 
                xerr=genus_data['std_correlation'], fmt='none', color='black', alpha=0.5)
    
    ax.set_yticks(range(len(genus_data)))
    ax.set_yticklabels([f"{row['Genus']} (n={row['n_species']})" 
                        for _, row in genus_data.iterrows()])
    ax.set_xlabel('Mean Species-pH Correlation')
    ax.set_title('Phylogenetic pH Preferences by Genus\n(Red = Acidophilic, Blue = Alkaliphilic)', 
                 fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/phylogenetic_ph_patterns.svg', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved phylogenetic pH patterns plot")

def main():
    """Main function to run all species-pH analyses"""
    print("="*60)
    print("SPECIES-pH CORRELATION ANALYSIS")
    print("="*60)
    
    # Load data
    merged_data = load_species_ph_data()
    taxonomy_df = get_asv_taxonomy()
    
    # Analysis 1: Calculate correlations
    correlation_df = calculate_species_ph_correlations(merged_data)
    
    # Analysis 2: Identify pH-associated species
    ph_species_data = identify_ph_associated_species(correlation_df, taxonomy_df)
    
    # Analysis 3: Phylogenetic patterns
    phylo_patterns = analyze_phylogenetic_ph_patterns(ph_species_data)
    
    # Analysis 4: pH tolerance ranges
    tolerance_df = calculate_ph_tolerance_ranges(merged_data)
    
    # Analysis 5: pH prediction models
    model_results, feature_importance = build_ph_prediction_models(merged_data)
    
    # Generate visualizations
    plot_correlation_heatmap(correlation_df, taxonomy_df)
    plot_ph_association_barplot(ph_species_data)
    plot_ph_tolerance_ranges(tolerance_df, taxonomy_df)
    
    # Plot top correlated species
    top_species = ph_species_data.iloc[ph_species_data['pearson_r'].abs().argsort()[-12:]]
    plot_species_ph_scatter(merged_data, top_species)
    plot_phylogenetic_ph_summary(phylo_patterns)
    
    # Save results to files
    correlation_df.to_csv(f'{output_dir}/species_ph_correlations.csv', index=False)
    ph_species_data.to_csv(f'{output_dir}/ph_associated_species.csv', index=False)
    tolerance_df.to_csv(f'{output_dir}/ph_tolerance_ranges.csv', index=False)
    feature_importance.to_csv(f'{output_dir}/ph_prediction_importance.csv', index=False)
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print(f"📁 All results saved to: {output_dir}/")
    print(f"📊 Generated files:")
    print(f"  - species_ph_correlations.csv")
    print(f"  - ph_associated_species.csv")
    print(f"  - ph_tolerance_ranges.csv")
    print(f"  - ph_prediction_importance.csv")
    print(f"  - Multiple visualization plots (.svg)")
    
    return {
        'merged_data': merged_data,
        'correlations': correlation_df,
        'ph_species': ph_species_data,
        'tolerance': tolerance_df,
        'models': model_results,
        'feature_importance': feature_importance
    }

if __name__ == "__main__":
    results = main()