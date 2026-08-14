# P3.5 — Richness Across Media Conditions (Experimental)

## Reviewer: R3, Point #2 (Critical, part a)
## Status: COMPLETED
## Confidence: 95%

### Reviewer Comment
"Show richness across Base/Nutr-/Nutr+ for synthetic communities"

### What They Want
If nutrient enrichment reduces species richness (by intensifying competition), then the observed increase in Dominance with enrichment could be partly a geometric artifact of lower dimensionality. Need to show richness data to assess this confound.

### Key Results

**Parental communities (threshold > 0.1%):**
- Nutr-: median=12.0, mean=11.3 +/- 2.9 (n=60)
- Base:  median=8.0,  mean=9.5  +/- 5.5 (n=59)
- Nutr+: median=7.5,  mean=8.5  +/- 5.3 (n=60)
- Kruskal-Wallis H = 15.79, p = 3.73e-04 (significant)
- Pairwise: Nutr- vs Base p=0.010, Nutr- vs Nutr+ p=7.0e-05, Base vs Nutr+ p=0.28

**Coalesced communities (threshold > 0.1%):**
- Nutr-: median=13.0, mean=13.0 +/- 2.7 (n=90)
- Base:  median=7.0,  mean=9.9  +/- 5.0 (n=83)
- Nutr+: median=9.0,  mean=8.5  +/- 3.7 (n=90)
- Kruskal-Wallis H = 53.93, p = 1.95e-12 (highly significant)

**Richness does decrease with nutrient enrichment.** This is a real effect that the reviewer correctly identified. However, Dominance frequency increases even more dramatically (from ~39% to ~76%), which is disproportionate to the richness change, suggesting it is not purely a geometric artifact.

**Coalesced vs parental richness change:**
- Nutr-: mean change = +2.27 (coalescence increases richness)
- Base:  mean change = +1.16
- Nutr+: mean change = -0.38 (coalescence slightly decreases richness)

### Output Figures
- `richness_by_medium.{svg,pdf,png}` — Violin/box plot, parents vs coalesced
- `richness_thresholds.{svg,pdf,png}` — Robustness across 4 detection thresholds
- `richness_coalesced_vs_parental.{svg,pdf,png}` — Scatter + change by medium

### Code Location
`/Figure_generate/code/Figure_revision/R3_2_richness_media/analyze_richness_media.py`

### Implications for Manuscript
- Richness does decrease with nutrient enrichment (p < 0.001)
- This should be acknowledged as a contributing factor
- But the Dominance shift is larger than expected from dimensionality alone
- Recommend: new Supplementary Figure + brief discussion of the confound
