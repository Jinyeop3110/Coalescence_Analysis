# Assembly Effect Analysis - Final Summary

## Three Approaches to Identifying Comparable Pairs

We created three different approaches for identifying assembly effect pairs, each with different assumptions about what constitutes "comparable" communities:

---

## Approach 1: Match by Final Species Composition (**DEPRECATED**)
**File:** `identify_assembly_effect_pairs.py`

### Method:
- Compare **final observed species** in parent vs coalesced communities
- Filter for pairs with ≥80% species overlap in final composition

### Results:
- **Total: 3 unique pairs** (8 counting replicates)
  - LN: 2 pairs (24 vs 12+12)
  - MN: 1 pair (24 vs 12+12)
  - HN: 0 pairs

### Problems:
- **Wrong comparison**: Uses OUTCOME as selection criterion
- Species overlap in final composition is what we want to MEASURE, not use for filtering
- Misses most potentially interesting pairs

---

## Approach 2: All Pairwise Comparisons (**TOO BROAD**)
**File:** `identify_assembly_effect_pairs_corrected.py`

### Method:
- Compare ALL parent communities with ALL coalesced communities
- No filtering by species composition
- Only requirement: same medium condition

### Results:
- **Total: 5,264 pairs**
  - LN: 1,692 pairs (396 for 12 vs 6+6, 1,296 for 24 vs 12+12)
  - MN: 1,772 pairs (476 for 12 vs 6+6, 1,296 for 24 vs 12+12)
  - HN: 1,800 pairs (504 for 12 vs 6+6, 1,296 for 24 vs 12+12)

### Problems:
- **Too many comparisons**: Includes many incomparable pairs
- Compares communities with completely different initial species pools
- Not a fair "assembly effect" comparison if starting pools are different
- Good for exploratory analysis, but not targeted comparison

---

## Approach 3: Match by INITIAL Species Pool (**RECOMMENDED** ✓)
**File:** `identify_assembly_pairs_by_initial_pool.py`

### Method:
- **Infer initial species pool** from observed species (low threshold to catch rare species)
- For coalesced: initial pool = union of species in Sub1 + Sub2
- For parent: initial pool = species observed in parent community
- Match pairs with ≥80% Jaccard similarity in **INITIAL** pools

### Results:
- **Total: 6 pairs**
  - LN: 4 pairs (0 for 12 vs 6+6, 4 for 24 vs 12+12)
  - MN: 0 pairs
  - HN: 2 pairs (0 for 12 vs 6+6, 2 for 24 vs 12+12)

### Advantages:
- **Correct comparison**: Matches communities that started with same species pool
- Fair test of assembly effect: same starting conditions, different assembly pathways
- Separates initial pool (controlled) from final outcome (measured)

---

## Recommended Approach: Approach 3

**Use `identify_assembly_pairs_by_initial_pool.py`** for assembly effect analysis.

### Why This is Correct:

1. **Assembly effect definition**: How does assembly pathway (direct vs coalescence) affect final community **given the same initial species pool**?

2. **Controlled comparison**:
   - **Same**: Initial species available
   - **Different**: Assembly pathway (direct vs coalescence)
   - **Measure**: Final diversity, composition, stability

3. **Fair comparison**: Both communities had access to the same species, but one was assembled directly while the other went through coalescence

### The 6 Identified Pairs:

All 6 pairs are for **Pool 24 vs 12+12** comparison:
- 4 pairs in LN medium
- 0 pairs in MN medium
- 2 pairs in HN medium

**Note:** No pairs found for Pool 12 vs 6+6, suggesting the experimental design didn't create matching initial pools at this scale.

---

## Data Files Summary

### Generated Files (in `Figure/Assembly_effect/`):

1. **assembly_pairs_initial_pool.pkl** ✓ RECOMMENDED
   - 6 pairs matched by initial species pool
   - Includes both initial pool and final composition data

2. **all_assembly_pairs.pkl**
   - 5,264 all pairwise comparisons
   - Useful for exploratory analysis

3. **comparable_pairs.pkl** (DEPRECATED)
   - 3 pairs matched by final composition
   - Do not use

### Summary Files:

1. **assembly_pairs_statistics.csv** - Statistics from all pairwise approach
2. **comparable_pairs_summary.csv** - Summary from deprecated approach

---

## Key Findings

### Initial Pool Matching Results:

**LN Medium (4 pairs found):**
- These pairs have 80%+ overlap in initial species pools
- Can directly compare assembly effects

**MN Medium (0 pairs):**
- No parent-24 communities share initial pools with coalesced 12+12
- Cannot do assembly effect comparison at this pool size

**HN Medium (2 pairs):**
- Limited pairs available for comparison

### Interpretation:

The **small number of pairs** (6 total) suggests:
1. The experiment was not specifically designed to create matching initial pools
2. Each community had a unique species composition
3. By chance, a few pairs have similar enough initial pools for comparison

---

## Example Usage

```python
import pickle

# Load the recommended dataset
with open('Figure/Assembly_effect/assembly_pairs_initial_pool.pkl', 'rb') as f:
    data = pickle.load(f)

# Access LN medium pairs for 24 vs 12+12
ln_pairs = data['pairs']['LN']['24_vs_12+12']

for pair in ln_pairs:
    print(f"Parent {pair['parent_community_idx']} vs Coalesced {pair['coalesced_community_idx']}")
    print(f"  Initial pool overlap: {pair['initial_pool_jaccard']:.1%}")
    print(f"  Parent final diversity: {pair['parent_final_diversity']}")
    print(f"  Coalesced final diversity: {pair['coalesced_final_diversity']}")
    print(f"  Difference: {pair['parent_final_diversity'] - pair['coalesced_final_diversity']}")
```

---

## Next Steps for Analysis

With the 6 pairs matched by initial pool:

1. **Diversity comparison**:
   - Does assembly pathway affect final species richness?
   - Statistical test: paired t-test or Wilcoxon

2. **Compositional analysis**:
   - Which species survive in each pathway?
   - Bray-Curtis dissimilarity between pathways

3. **Retention analysis**:
   - What fraction of initial pool survives in each pathway?
   - Are certain species more/less likely to survive through coalescence?

4. **Medium effects**:
   - Why do pairs exist in LN and HN but not MN?
   - Do environmental conditions interact with assembly pathway?

---

## Files Location

All analysis files are in:
```
/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/
```

### Recommended files:
- **Script**: `identify_assembly_pairs_by_initial_pool.py`
- **Data**: `Figure/Assembly_effect/assembly_pairs_initial_pool.pkl`
- **Documentation**: This file

---

## Conclusion

**Use Approach 3** (matching by initial species pool) for assembly effect analysis. This gives you **6 high-quality pairs** where:
- Initial species pools are matched (≥80% Jaccard similarity)
- Assembly pathways differ (direct vs coalescence)
- Final outcomes can be fairly compared

The small number of pairs reflects the reality that the experiment wasn't designed for this specific comparison, but these 6 pairs provide a solid foundation for analyzing assembly effects where they do exist.
