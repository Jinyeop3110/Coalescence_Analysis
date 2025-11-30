"""
Plot_predictability_simulation.py

Purpose: Analyzes simulation data with varying parameters
Key features:
- Processes simulation results from different k_gamma values (0, 0.5, 1, 2, 4)
- Creates heatmaps showing test MSE across different interaction strengths and carrying capacity variations
- Analyzes dominance fractions in the simulations
- Uses JSON files to store and retrieve simulation results

Saving paths:
- No direct figure saving paths (shows plots only)
"""

from common_setup import *
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import ShuffleSplit
from typing import Tuple, List

def make_polynomial_features(X: np.ndarray, order: int) -> np.ndarray:
    """Generate polynomial features up to 'order'."""
    if order < 1 or order > 2:
        raise ValueError("Only order=1 or order=2 are supported.")
    
    poly = PolynomialFeatures(degree=order, include_bias=True)
    return poly.fit_transform(X)

def sigmoid(s1,s2):
    diff=s1-s2
    ratio_pred=1.0/(1.0+np.exp(-diff))-0.5
    return ratio_pred

def inv_sigmoid(ratio_pred):
    return np.log((ratio_pred + 0.5) / (0.5 - ratio_pred))

def fit_definite_strength_poly(
    X1: np.ndarray,
    X2: np.ndarray,
    y: np.ndarray,
    order: int = 1,
    alpha: List[float] = None,
    w_init: np.ndarray = None
) -> np.ndarray:
    """Fit polynomial model with L1 regularization."""
    if alpha is None:
        alpha = [0.0] * (2 if order == 1 else 3)
    
    if order == 1 and len(alpha) != 2:
        raise ValueError("For order=1, alpha must have length=2.")
    if order == 2 and len(alpha) != 3:
        raise ValueError("For order=2, alpha must have length=3.")
    
    Z1 = make_polynomial_features(X1, order)
    Z2 = make_polynomial_features(X2, order)
    n_samples, n_poly_features = Z1.shape
    
    d = X1.shape[1]
    intercept_idx = [0]
    linear_idx = list(range(1, d+1))
    if order == 1:
        quadratic_idx = []
    else:
        quadratic_idx = list(range(d+1, n_poly_features))
    
    alpha0 = alpha[0]  # intercept
    alpha1 = alpha[1]  # linear
    alpha2 = alpha[2] if order == 2 else 0.0  # quadratic

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
        reg_quad = alpha2 * np.sum(np.abs(w[q]) for q in quadratic_idx)
        
        reg = reg_intercept + reg_linear + reg_quad
        return sse + reg

    result = minimize(objective, w_init, method='BFGS', options={'maxiter': 100000} )
    return result.x

def predict_ratio_poly(w: np.ndarray, X1: np.ndarray, X2: np.ndarray, order: int) -> np.ndarray:
    """Predict using fitted polynomial model."""
    Z1 = make_polynomial_features(X1, order)
    Z2 = make_polynomial_features(X2, order)
    s1 = Z1.dot(w)
    s2 = Z2.dot(w)
    return sigmoid(s1,s2)

def extract_sc_cc_numeric(loaded_results, rep_num, intensity_index):
    """Extract and convert sc_list and cc_list for a specified intensity and replicate number."""
    import sys

    # Retrieve the specified intensity key
    intensity_keys = sorted(loaded_results.keys())
    if len(intensity_keys) <= intensity_index:
        raise ValueError(f"The loaded_results dictionary does not contain an intensity at index {intensity_index}.")

    intensity_key = intensity_keys[intensity_index]
    print(f"Selected Intensity: {intensity_key}")

    # Construct the community key
    community_key = f'community_{rep_num}'
    print(f"Selected Community: {community_key}")

    # Access the community data
    community_data = loaded_results.get(intensity_key, {}).get(community_key, {})
    if not community_data:
        raise ValueError(f"Community '{community_key}' not found under intensity '{intensity_key}'.")

    # Extract sc_list and cc_list
    sc_list = community_data.get('sc_list', {})
    cc_list = community_data.get('cc_list', {})

    # Convert sc_list keys from strings to integers
    sc_list_numeric = {}
    for k, v in sc_list.items():
        try:
            key_num = int(k)
            sc_list_numeric[key_num] = v
        except ValueError:
            print(f"Warning: Invalid sc_list key '{k}'. Skipping.", file=sys.stderr)

    # Convert cc_list keys from 'x_y' strings to (x, y) tuples of integers
    cc_list_numeric = {}
    for k, v in cc_list.items():
        try:
            key_tuple = tuple(int(part) for part in k.split('_'))
            if len(key_tuple) != 2:
                raise ValueError
            cc_list_numeric[key_tuple] = v
        except ValueError:
            print(f"Warning: Invalid cc_list key '{k}'. Expected format 'x_y'. Skipping.", file=sys.stderr)

    return sc_list_numeric, cc_list_numeric

def prepare_X1_X2_y(loaded_results, rep_num, intensity_index, eps=1e-3):
    """Prepare X1_all, X2_all, and y_all by processing sc_list and cc_list."""
    # Extract sc_list and cc_list with numeric keys
    sc_list_numeric, cc_list_numeric = extract_sc_cc_numeric(loaded_results, rep_num, intensity_index)

    X1_all, X2_all, y_all = [], [], []

    # Iterate over each coalescence pair
    for (c1_idx, c2_idx), cmix in cc_list_numeric.items():
        c1 = sc_list_numeric.get(c1_idx)
        c2 = sc_list_numeric.get(c2_idx)

        if c1 is None or c2 is None:
            print(f"Warning: Sub-community indices {c1_idx}, {c2_idx} not found. Skipping.", file=sys.stderr)
            continue

        # Apply the metric function
        try:
            u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
        except np.linalg.LinAlgError as e:
            if 'Singular matrix' in str(e):
                print("Singular matrix error occurred.")
                print(f"c1: {c1}")
                print(f"c2: {c2}")
                print(f"cmix: {cmix}")
                u1=u2=1/np.sqrt(2)
        
        # Calculate y
        y = (np.arctan((np.abs(u) + eps) / (np.abs(v) + eps)) / (np.pi / 2)) - 0.5

        # Append to the lists
        X1_all.append(c1)
        X2_all.append(c2)
        y_all.append(y)

    return np.array(X1_all), np.array(X2_all), np.array(y_all)

def plot_mse_heatmap(save_path=None):
    """Plot heatmap of MSE results across different simulation parameters.
    
    Args:
        save_path: Optional path to save the figure
    """
    # Define session names and intensity indices
    session_names = [
         "Simulation_Data/standard_defined_pool",
        "Simulation_Data/k_gamma_0.5_defined_pool_nooverlap_12from48",
        "Simulation_Data/k_gamma_1_defined_pool_nooverlap_12from48",
         "Simulation_Data/k_gamma_2_defined_pool_nooverlap_12from48",
          "Simulation_Data/k_gamma_4_defined_pool_nooverlap_12from48",
    ]
    session_labels = [0, 0.5, 1, 2, 4]
    intensity_indices = [0, 2, 4, 6, 8, 10]

    # Initialize dictionaries to store mean and std MSE values
    mean_mse_results = {}
    std_mse_results = {}

    # Sort sessions based on k_gamma in ascending order
    sorted_sessions = session_names[::-1]
    session_labels= session_labels[::-1]
    
    # Read JSON files and compute mean and std test MSE
    for session_name in sorted_sessions:
        result_file = Path(session_name) / 'results_intensity_10.json'
        
        if not result_file.exists():
            print(f"Warning: File not found: {result_file}")
            continue
        
        with open(result_file, 'r') as infile:
            try:
                session_results = json.load(infile)
            except json.JSONDecodeError:
                print(f"Error: JSON decoding failed for file: {result_file}")
                continue
        
        # Initialize dictionaries for current session
        mean_mse_results[session_name] = {}
        std_mse_results[session_name] = {}
        
        # Calculate mean and std test MSE for each intensity index
        for idx in intensity_indices:
            if str(idx) in session_results:
                mse_values = session_results[str(idx)]['best_test_mse']
                mean_mse = np.nanmean(mse_values)
                std_mse = np.nanstd(mse_values)
                mean_mse_results[session_name][idx] = mean_mse
                std_mse_results[session_name][idx] = std_mse
            else:
                # Handle missing intensity index
                mean_mse_results[session_name][idx] = np.nan
                std_mse_results[session_name][idx] = np.nan
                print(f"Warning: Intensity index {idx} not found in {result_file}")

    # Prepare data for heatmap
    heatmap_means = []
    heatmap_stds = []

    for session_name in sorted_sessions:
        if session_name in mean_mse_results:
            mse_data = mean_mse_results[session_name]
            std_data = std_mse_results[session_name]
            
            # Append mean and std data in the order of intensity_indices
            heatmap_means.append([mse_data.get(idx, np.nan) for idx in intensity_indices])
            heatmap_stds.append([std_data.get(idx, np.nan) for idx in intensity_indices])
        else:
            continue

    heatmap_means = np.array(heatmap_means)
    heatmap_stds = np.array(heatmap_stds)

    # Create annotation labels combining mean and std
    annotations = np.empty_like(heatmap_means, dtype=object)
    for i in range(heatmap_means.shape[0]):
        for j in range(heatmap_means.shape[1]):
            mean = heatmap_means[i, j]
            std = heatmap_stds[i, j]
            if np.isnan(mean) or np.isnan(std):
                annotations[i, j] = "N/A"
            else:
                annotations[i, j] = f"{mean:.2f} ± {std:.2f}"

    # Prepare intensity labels by multiplying by 0.1
    intensity_labels = [f"{idx * 0.1:.1f}" for idx in intensity_indices]

    # Plot heatmap with annotations
    plt.figure(figsize=(4, 3))
    sns.heatmap(
        heatmap_means, 
        annot=annotations, 
        annot_kws={'size': 5},
        fmt='',  # Custom annotations already formatted
        cmap="inferno", 
        xticklabels=intensity_labels, 
        yticklabels=session_labels,
        cbar_kws={'label': 'Mean Test MSE'}
    )
    plt.title("Test MSE")
    plt.xlabel("Interaction strength(I)")
    plt.ylabel("Carrying capacity var$(K_{var})$")

    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_dominance_heatmap(save_path=None):
    """Plot heatmap of dominance fractions across different simulation parameters.
    
    Args:
        save_path: Optional path to save the figure
    """
    # Define session names and intensity indices
    session_names = [
         "Simulation_Data/standard_defined_pool",
        "Simulation_Data/k_gamma_0.5_defined_pool_nooverlap_12from48",
        "Simulation_Data/k_gamma_1_defined_pool_nooverlap_12from48",
         "Simulation_Data/k_gamma_2_defined_pool_nooverlap_12from48",
          "Simulation_Data/k_gamma_4_defined_pool_nooverlap_12from48",
    ]
    session_labels = [0, 0.5, 1, 2, 4]
    intensity_indices = [0, 2, 4, 6, 8, 10]

    # Initialize dictionaries to store mean and std MSE values
    mean_mse_results = {}
    std_mse_results = {}

    # Sort sessions based on k_gamma in ascending order
    sorted_sessions = session_names[::-1]
    session_labels= session_labels[::-1]
    
    # Read JSON files and compute mean and std test MSE
    for session_name in sorted_sessions:
        result_file = Path(session_name) / 'results_dominance_fractions.json'
        
        if not result_file.exists():
            print(f"Warning: File not found: {result_file}")
            continue
        
        with open(result_file, 'r') as infile:
            try:
                session_results = json.load(infile)
            except json.JSONDecodeError:
                print(f"Error: JSON decoding failed for file: {result_file}")
                continue
        
        # Initialize dictionaries for current session
        mean_mse_results[session_name] = {}
        std_mse_results[session_name] = {}
        
        # Calculate mean and std test MSE for each intensity index
        for idx in intensity_indices:
            if str(idx) in session_results:
                mse_values = session_results[str(idx)]['dominance']
                mean_mse = np.mean(np.array(mse_values)==0)
                std_mse = 0
                mean_mse_results[session_name][idx] = mean_mse
                std_mse_results[session_name][idx] = std_mse
            else:
                # Handle missing intensity index
                mean_mse_results[session_name][idx] = np.nan
                std_mse_results[session_name][idx] = np.nan
                print(f"Warning: Intensity index {idx} not found in {result_file}")

    # Prepare data for heatmap
    heatmap_means = []
    heatmap_stds = []

    for session_name in sorted_sessions:
        if session_name in mean_mse_results:
            mse_data = mean_mse_results[session_name]
            std_data = std_mse_results[session_name]
            
            # Append mean and std data in the order of intensity_indices
            heatmap_means.append([mse_data.get(idx, np.nan) for idx in intensity_indices])
            heatmap_stds.append([std_data.get(idx, np.nan) for idx in intensity_indices])
        else:
            continue

    heatmap_means = np.array(heatmap_means)
    heatmap_stds = np.array(heatmap_stds)

    # Create annotation labels combining mean and std
    annotations = np.empty_like(heatmap_means, dtype=object)
    for i in range(heatmap_means.shape[0]):
        for j in range(heatmap_means.shape[1]):
            mean = heatmap_means[i, j]
            std = heatmap_stds[i, j]
            if np.isnan(mean) or np.isnan(std):
                annotations[i, j] = "N/A"
            else:
                annotations[i, j] = f"{mean:.2f} ± {std:.2f}"

    # Prepare intensity labels by multiplying by 0.1
    intensity_labels = [f"{idx * 0.1:.1f}" for idx in intensity_indices]

    # Plot heatmap with annotations
    plt.figure(figsize=(4, 3))
    sns.heatmap(
        heatmap_means, 
        annot=annotations, 
        annot_kws={'size': 5},
        fmt='',  # Custom annotations already formatted
        cmap="inferno", 
        xticklabels=intensity_labels, 
        yticklabels=session_labels,
        cbar_kws={'label': 'Mean Test MSE'}
    )
    plt.title("Dominance fraction")
    plt.xlabel("Interaction strength(I)")
    plt.ylabel("Carrying capacity var$(K_{var})$")

    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def main():
    """Main function to run simulation analysis."""
    print("Plotting MSE heatmap...")
    plot_mse_heatmap(save_path="Figure/Predictability/Fig_predictability_simulation_mse_heatmap.svg")
    
    print("Plotting dominance fraction heatmap...")
    plot_dominance_heatmap(save_path="Figure/Predictability/Fig_predictability_simulation_dominance_heatmap.svg")

if __name__ == "__main__":
    main()