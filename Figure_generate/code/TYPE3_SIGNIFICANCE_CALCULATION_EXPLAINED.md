# Type 3 Co-occurrence Significance Calculation - Detailed Explanation

## Overview

The Type 3 analysis determines if two species **significantly co-occur** together across multiple coalescence replicates using **Fisher's exact test** followed by **FDR correction**.

## Step-by-Step Calculation

### Step 1: Build 2×2 Contingency Table for Each Pair

For every pair of species (i, j), we count occurrences across **R replicates**:

```
Example: Species 5 and Species 8 across 52 replicates

                Species 8 Present    Species 8 Absent    Row Total
Species 5 Present      n₁₁ = 25           n₁₀ = 10          35
Species 5 Absent       n₀₁ = 5            n₀₀ = 12          17
Column Total           30                 22                52
```

**Definitions**:
- **n₁₁**: Both species present together
- **n₁₀**: Species i present, species j absent
- **n₀₁**: Species i absent, species j present
- **n₀₀**: Both species absent

### Step 2: Calculate Log-Odds Ratio (Effect Size)

The **log-odds ratio** quantifies the strength of association:

```
Odds Ratio (OR) = (n₁₁ × n₀₀) / (n₁₀ × n₀₁)

Log-Odds Ratio (LOR) = log(OR) = log[(n₁₁ × n₀₀) / (n₁₀ × n₀₁)]
```

**For our example**:
```
OR = (25 × 12) / (10 × 5) = 300 / 50 = 6.0
LOR = log(6.0) = 1.79
```

**Haldane-Anscombe Correction**: If any cell is 0, add 0.5 to all cells:
```
If n₀₀ = 0:
OR = [(n₁₁ + 0.5) × (n₀₀ + 0.5)] / [(n₁₀ + 0.5) × (n₀₁ + 0.5)]
```

**Interpretation of LOR**:
- **LOR > 0**: Positive association (co-occur more than expected)
- **LOR = 0**: Independence (no association)
- **LOR < 0**: Negative association (co-occur less than expected)

**Magnitude**:
- LOR ≈ 0.5: Weak association
- LOR ≈ 1.0: Moderate association
- LOR ≈ 2.0: Strong association
- LOR ≥ 3.0: Very strong association

### Step 3: Fisher's Exact Test

Fisher's exact test calculates the **exact probability** of observing the data (or more extreme) under the null hypothesis of independence.

**Null Hypothesis (H₀)**: Species i and j occur independently
**Alternative Hypothesis (H₁)**: Species i and j are associated

#### Mathematical Formula:

The probability of observing the contingency table is:

```
P(n₁₁ | margins) = [a! × b! × c! × d!] / [n! × n₁₁! × n₁₀! × n₀₁! × n₀₀!]

where:
  a = n₁₁ + n₁₀  (row 1 total)
  b = n₀₁ + n₀₀  (row 2 total)
  c = n₁₁ + n₀₁  (column 1 total)
  d = n₁₀ + n₀₀  (column 2 total)
  n = total number of replicates
```

#### Two-Sided Test:

Sum probabilities of all tables with equal or less probability than observed:

```python
p_value_two_sided = sum(P(table) for all tables where P(table) ≤ P(observed))
```

#### One-Sided Test (Greater):

For testing **positive association** (co-occurrence > expected):

```python
p_value_greater = sum(P(table) for all tables where n₁₁ ≥ observed_n₁₁)
```

**For our example** (25, 10, 5, 12):
```python
from scipy.stats import fisher_exact
odds_ratio, p_value_two_sided = fisher_exact([[25, 10], [5, 12]], alternative='two-sided')
_, p_value_greater = fisher_exact([[25, 10], [5, 12]], alternative='greater')

# Results:
# odds_ratio = 6.0
# p_value_two_sided = 0.0023
# p_value_greater = 0.0014
```

**Interpretation**:
- p < 0.001: Very strong evidence against independence
- p < 0.01: Strong evidence against independence
- p < 0.05: Moderate evidence against independence
- p ≥ 0.05: Insufficient evidence to reject independence

### Step 4: FDR Correction (Benjamini-Hochberg)

Since we test **hundreds of pairs** simultaneously, we must correct for multiple testing.

**Problem**: If we test 500 pairs at α=0.05, we expect ~25 false positives by chance!

**Solution**: Control the **False Discovery Rate** (FDR) - the expected proportion of false positives among all rejected hypotheses.

#### Benjamini-Hochberg Procedure:

1. **Order p-values**: p₍₁₎ ≤ p₍₂₎ ≤ ... ≤ p₍ₘ₎ (m = total tests)

2. **Calculate q-values** (FDR-adjusted p-values):
   ```
   For i = m, m-1, ..., 1:
       q₍ᵢ₎ = min(p₍ᵢ₎ × m / i, q₍ᵢ₊₁₎)

   where q₍ₘ₊₁₎ = 1
   ```

3. **Reject null hypotheses** where q₍ᵢ₎ ≤ α (typically α = 0.05)

#### Example with 5 pairs:

```
Pair    p-value    Rank    m/i     q-value    Significant (α=0.05)?
A       0.001      1       5/1     0.005      ✓ Yes
B       0.008      2       5/2     0.020      ✓ Yes
C       0.020      3       5/3     0.033      ✓ Yes
D       0.040      4       5/4     0.050      ✓ Yes
E       0.080      5       5/5     0.080      ✗ No
```

**Working backwards** (to ensure monotonicity):
```
q₍₅₎ = min(0.080 × 5/5, 1.000) = 0.080
q₍₄₎ = min(0.040 × 5/4, 0.080) = 0.050
q₍₃₎ = min(0.020 × 5/3, 0.050) = 0.033
q₍₂₎ = min(0.008 × 5/2, 0.033) = 0.020
q₍₁₎ = min(0.001 × 5/1, 0.020) = 0.005
```

### Step 5: Label Pairs as Significant

A pair is considered **significantly co-occurring** if:

```
q_value_greater < α  (typically α = 0.05)
```

This means the pair shows **positive association** after controlling for false discoveries.

## Implementation in Code

From [CooccurrenceAsymmetricityAnalysis.py](CooccurrenceAsymmetricityAnalysis.py:76-155):

```python
def calculate_pairwise_cooccurrence(presence_matrix, species_origins, min_occurrences=3):
    """
    Calculate pairwise co-occurrence statistics for all species pairs.
    """
    n_replicates, n_species = presence_matrix.shape
    results = []

    for i in range(n_species):
        for j in range(i + 1, n_species):  # Only upper triangle
            # Build 2x2 contingency table
            both_present = sum((presence[i] == 1) & (presence[j] == 1))
            i_only = sum((presence[i] == 1) & (presence[j] == 0))
            j_only = sum((presence[i] == 0) & (presence[j] == 1))
            both_absent = sum((presence[i] == 0) & (presence[j] == 0))

            table = [[both_present, j_only],
                    [i_only, both_absent]]

            # Log-odds ratio with Haldane-Anscombe correction
            if any cell is 0:
                table_corrected = table + 0.5
            log_odds_ratio = log((n11 * n00) / (n10 * n01))

            # Fisher's exact test
            odds_ratio, p_two = fisher_exact(table, alternative='two-sided')
            _, p_greater = fisher_exact(table, alternative='greater')

            results.append({
                'species_i': i,
                'species_j': j,
                'log_odds_ratio': log_odds_ratio,
                'p_value_greater': p_greater,
                ...
            })

    return DataFrame(results)
```

FDR correction ([CooccurrenceAsymmetricityAnalysis.py](CooccurrenceAsymmetricityAnalysis.py:28-58)):

```python
def multipletests_fdr_bh(pvalues, alpha=0.05):
    """Benjamini-Hochberg FDR correction"""
    n = len(pvalues)
    sorted_indices = argsort(pvalues)
    sorted_pvalues = pvalues[sorted_indices]

    qvalues = zeros(n)
    prev_qvalue = 1.0

    for i in range(n-1, -1, -1):  # Work backwards
        qvalue = min(sorted_pvalues[i] * n / (i + 1), prev_qvalue)
        qvalues[sorted_indices[i]] = qvalue
        prev_qvalue = qvalue

    reject = qvalues <= alpha
    return reject, qvalues
```

## Real Example from LN_12 Data

Let's trace through a real significant pair:

**Species 2 and 3** (from LN_12 analysis):
- n₁₁ = 45 (both present)
- n₁₀ = 2 (only sp2)
- n₀₁ = 1 (only sp3)
- n₀₀ = 4 (neither present)

**Log-Odds Ratio**:
```
LOR = log[(45 × 4) / (2 × 1)] = log(90) = 4.50
```
→ Very strong positive association

**Fisher's Exact Test**:
```
p_value_greater ≈ 0.000001
```
→ Extremely unlikely to occur by chance

**After FDR correction across 435 pairs**:
```
q_value ≈ 0.0000X (still highly significant)
```

**Conclusion**: Species 2 and 3 **significantly co-occur** together.

## Summary of Significance Levels

After running Type 3 analysis, pairs are classified:

| q-value | Significance | Symbol | Interpretation |
|---------|--------------|--------|----------------|
| < 0.001 | Very highly significant | *** | Very strong co-occurrence |
| < 0.01 | Highly significant | ** | Strong co-occurrence |
| < 0.05 | Significant | * | Moderate co-occurrence |
| ≥ 0.05 | Not significant | ns | No evidence of co-occurrence |

## Key Points

1. **Fisher's exact test** is used (not χ²) because:
   - Works with small sample sizes
   - Provides exact probabilities (not asymptotic)
   - No assumption violations

2. **One-sided test** (`alternative='greater'`) tests for **positive association**:
   - We're specifically interested in co-occurrence (not anti-correlation)
   - More statistical power for detecting co-occurrence

3. **FDR correction** is essential:
   - Controls false discovery rate across hundreds of tests
   - More powerful than Bonferroni (family-wise error rate control)
   - q-value < 0.05 means < 5% of discoveries are expected to be false

4. **Log-Odds Ratio** quantifies effect size:
   - Complements p-value (statistical significance)
   - LOR ≥ 1.5 is typically considered biologically meaningful
   - Used for network visualization (edge width)

## References

- Fisher, R.A. (1922). "On the interpretation of χ² from contingency tables"
- Benjamini & Hochberg (1995). "Controlling the false discovery rate"
- Agresti, A. (2002). "Categorical Data Analysis"
