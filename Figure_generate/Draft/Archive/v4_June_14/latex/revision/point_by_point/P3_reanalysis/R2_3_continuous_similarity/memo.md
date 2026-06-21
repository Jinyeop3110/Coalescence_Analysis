# P3.6 — Continuous Similarity Measures Alongside Categories

## Reviewer: R2, Point #3 (Moderate)
## Status: COMPLETED
## Confidence: 95%

### Reviewer Comment
"Classification depends on thresholds; present continuous measures; clarify restructuring"

### What They Want
The Dominance/Mixture/Restructuring categories depend on arbitrary thresholds. Show the underlying continuous distributions (PDI, retention magnitude) so readers can judge for themselves.

### Key Results

**Continuous metric definitions:**
- x = sqrt(u^2 + v^2) : retention magnitude (how much parental composition is retained)
- y = asymmetricity : direction-independent asymmetry score (0 = balanced, 1 = one parent dominates)
- PDI = (2/pi) arctan(u/v) : manuscript continuous parental dominance index
- Thresholds: x^2 > 0.5 separates Restructuring from Dominance/Mixing; y > 0.5 separates Dominance from Mixing

**Distributions by medium condition (threshold > 0.1%):**

| Medium | n  | y median | y mean | x^2 (retention) median | x^2 mean |
|--------|----|----------------|--------|------------------------|----------|
| Nutr-  | 90 | 0.410          | 0.424  | 0.792                  | 0.755    |
| Base   | 83 | 0.915          | 0.812  | 0.722                  | 0.655    |
| Nutr+  | 90 | 0.985          | 0.862  | 0.924                  | 0.786    |

**Statistical tests:**
- asymmetry y across media: KW H = 110.71, p = 9.12e-25 (highly significant)
- x^2 (retention) across media: KW H = 18.05, p = 1.21e-04 (significant)

**Category fractions:**
- Nutr-: Dominance 38.9%, Mixing 53.3%, Restructuring 7.8%
- Base:  Dominance 65.1%, Mixing 3.6%, Restructuring 31.3%
- Nutr+: Dominance 75.6%, Mixing 5.6%, Restructuring 18.9%

**Boundary sensitivity:** Reclassifying Dominance after varying the PDI boundary or the retention boundary `x^2` supports the same nutrient-dependent trend.

| Criterion | Nutr- | Base | Nutr+ |
|-----------|-------|------|-------|
| Manuscript baseline: `|PDI - 0.5| >= 0.25`, `x^2 > 0.5` | 38.9% | 65.1% | 75.6% |

**Key insight:** The continuous coordinates and boundary-sensitivity analysis support the same core result as the categorical summary: Dominance increases from Nutr- to Base to Nutr+. The retention magnitude (x^2) is generally high, indicating most events preserve parental composition, while lower-retention events correspond to the Restructuring category.

### Jaccard Subquestion

Reviewer 2 specifically flagged the dot-product versus Jaccard divergence as potentially informative. A per-medium check supports a careful, two-part interpretation:

| Medium | Vector decomposition D/M/R | Jaccard D/M/R | Main interpretation |
|--------|-----------------------------|---------------|---------------------|
| Nutr-  | 35/48/7                     | 5/55/30       | Jaccard further suppresses Dominance, consistent with weak interactions and species-level persistence. |
| Base   | 54/3/26                     | 21/27/35      | Many abundance-dominance events are not dominance of a full parental ASV set. |
| Nutr+  | 68/5/17                     | 11/20/59      | Strong abundance dominance coexists with severe species-identity filtering/loss. |

Response framing:
- Dot product / vector decomposition is abundance-weighted and addresses quantitative parental dominance.
- Jaccard is presence/absence-based and addresses species-identity retention.
- The low-nutrient Jaccard result supports the reviewer's species-level interpretation, but the same wording should not be extended uncritically to Base or Nutr+, where Jaccard mostly shows that abundance dominance does not require retaining the winner parent's full ASV list.

### Output Figures
- `scatter_retention_vs_PDI.{svg,pdf,png}` — 2D scatter with category regions and threshold lines
- `marginal_distributions_by_medium.{svg,pdf,png}` — three-by-three PDI, y, and x^2 figure with nutrient conditions separated by row
- `marginal_distributions_nutr_minus_only.{svg,pdf,png}` — Nutr-minus one-row PDI, y, and x^2 figure for Supplementary Fig. 30
- `marginal_distributions_nutr_plus_only.{svg,pdf,png}` — Nutr-plus one-row PDI, y, and x^2 figure for Supplementary Fig. 31
- `boundary_sensitivity_by_medium.{svg,pdf,png}` — two-panel PDI-boundary and retention-boundary sensitivity analysis
- `scatter_by_medium.{svg,pdf,png}` — 2D scatter faceted by medium with category fractions
- `bray_curtis_similarity.{svg,pdf,png}` — Bray-Curtis similarity to parents

### Code Location
`/Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`

### Implications for Manuscript
- New Supplementary Figure showing continuous distributions
- The categorical trends are strongly supported by continuous analysis
- Brief mention in Results: "Continuous similarity measures confirmed the categorical trends"
- Clarify Restructuring: events with low parental retention may reflect competitive exclusion producing novel dominance hierarchies
