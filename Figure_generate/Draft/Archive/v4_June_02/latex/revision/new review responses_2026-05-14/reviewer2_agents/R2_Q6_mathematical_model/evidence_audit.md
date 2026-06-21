# Evidence Audit: Reviewer 2, Question 6

## Scope

This audit covers only Reviewer 2, Question 6: mathematical model framing, competitive-only gLV limitation, environmental mediation such as pH, biological interpretation of interaction coefficient distributions, and interpretation of mean interaction strength `\mu`.

## Source Comment

- Reviewer source: `revision/converted/reviewer2.txt`, lines 93-99.
- Comment summary: reviewer accepts gLV as a useful minimal framework but asks that it be framed as phenomenological, that competitive-only and pH/environmental omissions be explicit, and that coefficient distributions and `\mu` receive biological interpretation.

## Claims and Traceability

| Claim in response | Source | Audit status |
|---|---|---|
| The gLV model should be framed as phenomenological rather than as a complete mechanistic account. | `sections/results.tex` line 42: revised text says the gLV model is a phenomenological framework and not a mechanistic model of pH modification, metabolic cross-feeding, or carrying-capacity variation. | Pass |
| The model uses gLV equations with growth, self-interaction, and off-diagonal coefficients. | `sections/results.tex` lines 38-42; `sections/methods.tex` lines 43-46; `supplementary_sections/supplementary_methods.tex` lines 78-83. | Pass |
| Off-diagonal coefficients are drawn from `U(0, 2\mu)` and `\mu` is the mean interaction strength in the model. | `sections/results.tex` line 42; `sections/methods.tex` line 46; `supplementary_sections/supplementary_methods.tex` line 83. | Pass |
| `\alpha_{ij}` is an effective per-capita inhibitory term, and it can absorb direct and indirect inhibitory mechanisms but does not identify biochemical mechanisms. | `supplementary_sections/supplementary_methods.tex` line 83. | Pass |
| The model does not dynamically represent pH or other environmental state variables. | `supplementary_sections/supplementary_methods.tex` line 83; `sections/results.tex` line 42. | Pass |
| The model is competitive-only because `\alpha_{ij} >= 0`; facilitative interactions such as cross-feeding are not represented. | `supplementary_sections/supplementary_methods.tex` line 83; `sections/discussion.tex` line 22. | Pass |
| Alternative coefficient distributions are phenomenological ensembles rather than fitted biochemical distributions. | `supplementary_sections/supplementary_methods.tex` line 83. | Pass |
| Distribution robustness compared uniform, Gaussian, and Gamma distributions with matched mean and variance. | `supplementary_sections/simulations.tex` line 7; `supplementary_sections/supplementary_methods.tex` line 149; `supplementary_sections/figures.tex` lines 62-74. | Pass |
| Robustness result: qualitative transition from Mixture-dominated to Dominance/Restructuring outcomes was robust across the tested coefficient distributions. | `supplementary_sections/simulations.tex` line 7; `supplementary_sections/supplementary_methods.tex` line 149; `supplementary_sections/figures.tex` line 74. | Pass |
| Competition-only gLV is sufficient to reproduce frequent Dominance at `\mu = 0.6` with 61% Dominance, 26% Restructuring, and 13% Mixture. | `sections/results.tex` line 44; Fig. 2 caption at `sections/results.tex` line 53. | Pass |
| Assembly filters species into mutually weakly competing groups and produces coupled fates. | `sections/results.tex` line 46; Supplementary Fig. 27 caption at `supplementary_sections/figures.tex` lines 354-359. | Pass |
| Supplementary Fig. 27 values: within-community coefficients mean 0.389, between-community mean 0.500 for `\mu = 0.50`, Mann-Whitney `p < 0.001`. | `supplementary_sections/figures.tex` line 358. | Pass |
| Nutrient enrichment is not a direct measurement of `\mu`; the mapping is approximate and reflects net interaction intensity. | `sections/discussion.tex` line 18. | Pass |
| In the baseline competitive ensemble, `\mu` is a single minimal parameter that shifts coefficients away from zero and broadens their sampled range; the mean-vs-variance sweep shows coefficient mean alone is not sufficient, while both mean and spread contribute to high-Dominance regimes. | `supplementary_sections/supplementary_methods.tex` line 83; `supplementary_sections/simulations.tex` line 17; Reviewer 3 response R3-4 mean-vs-variance paragraph. | Pass |
| Failed pairwise invasion fractions across nutrient conditions are Nutr- `2 +/- 1%`, Base `33 +/- 4%`, Nutr+ `48 +/- 4%`. | `sections/results.tex` line 79; Fig. 4 caption at `sections/results.tex` line 87. | Pass |
| Nutrient-dependent interaction intensity may reflect several processes, including resource competition, metabolic activity, pH shifts, and competition-facilitation balance. | `sections/discussion.tex` line 18. | Pass |
| pH modification may contribute to winner identity in Nutr+, but pH mismatch alone does not explain Dominance frequency. | `sections/results.tex` line 102; `sections/discussion.tex` line 8. | Pass |
| pH mismatch did not significantly increase Dominance frequency within Base or Nutr+. | `sections/results.tex` line 102: Fisher exact tests `p = 0.49` in Base and `p = 0.47` in Nutr+. | Pass |
| Acidic parental communities won 38/44 acid-alkaline Nutr+ events, 86.4%, binomial `p = 9.4 x 10^{-7}`. | `sections/results.tex` line 102; Supplementary Fig. 37 caption at `supplementary_sections/figures.tex` lines 434-440. | Pass |
| No new figure was generated for this response. | Decision by this worker; rationale recorded in `figure_code/README.md`. | Pass |

## Manuscript-Change Claims

| Response statement | Source | Audit status |
|---|---|---|
| "We revised the Results..." | `sections/results.tex` line 42 contains `\rev{}` text adding phenomenological model framing. | Pass |
| "We revised the Supplementary Methods..." | `supplementary_sections/supplementary_methods.tex` line 83 contains `\rev{}` text defining effective coefficients, competitive-only limitation, `\mu`, and distribution interpretation. | Pass |
| "We revised the Discussion..." | `sections/discussion.tex` line 18 contains `\rev{}` text on approximate nutrient-to-`\mu` mapping and possible mechanisms; line 22 notes competitive model and facilitation limitation. | Pass |

## Evidence Gaps or Limitations

- The response should not claim that `\mu` is a mechanistic resource-supply parameter. The manuscript supports only an effective interaction-intensity interpretation.
- The response should not claim that pH is dynamically represented in gLV. The Supplementary Methods explicitly say pH and other environmental state variables are not dynamically modeled.
- The response should not claim that facilitation was fully analyzed. The Discussion only supports a limited caveat that systems with substantial mutualism or facilitation may behave differently.
