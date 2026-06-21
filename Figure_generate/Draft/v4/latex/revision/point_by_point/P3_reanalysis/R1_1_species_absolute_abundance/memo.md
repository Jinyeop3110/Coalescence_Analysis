# P3.X — Species Absolute Abundance as Alternative Explanation

## Reviewer / Source
- Reviewer 1, Point #1 (extension of OD concern)
- PI discussion note 04/17: "Correlation between species absolute abundance (OD x relative abundance) and retention."

## Status
- NOT STARTED
- Confidence: 80%

## Why This Exists
The existing OD analysis tests whether the denser parental community tends to win. This follow-up asks a finer-grained question: do species with higher initial absolute abundance after mixing preferentially persist, independent of community origin? If so, some apparent community-level selection could partly reflect numerical advantage at the species level.

## Core Question
Does species-level absolute abundance at the time of mixing predict post-coalescence retention strongly enough to explain Dominance patterns?

## Proposed Analysis
1. For each coalescence event, estimate species absolute abundance at mixing:
   - parental community OD
   - species relative abundance within parent
   - mixed-community expected absolute abundance after 1:1 pooling
2. Test whether higher absolute-abundance species are more likely to survive in the coalesced community.
3. Compare predictive power of:
   - species absolute abundance alone
   - parental-community origin alone
   - combined models
4. Ask whether surviving species are enriched for the initially more abundant parental side even in events classified as Dominance.

## Suggested Outputs
- Species retention probability vs estimated initial absolute abundance
- Logistic regression or rank-based analysis for survival vs abundance
- Stratification by medium (Nutr-, Base, Nutr+)
- Summary statistic comparing numerical-advantage explanation vs community-origin explanation

## Candidate Figure Names
- `Fig_R1_1d_species_retention_vs_abs_abundance`
- `Fig_R1_1e_abs_abundance_by_origin`

## Possible Interpretation
- Weak predictive power would strengthen the claim that Dominance is not reducible to species-level inoculum size.
- Strong predictive power would suggest numerical advantage contributes and should be discussed explicitly as a partial mechanism.

## Code Location
- Suggested folder: `Figure_generate/code/Figure_revision/R1_1_species_absolute_abundance/`

## Changes to Manuscript
- Add 1-2 sentences near the OD-control discussion.
- If effect is substantial, discuss species-level abundance advantage as a partial but insufficient explanation for community-level outcomes.
