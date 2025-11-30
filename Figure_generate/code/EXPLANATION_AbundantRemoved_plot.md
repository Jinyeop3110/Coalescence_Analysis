# Complete Explanation: How Fig_MostAbundant_Correlation_M_H_Combined_AbundantRemoved.svg is Generated

## Step-by-Step Process:

### 1. **Load Pairwise Experimental Data** (lines 574-584)
   - Loads colony counting data from Excel file
   - Processes pairwise ratios: `data_p_ratio[i,j]` = fraction of species i when paired with species j
   - This gives species-level dominance from PAIRWISE experiments

### 2. **For Each Medium (M and H)** (line 583)
   Loop through both MN and HN media separately

### 3. **For Each Pool Size (6, 12, 24)** (line 592)
   Loop through different species pool sizes

### 4. **For Each Coalescence Event** (line 604)
   Process individual coalescence events (c1 + c2 → c_mix)

### 5. **IDENTIFY Most Abundant Species** (lines 611-617)
   ```python
   C1_idx = np.argmax(c_1)  # Most abundant in parent community 1
   C2_idx = np.argmax(c_2)  # Most abundant in parent community 2

   # Store for later (x-axis calculation)
   C1 = C1_idx
   C2 = C2_idx
   ```

   **Example:**
   - c1: [0.5, 0.2, 0.15, ...] → C1_idx = 0 (species 0 is most abundant)
   - c2: [0.1, 0.6, 0.1, ...]  → C2_idx = 1 (species 1 is most abundant)

### 6. **REMOVE Both Most Abundant Species** (lines 619-638)
   ```python
   # Remove BOTH C1_idx and C2_idx from ALL THREE communities
   c_1_removed[C1_idx] = 0
   c_1_removed[C2_idx] = 0  # Remove both!
   c_2_removed[C1_idx] = 0
   c_2_removed[C2_idx] = 0
   c_mix_removed[C1_idx] = 0
   c_mix_removed[C2_idx] = 0

   # Renormalize each to sum to 1
   ```

   **Example (continuing):**
   - Original c1: [0.5, 0.2, 0.15, 0.1, 0.05]
   - After removal: [0, 0, 0.15, 0.1, 0.05] (removed sp0 and sp1)
   - After renorm: [0, 0, 0.5, 0.33, 0.17] (renormalized to sum=1)

### 7. **Calculate Y-axis: Subdominant Community Dominance** (lines 644-657)
   ```python
   # Vector decomposition on MODIFIED communities (without dominant species)
   u, v, k = metric_VectorDecomposition_onlyPositive(c_1_removed, c_2_removed, c_mix_removed)

   # Y-axis = arctan(u/v) normalized
   vector_similarity_score = np.arctan(u / (v + 1e-8)) / (np.pi / 2)
   ```

   **Y-axis represents:**
   - Among SUBDOMINANT species only, which parent community does c_mix resemble?
   - y ≈ 1: c_mix subdominants look like c1 subdominants
   - y ≈ 0: c_mix subdominants look like c2 subdominants
   - y ≈ 0.5: subdominants are a 50-50 mix

### 8. **Apply Mixing Filter** (lines 660-663)
   ```python
   mixing_strength = u**2 + v**2
   if mixing_strength <= 0.5:
       continue
   ```

   **Filters out ~70% of data!**
   - Only keeps events where subdominants show mixing (not restructuring)

### 9. **Calculate X-axis: ORIGINAL Dominant Species Pairwise Outcome** (lines 671-680)
   ```python
   # Check if C1 and C2 are in pairwise data (must be < 12)
   if C1 >= 12 or C2 >= 12:
       continue

   # Use ORIGINAL dominant species (C1, C2) for x-axis
   # NOT the removed communities!
   data_abspecies.append(np.mean([1-data_p_ratio[C1,C2], data_p_ratio[C2,C1]]))
   ```

   **X-axis represents:**
   - Pairwise dominance of the REMOVED dominant species
   - From colony counting experiments (not from the coalescence)
   - x ≈ 1: In pairwise culture, species C1 dominates species C2
   - x ≈ 0: In pairwise culture, species C2 dominates species C1

### 10. **Apply Arctan Normalization** (lines 682-690)
   ```python
   x_raw = 1 - np.array(data_abspecies)
   ratio = x_raw / (1 - x_raw + 1e-8)
   x = np.arctan(ratio) / (np.pi / 2)
   ```

### 11. **Duplicate Data Points** (lines 695-699)
   ```python
   x = np.concatenate((x, 1-x))
   y = np.concatenate((y, 1-y))
   ```

   Reflects data across diagonal (symmetry)

### 12. **Plot M and H Separately** (lines 717-753)
   - Separate colors for MN vs HN
   - Separate regression lines
   - Separate R² values
   - Combined heatmap background

## KEY INSIGHT: What This Plot Tests

**The plot asks:**
> "If I know which dominant species wins in pairwise culture (x-axis),
> can I predict which parent community's SUBDOMINANT species will dominate
> in the coalesced community (y-axis)?"

**In other words:**
- X-axis: "In a fight between sp0 and sp1, sp0 wins" (from pairwise experiment)
- Y-axis: "After removing sp0 and sp1, do the remaining species from c1 or c2 dominate?"

**This tests whether:**
1. **Top-down control cascades down the hierarchy** - if dominant species A beats B, do A's subdominants also beat B's subdominants?
2. **Or subdominants have independent dynamics** - dominant species outcomes don't predict subdominant outcomes

## CRITICAL BUG NOTICED:

**Lines 678-680 have incorrect indentation!**

```python
675:                if data_p_ratio[C1, C2] == None:
676:                    continue
677:
678:                    data_label.append(ii)  # WRONG INDENTATION!
679:                    data_community.append(vector_similarity_score)
680:                    data_abspecies.append(np.mean([1-data_p_ratio[C1,C2], data_p_ratio[C2,C1]]))
```

These lines are indented under the `if data_p_ratio[C1, C2] == None: continue` block,
which means **they never execute**! They should be dedented to the same level as the `if` statement.

This means **the plot currently has NO DATA POINTS** because data is never appended!

Actually wait - let me check if there's an `else:` that I'm missing...
