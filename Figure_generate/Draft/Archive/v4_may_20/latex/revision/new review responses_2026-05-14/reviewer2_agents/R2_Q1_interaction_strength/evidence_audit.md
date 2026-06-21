# Evidence Audit: Reviewer 2 Q1

## Scope

Question: Relationship between nutrient enrichment and "interaction strength."

Reviewer source: `Figure_generate/Draft/v4/latex/revision/converted/reviewer2.txt`, lines 20-42.

Off-limits folder check: no file inside `Figure_generate/Draft/v4/latex/revision/response/` was read, diffed, copied, or edited.

## Claims and Sources

| Claim in response | Source | Status |
|---|---|---|
| The reviewer asks whether enrichment is being used too simply as a proxy for pairwise interaction strength. | `converted/reviewer2.txt`, lines 20-42. | Traceable |
| gLV parameter `mu` is a phenomenological model parameter, not a mechanistic biochemical model. | `sections/results.tex`, line 42; `supplementary_sections/supplementary_methods.tex`, line 83. | Traceable |
| Pairwise failed-invasion frequency is used as an operational proxy for interaction intensity in the experiment. | `sections/results.tex`, line 79; `supplementary_sections/supplementary_methods.tex`, line 98. | Traceable |
| Failed-invasion frequency values are Nutr-: `2 \pm 1%`, Base: `33 \pm 4%`, Nutr+: `48 \pm 4%`. | `sections/results.tex`, lines 79 and 87. | Traceable |
| Dominance frequency values are Nutr-: 39%, Base: 65%, Nutr+: 76%; Mixture is 53%, 4%, and 6%. | `sections/results.tex`, lines 81 and 87. | Traceable |
| Species richness decreases with enrichment, with median parental richness 12, 9, and 7.5 ASVs. | `sections/results.tex`, line 81; `point_by_point/P3_reanalysis/R3_2_richness_media/memo.md`, key results. | Traceable |
| Higher-OD parental communities do not explain Dominance direction in Base and Nutr+. | `sections/results.tex`, line 81; `supplementary_sections/figures.tex`, lines 402-417. | Traceable |
| Dominant ASV abundance increases from `44 \pm 2%` to `51 \pm 5%` to `67 \pm 4%`. | `sections/results.tex`, line 98. | Traceable |
| Dominant-species predictability is weak in Base and stronger in Nutr+, with `R^2 = 0.11` and `R^2 = 0.49`. | `sections/results.tex`, line 98. | Traceable |
| Dominant taxa include strong pH modifiers and dominant pH-modifying taxa predict community pH. | `sections/results.tex`, line 102; `supplementary_sections/figures.tex`, lines 115-128. | Traceable |
| pH mismatch alone does not significantly increase Dominance frequency in Base or Nutr+, with Fisher's exact test `p = 0.49` and `p = 0.47`. | `sections/results.tex`, line 102; `supplementary_sections/figures.tex`, lines 420-425; `point_by_point/P3_reanalysis/R1_2_pH_dominance/memo.md`, key results. | Traceable |
| Within acid-alk pairs, acidic parent wins 38/44 Nutr+ events, 86.4%, binomial `p = 9.4e-7`; Base is 28/44, 63.6%, binomial `p = 0.10`. | `sections/results.tex`, line 102; `point_by_point/P3_reanalysis/R1_2_pH_dominance/memo.md`, key results. | Traceable |
| The current Discussion acknowledges the nutrient-to-`mu` mapping is approximate and may reflect resource competition, metabolic activity, pH shifts, and competition-facilitation balance. | `sections/discussion.tex`, line 18. | Traceable |
| Community-level selection is now framed as origin-correlated persistence, not one exclusive biochemical mechanism. | `sections/results.tex`, first Results paragraph, and `sections/discussion.tex`, line 16. | Traceable |
| Goldford et al. 2018 and Estrela et al. 2021 are present in the bibliography. | `references.bib`, lines 268-287. | Traceable |
| `DuanPawar2025` is present and explicitly annotated as the reviewer-cited consumer-resource mapping preprint. | `references.bib`, lines 858-869. | Traceable |

## Figure Audit

Generated figure: `figures/r2_q1_nutrient_interaction_feedback.pdf` and `.png`.

Generating code: `figure_code/make_response_figure.py`.

The figure contains no new statistical analysis. It summarizes traced values:

| Panel | Values | Source |
|---|---|---|
| A | Failed invasions: 2, 33, 48%; Dominance: 39, 65, 76%; Mixture: 53, 4, 6%. | `sections/results.tex`, lines 79, 81, 87. |
| B | Dominant ASV abundance: 44, 51, 67%; median parental richness: 12, 9, 7.5 ASVs. | `sections/results.tex`, lines 81 and 98. |
| C | Acidic parent wins acid-alk pairs: Base 63.6%, Nutr+ 86.4%; p-values 0.10 and 9.4e-7. | `point_by_point/P3_reanalysis/R1_2_pH_dominance/memo.md`; `sections/results.tex`, line 102. |

## Manuscript-Change Claims

| Response statement | Source or patch |
|---|---|
| Results and Supplementary Methods frame gLV as phenomenological. | Already present: `sections/results.tex`, line 42; `supplementary_sections/supplementary_methods.tex`, line 83. |
| Discussion states the nutrient-to-`mu` mapping is approximate and lists multiple mechanisms. | Already present: `sections/discussion.tex`, line 18. |
| Proposed replacement of direct "nutrient-dependent interaction strength" language. | See `proposed_v4_patches.md`; not applied by this worker. |
| Proposed citation of `Goldford2018`, `Estrela2021`, and `DuanPawar2025` in the caveat paragraph. | See `proposed_v4_patches.md`; references already exist in `references.bib`. |

## Evidence Limits

The response does not claim that nutrient supply maps monotonically to effective pairwise Lotka--Volterra coefficients. The available data support increased operational invasion resistance and altered coalescence outcomes across the nutrient gradient, plus a Nutr+ pH-mediated route for winner identity. They do not uniquely decompose the nutrient effect into resource competition, pH feedbacks, carrying-capacity changes, metabolic rate changes, and facilitation.
