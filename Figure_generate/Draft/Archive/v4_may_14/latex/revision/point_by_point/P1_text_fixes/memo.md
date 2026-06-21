# Phase 1: Text-Only Fixes

## Status: COMPLETE (2026-04-14)

All 13 items have been addressed. Summary below.

---

### P1.1 — Typo: "generalis ability" (R2-M5)
- **Status**: [x] ALREADY FIXED
- **Action**: Searched all .tex files in v4/latex/. The typo "generalis ability" does not appear in any .tex file — it was already corrected in v4 (likely fixed during the v3-to-v4 transition).
- **Files changed**: None

### P1.2 — Wrong ED Fig reference (R1-11)
- **Status**: [x] FIXED
- **Action**: Found TWO files with off-by-one ED Fig references:
  1. `supplementary_sections/simulations.tex`: "Extended Data Fig.~5" → "Extended Data Fig.~4" (community size effect is ED Fig. 4, not 5)
  2. `supplementary_sections/pairwise_selection_correlation.tex`: "Extended Data Fig.~6a--d" → "Extended Data Fig.~5a--d", "Extended Data Fig.~7" → "Extended Data Fig.~6" (pairwise selection correlation figures were renumbered)
- **Files changed**: `supplementary_sections/simulations.tex`, `supplementary_sections/pairwise_selection_correlation.tex`

### P1.3 — Terminology consistency (R2-M4)
- **Status**: [x] REVIEWED (report only, no changes made)
- **Findings**:
  - "coalescence event" (used ~20 times) vs "coalescence experiment" (used ~5 times): Both are used appropriately — "event" for individual pairings, "experiment" for the experimental campaign. Consistent usage, no change needed.
  - mu notation: Consistently written as `$\mu$` throughout. Used with "interaction strength" or "mean competition coefficient" qualifiers.
  - alpha_ij notation: Consistently written as `$\alpha_{ij}$` throughout. Defined in both results.tex and supplementary_methods.tex.
  - "interaction strength" vs "competition strength": See P1.4 below — a disambiguation sentence was added.
- **Files changed**: None

### P1.4 — "Interaction strength" terminology (R3-4)
- **Status**: [x] FIXED
- **Action**: Added a disambiguation sentence at first use of mu in `sections/results.tex` (gLV model section): "Throughout the text, we use 'interaction strength' as shorthand for this mean competition coefficient mu when referring to the gLV model; in the experimental context, we use the term more broadly to denote the overall intensity of competitive interactions, as proxied by the frequency of failed pairwise invasions."
- **Files changed**: `sections/results.tex`

### P1.5 — Tone down robustness claim (R1-5)
- **Status**: [x] FIXED
- **Action**: Changed "was robust across variants of similarity metrics" to "was broadly consistent across several similarity metrics, including Bray--Curtis dissimilarity and Euclidean distance (Extended Data Fig.~2), although the relative ranking of outcome types was sensitive to metric choice: Jensen--Shannon divergence and Jaccard index yielded somewhat different orderings."
- **Files changed**: `sections/results.tex` (line 24)

### P1.6 — Frame gLV as phenomenological (R2-6)
- **Status**: [x] FIXED
- **Action**: Added sentence after gLV model introduction: "We emphasize that the gLV model serves as a phenomenological framework to explore how the statistical properties of interaction coefficients shape coalescence outcomes, rather than as a mechanistic model of the specific biochemical interactions underlying our experimental observations."
- **Files changed**: `sections/results.tex` (line 42, after model description)

### P1.7 — Emphasize "cohesion without cooperation" (R1-9)
- **Status**: [x] FIXED
- **Action**: Expanded the paragraph referencing Tikhonov in discussion.tex: "Notably, our results demonstrate that community-level cohesion can emerge without cooperative interactions between species — a prediction made by Tikhonov using resource-competition models. In our system, purely competitive interactions, when structured by assembly history, are sufficient to produce the correlated species fates that underlie Dominance. This 'cohesion without cooperation' arises because assembly filters species into internally compatible groups whose members compete weakly with each other but face stronger competition from outsiders."
- **Files changed**: `sections/discussion.tex` (paragraph 2)

### P1.8 — Tone down natural community claims (R3-3)
- **Status**: [x] FIXED
- **Action**: Replaced the strong generality claim at end of natural communities section with nuanced language: acknowledged that higher Restructuring "may reflect greater taxonomic diversity, more complex interaction networks, or the presence of facilitative interactions not captured by our competition-only model." Added caveat: "the higher Restructuring frequency in natural communities warrants caution in drawing direct quantitative comparisons."
- **Files changed**: `sections/results.tex` (natural communities section, line ~120)

### P1.9 — Discuss alternative mechanisms (R2-2)
- **Status**: [x] FIXED
- **Action**: Added a full paragraph in discussion.tex addressing three alternative mechanisms: (1) environmental filtering, (2) neutral hitchhiking, (3) shared trait correlations. Then argued against each using: pairwise selection correlation persisting after abundance controls, assembly history effect (ED Fig. 7, Suppl. Fig. 19), and gLV model reproducing patterns without environmental filtering. Cited Keddy1992, Leibold2004, McGill2006.
- **Files changed**: `sections/discussion.tex` (new paragraph 4)

### P1.10 — Natural community pre-selection (R2-5)
- **Status**: [x] FIXED
- **Action**: Added paragraph in discussion.tex acknowledging that "The stabilization phase — seven serial growth-dilution cycles in defined laboratory media — may pre-select natural communities toward species that thrive under these specific culture conditions, potentially reducing effective diversity..." Noted this does not explain the qualitative trend of increasing Dominance with nutrient concentration.
- **Files changed**: `sections/discussion.tex` (new paragraph 6)

### P1.11 — Reframe nutrient enrichment ≠ interaction strength (R2-1)
- **Status**: [x] FIXED
- **Action**: Three changes:
  1. `sections/results.tex` (Fig. 4 section): Rewrote to acknowledge nutrient enrichment is a complex perturbation (citing Duan2025), not equivalent to simple increase in alpha_ij. Reframed: "While nutrient enrichment is not a simple proxy for the gLV parameter mu, it consistently increased the frequency of failed pairwise invasions — our experimental proxy for the overall intensity of competitive interactions." Changed "mean interaction strengths" to "mean competition coefficients."
  2. `sections/discussion.tex`: Added new paragraph discussing mu as "idealized, single-axis control" and the mapping between nutrient concentration and mu as "necessarily approximate."
  3. `references.bib`: Added Duan2025 reference (Duan, Bueno, Dai. Nature Ecology & Evolution, 2025).
- **Files changed**: `sections/results.tex`, `sections/discussion.tex`, `references.bib`

### P1.12 — pH measurement method (R2-M2)
- **Status**: [x] ALREADY SPECIFIED
- **Action**: Checked `sections/methods.tex`. The pH measurement method IS specified: "Community pH was measured using a benchtop pH meter (Apera Instruments PH5500)." No placeholder needed.
- **Files changed**: None

### P1.13 — Biological meaning of interaction coefficients (R2-M3)
- **Status**: [x] FIXED
- **Action**: Added biological interpretation in `supplementary_sections/supplementary_methods.tex` (Lotka-Volterra Simulations subsection): "Biologically, each alpha_ij represents the net per-capita effect of species j on species i's per-capita growth rate, encompassing both direct mechanisms (e.g., resource competition, interference) and indirect mechanisms (e.g., metabolite-mediated inhibition, pH modification). Because we restrict alpha_ij >= 0, the model captures only competitive (growth-inhibiting) interactions; facilitative interactions such as cross-feeding are not represented."
- **Files changed**: `supplementary_sections/supplementary_methods.tex`

---

## Summary of files modified

| File | Items addressed |
|------|----------------|
| `sections/results.tex` | P1.4, P1.5, P1.6, P1.8, P1.11 |
| `sections/discussion.tex` | P1.7, P1.9, P1.10, P1.11 |
| `supplementary_sections/simulations.tex` | P1.2 |
| `supplementary_sections/pairwise_selection_correlation.tex` | P1.2 |
| `supplementary_sections/supplementary_methods.tex` | P1.13 |
| `references.bib` | P1.11 (added Duan2025) |

## New references added
- Duan2025: Duan, Bueno, Dai. "Resource Competition Predicts Assembly of Gut Bacterial Communities In Vitro." Nature Ecology & Evolution 9, 247-257 (2025).

## Items requiring no changes
- P1.1: Typo already fixed in v4
- P1.3: Terminology is consistent (report only)
- P1.12: pH method already specified
