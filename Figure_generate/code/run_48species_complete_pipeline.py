#!/usr/bin/env python
"""
Complete pipeline to run 48-species simulations and create heatmap visualizations.

This script:
1. Runs the simulation (if needed)
2. Performs vector decomposition analysis
3. Creates heatmap visualizations

Usage:
python run_48species_complete_pipeline.py
"""

import subprocess
import sys
import os
import time


def run_simulation():
    """Run the 48-species simulation if data doesn't exist."""
    data_file = "Simulation_Data/48species_100reps/Community_100reps.json"
    
    if os.path.exists(data_file):
        print(f"Simulation data already exists at: {data_file}")
        response = input("Do you want to re-run the simulation? (y/n): ")
        if response.lower() != 'y':
            return True
    
    print("\n" + "="*70)
    print("RUNNING 48-SPECIES SIMULATION (100 REPETITIONS)")
    print("="*70)
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, "run_48species_100reps_simulation.py"], 
                              check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running simulation: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    
    end_time = time.time()
    print(f"\nSimulation completed in {(end_time - start_time)/60:.1f} minutes")
    
    return True


def run_analysis():
    """Run the vector decomposition analysis with heatmap visualization."""
    print("\n" + "="*70)
    print("RUNNING VECTOR DECOMPOSITION ANALYSIS WITH HEATMAP VISUALIZATION")
    print("="*70)
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, "vector_decomp_48species_heatmap.py"], 
                              check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running analysis: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    
    end_time = time.time()
    print(f"\nAnalysis completed in {(end_time - start_time)/60:.1f} minutes")
    
    return True


def main():
    """Main pipeline execution."""
    print("\n" + "="*70)
    print("48-SPECIES COALESCENCE SIMULATION AND ANALYSIS PIPELINE")
    print("="*70)
    print("\nThis pipeline will:")
    print("1. Run 100 repetitions of 48-species coalescence simulations")
    print("2. For interaction strengths: 0.3, 0.5, 0.8")
    print("3. Create heatmap visualizations with contours")
    print("\nEstimated time: 30-60 minutes (depending on CPU)")
    
    response = input("\nDo you want to continue? (y/n): ")
    if response.lower() != 'y':
        print("Pipeline cancelled.")
        return
    
    # Step 1: Run simulation
    print("\n[Step 1/2] Running simulations...")
    if not run_simulation():
        print("Simulation failed. Exiting pipeline.")
        return
    
    # Step 2: Run analysis
    print("\n[Step 2/2] Running analysis...")
    if not run_analysis():
        print("Analysis failed. Exiting pipeline.")
        return
    
    # Summary
    print("\n" + "="*70)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nResults saved in:")
    print("- Simulation data: Simulation_Data/48species_100reps/Community_100reps.json")
    print("- Heatmap figures: Figure/VectorDecomp_48species_heatmap/")
    print("\nKey outputs:")
    print("- VectorDecomp_48species_u0.3_heatmap.svg")
    print("- VectorDecomp_48species_u0.5_heatmap.svg") 
    print("- VectorDecomp_48species_u0.8_heatmap.svg")
    print("- VectorDecomp_48species_comparison_heatmap.svg")
    print("\nThank you for using the pipeline!")


if __name__ == "__main__":
    main()