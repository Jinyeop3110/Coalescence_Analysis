"""
plot_phase_diagram_natural_pie.py

Purpose: Generate pie plots for natural coalescence data showing distribution of outcomes
Key features:
- Creates pie charts for dominance, mixing, and restructuring outcomes
- Shows percentage distributions for each nutrient condition (LN, MN, HN)
- Uses the same data classification as phase diagrams but displays as pie charts
- Complementary to synthetic community pie charts

Output:
- Figure/PhaseDiagram/Fig_phase_diagram_natural_pie.svg

Author: Gore Lab Analysis Team
Date: January 2025
"""

from common_setup import *
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

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

def collect_natural_data():
    """Collect and process natural coalescence data for pie charts."""
    
    nutrient_levels = ['LN', 'MN', 'HN']
    pie_data = {}
    
    for nutrient_level in nutrient_levels:
        print(f"Processing {nutrient_level} natural communities...")
        
        if nutrient_level not in Nat_Coal_IDX:
            print(f"Warning: {nutrient_level} not found in Nat_Coal_IDX")
            pie_data[nutrient_level] = {'dominance': 0, 'mixing': 0, 'restructuring': 0, 'total': 0}
            continue
        
        IDX_list = Nat_Coal_IDX[nutrient_level]
        
        if len(IDX_list) == 0:
            print(f"Warning: No data found for {nutrient_level}")
            pie_data[nutrient_level] = {'dominance': 0, 'mixing': 0, 'restructuring': 0, 'total': 0}
            continue
        
        u_combined = []
        v_combined = []
        k_combined = []
        
        # Get coalescence event indices
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        if len(idx) == 0:
            print(f"Warning: No coalescence data found for {nutrient_level}")
            pie_data[nutrient_level] = {'dominance': 0, 'mixing': 0, 'restructuring': 0, 'total': 0}
            continue
        
        # Get parent community indices
        idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
        idx_1 = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in idx_1])
        
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
        idx_2 = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in idx_2])
        
        # Get mixed community indices
        idx = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in IDX_list])
        
        successful_events = 0
        
        for i in range(len(idx)):
            try:
                # Get abundance vectors
                c_mix = Processed_sequences_natural.iloc[idx[i]].values.tolist()[1:]
                c_1 = np.array(Processed_sequences_natural.iloc[idx_1[i]].values.tolist()[1:])
                c_2 = np.array(Processed_sequences_natural.iloc[idx_2[i]].values.tolist()[1:])
                
                # Apply threshold filtering
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                # Calculate vector decomposition
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                u_combined.append(u)
                v_combined.append(v)
                k_combined.append(k)
                successful_events += 1
                
            except Exception as e:
                print(f"Error processing event {i} for {nutrient_level}: {e}")
                continue
        
        # Classify outcomes
        dominance_count, mixing_count, restructuring_count = classify_outcomes(
            u_combined, v_combined, k_combined
        )
        
        pie_data[nutrient_level] = {
            'dominance': dominance_count,
            'mixing': mixing_count,
            'restructuring': restructuring_count,
            'total': successful_events
        }
        
        print(f"  {nutrient_level}: {successful_events} events processed")
        print(f"    Dominance: {dominance_count}, Mixing: {mixing_count}, Restructuring: {restructuring_count}")
    
    return pie_data

def create_pie_chart(pie_data):
    """Create pie chart visualization for natural communities."""
    
    # Define colors (same as phase diagram)
    colors = ['#E24912', '#A7216A', '#802000']  # Red, Purple, Green equivalent
    labels = ['Dominance', 'Mixing', 'Restructuring']
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Natural Community Coalescence Outcomes', fontsize=16, fontweight='bold')
    
    nutrient_levels = ['LN', 'MN', 'HN']
    nutrient_titles = ['Low Nutrient (LN)', 'Medium Nutrient (MN)', 'High Nutrient (HN)']
    
    for i, (nutrient_level, title) in enumerate(zip(nutrient_levels, nutrient_titles)):
        data = pie_data[nutrient_level]
        
        if data['total'] == 0:
            # No data - show empty pie with message
            axes[i].text(0.5, 0.5, 'No Data\nAvailable', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=axes[i].transAxes, fontsize=12)
            axes[i].set_title(f'{title}\n(0 events)', fontweight='bold')
        else:
            # Create pie chart
            sizes = [data['dominance'], data['mixing'], data['restructuring']]
            # Only show non-zero slices
            non_zero_sizes = [size for size in sizes if size > 0]
            non_zero_labels = [labels[j] for j, size in enumerate(sizes) if size > 0]
            non_zero_colors = [colors[j] for j, size in enumerate(sizes) if size > 0]
            
            if len(non_zero_sizes) > 0:
                wedges, texts, autotexts = axes[i].pie(
                    non_zero_sizes, 
                    labels=non_zero_labels,
                    colors=non_zero_colors,
                    autopct=lambda pct: f'{int(pct*data["total"]/100)} / {data["total"]}' if pct > 0 else '',
                    startangle=90,
                    textprops={'fontsize': 10}
                )
                
                # Make percentage text bold
                for autotext in autotexts:
                    autotext.set_color('black')
                    autotext.set_fontweight('bold')
            
            axes[i].set_title(f'{title}\n({data["total"]} events)', fontweight='bold')
    
    # Create overall legend
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=colors[j], label=labels[j]) for j in range(3)]
    fig.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.5, 0.02), ncol=3, fontsize=12)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # Make room for legend
    
    return fig

def main():
    """Main function to generate pie plots for natural coalescence data."""
    
    # Create output directory
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating pie plots for natural coalescence data...")
    
    # Collect data
    pie_data = collect_natural_data()
    
    # Check if we have any data
    total_events = sum(data['total'] for data in pie_data.values())
    if total_events == 0:
        print("Error: No coalescence events found for natural communities!")
        return
    
    print(f"\nTotal events across all conditions: {total_events}")
    
    # Create pie chart
    fig = create_pie_chart(pie_data)
    
    # Save figure
    output_filename = "Figure/PhaseDiagram/Fig_phase_diagram_natural_pie.svg"
    
    try:
        fig.savefig(output_filename, format='svg', dpi=300, bbox_inches='tight')
        plt.show()
        print(f"✓ Created: {output_filename}")
    except Exception as e:
        print(f"✗ Error creating {output_filename}: {e}")
        import traceback
        traceback.print_exc()
    
    # Print summary statistics
    print(f"\n📊 Summary Statistics:")
    total_dominance = sum(data['dominance'] for data in pie_data.values())
    total_mixing = sum(data['mixing'] for data in pie_data.values())
    total_restructuring = sum(data['restructuring'] for data in pie_data.values())
    
    if total_events > 0:
        print(f"Overall distribution across all natural communities:")
        print(f"  - Dominance: {total_dominance} ({100*total_dominance/total_events:.1f}%)")
        print(f"  - Mixing: {total_mixing} ({100*total_mixing/total_events:.1f}%)")
        print(f"  - Restructuring: {total_restructuring} ({100*total_restructuring/total_events:.1f}%)")
    
    print(f"\n🎉 Natural community pie chart generation complete!")
    print(f"📁 Output directory: Figure/PhaseDiagram/")

if __name__ == "__main__":
    main()