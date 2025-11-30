#!/usr/bin/env python3
"""
Check interaction matrices across different simulation directories
"""

import pandas as pd
import numpy as np
import os
import glob

# Find all simulation directories with parameter files
simulation_dirs = glob.glob('Simulation_Data/*/parameter.xlsx')

print("Checking interaction matrices across simulation directories:\n")

for param_path in simulation_dirs:
    sim_dir = os.path.dirname(param_path)
    print(f'=== {sim_dir} ===')
    
    try:
        # Check if has interaction matrix
        interaction_matrix = pd.read_excel(param_path, sheet_name='Sheet2', index_col=0)
        
        # Calculate off-diagonal statistics
        mask = ~np.eye(interaction_matrix.shape[0], dtype=bool)
        off_diag = interaction_matrix.values[mask]
        non_zero = off_diag[off_diag != 0]
        
        print(f'Matrix shape: {interaction_matrix.shape}')
        print(f'Non-zero interactions: {len(non_zero)} ({len(non_zero)/len(off_diag):.1%})')
        
        if len(non_zero) > 0:
            print(f'Interaction value range: [{off_diag.min():.3f}, {off_diag.max():.3f}]')
            print(f'Mean interaction strength: {np.mean(np.abs(non_zero)):.3f}')
        else:
            print('No pairwise interactions (diagonal matrix)')
            
    except Exception as e:
        print(f'Error reading: {e}')
    
    print()