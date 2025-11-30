#!/usr/bin/env python3
"""
Create main pH analysis plots matching existing project style
- main_optimal_pH_histogram
- main_pH_after_15h_histogram
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set Arial font for all text
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

def load_ph_response_data():
    """Load pH response data for isolates"""
    file_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/2209_pHresponse_Isolates.xlsx'
    
    ph_levels = ['4.0', '5.0', '6.0', '7.0', '8.0', '9.0']
    all_data = []
    
    for ph in ph_levels:
        try:
            df = pd.read_excel(file_path, sheet_name=ph, header=None)
            
            # Find data start row
            data_start = None
            for i in range(len(df)):
                if df.iloc[i, 0] == 'A':
                    data_start = i
                    break
            
            if data_start is None:
                continue
                
            # Extract 8x12 plate data
            for row_idx, row_label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
                if data_start + row_idx >= len(df):
                    break
                    
                row_data = df.iloc[data_start + row_idx, 1:13]
                
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
    
    return pd.DataFrame(all_data)

def load_ph_change_data():
    """Load pH change data after 15 hours"""
    file_path = '../../ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/230623_pH.xlsx'
    
    try:
        df = pd.read_excel(file_path, sheet_name='after 15h', header=None)
        
        # Find data start
        data_start = None
        for i in range(len(df)):
            if df.iloc[i, 0] == 'A':
                data_start = i
                break
        
        if data_start is None:
            return pd.DataFrame()
        
        all_data = []
        
        for row_idx, row_label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            if data_start + row_idx >= len(df):
                break
                
            row_data = df.iloc[data_start + row_idx, 1:13]
            
            for col_idx, ph_change in enumerate(row_data):
                if pd.notna(ph_change) and isinstance(ph_change, (int, float)):
                    all_data.append({
                        'Well': f"{row_label}{col_idx+1}",
                        'pH_final': float(ph_change) / 10.0,
                        'Species': f"{row_label}{col_idx+1}"
                    })
        
        return pd.DataFrame(all_data)
        
    except Exception as e:
        print(f"Error loading pH change data: {e}")
        return pd.DataFrame()

def analyze_ph_preference(df_response):
    """Find optimal pH for each species"""
    results = []
    
    for species in df_response['Species'].unique():
        species_data = df_response[df_response['Species'] == species]
        mean_data = species_data.groupby('pH')['OD'].mean().reset_index()
        optimal_idx = mean_data['OD'].idxmax()
        optimal_ph = mean_data.loc[optimal_idx, 'pH']
        
        results.append({
            'Species': species,
            'Optimal_pH': optimal_ph
        })
    
    return pd.DataFrame(results)

def create_main_optimal_ph_histogram(df_preference, output_dir):
    """Create clean histogram of optimal pH matching project style"""
    
    # Use compact figure size
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Create histogram with clean styling
    n, bins, patches = ax.hist(df_preference['Optimal_pH'], 
                              bins=np.arange(3.5, 9.5, 1.0),
                              edgecolor='none', 
                              linewidth=0,
                              alpha=0.7,
                              color='gray')
    
    # Match existing text styling
    ax.set_xlabel('Optimal pH')
    ax.set_ylabel('Number of Species')
    ax.set_title('Distribution of Optimal pH')
    
    # Match existing tick styling
    ax.tick_params(labelsize=8)
    ax.set_xticks([3, 4, 5, 6, 7, 8, 9])
    ax.set_xlim(2.5, 9.5)
    
    # Add simple statistics text (matching existing text style)
    total_species = len(df_preference)
    acidophiles = len(df_preference[df_preference['Optimal_pH'] <= 5.0])
    alkaliphiles = len(df_preference[df_preference['Optimal_pH'] >= 8.0])
    
    stats_text = f'n = {total_species}\nAcidophiles: {acidophiles}\nAlkaliphiles: {alkaliphiles}'
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    
    # Save in project standard format
    fig.savefig(f"{output_dir}/main_optimal_pH_histogram.svg", bbox_inches='tight')
    fig.savefig(f"{output_dir}/main_optimal_pH_histogram.png", bbox_inches='tight')
    
    return fig

def create_main_ph_after_15h_histogram(df_change, output_dir):
    """Create clean histogram of pH after 15h matching project style"""
    
    # Use compact figure size
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Create histogram with clean styling
    n, bins, patches = ax.hist(df_change['pH_final'], 
                              bins=np.arange(2.5, 8.5, 0.5),
                              edgecolor='none', 
                              linewidth=0,
                              alpha=0.8,
                              color='gray')
    
    # Match existing text styling
    ax.set_xlabel('Final pH After 15 Hours')
    ax.set_ylabel('Number of Species')
    
    # Match existing tick styling  
    ax.tick_params(labelsize=8)
    ax.set_xticks([3, 4, 5, 6, 7, 8])
    ax.set_xlim(2.5, 8.5)
    
    # Add initial pH reference line
    ax.axvline(x=6.5, color='black', linestyle='-', linewidth=1.0, alpha=0.8)
    ax.text(6.5, ax.get_ylim()[1] * 0.95, 'Initial pH', ha='center', va='bottom', 
            fontsize=10, color='black')
    
    # Add acidifier and alkalizer labels next to initial pH line
    y_pos = ax.get_ylim()[1] * 0.85
    
    # Left label for acidifiers (positioned closer to initial pH line)
    ax.text(6.3, y_pos, '← Acidifiers', ha='right', va='center', 
            fontsize=10, color='red')
    
    # Right label for alkalizers (positioned closer to initial pH line)  
    ax.text(6.7, y_pos, 'Alkalizers →', ha='left', va='center', 
            fontsize=10, color='blue')
    
    plt.tight_layout()
    
    # Save in project standard format
    fig.savefig(f"{output_dir}/main_pH_after_15h_histogram.svg", bbox_inches='tight')
    fig.savefig(f"{output_dir}/main_pH_after_15h_histogram.png", bbox_inches='tight')
    
    return fig

def main():
    """Create main pH plots matching project style"""
    
    # Create output directory
    output_dir = "Figure/pH_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Creating main pH plots...")
    
    # Load data
    df_response = load_ph_response_data()
    df_change = load_ph_change_data()
    
    if df_response.empty:
        print("Error: No pH response data found!")
        return
    
    # Analyze preferences
    df_preference = analyze_ph_preference(df_response)
    
    # Create main plots
    print("Creating main_optimal_pH_histogram...")
    fig1 = create_main_optimal_ph_histogram(df_preference, output_dir)
    print("✓ Saved main_optimal_pH_histogram")
    
    if not df_change.empty:
        print("Creating main_pH_after_15h_histogram...")
        fig2 = create_main_ph_after_15h_histogram(df_change, output_dir)
        print("✓ Saved main_pH_after_15h_histogram")
    else:
        print("Skipping pH after 15h histogram - no data")
    
    print("✓ Main plots complete!")

if __name__ == "__main__":
    main()