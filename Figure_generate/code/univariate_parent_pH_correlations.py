#!/usr/bin/env python3
"""
Univariate Correlations: Each Parent Species vs Final pH
Creates Excel file with separate sheets for each medium
"""

import numpy as np
import pandas as pd
import os
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def load_parent_coalescence_data():
    """Load and link parent communities to coalescence outcomes"""
    print("Loading parent-coalescence linked data...")
    
    # Load coalescence recipe
    recipe = pd.read_excel("../../Postprocessed/CoalescenceRecipe.xlsx")
    
    # Load abundance and metadata
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
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
    
    # Separate parent and coalesced communities
    parent_communities = full_data[full_data['CoalescenceType'] == 'S'].copy()
    coalesced_communities = full_data[full_data['CoalescenceType'] == 'C'].copy()
    
    # Get abundance columns (only species 1-15)
    abundance_cols = [f'NormalizedAbundance{i}' for i in range(1, 16)]
    # Filter to only include columns that actually exist in the data
    abundance_cols = [col for col in abundance_cols if col in parent_communities.columns]
    print(f"✓ Using species 1-15: {len(abundance_cols)} species columns")
    
    # Aggregate by CommunityIDX and Medium (mean abundances)
    parent_agg = parent_communities.groupby(['CommunityIDX', 'Medium']).agg({
        **{col: 'mean' for col in abundance_cols},
        'fieldPH1': 'mean', 'fieldPH7': 'mean'
    }).reset_index()
    
    coalesced_agg = coalesced_communities.groupby(['CommunityIDX', 'Medium']).agg({
        **{col: 'mean' for col in abundance_cols},
        'fieldPH1': 'mean', 'fieldPH7': 'mean'
    }).reset_index()
    
    # Create mappings
    parent_dict = {}
    for _, row in parent_agg.iterrows():
        key = (row['CommunityIDX'], row['Medium'])
        parent_dict[key] = row.to_dict()
    
    coalesced_dict = {}
    for _, row in coalesced_agg.iterrows():
        key = (row['CommunityIDX'], row['Medium'])
        coalesced_dict[key] = row.to_dict()
    
    # Link parent compositions to final pH outcomes
    linked_data = []
    
    for medium in ['H', 'L', 'M']:
        for _, row in recipe.iterrows():
            coal_idx = row['CommunityIDX_Coal']
            sub1_idx = row['CommunityIDX_Sub1']
            sub2_idx = row['CommunityIDX_Sub2']
            
            coal_key = (coal_idx, medium)
            sub1_key = (sub1_idx, medium)
            sub2_key = (sub2_idx, medium)
            
            if (coal_key in coalesced_dict and 
                sub1_key in parent_dict and 
                sub2_key in parent_dict):
                
                coal_data = coalesced_dict[coal_key]
                parent1_data = parent_dict[sub1_key]
                parent2_data = parent_dict[sub2_key]
                
                if not pd.isna(coal_data['fieldPH7']):
                    # Add records for both parents
                    for parent_idx, parent_data, parent_label in [(sub1_idx, parent1_data, 'Parent1'), 
                                                                  (sub2_idx, parent2_data, 'Parent2')]:
                        record = {
                            'CoalescedCommunityIDX': coal_idx,
                            'ParentCommunityIDX': parent_idx,
                            'ParentLabel': parent_label,
                            'Medium': medium,
                            'Final_pH': coal_data['fieldPH7'],
                            'Initial_pH': coal_data['fieldPH1'],
                            'Parent_Initial_pH': parent_data['fieldPH1'],
                            'Parent_Final_pH': parent_data['fieldPH7']
                        }
                        
                        # Add all parent species abundances
                        for col in abundance_cols:
                            record[f'Parent_{col}'] = parent_data[col]
                        
                        linked_data.append(record)
    
    linked_df = pd.DataFrame(linked_data)
    print(f"✓ Created {len(linked_df)} parent-coalescence records")
    print(f"✓ Medium breakdown: {linked_df['Medium'].value_counts().to_dict()}")
    
    return linked_df, abundance_cols

def calculate_univariate_correlations(linked_df, abundance_cols, medium_type):
    """Calculate univariate correlations for each species in specific medium"""
    print(f"\\nCalculating correlations for Medium {medium_type}...")
    
    # Filter for specific medium
    medium_data = linked_df[linked_df['Medium'] == medium_type].copy()
    print(f"   Records for medium {medium_type}: {len(medium_data)}")
    
    if len(medium_data) < 5:
        print(f"   ⚠️ Too few records for medium {medium_type}")
        return pd.DataFrame()
    
    results = []
    
    for species_col in abundance_cols:
        parent_col = f'Parent_{species_col}'
        
        if parent_col in medium_data.columns:
            # Get species abundance and final pH data
            species_abundance = medium_data[parent_col].values
            final_pH = medium_data['Final_pH'].values
            
            # Remove missing values
            valid_mask = ~(np.isnan(species_abundance) | np.isnan(final_pH))
            if np.sum(valid_mask) < 5:
                continue
                
            clean_abundance = species_abundance[valid_mask]
            clean_pH = final_pH[valid_mask]
            
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
                    'Correlation_with_Final_pH': correlation,
                    'P_Value': p_value,
                    'Significant': p_value < 0.05,
                    'N_Samples': len(clean_abundance),
                    'Mean_Abundance': mean_abundance,
                    'Std_Abundance': std_abundance,
                    'Max_Abundance': max_abundance,
                    'Presence_Rate': presence_rate,
                    'pH_Effect': 'Increases' if correlation > 0 else 'Decreases'
                })
                
            except Exception as e:
                print(f"     Error calculating correlation for {species_col}: {e}")
                continue
    
    results_df = pd.DataFrame(results)
    if len(results_df) > 0:
        results_df = results_df.sort_values('Correlation_with_Final_pH', key=abs, ascending=False)
        
        print(f"   ✓ Calculated correlations for {len(results_df)} species")
        print(f"   ✓ Significant correlations (p<0.05): {results_df['Significant'].sum()}")
        
        # Show top correlations
        print(f"   Top 5 correlations:")
        for i, (_, row) in enumerate(results_df.head(5).iterrows(), 1):
            sig = "*" if row['Significant'] else " "
            print(f"     {i}. {row['Species']}: r={row['Correlation_with_Final_pH']:.3f}{sig}, p={row['P_Value']:.3f}")
    
    return results_df

def create_excel_output(all_results, linked_df):
    """Create Excel file with multiple sheets"""
    print("\\nCreating Excel output...")
    
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    excel_file = f"{output_dir}/Parent_Species_pH_Correlations_by_Medium.xlsx"
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        
        # Create summary sheet
        summary_data = []
        for results_df in all_results:
            if len(results_df) > 0:
                medium = results_df['Medium'].iloc[0]
                n_species = len(results_df)
                n_significant = results_df['Significant'].sum()
                n_samples = results_df['N_Samples'].iloc[0] if len(results_df) > 0 else 0
                
                # Top positive and negative correlations
                top_positive = results_df[results_df['Correlation_with_Final_pH'] > 0].head(1)
                top_negative = results_df[results_df['Correlation_with_Final_pH'] < 0].head(1)
                
                top_pos_species = top_positive['Species'].iloc[0] if len(top_positive) > 0 else "None"
                top_pos_corr = top_positive['Correlation_with_Final_pH'].iloc[0] if len(top_positive) > 0 else 0
                
                top_neg_species = top_negative['Species'].iloc[0] if len(top_negative) > 0 else "None"
                top_neg_corr = top_negative['Correlation_with_Final_pH'].iloc[0] if len(top_negative) > 0 else 0
                
                summary_data.append({
                    'Medium': medium,
                    'N_Species_Analyzed': n_species,
                    'N_Significant_Correlations': n_significant,
                    'N_Samples': n_samples,
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
        
        # Create combined sheet with all results
        if all_results:
            combined_df = pd.concat([df for df in all_results if len(df) > 0], ignore_index=True)
            combined_df.to_excel(writer, sheet_name='All_Media_Combined', index=False)
        
        # Add raw data sheet
        sample_data = linked_df[['Medium', 'Final_pH', 'Initial_pH', 'ParentCommunityIDX', 'CoalescedCommunityIDX']].copy()
        sample_data.to_excel(writer, sheet_name='Raw_Data_Sample', index=False)
    
    print(f"✓ Excel file saved: {excel_file}")
    
    # Also create CSV files for each medium
    for results_df in all_results:
        if len(results_df) > 0:
            medium = results_df['Medium'].iloc[0]
            csv_file = f"{output_dir}/Parent_Species_pH_Correlations_Medium_{medium}.csv"
            results_df.to_csv(csv_file, index=False)
            print(f"✓ CSV saved: {csv_file}")
    
    return excel_file

def main():
    """Main analysis function"""
    print("=" * 80)
    print("UNIVARIATE PARENT SPECIES → FINAL pH CORRELATION ANALYSIS")
    print("=" * 80)
    
    # Load data
    linked_df, abundance_cols = load_parent_coalescence_data()
    
    # Calculate correlations for each medium
    all_results = []
    for medium in ['H', 'L', 'M']:
        results_df = calculate_univariate_correlations(linked_df, abundance_cols, medium)
        all_results.append(results_df)
    
    # Create Excel output
    excel_file = create_excel_output(all_results, linked_df)
    
    print("\\n" + "="*60)
    print("🎉 UNIVARIATE CORRELATION ANALYSIS COMPLETE!")
    print("✅ Individual species correlations with final pH")
    print("✅ Separate analysis by medium type (H/L/M)")
    print("✅ Statistical significance testing")
    print(f"📊 Results saved to Excel: {excel_file}")
    print("="*60)
    
    return all_results, linked_df

if __name__ == "__main__":
    results, data = main()