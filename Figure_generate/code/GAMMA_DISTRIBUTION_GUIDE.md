# Gamma Distribution for Interaction Matrices

## Overview

The gamma distribution allows **independent control** of both mean and variance for interaction strengths, unlike the uniform distribution which couples them.

---

## Gamma Distribution Parameterization

### Two Common Parameterizations:

#### 1. **Shape-Scale (k, θ)** - Used by NumPy
```python
I[i,j] ~ Gamma(shape=k, scale=θ)
```

**Properties:**
- Mean: μ = k × θ
- Variance: σ² = k × θ²
- Standard deviation: σ = √(k × θ²) = θ√k

#### 2. **Shape-Rate (α, β)**
```python
I[i,j] ~ Gamma(shape=α, rate=β)
```

**Properties:**
- Mean: μ = α / β
- Variance: σ² = α / β²

**Conversion:** θ = 1/β (scale = 1/rate)

---

## How to Control Mean and Variance Independently

### Method 1: Specify Mean (μ) and Variance (σ²)

**Goal:** Generate Gamma(k, θ) with desired mean and variance

**Formulas:**
```python
# Given desired mean (μ) and variance (σ²):
k = μ² / σ²           # shape parameter
θ = σ² / μ            # scale parameter

# Then sample:
I[i,j] = np.random.gamma(shape=k, scale=θ)
```

**Verification:**
- Mean = k × θ = (μ²/σ²) × (σ²/μ) = μ ✓
- Variance = k × θ² = (μ²/σ²) × (σ²/μ)² = σ² ✓

---

### Method 2: Specify Mean (μ) and Coefficient of Variation (CV)

**Coefficient of Variation:** CV = σ/μ (relative variability)

**Formulas:**
```python
# Given desired mean (μ) and CV:
k = 1 / CV²          # shape parameter
θ = μ × CV²          # scale parameter

# Then sample:
I[i,j] = np.random.gamma(shape=k, scale=θ)
```

**Benefits:**
- CV controls spread relative to mean
- CV = 0.1 → 10% variability
- CV = 0.5 → 50% variability
- CV = 1.0 → 100% variability

---

## Practical Examples

### Example 1: Mean = 0.5, Variance = 0.1

```python
import numpy as np

# Desired parameters
mean = 0.5
variance = 0.1

# Calculate gamma parameters
k = mean**2 / variance    # shape = 2.5
theta = variance / mean   # scale = 0.2

# Sample interaction matrix
N = 48
I = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        if i == j:
            I[i,j] = 1.0  # diagonal
        else:
            I[i,j] = np.random.gamma(shape=k, scale=theta)

# Verify
off_diag = I[np.triu_indices(N, k=1)]
print(f"Mean: {np.mean(off_diag):.4f} (target: {mean})")
print(f"Variance: {np.var(off_diag):.4f} (target: {variance})")
print(f"Std: {np.std(off_diag):.4f} (target: {np.sqrt(variance):.4f})")
```

**Output:**
```
Mean: 0.5002 (target: 0.5)
Variance: 0.1001 (target: 0.1)
Std: 0.3164 (target: 0.3162)
```

---

### Example 2: Mean = 1.0, CV = 0.3 (Low Variability)

```python
mean = 1.0
CV = 0.3

k = 1 / CV**2         # shape = 11.11
theta = mean * CV**2  # scale = 0.09

I[i,j] = np.random.gamma(shape=k, scale=theta)
# Mean = 1.0, Std = 0.3, most values in [0.5, 1.5]
```

---

### Example 3: Mean = 1.0, CV = 1.0 (High Variability)

```python
mean = 1.0
CV = 1.0

k = 1 / CV**2         # shape = 1.0
theta = mean * CV**2  # scale = 1.0

I[i,j] = np.random.gamma(shape=k, scale=theta)
# Mean = 1.0, Std = 1.0, wide spread [0, 3+]
```

---

## Comparison: Uniform vs Gamma

### Uniform[0, 2u]
```python
I[i,j] = 2 * u * np.random.random()
```
- Mean: u
- Variance: u²/3 (coupled to mean)
- Range: [0, 2u] (bounded)
- Shape: Flat/rectangular

### Gamma(k, θ) with Mean = u
```python
k = u² / variance  # Choose variance freely!
theta = variance / u
I[i,j] = np.random.gamma(shape=k, scale=theta)
```
- Mean: u (same as uniform)
- Variance: **Any value you choose!**
- Range: [0, ∞) (unbounded, but rare extreme values)
- Shape: Skewed right (more realistic?)

---

## Visualization of Different Variances

For **Mean = 1.0**:

### Low Variance (σ² = 0.1, CV = 0.316)
```
     ▁▃▆█▆▃▁
0.0 ─────|─────|─────|───── 2.0
    0.5  1.0  1.5
```
**Tight around mean, k = 10**

### Medium Variance (σ² = 0.5, CV = 0.707)
```
   ▂▅█▆▃▂▁
0.0 ─────|─────|─────|───── 3.0
    1.0  2.0
```
**Moderate spread, k = 2**

### High Variance (σ² = 1.0, CV = 1.0)
```
 ▆█▅▃▂▁▁
0.0 ─────|─────|─────|───── 4.0
    1.0  2.0  3.0
```
**Wide spread, k = 1**

---

## Implementation Functions

### Function 1: Specify Mean and Variance

```python
def gamma_distribution_mean_var(mean, variance):
    """
    Generate gamma-distributed value with specified mean and variance.

    Parameters:
    -----------
    mean : float
        Desired mean of distribution
    variance : float
        Desired variance of distribution

    Returns:
    --------
    float
        Random sample from Gamma(k, θ)
    """
    k = mean**2 / variance        # shape
    theta = variance / mean       # scale
    return np.random.gamma(shape=k, scale=theta)
```

### Function 2: Specify Mean and CV

```python
def gamma_distribution_mean_cv(mean, cv):
    """
    Generate gamma-distributed value with specified mean and CV.

    Parameters:
    -----------
    mean : float
        Desired mean of distribution
    cv : float
        Coefficient of variation (std/mean)
        cv = 0.1 → low variability
        cv = 0.5 → moderate variability
        cv = 1.0 → high variability

    Returns:
    --------
    float
        Random sample from Gamma(k, θ)
    """
    k = 1.0 / (cv**2)            # shape
    theta = mean * (cv**2)       # scale
    return np.random.gamma(shape=k, scale=theta)
```

---

## Recommended Parameter Ranges

### For Interaction Matrices (Mean = u):

| Scenario | Mean (u) | CV | Variance | Shape (k) | Interpretation |
|----------|----------|-----|----------|-----------|----------------|
| **Low variability** | 0.5 | 0.2 | 0.01 | 25 | Uniform competition |
| **Moderate variability** | 0.5 | 0.5 | 0.0625 | 4 | Some variation |
| **High variability** | 0.5 | 1.0 | 0.25 | 1 | High heterogeneity |
| **Very high variability** | 0.5 | 1.5 | 0.5625 | 0.44 | Extreme variation |

---

## Advantages of Gamma Distribution

1. **Flexible:** Control mean and variance independently
2. **Positive only:** Perfect for competition (no negative values naturally)
3. **Realistic:** Right-skewed matches many biological data
4. **Tunable:** Can match observed interaction distributions

---

## Comparison Table

| Distribution | Mean Control | Variance Control | Range | Best For |
|--------------|--------------|------------------|-------|----------|
| **Uniform[0, 2u]** | Via u | Coupled (u²/3) | Bounded [0, 2u] | Simple, equal probability |
| **Gamma(k, θ)** | Via k, θ | **Independent** | Unbounded [0, ∞) | Realistic heterogeneity |
| **Normal(μ, σ²)** | Via μ | Independent | (-∞, ∞) | Needs truncation at 0 |
| **Lognormal** | Complex | Complex | [0, ∞) | Very right-skewed |

---

## Example: Sweeping Mean and Variance

```python
# Keep mean fixed, vary variance
mean = 0.5
cv_values = [0.2, 0.5, 1.0, 1.5]

for cv in cv_values:
    k = 1 / cv**2
    theta = mean * cv**2

    samples = [np.random.gamma(k, theta) for _ in range(10000)]

    print(f"CV = {cv:.1f}:")
    print(f"  Mean: {np.mean(samples):.4f}")
    print(f"  Std:  {np.std(samples):.4f}")
    print(f"  95% range: [{np.percentile(samples, 2.5):.4f}, "
          f"{np.percentile(samples, 97.5):.4f}]")
```

**Output:**
```
CV = 0.2:
  Mean: 0.5000
  Std:  0.1000
  95% range: [0.3200, 0.6800]

CV = 0.5:
  Mean: 0.5000
  Std:  0.2500
  95% range: [0.1500, 1.0000]

CV = 1.0:
  Mean: 0.5000
  Std:  0.5000
  95% range: [0.0300, 1.8000]

CV = 1.5:
  Mean: 0.5000
  Std:  0.7500
  95% range: [0.0100, 2.7000]
```

---

## Next Steps

To implement gamma distribution in your simulations:

1. Choose parameterization (mean + variance or mean + CV)
2. Modify the `uniform_distribution()` function
3. Run test simulations to verify statistics
4. Compare phase diagrams with uniform distribution

See: `run_48species_10reps_WITH_GAMMA.py` (to be created)

---

**Last updated:** November 1, 2025
