#!/usr/bin/env python3
"""
Multivariate Regression Analysis: Species Abundances vs pH
Separate analysis for each medium type (H, L, M)
"""

import numpy as np
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load species abundance and pH data with medium information"""
    print("Loading data with medium information...")
    
    # Species abundance data
    abundance_synthetic = pd.read_excel("../../Postprocessed/processed_Sequences_synthetic.xlsx")
    abundance_natural = pd.read_excel("../../Postprocessed/processed_Sequences_natural.xlsx")
    abundance_data = pd.concat([abundance_synthetic, abundance_natural], ignore_index=True)
    
    # Community pH data with medium information
    communities_synthetic = pd.read_excel("../../Analyzed/processed_Communities_synthetic.xlsx")
    communities_natural = pd.read_excel("../../Analyzed/processed_Communities_natural.xlsx")
    communities_data = pd.concat([communities_synthetic, communities_natural])
    
    # Merge data including medium
    merged_data = abundance_data.merge(
        communities_data[['SampleIDX', 'Medium', 'fieldPH1', 'fieldPH7']], 
        on='SampleIDX', 
        how='inner'
    )
    
    print(f"✓ Loaded {len(merged_data)} samples with abundance, pH, and medium data")
    return merged_data

def run_regression_by_medium(merged_data, medium_type):
    """Run multivariate regression for specific medium type"""
    print(f"\n{'='*20} MEDIUM {medium_type} ANALYSIS {'='*20}")
    
    # Filter data for this medium
    medium_data = merged_data[merged_data['Medium'] == medium_type].copy()
    print(f"Samples for medium {medium_type}: {len(medium_data)}")
    
    # Get first 10 species abundance columns
    abundance_columns = [col for col in medium_data.columns if col.startswith('NormalizedAbundance')][:10]
    
    # Prepare feature matrix (X) and target variable (y)
    X = medium_data[abundance_columns].copy()
    y = medium_data['fieldPH7'].copy()
    
    # Remove samples with missing pH data
    valid_mask = ~y.isna()
    X = X[valid_mask]
    y = y[valid_mask]
    
    # Fill any missing abundance values with 0
    X = X.fillna(0)
    
    print(f"✓ Final dataset: {len(X)} samples, pH range: {y.min():.2f} - {y.max():.2f}")
    
    if len(X) < 20:
        print(f"⚠️  WARNING: Only {len(X)} samples for medium {medium_type}. Results may be unreliable.")
        return None
    
    # Split data for validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Fit multivariate regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Calculate metrics
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    print(f"📊 RESULTS FOR MEDIUM {medium_type}:")
    print(f"   Training R² = {r2_train:.4f}")
    print(f"   Test R² = {r2_test:.4f}")
    print(f"   Training RMSE = {rmse_train:.4f}")
    print(f"   Test RMSE = {rmse_test:.4f}")
    print(f"   Intercept = {model.intercept_:.4f}")
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'Species': abundance_columns,
        'Coefficient': model.coef_,
        'Abs_Coefficient': np.abs(model.coef_),
        'Medium': medium_type
    })
    
    # Sort by absolute coefficient value
    results_df = results_df.sort_values('Abs_Coefficient', ascending=False)
    
    print(f"   Top 5 most important species:")
    for i, (_, row) in enumerate(results_df.head(5).iterrows(), 1):
        direction = "increases" if row['Coefficient'] > 0 else "decreases"
        print(f"     {i}. {row['Species']}: {row['Coefficient']:.4f} (pH {direction})")
    
    return {
        'medium': medium_type,
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

def save_results_by_medium(all_results):
    """Save results for all medium types"""
    print(f"\n{'='*20} SAVING RESULTS {'='*20}")
    
    # Create output directory
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    # Combine all coefficient results
    all_coefficients = []
    for result in all_results:
        if result:
            all_coefficients.append(result['results_df'])
    
    combined_coefficients = pd.concat(all_coefficients, ignore_index=True)
    combined_coefficients.to_csv(f'{output_dir}/multivariate_coefficients_by_medium.csv', index=False)
    
    # Save comprehensive summary
    with open(f'{output_dir}/multivariate_by_medium_summary.txt', 'w') as f:
        f.write("MULTIVARIATE SPECIES-pH REGRESSION BY MEDIUM\n")
        f.write("=" * 60 + "\n\n")
        
        for result in all_results:
            if result:
                medium = result['medium']
                metrics = result['metrics']
                results_df = result['results_df']
                model = result['model']
                
                f.write(f"MEDIUM {medium} RESULTS:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Samples: {metrics['n_samples']}\n")
                f.write(f"Training R² = {metrics['r2_train']:.4f}\n")
                f.write(f"Test R² = {metrics['r2_test']:.4f}\n")
                f.write(f"Training RMSE = {metrics['rmse_train']:.4f}\n")
                f.write(f"Test RMSE = {metrics['rmse_test']:.4f}\n")
                f.write(f"Intercept = {model.intercept_:.4f}\n\n")
                
                f.write("Species Coefficients (top 10):\n")
                for _, row in results_df.head(10).iterrows():
                    direction = "increases" if row['Coefficient'] > 0 else "decreases"
                    f.write(f"  {row['Species']}: {row['Coefficient']:.4f} (pH {direction})\n")
                f.write("\n")
    
    # Save individual medium files
    for result in all_results:
        if result:
            medium = result['medium']
            result['results_df'].to_csv(f'{output_dir}/medium_{medium}_coefficients.csv', index=False)
    
    print(f"✓ Results saved to {output_dir}/")
    print("  - multivariate_coefficients_by_medium.csv (combined)")
    print("  - multivariate_by_medium_summary.txt")
    for result in all_results:
        if result:
            print(f"  - medium_{result['medium']}_coefficients.csv")

def compare_media_effects(all_results):
    """Compare effects across different media"""
    print(f"\n{'='*20} CROSS-MEDIUM COMPARISON {'='*20}")
    
    # Create comparison table for top species
    comparison_data = []
    
    # Get species that appear in top 5 for any medium
    top_species = set()
    for result in all_results:
        if result:
            top_species.update(result['results_df'].head(5)['Species'].tolist())
    
    for species in sorted(top_species):
        species_data = {'Species': species}
        for result in all_results:
            if result:
                medium = result['medium']
                species_row = result['results_df'][result['results_df']['Species'] == species]
                if not species_row.empty:
                    coef = species_row.iloc[0]['Coefficient']
                    species_data[f'Medium_{medium}'] = coef
                else:
                    species_data[f'Medium_{medium}'] = 0.0
        comparison_data.append(species_data)
    
    comparison_df = pd.DataFrame(comparison_data)
    
    print("Top species coefficient comparison across media:")
    print(comparison_df.to_string(index=False, float_format='%.3f'))
    
    # Save comparison
    output_dir = "Figure/pH_Analysis"
    comparison_df.to_csv(f'{output_dir}/medium_comparison_top_species.csv', index=False)

def main():
    """Main analysis function"""
    print("=" * 80)
    print("MULTIVARIATE SPECIES-pH REGRESSION BY MEDIUM TYPE")
    print("=" * 80)
    
    # Load data
    merged_data = load_data()
    
    # Run regression for each medium type
    media_types = ['H', 'L', 'M']
    all_results = []
    
    for medium in media_types:
        result = run_regression_by_medium(merged_data, medium)
        all_results.append(result)
    
    # Save results
    save_results_by_medium(all_results)
    
    # Compare across media
    compare_media_effects(all_results)
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print("✅ Separate multivariate regressions run for each medium type")
    print("📊 Results show how species effects vary by medium")
    
    return all_results

if __name__ == "__main__":
    results = main()