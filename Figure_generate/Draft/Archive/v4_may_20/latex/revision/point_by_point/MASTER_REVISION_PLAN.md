# Master Revision Plan

## Guiding Principle: Order of Operations
1. **Phase 1 — Text-only fixes** (typos, terminology, framing): no figure regeneration needed
2. **Phase 2 — Figure style/caption fixes**: modify existing figures, no new analysis
3. **Phase 3 — Reanalysis of existing data**: new plots from data already in hand
4. **Phase 4 — New simulations**: computational work, may take time but no wet-lab
5. **Phase 5 — Manuscript restructuring**: rewrite paragraphs incorporating new results
6. **Phase 6 — Response letter**: compile point-by-point responses

Each later phase builds on earlier phases, so completing Phase 1-2 first avoids rework.

---

## Complete Point Classification

### PHASE 1: Text-only fixes (no figures, no analysis)
**Status: ✅ COMPLETE (2026-04-14)**
*Estimated effort: Low. Do these first.*

| ID | Reviewer | Point | What to do | Confidence |
|----|----------|-------|------------|------------|
| P1.1 | R2-M5 | "generalis ability" typo | Fix typo → "generalisability" | 100% |
| P1.2 | R1-11 | SI p.9 wrong ED Fig ref | Change "ED Fig. 5" → "ED Fig. 4" | 100% |
| P1.3 | R2-M4 | Inconsistent terminology/notation | Review and unify throughout | 95% |
| P1.4 | R3-4 | "Interaction strength" → clarify | Add qualifier or use "competition strength" in model context; keep "interaction strength" for experiments but clarify | 90% |
| P1.5 | R1-5 | Robustness claim (line 134) misleading | Tone down: "Dominance was the most frequent outcome under Bray-Curtis and cosine similarity, though less pronounced under Jensen-Shannon and Jaccard" | 95% |
| P1.6 | R2-6 | Frame gLV model as phenomenological | Add sentence: "We emphasize that the gLV model is used as a phenomenological framework..." | 95% |
| P1.7 | R1-9 | Emphasize "cohesion without cooperation" | Expand 1-2 sentences in Discussion referencing Tikhonov | 90% |
| P1.8 | R3-3 | Tone down natural community claims (lines 292-294) | Soften language, acknowledge facilitation limitation | 90% |
| P1.9 | R2-2 | Discuss alternative mechanisms for community-level selection | Add paragraph in Discussion: environmental filtering, hitchhiking, shared traits | 85% |
| P1.10 | R2-5 | Discuss natural community pre-selection during stabilization | Add paragraph acknowledging functional convergence during stabilization | 85% |
| P1.11 | R2-1 | Reframe nutrient enrichment ≠ interaction strength | Revise framing in Results and Discussion; cite Duan et al. 2025 | 80% |
| P1.12 | R2-M2 | Specify pH measurement method | Add to Methods | 95% |
| P1.13 | R2-M3 | Clarify biological meaning of interaction coefficient distributions | Add to model description | 85% |

### PHASE 2: Figure style / caption fixes (modify existing figures, no new analysis)
**Status: ⚠️ IN PROGRESS (captions done; two items need figure regeneration decisions)**
*Estimated effort: Low-Medium. Do after Phase 1.*

| ID | Reviewer | Point | What to do | Confidence |
|----|----------|-------|------------|------------|
| P2.1 | R1-6 | Gray reflection points confusing (Figs 1E, 4C, 5C, 6B) | Add caption note explaining gray = reflected pair, OR remove them | 95% |
| P2.2 | R1-8 | Fig. 2D: unclear points/squares/gray bars | Clarify in caption | 95% |
| P2.3 | R1-10 | ED Fig. 5C: check if means missing | Check data, add mean markers if absent | 90% |
| P2.4 | R2-M1 | Improve pairwise correlation visualization | Update styling of existing figure | 80% |

### PHASE 3: Reanalysis of existing data (new figures from existing experimental data)
**Status: ✅ COMPLETE (2026-04-14/15) — all 7 scripts done, figures generated**
*Estimated effort: Medium. Core of the revision. Do after Phase 2.*

| ID | Reviewer | Point | What to do | Code folder | Confidence |
|----|----------|-------|------------|-------------|------------|
| P3.1 | R1-1 | Absolute density (OD) check | Analyze OD data across conditions; show density doesn't explain Dominance patterns | `R1_1_OD_density` | 85% — depends on OD data availability |
| P3.2 | R1-2 | pH × Dominance: acidic vs alkaline parents | Compare Dominance frequency: same-pH vs different-pH parent pairs | `R1_2_pH_dominance` | 90% — straightforward from existing pH + outcome data |
| P3.3 | R1-3 | PDI without dominant species (circularity check) | Recalculate PDI excluding dominant species from Fig. 5C correlation | `R1_3_PDI_no_dominant` | 90% — reanalysis of existing data |
| P3.4 | R3-1 | **Per-event additive null model** | For each coalescence event, compute n_C,null = n_A + n_B (normalized), compare to observed n_C | `R3_1_additive_null` | 80% — critical point, need careful implementation |
| P3.5 | R3-2a | Richness across media (experiment) | Show species richness in Base/Nutr-/Nutr+ for synthetic communities | `R3_2_richness_media` | 90% — from existing sequencing data |
| P3.6 | R2-3 | Continuous similarity alongside categories | Plot continuous PDI and retention magnitude distributions, not just categories | `R2_3_continuous_similarity` | 90% — replot existing data |
| P3.7 | R1-4 | Pool size / richness detail | Plot realized richness, interaction strength vs initial richness; survival ratio vs richness | `R1_4_pool_size` | 85% — may need both experiment + simulation data |
| P3.8 | R1-1 ext. | Species absolute abundance explanation | Test whether species-level absolute abundance at mixing predicts retention better than community origin | `R1_1_species_absolute_abundance` | 80% — useful extension of OD-control analysis |
| P3.9 | R1-5 ext. | Why JS/Jaccard are outlier metrics | Analyze event-level classification switches and feature sensitivity of outlier metrics | `R1_5_metric_outliers` | 85% — likely interpretable from abundance vs presence/absence weighting |
| P3.10 | R3-1 ext. | Dimensionality-adjusted thresholds | Rescale dominance boundaries using effective dimensionality and test whether conclusions hold | `R3_1_dimensionality_adjusted_thresholds` | 75% — secondary robustness check after additive null |

### PHASE 4: New simulations / computational analysis
**Status: ✅ COMPLETE (2026-04-14/15) — all 3 scripts done, figures generated**
*Estimated effort: Medium-High. Do after Phase 3.*

| ID | Reviewer | Point | What to do | Code folder | Confidence |
|----|----------|-------|------------|-------------|------------|
| P4.1 | R3-2b | Richness vs mu in model | Run/analyze gLV: plot richness vs mu; test if Dominance increase exceeds null from richness decrease alone | `R3_2_richness_mu_model` | 75% — need to disentangle richness effect from interaction effect |
| P4.2 | R1-7 | Interaction matrix after assembly | Show block structure in interaction coefficient matrix post-assembly | `R1_7_interaction_matrix` | 85% — visualization from existing simulation framework |
| P4.3 | R2-4 | Connect pairwise selection to invasion fitness | Theoretical paragraph + possibly a supporting figure linking PDI to gLV invasion fitness | `R2_4_invasion_fitness` | 70% — may need new theoretical derivation |
| P4.4 | R2-1 / PI | Alternative model beyond gLV | Build a simple pH-based or hybrid environment-feedback model for comparison | `R2_1_pH_model_or_alt_model` | 65% — conceptual payoff is high even for a toy model |
| P4.5 | PI / R2-2 | "Acidic always wins" rule vs gLV | Test where a naive pH-only rule succeeds and fails relative to observed outcomes | `R2_2_acidic_always_wins_vs_gLV` | 75% — could sharpen Base vs Nutr+ mechanism split |
| P4.6 | R2-6 / PI | gLV failure modes | Explicitly quantify data features captured poorly by competition-only gLV | `R2_6_gLV_failure_modes` | 85% — strong framing value for revision and response letter |

### PHASE 5: Manuscript integration (after all analyses done)
**Status: ⏳ NOT STARTED**
*Do last — incorporate all new figures and text into LaTeX.*

| ID | What | Depends on |
|----|------|------------|
| P5.1 | Update results.tex with new analyses and reframed language | P1, P3, P4 |
| P5.2 | Update discussion.tex with new paragraphs | P1.7-P1.11 |
| P5.3 | Update methods.tex with pH details, model framing | P1.6, P1.12 |
| P5.4 | Update supplementary.tex with new figures/notes | P3, P4 |
| P5.5 | Update figure captions | P2 |
| P5.6 | Add new Extended Data / Supplementary figures | P3, P4 |
| P5.7 | Fix all cross-references | All |

### PHASE 6: Response letter
**Status: ⏳ NOT STARTED — response_letter.tex does not exist yet**
*Compile after manuscript is updated.*

| ID | What |
|----|------|
| P6.1 | Write point-by-point response to Reviewer 1 |
| P6.2 | Write point-by-point response to Reviewer 2 |
| P6.3 | Write point-by-point response to Reviewer 3 |

---

## Dependency Graph

```
Phase 1 (text fixes) ──────────────────────────────────────┐
    │                                                       │
Phase 2 (figure style fixes)                                │
    │                                                       │
Phase 3 (reanalysis) ──────────────┐                        │
    │                              │                        │
Phase 4 (new simulations) ─────────┤                        │
                                   │                        │
                            Phase 5 (manuscript integration)│
                                   │                        │
                            Phase 6 (response letter) ──────┘
```

## Risk Assessment

| Risk | Points affected | Mitigation |
|------|----------------|------------|
| OD data not available/sufficient | P3.1 | Check data files first; if missing, argue from indirect evidence |
| Additive null model undermines Dominance claims | P3.4 | Run analysis honestly; if some events are null-compatible, report transparently and emphasize the ones that aren't |
| Richness-mu confound explains away mu effect | P4.1 | If richness decrease accounts for most Dominance increase, reframe as "interaction strength reduces richness which geometrically promotes Dominance" — still interesting |
| Invasion fitness derivation too complex | P4.3 | Fall back to conceptual argument + citation rather than formal derivation |
| Natural community pre-selection critique | P1.10 | Acknowledge openly; this is a limitation, not a fatal flaw |

---

## Recommended Execution Order (within each phase)

### Phase 1 order:
1. P1.1, P1.2 (instant fixes)
2. P1.5, P1.12 (quick edits)
3. P1.3, P1.4 (terminology sweep)
4. P1.6, P1.13 (model framing)
5. P1.7, P1.8 (discussion edits)
6. P1.9, P1.10, P1.11 (substantial paragraph writing — do last in Phase 1)

### Phase 3 order:
1. P3.5, P3.6 (quick replots)
2. P3.1, P3.2, P3.3 (moderate reanalysis)
3. P3.7 (pool size detail)
4. P3.4 (additive null model — most critical and complex)

### Phase 4 order:
1. P4.2 (interaction matrix visualization — quick)
2. P4.1 (richness vs mu — important)
3. P4.3 (invasion fitness connection — hardest)
