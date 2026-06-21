# P3.7 — Pool Size / Richness Effects

## Reviewer: R1, Point #4 (Moderate)
## Status: COMPLETED
## Confidence: 92%

### Reviewer Comment
"Effect of initial pool size -- more detail on richness effects in model and experiment"

### What They Want
The paper uses parental communities assembled from pools of 6, 12, and 24 species. The reviewer wants to see how realized richness, assembly retention, and Dominance frequency relate to initial pool size.

### Key Results

**Realized richness vs pool size (parental communities):**
- Pool 6:  n=54, mean=7.1 +/- 4.3, median=7
- Pool 12: n=53, mean=10.4 +/- 5.1, median=10
- Pool 24: n=72, mean=11.3 +/- 4.1, median=12
- Kruskal-Wallis H = 27.48, p = 1.08e-06 (highly significant)

**ASV richness per inoculated isolate (realized parental ASV richness / inoculated pool size):**
- Pool 6:  mean=1.185 +/- 0.714 (more species survive than initially inoculated -- likely contaminants or rare ASVs)
- Pool 12: mean=0.868 +/- 0.425
- Pool 24: mean=0.471 +/- 0.173
- Kruskal-Wallis H = 56.40, p = 5.65e-13
- Larger pools have lower ASV richness per inoculated isolate, consistent with stronger assembly filtering

**Outcome distribution by pool size:**
- Pool 6:  61.3% Dominance (n=80)
- Pool 12: 58.9% Dominance (n=151)
- Pool 24: 59.4% Dominance (n=32)
- Chi-square test of the full three-category outcome distribution: chi2 = 2.24, p = 0.69 (NOT significant)
- Dominance frequency is stable across pool sizes; medium-stratified Dominance-vs-non-Dominance tests are also not significant

**Dominance by pool size AND medium (most informative):**
- Pool 6:  Nutr- 50%, Base 67%, Nutr+ 67%
- Pool 12: Nutr- 35%, Base 66%, Nutr+ 77%
- Pool 24: Nutr- 33%, Base 56%, Nutr+ 91%
- The nutrient effect on Dominance is amplified at higher pool sizes

### Output Figures
- `pool_size_analysis.{svg,pdf,png}` — 6-panel: (A) realized parental richness, (B) ASV richness per inoculated isolate, (C) experimental Dominance fraction with the pooled statistic scoped to the full three-category outcome distribution, (D) experimental pairwise fate concordance, (E) model Dominance fraction, (F) model pairwise fate concordance
- `pool_size_analysis_AB.{svg,pdf,png}` — 2-panel export of realized richness and ASV richness per inoculated isolate
- `pool_size_by_medium.{svg,pdf,png}` — Richness by pool size, faceted by medium

### Code Location
`/Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`

### Implications for Manuscript
- Realized richness increases with pool size but with diminishing returns (saturation)
- ASV richness per inoculated isolate decreases with pool size (assembly filtering)
- Dominance frequency is NOT significantly affected by pool size overall
- BUT the nutrient-Dominance interaction is stronger at higher pool sizes
- Recommend: new Supplementary Figure + 1-2 sentences in Results
