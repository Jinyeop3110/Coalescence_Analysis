"""
Plot_predictability_single_model.py
Purpose: Fits a SINGLE predictive model using combined data from S6, S12, and S24
instead of separate models for each species number
"""

from common_setup import *
import matplotlib
matplotlib.use('Agg')
import numpy as np
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import ShuffleSplit
from typing import Tuple, List
from scipy import stats

def make_polynomial_features(X: np.ndarray, order: int) -> np.ndarray:
    if order < 1 or order > 2:
        raise ValueError("Only order=1 or order=2 are supported.")
    poly = PolynomialFeatures(degree=order, include_bias=True)
    return poly.fit_transform(X)

def sigmoid(s1,s2):
    diff=s1-s2
    # Return raw sigmoid output scaled to [0, pi/2]
    ratio_pred=1.0/(1.0+np.exp(-diff))
    return ratio_pred * (np.pi/2)

def inv_sigmoid(ratio_pred):
    # Convert from [0, pi/2] back to original scale
    norm_pred = ratio_pred / (np.pi/2)
    return np.log(norm_pred / (1 - norm_pred))

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

def predict_ratio_poly(w, X1, X2, order):
    Z1 = make_polynomial_features(X1, order)
    Z2 = make_polynomial_features(X2, order)
    s1 = Z1.dot(w)
    s2 = Z2.dot(w)
    return sigmoid(s1,s2)

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

def main():
    species_nums = [6, 12, 24]
    medium_list = ["L", "M", "H"]
    
    # Colors for different media (same as individual plots)
    medium_colors = {'L': '#A7216A', 'M': '#802000', 'H': '#E24912'}
    
    # Single alpha value for the unified model (you may need to tune this)
    single_alpha = 0.05
    
    # Create output directory
    import os
    output_dir = "Figure/Predictability_single_model"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create plots for each medium with single model
    for medium in medium_list:
        print(f"Creating single model plot for medium {medium}...")
        
        # Collect all data from all species numbers
        X1_combined = []
        X2_combined = []
        y_combined = []
        species_labels = []
        
        for species_num in species_nums:
            try:
                # Get data for this species/medium combination
                X1_all, X2_all, y_all = get_data_for_species(species_num, medium)
                
                if len(y_all) == 0:
                    print(f"  No data for S{species_num}")
                    continue
                
                X1_combined.extend(X1_all)
                X2_combined.extend(X2_all)
                y_combined.extend(y_all)
                species_labels.extend([species_num] * len(y_all))
                
                print(f"  S{species_num}: n={len(y_all)} samples")
                
            except Exception as e:
                print(f"  Error with S{species_num}: {str(e)[:80]}")
                continue
        
        # Convert to arrays
        X1_combined = np.array(X1_combined)
        X2_combined = np.array(X2_combined)
        y_combined = np.array(y_combined)
        species_labels = np.array(species_labels)
        
        print(f"  Total combined samples: {len(y_combined)}")
        
        # Fit SINGLE model on all combined data
        X1_train = X1_combined
        X2_train = X2_combined
        y_train = y_combined
        
        w_fit = fit_definite_strength_poly(
            X1_train, X2_train, y_train,
            order=1,
            alpha=[0.1, single_alpha]
        )
        
        # Predict using the single model
        y_pred_combined = predict_ratio_poly(w_fit, X1_combined, X2_combined, order=1)
        
        # Calculate overall MSE and R²
        mse_overall = np.mean((y_combined - y_pred_combined)**2)
        ss_res = np.sum((y_combined - y_pred_combined)**2)  # Sum of squares of residuals
        ss_tot = np.sum((y_combined - np.mean(y_combined))**2)  # Total sum of squares
        r2_overall = 1 - (ss_res / ss_tot)
        print(f"  Overall MSE: {mse_overall:.4f}, R²: {r2_overall:.4f}")
        
        # Create plot
        fig, ax = plt.subplots(figsize=(3, 2.5))
        
        # Plot all points with same color
        ax.scatter(y_combined, y_pred_combined, 
                  alpha=0.5, 
                  color=medium_colors[medium], 
                  s=7)
        
        # Draw reference line and regression line
        min_val = min(y_combined.min(), y_pred_combined.min())
        max_val = max(y_combined.max(), y_pred_combined.max())
        
        # Perfect prediction line
        ax.plot([min_val, max_val], [min_val, max_val], 
                color='grey', linestyle='--', linewidth=0.5)
        
        # Regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(y_combined, y_pred_combined)
        x_line = np.array([min_val, max_val])
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color=medium_colors[medium], linewidth=1.5, linestyle='-')
        
        # Add R² text
        ax.text(0.05, 0.95, f"R² = {r2_overall:.3f}", 
                transform=ax.transAxes, fontsize=10, 
                verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5))
        
        # Remove axis labels
        ax.set_xlabel("")
        ax.set_ylabel("")
        # Remove title
        ax.set_title("")
        ax.grid(True, alpha=0.3)
        
        # Set tick locations and labels for pi values
        pi_ticks = [0, np.pi/4, np.pi/2]
        pi_labels = ['0', 'π/4', 'π/2']
        ax.set_xticks(pi_ticks)
        ax.set_xticklabels(pi_labels)
        ax.set_yticks(pi_ticks)
        ax.set_yticklabels(pi_labels)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/Fig_predictability_single_model_{medium}.svg", 
                   dpi=100, bbox_inches='tight')
        plt.close()
        
        # Also create species-colored version to see the breakdown
        fig, ax = plt.subplots(figsize=(3, 2.5))
        
        # Plot with different colors for each species
        colors_species = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        for i, species_num in enumerate(species_nums):
            mask = species_labels == species_num
            if np.any(mask):
                ax.scatter(y_combined[mask], y_pred_combined[mask], 
                          alpha=0.5, 
                          color=colors_species[i], 
                          s=7,
                          label=f'S{species_num}')
        
        # Reference and regression lines
        ax.plot([min_val, max_val], [min_val, max_val], 
                color='grey', linestyle='--', linewidth=0.5)
        ax.plot(x_line, y_line, color='black', linewidth=1.5, linestyle='-')
        
        ax.text(0.05, 0.95, f"R² = {r2_overall:.3f}", 
                transform=ax.transAxes, fontsize=10, 
                verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5))
        
        # Remove axis labels
        ax.set_xlabel("")
        ax.set_ylabel("")
        # Remove title
        ax.set_title("")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
        
        # Set tick locations and labels for pi values
        ax.set_xticks(pi_ticks)
        ax.set_xticklabels(pi_labels)
        ax.set_yticks(pi_ticks)
        ax.set_yticklabels(pi_labels)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/Fig_predictability_single_model_{medium}_species_colored.svg", 
                   dpi=100, bbox_inches='tight')
        plt.close()
    
    # Create overall plot (all media together)
    print("\nCreating overall single model plot...")
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.5))
    
    for med_idx, medium in enumerate(medium_list):
        ax = axes[med_idx]
        
        # Collect all data
        X1_combined = []
        X2_combined = []
        y_combined = []
        
        for species_num in species_nums:
            try:
                X1_all, X2_all, y_all = get_data_for_species(species_num, medium)
                
                if len(y_all) == 0:
                    continue
                
                X1_combined.extend(X1_all)
                X2_combined.extend(X2_all)
                y_combined.extend(y_all)
                          
            except:
                continue
        
        # Convert to arrays
        X1_combined = np.array(X1_combined)
        X2_combined = np.array(X2_combined)
        y_combined = np.array(y_combined)
        
        # Fit single model
        w_fit = fit_definite_strength_poly(
            X1_combined, X2_combined, y_combined,
            order=1, alpha=[0.1, single_alpha]
        )
        
        y_pred_combined = predict_ratio_poly(w_fit, X1_combined, X2_combined, order=1)
        
        # Calculate R² for this medium
        ss_res = np.sum((y_combined - y_pred_combined)**2)
        ss_tot = np.sum((y_combined - np.mean(y_combined))**2)
        r2_med = 1 - (ss_res / ss_tot)
        
        # Plot
        ax.scatter(y_combined, y_pred_combined, 
                  alpha=0.5, 
                  color=medium_colors[medium], 
                  s=7)
        
        # Reference and regression lines
        min_val = min(y_combined.min(), y_pred_combined.min())
        max_val = max(y_combined.max(), y_pred_combined.max())
        
        ax.plot([min_val, max_val], [min_val, max_val], 
                color='grey', linestyle='--', linewidth=0.5)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(y_combined, y_pred_combined)
        x_line = np.array([min_val, max_val])
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color=medium_colors[medium], linewidth=1.5, linestyle='-')
        
        # Add R² text
        ax.text(0.05, 0.95, f"R² = {r2_med:.3f}", 
                transform=ax.transAxes, fontsize=10, 
                verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5))
        
        # Remove axis labels
        ax.set_xlabel("")
        ax.set_ylabel("")
        # Remove title
        ax.set_title("")
        ax.grid(True, alpha=0.3)
        
        # Set tick locations and labels for pi values
        pi_ticks = [0, np.pi/4, np.pi/2]
        pi_labels = ['0', 'π/4', 'π/2']
        ax.set_xticks(pi_ticks)
        ax.set_xticklabels(pi_labels)
        ax.set_yticks(pi_ticks)
        ax.set_yticklabels(pi_labels)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Fig_predictability_single_model_all.svg", 
               dpi=100, bbox_inches='tight')
    plt.close()
    
    print("Single model plots created successfully!")

if __name__ == "__main__":
    main()