# Type 3 Co-occurrence Asymmetricity Analysis

## Overview

Type 3 asymmetricity analysis quantifies whether **paired species co-occurrence** in coalesced communities is biased toward **same-origin pairs** (both from Parent A or both from Parent B) compared to **mixed-origin pairs** (one from each parent).

## Key Question

**Are co-occurring species pairs in the coalesced community C enriched for same-origin (A–A or B–B) vs mixed-origin (A–B) pairs, beyond what we would expect from marginal invasion success alone?**

## Conceptual Framework

### The Problem with Simple Diversity Metrics (Type 1 & 2)

Type 1 and Type 2 diversity asymmetricity measure:
- **Type 1**: Count differences of unique species retained from each parent
- **Type 2**: Count differences of all species (including overlaps)

**Limitation**: These metrics ignore **which species co-occur together**. They treat all species as independent, but ecological communities have structure.

### Type 3 Solution: Pairwise Co-occurrence Analysis

Type 3 asks: "Do species from the same parent **preferentially co-occur** together in offspring communities?"

This reveals:
1. **Competitive hierarchies** within parent communities
2. **Facilitative interactions** between species
3. **Community assembly constraints** beyond simple retention rates

## Statistical Methodology

### 1. Build 2×2 Contingency Tables

For every pair of species (i, j) across R replicates:

```
                Species j Present    Species j Absent
Species i Present      n₁₁               n₁₀
Species i Absent       n₀₁               n₀₀
```

### 2. Calculate Log-Odds Ratio

```
LOR = log[(n₁₁ × n₀₀) / (n₁₀ × n₀₁)]
```

With Haldane-Anscombe correction (+0.5 to all cells if any is 0)

**Interpretation**:
- LOR > 0: Species co-occur more than expected (positive association)
- LOR < 0: Species co-occur less than expected (negative association)
- LOR ≈ 0: Co-occurrence matches independence

### 3. Fisher's Exact Test

For each pair, test:
- **Two-sided**: Is co-occurrence different from independence?
- **One-sided (greater)**: Is co-occurrence greater than independence?

### 4. FDR Correction

Apply Benjamini-Hochberg FDR correction across all pairs to control false discovery rate.

### 5. Enrichment Analysis

Compare same-origin vs mixed-origin pairs:

**Fisher's Exact Test** on 2×2 table:

```
                  Significant    Not Significant
Same-Origin         n_AA+BB         N_AA+BB - n_AA+BB
Mixed-Origin        n_AB            N_AB - n_AB
```

**Enrichment Ratio** = (n_same_sig / N_same) / (n_mixed_sig / N_mixed)

## Formulas

### Diversity Asymmetricity (for comparison)

**Type 1** (Excluding overlaps):
```
A₁ = |spp_from_p1_only - spp_from_p2_only| / (spp_from_p1_only + spp_from_p2_only)
```

**Type 2** (Including overlaps):
```
A₂ = |(spp_from_p1_only + overlap) - (spp_from_p2_only + overlap)| / (spp_from_p1_only + spp_from_p2_only + overlap)
```

### Type 3 Co-occurrence Asymmetricity

**Enrichment Metric**:
```
E = (# same-origin pairs significant) / (# same-origin pairs total)
    ÷ (# mixed-origin pairs significant) / (# mixed-origin pairs total)
```

**Statistical Test**:
- **Null Hypothesis**: Same-origin and mixed-origin pairs have equal co-occurrence rates
- **Alternative**: Same-origin pairs are enriched for co-occurrence
- **Test**: Fisher's exact test (one-sided, greater)

## Implementation

### Main Module: `CooccurrenceAsymmetricityAnalysis.py`

**Key Functions**:

1. `analyze_type3_asymmetricity()`: Main analysis function
   - Input: Lists of offspring, parent1, parent2 abundance vectors
   - Output: Co-occurrence statistics and enrichment metrics

2. `calculate_pairwise_cooccurrence()`: Build contingency tables for all pairs
   - Computes log-odds ratios
   - Runs Fisher's exact tests
   - Labels pairs as same-origin or mixed-origin

3. `apply_fdr_correction()`: Benjamini-Hochberg FDR correction

4. `calculate_enrichment_statistics()`: Compare same-origin vs mixed-origin enrichment

### Visualization Functions:

1. `plot_enrichment_barplot()`: Bar plot comparing proportion significant
2. `plot_cooccurrence_heatmap()`: Heatmap of log-odds ratios
3. `plot_cooccurrence_network()`: Network diagram of significant pairs

### Analysis Script: `run_type3_cooccurrence_analysis.py`

Runs Type 3 analysis for all nutrient conditions and species pools.

**Usage**:
```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code
python run_type3_cooccurrence_analysis.py
```

## Results Summary

### Significant Enrichment Detected:

| Condition | Enrichment Ratio | p-value | Interpretation |
|-----------|-----------------|---------|----------------|
| **LN_12** | **7.77×** | **9.8e-07 (\*\*\*)** | Same-origin pairs 7.77× more likely to co-occur |
| **MN_12** | **3.34×** | **1.6e-05 (\*\*\*)** | Same-origin pairs 3.34× more likely to co-occur |
| **HN_6**  | **∞** | **0.034 (\*)** | Only same-origin pairs co-occur significantly |

### No Significant Enrichment:

| Condition | Enrichment Ratio | p-value | Interpretation |
|-----------|-----------------|---------|----------------|
| LN_6 | 2.92× | 0.067 (ns) | Marginally non-significant |
| MN_6 | 1.89× | 0.059 (ns) | Marginally non-significant |
| HN_12 | 0.90× | 0.703 (ns) | No enrichment |
| LN_24, MN_24, HN_24 | N/A | 1.000 (ns) | No significant pairs found |

## Key Findings

### 1. **Nutrient-Dependent Community Structure**

- **Low Nutrient (LN) - 12 species**: Strongest enrichment (7.77×)
  - Species from same parent strongly co-occur
  - Suggests parent community structure is preserved

- **Medium Nutrient (MN) - 12 species**: Moderate enrichment (3.34×)
  - Still significant but weaker than LN

- **High Nutrient (HN)**: Mixed results
  - HN_6: Infinite enrichment (only same-origin pairs significant)
  - HN_12: No enrichment (balanced co-occurrence)

### 2. **Species Pool Size Effects**

- **12-species pools**: Show strongest, most consistent enrichment
- **6-species pools**: Variable results (some enrichment, some not)
- **24-species pools**: No significant co-occurrence detected
  - Likely due to smaller sample sizes (n=12 replicates)

### 3. **Biological Interpretation**

**Same-origin enrichment suggests**:
1. **Community-level selection**: Parent communities maintain internal structure
2. **Facilitative networks**: Species from same community support each other
3. **Competitive exclusion**: Mixed communities undergo competitive reorganization
4. **Pre-adapted consortia**: Species pre-adapted to coexist persist together

**Negative log-odds for mixed-origin pairs** (e.g., LN_12: -0.64):
- Species from different parents **avoid** co-occurring
- Suggests competitive exclusion between communities
- Parent identity matters for assembly outcomes

## Output Files

Results saved to: `Figure/AsymmetricityNullModelAnalysis/cooccurrence_analysis/`

### For each condition (e.g., LN_12):

1. **enrichment_LN_12.png**: Bar plots showing enrichment
2. **heatmap_all_LN_12.png**: Heatmap of all co-occurrence LORs
3. **heatmap_significant_LN_12.png**: Heatmap of significant pairs only
4. **network_LN_12.png**: Network diagram of top co-occurring pairs
5. **cooccurrence_table_LN_12.csv**: Full statistical results table

### Summary file:

- **type3_summary.csv**: Comparison across all conditions

## Comparison: Type 1, 2, vs 3

| Metric | What it Measures | Units | Biological Interpretation |
|--------|-----------------|-------|--------------------------|
| **Type 1** | Species count asymmetry (unique only) | [0, 1] | Dominance of unique species retention |
| **Type 2** | Species count asymmetry (all species) | [0, 1] | Overall parent contribution asymmetry |
| **Type 3** | Paired co-occurrence enrichment | Ratio | Community structure preservation |

**Key Differences**:

- **Type 1 & 2**: Univariate (count species independently)
- **Type 3**: Bivariate (analyze species pairs)

**Type 3 reveals**:
- **Which species co-occur** (not just which survive)
- **Community assembly rules** beyond retention rates
- **Interaction networks** within parent communities

## Code Example

```python
from CooccurrenceAsymmetricityAnalysis import (
    analyze_type3_asymmetricity,
    print_type3_summary,
    plot_enrichment_barplot
)

# Run analysis
results = analyze_type3_asymmetricity(
    offspring_list,    # List of offspring abundance vectors
    parent1_list,      # List of parent1 abundance vectors
    parent2_list,      # List of parent2 abundance vectors
    threshold=1e-4,    # Presence/absence threshold
    alpha=0.05,        # FDR significance level
    min_occurrences=3  # Minimum occurrences to test a pair
)

# Print summary
print_type3_summary(results)

# Plot enrichment
plot_enrichment_barplot(
    results['enrichment_stats'],
    save_path='enrichment_plot.png'
)

# Access results
cooccurrence_df = results['cooccurrence_df']
enrichment_stats = results['enrichment_stats']
species_origins = results['species_origins']
```

## References

### Statistical Methods

- **Fisher's Exact Test**: Fisher, R.A. (1922). "On the interpretation of χ² from contingency tables, and the calculation of P". Journal of the Royal Statistical Society.

- **Benjamini-Hochberg FDR**: Benjamini, Y., & Hochberg, Y. (1995). "Controlling the false discovery rate: a practical and powerful approach to multiple testing". Journal of the Royal Statistical Society, Series B.

- **Log-Odds Ratio**: Agresti, A. (2002). "Categorical Data Analysis". Wiley.

### Ecological Context

- **Community Assembly**: HilleRisLambers, J., et al. (2012). "Rethinking community assembly through the lens of coexistence theory". Annual Review of Ecology, Evolution, and Systematics.

- **Priority Effects**: Fukami, T. (2015). "Historical contingency in community assembly". Annual Review of Ecology, Evolution, and Systematics.

## Author

Gore Lab Coalescence Analysis Team
November 2025

## Files

- `CooccurrenceAsymmetricityAnalysis.py`: Core analysis module (560 lines)
- `run_type3_cooccurrence_analysis.py`: Analysis script for real data
- `TYPE3_COOCCURRENCE_ANALYSIS_README.md`: This documentation
