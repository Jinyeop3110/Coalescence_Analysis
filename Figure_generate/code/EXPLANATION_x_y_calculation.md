# Explanation: How x and y are Calculated in Correlation Plots

This document explains exactly how the x-axis (species-level dominance) and y-axis (community-level dominance) are calculated for the correlation plots.

## Overview

For each pairwise coalescence event (e.g., c1 + c2 → c_mix), we calculate:
- **x (Species LV Dominance)**: Predicted dominance from pairwise Lotka-Volterra equilibrium of the most abundant species
- **y (Community Dominance)**: Observed dominance from vector decomposition of the community composition

Then we **duplicate** the data points by plotting both (x, y) and (1-x, 1-y) to create symmetry.

---

## Step-by-Step Calculation

### Input Data for Each Coalescence Event

Consider coalescence: **c1 + c2 → c_mix**

**c1** (community 1, 48 species):
```
c1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.5188, ..., 0.0]  # Species 5 is most abundant
```

**c2** (community 2, 48 species):
```
c2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ..., 0.4212, ...]  # Species 17 is most abundant
```

**c_mix** (coalescence outcome, 48 species):
```
c_mix = [abundance vector after coalescence]
```

**Interaction matrix** (48×48):
```
alpha[5, 17] = 0.1352  # Effect of species 17 on species 5
alpha[17, 5] = 0.1741  # Effect of species 5 on species 17
```

---

## Calculating x: Species-Level Dominance

### Step 1: Identify Most Abundant Species

```python
C1 = argmax(c1) = 5   # Species 5 is most abundant in c1
C2 = argmax(c2) = 17  # Species 17 is most abundant in c2
```

### Step 2: Extract Interaction Coefficients

```python
alpha_12 = interaction_matrix[C1, C2] = interaction_matrix[5, 17] = 0.1352
alpha_21 = interaction_matrix[C2, C1] = interaction_matrix[17, 5] = 0.1741
```

**Interpretation**:
- α₁₂ = 0.1352 = effect of species 17 (C2) on species 5 (C1)
- α₂₁ = 0.1741 = effect of species 5 (C1) on species 17 (C2)

### Step 3: Calculate LV Equilibrium Dominance

Using the Lotka-Volterra two-species model:
```
dN1/dt = r1·N1·(1 - (N1 + α₁₂·N2)/K1)
dN2/dt = r2·N2·(1 - (N2 + α₂₁·N1)/K2)
```

At equilibrium (with K1 = K2 = 1):
```
N1* = (1 - α₁₂)/(2 - α₁₂ - α₂₁)
N2* = (1 - α₂₁)/(2 - α₁₂ - α₂₁)
```

**Species dominance** = N1*/(N1* + N2*):
```python
species_dominance = (1 - alpha_12) / (2 - alpha_12 - alpha_21)
                  = (1 - 0.1352) / (2 - 0.1352 - 0.1741)
                  = 0.8648 / 1.6907
                  = 0.5115
```

**This is our x value for this coalescence event: x = 0.5115**

### Step 4: Handle Different LV Cases

The code handles 4 cases:

1. **Both α < 1, sum < 2**: Stable coexistence → use formula above
2. **Both α < 1, sum > 2**: Bistability → return 0.5 (unpredictable)
3. **α₁₂ > 1, α₂₁ < 1**: Species 1 wins → return 1.0
4. **α₁₂ < 1, α₂₁ > 1**: Species 2 wins → return 0.0
5. **Both α > 1**: Competitive exclusion → return 0.5 (unpredictable)

---

## Calculating y: Community-Level Dominance

### Step 1: Vector Decomposition

Decompose the coalescence outcome **c_mix** into contributions from **c1** and **c2**:

```python
u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, c_mix)
```

This solves for:
```
c_mix ≈ u·c1 + v·c2 + k·(restructuring component)
```

Where u, v, k are normalized such that: **u² + v² + k² = 1**

**Example output**:
```
u = 0.65  # Contribution from c1 (squared norm)
v = 0.35  # Contribution from c2 (squared norm)
k = 0.20  # Restructuring (orthogonal component)
```

### Step 2: Filter for Substantial Mixing

Only keep cases where mixing dominates over restructuring:
```python
mixing_strength = u**2 + v**2
if mixing_strength <= 0.66:
    skip this event
```

Example:
```
mixing_strength = 0.65² + 0.35² = 0.4225 + 0.1225 = 0.545
```
If 0.545 ≤ 0.66 → **skip this event** (too much restructuring)

### Step 3: Calculate Community Dominance

Using arctan normalization to map the ratio u/v to [0, 1]:

```python
community_dominance = arctan(u/v) / (π/2)
```

**Example** (if u=0.8, v=0.4):
```
ratio = u/v = 0.8/0.4 = 2.0
arctan(2.0) = 1.1071 radians
community_dominance = 1.1071 / (π/2) = 1.1071 / 1.5708 = 0.7048
```

**This is our y value for this coalescence event: y = 0.7048**

### Why arctan normalization?

- **Linear normalization**: u/(u+v) compresses high ratios too much
- **Arctan normalization**: arctan(u/v)/(π/2) spreads out the full range more evenly
  - u >> v → arctan → π/2 → normalized to 1.0
  - u << v → arctan → 0 → normalized to 0.0
  - u = v → arctan(1) = π/4 → normalized to 0.5

---

## Data Point Duplication

After collecting all (x, y) pairs, we **duplicate** them with symmetry:

```python
x_original = [0.5115, 0.7234, 0.3456, ...]
y_original = [0.7048, 0.6123, 0.4567, ...]

# Duplicate with (1-x, 1-y)
x_final = [0.5115, 0.7234, 0.3456, ..., 0.4885, 0.2766, 0.6544, ...]
y_final = [0.7048, 0.6123, 0.4567, ..., 0.2952, 0.3877, 0.5433, ...]
```

This creates symmetry around (0.5, 0.5) because:
- If community 1 has dominance x → community 2 has dominance 1-x
- If coalescence favors c1 with y → it disfavors c2 with 1-y

---

## Complete Example

Let's trace one complete example:

### Given:
- c1: species 5 most abundant (0.5188)
- c2: species 17 most abundant (0.4212)
- α₁₂ = 0.1352, α₂₁ = 0.1741
- Vector decomposition: u=0.65, v=0.35, k=0.20

### Calculate x (species dominance):
```
x = (1 - 0.1352) / (2 - 0.1352 - 0.1741) = 0.5115
```

### Calculate y (community dominance):
```
mixing_strength = 0.65² + 0.35² = 0.545
if 0.545 > 0.66: NO → skip (in reality this would be filtered out)
```

Let's say u=0.8, v=0.6 instead (mixing = 1.0, passes filter):
```
y = arctan(0.8/0.6) / (π/2) = arctan(1.333) / 1.5708 = 0.927 / 1.5708 = 0.590
```

### Final data points added:
```
Original: (x=0.5115, y=0.590)
Duplicate: (x=0.4885, y=0.410)
```

---

## Summary

**x-axis (Species LV Dominance)**:
1. Find most abundant species in each community (C1, C2)
2. Get pairwise competition coefficients (α₁₂, α₂₁)
3. Calculate LV equilibrium: x = (1-α₁₂)/(2-α₁₂-α₂₁)
4. Range: [0, 1] where 0=sp2 dominates, 1=sp1 dominates, 0.5=equal

**y-axis (Community Dominance)**:
1. Vector decomposition: c_mix ≈ u·c1 + v·c2 + k·orthogonal
2. Filter: only keep if u²+v² > 0.66 (substantial mixing)
3. Calculate: y = arctan(u/v)/(π/2)
4. Range: [0, 1] where 0=c2 dominates, 1=c1 dominates, 0.5=equal

**Duplication**:
- Plot both (x, y) and (1-x, 1-y) for symmetry
- This doubles the number of points in the scatter plot

**Key Insight**:
- If x predicts y well → high R² → species-level competition predicts community outcomes
- If x does NOT predict y well → low R² → community dynamics are not governed by pairwise competition alone
