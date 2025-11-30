# Narrow Uniform Distribution Implementation Summary

## Overview

Successfully implemented and ran simulations with a **narrow uniform distribution** for interaction matrices: **Uniform[mean×0.5, mean×1.5]**

This distribution has **half the variance** of the original wide uniform distribution.

---

## Distribution Comparison

### Original Wide Uniform Distribution
```python
I[i,j] ~ Uniform[0, 2×mean]
```

**Properties:**
- Mean: μ = mean
- Variance: σ² = (mean)²/3
- Standard deviation: σ = mean/√3 ≈ 0.577 × mean
- **Coefficient of variation: CV = 1/√3 ≈ 0.577** (fixed)
- Range: [0, 2×mean]

### New Narrow Uniform Distribution
```python
I[i,j] ~ Uniform[0.5×mean, 1.5×mean]
```

**Properties:**
- Mean: μ = mean
- Variance: σ² = (mean)²/12
- Standard deviation: σ = mean/(2√3) ≈ 0.289 × mean
- **Coefficient of variation: CV = 1/(2√3) ≈ 0.289** (fixed)
- Range: [0.5×mean, 1.5×mean]

### Key Difference
**The narrow uniform has EXACTLY HALF the CV of the wide uniform!**

| Distribution | CV | Variance Ratio |
|--------------|-----|----------------|
| Wide Uniform [0, 2μ] | 0.577 | 1.0× (baseline) |
| Narrow Uniform [0.5μ, 1.5μ] | 0.289 | 0.25× (1/4 variance) |

---

## Mathematical Derivation

For Uniform[a, b]:
- Mean: μ = (a + b) / 2
- Variance: σ² = (b - a)² / 12

### Wide Uniform [0, 2μ]
- Mean: (0 + 2μ) / 2 = μ ✓
- Variance: (2μ - 0)² / 12 = 4μ² / 12 = μ² / 3
- CV: √(μ²/3) / μ = 1/√3 ≈ 0.577

### Narrow Uniform [0.5μ, 1.5μ]
- Mean: (0.5μ + 1.5μ) / 2 = μ ✓
- Variance: (1.5μ - 0.5μ)² / 12 = μ² / 12
- CV: √(μ²/12) / μ = 1/(2√3) ≈ 0.289

**Variance ratio: (μ²/12) / (μ²/3) = 1/4** ✓

---

## Files Generated

### 1. Simulation Script
**[run_uniform_narrow_range.py](run_uniform_narrow_range.py)**
- Implements narrow uniform distribution: `uniform_narrow_range(mean)`
- Same structure as existing simulation code
- Saves full 48×48 interaction matrices
- Successfully completed 240 simulations (10 reps × 24 means)

### 2. Simulation Data
**Simulation_Data/48species_10reps_narrow_uniform/Community_10reps_narrow_uniform.json**
- Size: 19.6 MB
- 10 repetitions
- 24 interaction strengths: 0.05 to 1.20 (step 0.05)
- Total: 240 simulations
- Runtime: 11.2 minutes

**Simulation_Data/48species_10reps_narrow_uniform/simulation_parameters.xlsx**
- Excel file with all simulation parameters
- Includes theoretical mean, std, and CV for each u value

### 3. Phase Diagram
**[Figure/PhaseDiagram/Fig_phase_diagram_10reps_narrow_uniform.svg](Figure/PhaseDiagram/Fig_phase_diagram_10reps_narrow_uniform.svg)**
- Size: 18 KB
- Shows fraction of Dominance, Mixing, and Restructuring outcomes
- Format matches existing phase diagrams for easy comparison

### 4. Plotting Script
**[plot_narrow_uniform.py](plot_narrow_uniform.py)**
- Modified version of plot_phase_diagrams_WITH_MATRICES.py
- Handles narrow uniform data structure
- Generates phase diagram with proper formatting

---

## Simulation Results Summary

### Execution
```
Total simulations: 240 (24 means × 10 reps)
Total time: 11.2 minutes
Average time per simulation: 2.8 seconds
Mean values tested: 0.05 to 1.20 (step 0.05)
```

### Data Verified
✓ All 240 simulations completed successfully
✓ Full interaction matrices saved for all simulations
✓ Empirical CV matches theoretical value (≈0.289)
✓ Phase diagram generated successfully

---

## Distribution Statistics Examples

### Example 1: mean = 0.30
**Wide Uniform [0, 0.60]:**
- Mean: 0.30
- Std: 0.173
- CV: 0.577
- Range: [0, 0.60]

**Narrow Uniform [0.15, 0.45]:**
- Mean: 0.30
- Std: 0.087
- CV: 0.289
- Range: [0.15, 0.45]

### Example 2: mean = 0.50
**Wide Uniform [0, 1.00]:**
- Mean: 0.50
- Std: 0.289
- CV: 0.577
- Range: [0, 1.00]

**Narrow Uniform [0.25, 0.75]:**
- Mean: 0.50
- Std: 0.144
- CV: 0.289
- Range: [0.25, 0.75]

### Example 3: mean = 0.80
**Wide Uniform [0, 1.60]:**
- Mean: 0.80
- Std: 0.462
- CV: 0.577
- Range: [0, 1.60]

**Narrow Uniform [0.40, 1.20]:**
- Mean: 0.80
- Std: 0.231
- CV: 0.289
- Range: [0.40, 1.20]

---

## Research Questions

### Primary Question
**At the same mean interaction strength, does reducing variance (heterogeneity) change coalescence outcomes?**

### Specific Hypotheses to Test

1. **Dominance Fraction:**
   - Hypothesis: Narrower distribution → More dominance (less stochasticity)
   - Test: Compare dominance fraction at each mean value

2. **Mixing Fraction:**
   - Hypothesis: Narrower distribution → More stable mixing (less restructuring)
   - Test: Compare mixing vs restructuring ratio

3. **Phase Transition Points:**
   - Hypothesis: Narrower distribution → Sharper transitions between phases
   - Test: Compare slope of phase boundaries

4. **Outcome Predictability:**
   - Hypothesis: Narrower distribution → More reproducible outcomes
   - Test: Compare variance across repetitions

---

## Comparison with Other Distributions

### All Distributions with Same Mean (0.5)

| Distribution | Range | CV | Std | Variance |
|--------------|-------|-----|-----|----------|
| **Wide Uniform [0, 1.0]** | [0, 1.0] | 0.577 | 0.289 | 0.083 |
| **Narrow Uniform [0.25, 0.75]** | [0.25, 0.75] | 0.289 | 0.144 | 0.021 |
| **Gamma (k=25, θ=0.02)** | [0, ∞) | 0.2 | 0.100 | 0.010 |
| **Gamma (k=4, θ=0.125)** | [0, ∞) | 0.5 | 0.250 | 0.063 |
| **Gamma (k=1, θ=0.5)** | [0, ∞) | 1.0 | 0.500 | 0.250 |

**Key Insight:**
- Narrow uniform CV (0.289) is between low-CV gamma (0.2) and uniform-like gamma (0.577)
- Allows testing "intermediate" heterogeneity
- Still bounded (unlike gamma), which may be biologically relevant

---

## Next Steps

### Immediate Analysis
1. **Compare phase diagrams:**
   - Wide uniform vs narrow uniform
   - Look for differences in phase transitions
   - Quantify changes in outcome fractions

2. **Statistical comparison:**
   - Chi-square test for outcome distributions
   - Effect size of variance reduction
   - Identify critical interaction strengths where variance matters most

### Future Experiments

1. **Increase replication:**
   ```bash
   # Modify run_uniform_narrow_range.py to N_reps = 100
   # Runtime: ~110 minutes for 2,400 simulations
   ```

2. **Create comparison plots:**
   - Side-by-side phase diagrams
   - Difference plot (narrow - wide)
   - Variance in outcomes vs interaction strength

3. **Mechanistic analysis:**
   - Use saved interaction matrices
   - Correlate specific matrix properties with outcomes
   - Identify which aspects of heterogeneity drive effects

---

## Command Reference

### Run Simulation
```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code
conda activate coalescence
python run_uniform_narrow_range.py
```

### Generate Phase Diagram
```bash
python plot_narrow_uniform.py
```

### Compare with Original
```bash
# Wide uniform (original)
ls -lh Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json
ls -lh Figure/PhaseDiagram/Fig_phase_diagram_10reps_WITH_MATRICES.svg

# Narrow uniform (new)
ls -lh Simulation_Data/48species_10reps_narrow_uniform/Community_10reps_narrow_uniform.json
ls -lh Figure/PhaseDiagram/Fig_phase_diagram_10reps_narrow_uniform.svg
```

---

## Technical Notes

### Implementation Details
- Distribution function: `uniform_narrow_range(mean)` returns `mean * 0.5 + mean * np.random.random()`
- Equivalent to: `np.random.uniform(0.5*mean, 1.5*mean)`
- Diagonal elements still set to 1.0 (self-interaction)
- All other parameters identical to original simulations

### Data Structure
Same JSON structure as wide uniform data:
```json
{
  "0.50": {
    "rep_000": {
      "sc_list": {...},
      "cc_list": {...},
      "parameters": {
        "seed": 5000,
        "u": 0.5,
        "distribution": "uniform_narrow",
        "distribution_range": "[0.250, 0.750]",
        "interaction_matrix": [[...]],
        "interaction_matrix_stats": {
          "mean": 0.502,
          "std": 0.145,
          "theoretical_cv": 0.28867513459481287,
          "empirical_cv": 0.289
        }
      }
    }
  }
}
```

### Compatibility
- Works with existing analysis pipeline
- Can use same plotting functions (with minor key adjustments)
- Comparable to gamma distribution results

---

## Summary

✅ **Successfully implemented narrow uniform distribution [0.5μ, 1.5μ]**
✅ **Completed 240 simulations (10 reps × 24 means) in 11.2 minutes**
✅ **Generated phase diagram for comparison with wide uniform**

**Key Achievement:**
- Reduced coefficient of variation from 0.577 to 0.289 (50% reduction)
- Maintained same mean interaction strengths
- Created controlled experiment to test effect of heterogeneity

**Next:**
- Compare phase diagrams
- Quantify differences in coalescence outcomes
- Determine if variance matters at fixed mean

---

## File Locations

All files in: `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/`

**Simulation:**
- `run_uniform_narrow_range.py` (script)
- `Simulation_Data/48species_10reps_narrow_uniform/` (data)

**Visualization:**
- `plot_narrow_uniform.py` (script)
- `Figure/PhaseDiagram/Fig_phase_diagram_10reps_narrow_uniform.svg` (output)

**Documentation:**
- `NARROW_UNIFORM_SUMMARY.md` (this file)
