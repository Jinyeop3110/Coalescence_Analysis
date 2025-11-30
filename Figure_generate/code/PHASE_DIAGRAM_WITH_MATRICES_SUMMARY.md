# Phase Diagrams with Interaction Matrices - Summary

## ✅ Completed

Successfully generated phase diagrams for simulations that include full interaction matrices!

---

## Generated Files

### 1. **10 Reps Phase Diagram** (READY TO USE)

**File:** [Figure/PhaseDiagram/Fig_phase_diagram_10reps_WITH_MATRICES.svg](Figure/PhaseDiagram/Fig_phase_diagram_10reps_WITH_MATRICES.svg)

**Data source:** `Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json`

**Statistics:**
- **Repetitions:** 10 per intensity
- **Interaction strengths:** 24 (0.05 to 1.20, step 0.05)
- **Total coalescence events:** 1,440 (10 reps × 24 u × 6 pairs)
- **Interaction matrices:** 240 (48×48 each, fully saved)
- **File size:** 17.9 KB

**Status:** ✅ **Complete and ready to use**

---

### 2. **500 Reps Phase Diagram** (FOR FUTURE)

**File:** [Figure/PhaseDiagram/Fig_phase_diagram_500reps_WITH_MATRICES.svg](Figure/PhaseDiagram/Fig_phase_diagram_500reps_WITH_MATRICES.svg)

**Data source:** `Simulation_Data/48species_500reps_fine_WITH_MATRICES/Community_500reps_fine_WITH_MATRICES.json`

**Planned statistics:**
- **Repetitions:** 500 per intensity
- **Interaction strengths:** 24 (0.05 to 1.20, step 0.05)
- **Total coalescence events:** 72,000 (500 reps × 24 u × 6 pairs)
- **Interaction matrices:** 12,000 (48×48 each)
- **Expected file size:** ~600 MB

**Status:** 🔄 **Requires running full 500 reps simulation (~8 hours)**

**Current status:** Partial data from previous interrupted run (200 reps at u=0.05 only)

---

## Comparison with Original

| Feature | Original 200 reps | New 10 reps | Planned 500 reps |
|---------|------------------|-------------|------------------|
| **Phase diagram file** | Fig_phase_diagram_48species_200reps_fine.svg | Fig_phase_diagram_10reps_WITH_MATRICES.svg | Fig_phase_diagram_500reps_WITH_MATRICES.svg |
| **Repetitions** | 200 | 10 | 500 |
| **Total simulations** | 4,800 | 240 | 12,000 |
| **Coalescence events** | 28,800 | 1,440 | 72,000 |
| **Interaction matrices** | ❌ Not saved | ✅ 240 matrices | ✅ 12,000 matrices |
| **Data file size** | 41 MB | 19.6 MB | ~600 MB |
| **Completion time** | Historical | ✅ 9 min | ~8 hours |
| **Status** | Complete | ✅ **Complete** | Needs running |

---

## Scripts

### Simulation Scripts

**10 reps (COMPLETED):**
```bash
# Already run
python run_48species_10reps_fine_WITH_MATRICES.py
```

**500 reps (FOR FUTURE):**
```bash
# Run this when ready for production version
conda activate coalescence
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code

# Run in background (takes ~8 hours)
nohup python run_48species_200reps_fine_WITH_MATRICES.py > simulation_500reps.log 2>&1 &

# Monitor progress
python monitor_500reps_simulation.py --watch
```

### Plotting Script

**Single script handles both 10 and 500 reps:**
```bash
python plot_phase_diagrams_WITH_MATRICES.py
```

This script:
- Automatically detects available data
- Generates phase diagrams for both 10 and 500 reps
- Uses same format as original plots (compatible with existing pipeline)

---

## Usage Examples

### Load and Visualize 10 Reps Data

```python
import json
import numpy as np
import matplotlib.pyplot as plt

# Load data
with open('Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json') as f:
    data = json.load(f)

# Example: Analyze u = 0.5, rep 5
I = np.array(data["0.50"]["rep_005"]["parameters"]["interaction_matrix"])

# Plot interaction matrix
plt.figure(figsize=(8, 8))
plt.imshow(I, cmap='RdBu_r', vmin=-0.5, vmax=2.5)
plt.colorbar(label='Interaction strength')
plt.title('Interaction Matrix (u=0.5, rep 5)')
plt.xlabel('Species j')
plt.ylabel('Species i')
plt.savefig('interaction_matrix_example.pdf')
```

### Compare Outcomes Across Interaction Strengths

```python
# Analyze how outcomes change with interaction strength
from common_setup import metric_VectorDecomposition_onlyPositive, calculate_assymetricity, characterize_case

outcomes_by_u = {}

for u_str in ['0.20', '0.50', '0.80', '1.00']:
    outcomes = []
    for rep in range(10):
        rep_key = f"rep_{rep:03d}"
        rep_data = data[u_str][rep_key]

        # Analyze first coalescence pair (0_1)
        c1 = np.array(rep_data['sc_list']['0'])
        c2 = np.array(rep_data['sc_list']['1'])
        cmix = np.array(rep_data['cc_list']['0_1'])

        u_coeff, v_coeff, k_coeff = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
        x, y = calculate_assymetricity(u_coeff, v_coeff, k_coeff)
        outcome = characterize_case(x, y)  # 0=Dominance, 1=Mixing, 2=Restructuring

        outcomes.append(outcome)

    outcomes_by_u[u_str] = outcomes
    print(f"u = {u_str}: Dominance: {outcomes.count(0)}, Mixing: {outcomes.count(1)}, Restructuring: {outcomes.count(2)}")
```

---

## Workflow for 500 Reps Production Run

### Step 1: Run Simulation
```bash
# Start simulation (run overnight)
conda activate coalescence
cd Figure_generate/code
nohup python run_48species_200reps_fine_WITH_MATRICES.py > sim500.log 2>&1 &
```

### Step 2: Monitor Progress
```bash
# Check progress
python monitor_500reps_simulation.py

# Continuous monitoring
python monitor_500reps_simulation.py --watch
```

### Step 3: Generate Phase Diagram
```bash
# After simulation completes
python plot_phase_diagrams_WITH_MATRICES.py
```

**Output:** `Figure/PhaseDiagram/Fig_phase_diagram_500reps_WITH_MATRICES.svg`

---

## Key Advantages of Having Interaction Matrices

### Now Possible:

1. **Direct interaction analysis:**
   - Compare I[i,j] vs I[j,i] for asymmetry
   - Identify hierarchical structures
   - Network topology analysis

2. **Outcome prediction:**
   - Correlate matrix properties with coalescence outcomes
   - Identify which interaction patterns lead to dominance/mixing/restructuring

3. **Species-specific analysis:**
   - Which species are strong competitors? (high I[i,j] values)
   - Which species facilitate others? (low/negative I[i,j] values)
   - Keystone species identification

4. **Mechanistic understanding:**
   - Link specific interaction strengths to outcomes
   - Test theoretical predictions
   - Validate models

### Previously:

- Could only reconstruct matrices from seeds (slower)
- Only had summary statistics (mean, std)
- Limited ability to analyze specific interactions

---

## File Locations

### Data Files
```
Simulation_Data/
├── 48species_10reps_fine_WITH_MATRICES/
│   └── Community_10reps_fine_WITH_MATRICES.json (19.6 MB) ✅
└── 48species_500reps_fine_WITH_MATRICES/
    └── Community_500reps_fine_WITH_MATRICES.json (partial) 🔄
```

### Phase Diagrams
```
Figure/PhaseDiagram/
├── Fig_phase_diagram_10reps_WITH_MATRICES.svg (17.9 KB) ✅
└── Fig_phase_diagram_500reps_WITH_MATRICES.svg (18.1 KB) 🔄
```

### Scripts
```
run_48species_10reps_fine_WITH_MATRICES.py       (completed)
run_48species_200reps_fine_WITH_MATRICES.py      (for 500 reps)
plot_phase_diagrams_WITH_MATRICES.py             (plotting script)
monitor_500reps_simulation.py                    (monitoring tool)
```

---

## Recommendations

### For Immediate Use:
✅ **Use the 10 reps version:**
- File: `Fig_phase_diagram_10reps_WITH_MATRICES.svg`
- Complete data for all 24 interaction strengths
- All 240 interaction matrices saved and accessible
- Good for initial analysis and exploration

### For Publication/Final Analysis:
🔄 **Run the 500 reps version:**
- Much better statistics (500 vs 10 reps)
- Same format, same plotting script
- Takes ~8 hours but provides publication-quality data
- 12,000 interaction matrices for comprehensive analysis

---

## Next Steps

1. **Immediate:** Use 10 reps phase diagram for current analysis
2. **Soon:** Run 500 reps simulation when ready for production
3. **Future:** Analyze interaction matrices to understand coalescence mechanisms

---

**Date:** November 1, 2025
**Status:** ✅ 10 reps complete, 500 reps ready to run
**Location:** `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code`
