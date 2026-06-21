# P4.X — "Acidic Always Wins" pH Rule vs gLV Predictions

## Reviewer / Source
- PI discussion note 04/17: "Pure pH model -> acidic pH wins. Does this contradict gLV?"
- Related to Reviewer 2's alternative-mechanism concern

## Status
- NOT STARTED
- Confidence: 75%

## Why This Exists
The current manuscript discusses a top-down pH-mediated regime in Nutr+, but it does not explicitly test whether a very simple pH rule already explains the outcomes. This memo tracks a direct comparison between a naive pH rule and the broader gLV interpretation.

## Core Question
How much of the data can be explained by a simple rule such as "the more acidic parental community wins," and where does that rule fail?

## Proposed Analysis
1. Define a simple pH-only predictor at the community level:
   - acidic community wins
   - or larger `|delta pH|` predicts stronger one-sided outcomes
2. Compare prediction accuracy across media:
   - Nutr-
   - Base
   - Nutr+
3. Compare pH-rule accuracy against:
   - dominant-species pairwise-assay predictor
   - gLV-inspired interaction-strength framing
4. Identify failure cases:
   - events where acidic parent loses
   - same-pH cases with clear Dominance
   - strong Dominance without large pH difference

## Suggested Outputs
- Confusion matrix or prediction-accuracy summary for pH-only rule
- Medium-stratified performance
- Side-by-side figure: pH-only rule vs observed outcomes

## Candidate Figure Names
- `Fig_R2_2_ph_rule_accuracy`
- `Fig_R2_2_ph_rule_failure_cases`

## Possible Interpretation
- If the pH-only rule works only in Nutr+, that would support the paper's "top-down regime" claim without replacing the gLV story.
- If it works broadly, the manuscript should more explicitly acknowledge that environment-mediated filtering may explain a substantial part of the signal.

## Code Location
- Suggested folder: `Figure_generate/code/Figure_revision/R2_2_acidic_always_wins_vs_gLV/`

## Changes to Manuscript
- Add an explicit sentence on where pH-only reasoning succeeds and fails.
- Use this to sharpen the distinction between Base and Nutr+ mechanistic regimes.
