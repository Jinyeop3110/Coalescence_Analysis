# P3.X — Dimensionality-Adjusted Dominance Thresholds

## Reviewer / Source
- Reviewer 3, Point #1
- PI discussion note 04/17: dimensionality concern remains important beyond the additive null

## Status
- NOT STARTED
- Confidence: 75%

## Why This Exists
The additive-null analysis addresses a major part of Reviewer 3's concern, but the notes also propose a second response: adjust classification boundaries based on effective dimensionality so that low-diversity communities are not unfairly pushed toward Dominance by geometry alone.

## Core Question
Do the qualitative conclusions survive if Dominance thresholds are rescaled by community effective dimensionality?

## Proposed Analysis
1. Define effective dimensionality using inverse Simpson diversity or another justified `N_eff`.
2. Construct a dimensionality-adjusted asymmetry threshold, potentially scaling with `1 / sqrt(N_eff)`.
3. Reclassify events under adjusted thresholds.
4. Compare:
   - overall Dominance / Mixture / Restructuring fractions
   - medium dependence
   - simulation dependence on `mu`
   - agreement with original classification
5. Benchmark adjusted-threshold results against the additive-null analysis already completed.

## Suggested Outputs
- Schematic of fixed vs adjusted classification boundaries
- Dominance fraction under original and adjusted thresholds
- Per-medium comparison
- Sensitivity sweep across several threshold-scaling choices

## Candidate Figure Names
- `Fig_R3_1_dimensionality_adjusted_boundaries`
- `Fig_R3_1_threshold_scaling_sensitivity`

## Possible Interpretation
- If the nutrient and `mu` trends remain strong, this provides a second, independent answer to the geometric-artifact critique.
- If results weaken substantially, the manuscript should present the additive-null result as the primary defense and discuss threshold sensitivity more carefully.

## Code Location
- Suggested folder: `Figure_generate/code/Figure_revision/R3_1_dimensionality_adjusted_thresholds/`

## Changes to Manuscript
- Add as a supplementary robustness analysis if successful.
- Mention explicitly as a response to Reviewer 3's dimensionality concern.
