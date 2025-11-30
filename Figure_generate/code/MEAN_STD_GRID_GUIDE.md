# Mean × Std Grid Simulation Guide

## Overview

This simulation explores the **2D parameter space** of mean and standard deviation independently, rather than just varying mean with a fixed coefficient of variation (CV).

---

## Key Difference from Previous Simulations

### Previous Approach (Uniform Distributions)
- **Fixed CV:** Variance scaled proportionally with mean
- **1D sweep:** Only varied mean, CV was locked at 0.289 or 0.577
- **Question:** How does mean interaction strength affect outcomes?

### New Approach (Mean × Std Grid)
- **Independent control:** Mean and std can be varied separately
- **2D grid:** Explores all combinations of mean and std
- **Question:** How do BOTH mean AND variance independently affect outcomes?

---

## Parameter Space

### Grid Specification

**Mean values:** 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2 (12 values)
**Std values:** 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 (6 values)

**Grid size:** 12 × 6 = **72 parameter combinations**
**Repetitions:** 100 per combination
**Total simulations:** 72 × 100 = **7,200 simulations**

### Visual Grid

```
                              Mean →
      0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9  1.0  1.1  1.2
    ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
0.1 │    │    │    │    │    │    │    │    │    │    │    │    │
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
Std 0.2 │    │    │    │    │    │    │    │    │    │    │    │    │
 ↓  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
    0.3 │    │    │    │    │    │    │    │    │    │    │    │    │
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
    0.4 │    │    │    │    │    │    │    │    │    │    │    │    │
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
    0.5 │    │    │    │    │    │    │    │    │    │    │    │    │
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
    0.6 │    │    │    │    │    │    │    │    │    │    │    │    │
    └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘

Each cell: 100 repetitions
```

---

## Distribution: Truncated Normal

### Why Truncated Normal?

We use **truncated normal distribution** N(mean, std²) with support [0, ∞) because:

1. **Non-negative interactions:** Ensures all I[i,j] ≥ 0 (biologically realistic)
2. **Independent parameters:** Mean and std can be set independently
3. **Smooth distribution:** More realistic than uniform

### Mathematical Definition

```python
I[i,j] ~ TruncatedNormal(μ=mean, σ=std, lower=0, upper=∞)
```

Properties:
- **Support:** [0, ∞)
- **Target mean:** μ
- **Target std:** σ
- **Actual mean/std:** Slightly different due to truncation at 0

### Truncation Effect

The truncation at 0 causes a small shift in the empirical mean and std:

| Target Mean | Target Std | Empirical Mean | Empirical Std | Shift |
|-------------|------------|----------------|---------------|-------|
| 0.5 | 0.1 | ~0.502 | ~0.098 | Small |
| 0.5 | 0.3 | ~0.512 | ~0.285 | Moderate |
| 0.1 | 0.1 | ~0.125 | ~0.085 | Larger |

**Note:** The shift is largest when std is large relative to mean (high CV).

---

## Coefficient of Variation (CV) Across Grid

CV = std / mean

The grid covers a wide range of CV values:

### CV Values in Grid

```
                              Mean →
      0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9   1.0   1.1   1.2
    ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
0.05│ 0.5 │ 0.25│ 0.17│ 0.12│ 0.1 │ 0.08│ 0.07│ 0.06│ 0.06│ 0.05│ 0.05│ 0.04│
    ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
0.10│ 1.0 │ 0.5 │ 0.33│ 0.25│ 0.2 │ 0.17│ 0.14│ 0.12│ 0.11│ 0.1 │ 0.09│ 0.08│
Std ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
 ↓  0.20│ 2.0 │ 1.0 │ 0.67│ 0.5 │ 0.4 │ 0.33│ 0.29│ 0.25│ 0.22│ 0.2 │ 0.18│ 0.17│
    ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
    0.30│ 3.0 │ 1.5 │ 1.0 │ 0.75│ 0.6 │ 0.5 │ 0.43│ 0.38│ 0.33│ 0.3 │ 0.27│ 0.25│
    ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
    0.60│ 6.0 │ 3.0 │ 2.0 │ 1.5 │ 1.2 │ 1.0 │ 0.86│ 0.75│ 0.67│ 0.6 │ 0.55│ 0.5 │
    └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

**CV Range:** 0.04 to 6.0 (very wide range!)

---

## Example Parameter Combinations

### Low Mean, Low Std (mean=0.2, std=0.05)
- **CV = 0.25** (low variability)
- **Interpretation:** Weak, homogeneous interactions
- **Expected outcome:** More mixing

### Medium Mean, Medium Std (mean=0.5, std=0.15)
- **CV = 0.3** (moderate variability)
- **Interpretation:** Moderate, somewhat variable interactions
- **Expected outcome:** Mix of outcomes

### High Mean, Low Std (mean=1.0, std=0.1)
- **CV = 0.1** (very low variability)
- **Interpretation:** Strong, homogeneous interactions
- **Expected outcome:** Consistent dominance

### High Mean, High Std (mean=1.0, std=0.5)
- **CV = 0.5** (high variability)
- **Interpretation:** Strong, heterogeneous interactions
- **Expected outcome:** Variable outcomes, possibly restructuring

### Low Mean, High Std (mean=0.2, std=0.3)
- **CV = 1.5** (very high variability!)
- **Interpretation:** Weak on average, but occasional strong interactions
- **Expected outcome:** Unpredictable

---

## Computational Requirements

### Time Estimate
- **Simulations:** 7,200
- **Time per simulation:** ~2 seconds
- **Total time:** ~14,400 seconds ≈ **4 hours**

### Storage Estimate
- **Each simulation:** ~10 KB (with full 48×48 matrix)
- **Total data:** 7,200 × 10 KB ≈ **70 MB**
- **With JSON overhead:** ~**100-150 MB**

### Checkpointing
- **Automatic saves** every 100 simulations
- Can resume if interrupted
- Checkpoint files automatically cleaned up at end

---

## Running the Simulation

### Basic Usage

```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code
conda activate coalescence

python run_mean_std_grid.py
```

The script will:
1. Show parameter grid summary
2. Estimate time and file size
3. **Ask for confirmation** before starting
4. Save checkpoints every 100 simulations
5. Clean up temporary files when done

### Output Files

```
Simulation_Data/mean_std_grid_100reps/
├── Community_mean_std_grid_100reps.json      # Main data file (~200-300 MB)
├── simulation_parameters.xlsx                 # All 14,400 parameter combinations
└── parameter_grid.xlsx                        # Summary of 144 unique (mean, std) pairs
```

---

## Data Structure

### JSON Format

```json
{
  "mean0.50_std0.15": {                // Parameter combination key
    "rep_000": {                       // Repetition 0
      "sc_list": {
        "c1": [...],                   // 48 abundances
        "c2": [...],
        "c3": [...],
        "c4": [...]
      },
      "cc_list": {
        "c1_c2": [...],                // Coalescence outcomes
        "c1_c3": [...],
        "c1_c4": [...],
        "c2_c3": [...],
        "c2_c4": [...],
        "c3_c4": [...]
      },
      "parameters": {
        "seed": 10000,
        "target_mean": 0.5,
        "target_std": 0.15,
        "target_cv": 0.3,
        "distribution": "truncated_normal",
        "interaction_matrix": [[48×48]],
        "growth_rates": [48 values],
        "carrying_capacities": [48 values],
        "interaction_matrix_stats": {
          "empirical_mean": 0.502,     // Actual mean after truncation
          "empirical_std": 0.148,      // Actual std after truncation
          "empirical_cv": 0.295,
          "min": 0.001,
          "max": 1.234
        }
      }
    },
    "rep_001": {...},
    ...
    "rep_099": {...}
  },
  "mean0.50_std0.20": {...},
  ...
}
```

---

## Analysis Possibilities

### 1. 2D Heatmaps

Create heatmaps showing fraction of each outcome type (dominance/mixing/restructuring) across the mean-std grid:

```python
import matplotlib.pyplot as plt
import numpy as np

# Create 12×12 heatmap for each outcome type
# X-axis: mean (0.1 to 1.2)
# Y-axis: std (0.05 to 0.6)
# Color: fraction of dominance/mixing/restructuring
```

### 2. Iso-CV Contours

Extract data along lines of constant CV:

```python
# CV = 0.3 line
points = [
    (mean=0.1, std=0.03),
    (mean=0.2, std=0.06),
    (mean=0.3, std=0.09),
    (mean=0.5, std=0.15),
    (mean=1.0, std=0.30),
]
```

### 3. Compare Mean Effect at Different Std

```python
# Fix std=0.2, vary mean
# Fix std=0.4, vary mean
# Compare how mean affects outcomes at different variance levels
```

### 4. Compare Std Effect at Different Mean

```python
# Fix mean=0.5, vary std
# Fix mean=1.0, vary std
# Compare how variance affects outcomes at different mean levels
```

---

## Research Questions

### Primary Question
**How do mean and variance independently and jointly affect community coalescence outcomes?**

### Specific Hypotheses

1. **Main effects:**
   - Higher mean → More dominance
   - Higher std → More restructuring

2. **Interaction effects:**
   - At low mean, std has little effect (all interactions weak regardless of variance)
   - At high mean, std matters a lot (variance in strong interactions matters)

3. **CV vs independent mean/std:**
   - Is CV (relative variability) the important factor, or absolute variance?
   - Do systems with same CV but different (mean, std) behave differently?

4. **Critical transitions:**
   - Are there sharp boundaries in the mean-std space where outcomes change?
   - Does the phase diagram structure depend on the path through parameter space?

---

## Comparison with Previous Simulations

### Narrow Uniform [0.5μ, 1.5μ] - CV = 0.289
This is approximately equivalent to points along a diagonal in the grid:
- (mean=0.3, std=0.087)
- (mean=0.5, std=0.145)
- (mean=0.8, std=0.231)

### Wide Uniform [0, 2μ] - CV = 0.577
This is approximately equivalent to points along another diagonal:
- (mean=0.3, std=0.173)
- (mean=0.5, std=0.289)
- (mean=0.8, std=0.462)

**The grid contains these lines PLUS all other combinations!**

---

## Safety Features

1. **Confirmation prompt:** Prevents accidental 8-hour runs
2. **Progress tracking:** Shows time remaining
3. **Automatic checkpoints:** Every 100 simulations
4. **Resume capability:** Can restart from checkpoints (with manual editing)
5. **Cleanup:** Removes temporary files when done

---

## Next Steps After Completion

1. **Generate 2D heatmaps** for each outcome type
2. **Extract iso-CV slices** and compare with uniform distribution results
3. **Identify regions** of parameter space with interesting behavior
4. **Statistical analysis** of mean effects, std effects, and interactions

---

## Summary

**Created:** `run_mean_std_grid.py`
- **Grid:** 12 mean × 12 std = 144 combinations
- **Reps:** 100 per combination
- **Total:** 14,400 simulations
- **Time:** ~8 hours
- **Size:** ~200-300 MB
- **Distribution:** Truncated normal N(mean, std²) on [0, ∞)

This allows comprehensive exploration of how BOTH mean AND variance affect coalescence outcomes! 🚀
