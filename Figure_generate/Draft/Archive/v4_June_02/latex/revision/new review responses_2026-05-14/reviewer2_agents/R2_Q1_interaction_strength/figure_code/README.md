# Figure Code README

## Purpose

This folder contains the reproducible code for the single response figure used for Reviewer 2 Question 1.

Generated outputs:

- `../figures/r2_q1_nutrient_interaction_feedback.pdf`
- `../figures/r2_q1_nutrient_interaction_feedback.png`

## Why one figure

Only one figure is needed for this question. The reviewer's concern is conceptual framing, not a request for a new analysis. A single compact synthesis is sufficient to show that the manuscript supports increased operational invasion resistance while also acknowledging environmental feedbacks and network restructuring. A second figure would either duplicate existing manuscript figures or imply a new mechanistic decomposition that the available data do not support.

## Script

Run from the assigned worker folder:

```sh
/Users/jysong/miniforge3/bin/python figure_code/make_response_figure.py
```

The default `/opt/homebrew/bin/python3` in this shell does not have matplotlib installed. The miniforge Python environment does.

## Data provenance

The script hard-codes summary values already reported in v4 manuscript sources and revision memos. It does not read prohibited response files and does not perform new statistics.

| Figure panel | Values | Source |
|---|---|---|
| A | Failed invasion frequency: 2, 33, 48%; s.e.m.: 1, 4, 4%. | `Figure_generate/Draft/v4/latex/sections/results.tex`, Fig. 4 text and caption. |
| A | Dominance fractions: 39, 65, 76%; Mixture fractions: 53, 4, 6%. | `Figure_generate/Draft/v4/latex/sections/results.tex`, Fig. 4 text and caption. |
| B | Dominant ASV abundance: 44, 51, 67%; s.e.m.: 2, 5, 4%. | `Figure_generate/Draft/v4/latex/sections/results.tex`, Fig. 5 text. |
| B | Median parental richness: 12, 9, 7.5 ASVs. | `Figure_generate/Draft/v4/latex/sections/results.tex` revised richness text and `point_by_point/P3_reanalysis/R3_2_richness_media/memo.md`. |
| C | Acidic parent win fraction in acid-alk pairs: Base 63.6%, Nutr+ 86.4%; p-values 0.10 and 9.4e-7. | `point_by_point/P3_reanalysis/R1_2_pH_dominance/memo.md` and `Figure_generate/Draft/v4/latex/sections/results.tex` pH paragraph. |

## Output interpretation

Panel A supports the operational claim that invasion resistance and Dominance increase across the nutrient gradient. Panel B shows that enrichment also changes community structure, so nutrient concentration is not a pure scalar proxy for pairwise coefficients. Panel C shows that pH-mediated environmental feedbacks may contribute to winner identity in Nutr+, while not explaining Dominance frequency by themselves.
