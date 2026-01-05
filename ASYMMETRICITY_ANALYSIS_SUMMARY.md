# Asymmetricity Analysis in Coalescence Communities: Statistical Methods and Null Models

## Overview

This analysis framework quantifies asymmetricity in microbial community coalescence experiments - measuring how much offspring communities deviate from being equally similar to both parent communities. The code implements multiple asymmetricity metrics and compares experimental results against null models to test specific hypotheses about coalescence mechanisms.

## Asymmetricity Measures

### 1. Similarity-Based Asymmetricity
**Formula:** `|sim1 - sim2| / (sim1 + sim2)`

- **What it measures:** Differential similarity of offspring to each parent
- **Range:** [0, 1] where 0 = perfect symmetry, 1 = complete asymmetry
- **Interpretation:** High values indicate offspring community is much more similar to one parent than the other
- **Metrics used:** Bray-Curtis, Jensen-Shannon divergence, Jaccard, Cosine, Euclidean distance

### 2. Vector-Based Asymmetricity
**Formula:** Uses arctangent approach: `|arctan(magA/magB) - π/4| / (π/4)`

- **What it measures:** Deviation from equal contribution of parents in vector decomposition
- **Method:** Decomposes offspring as linear combination of parents: `O = α·P1 + β·P2 + residual`
- **Range:** [0, 1] where 0 = equal magnitudes (45° angle), 1 = one parent dominates
- **Interpretation:** Quantifies relative "pull" of each parent community on offspring composition

### 3. Diversity-Based Asymmetricity (Two formulations)

#### Type 1: Exclusive Species Count
**Formula:** `|species_from_P1_only - species_from_P2_only| / (species_from_P1_only + species_from_P2_only)`

- **What it measures:** Asymmetry in retention of parent-specific species (excluding overlaps)
- **Focus:** Species unique to each parent that survive in offspring
- **Interpretation:** Which parent's unique species are preferentially retained

#### Type 2: Inclusive Species Count  
**Formula:** `|species_from_P1_total - species_from_P2_total| / (species_from_P1_total + species_from_P2_total)`

- **What it measures:** Total species contribution from each parent (overlaps counted for both)
- **Focus:** Overall species retention patterns including shared species
- **Interpretation:** Total species "heritage" from each parent

## Null Models

### 1. Neutral Mixing Model
**Hypothesis:** Asymmetricity arises from random neutral mixing without ecological interactions

**Implementation:**
- Offspring = α × Parent1 + (1-α) × Parent2
- α randomly sampled from uniform distribution [0, 1]
- Tests whether observed asymmetricity exceeds neutral expectation

**Relevant for:** Similarity and vector-based asymmetricity

### 2. Random Selection Models (Two Versions)

**Hypothesis:** Species retention is a stochastic process with empirically-derived probabilities

#### Version 1: Excluding Overlaps
- Uses retention probabilities calculated from unique species only
- Empirical probabilities by condition:
  - LN: 0.61-0.66
  - MN: 0.37-0.66  
  - HN: 0.39-0.61
- **Paired with:** Diversity asymmetricity Type 1

#### Version 2: Including Overlaps
- Uses retention probabilities calculated including shared species
- Empirical probabilities by condition:
  - LN: 0.70-0.76
  - MN: 0.54-0.90
  - HN: 0.55-0.90
- **Paired with:** Diversity asymmetricity Type 2

**Implementation:**
- Each species has binomial probability of retention based on empirical rates
- Selected species receive random exponential abundances
- Tests whether observed diversity asymmetricity differs from random selection

## Statistical Testing

### Methods Used:
1. **Mann-Whitney U test:** Non-parametric comparison between experimental and null distributions
2. **Kruskal-Wallis test:** Comparing asymmetricity across nutrient conditions (LN, MN, HN)
3. **Effect size:** Mean difference between experimental and null model

### Significance Interpretation:
- If experimental > null model: Deterministic factors enhance asymmetricity
- If experimental ≈ null model: Asymmetricity explained by neutral/random processes
- If experimental < null model: Stabilizing mechanisms reduce asymmetricity

## Key Scientific Insights

1. **Neutral vs. Non-neutral Dynamics:** Deviation from neutral mixing indicates ecological interactions, priority effects, or environmental filtering

2. **Species-Specific vs. Community-Level Effects:** Different asymmetricity types reveal different scales of coalescence mechanisms

3. **Nutrient Dependency:** Variation across LN/MN/HN conditions suggests resource availability modulates coalescence outcomes

4. **Empirical Retention Probabilities:** Species retention rates vary systematically with nutrient conditions, suggesting environment-dependent filtering

## Analysis Workflow

1. **Data Loading:** Extract community abundance vectors from experimental coalescence events
2. **Asymmetricity Calculation:** Compute all metrics for each coalescence event
3. **Null Model Generation:** Create 1000 permutations for each null model
4. **Statistical Comparison:** Test experimental vs. null distributions
5. **Visualization:** Box plots with significance annotations grouped by condition and species pool size

## Interpretation Guidelines

- **High similarity/vector asymmetricity + significant deviation from neutral mixing:** Strong priority effects or competitive exclusion
- **High diversity asymmetricity + deviation from random selection:** Selective species filtering or facilitation
- **Asymmetricity matching null models:** Neutral assembly processes dominate
- **Lower asymmetricity than null models:** Stabilizing mechanisms promoting coexistence

## Implementation Notes

- Threshold of 1e-3 or 1e-4 applied to filter rare species
- All abundance vectors normalized to sum to 1
- Analysis restricted to synthetic coalescence events for controlled species pools
- Species pool sizes: 6, 12, or 24 species depending on experimental design