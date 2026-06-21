# Pairwise Correlation Figure Same-Style Previews

This folder contains a standalone preview workflow for regenerating pairwise selection correlation panels discussed in R1-8 using the same visual style as the current manuscript figures.

Run from this folder:

```sh
python make_pairwise_correlation_same_style.py
```

Outputs are written back into this folder:

- `Fig2D/simulation_pairwise_correlation_same_style.pdf/png`: same-style simulation `mu=0.6` Fig. 2D preview panel.
- `Fig2D/experiment_pairwise_correlation_same_style.pdf/png`: same-style experimental Base Fig. 2D preview panel.
- `pairwise_correlation_simulation_all_same_style.pdf/png`: same-style simulation panels for `mu=0.3`, `0.6`, and `0.8`.
- `pairwise_correlation_experiment_all_same_style.pdf/png`: same-style experimental panels for Nutr-, Base, and Nutr+.
- `pairwise_correlation_same_style_summary.csv`: summary values used in the plots.

The Fig. 2D panels use a narrow embedded-panel size, smaller square mean markers than the earlier preview, and separate y-axis limits for simulation and experiment.

The active manuscript figures are not overwritten by this preview script.
