# Bug Fixes Summary - Species LV Dominance Calculation

## Date: November 2, 2024

## Issues Identified

### Bug #1: Using WRONG Interaction Matrix ❌
**Problem:**
- Code loaded interaction matrix from external `parameter.xlsx` file
- This file contained a DIFFERENT interaction matrix (mean α = 1.19) than the actual simulation
- The 48species_10reps_WITH_MATRICES dataset has **rep-specific matrices embedded in JSON** (mean α = 0.20 for u=0.2)

**Evidence:**
```
For species 8 vs species 26 at u=0.2:
  Wrong (parameter.xlsx):  α₁₂ = 0.566, α₂₁ = 1.551
  Correct (JSON):          α₁₂ = 0.327, α₂₁ = 0.122
  Difference:              Δα₁₂ = 0.240, Δα₂₁ = 1.429
```

### Bug #2: Using Simple Addition Instead of Actual Coalescence ❌
**Problem:**
- Code calculated coalescence as `c_mix = c_1 + c_2` (simple addition)
- The JSON contains actual LV simulation results which are DIFFERENT
- Coalescence was simulated with full LV dynamics, not simple mixing

**Evidence:**
```
Coalescence 0_1:
  From JSON (actual):     17 species surviving
  Calculated (c1+c2):     23 species present
  Match? NO
```

## Fixes Implemented

### Fix #1: Use Rep-Specific Interaction Matrices from JSON ✅
```python
# OLD CODE (WRONG):
alpha_12 = interaction_matrix.iloc[C1, C2]  # From external parameter.xlsx

# NEW CODE (CORRECT):
rep_interaction_matrix = np.array(rep_data['parameters']['interaction_matrix'])
alpha_12 = rep_interaction_matrix[C1, C2]  # From JSON per replicate
```

### Fix #2: Use Actual Coalescence Outcomes from cc_list ✅
```python
# OLD CODE (WRONG):
c_mix = c_1 + c_2  # Simple addition
c_mix = c_mix / np.sum(c_mix)

# NEW CODE (CORRECT):
c_mix = np.array(cc_list[coal_key])  # Actual LV simulation result
c_mix = c_mix / (np.sum(c_mix) + 1e-8)
```

### Additional Improvements
1. **Process all replicates**: Now loops through all 10 reps per intensity
2. **Correct data flow**: Uses rep-specific matrices for each replicate's communities
3. **Proper normalization**: All abundance vectors normalized consistently
4. **Better data points**: 60 points per intensity (10 reps × 4 communities → 6 pairs/rep × 10)

## Results Comparison

### Before (with bugs):
| Intensity | R² Value | Notes |
|-----------|----------|-------|
| 0.2       | 0.001    | Using wrong matrix |
| 0.4       | 0.018    | Using wrong matrix |
| 0.6       | 0.055    | Using wrong matrix |
| 0.8       | 0.019    | Using wrong matrix |
| 1.0       | 0.031    | Using wrong matrix |

### After (fixed):
| Intensity | R² Value | Improvement |
|-----------|----------|-------------|
| 0.2       | 0.002    | ✓ Similar (weak competition) |
| 0.4       | 0.054    | ✓ 3× better! |
| 0.6       | 0.104    | ✓ 2× better! |
| 0.8       | 0.031    | ✓ Similar |
| 1.0       | 0.091    | ✓ 3× better! |

## Interpretation

The corrected R² values show:
1. **Modest improvement** at moderate-to-strong competition (u=0.6, 1.0)
2. **R² still relatively low** (< 0.11) across all intensities
3. **Key finding remains**: Pairwise dominant species competition CANNOT strongly predict community-level coalescence outcomes

However, the trend is now clearer:
- u=0.6 shows the HIGHEST predictability (R²=0.104)
- This suggests a "sweet spot" where:
  - Competition is strong enough to matter
  - But not so strong that stochastic exclusion dominates

## Files Modified

1. `generate_fig5_4_mostabundant_simulation_correct_intensity.py`:
   - Lines 364-473: Complete rewrite of data loading and processing loop
   - Now uses JSON-embedded interaction matrices
   - Now uses actual cc_list coalescence outcomes
   - Processes all 10 replicates per intensity

2. Generated figure:
   - `Fig_MostAbundant_Correlation_48species_10reps_WITH_MATRICES_Subplots.svg`
   - Updated with corrected calculations

## Validation

Tested with u=0.2, rep_000, coalescence 0_1:
- ✅ Correct interaction matrix values from JSON
- ✅ Actual coalescence outcome from cc_list  
- ✅ All 10 replicates processed per intensity
- ✅ 60 data points collected per intensity (10 reps × 6 pairs)
- ✅ Doubled to 120 points with symmetry (x,y) and (1-x,1-y)

## Why These Bugs Mattered

1. **Wrong matrices** → Predicted dominance based on UNRELATED species interactions
2. **Wrong coalescence** → Compared predictions to INCORRECT outcomes
3. **Result**: Analysis was testing whether random interactions predict random outcomes!

With fixes:
- Analysis now correctly tests whether pairwise competition of most abundant species (using actual interaction matrices) predicts actual coalescence outcomes (from LV simulations)
