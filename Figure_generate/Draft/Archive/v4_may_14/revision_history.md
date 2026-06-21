# Revision History for `v4`

This log records rebuttal-stage changes made in `Figure_generate/Draft/v4`.

Entries are organized primarily by reviewer question, with a small infrastructure section for workflow changes that support the rebuttal package as a whole.

---

## 2026-05-13

### R3-2 retention-notation clarification

- **Affected reviewer points**: R3-2, with consistency updates to R2-3.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/sections/methods.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/revision/revision_figure_folder/source.md`

- **What changed**
  - Standardized retention magnitude notation to `r` and squared retention to `r^2` in the main Methods, Supplementary Methods, response text, and relevant supplementary/response figure captions.
  - Added a concise implication sentence to the R3-2 response after reproducing the reviewer toy nulls: the low-richness null behavior supports the validity of the manuscript classifier at the low-richness end of the tested species-pool sizes.
  - Split the R3-2 response so the "We have revised..." manuscript-change statement starts a separate paragraph.

- **Type**
  - Response text edit
  - Manuscript notation clarification
  - Supplementary caption/provenance cleanup

---

## 2026-05-14

### R3-2 toy-null response wording tightened

- **Affected reviewer points**: R3-2.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/analyze_parent_norm_asymmetry.py`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/Fig_R3_2_parent_norm_asymmetry.pdf`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Rewrote the opening R3-2 response paragraph to thank the reviewer for the suggestion, state that the toy-null reproduction used the exact same L$_2$/cosine analysis as the manuscript, and identify the reviewer-attachment boundary mismatch concisely.
  - Removed the verbose metric-clarification sentence and the quoted Methods/Supplementary Methods boundary block from the response.
  - Reframed the toy-null results as recovering the expected outcomes under the manuscript classifier.

- **Type**
  - Response text cleanup
  - PDF regeneration

### R3-2 case-by-case additive-null response refactored

- **Affected reviewer points**: R3-2.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Split the second R3-2 reviewer comment so the general distribution-level concern and the case-by-case additive-null request are answered separately.
  - Refactored the case-by-case additive-null response around parental count-vector norm fold differences, comparing experimental pairs with the skewed low-richness toy additive model.
  - Reworked Response Fig.~R3-2C from a three-panel raw-read/norm diagnostic into a three-panel figure showing parental raw L$_2$ norm density, paired-parent L$_2$ norm fold differences alongside skewed toy additive cases at $N=2$ and $N=4$, and per-medium additive-null classification fractions.
  - Added per-medium additive-null Mixture fractions to state directly that the pair-specific raw-count additive null is mostly Mixture in each nutrient condition and does not explain the observed Dominance tendency.

- **Type**
  - Response text restructuring
  - PDF regeneration

### R3-4 analytic coefficient histograms added

- **Affected reviewer points**: R3-4.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mixed_sign_higher_order_figure.py`
  - `Figure_generate/code/Figure_revision/R3_3_pair_additivity/make_R3_3_figure.py`
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_p_axis_fine_figure.py`
  - `latex/revision/revision_figure_folder/R3_4_mixed_sign_higher_order.pdf`
  - `latex/revision/revision_figure_folder/R3_4_simulation.pdf`
  - `latex/revision/revision_figure_folder/R3_4_pair_coupling_fine.pdf`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/source.md`

- **What changed**
  - Added top analytic coefficient-distribution histograms to Response Figs. R3-4b and R3-4c, showing the formula-implied sampling density of `alpha/mu` rather than Monte Carlo coefficient samples.
  - Added compact analytic coefficient-distribution strips for `p=-1`, `p=0`, and `p=+1` above the fine `p` sweep in Response Fig. R3-4d.
  - Removed redundant inset titles and moved class legends outside the data axes to avoid overlap with panel titles and bars.
  - Updated captions and figure provenance to distinguish these analytic sampling-density references from the simulated outcome fractions below them.

- **Type**
  - Response figure update
  - Caption/provenance cleanup

### Response-letter status/confidence markers removed

- **Affected reviewer points**: Global response-letter formatting.

- **Files changed**
  - `latex/revision/response_letter.tex`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response/README.md`

- **What changed**
  - Removed all reviewer-facing `\statusline{...}{...}` markers so the compiled response letter no longer displays `Status:` / `Confidence:` lines.
  - Removed the now-unused `\statusline`, `\statusdone`, and `\statuspending` macro definitions.
  - Updated the response README rule to prevent reintroducing workflow triage markers in reviewer-facing files.

- **Type**
  - Response-letter formatting cleanup

### R3-1 response wording shortened

- **Affected reviewer points**: R3-1.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/sections/results.tex`
  - `latex/sections/methods.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Removed the explanatory sentence describing code-level Euclidean normalization, dot products, cosine similarities, and vector-decomposition/classification reuse from the opening R3-1 response paragraph.
  - Rephrased the opening sentence to thank the reviewer for identifying the ambiguity and apologize for the confusion.
  - Added a concise clarification that cosine similarity was computed after Euclidean normalization (L$_2$ norm) of the abundance vectors.
  - Removed the final sentence stating that this was a clarification rather than an analysis change.
  - Reworded the Results \S2.1 vector-definition sentence to avoid the phrase "normalized forms" and use a more natural description of $\vec{x}_A$, $\vec{x}_B$, and $\vec{x}_C$ after Euclidean normalization.
  - Updated the Methods and Supplementary Methods metric descriptions to use Euclidean normalization / Euclidean-normalized vectors, while keeping the Supplementary Methods paragraph close to the submitted v3 wording.

- **Type**
  - Response text cleanup
  - Manuscript wording cleanup
  - PDF regeneration

### R3-4 response wording aligned with updated competition evidence

- **Affected reviewer points**: R3-4, with consistency update to R3-5.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/sections/discussion.tex`
  - `latex/revision/revision_figure_folder/source.md`

- **What changed**
  - Reframed the R3-4 response so the competition-only gLV is described as an empirically motivated approximation for this experiment, not as a general claim that facilitation is absent from microbial coalescence.
  - Matched the prose to the updated species-level R3-4a result: 79/84/93% of species-in-pair observations fall below monoculture expectation in Nutr-/Base/Nutr+.
  - Kept the literature support limited to nutrient-dependent competitive exclusion / interaction strength, and avoided using positive-interaction literature as support for the competition baseline.
  - Updated the Discussion caveat and R3-5 cross-reference to use the same "frequent growth-inhibiting effects" and "competitive-interaction regime" wording.
  - Clarified in response-figure provenance that stricter pair-level RYT summaries are retained in source documentation but are not used in the current response prose.

- **Type**
  - Response text edit
  - Manuscript caveat edit
  - Figure provenance cleanup

### R3-5 interaction-strength terminology justification

- **Affected reviewer points**: R3-5.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/sections/discussion.tex`

- **What changed**
  - Added a concise literature-based justification for retaining the term "interaction strength," citing consistency with May's classic random community model (May 1972) and recent microbial gLV work by Hu et al. (2022, 2025).
  - Kept the response focused on the revised manuscript scope: the work addresses a competition-dominated regime, while mutualism/facilitation is handled in R3-4.
  - Revised the response to comply with the response-letter format: direct answer in the opening sentence and a separate response label for the mutualism subquestion.
  - Removed the duplicate R3-5 quotation of the Discussion scope sentence because the same manuscript change is already quoted in R3-4.
  - Marginally revised the Discussion caveat to acknowledge that limited facilitative extensions were explored while retaining the warning that substantial mutualism or facilitation may behave differently.

- **Type**
  - Response text edit
  - Manuscript text edit

### R3-5 competition-strength terminology rollback

- **Affected reviewer points**: R3-5, R2-1.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`
  - `latex/main.tex`
  - `latex/supplementary.tex`

- **What changed**
  - Reverted manuscript-facing wording away from the reviewer-suggested "competition strength" framing and restored the v3-style interaction-strength language in the model, experiment, and pairwise-invasion method text.
  - Marked the restored passages with `\rollback{}` green text so they can be checked before final cleanup.
  - Updated R3-5 to thank the reviewer for the semantic concern, state the decision to retain "interaction strength," reference the revised Discussion scope, and split the mutualism question into a separate subquestion answered by R3-4.

- **Type**
  - Response text edit
  - Manuscript text rollback
  - LaTeX revision markup support

### R3-4 positive-interaction citation removed from response prose

- **Affected reviewer points**: R3-4.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Removed the Kehe et al. 2021 parenthetical from the R3-4 prose because it supports the reviewer's facilitation concern rather than the competition-focused baseline.
  - Left the logic as a direct transition: interaction type is context-dependent, so we tested extension beyond strictly competitive interactions using the facilitative-tail model.
  - Recompiled `latex/revision/response_letter.tex` successfully.

- **Type**
  - Response text edit
  - PDF regeneration

### R3-3A richness figure switched to R1-4 A/B panels

- **Affected reviewer points**: R3-3, with figure reuse from R1-4.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`
  - `Figure_generate/code/Figure_revision/R1_4_pool_size/pool_size_analysis_AB.pdf`
  - `latex/revision/revision_figure_folder/pool_size_analysis_AB.pdf`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Added a dedicated two-panel `pool_size_analysis_AB.pdf` export from the existing R1-4 plotting script, matching Response Fig.~R1-4 panels A and B.
  - Replaced the standalone `richness_by_medium.pdf` R3-3A include with the new two-panel richness/retention export.
  - Updated the R3-3A caption to describe realized parental richness and parental ASV retention ratio, and removed the p-value sentence from the caption.
  - Updated the R3-3 response prose to mention the parental ASV retention ratio.

- **Type**
  - Response figure export/reuse
  - Response text/caption cleanup
  - Figure provenance update
  - PDF regeneration

### R3-3 pool-size cross-reproduced figure removed

- **Affected reviewer points**: R3-3.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Removed the reproduced R1-4 pool-size figure block from the R3-3 response.
  - Removed the associated R3-3 prose sentence using the R1-4 pool-size ablation as corroborating evidence, keeping R3-3 focused on final richness across media and the $\mu$-matched simulation null.

- **Type**
  - Response text cleanup
  - PDF regeneration

### R3-4 literature framing refined for Gore/Friedman positive-interaction paper

- **Affected reviewer points**: R3-4.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Clarified the literature framing around interaction types: Ratzke et al. 2020 and Hu et al. 2022/2025 support the competition-focused baseline in complex-media synthetic communities.
  - Added Kehe et al. 2021 as the Jeff Gore / Jonathan Friedman positive-interaction paper motivating the need to test extension beyond strictly competitive interactions.
  - Recompiled `latex/revision/response_letter.tex` successfully.

- **Type**
  - Response text edit
  - PDF regeneration

### R3-4 competition-evidence paragraph simplified

- **Affected reviewer points**: R3-4.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Removed detailed relative-yield and RYT percentage values from the main R3-4 response prose while leaving the figure/caption evidence intact.
  - Reframed the empirical point more simply: competitive suppression is frequent in the experiment, supporting the competition-focused baseline.
  - Replaced the broader Coyte/Foster citation framing with already cited Hu et al. synthetic microbial-community studies in complex media (`Hu2022`, `Hu2025`).
  - Recompiled `latex/revision/response_letter.tex` successfully.

- **Type**
  - Response text edit
  - PDF regeneration

### R3-4a revised from pair-total additivity to species-level coculture suppression

- **Affected reviewer points**: R3-4.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_3_pair_additivity/analyze_pair_additivity.py`
  - `Figure_generate/code/Figure_revision/R3_3_pair_additivity/make_R3_3_figure.py`
  - `Figure_generate/code/Figure_revision/R3_4_experiment.pdf`
  - `latex/revision/revision_figure_folder/R3_4_experiment.pdf`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Replaced the active R3-4a scatter panels from total coculture CFU vs summed monoculture CFU (`C_i+C_j` vs `M_i+M_j`) with per-species coculture suppression plots (`C_i` vs `M_i` for each focal ASV in each pair).
  - Added species-level summary values to the response: 79/84/93\% of species-in-pair observations are below monoculture expectation in Nutr$-$/Base/Nutr$+$, with median relative yields `C_i/M_i = 0.67/0.05/0.04`.
  - Kept the stricter pair-level RYT<1 values in response prose as supporting evidence: 20/69/88\% in Nutr$-$/Base/Nutr$+$.
  - Updated the R3-4a caption and figure provenance so the competition connection is direct: points below the diagonal are individual ASVs suppressed in coculture relative to monoculture.
  - Recompiled `latex/revision/response_letter.tex` successfully.

- **Type**
  - Response figure regeneration
  - Response text/caption update
  - Figure provenance update
  - PDF regeneration

### R3-5 interaction-strength terminology rollback

- **Affected reviewer points**: R3-5, with scope cross-reference to R3-4.

- **Files changed**
  - `latex/main.tex`
  - `latex/supplementary.tex`
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Added `\rollback{}` as a green text marker in the main manuscript and supplementary LaTeX preambles so the rolled-back terminology can be checked visually.
  - Reverted Results \S2.2 wording away from the reviewer-prompted "mean competition coefficient" framing and back toward the v3 wording for $\mu$.
  - Reverted Results \S2.4 and Supplementary Methods pairwise-invasion language away from the "empirical interaction-strength readout" phrasing and back toward the v3 nutrient-gradient/proxy language.
  - Restored the v3 transition sentence "Given that nutrient concentration modulates interaction strength..." to remove the remaining "interaction readout" phrasing.
  - Removed the remaining "mean competition strength" phrase from the Discussion's $\mu$ mapping caveat.
  - Aligned the R2-2 response so it no longer quotes the rolled-back empirical-readout wording.
  - Removed the internal rollback-explanation paragraph from the R3-5 response letter.
  - Tightened the R3-5 response to go directly from the semantic concern to the decision to keep "interaction strength" and the concise competition-scope rationale.
  - Split the reviewer's mutualism question into a separate R3-5 subquestion and answered it with a one-sentence cross-reference to R3-4.
  - Rewrote the R3-5 response to thank the reviewer for the concern, state that we are not adopting "competition strength" as the manuscript-wide replacement, and instead point to the revised Discussion scope statement and the R3-4 ablation/robustness analyses.

- **Type**
  - Manuscript terminology rollback
  - Supplementary methods terminology rollback
  - Response text edit

### R3-4 first response reframed around empirical competition evidence

- **Affected reviewer points**: R3-4.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/response_letter.pdf`

- **What changed**
  - Rewrote the first R3-4 response block to open with gratitude and direct agreement about the limitation of competition-only gLV models.
  - Moved the empirical justification for focusing on competitive interactions earlier: the 12-isolate coculture data show lower paired growth than monoculture expectations in most pairs, with the strongest strict net-competition signal in Base and Nutr$+$.
  - Added prose alignment with Coyte, Schluter and Foster (Science 2015) on competition as a dominant structuring force in microbial communities.
  - Reframed the facilitative-tail model as a direct test of whether the scenario extends beyond strict competition, emphasizing that facilitation can alter Mixture/Restructuring balance while the monotonic rise of Dominance with $\mu$ remains largely valid.
  - Recompiled `latex/revision/response_letter.tex` successfully.

- **Type**
  - Response text edit
  - PDF regeneration

### R3-4 figure provenance aligned with current split response figures

- **Affected reviewer points**: R3-4.

- **Files changed**
  - `latex/revision/revision_figure_folder/source.md`

- **What changed**
  - Updated the provenance entry for `R3_3_combined.pdf` to mark it as a superseded R3-4 composite rather than the active response figure.
  - Updated `R3_4_mixed_sign_higher_order.pdf` from a candidate/not-yet-embedded figure to the current Response Fig.~R3-4b.
  - Confirmed the active R3-4 response uses split figures `R3_4_experiment.pdf`, `R3_4_mixed_sign_higher_order.pdf`, `R3_4_simulation.pdf`, and `R3_4_pair_coupling_fine.pdf`.

- **Type**
  - Figure provenance cleanup
  - No manuscript or response-letter text change

### R3-3 reviewer question and response merged

- **Affected reviewer points**: R3-3.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Merged the two R3-3 reviewer-comment fragments into a single quoted question covering both the richness-confound null-model request and the request to show final-community richness across simulation $\mu$ and experimental media.
  - Reorganized the R3-3 answer into one continuous response covering simulation nulls, experimental richness, pool-size controls, and pairwise-selection-correlation evidence without changing the reported statistics.

- **Type**
  - Response structure edit

### R3-2 parent-vector norm-imbalance caveat quantified

- **Affected reviewer points**: R3-2, with conceptual link to R1-1 biomass/OD control.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/analyze_parent_norm_asymmetry.py`
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_parent_norm_asymmetry.pdf`
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/parent_norm_asymmetry_events.csv`
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/parent_norm_asymmetry_parent_vectors.csv`
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/parent_norm_asymmetry_raw_read_counts.csv`
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/parent_norm_asymmetry_summary.csv`
  - `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
  - `Figure_generate/code/Figure_revision/R3_1_additive_null/Fig_R3_2_additive_null_comparison.pdf`
  - `Figure_generate/code/Figure_revision/R3_1_additive_null/base_raw_count_additive_null_events.csv`
  - `latex/revision/revision_figure_folder/Fig_R3_2_parent_norm_asymmetry.pdf`
  - `latex/revision/revision_figure_folder/Fig_R3_2_additive_null_comparison.pdf`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Added an experimental norm-imbalance check for the additive-null caveat raised by the skewed-abundance toy model.
  - Quantified total 16S reads and raw ASV count-vector L$_2$ norms per parental community directly from `SEQanalysis/excludeNatural/M_OTUtableGreenGenes.csv`, before sample-wise normalization.
  - Regenerated Response Fig. R3-2C as a three-panel raw-count diagnostic: per-parent total-read histograms, per-parent raw count-vector norms, and paired lower/higher parent count-vector norms for each coalescence event.
  - Placed R3-2C before the current R3-2A/B figure blocks in the R3-2 response.
  - Replaced the previous R3-2A/R3-2B bar/scatter presentation with one Base-medium raw-count null figure: a manuscript-style similarity map with representative null-to-experiment arrows, paired directional PDI arrows for all 83 Base-medium synthetic events, and a raw-count-null-class to experimental-class transition heatmap.
  - Added a detailed response-text description of the raw-count additive-null motivation, hypothesis, event-by-event construction, classifier reuse, and paired statistical comparison.
  - Updated the R3-2 second-subquestion response to acknowledge that unequal parental vector norms are a real raw-count caveat, then show that Base-medium experimental PDI remains significantly greater than the event-matched raw-count additive null.
  - Added one concise cross-link to the Reviewer 1 OD control, noting that higher-biomass parental communities do not preferentially win Dominance events.

- **Type**
  - New response-only analysis figure
  - Response prose/caption update
  - Figure provenance update

### R3-2 skewed-abundance additive null added

- **Affected reviewer points**: R3-2.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/reproduce_reviewer_norm_figures.py`
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_reviewer_reproduction_L1.pdf`
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_reviewer_reproduction_L2.pdf`
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/reviewer_norm_comparison_summary.csv`
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L1.pdf`
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L2.pdf`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Added a fourth row to Response Fig.~R3-2.0a/b for simple additive mixing with skewed parental abundances sampled as `10^U(-3,0)`.
  - Preserved the previous Monte Carlo seeds for existing rows by assigning explicit seeds per normalization, null construction, and richness value.
  - Updated the R3-2 response text and caption to distinguish uniform additive mixing, which is primarily Mixture, from skewed additive mixing, which remains high-retention but can be classified as Dominance at low richness because the additive composition is abundance-skewed.

- **Type**
  - Response figure regeneration
  - Simulation script update
  - Response caption/prose update
  - Figure provenance update

### Reviewer 3 attachment cropped in response letter

- **Affected reviewer points**: R3-2.

- **Files changed**
  - `latex/revision/revision_figure_folder/Reviewer3_attachment_figures.pdf`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Cropped the local response-letter copy of the Reviewer 3 attachment so it shows only Reviewer Figures 1--3, removing the original A4 page whitespace and bottom page number.
  - Left the raw reviewer-supplied attachment unchanged in `latex/revision/raw/`.
  - Updated the caption and figure provenance to state that the response-letter copy is cropped from the reviewer attachment and is not assigned a Response Fig. R3-2 number.

- **Type**
  - Response figure crop
  - Response caption/provenance update

### R3-2 reviewer-null figure row subtitles

- **Affected reviewer points**: R3-2.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/reproduce_reviewer_norm_figures.py`
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L1.pdf`
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L2.pdf`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/source.md`

- **What changed**
  - Added explicit row subtitles to the reviewer-null reproduction figures: A, random restructuring with abundances `~ U(0, 1)`; B, random restructuring with abundances `~ 10^U(-3, 0)`; C, simple additive mixing `n_C = n_A + n_B`.
  - Regenerated the L1 and L2 PDFs and recopied them into the response figure folder.
  - Updated the Response Fig. R3-2.0a caption to define the three rows.

- **Type**
  - Response figure regeneration
  - Response caption edit
  - Figure provenance update

## 2026-05-11

### R1-2 pH-pair analysis integrated

- **Affected reviewer points**: R1-2.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/supplementary_figs/Fig_R1_2_acidalk_per_medium.pdf`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/TODO.md`

- **What changed**
  - Added the already drafted pH-mismatch / acid--alk winner-identity sentence to Results \S2.5, preserving the response-letter wording and replacing the placeholder figure number with Supplementary Fig.~33.
  - Copied the R1-2 response figure into the supplementary figure folder and added it as Supplementary Fig.~33.
  - Promoted R1-2 from `Blocked` to `Completed` in the Reviewer 1 response and TODO tracker.
  - Performed a notation-only cleanup of active author-written prose so the high-nutrient condition is consistently rendered as `Nutr$+$`; reviewer quotes, comments, and filenames were left unchanged.

- **Type**
  - Manuscript text integration
  - Supplementary figure insertion
  - Response status update
  - Notation cleanup

### R1-5 metric-sensitivity explanation aligned

- **Affected reviewer points**: R1-5, with consistency update to R2-2 metric-divergence wording.

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/extended_data.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`

- **What changed**
  - Replaced the R1-5 response with a concise explanation that Jaccard, Jensen--Shannon, and abundance-weighted metrics emphasize different aspects of community composition.
  - Updated Results \S2.1 and the Extended Data Fig.~2 caption so the response letter quotes actual manuscript-bound text rather than only describing the change.
  - Removed the overbroad phrasing that Jensen--Shannon and Jaccard both primarily weight presence/absence.

- **Type**
  - Response text edit
  - Manuscript text edit
  - Supplementary caption/methods edit

### Rebuttal terminology rule added

- **Affected reviewer points**: Global rebuttal workflow.

- **Files changed**
  - `revision.rule.md`
  - `latex/writing_rules.md`

- **What changed**
  - Added an explicit rebuttal-stage rule that manuscript terminology standards also apply to response-letter prose, captions, response-only figure labels, response-figure generation code, and figure provenance text.
  - Added the two common checks from the terminology cleanup pass: use `parental community/communities` instead of standalone `parent/parents`, and use `Mixture` rather than `Mixing` for the outcome class.
  - Updated the practical workflow to require checking both captions and figure-generation code before finalizing regenerated response figures.

- **Type**
  - Workflow rule
  - Terminology standard

### Response-letter terminology cleanup: parent/Mixing

- **Affected reviewer points**: R1-1, R1-2, R1-3, R1-4, R2-2, R2-3, R3-1, R3-2, R3-3.

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/revision_figure_folder/*.pdf` for the regenerated response figures touched by the terminology pass
  - `latex/supplementary_figs/marginal_distributions_by_medium.pdf`
  - `latex/supplementary_figs/Fig_R1_3_per_medium_scatter.pdf`
  - Figure-generation scripts under `Figure_generate/code/Figure_revision/` for R1-1, R1-2, R1-3, R1-4, R2-3, R3-1, R3-2, and R3-3 richness analyses.

- **What changed**
  - Replaced author-side `parent`/`parents` noun usage with `parental community/communities` where it appeared in the response letter terminology pass.
  - Replaced outcome-class `Mixing` with `Mixture` in response captions/prose and in regenerated reviewer-facing figure labels.
  - Left reviewer-quoted text unchanged.
  - Recompiled `latex/revision/response_letter.tex` successfully after regenerating and copying the updated PDFs.

- **Type**
  - Response text terminology edit
  - Figure-generation code terminology edit
  - Response figure regeneration
  - Figure provenance text update

### Response-letter paragraph spacing aligned to raw Reviewer 2 structure

- **Affected reviewer points**: Reviewer 2 response formatting; internal memo readability.

- **Files changed**
  - `latex/revision/response_letter.tex`: added modest paragraph spacing (`\parskip`) and removed paragraph indentation so response paragraphs separate visibly in the compiled PDF.
  - `latex/revision/internal_memo.tex`: applied the same paragraph-spacing convention for consistency with the response letter.
  - `latex/revision/response/reviewer2_response.tex`: restored the raw Reviewer 2 paragraph breaks in the quoted reviewer comments, especially R2-1, where the original review separates the central claim, bullet list, conceptual question, consumer-resource point, and closing request.
  - `latex/revision/response/reviewer3_response.tex`: moved one R3-2 response sentence from the pre-answer context block to the response body after `\responselabel`.

- **What changed**
  - The response letter now follows the original raw Reviewer 2 line/paragraph splitting instead of collapsing multi-paragraph comments into a single dense block.
  - Structure-only audit of Reviewer 1 and Reviewer 3 found no missing paragraph/list structure in the quoted question text. Reviewer 1's raw review is a bullet list of one-paragraph questions, represented as separate response subsections; Reviewer 3's only multi-paragraph question is R3-2, which already preserved paragraphs, equations, and attachment placeholders.
  - No scientific wording, response claims, figures, status markers, or manuscript-bound `\mschange{}` text were changed.
  - Recompiled `latex/revision/response_letter.tex` and `latex/revision/internal_memo.tex`. The response letter now builds to 37 pages; the internal memo builds to 33 pages.

- **Type**
  - Formatting/readability edit
  - PDF regeneration

---

### R3-1 traceability audit: response quotes aligned to source

- **Affected reviewer points**: R3-1 (P1, L$_1$ vs L$_2$ normalization clarification).

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`: updated the Results \S2.1 and Supplementary Methods `\mschange{}` snippets so the blue manuscript-bound text matches the current manuscript/SI wording rather than paraphrasing it. The Results snippet uses the rendered `Fig.~1B` form rather than the manuscript-only `\figref{}` macro so the standalone response letter remains compileable.
  - `latex/revision/TODO.md`: updated the last-checked date and R3-1 next action to record that quote/source traceability has been checked.

- **What changed**
  - Confirmed the implemented metric is L$_2$/cosine: `common_setup.normalize()` divides by Euclidean norm, and `metric_VectorDecomposition_onlyPositive()` applies that normalization to both parents and the coalesced community before computing projection/dot-product terms.
  - Confirmed main Results, Fig.~1B caption, Methods, and Supplementary Methods all state the same workflow: relative-abundance vectors are used as the abundance representation, then L$_2$ normalization is applied for the similarity calculation.
  - Left the R3-1 status marker as `Before review`; `revision.rule.md` says promotion requires an explicit joint review pass.

- **Type**
  - Response-letter traceability edit
  - No manuscript text edit, no analysis change

---

## 2026-05-11

### Q5b environmental-filtering model richness-matched gamma calibration

- **Affected reviewer points**: R2-2 (alternative explanations for community-level selection); internal Q5b environmental-filtering control.

- **Files changed**
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/environmental_filter_model.py`: changed the default filter levels to a gamma-only nutrient calibration with fixed `theta = 0` and `sigma = 1`.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/simulate_Q5_phase_environmental_filter.py`: rerun to regenerate `Q5_phase_events_filter.csv`.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/make_Q5_phase_environmental_filter.py`: updated panel labels/title for the gamma-only richness-matched Nutr-/Base/Nutr+ filters and regenerated `Fig_Q5_phase_filter.{pdf,png,svg}`.
  - `latex/revision/revision_figure_folder/internal_Q5_phase_filter.pdf`: replaced with the regenerated richness-matched figure.
  - `latex/revision/revision_figure_folder/source.md`: updated figure provenance and interpretation.
  - `latex/revision/internal_memo.tex`: updated Q5b parameter table, figure caption, interpretation, and pending-deliverables summary.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/README.md`: updated description of the environmental-filter calibration.

- **What changed**
  - Replaced the earlier weak/mid/strong filter design, which changed `theta`, `sigma`, and `gamma` together, with a one-knob selection-strength calibration: Nutr- `gamma = 2.80`, Base `gamma = 7.95`, Nutr+ `gamma = 10.15`, with `theta = 0`, `sigma = 1`, and threshold `0.02` fixed.
  - These values target the observed P12 coalesced richness means (Nutr- 13.44, Base 9.62, Nutr+ 8.85). The regenerated 500-pool-per-condition run gives mean coalesced richness 13.5 / 9.8 / 8.8 for Nutr- / Base / Nutr+.
  - Outcome fractions under the richness-matched filters are overwhelmingly Mixture: Dominance 0.0% / 1.2% / 1.0% for Nutr- / Base / Nutr+. The internal memo interpretation was updated accordingly: environmental filtering can reproduce the richness scale but does not explain the observed Dominance trend when constrained to observed P12 coalesced richness.

- **Type**
  - Simulation parameter recalibration
  - Figure regeneration + import
  - Internal-memo update
  - Provenance update
  - No manuscript or response-letter changes

---

## 2026-05-10

### Q5b trait-based environmental filtering model implementation

- **Affected reviewer points**: R2-2 (alternative explanations for community-level selection); Q5 internal alternative-model planning.

- **Files changed**
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/environmental_filter_model.py` (new): reusable interaction-free trait-filtering model with latent species traits and medium-specific Gaussian filters.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/simulate_Q5_phase_environmental_filter.py` (new): event-level simulation driver writing `Q5_phase_events_filter.csv`.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/make_Q5_phase_environmental_filter.py` (new): Q5-pH-style phase-diagram renderer.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Q5_phase_events_filter.csv` (generated): 1,500 event-level rows across weak/mid/strong filters.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Fig_Q5_phase_filter.pdf` (generated): phase diagram for the filtering model.
  - `latex/revision/revision_figure_folder/internal_Q5_phase_filter.pdf` (new import): local copy for the internal memo.
  - `latex/revision/revision_figure_folder/source.md`: added provenance entry for `internal_Q5_phase_filter.pdf`.
  - `latex/revision/internal_memo.tex`: added and then updated the `Trait-based environmental filtering model for nutrient-dependent niche availability` section after the Q5 pH/gLV alternative-framework section and before the gLV-scope limitations section.

- **What changed**
  - Implemented a fourth Q5 alternative model testing whether nutrient-dependent environmental filtering alone can reproduce reduced diversity and increased Dominance at higher nutrient.
  - The model assigns each species a latent trait, assigns each filter level a center/breadth/strength, maps higher nutrient to a narrower/stronger shifted filter, assembles parents and coalesced communities through the same filter, and then uses the existing L2/cosine outcome-classification and `|\phi|` pipeline.
  - Q5-filter result: weak filter gives 0% Dominance / 100% Mixture / 0% Restructuring with mean coalesced richness 22.4; mid filter gives 4% / 96% / 0% with richness 8.4; strong filter gives 57% / 43% / 0% with richness 2.8 and mean `|\phi|=0.56`.
  - Updated the internal memo interpretation: filtering alone can create Dominance when the high-nutrient niche filter is severe, but this requires a strong survivor bottleneck and does not replace the broader interaction-strength interpretation.
  - Updated the Q5b line in the internal memo's pending-deliverables summary to `Implemented`.

- **Type**
  - New simulation code
  - New figure generation + import
  - Internal-memo update
  - Provenance update
  - No manuscript or response-letter changes

---

### R1-3 per-medium-only response figure and significance framing

- **Affected reviewer points**: R1-3 (Fig. 5C circularity / PDI excluding dominant species).

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`: updated `Fig_R1_3_per_medium_scatter` annotations to include slope plus independent-event Spearman rho and p-values for each per-medium panel.
  - `latex/revision/revision_figure_folder/Fig_R1_3_per_medium_scatter.pdf`: regenerated and recopied.
  - `latex/revision/response/reviewer1_response.tex`: removed the merged Base+Nutr+ summary from R1-3 and reframed the response around per-medium Base and Nutr+ results only.
  - `latex/revision/revision_figure_folder/source.md`: updated provenance text to document the no-pooling convention and Spearman annotations.

- **What changed**
  - Response Fig. R1-3 now presents Base and Nutr+ separately, with no pooled Base+Nutr+ claim.
  - R1-3 response now emphasizes that Nutr+ remains statistically supported after dominant-species removal: Spearman rho `0.41` (`p=8.2e-4`) for mix-winner removal and rho `0.42` (`p=1.3e-3`) for parent-dominant removal, while Base does not retain a significant post-removal correlation.
  - 2026-05-10 follow-up: removed the per-panel `n=` annotation from Response Fig. R1-3 while retaining compact Spearman p-value labels.
  - 2026-05-10 follow-up: added a caption sentence defining the plotted Spearman `p` values as two-sided rank-correlation tests of the null hypothesis of no monotonic association.
  - 2026-05-10 follow-up: revised the R1-3 opening sentence to comply better with `style_insights.md` by leading with the direct mixed answer (Base does not survive removal; Nutr+ is reduced but remains significant).

- **Type**
  - Figure regeneration + import
  - Response-letter number/significance update
  - Provenance update

---

## 2026-05-10

### R1-4 pool-size figure regrouping

- **Affected reviewer points**: R1-4 (pool-size effects).

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`: changed the experimental Dominance and experimental pairwise-selection panels so initial species pool size is the explicit grouping variable. Panel B now shows medium on the x-axis with bars grouped and colored by initial pool size; panel C uses initial pool size as the color grouping for same/cross pairwise species selection.
  - `latex/revision/revision_figure_folder/pool_size_analysis.pdf`: regenerated and recopied.
  - `latex/revision/revision_figure_folder/pool_size_by_medium.pdf`: regenerated and recopied.
  - `latex/revision/response/reviewer1_response.tex`: updated the Response Fig. R1-4 caption to match the regrouped experimental panels.
  - `latex/revision/revision_figure_folder/source.md`: updated the R1-4 provenance description.

- **What changed**
  - The previous figure put initial pool size on the x-axis in panel B but used medium as the color grouping, which made the intended grouping by initial species pool size visually ambiguous.
  - The regenerated response figure now makes pool size the grouping/legend variable in the experimental panels while preserving the same underlying statistics (`\chi^2 = 2.24`, `p = 0.69`).
  - Follow-up correction: panel A now also uses the same two-factor grouping as panel B, with medium on the x-axis and initial species pool size as the grouped/color variable.

- **Type**
  - Figure-style regrouping
  - Figure regeneration + import
  - Response-caption update
  - Provenance update

## 2026-05-08

### R1-3 original-anchored filtering for dominant-species removal plots

- **Affected reviewer points**: R1-3 (Fig. 5C circularity / PDI excluding dominant species).

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`: changed the Fig. 5C-style pairwise/PDI filtering so Original defines the event set. Dominant-removal columns now recompute community-level PDI on events that pass the original non-Restructuring filter and original pairwise-assay lookup, rather than re-filtering each group after PDI recalculation.
  - `latex/revision/revision_figure_folder/Fig_R1_3_per_medium_scatter.pdf`: regenerated and recopied.
  - `latex/revision/revision_figure_folder/Fig_R1_3_per_medium_R2.pdf`: regenerated and recopied.
  - `latex/revision/revision_figure_folder/Fig_R1_3ab_PDI_comparison.pdf` and `Fig_R1_3d_R2_comparison.pdf`: regenerated and recopied.
  - `latex/revision/response/reviewer1_response.tex`: updated R1-3 numerical values and added the original-anchored filtering clarification.
  - `latex/revision/revision_figure_folder/source.md`: added provenance entries for the current per-medium R1-3 figures and documented the filtering convention.

- **What changed**
  - The comparison now tests alternative PDI calculations on the same original-selected events, which is the appropriate design for the circularity question.
  - Updated pairwise Fig. 5C-style result: Original M+H combined remains `n=97`, `R^2=0.34`; dominant-from-mix removal is now `n=96`, `R^2=0.12` (one event becomes empty after removal).
  - Updated per-medium results: Base `R^2=0.11/0.00/0.07` with `n=34/34/34`; Nutr+ `R^2=0.49/0.24/0.18` with `n=63/62/55` for Original / mix-dominant removed / parent-dominants removed.

- **Type**
  - Analysis-script filtering correction
  - Figure regeneration + import
  - Response-letter number update
  - Provenance update

---

## 2026-04-30

### Internal memo K/r heterogeneity gLV stress test

- **Affected reviewer points**: R2-1 / R2-6 model-scope framing; internal memo gLV failure-mode section.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R2_6_gLV_K_r_heterogeneity/analyze_K_r_heterogeneity.py`: corrected to use the same finite-time ODE endpoint and random-stream structure as `run_48species_100reps_final.py`, while only changing sampled `K_i` and `r_i`.
  - `latex/revision/internal_memo.tex`: replaced the earlier equilibrium-shortcut K/r result with a pending-status note.
  - `latex/revision/revision_figure_folder/source.md`: marked the previous `Fig_Q6_Kr_{phase_trend,winner_direction}.pdf` files as superseded / do not cite.

- **What changed**
  - The earlier K/r result used a feasible-equilibrium shortcut. That was not the same as the manuscript gLV figure pipeline and inflated Restructuring even at `K_sd = r_sd = 0`.
  - The corrected script preserves the canonical interaction matrix, community assignment, initial abundances, time horizon, extinction threshold, and classification pipeline. With `K_sd = r_sd = 0`, it matched the stored canonical run for the first 10 replicate pools tested (180/180 event classifications).
  - The full K/r heterogeneity grid remains pending because high-heterogeneity ODE cells are slow. No numerical K/r conclusion should be cited until the ODE-consistent grid finishes and the baseline panel passes this reproduction check.

- **Type**
  - Simulation-method correction
  - Internal-memo evidence downgrade
  - Provenance update

---

## 2026-04-30

### Internal memo gLV failure-mode review

- **Affected reviewer points**: R2-1 / R2-6 model-scope framing; internal memo sections on gLV failure modes and unexplained data features.

- **Files changed**
  - `latex/revision/internal_memo.tex`: replaced the stale placeholder "Failure 1 / Failure 2" block with two completed scope-limit sections: (1) negative OD--PDI / denser-parent-loses direction in Base/Nutr$+$, and (2) natural-community Restructuring excess / non-competitive interactions.
  - `latex/revision/internal_memo.tex`: updated the memo purpose sentence so it no longer says the document consists of placeholder answers.
  - `latex/revision/internal_memo.tex`: corrected Q6 wording from "ran simulation" to the intended baseline outcome-class simulation phrasing.

- **What changed**
  - The memo now uses one consistent framing: these are baseline-gLV scope limits, not refutations of the interaction-strength claim.
  - The early narrative section now aligns with the later Q6 triage table, which remains the detailed itemized version.

- **Type**
  - Internal-memo text cleanup
  - Scope-framing review

---

## 2026-04-30

### R1-1 OD-density figure readability refresh

- **Affected reviewer points**: R1-1, R2-2 reuse, internal memo Q1.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_OD_density.py`: updated the consolidated Winner OD vs Loser OD response figure so OD axes extend slightly below zero and Dominance points use lower opacity.
  - `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_per_medium_OD_PDI_zoom.py`: applied the same below-zero OD padding and lower point opacity to the per-medium zoom panels used in the internal memo.
  - `latex/revision/revision_figure_folder/Fig_R1_1A_winner_loser_OD.pdf`: regenerated and recopied for the response letter.
  - `latex/revision/revision_figure_folder/internal_{LN,MN,HN}_OD_PDI_zoom.pdf`: regenerated and recopied for the internal memo.
  - `latex/revision/revision_figure_folder/source.md`: provenance notes updated to document the readability change.

- **What changed**
  - Low-OD points in Base and Nutr$+$ no longer sit directly on the plot frame, because the visible OD window now starts slightly below zero while the biological zero remains inside the axis.
  - Dominance points are semi-transparent, making overlapping low-OD events easier to see without changing the underlying statistics.

- **Type**
  - Figure-style regeneration
  - Provenance update

---

## 2026-04-30

### R3-2 boundary-convention clarification (reviewer $r=1/2$ vs manuscript $r=1/\sqrt{2}$)

- **Affected reviewer points**: R3-2 (P0, dimensionality artifact in similarity metrics); R3-1 normalization/boundary clarity follow-on.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/reproduce_reviewer_norm_figures.py`: updated the reviewer-style toy-null figure renderer so every scatter panel overlays both retention-boundary conventions: the reviewer's visual guide at $r=1/2$ (gray dotted arc) and the manuscript classifier at $r=1/\sqrt{2}$, equivalently $x^2=0.5$ (black dashed arc). The stacked class-fraction bars remain computed with the manuscript classifier.
  - `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`: refreshed the additive-null R3-2A/B figure styling so R3-2A uses a neutral opacity legend for observed vs null rather than class-colored legend handles, and R3-2B labels the plotted classifier coordinates as retention and asymmetry.
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L{1,2}.pdf`: regenerated and recopied from the updated renderer.
  - `latex/revision/revision_figure_folder/fig1_paired_classification.pdf` and `fig6_asymmetricity_space.pdf`: regenerated and recopied after the R3-2A/B style check.
  - `latex/revision/response/reviewer3_response.tex`: rewrote the opening R3-2 response to distinguish the reviewer's display boundary from the manuscript classifier boundary, replaced the ambiguous "PDI $=0.5$" wording with angular asymmetry $y=0.5$, updated the toy-null numbers to emphasize Restructuring fractions under the manuscript classifier, and added an integrated manuscript-change note.
  - `latex/revision/response/reviewer2_response.tex`: removed the cross-reference to the superseded Response Fig. R3-2E threshold-sensitivity sweep from R2-3, keeping the threshold-dependence discussion tied to continuous coordinates and the current R3-2 null-model response.
  - `latex/sections/methods.tex`: added a `\rev{}`-wrapped sentence stating that the Restructuring boundary is $x^2 \le 0.5$, equivalently $x \le 1/\sqrt{2}$ in the similarity map.
  - `latex/supplementary_sections/supplementary_methods.tex`: added `\rev{}`-wrapped clarification that $x^2=0.5$ corresponds to radius $x=1/\sqrt{2}$, not $x=1/2$.
  - `latex/revision/revision_figure_folder/source.md`: updated provenance descriptions for the regenerated R3-2.0a/b figures.

- **What changed**
  - Corrects a subtle but important reviewer-psychology issue: the reviewer's toy phase diagrams visually used an $r=1/2$ restructuring guide, whereas our actual classifier uses $x^2=0.5$ ($r=1/\sqrt{2}$). The response now makes the distinction explicit instead of letting the reader infer it.
  - Under the manuscript boundary, the reviewer's own toy constructions behave in the expected direction: random restructuring becomes predominantly Restructuring at moderate-to-large $N$, and passive additive mixing sits on the symmetric Mixing axis. This strengthens the R3-2 response before the case-by-case experimental additive-null result.
  - Removed the previous Response Fig. R3-2.0b, R3-2C, and R3-2E blocks, plus their connecting text and a downstream R2-3 cross-reference, because they broadened the response beyond the revised boundary/null-model point and are no longer needed for this answer. The L$_1$ comparison is retained only as a brief prose note.

- **Type**
  - Figure regeneration (boundary overlay)
  - Response-letter text edit
  - Manuscript Methods clarification
  - Supplementary Methods clarification
  - Provenance update

---

## 2026-04-30

### R3-4 Version A mixed-sign facilitative-tail gLV with higher-order self-limitation

- **Affected reviewer points**: R3-4 (P2, gLV excludes facilitation).

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mixed_sign_higher_order.py` (new): implements the true facilitation-facing model. Dynamics are `dn_i/dt = n_i (1 - (A n)_i - gamma n_i^2)` with fixed `gamma = 0.10`; off-diagonal coefficients are sampled iid from `U[-f mu, (2+f) mu]`, so the mean interaction coefficient remains `mu` while the facilitative tail increases with `f`.
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mixed_sign_higher_order_figure.py` (new): renders the R3-4-style stacked outcome bars.
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/mixed_sign_higher_order_results.json` (new): 15-cell sweep over `mu = 0.30, 0.60, 0.80` and `f = 0, 0.10, 0.20, 0.40, 0.80`, 200 pools per cell.
  - `Figure_generate/code/Figure_revision/R3_4_mixed_sign_higher_order.{pdf,png,svg}` (new): rendered output figure.
  - `latex/revision/revision_figure_folder/R3_4_mixed_sign_higher_order.pdf` (new import).
  - `latex/revision/revision_figure_folder/source.md`: provenance entry added.
  - `latex/revision/internal_memo.tex`: planning block added that separates Version A (true mixed-sign facilitation/exploitation with density-dependent self-limitation) from Version B (reciprocal-correlation / pair-coupling robustness).
  - `latex/revision/response/reviewer3_response.tex`: R3-4 response updated to show all three figures (pairwise coculture additivity, mixed-sign facilitative-tail gLV, reciprocal pair-coupling robustness).
  - `latex/revision/response_letter.pdf`: recompiled.

- **What changed**
  - This is the direct facilitation-facing alternative requested for R3-4. Unlike the existing signed-`p` correlation sweep, this model actually permits facilitative ecological effects (`alpha_ij < 0` under the manuscript sign convention) while preserving the mean coefficient `E[alpha_ij] = mu`.
  - Numerical integration used LSODA instead of RK23 for this mixed-sign higher-order model, because the strongest facilitative-tail cells were stiff with RK23. The ODE definition and classification pipeline are otherwise unchanged.
  - Main result: Dominance still increases with `mu` at every facilitative-tail strength. At low `mu`, increasing `f` shifts outcomes away from Mixture toward both Dominance and Restructuring (Dom/Mix/Res at `mu=0.30`: 18/73/9% at `f=0`; 43/33/24% at `f=0.8`). At high `mu`, Dominance remains high across the facilitative tail (about 70-76%). Rejection and coalescence-failure rates remain modest with `gamma=0.10`.
  - The R3-4 response now distinguishes true facilitation (negative `alpha_ij` values under the manuscript sign convention; Version A) from reciprocal-correlation structure under a non-negative marginal (Version B). The old `p>0` panels are now described as symmetric competition rather than ecological cooperation.
  - All three R3-4 figures are now shown in the response: Response Fig. R3-4a (pairwise coculture additivity), Response Fig. R3-4b (mixed-sign facilitative-tail gLV with density-dependent self-limitation), and Response Fig. R3-4c (reciprocal pair-coupling robustness).
  - Follow-up polish: R3-4c was regenerated with panels ordered monotonically from `p=-1` to `p=+1`; class-fraction checks confirmed Dominance/Mixture/Restructuring fractions sum to 1.000000 in every (`p`, `mu`) cell.
  - Added a separate fine-resolution reciprocal pair-coupling sweep (`p=-1,-0.8,...,+1`) as Response Fig. R3-4d. The 33-cell sweep completed with all class fractions normalized and minimum usable event count 1158/1200.

- **Type**
  - New simulation code
  - New figure generation
  - Revision-figure import + provenance
  - Internal-memo planning update
  - Response-letter text edit + figure insertion
  - Compileability confirmation
  - No manuscript text edit

---

## 2026-04-30

### Q5 pure-pH model aligned to original Ratzke simulation form

- **Affected reviewer points**: R2-1 / R2-2 / R2-6 framing support; internal memo Q5 ("Beyond the pairwise model: alternative frameworks").

- **Files changed**
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/pH_feedback_model.py`: updated the pure pH-feedback model to the original-code-like form: Gaussian kernel denominator `2 p_c^2`, per-species logistic term `n_i(1-n_i)`, `p_o ~ U(4.5, 9.5)`, `p_c = 2.5`, random signed `c_i ~ U(-c_max, c_max)`, `K = 1e10`, `k_growth = k_death = 10`, and a continuous additive relaxation term toward `p_fresh = 7` instead of the original daily dilution/reset loop. Reduced default integration horizon to 200 after sanity checks confirmed steady-state behavior.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/simulate_Q5_all_models.py`: updated pure-pH parameter settings to the original-code-like sampling (`p_o` range, fixed `p_c`, random signed `c_i`) and switched the pure-pH sweep to the public-code interaction-strength grid `0, 1e-10, 1e-9, 1e-8, 1e-6, 1e-5, 1e-4, 1e-2` (stored as `tau = interaction_strength / 1e-10`).
  - Coalescence events in the pH-feedback simulations initialize the environmental coordinate from the stabilized parents, `p_AB,0 = (p_A + p_B)/2`, matching the 50/50 biomass merge rather than resetting to fresh medium.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/test_sanity.py`: adjusted checks for per-species logistic carrying scale.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/README.md`: updated equation and parameter documentation.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Q5_all_models_results.json`: regenerated pure-pH entries only.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Q5_phase_events.csv`: regenerated pure-pH phase-diagram rows only.
  - `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Fig_Q5_phase_{gLV,pH,hybrid}.pdf` and `Fig_Q5_three_models_per_model.pdf`: regenerated from the updated event/result files.
  - `latex/revision/revision_figure_folder/internal_Q5_phase_{gLV,pH,hybrid}.pdf` and `internal_Q5_three_models_per_model.pdf`: refreshed local memo figure copies.
  - `latex/revision/revision_figure_folder/source.md`: updated Q5 provenance and interpretation.
  - `latex/revision/internal_memo.tex`: updated Q5 equations, captions, and conclusions.
  - `latex/revision/internal_memo.pdf`: recompiled.

- **What changed**
  - The pure pH-feedback alternative is now much closer to the public Ratzke `Interaction-biodiversity-stability` simulation equations while remaining compatible with coalescence-style single assembly/merger integrations.
  - After replacing the bounded relaxation term with plain relaxation and excluding degenerate pH events where A, B, or C has no survivor, the pure-pH model was rerun with 100 pools. Clean representative pH points `c_max=1e-10/1e-9/3e-8` give Dominance `2/37/59%` in the summary run and `0/37/56%` in the phase run. The original-grid high end (`c_max >= 1e-6`) is dominated by excluded boundary-collapse events (79-85 per 100), so it is no longer treated as an ordinary high-strength coalescence regime.
  - Q5 framing changed accordingly: pure pH feedback alone is no longer treated as a plausible replacement on Dominance frequency; it remains useful as a calibrated future model for winner-direction effects, especially Nutr+ pH asymmetry. Intermediate pH strengths can produce moderate `|phi|`, but not the paired high-Dominance/high-`|phi|` pattern of gLV.

- **Type**
  - Model-equation update
  - Simulation refresh (pure-pH entries/rows)
  - Internal-memo figure refresh
  - Internal-memo text update
  - No manuscript edit
  - No response-letter edit

## 2026-04-23

### R3-2 figures regenerated against manuscript pipeline (Figs. R3-2.0a / R3-2.0b)

- **Affected reviewer points**: R3-2 (P0, dimensionality artifact in similarity metrics). Follow-on from R3-1.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/reproduce_reviewer_norm_figures.py`: refactored. The L$_2$ path now calls `common_setup.metric_VectorDecomposition_onlyPositive`, `calculate_assymetricity`, and `characterize_case` directly (the exact manuscript pipeline used for Fig. 1E), rather than a local raw-dot-product reimplementation. The L$_1$ path keeps the local raw-dot-product computation (no manuscript counterpart) but is routed through `common_setup.characterize_case` so the classification thresholds come from the canonical source. Added `verify_L2_against_raw_dot_product()` asserting zero drift between the manuscript pipeline and a raw L$_2$ dot product for the reviewer's non-overlapping-parent nulls; called first in `main()` so the script refuses to run if `common_setup` ever changes in a way that alters Fig. R3-2.0a's meaning. Reduced `N_SAMPLES` from 20000 to 1000 (MC standard error ~1.5pp on fractions, still well within signal).
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L{1,2}.pdf`: regenerated from the refactored script.
  - `latex/revision/response/reviewer3_response.tex` R3-2 response prose: updated the Dominance fractions for random-restructuring ($40.6/22.0/9.2/7.0\%$, was $42.4/21.2/10.9/6.4\%$) and the additive-Mixing fractions ($80.5/97.4/99.1/99.7\%$, was $82.0/96.3/99.2/99.8\%$) to match the N=1000 regeneration; relaxed the caption's "$\geq 82\%$" claim to "$\geq 80\%$" (the N=2 additive-Mixing bin is 80.5% at N=1000, so the earlier bound no longer holds to the tenth of a percent). Added a one-sentence statement in the R3-2.0a caption documenting that the L$_2$ path is the manuscript pipeline and that a runtime assertion guarantees parity with raw cosine similarity.
  - `latex/revision/response_letter.pdf`: recompiled.

- **What changed**
  - Direct answer to the R3-1-style concern applied to R3-2 itself: the L$_2$ similarity + classification in Figs. R3-2.0a/b is now literally the same code path that produces Fig. 1E, not a local reimplementation that happens to agree. The 1200-event runtime assertion confirms zero drift (max scatter-coord difference 1.77e-14, zero classification disagreements).
  - Response-letter numbers now match the figure to the tenth of a percent.

- **Type**
  - Analysis-script refactor (manuscript-pipeline routing + verification assertion)
  - Figure regeneration (R3-2.0a/b at N=1000)
  - Response-letter number update (text aligned with regenerated figures)
  - No manuscript text edit, no statusline promotion

---

## 2026-04-22

### R3-1 close-out: methods.tex normalization wording aligned (L$_2$/cosine)

- **Affected reviewer points**: R3-1 (P1, L$_1$ vs L$_2$ normalization clarification).

- **Files changed**
  - `latex/sections/methods.tex` \S Classification of Coalescence Outcomes: replaced the ambiguous "normalized abundance vector ... dot product" sentence at line 39 with a `\rev{}`-wrapped clarification matching the wording already in Results \S2.1, Fig.~1B caption, and Supplementary Methods. The Methods section now explicitly states (i) relative-abundance vector representation, (ii) L$_2$ normalization for the similarity calculation, and (iii) that the metric is cosine similarity (equivalently, the dot product of the L$_2$-normalized vectors).
  - `latex/revision/response/reviewer3_response.tex` (R3-1 block): added a fourth "Manuscript changes" bullet quoting the new Methods wording in blue per README Rules 4 and 10; also trimmed the over-apologetic "Our previous wording compressed two distinct steps ..." sentence in the response prose, and updated the sentence listing integrated changes to include the Methods edit.
  - `latex/main.pdf` (recompiled).

- **What changed**
  - Closes a Rule 8 (reviewer-to-manuscript traceability) leak: the response letter had promised three manuscript edits but the Methods blurb at `methods.tex:39` still carried the exact "normalized abundance vector" / "dot product" phrasing the reviewer flagged. A method-seeking reader landing in Methods now sees the same L$_2$/cosine language used everywhere else.
  - No new analysis, no new figure, no statusline promotion. `\statusline{Before review}{95\%}` retained per Rule 11 (promotion requires a joint co-review pass, not solo edits).

- **Type**
  - Manuscript text edit (Methods classification paragraph)
  - Response-letter text edit (R3-1 Manuscript-changes bullet expanded, response prose trimmed)
  - No new figure, no supplementary change, no statusline promotion

### Internal memo Q1 gLV-simulation counterpart (Figs. LN-sim / MN-sim / HN-sim)

- **Affected reviewer points**: R1-1 (P0), R2-1 (P0). Internal memo section \S Q1 "In Nutr-/Base/Nutr+, can community OD explain PDI?".

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_per_medium_biomass_PDI_zoom_simulation.py` (new script): simulation analogue of `analyze_per_medium_OD_PDI_zoom.py`. Loads `Simulation_Data/48species_100reps_final/Community_100reps_final.json`, replaces community OD by total final-day biomass $\sum_i y_i$, and reruns the identical `common_setup.metric_VectorDecomposition_onlyPositive` -> `calculate_assymetricity` -> `characterize_case` pipeline on each (sc_list[i], sc_list[j], cc_list["i_j"]) triple. Writes three combined 1x2 figures `Fig_{LN,MN,HN}_zoom_simulation_combined.{pdf,svg,png}` plus per-panel variants. Per-medium statistics printed to stdout.
  - `latex/revision/revision_figure_folder/internal_{LN,MN,HN}_biomass_PDI_zoom_simulation.pdf` (new imports; copied from `Figure_revision/R1_1_OD_density/`).
  - `latex/revision/revision_figure_folder/source.md`: three new provenance entries directly before the `internal_Q3_pH_rule_vs_gLV.pdf` block.
  - `latex/revision/internal_memo.tex`: added a new `\subsection*{gLV-simulation counterpart}` directly after the HN-zoom experimental figure in \S Q1, with a two-paragraph framing (pipeline identity + key contrast) and three `\begin{figure}` blocks (LN-sim / MN-sim / HN-sim). No `\rev{}` wraps (internal memo only; not manuscript-facing).
  - `latex/revision/internal_memo.pdf`: recompiled, 20 pages (was 18), clean.

- **What changed**
  - **Scientific result.** In the canonical 48-species 100-rep main-text gLV run, the denser parent \emph{wins} at all three interaction strengths: winner-denser $= 86\%$ at $\mu=0.3$ (binomial $p = 1.2\times 10^{-15}$), $65\%$ at $\mu=0.6$ ($p = 8.4\times 10^{-9}$), $65\%$ at $\mu=0.8$ ($p = 1.4\times 10^{-9}$). The signed $\Delta$biomass--PDI correlation is \emph{positive} in all three: Spearman $\rho = +0.42 / +0.29 / +0.30$ at $\mu = 0.3/0.6/0.8$. This is the opposite sign from the experimental zooms (especially HN, where winner-denser is $13\%$ and $\rho = -0.60$).
  - **Rebuttal value.** This is a clean demonstration that the experimental "denser parent loses" pattern (Nutr$+$, and weakly in Base/Nutr$-$) is not a feature a random-$\alpha_{ij}$ competition-only gLV can reproduce. The internal memo now has a side-by-side experimental/simulation comparison in \S Q1 that directly supports the R2-1 and R1-1 interpretation: biomass-based displacement is gLV-native, identity-based displacement (pH-mediated acid-producer asymmetry; R1-2, Q3) is not.
  - **Pipeline identity.** The simulation script imports the same `common_setup` helpers used by the experimental script, so the only difference between the two sides of the comparison is (i) the data source (simulation JSON vs experimental coalescence/sequence tables) and (ii) the "OD" observable (total biomass vs community OD$_{600}$).

- **Type**
  - New analysis script (simulation pipeline on main-text gLV JSON)
  - Three revision-figure imports into `revision_figure_folder/`
  - Internal-memo figure insertions + framing paragraphs (no `\rev{}`, not manuscript-facing)
  - No manuscript text edit
  - No response-letter edit
  - Compileability of `internal_memo.tex` re-verified

### R2 reflection-driven revision pass (R2-1 through R2-minor)

- **Affected reviewer points**: R2-1, R2-2, R2-3, R2-4, R2-5, R2-6, R2 minor.

- **Files changed**
  - `latex/supplementary_sections/figures.tex`: added Supp Fig. 28 (invasion-fitness vs $\mu$, `invasion_fitness_supp.pdf`) and Supp Fig. 29 (continuous per-medium PDI / retention marginals, `marginal_distributions_by_medium.pdf`). Both captions wrapped in `\rev{}`.
  - `latex/supplementary_figs/marginal_distributions_by_medium.pdf`: copied from `latex/revision/revision_figure_folder/`.
  - `latex/sections/results.tex` §2.1: expanded Restructuring definition with a `\rev{}`-wrapped elaboration and cross-reference to Supp Fig. 29.
  - `latex/revision/response/reviewer2_response.tex`:
    - R2-1: softened the "feature rather than confounder" phrasing; trimmed paragraph 2 by ~30%; promoted status to `Completed`.
    - R2-2: inserted an explicit Nutr+ concession (pH-modifying dominants; cross-ref to R1-2 acidic-parent 86.4% win rate); split the manuscript-change block into Integrated (Mansour2018 citation in Discussion) and Blocked (Results §2.4 invasion-resistance clarifier). Status demoted to `Blocked` per Rule 1 because the Results §2.4 clarifier is not yet in the manuscript.
    - R2-3: rewrote the manuscript-change block as Integrated (Restructuring definition now in Results §2.1; ED Fig. 2 caption already `\rev{}`-wrapped; Supp Fig. 29 now live) plus a small Pending line noting the optional threshold-sensitivity figure. Replaced the "we will add" promise that the R3-2 joint-axis sweep partially already serves. Status promoted to `Completed`.
    - R2-4: removed the `[PLACEHOLDER]` and "excess concordance" wording; replaced with "excess same-parent selection correlation" to match the integrated SI paragraph and Supp Fig. 28 caption. Added an explicit artifact-rule-out paragraph directly answering the reviewer's methodological concern. Status promoted to `Completed`.
    - R2-5: expanded from two sentences to four paragraphs (concession, what the data can establish, what it cannot, narrowed generality claim). Quoted the actual Discussion caveat at `sections/discussion.tex` $\sim$line 20 verbatim in blue. Noted that a paired pre/post-stabilisation 16S study would be needed for direct convergence quantification. Status promoted to `Completed`.
    - R2-6: added explicit section citations (Results §2.2, Supplementary Methods, Discussion $\sim$line 18 cross-reference) and trimmed the $\alpha_{ij}$-effective-coefficient elaboration that duplicated R2-1. Status promoted to `Completed`.
    - R2 minor: removed `[PLACEHOLDER --- confirm final styling]`; replaced vague prose with a 5-item itemised mapping, each line pointing to one concrete revision location (Fig. 2D caption; `supplementary_methods.tex` pH subsection; `supplementary_methods.tex` $\alpha_{ij}$ sentence; terminology unification pass; "generalisability" typo grep result). Status promoted to `Completed`.
  - `latex/main.pdf` (recompiled, 30 pages, clean).
  - `latex/supplementary.pdf` (recompiled, 38 pages, clean).
  - `latex/revision/response_letter.pdf` (recompiled, 48 pages, clean).

- **What changed**
  - Closed the three unfinished integrations flagged in `latex/revision/response/reviewer2_reflection_2026-04-22.md`: R2-3 (Restructuring definition + ED Fig. 2 caption + Supp Fig. 29), R2-4 (Supp Fig. 28 entered in `figures.tex` to resolve the dangling reference from the already-integrated SI paragraph at `supplementary_sections/pairwise_selection_correlation.tex:16`), and R2-minor (placeholder removed, mapping made verifiable).
  - Standardised terminology: response letter and SI now both use "excess same-parent selection correlation" (the term "excess concordance" is no longer used anywhere).
  - R2-2 now explicitly concedes Nutr+ environmental filtering and cross-references R1-2 evidence, per the reflection's "make the Nutr+ concession legible" recommendation.
  - R2-5 now states explicitly what the current data can and cannot establish about stabilisation-phase convergence, matching the reflection's recommended 4-paragraph arc.
  - Statusline promotions: R2-1, R2-3, R2-4, R2-5, R2-6, R2 minor all promoted from `Before review` to `Completed`. R2-2 demoted from `Before review` to `Blocked` with a clear blocker note, per Rule 1, because the promised Results §2.4 invasion-resistance clarifier is not yet in `sections/results.tex`.

- **Type**
  - Manuscript text edit (Results §2.1 Restructuring definition)
  - Supplementary figure import + `figures.tex` entries (Supp Figs. 28, 29)
  - Response letter text rewrite and status promotion
  - Response-letter / SI terminology standardisation ("excess same-parent selection correlation")
  - Workflow: Rule 1 status compliance (R2-2 demoted to `Blocked` because of a pending manuscript insert)

### Internal memo Q6 triage finalized and Q7 ``why gLV'' paragraph drafted

- **Affected reviewer points**: R2-1 (P1, $\alpha_{ij}$ interpretation), R2-6 (P1, mechanism vs phenomenology), R3-4 (P2, framework scope). Internal memo items Q6 (\S\ref{sec:q6_unexplained}) and Q7 (\S\ref{sec:q7_why_gLV}).

- **Files changed**
  - `latex/revision/internal_memo.tex` \S6 (Aspects of the data the gLV model does not explain): replaced the placeholder working-list with a completed 4-item triage table; each item classified by (i) whether an extension we ran captures it, (ii) limitation vs.\ refutation, (iii) impact on the central claim. Added a ``not on the list, by design'' subsection (PDI bimodality, pH$\Delta$--PDI slope asymmetry, LN OD dynamic range) and a rebuttal-framing takeaway pointing to a downstream Discussion ``honest scope'' paragraph.
  - `latex/revision/internal_memo.tex` \S7 (Why did we pick the gLV model?): replaced the placeholder sketch with a 3-sentence \texttt{\textbackslash rev\{\}}-ready draft paragraph, three placement options against the existing framing sentence at \texttt{results.tex}:42, and an explicit PI-gate block. Flipped \texttt{\textbackslash statusmark} from ``framing needed'' to ``draft complete; awaiting PI sign-off and placement decision.''
  - `latex/revision/internal_memo.tex` \S``Summary of pending deliverables'': Q6 flipped to ``Done'' with cross-reference; Q7 flipped to ``Drafted, awaiting PI sign-off.''

- **What changed**
  - **Q6 triage decision**: the four features the baseline gLV does not reproduce (negative $\Delta$OD--PDI sign in Base / Nutr$+$; Restructuring excess in natural communities; acidic-parent bias in Nutr$+$; pairwise CFU sub-additivity magnitude) are all classified as \emph{scope statements}, not refutations. Rationale: the central claim is made at the level of outcome-class frequency and within-community selection correlation; finer axes (winner direction, absolute biomass) are not targets of the claim. Item~2 is already partially addressed by the R3-4 cooperative extension; item~3 is addressed as a complementary predictor by the pH rule (\S3 of the memo); item~4 is supportive rather than contradictory. No new analysis owed.
  - **Q7 manuscript-facing draft**: three reasons for choosing gLV, condensed to one paragraph: (i)~single-scalar $\mu$ axis matching the nutrient-tunable experimental observable, (ii)~phenomenological parameters absorbing diverse mechanisms without committing to a biochemical source, (iii)~failed-invasion calibration compatibility that has no analogue in neutral models and needs mapping assumptions in consumer-resource models. Three placement options against the existing framing sentence in \texttt{results.tex} (replacement vs.\ insertion vs.\ split). Not inserted into \texttt{results.tex}; held behind a PI-approval gate per the memo's explicit ``confirm with PI before marking it as a manuscript edit'' note.
  - **Response-letter and manuscript impact**: none. These are internal-memo edits only. No \texttt{\textbackslash rev\{\}} wraps, no \texttt{reviewer\{1,2,3\}\_response.tex} edits, no figure imports.

- **Type**
  - Internal-memo scope finalization (Q6) and draft (Q7)
  - No new analysis
  - No manuscript edit (Q7 held at PI gate)
  - No response-letter edit
  - Compileability of \texttt{internal\_memo.tex} re-verified (next)

### Internal memo Q4 closed as superseded (geometric null on asymmetry coordinate)

- **Affected reviewer points**: R3-1 (P0), R3-2 (P0). Internal memo item Q4 (\S\ref{sec:q4_geometric_factor}).

- **Files changed**
  - `latex/revision/internal_memo.tex` \S4 (Simulation of the geometric / asymmetric factor): replaced the placeholder "implementation pending" plan with an explicit mapping table showing that each component of the Q4 plan is already delivered elsewhere in the rebuttal package. Removed the trailing `\todomark`. Flipped `\statusmark` from `Direction approved ("sounds good"); implementation pending.` to `Superseded by existing rebuttal coverage (see table below).`
  - `latex/revision/internal_memo.tex` \S"Summary of pending deliverables": Q4 bullet rewritten from a pending-analysis description to a closed/superseded entry pointing at R3-2.0a/b, R3-1 Option E, R3-3B, R3-3C / R1-4 / Extended Data Fig.~4, R3-2E, and Extended Data Fig.~3 / Supp.~Note 1.

- **What changed**
  - **Scope decision**: the Q4 proposal (per-event pure-geometric null preserving support sizes + one tunable unevenness parameter; per-medium $y$-CDF overlay with KS statistic) is not run as a new analysis. The rationale is that the same geometric/dimensionality concern is already tested on six independent axes in the package: (i) Response Fig.~R3-2.0a/b reproduces the reviewer's three toy null constructions at $N = 2, 4, 6, 8$ under both L$_2$ and L$_1$, parameterising unevenness via $U(0,1)$ vs $10^{U(-3,0)}$, on the same L$_2$/cosine pipeline the Q4 plan specified; (ii) R3-1 Option E runs a per-event richness-matched identity-permuted null (obs Dom $59.7\%$ vs null $12.3\%$); (iii) R3-3B is a per-$\mu$ composition-shuffling null preserving unevenness ($\sim 35\%$ vs observed $\sim 77\%$ at high $\mu$, Pearson $r = 0.695$, $p = 1.65 \times 10^{-4}$); (iv) R3-3C / R1-4 and Extended Data Fig.~4 directly vary initial richness and show Dominance is flat across pool sizes in experiment ($\chi^2 = 2.24$, $p = 0.69$) and simulation ($4$--$48$ species); (v) R3-2E applies richness-aware $y_{\mathrm{adj}}$/$x^2_{\mathrm{adj}}$ joint-axis tightening at the classifier level per medium; (vi) Extended Data Fig.~3 / Supp.~Note 1 are the abundance-based nulls already in the manuscript.
  - **Residual gap noted, not addressed**: there is no per-medium (Nutr$-$ / Base / Nutr$+$) experimental $y$-CDF against a pure-geometric null, because R3-2.0a is on synthetic $N$-series and Supp.~Note 1 is Base-only. Decision recorded in the memo: do not add one, because R3-2E (per-medium, joint-axis, classifier-level) + R3-3B (per-$\mu$ null-vs-observed gap) + R3-3C (pool-size ablation per medium) cover the per-medium concern on stronger ground than a $y$-CDF reformulation would.
  - **No manuscript or response-letter edits**: this change is confined to the working internal memo; no `\rev{}` marks, no `response/reviewer3_response.tex` edits, no new figure imports.

- **Type**
  - Internal-memo scope decision (Q4 closed)
  - No new analysis
  - No manuscript edit
  - No response-letter edit
  - Compileability of `internal_memo.tex` to be confirmed

---

## 2026-04-21

### R3-2 joint-axis diversity-adjusted threshold (Fig. R3-2E)

- **Affected reviewer point**: R3-2 (dimensionality artifact in similarity metrics; P0).

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/analyze_diversity_adjusted.py`: appended a joint-axis section after the single-axis (y-only) sweep. Sweep $(k_y, k_x)$ on a $5 \times 5$ grid over $\{0, 0.25, 0.5, 0.75, 1.0\}^2$; for each grid cell classify every event with $y_{\mathrm{adj}} = \min(1, 0.5 + k_y/\sqrt{N_{\mathrm{eff}}})$ AND $x^2_{\mathrm{adj}} = \min(1, 0.5 + k_x/\sqrt{N_{\mathrm{eff}}})$; compute overall + per-medium + class composition.
  - `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/Fig_R3_1_diversity_adjusted_joint.pdf` (new output): 6 panels (diagonal sweep line plot with y-only overlay; stacked class composition along the diagonal; pooled Dominance heatmap; per-medium Dominance heatmaps for LN/MN/HN).
  - `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/diversity_adjusted_joint.csv` (new output).
  - `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/memo.md` (appended "joint-axis sensitivity check" paragraph summarising the motivation and headline numbers).
  - `latex/revision/revision_figure_folder/Fig_R3_1_diversity_adjusted_joint.pdf` (copied).
  - `latex/revision/revision_figure_folder/source.md` (new provenance entry).
  - `latex/revision/response/reviewer3_response.tex`: added one paragraph + one `\begin{figure}` at the end of R3-2 (before R3-3 subsection), presenting the joint-axis result as `Response Fig. R3-2E`.
  - `latex/revision/response_letter.pdf` (recompiled, 41 pages).

- **What changed**
  - **Motivation**: y-only adjustment addresses R3's stated concern about Dominance inflation, but the reviewer's geometric argument in principle inflates BOTH the asymmetry ($y$) and retention ($x^2$) coordinates at low $N_{\mathrm{eff}}$ (low-dim positive vectors are more likely to look both asymmetric AND well-captured). The joint-axis sweep tests whether Dominance survives simultaneous tightening of both axes.
  - **Key numbers (diagonal $k_y = k_x = k$)**:
    - $k = 0$ (baseline): overall Dom 59.7% (LN 38.9% / MN 65.1% / HN 75.6%).
    - $k = 0.5$ (moderate joint): overall Dom 25.1%, Mix 30.0%, Rest 44.9% (LN 8.9% / MN 24.1% / HN 42.2%). HN/LN Dominance ratio 4.7x (widened from 1.94x).
    - $k = 0.75$ and above: over-corrected (Rest > 84%, Dom < 2%).
  - **Comparison with y-only at $k = 0.5$**: y-only keeps Restructuring at 19.0% (unchanged) and pushes events into Mixing; joint pushes some events further into Restructuring (Rest 44.9%). Dominance-level nutrient ordering preserved under both.
  - **Interpretation**: the Nutr+ Dominance signal is robust under moderate joint tightening (the exact regime where the geometric-inflation hypothesis would predict it to collapse first), which rules out both-axis dimensionality inflation as the cause.

- **Type**
  - New analysis (script extension)
  - Figure generation + import
  - Response letter edit (R3-2 extended by one paragraph + one figure)
  - Compileability confirmation

### R3-4 (facilitation) new evidence: pairwise CFU sub-additivity + non-competitive gLV extension

- **Affected reviewer point**: R3-4 in current numbering (P2, gLV excludes facilitation; was R3-3 in earlier drafts, the user still refers to it as "R3-3" in conversation).

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_3_pair_additivity/analyze_pair_additivity.py` (new; pairwise CFU sub-additivity + Relative Yield Total per medium from the 12-isolate pairwise invasion data at `Postprocessed/PairwiseColonyCountings_processed_230915.xlsx`).
  - `Figure_generate/code/Figure_revision/R3_3_pair_additivity/make_R3_3_figure.py` (new; assembles the 8-panel combined figure).
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_non_competitive.py` (new; gLV extension with exploitation and cooperation regimes; community-level row-sum stability screen + hard-reject of unstable matrices; writes `non_competitive_results.json`).
  - `Figure_generate/code/Figure_revision/R3_3_combined.pdf` (new; 2x4 layout: row A-D experiment sub-additivity, row E-H simulation robustness).
  - `latex/revision/revision_figure_folder/R3_3_combined.pdf` (imported).
  - `latex/revision/revision_figure_folder/source.md` (new provenance entry; reference label corrected to Response Fig. R3-4 to match current subsection numbering).
  - `latex/revision/response/reviewer3_response.tex` R3-4 subsection (rewritten, single flowing paragraph; embedded figure; status `Before review` / confidence 92\%).
  - `latex/revision/response_letter.pdf` (recompiled, 40 pages, clean).

- **What changed**
  - Added first part of the new evidence: experimental pairwise CFU shows 80/93/90\% sub-additive and 20/69/88\% RYT$<$1 for Nutr$-$/Base/Nutr$+$, escalating with nutrient concentration and supporting competition as the dominant pair-level interaction mode in our system.
  - Added second part: gLV extended with 15\% asymmetric (exploitative) or 15\% cooperative pairs at $\mu \in \{0.3, 0.6, 0.8\}$. Paper's main qualitative claims survive: Dominance rises with $\mu$ (comp 22/60/73, exploit 30/62/69, coop 47/80/78 percent), $|\phi|$ rises with $\mu$ in every regime. Cooperation raises Restructuring at weak interactions (10\% -> 25\% at $\mu = 0.30$), which matches the Restructuring excess in natural communities (main text Fig.~6C); exploitation shifts outcomes only marginally.
  - Stability caveat: coop15 at $\mu = 0.80$ yielded only 78 events after 954 rejections; flagged in both the caption and the source.md description.
  - Manuscript edits already in place are cross-referenced (Results \S2.6 summary, Results \S2.6 attribution sentence, Discussion mutualism caveat); no additional main-text edits were applied for this revision. Response-only deliverable per user instruction; ready to migrate into Supplementary Information if editor requests.

- **Type**
  - New analysis code (experiment + simulation)
  - New figure (Response Fig. R3-4)
  - Figure import into rebuttal package
  - Response text rewrite (previous paragraph replaced with evidence-forward single paragraph + figure)
  - Compileability confirmation

### R1 response-rule enforcement

- **Affected reviewer points**: R1-1, R1-2, R1-3, R1-4, R1-8, R1-9, R1-10.

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`

- **What changed**
  - Enforced the canonical response-letter workflow states by replacing invalid `After review` markers with valid statuses.
  - Promoted R1-1, R1-2, R1-3, and R1-4 to `Blocked` because each explicitly says the manuscript edit is still pending integration; added short blocker notes naming the pending section.
  - Tightened several responses to better match the prose/tone rules in `latex/revision/response/README.md`: removed defensive phrasing, reduced rhetorical emphasis, and kept responses closer to the reviewer’s actual question.
  - Removed bold callout sentences from R1-4 so the subsection complies with the “bold sparingly” rule.
  - Added an explicit manuscript-change closeout to R1-10 so every response ends with a manuscript-change statement or a no-change justification.

- **Type**
  - Response text cleanup
  - Workflow/status compliance fix
  - Style-rule enforcement

### R3-4 (refactor, manuscript \rev{} wrap, cross-linking)

- **Affected reviewer point**: R3-4 (P2, terminology).

- **Files changed**
  - `latex/sections/results.tex` (line 42, \S2.2): wrapped the disambiguation sentence ("Throughout the text, we use `interaction strength' as shorthand for this mean competition coefficient $\mu$\ldots") in `\rev{}` per Rule 2. The sentence was added for the rebuttal but had been inserted unmarked, which was a silent Rule 2 violation flagged during review.
  - `latex/revision/response/reviewer3_response.tex` (R3-4 subsection): rewrote the response in a single prose paragraph. Removed the "(1)\ldots(2)\ldots" inline numbered list (Rule 6 borderline). Broadened the defence to clarify that the failed-invasion proxy is outcome-level and mechanism-agnostic, rather than strictly competitive, resolving an internal inconsistency with R2-1 and R2-6. Added a direct answer to the reviewer's mutualism example: a genuinely mutualistic pair would register as \emph{weak} on the failed-invasion metric because the resident fails to exclude a partner that helps it; in the gLV model the mutualistic case is out of scope by construction ($\alpha_{ij} > 0$), a point cross-referenced to R3-3. Added cross-references to R2-1, R2-6, and R3-3. Noted in the response that the manuscript-integrated disambiguation is now `\rev{}`-marked.
  - `latex/revision/response_letter.pdf` (to be recompiled).
  - `latex/main.pdf` (to be recompiled).

- **What changed**
  - R3-4 response now conforms to all 11 style rules in `response/README.md` (verified, P2 cap of 1 paragraph now satisfied).
  - Reviewer's mutualism question is now directly answered rather than sidestepped.
  - Internal consistency across R2-1 / R2-6 / R3-3 / R3-4 established (all agree: interaction strength is outcome-level and mechanism-agnostic; gLV is a phenomenological framework restricted to competition by construction).
  - Rule 2 compliance for the disambiguation sentence restored.

- **Type**
  - Manuscript edit (`\rev{}` wrap, no new sentence)
  - Response text refactor (conciseness, directness, cross-linking)
  - Rule 2 compliance fix

### R3-1 diversity-adjusted thresholds + three new richness-aware nulls (Options E--H)

- **Files changed**
  - `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/analyze_diversity_adjusted.py` (new)
  - `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/{Fig_R3_1_diversity_adjusted_sweep.pdf, Fig_R3_1_per_medium_richness.pdf, memo.md, diversity_adjusted_{per_event,sweep}.csv}` (new outputs)
  - `Figure_generate/code/Figure_revision/R3_1_additional_nulls/analyze_additional_nulls.py` (new)
  - `Figure_generate/code/Figure_revision/R3_1_additional_nulls/{Fig_NullA_permutation.pdf, Fig_NullB_bootstrap.pdf, Fig_NullC_mixing_sweep.pdf, Fig_R3_1_all_nulls_summary.pdf, memo.md, summary_per_{medium,tertile}.csv, per_event_results.csv}` (new outputs)
  - `latex/revision/revision_figure_folder/` (copied six new PDFs: `Fig_R3_1_diversity_adjusted_sweep.pdf`, `Fig_R3_1_per_medium_richness.pdf`, `Fig_NullA_permutation.pdf`, `Fig_NullB_bootstrap.pdf`, `Fig_NullC_mixing_sweep.pdf`, `Fig_R3_1_all_nulls_summary.pdf`)
  - `latex/revision/revision_figure_folder/source.md` (six new provenance entries)
  - `latex/revision/response/reviewer3_response.tex` (R3-1 subsection extended with labelled Options E/F/G/H, all-null summary, bridge-to-R3-2 paragraph, and updated manuscript-change block; six new figures embedded)
  - `latex/revision/response_letter.pdf` (recompiled, 39 pages, bibtex clean)

- **What changed**
  - **Option E (richness-matched identity-permuted null).** Preserve $n_C$'s sorted rank-abundance vector, reassign species identities from $\mathrm{supp}(n_A \cup n_B)$ (500 draws / event). Observed Dominance 59.7\% vs Null 12.3\% overall; low-$N_{\mathrm{eff}}$ tertile 85.2\% obs vs 19.4\% null.
  - **Option F (richness-stratified bootstrap, conservative).** Resample $n_{C,\mathrm{null}}$ from other events' $n_C$ within the same $N_{\mathrm{eff}}$ quartile (within-medium / any-medium variants). Obs minus null (within-medium): +3 pp (LN), +26 pp (MN), +33 pp (HN).
  - **Option G (weighted mixing sweep $\alpha n_A + (1-\alpha)n_B$).** 11 $\alpha$ values. Dominance = 0\% at $\alpha = 0.5$ in every medium, rises monotonically to 100\% at endpoints. Also resolves the previously orphaned "mixing-ratio sweep" sentence in the prior R3-1 response.
  - **Option H (diversity-adjusted Dominance threshold).** $y_{\mathrm{adj}}(N_{\mathrm{eff}}) = 0.5 + k/\sqrt{N_{\mathrm{eff}}}$, sweep $k \in \{0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0\}$. At $k = 0.5$ overall Dominance drops to 35.7\% but nutrient ordering LN 8.9\% $<$ MN 44.6\% $<$ HN 54.4\% is preserved and widens. At $k \geq 1$ the classifier becomes over-corrected.
  - **All-null summary figure (Fig R3-1J)** compares per-medium Dominance across Observed, Additive, Null A, Null B (both variants), Null C @ 0.5, Null C any-$\alpha$.
  - Current R3-1 section is intentionally in "Options" form pending joint selection; `\statusline` kept as `Before review` until we pick the final subset, then will be promoted to `Blocked` with blocker note per Rule 11 (or `Completed` once integrated into `results.tex` §2.1).

- **Type**
  - New analysis code
  - Figure generation
  - Figure import into rebuttal package
  - Response letter extension (R3-1 expanded with four new options + summary)
  - Compileability confirmation

### R3-1 / R3-2 / R1-4 / R2-2 dimensionality-network consolidation

- **Affected reviewer points**: R3-1 (P0), R3-2 (P0), R1-4 (P2), R2-2 (P1). These were previously written as four independent responses but address overlapping null-model concerns; this edit explicitly links them as a four-axis rebuttal to the "passive explanations for Dominance" family.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
    - R3-1: added a new paragraph introducing the two additional, orthogonal nulls ($\mu$-level composition shuffling from R3-2; initial-richness ablation from R1-4). Added a new side-by-side imported figure (Response Fig. R3-1C + R3-1D) reusing `richness_mu_analysis.pdf` and `pool_size_analysis.pdf` at 0.42\textwidth each, captioned as reproduced from R3-2 and R1-4. Extended the blue Results §2.1 manuscript-change quote to mention the pool-size and composition-shuffling nulls as supplementary-figure references. Fixed an em-dash in the nutrient-transition sentence.
    - R3-2: replaced `\textbf{Experiments:}` / `\textbf{Simulations:}` bold paragraph-leads with prose (Rule 6). Replaced the em-dash in the excess-Dominance sentence (Rule 8). Added an opening pointer to R3-1 as the paired event-level null. Extended the composition-shuffling null definition (what is preserved vs randomized) and justified the "$\mu \geq 0.3$" cutoff as the ecologically active regime. Added a new imported figure (Response Fig. R3-2C, reproduced from R1-4, `pool_size_analysis.pdf` at 0.6\textwidth) as a direct initial-richness test. Strengthened the closing pairwise-selection-correlation paragraph as the artifact-free argument. Extended the Results §2.3 blue manuscript-change quote with a pool-size supplementary-figure reference.
  - `latex/revision/response/reviewer1_response.tex`
    - R1-4: added one sentence at the end of the mechanism paragraph pointing out that pool-size invariance is the cleanest direct test of the R3 dimensionality concern (cross-refs R3-1, R3-2).
  - `latex/revision/response/reviewer2_response.tex`
    - R2-2: added one sentence at the end of the simple-retention paragraph noting that the density and pool-size nulls are complementary to the R3 dimensionality nulls, giving four independent axes ruling out passive explanations.
  - `latex/revision/response_letter.pdf` (to be recompiled)

- **What changed**
  - R3-1 becomes the hub for the "dimensionality is ruled out" argument, now invoking per-event, per-$\mu$, and initial-richness nulls jointly rather than relying on a single case-by-case additive-null test.
  - R3-2 is tighter scientifically (definition of the null, cutoff justification) and now visibly pairs with R3-1 and R1-4 rather than reading as an isolated μ-level analysis.
  - R1-4 and R2-2 gain a single cross-reference sentence each so the reviewer sees the four-axis structure from multiple entry points.
  - No new figures imported into `revision_figure_folder/`: `richness_mu_analysis.pdf`, `pool_size_analysis.pdf`, `fig1_paired_classification.pdf`, and `fig6_asymmetricity_space.pdf` were already present. Primary figures remain at primary size in their home responses (R3-2, R1-4); small reuse happens at 0.42\textwidth (R3-1 panels C/D) and 0.6\textwidth (R3-2 panel C).
  - Rule 1 status unchanged: R3-1, R3-2, R1-4, R2-2 all remain `Before review` until the corresponding Results §2.1 / §2.2 / §2.3 / §2.4 manuscript inserts are applied.

- **Type**
  - Response text refactor and cross-linking
  - Figure reuse (no new imports)
  - Style cleanups (Rule 6, Rule 8) in R3-2

### Global / Infrastructure cleanup

- **Files changed**
  - Moved 14 stale Markdown files into `latex/revision/deprecated/2026-04-21_md_cleanup/`:
    - `v4/bibtex_verification_report.md`, `citation_review.md`, `grammer_review.md`, `supple_report.md`, `supple_report_paragraphwise.md`, `relevant_works.md`, `NatEcoEvo_submission_plan.md`, `PNAS_submission_plan.md`
    - `latex/supplementary_figure_review_report.md`, `latex/figure_caption_examples.md`
    - `latex/revision/response/reviewer1_response.md`, `reviewer2_response.md`, `reviewer3_response.md`
    - `latex/revision/converted/revision_summary.md`
  - `latex/revision/README.md` (removed stale references to the three `reviewer*_response.md` planning drafts; added a one-line pointer to the deprecated location)
  - `latex/main.pdf` and `latex/supplementary.pdf` (recompiled after Mansour2018 addition; 29 and 36 pages respectively, bibtex clean)

- **What changed**
  - One-off pre-revision QA reports (bibtex verification, citation review, grammar review, supple reports, suppl-fig review) are no longer current; the manuscript/bib have evolved since.
  - Pre-submission target plans (NatEcoEvo, PNAS) are no longer active given the paper is mid-revision.
  - Literature compilation (`relevant_works.md`) is superseded by `references.bib` plus in-text citations.
  - Figure caption style reference is superseded by the actually-applied caption style in `sections/*.tex`.
  - Markdown reviewer-response planning drafts are superseded by the LaTeX response package per the Rule 7 convention.
  - Auto-generated `converted/revision_summary.md` was regenerable from the revision-summary scripts, no need to version it.
  - main.tex and supplementary.tex recompiled to confirm Mansour2018 resolves via natbib + naturemag bibstyle (Rule 10).

- **Type**
  - Repository hygiene
  - Documentation update
  - Compileability confirmation

### R2-1 (refactor)

- **Files changed**
  - `latex/references.bib` (added `@article{Estrela2021}` entry after `Goldford2018`; Estrela, Sanchez-Gorostiaga, Vila, Sanchez, *eLife* 2021, e65948)
  - `latex/sections/results.tex` (§2.4 paragraph: broadened `\citep{Duan2025}` with `\rev{...\citep{Goldford2018, Estrela2021}}`; added a `\rev{}`-marked sentence defining interaction strength at the normalized-abundance / population level rather than per-capita)
  - `latex/sections/discussion.tex` (paragraph 4: broadened `\citep{Duan2025}` with `\rev{...\citep{Goldford2018, Estrela2021}}`; added a `\rev{}`-marked sentence explaining $\alpha_{ij}$ as an effective per-capita coefficient absorbing direct and indirect mechanisms, with gLV framed as deliberately coarse-grained)
  - `latex/revision/response/reviewer2_response.tex` (R2-1 subsection rewritten; confidence flipped to 100%)
  - `latex/revision/response_letter.pdf` (recompiled, 32 pages)
  - `latex/main.pdf` (recompiled, 29 pages)

- **What changed**
  - Restructured R2-1 response around the 4-step criteria: acknowledgment + (1) interaction strength defined on normalized abundance, not per-capita; (2) gLV + $\mu$ as deliberate phenomenological coarse-graining with $\alpha_{ij}$ absorbing multiple mechanisms; (3) explicit alignment with Duan 2025, Goldford 2018, Estrela 2021.
  - Fixed two Rule 1 violations in the prior response: it claimed `Goldford2018` and `Estrela2021` citations in the manuscript, but Goldford was not cited in Results §2.4 and `Estrela2021` did not exist in `references.bib`. `Estrela2021` entry now added and both citations integrated in Results §2.4 and Discussion.
  - All newly added manuscript text wrapped in `\rev{}` per Rule 2. (Pre-existing P1.11 text from 2026-04-14 remains unwrapped — out of scope for this edit; flag for a separate `\rev{}` sweep.)
  - Response letter uses plain-text citations (e.g., "Duan et al. (2025)") since `response_letter.tex` has no bibliography package; `\citet` breaks compilation.
  - Manuscript-changes block in the response now quotes verbatim-updated text with new clauses in italics to flag the revision.

- **Type**
  - Response text refactor
  - Manuscript edit (two new sentences + two new citations, all `\rev{}`-marked)
  - Bib addition (`Estrela2021`)
  - Rule 1 compliance fix

### R2-1 (prose pass + emphasis + supp-methods `\rev{}`)

- **Files changed**
  - `latex/revision/response/reviewer2_response.tex` (R2-1 rewritten into flowing prose; removed three bold-lead `(1)/(2)/(3)` blocks; added transition sentence connecting α_ij/μ notation to prior-work consistency; added `\emph{}` emphasis on four key claim phrases — thesis, rebuttal, generalization, closing)
  - `latex/supplementary_sections/supplementary_methods.tex` (wrapped the P1.11 α_ij interpretation sentence in `\rev{}` per Rule 2; this sentence is directly cited by the R2-1 response as a manuscript change)
  - `latex/revision/response_letter.pdf` (recompiled, 32 pages)
  - `latex/supplementary.pdf` (recompiled, 37 pages)

- **What changed**
  - Style: matched the R2-2 flowing-prose precedent by collapsing bold-lead scaffolding into three continuous paragraphs while preserving all three arguments (normalized-abundance definition → α_ij/μ as deliberate coarse-graining → literature alignment).
  - Added an explicit bridge sentence at the end of para 2 stating the α_ij/μ notation is consistent with how effective interaction coefficients are used in the broader microbial-ecology literature, which the reviewer themselves cites. Para 3 now opens "Building on this, the three works the reviewer highlights align directly…".
  - Selective `\emph{}` emphasis on short claim-phrases: "deliberately coarse-grained and operates at the outcome level"; "absorbed into the definition rather than acting as confounders"; "a feature that is correctly captured by our metric rather than a confounder of it"; "any perturbation that intensifies effective interspecific coupling … is predicted to shift the system toward the stronger-μ regime"; "direct operational evidence—independent of mechanistic attribution—that the effective competitive coupling intensifies across our gradient".
  - Rule 2 closure: wrapped the pre-existing P1.11 α_ij sentence in `supplementary_methods.tex` so the R2-1 manuscript-change claim is fully `\rev{}`-traceable. (Remaining P1.11 text throughout the manuscript is still unwrapped and will need a separate sweep.)

- **Type**
  - Style refactor (bold-lead → prose)
  - Emphasis layer (`\emph{}` on claim sentences)
  - Manuscript edit (P1.11 α_ij sentence now `\rev{}`-wrapped)
  - Rule 2 compliance fix

### Global blue-sweep (README Rule 10)

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex` (R1-11 "Corrected to …" manuscript quote wrapped in `\textcolor{blue}{}`)
  - `latex/revision/response/reviewer2_response.tex` (R2-1 three manuscript-change quotes converted from `\emph{}` to `\textcolor{blue}{}`; R2-3 three pending-integration quotes wrapped in `\textcolor{blue}{}`; R2-6 two integrated manuscript-text quotes wrapped in `\textcolor{blue}{}`; added a Supplementary-Methods manuscript-change line in the R2-1 block for traceability)
  - `latex/revision/response/reviewer3_response.tex` (R3-1 one manuscript-change quote, R3-2 two manuscript-change quotes, R3-3 three tone-down quotes, R3-4 one disambiguation quote all wrapped in `\textcolor{blue}{}`)
  - `latex/revision/response_letter.pdf` (recompiled, 32 pages)

- **What changed**
  - Applied `response/README.md` Rule 10 ("Highlight manuscript-bound text in blue") consistently across all three response files. Previously, R1 was mostly in compliance but R2 and R3 had manuscript-change quotes rendered as plain `` `` text or `\emph{}`, which is inconsistent with the README convention and confusing for the reader trying to spot what is a proposed manuscript edit vs running prose.
  - Scope: only text that will be inserted/substituted into the main manuscript or supplementary was wrapped. In-prose scare quotes (e.g., ``"strong interaction"``, ``"excess Dominance"``, ``"simple retention"``) were left alone since they are term introductions inside the response, not manuscript insertions.
  - `\reviewercomment{}` blocks were explicitly excluded — those are the reviewer's own text, not proposed manuscript content.

- **Type**
  - Styling pass (README Rule 10 compliance)
  - No new manuscript edits
  - No response-content changes (wrapping only)

## 2026-04-20 (late afternoon)

### R2-2 (refactor)

- **Files changed**
  - `latex/references.bib` (added `@article{Mansour2018}` entry, lines 170--179)
  - `latex/sections/discussion.tex` (inserted `\rev{\citep{Mansour2018}}` in the alternative-mechanisms paragraph, ~line 16)
  - `latex/revision/response/reviewer2_response.tex` (R2-2 subsection rewritten, lines 31--51)
  - `latex/revision/response_letter.pdf` (recompiled, 31 pages)

- **What changed**
  - Rewrote R2-2 response in flowing prose: removed `\begin{enumerate}` with four bold-lead items, removed both em-dashes, removed `[PLACEHOLDER]` supplementary-figure marker.
  - Aligned the three alternatives listed in the response (environmental filtering / neutral hitchhiking / shared trait correlations) with what is actually present in `discussion.tex`, rather than the earlier response-letter list (environmental filtering / correlated traits / assembly history / Nutr+ as environmental filtering), which did not match the manuscript.
  - Added a second paragraph testing two further "simple retention" proxies (absolute parental density and initial pool size) by reusing R1-1A and R1-4 analyses; neither reproduces the Dominance pattern, supporting the interaction-driven interpretation.
  - Embedded `Fig_R1_1A_winner_loser_OD.pdf` and `pool_size_analysis.pdf` side-by-side at `0.42\textwidth` each (no new figure import; both already in `revision_figure_folder/`).
  - Split manuscript-change block into two clearly-labelled parts: *integrated* (Discussion Mansour citation) and *pending integration* (Results §2.4 "invasion resistance" clarifier).
  - Added `Mansour2018` bib entry (Mansour, Heppell, Ryo, Rillig, *Biological Reviews* 2018) and wrapped the new citation in `\rev{}` in `discussion.tex` per `revision.rule.md` Rule 2.

- **Type**
  - Response text refactor
  - Manuscript edit (citation added, `\rev{}`-marked)
  - Bib addition
  - Figure reuse (no new import)

### R1-4 (refactor, v4)

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py` (PSC decomposed into same vs cross co-persistence rates; panels renumbered A-F)
  - `latex/revision/revision_figure_folder/pool_size_analysis.pdf` (regenerated, 2x3 fully filled A-F)
  - `latex/revision/revision_figure_folder/source.md` (R1-4 entry updated)
  - `latex/revision/response/reviewer1_response.tex` (R1-4 tightened to single paragraph, two bolded emphasis sentences)
  - `latex/revision/response_letter.pdf` (recompiled, 32 pages)

- **What changed**
  - Filled the previously empty top-right panel with the classic same-origin (solid) vs cross-origin (dashed) co-persistence rate (new panel C), the direct simulation analog of the paper's pairwise selection correlation.
  - Renumbered panels A-F in reading order: A/B experiment (richness, Dominance), C same/cross co-persistence, D within/between $\alpha$, E Dominance, F origin-persistence $|\phi|$.
  - Same/cross co-persistence confirms: indistinguishable at $\mu = 0.30$ (no community-level selection), diverge at $\mu = 0.60$, separate widely at $\mu = 0.80$ (same $\sim 0.4$, cross $\sim 0.1$ at pool=48). $|\phi|$ summarises this as a single scalar per event.
  - Response text shortened; two bolded emphasis sentences: (1) "Both views deliver the same message: the strength of community-level selection is set by $\mu$, not by pool size"; (2) "Our coalescence results generalise across pool sizes spanning an order of magnitude."

- **Type**
  - Analysis extension
  - Figure regeneration
  - Response text
  - Documentation

### R1-4 (refactor, v3)

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py` (added PSC computation and panel E)
  - `latex/revision/revision_figure_folder/pool_size_analysis.pdf` (regenerated, 2x3 with top-right empty)
  - `latex/revision/revision_figure_folder/source.md` (R1-4 entry updated)
  - `latex/revision/response/reviewer1_response.tex` (R1-4 text expanded with bolded emphasis sentences and panel E caption)

- **What changed**
  - Added a pairwise selection correlation metric to the simulation analysis: per coalescence event, $|\phi|$ (Pearson) between species origin label (parent A vs parent B) and persistence in the coalesced community. High $|\phi|$ means one parent's survivors preferentially persist together, i.e. community-level selection; low $|\phi|$ means origin-independent selection.
  - New panel E shows $|\phi|$ vs pool size at $\mu \in \{0.30, 0.60, 0.80\}$: $|\phi| \approx 0.24$ / $0.55$ / $0.70$ across pool sizes 4-48, essentially flat within each $\mu$.
  - Response text rewritten with two bolded/italic emphasis sentences: (1) "both Dominance frequency and pairwise selection correlation are set by $\mu$, not by pool size"; (2) "the experiment-model match is not contingent on the particular richness of our synthetic consortia: the mechanism generalises across pool sizes spanning an order of magnitude."

- **Type**
  - Analysis extension
  - Figure regeneration
  - Response text
  - Documentation

### R1-4 (refactor, v2)

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py` (second rewrite)
  - `latex/revision/revision_figure_folder/pool_size_analysis.pdf` (regenerated, 2x2 layout)
  - `latex/revision/revision_figure_folder/source.md` (R1-4 entry rewritten)
  - `latex/revision/response/reviewer1_response.tex` (R1-4 subsection rewritten)
  - `latex/revision/response_letter.pdf` (recompiled, 28 pages)

- **What changed**
  - Restructured R1-4 figure from 2x3 (6 panels) to 2x2 (4 panels):
    - Dropped experimental survival-ratio panel (realized-ASV/inoculum-species ratio exceeded 1, which is meaningless given 16S copy-number variation).
    - Dropped model realized-richness panel (redundant with the within/between alpha mechanism).
    - Removed n= count annotations that were coarse-grained across media and misleading.
  - Extended model analysis from a single $\mu=0.50$ to $\mu \in \{0.30, 0.60, 0.80\}$ to parallel the three experimental media (Nutr-, Base, Nutr+). Both the within/between alpha panel and the Dominance panel now show all three mu levels, making the experiment-model parallel direct.
  - Key numerical result: the within/between alpha gap grows with mu (0.03 / 0.17 / 0.32 at mu = 0.30 / 0.60 / 0.80) and is pool-size invariant at every mu; Dominance fraction is dominated by mu rather than pool size (0.13-0.25 / 0.55-0.65 / 0.68-0.79 across pool sizes 4-48).
  - Response text rewritten in flowing prose (per response/README.md P2 tier: 1 paragraph, no explicit (a)/(b) scaffolding, no em-dashes).

- **Type**
  - Analysis refactor
  - Figure regeneration
  - Response text
  - Documentation

### R1-4 (refactor, v1)

### R1-1 (refactor)

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_OD_density.py` (complete rewrite)
  - `latex/revision/revision_figure_folder/Fig_R1_1A_winner_loser_OD.pdf` (new)
  - `latex/revision/revision_figure_folder/Fig_R1_1B_OD_vs_PDI.pdf` (new)
  - `latex/revision/revision_figure_folder/Fig_R1_1C_pairwise_corr_vs_OD.pdf` (new)
  - `latex/revision/revision_figure_folder/Fig_R1_1a_dominance_vs_OD_diff.pdf` (removed)
  - `latex/revision/revision_figure_folder/Fig_R1_1b_winner_OD_rank.pdf` (removed)
  - `latex/revision/revision_figure_folder/Fig_R1_1c_dominance_by_medium_OD.pdf` (removed)
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/response/reviewer1_response.tex` (R1-1 subsection rewritten)
  - `latex/revision/response_letter.pdf` (recompiled, 26 pages)

- **What changed**
  - Refactored R1-1 analysis into three medium-stratified figures:
    - A: winner-OD vs loser-OD scatter per medium (directional test on Dominance events).
    - B: per-event signed $\Delta$OD vs PDI scatter per medium, with Spearman $\rho$.
    - C: same- and cross-origin pairwise selection correlation vs meanOD, both binned (tertile) and continuous (scatter).
  - Rewrote R1-1 response to report actual statistics (winner-denser 26.8% pooled, negative $\rho$ in Nutr$+$ $= -0.60$, no significant OD-driven same-parent correlation). Removed both `[PLACEHOLDER]` markers in R1-1. Manuscript integration still flagged as pending.

- **Type**
  - Analysis refactor
  - Figure import (new)
  - Figure removal (old)
  - Response text
  - Documentation

## 2026-04-20

### Global / Revision Infrastructure

- **Files changed**
  - `latex/revision/response_letter.tex`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/README.md`
  - `latex/revision/revision_figure_folder/*.pdf` (copied imports)

- **What changed**
  - Created a compileable LaTeX response-letter package.
  - Added reviewer-specific LaTeX response sections.
  - Created `revision_figure_folder/` as the local figure store for rebuttal figures.
  - Imported revision-analysis PDFs from `Figure_generate/code/Figure_revision/...`.
  - Added `source.md` documenting the provenance of imported response figures.
  - Rewrote the revision `README.md` to describe the LaTeX-centered rebuttal workflow and the role of `revision_figure_folder/`.

- **Type**
  - Response infrastructure
  - Figure import
  - Documentation

### R1-6, R1-8, R1-10, R1-11

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`

- **What changed**
  - Added submission-style LaTeX responses covering:
    - reflected gray points clarification
    - Fig. 2D caption clarification
    - confirmation that means are present in ED Fig. 5C
    - wrong Extended Data reference correction

- **Type**
  - Response text

### R1-1, R1-2, R1-3, R1-4, R1-7

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/revision_figure_folder/Fig_R1_1b_winner_OD_rank.pdf`
  - `latex/revision/revision_figure_folder/Fig_R1_2a_dominance_by_pH_pair.pdf`
  - `latex/revision/revision_figure_folder/Fig_R1_3ab_PDI_comparison.pdf`
  - `latex/revision/revision_figure_folder/pool_size_analysis.pdf`
  - `latex/revision/revision_figure_folder/interaction_matrix_assembly.pdf`

- **What changed**
  - Added reviewer-facing LaTeX responses for:
    - OD-based alternative explanation
    - pH mismatch analysis
    - dominant-species circularity check
    - pool-size analysis
    - interaction-matrix-after-assembly analysis
  - Embedded representative response figures into the rebuttal package.

- **Type**
  - Response text
  - Figure import

### R1-5, R1-9

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`

- **What changed**
  - Added response text for:
    - softened similarity-metric robustness claim
    - expanded “cohesion without cooperation” framing

- **Type**
  - Response text

### R2-1, R2-2, R2-5, R2-6

- **Files changed**
  - `latex/revision/response/reviewer2_response.tex`

- **What changed**
  - Added response text for:
    - nutrient-enrichment reframing
    - alternative explanations for community-level selection
    - natural-community pre-selection caveat
    - phenomenological framing of gLV

- **Type**
  - Response text

### R2-3, R2-4

- **Files changed**
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/revision_figure_folder/scatter_retention_vs_PDI.pdf`
  - `latex/revision/revision_figure_folder/bray_curtis_similarity.pdf`
  - `latex/revision/revision_figure_folder/invasion_fitness_analysis.pdf`

- **What changed**
  - Added response text and figures for:
    - continuous similarity measures alongside categories
    - invasion-fitness interpretation of pairwise selection correlation

- **Type**
  - Response text
  - Figure import

### R3-1, R3-2

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/fig1_paired_classification.pdf`
  - `latex/revision/revision_figure_folder/fig6_asymmetricity_space.pdf`
  - `latex/revision/revision_figure_folder/richness_by_medium.pdf`
  - `latex/revision/revision_figure_folder/richness_mu_analysis.pdf`

- **What changed**
  - Added response text and figures for:
    - case-by-case additive-null analysis
    - richness / dimensionality confound analyses in experiment and simulation

- **Type**
  - Response text
  - Figure import

### R3-3, R3-4

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Added response text for:
    - toned-down natural-community claims due to missing facilitation
    - clarification of “interaction strength” versus “competition strength”
  - 2026-04-21: Refactored R3-3 from bulleted `\begin{itemize}` list to single flowing paragraph per response README rule 6. Verified all three blue-highlighted manuscript quotes match the actual text in `sections/results.tex` line 120 and `sections/discussion.tex` line 22 verbatim. No manuscript edits needed (the three claimed edits were already applied previously).

- **Type**
  - Response text

### Global / Rebuttal Governance

- **Files changed**
  - `revision.rule.md`
  - `revision_history.md`
  - `latex/main.tex`
  - `latex/supplementary.tex`

- **What changed**
  - Created `revision.rule.md` to define strong rebuttal-stage working rules.
  - Created `revision_history.md` to track changes by reviewer question.
  - Added `\rev{}` macro to both the main and supplementary LaTeX entrypoints so future manuscript edits can be marked in red.

- **Type**
  - Workflow rule
  - Change log
  - LaTeX revision markup support

---

## 2026-04-21 — R1-5, R1-7, R1-9 manuscript integration

- **Affected reviewer points**: R1-5, R1-7, R1-9 (R1 style/minor tier, but each required a true manuscript edit).
- **Files changed**
  - `latex/sections/results.tex`
    - §2.1: appended `\rev{}` rationale clause explaining why Jensen--Shannon and Jaccard yield different orderings (presence/absence weighting vs abundance-weighted asymmetry). — R1-5.
    - §2.2: inserted `\rev{}` sentence pointing to the new post-assembly interaction matrix (Supp. Fig. 27). — R1-7.
  - `latex/sections/discussion.tex`
    - Added `\rev{}` counterintuitive-framing sentence after the "cohesion without cooperation" mechanism. — R1-9.
  - `latex/supplementary_sections/extended_data.tex`
    - ED Fig. 2 caption: replaced the overclaim "All metrics produce qualitatively similar outcome distributions, demonstrating that the prevalence of Dominance is robust to the choice of similarity metric" with a softened `\rev{}` version distinguishing abundance-weighted vs presence/absence metrics. — R1-5.
  - `latex/supplementary_sections/figures.tex`
    - Added new Supplementary Fig. 27 (post-assembly interaction matrix with block structure, Mann-Whitney U test result). — R1-7.
  - `latex/supplementary_figs/interaction_matrix_post_assembly.pdf`
    - Newly copied from `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/interaction_matrix_assembly.pdf`.
  - `latex/revision/revision_figure_folder/source.md`
    - New entry for `interaction_matrix_post_assembly.pdf` with manuscript destination noted.
  - `latex/revision/response/reviewer1_response.tex`
    - R1-5, R1-7, R1-9 promoted from `Blocked` to `Completed` with blocker notes removed and response text updated to match the now-integrated manuscript edits.
- **Type**
  - Manuscript text edit (main + supplementary)
  - Figure import into the manuscript figure tree
  - Response letter text + status promotion
  - Figure provenance (source.md)

---

## 2026-04-21 — R1-5, R1-8 fidelity pass + R1 status promotions

- **Affected reviewer points**: R1-5 (wording), R1-8 (caption + response), R1-6, R1-10, R1-11 (status bookkeeping).
- **Files changed**
  - `latex/sections/results.tex`
    - §2.1 (R1-5): sharpened the \rev{} clause from "somewhat different orderings" to "reversed orderings, with Dominance becoming the least frequent outcome, ..." to match the reviewer's own characterization.
    - Fig. 2 caption (R1-8): added \rev{} clauses explaining that only 50 stratified samples are displayed per group while the squares show the mean across all ~1,200 events — directly addressing why squares need not coincide visually with the displayed dots.
  - `latex/revision/response/reviewer1_response.tex`
    - R1-5 response: updated blue-quoted text to match the sharpened results.tex wording.
    - R1-8 response: rewrote to explicitly name the stratified-sampling source of the visual mismatch the reviewer complained about, and quote the new caption verbatim.
    - Status promotions: R1-6 → Completed (100%), R1-8 → Completed (100%), R1-10 → Completed (100%), R1-11 → Completed (100%).
- **Type**
  - Manuscript text edit (captions only)
  - Response letter text update (wording + verbatim alignment)
  - Workflow: status promotion
