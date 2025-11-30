# Interaction Matrix Sampling Distribution

## Summary

The current simulations use a **Uniform[0, 2u]** distribution for off-diagonal interaction matrix elements.

---

## Mathematical Definition

### Distribution Function

```python
def uniform_distribution(u, o):
    """Generate uniform random interaction strength."""
    return (2*u + 2*o) * np.random.random() - o
```

### Current Parameters
- **u:** Interaction strength parameter (varies: 0.05 to 1.20)
- **o:** Offset parameter = **0** (currently)

### Simplified Form (with o=0)
```python
I[i,j] = 2*u * np.random.random()
       = Uniform[0, 2u]
```

---

## Distribution Properties

### For Off-Diagonal Elements I[i,j] (i ≠ j):

| Property | Formula | Description |
|----------|---------|-------------|
| **Distribution** | Uniform[0, 2u] | Continuous uniform |
| **Range** | [0, 2u] | All values equally likely |
| **Mean** | u | Expected interaction strength |
| **Standard Deviation** | u/√3 ≈ 0.577u | Spread around mean |
| **Minimum** | 0 | Weakest competition |
| **Maximum** | 2u | Strongest competition |

### For Diagonal Elements I[i,i]:
- **Fixed value:** 1.0 (self-interaction/intraspecific competition)

---

## Empirical Verification

Measured from actual simulation data (10 reps):

| u | Mean | Std | Min | Max | Theoretical Mean | Theoretical Std |
|---|------|-----|-----|-----|-----------------|----------------|
| **0.05** | 0.0505 | 0.0288 | 0.0004 | 0.0999 | 0.0500 | 0.0289 |
| **0.30** | 0.2937 | 0.1724 | 0.0004 | 0.5991 | 0.3000 | 0.1732 |
| **0.50** | 0.5135 | 0.2892 | 0.0003 | 0.9985 | 0.5000 | 0.2887 |
| **0.80** | 0.7942 | 0.4642 | 0.0001 | 1.5965 | 0.8000 | 0.4619 |
| **1.00** | 0.9654 | 0.5830 | 0.0027 | 1.9997 | 1.0000 | 0.5774 |
| **1.20** | 1.2104 | 0.6863 | 0.0005 | 2.3967 | 1.2000 | 0.6928 |

✅ **Empirical values match theoretical predictions very well**

---

## Biological Interpretation

### Interaction Type: **Pure Competition**

1. **All interactions are positive** (I[i,j] > 0)
   - Species always compete (never facilitate)
   - No mutualistic or commensal interactions
   - Reflects competitive exclusion principle

2. **Symmetric vs Asymmetric**
   - I[i,j] ≠ I[j,i] in general (independent draws)
   - Allows for hierarchical competitive relationships
   - Species i can be stronger competitor against j than vice versa

3. **Intensity scales with u**
   - **Low u (e.g., 0.05):** Weak competition, species coexist easily
   - **Medium u (e.g., 0.5):** Moderate competition
   - **High u (e.g., 1.2):** Strong competition, more exclusion

---

## Example Interaction Matrix

Sample matrix for **u = 0.50**, **rep_000**:

```
       Species 0  Species 1  Species 2  Species 3  Species 4
Species 0   1.0000     0.3607     0.7277     0.1127     0.6078
Species 1   0.6185     1.0000     0.9149     0.8985     0.6464
Species 2   0.5229     0.1192     1.0000     0.3750     0.7275
Species 3   0.0118     0.1024     0.6159     1.0000     0.4969
Species 4   0.0261     0.9868     0.7567     0.0459     1.0000
```

**Interpretation:**
- Diagonal = 1.0 (self-competition)
- I[0,1] = 0.361: Species 1 has moderate competitive effect on Species 0
- I[1,0] = 0.619: Species 0 has stronger competitive effect on Species 1
- **Asymmetric:** Species 0 is stronger competitor against Species 1
- All values ∈ [0, 1.0] as expected for u=0.5

---

## Generalized Lotka-Volterra Model

### Dynamics Equation

```
dN_i/dt = g_i * N_i * (1 - Σ_j(I_ij * N_j) / k_i)
```

Where:
- **N_i:** Abundance of species i
- **g_i = 1:** Growth rate (constant for all species)
- **k_i = 1:** Carrying capacity (constant for all species)
- **I_ij ~ Uniform[0, 2u]:** Competition coefficient
- **I_ii = 1:** Intraspecific competition

### Interpretation of I_ij:
- **I_ij = 0:** Species j has no effect on species i
- **I_ij = 1:** Species j has same effect as species i on itself
- **I_ij > 1:** Species j is stronger competitor than species i (to itself)
- **I_ij = 2u:** Maximum competition strength

---

## Alternative Distributions (Not Currently Used)

The code supports other distributions via the `o` parameter:

### 1. Uniform[-o, 2u+o] (General form)
```python
I[i,j] = (2*u + 2*o) * np.random.random() - o
```
- With o > 0: Shifts distribution to include negative values
- Allows facilitation (I[i,j] < 0)

### 2. Example: Uniform[-0.2, 1.0] with u=0.4, o=0.2
```python
I[i,j] = (2*0.4 + 2*0.2) * random() - 0.2
       = 1.2 * random() - 0.2
       = Uniform[-0.2, 1.0]
```
- 20% of interactions could be facilitative (negative)

---

## Comparison Across Interaction Strengths

### Visualization of Ranges

```
u = 0.05:  [0.000 ━━━━━━━━━━━━━━━━━━━━━━━━ 0.10]
u = 0.30:  [0.000 ━━━━━━━━━━━━━━━━━━━━━━━━ 0.60]
u = 0.50:  [0.000 ━━━━━━━━━━━━━━━━━━━━━━━━ 1.00]
u = 0.80:  [0.000 ━━━━━━━━━━━━━━━━━━━━━━━━ 1.60]
u = 1.00:  [0.000 ━━━━━━━━━━━━━━━━━━━━━━━━ 2.00]
u = 1.20:  [0.000 ━━━━━━━━━━━━━━━━━━━━━━━━ 2.40]
```

### Scaling Relationship

| u | Mean Competition | Max Competition | Ecological Regime |
|---|-----------------|----------------|-------------------|
| 0.05 | Weak (0.05) | Weak (0.10) | High coexistence |
| 0.30 | Moderate (0.30) | Moderate (0.60) | Mixed outcomes |
| 0.50 | Moderate-Strong (0.50) | Strong (1.00) | Some exclusion |
| 0.80 | Strong (0.80) | Very Strong (1.60) | Frequent exclusion |
| 1.00 | Strong (1.00) | Very Strong (2.00) | Dominance common |
| 1.20 | Very Strong (1.20) | Extreme (2.40) | Strong dominance |

---

## Matrix Symmetry Properties

### Upper vs Lower Triangle

For a 48×48 matrix:
- **Upper triangle:** 1,128 independent values (excluding diagonal)
- **Lower triangle:** 1,128 independent values
- **Total off-diagonal:** 2,256 independent interaction strengths
- **Diagonal:** 48 values (all = 1.0)

### Asymmetry Index

```python
asymmetry = |I[i,j] - I[j,i]| / (I[i,j] + I[j,i])
```

- **Mean asymmetry:** ~0.33 (typical for uniform random)
- **Max asymmetry:** 1.0 (when one is near 0, other near 2u)
- **Min asymmetry:** 0.0 (when both are equal by chance)

---

## Data Access

### Load Interaction Matrices

```python
import json
import numpy as np

# Load data
with open('Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json') as f:
    data = json.load(f)

# Access specific matrix
u_value = "0.50"
rep_number = "rep_005"
I = np.array(data[u_value][rep_number]['parameters']['interaction_matrix'])

# Analyze distribution
off_diagonal = I[np.triu_indices(48, k=1)]
print(f"Mean: {np.mean(off_diagonal):.4f}")
print(f"Std: {np.std(off_diagonal):.4f}")
print(f"Range: [{np.min(off_diagonal):.4f}, {np.max(off_diagonal):.4f}]")
```

---

## Key Findings

1. ✅ **Distribution matches theory perfectly**
   - Empirical mean ≈ theoretical mean (u)
   - Empirical std ≈ theoretical std (u/√3)

2. ✅ **All interactions are competitive**
   - No negative values observed
   - Range: [0, 2u] as designed

3. ✅ **Proper asymmetry**
   - I[i,j] ≠ I[j,i] allows hierarchies
   - Independent sampling for each pair

4. ✅ **Scales correctly with u**
   - Low u → weak competition → coexistence
   - High u → strong competition → exclusion

---

## Citation / Implementation

**Source code:** `run_48species_10reps_fine_WITH_MATRICES.py`

**Function:**
```python
def uniform_distribution(u, o):
    """Generate uniform random interaction strength."""
    return (2*u + 2*o) * np.random.random() - o
```

**Usage:**
```python
I, g, k = InitializeSpeciesPool(
    N=48,
    f_interaction=lambda: uniform_distribution(u=0.5, o=0),
    f_g=lambda: 1.0,
    f_k=lambda: 1.0,
    is_diagonal_one=True
)
```

---

**Last updated:** November 1, 2025
**Verified on:** 10 reps simulation data (240 matrices analyzed)
