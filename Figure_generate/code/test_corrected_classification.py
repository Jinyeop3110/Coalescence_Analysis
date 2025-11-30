"""
Test corrected classification logic for natural communities
"""

from common_setup import *
import numpy as np
import matplotlib.pyplot as plt

def corrected_calculate_asymmetricity(u, v, k):
    """
    Corrected asymmetricity calculation that properly handles edge cases.
    
    x: magnitude of parent contributions (high = parents contribute, low = restructuring)
    y: balance between parents (0 = equal contribution, 1 = one parent dominates)
    """
    u = np.array(u)
    v = np.array(v)
    
    # x represents the total magnitude of parent contributions
    x = np.sqrt(u**2 + v**2)
    
    # y represents the imbalance between parent contributions
    # When u≈v, y should be close to 0 (balanced mixing)
    # When either u>>v or v>>u, y should be close to 1 (dominance)
    
    # Use a different approach that avoids division issues
    total = np.abs(u) + np.abs(v) + 1e-8  # Add small value to avoid division by zero
    imbalance = np.abs(u - v) / total
    y = imbalance  # This ranges from 0 (equal) to ~1 (one dominates)
    
    return x, y

def corrected_characterize_case(x, y):
    """
    Corrected classification based on proper interpretation:
    - Dominance: High parent contribution (x^2 > 0.5) AND imbalanced (y > 0.5)
    - Mixing: High parent contribution (x^2 > 0.5) AND balanced (y < 0.5)
    - Restructuring: Low parent contribution (x^2 < 0.5)
    """
    if x**2 > 0.5:
        if y > 0.5:
            return 0  # Dominance
        else:
            return 1  # Mixing
    else:
        return 2  # Restructuring

def test_classification():
    """Test the corrected classification with various scenarios."""
    
    print("Testing corrected classification logic:")
    print("="*60)
    
    test_cases = [
        # (u, v, expected_outcome)
        (0.9, 0.1, "Dominance"),      # Parent 1 dominates
        (0.1, 0.9, "Dominance"),      # Parent 2 dominates
        (0.7, 0.7, "Mixing"),         # Both contribute equally
        (0.8, 0.6, "Mixing"),         # Both contribute significantly
        (0.2, 0.2, "Restructuring"),  # Low contribution from both
        (0.1, 0.1, "Restructuring"),  # Very low contribution
        (1.0, 0.0, "Dominance"),      # Complete dominance
        (0.0, 1.0, "Dominance"),      # Complete dominance
        (0.5, 0.5, "Mixing"),         # Moderate equal contribution
    ]
    
    for u, v, expected in test_cases:
        # Original calculation (with error handling)
        try:
            x_orig, y_orig = calculate_assymetricity(u, v, 0)
            class_orig = characterize_case(x_orig, y_orig)
            orig_names = {0: "Dominance", 1: "Mixing", 2: "Restructuring"}
            orig_result = orig_names.get(class_orig, "Error")
        except:
            orig_result = "Error"
            x_orig, y_orig = np.nan, np.nan
        
        # Corrected calculation
        x_corr, y_corr = corrected_calculate_asymmetricity(u, v, 0)
        class_corr = corrected_characterize_case(x_corr, y_corr)
        corr_names = {0: "Dominance", 1: "Mixing", 2: "Restructuring"}
        corr_result = corr_names[class_corr]
        
        print(f"\nu={u:.1f}, v={v:.1f} -> Expected: {expected}")
        print(f"  Original: x={x_orig:.3f}, y={y_orig:.3f} -> {orig_result}")
        print(f"  Corrected: x={x_corr:.3f}, y={y_corr:.3f} -> {corr_result}")
        print(f"  Match expected: {'✓' if corr_result == expected else '✗'}")

def analyze_natural_with_corrected_logic():
    """Reanalyze natural data with corrected classification."""
    
    print("\n\n" + "="*60)
    print("REANALYSIS WITH CORRECTED CLASSIFICATION")
    print("="*60)
    
    results_comparison = {}
    
    for nutrient_level in ['LN', 'MN', 'HN']:
        print(f"\nProcessing {nutrient_level}...")
        
        if nutrient_level not in Nat_Coal_IDX:
            continue
            
        IDX_list = Nat_Coal_IDX[nutrient_level]
        
        # Get coalescence events
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        
        # Get parent indices
        idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
        idx_1 = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in idx_1])
        
        idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
        idx_2 = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in idx_2])
        
        # Get mixed indices
        idx_mix = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in IDX_list])
        
        orig_counts = {0: 0, 1: 0, 2: 0}
        corr_counts = {0: 0, 1: 0, 2: 0}
        
        for i in range(len(idx)):
            try:
                # Get vectors
                c_1 = np.array(Processed_sequences_natural.iloc[idx_1[i]].values.tolist()[1:])
                c_2 = np.array(Processed_sequences_natural.iloc[idx_2[i]].values.tolist()[1:])
                c_mix = Processed_sequences_natural.iloc[idx_mix[i]].values.tolist()[1:]
                
                # Apply threshold
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                # Vector decomposition
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                
                # Original classification
                try:
                    x_orig, y_orig = calculate_assymetricity(u, v, k)
                    class_orig = characterize_case(x_orig, y_orig)
                    orig_counts[class_orig] += 1
                except:
                    pass
                
                # Corrected classification
                x_corr, y_corr = corrected_calculate_asymmetricity(u, v, k)
                class_corr = corrected_characterize_case(x_corr, y_corr)
                corr_counts[class_corr] += 1
                
            except Exception as e:
                continue
        
        results_comparison[nutrient_level] = {
            'original': orig_counts,
            'corrected': corr_counts
        }
        
        print(f"  Original:  Dom={orig_counts[0]}, Mix={orig_counts[1]}, Res={orig_counts[2]}")
        print(f"  Corrected: Dom={corr_counts[0]}, Mix={corr_counts[1]}, Res={corr_counts[2]}")
    
    return results_comparison

def create_comparison_visualization(results):
    """Create a visual comparison of original vs corrected classification."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    nutrients = ['LN', 'MN', 'HN']
    class_names = ['Dominance', 'Mixing', 'Restructuring']
    colors = ['#E24912', '#A7216A', '#802000']
    
    # Original classification
    bottom = np.zeros(3)
    for i, class_name in enumerate(class_names):
        values = [results[nut]['original'][i] for nut in nutrients]
        ax1.bar(nutrients, values, bottom=bottom, label=class_name, color=colors[i])
        bottom += values
    
    ax1.set_title("Original Classification")
    ax1.set_ylabel("Number of Events")
    ax1.legend()
    
    # Corrected classification
    bottom = np.zeros(3)
    for i, class_name in enumerate(class_names):
        values = [results[nut]['corrected'][i] for nut in nutrients]
        ax2.bar(nutrients, values, bottom=bottom, label=class_name, color=colors[i])
        bottom += values
    
    ax2.set_title("Corrected Classification")
    ax2.set_ylabel("Number of Events")
    ax2.legend()
    
    plt.suptitle("Natural Community Classification: Original vs Corrected")
    plt.tight_layout()
    plt.savefig("Figure/PhaseDiagram/classification_comparison.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Test the classification logic
    test_classification()
    
    # Analyze natural data with corrected logic
    results = analyze_natural_with_corrected_logic()
    
    # Create visualization
    create_comparison_visualization(results)