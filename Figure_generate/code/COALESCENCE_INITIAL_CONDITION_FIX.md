# Coalescence Initial Condition - Critical Fix

## The Problem

The original simulation code had **incorrect initial conditions** for coalescence experiments.

### What Was Wrong

**INCORRECT (Original):**
```python
# Coalescence initial condition
y0 = np.zeros(48)
y0[start1:end1] = 0.01  # Community 1 species at 0.01
y0[start2:end2] = 0.01  # Community 2 species at 0.01
```

This starts **both communities from the same low abundance (0.01)**, which is NOT a proper coalescence experiment. This is essentially starting from scratch with both communities present, not mixing two established communities.

### What Should Be Correct

**CORRECT (Fixed):**
```python
# Get equilibrium states of each community
c1_equilibrium = sc_list[f"c{comm1_idx+1}"]  # Already at equilibrium
c2_equilibrium = sc_list[f"c{comm2_idx+1}"]  # Already at equilibrium

# Coalescence: Mix 50% of each equilibrium community
y0 = 0.5 * c1_equilibrium + 0.5 * c2_equilibrium
```

This properly models **mixing two established communities** at their equilibrium states, which is what a coalescence experiment should be.

---

## Why This Matters

### Biological Interpretation

**Coalescence = Mixing two established communities**

In real coalescence experiments:
1. Community 1 grows alone to equilibrium
2. Community 2 grows alone to equilibrium
3. You **mix equal amounts** of these two equilibrated communities
4. Observe the outcome after the mixture re-equilibrates

### The Old Method Was Wrong Because:

1. **Not mixing equilibrium communities**: Starting both at 0.01 means neither community has reached its natural equilibrium state yet
2. **Equal starting conditions don't reflect reality**: In real experiments, each community would have different species abundances at equilibrium
3. **Confounds competition dynamics**: The dynamics observed would be from simultaneous colonization + competition, not from established communities interacting

### The New Method Is Correct Because:

1. **Uses equilibrium states**: Each community is first grown to equilibrium separately
2. **Proper mixing**: Takes 50% biomass from each equilibrated community
3. **Reflects real coalescence**: This matches what you'd do experimentally - mix equal volumes of two cultures

---

## Example

### Community 1 at Equilibrium (12 species)
```
Species 0-11 abundances: [0.8, 0.0, 1.2, 0.0, 0.5, ...]
(Some species survived, some went extinct)
```

### Community 2 at Equilibrium (12 species)
```
Species 12-23 abundances: [0.0, 1.1, 0.0, 0.7, 0.9, ...]
(Different pattern of survival)
```

### Coalescence Initial Condition (Correct)
```
y0 = 0.5 × c1_equilibrium + 0.5 × c2_equilibrium

Species 0-11:  [0.4, 0.0, 0.6, 0.0, 0.25, ...]  (50% of c1)
Species 12-23: [0.0, 0.55, 0.0, 0.35, 0.45, ...] (50% of c2)
Species 24-47: [0, 0, 0, ...]                     (not involved)
```

This is a **realistic starting point** for observing coalescence dynamics!

---

## What Was Fixed

### File: `run_uniform_narrow_range.py`

**Before (Lines 110-113):**
```python
# Initial condition: both communities present
y0 = np.zeros(N)
y0[start1:end1] = 0.01
y0[start2:end2] = 0.01
```

**After (Lines 105-110):**
```python
# Get equilibrium states of both communities
c1_equilibrium = np.array(sc_list[f"c{comm1_idx+1}"])
c2_equilibrium = np.array(sc_list[f"c{comm2_idx+1}"])

# Initial condition: 0.5 of each equilibrium community
y0 = 0.5 * c1_equilibrium + 0.5 * c2_equilibrium
```

---

## Impact on Results

### Expected Differences

1. **Phase boundaries may shift**: The interaction strength at which outcomes change could be different
2. **More realistic dynamics**: Results should better reflect real coalescence experiments
3. **Species identity matters more**: The specific equilibrium composition of each community now affects the outcome

### What Needs Checking

**All previous simulations with the old initial conditions need to be re-evaluated!**

Including:
- ✅ Narrow uniform distribution (already fixed and rerun)
- ⚠️ Wide uniform distribution (needs fixing)
- ⚠️ Gamma distribution simulations (needs fixing)
- ⚠️ All phase diagrams from old data (need regenerating)

---

## Verification

### Narrow Uniform Distribution (Fixed)

**Re-run completed:** ✅
- File: `run_uniform_narrow_range.py`
- Data: `Simulation_Data/48species_10reps_narrow_uniform/Community_10reps_narrow_uniform.json`
- Phase diagram: `Figure/PhaseDiagram/Fig_phase_diagram_10reps_narrow_uniform.svg`
- Time: 8.3 minutes
- Simulations: 240 (24 means × 10 reps)

**Verification:**
```python
# Check one example from the data
import json
with open('Simulation_Data/48species_10reps_narrow_uniform/Community_10reps_narrow_uniform.json', 'r') as f:
    data = json.load(f)

# Get equilibrium communities
c1 = data['0.50']['rep_000']['sc_list']['c1']
c2 = data['0.50']['rep_000']['sc_list']['c2']

# Get coalescence
c1_c2 = data['0.50']['rep_000']['cc_list']['c1_c2']

# The coalescence should have started from 0.5*c1 + 0.5*c2
# (We can't verify the initial condition directly, but the final states should be consistent)
```

---

## Action Items

### Immediate

- [x] Fix narrow uniform simulation
- [x] Rerun narrow uniform with correct initial conditions
- [x] Regenerate phase diagram

### To Do

- [ ] Check and fix ALL other simulation scripts
- [ ] Rerun wide uniform distribution with correct initial conditions
- [ ] Rerun gamma distribution simulations
- [ ] Regenerate all phase diagrams
- [ ] Compare old vs new results to quantify the impact

---

## Files That Need Fixing

Search for this pattern in all simulation scripts:

```python
# WRONG PATTERN (needs fixing):
y0 = np.zeros(N)
y0[start1:end1] = 0.01
y0[start2:end2] = 0.01
```

Replace with:

```python
# CORRECT PATTERN:
c1_equilibrium = np.array(sc_list[f"c{comm1_idx+1}"])
c2_equilibrium = np.array(sc_list[f"c{comm2_idx+1}"])
y0 = 0.5 * c1_equilibrium + 0.5 * c2_equilibrium
```

### Files to Check:

```bash
grep -l "y0\[start1:end1\] = 0.01" *.py
```

Likely candidates:
- `run_48species_10reps_fine_WITH_MATRICES.py`
- `run_48species_200reps_fine_WITH_MATRICES.py`
- `run_simulation_WITH_GAMMA.py`
- Any other simulation scripts

---

## Summary

### The Fix

**Changed from:**
- Starting coalescence with both communities at arbitrary low abundance (0.01)

**Changed to:**
- Starting coalescence with 50% of each community's equilibrium state

### Why It Matters

This is **not a minor technical detail** - it's **fundamental to what coalescence means**:
- Old method: "What happens when two groups of species colonize together?"
- New method: "What happens when two established communities are mixed?"

These are **different biological questions** with potentially **different answers**.

### Current Status

✅ Narrow uniform distribution: **FIXED and rerun**
⚠️ All other simulations: **Need to be checked and potentially rerun**

---

## Technical Note

The old method might still be valid for some specific questions (like "competitive exclusion from low abundance"), but for **community coalescence** experiments (which is what this study is about), the corrected method is appropriate.

If you want to keep the old method for comparison, it should be renamed to something like "co-colonization" or "simultaneous invasion" to distinguish it from true coalescence.
