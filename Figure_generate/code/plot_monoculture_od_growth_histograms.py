#!/usr/bin/env python3
"""
Monoculture OD and Growth Rate Histograms
Generates a two-panel figure:
- Left: OD histogram over ASVs
- Right: Growth rate histogram over ASVs

Growth rates are computed from full kinetic time-course data (480 cycles, ~3 min intervals)
using exponential-phase log-linear regression, replicating the MATLAB GRcalculate_500 method.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os


def set_academic_style():
    """Set matplotlib parameters for academic paper quality figures"""
    rcParams['font.family'] = 'Arial'
    rcParams['font.size'] = 10
    rcParams['axes.titlesize'] = 12
    rcParams['axes.labelsize'] = 11
    rcParams['xtick.labelsize'] = 10
    rcParams['ytick.labelsize'] = 10
    rcParams['legend.fontsize'] = 9
    rcParams['axes.linewidth'] = 1.0
    rcParams['xtick.major.width'] = 1.0
    rcParams['ytick.major.width'] = 1.0
    rcParams['axes.spines.top'] = False
    rcParams['axes.spines.right'] = False
    rcParams['savefig.dpi'] = 300
    rcParams['savefig.bbox'] = 'tight'


def load_od_data(file_path, sheet_name='Sheet4'):
    """Load OD data from Excel file (96-well plate format, single time point)"""
    print(f"Loading OD data from {sheet_name}...")

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # Find where the actual data starts (look for row with 'A')
        data_start = None
        for i in range(len(df)):
            if df.iloc[i, 0] == 'A':
                data_start = i
                break

        if data_start is None:
            print("Could not find data start row")
            return pd.DataFrame()

        all_data = []

        # Extract the 8x12 plate data (A-H rows, 1-12 columns)
        for row_idx, row_label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            if data_start + row_idx >= len(df):
                break

            row_data = df.iloc[data_start + row_idx, 1:13]  # Columns 1-12

            for col_idx, od_value in enumerate(row_data):
                if pd.notna(od_value) and isinstance(od_value, (int, float)):
                    well_id = f"{row_label}{col_idx+1}"
                    all_data.append({
                        'Well': well_id,
                        'Row': row_label,
                        'Column': col_idx + 1,
                        'OD': float(od_value),
                        'ASV': well_id  # Using well as ASV identifier
                    })

        df_od = pd.DataFrame(all_data)
        print(f"  Loaded {len(df_od)} OD measurements")
        return df_od

    except Exception as e:
        print(f"Error loading OD data: {e}")
        return pd.DataFrame()


def gr_calculate_500(odt, time_s):
    """
    Python port of GRcalculate_500.m
    Computes exponential growth rate by fitting ln(OD) vs time in the
    exponential phase window.

    Parameters:
        odt: array of OD values over time
        time_s: array of time values in seconds

    Returns:
        growth rate in h^-1
    """
    odt = np.abs(odt)

    # Remove NaNs
    valid = ~np.isnan(odt) & ~np.isnan(time_s)
    odt = odt[valid]
    time = time_s[valid]

    if len(odt) < 2:
        return np.nan

    maxval = np.max(odt)
    maxval_2 = np.mean(odt[odt > maxval * 0.9])

    # Top window: first index where OD exceeds 80% of plateau
    top_idx = np.where(odt > maxval_2 * 0.8)[0]
    if len(top_idx) == 0:
        return np.nan
    topwindowind = top_idx[0]

    # Bottom window: max of (last index before 2000s, first index with OD > 0.005)
    bottom_candidates = np.where(time < 2000)[0]
    od_above = np.where(odt > 0.005)[0]

    if len(bottom_candidates) == 0 or len(od_above) == 0:
        return np.nan
    bottomwindowind = max(bottom_candidates[-1], od_above[0])

    if bottomwindowind >= topwindowind:
        return np.nan

    # Linear fit of log(OD) vs time in seconds
    x = time[bottomwindowind:topwindowind + 1]
    y = np.log(odt[bottomwindowind:topwindowind + 1])

    # Filter out -inf or nan
    valid2 = np.isfinite(y)
    x = x[valid2]
    y = y[valid2]

    if len(x) < 2:
        return np.nan

    # Least squares: y = b0 + b1*x
    X = np.column_stack([np.ones(len(x)), x])
    b, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    growth_rate = b[1]  # slope in s^-1
    gr_per_hour = growth_rate * 3600  # convert to h^-1

    return gr_per_hour


def load_kinetic_growth_data(file_path):
    """
    Load full kinetic time-course OD data from Tecan plate reader Excel file.
    Computes growth rates using log-linear regression (GRcalculate_500 method).

    Parameters:
        file_path: path to the kinetic data Excel file (e.g., MN_ISO_GR.xlsx)

    Returns:
        DataFrame with columns ['Well', 'GrowthRate']
    """
    print(f"Loading kinetic growth data from {file_path}...")

    df = pd.read_excel(file_path, sheet_name='Sheet2', header=None)

    # Extract time vector (row with 'Time [s]')
    time_row = None
    for i in range(len(df)):
        cell = str(df.iloc[i, 0])
        if 'Time [s]' in cell:
            time_row = i
            break

    if time_row is None:
        print("  Could not find time row")
        return pd.DataFrame()

    time_s = df.iloc[time_row, 1:].values.astype(float)
    # Remove trailing NaNs
    valid_time = ~np.isnan(time_s)
    time_s = time_s[valid_time]
    n_timepoints = len(time_s)
    print(f"  Time points: {n_timepoints}, range: {time_s[0]:.0f} to {time_s[-1]:.0f} s ({time_s[-1]/3600:.1f} h)")

    # Extract well data (rows after time row + 1 for temperature)
    data_start = time_row + 2  # skip Temp row
    results = []

    for i in range(data_start, len(df)):
        label = str(df.iloc[i, 0])
        if label == 'nan' or label == '':
            break

        vals = df.iloc[i, 1:n_timepoints + 1].values.astype(float)
        gr = gr_calculate_500(vals, time_s)
        results.append({'Well': label, 'GrowthRate': gr})

    df_gr = pd.DataFrame(results)
    valid = df_gr['GrowthRate'].notna() & (df_gr['GrowthRate'] > 0)
    print(f"  Valid growth rates: {valid.sum()} / {len(df_gr)}")

    return df_gr


def create_two_panel_histogram(df_od, df_growth, output_dir):
    """
    Create a two-panel figure with OD and growth rate histograms.
    """
    print("\nCreating two-panel histogram figure...")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Left panel: OD histogram (all 54 isolates)
    ax1 = axes[0]
    od_values = df_od['OD'].dropna().values

    n_asvs_od = len(od_values)

    ax1.hist(od_values, bins=15, edgecolor='black', linewidth=0.8,
             color='#4C72B0', alpha=0.8)
    ax1.set_xlabel('Optical Density (OD)')
    ax1.set_ylabel('Number of ASVs')
    ax1.set_title(f'Monoculture OD Distribution (Base)\n(n = {n_asvs_od} ASVs)')

    # Add mean and std annotation
    mean_od = np.mean(od_values)
    std_od = np.std(od_values)
    ax1.axvline(mean_od, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_od:.2f}')
    ax1.text(0.95, 0.95, f'Mean: {mean_od:.2f}\nStd: {std_od:.2f}',
             transform=ax1.transAxes, va='top', ha='right',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=9)

    # Right panel: Growth rate histogram
    ax2 = axes[1]

    if not df_growth.empty and 'GrowthRate' in df_growth.columns:
        gr_values = df_growth['GrowthRate'].dropna().values
        n_asvs_gr = len(gr_values)

        ax2.hist(gr_values, bins=15, edgecolor='black', linewidth=0.8,
                 color='#55A868', alpha=0.8)
        ax2.set_xlabel('Growth Rate (h$^{-1}$)')
        ax2.set_ylabel('Number of ASVs')
        ax2.set_title(f'Monoculture Growth Rate (Base)\n(n = {n_asvs_gr} ASVs)')

        # Add mean and std annotation
        mean_gr = np.mean(gr_values)
        std_gr = np.std(gr_values)
        ax2.axvline(mean_gr, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_gr:.2f}')
        ax2.text(0.95, 0.95, f'Mean: {mean_gr:.2f}\nStd: {std_gr:.2f}',
                 transform=ax2.transAxes, va='top', ha='right',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                 fontsize=9)
    else:
        ax2.text(0.5, 0.5, 'Growth rate data\nnot available',
                 transform=ax2.transAxes, ha='center', va='center',
                 fontsize=12, color='gray')
        ax2.set_xlabel('Growth Rate (h$^{-1}$)')
        ax2.set_ylabel('Number of ASVs')
        ax2.set_title('Monoculture Growth Rate Distribution')

    plt.tight_layout()

    # Save figures
    fig.savefig(os.path.join(output_dir, 'monoculture_od_growth_histograms.svg'),
                dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'monoculture_od_growth_histograms.png'),
                dpi=300, bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'monoculture_od_growth_histograms.pdf'),
                dpi=300, bbox_inches='tight')

    print(f"  Saved figures to {output_dir}/")
    plt.close(fig)

    return fig


def main():
    """Main function to generate monoculture OD and growth rate histograms"""

    # Set style
    set_academic_style()

    # Define paths
    od_base_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates'
    gr_file_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/Isolates/MN_ISO_GR.xlsx'
    output_dir = 'Figure/Monoculture_OD_Growth'

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    print("\n=== Monoculture OD and Growth Rate Analysis ===\n")

    # Load OD data (final time point from separate experiment)
    od_file = os.path.join(od_base_path, '220910_54isolatesOD_flat100um.xlsx')
    df_od = load_od_data(od_file, sheet_name='Sheet4')

    if df_od.empty:
        print("Error: Could not load OD data!")
        return

    # Limit to first 54 isolates (our strain library size)
    N_ISOLATES = 54
    df_od = df_od.head(N_ISOLATES)
    print(f"  Truncated OD data to first {N_ISOLATES} isolates")

    # Load kinetic time-course data and compute proper growth rates
    df_growth = load_kinetic_growth_data(gr_file_path)

    # Limit to first 54 isolates
    df_growth = df_growth.head(N_ISOLATES)
    print(f"  Truncated growth data to first {N_ISOLATES} isolates")

    # Create two-panel histogram
    create_two_panel_histogram(df_od, df_growth, output_dir)

    # Print summary
    print("\n=== Summary ===")
    print(f"Total ASVs with OD data: {len(df_od)}")
    od_filtered = df_od[df_od['OD'] > 0.1]
    print(f"ASVs with OD > 0.1: {len(od_filtered)}")
    print(f"Mean OD: {od_filtered['OD'].mean():.3f}")
    print(f"Std OD: {od_filtered['OD'].std():.3f}")

    if not df_growth.empty:
        gr_filtered = df_growth[df_growth['GrowthRate'] > 0]['GrowthRate']
        print(f"\nASVs with valid growth rate: {len(gr_filtered)}")
        print(f"Mean growth rate: {gr_filtered.mean():.2f} h^-1")
        print(f"Std growth rate: {gr_filtered.std():.2f} h^-1")

    print(f"\nFigures saved to: {output_dir}/")
    print("  - monoculture_od_growth_histograms.svg")
    print("  - monoculture_od_growth_histograms.png")
    print("  - monoculture_od_growth_histograms.pdf")


if __name__ == "__main__":
    main()
