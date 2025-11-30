#!/usr/bin/env python3
"""Check pH data structure in detail"""

import pandas as pd

# Check first file - look for actual data
print("Checking 2209_pHresponse_Isolates.xlsx in detail...")
file1 = '/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/2209_pHresponse_Isolates.xlsx'

# Look at pH 7.0 sheet in more detail
df = pd.read_excel(file1, sheet_name='7.0')
print(f"\nSheet '7.0' full preview:")
print(f"Shape: {df.shape}")

# Find where the actual data starts (look for well labels like A1, A2, etc)
for i in range(min(20, len(df))):
    row_str = str(df.iloc[i].values)
    if 'A1' in row_str or 'Well' in row_str or '<>' in row_str:
        print(f"Row {i}: {row_str[:200]}...")
        
# Also check if there's a pattern in the data
print("\n\nLooking for data patterns...")
df_no_header = pd.read_excel(file1, sheet_name='7.0', header=None)
for i in range(min(df_no_header.shape[0], 40)):
    row = df_no_header.iloc[i]
    if any(str(val).strip() in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] for val in row.values):
        print(f"Row {i}: {list(row.values)}")
        # Print next few rows too
        for j in range(i+1, min(i+5, df_no_header.shape[0])):
            print(f"Row {j}: {list(df_no_header.iloc[j].values)}")
        break

# Check the second file similarly
print("\n\n\nChecking 230623_pH.xlsx in detail...")
file2 = '/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/230623_pH.xlsx'
df2 = pd.read_excel(file2, sheet_name='after 15h', header=None)
print(f"\nSheet 'after 15h' preview:")
for i in range(min(df2.shape[0], 40)):
    row = df2.iloc[i]
    if any(str(val).strip() in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] for val in row.values):
        print(f"Row {i}: {list(row.values)}")
        # Print next few rows too
        for j in range(i+1, min(i+5, df2.shape[0])):
            print(f"Row {j}: {list(df2.iloc[j].values)}")
        break