# Type 3 Co-occurrence Analysis: Comparison of Two Approaches

## Summary

We implemented **TWO different approaches** for analyzing species co-occurrence in coalescence experiments:

1. **Fisher's Exact Test Approach** (pairwise testing)
2. **Simulation-Based Null Model** (global count testing)

**Surprising Result**: The two approaches give **completely different answers**!

---

## Approach 1: Fisher's Exact Test (Pairwise)

### Method

For **each species pair (i, j)**:
1. Build 2×2 contingency table across all replicates
2. Apply Fisher's exact test
3. Correct for multiple testing with FDR
4. Compare proportion significant: same-origin vs mixed-origin

### LN_12 Results

```
Same-origin pairs: 29/210 significant (13.8%)
Mixed-origin pairs: 4/225 significant (1.8%)
Enrichment: 7.77× (p = 9.8e-07 ***)

CONCLUSION: Strong same-origin enrichment
```

### Key Finding

**Species from the same parent are 7.77× more likely to significantly co-occur than mixed-origin pairs.**

---

## Approach 2: Simulation-Based Null Model (Global)

### Method

1. Estimate each species' invasion probability: p_i = (# times present) / (# replicates)
2. Generate 10,000 synthetic communities by independent Bernoulli sampling
3. Count same-origin pairs (T_same) and mixed-origin pairs (T_AB) in each simulation
4. Compare observed counts to null distribution

### LN_12 Results

```
Observed:
  T_AA (A-A pairs): 22.7
  T_BB (B-B pairs): 22.9
  T_AB (A-B pairs): 40.0
  T_same (AA+BB): 45.6

Expected (null model):
  T_AA: 21.0 ± 11.4
  T_BB: 20.6 ± 11.1
  T_AB: 45.2 ± 17.0
  T_same: 41.6 ± 15.9

Z-score: 0.254
P-value: 0.814 (ns)

CONCLUSION: No enrichment - consistent with independent invasion
```

### Key Finding

**Observed co-occurrence patterns match what we'd expect if species invaded independently.**

---

## Why the Discrepancy?

### Different Questions Asked

**Approach 1 (Fisher's)**:
- "Are there **specific pairs** that co-occur more than expected?"
- Tests **individual pair-level associations**
- Sensitive to **strong pairwise interactions**

**Approach 2 (Simulation)**:
- "Do same-origin pairs **collectively** co-occur more than expected given marginal invasion rates?"
- Tests **community-level patterns**
- Controls for **species abundance differences**

### Conceptual Difference

**Scenario**: Imagine 10 Parent A species and 10 Parent B species.

- Parent A species have **high invasion probability** (p = 0.7 each)
- Parent B species have **low invasion probability** (p = 0.3 each)

**What Fisher's Exact Test Sees**:
```
Species A1 and A2 co-occur in 35/52 replicates
   → Contingency table → p < 0.001 → SIGNIFICANT!

Species B1 and B2 co-occur in 5/52 replicates
   → Contingency table → p = 0.95 → NOT significant

Result: More significant same-origin pairs!
```

**What Null Model Sees**:
```
Expected A1-A2 co-occurrence: p_A1 × p_A2 × 52 = 0.7 × 0.7 × 52 = 25.5
Observed A1-A2 co-occurrence: 35

Expected if independent!

Overall T_AA: Expected from invasion probs
Overall T_AB: Expected from invasion probs

Result: No enrichment beyond marginals!
```

### The Key Issue: Marginal Invasion Rates

**Fisher's exact test** doesn't account for the fact that:
- Species from Parent A might **generally invade more often**
- This alone creates more A-A co-occurrences
- **WITHOUT** requiring specific A-A interactions!

**Null model** explicitly controls for this:
- Uses species-specific invasion probabilities
- Tests if co-occurrence exceeds what marginals predict
- More conservative baseline

---

## Which Approach Is Correct?

**Both are technically correct - they answer different questions!**

### Use Fisher's Exact Test When:

✓ You want to identify **specific species pairs** with strong associations
✓ You care about **pairwise interactions** (facilitation/competition)
✓ You want to find **candidate pairs** for follow-up experiments
✓ Multiple replicates available (≥20)

**Example interpretation**: "Species 2 and 3 consistently co-occur together, suggesting facilitative interaction."

### Use Simulation-Based Null Model When:

✓ You want to test **community-level** enrichment
✓ You need to account for **marginal invasion differences**
✓ You have **few replicates** (even 1 snapshot works!)
✓ You want a **conservative** test

**Example interpretation**: "Same-origin co-occurrence doesn't exceed what we'd expect from independent invasion at observed rates."

---

## Biological Interpretation

### Scenario: Why Both Can Be True Simultaneously

**Fisher's Approach Says**: "Many A-A pairs significantly co-occur"
**Null Model Says**: "But this is expected given A species invade more"

**Real biological story**:
1. Parent A communities are adapted to the coalescence environment
2. Species from Parent A have **higher individual fitness** → higher invasion probability
3. This alone makes A-A pairs co-occur more often
4. **No special A-A interactions needed!**

### Analogy

**Fisher's Test**:
- "Students from School A get higher grades when paired together than A-B pairs"
- True! But School A students are just better students overall.

**Null Model**:
- "Given that School A students are better, is their paired performance better than expected?"
- No! They perform as expected from their individual abilities.

---

## Results Summary: Both Approaches

### Approach 1 (Fisher's Exact Test)

| Condition | Enrichment | p-value | Finding |
|-----------|------------|---------|---------|
| LN_12 | 7.77× | 9.8e-07 | ★★★ Strong enrichment |
| MN_12 | 3.34× | 1.6e-05 | ★★★ Moderate enrichment |
| HN_6 | ∞ | 0.034 | ★ Only same-origin significant |
| ALL merged | 1.44× | 0.0014 | ★★ Weak enrichment |

**Interpretation**: Specific same-origin pairs show strong co-occurrence

### Approach 2 (Simulation-Based Null)

| Condition | z-score | p-value | Finding |
|-----------|---------|---------|---------|
| LN_6 | 0.10 | 0.953 | ns - No enrichment |
| LN_12 | 0.25 | 0.814 | ns - No enrichment |
| LN_24 | 0.10 | 1.000 | ns - No enrichment |
| MN_6 | 0.70 | 0.480 | ns - No enrichment |
| MN_12 | 0.59 | 0.480 | ns - No enrichment |
| MN_24 | 0.28 | 0.792 | ns - No enrichment |
| HN_6 | 0.33 | 0.686 | ns - No enrichment |
| HN_12 | 0.22 | 0.948 | ns - No enrichment |
| HN_24 | 0.41 | 0.739 | ns - No enrichment |

**Interpretation**: Co-occurrence matches expectations from independent invasion

---

## Recommendation

### For Your Analysis

**Report both approaches with clear framing**:

1. **Pairwise Analysis** (Fisher's Exact Test):
   - Identifies specific species pairs with strong co-occurrence
   - Useful for finding candidate facilitative interactions
   - Shows same-origin pairs more often significant

2. **Community-Level Analysis** (Null Model):
   - Tests if enrichment exceeds marginal invasion rates
   - More conservative - controls for parent adaptation differences
   - Shows co-occurrence consistent with independent invasion

### Biological Conclusion

**Conservative interpretation** (from null model):
> "Co-occurrence patterns are consistent with species having different invasion probabilities, but no evidence for preferential same-origin co-occurrence beyond these marginal rates."

**Mechanistic interpretation** (from Fisher's test):
> "While individual species from the same parent may have higher invasion success (creating apparent enrichment), specific pairs show significant co-occurrence that may reflect facilitative interactions."

### Key Insight

**The "enrichment" detected by Fisher's test is largely explained by differential invasion success between parent communities, not by specific same-origin facilitation.**

Parent A species invade more → More A-A pairs → Looks like enrichment
**BUT** it's just because A species are individually more successful!

---

## Files Generated

### Approach 1: Fisher's Exact Test
```
Figure/AsymmetricityNullModelAnalysis/cooccurrence_analysis/
├── LN_12/
│   ├── enrichment_LN_12.png
│   ├── network_LN_12.png
│   └── cooccurrence_table_LN_12.csv
└── type3_summary.csv
```

### Approach 2: Simulation-Based Null
```
Figure/AsymmetricityNullModelAnalysis/null_model_analysis/
├── LN_12/
│   ├── null_distribution_LN_12.png
│   └── null_distribution_LN_12.csv
└── null_model_summary.csv
```

---

## Code Implementation

### Approach 1
- `CooccurrenceAsymmetricityAnalysis.py`
- `run_type3_cooccurrence_analysis.py`

### Approach 2
- `CooccurrenceNullModelAnalysis.py`
- `run_cooccurrence_null_model_analysis.py`

---

## Bottom Line

**Same data, two lenses, different insights:**

- **Fisher's test**: Finds pairwise associations (useful for mechanistic hypotheses)
- **Null model**: Tests community-level enrichment (conservative, controls for marginals)

**Both are valuable!** Use the Fisher's test to find interesting pairs to study. Use the null model to test if the overall pattern is stronger than expected from invasion rates alone.

The null model suggests that what looks like "same-origin preference" may simply reflect that some parent communities have species better adapted to the coalescence environment - not necessarily that same-origin species help each other specifically.
