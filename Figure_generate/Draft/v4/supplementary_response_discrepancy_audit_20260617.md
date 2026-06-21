# Supplementary Notes vs Response Letter Audit

Date: 2026-06-17

Scope checked:
- Current supplementary source: `latex/supplementary.tex`, `latex/supplementary_sections/*.tex`
- Current response source: `latex/revision/response_letter.tex`, `latex/revision/response/*.tex`
- Upload PDFs: `revision_submission/00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/04_Response_to_Reviewers_and_Editor.pdf` and `05_Supplementary_Information_Revised.pdf`

## Executive summary

After rechecking the current supplementary source, response-letter source, and upload PDFs, I found no unresolved substantive discrepancy between the Supplementary Notes and the response letter.

The main response-letter promises are now supported in the Supplementary Information: boundary and metric controls, additive/null controls, biomass and richness controls, pH-feedback controls, simulation-scope controls, invasion-resistance framing, pairwise selection-correlation interpretation, and the natural-community caveat.

The initial audit identified five issues. All have now been resolved:

1. The upload supplementary PDF was out of sync with the current compiled supplementary PDF/source. It has been rebuilt and replaced.
2. Response-letter wording that placed metric/threshold definitions in Supplementary Note 1 has been corrected to point to Methods and Supplementary Methods.
3. The pH-methods replicate-treatment sentence promised in the response letter has been added to Supplementary Methods.
4. The pairwise selection-correlation wording no longer claims the same-versus-cross separation is strongest in Nutr+ when the reported Delta is larger in Base. The analysis is now organized in Supplementary Note 7, with Base explicitly described as largest and Nutr+ as still significant.
5. The response-letter reference to Supplementary Note 5 now uses the current Note 5 title.

I also checked the apparent Supplementary Note 7 references. They are intentional: `latex/supplementary.tex` includes `supplementary_sections/pairwise_selection_correlation.tex` as Supplementary Note 7.

## Version and packaging status

The upload PDFs now match the current compiled PDFs:

- Supplementary Information: `latex/supplementary.pdf` and upload `05_Supplementary_Information_Revised.pdf` have matching SHA256 hash `95321ca7d5bac86b480ff4b73c8c38a5cafe54f7c7b1398c9057f61359f3d5ed`.
- Response letter: `latex/revision/response_letter.pdf` and upload `04_Response_to_Reviewers_and_Editor.pdf` have matching SHA256 hash `0a82aa4f601b53f00ef9a447cf3f0735c3f5a449e9d5a411d92a83d39c8616b5`.

The previous source/upload mismatch is resolved.

## Resolved discrepancies

### 1. Metric and threshold location wording

Initial issue:
- The response letter said the cosine-similarity metric definition and retention-threshold clarification were in Supplementary Note 1.
- The current SI organization places those definitions in Supplementary Methods, while Supplementary Note 1 contains robustness checks and points readers back to Supplementary Methods.

Resolution:
- Updated `latex/revision/response/reviewer3_response.tex` so the response now refers to Methods and Supplementary Methods for the metric and threshold definitions.
- Current support is in `latex/supplementary_sections/supplementary_methods.tex`, including the cosine-similarity definition and the `r <= 1/sqrt(2)` retention-boundary explanation.

Status: resolved.

### 2. pH replicate-treatment sentence

Initial issue:
- `latex/revision/response/reviewer2_response.tex` promised that biological replicates were treated as separate event-level observations.
- The endpoint pH timing sentence was present in Supplementary Methods, but the replicate-treatment sentence was missing.

Resolution:
- Added the replicate-treatment sentence to `latex/supplementary_sections/supplementary_methods.tex` in the pH/OD methods paragraph:
  "For analyses involving replicated communities or coalescence events, biological replicates were retained as separate event-level observations, matching the treatment used for composition, OD, and outcome analyses."
- Confirmed the sentence appears in the rebuilt upload SI PDF text.

Status: resolved.

### 3. Pairwise selection-correlation ranking across media

Initial issue:
- Earlier SI wording described the same-versus-cross separation as strongest in Nutr+, while the reported Delta was larger in Base.

Current source:
- Supplementary Note 7 now states that the same-versus-cross separation is significant in Base and Nutr+, not significant in Nutr-, and largest in Base.
- Extended Data Fig. 6 caption also states that Base has the largest same-versus-cross separation among the three media, with Nutr+ remaining significant.

Assessment:
- This is now numerically consistent with the reported values: Base Delta = 0.235, Nutr+ Delta = 0.141, Nutr- Delta = 0.016.

Status: resolved.

### 4. Supplementary Note 5 title mismatch

Initial issue:
- The response letter used the older title "Alternative biological explanations and controls for community-level selection."
- The current SI title is "Alternative explanations for the nutrient-dependent Dominance."

Resolution:
- Updated `latex/revision/response/reviewer1_response.tex` to use the current Note 5 title.

Status: resolved.

## Note-by-note consistency check

### Supplementary Note 1: Robustness of coalescence outcome classification and null-model controls

Related response sections:
- R1-5 metric robustness: `reviewer1_response.tex`
- R2-3 continuous measures and boundary sensitivity: `reviewer2_response.tex`
- R3-1/R3-2/R3-3 classification, normalization, geometric/null concerns: `reviewer3_response.tex`

Current source support:
- Classification framework, metric, and thresholds are defined in Supplementary Methods.
- Boundary sensitivity, abundance-skew nulls, simple additive null, metric sensitivity, and dominant-species PDI removal are in `supplementary_sections/skewness_null_model.tex`.

Assessment:
- Consistent. The previous location mismatch has been resolved by changing the response-letter wording.

### Supplementary Note 2: Shared assembly history promotes Dominance

Related response sections:
- R1-7/R1-8 Fig. 2C/2D visualization clarifications: `reviewer1_response.tex`
- R2-4 pairwise selection-correlation interpretation: `reviewer2_response.tex`

Current source support:
- Assembly-history comparison and reduced within-community interaction coefficients are in `supplementary_sections/assembly_effect.tex`.
- The note now directs the pair-level parental-affiliation-correlated fate analysis to Supplementary Note 7.

Assessment:
- Consistent. No remaining "strongest in Nutr+" inconsistency in this note.

### Supplementary Note 3: Robustness of the simulated Dominance transition to model assumptions

Related response sections:
- R2-6 phenomenological gLV framing and mu interpretation: `reviewer2_response.tex`
- R3-4/R3-5 facilitation, mutualism, and interaction-strength terminology: `reviewer3_response.tex`

Current source support:
- Baseline model and mu as an effective interaction-strength axis.
- Growth-rate/carrying-capacity robustness.
- Uniform/Gaussian/Gamma coefficient distributions.
- Community-size/richness robustness.
- Facilitative-tail, reciprocal pair-coupling, weak mutualistic-pair, and mean/variance sensitivity analyses.

Assessment:
- Consistent with the response letter.

### Supplementary Note 4: Nutrient dependence of pairwise invasion resistance

Related response sections:
- R2-1/R2-2 nutrient enrichment reframing and invasion resistance: `reviewer2_response.tex`
- R2-4 distinction between pairwise invasion assays and pairwise selection correlation: `reviewer2_response.tex`

Current source support:
- Assay design and failed invasion as an empirical invasion-resistance readout are in `supplementary_sections/invasion.tex`.
- Supplementary Methods frames failed invasion as an empirical proxy, not a literal biochemical mechanism.

Assessment:
- Consistent with the response letter.

### Supplementary Note 5: Alternative explanations for the nutrient-dependent Dominance

Related response sections:
- R1-1 biomass/OD: `reviewer1_response.tex`
- R1-2 pH contrast: `reviewer1_response.tex`
- R1-4 pool size/richness: `reviewer1_response.tex`
- R2-2 alternative mechanisms organization: `reviewer2_response.tex`

Current source support:
- Biomass and OD control.
- Initial richness and pool-size analyses.
- pH-feedback model and pH-contrast analysis.
- Supplementary Figs. 13, 45, and 46.

Assessment:
- Consistent. The previous title mismatch has been resolved.

### Supplementary Note 6: Dominance extends to laboratory-stabilized natural communities, with limits on generality

Related response sections:
- R2-5 pre-selection of natural communities: `reviewer2_response.tex`
- R3-4 natural-community caution: `reviewer3_response.tex`

Current source support:
- Laboratory-stabilized, not unfiltered natural ecosystems.
- Higher richness and retained source-specific taxonomic structure.
- No pre-enrichment sequencing or functional data; caveat against unrestricted generality.

Assessment:
- Consistent with the response letter.

### Supplementary Note 7: Interpretation of pairwise selection correlation

Related response sections:
- R2-4 pairwise selection-correlation interpretation and invasion-fitness bridge: `reviewer2_response.tex`
- R1-1/R1-4 controls involving pairwise selection correlation: `reviewer1_response.tex`

Current source support:
- Metric interpretation.
- Simulation evidence.
- Experimental evidence across Nutr-, Base, and Nutr+.
- Biological interpretation as parental-affiliation-correlated species fates.
- Relationship to invasion fitness and the auxiliary gLV analysis in Supplementary Fig. 36.

Assessment:
- Consistent with the response letter. The Note 7 numbering is real and intentional.

## Final status

No remaining actionable discrepancy was found in the current source or upload PDFs after the fixes above.
