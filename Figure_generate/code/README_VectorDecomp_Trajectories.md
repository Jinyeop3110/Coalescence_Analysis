# Vector Decomposition Trajectory Plots

## Overview

These scripts generate vector decomposition maps showing coalescence trajectories - how mixed communities evolve during the coalescence process starting from the theoretical initial state at (1/√2, 1/√2) ≈ (0.707, 0.707).

## Generated Scripts

### 1. `generate_vectordecomp_with_trajectories.py`
**Single Interaction Matrix Version**

- Uses one fixed random interaction matrix for all 100 simulations
- Shows deterministic dynamics - all trajectories converge to the same point
- Good for understanding the dynamics for a specific interaction network
- **Results for u=0.6:**
  - All 100 trajectories converged to (u=0.314, v=0.873)
  - Demonstrates strong bias towards community 2 for this particular interaction matrix
  - Zero variance in final outcomes (deterministic)

### 2. `generate_vectordecomp_with_varied_trajectories.py` ⭐ **Recommended**
**Varied Interaction Matrices Version**

- Each of the 100 simulations uses a different random interaction matrix
- Shows the diversity of outcomes across different interaction networks at u=0.6
- More representative of the ensemble of possible coalescence outcomes
- **Results for u=0.6:**
  - Final u coordinates: 0.471 ± 0.371 (range: 0.0 - 1.0)
  - Final v coordinates: 0.498 ± 0.370 (range: 0.0 - 1.0)
  - Roughly symmetric around diagonal (u-v ≈ 0)
  - Average distance from initial state: 0.591 ± 0.159

## Output Files

All files are saved to: `Figure_generate/code/Figure/Dynamics/`

### Fixed Interaction Matrix Outputs:
1. **VectorDecomp_u0.6_trajectories.svg**
   - Shows all 100 trajectories on background density field
   - Trajectories in blue, initial state marked with gold star

2. **VectorDecomp_u0.6_trajectories_detailed.svg**
   - Shows 20 individual trajectories with rainbow colors
   - Easier to distinguish individual paths

### Varied Interaction Matrices Outputs:
1. **VectorDecomp_u0.6_varied_trajectories.svg**
   - Shows all 100 trajectories with different interaction matrices
   - Background density field shows distribution of final states
   - Trajectories in steel blue, endpoints in dark blue

2. **VectorDecomp_u0.6_varied_trajectories_detailed.svg**
   - Shows 30 individual trajectories with rainbow colors
   - Circle = start point, Square = end point

## Key Features

### Vector Decomposition Metric
- Projects mixed community composition onto basis of two parent communities
- u = contribution from community 1
- v = contribution from community 2
- Normalized so that u² + v² + k² = 1 (k = novelty component)

### Initial State
- Mixed communities start at (1/√2, 1/√2) ≈ (0.707, 0.707)
- This represents equal contribution from both parent communities
- Marked with gold star in all plots

### Trajectory Evolution
- 100 simulations run for each version
- Each simulation:
  1. Grows two separate communities to equilibrium
  2. Mixes them together (coalescence event)
  3. Tracks vector decomposition coordinates over time
  4. Records ~57 time points from t=0 to t=5000

### Time Points
- Logarithmically spaced for better resolution of early dynamics:
  - 0-100: 20 points
  - 100-500: 14 points
  - 500-2000: 14 points
  - 2000-5000: 9 points

## Interpretation

### Fixed Matrix Version
- Shows that for a given interaction network, coalescence outcomes are deterministic
- The particular u=0.6 matrix tested strongly favored community 2
- Useful for understanding mechanistic details of specific systems

### Varied Matrix Version
- Shows the ensemble behavior across different realizations of u=0.6
- Reveals diversity of possible outcomes
- Distribution roughly symmetric → no systematic bias at u=0.6
- Large spread in outcomes → interaction network structure matters more than average interaction strength

## Parameters

- **u**: 0.6 (interaction strength parameter)
- **num_C**: 2 (number of communities)
- **num_S**: 12 (species per community)
- **N**: 24 (total species)
- **num_reps**: 100 (number of trajectories)
- **threshold**: 1e-3 (extinction threshold)
- **t_final**: 5000 (final simulation time)

## Usage

```bash
# Run fixed interaction matrix version
conda run -n coalescence python Figure_generate/code/generate_vectordecomp_with_trajectories.py

# Run varied interaction matrices version (recommended)
conda run -n coalescence python Figure_generate/code/generate_vectordecomp_with_varied_trajectories.py
```

## Dependencies

- numpy
- matplotlib
- scipy
- LV.py (Lotka-Volterra dynamics)
- InitializeSpeciesPool.py (for varied version only)

## Notes

1. The background density field uses radial smoothing (σ=6.0 for varied version)
2. Trajectories are semi-transparent to show overlap
3. All plots maintain equal aspect ratio for accurate geometric interpretation
4. The varied matrices version is more representative of real coalescence experiments where interaction networks vary
