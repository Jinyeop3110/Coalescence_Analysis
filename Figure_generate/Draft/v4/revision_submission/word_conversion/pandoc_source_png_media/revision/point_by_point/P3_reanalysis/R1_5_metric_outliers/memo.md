# P3.X — Why Jensen-Shannon and Jaccard Behave as Outlier Metrics

## Reviewer / Source
- Reviewer 1, Point #5
- PI discussion note 04/17: "Additional analysis if possible: why are they outliers?"

## Status
- DONE
- Confidence: 90%

## Why This Exists
The manuscript already softens the claim that classification is robust across metrics. This memo tracks a deeper follow-up analysis: explain why Jensen-Shannon divergence and Jaccard index produce different outcome rankings from vector decomposition, Euclidean distance, and Bray-Curtis.

## Core Question
What feature of the data causes Jensen-Shannon and Jaccard to disagree with the main metric family?

## Analysis Completed

Script:
- `analyze_metric_outliers.py`

Outputs:
- `metric_outlier_event_table.csv`
- `metric_outlier_label_counts.csv`
- `metric_outlier_feature_summary.csv`
- `metric_outlier_summary.md`
- `metric_outlier_audit.pdf`
- `metric_outlier_audit.png`

Scope:
- Base-medium synthetic coalescence events, matching the Extended Data Fig. 2 robustness comparison.
- Existing exclusion list applied.
- Final event count: 83.

## Main Results

Outcome counts:
- Vector decomposition: Dominance 54/83 (65.1%), Mixture 3/83 (3.6%), Restructuring 26/83 (31.3%).
- Euclidean: Dominance 47/83 (56.6%), Mixture 9/83 (10.8%), Restructuring 27/83 (32.5%).
- Bray-Curtis: Dominance 44/83 (53.0%), Mixture 18/83 (21.7%), Restructuring 21/83 (25.3%).
- Jensen-Shannon: Dominance 20/83 (24.1%), Mixture 34/83 (41.0%), Restructuring 29/83 (34.9%).
- Jaccard: Dominance 21/83 (25.3%), Mixture 27/83 (32.5%), Restructuring 35/83 (42.2%).

Event-level disagreement:
- Jensen-Shannon reclassified 35/54 vector-Dominance events (64.8%) as non-Dominance.
- Jaccard reclassified 41/54 vector-Dominance events (75.9%) as non-Dominance.
- For Jaccard, vector-Dominance events that lost the Dominance label had lower retained-abundance skew (median 0.897 vs 1.000; Mann-Whitney p = 0.0062) and much lower retained-richness skew (median 0.333 vs 1.000; p = 0.0040).
- Jensen-Shannon showed the same qualitative direction but weaker feature separation: lost events had lower retained-abundance skew (median 0.897 vs 1.000; p = 0.0795) and higher mix richness (median 8 vs 6; p = 0.0521).
- Rare-taxon abundance did not clearly explain the switch by itself.

## Interpretation

The disagreement is not arbitrary. Vector decomposition, Euclidean distance, and Bray-Curtis remain aligned because they retain quantitative abundance information. Jaccard diverges because it collapses communities to presence/absence, so a coalesced community can be strongly skewed toward one parent by abundance while still retaining comparable numbers of taxa from both parents. Jensen-Shannon is intermediate: it keeps abundance information, but because it evaluates divergence across the full abundance distribution, it can soften the Dominance label when subdominant taxa are redistributed across both parental supports.

This supports the current response-letter framing: Jensen-Shannon and Jaccard are complementary metrics measuring different biological/compositional features, not failed robustness checks for the abundance-weighted Dominance classification.

## Proposed Analysis
1. Compare event-by-event classifications across metrics. DONE.
2. Identify the subset of events that switch labels under JS or Jaccard. DONE.
3. Test whether switched events are characterized by:
   - low total retention
   - many low-abundance taxa
   - shared rare ASVs
   - low richness / high richness
   - strong or weak parental overlap
   DONE for retained abundance skew, retained richness skew, mix richness, retained richness, rare-taxon count, rare-abundance fraction, and rare retained-taxon fraction.
4. Quantify whether JS/Jaccard are especially sensitive to rare taxa or presence/absence structure. DONE: Jaccard switch is best explained by retained-richness skew versus retained-abundance skew; rare-taxon abundance alone is not the main driver.
5. If possible, add a schematic showing how cosine/vector-decomposition vs Jaccard weight abundance information differently. OPTIONAL; not necessary for current response because the caption prose now carries the distinction.

## Suggested Outputs
- Confusion matrices between metrics. DONE in `metric_outlier_summary.md` and `metric_outlier_audit.pdf`.
- Event-level scatter of retained richness skew versus retained abundance skew. DONE in `metric_outlier_audit.pdf`.
- Feature comparison of switched vs stable events. DONE in `metric_outlier_feature_summary.csv`.
- Short interpretive note: abundance-sensitive vs presence/absence-sensitive metrics. DONE above.

## Candidate Figure Names
- `Fig_R1_5_metric_confusion`
- `Fig_R1_5_switched_events_features`

## Possible Interpretation
- This analysis could turn a weakness into a strength by showing that the disagreement is biologically interpretable rather than arbitrary.
- Likely conclusion: Jaccard and JS overweight low-abundance or presence/absence structure compared with abundance-weighted parental retention.

## Code Location
- Suggested folder: `Figure_generate/code/Figure_revision/R1_5_metric_outliers/`

## Changes to Manuscript
- Existing v4 response and Extended Data Fig. 2 caption already contain the needed claim calibration.
- A supplementary figure is not necessary unless PI wants to elevate this from an internal audit to a reviewer-facing analysis.
