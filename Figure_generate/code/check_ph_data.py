#!/usr/bin/env python3
"""Check pH data structure"""

import pandas as pd

# Check first file
print("Checking 2209_pHresponse_Isolates.xlsx...")
file1 = '/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/2209_pHresponse_Isolates.xlsx'
xl1 = pd.ExcelFile(file1)
print(f"Sheet names: {xl1.sheet_names}")

# Check a few sheets
for sheet in xl1.sheet_names[:3]:
    df = pd.read_excel(file1, sheet_name=sheet)
    print(f"\nSheet '{sheet}':")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns[:5])}")
    if len(df) > 0:
        print(f"  First few rows:")
        print(df.head(3))

# Check second file
print("\n\nChecking 230623_pH.xlsx...")
file2 = '/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/230623_pH.xlsx'
xl2 = pd.ExcelFile(file2)
print(f"Sheet names: {xl2.sheet_names}")

# Check a few sheets
for sheet in xl2.sheet_names[:3]:
    df = pd.read_excel(file2, sheet_name=sheet)
    print(f"\nSheet '{sheet}':")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns[:5])}")
    if len(df) > 0:
        print(f"  First few rows:")
        print(df.head(3))