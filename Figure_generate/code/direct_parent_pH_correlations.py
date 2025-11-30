#!/usr/bin/env python3
"""
Direct Parent Community Analysis: Parent Species vs Parent pH
Analyzes correlations within parent communities only (no coalescence linking)
"""

import numpy as np
import pandas as pd
import os
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def load_parent_community_data():
    """Load parent community data directly"""
    print("Loading parent community data...")
    
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
    
    # Filter for PARENT communities only (CoalescenceType == 'S')
    parent_communities = full_data[full_data['CoalescenceType'] == 'S'].copy()
    
    # Get abundance columns (species 1-15 only)
    abundance_cols = [f'NormalizedAbundance{i}' for i in range(1, 16)]
    abundance_cols = [col for col in abundance_cols if col in parent_communities.columns]
    
    print(f"✓ Parent communities: {len(parent_communities)} records")
    print(f"✓ Using species 1-15: {len(abundance_cols)} species columns")
    print(f"✓ Medium breakdown:")
    medium_counts = parent_communities['Medium'].value_counts()
    for medium, count in medium_counts.items():
        print(f"   {medium}: {count} parent communities")
    
    # Remove records with missing pH data
    parent_communities = parent_communities[~parent_communities['fieldPH7'].isna()].copy()
    print(f"✓ Parent communities with pH data: {len(parent_communities)}")
    
    return parent_communities, abundance_cols

def calculate_parent_correlations(parent_communities, abundance_cols, medium_type):
    """Calculate correlations between species abundance and pH within parent communities"""
    print(f"\\nAnalyzing Medium {medium_type} parent communities...")
    
    # Filter for specific medium
    medium_data = parent_communities[parent_communities['Medium'] == medium_type].copy()
    print(f"   Parent communities in medium {medium_type}: {len(medium_data)}")
    
    if len(medium_data) < 5:
        print(f"   ⚠️ Too few parent communities for medium {medium_type}")
        return pd.DataFrame()
    
    results = []
    
    for species_col in abundance_cols:
        if species_col in medium_data.columns:
            # Get species abundance and parent community pH
            species_abundance = medium_data[species_col].values
            parent_pH = medium_data['fieldPH7'].values  # Use parent's own pH
            
            # Remove missing values
            valid_mask = ~(np.isnan(species_abundance) | np.isnan(parent_pH))
            if np.sum(valid_mask) < 5:
                continue
                
            clean_abundance = species_abundance[valid_mask]
            clean_pH = parent_pH[valid_mask]
            
            # Calculate Pearson correlation
            try:
                correlation, p_value = stats.pearsonr(clean_abundance, clean_pH)
                
                # Calculate additional statistics
                mean_abundance = np.mean(clean_abundance)
                std_abundance = np.std(clean_abundance)
                max_abundance = np.max(clean_abundance)
                presence_rate = np.sum(clean_abundance > 0.001) / len(clean_abundance)
                
                results.append({
                    'Species': species_col,
                    'Medium': medium_type,
                    'Correlation_with_pH': correlation,
                    'P_Value': p_value,
                    'Significant': p_value < 0.05,
                    'N_Communities': len(clean_abundance),
                    'Mean_Abundance': mean_abundance,
                    'Std_Abundance': std_abundance,
                    'Max_Abundance': max_abundance,
                    'Presence_Rate': presence_rate,
                    'pH_Effect': 'Increases' if correlation > 0 else 'Decreases',
                    'pH_Range': f"{clean_pH.min():.2f} - {clean_pH.max():.2f}"
                })
                
            except Exception as e:
                print(f"     Error calculating correlation for {species_col}: {e}")
                continue
    
    results_df = pd.DataFrame(results)
    if len(results_df) > 0:
        results_df = results_df.sort_values('Correlation_with_pH', key=abs, ascending=False)
        
        print(f"   ✓ Analyzed {len(results_df)} species")
        print(f"   ✓ Significant correlations (p<0.05): {results_df['Significant'].sum()}")
        
        # Show pH range for this medium
        if len(results_df) > 0:
            print(f"   ✓ pH range: {results_df['pH_Range'].iloc[0]}")
        
        # Show top correlations
        print(f"   Top 5 correlations:")
        for i, (_, row) in enumerate(results_df.head(5).iterrows(), 1):
            sig = "*" if row['Significant'] else " "
            print(f"     {i}. {row['Species']}: r={row['Correlation_with_pH']:.3f}{sig}, p={row['P_Value']:.3f}")
    
    return results_df

def create_excel_output(all_results, parent_communities):
    """Create Excel file with results"""
    print("\\nCreating Excel output...")
    
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    excel_file = f"{output_dir}/Parent_Community_Species_pH_Correlations.xlsx"
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        
        # Create summary sheet
        summary_data = []
        for results_df in all_results:
            if len(results_df) > 0:
                medium = results_df['Medium'].iloc[0]
                n_species = len(results_df)
                n_significant = results_df['Significant'].sum()
                n_communities = results_df['N_Communities'].iloc[0] if len(results_df) > 0 else 0
                ph_range = results_df['pH_Range'].iloc[0] if len(results_df) > 0 else "N/A"
                
                # Top positive and negative correlations
                top_positive = results_df[results_df['Correlation_with_pH'] > 0].head(1)
                top_negative = results_df[results_df['Correlation_with_pH'] < 0].head(1)
                
                top_pos_species = top_positive['Species'].iloc[0] if len(top_positive) > 0 else "None"
                top_pos_corr = top_positive['Correlation_with_pH'].iloc[0] if len(top_positive) > 0 else 0
                
                top_neg_species = top_negative['Species'].iloc[0] if len(top_negative) > 0 else "None"
                top_neg_corr = top_negative['Correlation_with_pH'].iloc[0] if len(top_negative) > 0 else 0
                
                summary_data.append({
                    'Medium': medium,
                    'N_Parent_Communities': n_communities,
                    'pH_Range': ph_range,
                    'N_Species_Analyzed': n_species,
                    'N_Significant_Correlations': n_significant,
                    'Top_pH_Increaser': top_pos_species,
                    'Top_pH_Increaser_Correlation': top_pos_corr,
                    'Top_pH_Decreaser': top_neg_species,
                    'Top_pH_Decreaser_Correlation': top_neg_corr
                })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Create individual medium sheets
        for results_df in all_results:
            if len(results_df) > 0:
                medium = results_df['Medium'].iloc[0]
                sheet_name = f'Medium_{medium}'
                results_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Create combined sheet
        if all_results:
            combined_df = pd.concat([df for df in all_results if len(df) > 0], ignore_index=True)
            combined_df.to_excel(writer, sheet_name='All_Media_Combined', index=False)
        
        # Add parent community info
        parent_info = parent_communities[['Medium', 'CommunityIDX', 'fieldPH7']].groupby(['Medium', 'CommunityIDX']).mean().reset_index()
        parent_info.to_excel(writer, sheet_name='Parent_Community_Info', index=False)
    
    print(f"✓ Excel file saved: {excel_file}")
    
    # Also create CSV files
    for results_df in all_results:
        if len(results_df) > 0:
            medium = results_df['Medium'].iloc[0]
            csv_file = f"{output_dir}/Parent_Communities_Medium_{medium}.csv"
            results_df.to_csv(csv_file, index=False)
            print(f"✓ CSV saved: {csv_file}")
    
    return excel_file

def main():
    """Main analysis function"""
    print("=" * 80)
    print("DIRECT PARENT COMMUNITY ANALYSIS")  
    print("Species Abundance vs pH within Parent Communities")
    print("=" * 80)
    
    # Load parent community data directly
    parent_communities, abundance_cols = load_parent_community_data()
    
    # Calculate correlations for each medium
    all_results = []
    for medium in ['H', 'L', 'M']:
        results_df = calculate_parent_correlations(parent_communities, abundance_cols, medium)
        all_results.append(results_df)
    
    # Create Excel output
    excel_file = create_excel_output(all_results, parent_communities)
    
    print("\\n" + "="*60)
    print("🎉 PARENT COMMUNITY ANALYSIS COMPLETE!")
    print("✅ Direct analysis of parent communities only")
    print("✅ Species abundance vs parent community pH")
    print("✅ No coalescence event linking required")
    print(f"📊 Results saved to Excel: {excel_file}")
    print("="*60)
    
    return all_results, parent_communities

if __name__ == "__main__":
    results, data = main()