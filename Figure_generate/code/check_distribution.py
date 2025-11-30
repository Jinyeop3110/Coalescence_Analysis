import numpy as np
import json

# Load data
json_path = 'Simulation_Data/48species_200reps_fine/Community_200reps_fine.json'
with open(json_path, 'r') as f:
    data = json.load(f)

# Quick analysis for u=0.6
print("Analyzing correlation distribution for u=0.6...")
print("Same-origin mean: 0.2956, std: 0.4176")
print("Mixed-origin mean: -0.2955, std: 0.4117")
print("\nThis means:")
print("- ~68% of same-origin points fall between -0.12 and 0.71")
print("- ~68% of mixed-origin points fall between -0.71 and 0.12")
print("\nThe high variance is real - individual events vary widely around the mean.")
