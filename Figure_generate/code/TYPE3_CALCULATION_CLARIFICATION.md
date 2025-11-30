# Type 3 Co-occurrence Analysis - What Gets Calculated

## Common Misunderstanding

**WRONG**: Calculate log-odds ratio for each coalescence event individually ❌

**CORRECT**: Calculate ONE log-odds ratio per species pair across ALL coalescence replicates ✓

## Step-by-Step Example

### Setup

**Condition**: LN_12 (Low Nutrient, 12 species pool)
**Number of replicates**: 52 coalescence experiments
**Total species in dataset**: 130 species

### What We Actually Do

For **every possible pair** of species (i, j):

1. Look across **all 52 replicates**
2. Count in how many replicates:
   - Both species present
   - Only species i present
   - Only species j present
   - Neither present
3. Build ONE contingency table
4. Calculate ONE log-odds ratio
5. Calculate ONE p-value

### Concrete Example: Species 2 and Species 3

#### Step 1: Check Presence/Absence Across Replicates

```
Replicate #1:   offspring = [0.05, 0.10, 0.08, ...]
                → Species 2 present? YES (abundance = 0.10 > threshold)
                → Species 3 present? YES (abundance = 0.08 > threshold)
                → Category: BOTH PRESENT

Replicate #2:   offspring = [0.12, 0.15, 0.00, ...]
                → Species 2 present? YES (0.15)
                → Species 3 present? NO (0.00)
                → Category: ONLY SPECIES 2

Replicate #3:   offspring = [0.00, 0.00, 0.20, ...]
                → Species 2 present? NO
                → Species 3 present? YES (0.20)
                → Category: ONLY SPECIES 3

...continue for all 52 replicates...

Replicate #52:  offspring = [0.08, 0.12, 0.09, ...]
                → Species 2 present? YES
                → Species 3 present? YES
                → Category: BOTH PRESENT
```

#### Step 2: Tally Results Across All 52 Replicates

```
Both Species 2 and 3 present:    45 replicates
Only Species 2 present:           2 replicates
Only Species 3 present:           1 replicate
Neither present:                  4 replicates
                                 ───
Total:                           52 replicates
```

#### Step 3: Build ONE 2×2 Contingency Table

```
                    Species 3 Present    Species 3 Absent    Total
Species 2 Present         45                   2              47
Species 2 Absent           1                   4               5
Total                     46                   6              52
```

#### Step 4: Calculate ONE Log-Odds Ratio

```
LOR = log[(n₁₁ × n₀₀) / (n₁₀ × n₀₁)]
    = log[(45 × 4) / (2 × 1)]
    = log[180 / 2]
    = log[90]
    = 4.50
```

**Interpretation**: Species 2 and 3 have a **very strong positive association** (LOR = 4.50)

#### Step 5: Fisher's Exact Test

```python
from scipy.stats import fisher_exact

table = [[45, 2],
         [1, 4]]

odds_ratio, p_value = fisher_exact(table, alternative='greater')

# Results:
# odds_ratio = 90.0
# p_value ≈ 0.00001  (very small!)
```

**Interpretation**: The probability of seeing this strong co-occurrence by chance is **< 0.00001** - highly significant!

#### Step 6: After FDR Correction

After correcting for testing 435 pairs in LN_12:

```
q_value ≈ 0.0001  (still highly significant after correction)
```

**Final Result**: Species 2 and 3 **significantly co-occur** (***) in LN_12 condition.

---

## What We Do For EVERY Pair

For **LN_12** with 130 species:
- Total possible pairs = 130 × 129 / 2 = **8,415 pairs**
- But only pairs that appear in enough replicates are tested
- In LN_12: **435 pairs** tested (those appearing in ≥ 5 replicates)

**For each of these 435 pairs**:
- Build ONE contingency table across 52 replicates
- Calculate ONE log-odds ratio
- Calculate ONE p-value
- After FDR correction → ONE q-value

---

## Summary Table Format

The output table `cooccurrence_table_LN_12.csv` has this structure:

| species_i | species_j | n11_both | n10_i_only | n01_j_only | n00_neither | log_odds_ratio | p_value | q_value | significant |
|-----------|-----------|----------|------------|------------|-------------|----------------|---------|---------|-------------|
| 2         | 3         | 45       | 2          | 1          | 4           | 4.50           | 0.00001 | 0.0001  | TRUE        |
| 5         | 8         | 25       | 10         | 5          | 12          | 1.79           | 0.0023  | 0.015   | TRUE        |
| 10        | 15        | 8        | 12         | 15         | 17          | -0.35          | 0.82    | 0.95    | FALSE       |
| ...       | ...       | ...      | ...        | ...        | ...         | ...            | ...     | ...     | ...         |

**Each row = one species pair**
**Values in each row = aggregated across all 52 replicates**

---

## Visual Representation

```
                    52 Coalescence Replicates
                    ↓
    ┌─────────────────────────────────────────────────┐
    │  Rep1   Rep2   Rep3  ...  Rep51   Rep52         │
    │   ●●     ●○     ○●        ●●      ●●           │ ← Species 2 & 3
    │   ●○     ○○     ●●        ○●      ●○           │ ← Species 5 & 8
    │   ○○     ●●     ○○        ○○      ●●           │ ← Species 10 & 15
    │   ...    ...    ...       ...     ...          │
    └─────────────────────────────────────────────────┘
                    ↓
            Count occurrences for each pair
                    ↓
    ┌──────────────────────────────────────┐
    │ Species 2 & 3:                      │
    │   Both present (●●): 45 times       │
    │   Only 2 (●○): 2 times              │
    │   Only 3 (○●): 1 time               │
    │   Neither (○○): 4 times             │
    │   → LOR = 4.50, p < 0.00001         │
    └──────────────────────────────────────┘
```

---

## Why This Matters

**This is fundamentally different from:**

1. **Type 1/2 Diversity Asymmetricity**:
   - Calculated **per coalescence event**
   - Then averaged or compared across events
   - Asks: "For this specific coalescence, which parent contributed more species?"

2. **Type 3 Co-occurrence Asymmetricity**:
   - Calculated **per species pair across ALL events**
   - Asks: "Across all coalescence experiments, do these two species tend to co-occur?"
   - Statistical power comes from **multiple replicates**

---

## Analogy

Think of it like a **clinical trial**:

**Type 1/2** is like asking:
- "Did this patient get better?" (yes/no for each patient)
- Then: "What % of patients got better?"

**Type 3** is like asking:
- "Do patients who take Drug A also tend to have Symptom B?"
- You look at ALL patients together to find the association
- One p-value for the Drug A ↔ Symptom B relationship

Similarly, Type 3 asks:
- "Do Species 2 and Species 3 co-occur together?"
- You look at ALL coalescence replicates together
- One p-value for the Species 2 ↔ Species 3 relationship

---

## In Code

From `CooccurrenceAsymmetricityAnalysis.py`:

```python
def calculate_pairwise_cooccurrence(presence_matrix, species_origins, min_occurrences=3):
    """
    Args:
        presence_matrix: Binary matrix of shape (R replicates × S species)
                        Each row = one coalescence experiment
                        Each column = one species (0 = absent, 1 = present)

    Returns:
        DataFrame with ONE ROW per species pair
    """
    n_replicates, n_species = presence_matrix.shape  # e.g., (52, 130)

    results = []

    for i in range(n_species):
        for j in range(i + 1, n_species):

            # Count across ALL replicates (aggregation happens here!)
            both_present = np.sum((presence_matrix[:, i] == 1) &
                                  (presence_matrix[:, j] == 1))  # Sum over all rows
            i_only = np.sum((presence_matrix[:, i] == 1) &
                           (presence_matrix[:, j] == 0))
            j_only = np.sum((presence_matrix[:, i] == 0) &
                           (presence_matrix[:, j] == 1))
            both_absent = np.sum((presence_matrix[:, i] == 0) &
                                (presence_matrix[:, j] == 0))

            # Build ONE table for this pair
            table = [[both_present, j_only],
                    [i_only, both_absent]]

            # Calculate ONE log-odds ratio
            log_odds_ratio = np.log((both_present * both_absent) /
                                   (i_only * j_only + 0.5))

            # Calculate ONE p-value
            _, p_value = fisher_exact(table, alternative='greater')

            # Store ONE result for this pair
            results.append({
                'species_i': i,
                'species_j': j,
                'n11_both_present': both_present,  # Aggregated count
                'n10_i_only': i_only,              # Aggregated count
                'n01_j_only': j_only,              # Aggregated count
                'n00_both_absent': both_absent,    # Aggregated count
                'log_odds_ratio': log_odds_ratio,  # One value
                'p_value_greater': p_value         # One value
            })

    return pd.DataFrame(results)  # One row per pair
```

The key line is:
```python
both_present = np.sum((presence_matrix[:, i] == 1) & (presence_matrix[:, j] == 1))
```

The `np.sum()` aggregates across **ALL replicates** (all rows) to get a **single count**.

---

## Key Takeaway

✓ **One log-odds ratio per species pair** (aggregated across all replicates)

✗ **NOT one log-odds ratio per coalescence event**

The statistical power comes from having **multiple replicates** that let us build a contingency table and test if the co-occurrence pattern is significant.
