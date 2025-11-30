"""
analyze_competitive_coefficients.py
Purpose: Analyzes the model coefficients from single unified predictability model
to identify ASVs with high competitive scores. Creates publication-ready heatmaps.
"""

from common_setup import *
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

def make_polynomial_features(X: np.ndarray, order: int) -> np.ndarray:
    if order < 1 or order > 2:
        raise ValueError("Only order=1 or order=2 are supported.")
    poly = PolynomialFeatures(degree=order, include_bias=True)
    return poly.fit_transform(X)

def sigmoid(s1,s2):
    diff=s1-s2
    ratio_pred=1.0/(1.0+np.exp(-diff))
    return ratio_pred * (np.pi/2)

def fit_definite_strength_poly(X1, X2, y, order=1, alpha=None, w_init=None):
    if alpha is None:
        alpha = [0.0] * (2 if order == 1 else 3)
    
    Z1 = make_polynomial_features(X1, order)
    Z2 = make_polynomial_features(X2, order)
    n_samples, n_poly_features = Z1.shape
    
    d = X1.shape[1]
    intercept_idx = [0]
    linear_idx = list(range(1, d+1))
    quadratic_idx = list(range(d+1, n_poly_features)) if order == 2 else []
    
    alpha0 = alpha[0]
    alpha1 = alpha[1] 
    alpha2 = alpha[2] if order == 2 else 0.0

    if w_init is None:
        w_init = np.zeros(n_poly_features)

    def objective(w):
        s1 = Z1.dot(w)
        s2 = Z2.dot(w)
        ratio_pred = sigmoid(s1,s2)
        residuals = y - ratio_pred
        sse = np.sum(residuals**2)

        reg_intercept = alpha0 * np.sum(np.abs(w[intercept_idx]))
        reg_linear = alpha1 * np.sum(np.abs(w[linear_idx]))
        reg_quad = alpha2 * sum(np.abs(w[q]) for q in quadratic_idx)
        
        return sse + reg_intercept + reg_linear + reg_quad

    result = minimize(objective, w_init, method='BFGS', options={'maxiter': 100000})
    return result.x

def get_data_for_species(species_num, medium):
    """Get predictability data for a specific species number and medium."""
    com_type = "S"
    rep = -1
    mode = "Casewise"
    
    if mode == "Casewise":
        X1_all = []
        X2_all = []
        y_all = []
        
        IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, rep)
        
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
        idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
        idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
        idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
        
        for i in range(len(idx)):
            c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
            c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
            c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
            c_1 = c_1*(c_1>1e-4)
            c_2 = c_2*(c_2>1e-4)
            
            u,v,k = metric_VectorDecomposition_onlyPositive(c_1,c_2,c_mix)
            
            eps = 1e-3
            y = np.arctan(np.array(np.abs(u)+eps)/np.array(np.abs(v)+eps))
            X1_all.append(c_1)
            X2_all.append(c_2)
            y_all.append(y)
        
        return np.array(X1_all), np.array(X2_all), np.array(y_all)

def get_asv_names():
    """Get ASV names from the processed sequences data."""
    # Get column names (ASV identifiers) excluding the first column (SampleIDX)
    asv_names = Processed_sequences_synthetic.columns[1:].tolist()
    return asv_names

def main():
    species_nums = [6, 12, 24]
    medium_list = ["L", "M", "H"]
    single_alpha = 0.05
    
    # Create output directory
    import os
    output_dir = "Figure/Predictability_single_model"
    os.makedirs(output_dir, exist_ok=True)
    
    # Dictionary to store coefficients for each medium
    all_coefficients = {}
    asv_names = get_asv_names()
    
    print("Analyzing model coefficients for competitive scores...")
    print(f"Number of ASVs: {len(asv_names)}")
    
    for medium in medium_list:
        print(f"\nAnalyzing medium {medium}...")
        
        # Collect all data from all species numbers
        X1_combined = []
        X2_combined = []
        y_combined = []
        
        for species_num in species_nums:
            try:
                X1_all, X2_all, y_all = get_data_for_species(species_num, medium)
                
                if len(y_all) == 0:
                    print(f"  No data for S{species_num}")
                    continue
                
                X1_combined.extend(X1_all)
                X2_combined.extend(X2_all)
                y_combined.extend(y_all)
                
                print(f"  S{species_num}: n={len(y_all)} samples")
                
            except Exception as e:
                print(f"  Error with S{species_num}: {str(e)[:80]}")
                continue
        
        # Convert to arrays
        X1_combined = np.array(X1_combined)
        X2_combined = np.array(X2_combined)
        y_combined = np.array(y_combined)
        
        print(f"  Total combined samples: {len(y_combined)}")
        
        # Fit SINGLE model on all combined data
        w_fit = fit_definite_strength_poly(
            X1_combined, X2_combined, y_combined,
            order=1,
            alpha=[0.1, single_alpha]
        )
        
        # Store coefficients (excluding intercept at index 0)
        linear_coefficients = w_fit[1:len(asv_names)+1]  # Linear terms for each ASV
        all_coefficients[medium] = linear_coefficients
        
        print(f"  Model fitted with {len(w_fit)} total coefficients")
        print(f"  Linear coefficients range: {linear_coefficients.min():.4f} to {linear_coefficients.max():.4f}")
        print(f"  Intercept w[0] = {w_fit[0]:.4f}")
        print(f"  First 10 ASV coefficients w[1:11]:")
        for i in range(10):
            asv_idx = i + 1
            coeff_val = w_fit[asv_idx] if asv_idx < len(w_fit) else 0
            asv_name = asv_names[i] if i < len(asv_names) else "Unknown"
            print(f"    {asv_name} -> ASV{asv_idx} (w[{asv_idx}]) = {coeff_val:.6f}")
        
        # Also show how the coefficients are stored
        print(f"  How coefficients are stored in all_coefficients[{medium}]:")
        stored_coeffs = w_fit[1:len(asv_names)+1]
        for i in range(min(5, len(stored_coeffs))):
            print(f"    all_coefficients[{medium}][{i}] = {stored_coeffs[i]:.6f} (for {asv_names[i]})")
        print()
    
    # Create coefficient matrix for heatmap
    coeff_matrix = np.array([all_coefficients[medium] for medium in medium_list])
    
    # Create DataFrame for easier manipulation
    coeff_df = pd.DataFrame(coeff_matrix.T, 
                           columns=[f'Medium {m}' for m in medium_list],
                           index=asv_names)
    
    # Sort by overall competitive score (mean absolute coefficient across media)
    coeff_df['Mean_Abs_Coeff'] = coeff_df.abs().mean(axis=1)
    coeff_df = coeff_df.sort_values('Mean_Abs_Coeff', ascending=False)
    
    # Use all ASVs but keep them in ORIGINAL ORDER, not ranked order
    # Create DataFrame in original ASV order (not sorted by competitive score)
    original_coeff_df = pd.DataFrame(coeff_matrix.T, 
                                   columns=[f'Medium {m}' for m in medium_list],
                                   index=asv_names)  # Keep original order
    
    # Remove the helper column for plotting (plot_data is now in original ASV order)
    plot_data = original_coeff_df.copy()
    
    print(f"\nTop 20 most competitive ASVs (by ranking):")
    for i, (asv, row) in enumerate(coeff_df.head(20).iterrows()):
        print(f"  {i+1:2d}. {asv}: Mean|coeff|={row['Mean_Abs_Coeff']:.4f}")
        print(f"      L={row['Medium L']:.6f}, M={row['Medium M']:.6f}, H={row['Medium H']:.6f}")
    
    # Debug: Check what happens to ASV4 specifically in ORIGINAL ORDER
    print(f"\nDEBUG - ASV4 (NormalizedAbundance4) details in ORIGINAL order:")
    asv4_row = original_coeff_df.loc['NormalizedAbundance4']
    print(f"  L coeff: {asv4_row['Medium L']:.6f}")  
    print(f"  M coeff: {asv4_row['Medium M']:.6f}")
    print(f"  H coeff: {asv4_row['Medium H']:.6f}")
    print(f"  Original position in heatmap: {list(original_coeff_df.index).index('NormalizedAbundance4') + 1}")
    print()
    
    # Create simplified ASV labels (1, 2, 3, ...)
    simplified_labels = [str(i+1) for i in range(len(original_coeff_df))]
    plot_data_simple = plot_data.copy()
    plot_data_simple.index = simplified_labels
    
    # Create single-row heatmaps showing only first 12 ASVs for each medium
    first_12_asvs = 12
    
    for medium in medium_list:
        plt.figure(figsize=(8, 1.2))  # Single row, wider format
        
        # Extract data for this medium only - first 12 ASVs
        medium_data_1d = plot_data_simple[f'Medium {medium}'].values[:first_12_asvs]
        
        # Reshape into single row
        medium_data_2d = medium_data_1d.reshape(1, first_12_asvs)
        
        # Use a diverging colormap to show positive/negative coefficients
        ax = sns.heatmap(medium_data_2d, 
                         cmap='RdBu_r', 
                         center=0,
                         annot=False,  # No text annotations
                         cbar=True,
                         cbar_kws={'shrink': 0.6, 'aspect': 10},
                         linewidths=0.05,
                         square=True)
        
        # Set x-tick labels for ASV numbers (1-12) and move to top
        ax.set_xticks(np.arange(first_12_asvs) + 0.5)
        ax.set_xticklabels([str(i+1) for i in range(first_12_asvs)], fontsize=14)
        ax.tick_params(axis='x', top=True, bottom=False, labeltop=True, labelbottom=False)
        
        # Remove y-tick labels (single row)
        ax.set_yticks([])
        ax.set_yticklabels([])
        
        # Remove all labels and titles
        plt.xlabel('')
        plt.ylabel('')
        plt.title('')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/Fig_competitive_coefficients_{medium}.svg", 
                    dpi=300, bbox_inches='tight')
        plt.close()
    
    # Create full version heatmaps showing first 40 ASVs (4 rows of 10 each)
    first_40_asvs = 40
    rows = 4
    cols = 10
    
    for medium in medium_list:
        plt.figure(figsize=(10, 4))  # 4 rows format
        
        # Extract data for this medium only - first 40 ASVs
        medium_data_1d = plot_data_simple[f'Medium {medium}'].values[:first_40_asvs]
        
        # Reshape into 4 rows of 10 columns
        medium_data_2d = medium_data_1d.reshape(rows, cols)
        
        # Use a diverging colormap to show positive/negative coefficients
        ax = sns.heatmap(medium_data_2d, 
                         cmap='RdBu_r', 
                         center=0,
                         annot=False,  # No text annotations
                         cbar=True,
                         cbar_kws={'shrink': 0.6, 'aspect': 20},
                         linewidths=0.05,
                         square=True)
        
        # Set x-tick labels for ASV numbers (1-10 for each row)
        ax.set_xticks(np.arange(cols) + 0.5)
        ax.set_xticklabels([str(i+1) for i in range(cols)], fontsize=8)
        
        # Set y-tick labels for row numbers (1-10, 11-20, 21-30, 31-40)
        ax.set_yticks(np.arange(rows) + 0.5)
        row_labels = [f'{i*10+1}-{(i+1)*10}' for i in range(rows)]
        ax.set_yticklabels(row_labels, fontsize=8)
        
        # Remove all labels and titles
        plt.xlabel('')
        plt.ylabel('')
        plt.title('')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/Fig_competitive_coefficients_{medium}_full.svg", 
                    dpi=300, bbox_inches='tight')
        plt.close()
    
    # Save coefficient data to CSV for further analysis
    coeff_df.to_csv(f"{output_dir}/competitive_coefficients_data.csv")
    
    # Create summary statistics
    summary_stats = {
        'Total_ASVs': len(asv_names),
        'All_ASVs_shown': len(original_coeff_df),
        'Model_alpha': single_alpha,
        'Media_analyzed': medium_list
    }
    
    print(f"\nSummary:")
    print(f"  Created heatmaps showing all {len(original_coeff_df)} ASVs IN ORIGINAL ORDER")
    print(f"  Coefficients saved to: {output_dir}/competitive_coefficients_data.csv")
    print(f"  Heatmap plots saved to: {output_dir}/Fig_competitive_coefficients_*.svg")
    
    return original_coeff_df, summary_stats

if __name__ == "__main__":
    main()