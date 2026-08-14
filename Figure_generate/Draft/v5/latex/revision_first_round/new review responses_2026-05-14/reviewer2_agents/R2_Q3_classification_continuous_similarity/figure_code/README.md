# Figure Code: Reviewer 2 Question 3

## Purpose

Generate one response-only figure for Reviewer 2 Question 3. The figure shows:

1. Continuous similarity coordinates for each synthetic coalescence event.
2. Outcome-fraction divergence between the manuscript dot-product/vector-decomposition classification and a Jaccard presence/absence classification.

Only one figure is generated because it covers both visual needs for this response: continuous similarity structure and dot product versus Jaccard divergence. A second figure would duplicate Supplementary Figs. 29 and 30, which already exist in the v5 supplement.

## Inputs

The script reads the original processed data files:

- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Postprocessed/processed_Sequences_synthetic.xlsx`
- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Analyzed/processed_CoalescenceEvent_synthetic.xlsx`

## Outputs

- `../figures/r2_q3_continuous_similarity_and_metric_divergence.pdf`
- `../figures/r2_q3_continuous_similarity_and_metric_divergence.png`
- `r2_q3_event_metrics.csv`
- `r2_q3_summary_stats.csv`

## Reproduction

From this assigned worker folder:

```sh
python figure_code/generate_r2_q3_figure.py
```

The script is self-contained in this folder and does not import another worker's figure code.
