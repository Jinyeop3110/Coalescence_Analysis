#!/usr/bin/env python3
"""
examine_sequences.py
Quick script to examine the structure of processed sequences data
"""

import pandas as pd
import numpy as np

# Load processed sequences data
sequences_path = '/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Postprocessed/processed_Sequences_synthetic.xlsx'
df = pd.read_excel(sequences_path)

print('Dataset shape:', df.shape)
print('\nFirst few columns:')
print(df.columns[:10].tolist())
print('\nSample of first few rows and columns:')
print(df.iloc[:5, :6])
print('\nASV columns (excluding SampleIDX):')
asv_cols = [col for col in df.columns if col != 'SampleIDX']
print('Number of ASVs:', len(asv_cols))
print('First 10 ASV names:', asv_cols[:10])

# Check abundance distributions
print('\nAbundance statistics for first ASV:')
print(df[asv_cols[0]].describe())

# Check which samples have high abundance for first few ASVs
print('\nTop samples for first ASV:', asv_cols[0])
top_samples = df.nlargest(5, asv_cols[0])[['SampleIDX', asv_cols[0]]]
print(top_samples)