# Evidence Audit: Reviewer 2 Question 3

## Scope

Reviewer 2 asks about thresholding a continuous similarity space, continuous similarity measures, the biological interpretation of Restructuring, and dot product versus Jaccard divergence. Work product is limited to this folder.

## Sources Checked

| Source | Use |
|---|---|
| `revision/converted/reviewer2.txt`, lines 59-70 | Original reviewer comment. |
| `revision/new review responses_2026-05-14/SPECIAL_REVIEW_EXPERT_AGENT.md` | Required response rules and isolation rules. |
| `revision/point_by_point/P3_reanalysis/R2_3_continuous_similarity/memo.md` | Prior R2-3 analysis summary and expected values. |
| `Figure_generate/Draft/v5/latex/sections/results.tex`, lines 18, 22, 24 | Current v5 Results text on similarity map, Restructuring, Supplementary Fig. 29, metric robustness, and Jaccard interpretation. |
| `Figure_generate/Draft/v5/latex/supplementary_sections/supplementary_methods.tex`, lines 50-69 and 147 | Current v5 methods text defining dot product/cosine similarity, retention magnitude, PDI, thresholds, boundary sensitivity, and metric interpretation. |
| `Figure_generate/Draft/v5/latex/supplementary_sections/figures.tex`, lines 370-384 | Current v5 Supplementary Figs. 29 and 30 captions. |
| `Figure_generate/Draft/v5/latex/supplementary_sections/extended_data.tex`, lines 18-24 | Current v5 Extended Data Fig. 2 caption. |
| `Postprocessed/processed_Sequences_synthetic.xlsx` | Original processed synthetic ASV relative-abundance table used for response-only recalculation. |
| `Analyzed/processed_CoalescenceEvent_synthetic.xlsx` | Original processed synthetic coalescence event metadata used for response-only recalculation. |
| `figure_code/generate_r2_q3_figure.py` | New self-contained code for this worker's response figure and stats. |
| `figure_code/r2_q3_event_metrics.csv` and `figure_code/r2_q3_summary_stats.csv` | Generated event-level metrics and summary values used in the response. |

## Claim Trace

| Claim or number in response | Source and trace | Audit status |
|---|---|---|
| The reviewer concern is about thresholding continuous similarity, Restructuring interpretation, and dot product versus Jaccard divergence. | `reviewer2.txt`, lines 59-70. | Pass |
| Classification uses retention magnitude $r = \sqrt{u^2+v^2}$ and PDI. | `supplementary_methods.tex`, lines 54-63. | Pass |
| Restructuring threshold is $r^2 \leq 0.5`; Mixture is $r^2 > 0.5$ and $0.25 \leq \mathrm{PDI} \leq 0.75$; CLS/Dominance is $r^2 > 0.5$ and PDI outside that interval. | `supplementary_methods.tex`, line 65. | Pass |
| Threshold rationale: $r^2 = 0.5$ means half of coalesced composition is explained by parental-community vectors; PDI boundaries correspond to about 3:1 contribution ratios. | `supplementary_methods.tex`, line 67. | Pass |
| Continuous distributions and boundary sensitivity are now reported in Supplementary Figs. 29 and 30. | `supplementary_methods.tex`, line 69; `figures.tex`, lines 370-384. | Pass |
| 263 synthetic coalescence events used in response-only nutrient-gradient recalculation. | `figure_code/generate_r2_q3_figure.py`; generated output says "Wrote 263 event records"; `r2_q3_event_metrics.csv` has 263 rows. | Pass |
| Asymmetry differs across media with Kruskal--Wallis $H = 110.71$, $p = 9.12 \times 10^{-25}$. | `figure_code/r2_q3_summary_stats.csv`, row `kruskal_asymmetry`: H 110.708364, p 9.119776e-25. | Pass |
| Median asymmetry values are 0.410, 0.915, and 0.985 for Nutr-, Base medium, and Nutr+. | `figure_code/r2_q3_summary_stats.csv`, rows `continuous_asymmetry`: medians 0.410377, 0.914773, 0.984902. | Pass |
| Retention magnitude differs across media with Kruskal--Wallis $H = 18.05$, $p = 1.21 \times 10^{-4}$. | `figure_code/r2_q3_summary_stats.csv`, row `kruskal_retention_sq`: H 18.046964, p 1.205456e-04. | Pass |
| Median $r^2$ values are 0.792, 0.722, and 0.924 for Nutr-, Base medium, and Nutr+. | `figure_code/r2_q3_summary_stats.csv`, rows `retention_sq`: medians 0.791552, 0.722254, 0.924335. | Pass |
| Restructuring means low parental retention and may reflect new stable composition from cross-community interactions. | Results source says Restructuring denotes low parental retention and may reflect a new stable composition from previously unseen cross-community species interactions, `results.tex`, line 18. Supplementary Methods says residual quantifies novel restructuring, lines 52 and 65. | Pass |
| Boundary: Restructuring does not identify the causal interaction mechanism by itself. | Inference from metric definition in `supplementary_methods.tex`, lines 52, 56, 65. This is a limitation, not an added empirical claim. | Pass |
| Dot product/vector decomposition is abundance-weighted; Jaccard is presence/absence species-identity retention. | `supplementary_methods.tex`, line 147; `extended_data.tex`, line 22. | Pass |
| Nutr- dot-product classification gives 35 CLS, 48 Mixture, 7 Restructuring; Jaccard gives 5 CLS, 55 Mixture, 30 Restructuring. | `figure_code/r2_q3_summary_stats.csv`, rows for Nutr- `dot_product` and `jaccard`. | Pass |
| Base medium and Nutr+ Jaccard divergence should be interpreted cautiously as abundance dominance not requiring full species-list retention. | `figure_code/r2_q3_summary_stats.csv` shows Jaccard shifts many Base and Nutr+ events away from CLS; `supplementary_methods.tex`, line 147 and `extended_data.tex`, line 22 define Jaccard as species-identity retention, not abundance dominance. | Pass |
| Manuscript revised Results, Supplementary Methods, Supplementary Figs. 29 and 30, and Extended Data Fig. 2 caption. | Existing v5 source lines cited above contain `\rev{}` additions. | Pass |

## Figure Audit

| Figure | Path | Code | Data | Notes |
|---|---|---|---|---|
| Response Fig. R2Q3 | `figures/r2_q3_continuous_similarity_and_metric_divergence.pdf` and `.png` | `figure_code/generate_r2_q3_figure.py` | `processed_Sequences_synthetic.xlsx`, `processed_CoalescenceEvent_synthetic.xlsx` | Single response figure. This stays within the maximum of two figures. |

## Remaining Gaps

No unresolved evidence gaps for this response fragment. The response uses "we revised" only for changes verified in the current v5 source files.
