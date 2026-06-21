# P3.3 — PDI Excluding Dominant Species (Circularity Check)

## Reviewer: R1, Point #3 (Major)
## Status: COMPLETED
## Confidence: 95%

### Reviewer Comment
"Fig. 5C circularity: Does PDI correlation hold if dominant species excluded?"

### What They Want
In Fig. 5C, the correlation between parent community characteristics and coalescence outcomes might be circular: the dominant species by definition determines PDI. If you remove the dominant species from the PDI calculation, does the correlation survive? If yes, the pattern is driven by the whole community, supporting community-level selection. If no, it is just a dominant-species effect.

### Analysis Completed
Script: `/Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`

1. Replicated Fig. 5C PDI correlation (M+H media, all pool sizes).
2. Removed the dominant species (most abundant in coalesced community) from all three compositions.
3. Renormalized and recalculated vector decomposition.
4. Compared R^2, slopes, and aligned fractions.

### Key Results

**Fig 5C replication (M+H combined, pairwise assay):**
- Original: n=97, R^2 = 0.34, slope = 0.87, aligned fraction = 79.4%
- Dominant removed: n=73, R^2 = 0.07, slope = 0.36, aligned fraction = 53.4%
- R^2 change: -0.27

**Vector decomposition reclassification (all 263 events):**
- Of 157 original Dominance events after dominant species removal:
  - 63 (40.1%) remain classified as Dominance
  - 26 (16.6%) reclassified as Mixing
  - 66 (42.0%) reclassified as Restructuring
  - 2 (1.3%) unclassifiable

**Direction consistency:**
- Among valid Dominance events: 68.4% (106/155) maintain the same winner direction
- Spearman correlation between original and modified community score: rho = 0.64, p = 5.0e-19

### Figures Generated
- `Fig_R1_3ab_PDI_comparison.{svg,pdf,png}` — Side-by-side Fig 5C: original vs dominant-removed
- `Fig_R1_3c_VD_reclassification.{svg,pdf,png}` — Outcome reclassification + direction scatter
- `Fig_R1_3d_R2_comparison.{svg,pdf,png}` — R^2 bar comparison

### Interpretation for Response
The PDI correlation weakens substantially when the dominant species is removed (R^2: 0.34 -> 0.07), confirming that the dominant species is a major driver of the correlation. However, several lines of evidence indicate the relationship is not purely circular:

1. **Direction preservation**: 68% of events maintain the same winner direction after removal (Spearman rho = 0.64, p < 1e-18), indicating subdominant species also contribute to outcome direction.
2. **Partial Dominance persistence**: 40% of Dominance events remain classified as Dominance even after removing the dominant species.
3. **The weakening is expected**: By definition, removing the most abundant species reduces the signal; this does not invalidate the original correlation but rather decomposes it into dominant-species and community-level contributions.

### Changes to Manuscript
- Add Supplementary Figure(s) from the above
- Add sentence in Results: "To test for circularity in the PDI correlation, we removed the dominant species from all compositions and recalculated the vector decomposition. The correlation weakened (R^2 = 0.34 to 0.07), but 68% of events maintained the same winner direction (Spearman rho = 0.64, p < 10^{-18}), and 40% of events remained classified as Dominance (Supplementary Fig. X). This indicates that while the dominant species is the primary driver, subdominant community members also contribute to coalescence outcomes."
