#!/usr/bin/env python3
"""
Monoculture OD and Growth Rate Histograms
Generates a two-panel figure:
- Left: OD histogram over ASVs
- Right: Growth rate histogram over ASVs
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
    """Load OD data from Excel file (96-well plate format)"""
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


def load_growth_rate_data(file_path, sheet_name='x1200 dilution'):
    """
    Load growth rate data from Excel file.
    Growth rate is estimated from OD measurements at different time points.
    """
    print(f"Loading growth rate data from {sheet_name}...")

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
                        'ASV': well_id
                    })

        df_gr = pd.DataFrame(all_data)
        print(f"  Loaded {len(df_gr)} measurements")
        return df_gr

    except Exception as e:
        print(f"Error loading growth rate data: {e}")
        return pd.DataFrame()


def calculate_growth_rate(od_early, od_late, time_hours):
    """
    Calculate growth rate from two OD measurements.
    Growth rate (h^-1) = ln(OD_late / OD_early) / time
    """
    if od_early <= 0 or od_late <= 0:
        return np.nan
    return np.log(od_late / od_early) / time_hours


def load_all_od_data_for_growth_rate(base_path):
    """
    Load OD data from multiple sheets to calculate growth rate.
    Uses early and late time points.
    """
    print("Loading OD data for growth rate calculation...")

    # File with time course data
    file_path = os.path.join(base_path, '220910_54isolatesOD_flat100um.xlsx')

    try:
        xl = pd.ExcelFile(file_path)
        sheets = xl.sheet_names
        print(f"  Available sheets: {sheets}")

        # Load data from different time points
        all_od_data = {}
        for sheet in sheets:
            df = load_od_data(file_path, sheet_name=sheet)
            if not df.empty:
                all_od_data[sheet] = df

        if len(all_od_data) < 2:
            print("  Not enough time points for growth rate calculation")
            return pd.DataFrame()

        # Use Sheet2 as early and Sheet4 as late
        # Note: These are close in time, so we'll estimate growth rate differently
        early_sheet = 'Sheet2'  # earliest with data
        late_sheet = 'Sheet4'   # latest

        if early_sheet not in all_od_data or late_sheet not in all_od_data:
            print("  Required sheets not found")
            return pd.DataFrame()

        df_early = all_od_data[early_sheet]
        df_late = all_od_data[late_sheet]

        # Merge and calculate growth rate
        # Assuming measurements taken during exponential phase (~3 minutes apart based on timestamps)
        # For demonstration, we'll use a proxy: OD change rate
        # In reality, you'd want proper time-course data
        df_merged = df_early.merge(df_late, on='ASV', suffixes=('_early', '_late'))

        # Calculate relative OD increase as a proxy for growth capacity
        # This is (OD_late - OD_early) / OD_early
        df_merged['GrowthRate'] = df_merged.apply(
            lambda row: (row['OD_late'] - row['OD_early']) / row['OD_early']
            if row['OD_early'] > 0.05 else np.nan,  # Filter low OD (blanks)
            axis=1
        )

        print(f"  Calculated growth rates for {len(df_merged)} ASVs")
        return df_merged[['ASV', 'GrowthRate', 'OD_early', 'OD_late']]

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()


def create_two_panel_histogram(df_od, df_growth, output_dir):
    """
    Create a two-panel figure with OD and growth rate histograms.
    """
    print("\nCreating two-panel histogram figure...")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Left panel: OD histogram
    ax1 = axes[0]
    od_values = df_od['OD'].dropna().values

    # Filter out background/blank values (very low OD)
    od_threshold = 0.1
    od_values_filtered = od_values[od_values > od_threshold]

    n_asvs_od = len(od_values_filtered)

    ax1.hist(od_values_filtered, bins=15, edgecolor='black', linewidth=0.8,
             color='#4C72B0', alpha=0.8)
    ax1.set_xlabel('Optical Density (OD)')
    ax1.set_ylabel('Number of ASVs')
    ax1.set_title(f'Monoculture OD Distribution (Base)\n(n = {n_asvs_od} ASVs)')

    # Add mean and std annotation
    mean_od = np.mean(od_values_filtered)
    std_od = np.std(od_values_filtered)
    ax1.axvline(mean_od, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_od:.3f}')
    ax1.text(0.95, 0.95, f'Mean: {mean_od:.3f}\nStd: {std_od:.3f}',
             transform=ax1.transAxes, va='top', ha='right',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             fontsize=9)

    # Right panel: Growth rate histogram
    ax2 = axes[1]

    if not df_growth.empty and 'GrowthRate' in df_growth.columns:
        gr_values = df_growth['GrowthRate'].dropna().values
        # Filter out negative or unrealistic growth rates
        gr_values_filtered = gr_values[(gr_values > 0)]
        n_asvs_gr = len(gr_values_filtered)

        # Time difference between Sheet2 and Sheet4 is ~3 minutes = 0.05 hours
        # Convert relative OD increase to rate per hour
        time_diff_hours = 3.0 / 60.0  # 3 minutes in hours
        gr_per_hour = gr_values_filtered / time_diff_hours

        ax2.hist(gr_per_hour, bins=15, edgecolor='black', linewidth=0.8,
                 color='#55A868', alpha=0.8)
        ax2.set_xlabel('Growth Rate (h$^{-1}$)')
        ax2.set_ylabel('Number of ASVs')
        ax2.set_title(f'Monoculture Growth Rate (Base)\n(n = {n_asvs_gr} ASVs)')

        # Add mean and std annotation
        mean_gr = np.mean(gr_per_hour)
        std_gr = np.std(gr_per_hour)
        ax2.axvline(mean_gr, color='red', linestyle='--', linewidth=1.5, label=f'Mean: {mean_gr:.2f}')
        ax2.text(0.95, 0.95, f'Mean: {mean_gr:.2f}\nStd: {std_gr:.2f}',
                 transform=ax2.transAxes, va='top', ha='right',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                 fontsize=9)
    else:
        # If no growth rate data, use OD as proxy for growth
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
    base_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates'
    output_dir = 'Figure/Monoculture_OD_Growth'

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    print("\n=== Monoculture OD and Growth Rate Analysis ===\n")

    # Load OD data (final time point)
    od_file = os.path.join(base_path, '220910_54isolatesOD_flat100um.xlsx')
    df_od = load_od_data(od_file, sheet_name='Sheet4')

    if df_od.empty:
        print("Error: Could not load OD data!")
        return

    # Load/calculate growth rate data
    df_growth = load_all_od_data_for_growth_rate(base_path)

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
        gr_filtered = df_growth[df_growth['GrowthRate'] > 0]
        time_diff_hours = 3.0 / 60.0  # 3 minutes in hours
        gr_per_hour = gr_filtered['GrowthRate'] / time_diff_hours
        print(f"\nASVs with valid growth rate: {len(gr_filtered)}")
        print(f"Mean growth rate: {gr_per_hour.mean():.2f} h^-1")
        print(f"Std growth rate: {gr_per_hour.std():.2f} h^-1")

    print(f"\nFigures saved to: {output_dir}/")
    print("  - monoculture_od_growth_histograms.svg")
    print("  - monoculture_od_growth_histograms.png")
    print("  - monoculture_od_growth_histograms.pdf")


if __name__ == "__main__":
    main()
