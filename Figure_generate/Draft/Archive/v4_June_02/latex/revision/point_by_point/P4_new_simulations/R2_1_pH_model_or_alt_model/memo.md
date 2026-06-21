# P4.X — Alternative Model Beyond Pairwise gLV (pH-Based or Hybrid Model)

## Reviewer / Source
- Reviewer 2, major framing concern
- PI discussion note 04/17: "Include a new model (e.g., pH-based model)."

## Status
- NOT STARTED
- Confidence: 65%

## Why This Exists
The current revision package shows that gLV captures much of the data, but Jeff's note argues that we should avoid presenting pairwise gLV as the only valid framework. A lightweight alternative model would demonstrate that the phenomena may also emerge from environment-mediated mechanisms, especially pH modification.

## Core Question
Can a simple pH-mediated or hybrid environmental-feedback model reproduce key qualitative patterns that gLV explains?

## Candidate Model Directions
1. Pure pH rule-based model:
   - species modify environmental pH
   - growth or survival depends on distance from preferred pH
2. Hybrid phenomenological model:
   - pairwise competition + shared environmental state variable
3. Parent-level effective model:
   - dominant taxa determine community pH, which then filters the merged community

## Minimum Deliverable
Even a deliberately simple toy model would be useful if it reproduces:
- weak-selection / mixing regime
- strong-selection / one-sided regime
- stronger predictability in Nutr+ than Base

## Suggested Outputs
- Diagram of model assumptions
- Qualitative phase plots comparable to the gLV outputs
- Side-by-side comparison: what gLV explains vs what pH model explains

## Candidate Figure Names
- `Fig_R2_1_alt_model_framework`
- `Fig_R2_1_alt_model_vs_glv`

## Possible Interpretation
- The goal is not to replace gLV but to show that multiple coarse-grained models can generate the observed transition.
- This would support the reframing of "interaction strength" as a coarse-grained systems property rather than a single mechanistic coefficient.

## Code Location
- Suggested folder: `Figure_generate/code/Figure_revision/R2_1_pH_model_or_alt_model/`

## Changes to Manuscript
- Add a paragraph explaining why gLV was chosen as the simplest baseline.
- Add a complementary statement that alternative environment-mediated models may capture other aspects of the data.
