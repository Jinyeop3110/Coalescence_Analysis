# Phase 2: Figure Style / Caption Fixes

## Status: IN PROGRESS (captions done; two items need figure regeneration decisions)

---

### P2.1 -- Gray reflection points (R1-6)
- **Status**: [x] DONE (caption edits applied)
- **Reviewer says**: Gray points in Figs 1E, 4C, 5C, 6B are reflections and confusing
- **Action taken**: Added the following sentence to each relevant figure caption:
  - Fig. 1 (panel e): "Gray points represent the symmetric counterpart of each coalescence event (community B versus A), included to illustrate the symmetry of the similarity space."
  - Fig. 4 (panel c): Same sentence, inserted after the initial richness symbol legend and before the PDI histogram description.
  - Fig. 5 (panel c): "Gray points represent the symmetric counterpart of each coalescence event (community B versus A), included to illustrate the symmetry of the relationship." (slightly different wording since this is a predictability scatter, not similarity space)
  - Fig. 6 (panel b): Same sentence as Figs 1/4, inserted after the description of outcome clustering.
- **Files modified**: `sections/results.tex` (lines ~30, ~87, ~107, ~127)
- **Decision**: Kept gray points with caption clarification (Option A from original memo). No figure regeneration needed.

### P2.2 -- Fig. 2D clarity (R1-8)
- **Status**: [x] DONE (caption edits applied)
- **Reviewer says**: Relationship between points and squares is unclear; gray bars unexplained
- **Action taken**: Expanded the Fig. 2D caption to explicitly describe all visual elements:
  - Individual dots = per-event pairwise selection correlations
  - Squares with error bars = mean +/- s.e.m.
  - Gray horizontal lines = random selection baseline from null model (species origin labels shuffled)
  - Red = same parental community; Blue = cross-community pairs
- **Old caption text**: "Pairwise selection correlation. Species pairs from the same parental community show positive correlation (co-survival), while cross-community pairs show negative correlation, indicating community-level selection. This pattern holds for both simulations (left) and experiments (right). Error bars, s.e.m."
- **New caption text**: "Pairwise selection correlation. Individual dots show per-event pairwise selection correlations; squares with error bars show mean +/- s.e.m. Gray horizontal lines indicate the random selection baseline from a null model in which species origin labels are shuffled (see Supplementary Information). Species pairs from the same parental community (red) show positive correlation (co-survival), while cross-community pairs (blue) show negative correlation, indicating community-level selection. This pattern holds for both simulations (left) and experiments (right)."
- **Files modified**: `sections/results.tex` (line ~53)
- **Note**: This clarification matches the language already used in the ED Fig. 5 caption in `supplementary_sections/extended_data.tex`, which already explained these elements. Now Fig. 2D is consistent.

### P2.3 -- ED Fig. 5C means (R1-10)
- **Status**: [x] INVESTIGATED -- No change needed
- **Reviewer asks**: Are means missing from ED Fig. 5C?
- **Finding**: Means ARE present in panel c. Visual inspection of `figures/extended_data/ED_Fig5_combined.jpg` confirms that all three panels (a, b, c) contain:
  - Small scattered dots (individual per-event correlations, 50 stratified samples displayed)
  - Large filled squares with error bars (mean +/- s.e.m.) for both "Same Parent" (red) and "Cross Parents" (blue)
  - Gray horizontal lines (random selection baseline)
- **Panel c details** (mu=0.8): Red square (Same Parent mean) is at approximately +0.15, blue square (Cross Parents mean) is at approximately -0.40. The separation (Delta = 0.94 per caption) is the largest among panels a-c.
- **Caption already states**: "Individual dots show per-event correlations (50 stratified samples displayed); squares with error bars show mean +/- s.e.m."
- **Conclusion**: No figure regeneration or caption change needed. The means are clearly shown. If the reviewer found them hard to see, the issue may be that the squares overlap with the dense scatter of individual dots. This overlaps with the P2.4 visualization improvement issue.
- **Possible enhancement** (if desired): Increase the size of the mean squares or add a white edge/outline to make them stand out more from the background dots. This would require regenerating the figure using `plot_correlation_barplots_clean.py` or the simulation equivalent.

### P2.4 -- Pairwise correlation visualization (R2-M1)
- **Status**: [x] INVESTIGATED -- Figure regeneration recommended
- **Reviewer says** (Reviewer 2, Minor Comment): "Improve the visualisation of pairwise correlation results, as the separation between groups is not visually clear."
- **Affected figures**: Fig. 2D (main), ED Fig. 5 (panels a-c), ED Fig. 6 (panels a-c)
- **Current state analysis**:
  - The plots use jittered scatter of individual per-event correlations (small semi-transparent dots, alpha=0.3, size=15) overlaid with filled squares (mean) and error bars (s.e.m.).
  - The dot scatter is dense and the two groups (red/blue) overlap considerably, especially in conditions with weak interactions (Nutr-, mu=0.3).
  - The mean squares, while present, can be visually lost among the scattered dots.
  - The gray baseline line is subtle.
- **Code location**: `Figure_generate/code/plot_correlation_barplots_clean.py` (experimental), `plot_correlation_barplot_simulation_u0.6.py` and related scripts (simulation)
- **Suggested improvements** (ranked by impact):
  1. **Increase mean marker size and add white edge**: Change `markersize=12` to `markersize=14` or larger, and increase `markeredgewidth` from 0.5 to 1.5 with white edge color. This makes means stand out from background dots.
  2. **Add violin or box plot overlay**: Replace or supplement the raw dot scatter with split violin plots or box plots showing the distribution of each group. This would make the separation between groups immediately visible.
  3. **Reduce dot opacity or use smaller dots**: Change `alpha=0.3` to `alpha=0.15` and `s=15` to `s=8` so dots serve as subtle background context rather than competing with the means.
  4. **Add Delta annotation**: Show the difference (Delta = mean_same - mean_cross) as a numeric annotation on each panel, making the separation quantifiable at a glance.
  5. **Use horizontal offset**: Slightly offset the two groups horizontally (e.g., Same Parent at x=0.0, Cross Parents at x=1.0 but with staggered jitter) to reduce visual overlap.
  6. **Thicken the gray baseline**: Make the null baseline more prominent (increase linewidth or add a subtle gray shaded band showing null s.e.m.).
- **Decision needed**: Which improvement approach to use? Option 2 (violin plots) would be the most impactful visual change but alters the figure style. Options 1+3+4 together would be a conservative enhancement that keeps the current style but improves clarity.
- **Implementation note**: Changes would require re-running the plotting scripts and re-combining panels into the composite figures (ED_Fig5_combined.pdf, ED_Fig6_combined.pdf, figure_main_2_simulation_framework.pdf).

---

## Summary of completed actions

| Item | Status | Action | Files changed |
|------|--------|--------|---------------|
| P2.1 | DONE | Added gray reflection point explanation to Figs 1, 4, 5, 6 captions | `sections/results.tex` |
| P2.2 | DONE | Clarified Fig. 2D caption: dots, squares, gray lines, colors | `sections/results.tex` |
| P2.3 | No change needed | Means ARE present in ED Fig. 5C; caption already explains them | -- |
| P2.4 | Needs decision | Documented current state and 6 improvement suggestions | -- |
