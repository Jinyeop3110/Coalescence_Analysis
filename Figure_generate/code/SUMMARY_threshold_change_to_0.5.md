# Summary: Changed Mixing Filter Threshold from 0.66 to 0.5

## Changes Made:

### 1. **Simulation Correlation Plots** - Changed 0.66 → 0.5
   - **File**: `plot_20reps_correlation.py` (line 179-181)
   - **File**: `plot_narrow_uniform_correlation.py` (line 177-179)

   **Before:**
   ```python
   # FILTER: Only consider cases where x1² + x2² > 0.66 (substantial mixing)
   mixing_strength = u**2 + v**2
   if mixing_strength <= 0.66:
       continue
   ```

   **After:**
   ```python
   # FILTER: Only consider cases where x1² + x2² > 0.5 (substantial mixing)
   mixing_strength = u**2 + v**2
   if mixing_strength <= 0.5:
       continue
   ```

### 2. **Experimental Plots** - Already using 0.5
   - **File**: `generate_fig5_4_mostabundant_experimental.py`
   - No changes needed - already using 0.5 threshold

## Affected Plots:

### Simulation Plots (regenerating with new threshold):
1. `Fig_MostAbundant_Correlation_10reps_narrow_uniform_Subplots.svg`
2. `Fig_MostAbundant_Correlation_20reps_narrow_uniform_Subplots.svg`
3. `Fig_MostAbundant_Correlation_20reps_wide_uniform_Subplots.svg`

### Experimental Plots (unchanged threshold, already 0.5):
1. `Fig_MostAbundant_Correlation_H_Combined.svg`
2. `Fig_MostAbundant_Correlation_L_Combined.svg`
3. `Fig_MostAbundant_Correlation_M_Combined.svg`
4. `Fig_MostAbundant_Correlation_M_H_Combined.svg`
5. `Fig_MostAbundant_Correlation_M_H_Combined_AbundantRemoved.svg`
6. `Fig_MostAbundant_Correlation_M_H_Combined_DominantFraction.svg`

## Impact of Threshold Change (0.66 → 0.5):

### What changes:
- **More data points included** in simulation plots
- 0.66 threshold: requires √0.66 ≈ 81% variance in mixing (u,v)
- 0.5 threshold: requires √0.5 ≈ 71% variance in mixing (u,v)
- **More lenient** - allows events with 50-66% mixing strength that were previously excluded

### Expected effects:
1. **More data points** per subplot
2. **Potentially lower R² values** (including more borderline mixing cases)
3. **Better statistical power** (more data for regression)
4. **Consistency** across simulation and experimental plots (same threshold)

## Rationale:

**Why change to 0.5?**
1. **Consistency**: All plots now use the same threshold (simulation & experimental)
2. **Standard definition**: u²+v² > 0.5 means mixing component > restructuring component (k²)
3. **More inclusive**: Captures events where mixing is dominant but not overwhelming
4. **Better data retention**: Particularly important at high competition where fewer events pass filters

**Threshold interpretation:**
- **u²+v² > 0.5**: Mixing dominates over restructuring (mixing > 50% of variance)
- **u²+v² > 0.66**: Strong mixing dominates (mixing > 66% of variance)

The 0.5 threshold is the natural cutoff where mixing becomes the dominant mode over restructuring.

## Status:

- ✅ Simulation plot scripts updated (0.66 → 0.5)
- ⏳ Regenerating simulation correlation plots
- ✅ Experimental plots already using 0.5
- ⚠️  Experimental plot script has bugs preventing M_H_combined plots from generating

## Files Modified:
1. `plot_20reps_correlation.py` - threshold changed
2. `plot_narrow_uniform_correlation.py` - threshold changed
