# Supplementary Materials Consistency Review Report

## Overview
This report identifies terminology and description inconsistencies between the main text and supplementary materials (including figure captions) in the manuscript "Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence."

---

## FIXES APPLIED

### 1. Supplementary Fig. 24 cross-reference
- **Issue:** Referenced "Supplementary Fig. 12" (Nutr- medium) but should reference Fig. 11 (Base medium)
- **Status:** FIXED - Changed to "Supplementary Fig. 11"

### 2. "One-sided selection" vs "Dominance" terminology
- **Issue:** Supplementary Note 1, Extended Data Fig. 1, and Supplementary Methods used "one-sided selection" while main text uses "Dominance"
- **Status:** FIXED - Changed to "Dominance" in:
  - Supplementary Note 1 (skewness_null_model.tex)
  - Extended Data Fig. 1 caption
  - Supplementary Methods (statistical analyses section)

### 3. Threshold confusion (0.01% vs 0.1%)
- **Issue:** Two different thresholds mentioned (0.01% for filtering, 0.1% for extinction)
- **Status:** FIXED - Removed 0.01% reference, now consistently uses 0.1% extinction threshold

### 4. SEM vs s.e.m. capitalization
- **Issue:** Extended Data Figs 1-3 used "SEM" while main text uses "s.e.m."
- **Status:** FIXED - Changed to "s.e.m." in Extended Data Figs 1, 2, and 3

### 5. "(sub)communities" terminology
- **Issue:** Term undefined in main text, used in Supplementary Figs 11-13, 23-25
- **Status:** FIXED - Changed to "Parental communities"

### 6. Supplementary Fig. 19 labels
- **Issue:** "inter-community" vs "intra-community" labels were confusing
- **Status:** FIXED - Changed to "pre-assembly species pool" vs "within-community"

### 7. Failed invasion hyphenation
- **Issue:** Supplementary Figs 6-8 used "failed-invasion frequency" (hyphenated) while main text uses "failed invasion frequency"
- **Status:** FIXED - Standardized to "failed invasion frequency" (no hyphen)

### 8. "subcommunities" in time series figures
- **Issue:** Extended Data Fig. 6 and Supplementary Figs 17-18 used "subcommunities"
- **Status:** FIXED - Changed to "parental communities"

### 9. "simulation" vs "simulations" (singular/plural)
- **Issue:** Supplementary Methods used "simulation" (singular) while main text uses "simulations" (plural)
- **Status:** FIXED - Changed to "simulations" for consistency

### 10. Time unit formatting
- **Issue:** Supplementary Fig. 9 used "15h" instead of "15~h"
- **Status:** FIXED - Changed to "15~h" with proper spacing

---

## ITEMS NOT REQUIRING CHANGES

### Extended Data Fig. 2 terminology
- **Issue noted:** Uses "Same parental community" while main text uses "within-community"
- **Decision:** OK as is - both are acceptable and clear

### OD normalization
- **Issue noted:** Mentioned in supplementary but not main Methods
- **Decision:** OK as is - appropriate level of detail for supplementary

---

## PREVIOUSLY RESOLVED (by user)

### Coalescence event count
- The supplementary methods now clarifies: "Each of the 47 coalescence pairs was performed with two biological replicates, yielding 94 total coalescence events; 11 events were excluded due to sequencing failures or contamination, resulting in 83 coalescence events for synthetic community analyses."

### Assembly effect terminology
- Changed "confirmed" to "supported" in Supplementary Note 2 (assembly_effect.tex)

---

## FILES MODIFIED

1. `latex/supplementary_sections/figures.tex`
   - Fixed Supplementary Fig. 24 cross-reference
   - Changed "(sub)communities" to "Parental communities" (6 occurrences)
   - Changed "subcommunities" to "parental communities" (2 occurrences)
   - Changed "failed-invasion" to "failed invasion" (3 occurrences)
   - Fixed Supplementary Fig. 19 labels
   - Fixed "15h" to "15~h"

2. `latex/supplementary_sections/extended_data.tex`
   - Changed "SEM" to "s.e.m." (3 occurrences)
   - Changed "one-sided selection" to "Dominance" (2 occurrences)
   - Changed "subcommunities" to "parental communities" (1 occurrence)

3. `latex/supplementary_sections/skewness_null_model.tex`
   - Changed "one-sided selection" to "Dominance" (4 occurrences)

4. `latex/supplementary_sections/supplementary_methods.tex`
   - Changed "one-sided selection" to "Dominance" (1 occurrence)
   - Removed 0.01% threshold reference
   - Changed "simulation" to "simulations" (1 occurrence)

---

*Report generated: February 6, 2026*
*All fixes applied*
