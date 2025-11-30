#!/usr/bin/env python3
"""
Species-wise pH Analysis
Analyzes pH effects on species growth from isolate experiments
"""

import numpy as np
import pandas as pd
import os
try:
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("Warning: matplotlib not available, will generate data only")
    MATPLOTLIB_AVAILABLE = False

def load_ph_response_data():
    """Load pH response data for isolates"""
    print("Loading pH response data...")
    
    file_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/2209_pHresponse_Isolates.xlsx'
    
    # pH levels to analyze
    ph_levels = ['4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
    
    all_data = []
    
    for ph in ph_levels:
        try:
            # Read the sheet - data starts around row 24
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
                            'Row': row_label,
                            'Column': col_idx + 1,
                            'OD': float(od_value),
                            'Species': f"{row_label}{col_idx+1}"  # Using well as species identifier
                        })
        except Exception as e:
            print(f"Error reading pH {ph}: {e}")
            continue
    
    df_response = pd.DataFrame(all_data)
    print(f"✓ Loaded {len(df_response)} data points for {len(df_response['Species'].unique())} species")
    
    return df_response

def load_ph_change_data():
    """Load pH change data after 15 hours"""
    print("\nLoading pH change data...")
    
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
                        'Row': row_label,
                        'Column': col_idx + 1,
                        'pH_change': float(ph_change) / 10.0,  # Convert to actual pH units (e.g., 65 -> 6.5)
                        'Species': f"{row_label}{col_idx+1}"
                    })
        
        df_change = pd.DataFrame(all_data)
        print(f"✓ Loaded pH change data for {len(df_change)} species")
        
    except Exception as e:
        print(f"Error loading pH change data: {e}")
        df_change = pd.DataFrame()
    
    return df_change

def plot_species_ph_response_curves(df_response):
    """Plot pH vs OD curves for all species in a single plot"""
    
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib not available, skipping plot")
        return None
    
    # Get unique species
    species_list = sorted(df_response['Species'].unique())
    n_species = len(species_list)
    
    # Create color map
    colors = cm.rainbow(np.linspace(0, 1, n_species))
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot each species
    for i, species in enumerate(species_list):
        species_data = df_response[df_response['Species'] == species]
        
        # Calculate mean OD for each pH
        mean_data = species_data.groupby('pH')['OD'].mean().reset_index()
        
        # Plot the curve
        ax.plot(mean_data['pH'], mean_data['OD'], 
                marker='o', markersize=6, linewidth=2,
                color=colors[i], label=species, alpha=0.8)
    
    ax.set_xlabel('Initial pH', fontsize=12)
    ax.set_ylabel('Optical Density (OD)', fontsize=12)
    ax.set_title('Species Growth Response to pH', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.set_xticks([4, 5, 6, 7, 8, 9])
    
    # Add legend outside plot
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2, fontsize=8)
    
    plt.tight_layout()
    return fig

def plot_ph_change_heatmap(df_change):
    """Plot heatmap of pH changes after 15 hours"""
    
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib not available, skipping heatmap")
        return None
        
    if df_change.empty:
        print("No pH change data available")
        return None
    
    # Create a pivot table for heatmap
    # Arrange by row and column to match plate layout
    heatmap_data = np.full((8, 12), np.nan)
    
    for _, row in df_change.iterrows():
        row_idx = ord(row['Row']) - ord('A')
        col_idx = row['Column'] - 1
        heatmap_data[row_idx, col_idx] = row['pH_change']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create heatmap
    im = ax.imshow(heatmap_data, cmap='RdBu_r', aspect='auto', vmin=3, vmax=8)
    
    # Set ticks and labels
    ax.set_xticks(range(12))
    ax.set_xticklabels([str(i+1) for i in range(12)])
    ax.set_yticks(range(8))
    ax.set_yticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Final pH after 15h', rotation=270, labelpad=20)
    
    # Add text annotations
    for i in range(8):
        for j in range(12):
            if not np.isnan(heatmap_data[i, j]):
                text = ax.text(j, i, f'{heatmap_data[i, j]:.1f}',
                             ha='center', va='center', color='black' if 4.5 < heatmap_data[i, j] < 6.5 else 'white',
                             fontsize=8)
    
    ax.set_xlabel('Column', fontsize=12)
    ax.set_ylabel('Row', fontsize=12)
    ax.set_title('pH Change After 15 Hours (Starting pH: 6.5)', fontsize=14)
    
    plt.tight_layout()
    return fig

def analyze_ph_preference(df_response):
    """Analyze pH preference for each species"""
    
    results = []
    
    for species in df_response['Species'].unique():
        species_data = df_response[df_response['Species'] == species]
        
        # Calculate mean OD for each pH
        mean_data = species_data.groupby('pH')['OD'].agg(['mean', 'std', 'count']).reset_index()
        
        # Find optimal pH (highest mean OD)
        optimal_idx = mean_data['mean'].idxmax()
        optimal_ph = mean_data.loc[optimal_idx, 'pH']
        optimal_od = mean_data.loc[optimal_idx, 'mean']
        
        # Calculate pH tolerance range (where OD > 50% of optimal)
        threshold = optimal_od * 0.5
        tolerance_data = mean_data[mean_data['mean'] > threshold]
        ph_range = (tolerance_data['pH'].min(), tolerance_data['pH'].max())
        
        results.append({
            'Species': species,
            'Optimal_pH': optimal_ph,
            'Optimal_OD': optimal_od,
            'pH_Range_Min': ph_range[0],
            'pH_Range_Max': ph_range[1],
            'pH_Tolerance': ph_range[1] - ph_range[0]
        })
    
    return pd.DataFrame(results)

def plot_species_groups_by_ph_preference(df_preference):
    """Group species by their pH preferences"""
    
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib not available, skipping preference plots")
        return None
    
    # Categorize species
    df_preference['Category'] = 'Neutrophile'
    df_preference.loc[df_preference['Optimal_pH'] <= 5.0, 'Category'] = 'Acidophile'
    df_preference.loc[df_preference['Optimal_pH'] >= 8.0, 'Category'] = 'Alkaliphile'
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Distribution of optimal pH
    ax1.hist(df_preference['Optimal_pH'], bins=6, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Optimal pH', fontsize=12)
    ax1.set_ylabel('Number of Species', fontsize=12)
    ax1.set_title('Distribution of Optimal pH Among Species', fontsize=14)
    ax1.set_xticks([4, 5, 6, 7, 8, 9])
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: pH tolerance by category
    categories = df_preference.groupby('Category')
    positions = [1, 2, 3]
    colors = ['red', 'green', 'blue']
    labels = ['Acidophile', 'Neutrophile', 'Alkaliphile']
    
    for i, (category, color, label) in enumerate(zip(['Acidophile', 'Neutrophile', 'Alkaliphile'], colors, labels)):
        cat_data = df_preference[df_preference['Category'] == category]
        if len(cat_data) > 0:
            ax2.scatter([positions[i]] * len(cat_data), cat_data['pH_Tolerance'], 
                       color=color, alpha=0.6, s=100, label=f'{label} (n={len(cat_data)})')
            ax2.boxplot([cat_data['pH_Tolerance'].values], positions=[positions[i]], 
                       widths=0.3, patch_artist=True,
                       boxprops=dict(facecolor=color, alpha=0.3))
    
    ax2.set_xticks(positions)
    ax2.set_xticklabels(labels)
    ax2.set_ylabel('pH Tolerance Range', fontsize=12)
    ax2.set_title('pH Tolerance by Species Category', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig

def main():
    """Main analysis function"""
    
    # Create output directory
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load pH response data
    print("=== Species pH Response Analysis ===")
    df_response = load_ph_response_data()
    
    # Load pH change data
    df_change = load_ph_change_data()
    
    if df_response.empty:
        print("Error: No pH response data found!")
        return
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # 1. Plot all species pH response curves in one plot
    print("\n1. Creating species pH response curves...")
    fig1 = plot_species_ph_response_curves(df_response)
    if fig1:
        fig1.savefig(f"{output_dir}/species_ph_response_curves.svg", bbox_inches='tight', dpi=300)
        fig1.savefig(f"{output_dir}/species_ph_response_curves.png", bbox_inches='tight', dpi=300)
        print(f"✓ Saved pH response curves")
    
    # 2. Plot pH change heatmap
    if not df_change.empty:
        print("\n2. Creating pH change heatmap...")
        fig2 = plot_ph_change_heatmap(df_change)
        if fig2:
            fig2.savefig(f"{output_dir}/ph_change_heatmap.svg", bbox_inches='tight', dpi=300)
            fig2.savefig(f"{output_dir}/ph_change_heatmap.png", bbox_inches='tight', dpi=300)
            print(f"✓ Saved pH change heatmap")
    
    # 3. Analyze pH preferences
    print("\n3. Analyzing pH preferences...")
    df_preference = analyze_ph_preference(df_response)
    
    # Save preference analysis
    df_preference.to_csv(f"{output_dir}/species_ph_preferences.csv", index=False)
    print(f"✓ Saved pH preference analysis")
    
    # 4. Plot species groups by pH preference
    print("\n4. Creating pH preference grouping plots...")
    fig3 = plot_species_groups_by_ph_preference(df_preference)
    if fig3:
        fig3.savefig(f"{output_dir}/species_ph_preference_groups.svg", bbox_inches='tight', dpi=300)
        fig3.savefig(f"{output_dir}/species_ph_preference_groups.png", bbox_inches='tight', dpi=300)
        print(f"✓ Saved pH preference grouping plots")
    
    # Print summary statistics
    print("\n=== Summary ===")
    print(f"Total species analyzed: {len(df_preference)}")
    print(f"- Acidophiles (optimal pH ≤ 5.0): {len(df_preference[df_preference['Optimal_pH'] <= 5.0])}")
    print(f"- Neutrophiles (5.0 < optimal pH < 8.0): {len(df_preference[(df_preference['Optimal_pH'] > 5.0) & (df_preference['Optimal_pH'] < 8.0)])}")
    print(f"- Alkaliphiles (optimal pH ≥ 8.0): {len(df_preference[df_preference['Optimal_pH'] >= 8.0])}")
    
    print(f"\nMean pH tolerance range: {df_preference['pH_Tolerance'].mean():.1f} pH units")
    print(f"Most acid-loving species: {df_preference.loc[df_preference['Optimal_pH'].idxmin(), 'Species']} (optimal pH: {df_preference['Optimal_pH'].min():.1f})")
    print(f"Most alkali-loving species: {df_preference.loc[df_preference['Optimal_pH'].idxmax(), 'Species']} (optimal pH: {df_preference['Optimal_pH'].max():.1f})")
    
    print("\n✓ Analysis complete!")
    print(f"✓ All results saved to: {output_dir}/")

if __name__ == "__main__":
    main()