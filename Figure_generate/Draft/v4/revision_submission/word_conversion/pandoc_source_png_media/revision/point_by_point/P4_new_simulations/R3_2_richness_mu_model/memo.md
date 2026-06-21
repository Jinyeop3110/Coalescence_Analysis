# P4.1 — Richness vs mu in Model (Richness-Dominance Confound)

## Reviewer: R3, Point #2 (Critical, part b)
## Status: COMPLETED
## Confidence: 90%

### Reviewer Comment
"Increasing mu reduces richness, which geometrically increases Dominance — confound. Show richness vs mu in model; compare Dominance increase to null expectation from richness decrease alone."

### Why This Matters
If stronger competition (larger mu) simply kills off more species, lower richness might make Dominance classification geometrically easier (fewer dimensions = vectors more likely to align). The observed Dominance increase with mu could be a statistical artifact, not an ecological effect.

### Analysis Performed
Script: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/analyze_richness_mu.py`

1. Used existing simulation data (200 reps x 24 mu values, from
   `Simulation_Data/48species_200reps_fine/Community_200reps_fine.json`).
2. Computed richness and Dominance fraction at each mu.
3. Built a **composition-matched geometric null model**:
   - Samples two observed abundance vectors from the same mu.
   - Randomly permutes species labels independently (breaking ecological identity).
   - Averages the permuted vectors and classifies the outcome.
   - This preserves abundance unevenness while removing species-specific structure.

### Key Results

| mu   | SC Richness | Dom (observed) | Dom (null) | Excess Dom |
|------|-------------|----------------|------------|------------|
| 0.05 | 12.0        | 0.000          | 0.000      | 0.000      |
| 0.30 | 9.7         | 0.204          | 0.000      | 0.204      |
| 0.50 | 6.2         | 0.532          | 0.006      | 0.526      |
| 0.70 | 4.4         | 0.592          | 0.114      | 0.478      |
| 1.00 | 3.1         | 0.704          | 0.270      | 0.434      |
| 1.20 | 2.5         | 0.773          | 0.345      | 0.429      |

- At high mu, composition unevenness alone accounts for ~35% Dominance.
- Observed Dominance is ~77%, yielding ~43% excess Dominance.
- Correlation of excess Dominance with mu: r=0.695, p=1.65e-04.
- Mean excess Dominance for mu >= 0.3: **0.452** (45.2 percentage points).

### Conclusion
Reduced richness and increased composition unevenness contribute modestly
to Dominance at high mu, but the **majority** of Dominance (excess ~45%)
is driven by ecological assembly structure — the specific species identities
and interaction relationships created during assembly. This goes well beyond
a simple geometric effect of lower richness.

### Output Figures
- `richness_mu_analysis.{svg,pdf,png}` — 3-panel (richness, Dom obs vs null, excess)
- `richness_mu_stacked.{svg,pdf,png}` — Stacked phase diagrams (observed vs null)

### Code Location
`Figure_generate/code/Figure_revision/R3_2_richness_mu_model/analyze_richness_mu.py`

### Changes to Manuscript
- New Extended Data Figure or Supplementary Figure
- Add paragraph in Results or Supplementary Note addressing the confound:
  "While reduced richness at high mu contributes to Dominance through composition
  unevenness, a composition-matched null model shows that ~45% of observed
  Dominance is attributable to ecological assembly structure rather than geometric
  effects of richness alone."
