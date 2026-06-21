# Revision Summary: All Reviewer Comments

## Overview

- **Reviewer 1**: Very positive ("really enjoyed reading this manuscript... strong impact in the ecological literature"). Raises several specific questions, mostly moderate in severity. Largely supportive of the framework.
- **Reviewer 2** (Samraat Pawar, Jiayi Chen, Danica Duan, Yan Zhu): Positive on experimental design ("elegance of the experimental setup"), but raises conceptual concerns about conflating nutrient enrichment with interaction strength, and whether observed patterns truly demonstrate community-level selection.
- **Reviewer 3**: Raises a critical technical point about the statistical/geometric effect of dimensionality on similarity metrics — that Dominance classification may be inflated in low-diversity communities due to a purely geometric artifact.

---

## CROSS-CUTTING THEMES (raised by multiple reviewers)

### Theme 1: Nutrient enrichment ≠ interaction strength
- **R2 (Major #1)**: Central concern — nutrient enrichment affects carrying capacities, metabolic rates, environmental modification (pH), competition/facilitation balance. Cite Duan et al. 2025 showing resource supply rate can cancel out in effective LV coefficients.
- **R3 (#4)**: "Interaction strength" is confusing since gLV only has competition. Suggest "competition strength."
- **Action needed**: Reframe discussion to acknowledge nutrient enrichment as a complex perturbation; use more nuanced terminology.

### Theme 2: Is this truly community-level selection?
- **R1 (#1, implicit)**: Could absolute density differences explain Dominance and pairwise selection correlations?
- **R2 (Major #2)**: Correlated persistence could arise from shared environmental filtering, correlated traits, or pH tolerance — not community-level selection per se.
- **R3 (#3)**: Facilitative interactions may matter; "Restructuring" is more common in natural communities.
- **Action needed**: Clarify what "community-level selection" means mechanistically; discuss alternative explanations (environmental filtering, hitchhiking, shared traits).

### Theme 3: Classification of outcomes — thresholds and metric sensitivity
- **R1 (#5, line 134)**: Claim of robustness across metrics is "misleading" — Dominance is least likely under Jensen-Shannon and Jaccard.
- **R2 (Major #3)**: Present continuous similarity alongside categories; clarify "restructuring" biologically.
- **R3 (#1, #2)**: **Critical** — Dominance fraction may be inflated by geometric/statistical artifact in low dimensions. Need case-by-case null model (n_C,null = n_A + n_B) comparison, not just distribution-level comparison.
- **Action needed**: (1) Tone down robustness claim. (2) Add per-event null model comparison (additive model). (3) Show continuous metrics. (4) Address dimensionality effect explicitly.

### Theme 4: gLV model lacks pH/environmental modification mechanism
- **R2 (Major #6)**: Frame model as phenomenological, not mechanistic. Model lacks pH dynamics that the paper identifies as key driver.
- **R3 (#3)**: Model limited to competitive interactions; facilitation/cross-feeding could be important, especially for natural communities.
- **Action needed**: Explicitly acknowledge model as phenomenological. Discuss why it captures qualitative patterns despite lacking pH mechanism. Consider whether Dominance increase with mu could be a statistical artifact of reduced richness (R3 #2).

### Theme 5: Natural community evidence is limited
- **R2 (Major #5)**: Pre-selection in defined media may filter natural communities to resemble synthetic ones. Discuss taxonomic/functional convergence during stabilization.
- **R3 (#3)**: Natural communities show more Restructuring — could indicate facilitative interactions not captured by model. Tone down claims (lines 292-294).
- **Action needed**: Discuss pre-selection effects; moderate generalizability claims; note higher Restructuring in natural communities.

---

## REVIEWER-SPECIFIC COMMENTS

### Reviewer 1 — Specific Comments

| # | Comment | Severity | Action |
|---|---------|----------|--------|
| 1 | Could absolute density differences explain results? Use OD data to check. | Major | Analyze OD data across conditions; show that density heterogeneity doesn't explain patterns |
| 2 | Does Dominance become more likely when parents have different pH (acidic vs alkaline) vs same pH? | Major | Test and report this comparison |
| 3 | Fig. 5C circularity: Does PDI correlation hold if dominant species excluded? | Major | Recalculate PDI excluding dominant species |
| 4 | Effect of initial pool size — more detail on richness effects in model and experiment | Moderate | Plot realized richness and interaction strength vs initial richness; show survival ratio vs richness |
| 5 | Robustness claim (line 134) is misleading — Jensen-Shannon and Jaccard give different results | Moderate | Tone down the claim |
| 6 | Gray points in Figs 1E, 4C, 5C, 6B are reflections — confusing | Minor | Add note to caption or remove gray points |
| 7 | Fig. 2A: Show interaction matrix after assembly (block structure) | Minor | Add panel or supplementary figure |
| 8 | Fig. 2D: Relationship between points and squares unclear; gray bars unexplained | Minor | Clarify in caption |
| 9 | Discussion lines 342-345: Emphasize "community-level cohesion without cooperation" (Tikhonov) more | Minor | Expand this point in Discussion |
| 10 | ED Fig. 5C: Are means missing? | Minor | Check and add means |
| 11 | SI p.9: "Extended Data Fig. 5" should be "ED Fig. 4" | Typo | Fix reference |

### Reviewer 2 — Specific Comments

| # | Comment | Severity | Action |
|---|---------|----------|--------|
| 1 | Nutrient enrichment ≠ interaction strength; reframe in terms of interaction intensity and environmental feedbacks | Major | Revise framing; discuss Duan et al. 2025 |
| 2 | Evidence for community-level selection is not uniquely diagnostic; discuss alternatives | Major | Add discussion of alternative mechanisms |
| 3 | Classification depends on thresholds; present continuous measures; clarify "restructuring" | Moderate | Add continuous similarity plots |
| 4 | Pairwise selection correlation interpretation unclear; link to invasion fitness in gLV framework | Moderate | Add theoretical paragraph connecting metrics |
| 5 | Natural community pre-selection during stabilization phase | Moderate | Discuss functional convergence |
| 6 | gLV model: frame as phenomenological; discuss biological meaning of mu | Moderate | Revise model description |
| M1 | Improve pairwise correlation visualization | Minor | Update figure |
| M2 | Specify how pH was measured | Minor | Clarify in Methods |
| M3 | Clarify biological interpretation of interaction coefficient distributions | Minor | Add to model description |
| M4 | Consistent terminology and notation | Minor | Review throughout |
| M5 | "generalis ability" → "generalisability" | Typo | Fix |

### Reviewer 3 — Specific Comments

| # | Comment | Severity | Action |
|---|---------|----------|--------|
| 1 | Dimensionality/geometric artifact inflates Dominance in low-diversity communities; need case-by-case null model (n_C,null = n_A + n_B) | **Critical** | Implement per-event additive null model comparison |
| 2 | Increasing mu reduces richness, which geometrically increases Dominance — confound. Show richness vs mu in model and across media | **Critical** | (a) Plot richness vs mu. (b) Compare Dominance increase to null expectation from richness decrease. (c) Show richness across Base/Nutr-/Nutr+ for synthetic communities |
| 3 | gLV lacks facilitation; natural communities show more Restructuring; tone down claims (lines 292-294) | Major | Moderate claims about generalizability |
| 4 | "Interaction strength" terminology confusing — consider "competition strength" | Minor | Consider terminology change or clarify |

---

## PRIORITY ACTION ITEMS

### Tier 1: Must address (critical/major issues raised by multiple reviewers)

1. **Additive null model comparison** (R3 #1): Per-event comparison of coalesced community to n_C,null = n_A + n_B
2. **Richness-Dominance confound** (R3 #2): Show richness vs mu in model; show richness across media in experiments; test whether Dominance increase exceeds null expectation from richness decrease alone
3. **Reframe "interaction strength"** (R2 #1, R3 #4): Acknowledge complexity of nutrient enrichment; consider "competition strength" or qualify "interaction strength"
4. **Clarify community-level selection** (R2 #2, R1 implicit): Discuss alternative mechanisms; distinguish from environmental filtering and hitchhiking
5. **Absolute density check** (R1 #1): Analyze OD data to rule out density differences as alternative explanation

### Tier 2: Important but more straightforward

6. **PDI without dominant species** (R1 #3): Recalculate to address circularity concern
7. **pH and Dominance likelihood** (R1 #2): Test whether different-pH matchups show more Dominance
8. **Tone down robustness claim** (R1 #5): Revise line 134
9. **Model as phenomenological** (R2 #6, R3 #3): Reframe in text
10. **Natural community pre-selection** (R2 #5): Add discussion
11. **Pool size / richness detail** (R1 #4): Additional analysis and plots
12. **Connect pairwise selection to invasion fitness** (R2 #4): Add theoretical paragraph

### Tier 3: Minor revisions

13. Figure clarifications (R1 #6, #7, #8, #10)
14. Discussion emphasis on "cohesion without cooperation" (R1 #9)
15. Continuous similarity measures alongside categories (R2 #3)
16. Visualization improvements (R2 M1)
17. pH measurement details (R2 M2)
18. Terminology consistency (R2 M4)
19. Typos: "generalis ability", ED Fig 5→4 reference, etc.
