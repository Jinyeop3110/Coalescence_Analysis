"""
plot_phase_diagram_simulation.py

Purpose: Generate phase diagrams for Lotka-Volterra simulation data
Key features:
- Creates phase diagrams for different Gaussian interaction strength parameters
- Shows distribution of dominance, mixing, and restructuring outcomes
- Uses vector decomposition to classify simulation coalescence events
- Processes multiple simulation sessions with varying interaction parameters

Outputs:
- Figure/PhaseDiagram/Fig_phase_diagram_Simul_k_gaussian_0.05.svg
- Figure/PhaseDiagram/Fig_phase_diagram_Simul_k_gaussian_0.1.svg
- Figure/PhaseDiagram/Fig_phase_diagram_Simul_k_gaussian_0.15.svg
- Figure/PhaseDiagram/Fig_phase_diagram_Simul_k_gaussian_0.2.svg
- Figure/PhaseDiagram/Fig_phase_diagram_Simul_k_gaussian_0.25.svg
- Figure/PhaseDiagram/Fig_phase_diagram_Simul_standard.svg

Converted from: new_Plot_phase_diagram_simulation.ipynb
"""

from common_setup import *
from pathlib import Path
import json
import pandas as pd
import numpy as np

def read_simulation_excel(file_path):
    """Read simulation data from Excel file with multiple sheets."""
    data_sheets = []
    try:
        for sheet_name in range(3):
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            df = df.drop(df.columns[0], axis=1)  # Drop first column (index)
            df = df.transpose()  # Transpose to get correct orientation
            data_sheets.append(df)
        return data_sheets
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def process_simulation_session(session_name):
    """Process a single simulation session and return phase diagram data."""
    
    print(f"Processing simulation session: {session_name}")
    
    file_path = f"Simulation_Data/{session_name}/Similarity.xlsx"
    
    if not Path(file_path).exists():
        print(f"Warning: File not found: {file_path}")
        return None, None, None, None
    
    # Read the simulation data
    excel_data = read_simulation_excel(file_path)
    if excel_data is None:
        return None, None, None, None
    
    data1, data2, data3 = excel_data
    
    # Convert to dictionary format expected by create_phase_diagram
    data1_dict = {}
    data2_dict = {}
    data3_dict = {}
    
    # The simulation data has different structure - each column represents a type
    types_to_plot = np.arange(min(12, len(data1.columns)))  # Limit to 12 types max
    
    for type_idx in types_to_plot:
        if type_idx < len(data1.columns):
            # Extract data for this type (remove NaN values)
            type_data1 = data1.iloc[:, type_idx].dropna().tolist()
            type_data2 = data2.iloc[:, type_idx].dropna().tolist()
            type_data3 = data3.iloc[:, type_idx].dropna().tolist()
            
            # Ensure all arrays have the same length
            min_length = min(len(type_data1), len(type_data2), len(type_data3))
            type_data1 = type_data1[:min_length]
            type_data2 = type_data2[:min_length]
            type_data3 = type_data3[:min_length]
            
            data1_dict[type_idx] = type_data1
            data2_dict[type_idx] = type_data2
            data3_dict[type_idx] = type_data3
        else:
            # Fill missing types with empty lists
            data1_dict[type_idx] = []
            data2_dict[type_idx] = []
            data3_dict[type_idx] = []
    
    return types_to_plot, data1_dict, data2_dict, data3_dict

def main():
    """Main function to generate all simulation phase diagrams."""
    
    # Create output directory
    output_dir = Path("Figure/PhaseDiagram")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating phase diagrams for simulation data...")
    print("🎨 Using new colormap: Red (Dominance), Purple (Mixing), Green (Restructuring)")
    
    # List of simulation sessions to process
    session_names = [
        "k_gaussian_0.05",
        "k_gaussian_0.1", 
        "k_gaussian_0.15",
        "k_gaussian_0.2",
        "k_gaussian_0.25",
        "standard"
    ]
    
    successful_plots = 0
    failed_plots = 0
    
    for session_name in session_names:
        print(f"\n--- Processing {session_name} ---")
        
        # Process the simulation data
        types_to_plot, data1, data2, data3 = process_simulation_session(session_name)
        
        if types_to_plot is None:
            print(f"✗ Skipping {session_name} due to data processing error")
            failed_plots += 1
            continue
        
        # Set up plotting parameters
        custom_x_ticks = np.arange(7) * 2  # 0, 2, 4, 6, 8, 10, 12
        custom_x_labels = [f"{i * 0.2:.1f}" for i in range(7)]  # 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2
        
        # Generate output filename
        output_filename = f"Figure/PhaseDiagram/Fig_phase_diagram_Simul_{session_name}.svg"
        
        try:
            # Create the phase diagram
            create_phase_diagram(
                types_to_plot, 
                data1, data2, data3, 
                custom_x_ticks, 
                custom_x_labels, 
                output_filename=output_filename,
                plot_boundary=False  # No boundary for simulation plots
            )
            
            print(f"✓ Created: {output_filename}")
            successful_plots += 1
            
            # Print some statistics about the data
            total_points = sum(len(data1.get(t, [])) for t in types_to_plot)
            print(f"  Data points processed: {total_points}")
            
        except Exception as e:
            print(f"✗ Error creating {output_filename}: {e}")
            failed_plots += 1
    
    # Summary
    print(f"\n🎉 Simulation phase diagram generation complete!")
    print(f"✓ Successful plots: {successful_plots}")
    print(f"✗ Failed plots: {failed_plots}")
    print(f"📁 Output directory: Figure/PhaseDiagram/")
    
    if successful_plots > 0:
        print(f"\n📊 Generated phase diagrams for:")
        for session_name in session_names:
            output_file = f"Fig_phase_diagram_Simul_{session_name}.svg"
            if Path(f"Figure/PhaseDiagram/{output_file}").exists():
                print(f"  • {session_name} → {output_file}")

def analyze_simulation_parameters():
    """Optional function to analyze the simulation parameters and their effects."""
    
    print("\n📈 SIMULATION PARAMETER ANALYSIS")
    print("=" * 50)
    
    session_names = ["k_gaussian_0.05", "k_gaussian_0.1", "k_gaussian_0.15", 
                     "k_gaussian_0.2", "k_gaussian_0.25", "standard"]
    
    for session_name in session_names:
        param_file = f"Simulation_Data/{session_name}/parameter.xlsx"
        
        if Path(param_file).exists():
            try:
                # Read parameter information
                params = pd.read_excel(param_file, sheet_name='Sheet1')
                if 'k' in params.columns:
                    k_values = params['k'].dropna()
                    print(f"\n{session_name}:")
                    print(f"  k parameter: mean={k_values.mean():.3f}, std={k_values.std():.3f}")
                    print(f"  k range: [{k_values.min():.3f}, {k_values.max():.3f}]")
                
            except Exception as e:
                print(f"\n{session_name}: Could not read parameters ({e})")
        else:
            print(f"\n{session_name}: No parameter file found")


if __name__ == "__main__":
    main()
    
    # Optionally run parameter analysis
    try:
        analyze_simulation_parameters()
    except Exception as e:
        print(f"\nParameter analysis failed: {e}")
    
    # Run robust 500 species analysis
    print("\n" + "="*60)
    print("GENERATING ROBUST 500-SPECIES PHASE DIAGRAM")
    print("="*60)
    print("🎨 Using new colormap: Red (Dominance), Purple (Mixing), Green (Restructuring)")
    
    # Session name for 500 species
    session_name = "new_k_gamma_0_defined_pool_nooverlap_50from500_natural"
    data_path = f"Simulation_Data/{session_name}"
    
    successful_plots = 0
    failed_plots = 0
    
    try:
        # 1. Verify data files exist
        json_file = f"{data_path}/Community.json"
        excel_file = f"{data_path}/Similarity.xlsx"
        
        print(f"\n📁 Checking data files...")
        if not Path(json_file).exists():
            raise FileNotFoundError(f"JSON data file not found: {json_file}")
        
        if not Path(excel_file).exists():
            print(f"⚠️  Excel file not found: {excel_file}")
            print("🔄 Running Excel converter...")
            
            # Run the converter
            from pathlib import Path
            import subprocess
            result = subprocess.run([
                "/Users/jysong/miniforge3/envs/coalescence/bin/python", 
                "convert_500species_to_excel.py"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Excel conversion successful")
            else:
                print(f"✗ Excel conversion failed: {result.stderr}")
                raise RuntimeError("Excel conversion failed")
        
        # 2. Load and validate 500-species JSON data structure
        print(f"\n📊 Loading and validating 500-species data structure...")
        import json
        with open(json_file, 'r') as f:
            raw_data = json.load(f)
        
        print(f"   Data structure: {list(raw_data.keys())}")
        u_values = [float(k) for k in raw_data.keys()]
        u_values.sort()
        print(f"   Interaction strengths: {u_values}")
        
        # 3. Process 500-species specific data for phase diagram
        print(f"\n🔄 Processing 500-species simulation data...")
        excel_data = read_simulation_excel(excel_file)
        if excel_data is None:
            raise RuntimeError("Failed to read Excel data")
            
        data1, data2, data3 = excel_data
        print(f"   Excel sheets loaded: {len(data1)}, {len(data2)}, {len(data3)} entries")
        
        # Process 500-species Excel data properly 
        # The Excel format for 500-species has columns for each u-value
        data1_dict = {}
        data2_dict = {}  
        data3_dict = {}
        
        print(f"   Processing Excel data with {len(data1.columns)} columns...")
        
        # Map u-values to columns with proper column names (u_0.3, u_0.5, u_0.7)
        for i, u_val in enumerate(u_values):
            type_key = np.int64(i)
            col_name = f"u_{u_val}"
            
            if col_name in data1.columns:
                # Extract data for this u-value using column name
                type_data1 = data1[col_name].dropna().tolist()
                type_data2 = data2[col_name].dropna().tolist()
                type_data3 = data3[col_name].dropna().tolist()
                
                print(f"   u={u_val:.1f} -> column '{col_name}': {len(type_data1)} dominance, {len(type_data2)} mixing, {len(type_data3)} restructuring points")
                
                # Ensure consistent lengths
                min_length = min(len(type_data1), len(type_data2), len(type_data3))
                if min_length > 0:
                    data1_dict[type_key] = type_data1[:min_length]
                    data2_dict[type_key] = type_data2[:min_length]
                    data3_dict[type_key] = type_data3[:min_length]
                else:
                    # If no data, create zeros
                    data1_dict[type_key] = [0.0]
                    data2_dict[type_key] = [0.0]
                    data3_dict[type_key] = [0.0]
            else:
                print(f"   Warning: Column '{col_name}' not found for u={u_val:.1f}")
                print(f"   Available columns: {list(data1.columns)}")
                data1_dict[type_key] = [0.0]
                data2_dict[type_key] = [0.0]
                data3_dict[type_key] = [0.0]
        
        types_to_plot = list(data1_dict.keys())
        print(f"   Types to plot: {types_to_plot}")
        
        # Calculate summary statistics
        for type_key in types_to_plot:
            dom_avg = np.mean(data1_dict[type_key]) if data1_dict[type_key] else 0
            mix_avg = np.mean(data2_dict[type_key]) if data2_dict[type_key] else 0  
            rest_avg = np.mean(data3_dict[type_key]) if data3_dict[type_key] else 0
            print(f"   Type {type_key}: Dom={dom_avg:.3f}, Mix={mix_avg:.3f}, Rest={rest_avg:.3f}")
        
        # 4. Validate processed data
        print(f"\n✓ Data processing complete")
        
        if not data1_dict:
            raise ValueError("No data generated")
        
        total_points = sum(len(data1_dict[k]) for k in types_to_plot)
        print(f"✓ Generated {total_points} total data points for phase diagram")
        
        # 5. Set up robust plotting parameters  
        print(f"\n🎨 Setting up plotting parameters...")
        
        # Map the 3 u-values to appropriate x-axis positions for 0.1-1.2 range
        # u=0.3 -> x=1, u=0.5 -> x=2, u=0.7 -> x=3
        custom_x_ticks = np.array([0, 2, 4, 6, 8, 10])  # Full range ticks
        custom_x_labels = ["0.1", "0.3", "0.5", "0.7", "0.9", "1.1"]  # Full range labels
        
        # Map our data types to the correct x-positions
        # types_to_plot contains [0, 1, 2] for the three u-values
        # We want to place them at positions corresponding to 0.3, 0.5, 0.7
        u_to_x_map = {0: 1, 1: 2, 2: 3}  # Map type indices to x-axis positions
        
        print(f"✓ Mapping {len(types_to_plot)} data types to x-positions")
        for i, type_key in enumerate(types_to_plot):
            x_pos = u_to_x_map.get(i, i)
            u_val = u_values[i] if i < len(u_values) else f"unknown_{i}"
            print(f"   Type {type_key} (u={u_val}) -> x-position {x_pos}")
        
        # 6. Create output directory and filename
        output_dir = Path("Figure/PhaseDiagram")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_filename = output_dir / "Fig_phase_diagram_Simul_50from500.svg"
        
        print(f"📁 Output file: {output_filename}")
        
        # 7. Generate phase diagram with corrected approach for simulation data
        print(f"\n🎨 Creating phase diagram with proper simulation classification...")
        
        # Import the fixed version
        from common_setup_simulation_fix import create_phase_diagram_for_simulation
        
        print(f"   Using type keys: {types_to_plot}")
        print(f"   Available data keys: {list(data1_dict.keys())}")
        
        create_phase_diagram_for_simulation(
            types_to_plot,
            data1_dict, data2_dict, data3_dict, 
            custom_x_ticks, 
            custom_x_labels, 
            output_filename=str(output_filename),
            plot_boundary=False,
            u_values=u_values  # Pass the actual u-values for proper full-range display
        )
        
        # 7. Verify output file was created
        if output_filename.exists():
            file_size = output_filename.stat().st_size
            print(f"✓ Phase diagram created successfully!")
            print(f"✓ File size: {file_size:,} bytes")
            successful_plots += 1
        else:
            raise RuntimeError("Output file was not created")
            
    except FileNotFoundError as e:
        print(f"✗ File not found: {e}")
        failed_plots += 1
    except ValueError as e:
        print(f"✗ Data validation error: {e}")
        failed_plots += 1
    except RuntimeError as e:
        print(f"✗ Runtime error: {e}")
        failed_plots += 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        print(f"✗ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        failed_plots += 1
    
    # Enhanced summary
    print(f"\n" + "="*60)
    print("500-SPECIES PHASE DIAGRAM GENERATION SUMMARY")
    print("="*60)
    print(f"✓ Successful plots: {successful_plots}")
    print(f"✗ Failed plots: {failed_plots}")
    
    if successful_plots > 0:
        print(f"📁 Output location: Figure/PhaseDiagram/Fig_phase_diagram_Simul_50from500.svg")
        print(f"🎯 Data range: u ∈ [0.3, 0.5, 0.7] mapped to x-axis [0.1, 1.1]")
        print(f"📊 Visualization: Red=Dominance, Green=Restructuring, Purple=Mixing")
    else:
        print(f"💡 Troubleshooting suggestions:")
        print(f"   - Check if simulation data exists: {data_path}/Community.json")
        print(f"   - Verify u_values [0.3, 0.5, 0.7] are present in data")
        print(f"   - Run: python convert_500species_to_excel.py")
        print(f"   - Check create_phase_diagram function compatibility")
    
    print("="*60)