# Final Summary: 20 Reps Narrow vs Wide Uniform Distributions

## ✅ COMPLETE - Both Simulations and Phase Diagrams Ready

---

## What Was Accomplished

Successfully ran **480 simulations each** (24 interaction strengths × 20 reps) for both narrow and wide uniform distributions, with **CORRECT coalescence initial conditions** (0.5 × equilibrium_c1 + 0.5 × equilibrium_c2).

---

## Phase Diagrams Generated

### 1. Narrow Uniform Distribution [0.5μ, 1.5μ]
**File:** [Figure/PhaseDiagram/Fig_phase_diagram_20reps_narrow_uniform.svg](Figure/PhaseDiagram/Fig_phase_diagram_20reps_narrow_uniform.svg)
- **CV:** 0.289 (low variance)
- **Data points:** 2,706 coalescence events
- **Size:** 17.8 KB

### 2. Wide Uniform Distribution [0, 2μ]
**File:** [Figure/PhaseDiagram/Fig_phase_diagram_20reps_wide_uniform.svg](Figure/PhaseDiagram/Fig_phase_diagram_20reps_wide_uniform.svg)
- **CV:** 0.577 (high variance - 4× the variance of narrow)
- **Data points:** 2,722 coalescence events
- **Size:** 17.8 KB

---

## Key Comparison

| Property | Narrow Uniform [0.5μ, 1.5μ] | Wide Uniform [0, 2μ] |
|----------|------------------------------|----------------------|
| **Range at μ=0.5** | [0.25, 0.75] | [0, 1.0] |
| **CV** | 0.289 | 0.577 |
| **Variance** | μ²/12 | μ²/3 |
| **Variance Ratio** | 1× (baseline) | **4×** (4 times larger!) |
| **Standard Deviation** | 0.289μ | 0.577μ |
| **Biological Interpretation** | Homogeneous interactions | Heterogeneous interactions |

---

## Critical Fix Applied

### The Problem
Original simulations used **INCORRECT** coalescence initial conditions:
```python
# WRONG: Both communities start at arbitrary low abundance
y0[community1_species] = 0.01
y0[community2_species] = 0.01
```

### The Solution
Now uses **CORRECT** coalescence initial conditions:
```python
# CORRECT: Mix 50% of each community's equilibrium state
c1_equilibrium = sc_list["c1"]  # Community 1 at equilibrium
c2_equilibrium = sc_list["c2"]  # Community 2 at equilibrium
y0 = 0.5 * c1_equilibrium + 0.5 * c2_equilibrium
```

This properly models **mixing two established communities**, which is what coalescence experiments actually do!

---

## Simulation Details

### Common Parameters
- **Species:** 48 total (4 communities × 12 species each)
- **Repetitions:** 20 per interaction strength
- **Interaction strengths (μ):** 24 values from 0.05 to 1.20 (step 0.05)
- **Total simulations per distribution:** 480
- **Integration time:** 0 to 2000 time units
- **Extinction threshold:** 10⁻⁶
- **Growth rates (g):** All 1.0
- **Carrying capacities (k):** All 1.0
- **Diagonal elements (self-interaction):** All 1.0

### Narrow Uniform Distribution
- **Function:** `I[i,j] ~ Uniform[0.5μ, 1.5μ]`
- **Runtime:** ~17 minutes
- **Data file:** `Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json`
- **File size:** 39 MB
- **Successful events:** 2,706 / 2,880 possible (94%)

### Wide Uniform Distribution
- **Function:** `I[i,j] ~ Uniform[0, 2μ]`
- **Runtime:** ~16 minutes
- **Data file:** `Simulation_Data/48species_20reps_wide_uniform/Community_20reps_wide_uniform.json`
- **File size:** 39 MB
- **Successful events:** 2,722 / 2,880 possible (94.5%)

---

## File Structure

### Simulation Data
```
Simulation_Data/
├── 48species_20reps_narrow_uniform/
│   ├── Community_20reps_narrow_uniform.json (39 MB)
│   └── simulation_parameters.xlsx
└── 48species_20reps_wide_uniform/
    ├── Community_20reps_wide_uniform.json (39 MB)
    └── simulation_parameters.xlsx
```

### Phase Diagrams
```
Figure/PhaseDiagram/
├── Fig_phase_diagram_20reps_narrow_uniform.svg (18 KB)
└── Fig_phase_diagram_20reps_wide_uniform.svg (18 KB)
```

### Scripts
```
Code/
├── run_uniform_narrow_range.py     (narrow simulation)
├── run_uniform_wide_range.py       (wide simulation)
└── plot_both_distributions.py      (plotting both)
```

---

## Data Structure

Each JSON file contains:
```json
{
  "0.50": {                          // Interaction strength (μ)
    "rep_000": {                     // Repetition 0
      "sc_list": {                   // Single communities
        "c1": [...],                 // Community 1 at equilibrium (48 abundances)
        "c2": [...],                 // Community 2 at equilibrium
        "c3": [...],                 // Community 3 at equilibrium
        "c4": [...]                  // Community 4 at equilibrium
      },
      "cc_list": {                   // Coalescence events
        "c1_c2": [...],              // c1+c2 coalescence outcome
        "c1_c3": [...],              // c1+c3 coalescence outcome
        "c1_c4": [...],              // c1+c4 coalescence outcome
        "c2_c3": [...],              // c2+c3 coalescence outcome
        "c2_c4": [...],              // c2+c4 coalescence outcome
        "c3_c4": [...]               // c3+c4 coalescence outcome
      },
      "parameters": {
        "seed": 5000,
        "u": 0.5,
        "distribution": "uniform_narrow" or "uniform_wide",
        "interaction_matrix": [[48×48 matrix]],
        "growth_rates": [48 values],
        "carrying_capacities": [48 values],
        "interaction_matrix_stats": {
          "mean": 0.502,
          "std": 0.145,              // Different for narrow vs wide
          "min": 0.001,
          "max": 1.998,
          "theoretical_cv": 0.289 or 0.577,
          "empirical_cv": 0.289 or 0.577
        }
      }
    },
    "rep_001": {...},
    ...
    "rep_019": {...}
  },
  "0.55": {...},
  ...
}
```

---

## Phase Diagram Interpretation

Each phase diagram shows three stacked areas representing the fraction of coalescence events resulting in:

1. **Red (Dominance):** One community dominates, the other goes extinct
2. **Purple (Mixing):** Both communities coexist stably
3. **Green (Restructuring):** Completely different outcome from either parent community

### Expected Differences

**At Low Interaction Strength (μ < 0.3):**
- **Narrow:** More mixing (predictable weak interactions)
- **Wide:** More variable outcomes (some interactions by chance are stronger)

**At Intermediate Interaction Strength (0.3 < μ < 0.8):**
- **Narrow:** Sharper transitions between phases
- **Wide:** Smoother transitions (more stochasticity)

**At High Interaction Strength (μ > 0.8):**
- **Narrow:** Consistent dominance (strong competition)
- **Wide:** Mix of dominance and restructuring (occasional very strong interactions)

---

## Next Steps for Analysis

### 1. Visual Comparison
Open both SVG files side-by-side:
- `Fig_phase_diagram_20reps_narrow_uniform.svg`
- `Fig_phase_diagram_20reps_wide_uniform.svg`

### 2. Quantitative Analysis
```python
import json
import numpy as np

# Load both datasets
with open('Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json') as f:
    narrow_data = json.load(f)

with open('Simulation_Data/48species_20reps_wide_uniform/Community_20reps_wide_uniform.json') as f:
    wide_data = json.load(f)

# Compare outcome fractions at each interaction strength
# Calculate statistical significance of differences
# Identify interaction strengths where variance matters most
```

### 3. Specific Questions to Answer

**Q1:** Does higher variance lead to more restructuring?
- **Hypothesis:** Wide distribution has more green (restructuring) area

**Q2:** Are phase transitions sharper with lower variance?
- **Hypothesis:** Narrow distribution has more abrupt color changes

**Q3:** At what interaction strength does variance matter most?
- **Method:** Calculate difference in outcome fractions between distributions

**Q4:** Is there a critical CV value where outcomes fundamentally change?
- **Future:** Run intermediate CV values (0.3, 0.4, 0.5, etc.)

---

## Mathematical Verification

### Narrow Uniform [0.5μ, 1.5μ]
```
Mean = (0.5μ + 1.5μ) / 2 = μ ✓
Variance = (1.5μ - 0.5μ)² / 12 = μ² / 12
Std = μ / (2√3) ≈ 0.289μ
CV = 1 / (2√3) ≈ 0.289
```

### Wide Uniform [0, 2μ]
```
Mean = (0 + 2μ) / 2 = μ ✓
Variance = (2μ - 0)² / 12 = μ² / 3
Std = μ / √3 ≈ 0.577μ
CV = 1 / √3 ≈ 0.577
```

### Variance Ratio
```
Var(wide) / Var(narrow) = (μ²/3) / (μ²/12) = 4
```

**Wide distribution has EXACTLY 4× the variance of narrow!**

---

## Documentation Files

- **[COALESCENCE_INITIAL_CONDITION_FIX.md](COALESCENCE_INITIAL_CONDITION_FIX.md)** - Explains the critical fix to coalescence initial conditions
- **[NARROW_UNIFORM_SUMMARY.md](NARROW_UNIFORM_SUMMARY.md)** - Details about narrow distribution implementation
- **[DISTRIBUTION_COMPARISON.md](DISTRIBUTION_COMPARISON.md)** - Mathematical comparison of distributions (for gamma)
- **[GAMMA_DISTRIBUTION_GUIDE.md](GAMMA_DISTRIBUTION_GUIDE.md)** - Guide for gamma distribution (future work)
- **[FINAL_SUMMARY_20REPS.md](FINAL_SUMMARY_20REPS.md)** - This file

---

## Command Reference

### Rerun Simulations
```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code
conda activate coalescence

# Narrow uniform
python run_uniform_narrow_range.py

# Wide uniform
python run_uniform_wide_range.py
```

### Regenerate Phase Diagrams
```bash
# Both at once
python plot_both_distributions.py
```

### Check File Sizes
```bash
ls -lh Simulation_Data/48species_20reps*/Community*.json
ls -lh Figure/PhaseDiagram/Fig_phase_diagram_20reps*.svg
```

---

## Performance Statistics

| Metric | Narrow Uniform | Wide Uniform |
|--------|----------------|--------------|
| **Total simulations** | 480 | 480 |
| **Runtime** | 17 min | 16 min |
| **Average per simulation** | 2.1 sec | 2.0 sec |
| **Data file size** | 39 MB | 39 MB |
| **Coalescence events** | 2,706 | 2,722 |
| **Success rate** | 94.0% | 94.5% |
| **Phase diagram size** | 17.8 KB | 17.8 KB |

---

## Summary

✅ **Successfully completed:**
1. Fixed critical bug in coalescence initial conditions
2. Implemented correct narrow uniform distribution [0.5μ, 1.5μ]
3. Implemented correct wide uniform distribution [0, 2μ]
4. Ran 480 simulations for each distribution (20 reps × 24 interaction strengths)
5. Generated phase diagrams for both distributions
6. Saved all interaction matrices for future analysis

✅ **Ready for analysis:**
- Phase diagrams can be directly compared
- All raw data available with full 48×48 interaction matrices
- Can now investigate how variance affects coalescence outcomes

✅ **Key finding confirmed:**
- Wide distribution has **4× the variance** of narrow distribution
- Both maintain the same mean at each interaction strength
- This is a clean experiment to test the effect of heterogeneity!

---

## Files to Share/Analyze

1. **Phase Diagrams (ready to view):**
   - `Figure/PhaseDiagram/Fig_phase_diagram_20reps_narrow_uniform.svg`
   - `Figure/PhaseDiagram/Fig_phase_diagram_20reps_wide_uniform.svg`

2. **Raw Data (for further analysis):**
   - `Simulation_Data/48species_20reps_narrow_uniform/Community_20reps_narrow_uniform.json`
   - `Simulation_Data/48species_20reps_wide_uniform/Community_20reps_wide_uniform.json`

3. **Scripts (reproducible):**
   - `run_uniform_narrow_range.py`
   - `run_uniform_wide_range.py`
   - `plot_both_distributions.py`

Everything is ready for analysis and comparison! 🎉
