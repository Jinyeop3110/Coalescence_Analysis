"""
plot_predictability_community_averaged_single_model.py
Purpose: Community-averaged predictability plots using SINGLE unified model 
(like single_model approach but with community averaging like community_averaged)
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
from collections import defaultdict

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

def get_data_with_community_info(species_num, medium):
    """Get predictability data with community information for averaging."""
    com_type = "S"
    rep = -1
    mode = "Casewise"
    
    if mode == "Casewise":
        X1_all = []
        X2_all = []
        y_all = []
        community_idx_all = []
        sub1_idx_all = []
        sub2_idx_all = []
        
        IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, rep)
        
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
        sub1_idx_all = idx_1.copy()
        idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
        sub2_idx_all = idx_2.copy()
        idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
        idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
        
        # Get community indices
        community_idx_all = Coalescence_data.iloc[np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])]["CommunityIDX"].tolist()
        
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
        
        return np.array(X1_all), np.array(X2_all), np.array(y_all), sub1_idx_all, sub2_idx_all, community_idx_all

def main():
    species_nums = [6, 12, 24]
    medium_list = ["L", "M", "H"]
    
    # Colors for different media (same as individual plots)
    medium_colors = {'L': '#A7216A', 'M': '#802000', 'H': '#E24912'}
    
    # Single alpha value for the unified model
    single_alpha = 0.05
    
    # Use existing single model directory
    import os
    output_dir = "Figure/Predictability_single_model"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create community-averaged plots using single model for each medium
    for medium in medium_list:
        print(f"Creating community-averaged single model plot for medium {medium}...")
        
        # Collect all data from all species numbers for SINGLE model training
        X1_combined = []
        X2_combined = []
        y_combined = []
        
        # Dictionary to store community-averaged values
        community_true_values = defaultdict(list)
        community_pred_values = defaultdict(list)
        community_X1_values = defaultdict(list)
        community_X2_values = defaultdict(list)
        
        # First pass: collect all training data
        for species_num in species_nums:
            try:
                X1_all, X2_all, y_all, sub1_idx, sub2_idx, community_idx = get_data_with_community_info(species_num, medium)
                
                if len(y_all) == 0:
                    print(f"  No data for S{species_num}")
                    continue
                
                X1_combined.extend(X1_all)
                X2_combined.extend(X2_all)
                y_combined.extend(y_all)
                
                print(f"  S{species_num}: n={len(y_all)} coalescence events")
                
            except Exception as e:
                print(f"  Error with S{species_num}: {str(e)[:80]}")
                continue
        
        # Convert to arrays and train SINGLE model
        X1_combined = np.array(X1_combined)
        X2_combined = np.array(X2_combined)
        y_combined = np.array(y_combined)
        
        print(f"  Training single model on {len(y_combined)} total events...")
        
        w_fit = fit_definite_strength_poly(
            X1_combined, X2_combined, y_combined,
            order=1,
            alpha=[0.1, single_alpha]
        )
        
        # Second pass: predict and group by communities  
        for species_num in species_nums:
            try:
                X1_all, X2_all, y_all, sub1_idx, sub2_idx, community_idx = get_data_with_community_info(species_num, medium)
                
                if len(y_all) == 0:
                    continue
                
                # Predict using the SINGLE unified model
                y_pred = predict_ratio_poly(w_fit, X1_all, X2_all, order=1)
                
                # Group by sub-communities
                for i in range(len(y_all)):
                    # Use sub-community indices as keys
                    comm_key1 = f"{sub1_idx[i]}_{species_num}"
                    comm_key2 = f"{sub2_idx[i]}_{species_num}"
                    
                    # Store values for each sub-community
                    community_true_values[comm_key1].append(y_all[i])
                    community_pred_values[comm_key1].append(y_pred[i])
                    community_true_values[comm_key2].append(y_all[i])
                    community_pred_values[comm_key2].append(y_pred[i])
                
            except Exception as e:
                print(f"  Error with S{species_num}: {str(e)[:80]}")
                continue
        
        # Calculate community means
        comm_mean_true = []
        comm_mean_pred = []
        
        for comm_key in community_true_values:
            if comm_key in community_pred_values:
                mean_true = np.mean(community_true_values[comm_key])
                mean_pred = np.mean(community_pred_values[comm_key])
                comm_mean_true.append(mean_true)
                comm_mean_pred.append(mean_pred)
        
        comm_mean_true = np.array(comm_mean_true)
        comm_mean_pred = np.array(comm_mean_pred)
        
        # Calculate R² for community-averaged values
        ss_res = np.sum((comm_mean_true - comm_mean_pred)**2)
        ss_tot = np.sum((comm_mean_true - np.mean(comm_mean_true))**2)
        r2_community = 1 - (ss_res / ss_tot)
        
        print(f"  Community-averaged R²: {r2_community:.4f}")
        print(f"  Number of communities: {len(comm_mean_true)}")
        
        # Create plot
        fig, ax = plt.subplots(figsize=(2.3, 2.2))
        
        # Map values from [0, π/2] to [0, 1]
        # Original range is [0, π/2], we want to map to [0, 1]
        comm_mean_true_mapped = comm_mean_true / (np.pi/2)
        comm_mean_pred_mapped = comm_mean_pred / (np.pi/2)
        
        # Plot community-averaged points (predicted on x, true on y)
        ax.scatter(comm_mean_pred_mapped, comm_mean_true_mapped, 
                  alpha=0.7, 
                  color=medium_colors[medium], 
                  s=12)  # Slightly larger since fewer points
        
        # Draw reference line and regression line
        min_val = min(comm_mean_true_mapped.min(), comm_mean_pred_mapped.min())
        max_val = max(comm_mean_true_mapped.max(), comm_mean_pred_mapped.max())
        
        # Perfect prediction line extending to full range
        ax.plot([-0.02, 1.02], [-0.02, 1.02], 
                color='grey', linestyle='--', linewidth=0.5)
        
        # Regression line (x=predicted, y=true)
        slope, intercept, r_value, p_value, std_err = stats.linregress(comm_mean_pred_mapped, comm_mean_true_mapped)
        print(f"  Regression for medium {medium}: slope={slope:.3f}, intercept={intercept:.3f}")
        print(f"  Data range: pred=[{comm_mean_pred_mapped.min():.3f}, {comm_mean_pred_mapped.max():.3f}], true=[{comm_mean_true_mapped.min():.3f}, {comm_mean_true_mapped.max():.3f}]")
        print(f"  Range ratio (true/pred): {(comm_mean_true_mapped.max()-comm_mean_true_mapped.min())/(comm_mean_pred_mapped.max()-comm_mean_pred_mapped.min()):.3f}")
        
        # Double-check correlation
        corr = np.corrcoef(comm_mean_pred_mapped, comm_mean_true_mapped)[0,1]
        print(f"  Correlation: {corr:.3f}, R²={corr**2:.3f}")
        
        # Also calculate regression the other way for comparison
        slope_rev, intercept_rev, r_value_rev, p_value_rev, std_err_rev = stats.linregress(comm_mean_true_mapped, comm_mean_pred_mapped)
        print(f"  Reverse regression (true->pred): slope={slope_rev:.3f}, intercept={intercept_rev:.3f}")
        
        # Draw regression line using true->pred regression but on swapped axes
        # true->pred gives: pred = slope_rev * true + intercept_rev
        # Solving for true: true = (pred - intercept_rev) / slope_rev
        x_line = np.array([-0.02, 1.02])
        y_line = (x_line - intercept_rev) / slope_rev
        ax.plot(x_line, y_line, color=medium_colors[medium], linewidth=1.5, linestyle='-')
        
        # Add R² text (use r_value from true->pred regression which matches the plotted line)
        ax.text(0.05, 0.95, f"R² = {r_value_rev**2:.3f}", 
                transform=ax.transAxes, fontsize=10, 
                verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5))
        
        # Remove axis labels and titles
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title("")
        ax.grid(True, alpha=0.3)
        
        # Set tick locations and labels for [0, 1] range
        ticks = [0, 0.25, 0.5, 0.75, 1.0]
        labels = ['0', '0.25', '0.5', '0.75', '1']
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels, fontsize=8)
        
        # Set axis limits to [-0.02, 1.02] for padding
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/Fig_predictability_community_averaged_single_model_{medium}.svg", 
                   dpi=100, bbox_inches='tight')
        plt.close()
    
    print("Community-averaged single model plots created successfully!")

if __name__ == "__main__":
    main()