# Interaction Matrix Distribution Comparison: Uniform vs Gamma

## Quick Reference

| Distribution | Mean Control | Variance Control | When to Use |
|--------------|--------------|------------------|-------------|
| **Uniform [0, 2u]** | ✓ (via u) | ✗ (coupled to mean) | Simple baseline, symmetric bounds |
| **Gamma(k, θ)** | ✓ (via mean) | ✓ (via CV, independent) | Biological realism, flexible variance |

---

## 1. Current Implementation: Uniform Distribution

### Formula
```python
I[i,j] = uniform_distribution(u, 0)
       = Uniform[0, 2u]
```

### Properties
- **Mean**: μ = u
- **Variance**: σ² = u²/3
- **Standard deviation**: σ = u/√3 ≈ 0.577u
- **Coefficient of variation**: CV = σ/μ = 1/√3 ≈ 0.577 **(FIXED!)**
- **Range**: [0, 2u]

### Limitation
**Variance is LOCKED to mean**: When you change u to adjust mean, variance changes proportionally. CV is always ≈ 0.577.

### Example
```
u = 0.3:  mean = 0.30, std = 0.173, CV = 0.577
u = 0.5:  mean = 0.50, std = 0.289, CV = 0.577
u = 0.8:  mean = 0.80, std = 0.462, CV = 0.577
```

---

## 2. New Implementation: Gamma Distribution

### Formula
```python
I[i,j] = gamma_distribution_mean_cv(mean, cv)
       = Gamma(k=1/CV², θ=mean×CV²)
```

### Properties
- **Mean**: μ = k × θ (you specify directly)
- **Variance**: σ² = k × θ² = (mean × CV)²
- **Standard deviation**: σ = mean × CV
- **Coefficient of variation**: CV (you specify directly)
- **Range**: [0, ∞) (effectively [0, mean + 3σ])

### Advantage
**Independent control**: Fix mean, vary CV to change variance. Or vice versa!

### Example: Same mean, different variance
```
mean = 0.5, CV = 0.2:  std = 0.10  (tight distribution)
mean = 0.5, CV = 0.5:  std = 0.25  (moderate spread)
mean = 0.5, CV = 1.0:  std = 0.50  (wide spread)
mean = 0.5, CV = 1.5:  std = 0.75  (very wide spread)
```

### Example: Match uniform's CV = 0.577
```
mean = 0.3, CV = 0.577:  std = 0.173  (same as uniform u=0.3)
mean = 0.5, CV = 0.577:  std = 0.289  (same as uniform u=0.5)
mean = 0.8, CV = 0.577:  std = 0.462  (same as uniform u=0.8)
```

---

## 3. Visual Comparison

### Scenario 1: Varying Mean (Fixed CV = 0.577, matching uniform)

```
Uniform:              Gamma (CV=0.577):
u=0.3 → CV=0.577      mean=0.3, CV=0.577
u=0.5 → CV=0.577      mean=0.5, CV=0.577
u=0.8 → CV=0.577      mean=0.8, CV=0.577

Result: IDENTICAL statistical properties
```

### Scenario 2: Varying Variance (Fixed Mean = 0.5)

```
Uniform:              Gamma:
u=0.5 → CV=0.577      mean=0.5, CV=0.2  (TIGHTER)
(only one option)     mean=0.5, CV=0.577 (SAME)
                      mean=0.5, CV=1.0  (WIDER)
                      mean=0.5, CV=1.5  (MUCH WIDER)

Result: Gamma allows exploration of variance at fixed mean!
```

---

## 4. Biological Interpretation

### Low CV (0.2 - 0.3): Homogeneous Interactions
- All species interact with similar strength
- Predictable, uniform competition
- Example: Well-mixed, resource-limited environment

### Medium CV (0.5 - 0.7): Moderate Heterogeneity
- Some variation in interaction strengths
- Most interactions near mean, some outliers
- Similar to uniform distribution (CV ≈ 0.577)
- Example: Natural communities with niche structure

### High CV (1.0 - 1.5): Heterogeneous Interactions
- Wide range of interaction strengths
- Many weak interactions, occasional strong ones
- Skewed distribution (more small values)
- Example: Complex food webs with specialists and generalists

---

## 5. Research Questions Enabled

### With Uniform (Current)
- ✓ How does mean interaction strength affect coalescence?
- ✗ How does interaction heterogeneity affect coalescence at fixed mean?

### With Gamma (New)
- ✓ How does mean interaction strength affect coalescence?
- ✓ How does interaction heterogeneity affect coalescence at fixed mean?
- ✓ Does high variance lead to more unpredictable outcomes?
- ✓ Are homogeneous vs heterogeneous systems fundamentally different?

---

## 6. Practical Usage

### Match existing uniform simulations:
```bash
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.3 0.5 0.8 \
  --cvs 0.577 0.577 0.577 \
  --reps 10
```

### Explore variance at fixed mean:
```bash
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.5 0.5 0.5 \
  --cvs 0.2 0.5 1.0 \
  --reps 10
```

### Compare distributions directly:
```bash
# Uniform baseline
python run_simulation_WITH_GAMMA.py \
  --distribution uniform \
  --means 0.3 0.5 0.8 \
  --reps 10

# Gamma with matched CV
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.3 0.5 0.8 \
  --cvs 0.577 \
  --reps 10
```

---

## 7. Expected Results

### Hypothesis: Variance matters!

**At low mean (e.g., 0.3):**
- High CV → More mixing (weak interactions can't dominate)
- Low CV → More dominance (predictable competition)

**At high mean (e.g., 0.8):**
- High CV → More restructuring (occasional very strong interactions)
- Low CV → More dominance (consistently strong competition)

**Test this by comparing phase diagrams!**

---

## 8. File Naming Convention

To distinguish distributions in saved data:

```
Uniform:
Simulation_Data/gamma_mean0.30_cv0.577_10reps/Community_uniform.json

Gamma (match uniform):
Simulation_Data/gamma_mean0.30_cv0.577_10reps/Community_gamma.json

Gamma (explore variance):
Simulation_Data/gamma_mean0.50_cv0.20_10reps/Community_gamma.json
Simulation_Data/gamma_mean0.50_cv0.50_10reps/Community_gamma.json
Simulation_Data/gamma_mean0.50_cv1.00_10reps/Community_gamma.json
```

---

## Summary

**Before (Uniform):** One parameter (u) controls both mean and variance together

**After (Gamma):** Two parameters (mean, CV) control mean and variance independently

**Key Insight:** Gamma distribution lets you ask: "At the same average interaction strength, does variability in interaction strengths change community coalescence outcomes?"

This is a fundamental ecological question that the uniform distribution cannot address!
