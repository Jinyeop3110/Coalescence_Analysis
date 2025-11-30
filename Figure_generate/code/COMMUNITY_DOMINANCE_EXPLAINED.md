# Community Dominance Calculation - Complete Explanation

## Overview

**Question**: When two communities coalesce, which parent contributed more to the outcome?

**Method**: Vector decomposition in 48-dimensional species space

**Result**: A dominance value between 0 and 1
- 0.0 = Community 2 fully dominates
- 0.5 = Equal contribution (neutral)
- 1.0 = Community 1 fully dominates

---

## Mathematical Framework

### Input: Three Community Vectors

Each community is a 48-dimensional vector (one dimension per species):

```
c_1 = [sp0_abundance, sp1_abundance, ..., sp47_abundance]  ← Parent 1
c_2 = [sp0_abundance, sp1_abundance, ..., sp47_abundance]  ← Parent 2
c_mix = [sp0_abundance, sp1_abundance, ..., sp47_abundance] ← Coalescence outcome
```

### Goal: Decompose c_mix

We want to express:
```
c_mix ≈ α·c_1 + β·c_2 + restructuring

Where:
  α = contribution from parent 1
  β = contribution from parent 2
  restructuring = new community structure (not from either parent)
```

---

## Step-by-Step Calculation

### Step 1: Normalize to Unit Vectors

```python
u = c_1 / ||c_1||    # Unit vector for parent 1
v = c_2 / ||c_2||    # Unit vector for parent 2
m = c_mix / ||c_mix|| # Unit vector for coalescence

# After normalization: ||u|| = ||v|| = ||m|| = 1
```

**Why normalize?** So we measure *direction* (composition) not *magnitude* (total abundance)

---

### Step 2: Project m onto (u,v) Plane

We solve for coefficients e₁ and e₂ in:
```
m ≈ e₁·u + e₂·v
```

This is a **least squares problem**:
```
Minimize: ||m - (e₁·u + e₂·v)||²

Solution: Solve A·[e₁, e₂]ᵀ = [u·m, v·m]ᵀ

Where A is the Gram matrix:
A = [[u·u, u·v],
     [u·v, v·v]]
```

**Geometric interpretation**: Finding the best approximation of m using only u and v

---

### Step 3: Apply Positivity Constraint

```python
x₁ = max(e₁, 0)  # Only keep positive contribution
x₂ = max(e₂, 0)  # Negative would mean "opposite direction"
```

**Why?** Negative coefficients don't make biological sense (can't have negative contribution)

---

### Step 4: Calculate Restructuring

```python
residual = m - (e₁·u + e₂·v)
x₃ = ||residual||
```

**Interpretation**: 
- x₃ = 0 → Perfect mixture of parents
- x₃ = 1 → Completely new structure
- Typically x₃ ≈ 0.2-0.5 (moderate restructuring)

---

### Step 5: Normalize to Sum to 1

Ensure total variance sums to 1:
```python
# We want: x₁² + x₂² + x₃² = 1

convert = √[(1 - x₃²) / (x₁² + x₂²)]

final_x₁ = convert · x₁
final_x₂ = convert · x₂
final_x₃ = x₃
```

---

### Step 6: Calculate Dominance

```python
community_dominance = x₁ / (x₁ + x₂)
```

**Interpretation**:
- Ignores restructuring component
- Focuses only on relative contributions from the two parents
- Range: [0, 1] where 0.5 = equal

---

## Worked Example

Using actual data: u=0.2, rep_000, coalescence 0_1

### Input:
```
Community 1: 12 species active (e.g., sp0=0.457, sp8=0.581, ...)
Community 2: 11 species active (e.g., sp7=0.340, sp26=0.605, ...)
Coalescence: 17 species active (mix of both + some lost/gained)
```

### After normalization:
```
||u|| = 1.0000
||v|| = 1.0000
||m|| = 1.0000
```

### Projection coefficients:
```
e₁ = 0.6607  (coefficient for parent 1)
e₂ = 0.6338  (coefficient for parent 2)
```

### Decomposition:
```
x₁ = 0.6607  (43.6% of variance from parent 1)
x₂ = 0.6338  (40.2% of variance from parent 2)
x₃ = 0.4023  (16.2% is restructuring)

Verification: 0.6607² + 0.6338² + 0.4023² = 1.0000 ✓
```

### Final dominance:
```
dominance = 0.6607 / (0.6607 + 0.6338)
          = 0.6607 / 1.2945
          = 0.5104
          = 51.0%
```

**Interpretation**: Community 1 barely dominates (51% vs 49%)

---

## Visual Interpretation

### 3D Representation

```
            m (coalescence)
           /|\
          / | \     ← Perpendicular distance = restructuring (x₃)
         /  |  \
        /   |   \
       /    |    \
------+-----+-----+------ Plane spanned by u and v
       \    |    /
        \   |   /  
         \  |  /
          \ | /    ← Projection = α·u + β·v
           \|/
            
On the plane: 
  α = 0.661 along u direction
  β = 0.634 along v direction
  
Dominance = α/(α+β) = 51%
```

### 2D Simplified View

```
        v (parent 2)
        ↑
        |
    β   |
   ⟋    |
  m     |     α
    ⟍   |   ⟋
        + -------→ u (parent 1)
        
If m closer to u → parent 1 dominates
If m closer to v → parent 2 dominates
If m in middle → balanced
```

---

## Why This Metric?

### Advantages:
1. **Accounts for full community composition** (all 48 species)
2. **Separates mixture from restructuring** (x₁, x₂ vs x₃)
3. **Scale-invariant** (uses normalized vectors)
4. **Symmetric** (treats both parents equally)

### What it measures:
- **NOT** which species survived
- **NOT** total abundance
- **YES** compositional similarity to each parent
- **YES** relative balance of contributions

---

## Connection to Your Analysis

### In the plot:

**X-axis**: Species-level dominance (from pairwise LV competition)
- Based on: Most abundant species only (2 species)
- Prediction from: α₁₂, α₂₁ interaction coefficients

**Y-axis**: Community-level dominance (from vector decomposition)
- Based on: All species (48 dimensions)
- Calculated from: Actual coalescence outcome

### Why low correlation (R² < 0.11)?

```
Species-level (X): Predicts based on 2 species pairwise competition
                   "If species 8 vs 26 competed alone..."

Community-level (Y): Reality of 17 species interacting
                     "When 23 species from both communities mixed..."

Gap: Multi-species interactions >> pairwise predictions
```

---

## Example Scenarios

### Scenario 1: Perfect Mixture
```
x₁ = 0.707, x₂ = 0.707, x₃ = 0
dominance = 0.5 (50%)
→ Equal contribution, no restructuring
```

### Scenario 2: Complete Dominance
```
x₁ = 1.0, x₂ = 0, x₃ = 0
dominance = 1.0 (100%)
→ Parent 1 completely took over
```

### Scenario 3: High Restructuring (typical)
```
x₁ = 0.6, x₂ = 0.6, x₃ = 0.53
dominance = 0.5 (50%)
→ Equal contribution but 28% new structure!
```

### Scenario 4: Asymmetric with Restructuring
```
x₁ = 0.8, x₂ = 0.4, x₃ = 0.45
dominance = 0.67 (67%)
→ Parent 1 dominates, 20% restructuring
```

---

## Key Insights from Your Data

Looking at coalescence 0_1 (u=0.2):

| Metric | Value | Meaning |
|--------|-------|---------|
| x₁ | 0.661 | Parent 1 contributes 44% of variance |
| x₂ | 0.634 | Parent 2 contributes 40% of variance |
| x₃ | 0.402 | Restructuring is 16% of variance |
| dominance | 0.510 | Barely balanced (51% vs 49%) |

**High restructuring** (16%) indicates:
- Coalescence created novel community structure
- Not just a simple mixture
- Species interactions matter
- Context-dependent assembly

This is why **top-down predictions fail**: The most abundant species (8 vs 26) predicted 79% dominance, but reality was 51% (nearly equal)!

---

## Mathematical Properties

### Constraints:
- x₁, x₂, x₃ ≥ 0 (non-negative)
- x₁² + x₂² + x₃² = 1 (normalized)
- dominance ∈ [0, 1] (bounded)

### Special cases:
- If u ⊥ v (orthogonal): A is diagonal, easy to solve
- If u ∥ v (parallel): Cannot decompose (degenerate)
- If m ⊥ plane(u,v): x₃ = 1 (pure restructuring)

### Numerical stability:
- Small ε (1e-8) prevents division by zero
- Positivity constraint prevents negative contributions
- Normalization ensures scale-invariance

---

## Summary

**Community dominance** = Relative contribution of parent communities to coalescence outcome, measured by vector decomposition in high-dimensional species space.

**Key formula**: `dominance = x₁ / (x₁ + x₂)`

Where x₁, x₂ come from projecting the coalescence outcome onto the plane spanned by the two parent communities.

This metric captures **compositional similarity** while accounting for **restructuring**, making it a robust measure of community-level outcomes! 🎯
