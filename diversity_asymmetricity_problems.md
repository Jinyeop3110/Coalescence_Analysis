# Problems with Current Diversity-Based Asymmetricity Measures

## The Fundamental Flaw

The current diversity-based asymmetricity measures (Type 1 and Type 2) suffer from a **critical statistical bias**: they conflate **initial diversity differences** with **asymmetric coalescence effects**.

### Problem 1: Baseline Diversity Bias

**Current formulas:**
- Type 1: `|min(div1, mixed) - min(div2, mixed)| / mixed`  
- Type 2: `|min(div1, mixed) - min(div2, mixed)| / (mixed - min(div1, div2))`

**The issue:** Communities with different starting diversities have fundamentally different **mathematical opportunities** for species loss.

### Concrete Example of the Bias

Consider two coalescence events with identical biological processes but different starting diversities:

**Event A (High Diversity Parents):**
- Parent 1: 20 species → 15 survive (75% retention)
- Parent 2: 18 species → 13 survive (72% retention)  
- Mixed: 22 species
- **Biological reality:** Nearly symmetric retention (75% vs 72%)
- **Type 1 score:** |min(20,22) - min(18,22)| / 22 = |20 - 18| / 22 = **0.09**

**Event B (Low Diversity Parents):**
- Parent 1: 4 species → 3 survive (75% retention)  
- Parent 2: 2 species → 1 survive (50% retention)
- Mixed: 4 species
- **Biological reality:** Moderately asymmetric retention (75% vs 50%)
- **Type 1 score:** |min(4,4) - min(2,4)| / 4 = |4 - 2| / 4 = **0.50**

### The Paradox

Event B appears **5× more asymmetric** than Event A, despite:
1. Event A having a larger absolute difference (2 vs 1 species)
2. Event B having only moderate biological asymmetry
3. **Both events following the same underlying coalescence mechanism**

This occurs because **low-diversity communities have fewer species available to lose**, creating an artificial ceiling effect.

### Problem 2: Mathematical Constraints Create False Patterns

**Mathematical ceiling effects:**
- A 2-species community can lose at most 2 species
- A 20-species community can lose up to 20 species  
- The **opportunity space** for asymmetricity scales with initial diversity
- Current measures don't account for this fundamental constraint

**False biological conclusions:**
- Low-diversity coalescences appear "more asymmetric" mathematically
- High-diversity coalescences appear "more symmetric" mathematically
- **This bias obscures real biological differences in competitive dynamics**

### Problem 3: Failure to Control for Expected Patterns

**Missing null expectation:** The current measures don't ask:
- "Given these starting diversities, how asymmetric would we expect purely random species loss to be?"
- "Is the observed asymmetricity significantly different from random chance?"

**Statistical significance ignored:** Without controlling for baseline expectations:
- We can't distinguish biological asymmetricity from mathematical artifacts
- We can't compare asymmetricity across different diversity contexts
- We can't identify which coalescence events are **truly** biologically meaningful

### Problem 4: Ignores Species Identity and Overlap

**Current approach assumes:**
- All species are equivalent
- Species identity doesn't matter
- Overlap between communities is irrelevant

**Biological reality:**
- Overlapping species have different retention dynamics
- Parent-specific species face different competitive pressures
- The **mechanism** of asymmetricity depends on which types of species are lost

## Why This Matters for Coalescence Research

### Scientific Validity
- **Current measures conflate mathematical artifacts with biological mechanisms**
- Results may mislead about which conditions promote asymmetric coalescence
- Cross-condition comparisons are statistically invalid

### Experimental Design Impact  
- Studies comparing different diversity levels will show spurious patterns
- Effect sizes will be systematically biased by initial diversity
- **Publication bias toward low-diversity "significant" results**

### Mechanistic Understanding
- Can't distinguish between:
  - Competitive exclusion (active suppression)
  - Random species loss (neutral drift)  
  - Environmental filtering (shared responses)
  - Priority effects (establishment order)

## Conclusion

The current diversity-based asymmetricity measures are **mathematically flawed** and **biologically misleading**. They create systematic biases that obscure the true biological processes underlying community coalescence.

**We need retention-based measures that:**
1. Control for initial diversity differences
2. Account for species identity and overlap patterns
3. Test against appropriate null expectations
4. Distinguish random from directed asymmetricity

The next step is developing **retention probability-based asymmetricity measures** that address these fundamental issues.