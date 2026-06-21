# Evidence Audit: Reviewer 2, Question 2

Scope: Evidence for community-level selection, alternative mechanisms, and failed-invasion/invasion-fitness framing.

## Reviewer Source

- Reviewer 2 Q2 comment: `Figure_generate/Draft/v4/latex/revision/converted/reviewer2.txt`, lines 44-58.

## Claim Trace

| Claim in response | Source | Audit status |
|---|---|---|
| Dominance and origin-correlated persistence are not uniquely diagnostic of one mechanism; CLS is now defined operationally. | `sections/results.tex`, line 18 defines CLS as origin-correlated persistence and states that the definition is mechanism-agnostic. `sections/discussion.tex`, line 16 repeats this boundary and cites `Mansour2018,Rillig2015`. | Pass |
| Alternative mechanisms now discussed: shared environmental tolerances, correlated traits, environmental filtering, pH modification by dominant taxa. | `sections/results.tex`, line 18; `sections/discussion.tex`, line 16. | Pass |
| Nutr+ is framed as a top-down route involving pH-modifying dominant taxa. | `sections/results.tex`, lines 98 and 102; `sections/discussion.tex`, lines 8 and 16. | Pass |
| Dominant-species competition predicts winner identity more strongly in Nutr+ than Base. | `sections/results.tex`, lines 98-109: Fig. 5C reports `R^2 = 0.11` in Base and `R^2 = 0.49` in Nutr+. | Pass |
| pH mismatch alone does not significantly increase Dominance frequency within Base or Nutr+. | `sections/results.tex`, line 102: Fisher's exact test `p = 0.49` in Base and `p = 0.47` in Nutr+. `supplementary_sections/figures.tex`, lines 420-425 describe Supplementary Fig. 34. | Pass |
| Among acid-alk pairs, acidic parental communities win most Nutr+ events. | `sections/results.tex`, line 102: 38/44 events, 86.4%, binomial `p = 9.4 x 10^-7`; Supplementary Fig. 34 caption in `supplementary_sections/figures.tex`, lines 420-425. | Pass |
| Base and Nutr+ show significant within-community pairwise selection correlation relative to cross-community correlation; Nutr- lacks it. | `sections/results.tex`, line 81: Base and Nutr+ `P < 0.001`, Nutr- no such correlation, Extended Data Fig. 6. `supplementary_sections/pairwise_selection_correlation.tex`, lines 7-11 define and interpret the metric. | Pass |
| gLV model lacks explicit environmental filtering/pH and uses identical growth rates; it can generate Dominance and positive pairwise selection correlation. | `sections/results.tex`, lines 37-46: `r_i = 1`, gLV model framing, 61% Dominance at `mu = 0.6`, positive same-parent and negative cross-parent pairwise selection correlation. `supplementary_sections/supplementary_methods.tex`, line 83 states the model does not represent pH or environmental variables. | Pass |
| Dominant-species-removal analysis reduces but does not eliminate Nutr+ association. | `sections/results.tex`, line 100: Spearman `rho = 0.41--0.42`, `p <= 1.3 x 10^-3`, Supplementary Fig. 31. `supplementary_sections/figures.tex`, lines 390-391 caption and label the control. | Pass |
| Assembly history comparison supports effect of pre-assembly. | `sections/discussion.tex`, line 16 cites Extended Data Fig. 7 and Supplementary Fig. 19. `supplementary_sections/assembly_effect.tex`, line 13 and `supplementary_sections/figures.tex`, lines 286-287 describe Supplementary Fig. 19. | Pass |
| Failed invasion assay design: resident:invader at 95:5, seven daily dilution cycles, failed if invader remains below 1%. | `sections/methods.tex`, lines 51-53; `supplementary_sections/invasion.tex`, lines 7-9; `supplementary_sections/supplementary_methods.tex`, lines 96-98. | Pass |
| Failed invasion frequency increases with nutrient supply: Nutr- `2 +/- 1%`, Base `33 +/- 4%`, Nutr+ `48 +/- 4%`. | `sections/results.tex`, lines 79 and 87; Fig. 4B caption. | Pass |
| Failed invasion is reframed as invasion resistance, not a direct formal invasion-fitness measurement. | `sections/discussion.tex`, line 18 states the nutrient-dependent increase in invasion resistance and describes non-mutually exclusive processes. `supplementary_sections/pairwise_selection_correlation.tex`, lines 13-16 defines invasion fitness and states the empirical assays approximate two-species invasion fitness at 5% initial invader frequency. | Pass |
| Supplementary invasion-fitness analysis: excess same-parent concordance tracks `mu` with Pearson `r = 0.870`, `p = 3.2 x 10^-8`. | `supplementary_sections/pairwise_selection_correlation.tex`, line 16; `supplementary_sections/figures.tex`, lines 362-367; memo `point_by_point/P4_new_simulations/R2_4_invasion_fitness/memo.md`. | Pass |
| Manuscript changes claimed in `\mschange{...}` exist. | Results changes: `sections/results.tex`, lines 18 and 46. Discussion changes: `sections/discussion.tex`, lines 16 and 18. Methods: `sections/methods.tex`, lines 51-53. Supplementary Note 4: `supplementary_sections/pairwise_selection_correlation.tex`, lines 13-16 and Supplementary Fig. 28 in `supplementary_sections/figures.tex`, lines 362-367. | Pass |

## Evidence Boundaries

- The response does not claim that Dominance plus correlated persistence uniquely identifies direct interspecies competition.
- The response does not claim that the 5% empirical pairwise invasion assay is a formal rare-invader fitness measurement.
- The response treats pH-mediated environmental modification as a supported mechanism in Nutr+, not as a rejected alternative.
- The response treats the gLV model as a sufficiency result for competitive interaction structure, not as proof that pH or shared traits are absent from experiments.

## Figures

No new response-only figure was generated for this question. Existing manuscript and supplementary figures already contain the relevant evidence: Fig. 4B, Fig. 5C, Extended Data Figs. 6-7, Supplementary Figs. 19, 28, 31, and 34.
