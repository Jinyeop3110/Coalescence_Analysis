#!/usr/bin/env python3

# Debug script to check V3/V4 null model generation in retention analysis
print("Debugging V3/V4 retention analysis...")

# Check if the retention analysis is actually calling V3/V4
import sys
import os
sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

try:
    from AsymmetricityNullModelAnalysis import run_retention_asymmetricity_analysis
    
    print("Running retention analysis with V3/V4...")
    
    # Run with very small sample size to debug quickly
    results = run_retention_asymmetricity_analysis(n_permutations=2, save_plots=False)
    
    if 'null_models' in results:
        print("\nNull models found:")
        for model_name in results['null_models'].keys():
            print(f"  - {model_name}")
            
            # Check sample counts for each model
            if 'LN_6' in results['null_models'][model_name]:
                n_samples = len(results['null_models'][model_name]['LN_6']['type1']['asymmetricity'])
                print(f"    LN_6 samples: {n_samples}")
        
        # Check if V3/V4 are present
        if 'random_selection_v3' in results['null_models']:
            print("\n✅ V3 found in retention results!")
        else:
            print("\n❌ V3 NOT found in retention results!")
            
        if 'random_selection_v4' in results['null_models']:
            print("✅ V4 found in retention results!")
        else:
            print("❌ V4 NOT found in retention results!")
    else:
        print("❌ No null_models found in results!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()