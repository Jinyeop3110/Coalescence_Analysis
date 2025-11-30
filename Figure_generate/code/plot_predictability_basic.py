"""
Plot_predictability_basic.py

Purpose: Develops predictive models for coalescence outcomes using polynomial features
Key functions:
- fit_definite_strength_poly(): Fits polynomial models with L1 regularization
- find_optimal_alpha(): Performs cross-validation to find optimal regularization parameter
- Uses sigmoid transformation for predictions
- Generates scatter plots comparing predicted vs actual outcomes
- Creates plots showing model performance (MSE) across different regularization strengths

Saving paths:
- f"../figure/Fig_predictabiltiy_alpha_vs_mse_{medium}.svg"
- f"../figure/Fig_predictabiltiy_predictability_{medium}.svg"
- f"../figure/Fig_predictabiltiy_predictability_{medium}_normalized.svg"
"""

from common_setup import *
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
from scipy.optimize import minimize
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import ShuffleSplit
from typing import Tuple, List
from scipy import stats

def make_polynomial_features(X: np.ndarray, order: int) -> np.ndarray:
    """
    Generate polynomial features up to 'order'.
    If order=1, we get [1, x1, x2, ...].
    If order=2, we get [1, x1, x2, ..., x1^2, x1*x2, ...].
    """
    if order < 1 or order > 2:
        raise ValueError("Only order=1 or order=2 are supported.")
    
    poly = PolynomialFeatures(degree=order, include_bias=True)
    # shape: (n_samples, number_of_poly_features)
    return poly.fit_transform(X)

def sigmoid(s1,s2):
    diff=s1-s2
    # Return raw sigmoid output scaled to [0, pi/2] instead of [-0.5, 0.5]
    ratio_pred=1.0/(1.0+np.exp(-diff))
    return ratio_pred * (np.pi/2)

def inv_sigmoid(ratio_pred):
    # Convert from [0, pi/2] back to original scale
    norm_pred = ratio_pred / (np.pi/2)
    return np.log(norm_pred / (1 - norm_pred))

def fit_definite_strength_poly(
    X1: np.ndarray,
    X2: np.ndarray,
    y: np.ndarray,
    order: int = 1,
    alpha: List[float] = None,
    w_init: np.ndarray = None
) -> np.ndarray:
    if alpha is None:
        # Default: no regularization if not specified
        alpha = [0.0] * (2 if order == 1 else 3)
    
    if order == 1 and len(alpha) != 2:
        raise ValueError("For order=1, alpha must have length=2.")
    if order == 2 and len(alpha) != 3:
        raise ValueError("For order=2, alpha must have length=3.")
    
    # Transform X1, X2 to polynomial features
    Z1 = make_polynomial_features(X1, order)  # shape: (n_samples, n_poly_features)
    Z2 = make_polynomial_features(X2, order)  # same shape
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
    alpha2 = alpha[2] if order == 2 else 0.0  # quadratic (only if order=2)

    # Initial guess
    if w_init is None:
        w_init = np.zeros(n_poly_features)

    def objective(w):
        # Predictions for each sample pair
        s1 = Z1.dot(w)  # shape: (n_samples,)
        s2 = Z2.dot(w)

        ratio_pred = sigmoid(s1,s2)  # shape: (n_samples,)
        # sum of squared errors
        residuals = y - ratio_pred
        sse = np.sum(residuals**2)

        # Regularization
        reg_intercept = alpha0 * np.sum(np.abs(w[intercept_idx]))
        reg_linear = alpha1 * np.sum(np.abs(w[linear_idx]))
        reg_quad = alpha2 * np.sum(np.abs(w[q]) for q in quadratic_idx)
        
        reg = reg_intercept + reg_linear + reg_quad
        return sse + reg

    # Minimize
    result = minimize(objective, w_init, method='BFGS', options={'maxiter': 100000} )
    w_opt = result.x
    return w_opt

def predict_ratio_poly(w: np.ndarray, X1: np.ndarray, X2: np.ndarray, order: int) -> np.ndarray:
    """
    Given fitted parameters w for polynomial of 'order',
    predict ratio = s1 / (s1 + s2).
    """
    Z1 = make_polynomial_features(X1, order)
    Z2 = make_polynomial_features(X2, order)
    s1 = Z1.dot(w)
    s2 = Z2.dot(w)
    return sigmoid(s1,s2)

def find_optimal_alpha(
    alpha_list, 
    X1_all, 
    X2_all, 
    y_all, 
    order, 
    shuffle_split, 
    to_plot=False, 
    save_filepath=None
):
    """
    Iterates over a list of alpha values, performs cross-validation using `shuffle_split`,
    computes train/test MSE for each alpha, and returns the alpha with the lowest test MSE.
    """
    # Store the average MSE per alpha
    alpha_mse_train_list = []
    alpha_mse_test_list = []

    # Iterate over each candidate alpha
    for alpha in alpha_list:
        mse_train_folds = []
        mse_test_folds = []

        # Cross-validation
        for fold_idx, (train_idx, test_idx) in enumerate(shuffle_split.split(X1_all)):
            X1_train, X2_train, y_train = X1_all[train_idx], X2_all[train_idx], y_all[train_idx]
            X1_test,  X2_test,  y_test  = X1_all[test_idx],  X2_all[test_idx],  y_all[test_idx]

            # No duplication needed for [0, pi/2] range

            # Fit the model
            w_fit = fit_definite_strength_poly(
                X1_train, X2_train, y_train,
                order=order,
                alpha=[0.1, alpha]
            )

            # Predict on test set
            y_pred_test = predict_ratio_poly(w_fit, X1_test, X2_test, order=order)
            # Predict on train set
            y_pred_train = predict_ratio_poly(w_fit, X1_train, X2_train, order=order)

            # Calculate MSE on test set
            mse_tst = np.mean((y_test - y_pred_test)**2) / np.var(y_all)
            mse_test_folds.append(mse_tst)

            # Calculate MSE on train set
            mse_trn = np.mean((y_train - y_pred_train)**2) / np.var(y_all)
            mse_train_folds.append(mse_trn)

        # Average MSE across folds for this alpha
        avg_mse_test  = np.mean(mse_test_folds)
        avg_mse_train = np.mean(mse_train_folds)

        alpha_mse_test_list.append(avg_mse_test)
        alpha_mse_train_list.append(avg_mse_train)

        print(f"Alpha={alpha}: avg test MSE={avg_mse_test:.4f}, avg train MSE={avg_mse_train:.4f}")

    # Find the best alpha
    best_index     = np.argmin(alpha_mse_test_list)
    best_alpha     = alpha_list[best_index]
    best_test_mse  = alpha_mse_test_list[best_index]

    print(f"\nOptimal alpha: {best_alpha}, Test MSE={best_test_mse:.4f}")

    if to_plot:
        plt.figure(figsize=(6, 4))
        # Plot test MSE
        plt.plot(alpha_list, alpha_mse_test_list, marker='o', label='Test MSE')
        # Plot train MSE
        plt.plot(alpha_list, alpha_mse_train_list, marker='s', label='Train MSE')

        # Use log scale on the x-axis
        plt.xscale('log')

        # Mark the best alpha
        plt.plot(best_alpha, best_test_mse, marker='*', markersize=14, 
                color='red', label='Optimal alpha')

        plt.xlabel("Alpha (log scale)")
        plt.ylabel("MSE (normalized)")
        plt.title("Alpha vs. MSE")
        plt.legend()

        if save_filepath:
            plt.savefig(save_filepath, dpi=100, bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    return best_alpha, best_test_mse, alpha_mse_train_list, alpha_mse_test_list

def plot_predictions_for_alpha(
    alpha,
    X1_all,
    X2_all,
    y_all,
    order,
    to_plot=False,
    save_filepath=None,
    scatter_color='blue',
    draw_reference_line=True,
    draw_shade=False,
    normalize=lambda x:x,
    confidence=0.95
):
    """Plot predictions vs actual values for a given alpha value."""
    # Duplicate X and y
    X1_train = X1_all
    X2_train = X2_all
    y_train  = y_all

    # Fit the model
    w_fit = fit_definite_strength_poly(
        X1_train, X2_train, y_train,
        order=order,
        alpha=[0.1, alpha]
    )

    # Predict on the original data
    y_pred = predict_ratio_poly(w_fit, X1_all, X2_all, order=order)

    # Compute the normalized MSE
    mse = np.mean((y_all - y_pred)**2) / np.var(y_all)

    print(f"Alpha={alpha}, MSE={mse:.4f}")

    if to_plot:
        # No flipping needed since we're using [0, pi/2] range
        y_all_plot = y_all
        y_pred_plot = y_pred

        # Plotting
        mm = 1 / 25.4 * 72
        fig_width  = 70 * mm
        fig_height = 60 * mm

        fig, ax = plt.subplots(
            figsize=(fig_width / 72, fig_height / 72),
            facecolor='w', edgecolor='k'
        )

        # Apply normalization if requested, otherwise use raw values
        y_true_norm = normalize(y_all_plot)
        y_pred_norm = normalize(y_pred_plot)

        # Plot flipped y vs flipped predictions
        ax.scatter(
            y_true_norm,
            y_pred_norm,
            alpha=0.5,
            color=scatter_color,
            label="Predicted vs True",
            s=7
        )

        # Draw reference line if requested
        if draw_reference_line:
            min_val = min(y_true_norm.min(), y_pred_norm.min())
            max_val = max(y_true_norm.max(), y_pred_norm.max())
            ax.plot(
                [min_val, max_val],
                [min_val, max_val],
                color='grey',
                linestyle='--',
                label="Ideal Fit (y = x)",
                linewidth=0.5
            )
        
        # Add regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(y_true_norm, y_pred_norm)
        x_line = np.array([min_val, max_val])
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color=scatter_color, linewidth=1.5, linestyle='-')

        # Conditionally draw confidence interval
        if draw_shade:
            # Compute linear regression for the trend line
            slope, intercept, r_value, p_value, std_err = stats.linregress(y_true_norm, y_pred_norm)
            y_fit = slope * y_true_norm + intercept

            # Calculate confidence intervals
            n = len(y_true_norm)
            dof = n - 2
            t_stat = stats.t.ppf((1 + confidence) / 2., dof)
            residuals = y_pred_norm - y_fit
            s_err = np.sqrt(np.sum(residuals**2) / dof)

            ci = t_stat * s_err * np.sqrt(
                1/n + (y_true_norm - np.mean(y_true_norm))**2 / np.sum((y_true_norm - np.mean(y_true_norm))**2)
            )
            upper = y_fit + ci
            lower = y_fit - ci

            # Sort the data for proper plotting
            sorted_indices = np.argsort(y_true_norm)
            y_true_sorted = y_true_norm[sorted_indices]
            upper_sorted = upper[sorted_indices]
            lower_sorted = lower[sorted_indices]

            # Fill between the confidence intervals
            ax.fill_between(
                y_true_sorted,
                lower_sorted,
                upper_sorted,
                color=scatter_color,
                alpha=0.2,
                label=f"{int(confidence*100)}% Confidence Interval"
            )

        # Add MSE Text instead of R-squared
        ax.text(
            0.05, 0.95,
            f"Test MSE = {mse:.4f}",
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.5)
        )

        # Additional Plot Settings
        ax.set_xlabel("True y")
        ax.set_ylabel("Predicted y")
        ax.grid(True)
        
        # Set tick locations and labels for pi values
        pi_ticks = [0, np.pi/4, np.pi/2]
        pi_labels = ['0', 'π/4', 'π/2']
        ax.set_xticks(pi_ticks)
        ax.set_xticklabels(pi_labels)
        ax.set_yticks(pi_ticks)
        ax.set_yticklabels(pi_labels)

        # Save or show
        if save_filepath:
            fig.savefig(save_filepath, dpi=100, bbox_inches='tight')
            plt.close(fig)
        else:
            plt.show()

    return y_pred, mse

def main():
    """Main function to run predictability analysis for different media."""
    medium_list=["L", "M", "H"]
    alphas=[0.01, 0.1, 0.063095]  # Optimal alphas for each medium
    colors = ['#A7216A',  # rich magenta-purple
              '#802000',
              '#E24912',  # deep orange-red
              ]

    for medium, alpha, color in zip(medium_list, alphas, colors):
        species_num=12
        com_type="S"
        rep=-1

        mode="Casewise"  # or "Communitywise"

        if mode=="Casewise":
            degList=np.zeros(43)

            X1_all=[]
            X2_all=[]
            y_all=[]

            IDX_list = Community_PermutateList("F", com_type, medium, "C", species_num, rep)
            print(IDX_list)

            idx=np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_1=Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
            idx=np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_2=Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
            idx=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
            
            data1=[]
            data2=[]
            data3=[]
            species_num=len(degList)
            data_null_model=[]
            
            for i in range(len(idx)):
                c_mix=Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                c_1=np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                c_2=np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                c_1=c_1*(c_1>1e-4)
                c_2=c_2*(c_2>1e-4)
                
                u,v,k=metric_VectorDecomposition_onlyPositive(c_1,c_2,c_mix)
                data1.append(u)
                data2.append(v)
                data3.append(k)
                
                eps=1e-3
                y=np.arctan(np.array(np.abs(u)+eps)/np.array(np.abs(v)+eps))
                X1_all.append(c_1)
                X2_all.append(c_2)
                y_all.append(y)

            X1_all=np.array(X1_all)
            X2_all=np.array(X2_all)
            y_all=np.array(y_all)

        # Cross-validation setup
        n_splits = 10
        shuffle_split = ShuffleSplit(n_splits=n_splits, test_size=0.2, random_state=123)
        order=1

        # Find optimal alpha
        alpha_list = np.logspace(-0, -3, 16)

        best_alpha, best_test_mse, train_mse_list, test_mse_list = find_optimal_alpha(
            alpha_list=alpha_list,
            X1_all=X1_all,
            X2_all=X2_all,
            y_all=y_all,
            order=1,
            shuffle_split=shuffle_split,
            to_plot=True,
            save_filepath=f"Figure/Predictability/Fig_predictability_alpha_vs_mse_{medium}.svg"
        )

        # Plot predictions with optimal alpha
        plot_predictions_for_alpha(
            alpha,
            X1_all,
            X2_all,
            y_all,
            order,
            to_plot=True,
            save_filepath=f"Figure/Predictability/Fig_predictability_{medium}.svg",
            normalize=lambda x:x,
            scatter_color=color,
            draw_reference_line=True,
            draw_shade=True,
        )

        plot_predictions_for_alpha(
            alpha,
            X1_all,
            X2_all,
            y_all,
            order,
            to_plot=True,
            save_filepath=f"Figure/Predictability/Fig_predictability_{medium}_normalized.svg",
            normalize=lambda x:inv_sigmoid(x),
            scatter_color=color,
            draw_reference_line=True,
            draw_shade=True,
        )

if __name__ == "__main__":
    main()