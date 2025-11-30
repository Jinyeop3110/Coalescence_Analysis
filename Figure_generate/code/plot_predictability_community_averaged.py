"""
Plot_predictability_community_averaged.py
Purpose: Creates community-averaged predictability plots where each point represents 
the mean dominance value for a specific sub-community
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

def get_data_with_community_info(species_num, medium):
    """Get predictability data along with community information."""
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
    
    # Pre-defined optimal alphas for each species/medium combination
    optimal_alphas = {
        6: {"L": 0.05, "M": 0.08, "H": 0.05},
        12: {"L": 0.01, "M": 0.1, "H": 0.063095},
        24: {"L": 0.03, "M": 0.05, "H": 0.04}
    }
    
    # Create community-averaged plots for each medium
    for medium in medium_list:
        print(f"Creating community-averaged plot for medium {medium}...")
        
        fig, ax = plt.subplots(figsize=(3, 2.5))
        
        # Dictionary to store community-averaged values
        community_true_values = defaultdict(list)
        community_pred_values = defaultdict(list)
        
        for species_idx, species_num in enumerate(species_nums):
            try:
                # Get data with community information
                X1_all, X2_all, y_all, sub1_idx, sub2_idx, community_idx = get_data_with_community_info(species_num, medium)
                
                if len(y_all) == 0:
                    print(f"  No data for S{species_num}")
                    continue
                
                # Fit model (no duplication for [0, pi/2] range)
                X1_train = X1_all
                X2_train = X2_all
                y_train = y_all
                
                alpha = optimal_alphas[species_num][medium]
                
                w_fit = fit_definite_strength_poly(
                    X1_train, X2_train, y_train,
                    order=1,
                    alpha=[0.1, alpha]
                )
                
                # Predict
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
                
                print(f"  S{species_num}: n={len(y_all)} coalescence events")
                
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
        
        # Plot community-averaged values
        ax.scatter(comm_mean_true, comm_mean_pred, 
                  alpha=0.5, 
                  color=medium_colors[medium], 
                  s=7)
        
        # Draw reference line and regression line
        if len(comm_mean_true) > 0:
            min_val = min(comm_mean_true.min(), comm_mean_pred.min())
            max_val = max(comm_mean_true.max(), comm_mean_pred.max())
            
            # Perfect prediction line
            ax.plot([min_val, max_val], [min_val, max_val], 
                    color='grey', linestyle='--', linewidth=0.5)
            
            # Regression line
            slope, intercept, r_value, p_value, std_err = stats.linregress(comm_mean_true, comm_mean_pred)
            x_line = np.array([min_val, max_val])
            y_line = slope * x_line + intercept
            ax.plot(x_line, y_line, color=medium_colors[medium], linewidth=1.5, linestyle='-')
            
            # Calculate MSE
            mse = np.mean((comm_mean_true - comm_mean_pred)**2)
            ax.text(0.05, 0.95, f"Test MSE = {mse:.4f}", 
                    transform=ax.transAxes, fontsize=10, 
                    verticalalignment='top',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5))
        
        # Remove axis labels and title
        ax.set_xlabel("")
        ax.set_ylabel("")
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
        plt.savefig(f"Figure/Predictability/Fig_predictability_community_averaged_{medium}.svg", 
                   dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"  Created plot with {len(comm_mean_true)} community averages")
    
    # Create overall community-averaged plot (all media together)
    print("\nCreating overall community-averaged plot...")
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.5))
    
    for med_idx, medium in enumerate(medium_list):
        ax = axes[med_idx]
        
        community_true_values = defaultdict(list)
        community_pred_values = defaultdict(list)
        
        for species_idx, species_num in enumerate(species_nums):
            try:
                X1_all, X2_all, y_all, sub1_idx, sub2_idx, community_idx = get_data_with_community_info(species_num, medium)
                
                if len(y_all) == 0:
                    continue
                
                X1_train = X1_all
                X2_train = X2_all
                y_train = y_all
                
                alpha = optimal_alphas[species_num][medium]
                
                w_fit = fit_definite_strength_poly(
                    X1_train, X2_train, y_train,
                    order=1, alpha=[0.1, alpha]
                )
                
                y_pred = predict_ratio_poly(w_fit, X1_all, X2_all, order=1)
                
                # Group by sub-communities
                for i in range(len(y_all)):
                    comm_key1 = f"{sub1_idx[i]}_{species_num}"
                    comm_key2 = f"{sub2_idx[i]}_{species_num}"
                    
                    community_true_values[comm_key1].append(y_all[i])
                    community_pred_values[comm_key1].append(y_pred[i])
                    community_true_values[comm_key2].append(y_all[i])
                    community_pred_values[comm_key2].append(y_pred[i])
                          
            except:
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
        
        # Plot
        ax.scatter(comm_mean_true, comm_mean_pred, 
                  alpha=0.5, 
                  color=medium_colors[medium], 
                  s=7)
        
        # Reference and regression lines
        if len(comm_mean_true) > 0:
            min_val = min(comm_mean_true.min(), comm_mean_pred.min())
            max_val = max(comm_mean_true.max(), comm_mean_pred.max())
            
            ax.plot([min_val, max_val], [min_val, max_val], 
                    color='grey', linestyle='--', linewidth=0.5)
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(comm_mean_true, comm_mean_pred)
            x_line = np.array([min_val, max_val])
            y_line = slope * x_line + intercept
            ax.plot(x_line, y_line, color=medium_colors[medium], linewidth=1.5, linestyle='-')
        
        # Remove axis labels and title
        ax.set_xlabel("")
        ax.set_ylabel("")
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
    plt.savefig("Figure/Predictability/Fig_predictability_community_averaged_all.svg", 
               dpi=100, bbox_inches='tight')
    plt.close()
    
    print("Community-averaged plots created successfully!")

if __name__ == "__main__":
    main()