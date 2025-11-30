# 500 Reps Simulation with Full Interaction Matrices

## Summary

✅ **Successfully launched** 500 repetitions × 24 interaction strengths simulation
✅ **Saving full 48×48 interaction matrices** for each repetition
✅ **Running in background** with PID 1574

---

## What Changed

### Original Simulation
- **File:** `run_48species_200reps_fine_intervals.py`
- **Output:** `Simulation_Data/48species_200reps_fine/Community_200reps_fine.json` (41 MB)
- **Reps:** 200 per intensity
- **Interaction matrices:** NOT saved (only summary statistics)

### New Simulation
- **File:** `run_48species_200reps_fine_WITH_MATRICES.py`
- **Output:** `Simulation_Data/48species_500reps_fine_WITH_MATRICES/Community_500reps_fine_WITH_MATRICES.json`
- **Reps:** **500 per intensity** (increased from 200)
- **Interaction matrices:** **FULL 48×48 matrices saved for each rep**
- **Expected file size:** ~500-700 MB

---

## Simulation Parameters

```python
N = 48                    # Total species
num_S = 12                # Species per community
num_C = 4                 # Number of communities
N_reps = 500              # Repetitions per intensity (NEW: 500)
u_list = [0.05, 0.10, 0.15, ..., 1.20]  # 24 values
threshold = 1e-3          # Extinction threshold
t = [0, 5000]            # Time span
```

**Total simulations:** 500 reps × 24 intensities = **12,000 simulations**
**Total interaction matrices:** **12,000 matrices** (48×48 each)

---

## Data Structure

### JSON Format

```json
{
  "0.05": {
    "rep_000": {
      "sc_list": {
        "0": [48 species abundances],
        "1": [48 species abundances],
        "2": [48 species abundances],
        "3": [48 species abundances]
      },
      "cc_list": {
        "0_1": [48 species abundances],
        "0_2": [48 species abundances],
        ...
        "2_3": [48 species abundances]
      },
      "parameters": {
        "seed": 500,
        "u": 0.05,
        "interaction_matrix": [
          [1.0, 0.023, 0.067, ...],
          [0.045, 1.0, 0.012, ...],
          ...
          [0.089, 0.034, 0.056, ..., 1.0]
        ],  // NEW: Full 48×48 matrix
        "growth_rates": [1.0, 1.0, ..., 1.0],  // NEW
        "carrying_capacities": [1.0, 1.0, ..., 1.0],  // NEW
        "interaction_matrix_stats": {
          "mean": 0.0505,
          "std": 0.0288,
          "min": 0.0001,  // NEW
          "max": 0.0998   // NEW
        }
      }
    },
    "rep_001": {...},
    ...
    "rep_499": {...}
  },
  "0.10": {...},
  ...
  "1.20": {...}
}
```

---

## Monitoring the Simulation

### Check Progress
```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code

# Single check
python monitor_500reps_simulation.py

# Continuous monitoring (updates every minute)
python monitor_500reps_simulation.py --watch
```

### Check Process Status
```bash
# Check if simulation is running
ps aux | grep run_48species.*WITH_MATRICES | grep -v grep

# Should show:
# jysong  1574  98.8  1.0  ... python run_48species_200reps_fine_WITH_MATRICES.py
```

### Check Output File
```bash
# File size
ls -lh Simulation_Data/48species_500reps_fine_WITH_MATRICES/Community_500reps_fine_WITH_MATRICES.json

# Current status
python3 -c "import json; data = json.load(open('Simulation_Data/48species_500reps_fine_WITH_MATRICES/Community_500reps_fine_WITH_MATRICES.json')); print(f'Intensities: {len(data)}, Total reps: {sum(len(data[u]) for u in data)}')"
```

---

## Timeline Estimates

- **Started:** November 1, 2025, 7:20 PM
- **Estimated completion:** ~8 hours (November 2, 2025, ~3:20 AM)
- **Progress updates:** Saves every 20 repetitions

Current status:
- 0.5% complete (60 / 12,000 repetitions)
- File size: 5.1 MB → Expected: 500-700 MB
- Working on: u = 0.05

---

## Files Created

### Main Simulation Script
- `run_48species_200reps_fine_WITH_MATRICES.py` - Modified simulation code

### Test Scripts
- `test_matrices_save.py` - Small test (2 reps × 2 intensities) ✅ PASSED
- `monitor_500reps_simulation.py` - Progress monitoring tool

### Output Directory
`Simulation_Data/48species_500reps_fine_WITH_MATRICES/`
- `Community_500reps_fine_WITH_MATRICES.json` - Main data file (growing)
- `simulation_parameters.xlsx` - Simulation metadata
- `communityLibrary.xlsx` - Community composition (gets overwritten)
- `parameter.xlsx` - Last I, g, k matrices (gets overwritten)

---

## Using the Data

### Load Data
```python
import json
import numpy as np

# Load full data
with open('Simulation_Data/48species_500reps_fine_WITH_MATRICES/Community_500reps_fine_WITH_MATRICES.json', 'r') as f:
    data = json.load(f)

# Access interaction matrix for specific simulation
u_value = "0.05"
rep_number = "rep_000"
I_matrix = np.array(data[u_value][rep_number]['parameters']['interaction_matrix'])

print(f"Interaction matrix shape: {I_matrix.shape}")
print(f"Diagonal: {np.diag(I_matrix)[:5]}")  # Should be [1, 1, 1, 1, 1]
print(f"Mean: {np.mean(I_matrix[np.triu_indices(48, k=1)])}")
```

### Extract Specific Data
```python
# Get all interaction matrices for u = 0.5
u_05_matrices = []
for rep in range(500):
    rep_key = f"rep_{rep:03d}"
    if rep_key in data["0.50"]:
        I = np.array(data["0.50"][rep_key]['parameters']['interaction_matrix'])
        u_05_matrices.append(I)

print(f"Collected {len(u_05_matrices)} matrices for u = 0.50")
```

### Reproduce Exact Simulation
```python
# Each simulation can be exactly reproduced using the seed
seed = data[u_value][rep_number]['parameters']['seed']
u = data[u_value][rep_number]['parameters']['u']

np.random.seed(seed)
# Regenerate the exact same interaction matrix...
```

---

## Differences from Original

| Feature | Original (200 reps) | New (500 reps) |
|---------|---------------------|----------------|
| Repetitions per u | 200 | **500** |
| Total simulations | 4,800 | **12,000** |
| Interaction matrix | ❌ Not saved | ✅ **Full 48×48 saved** |
| Growth rates | ❌ Not saved | ✅ Saved (all 1.0) |
| Carrying capacities | ❌ Not saved | ✅ Saved (all 1.0) |
| Matrix min/max | ❌ Not saved | ✅ Saved in stats |
| File size | 41 MB | **~600 MB** (est.) |
| Random seed | ✅ Saved | ✅ Saved |
| Community outcomes | ✅ Saved | ✅ Saved |

---

## Why This Matters

### Previously
- Could reconstruct matrices using seed (requires re-running generation)
- Only had summary statistics (mean, std)
- Harder to analyze specific interaction patterns

### Now
- **Direct access** to all interaction matrices
- Can analyze:
  - Specific interaction strengths between species
  - Asymmetry in interactions (I[i,j] vs I[j,i])
  - Correlation between interaction structure and outcomes
  - Species-specific competitive advantages
  - Network properties of interaction matrices
- **No need to regenerate** - everything is stored

---

## Next Steps

1. **Wait for completion** (~8 hours from 7:20 PM)
2. **Verify final output:**
   ```bash
   python monitor_500reps_simulation.py
   ```
3. **Generate phase diagrams** using existing plotting code
4. **Analyze interaction matrices** to understand outcome patterns

---

## Contact

- **Simulation started by:** Claude Code Assistant
- **Date:** November 1, 2025
- **Environment:** coalescence (conda)
- **Location:** `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code`

---

## Troubleshooting

### If simulation stops
```bash
# Check if still running
ps aux | grep 1574

# If stopped, restart from last save point
# The JSON file is saved every 20 reps, so minimal loss
conda activate coalescence
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code
python run_48species_200reps_fine_WITH_MATRICES.py
```

### If file gets corrupted
- Backups are saved every 20 reps
- Check file integrity:
  ```python
  import json
  with open('Simulation_Data/48species_500reps_fine_WITH_MATRICES/Community_500reps_fine_WITH_MATRICES.json') as f:
      data = json.load(f)  # Will error if corrupted
  ```

---

**Status:** ✅ Running successfully
**Last updated:** November 1, 2025, 7:23 PM
