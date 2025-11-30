#!/usr/bin/env python
"""
Complete pipeline to run 48-species simulations and create heatmap visualizations.
Auto version - runs without user input.

This script:
1. Runs the simulation (if needed)
2. Performs vector decomposition analysis
3. Creates heatmap visualizations

Usage:
python run_48species_complete_pipeline_auto.py
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
        print("Skipping simulation step.")
        return True
    
    print("\n" + "="*70)
    print("RUNNING 48-SPECIES SIMULATION (100 REPETITIONS)")
    print("="*70)
    
    start_time = time.time()
    
    # Run simulation directly using exec to avoid subprocess issues
    print("Running simulation script directly...")
    exec(open("run_48species_100reps_simulation.py").read())
    
    end_time = time.time()
    print(f"\nSimulation completed in {(end_time - start_time)/60:.1f} minutes")
    
    return True


def run_analysis():
    """Run the vector decomposition analysis with heatmap visualization."""
    print("\n" + "="*70)
    print("RUNNING VECTOR DECOMPOSITION ANALYSIS WITH HEATMAP VISUALIZATION")
    print("="*70)
    
    start_time = time.time()
    
    # Run analysis directly using exec to avoid subprocess issues
    print("Running analysis script directly...")
    exec(open("vector_decomp_48species_heatmap.py").read())
    
    end_time = time.time()
    print(f"\nAnalysis completed in {(end_time - start_time)/60:.1f} minutes")
    
    return True


def main():
    """Main pipeline execution."""
    print("\n" + "="*70)
    print("48-SPECIES COALESCENCE SIMULATION AND ANALYSIS PIPELINE (AUTO)")
    print("="*70)
    print("\nThis pipeline will:")
    print("1. Run 100 repetitions of 48-species coalescence simulations")
    print("2. For interaction strengths: 0.3, 0.5, 0.8")
    print("3. Create heatmap visualizations with contours")
    print("\nEstimated time: 30-60 minutes (depending on CPU)")
    print("\nStarting automatically...")
    
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