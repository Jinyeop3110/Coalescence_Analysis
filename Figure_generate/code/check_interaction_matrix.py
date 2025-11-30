#!/usr/bin/env python3
"""
Check interaction matrix in simulation parameter files
"""

import pandas as pd
import numpy as np
import os

# Check standard pool parameter file
param_file = 'Simulation_Data/standard_defined_pool/parameter.xlsx'

if os.path.exists(param_file):
    print(f'Checking {param_file}')
    
    # Read interaction matrix from Sheet2
    interaction_matrix = pd.read_excel(param_file, sheet_name='Sheet2', index_col=0)
    
    print(f'\nInteraction matrix shape: {interaction_matrix.shape}')
    print(f'Matrix appears to be symmetric: {np.allclose(interaction_matrix.values, interaction_matrix.values.T)}')
    
    # Check diagonal values
    print('\nDiagonal values (self-interaction):')
    print(interaction_matrix.values.diagonal()[:10])
    
    # Check off-diagonal values
    mask = ~np.eye(96, dtype=bool)
    off_diag = interaction_matrix.values[mask]
    print(f'\nOff-diagonal values range: [{off_diag.min():.3f}, {off_diag.max():.3f}]')
    
    # Count non-zero interactions
    non_zero_mask = off_diag != 0
    non_zero_count = np.sum(non_zero_mask)
    print(f'\nNumber of non-zero off-diagonal elements: {non_zero_count}')
    print(f'Proportion of non-zero interactions: {non_zero_count/len(off_diag):.2%}')
    
    # Show some example interactions
    print('\nExample interaction values (first 5x5 submatrix):')
    print(interaction_matrix.iloc[:5, :5])
    
    # Check for species in community pool
    comm_file = 'Simulation_Data/standard_defined_pool/commuityLibrary.xlsx'
    if os.path.exists(comm_file):
        print(f'\n\nChecking community library: {comm_file}')
        comm_lib = pd.read_excel(comm_file, sheet_name='Sheet1', index_col=0)
        print(f'Community library shape: {comm_lib.shape}')
        print(f'Number of communities: {comm_lib.shape[0]}')
        print(f'Number of species in pool: {comm_lib.shape[1]}')
        
        # Show which species are in each community
        for i in range(min(5, comm_lib.shape[0])):
            species_in_comm = np.where(comm_lib.iloc[i].values > 0)[0]
            print(f'\nCommunity {i}: species {list(species_in_comm)}')