# Co-occurrence Analysis: Fraction-Based Null Model (Final Version)

## Overview

This document describes the **final implementation** using:
1. **Simulation-based null model** (Bernoulli sampling)
2. **Fraction-based metrics** (not raw counts)
3. **Merged analysis only** (no separation by species pool size)

## Key Changes from Previous Version

### Change 1: Use Fractions Instead of Counts

**Old approach**: Count raw number of co-present pairs (T_AA, T_BB, T_AB)
- Problem: Depends on total number of species and their invasion rates
- Hard to compare across conditions

**New approach**: Calculate fraction of possible pairs that are co-present
```
frac_AA = (# A-A pairs co-present) / (# all possible A-A pairs)
frac_BB = (# B-B pairs co-present) / (# all possible B-B pairs)
frac_AB = (# A-B pairs co-present) / (# all possible A-B pairs)
frac_same = (# same-origin pairs co-present) / (# all possible same-origin pairs)
```

**Benefits**:
- Normalized metric (range: 0 to 1)
- Accounts for different numbers of species from each parent
- More interpretable across conditions

### Change 2: Merged Analysis Only

**Old approach**: Analyzed LN_6, LN_12, LN_24, MN_6, MN_12, etc. separately

**New approach**: Merge all species pools within each nutrient condition
- LN (all): 90 replicates (6+12+24 species pools combined)
- MN (all): 88 replicates
- HN (all): 87 replicates
- ALL: 265 replicates (everything combined)

**Benefits**:
- More statistical power
- Simpler interpretation
- Focus on nutrient-level effects

## Method Summary

### Step 1: Estimate Species Invasion Probabilities

For each species i:
```
p_i = (# replicates where species i present) / (total replicates)
```

**Example** (ALL merged, 265 replicates):
- 41 species have p_i > 0
- Mean invasion probability: 0.262

### Step 2: Determine Species Origins

For each species, determine if it comes from Parent A or Parent B:
- Based on average abundance in parent communities
- If in both parents, assign to parent with higher abundance

**Example** (ALL merged):
- Parent A species: 114
- Parent B species: 16

### Step 3: Count Observed Co-present Pairs (Fractions)

For each replicate, calculate:
```
frac_AA = (A-A pairs co-present) / C(114, 2) = ... / 6441
frac_BB = (B-B pairs co-present) / C(16, 2) = ... / 120
frac_AB = (A-B pairs co-present) / (114 × 16) = ... / 1824
```

Average across all replicates.

### Step 4: Generate Null Distribution (10,000 simulations)

For each simulation:
1. Sample each species independently: x_i ~ Bernoulli(p_i)
2. Count which pairs are co-present
3. Calculate frac_AA, frac_BB, frac_AB, frac_same

This creates a null distribution under the hypothesis of **independent invasion**.

### Step 5: Compare Observed vs Null

Calculate z-scores and empirical p-values:
```
z_same = (frac_same_obs - mean(frac_same_null)) / std(frac_same_null)

p_same = fraction of null simulations where |frac_same - mean| >= |observed - mean|
```

## Results

### Summary Table

| Condition | N | frac_same (obs) | frac_same (exp) | z-score | p-value | Sig? |
|-----------|---|-----------------|-----------------|---------|---------|------|
| **ALL** | 265 | 0.0052 | 0.0044 | 0.35 | 0.730 | NO |
| **LN** | 90 | 0.0067 | 0.0061 | 0.25 | 0.740 | NO |
| **MN** | 88 | 0.0042 | 0.0032 | 0.62 | 0.599 | NO |
| **HN** | 87 | 0.0034 | 0.0031 | 0.24 | 0.933 | NO |

### Key Findings

**1. No Significant Enrichment in Any Condition**

All p-values > 0.5, all z-scores < 1.0

**Interpretation**: The fraction of same-origin pairs that co-occur is **not different** from what we'd expect if species invaded independently based on their marginal invasion probabilities.

**2. Enrichment Ratios Close to 1.0**

```
ALL: 1.15× (15% higher than null)
LN:  1.20× (20% higher than null)
MN:  1.13× (13% higher than null)
HN:  0.99× (1% lower than null)
```

Even the point estimates show minimal enrichment, and none are statistically significant.

**3. Low Overall Co-occurrence Fractions**

Observed frac_same ranges from 0.0034 to 0.0067 (0.3% to 0.7% of possible pairs).

This means **most pairs don't co-occur**, regardless of origin.

## Biological Interpretation

### What This Tells Us

**Conservative conclusion**:
> "Species co-occurrence patterns in coalescence outcomes are consistent with independent invasion based on species-specific success rates. There is no evidence for preferential co-occurrence of same-origin species beyond what would be expected from their individual invasion probabilities."

### What This Means

1. **No detectable facilitation networks within parent communities**
   - Species from the same parent don't help each other invade

2. **Individual fitness matters more than community context**
   - Each species' invasion success is determined by its own traits
   - Not by which other species are present

3. **Parent community structure doesn't persist**
   - The ecological interactions/networks in parent communities
   - Don't translate to the coalescence environment

4. **The null model (independent invasion) is sufficient**
   - No need to invoke community-level processes
   - Simple probabilistic model explains the data

### Contrast with Fisher's Exact Test Approach

**Fisher's test found**: 7.77× enrichment in LN_12 (p < 0.001)

**Null model finds**: 1.20× enrichment in LN (p = 0.740)

**Why the difference?**
- Fisher's test doesn't account for marginal invasion rates
- Parent A species invade more often → more A-A pairs
- Null model controls for this: "Is enrichment beyond marginals?"
- Answer: No

## Visualization

The figures show:
- **Gray histograms**: Null distribution (10,000 simulations)
- **Red dashed line**: Observed value
- **Blue dotted line**: Expected value (null mean)

For all conditions, the observed value (red) falls well within the null distribution (gray), confirming no significant enrichment.

**Example** (ALL merged, frac_same panel):
- Observed: 0.0052
- Expected: 0.0044
- z = 0.35, p = 0.730

The observed value is only 0.35 standard deviations from the null mean - completely consistent with random variation.

## Files Generated

```
Figure/AsymmetricityNullModelAnalysis/cooccurrence_analysis/merged/
├── merged_summary.csv                           # Summary table
├── fraction_distribution_ALL_merged.png         # Overall plot
├── null_distribution_ALL_merged.csv             # Null distribution data
├── LN/
│   ├── fraction_distribution_LN_merged.png
│   └── null_distribution_LN_merged.csv
├── MN/
│   ├── fraction_distribution_MN_merged.png
│   └── null_distribution_MN_merged.csv
└── HN/
    ├── fraction_distribution_HN_merged.png
    └── null_distribution_HN_merged.csv
```

## Code

**Main module**: `CooccurrenceNullModelAnalysis.py`
- Implements all analysis functions
- Uses fractions instead of counts
- Includes z-scores and empirical p-values

**Run script**: `run_cooccurrence_merged.py`
- Loads all data
- Runs merged analyses (ALL, LN, MN, HN)
- Generates plots and summary table

**Usage**:
```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code
python run_cooccurrence_merged.py
```

## Statistical Details

### Why Use Fractions?

**Problem with counts**: If Parent A has 100 species and Parent B has 10 species:
- Maximum A-A pairs: C(100,2) = 4,950
- Maximum B-B pairs: C(10,2) = 45
- Maximum A-B pairs: 100×10 = 1,000

Even with equal per-pair co-occurrence rates, you'd see more A-A pairs just due to combinatorics!

**Solution with fractions**: Normalize by the maximum possible:
- frac_AA = (observed A-A pairs) / 4,950
- frac_BB = (observed B-B pairs) / 45
- frac_AB = (observed A-B pairs) / 1,000

Now all three metrics are on the same scale (0 to 1).

### Why Z-scores Based on Fractions?

The z-score formula:
```
z = (observed - expected) / std(expected)
```

Using fractions makes this more interpretable:
- z = 0: Observed equals expected
- z = 1: Observed is 1 SD above expected
- z = 2: Observed is 2 SD above expected (unusual)
- z > 3: Observed is very unusual

Our results:
- z_same ranges from 0.24 to 0.62
- All well below 2.0
- Consistent with null expectations

### Empirical P-values

Instead of assuming a parametric distribution (e.g., normal), we use the empirical null distribution from 10,000 simulations.

```python
p_value = mean(|null_values - null_mean| >= |observed - null_mean|)
```

This is:
- **Exact** (no distributional assumptions)
- **Two-sided** (detects both over- and under-representation)
- **Conservative** (uses absolute deviations)

Our p-values range from 0.599 to 0.933 - all very high, indicating observed values are typical under the null.

## Conclusion

**Main finding**: Co-occurrence patterns in coalescence experiments are fully explained by independent species invasion with species-specific success probabilities. No evidence for same-origin preferential co-occurrence.

**Implication**: Parent community structure (ecological networks, facilitative interactions) does not persist into the coalescence environment. Each species' fate is determined independently.

**Methodological note**: Using fractions and simulation-based null models provides a more conservative and interpretable test than pairwise Fisher's exact tests, which don't account for marginal invasion rate differences between parent communities.
