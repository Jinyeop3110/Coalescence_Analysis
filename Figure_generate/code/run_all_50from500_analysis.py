#!/usr/bin/env python
"""
Run all 500 species simulation analyses

This script runs all the plotting functions for the 500 species simulation data:
1. Vector decomposition analysis
2. Phase diagram generation
3. Pie chart creation

Usage:
conda activate coalescence
python run_all_50from500_analysis.py
"""

import os
import sys
import traceback

def run_analysis():
    """Run all 500 species analyses."""
    
    print("="*60)
    print("🔬 Running All 500 Species Simulation Analyses")
    print("="*60)
    
    success_count = 0
    total_analyses = 3
    
    # 1. Vector Decomposition Analysis
    print("\n1️⃣ Running Vector Decomposition Analysis...")
    try:
        from vector_decomp_simulation import main_50from500 as vector_main
        vector_main()
        print("✅ Vector decomposition analysis completed successfully!")
        success_count += 1
    except Exception as e:
        print(f"❌ Vector decomposition analysis failed: {e}")
        print("Traceback:")
        traceback.print_exc()
    
    # 2. Phase Diagram Generation
    print("\n2️⃣ Running Phase Diagram Generation...")
    try:
        from plot_phase_diagram_simulation import main_50from500 as phase_main
        phase_main()
        print("✅ Phase diagram generation completed successfully!")
        success_count += 1
    except Exception as e:
        print(f"❌ Phase diagram generation failed: {e}")
        print("Traceback:")
        traceback.print_exc()
    
    # 3. Pie Chart Creation
    print("\n3️⃣ Running Pie Chart Creation...")
    try:
        from plot_phase_diagram_simulation_pie import main_50from500 as pie_main
        pie_main()
        print("✅ Pie chart creation completed successfully!")
        success_count += 1
    except Exception as e:
        print(f"❌ Pie chart creation failed: {e}")
        print("Traceback:")
        traceback.print_exc()
    
    # Summary
    print("\n" + "="*60)
    print("📊 ANALYSIS SUMMARY")
    print("="*60)
    print(f"✅ Successful analyses: {success_count}/{total_analyses}")
    print(f"❌ Failed analyses: {total_analyses - success_count}/{total_analyses}")
    
    if success_count > 0:
        print(f"\n📁 Output files saved in:")
        print(f"   • Figure/VectorDecomp/ (vector decomposition plots)")
        print(f"   • Figure/PhaseDiagram/ (phase diagram and pie chart)")
    
    if success_count == total_analyses:
        print("\n🎉 All analyses completed successfully!")
    else:
        print(f"\n⚠️ {total_analyses - success_count} analysis(es) failed. Check error messages above.")
    
    return success_count == total_analyses

if __name__ == "__main__":
    # Check if we're in the right directory
    if not os.path.exists("Simulation_Data"):
        print("❌ Error: Please run this script from the code directory containing Simulation_Data/")
        sys.exit(1)
    
    # Check if simulation data exists
    data_path = "Simulation_Data/new_k_gamma_0_defined_pool_nooverlap_50from500_natural/Community.json"
    if not os.path.exists(data_path):
        print("❌ Error: 500 species simulation data not found!")
        print(f"   Expected: {data_path}")
        print("   Please run the simulation first: python run_simulation_500_species_for_natural.py")
        sys.exit(1)
    
    # Run all analyses
    success = run_analysis()
    sys.exit(0 if success else 1)