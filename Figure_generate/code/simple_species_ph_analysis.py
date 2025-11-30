#!/usr/bin/env python3
"""
Simple Species-pH Analysis
Simplified version to work around environment compatibility issues
"""

import numpy as np
import pandas as pd
import os

# Load data directly
def load_data():
    """Load species abundance and pH data"""
    print("Loading data...")
    
    # Species abundance data
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    # Community pH data
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    ph_data = communities_data[['SampleIDX', 'fieldPH1', 'fieldPH7']].copy()
    
    # Merge data
    merged_data = abundance_data.merge(ph_data, on='SampleIDX', how='inner')
    
    print(f"✓ Loaded {len(merged_data)} samples with both species and pH data")
    print(f"✓ Data shape: {merged_data.shape}")
    print(f"✓ pH data columns: fieldPH1, fieldPH7")
    
    return merged_data

def calculate_simple_correlations(merged_data):
    """Calculate basic correlations between species abundance and pH"""
    print("\\nCalculating species-pH correlations...")
    
    # Get species abundance columns
    abundance_columns = [col for col in merged_data.columns if col.startswith('NormalizedAbundance')]
    print(f"Found {len(abundance_columns)} species abundance columns")
    
    results = []
    
    # Calculate correlations for fieldPH7 (final pH)
    ph_data = merged_data['fieldPH7'].dropna()
    valid_indices = ph_data.index
    
    print(f"Valid pH measurements: {len(ph_data)} samples")
    
    for species_col in abundance_columns:
        species_data = merged_data.loc[valid_indices, species_col]
        
        # Calculate Pearson correlation manually
        if len(species_data) > 10:  # Need sufficient data
            # Remove cases where both values are zero/missing
            mask = ~(np.isnan(species_data) | np.isnan(ph_data))
            if np.sum(mask) > 10:
                clean_species = species_data[mask]
                clean_ph = ph_data[mask]
                
                # Calculate correlation manually
                mean_species = np.mean(clean_species)
                mean_ph = np.mean(clean_ph)
                
                numerator = np.sum((clean_species - mean_species) * (clean_ph - mean_ph))
                denom_species = np.sum((clean_species - mean_species) ** 2)
                denom_ph = np.sum((clean_ph - mean_ph) ** 2)
                
                if denom_species > 0 and denom_ph > 0:
                    correlation = numerator / np.sqrt(denom_species * denom_ph)
                    
                    # Calculate some basic statistics
                    mean_abundance = np.mean(clean_species)
                    max_abundance = np.max(clean_species)
                    presence_rate = np.sum(clean_species > 0.001) / len(clean_species)  # >0.1% abundance
                    
                    results.append({
                        'Species': species_col,
                        'Correlation_with_pH': correlation,
                        'Mean_Abundance': mean_abundance,
                        'Max_Abundance': max_abundance, 
                        'Presence_Rate': presence_rate,
                        'N_Samples': len(clean_species)
                    })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Correlation_with_pH', key=abs, ascending=False)
    
    print(f"✓ Calculated correlations for {len(results_df)} species")
    
    return results_df

def analyze_ph_associations(results_df):
    """Analyze pH associations and identify key species"""
    print("\\nAnalyzing pH associations...")
    
    # Define thresholds
    strong_correlation = 0.3
    moderate_correlation = 0.2
    
    # Classify species
    alkaliphiles = results_df[results_df['Correlation_with_pH'] > moderate_correlation]
    acidophiles = results_df[results_df['Correlation_with_pH'] < -moderate_correlation]
    neutral = results_df[abs(results_df['Correlation_with_pH']) <= moderate_correlation]
    
    print(f"\\n📊 SPECIES CLASSIFICATION:")
    print(f"Alkaliphiles (pH increasers): {len(alkaliphiles)} species")
    print(f"Acidophiles (pH decreasers): {len(acidophiles)} species")
    print(f"Neutral species: {len(neutral)} species")
    
    print(f"\\n🔵 TOP 10 ALKALIPHILES (High pH lovers):")
    for i, (_, row) in enumerate(alkaliphiles.head(10).iterrows(), 1):
        print(f"  {i}. {row['Species']}: r = {row['Correlation_with_pH']:.3f}, presence = {row['Presence_Rate']:.1%}")
    
    print(f"\\n🔴 TOP 10 ACIDOPHILES (Low pH lovers):")
    for i, (_, row) in enumerate(acidophiles.head(10).iterrows(), 1):
        print(f"  {i}. {row['Species']}: r = {row['Correlation_with_pH']:.3f}, presence = {row['Presence_Rate']:.1%}")
    
    return alkaliphiles, acidophiles, neutral

def save_results(results_df, alkaliphiles, acidophiles):
    """Save analysis results to files"""
    
    # Create output directory
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save main results
    results_df.to_csv(f'{output_dir}/species_ph_correlations_simple.csv', index=False)
    
    # Save classified species
    alkaliphiles.to_csv(f'{output_dir}/alkaliphile_species.csv', index=False)
    acidophiles.to_csv(f'{output_dir}/acidophile_species.csv', index=False)
    
    # Create summary report
    with open(f'{output_dir}/analysis_summary.txt', 'w') as f:
        f.write("SPECIES-pH CORRELATION ANALYSIS SUMMARY\\n")
        f.write("=" * 50 + "\\n\\n")
        
        f.write(f"Total species analyzed: {len(results_df)}\\n")
        f.write(f"Alkaliphiles (r > 0.2): {len(alkaliphiles)}\\n")
        f.write(f"Acidophiles (r < -0.2): {len(acidophiles)}\\n\\n")
        
        f.write("TOP ALKALIPHILES:\\n")
        f.write("-" * 20 + "\\n")
        for _, row in alkaliphiles.head(5).iterrows():
            f.write(f"{row['Species']}: r = {row['Correlation_with_pH']:.3f}\\n")
        
        f.write("\\nTOP ACIDOPHILES:\\n")
        f.write("-" * 20 + "\\n")
        for _, row in acidophiles.head(5).iterrows():
            f.write(f"{row['Species']}: r = {row['Correlation_with_pH']:.3f}\\n")
    
    print(f"\\n📁 Results saved to {output_dir}/")
    print("  - species_ph_correlations_simple.csv")
    print("  - alkaliphile_species.csv") 
    print("  - acidophile_species.csv")
    print("  - analysis_summary.txt")

def main():
    """Main analysis function"""
    print("=" * 60)
    print("SIMPLE SPECIES-pH CORRELATION ANALYSIS")
    print("=" * 60)
    
    # Load data
    merged_data = load_data()
    
    # Calculate correlations
    results_df = calculate_simple_correlations(merged_data)
    
    # Analyze associations
    alkaliphiles, acidophiles, neutral = analyze_ph_associations(results_df)
    
    # Save results
    save_results(results_df, alkaliphiles, acidophiles)
    
    print("\\n🎉 ANALYSIS COMPLETE!")
    print("✅ Successfully identified pH-associated species")
    print("📊 Results saved for further analysis")
    
    return results_df, alkaliphiles, acidophiles

if __name__ == "__main__":
    results = main()