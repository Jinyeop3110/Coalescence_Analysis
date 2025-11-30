#!/usr/bin/env python3
"""
Multivariate Regression Analysis: Species Abundances vs pH
Uses first 10 species abundances as predictors for pH
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
    return merged_data

def prepare_regression_data(merged_data):
    """Prepare data for multivariate regression"""
    print("Preparing regression data...")
    
    # Get first 10 species abundance columns
    abundance_columns = [col for col in merged_data.columns if col.startswith('NormalizedAbundance')][:10]
    print(f"Using first 10 species: {abundance_columns}")
    
    # Prepare feature matrix (X) and target variable (y)
    X = merged_data[abundance_columns].copy()
    y = merged_data['fieldPH7'].copy()
    
    # Remove samples with missing pH data
    valid_mask = ~y.isna()
    X = X[valid_mask]
    y = y[valid_mask]
    
    # Fill any missing abundance values with 0
    X = X.fillna(0)
    
    print(f"✓ Final dataset: {len(X)} samples, {X.shape[1]} species features")
    print(f"✓ pH range: {y.min():.2f} - {y.max():.2f}")
    
    return X, y, abundance_columns

def perform_multivariate_regression(X, y, species_names):
    """Perform multivariate linear regression"""
    print("\nPerforming multivariate regression...")
    
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
    
    print(f"✓ Training R² = {r2_train:.4f}")
    print(f"✓ Test R² = {r2_test:.4f}")
    print(f"✓ Training RMSE = {rmse_train:.4f}")
    print(f"✓ Test RMSE = {rmse_test:.4f}")
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'Species': species_names,
        'Coefficient': model.coef_,
        'Abs_Coefficient': np.abs(model.coef_)
    })
    
    # Sort by absolute coefficient value
    results_df = results_df.sort_values('Abs_Coefficient', ascending=False)
    
    print(f"\n📊 MULTIVARIATE REGRESSION RESULTS:")
    print(f"Intercept: {model.intercept_:.4f}")
    print(f"Most important species (by |coefficient|):")
    for i, (_, row) in enumerate(results_df.head(5).iterrows(), 1):
        direction = "increases" if row['Coefficient'] > 0 else "decreases"
        print(f"  {i}. {row['Species']}: {row['Coefficient']:.4f} (pH {direction})")
    
    return model, results_df, r2_train, r2_test, rmse_train, rmse_test

def save_results(model, results_df, r2_train, r2_test, rmse_train, rmse_test, X, y):
    """Save multivariate regression results"""
    print("\nSaving results...")
    
    # Create output directory
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save coefficient results
    results_df.to_csv(f'{output_dir}/multivariate_species_ph_coefficients.csv', index=False)
    
    # Save model summary
    with open(f'{output_dir}/multivariate_regression_summary.txt', 'w') as f:
        f.write("MULTIVARIATE SPECIES-pH REGRESSION SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("MODEL PERFORMANCE:\n")
        f.write(f"Training R² = {r2_train:.4f}\n")
        f.write(f"Test R² = {r2_test:.4f}\n")
        f.write(f"Training RMSE = {rmse_train:.4f}\n")
        f.write(f"Test RMSE = {rmse_test:.4f}\n\n")
        
        f.write(f"Intercept: {model.intercept_:.4f}\n\n")
        
        f.write("SPECIES COEFFICIENTS (sorted by importance):\n")
        f.write("-" * 40 + "\n")
        for _, row in results_df.iterrows():
            direction = "increases" if row['Coefficient'] > 0 else "decreases"
            f.write(f"{row['Species']}: {row['Coefficient']:.4f} (pH {direction})\n")
        
        f.write(f"\nSample size: {len(X)} samples\n")
        f.write(f"Number of predictors: {X.shape[1]} species\n")
        f.write(f"pH range: {y.min():.2f} - {y.max():.2f}\n")
    
    print(f"✓ Results saved to {output_dir}/")
    print("  - multivariate_species_ph_coefficients.csv")
    print("  - multivariate_regression_summary.txt")

def main():
    """Main analysis function"""
    print("=" * 60)
    print("MULTIVARIATE SPECIES-pH REGRESSION ANALYSIS")
    print("=" * 60)
    
    # Load data
    merged_data = load_data()
    
    # Prepare regression data
    X, y, species_names = prepare_regression_data(merged_data)
    
    # Perform multivariate regression
    model, results_df, r2_train, r2_test, rmse_train, rmse_test = perform_multivariate_regression(X, y, species_names)
    
    # Save results
    save_results(model, results_df, r2_train, r2_test, rmse_train, rmse_test, X, y)
    
    print("\n🎉 MULTIVARIATE REGRESSION COMPLETE!")
    print("✅ Model considers all 10 species simultaneously")
    print("📊 Results show which species most strongly predict pH")
    
    return model, results_df

if __name__ == "__main__":
    model, results = main()