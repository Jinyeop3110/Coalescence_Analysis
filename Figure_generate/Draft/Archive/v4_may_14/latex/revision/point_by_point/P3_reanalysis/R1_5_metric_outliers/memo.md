# P3.X — Why Jensen-Shannon and Jaccard Behave as Outlier Metrics

## Reviewer / Source
- Reviewer 1, Point #5
- PI discussion note 04/17: "Additional analysis if possible: why are they outliers?"

## Status
- NOT STARTED
- Confidence: 85%

## Why This Exists
The manuscript already softens the claim that classification is robust across metrics. This memo tracks a deeper follow-up analysis: explain why Jensen-Shannon divergence and Jaccard index produce different outcome rankings from vector decomposition, Euclidean distance, and Bray-Curtis.

## Core Question
What feature of the data causes Jensen-Shannon and Jaccard to disagree with the main metric family?

## Proposed Analysis
1. Compare event-by-event classifications across metrics.
2. Identify the subset of events that switch labels under JS or Jaccard.
3. Test whether switched events are characterized by:
   - low total retention
   - many low-abundance taxa
   - shared rare ASVs
   - low richness / high richness
   - strong or weak parental overlap
4. Quantify whether JS/Jaccard are especially sensitive to rare taxa or presence/absence structure.
5. If possible, add a schematic showing how cosine/vector-decomposition vs Jaccard weight abundance information differently.

## Suggested Outputs
- Confusion matrices between metrics
- Event-level scatter of "main metric" vs "outlier metric" scores
- Feature comparison of switched vs stable events
- Short interpretive note: abundance-sensitive vs presence/absence-sensitive metrics

## Candidate Figure Names
- `Fig_R1_5_metric_confusion`
- `Fig_R1_5_switched_events_features`

## Possible Interpretation
- This analysis could turn a weakness into a strength by showing that the disagreement is biologically interpretable rather than arbitrary.
- Likely conclusion: Jaccard and JS overweight low-abundance or presence/absence structure compared with abundance-weighted parental retention.

## Code Location
- Suggested folder: `Figure_generate/code/Figure_revision/R1_5_metric_outliers/`

## Changes to Manuscript
- Add a brief explanatory sentence after the robustness caveat.
- Potentially add a supplementary figure explaining why JS/Jaccard differ.
