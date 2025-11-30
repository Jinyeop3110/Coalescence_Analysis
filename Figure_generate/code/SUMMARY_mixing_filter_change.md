# Summary: Effect of Changing Mixing Filter from None to u²+v² > 0.5

## Experimental Plots Updated:
1. `Fig_MostAbundant_Correlation_H_Combined.svg`
2. `Fig_MostAbundant_Correlation_L_Combined.svg`
3. `Fig_MostAbundant_Correlation_M_Combined.svg`
4. `Fig_MostAbundant_Correlation_M_H_Combined.svg`
5. `Fig_MostAbundant_Correlation_M_H_Combined_AbundantRemoved.svg`
6. `Fig_MostAbundant_Correlation_M_H_Combined_DominantFraction.svg`

## Filter Added:
```python
# FILTER: Only include mixing events (u²+v² > 0.5)
mixing_strength = u**2 + v**2
if mixing_strength <= 0.5:
    continue
```

## Data Points Before vs After Filter:

### Single Medium Plots (after duplication):

| Medium | **BEFORE Filter** | **AFTER Filter** | Change | % Retained |
|--------|------------------|------------------|--------|------------|
| **LN** | 144 points (72 unique) | 132 points (66 unique) | -12 | 91.7% |
| **MN** | 106 points (53 unique) | 68 points (34 unique) | -38 | 64.2% |
| **HN** | 152 points (76 unique) | 126 points (63 unique) | -26 | 82.9% |

### AbundantRemoved Plot (M+H combined):

| Medium | **BEFORE Filter** | **AFTER Filter** | Change | % Retained |
|--------|------------------|------------------|--------|------------|
| **MN** | 53 unique | ~14 unique | -39 | 26.4% |
| **HN** | 68 unique | ~23 unique | -45 | 33.8% |

## Interpretation:

### 1. **Low Nitrogen (LN): Minimal filtering (91.7% retained)**
   - Most coalescence events already show mixing
   - Low competition → communities naturally mix
   - Filter removes very few restructuring events

### 2. **Medium Nitrogen (MN): Moderate filtering (64.2% retained)**
   - Removes ~36% of events
   - Mix of mixing and restructuring outcomes
   - Filter significantly changes the dataset

### 3. **High Nitrogen (HN): Some filtering (82.9% retained)**
   - Removes ~17% of events
   - Most events show mixing despite high competition
   - Dominant species drive mixing dynamics

### 4. **AbundantRemoved Plot: DRAMATIC filtering (26-34% retained)**
   - **73-74% of events are REMOVED!**
   - After removing dominant species, most subdominant communities restructure
   - Filter reveals that only ~1/3 of subdominant communities maintain mixing
   - Shows that dominant species are critical for maintaining community structure

## Biological Significance:

**The mixing filter (u²+v² > 0.5) specifically isolates coalescence events where:**
- Parent community identities are preserved
- Outcome is a weighted mixture of inputs
- No major restructuring occurs

**Excluding restructuring events means the plots now test:**
> "Among events where communities mix (not restructure), can dominant species pairwise outcomes predict the mixing proportions?"

This is a cleaner test of the top-down hypothesis because it removes confounding restructuring events where novel community compositions emerge that have no clear relationship to parent communities.

## Comparison to Simulation Plots:

**Simulation plots use u²+v² > 0.66** (slightly stricter)
**Experimental plots now use u²+v² > 0.5** (slightly more permissive)

The 0.5 threshold was chosen to:
1. Be more lenient than simulations (experimental data is noisier)
2. Still exclude clear restructuring events
3. Retain sufficient data points for statistical analysis

## Files Modified:
- `generate_fig5_4_mostabundant_experimental.py` - Added mixing filter to 4 plot functions
- All 6 SVG output files regenerated with filter applied
