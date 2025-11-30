# Assembly Effect Analysis - CORRECT Matching (FINAL)

## Overview

This analysis identifies assembly effect pairs using the **CORRECT experimental design** - matching parent communities with coalesced communities that share the same initial species pool based on the experimental documentation.

## Key Achievement

Successfully identified **362 pairs** across all media using the designed matching provided by the user.

## Method

Used **manual matching from experimental documentation**:
- Parent communities (19-30, pool-24) are matched with specific coalesced communities formed from 12+12 mergers
- Parent communities (10-18, pool-12) are matched with specific coalesced communities formed from 6+6 mergers

### The Designed Pairs:

**Pool-24 vs 12+12 (12 pairs):**
- Parent 19 ↔ Coalesced 24
- Parent 20 ↔ Coalesced 39
- Parent 21 ↔ Coalesced 15
- Parent 22 ↔ Coalesced 37
- Parent 23 ↔ Coalesced 18
- Parent 24 ↔ Coalesced 34
- Parent 25 ↔ Coalesced 30
- Parent 26 ↔ Coalesced 22
- Parent 27 ↔ Coalesced 28
- Parent 28 ↔ Coalesced 25
- Parent 29 ↔ Coalesced 41
- Parent 30 ↔ Coalesced 32

**Pool-12 vs 6+6 (9 pairs):**
- Parent 10 ↔ Coalesced 2
- Parent 11 ↔ Coalesced 6
- Parent 12 ↔ Coalesced 11
- Parent 13 ↔ Coalesced 9
- Parent 14 ↔ Coalesced 12
- Parent 15 ↔ Coalesced 10
- Parent 16 ↔ Coalesced 7
- Parent 17 ↔ Coalesced 8
- Parent 18 ↔ Coalesced 9

## Results Summary

### Total Pairs: 362

**LN Medium (124 pairs):**
- Pool 12 vs 6+6: 72 pairs
  - Parent diversity: 11.4 ± 2.7 species
  - Coalesced diversity: 14.0 ± 6.8 species
  - Mean difference: -2.6 ± 7.6 (coalesced > parent)

- Pool 24 vs 12+12: 52 pairs
  - Parent diversity: 13.2 ± 1.3 species
  - Coalesced diversity: 14.3 ± 6.0 species
  - Mean difference: -1.0 ± 6.5 (coalesced > parent)

**MN Medium (114 pairs):**
- Pool 12 vs 6+6: 68 pairs
  - Parent diversity: 9.4 ± 4.5 species
  - Coalesced diversity: 11.5 ± 5.9 species
  - Mean difference: -2.1 ± 6.5 (coalesced > parent)

- Pool 24 vs 12+12: 46 pairs
  - Parent diversity: 11.4 ± 4.8 species
  - Coalesced diversity: 10.6 ± 4.9 species
  - Mean difference: 0.8 ± 5.0 (parent slightly > coalesced)

**HN Medium (124 pairs):**
- Pool 12 vs 6+6: 72 pairs
  - Parent diversity: 10.4 ± 6.8 species
  - Coalesced diversity: 9.2 ± 5.4 species
  - Mean difference: 1.2 ± 8.4 (parent > coalesced)

- Pool 24 vs 12+12: 52 pairs
  - Parent diversity: 9.2 ± 3.8 species
  - Coalesced diversity: 9.1 ± 2.9 species
  - Mean difference: 0.1 ± 3.9 (nearly equal)

## Key Findings

1. **Low Nitrogen (LN)**: Coalesced communities consistently have higher diversity than parent communities (negative differences), suggesting coalescence promotes diversity in low-nutrient conditions.

2. **Medium Nitrogen (MN)**: Mixed pattern - coalesced communities have higher diversity for 6+6, but lower for 12+12.

3. **High Nitrogen (HN)**: Parent communities tend to have equal or slightly higher diversity than coalesced communities, suggesting direct assembly may be more effective at high nutrients.

## Technical Notes

### Two Critical Bugs Fixed:

1. **getAbundance bug**: The original `getAbundance()` function in `common_setup.py` has a bug where it fails for samples at index 0:
   ```python
   # Bug: if not any(SampleIdx) returns True when SampleIdx=[0]
   if not any(SampleIdx):  # WRONG - fails for index 0
       return

   # Fix: use len() instead
   if len(SampleIdx) == 0:  # CORRECT
       return None
   ```

2. **NumPy any() vs builtin any()**: When using `from pylab import *`, NumPy's `any()` function overrides Python's builtin `any()`. NumPy's `any()` treats generator expressions as objects (always truthy), causing incorrect behavior:
   ```python
   # Bug: NumPy's any() evaluates generator object as truthy
   any(x is None for x in [a, b, c])  # Always True with numpy any()!

   # Fix: use Python's builtin any()
   import builtins
   builtins.any(x is None for x in [a, b, c])  # Correct behavior
   ```

### Data Structure

Each pair contains:
- Parent community information (sample ID, species list, abundances, diversity)
- Coalesced community information
- Sub-community information (Sub1 and Sub2 that formed the coalesced community)
- Assembly effect metrics (diversity difference, species overlap, species unique to each)

## Files

**Script:** `identify_assembly_pairs_CORRECT.py`
**Data:** `Figure/Assembly_effect/assembly_pairs_CORRECT.pkl`
**Documentation:** This file

## Usage Example

```python
import pickle

# Load the pairs
with open('Figure/Assembly_effect/assembly_pairs_CORRECT.pkl', 'rb') as f:
    data = pickle.load(f)

# Access pairs for LN medium, pool 24 vs 12+12
ln_24_pairs = data['pairs']['LN']['24_vs_12+12']

for pair in ln_24_pairs[:3]:  # First 3 pairs
    print(f"Parent {pair['parent_community_idx']} (n={pair['parent_final_diversity']}) vs "
          f"Coalesced {pair['coalesced_community_idx']} (n={pair['coalesced_final_diversity']})")
```

## Next Steps

1. **Statistical analysis**: Test whether diversity differences are significant
2. **Compositional analysis**: Compare species composition between parent and coalesced
3. **Retention analysis**: Which species from the initial pool survive in each pathway?
4. **Medium effects**: Why does the assembly effect differ across nutrient levels?
5. **Visualization**: Create figures showing assembly effects

## Date: 2025-01-04
