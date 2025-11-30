#!/usr/bin/env python3
"""
Create main pH analysis plots with academic paper styling
- Histogram of optimal pH for species
- Histogram of pH after 15 hours
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import os

# Set academic paper style parameters
def set_academic_style():
    """Set matplotlib parameters for academic paper quality figures"""
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
    rcParams['font.size'] = 12
    rcParams['axes.titlesize'] = 14
    rcParams['axes.labelsize'] = 12
    rcParams['xtick.labelsize'] = 11
    rcParams['ytick.labelsize'] = 11
    rcParams['legend.fontsize'] = 11
    rcParams['figure.titlesize'] = 16
    rcParams['axes.linewidth'] = 1.2
    rcParams['xtick.major.width'] = 1.2
    rcParams['ytick.major.width'] = 1.2
    rcParams['xtick.minor.width'] = 0.8
    rcParams['ytick.minor.width'] = 0.8
    rcParams['axes.spines.top'] = False
    rcParams['axes.spines.right'] = False
    rcParams['axes.grid'] = True
    rcParams['grid.alpha'] = 0.3
    rcParams['grid.linewidth'] = 0.8
    rcParams['savefig.dpi'] = 300
    rcParams['savefig.bbox'] = 'tight'
    rcParams['savefig.pad_inches'] = 0.1

def load_ph_response_data():
    """Load pH response data for isolates"""
    print("Loading pH response data...")
    
    file_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/2209_pHresponse_Isolates.xlsx'
    
    # pH levels to analyze
    ph_levels = ['4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
    
    all_data = []
    
    for ph in ph_levels:
        try:
            # Read the sheet
            df = pd.read_excel(file_path, sheet_name=ph, header=None)
            
            # Find where the actual data starts (look for row with 'A')
            data_start = None
            for i in range(len(df)):
                if df.iloc[i, 0] == 'A':
                    data_start = i
                    break
            
            if data_start is None:
                continue
                
            # Extract the 8x12 plate data (A-H rows, 1-12 columns)
            for row_idx, row_label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
                if data_start + row_idx >= len(df):
                    break
                    
                row_data = df.iloc[data_start + row_idx, 1:13]  # Columns 1-12
                
                for col_idx, od_value in enumerate(row_data):
                    if pd.notna(od_value) and isinstance(od_value, (int, float)):
                        all_data.append({
                            'pH': float(ph),
                            'Well': f"{row_label}{col_idx+1}",
                            'OD': float(od_value),
                            'Species': f"{row_label}{col_idx+1}"
                        })
        except Exception as e:
            print(f"Error reading pH {ph}: {e}")
            continue
    
    df_response = pd.DataFrame(all_data)
    print(f"✓ Loaded {len(df_response)} data points for {len(df_response['Species'].unique())} species")
    
    return df_response

def load_ph_change_data():
    """Load pH change data after 15 hours"""
    print("Loading pH change data...")
    
    file_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/230623_pH.xlsx'
    
    try:
        # Read the 'after 15h' sheet
        df = pd.read_excel(file_path, sheet_name='after 15h', header=None)
        
        # Find where the actual data starts
        data_start = None
        for i in range(len(df)):
            if df.iloc[i, 0] == 'A':
                data_start = i
                break
        
        if data_start is None:
            print("Could not find data start")
            return pd.DataFrame()
        
        all_data = []
        
        # Extract the data
        for row_idx, row_label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            if data_start + row_idx >= len(df):
                break
                
            row_data = df.iloc[data_start + row_idx, 1:13]  # Columns 1-12
            
            for col_idx, ph_change in enumerate(row_data):
                if pd.notna(ph_change) and isinstance(ph_change, (int, float)):
                    all_data.append({
                        'Well': f"{row_label}{col_idx+1}",
                        'pH_final': float(ph_change) / 10.0,  # Convert to actual pH units
                        'Species': f"{row_label}{col_idx+1}"
                    })
        
        df_change = pd.DataFrame(all_data)
        print(f"✓ Loaded pH change data for {len(df_change)} species")
        
    except Exception as e:
        print(f"Error loading pH change data: {e}")
        df_change = pd.DataFrame()
    
    return df_change

def analyze_ph_preference(df_response):
    """Analyze pH preference for each species"""
    results = []
    
    for species in df_response['Species'].unique():
        species_data = df_response[df_response['Species'] == species]
        
        # Calculate mean OD for each pH
        mean_data = species_data.groupby('pH')['OD'].mean().reset_index()
        
        # Find optimal pH (highest mean OD)
        optimal_idx = mean_data['OD'].idxmax()
        optimal_ph = mean_data.loc[optimal_idx, 'pH']
        optimal_od = mean_data.loc[optimal_idx, 'OD']
        
        results.append({
            'Species': species,
            'Optimal_pH': optimal_ph,
            'Optimal_OD': optimal_od
        })
    
    return pd.DataFrame(results)

def create_optimal_ph_histogram(df_preference, output_dir):
    """Create academic-style histogram of optimal pH"""
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create histogram
    n, bins, patches = ax.hist(df_preference['Optimal_pH'], 
                              bins=np.arange(3.5, 10.0, 1.0),
                              edgecolor='black', 
                              linewidth=1.2,
                              alpha=0.7,
                              color='steelblue')
    
    # Color bars by category
    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd', '#8c564b']  # Academic color palette
    for i, patch in enumerate(patches):
        patch.set_facecolor(colors[i % len(colors)])
        patch.set_alpha(0.8)
    
    # Customize axes
    ax.set_xlabel('Optimal pH for Growth', fontweight='bold')
    ax.set_ylabel('Number of Species', fontweight='bold')
    ax.set_title('Distribution of pH Optima Among Bacterial Isolates', fontweight='bold', pad=20)
    
    # Set x-axis ticks
    ax.set_xticks([4, 5, 6, 7, 8, 9])
    ax.set_xlim(3.5, 9.5)
    
    # Add statistical annotations
    total_species = len(df_preference)
    acidophiles = len(df_preference[df_preference['Optimal_pH'] <= 5.0])
    neutrophiles = len(df_preference[(df_preference['Optimal_pH'] > 5.0) & 
                                   (df_preference['Optimal_pH'] < 8.0)])
    alkaliphiles = len(df_preference[df_preference['Optimal_pH'] >= 8.0])
    
    # Add text box with statistics
    stats_text = f'n = {total_species} species\n'
    stats_text += f'Acidophiles: {acidophiles} ({acidophiles/total_species*100:.1f}%)\n'
    stats_text += f'Neutrophiles: {neutrophiles} ({neutrophiles/total_species*100:.1f}%)\n'
    stats_text += f'Alkaliphiles: {alkaliphiles} ({alkaliphiles/total_species*100:.1f}%)'
    
    ax.text(0.02, 0.98, stats_text, 
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'),
            fontsize=10)
    
    # Add pH regime labels
    ax.axvspan(3.5, 5.5, alpha=0.1, color='red', zorder=0)
    ax.axvspan(5.5, 7.5, alpha=0.1, color='green', zorder=0)
    ax.axvspan(7.5, 9.5, alpha=0.1, color='blue', zorder=0)
    
    # Add regime labels at top
    ax.text(4.5, ax.get_ylim()[1] * 0.95, 'Acidic', ha='center', fontsize=10, 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.3))
    ax.text(6.5, ax.get_ylim()[1] * 0.95, 'Neutral', ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='green', alpha=0.3))
    ax.text(8.5, ax.get_ylim()[1] * 0.95, 'Alkaline', ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='blue', alpha=0.3))
    
    # Fine-tune layout
    plt.tight_layout()
    
    # Save figure
    fig.savefig(f"{output_dir}/optimal_pH_histogram.svg", dpi=300, bbox_inches='tight')
    fig.savefig(f"{output_dir}/optimal_pH_histogram.png", dpi=300, bbox_inches='tight')
    fig.savefig(f"{output_dir}/optimal_pH_histogram.pdf", dpi=300, bbox_inches='tight')
    
    print(f"✓ Saved optimal pH histogram")
    return fig

def create_ph_after_15h_histogram(df_change, output_dir):
    """Create academic-style histogram of pH after 15 hours"""
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create histogram
    n, bins, patches = ax.hist(df_change['pH_final'], 
                              bins=np.arange(3.0, 8.5, 0.5),
                              edgecolor='black', 
                              linewidth=1.2,
                              alpha=0.7,
                              color='darkslategray')
    
    # Color bars by pH range
    colors = ['#d62728', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#1f77b4', '#aec7e8', '#9467bd', '#c5b0d5']
    for i, patch in enumerate(patches):
        patch.set_facecolor(colors[i % len(colors)])
        patch.set_alpha(0.8)
    
    # Customize axes
    ax.set_xlabel('Final pH After 15 Hours', fontweight='bold')
    ax.set_ylabel('Number of Species', fontweight='bold')
    ax.set_title('Distribution of Final pH Values After 15-Hour Incubation\n(Initial pH: 6.5)', 
                 fontweight='bold', pad=20)
    
    # Set x-axis ticks
    ax.set_xticks(np.arange(3.0, 8.5, 0.5))
    ax.set_xlim(2.8, 8.2)
    
    # Add vertical line for initial pH
    ax.axvline(x=6.5, color='red', linestyle='--', linewidth=2, alpha=0.8, label='Initial pH (6.5)')
    
    # Add statistical annotations
    total_species = len(df_change)
    acidifiers = len(df_change[df_change['pH_final'] < 6.5])
    alkalizers = len(df_change[df_change['pH_final'] > 6.5])
    neutral = len(df_change[df_change['pH_final'] == 6.5])
    
    mean_final_ph = df_change['pH_final'].mean()
    std_final_ph = df_change['pH_final'].std()
    
    # Add text box with statistics
    stats_text = f'n = {total_species} species\n'
    stats_text += f'Mean final pH: {mean_final_ph:.2f} ± {std_final_ph:.2f}\n'
    stats_text += f'Acidifiers: {acidifiers} ({acidifiers/total_species*100:.1f}%)\n'
    stats_text += f'Alkalizers: {alkalizers} ({alkalizers/total_species*100:.1f}%)\n'
    stats_text += f'No change: {neutral} ({neutral/total_species*100:.1f}%)'
    
    ax.text(0.98, 0.98, stats_text, 
            transform=ax.transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'),
            fontsize=10)
    
    # Add pH change direction arrows and labels
    ax.annotate('', xy=(5.0, ax.get_ylim()[1] * 0.8), xytext=(6.5, ax.get_ylim()[1] * 0.8),
                arrowprops=dict(arrowstyle='<-', lw=2, color='red', alpha=0.7))
    ax.text(4.5, ax.get_ylim()[1] * 0.85, 'Acidification', ha='center', fontsize=10, 
            color='red', fontweight='bold')
    
    ax.annotate('', xy=(7.5, ax.get_ylim()[1] * 0.8), xytext=(6.5, ax.get_ylim()[1] * 0.8),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue', alpha=0.7))
    ax.text(7.8, ax.get_ylim()[1] * 0.85, 'Alkalization', ha='center', fontsize=10, 
            color='blue', fontweight='bold')
    
    # Add legend
    ax.legend(loc='upper left', framealpha=0.8)
    
    # Fine-tune layout
    plt.tight_layout()
    
    # Save figure
    fig.savefig(f"{output_dir}/pH_after_15h_histogram.svg", dpi=300, bbox_inches='tight')
    fig.savefig(f"{output_dir}/pH_after_15h_histogram.png", dpi=300, bbox_inches='tight')
    fig.savefig(f"{output_dir}/pH_after_15h_histogram.pdf", dpi=300, bbox_inches='tight')
    
    print(f"✓ Saved pH after 15h histogram")
    return fig

def main():
    """Main function to create academic-style pH histograms"""
    
    # Set academic style
    set_academic_style()
    
    # Create output directory
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=== Creating Main pH Analysis Plots ===")
    
    # Load data
    df_response = load_ph_response_data()
    df_change = load_ph_change_data()
    
    if df_response.empty:
        print("Error: No pH response data found!")
        return
    
    # Analyze pH preferences
    print("\nAnalyzing pH preferences...")
    df_preference = analyze_ph_preference(df_response)
    
    # Create main plots
    print("\nCreating main plots with academic styling...")
    
    # Plot 1: Optimal pH histogram
    print("\n1. Creating optimal pH histogram...")
    fig1 = create_optimal_ph_histogram(df_preference, output_dir)
    
    # Plot 2: pH after 15h histogram  
    if not df_change.empty:
        print("\n2. Creating pH after 15h histogram...")
        fig2 = create_ph_after_15h_histogram(df_change, output_dir)
    else:
        print("\n2. Skipping pH after 15h histogram - no data available")
    
    print("\n✓ Main plots created successfully!")
    print(f"✓ Files saved to: {output_dir}/")
    print("  - optimal_pH_histogram.svg/png/pdf")
    print("  - pH_after_15h_histogram.svg/png/pdf")

if __name__ == "__main__":
    main()