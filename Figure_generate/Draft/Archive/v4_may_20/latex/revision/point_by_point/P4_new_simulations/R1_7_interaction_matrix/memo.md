# P4.2 — Interaction Matrix After Assembly

## Reviewer: R1, Point #7 (Minor)
## Status: COMPLETED
## Confidence: 95%

### Reviewer Comment
"Fig. 2A: Show interaction matrix after assembly (block structure)"

### What They Want
The reviewer expects that after community assembly, the surviving species' interaction matrix should show block structure — strong within-community interactions, weak between-community interactions. This is the ecological basis for Dominance.

### Analysis Performed
Script: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/plot_interaction_matrix.py`

1. Used `48species_10reps_fine_WITH_MATRICES` dataset (contains full 48x48
   interaction matrices, growth rates, carrying capacities).
2. At mu=0.50, extracted surviving species from two assembled communities.
3. Reordered interaction submatrix by community membership (A-only, shared, B-only).
4. Visualized as heatmap with block boundaries.
5. Computed within-community vs between-community interaction statistics
   across all repetitions.
6. Extended analysis across all mu values (0.05 to 1.20).

### Key Results

**At mu=0.50 (example rep):**
- Community A: 7 survivors, Community B: 7 survivors, 0 shared
- Within-community mean interaction (off-diagonal): 0.384
- Between-community mean interaction: 0.544
- Pool mean (mu): 0.50

**Across all reps at mu=0.50:**
- Within-community: mean = 0.389 +/- 0.078
- Between-community: mean = 0.500 +/- 0.046

**Multi-mu analysis:**
- Within-community interactions are consistently LOWER than between-community
  interactions and lower than the pool mean mu.
- This is because assembly filters out species pairs with strong mutual competition.
- The ratio between/within increases with mu, showing stronger block structure
  at higher interaction strengths.

### Conclusion
Assembly creates structured interaction matrices: surviving species within a
community tend to have weaker mutual interactions than cross-community pairs.
This "competitive exclusion within, random between" structure is the ecological
mechanism behind Dominance during coalescence.

### Output Figures
- `interaction_matrix_assembly.{svg,pdf,png}` — 3-panel (before assembly,
  after assembly heatmap, within vs between box plot)
- `interaction_matrix_mu_comparison.{svg,pdf,png}` — within vs between
  interaction means across all mu values

### Code Location
`Figure_generate/code/Figure_revision/R1_7_interaction_matrix/plot_interaction_matrix.py`

### Changes to Manuscript
- New panel in Fig. 2 or new Supplementary Figure showing block structure
- Brief mention in Results: "Assembly creates structured interaction matrices
  where within-community competition is filtered below the pool mean, while
  between-community interactions remain near mu."
