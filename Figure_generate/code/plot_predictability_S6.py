"""
Plot_predictability_S6.py
Purpose: Predictive models for coalescence outcomes with 6 initial species
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

def main():
    species_num = 6
    medium_list = ["L", "M", "H"]
    colors = ['#A7216A', '#802000', '#E24912']
    alphas = [0.05, 0.08, 0.05]  # Adjusted for S6
    
    for medium, alpha, color in zip(medium_list, alphas, colors):
        print(f"Processing medium {medium} with {species_num} species...")
        
        com_type = "S"
        rep = -1
        mode = "Casewise"
        
        if mode == "Casewise":
            degList = np.zeros(43)
            
            X1_all = []
            X2_all = []
            y_all = []
            
            IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, rep)
            print(f"Found {len(IDX_list)} samples")
            
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
            
            X1_all = np.array(X1_all)
            X2_all = np.array(X2_all)
            y_all = np.array(y_all)
        
        # Fit model with pre-defined alpha (no duplication for [0, pi/2] range)
        X1_train = X1_all
        X2_train = X2_all
        y_train = y_all
        
        w_fit = fit_definite_strength_poly(
            X1_train, X2_train, y_train,
            order=1,
            alpha=[0.1, alpha]
        )
        
        # Predict and calculate MSE
        y_pred = predict_ratio_poly(w_fit, X1_all, X2_all, order=1)
        mse = np.mean((y_all - y_pred)**2) / np.var(y_all)
        
        print(f"Medium {medium}: MSE={mse:.4f}, alpha={alpha}, n_samples={len(y_all)}")
        
        # Create scatter plot
        fig, ax = plt.subplots(figsize=(3, 2.5))
        ax.scatter(y_all, y_pred, alpha=0.5, color=color, s=7)
        
        min_val = min(y_all.min(), y_pred.min())
        max_val = max(y_all.max(), y_pred.max())
        ax.plot([min_val, max_val], [min_val, max_val], 
                color='grey', linestyle='--', linewidth=0.5)
        
        # Add regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(y_all, y_pred)
        x_line = np.array([min_val, max_val])
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color=color, linewidth=1.5, linestyle='-')
        
        ax.text(0.05, 0.95, f"Test MSE = {mse:.4f}", 
                transform=ax.transAxes, fontsize=10, 
                verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5))
        
        # Remove axis labels
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.grid(True, alpha=0.3)
        
        # Set tick locations and labels for pi values
        pi_ticks = [0, np.pi/4, np.pi/2]
        pi_labels = ['0', 'π/4', 'π/2']
        ax.set_xticks(pi_ticks)
        ax.set_xticklabels(pi_labels)
        ax.set_yticks(pi_ticks)
        ax.set_yticklabels(pi_labels)
        
        plt.tight_layout()
        plt.savefig(f"Figure/Predictability/Fig_predictability_{medium}_S6.svg", 
                   dpi=100, bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    main()