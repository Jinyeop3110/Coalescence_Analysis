# How Coalescence Outcomes Are Classified

## Overview

The classification uses **vector decomposition** to represent the coalesced community as a combination of the two parent communities plus a novel component.

## Mathematical Framework

### Step 1: Vector Decomposition

Given:
- `c1_final`: Equilibrium abundances of parent community 1 (48-dimensional vector)
- `c2_final`: Equilibrium abundances of parent community 2 (48-dimensional vector)
- `cc_final`: Equilibrium abundances of coalesced community (48-dimensional vector)

The function `metric_VectorDecomposition_onlyPositive(c1, c2, cc)` decomposes the coalesced community:

```
cc_final ≈ x1 × c1_final + x2 × c2_final + x3 × (novel component)
```

Where:
- **x1** = coefficient for parent community 1 (how much c1 is retained)
- **x2** = coefficient for parent community 2 (how much c2 is retained)
- **x3** = coefficient for novel/restructured component (how much is new)

**Constraint**: x1² + x2² + x3² = 1 (coefficients are normalized)

### Step 2: Classification Rules

Based on the (x1, x2, x3) coefficients, outcomes are classified:

#### **Dominance** (one community wins)
```
if x1 > 0.7:
    → Community 1 dominates (c1 wins)

OR

if x2 > 0.7:
    → Community 2 dominates (c2 wins)
```

**Interpretation**: The coalesced community is >70% similar to one of the parent communities. The winning community's species dominate, and most species from the losing community go extinct.

#### **Restructuring** (novel community emerges)
```
if x3 > 0.7:
    → Restructuring (novel community)
```

**Interpretation**: The coalesced community is >70% composed of a novel configuration that cannot be explained by either parent community. This represents emergence of a new ecological structure through interactions.

#### **Mixing** (intermediate state)
```
else:
    → Mixing (both parents contribute)
```

**Interpretation**: Neither parent dominates (x1, x2 < 0.7), and the community is not restructured enough (x3 < 0.7). Both parent communities contribute substantially to the coalesced community - species from both coexist.

## Geometric Interpretation

Think of it as a 3D coordinate system:
- **x1-axis**: Contribution from community 1
- **x2-axis**: Contribution from community 2
- **x3-axis**: Novel/restructured component

The outcome classification divides this space into regions:

```
         x3 (Restructuring)
         ^
         |
         |     x3 > 0.7
         |   (Restructuring)
         |
         |________________> x1 (Community 1)
        /
       /
      /  x2 (Community 2)
     v
```

- **Dominance region**: Near x1-axis (x1 > 0.7) or x2-axis (x2 > 0.7)
- **Restructuring region**: Near x3-axis (x3 > 0.7)
- **Mixing region**: Intermediate space (no single coefficient > 0.7)

## Example Cases

### Example 1: Community 1 Dominates
```
x1 = 0.85, x2 = 0.15, x3 = 0.10
→ Classification: DOMINANCE (c1 wins)
→ Interpretation: 85% of coalesced community resembles c1
```

### Example 2: Restructuring
```
x1 = 0.20, x2 = 0.30, x3 = 0.75
→ Classification: RESTRUCTURING
→ Interpretation: 75% of coalesced community is a novel configuration
```

### Example 3: Mixing
```
x1 = 0.50, x2 = 0.45, x3 = 0.35
→ Classification: MIXING
→ Interpretation: Both parents contribute (50% and 45%), some novelty (35%)
```

### Example 4: Boundary Case
```
x1 = 0.65, x2 = 0.40, x3 = 0.35
→ Classification: MIXING (x1 < 0.7, so not dominance)
→ This is a "near-dominance" mixing case
```

## Why This Classification Makes Sense

1. **Biologically meaningful**: Captures whether species from one community outcompete the other, or if new ecological structures emerge

2. **Continuous metric**: The (x1, x2, x3) values provide quantitative information beyond just the category

3. **Symmetric**: Treats both parent communities equally (dominance by either parent is classified the same)

4. **Captures emergence**: The x3 component specifically quantifies novel ecological structure not present in either parent

## Threshold Sensitivity

The choice of **0.7 threshold** is somewhat arbitrary:
- Higher threshold (e.g., 0.8) → Fewer dominance/restructuring cases, more mixing
- Lower threshold (e.g., 0.6) → More dominance/restructuring cases, fewer mixing

This threshold affects the **boundary cases** and contributes to some of the variability seen in the heatmaps, especially when x1, x2, or x3 are near 0.7.

## Connection to Heatmaps

In the mean×variance heatmaps:
- **Dominance fraction**: Percentage of coalescence events where x1 > 0.7 OR x2 > 0.7
- **Mixing fraction**: Percentage where x1, x2, x3 all ≤ 0.7
- **Restructuring fraction**: Percentage where x3 > 0.7

These fractions always sum to 1.0 for each grid point.
