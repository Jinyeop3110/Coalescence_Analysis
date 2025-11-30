# ✅ 10 Reps Simulation with Interaction Matrices - COMPLETE

## Summary

**Successfully completed** a fast 10-repetition simulation with full interaction matrices saved!

---

## Key Results

**Total simulations:** 240 (10 reps × 24 interaction strengths)
**Total interaction matrices saved:** 240 (48×48 each)
**File size:** 19.6 MB
**Completion time:** ~10 minutes

---

## Output Files

**Main data file:**
```
Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json
```

**Size:** 19.6 MB

**Contents:**
- 240 complete simulations
- 240 interaction matrices (48×48 each)
- Community compositions (4 communities × 48 species each)
- Coalescence outcomes (6 pairs × 48 species each)
- Growth rates and carrying capacities
- Random seeds for reproducibility

---

## Simulation Parameters

```python
N = 48                    # Total species
num_S = 12                # Species per community
num_C = 4                 # Number of communities
N_reps = 10               # Repetitions per intensity
u_list = [0.05, 0.10, 0.15, ..., 1.20]  # 24 values
threshold = 1e-3          # Extinction threshold
t = [0, 5000]            # Time span
```

---

## Data Structure Verified

```json
{
  "0.05": {
    "rep_000": {
      "sc_list": {...},
      "cc_list": {...},
      "parameters": {
        "seed": 500,
        "u": 0.05,
        "interaction_matrix": [48×48 matrix],  ✅ SAVED
        "growth_rates": [48 values],           ✅ SAVED
        "carrying_capacities": [48 values],    ✅ SAVED
        "interaction_matrix_stats": {
          "mean": 0.0505,
          "std": 0.0288,
          "min": 0.0004,
          "max": 0.0999
        }
      }
    },
    ...
    "rep_009": {...}
  },
  "0.10": {...},
  ...
  "1.20": {...}
}
```

**Verification:**
- ✅ All 24 interaction strengths present
- ✅ All 10 reps per intensity complete
- ✅ All interaction matrices are 48×48
- ✅ All diagonal elements = 1.0
- ✅ Matrix statistics match expected values

---

## How to Use the Data

### Load and Access Matrices

```python
import json
import numpy as np

# Load data
with open('Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json', 'r') as f:
    data = json.load(f)

# Access specific interaction matrix
u_value = "0.50"
rep_number = "rep_005"
I_matrix = np.array(data[u_value][rep_number]['parameters']['interaction_matrix'])

print(f"Interaction matrix shape: {I_matrix.shape}")
print(f"Mean interaction strength: {np.mean(I_matrix[np.triu_indices(48, k=1)]):.4f}")
```

### Analyze All Matrices for a Given u

```python
# Get all matrices for u = 0.5
u_05_matrices = []
for rep in range(10):
    rep_key = f"rep_{rep:03d}"
    I = np.array(data["0.50"][rep_key]['parameters']['interaction_matrix'])
    u_05_matrices.append(I)

print(f"Collected {len(u_05_matrices)} matrices for u = 0.50")

# Analyze variability
means = [np.mean(I[np.triu_indices(48, k=1)]) for I in u_05_matrices]
print(f"Mean interaction strength across reps: {np.mean(means):.4f} ± {np.std(means):.4f}")
```

### Compare Community Outcomes with Interaction Structure

```python
# For a specific simulation
rep_data = data["0.80"]["rep_003"]

# Get interaction matrix
I = np.array(rep_data['parameters']['interaction_matrix'])

# Get community outcomes
communities = rep_data['sc_list']
coalescence = rep_data['cc_list']

# Analyze relationship between interactions and outcomes
# Example: Which species pairs coexist in coalescence?
c1 = np.array(communities['0'])
c2 = np.array(communities['1'])
cmix = np.array(coalescence['0_1'])

# Species present in final coalescence
survivors = cmix > 1e-3
print(f"Species surviving coalescence: {np.sum(survivors)}")

# Analyze their interaction strengths
survivor_indices = np.where(survivors)[0]
I_survivors = I[np.ix_(survivor_indices, survivor_indices)]
print(f"Mean interaction among survivors: {np.mean(I_survivors[np.triu_indices(len(survivor_indices), k=1)]):.4f}")
```

---

## Comparison with Original Data

| Feature | Original 200 reps | New 10 reps |
|---------|------------------|-------------|
| Repetitions | 200 | 10 |
| Total simulations | 4,800 | 240 |
| Interaction matrices | ❌ Not saved | ✅ Saved (48×48) |
| File size | 41 MB | 19.6 MB |
| Completion time | ~hours | ~10 minutes |
| Growth rates | ❌ Not saved | ✅ Saved |
| Carrying capacities | ❌ Not saved | ✅ Saved |

---

## Next Steps

### 1. Generate Phase Diagrams

Use existing plotting code with this new data:

```bash
# Modify plot_phase_diagram_json_simulations.py to include 10 reps data
# Add to json_sessions list:
{
    "name": "48species_10reps_fine",
    "json_file": "Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json",
    "description": "10 reps × 24 intensities with full matrices"
}
```

### 2. Analyze Interaction Patterns

Now that you have the full interaction matrices, you can:

- **Analyze asymmetry:** Compare I[i,j] vs I[j,i] for all species pairs
- **Network properties:** Calculate centrality, modularity of interaction networks
- **Outcome prediction:** Correlate interaction structure with coalescence outcomes
- **Species-specific effects:** Identify which interaction patterns lead to survival
- **Hierarchy analysis:** Link competitive hierarchies to matrix structure

### 3. Statistical Analysis

With 10 reps per intensity:

- Compare variability in outcomes vs variability in interaction matrices
- Test if certain matrix structures consistently produce similar outcomes
- Identify robust vs sensitive coalescence patterns

---

## File Locations

**Main output:**
```
Simulation_Data/48species_10reps_fine_WITH_MATRICES/
├── Community_10reps_fine_WITH_MATRICES.json  (19.6 MB) ← Main data
├── simulation_parameters.xlsx                 (5.1 KB)
├── communityLibrary.xlsx                      (5.6 KB)
└── parameter.xlsx                             (35 KB)
```

**Script used:**
```
run_48species_10reps_fine_WITH_MATRICES.py
```

---

## Performance

**Simulation speed:**
- ~2.5 seconds per repetition
- ~10 minutes total for 240 simulations
- File saves after each intensity (24 saves total)

**Storage:**
- ~82 KB per repetition (includes full 48×48 matrix)
- Scales linearly: 200 reps would be ~200 MB

---

## Validation

All checks passed:
- ✅ 24 intensity values (0.05 to 1.20)
- ✅ 10 repetitions per intensity
- ✅ 240 total simulations
- ✅ All interaction matrices saved correctly
- ✅ All matrices are 48×48
- ✅ All diagonal elements = 1.0
- ✅ Matrix statistics match generation parameters
- ✅ Community and coalescence data complete

---

**Date:** November 1, 2025
**Completion time:** 19:30-19:39 (9 minutes)
**Status:** ✅ COMPLETE AND VERIFIED
