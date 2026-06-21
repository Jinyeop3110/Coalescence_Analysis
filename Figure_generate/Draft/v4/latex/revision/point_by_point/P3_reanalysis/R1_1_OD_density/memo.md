# P3.1 — Absolute Density (OD) Check

## Reviewer: R1, Point #1 (Major)
## Status: COMPLETED
## Confidence: 90%

### Reviewer Comment
"Could absolute density differences explain results? Use OD data to check."

### What They Want
The reviewer suspects that if parent communities reach very different absolute densities (OD), the denser community simply "overwhelms" the sparser one — making Dominance a trivial dilution effect rather than ecological selection.

### Analysis Completed
Script: `/Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_OD_density.py`

1. Loaded OD measurements (fieldOD7) for 263 coalescence events across all conditions.
2. Computed |deltaOD| / mean(OD) for each event.
3. Tested whether Dominance is more frequent when OD difference is large.
4. Tested whether the dominant parent tends to be the denser one.

### Key Results

**OD difference is weakly associated with Dominance but does NOT explain it:**
- Mean relative |deltaOD|: Dominance = 0.79, non-Dominance = 0.53 (Mann-Whitney p = 0.0003)
- Spearman rho = 0.22 (p = 0.0003) — statistically significant but weak effect
- Logistic regression coefficient = 0.66 (positive but modest)

**Critically, the winner is NOT the denser parent:**
- Only 26.8% of Dominance events have the denser parent winning (42/157)
- Binomial test: p < 0.0001, rejecting H0 that winner = denser
- This means the LESS dense parent wins in ~73% of Dominance events
- **This strongly refutes a simple dilution/abundance explanation**

### Figures Generated
- `Fig_R1_1a_dominance_vs_OD_diff.{svg,pdf,png}` — Dominance frequency vs |deltaOD|/mean(OD) bins
- `Fig_R1_1b_winner_OD_rank.{svg,pdf,png}` — (left) winner vs loser OD scatter; (right) P(winner is denser) by outcome
- `Fig_R1_1c_dominance_by_medium_OD.{svg,pdf,png}` — Dominance fraction by medium and OD-difference tertile

### Interpretation for Response
While there is a weak statistical association between OD differences and Dominance frequency, the dominant parent is NOT typically the denser one (only 27% of the time). This rules out the hypothesis that density differences alone drive Dominance outcomes, as it implies the winning community succeeds through ecological competition rather than numerical advantage.

### Changes to Manuscript
- Add Supplementary Figure(s) from the above
- Add sentence in Results or Discussion: "We tested whether absolute community density (OD) could explain Dominance outcomes. While OD differences showed a weak association with Dominance frequency (Spearman rho = 0.22, p < 0.001), the dominant parent was the less dense community in 73% of cases (p < 0.001, binomial test), ruling out a simple numerical-advantage explanation."
