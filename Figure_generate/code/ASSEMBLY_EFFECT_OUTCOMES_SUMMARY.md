# Assembly Effect Outcome Analysis - Summary

## Hypothesis

**"Assembly effect (coalescence) produces more cases of dominance or restructuring compared to start all (direct parent assembly)."**

## Result

### ✓ HYPOTHESIS STRONGLY SUPPORTED

## Key Findings

### Start All (Parent Communities - Direct Assembly):
- **Dominance**: 0.0% (0 out of 362)
- **Mixing**: 100.0% (362 out of 362)
- **Restructuring**: 0.0% (0 out of 362)

### Assembly Effect (Coalesced Communities):
- **Dominance**: 21.0% (76 out of 362)
- **Mixing**: 68.0% (246 out of 362)
- **Restructuring**: 11.0% (40 out of 362)

## Statistical Differences

**Assembly Effect vs Start All:**
- **Dominance**: +21.0 percentage points
- **Mixing**: -32.0 percentage points
- **Restructuring**: +11.0 percentage points

## Interpretation

### Major Finding:

**Parent communities (start all) show EXCLUSIVELY mixing outcomes** - 100% of all 362 parent communities are classified as "mixing". This means when communities are assembled directly from the full species pool, they always result in balanced mixing of the two hypothetical sub-communities.

**Coalesced communities (assembly effect) show diverse outcomes** - They exhibit all three outcome types:
1. **Dominance (21%)**: One sub-community dominates the final community
2. **Mixing (68%)**: Balanced contribution from both sub-communities
3. **Restructuring (11%)**: Emergence of novel community structure

### Biological Interpretation:

1. **Direct assembly is predictable**: Starting with the full species pool leads to reproducible, balanced communities.

2. **Coalescence introduces history dependence**: The assembly pathway (merging two pre-established communities) introduces new dynamics:
   - Priority effects can lead to dominance
   - Community interactions can create novel structures
   - History-dependent outcomes emerge

3. **Assembly history matters**: The same initial species pool can lead to very different outcomes depending on the assembly pathway:
   - Direct inoculation → Always mixing
   - Sequential assembly (coalescence) → Dominance, mixing, OR restructuring

## Method

### Vector Decomposition Classification:

For each community outcome, we decompose it into three components:
- **u**: Contribution from sub-community 1
- **v**: Contribution from sub-community 2
- **k**: Orthogonal component (restructuring)

Classification rules (from phase diagram code):
- **Dominance**: High contribution from one parent (x² > 0.5, y > 0.5)
- **Mixing**: High contribution from both parents (x² > 0.5, y < 0.5)
- **Restructuring**: Low contribution from parents (x² < 0.5)

Where:
- x = √(u² + v²)
- y = |arctan(u/v) - π/4| / (π/4)

### Comparison Strategy:

**For Parent Communities (Start All):**
- Used the same two sub-communities that formed the matched coalesced community
- Treated the parent as the "outcome" to be decomposed
- This creates a fair comparison using the same sub-community species pools

**For Coalesced Communities (Assembly Effect):**
- Used the actual two sub-communities that merged
- Treated the coalesced community as the outcome
- Standard coalescence analysis

## Files

**Analysis script**: `analyze_assembly_effect_outcomes.py`
**Figure**: `Figure/Assembly_effect/Fig_assembly_effect_outcomes_comparison.svg`
**Results data**: `Figure/Assembly_effect/assembly_effect_outcomes_results.pkl`

## Significance

This finding demonstrates that:

1. **Assembly pathway fundamentally alters community outcomes**
2. **History matters**: The order and timing of species arrival affects final community structure
3. **Coalescence is not equivalent to direct assembly**: Even with identical species pools
4. **Assembly effect is a real ecological phenomenon**: It creates qualitatively different outcomes

## Next Steps

Potential follow-up analyses:
1. Test if dominance/restructuring correlates with specific environmental conditions (LN, MN, HN)
2. Identify which species drive dominance vs restructuring outcomes
3. Examine if certain sub-community combinations are more prone to dominance
4. Investigate temporal dynamics that lead to different outcomes

## Date: 2025-01-04
