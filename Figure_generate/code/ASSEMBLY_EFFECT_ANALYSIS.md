# Assembly Effect Analysis - Summary

## Overview

This analysis identifies pairs of communities where we can quantify the "assembly effect" by comparing:

1. **Parent communities** - Communities assembled directly from a larger species pool
2. **Coalesced communities** - Communities formed by merging two smaller parent communities

The key comparison allows us to address: **How different are communities when they are assembled directly vs. when they are formed through coalescence?**

## Experimental Design

### Comparison Groups

1. **Pool Size 12 (Parent) vs 6+6 (Coalesced)**
   - Parent: Directly assembled community with 12 species
   - Coalesced: Formed by merging two communities, each with 6 species
   - Both share the same (or very similar) initial species pool

2. **Pool Size 24 (Parent) vs 12+12 (Coalesced)**
   - Parent: Directly assembled community with 24 species
   - Coalesced: Formed by merging two communities, each with 12 species
   - Both share the same (or very similar) initial species pool

### Criteria for Comparable Pairs

For two communities to be comparable, they must:
- Share at least 80% overlap in their initial species pools
- Have the same medium condition (LN, MN, or HN)
- Both measured at final timepoint (F)

## Results Summary

### Total Pairs Identified: 8 comparable pairs

#### LN Medium (Low Nitrogen)
- **12 vs 6+6**: 0 pairs found
- **24 vs 12+12**: 6 pairs found
  1. Parent 20 (24 species) ↔ Coalesced 29 (Sub12+Sub17, 12 species each) - Overlap: 81.2%
  2. Parent 20 (24 species) ↔ Coalesced 29 (Sub12+Sub17, 12 species each) - Overlap: 81.2%
  3. Parent 20 (24 species) ↔ Coalesced 29 (Sub12+Sub17, 12 species each) - Overlap: 81.2%
  4. Parent 20 (24 species) ↔ Coalesced 29 (Sub12+Sub17, 12 species each) - Overlap: 81.2%
  5. Parent 25 (24 species) ↔ Coalesced 30 (Sub12+Sub18, 12 species each) - Overlap: 85.7%
  6. Parent 25 (24 species) ↔ Coalesced 30 (Sub12+Sub18, 12 species each) - Overlap: 85.7%

#### MN Medium (Medium Nitrogen)
- **12 vs 6+6**: 0 pairs found
- **24 vs 12+12**: 2 pairs found
  1. Parent 24 (24 species) ↔ Coalesced 33 (Sub13+Sub16, 12 species each) - Overlap: 88.9%
  2. Parent 24 (24 species) ↔ Coalesced 33 (Sub13+Sub16, 12 species each) - Overlap: 88.9%

#### HN Medium (High Nitrogen)
- **12 vs 6+6**: 0 pairs found
- **24 vs 12+12**: 0 pairs found

## Key Findings

1. **No comparable pairs found for pool size 12 vs 6+6**
   - This suggests that the experimental design did not create parent communities with pool size 12 that share the same species composition as coalesced communities from 6+6

2. **Multiple comparable pairs found for pool size 24 vs 12+12**
   - 6 pairs in LN medium (with some duplicates)
   - 2 pairs in MN medium
   - These pairs allow for direct comparison of assembly effects

3. **Medium-dependent patterns**
   - LN medium has the most comparable pairs (6)
   - MN medium has fewer pairs (2)
   - HN medium has no comparable pairs

## Data Files

The identified pairs have been saved to:
- **Pickle file**: `Figure/Assembly_effect/comparable_pairs.pkl`
- **Analysis script**: `identify_assembly_effect_pairs.py`
- **Figure folder**: `Figure/Assembly_effect/`

## Specific Comparable Pairs

### LN Medium - Pool 24 vs 12+12

#### Pair Group 1: Parent 20 ↔ Coalesced 29
- **Parent Community 20**
  - Sample ID: P2-52 (and replicates)
  - Pool size: 24 species
  - Medium: LN

- **Coalesced Community 29**
  - Formed from: Sub12 + Sub17
  - Sample ID: P6-70 (and replicates)
  - Each parent pool size: 12 species
  - Medium: LN
  - Species pool overlap: 81.2%

#### Pair Group 2: Parent 25 ↔ Coalesced 30
- **Parent Community 25**
  - Sample ID: P2-53 (and replicates)
  - Pool size: 24 species
  - Medium: LN

- **Coalesced Community 30**
  - Formed from: Sub12 + Sub18
  - Sample ID: P6-67 (and replicates)
  - Each parent pool size: 12 species
  - Medium: LN
  - Species pool overlap: 85.7%

### MN Medium - Pool 24 vs 12+12

#### Pair: Parent 24 ↔ Coalesced 33
- **Parent Community 24**
  - Sample ID: P2-76 (and replicates)
  - Pool size: 24 species
  - Medium: MN

- **Coalesced Community 33**
  - Formed from: Sub13 + Sub16
  - Sample ID: P6-64 (and replicates)
  - Each parent pool size: 12 species
  - Medium: MN
  - Species pool overlap: 88.9%

## Next Steps for Analysis

With these identified pairs, you can now:

1. **Compare final diversity**
   - How many species survive in parent vs coalesced communities?

2. **Compare composition**
   - Are the same species present in both types of communities?
   - What is the compositional similarity (e.g., Bray-Curtis, Jaccard)?

3. **Compare abundance patterns**
   - Do species have similar abundances in parent vs coalesced?

4. **Quantify assembly effect**
   - Calculate metrics that capture how "assembly history" affects final community state
   - E.g., difference in diversity, compositional dissimilarity, evenness, etc.

5. **Statistical testing**
   - Are differences between parent and coalesced communities statistically significant?
   - How does this vary by medium condition?

## Code Location

- **Analysis script**: `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/identify_assembly_effect_pairs.py`
- **Figure folder**: `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Assembly_effect/`
- **Results file**: `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Assembly_effect/comparable_pairs.pkl`
