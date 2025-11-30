#!/usr/bin/env python
"""
TEST VERSION: Verify interaction matrix saving works
Runs only 2 reps × 2 intensities for quick testing
"""

import os
import sys
import json
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from InitializeSpeciesPool import InitializeSpeceiesPool
from LV import run_lotka_volterra

def uniform_distribution(u, o):
    return (2*u + 2*o) * np.random.random() - o

def test_matrix_save():
    print("🧪 TESTING INTERACTION MATRIX SAVE\n")
    print("="*50)

    # Minimal parameters for testing
    session_name = "Simulation_Data/TEST_matrices"
    os.makedirs(session_name, exist_ok=True)

    N = 48
    num_C = 4
    num_S = 12
    N_reps = 2  # Just 2 reps for testing
    u_list = [0.3, 0.5]  # Just 2 intensities
    o = 0
    t = [0, 5000]
    threshold = 1e-3

    print(f"Test parameters:")
    print(f"  Species: {N}")
    print(f"  Reps: {N_reps}")
    print(f"  Intensities: {u_list}")
    print(f"  Expected matrices: {N_reps * len(u_list)}")
    print("="*50 + "\n")

    all_results = {}

    for u in u_list:
        print(f"Testing u = {u:.1f}...")
        all_results[f"{u:.1f}"] = {}

        for rep in range(N_reps):
            print(f"  Rep {rep}...", end=" ")

            seed = int(u * 10000) + rep * 100000
            np.random.seed(seed)

            # Generate interaction matrix
            I, g, k = InitializeSpeceiesPool(N,
                                           lambda: uniform_distribution(u, o),
                                           f_g=lambda: np.ones(1),
                                           f_k=lambda: 1,
                                           is_diagonal_one=True,
                                           save_path=session_name)

            # Quick single community simulation
            CommunitiesLibrary = np.zeros([num_C, N])
            all_species = np.random.permutation(N)
            for i in range(num_C):
                selected = all_species[i*num_S:(i+1)*num_S]
                CommunitiesLibrary[i, selected] = 1

            y = np.random.rand(N) * 0.1
            sc_list = {}
            for idx in range(num_C):
                y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
                y1[y1 < threshold] = 0
                sc_list[idx] = y1.tolist()

            # Store with interaction matrix
            all_results[f"{u:.1f}"][f"rep_{rep:03d}"] = {
                "sc_list": sc_list,
                "parameters": {
                    "seed": seed,
                    "u": u,
                    "interaction_matrix": I.tolist(),  # Save full matrix
                    "interaction_matrix_stats": {
                        "mean": float(np.mean(I[np.triu_indices(N, k=1)])),
                        "std": float(np.std(I[np.triu_indices(N, k=1)]))
                    }
                }
            }
            print("✓")

    # Save test results
    output_file = session_name + '/test_matrices.json'
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB")

    # Verify
    print("\n" + "="*50)
    print("VERIFICATION")
    print("="*50)

    with open(output_file, 'r') as f:
        loaded = json.load(f)

    for u_key in loaded.keys():
        for rep_key in loaded[u_key].keys():
            rep_data = loaded[u_key][rep_key]
            I_matrix = np.array(rep_data['parameters']['interaction_matrix'])

            print(f"\n{u_key}, {rep_key}:")
            print(f"  Matrix shape: {I_matrix.shape}")
            print(f"  Diagonal all 1.0? {np.allclose(np.diag(I_matrix), 1.0)}")
            print(f"  Mean: {rep_data['parameters']['interaction_matrix_stats']['mean']:.4f}")
            print(f"  Communities: {len(rep_data['sc_list'])}")

    print("\n✅ TEST PASSED! Matrix saving works correctly.")
    print(f"📁 Test data saved to: {output_file}")
    print(f"💡 You can now run the full simulation with 200 reps.")

    return output_file

if __name__ == "__main__":
    test_matrix_save()
