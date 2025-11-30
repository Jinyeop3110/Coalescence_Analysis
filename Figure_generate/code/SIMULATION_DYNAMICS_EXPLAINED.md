# How the Coalescence Simulation Works

## Overview

The simulation has **3 main stages** for each parameter combination:

1. **Parent communities grow alone** (4 communities)
2. **Coalescence events** (6 pairwise combinations)
3. **Record final equilibrium states**

---

## Stage 1: Parent Communities Growing Alone

### Initial Condition
Each community starts with **all 12 species at very low abundance** (0.01):

```python
y0 = np.zeros(48)
y0[start_idx:end_idx] = 0.01  # 12 species at 0.01 each
```

**Example for Community 1 (species 0-11):**
```
t=0:   [0.01, 0.01, 0.01, ..., 0.01]  (all 12 at 0.01)
       Total = 0.12
```

### Dynamics (Lotka-Volterra Integration)
The species grow and compete according to:

```
dN_i/dt = g_i × N_i × (1 - Σ_j(I_ij × N_j) / k_i)
```

Where:
- **g_i = 1.0** (growth rate)
- **k_i = 1.0** (carrying capacity)
- **I_ij** = interaction strength (from the interaction matrix)
- **I_ii = 1.0** (self-interaction)

### What Happens Over Time

**Early (t=0-50):**
- All species grow exponentially
- Total abundance increases rapidly
- Species don't yet compete strongly

**Middle (t=50-500):**
- Competition intensifies
- Weak competitors start declining
- Some species go extinct (abundance < 10⁻⁶)
- System approaches equilibrium

**Late (t=500-2000):**
- System settles to equilibrium
- Surviving species have stable abundances
- Extinct species remain at 0

### Final Equilibrium State

**Example at t=2000:**
```
c1: [0.31, 0.18, 0.27, 0.18, 0.30, 0.00, 0.32, ...]
    Total ≈ 2.8 (11 species survived, 1 extinct)
```

**Key observations:**
- Total abundance > initial (grew from 0.12 to 2.8)
- Not all species survive (competitive exclusion)
- Each community reaches its own equilibrium

---

## Stage 2: Coalescence (Mixing Two Communities)

### Initial Condition
Mix **50% of each parent community's equilibrium state**:

```python
c1_equilibrium = [0.31, 0.18, 0.27, ...]  # From parent c1
c2_equilibrium = [0.23, 0.05, 0.19, ...]  # From parent c2

y0_coalescence = 0.5 × c1_equilibrium + 0.5 × c2_equilibrium
```

**Example coalescence of c1 + c2:**
```
t=0 (initial):
  c1 species (0-11):  0.5 × [0.31, 0.18, ...] = [0.155, 0.09, ...]
  c2 species (12-23): 0.5 × [0.23, 0.05, ...] = [0.115, 0.025, ...]
  Total from c1: 1.41
  Total from c2: 0.88
  Grand total: 2.29
```

### Why This Initial Condition?

This models a **realistic coalescence experiment**:
1. Grow community 1 to equilibrium in one flask
2. Grow community 2 to equilibrium in another flask
3. Mix equal volumes from both flasks
4. Let the mixture re-equilibrate

### Dynamics During Coalescence

The mixed community undergoes **secondary competition**:

**Early (t=0-100):**
- Species from both communities are now competing
- New interactions that didn't exist in parent communities
- Some species may grow, others decline

**Middle (t=100-500):**
- Cross-community competition intensifies
- Species from one community may outcompete the other
- Total abundance may increase or decrease

**Late (t=500-2000):**
- New equilibrium is reached
- Three possible outcomes:
  1. **Dominance:** One community wins, other extinct
  2. **Mixing:** Both communities coexist
  3. **Restructuring:** Completely new composition

### Final Outcome Examples

**Case 1: Dominance**
```
Final state:
  c1 species: [0.31, 0.18, ...]  Total = 2.8 (same as parent)
  c2 species: [0.00, 0.00, ...]  Total = 0.0 (extinct!)

→ Community 1 dominated
```

**Case 2: Mixing**
```
Final state:
  c1 species: [0.20, 0.12, ...]  Total = 1.5 (reduced)
  c2 species: [0.18, 0.04, ...]  Total = 1.5 (also present)

→ Both communities coexist (50/50)
```

**Case 3: Restructuring**
```
Final state:
  c1 species: [0.05, 0.00, ...]  Total = 0.3 (mostly extinct)
  c2 species: [0.45, 0.20, ...]  Total = 2.5 (but different composition)

→ New community structure emerged
```

---

## Important Issues & Considerations

### 1. Numerical Instability

**Problem:** Sometimes the system doesn't truly equilibrate by t=2000, especially with:
- Very weak interactions (mean < 0.1)
- Very strong interactions (mean > 1.0)
- High variance (large std)

**Symptom:** Abundances explode to huge values (like 10^200) or oscillate

**Current handling:** Just take final state at t=2000 (may not be equilibrium!)

**Better solutions:**
- Check for stability (compare t=1900-2000)
- Detect oscillations
- Extend integration time for unstable systems
- Use adaptive time stepping

### 2. Oscillations

**Some systems never reach steady state** - they oscillate forever!

**Example:**
```
t=1800: Total = 3.2
t=1900: Total = 2.8
t=2000: Total = 3.2  ← Oscillating!
```

**Current handling:** Record whatever happens to be at t=2000

**Better handling:**
- Detect oscillations (FFT or autocorrelation)
- Time-average over last 500 time units
- Flag oscillating systems separately

### 3. Extinction Threshold

Species with abundance < 10⁻⁶ are set to exactly 0:

```python
final_state[final_state < 1e-6] = 0
```

**Purpose:** Prevent numerical artifacts from tiny abundances

**Effect:** A species at 10⁻⁷ is treated as extinct

---

## Step-by-Step Example

Let's trace one complete simulation:

### Parameters
- **mean = 0.3**
- **std = 0.1** (narrow uniform [0.15, 0.45])
- **rep = 0** (seed = 10000)

### Step 1: Generate Interaction Matrix
```
I[0,1] = 0.32  (random from [0.15, 0.45])
I[0,2] = 0.21
...
I[47,46] = 0.38
I[i,i] = 1.0  (diagonal)
```

### Step 2: Community 1 Alone (species 0-11)
```
t=0:    [0.01, 0.01, ..., 0.01]  Total = 0.12
t=100:  [0.25, 0.18, ..., 0.22]  Total = 2.1  (growing)
t=500:  [0.30, 0.17, ..., 0.00]  Total = 2.8  (equilibrium)
t=2000: [0.31, 0.18, ..., 0.00]  Total = 2.8  (stable)
        11 species survived
```

### Step 3: Community 2 Alone (species 12-23)
```
t=0:    [0.01, 0.01, ..., 0.01]  Total = 0.12
t=2000: [0.23, 0.05, ..., 0.07]  Total = 1.8
        12 species survived
```

### Step 4: Coalescence c1 + c2
```
Initial (mix 50/50):
  [0.155, 0.09, ..., 0.115, 0.025, ...]
  c1 total: 1.4, c2 total: 0.9, Total: 2.3

t=100 (competing):
  [0.20, 0.12, ..., 0.15, 0.03, ...]
  c1 total: 1.6, c2 total: 1.1, Total: 2.7

t=2000 (equilibrium):
  [0.20, 0.12, ..., 0.18, 0.04, ...]
  c1 total: 1.5, c2 total: 1.5, Total: 3.0

Outcome: MIXING (49.9% c1, 50.1% c2)
```

### Step 5: Vector Decomposition

The final coalescence state is decomposed into:
- **u_coeff:** Contribution from parent c1
- **v_coeff:** Contribution from parent c2
- **k_coeff:** Residual (new structure)

This determines the outcome classification.

---

## What Gets Saved

For each (mean, std, rep) combination, we save:

```json
{
  "sc_list": {
    "c1": [48 abundances],  // Community 1 equilibrium
    "c2": [48 abundances],  // Community 2 equilibrium
    "c3": [48 abundances],  // Community 3 equilibrium
    "c4": [48 abundances]   // Community 4 equilibrium
  },
  "cc_list": {
    "c1_c2": [48 abundances],  // c1+c2 coalescence outcome
    "c1_c3": [48 abundances],  // c1+c3 coalescence outcome
    ... (6 total)
  },
  "parameters": {
    "interaction_matrix": [[48×48 matrix]],
    "target_mean": 0.3,
    "target_std": 0.1,
    ...
  }
}
```

**Note:** We save the **final equilibrium states**, not the full time series!

---

## Summary

### The Process:
1. **Generate** interaction matrix with target mean/std
2. **Simulate** each community alone from t=0 to t=2000
3. **Mix** 50% of each equilibrium community
4. **Re-simulate** coalescence from t=0 to t=2000
5. **Record** final states
6. **Repeat** for all (mean, std, rep) combinations

### Key Points:
- ✅ Parent communities start from low abundance (0.01)
- ✅ Coalescence starts from 50% of each parent's equilibrium
- ✅ Integration time is t=2000 (may not always reach equilibrium!)
- ✅ Extinction threshold is 10⁻⁶
- ⚠️ Some systems may oscillate or be numerically unstable
- ⚠️ Taking final time point may miss oscillations

### Next Steps:
To improve robustness, consider:
1. Adding equilibrium detection
2. Detecting and handling oscillations
3. Using adaptive time stepping
4. Flagging problematic simulations
