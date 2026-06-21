# Supplementary Figure Review Report

## Executive Summary

This report identifies issues with text size, text consistency, and style consistency across the 34 supplementary figures compared to the 6 main figures. The analysis covers axis labels, legends, annotations, and overall visual style.

---

## 1. Text Size Issues

### 1.1 Figures with Text That May Be Too Small

| Figure | Issue | Specific Element |
|--------|-------|------------------|
| **Fig. S1** (Taxonomy color map) | Text is dense but readable | ASV labels and taxonomic classifications are small (~6-7pt effective when printed at full page width) |
| **Fig. S2** (Phylogenetic tree) | Small tip labels | ASV names and genus labels on tree tips appear ~6-7pt; may be difficult to read when scaled to 0.9\textwidth |
| **Fig. S6-S9** (Phase diagrams) | **Missing x-axis label** | The phase diagram subfigures (0.48\textwidth or 0.19\textwidth) lack visible x-axis labels for "Interaction Strength" or similar |
| **Fig. S9** (Species ablation) | Very small phase diagrams | At 0.19\textwidth (5 panels), axis labels and tick marks will be extremely small |
| **Fig. S11-S13** (Pairwise invasion matrices) | Small cell labels | The "0", "1", "T" tick labels within each matrix cell are very small (~5-6pt) |
| **Fig. S14** (Correlation barplots) | Acceptable but borderline | Y-axis labels and legend text appear adequate |
| **Fig. S16** (ASV vs pH combined) | Small subplot titles | With 8 panels, individual panel titles (e.g., "ASV 9 Base") are small |
| **Fig. S21-S23** (Coalescence matrices with pie charts) | **Very small labels** | Community labels (e.g., "P8-49", "P8-57") above pie charts are very small; difficult to read at 0.8\textwidth with 9 pies per row |
| **Fig. S24** (Time series Nutr-) | No axis labels visible | The stacked bar time series has no visible axis labels or tick marks |
| **Fig. S25** (Time series Nutr+) | No axis labels visible | Same as S24 |

### 1.2 Recommended Minimum Font Sizes

Based on main figure standards (which use ~8-10pt base font):
- **Axis labels**: Minimum 8pt
- **Tick labels**: Minimum 7pt
- **Legend text**: Minimum 7pt
- **Panel titles**: Minimum 9pt
- **Annotations (r, p values)**: Minimum 7pt

---

## 2. Text Inconsistencies

### 2.1 Terminology Inconsistencies

| Issue | Occurrences | Recommendation |
|-------|-------------|----------------|
| **"Nutr-" vs "Nutr−" vs "LN"** | S4 uses "Nutr-", S11 uses "Nutr−", S14 uses both "Nutr$-$" and "LN" in filename | Standardize to "Nutr−" (with proper minus sign) throughout |
| **"CLS" labeling** | Most figures use "CLS" but some use full "Community-Level Selection" | Use "CLS" consistently with definition in first reference |
| **"Mixing" vs "Mixture" vs "M"** | S4 uses "Mixing", S25/S27/S28 use "Mixing", main figures use "M" in legends | Standardize: use "M" in compact legends, "Mixture" in text |
| **Greek mu (μ) formatting** | Some figures show "μ=0.6", others show "µ=0.6" (different unicode) | Use consistent LaTeX $\mu$ throughout |
| **"rel.density" vs "Rel. density"** | Main Fig 2B shows "rel.density", main Fig 3 shows same | Keep lowercase as in main figures |

### 2.2 Axis Label Inconsistencies

| Axis Label | Variations Found |
|------------|------------------|
| Y-axis for abundance | "Relative Abundance" (S18-20), "Community pH" (S16), "Fraction" (S6-8) |
| X-axis for interaction | "Interaction Strength" (S10), "μ" only (S6-9), missing entirely (some phase diagrams) |
| Similarity axes | "Similarity(C,A)" / "Similarity(C,B)" - consistent |
| Correlation | "Pairwise Selection Correlation" (S10, S14) - consistent |

### 2.3 Caption Text vs Figure Text Mismatches

| Figure | Issue |
|--------|-------|
| S6-S8 | Caption mentions "mean interaction strength μ" but figures only show axis as unlabeled or "μ" |
| S15 | Caption says "acidifier vs alkalizer" but figure shows "Acidifiers" and "Alkalizers" |

---

## 3. Style Inconsistencies with Main Figures

### 3.1 Color Scheme Comparison

**Main Figures Color Standards:**
- CLS: Coral/salmon red (#E57373 or similar)
- Mixture/M: Light green (#81C784)
- Restructuring/R: Light purple (#BA68C8)
- Nutr-: Magenta-pink (#A7216A)
- Base: Brown-red (#802000)
- Nutr+: Orange-red (#E24912)

**Supplementary Figure Color Deviations:**

| Figure | Issue |
|--------|-------|
| S4 (Robustness stacked bar) | Colors match main figures - GOOD |
| S6-S9 (Phase diagrams) | Colors match main figures - GOOD |
| S10 (Correlation vs interaction) | Red/blue scheme matches main Fig 2D - GOOD |
| S14 (Correlation barplots) | Red/blue scheme consistent - GOOD |
| S18-S20 (Rank abundance) | Brown/maroon lines - differs from main figure color palette but acceptable for different data type |
| S21-S23 (Pie chart matrices) | Use taxonomy colormap - consistent with S1 |
| S25, S27, S28 (Stacked bars) | Colors match main CLS/M/R scheme - GOOD |
| S30 (Overlap histogram) | Different colors per condition (magenta/brown/orange) - matches Nutr condition colors - GOOD |

### 3.2 Panel Label Style

**Main Figures:**
- Use bold capital letters: **A**, **B**, **C**, **D**, **E**
- Positioned top-left of each panel
- Clean sans-serif font

**Supplementary Figures with Issues:**

| Figure | Issue |
|--------|-------|
| S3, S24, S25 (Time series) | Panel labels "Example 1", "Example 2" instead of **a**, **b**, **c** |
| S6-S8 (Phase diagrams) | Use "(A)", "(B)" in caption but no visible panel labels in figure |
| S9 (Species ablation) | Mix of lowercase (a)-(e) for phase diagrams and (f) for stacked bar |
| S14 | Panel labels visible and appropriate |
| S16 | No panel labels visible in figure; relies on subplot titles |
| S18-S20, S31-S33 | Use **A**, **B** - matches main figure style - GOOD |

### 3.3 Axis and Spine Style

**Main Figures:**
- Clean axes with spines on left and bottom only
- Top and right spines removed
- Tick marks pointing inward
- Consistent line width (~0.5pt)

**Supplementary Figures with Issues:**

| Figure | Issue |
|--------|-------|
| S6-S8 (Phase diagrams) | Missing x-axis labels entirely |
| S10 | Has all 4 spines with grid - differs from main figure style |
| S11-S13 (Pairwise matrices) | Complex grid structure - acceptable for matrix format |
| S24-S25 (Time series) | No visible axes at all - just stacked bars |

### 3.4 Legend Style

**Main Figures:**
- Legends positioned in upper right or beside plot
- Clean box or no box
- Consistent font size

**Supplementary Figures:**

| Figure | Issue |
|--------|-------|
| S4 | Legend in upper right - matches |
| S10 | Legend with box, positioned well - GOOD |
| S11-S13 | Comprehensive legend on right side - GOOD |
| S25, S27, S28 | Legend at top - GOOD |
| S6-S9 | **No legend for colors** - relies on reader knowledge of CLS/M/R colors |

### 3.5 Statistical Annotation Style

**Main Figures:**
- Use "***" for significance
- Show R² values cleanly
- Error bars with SEM

**Supplementary Figures:**

| Figure | Annotation Style | Consistent? |
|--------|-----------------|-------------|
| S5 | "***" significance bars | Yes |
| S10 | No significance shown (shows trend) | N/A |
| S14 | "***" significance | Yes |
| S16 | "r = X, p = Y" format | Yes, matches S-style |
| S18-20, S31-33 | Gini ± SD format | Consistent within group |

---

## 4. Priority Issues to Address

### HIGH PRIORITY (Readability concerns)

1. **Fig. S9**: Phase diagrams at 0.19\textwidth are too small; axis labels unreadable
2. **Fig. S21-S23**: Pie chart matrix labels (P8-XX) too small to read
3. **Fig. S24-S25**: Time series missing all axis labels
4. **Fig. S6-S8**: Phase diagrams missing x-axis label for interaction strength
5. **Fig. S2**: Phylogenetic tree tip labels very small when scaled

### MEDIUM PRIORITY (Consistency concerns)

1. **Panel labeling**: Standardize to **a**, **b**, **c** (lowercase bold) or **(A)**, **(B)**, **(C)** consistently
2. **Nutrient condition naming**: Standardize "Nutr−", "Base", "Nutr+" throughout (avoid "LN", "MN", "HN" in figures)
3. **Legend addition**: Add color legends to phase diagram figures (S6-S9) for CLS/Mixture/Restructuring
4. **μ symbol**: Ensure consistent unicode/LaTeX rendering

### LOW PRIORITY (Minor polish)

1. Standardize "Mixing" vs "Mixture" terminology
2. Grid lines in S10 differ from main figure style
3. Some figures use different brown shades for rank-abundance curves

---

## 5. Figure-by-Figure Summary

| Fig | Text Size | Text Consistency | Style Match | Overall |
|-----|-----------|------------------|-------------|---------|
| S1 | OK | OK | OK | PASS |
| S2 | SMALL | OK | OK | REVIEW |
| S3 | OK | Panel labels differ | OK | MINOR |
| S4 | OK | OK | OK | PASS |
| S5 | OK | OK | OK | PASS |
| S6 | SMALL | Missing x-label | No legend | REVIEW |
| S7 | SMALL | Missing x-label | No legend | REVIEW |
| S8 | SMALL | Missing x-label | No legend | REVIEW |
| S9 | **TOO SMALL** | Missing x-label | No legend | **FIX** |
| S10 | OK | OK | Grid differs | MINOR |
| S11 | SMALL cells | OK | OK | REVIEW |
| S12 | SMALL cells | OK | OK | REVIEW |
| S13 | SMALL cells | OK | OK | REVIEW |
| S14 | OK | OK | OK | PASS |
| S15 | OK | OK | OK | PASS |
| S16 | SMALL | OK | OK | REVIEW |
| S17 | OK | OK | OK | PASS |
| S18 | OK | OK | OK | PASS |
| S19 | OK | OK | OK | PASS |
| S20 | OK | OK | OK | PASS |
| S21 | **TOO SMALL** | OK | OK | **FIX** |
| S22 | **TOO SMALL** | OK | OK | **FIX** |
| S23 | **TOO SMALL** | OK | OK | **FIX** |
| S24 | **NO LABELS** | Panel labels differ | No axes | **FIX** |
| S25 | **NO LABELS** | Panel labels differ | No axes | **FIX** |
| S26 | OK | OK | OK | PASS |
| S27 | OK | OK | OK | PASS |
| S28 | OK | OK | OK | PASS |
| S29 | OK | OK | OK | PASS |
| S30 | OK | OK | OK | PASS |
| S31 | OK | OK | OK | PASS |
| S32 | OK | OK | OK | PASS |
| S33 | OK | OK | OK | PASS |
| S34 | OK | OK | OK | PASS |

---

## 6. Recommended Actions

### Immediate Fixes Required:

1. **Regenerate S9** with larger phase diagram panels or reduce to 3 panels
2. **Add x-axis labels** to S6-S8 phase diagrams ("Interaction Strength μ" or similar)
3. **Increase label sizes** in S21-S23 pie chart matrices
4. **Add axis labels** to S24-S25 time series (or add to caption that axes are intentionally minimal)
5. **Add color legends** to S6-S9 phase diagrams

### Style Standardization:

1. Audit all figures for "Nutr−" vs "Nutr-" vs "LN" and standardize
2. Standardize panel labels to match main figure convention
3. Review phylogenetic tree (S2) readability at final print size

---

*Report generated: 2026-01-15*
*Figures reviewed: 34 supplementary figures + 6 main figures*
