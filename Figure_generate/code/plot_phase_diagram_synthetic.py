"""
plot_phase_diagram_synthetic.py

Purpose: Generate phase diagrams for synthetic/experimental coalescence data
Key features:
- Creates phase diagrams for different species pool sizes (6, 12, 24)
- Shows distribution of dominance, mixing, and restructuring outcomes
- Uses vector decomposition to classify coalescence events
- Generates merged plots combining all species pool sizes

Outputs:
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_6.svg
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_12.svg  
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_24.svg
- Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged.svg

Converted from: new_Plot_phase_diagram.ipynb
"""

from common_setup import *
from pathlib import Path
import numpy as np

def plot_phase_diagram_for_pool_size(pool_sizes, output_suffix=""):
    """Plot phase diagram for specific pool sizes."""
    
    degList = np.zeros(43)
    data1_set = {}
    data2_set = {}
    data3_set = {}
    
    type_names = []
    custom_x_labels = []
    
    for pool_size in pool_sizes:
        for c_i, medium in enumerate(['LN', 'MN', 'HN']):
            type_name = f'{medium}_{pool_size}'
            type_names.append(type_name)
            custom_x_labels.append(medium)
            
            if type_name not in Syn_Coal_IDX:
                print(f"Warning: {type_name} not found in Syn_Coal_IDX")
                data1_set[type_name] = []
                data2_set[type_name] = []
                data3_set[type_name] = []
                continue
            
            IDX_list = Syn_Coal_IDX[type_name]
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_1 = Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()
            idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
            idx_2 = Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()
            idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
            idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])
            
            data1 = []
            data2 = []
            data3 = []
            
            for i in range(len(idx)):
                c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
                c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
                c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)
                
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                data1.append(u)
                data2.append(v)
                data3.append(k)
            
            data1_set[type_name] = data1
            data2_set[type_name] = data2
            data3_set[type_name] = data3
    
    return type_names, data1_set, data2_set, data3_set, custom_x_labels

def main():
    """Main function to generate all phase diagrams."""
    
    # Create output directory
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating phase diagrams for synthetic coalescence data...")
    
    # 1. Individual pool sizes
    for pool_size in [6, 12, 24]:
        print(f"\nGenerating phase diagram for species pool size {pool_size}...")
        
        type_names, data1_set, data2_set, data3_set, labels = plot_phase_diagram_for_pool_size([pool_size])
        
        # Set up plotting parameters
        types_to_plot = [f'LN_{pool_size}', f'MN_{pool_size}', f'HN_{pool_size}']
        custom_x_ticks = [0.5, 1.5, 2.5]
        custom_x_labels = ['LN', 'MN', 'HN']
        
        output_filename = f"Figure/PhaseDiagram/Fig_phase_diagram_synthetic_{pool_size}.svg"
        
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
    
    # 2. Special case for pool size 12 (duplicate with different filename)
    print(f"\nGenerating additional phase diagram for species pool size 12 (synthetic12)...")
    
    type_names, data1_set, data2_set, data3_set, labels = plot_phase_diagram_for_pool_size([12])
    
    types_to_plot = ['LN_12', 'MN_12', 'HN_12']
    custom_x_ticks = [0.5, 1.5, 2.5]
    custom_x_labels = ['LN', 'MN', 'HN']
    
    output_filename = "Figure/PhaseDiagram/Fig_phase_diagram_synthetic12.svg"
    
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
    
    # 3. Merged plot combining all species pool sizes
    print(f"\nGenerating merged phase diagram (all species pool sizes combined)...")
    
    degList = np.zeros(43)
    data1_set_merged = {}
    data2_set_merged = {}
    data3_set_merged = {}
    
    # Combine data for each nutrient level across all species pool sizes
    for nutrient_level in ['LN', 'MN', 'HN']:
        data1_combined = []
        data2_combined = []
        data3_combined = []
        
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
        
        data1_set_merged[nutrient_level] = data1_combined
        data2_set_merged[nutrient_level] = data2_combined
        data3_set_merged[nutrient_level] = data3_combined
    
    types_to_plot_merged = ['LN', 'MN', 'HN']
    custom_x_ticks = [0.5, 1.5, 2.5]
    custom_x_labels = ['LN', 'MN', 'HN']
    
    output_filename_merged = "Figure/PhaseDiagram/Fig_phase_diagram_synthetic_merged.svg"
    
    try:
        create_phase_diagram(
            types_to_plot_merged, data1_set_merged, data2_set_merged, data3_set_merged, 
            custom_x_ticks, custom_x_labels, 
            output_filename=output_filename_merged, 
            plot_boundary=True
        )
        print(f"✓ Created: {output_filename_merged}")
    except Exception as e:
        print(f"✗ Error creating {output_filename_merged}: {e}")
    
    # 4. General synthetic plot (same as merged)
    output_filename_synthetic = "Figure/PhaseDiagram/Fig_phase_diagram_synthetic.svg"
    
    try:
        create_phase_diagram(
            types_to_plot_merged, data1_set_merged, data2_set_merged, data3_set_merged, 
            custom_x_ticks, custom_x_labels, 
            output_filename=output_filename_synthetic, 
            plot_boundary=True
        )
        print(f"✓ Created: {output_filename_synthetic}")
    except Exception as e:
        print(f"✗ Error creating {output_filename_synthetic}: {e}")
    
    print(f"\n🎉 Phase diagram generation complete!")
    print(f"📁 Output directory: Figure/PhaseDiagram/")
    print(f"🎨 Using new colormap: Red (Dominance), Purple (Mixing), Green (Restructuring)")

if __name__ == "__main__":
    main()