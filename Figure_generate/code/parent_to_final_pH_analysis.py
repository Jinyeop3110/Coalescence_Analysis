#!/usr/bin/env python3
"""
Multivariate Regression: Parent Community Species → Final Coalesced pH
Analyzes how parent community composition predicts final pH after coalescence
"""

import numpy as np
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

def load_parent_and_coalescence_data():
    """Load parent community data and link to coalescence outcomes"""
    print("Loading parent communities and coalescence data...")
    
    # 1. Load coalescence recipe (shows which parents created which coalesced communities)
    recipe = pd.read_excel("../../Postprocessed/CoalescenceRecipe.xlsx")
    print(f"✓ Loaded coalescence recipe: {len(recipe)} coalescence events")
    
    # 2. Load abundance data for all communities
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    # 3. Load metadata to identify parent vs coalesced communities
    metadata = pd.read_excel("../../Postprocessed/Metadata.xlsx")
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    # 4. Merge abundance with metadata
    full_data = abundance_data.merge(
        metadata[['SampleIDX', 'CoalescenceType', 'Medium', 'CommunityIDX']], 
        on='SampleIDX', 
        how='inner'
    )
    
    # 5. Add pH data
    full_data = full_data.merge(
        communities_data[['SampleIDX', 'fieldPH1', 'fieldPH7']], 
        on='SampleIDX', 
        how='inner'
    )
    
    # 6. Separate parent and coalesced communities
    parent_communities = full_data[full_data['CoalescenceType'] == 'S'].copy()
    coalesced_communities = full_data[full_data['CoalescenceType'] == 'C'].copy()
    
    print(f"✓ Parent communities: {len(parent_communities)}")
    print(f"✓ Coalesced communities: {len(coalesced_communities)}")
    
    return parent_communities, coalesced_communities, recipe

def link_parents_to_outcomes(parent_communities, coalesced_communities, recipe):
    """Link parent community compositions to coalescence outcomes"""
    print("\\nLinking parent communities to coalescence outcomes...")
    
    # Handle duplicates by creating medium-specific mappings
    # Group by CommunityIDX and Medium, then take mean abundances
    abundance_cols = [col for col in parent_communities.columns if col.startswith('NormalizedAbundance')][:10]
    
    # Create aggregated parent data (mean abundances by CommunityIDX and Medium)
    parent_agg = parent_communities.groupby(['CommunityIDX', 'Medium']).agg({
        **{col: 'mean' for col in abundance_cols},
        'fieldPH1': 'mean',
        'fieldPH7': 'mean'
    }).reset_index()
    
    # Create aggregated coalesced data  
    coalesced_agg = coalesced_communities.groupby(['CommunityIDX', 'Medium']).agg({
        **{col: 'mean' for col in abundance_cols},
        'fieldPH1': 'mean',
        'fieldPH7': 'mean'
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
    
    linked_data = []
    
    # Try each medium separately
    for medium in ['H', 'L', 'M']:
        for _, row in recipe.iterrows():
            coal_idx = row['CommunityIDX_Coal']
            sub1_idx = row['CommunityIDX_Sub1']
            sub2_idx = row['CommunityIDX_Sub2']
            
            # Create keys for this medium
            coal_key = (coal_idx, medium)
            sub1_key = (sub1_idx, medium)
            sub2_key = (sub2_idx, medium)
            
            # Check if we have all the required data for this medium
            if (coal_key in coalesced_dict and 
                sub1_key in parent_dict and 
                sub2_key in parent_dict):
                
                coal_data = coalesced_dict[coal_key]
                parent1_data = parent_dict[sub1_key]
                parent2_data = parent_dict[sub2_key]
                
                # Check if pH data is available
                if not pd.isna(coal_data['fieldPH7']):
                    
                    # Create record with parent abundances and final pH
                    record = {
                        'CoalescedCommunityIDX': coal_idx,
                        'Parent1_IDX': sub1_idx,
                        'Parent2_IDX': sub2_idx,
                        'Medium': medium,
                        'Final_pH': coal_data['fieldPH7'],
                        'Initial_pH': coal_data['fieldPH1']
                    }
                    
                    # Add parent1 abundances (prefix with P1_)
                    for col in abundance_cols:
                        record[f'P1_{col}'] = parent1_data[col]
                    
                    # Add parent2 abundances (prefix with P2_)
                    for col in abundance_cols:
                        record[f'P2_{col}'] = parent2_data[col]
                    
                    # Add combined parent abundances (average)
                    for col in abundance_cols:
                        record[f'Combined_{col}'] = (parent1_data[col] + parent2_data[col]) / 2
                    
                    linked_data.append(record)
    
    linked_df = pd.DataFrame(linked_data)
    print(f"✓ Successfully linked {len(linked_df)} parent-coalescence pairs")
    
    if len(linked_df) > 0:
        print(f"✓ Medium breakdown:")
        for medium, count in linked_df['Medium'].value_counts().items():
            print(f"   {medium}: {count} coalescence events")
        
        print(f"✓ Final pH range: {linked_df['Final_pH'].min():.2f} - {linked_df['Final_pH'].max():.2f}")
    
    return linked_df

def run_parent_regression_by_medium(linked_df, medium_type, parent_type='Combined'):
    """Run regression using parent community composition to predict final pH"""
    print(f"\\n{'='*20} MEDIUM {medium_type} - {parent_type.upper()} PARENTS {'='*20}")
    
    # Filter for specific medium
    medium_data = linked_df[linked_df['Medium'] == medium_type].copy()
    print(f"Coalescence events for medium {medium_type}: {len(medium_data)}")
    
    if len(medium_data) < 10:
        print(f"⚠️  WARNING: Only {len(medium_data)} events for medium {medium_type}. Skipping.")
        return None
    
    # Prepare features (parent abundances) and target (final pH)
    abundance_cols = [col for col in medium_data.columns if col.startswith(f'{parent_type}_NormalizedAbundance')][:10]
    
    X = medium_data[abundance_cols].copy()
    y = medium_data['Final_pH'].copy()
    
    # Fill missing values
    X = X.fillna(0)
    
    print(f"✓ Using {len(abundance_cols)} parent species features")
    print(f"✓ Final pH range: {y.min():.2f} - {y.max():.2f}")
    
    # Split for validation if enough samples
    if len(X) >= 20:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Fit model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Metrics
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
        rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
        
        print(f"📊 RESULTS FOR MEDIUM {medium_type}:")
        print(f"   Training R² = {r2_train:.4f}")
        print(f"   Test R² = {r2_test:.4f}")
        print(f"   Training RMSE = {rmse_train:.4f}")
        print(f"   Test RMSE = {rmse_test:.4f}")
        
    else:
        # Use all data if sample size is small
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r2_train = r2_score(y, y_pred)
        r2_test = np.nan
        rmse_train = np.sqrt(mean_squared_error(y, y_pred))
        rmse_test = np.nan
        
        print(f"📊 RESULTS FOR MEDIUM {medium_type} (no train/test split):")
        print(f"   R² = {r2_train:.4f}")
        print(f"   RMSE = {rmse_train:.4f}")
    
    print(f"   Intercept = {model.intercept_:.4f}")
    
    # Create results dataframe
    species_names = [col.replace(f'{parent_type}_', '') for col in abundance_cols]
    results_df = pd.DataFrame({
        'Species': species_names,
        'Coefficient': model.coef_,
        'Abs_Coefficient': np.abs(model.coef_),
        'Medium': medium_type,
        'ParentType': parent_type
    })
    
    results_df = results_df.sort_values('Abs_Coefficient', ascending=False)
    
    print(f"   Top 5 most predictive parent species:")
    for i, (_, row) in enumerate(results_df.head(5).iterrows(), 1):
        direction = "increases" if row['Coefficient'] > 0 else "decreases"
        print(f"     {i}. {row['Species']}: {row['Coefficient']:.4f} (final pH {direction})")
    
    return {
        'medium': medium_type,
        'parent_type': parent_type,
        'model': model,
        'results_df': results_df,
        'metrics': {
            'r2_train': r2_train,
            'r2_test': r2_test,
            'rmse_train': rmse_train,
            'rmse_test': rmse_test,
            'n_samples': len(X)
        }
    }

def save_parent_analysis_results(all_results):
    """Save parent community analysis results"""
    print(f"\\n{'='*20} SAVING RESULTS {'='*20}")
    
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    # Combine all results
    all_coefficients = []
    for result in all_results:
        if result:
            all_coefficients.append(result['results_df'])
    
    if all_coefficients:
        combined_df = pd.concat(all_coefficients, ignore_index=True)
        combined_df.to_csv(f'{output_dir}/parent_to_final_pH_coefficients_by_medium.csv', index=False)
        
        # Create summary
        with open(f'{output_dir}/parent_to_final_pH_summary.txt', 'w') as f:
            f.write("PARENT COMMUNITY → FINAL pH ANALYSIS\\n")
            f.write("=" * 60 + "\\n\\n")
            
            for result in all_results:
                if result:
                    medium = result['medium']
                    parent_type = result['parent_type']
                    metrics = result['metrics']
                    results_df = result['results_df']
                    model = result['model']
                    
                    f.write(f"MEDIUM {medium} - {parent_type.upper()} PARENTS:\\n")
                    f.write("-" * 40 + "\\n")
                    f.write(f"Samples: {metrics['n_samples']}\\n")
                    f.write(f"Training R² = {metrics['r2_train']:.4f}\\n")
                    if not np.isnan(metrics['r2_test']):
                        f.write(f"Test R² = {metrics['r2_test']:.4f}\\n")
                    f.write(f"Training RMSE = {metrics['rmse_train']:.4f}\\n")
                    f.write(f"Intercept = {model.intercept_:.4f}\\n\\n")
                    
                    f.write("Top predictive species:\\n")
                    for _, row in results_df.head(10).iterrows():
                        direction = "increases" if row['Coefficient'] > 0 else "decreases"
                        f.write(f"  {row['Species']}: {row['Coefficient']:.4f} (final pH {direction})\\n")
                    f.write("\\n")
        
        print(f"✓ Results saved to {output_dir}/")
        print("  - parent_to_final_pH_coefficients_by_medium.csv")
        print("  - parent_to_final_pH_summary.txt")

def main():
    """Main analysis function"""
    print("=" * 80)
    print("PARENT COMMUNITY → FINAL pH MULTIVARIATE REGRESSION")
    print("=" * 80)
    
    # Load and link data
    parent_communities, coalesced_communities, recipe = load_parent_and_coalescence_data()
    linked_df = link_parents_to_outcomes(parent_communities, coalesced_communities, recipe)
    
    if len(linked_df) == 0:
        print("❌ No linked parent-coalescence data found!")
        return
    
    # Run analysis for each medium using combined parent abundances
    media_types = ['H', 'L', 'M']
    all_results = []
    
    for medium in media_types:
        result = run_parent_regression_by_medium(linked_df, medium, 'Combined')
        all_results.append(result)
    
    # Save results
    save_parent_analysis_results(all_results)
    
    print(f"\\n🎉 PARENT → FINAL pH ANALYSIS COMPLETE!")
    print("✅ Shows how parent community species predict final coalesced pH")
    print("📊 Separate analysis by medium type (H/L/M)")
    
    return all_results, linked_df

if __name__ == "__main__":
    results, data = main()