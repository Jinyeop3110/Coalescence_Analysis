# Grammar & Terminology Review (Updated)

Review of the manuscript "Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence" — paragraph-by-paragraph, starting from the abstract through the main text and supplementary.

**Note:** This is a fresh re-review of the current manuscript state. Previously fixed issues (#19, #30, #39, #57, #50/56/58, #136) are confirmed resolved and not re-listed.

---

## Abstract (title_abstract.tex)

### Line 29 (Abstract body)
1. **"indicating the absence of community-level selection"** — Slightly awkward parallel structure. The first clause says "indicating community-level selection" and the second says "indicating the absence of community-level selection." Consider: "consistent with the absence of community-level selection" for variety, or leave as-is if parallelism is intentional. *Severity: Low (style).*

2. **"communities derived from natural samples with greater taxonomic diversity and richness"** — Ambiguous: greater than what? The reader hasn't been told what the synthetic communities look like yet. Consider: "communities derived from natural samples with greater taxonomic diversity and richness than synthetic consortia." *Severity: Low (clarity).*

3. **"an emergent regime in which collective dynamics shape outcomes that cannot be predicted from species traits alone"** — Grammatically fine, but "shape outcomes that cannot be predicted" could be misread as "shape [specific] outcomes that happen to be unpredictable." Consider: "an emergent regime in which collective dynamics shape outcomes in ways that cannot be predicted from species traits alone." *Severity: Low (clarity).*

**No critical grammar errors in the abstract.**

---

## Introduction (introduction.tex)

### Paragraph 1 (Line 7)
4. **Missing space before `\citep` throughout** — e.g., `coevolution\citep{...}` on line 7. LaTeX usually renders this fine with natbib superscript citations, but check the rendered PDF to be sure. Multiple occurrences in intro and results. *Severity: Low (formatting — check PDF).*

5. **"termed community-level selection"** (Line 9) — The appositive is somewhat orphaned: "making the community the primary unit of selection, termed community-level selection." It reads as if "unit of selection" is what's "termed." Consider: "making the community the primary unit of selection — a pattern termed community-level selection." *Severity: Low (clarity).*

### Paragraph 3 (Line 11)
6. **"Notably, this structured interaction can arise due to ecological exclusion alone"** — "structured interaction" is singular but refers to a pattern. Consider "this structured interaction pattern" or "these structured interactions." *Severity: Low (style).*

7. **Trailing whitespace at end of line 11** — Minor. *Severity: Negligible.*

### Paragraph 4 (Line 13)
8. **"coexistence between species from different source communities is common through niche partitioning rather than competitive exclusion during macro-scale biogeographic interchange"** — "common through niche partitioning" is grammatically strained. Consider: "is common, arising through niche partitioning rather than competitive exclusion, during macro-scale biogeographic interchange." *Severity: Low (readability).*

### Paragraph 5 (Line 16)
9. **"These patterns generalize to natural communities with greater taxonomic complexity."** — Same ambiguity as in abstract (#2): "greater" than what? *Severity: Low (clarity).*

---

## Results (results.tex)

### Section 3.1 — "Coalescence frequently yields asymmetric outcomes..." (Lines 10–31)

10. **"Consider a coalescence event where communities A and B merge"** (Line 13) — In formal scientific prose, "in which" is preferred over "where" for non-spatial references. *Severity: Low (style).*

11. **"5~g~L$^{-1}$ glucose and 4~g~L$^{-1}$ urea"** (Line 20) — Missing Oxford comma before "and" in the medium composition list. Should be: "5~g~L$^{-1}$ glucose**,** and 4~g~L$^{-1}$ urea" for consistency with the other comma-separated items. *Severity: Low (punctuation).*

12. **83 coalescence events** (Lines 20, 24, Fig. 1 caption line 30) — A previous git commit message says "Fix coalescence event count: 83 -> 82 in Base medium," but the current text still uses 83 throughout. **Verify whether the correct number is 82 or 83.** *Severity: Medium (factual accuracy).*

13. **"Among 3 representative time-series trajectories, we did not observe Mixture cases"** (Line 22) — Slightly confusing: "among 3 representative" implies you chose them, so of course you wouldn't necessarily include a Mixture. Consider: "The three representative trajectories shown here illustrate Dominance and Restructuring; Mixture outcomes were rare (see Extended Data Fig. 6 for additional time series)." *Severity: Low (clarity).*

### Section 3.2 — "Random competitive interactions..." (Lines 35–54)

14. **"This observation suggests that interspecies interactions alone, a minimal and generic condition, are sufficient"** (Line 44) — "interspecies interactions alone" is not itself a "condition." Consider: "interspecies interactions alone — a minimal and generic ingredient — are sufficient." *Severity: Low (style).*

15. **Inconsistent citation spacing** — Line 46 uses `~\citep{Gilpin1994, Lechon2021}` (with non-breaking space), which is good. But many other citations lack a space before `\citep`. Standardize throughout. *Severity: Low (formatting).*

### Section 3.3 — "Interaction strength controls..." (Lines 58–71)

16. **"spanning our experimental species pool range"** (Line 63) — Ambiguous: does this mean the range of initial richness values (6–24) or the total pool size (54)? Consider clarifying. *Severity: Low (clarity).*

### Section 3.4 — "Nutrient-dependent interaction strength..." (Lines 75–90)

17. **"Assuming the uniform distribution used in the model, calibrating these values against gLV simulations yielded..."** (Line 78) — Dangling/mismatched modifier. "Assuming" and "calibrating" have different implied subjects. Consider: "Using the uniform distribution assumed in the model, we calibrated these values against gLV simulations, yielding..." *Severity: Low (grammar).*

18. **"In Base and Nutr+ media"** (Line 82) — **Still uses plain "Nutr+"** instead of "Nutr$+$" (math mode). This instance was missed in the previous fix. *Severity: Medium (consistency).*

### Section 3.5 — "Dominant community predictability..." (Lines 94–110)

19. **"We next asked whether we can predict"** (Line 97) — Tense shift: "can" (present) in a past-tense narrative. Consider: "could predict." *Severity: Low (tense).*

20. **Figure 4 caption (Line 88): "Nutr+" in two places** — The caption text on line 88 has plain "Nutr+" at "and Nutr+ has high glucose/urea" and "76\% in Nutr+". These should be "Nutr$+$" for consistency. *Severity: Medium (consistency).*

21. **Figure 5 caption (Line 108): "Nutr+" in one place** — "in Nutr+ where dominant species determine outcomes" should be "Nutr$+$". *Severity: Medium (consistency).*

### Section 3.6 — "Interaction-dependent coalescence outcomes..." (Lines 114–129)

22. **"naturally-evolved microbial assemblages"** (Line 121) — Hyphen is unnecessary when "naturally" is an adverb modifying "evolved." Should be "naturally evolved." *Severity: Low (punctuation).*

23. **"and Nutr+"** (Lines 119, 121) — Two more instances of plain "Nutr+" that should be "Nutr$+$". *Severity: Medium (consistency).*

24. **Figure 6 caption (Line 127): "Nutr+" in two places** — "77\% in Nutr+" should be "Nutr$+$". *Severity: Medium (consistency).*

---

## Discussion (discussion.tex)

### Paragraph 1 (Line 8)
25. **"interaction strength determines whether communities behave as cohesive units or loose species assemblages"** — Consider "as loose assemblages of species" for better parallel structure with "as cohesive units." *Severity: Low (style).*

### Paragraph 2 (Line 11)
26. **"Our work provides the first experimental demonstration"** — "first" is a strong claim; verify that no prior work has demonstrated this. *Severity: Low (factual — verify).*

27. **"extend this claim to include coalescence"** (Line 14) — "claim" is slightly imprecise; interaction strength as a key parameter is more of a finding. Consider "extend this finding." *Severity: Low (word choice).*

### Paragraph 4 (Line 16)
28. **"In nature, coalescence occurs in richer settings"** — "richer" is vague. Richer in nutrients, species, environmental complexity? Consider being more specific. *Severity: Low (clarity).*

29. **"Incorporating these axes into both theory and experiment"** — "these axes" is vague. Consider: "Incorporating these factors (environmental heterogeneity, host effects, mutualism) into both theory and experiment." *Severity: Low (clarity).*

---

## Supplementary Methods (supplementary_methods.tex)

### Strain Library (Lines 10–19)
30. **"54 bacterial isolates derived from soil, tree surface, and flower stamen environments collected in Cambridge"** — Slightly ambiguous: were the environments or isolates collected? Consider: "54 bacterial isolates from soil, tree-surface, and flower-stamen environments in Cambridge, MA, USA." *Severity: Low (clarity).*

### 16S rRNA Sequencing (Lines 36–41)
31. **"which corresponds to the 0.1\% extinction threshold used in simulation"** (Line 41) — "in simulation" → "in simulations" (plural, since multiple simulations were run). *Severity: Low (grammar).*

### Lotka-Volterra Simulations (Lines 73–88)
32. **Species assignment "(1--12, 13--24, 25--36, 37--48)"** (Line 83) — This uses 48 of 54 species, leaving 6 unused. The text says "pool of $N = 54$ species partitioned into four... communities of 12." Technically 48 are partitioned, not 54. Consider noting that 6 species remain unassigned. *Severity: Low (clarity).*

### Pairwise Invasion Assays (Lines 93–97)
33. **Bistability criterion not given** (Line 96) — Coexistence (both >10%) and exclusion (one <1%) thresholds are stated, but no threshold for bistability is specified. *Severity: Low (completeness).*

### Sensitivity Analysis (Lines 147–155)
34. **"Similarity Metric Robustness:" and "Simulation Robustness:"** — These labels are run into the paragraph text rather than formatted as subheadings. Consider `\paragraph{}` or `\textbf{}` markup for consistency. *Severity: Low (formatting).*

---

## Supplementary Note 1: Null Models (skewness_null_model.tex)

35. **"mean one-sided selection of 0.698 ($n = 83$)"** (Line 12) — Uses 83 again. Verify consistency with main text (see #12). *Severity: Medium (verify number).*

36. **No grammar issues found otherwise.**

---

## Supplementary Note 2: Assembly Effect (assembly_effect.tex)

37. **"Those that survive to coexistence"** (Line 9) — "survive to coexistence" is slightly unusual phrasing. Consider "survive and coexist" or "survive to reach coexistence." *Severity: Low (style).*

38. **No other issues.**

---

## Supplementary Note 3: Simulation Robustness (simulations.tex)

39. **No grammar issues found.**

---

## Supplementary Note 4: Pairwise Selection Correlation (pairwise_selection_correlation.tex)

40. **"one survives, one extinct"** (Line 7) — Mixes verb and adjective. Should be "one survives, one goes extinct" or "one surviving, one extinct." *Severity: Low (grammar).*

41. **No other issues.**

---

## Supplementary Note 5: Pairwise Invasion Experiments (invasion.tex)

42. **"Under Nutr$-$, more pairs achieved stable coexistence, while Nutr$+$ conditions led to more frequent exclusion"** (Line 11) — Inconsistent phrasing: "Under Nutr$-$" vs. "Nutr$+$ conditions led to." Consider: "Under Nutr$-$ conditions, more pairs achieved stable coexistence, while under Nutr$+$ conditions, exclusion was more frequent." *Severity: Low (style).*

---

## Extended Data Figure Captions (extended_data.tex)

43. **No grammar issues found in ED Fig. 1–8 captions.**

---

## Supplementary Figure Captions (figures.tex)

### Suppl. Fig. 9
44. **"Distribution of monoculture pH after 15h growth"** (Line 126) — Missing space: "15h" → "15~h" for consistency with the rest of the manuscript. *Severity: Low (formatting).*

### Suppl. Fig. 21
45. **Missing opening parenthesis** (Line 305) — Caption reads: "Base medium $n = 54$ isolates)." There is a closing parenthesis but no opening one. Should be: "(Base medium, $n = 54$ isolates)" or "Base medium ($n = 54$ isolates)." *Severity: **High** (typographical error).*

### Suppl. Fig. 24
46. **Cross-reference may be wrong** (Line 333) — Caption says "natural-community analog of Supplementary Fig.~12 for synthetic communities." Supplementary Fig. 12 is the Nutr$-$ rank-abundance for synthetic communities. Supplementary Fig. 24 is the **Base** medium natural community figure, so it should reference Supplementary Fig. **11** (Base, synthetic), not Fig. 12. *Severity: Medium (incorrect cross-reference).*

---

## Summary of Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 45 | **High** | Suppl. Fig. 21 caption | Missing opening parenthesis: "$n = 54$ isolates)" |
| 12 | **Medium** | Results §3.1 | 83 vs 82 coalescence events — verify correct count |
| 18 | **Medium** | Results §3.4, line 82 | Plain "Nutr+" should be "Nutr$+$" |
| 20 | **Medium** | Fig. 4 caption | Plain "Nutr+" (two instances) should be "Nutr$+$" |
| 21 | **Medium** | Fig. 5 caption | Plain "Nutr+" should be "Nutr$+$" |
| 23 | **Medium** | Results §3.6 | Plain "Nutr+" (two instances) should be "Nutr$+$" |
| 24 | **Medium** | Fig. 6 caption | Plain "Nutr+" should be "Nutr$+$" |
| 35 | **Medium** | Suppl. Note 1 | n=83 — verify consistency |
| 46 | **Medium** | Suppl. Fig. 24 caption | Cross-reference to Fig. 12 should be Fig. 11 |
| 11 | **Low** | Results §3.1 | Missing Oxford comma in medium composition |
| 17 | **Low** | Results §3.4 | Dangling modifier ("Assuming...calibrating...") |
| 22 | **Low** | Results §3.6 | "naturally-evolved" → "naturally evolved" |
| 40 | **Low** | Suppl. Note 4 | "one survives, one extinct" — mixed verb/adjective |
| 44 | **Low** | Suppl. Fig. 9 | "15h" → "15~h" |
| Others | **Low** | Various | Style/clarity suggestions (see items 1–10, 13–16, 19, 25–34, 37, 42) |
