"""
plot_phase_diagram_pie.py

Purpose: Generate pie plots for synthetic coalescence data showing distribution of outcomes
Key features:
- Creates pie charts for dominance, mixing, and restructuring outcomes
- Shows percentage distributions for each nutrient condition (LN, MN, HN)
- Uses the same data classification as phase diagrams but displays as pie charts

Output:
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged_pie.svg
"""

from common_setup import *
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from COLORMAP import get_phase_diagram_colors

def classify_outcomes(u_values, v_values, k_values):
    """
    Classify coalescence outcomes based on u, v, k values using the same logic as phase diagrams.
    
    Returns counts of:
    - Dominance (class 0)
    - Mixing (class 1)
    - Restructuring (class 2)
    """
    dominance_count = 0
    mixing_count = 0
    restructuring_count = 0
    
    for u, v, k in zip(u_values, v_values, k_values):
        # Use the same classification logic as in common_setup.py
        x = np.sqrt(u**2 + v**2)
        y = np.abs(np.abs(np.arctan(u/(v + 1e-8))) - np.pi/4) / (np.pi/4)
        
        # characterize_case logic
        if (x**2 > 0.5) * (y > 0.5):
            dominance_count += 1  # Class 0
        elif (x**2 > 0.5) * (y < 0.5):
            mixing_count += 1     # Class 1
        elif (x**2 < 0.5):
            restructuring_count += 1  # Class 2
    
    return dominance_count, mixing_count, restructuring_count

def main():
    """Main function to generate pie plots for synthetic merged data."""
    
    # Create output directory
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating pie plots for synthetic coalescence data...")
    
    # Collect data for each nutrient level across all species pool sizes
    nutrient_levels = ['LN', 'MN', 'HN']
    pie_data = {}
    
    for nutrient_level in nutrient_levels:
        data1_combined = []
        data2_combined = []
        data3_combined = []
        
        # Combine data from all pool sizes
        for pool_size in ['6', '12', '24']:
            type_name = f'{nutrient_level}_{pool_size}'
            
            if type_name in Syn_Coal_IDX:
                IDX_list = Syn_Coal_IDX[type_name]
                idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
                idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
                idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
                idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
                idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
                idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
                idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
                
                for i in range(len(idx)):
                    c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                    c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                    c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                    c_1 = c_1 * (c_1 > 1e-4)
                    c_2 = c_2 * (c_2 > 1e-4)
                    u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                    data1_combined.append(u)
                    data2_combined.append(v)
                    data3_combined.append(k)
        
        # Classify outcomes
        dominance, mixing, restructuring = classify_outcomes(data1_combined, data2_combined, data3_combined)
        pie_data[nutrient_level] = {
            'Dominance': dominance,
            'Mixing': mixing,
            'Restructuring': restructuring
        }
    
    # Create stacked bar plots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    colors = get_phase_diagram_colors()  # Get proper phase diagram colors

    for idx, (nutrient_level, ax) in enumerate(zip(nutrient_levels, axes)):
        data = pie_data[nutrient_level]
        values = [data['Dominance'], data['Mixing'], data['Restructuring']]
        labels = ['Dominance', 'Mixing', 'Restructuring']

        # Calculate total
        total = sum(values)

        # Create horizontal stacked bar chart
        left = 0
        for i, (value, label) in enumerate(zip(values, labels)):
            percentage = value / total * 100 if total > 0 else 0
            bar = ax.barh(0, percentage, left=left, color=colors[i],
                         alpha=0.85, height=0.5, edgecolor='white', linewidth=2)

            # Add text label with (n/total) format
            if percentage > 5:  # Only show label if segment is large enough
                ax.text(left + percentage/2, 0, f'{value}/{total}',
                       ha='center', va='center', fontsize=14, fontweight='bold',
                       color='black')

            left += percentage

        # Set axis properties
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel('Percentage (%)', fontsize=12)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add title
        ax.set_title(f'{nutrient_level} Medium', fontsize=14, fontweight='bold', pad=20)

    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    output_filename = "Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged_pie.svg"
    fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Created: {output_filename}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("-" * 50)
    for nutrient_level in nutrient_levels:
        data = pie_data[nutrient_level]
        values_list = list(data.values())
        total_count = sum(values_list)
        print(f"\n{nutrient_level} Medium (n={total_count}):")
        for outcome, count in data.items():
            if total_count > 0:
                percentage = count/total_count * 100
                print(f"  {outcome}: {count} ({percentage:.1f}%)")
            else:
                print(f"  {outcome}: {count} (0.0%)")

if __name__ == "__main__":
    main()