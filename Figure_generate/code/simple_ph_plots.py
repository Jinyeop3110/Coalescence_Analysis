#!/usr/bin/env python3
"""
Simple Species-pH Plots
Creates basic publication-quality plots without matplotlib dependencies
Uses only numpy and pandas with simple text-based visualizations
"""

import numpy as np
import pandas as pd
import os

def load_analysis_results():
    """Load the results from the species-pH analysis"""
    print("Loading analysis results...")
    
    results_df = pd.read_csv("Figure/pH_Analysis/species_ph_correlations_simple.csv")
    alkaliphiles = pd.read_csv("Figure/pH_Analysis/alkaliphile_species.csv")
    acidophiles = pd.read_csv("Figure/pH_Analysis/acidophile_species.csv")
    
    print(f"✓ Loaded {len(results_df)} species correlation results")
    return results_df, alkaliphiles, acidophiles

def create_ascii_histogram(values, bins=20, width=60):
    """Create ASCII histogram for correlations"""
    hist, bin_edges = np.histogram(values, bins=bins)
    max_count = max(hist)
    
    lines = []
    lines.append("Species-pH Correlation Distribution")
    lines.append("=" * 40)
    
    for i in range(bins):
        left_edge = bin_edges[i]
        right_edge = bin_edges[i + 1]
        count = hist[i]
        
        # Create bar
        bar_length = int((count / max_count) * width) if max_count > 0 else 0
        bar = "█" * bar_length
        
        # Format range
        range_str = f"[{left_edge:6.3f}, {right_edge:6.3f})"
        lines.append(f"{range_str} |{bar:<{width}} {count:3d}")
    
    return "\\n".join(lines)

def create_species_ranking_table(results_df, output_dir):
    """Create detailed ranking tables"""
    print("Creating species ranking tables...")
    
    # Top alkaliphiles table
    alkaliphiles = results_df[results_df['Correlation_with_pH'] > 0.2]
    acidophiles = results_df[results_df['Correlation_with_pH'] < -0.2]
    
    # Create ranking report
    with open(f'{output_dir}/species_rankings.txt', 'w') as f:
        f.write("SPECIES-pH CORRELATION RANKINGS\\n")
        f.write("=" * 60 + "\\n\\n")
        
        # Overall top correlations
        f.write("TOP 15 MOST pH-ASSOCIATED SPECIES (by absolute correlation):\\n")
        f.write("-" * 60 + "\\n")
        f.write(f"{'Rank':<4} {'Species':<20} {'Correlation':<12} {'Presence%':<10} {'Type':<12}\\n")
        f.write("-" * 60 + "\\n")
        
        top_15 = results_df.head(15)
        for i, (_, row) in enumerate(top_15.iterrows(), 1):
            species_name = row['Species'].replace('NormalizedAbundance', 'Species')
            corr = row['Correlation_with_pH']
            presence = row['Presence_Rate'] * 100
            
            if corr > 0.2:
                species_type = "Alkaliphile"
            elif corr < -0.2:
                species_type = "Acidophile"
            else:
                species_type = "Neutral"
            
            f.write(f"{i:<4} {species_name:<20} {corr:<12.3f} {presence:<10.1f} {species_type:<12}\\n")
        
        # Alkaliphiles section
        if len(alkaliphiles) > 0:
            f.write(f"\\n\\n🔵 ALKALIPHILES (pH increasers, r > 0.2): {len(alkaliphiles)} species\\n")
            f.write("-" * 60 + "\\n")
            for i, (_, row) in enumerate(alkaliphiles.iterrows(), 1):
                species_name = row['Species'].replace('NormalizedAbundance', 'Species')
                f.write(f"{i}. {species_name}: r = {row['Correlation_with_pH']:.3f}, ")
                f.write(f"presence = {row['Presence_Rate']*100:.1f}%\\n")
        
        # Acidophiles section  
        f.write(f"\\n\\n🔴 ACIDOPHILES (pH decreasers, r < -0.2): {len(acidophiles)} species\\n")
        f.write("-" * 60 + "\\n")
        for i, (_, row) in enumerate(acidophiles.iterrows(), 1):
            species_name = row['Species'].replace('NormalizedAbundance', 'Species')
            f.write(f"{i}. {species_name}: r = {row['Correlation_with_pH']:.3f}, ")
            f.write(f"presence = {row['Presence_Rate']*100:.1f}%\\n")
        
        # Statistical summary
        f.write(f"\\n\\nSTATISTICAL SUMMARY:\\n")
        f.write("-" * 30 + "\\n")
        f.write(f"Mean correlation: {results_df['Correlation_with_pH'].mean():.3f}\\n")
        f.write(f"Std correlation: {results_df['Correlation_with_pH'].std():.3f}\\n")
        f.write(f"Min correlation: {results_df['Correlation_with_pH'].min():.3f}\\n")
        f.write(f"Max correlation: {results_df['Correlation_with_pH'].max():.3f}\\n")
        f.write(f"Median presence rate: {results_df['Presence_Rate'].median()*100:.1f}%\\n")
        
        # Correlation histogram
        f.write(f"\\n\\nCORRELATION DISTRIBUTION:\\n")
        f.write("-" * 30 + "\\n")
        histogram = create_ascii_histogram(results_df['Correlation_with_pH'].values)
        f.write(histogram)
    
    print("✓ Created species ranking tables")

def create_presence_analysis(results_df, output_dir):
    """Analyze species presence patterns"""
    print("Creating presence analysis...")
    
    # Analyze presence vs correlation patterns
    high_presence = results_df[results_df['Presence_Rate'] > 0.3]  # Present in >30% samples
    low_presence = results_df[results_df['Presence_Rate'] < 0.1]   # Present in <10% samples
    
    with open(f'{output_dir}/presence_analysis.txt', 'w') as f:
        f.write("SPECIES PRESENCE vs pH CORRELATION ANALYSIS\\n")
        f.write("=" * 50 + "\\n\\n")
        
        f.write(f"HIGH PRESENCE SPECIES (>30% of samples): {len(high_presence)}\\n")
        f.write("-" * 50 + "\\n")
        f.write(f"{'Species':<25} {'Correlation':<12} {'Presence%':<10}\\n")
        f.write("-" * 50 + "\\n")
        
        for _, row in high_presence.sort_values('Correlation_with_pH', key=abs, ascending=False).head(10).iterrows():
            species_name = row['Species'].replace('NormalizedAbundance', 'Species')
            f.write(f"{species_name:<25} {row['Correlation_with_pH']:<12.3f} {row['Presence_Rate']*100:<10.1f}\\n")
        
        f.write(f"\\n\\nLOW PRESENCE SPECIES (<10% of samples): {len(low_presence)}\\n")
        f.write("-" * 50 + "\\n")
        f.write(f"{'Species':<25} {'Correlation':<12} {'Presence%':<10}\\n")
        f.write("-" * 50 + "\\n")
        
        for _, row in low_presence.sort_values('Correlation_with_pH', key=abs, ascending=False).head(10).iterrows():
            species_name = row['Species'].replace('NormalizedAbundance', 'Species')
            f.write(f"{species_name:<25} {row['Correlation_with_pH']:<12.3f} {row['Presence_Rate']*100:<10.1f}\\n")
        
        # Analysis insights
        f.write(f"\\n\\nKEY INSIGHTS:\\n")
        f.write("-" * 15 + "\\n")
        f.write(f"• Common species (high presence) show correlation range: ")
        f.write(f"{high_presence['Correlation_with_pH'].min():.3f} to {high_presence['Correlation_with_pH'].max():.3f}\\n")
        f.write(f"• Rare species (low presence) show correlation range: ")
        f.write(f"{low_presence['Correlation_with_pH'].min():.3f} to {low_presence['Correlation_with_pH'].max():.3f}\\n")
        f.write(f"• Mean correlation for common species: {high_presence['Correlation_with_pH'].mean():.3f}\\n")
        f.write(f"• Mean correlation for rare species: {low_presence['Correlation_with_pH'].mean():.3f}\\n")
    
    print("✓ Created presence analysis")

def create_abundance_analysis(results_df, output_dir):
    """Analyze abundance patterns"""
    print("Creating abundance analysis...")
    
    # Classify by abundance levels
    high_abundance = results_df[results_df['Max_Abundance'] > 0.1]  # Can reach >10% abundance
    moderate_abundance = results_df[(results_df['Max_Abundance'] > 0.01) & (results_df['Max_Abundance'] <= 0.1)]
    low_abundance = results_df[results_df['Max_Abundance'] <= 0.01]  # Never exceed 1%
    
    with open(f'{output_dir}/abundance_analysis.txt', 'w') as f:
        f.write("SPECIES ABUNDANCE vs pH CORRELATION ANALYSIS\\n")
        f.write("=" * 50 + "\\n\\n")
        
        f.write(f"HIGH ABUNDANCE SPECIES (max >10%): {len(high_abundance)}\\n")
        f.write("-" * 50 + "\\n")
        for _, row in high_abundance.sort_values('Correlation_with_pH', key=abs, ascending=False).iterrows():
            species_name = row['Species'].replace('NormalizedAbundance', 'Species')
            f.write(f"{species_name}: r = {row['Correlation_with_pH']:.3f}, ")
            f.write(f"max = {row['Max_Abundance']*100:.1f}%\\n")
        
        f.write(f"\\n\\nMODERATE ABUNDANCE SPECIES (1-10% max): {len(moderate_abundance)}\\n")
        f.write("-" * 50 + "\\n")
        for _, row in moderate_abundance.sort_values('Correlation_with_pH', key=abs, ascending=False).head(10).iterrows():
            species_name = row['Species'].replace('NormalizedAbundance', 'Species')
            f.write(f"{species_name}: r = {row['Correlation_with_pH']:.3f}, ")
            f.write(f"max = {row['Max_Abundance']*100:.1f}%\\n")
        
        f.write(f"\\n\\nLOW ABUNDANCE SPECIES (<1% max): {len(low_abundance)} (showing top 10)\\n")
        f.write("-" * 50 + "\\n")
        for _, row in low_abundance.sort_values('Correlation_with_pH', key=abs, ascending=False).head(10).iterrows():
            species_name = row['Species'].replace('NormalizedAbundance', 'Species')
            f.write(f"{species_name}: r = {row['Correlation_with_pH']:.3f}, ")
            f.write(f"max = {row['Max_Abundance']*100:.2f}%\\n")
        
        # Summary statistics
        f.write(f"\\n\\nABUNDANCE GROUP STATISTICS:\\n")
        f.write("-" * 30 + "\\n")
        f.write(f"High abundance - mean correlation: {high_abundance['Correlation_with_pH'].mean():.3f}\\n")
        f.write(f"Moderate abundance - mean correlation: {moderate_abundance['Correlation_with_pH'].mean():.3f}\\n")
        f.write(f"Low abundance - mean correlation: {low_abundance['Correlation_with_pH'].mean():.3f}\\n")
    
    print("✓ Created abundance analysis")

def create_scientific_summary(results_df, alkaliphiles, acidophiles, output_dir):
    """Create scientific publication summary"""
    print("Creating scientific summary...")
    
    with open(f'{output_dir}/scientific_summary.txt', 'w') as f:
        f.write("SPECIES-pH CORRELATION ANALYSIS: SCIENTIFIC SUMMARY\\n")
        f.write("=" * 60 + "\\n\\n")
        
        f.write("ABSTRACT\\n")
        f.write("-" * 8 + "\\n")
        f.write(f"We analyzed the correlation between individual species abundance and ")
        f.write(f"final pH in {results_df.iloc[0]['N_Samples']} microbial coalescence samples. ")
        f.write(f"Of {len(results_df)} species analyzed, {len(acidophiles)} showed significant ")
        f.write(f"negative correlation with pH (acidophiles, r < -0.2) while {len(alkaliphiles)} ")
        f.write(f"showed positive correlation (alkaliphiles, r > 0.2). The strongest pH ")
        f.write(f"associations were observed in acidophilic species, with {results_df.iloc[0]['Species']} ")
        f.write(f"showing the highest correlation magnitude (r = {results_df.iloc[0]['Correlation_with_pH']:.3f}).\\n\\n")
        
        f.write("KEY FINDINGS\\n")
        f.write("-" * 12 + "\\n")
        
        if len(acidophiles) > 0:
            strongest_acidophile = acidophiles.iloc[0]
            f.write(f"1. STRONGEST ACIDOPHILE: {strongest_acidophile['Species']}\\n")
            f.write(f"   - Correlation: r = {strongest_acidophile['Correlation_with_pH']:.3f}\\n")
            f.write(f"   - Present in {strongest_acidophile['Presence_Rate']*100:.1f}% of samples\\n")
            f.write(f"   - Maximum abundance: {strongest_acidophile['Max_Abundance']*100:.1f}%\\n\\n")
        
        if len(alkaliphiles) > 0:
            strongest_alkaliphile = alkaliphiles.iloc[0]
            f.write(f"2. STRONGEST ALKALIPHILE: {strongest_alkaliphile['Species']}\\n")
            f.write(f"   - Correlation: r = {strongest_alkaliphile['Correlation_with_pH']:.3f}\\n")
            f.write(f"   - Present in {strongest_alkaliphile['Presence_Rate']*100:.1f}% of samples\\n")
            f.write(f"   - Maximum abundance: {strongest_alkaliphile['Max_Abundance']*100:.1f}%\\n\\n")
        
        f.write(f"3. DISTRIBUTION OF pH ASSOCIATIONS\\n")
        f.write(f"   - Strong acidophiles (r < -0.3): {len(results_df[results_df['Correlation_with_pH'] < -0.3])}\\n")
        f.write(f"   - Moderate acidophiles (-0.3 ≤ r < -0.2): {len(results_df[(results_df['Correlation_with_pH'] >= -0.3) & (results_df['Correlation_with_pH'] < -0.2)])}\\n")
        f.write(f"   - Neutral species (-0.2 ≤ r ≤ 0.2): {len(results_df[(results_df['Correlation_with_pH'] >= -0.2) & (results_df['Correlation_with_pH'] <= 0.2)])}\\n")
        f.write(f"   - Moderate alkaliphiles (0.2 < r ≤ 0.3): {len(results_df[(results_df['Correlation_with_pH'] > 0.2) & (results_df['Correlation_with_pH'] <= 0.3)])}\\n")
        f.write(f"   - Strong alkaliphiles (r > 0.3): {len(results_df[results_df['Correlation_with_pH'] > 0.3])}\\n\\n")
        
        f.write("BIOLOGICAL IMPLICATIONS\\n")
        f.write("-" * 22 + "\\n")
        f.write(f"• pH-decreasing species outnumber pH-increasing species {len(acidophiles)}:{len(alkaliphiles)}\\n")
        f.write(f"• Most species ({len(results_df) - len(acidophiles) - len(alkaliphiles)}) are pH-neutral\\n")
        f.write(f"• Strong correlations suggest species-specific pH tolerance ranges\\n")
        f.write(f"• Species presence rates vary from {results_df['Presence_Rate'].min()*100:.1f}% ")
        f.write(f"to {results_df['Presence_Rate'].max()*100:.1f}%\\n\\n")
        
        f.write("STATISTICAL SUMMARY\\n")
        f.write("-" * 18 + "\\n")
        f.write(f"• Mean correlation coefficient: {results_df['Correlation_with_pH'].mean():.4f} ± {results_df['Correlation_with_pH'].std():.4f}\\n")
        f.write(f"• Range: {results_df['Correlation_with_pH'].min():.3f} to {results_df['Correlation_with_pH'].max():.3f}\\n")
        f.write(f"• Species with |r| > 0.2: {len(results_df[abs(results_df['Correlation_with_pH']) > 0.2])} ({len(results_df[abs(results_df['Correlation_with_pH']) > 0.2])/len(results_df)*100:.1f}%)\\n")
        f.write(f"• Species with |r| > 0.3: {len(results_df[abs(results_df['Correlation_with_pH']) > 0.3])} ({len(results_df[abs(results_df['Correlation_with_pH']) > 0.3])/len(results_df)*100:.1f}%)\\n")
    
    print("✓ Created scientific summary")

def main():
    """Main function to create all text-based analyses"""
    print("=" * 60)
    print("SPECIES-pH TEXT-BASED ANALYSIS GENERATION")
    print("=" * 60)
    
    # Load data
    results_df, alkaliphiles, acidophiles = load_analysis_results()
    
    output_dir = "Figure/pH_Analysis"
    
    # Create all text-based analyses
    create_species_ranking_table(results_df, output_dir)
    create_presence_analysis(results_df, output_dir)
    create_abundance_analysis(results_df, output_dir)
    create_scientific_summary(results_df, alkaliphiles, acidophiles, output_dir)
    
    print(f"\\n🎉 ALL TEXT-BASED ANALYSES COMPLETE!")
    print(f"📁 Saved to: {output_dir}/")
    print("📊 Generated analysis files:")
    print("  • species_rankings.txt - Comprehensive species rankings")
    print("  • presence_analysis.txt - Presence pattern analysis")  
    print("  • abundance_analysis.txt - Abundance pattern analysis")
    print("  • scientific_summary.txt - Publication-ready summary")
    print("\\n✅ Ready for scientific interpretation!")

if __name__ == "__main__":
    main()