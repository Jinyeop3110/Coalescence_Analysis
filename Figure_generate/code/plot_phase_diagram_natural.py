"""
plot_phase_diagram_natural.py

Purpose: Generate phase diagrams for natural coalescence data
Key features:
- Creates phase diagrams for natural communities across different nutrient levels
- Shows distribution of dominance, mixing, and restructuring outcomes
- Uses vector decomposition to classify coalescence events
- Complementary to synthetic phase diagrams

Outputs:
- Figure/PhaseDiagram/Fig_phase_diagram_natural.svg
- Figure/PhaseDiagram/Fig_phase_diagram_natural_pie.svg

Author: Gore Lab Analysis Team
Date: January 2025
"""

from common_setup import *
from pathlib import Path
import numpy as np

def plot_phase_diagram_natural():
    """Plot phase diagram for natural coalescence data."""
    
    degList = np.zeros(43)
    data1_set = {}
    data2_set = {}
    data3_set = {}
    
    type_names = []
    custom_x_labels = []
    
    # Process natural communities across nutrient levels
    for c_i, medium in enumerate(['LN', 'MN', 'HN']):
        type_name = medium
        type_names.append(type_name)
        custom_x_labels.append(medium)
        
        if type_name not in Nat_Coal_IDX:
            print(f"Warning: {type_name} not found in Nat_Coal_IDX")
            data1_set[type_name] = []
            data2_set[type_name] = []
            data3_set[type_name] = []
            continue
        
        IDX_list = Nat_Coal_IDX[type_name]
        
        if len(IDX_list) == 0:
            print(f"Warning: No data found for {type_name}")
            data1_set[type_name] = []
            data2_set[type_name] = []
            data3_set[type_name] = []
            continue
        
        # Get coalescence event indices
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        if len(idx) == 0:
            print(f"Warning: No coalescence data found for {type_name}")
            data1_set[type_name] = []
            data2_set[type_name] = []
            data3_set[type_name] = []
            continue
        
        # Get parent community indices
        idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
        idx_1 = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in idx_1])
        
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
        idx_2 = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in idx_2])
        
        # Get mixed community indices
        idx = np.squeeze([np.where(Processed_sequences_natural['SampleIDX']==x) for x in IDX_list])
        
        data1 = []
        data2 = []
        data3 = []
        
        print(f"Processing {len(idx)} coalescence events for {type_name}")
        
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
                data1.append(u)
                data2.append(v)
                data3.append(k)
                
            except Exception as e:
                print(f"Error processing event {i} for {type_name}: {e}")
                continue
        
        data1_set[type_name] = data1
        data2_set[type_name] = data2
        data3_set[type_name] = data3
        
        print(f"Successfully processed {len(data1)} events for {type_name}")
    
    return type_names, data1_set, data2_set, data3_set, custom_x_labels

def main():
    """Main function to generate natural community phase diagrams."""
    
    # Create output directory
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating phase diagrams for natural coalescence data...")
    
    # Generate phase diagram data
    type_names, data1_set, data2_set, data3_set, labels = plot_phase_diagram_natural()
    
    # Check if we have any data
    total_events = sum(len(data1_set[name]) for name in type_names)
    if total_events == 0:
        print("Error: No coalescence events found for natural communities!")
        return
    
    # Print data summary
    print(f"\nData summary:")
    for name in type_names:
        n_events = len(data1_set[name])
        print(f"  {name}: {n_events} coalescence events")
    
    # Set up plotting parameters
    types_to_plot = ['LN', 'MN', 'HN']
    custom_x_ticks = [0.5, 1.5, 2.5]
    custom_x_labels = ['LN', 'MN', 'HN']
    
    # 1. Generate main phase diagram
    output_filename = "Figure/PhaseDiagram/Fig_phase_diagram_natural.svg"
    
    try:
        create_phase_diagram(
            types_to_plot, data1_set, data2_set, data3_set, 
            custom_x_ticks, custom_x_labels, 
            output_filename=output_filename, 
            plot_boundary=True
        )
        print(f"✓ Created: {output_filename}")
    except Exception as e:
        print(f"✗ Error creating {output_filename}: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. Generate pie chart version (if pie chart function exists)
    try:
        # Check if pie chart function is available
        if 'create_phase_diagram_pie' in globals():
            output_filename_pie = "Figure/PhaseDiagram/Fig_phase_diagram_natural_pie.svg"
            
            create_phase_diagram_pie(
                types_to_plot, data1_set, data2_set, data3_set, 
                custom_x_ticks, custom_x_labels, 
                output_filename=output_filename_pie
            )
            print(f"✓ Created: {output_filename_pie}")
    except Exception as e:
        print(f"Note: Pie chart version not created: {e}")
    
    print(f"\n🎉 Natural community phase diagram generation complete!")
    print(f"📁 Output directory: Figure/PhaseDiagram/")
    print(f"🎨 Using colormap: Red (Dominance), Purple (Mixing), Green (Restructuring)")
    
    # Print summary statistics
    print(f"\n📊 Summary Statistics:")
    for name in types_to_plot:
        if name in data1_set and len(data1_set[name]) > 0:
            n_events = len(data1_set[name])
            dominance_events = sum(1 for u, v, k in zip(data1_set[name], data2_set[name], data3_set[name]) 
                                 if u > 0.5 and v > 0.5)
            mixing_events = sum(1 for u, v, k in zip(data1_set[name], data2_set[name], data3_set[name]) 
                              if u > 0.5 and v < 0.5)
            restructuring_events = sum(1 for u, v, k in zip(data1_set[name], data2_set[name], data3_set[name]) 
                                     if u < 0.5)
            
            print(f"  {name}: {n_events} total events")
            print(f"    - Dominance: {dominance_events} ({100*dominance_events/n_events:.1f}%)")
            print(f"    - Mixing: {mixing_events} ({100*mixing_events/n_events:.1f}%)")
            print(f"    - Restructuring: {restructuring_events} ({100*restructuring_events/n_events:.1f}%)")

if __name__ == "__main__":
    main()