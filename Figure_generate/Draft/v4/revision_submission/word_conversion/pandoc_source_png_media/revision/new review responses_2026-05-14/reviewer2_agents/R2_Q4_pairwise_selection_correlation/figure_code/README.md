# Figure Code: R2-Q4 Pairwise Selection Correlation

This folder contains independent code for the Reviewer 2, Question 4 response-support figure.

## Generated Figure

One figure was generated:

`../figures/R2_Q4_invasion_concordance.pdf`

The figure links pairwise selection correlation to invasion fitness in the gLV framework. For each ordered pair of assembled communities in the archived full-matrix simulation dataset, the script computes each source-community survivor's rare-invader growth rate into the target-community equilibrium,

```text
lambda_i = g_i * (1 - sum_j alpha_ij x_j / k_i)
```

It then measures whether source-community species pairs have concordant invasion outcomes more often than expected if each species invaded independently with the observed success probability.

## Why Only One Figure

A second figure is not needed for this question. The reviewer asked for conceptual clarification and a gLV invasion-fitness link, and the single figure covers the required quantitative bridge: same-parent invasion concordance, its null expectation, and the excess concordance trend across interaction strength.

## Reproduction

Run from the assigned folder:

```sh
/Users/jysong/miniforge3/bin/python figure_code/make_invasion_concordance_figure.py
```

Outputs:

```text
../figures/R2_Q4_invasion_concordance.pdf
../figures/R2_Q4_invasion_concordance.png
../figures/invasion_concordance_summary.csv
../figures/invasion_concordance_summary.json
```

The default data source is:

`/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json`

The generated summary reports Pearson `r = 0.8704534994664044`, `p = 3.224981618532111e-08` for excess concordance versus `mu`.
