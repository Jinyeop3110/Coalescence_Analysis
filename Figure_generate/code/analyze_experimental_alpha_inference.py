#!/usr/bin/env python3
"""
Analyze how to infer alpha values from experimental pairwise data.

From LV model:
dN1/dt = r1*N1*(1 - (N1 + α12*N2)/K1)
dN2/dt = r2*N2*(1 - (N2 + α21*N1)/K2)

At equilibrium in pairwise culture:
If both species coexist:
  N1* = (1 - α12) / (1 - α12*α21) * K1
  N2* = (1 - α21) / (1 - α12*α21) * K2

The ratio N1*/(N1*+N2*) is what we measure in pairwise colony counting.

If species 1 excludes species 2 (α12 < 1 < α21):
  N1* = K1, N2* = 0

If species 2 excludes species 1 (α21 < 1 < α12):
  N1* = 0, N2* = K2

The pairwise ratio p = N1*/(N1*+N2*) tells us:
- p ≈ 1: species 1 strongly dominates (likely α21 > 1, α12 < 1)
- p ≈ 0: species 2 strongly dominates (likely α12 > 1, α21 < 1)
- p ≈ 0.5: coexistence (both α < 1)
- p close to extremes (0 or 1): at least one α > 1

For the bistability filter (both α > 1), we look for contradictory patterns:
- If p12 ≈ 1 (sp1 wins when paired with sp2)
- AND p21 ≈ 0 (sp1 wins when paired with sp2 from other direction)
- This is CONSISTENT - species 1 dominates

But if:
- p12 ≈ 1 (sp1 wins) BUT ALSO p21 ≈ 1 (sp1 still wins from other perspective)
This would be contradictory and might indicate measurement error.

Actually, for inferring both α > 1 (mutual inhibition stronger than self-limitation):
This creates bistability where outcome depends on initial conditions.

The key insight: In pairwise experiments, we can't directly infer both α > 1 from
a SINGLE measurement because the outcome depends on initial conditions.

However, we can use the ratio values to estimate α:
From the equilibrium: p = N1*/(N1*+N2*)

If we assume K1 ≈ K2 (similar carrying capacities):
p ≈ (1 - α12) / (2 - α12 - α21)

Rearranging:
α12 ≈ (1 - 2p + p*α21) / (1 - p)
α21 ≈ (1 - 2(1-p) + (1-p)*α12) / p

This is a coupled system. We can solve iteratively or use the fact that:
If p is known, and we assume equal competitive effects (α12 = α21 = α):
p = (1 - α) / (2 - 2α) = (1-α)/(2(1-α)) = 1/2

This means equal α gives p = 0.5 regardless of α value!

So the ratio p only tells us the ASYMMETRY, not absolute values.

For a simpler heuristic to filter both α > 1:
- If BOTH species show strong exclusion in different contexts
- Look for cases where in one pairwise the ratio is extreme

Actually, the most practical approach:
Use the fact that if both α > 1, the system is bistable and the outcome
depends on initial conditions. In pairwise experiments with equal inoculum:
- Random outcome (50-50 chance either species wins)
- High variance across replicates

Let me check if there are replicate measurements in the data.
"""

import pandas as pd
import numpy as np

# Load the pairwise data
Pairwise_Count_data_path = "../../Postprocessed/PairwiseColonyCountings_processed_230915.xlsx"

print("="*80)
print("ANALYZING EXPERIMENTAL PAIRWISE DATA STRUCTURE")
print("="*80)

# Check what sheets are available
xl_file = pd.ExcelFile(Pairwise_Count_data_path)
print(f"\nAvailable sheets: {xl_file.sheet_names}")

# Load MN (medium nitrogen) pairwise data
print("\n" + "="*80)
print("LOADING MN PAIRWISE DATA")
print("="*80)

sheet1_idx = 3 + 1*2  # MN sheet 1 (index 1 for MN)
sheet2_idx = 4 + 1*2  # MN sheet 2

Data_1 = pd.read_excel(Pairwise_Count_data_path, sheet_name=sheet1_idx)
Data_2 = pd.read_excel(Pairwise_Count_data_path, sheet_name=sheet2_idx)

print(f"\nSheet {sheet1_idx} ({xl_file.sheet_names[sheet1_idx]}):")
print(f"Shape: {Data_1.shape}")
print(f"Columns: {Data_1.columns.tolist()}")
print(f"\nFirst few rows:")
print(Data_1.head())

print(f"\nSheet {sheet2_idx} ({xl_file.sheet_names[sheet2_idx]}):")
print(f"Shape: {Data_2.shape}")
print(f"Columns: {Data_2.columns.tolist()}")
print(f"\nFirst few rows:")
print(Data_2.head())

# Extract the data matrices
Data_1_matrix = np.array(Data_1.values[:,1:])
Data_2_matrix = np.array(Data_2.values[:,1:])

print(f"\nData_1 matrix shape: {Data_1_matrix.shape}")
print(f"Data_2 matrix shape: {Data_2_matrix.shape}")

print("\n" + "="*80)
print("STRATEGY FOR INFERRING BOTH α > 1")
print("="*80)

print("""
For Lotka-Volterra pairwise competition:
- α12 = competitive effect of species 2 ON species 1
- α21 = competitive effect of species 1 ON species 2

From pairwise colony counts, we have:
- N1_pairwise = colonies of species 1 when grown with species 2
- N2_pairwise = colonies of species 2 when grown with species 1
- N1_mono = colonies of species 1 in monoculture
- N2_mono = colonies of species 2 in monoculture

The code already computes:
- ratio = N1_pairwise/N1_mono / (N1_pairwise/N1_mono + N2_pairwise/N2_mono)

To infer α, we can use competitive reduction:
- α12 ≈ 1 - (N1_pairwise/N1_mono) / (N2_pairwise/N2_mono)
  (How much species 2 reduces species 1, relative to species 2's abundance)

Actually, a simpler empirical approach:
- If N1_pairwise << N1_mono: species 1 is strongly inhibited (α12 might be > 1)
- If N2_pairwise << N2_mono: species 2 is strongly inhibited (α21 might be > 1)
- If BOTH are strongly reduced: both α > 1 (mutual inhibition)

Threshold: reduction > 50% might indicate α > 1

Let me check the actual data to see the distribution.
""")

# Load monoculture data for comparison
print("\n" + "="*80)
print("LOADING MONOCULTURE DATA")
print("="*80)

Mono_Data = pd.read_excel(Pairwise_Count_data_path, sheet_name=1)  # MN monoculture
print(f"Monoculture data shape: {Mono_Data.shape}")
print(f"\nFirst few rows:")
print(Mono_Data.head())

Mono_matrix = np.transpose(np.array(Mono_Data.values[:,1:]))
print(f"\nMonoculture matrix shape: {Mono_matrix.shape}")
print(f"Mean monoculture counts per species: {np.mean(Mono_matrix, axis=1)}")

# Calculate reduction ratios
print("\n" + "="*80)
print("CALCULATING COMPETITIVE REDUCTION")
print("="*80)

mono_means = np.mean(Mono_matrix, axis=1)

print(f"\nExample calculations for species pairs:")
for i in range(min(3, 12)):
    for j in range(i+1, min(i+3, 12)):
        if not np.isnan(Data_1_matrix[i,j]):
            n1_pair = Data_1_matrix[i,j]
            n2_pair = Data_2_matrix[i,j]
            n1_mono = mono_means[i]
            n2_mono = mono_means[j]

            reduction_1 = 1 - (n1_pair / n1_mono)
            reduction_2 = 1 - (n2_pair / n2_mono)

            print(f"\nSpecies {i} vs Species {j}:")
            print(f"  Sp{i}: {n1_pair:.1f} (paired) vs {n1_mono:.1f} (mono) → {reduction_1*100:.1f}% reduction")
            print(f"  Sp{j}: {n2_pair:.1f} (paired) vs {n2_mono:.1f} (mono) → {reduction_2*100:.1f}% reduction")

            # Heuristic: both reduced > 50% suggests both α > 1
            if reduction_1 > 0.5 and reduction_2 > 0.5:
                print(f"  ⚠ BOTH STRONGLY REDUCED → Likely both α > 1 (bistability)")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("""
To filter experimental data for both α > 1:
1. Calculate reduction = 1 - (N_pairwise / N_mono) for both species
2. If BOTH reductions > threshold (e.g., 0.5 or 0.7), exclude the case
3. This heuristic identifies mutual strong inhibition (bistability regime)
""")
