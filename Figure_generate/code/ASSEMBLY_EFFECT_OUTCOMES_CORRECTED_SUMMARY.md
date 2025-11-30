# Assembly Effect Coalescence Outcomes - Corrected Analysis

## Overview

Analysis of coalescence outcomes (dominance, mixing, restructuring) for communities formed through the "assembly effect" pathway, separated by nutrient level.

## Important Note

**Parent communities are NOT analyzed** because they were assembled directly from the full species pool, not by merging two sub-communities. Vector decomposition only applies to coalesced communities that are formed by merging.

## Results by Medium

### Overall (All Media Combined, n=362):
- **Dominance**: 21.0% (76/362)
- **Mixing**: 68.0% (246/362)
- **Restructuring**: 11.0% (40/362)

### Low Nitrogen (LN, n=124):
- **Dominance**: 16.1% (20/124)
- **Mixing**: 69.4% (86/124)
- **Restructuring**: 14.5% (18/124)

### Medium Nitrogen (MN, n=114):
- **Dominance**: 22.8% (26/114)
- **Mixing**: 66.7% (76/114)
- **Restructuring**: 10.5% (12/114)

### High Nitrogen (HN, n=124):
- **Dominance**: 24.2% (30/124)
- **Mixing**: 67.7% (84/124)
- **Restructuring**: 8.1% (10/124)

## Key Findings

### 1. Nutrient-Dependent Dominance

**Dominance increases with nutrient availability:**
- HN (24.2%) > MN (22.8%) > LN (16.1%)

This suggests that in high-nutrient conditions, one sub-community is more likely to dominate after coalescence, possibly due to:
- Faster growth allowing priority effects
- Stronger competitive exclusion
- Less niche differentiation needed for survival

### 2. Nutrient-Dependent Restructuring

**Restructuring decreases with nutrient availability:**
- LN (14.5%) > MN (10.5%) > HN (8.1%)

This suggests that in low-nutrient conditions, coalescence is more likely to produce novel community structures, possibly due to:
- Greater niche differentiation
- Stronger species interactions
- More complex ecological dynamics under resource limitation

### 3. Mixing is Most Common

**Across all conditions, mixing (~68%) is the dominant outcome**, meaning that most coalesced communities integrate both parent communities relatively evenly.

## Biological Interpretation

### High Nitrogen Promotes Dominance:
- Fast-growing species can quickly dominate
- Priority effects are stronger
- Competitive hierarchies are clearer
- Less opportunity for coexistence

### Low Nitrogen Promotes Restructuring:
- Slower growth allows more complex interactions
- Resource limitation favors niche differentiation
- Community structure emerges from ecological dynamics
- Novel species combinations become viable

### Trade-off Pattern:
There appears to be a trade-off between dominance and restructuring:
- As dominance increases (HN), restructuring decreases
- As restructuring increases (LN), dominance decreases
- Mixing remains relatively constant (~67-69%)

## Method

### Vector Decomposition Classification:

For each coalesced community, we decompose it into:
- **u**: Contribution from sub-community 1
- **v**: Contribution from sub-community 2
- **k**: Orthogonal component (restructuring)

Where u² + v² + k² = 1

Classification rules:
- **Dominance**: One parent dominates (x² > 0.5, y > 0.5)
  - x = √(u² + v²), high parent contribution
  - y = asymmetry between u and v

- **Mixing**: Both parents contribute evenly (x² > 0.5, y < 0.5)
  - x = √(u² + v²), high parent contribution
  - y = symmetry between u and v

- **Restructuring**: Low parent contribution (x² < 0.5)
  - Novel community structure emerges

## Comparison to Existing Phase Diagrams

The existing phase diagram analysis (MN medium, all pool sizes merged) showed:
- Similar mixing percentage (~66-68%)
- Consistent classification method
- Our assembly effect analysis uses the same vector decomposition approach

This validates our methodology and shows that assembly effect communities follow similar ecological rules as other coalescence events.

## Files

**Analysis script**: `analyze_assembly_effect_outcomes.py`
**Figure**: `Figure/Assembly_effect/Fig_assembly_effect_outcomes_by_medium.svg`
**Results data**: `Figure/Assembly_effect/assembly_effect_outcomes_results.pkl`

## Significance

This analysis reveals that:

1. **Nutrient availability shapes coalescence outcomes**
   - High nutrients → Dominance
   - Low nutrients → Restructuring

2. **Environmental context matters for assembly history effects**
   - The same assembly pathway produces different outcomes depending on resources

3. **Ecological dynamics differ across nutrient gradients**
   - Competition vs coexistence trade-offs
   - Priority effects vs niche differentiation

## Next Steps

Potential follow-up analyses:
1. **Species-level analysis**: Which species drive dominance vs restructuring?
2. **Temporal dynamics**: How do outcomes change over time?
3. **Initial diversity effects**: Does 6+6 vs 12+12 affect outcomes?
4. **Interaction networks**: What drives restructuring in LN?
5. **Predictability**: Can we predict outcome type from initial conditions?

## Date: 2025-01-04
