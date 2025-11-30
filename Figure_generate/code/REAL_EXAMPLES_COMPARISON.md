# Real Examples: u=0.2 vs u=1.0 Comparison

## Summary

Comparing weak competition (u=0.2) vs strong competition (u=1.0) using real data from rep_000, coalescence 0_1.

---

## u=0.2: Weak Competition Example

### Interaction Matrix
```
Mean α_ij:    0.20
% α_ij > 1:   0%
Range:        0.0003 to 0.40

Interpretation: ALL cross-species interactions are weaker than self-competition
                → Species can easily coexist
```

### Communities
```
Community 1: 12 species active
  Most abundant: species 8 (58.1%)
  
Community 2: 11 species active  
  Most abundant: species 26 (60.5%)
  
Coalescence: 17 species survived
  Species gained: 6 new species present
  Diversity HIGH
```

### Species-Level Prediction
```
Pairwise competition (sp8 vs sp26):
  α_12 = 0.327  (sp26 inhibits sp8 weakly)
  α_21 = 0.122  (sp8 inhibits sp26 even more weakly)
  
Both < 1 → Coexistence predicted

Dominance formula: 1 - 0.327/(2-0.327-0.122) = 0.789

Prediction: Species 8 (community 1) should dominate 78.9%
```

### Actual Community-Level Outcome
```
Vector decomposition:
  x₁ = 0.661  (44% variance from c_1)
  x₂ = 0.634  (40% variance from c_2)
  x₃ = 0.402  (16% restructuring)
  
Community dominance = 0.661/(0.661+0.634) = 0.510

Reality: Community 1 barely dominates 51.0%
```

### Species Fates
```
Species 8 (most abundant in c_1):
  Started: Rank #1 in c_1 (58.1%)
  Ended:   Rank #6 in mix (34.5%)
  Result:  LOST DOMINANCE ❌
  
Species 26 (most abundant in c_2):
  Started: Rank #1 in c_2 (60.5%)
  Ended:   Rank #2 in mix (38.9%)
  Result:  MAINTAINED HIGH RANK ✓
  
New winner: Species 24 (from c_1)
  Became #1 in coalescence (39.6%)
```

### Key Insight
```
Mismatch: 78.9% predicted vs 51.0% actual
Gap:      27.9 percentage points
Reason:   Most abundant species didn't determine outcome
          Multi-species interactions created new winner
```

---

## u=1.0: Strong Competition Example

### Interaction Matrix
```
Mean α_ij:    0.96
% α_ij > 1:   47%
Range:        0.003 to 2.00

Interpretation: HALF of interactions exceed self-competition
                → Frequent competitive exclusion
```

### Communities
```
Community 1: 4 species active (MUCH LOWER diversity!)
  Most abundant: species 27 (50.4%)
  
Community 2: 2 species active (VERY LOW diversity!)
  Most abundant: species 14 (85.6%)
  
Coalescence: 3 species survived
  Species lost: High extinction rate
  Diversity VERY LOW
```

### Species-Level Prediction
```
Pairwise competition (sp27 vs sp14):
  α_12 = 0.497  (sp14 inhibits sp27 moderately)
  α_21 = 0.186  (sp27 inhibits sp14 weakly)
  
Both < 1 → Coexistence predicted (lucky!)

Dominance formula: 1 - 0.497/(2-0.497-0.186) = 0.623

Prediction: Species 27 (community 1) should dominate 62.3%
```

### Actual Community-Level Outcome
```
Vector decomposition:
  x₁ = 0.529  (28% variance from c_1)
  x₂ = 0.702  (49% variance from c_2)
  x₃ = 0.477  (23% restructuring - HIGHER!)
  
Community dominance = 0.529/(0.529+0.702) = 0.430

Reality: Community 2 dominates 57.0% (OPPOSITE PREDICTION!)
```

### Species Fates
```
Species 27 (most abundant in c_1):
  Started: Rank #1 in c_1 (50.4%)
  Ended:   Rank #2 in mix (60.7%)
  Result:  SURVIVED but not #1 ⚠️
  
Species 14 (most abundant in c_2):
  Started: Rank #1 in c_2 (85.6%)  
  Ended:   Rank #1 in mix (72.6%)
  Result:  MAINTAINED DOMINANCE ✓✓✓
  
Strong species stays strong!
```

### Key Insight
```
Mismatch: 62.3% predicted vs 43.0% actual
Gap:      19.3 percentage points
Reason:   Prediction REVERSED!
          Strong competition caused unexpected outcomes
          Higher restructuring (23% vs 16%)
```

---

## Side-by-Side Comparison

| Metric | u=0.2 (Weak) | u=1.0 (Strong) |
|--------|--------------|----------------|
| **Interaction Strength** | | |
| Mean α_ij | 0.20 | 0.96 |
| % α > 1 | 0% | 47% |
| | | |
| **Diversity** | | |
| Species in c_1 | 12 | 4 |
| Species in c_2 | 11 | 2 |
| Species in c_mix | 17 | 3 |
| Extinction rate | Low | **High** |
| | | |
| **Most Abundant Species** | | |
| Community 1 | sp8 (58%) | sp27 (50%) |
| Community 2 | sp26 (61%) | sp14 (86%) |
| In coalescence | sp24 (40%) | sp14 (73%) |
| Winner from | **Different sp!** | Same as c_2 |
| | | |
| **Predictions** | | |
| α_12, α_21 | 0.33, 0.12 | 0.50, 0.19 |
| Both < 1? | ✓ Yes | ✓ Yes |
| Species dominance | 0.789 | 0.623 |
| | | |
| **Reality** | | |
| x₁ (from c_1) | 0.661 | 0.529 |
| x₂ (from c_2) | 0.634 | 0.702 |
| x₃ (restructuring) | 0.402 (16%) | 0.477 (23%) |
| Community dominance | 0.510 | 0.430 |
| | | |
| **Prediction vs Reality** | | |
| Predicted | 78.9% | 62.3% |
| Actual | 51.0% | 43.0% |
| Gap | 27.9 pts | 19.3 pts |
| Direction | Both favor c_1 | **OPPOSITE!** |
| Agreement | Poor | Poor |

---

## Key Biological Insights

### At u=0.2 (Weak Competition):
1. **High diversity maintained** (12+11 → 17 species)
2. **Initial dominants lose rank** (sp8 drops from #1 to #6)
3. **Moderate species emerge as winners** (sp24 becomes #1)
4. **Low restructuring** (16%) but still significant
5. **Prediction overshoots** (predicts 79%, reality 51%)

**Biology**: Weak competition allows many species to coexist. Outcomes depend on complex multi-species interactions, not just the most abundant competitors.

---

### At u=1.0 (Strong Competition):
1. **Massive diversity loss** (4+2 → 3 species, only 3 survived!)
2. **Strong species stay strong** (sp14 with 86% dominates)
3. **High extinction** (most species couldn't survive)
4. **Higher restructuring** (23%) despite fewer species
5. **Prediction REVERSED** (predicts c_1 wins, but c_2 wins!)

**Biology**: Strong competition causes competitive exclusion. The community with the most competitive species wins, but pairwise predictions still fail because they ignore community context.

---

## Why Pairwise Predictions Fail

### At u=0.2:
```
Problem: Too many species matter
  - 17 species coexist
  - Most abundant sp8 and sp26 don't control outcome
  - Moderate species (sp24) becomes dominant
  - Multi-species network effects dominate

Top-down hypothesis: FAILS
Bottom-up processes: DOMINATE
```

### At u=1.0:
```
Problem: Context matters more than pairwise
  - Only 3 species survive
  - Strong competition amplifies context effects
  - sp14 (86% in c_2) crushes everything
  - But pairwise α values don't capture this
  - Initial community composition determines winner

Top-down hypothesis: PARTIALLY WORKS (strong species wins)
But pairwise prediction: STILL FAILS (wrong direction!)
```

---

## Mathematical Explanation

### Why higher restructuring at u=1.0?

```
Restructuring (x₃) measures perpendicular distance from (u,v) plane

u=0.2: c_mix ≈ mixture of c_1 and c_2
       → Stays close to (u,v) plane
       → Low x₃ (16%)

u=1.0: c_mix = survival of strongest after harsh competition
       → New community structure emerges
       → Orthogonal to parent compositions
       → High x₃ (23%)

Paradox: Fewer species, but MORE restructuring!
Why? Because strong exclusion creates qualitatively different outcomes
```

---

## Conclusion

### Both examples show:
1. ✓ Pairwise species predictions **cannot** predict community outcomes
2. ✓ R² stays low (0.002 to 0.104) across all intensities
3. ✓ Multi-species context **always** matters

### But they differ in mechanism:

**u=0.2 (Weak)**: 
- Many species coexist → complex interactions
- Most abundant species lose importance
- Moderate species can dominate

**u=1.0 (Strong)**:
- Few species survive → harsh selection
- Strong species stay strong
- But community context still overrides pairwise predictions

### The scientific conclusion:

**Community assembly is fundamentally a BOTTOM-UP process.**

Pairwise interactions of dominant species ≠ Community-level outcomes

This is true whether competition is weak (u=0.2) or strong (u=1.0)! 🎯
