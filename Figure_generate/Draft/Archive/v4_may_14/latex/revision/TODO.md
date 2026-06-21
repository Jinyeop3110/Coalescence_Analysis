# v4 Revision TODO

Last checked: 2026-05-11

This list tracks the submission-facing state of each reviewer point. Status is taken from the LaTeX response files in `latex/revision/response/`, with next actions interpreted using `revision.rule.md`.

## Immediate Priorities

| Priority | Point | Current state | Next action |
|---|---|---|---|
| 1 | R1-1 | Blocked | Integrate OD/absolute-density result into Results and add/cite the planned Supplementary Figure, then promote if response claim matches manuscript. |
| 2 | R1-2 | Completed | No action unless final copyedit changes wording. |
| 3 | R1-3 | Blocked | Integrate dominant-species-removal analysis into Results and add/cite the planned Supplementary Figure. |
| 4 | R1-4 | Blocked | Integrate pool-size result into Results and add/cite the planned Supplementary Figure. |
| 5 | R3-1 to R3-4 | Before review | Co-review response wording and decide whether each can be promoted or must be marked Blocked for any remaining manuscript/SI gaps. |

## Reviewer 1

| Point | Topic | Status | Next action |
|---|---|---|---|
| R1-1 | Absolute density as an alternative explanation for Dominance | Blocked | Add manuscript/SI integration for OD result. |
| R1-2 | Does pH mismatch predict Dominance? | Completed | No action unless final copyedit changes wording. |
| R1-3 | Circularity in Fig. 5C, PDI excluding dominant species | Blocked | Add manuscript/SI integration for dominant-species-removal analysis. |
| R1-4 | Pool-size effects | Blocked | Add manuscript/SI integration for pool-size analysis. |
| R1-5 | Similarity-metric robustness claim | Completed | No action unless final copyedit changes wording. |
| R1-6 | Gray reflected points in figures | Completed | No action unless final figure captions are regenerated. |
| R1-7 | Interaction matrix after assembly | Completed | No action; Supplementary Fig. 27 and Results cross-reference are integrated. |
| R1-8 | Fig. 2D visualization | Completed | No action; caption clarification is integrated. |
| R1-9 | Emphasize "cohesion without cooperation" | Completed | No action; Discussion text is integrated. |
| R1-10 | Means missing in Extended Data Fig. 5C | Completed | Optional final figure-polish only. |
| R1-11 | Incorrect Extended Data reference in the SI | Completed | No action. |

## Reviewer 2

| Point | Topic | Status | Next action |
|---|---|---|---|
| R2-1 | Nutrient enrichment versus interaction strength | Completed | No action unless final co-author wording changes are requested. |
| R2-2 | Alternative explanations for community-level selection | Completed | No action unless R1 blocked items change the shared simple-retention framing. |
| R2-3 | Continuous measures alongside categorical outcomes | Completed | No action; Supplementary Fig. 29 is integrated. |
| R2-4 | Interpretation of pairwise selection correlation | Completed | No action; Supplementary Fig. 28 and Supplementary Note text are integrated. |
| R2-5 | Pre-selection of natural communities | Completed | No action. |
| R2-6 | Frame gLV as phenomenological | Completed | No action. |
| R2-minor | Minor comments | Completed | No action. |

## Reviewer 3

| Point | Topic | Status | Next action |
|---|---|---|---|
| R3-1 | Clarify L1 vs L2 normalization in the similarity metric | Before review | Quote/source traceability checked; ready for explicit joint review decision on promotion. |
| R3-2 | Dimensionality artifact in similarity metrics | Before review | Co-review additive-null and reviewer-toy-null response; verify no response figure/text overclaims manuscript integration. |
| R3-3 | Interaction strength, diversity, and Dominance frequency | Before review | Co-review richness/null framing; confirm Results text and response numbers match final figures. |
| R3-4 | gLV model excludes facilitation | Before review | Co-review scope-limitation language and decide whether response-only robustness figures are sufficient. |
| R3-5 | "Interaction strength" versus "competition strength" | Completed | Final terminology and response-style pass completed. |

## Completion Gate

Before treating `v4` as submission-ready:

1. Clear or justify all `Blocked` status markers.
2. Promote or explicitly leave `Before review` markers after PI/co-author review.
3. Confirm every response phrase like "we have added" maps to manuscript or SI source.
4. Recompile `main.tex`, `supplementary.tex`, and `revision/response_letter.tex`.
5. Update `revision_history.md` for any new integration edits.
