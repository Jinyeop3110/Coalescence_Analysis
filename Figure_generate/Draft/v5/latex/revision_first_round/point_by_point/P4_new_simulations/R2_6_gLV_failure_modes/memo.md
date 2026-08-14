# P4.X — gLV Failure Modes and Unexplained Data Features

## Reviewer / Source
- Reviewer 2, Point #6 (model framing)
- PI discussion note 04/17: "Provide gLV failure modes clearly" and "Show aspects of data not explained by model."

## Status
- NOT STARTED
- Confidence: 85%

## Why This Exists
The current revision materials emphasize where gLV succeeds. For scientific balance and stronger reviewer-facing framing, we should also document where the model does not capture the data well.

## Core Question
Which empirical patterns are captured poorly or not at all by the competition-only gLV framework?

## Candidate Failure Modes to Test
1. pH-mediated asymmetry in Nutr+ stronger than gLV would predict
2. Natural-community Restructuring fraction exceeds model expectation
3. Metric sensitivity and rare-taxon structure not reproduced by gLV
4. Dominant-species predictability differs between Base and Nutr+ in a way not naturally encoded by random-interaction gLV
5. Any systematic mismatch in richness, overlap, or retention distributions

## Proposed Analysis
1. Build a table of "successes vs failures" for the model.
2. Compare experiment and simulation across several summary statistics, not just Dominance frequency.
3. Quantify mismatches and identify whether they point specifically toward environmental mediation, facilitation, or higher-order effects.

## Suggested Outputs
- Summary panel or table: experiment vs gLV across metrics
- Residual plots for key summary statistics
- Text box listing what the model captures and what it misses

## Candidate Figure Names
- `Fig_R2_6_glv_successes_failures`
- `Fig_R2_6_experiment_vs_model_residuals`

## Possible Interpretation
- This is a high-value honesty figure: it makes the phenomenological framing much more credible.
- It also creates a clean bridge to alternative models without undermining the central result that interaction strength matters.

## Code Location
- Suggested folder: `Figure_generate/code/Figure_revision/R2_6_gLV_failure_modes/`

## Changes to Manuscript
- Add a concise paragraph in Results or Discussion on where gLV succeeds and fails.
- Use this to support the statement that gLV is a useful baseline, not a complete mechanistic account.
