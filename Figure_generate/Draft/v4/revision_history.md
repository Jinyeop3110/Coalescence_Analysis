# Revision History for `v4`

This log records rebuttal-stage changes made in `Figure_generate/Draft/v4`.

Entries are organized primarily by reviewer question, with a small infrastructure section for workflow changes that support the rebuttal package as a whole.

---

## 2026-06-16 — Pairwise selection-correlation metric moved to Supplementary Methods

- **Affected reviewer points**: R2 pairwise selection-correlation metric interpretation and Supplementary Note~2 organization (methodological definition vs. results split).
- **Files changed**
  - `latex/supplementary_sections/supplementary_methods.tex`
    - Added a new "Pairwise Selection Correlation Metric" subsection (before "Statistical Analyses") holding the affiliation-label rule, the $\rho = 2\times\text{shared-fate rate}-1$ definition, $\rho_{\text{same}}/\rho_{\text{cross}}$, the 1,000-permutation null, and $\Delta$.
    - De-duplicated the "Statistical Analyses" permutation-test bullet to cross-reference the new subsection instead of restating the null.
  - `latex/supplementary_sections/assembly_effect.tex`
    - Removed the metric-definition paragraphs from Note~2's "Pairwise selection correlation" subsection; replaced with a one-line pointer to Supplementary Methods so the subsection now opens with results.
    - The invasion-fitness conceptual bridge and the auxiliary gLV result (r = 0.870; Supplementary Fig.~36) remain in Note~2, preserving the claim in `reviewer2_response.tex` (Rule 1).
- **Type**
  - Supplementary Information organization
- **Verification**
  - Confirmed `reviewer2_response.tex` "added this conceptual bridge to Supplementary Note~2" remains true (bridge + Fig.~36 result not moved).
  - Confirmed no figure cross-references (Extended Data Figs.~5--6) moved with the relocated method text.

## 2026-06-16 — Supplementary Note 5 biological-alternatives reorganization

- **Affected reviewer points**: Supplementary Note~5 organization, R2 pH-feedback alternative, R3-3 geometric/null-model controls, and R3-4 model-scope controls.
- **Files changed**
  - `latex/supplementary_sections/alternative_models_controls.tex`
    - Renamed Note~5 to "Alternative biological explanations and controls for community-level selection."
    - Merged the pH-feedback model and strict pH-contrast sections under "pH-mediated environmental modification."
    - Removed the additive/geometric null and model-scope summary subsections from Note~5.
  - `latex/supplementary_sections/skewness_null_model.tex`
    - Added "Geometric and parental-norm effects" to Note~1 so additive/geometric null controls sit with metric/null-model controls.
  - `latex/supplementary_sections/simulations.tex`
    - Clarified in Note~3 that the simulation sensitivity analyses define the scope of the effective-interaction framework.
  - `latex/revision/response/reviewer1_response.tex` and `latex/revision/response/reviewer3_response.tex`
    - Updated cross-references to the renamed Note~5 and moved geometric/null-model control.
- **Type**
  - Supplementary Information organization
- **Verification**
  - Checked active, staging, and word-conversion sources for stale Note~5 subsection headings and old cross-references.

## 2026-06-16 — Dominant-taxon PDI control moved to Note 1

- **Affected reviewer points**: R1-3 PDI circularity control and Supplementary Note organization.
- **Files changed**
  - `latex/supplementary_sections/skewness_null_model.tex`
    - Added the dominant-taxon removal control after the PDI definition and boundary-sensitivity discussion, where metric-related controls are defined.
  - `latex/supplementary_sections/alternative_models_controls.tex`
    - Removed the dominant-species circularity subsection from Supplementary Note~5 so Note~5 focuses more on biological alternative explanations.
  - `latex/revision/response/reviewer2_response.tex`
    - Updated the organizational cross-reference to state that controls are distributed across Supplementary Notes~1, 3, and 5.
- **Type**
  - Supplementary Information organization
- **Verification**
  - Checked active and staging sources for the moved subsection and stale Note~5 consolidation wording.

## 2026-06-16 — Unequal-biomass wording cleanup

- **Affected reviewer points**: R1-1 biomass/OD alternative explanation and Supplementary Note~5.
- **Files changed**
  - `latex/supplementary_sections/alternative_models_controls.tex`
    - Renamed the subsection to "Unequal parental biomass at mixing."
    - Clarified the alternative mechanism as passive effects of unequal parental biomass at mixing.
  - `latex/supplementary_sections/supplementary_methods.tex`, `latex/supplementary_sections/tables.tex`, and `latex/supplementary_figs/file_source.md`
    - Replaced unclear loading terminology with parental OD/biomass imbalance language.
- **Type**
  - Terminology clarity
- **Verification**
  - Ran targeted source checks for stale non-archive loading terminology.

## 2026-06-16 — PDI arctangent notation cleanup

- **Affected reviewer points**: Supplementary Note~1, Supplementary Figs.~10--12, and R1-1B notation.
- **Files changed**
  - `latex/supplementary_sections/skewness_null_model.tex`
    - Replaced the PDI definition with the ratio-based one-argument arctangent form, `PDI = (2/pi) arctan(u/v)`, and stated the `v=0`, `u>0` boundary value directly.
    - Corrected the PDI 0.25/0.75 threshold explanation from an approximate 3:1 ratio to an approximate 2.4:1 ratio.
  - `latex/supplementary_sections/figures.tex`, `latex/revision/response/reviewer1_response.tex`, and `latex/revision/revision_figure_folder/source.md`
    - Updated PDI captions and provenance text to use the same ratio-based arctangent notation and boundary convention.
- **Type**
  - Mathematical notation consistency
- **Verification**
  - Ran targeted source checks for stale two-argument arctangent wording in active LaTeX and provenance text.

## 2026-06-16 — Supplementary-response figure caption alignment

- **Affected reviewer points**: R1-1, R1-4, R2-2, R2-3, and R3-4 response-to-Supplementary Information traceability.
- **Files changed**
  - `latex/supplementary_sections/skewness_null_model.tex`
    - Added an explicit boundary convention for the PDI arctangent definition.
  - `latex/supplementary_sections/figures.tex`
    - Aligned the Supplementary Fig.~13 and 15 captions with the response-letter selection-correlation terminology.
    - Added the descriptive-analysis note to Supplementary Fig.~37 to match the response caption.
    - Clarified in Supplementary Figs.~10--12 that the PDI formula uses the arctangent definition from Supplementary Note~1.
    - Aligned active source comments with the current Supplementary Fig.~1--46 numbering after the reviewer-agent audit found stale navigation comments.
  - `latex/revision/response/reviewer1_response.tex`
    - Clarified the R1-1B PDI formula and boundary convention.
    - Aligned the R1-4 caption terminology with Supplementary Fig.~13.
  - `../../code/Figure_revision/R1_1_OD_density/analyze_OD_density.py` and `../../code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
    - Updated the visible PDI axis labels in regenerated response/supplementary figure assets to match the manuscript definition.
    - Updated the R1-1 OD-vs-PDI script calculation to match the manuscript definition.
  - `latex/revision/revision_figure_folder/Fig_R1_1B_OD_vs_PDI.pdf`, `latex/supplementary_figs/Fig_R1_1B_OD_vs_PDI.pdf`, `latex/revision/revision_figure_folder/marginal_distributions_by_medium.pdf`, and the medium-specific `latex/supplementary_figs/marginal_distributions_*_only.pdf` files
    - Replaced the affected figure PDFs with regenerated versions carrying the corrected PDI label.
  - `latex/revision/response/reviewer2_response.tex`
    - Added Supplementary Fig.~43 traceability for the pH-feedback model and aligned the feedback-range wording with the Supplementary Fig.~43 caption.
    - Clarified that Response Fig.~R2-3a was split into Supplementary Figs.~10--12 by medium.
  - `latex/revision/revision_figure_folder/source.md`
    - Updated figure-source provenance for the affected PDI figures.
    - Corrected stale R2-3/R1-4 provenance destinations and terminology after the reviewer-agent audit.
  - `latex/sections/results.tex` and `latex/revision/response/reviewer3_response.tex`
    - Added Supplementary Fig.~40 to the model-extension citation and specified reciprocal pair-coupling structure.
- **Type**
  - Supplementary/response caption consistency
  - Cross-reference traceability
- **Verification**
  - Ran targeted source checks for the stale caption/reference phrases.
  - Regenerated the affected response/supplementary figure PDFs and checked extracted PDF text for corrected PDI labels.
  - Rebuilt the main manuscript, Supplementary Information, and response letter.
  - Ran an independent reviewer-agent audit against concrete consistency criteria after the edits.

## 2026-06-15 — pH/top-down Results and R1-2 response punctuation aligned

- **Affected reviewer points**: R1-2 pH mismatch and Results \S2.5 readability.
- **Files changed**
  - `latex/sections/results.tex`
    - Replaced semicolon-linked clauses in the pH/top-down Results paragraph with sentence breaks while preserving the same pH-contrast statistics and interpretation.
  - `latex/revision/response/reviewer1_response.tex`
    - Updated the R1-2 response prose, manuscript-change quote, and response-figure caption to match the revised Results wording and avoid semicolon-linked clauses in the touched text.
- **Type**
  - Manuscript readability edit
  - Response-letter quote alignment
- **Verification**
  - Rebuilt the main manuscript with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
  - Rebuilt the response letter with `latexmk -pdf -interaction=nonstopmode -halt-on-error response_letter.tex`.
  - Checked the touched Results paragraph and R1-2 response section for remaining semicolons.

## 2026-06-15 — Main-figure caption label duplication fixed

- **Affected reviewer points**: Formatting/readability of the main manuscript PDF.
- **Files changed**
  - `latex/main.tex`
    - Suppressed the automatic LaTeX `Figure N:` caption label for main figures because the caption text already carries the journal-style `Fig.~N.` label.
- **Type**
  - Manuscript formatting fix
- **Verification**
  - Rebuilt the main manuscript with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
  - Checked the compiled PDF text to confirm `Figure N: Fig. N.` no longer appears.

## 2026-06-15 — Main-text coefficient-distribution robustness pointer added

- **Affected reviewer points**: R3-4 / model-scope robustness.
- **Files changed**
  - `latex/sections/results.tex`
    - Added one Results sentence pointing to Supplementary Fig.~42, stating that analysis separating the mean and variance of the interaction-coefficient distribution showed that both average inhibitory effect and coefficient heterogeneity contribute to the Dominance regime.
  - `latex/supplementary_sections/simulations.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`
  - `latex/supplementary_sections/alternative_models_controls.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/supplementary_figs/supple_fig_index.md`
  - `latex/supplementary_figs/file_source.md`
    - Replaced the informal phrase "mean-vs-variance" with wording describing analysis that separates the mean and variance of the interaction-coefficient distribution.
    - Made the R3-4 response explicit that coefficient variance is part of the effective interaction-strength axis, so adding mutualistic or facilitative coefficients can increase interaction strength when it broadens the interaction-coefficient distribution.
    - Reordered the R3-4 mutualism response so the coefficient-variance point opens the answer, followed by the weak-mutualistic-pair simulation test and then the general interaction-strength definition.
    - Tightened the opening R3-4 mutualism sentence to avoid an undefined antecedent and to specify "increasing the fraction or magnitude" of mutualistic/facilitative coefficients rather than implying that the number of matrix entries changes.
- **Type**
  - Main-text Results edit
  - Response-manuscript traceability
- **Verification**
  - Rebuilt the main manuscript with `latexmk -pdf -interaction=nonstopmode main.tex`.
  - Rebuilt the Supplementary Information with `latexmk -pdf -interaction=nonstopmode supplementary.tex`.
  - Rebuilt the response letter with `latexmk -pdf -interaction=nonstopmode response_letter.tex`.

## 2026-06-15 — R2-1 nutrient-availability preprint citation added

- **Affected reviewer points**: R2-1.
- **Files changed**
  - `latex/references.bib`
    - Added `DalBello2026`, the bioRxiv preprint "Nutrient Availability Shapes the Diversity and Structure of Microbial Communities" (DOI `10.64898/2026.04.14.718562`).
  - `latex/revision/response/reviewer2_response.tex`
    - Added `DalBello2026` to the R2-1 framing paragraph supporting the point that nutrient availability can reshape microbial community diversity and structure, not merely scale pairwise interaction coefficients.
    - Converted the existing plain-text citation list in that sentence to real natbib citations so the response bibliography resolves the added preprint.
- **Type**
  - Response-letter citation update
  - Bibliography update
- **Verification**
  - Crossref metadata verified the title, authors, bioRxiv posting date, and DOI before insertion.

---

## 2026-06-15 — R3-4 beneficial-interaction robustness added to Results

- **Affected reviewer points**: R3-4.
- **Files changed**
  - `latex/sections/results.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `revision_history.md`
- **What changed**
  - Replaced the broad Fig.~3 robustness sentence with a compact statement covering growth-rate variation, carrying-capacity variation, interaction-coefficient distributions, parental-community species richness, and model extensions allowing beneficial interactions.
  - Removed "similarity metrics" from that simulation-robustness list because the corresponding evidence is the Base-medium metric-sensitivity analysis in Extended Data Fig.~2, not part of the Fig.~3 simulation robustness package.
  - Folded the beneficial-interaction extensions into the same main-text robustness sentence, with pointers to Supplementary Figs.~39 and 41.
  - Updated the R3-4 response to quote this new Results text before the existing Supplementary Methods and Discussion scope quotes.
- **Type**
  - Main-text Results edit
  - Response-letter quote alignment
- **Verification**
  - Ran targeted text checks for the revised robustness sentence and stale "similarity metrics" wording in the Fig.~3 Results paragraph.

---

## 2026-06-15 — Supplementary Information navigation and provenance alignment

- **Affected reviewer points**: Cross-cutting SI readability and response traceability, especially R1-1 parental OD/biomass imbalance, R1-4 pool size, R2 natural-community caveats, and R3 null/robustness controls.
- **Files changed**
  - `latex/supplementary.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`
  - `latex/supplementary_sections/alternative_models_controls.tex`
  - `latex/sections/results.tex`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/supplementary_figs/file_source.md`
  - `revision_history.md`
- **What changed**
  - Added a concise Supplementary Information navigation roadmap after the note-order paragraph.
  - Corrected monoculture phenotype cross-references from Supplementary Fig.~34 to Supplementary Fig.~33 in the Supplementary Methods.
  - Added local subheadings to Supplementary Note~5 so parental OD/biomass imbalance, pool-size controls, pH alternatives, dominant-species circularity, additive/geometric null effects, and model-scope controls are easier to scan.
  - Aligned the Results biomass-control citation and matching R1-1 response quote to include Supplementary Fig.~45.
  - Synchronized `file_source.md` with active SI numbering and terminology for the targeted Supplementary Figures and Extended Data figure provenance entries.
- **Type**
  - SI navigation edit
  - Manuscript and response cross-reference alignment
  - Figure provenance documentation cleanup
- **Verification**
  - Ran targeted text checks for stale figure numbers and terminology in active SI/provenance files.
  - Rebuilt the supplementary information and response letter PDFs with `latexmk`.

## 2026-06-15 — R1-5 metric-sensitivity wording made explicit

- **Affected reviewer points**: R1-5, with related R2 minor metric-divergence comment.
- **Files changed**
  - `latex/sections/results.tex`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `revision_history.md`
- **What changed**
  - Replaced the main Results metric sentence with explicit mixed-result wording: abundance-weighted compositional metrics recover Dominance as the most frequent outcome, whereas Jaccard index and Jensen--Shannon divergence do not.
  - Refined the main-text explanation of the divergent metrics to state that Jaccard index emphasizes species-identity retention and Jensen--Shannon divergence emphasizes full-distribution divergence.
  - Updated the R1-5 and R2 metric-divergence response quotes to match the active Results sentence.
  - Tightened the R2 response prose from "relative-abundance metrics" to "abundance-weighted parental-similarity metrics" for consistency with the manuscript and Extended Data Fig.~2 caption.
- **Type**
  - Manuscript wording edit
  - Response-letter quote alignment
- **Verification**
  - Ran targeted text checks for stale broad robustness wording in active manuscript and response files.

---

## 2026-06-15 — Response quote citation alignment

- **Affected reviewer points**: R1-2, R2-1, R2-2, R2-4/R2-6, R3-4.
- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `revision_history.md`
- **What changed**
  - Added citations omitted from response-letter `\mschange{}` quotes where the corresponding manuscript text carries citations: Ratzke 2018/2020 for pH modification, Hu 2022/2025 and Ratzke 2018/2020 for nutrient-mediated interactions, Mansour 2018/Rillig 2015 for the operational community-level-selection framing, and Hu 2022/2025 for the gLV interaction-coefficient range statement.
- **Type**
  - Response-letter quote alignment
- **Verification**
  - Rebuilt `latex/revision/response_letter.pdf` with `latexmk -pdf -interaction=nonstopmode -halt-on-error response_letter.tex`.
  - Checked `response_letter.log` for fatal errors, undefined control sequences, and unresolved citation warnings.
  - Confirmed extracted PDF text renders the added citation numbers and reference entries.

---

## 2026-06-14 — R1-9 Lotka--Volterra citation wording tightened

- **Affected reviewer points**: R1-9.
- **Files changed**
  - `latex/sections/discussion.tex`
    - Changed "classical Lotka--Volterra theory" to "random Lotka--Volterra theory" in the cohesion-without-cooperation paragraph to better match the May 1972 and Grilli et al. 2017 citations.
  - `latex/revision/response/reviewer1_response.tex`
    - Updated the R1-9 response prose and quoted manuscript-change block to match the Discussion wording.
- **Type**
  - Manuscript wording edit
  - Response-letter quote alignment

---

## 2026-06-13 — R1-6 redundant response sentence removed

- **Affected reviewer points**: R1-6.
- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`
    - Removed the redundant closing sentence "We revised the captions of Figs. 1E, 4C, 5C, and 6B as quoted above." because the preceding sentence already states the caption change and quotes the inserted text.
- **Type**
  - Response letter wording polish

---

## 2026-06-13

### R1-1 response-caption wording cleanup

- **Affected reviewer points**: R1-1.

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`
  - `revision_history.md`

- **Source/reason**
  - Local caption wording cleanup requested for Response Fig.~R1-1A.

- **What changed**
  - Shortened the Response Fig.~R1-1A bold caption lead from "Higher parental-community OD does not preferentially predict the winner in Dominance events" to "Higher parental-community OD does not predict the winner in Dominance events."

- **Type**
  - Response-caption wording cleanup

- **Verification**
  - Ran targeted text checks for the old Response Fig.~R1-1A caption wording in active response files.

### R1-1 biomass-control wording strengthened

- **Affected reviewer points**: R1-1, with main-text relevance to R2-1/R2-2 nutrient interpretation.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/revision/response_letter.tex`
  - `latex/revision/response/reviewer1_response.tex`
  - `revision_history.md`

- **Source/reason**
  - Local wording review of the Results sentence citing Supplementary Note~5 and Supplementary Figs.~13--15.

- **What changed**
  - Removed "fully" from the Results statement, changing "did not fully account for" to "did not account for."
  - Added a minimal biomass-control clause stating that Dominance outcomes were not biased toward the higher-biomass parental community.
  - Updated the Reviewer 1 response prose and quoted manuscript-change sentence to match the revised Results wording.
  - Aligned the R1-9 response quote with the active Discussion wording and added the manuscript citations for Tikhonov, May, and Grilli.
  - Added `natbib` and the shared bibliography to `response_letter.tex` so those response-letter citations compile.

- **Type**
  - Manuscript wording edit
  - Response-letter quote alignment
  - Response-letter bibliography support

- **Verification**
  - Rebuilt `latex/main.pdf` with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
  - Rebuilt `latex/revision/response_letter.pdf` with `latexmk -pdf -interaction=nonstopmode -halt-on-error response_letter.tex`.
  - Checked logs for fatal errors, undefined control sequences, and unresolved citations.

---

## 2026-06-03

### R2-5 natural-community caveat folded into Results paragraph

- **Affected reviewer points**: R2-5, with related R3 natural-community tone-down wording.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `revision_history.md`

- **Source/reason**
  - Main-text flow review of Results \S2.6. The laboratory pre-selection caveat was accurate but did not need to stand as a separate paragraph.

- **What changed**
  - Folded the pre-selection caveat into the preceding natural-community Results paragraph, immediately after the sentence noting higher Restructuring fractions.
  - Kept the final "Overall" sentence as the paragraph-level conclusion.
  - Updated R2-5 and R3 response-letter `\mschange{}` quotes to match the integrated manuscript wording and removed the response claim that the caveat was added as a separate paragraph.

- **Type**
  - Manuscript paragraph-flow edit
  - Response-letter quote alignment

### R1-1/R1-4 control-language tone-down

- **Affected reviewer points**: R1-1, R1-4, with main-text relevance to R2-1/R2-2 nutrient interpretation.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/alternative_models_controls.tex`
  - `latex/revision/response/reviewer1_response.tex`
  - `revision_history.md`

- **Source/reason**
  - Main-text review of the Results \S2.4 sentence citing Supplementary Note~5 and Supplementary Figs.~13--15. The prior wording, "did not account for," sounded too absolute given that biomass, richness, and pool size can still modulate outcomes.

- **What changed**
  - Toned down the main Results sentence to state that parental-community biomass heterogeneity and initial richness effects "did not fully account for" the nutrient-dependent Dominance and correlated-fate trends.
  - Matched Supplementary Note~5 phrasing by changing biomass and pool-size conclusions from "do not explain" to "do not fully explain."
  - Updated the corresponding Reviewer 1 response prose and manuscript quote to match the revised Results wording.

- **Type**
  - Manuscript wording tone-down
  - Supplementary wording tone-down
  - Response-letter quote alignment

### R2-3 continuous-measures pointer moved out of main Results

- **Affected reviewer points**: R2-3.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/skewness_null_model.tex`
  - `revision_history.md`

- **Source/reason**
  - Main-text review of the R2-3 continuous-similarity insertion. The Results sentence pointing readers to the Base-medium PDI/asymmetry/retention distributions was judged too much like supplementary bookkeeping for the main text.

- **What changed**
  - Removed the full Supplementary Fig.~3 continuous-measures pointer from Results \S2.1, so the paragraph now moves directly from the Base-medium outcome counts to the metric-robustness and null-model controls.
  - Folded the same information into Supplementary Note~1, next to the existing paragraph on classification thresholds, continuous PDI/retention distributions, and boundary sensitivity.
  - Kept the moved text `\rev{}`-marked in the Supplementary Information.

- **Type**
  - Manuscript text trim
  - Supplementary text relocation

- **Verification**
  - Checked the edited Results and Supplementary Note~1 paragraphs for local flow.

## 2026-06-02

### R3-4 facilitative-tail caption and pair-coupling provenance cleanup

- **Affected reviewer points**: R3-4.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/supplementary_sections/figures.tex`
  - `../code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_p_axis.py`
  - `revision_history.md`

- **Source/reason**
  - Follow-up review of the R3-4 response package after moving from R3-2/R3-3 to the facilitation and mutualism comments.

- **What changed**
  - Removed the standalone Response Fig.~R3-4d fine pair-coupling panel from the response letter to shorten R3-4; the fine sweep remains cited as Supplementary Fig.~40.
  - Renumbered the weak mutualistic-pair response figure to R3-4d and the mean-vs-variance response figure to R3-4e.
  - Updated response-figure provenance to reflect the shortened R3-4 figure sequence.
  - Tightened R3-4 wording after a logic/style pass: "major source of interaction" became "dominant interaction mode"; reciprocal "sign/correlation" became "reciprocal pair-coupling"; the pair-coupling claim was softened from "does not affect" to "does not overturn"; and the mutualism answer now distinguishes coefficient magnitude/spread from the empirical invasion-resistance readout.
  - Corrected Supplementary Fig.~39 caption from 28.6\% to 22.2\% for the maximum expected facilitative fraction under $\alpha_{ij}\sim U[-f\mu,(2+f)\mu]$ with $f=0.8$.
  - Updated the `simulate_p_axis.py` header to match the current reciprocal pair-coupling sampler: iid competitive baseline at $p=0$, antisymmetric exploitation for $p<0$, and symmetric competition for $p>0$.

- **Type**
  - Supplementary figure caption correction
  - Analysis-code provenance/comment cleanup

- **Verification**
  - Checked R3-4 response summary values against JSON outputs for the mixed-sign facilitative-tail, weak mutualistic-pair, mean-vs-variance, and pair-coupling sweeps.
  - Compiled `latex/revision/response_letter.tex` successfully with `latexmk -pdf -interaction=nonstopmode`.
  - Compiled `latex/supplementary.tex` successfully with `latexmk -g -pdf -interaction=nonstopmode`.
  - Ran targeted scans confirming the stale 28.6\% value and old signed-marginal pair-coupling wording are absent from active R3-4 files.

### R3 reviewer-style geometric null terminology standardized

- **Affected reviewer points**: R3-2 and R3-3.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/skewness_null_model.tex`
  - `latex/supplementary_sections/alternative_models_controls.tex`
  - `latex/supplementary_sections/extended_data.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/supplementary_figs/file_source.md`
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L1.pdf`
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L1.png`
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L2.pdf`
  - `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L2.png`
  - `../code/Figure_revision/R3_2_reviewer_norm_comparison/reproduce_reviewer_norm_figures.py`
  - `../code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_reviewer_reproduction_L1.pdf`
  - `../code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_reviewer_reproduction_L1.png`
  - `../code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_reviewer_reproduction_L2.pdf`
  - `../code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_reviewer_reproduction_L2.png`
  - `revision_history.md`

- **Source/reason**
  - Response-tailoring terminology cleanup requested after reviewing the R3 toy/geometric null-model wording.
  - The prior response used several overlapping labels for the reviewer-inspired geometric examples and the real-data additive-null control.

- **Justification under minimal-change rule**
  - The edit is a local terminology normalization tied directly to Reviewer 3's geometric-null critique.
  - No analysis logic, statistics, classifier thresholds, or scientific claims were changed.

- **What changed**
  - Standardized the umbrella term to "reviewer-style geometric null constructions."
  - Standardized the two construction families to "random-restructuring null model" and "simple additive null model."
  - Reserved "event-matched simple additive null model" for the real-data null in which each null coalesced community is constructed from the same two parental communities as the observed event.
  - Updated the R3 response prose, Response Fig.~R3-2.0 caption, main Results, Supplementary Note~1, Extended Data Fig.~3 caption, Supplementary Fig.~38-related wording, figure provenance, and supplementary figure provenance.
  - Regenerated the Reviewer 3 L1/L2 reproduction figures so their visible row subtitles match the standardized terminology, then copied the regenerated assets into `latex/revision/revision_figure_folder/`.

- **Type**
  - Response text
  - Main manuscript text
  - Supplementary text/caption
  - Figure/provenance
  - Analysis/figure-generation label update

- **Verification**
  - Ran `python reproduce_reviewer_norm_figures.py` from `../code/Figure_revision/R3_2_reviewer_norm_comparison/`; the script verified the L2 implementation against raw cosine coordinates for 1600 events with max coordinate difference `3.49e-14` and zero class disagreements.
  - Verified regenerated source and copied response PDFs are byte-identical by checksum.
  - Visually inspected `latex/revision/revision_figure_folder/Fig_R3_2_reviewer_reproduction_L2.png` and confirmed row subtitles use "random-restructuring null model" and "simple additive null model."
  - Compiled `latex/revision/response_letter.tex`, `latex/main.tex`, and `latex/supplementary.tex` successfully with `latexmk -pdf -interaction=nonstopmode`.
  - Ran targeted text checks for stale terminology, workflow triage markers, and Unicode punctuation in affected files.

- **Remaining risk or follow-up**
  - The compile logs retain pre-existing minor overfull-box warnings; none are caused by the terminology change.
  - Reviewer-quoted text was intentionally left unchanged.

## 2026-05-29

### R1-8 same-style pairwise-correlation figure preview workspace

- **Affected reviewer points**: R1-8, with relevance to R2 minor figure-clarity feedback.

- **Files changed**
  - `latex/revision/revision_for_figure/README.md`
  - `latex/revision/revision_for_figure/make_pairwise_correlation_same_style.py`
  - `latex/revision/revision_for_figure/Fig2D/simulation_pairwise_correlation_same_style.pdf`
  - `latex/revision/revision_for_figure/Fig2D/simulation_pairwise_correlation_same_style.png`
  - `latex/revision/revision_for_figure/Fig2D/experiment_pairwise_correlation_same_style.pdf`
  - `latex/revision/revision_for_figure/Fig2D/experiment_pairwise_correlation_same_style.png`
  - `latex/revision/revision_for_figure/pairwise_correlation_simulation_all_same_style.pdf`
  - `latex/revision/revision_for_figure/pairwise_correlation_simulation_all_same_style.png`
  - `latex/revision/revision_for_figure/pairwise_correlation_experiment_all_same_style.pdf`
  - `latex/revision/revision_for_figure/pairwise_correlation_experiment_all_same_style.png`
  - `latex/revision/revision_for_figure/pairwise_correlation_same_style_summary.csv`
  - `revision_history.md`

- **What changed**
  - Added a standalone preview folder for regenerating same-style pairwise selection-correlation panels without overwriting active manuscript or Extended Data figure assets.
  - The script recomputes same-parent and cross-parent per-event pairwise selection correlations from the existing simulation JSON and experimental ASV/coalescence tables, while reusing the already verified random-selection baseline values from the existing correlation summary CSV files.
  - Generated separate same-style Fig.~2D preview panels for the simulation ($\mu=0.6$) and Base experiment in `revision_for_figure/Fig2D/`, plus three-panel simulation sweep and experimental nutrient-condition previews.
  - Adjusted the Fig.~2D preview panels to be slightly wider than the first narrow draft, use smaller square mean markers, and use different y-axis scales for simulation and experiment.
  - The previews preserve the existing visual grammar: jittered event points, square mean markers with s.e.m., gray random-selection baseline, same-parent red/cross-parent blue colors, and significance brackets.

- **Type**
  - Revision-only figure preview workflow
  - Not yet integrated into active manuscript figures

- **Verification**
  - Ran `python -m py_compile make_pairwise_correlation_same_style.py`.
  - Ran `python -u make_pairwise_correlation_same_style.py` successfully from `latex/revision/revision_for_figure/`.
  - Visually inspected the generated PNG previews.

### R3-2 case-by-case additive null promoted to Extended Data Fig.~3

- **Affected reviewer points**: R3-2, with downstream Supplementary Figure renumbering for R3-3, R3-4, R2-5.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/extended_data.tex`
  - `latex/supplementary_sections/skewness_null_model.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/supplementary_sections/alternative_models_controls.tex`
  - `latex/supplementary_sections/simulations.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/figures/extended_data/ED_Fig3_combined.pdf`
  - `latex/figures/extended_data/ED_Fig3_combined.jpg`
  - `latex/figures/extended_data/combine_extended_figures.py`
  - `latex/supplementary_figs/file_source.md`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/internal_memo.tex`
  - `revision_history.md`

- **What changed**
  - Replaced the old Extended Data Fig.~3 abundance-skew distribution-null figure with the event-matched simple additive null model comparison previously included as Supplementary Fig.~38 / Response Fig.~R3-2A.
  - Updated the Extended Data Fig.~3 caption to directly present the case-by-case null requested by Reviewer 3: $n_{C,\mathrm{null}}=n_A+n_B$, paired null-to-observed PDI/asymmetry shifts for all 83 Base-medium events, and the class-transition heatmap.
  - Revised the Results text so the main manuscript now points to Extended Data Fig.~3 for the case-by-case additive-null answer, while retaining the distribution-level abundance-skew nulls in Supplementary Note~1.
  - Removed the duplicate Supplementary Fig.~38 additive-null block and renumbered subsequent Supplementary Figs.~39--45 to Supplementary Figs.~38--44, updating active manuscript, supplement, response-letter, and provenance references.

- **Type**
  - Extended Data figure replacement
  - Main-text synchronization
  - Supplementary figure renumbering
  - Response-letter synchronization
  - Figure provenance

## 2026-05-26

### L1/L2 normalization wording made explicit in similarity definition

- **Affected reviewer points**: R3-1.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/sections/methods.tex`
  - `latex/supplementary_sections/skewness_null_model.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `revision_history.md`

- **What changed**
  - Replaced the remaining ambiguous Results phrasing that described communities as "normalized abundance vectors."
  - Reframed $\vec{x}_A$, $\vec{x}_B$, and $\vec{x}_C$ as community composition vectors, and moved the Euclidean normalization into the explicit cosine-similarity formula: $\mathrm{Sim}(C,A)=(\vec{x}_C \cdot \vec{x}_A)/(\|\vec{x}_C\|_2\|\vec{x}_A\|_2)$ and analogously for parental community B.
  - Added a Methods clarification that, in the experimental analyses, the community composition vector is the ASV-abundance vector derived from the 16S profiles.
  - Synchronized the Methods, Supplementary Note~1, and R3-1 response-letter text so the response states that $\vec{x}$ denotes the community composition vector and the L$_2$ normalization is applied through the cosine denominator.
  - Recompiled `main.pdf`, `supplementary.pdf`, and `response_letter.pdf`.

- **Type**
  - Manuscript metric-definition clarification
  - Response-letter synchronization

---

### Natural-community taxonomic-distinctness analysis promoted to Supplementary Fig.~45, with statistical annotations

- **Affected reviewer points**: R2-5, with cross-reference to R3-4.

- **Files changed**
  - `../code/Figure_revision/R2_5_natural_taxonomic_distinctness/analyze_natural_taxonomic_distinctness.py`
  - `../code/Figure_revision/R2_5_natural_taxonomic_distinctness/Fig_R2_5_natural_taxonomic_distinctness.pdf`
  - `../code/Figure_revision/R2_5_natural_taxonomic_distinctness/Fig_R2_5_natural_taxonomic_distinctness.png`
  - `../code/Figure_revision/R2_5_natural_taxonomic_distinctness/natural_taxonomic_distinctness_summary.txt`
  - `latex/revision/revision_figure_folder/Fig_R2_5_natural_taxonomic_distinctness.pdf`
  - `latex/supplementary_figs/natural_taxonomic_distinctness.pdf`
  - `latex/supplementary_sections/figures.tex`
  - `latex/sections/results.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/supplementary_figs/file_source.md`
  - `latex/revision/revision_figure_folder/source.md`
  - `revision_history.md`

- **What changed**
  - Promoted the R2-5 natural-community taxonomic-distinctness analysis into the Supplementary Information as Supplementary Fig.~45 (a byte-identical copy of Response Fig.~R2-5), closing the prior gap in which the R2-5 response relied on a response-only figure not present in the revised supplement. (This completes the figure-integration portion of TODO item~2; the earlier 2026-05-26 entry recorded the caption/Results-pointer step.)
  - Added statistical annotations to the analysis script: per-box sample sizes ($n=6$/$60$/$435$ same-source/different-source/coalesced pairs per medium) on the distinctness panels (b,e), and per-medium one-sided paired Wilcoxon signed-rank $p$-values plus event counts ($n=30$) on the parental-signal panels (c,f). Own-parent similarity exceeded unrelated-parent similarity in every medium (all $p<10^{-6}$ at the ASV and Genus levels).
  - Extended the analysis summary file with a per-medium own-vs-unrelated Wilcoxon section so the response and caption statistics are traceable.
  - Updated the Supplementary Fig.~45 and Response Fig.~R2-5 captions to report the per-category sample sizes and the paired-Wilcoxon result, and strengthened the corresponding R2-5 response sentence with the $n$ and $p$ values.
  - Added a Results cross-reference to Supplementary Fig.~45 for the "argue against complete ASV-level convergence" sentence.
  - Added a provenance block for the supplement copy in `file_source.md` and noted in both provenance logs that the supplement and response PDFs are byte-identical copies that must be regenerated and re-copied together.

- **Type**
  - Supplementary figure integration
  - Figure regeneration with statistical annotation
  - Caption and response synchronization
  - Figure provenance

---

### Interaction-strength terminology in main manuscript

- **Affected reviewer points**: R2-6, R3-5.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/sections/methods.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`
  - `latex/supplementary_sections/assembly_effect.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Replaced remaining main-manuscript uses of "mean interaction strength(s)" with revised `\rev{interaction strength}` wording.
  - Updated the Results model-description paragraph, Methods simulation paragraph, and Fig.~2 caption to frame $\mu$ as the interaction strength parameter that controls the width/range of the $\mathbb{U}(0,2\mu)$ sampling distribution, increasing both coefficient mean and variance, rather than as simply "mean interaction strength."
  - Reframed Fig.~2/Fig.~3 Results references and Fig.~3 caption references to $\mu$ as "interaction-strength parameter value(s)" to distinguish the model parameter from coefficient mean alone.
  - Propagated the same framing to Supplementary Methods, Supplementary Note~2, Supplementary Fig.~18, and the R2/R3 response-letter prose, while leaving reviewer-quoted wording unchanged.
  - Added explicit manuscript-change quotes to R2-6 and R3-5 so the response letter states that the $\mu$ framing was revised in Results/Methods, not only in Supplementary Methods.
  - Added `amssymb` to the response-letter preamble so exact manuscript quotes containing `\mathbb{U}` compile.

- **Type**
  - Manuscript terminology revision
  - Supplementary terminology revision
  - Response-letter synchronization

---

### Supplementary Information high-level restructuring

- **Affected reviewer points**: Global supplementary organization; R1-1, R1-2, R1-4, R2-2, R3-3 cross-references.

- **Files changed**
  - `latex/supplementary.tex`
  - `latex/supplementary_sections/supplementary_methods.tex`
  - `latex/supplementary_sections/skewness_null_model.tex`
  - `latex/supplementary_sections/assembly_effect.tex`
  - `latex/supplementary_sections/invasion.tex`
  - `latex/supplementary_sections/alternative_models_controls.tex`
  - `latex/supplementary_sections/pairwise_selection_correlation.tex`
  - `latex/supplementary_sections/pool_size_dependency.tex`
  - `latex/supplementary_sections/predictability.tex`
  - `latex/supplementary_sections/natural_communities.tex`
  - `latex/sections/results.tex`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `revision_history.md`

- **What changed**
  - Reordered the active supplementary notes into five high-level sections: outcome classification / metric sensitivity / null models; assembly history / origin-correlated species fates; simulation robustness; nutrient perturbation / pairwise invasion resistance; and alternative models / controls.
  - Moved outcome-classification and metric-sensitivity content out of Supplementary Methods and into Supplementary Note 1.
  - Merged the pairwise-selection-correlation note into Supplementary Note 2 with the assembly-history material.
  - Renumbered Pairwise Invasion Experiments from Note 5 to Note 4 and Alternative Models and Controls from Note 7 to Note 5.
  - Converted inactive duplicate/placeholder section files into explicit moved/deleted stubs so future searches do not show duplicate active note definitions.
  - Updated active manuscript and response-letter references from Supplementary Note 7 to Supplementary Note 5 where needed.

- **Type**
  - Supplementary structure reorganization
  - Cross-reference synchronization

---

## 2026-05-21

### Response-tailoring policy added

- **Affected reviewer points**: Workflow infrastructure for the next response-tailoring iteration.

- **Files changed**
  - `response_tailoring_policy.md`
  - `revision_history.md`

- **What changed**
  - Added a standing response-tailoring policy modeled on the camera-ready policy structure, adapted to the `v4` rebuttal workflow.
  - Defined scope, minimal-change rules, evidence standards, source-of-truth priority, response-letter style gates, manuscript/supplement synchronization rules, figure provenance boundaries, verification steps, external-review expectations, and human-approval gates.
  - Resolved the local workflow conflict around reviewer-facing status markers by following the current `latex/revision/response/README.md` rule that workflow-only status and confidence markers should not appear in compiled response files.

- **Type**
  - Workflow infrastructure

### Manuscript copyedit consistency pass

- **Affected reviewer points**: General manuscript and response-letter polish.

- **Files changed**
  - `latex/sections/introduction.tex`
  - `latex/sections/results.tex`
  - `latex/sections/discussion.tex`
  - `latex/sections/methods.tex`
  - `latex/revision/response/reviewer2_response.tex`

- **What changed**
  - Standardized remaining Unicode punctuation in manuscript section files: converted curly apostrophes/quotes in the Introduction to LaTeX-style ASCII punctuation, replaced Unicode range dashes with LaTeX `--`, and rewrote one Unicode em-dash construction as comma-separated prose.
  - Standardized the theory wording toward `resource-consumer` by changing the Discussion reference from `consumer-resource theory` to `resource-consumer theory`.
  - Changed `Among 3` to `Among three`, expanded first use of `BHI` to `Brain Heart Infusion (BHI)`, removed a stale inline commented phrase in the Introduction, and clarified the Methods dilution wording as `seven daily 30-fold serial dilutions`.
  - Changed the natural-community pre-selection sentence from present to past tense in both `results.tex` and the matching R2-5 response-letter `\mschange{}` quote.
  - Skipped the previously flagged `\rollback{}` item because no current `\rollback{}` usage was present in the active manuscript source.

- **Type**
  - Manuscript copyedit
  - Response-letter quote synchronization
  - Revision-log update

---

## 2026-05-20

### R1-1C compact nutrient-column layout

- **Affected reviewer points**: R1-1.

- **Files changed**
  - `../../code/Figure_revision/R1_1_OD_density/analyze_OD_density.py`
  - `../../code/Figure_revision/R1_1_OD_density/Fig_R1_1C_pairwise_corr_vs_OD.pdf`
  - `latex/revision/revision_figure_folder/Fig_R1_1C_pairwise_corr_vs_OD.pdf`
  - `latex/supplementary_figs/Fig_R1_1C_pairwise_corr_vs_OD.pdf`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/supplementary_figs/file_source.md`

- **What changed**
  - Regenerated R1-1C as a compact 2-by-3 figure with nutrient conditions as columns.
  - Moved OD-tertile summaries to the top row and per-event parental-community OD scatterplots to the bottom row.
  - Updated the response-letter caption, supplementary caption, and figure provenance descriptions to match the new layout.

- **Type**
  - Figure layout update
  - Caption/provenance synchronization

---

### R1-9 cohesion-without-cooperation surprise emphasis

- **Affected reviewer points**: R1-9.

- **Files changed**
  - `latex/sections/discussion.tex`
  - `latex/revision/response/reviewer1_response.tex`

- **What changed**
  - Removed the cohesion-without-cooperation sentences from the reconciliation paragraph and promoted them to a new standalone Discussion paragraph placed immediately after it.
  - The new paragraph opens with "Notably, and perhaps counterintuitively" to flag the surprise in the topic clause (directly addressing R1-9's ask), replaces the em-dash with a comma, and situates Tikhonov 2016 within classical random Lotka-Volterra theory by adding citations to May 1972 and Grilli et al. 2017. The two follow-up sentences articulating the assembly-filtering mechanism are retained verbatim from the prior wording.
  - Deleted the redundant trailing `\rev{}` sentence that previously restated "consistent with and extend Tikhonov" alongside the May/Grilli/Hu citations. Hu 2022/2025 are already cited in the next paragraph on interaction strength as a control parameter, so removing them from the cohesion sentence does not lose any citation.
  - Updated the R1-9 response in `reviewer1_response.tex` to describe the relocation-and-emphasis change and quote the new paragraph as the `\mschange{}` block.

- **Type**
  - Manuscript text revision (Discussion paragraph relocation)
  - Response-letter update

---

### R1-1 supplementary figure split

- **Affected reviewer points**: R1-1, with downstream supplementary figure renumbering.

- **Files changed**
  - `latex/supplementary_sections/figures.tex`
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/alternative_models_controls.tex`
  - `latex/supplementary_sections/skewness_null_model.tex`
  - `latex/supplementary_sections/simulations.tex`
  - `latex/supplementary_figs/file_source.md`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/new review responses_2026-05-14/reviewer2_agents/R2_Q1_interaction_strength/response_fragment.tex`
  - `latex/revision/new review responses_2026-05-14/reviewer2_agents/R2_Q2_community_level_selection/response_fragment.tex`
  - `latex/revision/new review responses_2026-05-14/reviewer2_agents/R2_Q6_mathematical_model/evidence_audit.md`

- **What changed**
  - Removed the winner-OD-vs-loser-OD panel from the supplementary R1-1 display.
  - Split the remaining R1-1 analyses into two standalone supplementary figures: OD difference versus PDI as Supplementary Fig. 35, and OD-binned pairwise selection correlation as Supplementary Fig. 36.
  - Shifted the former Supplementary Figs. 36--43 to Supplementary Figs. 37--44 and updated active manuscript, supplementary, response, and provenance references accordingly.

- **Type**
  - Supplementary figure organization
  - Cross-reference synchronization

---

## 2026-05-19

### R1-2 pH response figure directional panels split

- **Affected reviewer points**: R1-2.

- **Files changed**
  - `../../code/Figure_revision/R1_2_pH_dominance/analyze_pH_dominance.py`
  - `../../code/Figure_revision/R1_2_pH_dominance/Fig_R1_2_acidalk_per_medium.pdf`
  - `latex/revision/revision_figure_folder/Fig_R1_2_acidalk_per_medium.pdf`
  - `latex/supplementary_figs/Fig_R1_2_acidalk_per_medium.pdf`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/revision/revision_figure_folder/source.md`

- **What changed**
  - Regenerated Response Fig.~R1-2 / Supplementary Fig.~37 as a four-panel figure.
  - Preserved the Base and Nutr$+$ pH-pair outcome-fraction panels.
  - Split the signed-asymmetry panel into all pH-pair types (positive = lower-pH parental community wins) and Acid-Alk pairs only (positive = acidic parental community wins).
  - Updated response and supplementary captions plus response-figure provenance.
  - Refactored the R1-2 directional-response paragraph to focus on the core implication: pH mismatch does not explain Dominance frequency, but among pH-mismatched pairs, pH direction helps predict winner identity, especially in Nutr$+$.
  - Tightened the two R1-2 response paragraphs by removing the small-category caveat and answering the reviewer's narrower question directly: the pH-direction signal is amplified when restricted to acid--alk pairs.
  - Added a short rationale for keeping Fig.~5 based on all eligible events, while placing the pH-mismatch-specific analysis in Supplementary Note~7 and Supplementary Fig.~37.
  - Replaced signed-asymmetry t-test p-values in the figure annotations and response prose with binomial p-values for the displayed lower-pH / acidic-parent win fractions, avoiding the misleading Base `p = 0.030` label next to the 28/44 acid-win fraction and explicitly describing the Base acid--alk result as statistically insignificant (`p = 0.096`).

- **Type**
  - Figure regeneration
  - Response caption update
  - Supplementary caption update

---

### R1-2 pH-mismatch response opening clarified

- **Affected reviewer points**: R1-2.

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`

- **What changed**
  - Moved the main figure-level answer to the start of the R1-2 response paragraph.
  - Removed detailed global pH-pair counts from the response prose.
  - Replaced the set notation for same-pH pairs with plain language.
  - Reframed the nonsignificant comparison and small-category caveat as the direct implication that pH mismatch alone is not sufficient to explain Dominance frequency.

- **Type**
  - Response text cleanup

---

### R1-2 Results §2.5 pH-mismatch insertion reverted

- **Affected reviewer points**: R1-2.

- **Files changed**
  - `latex/sections/results.tex`
  - `latex/revision/response/reviewer1_response.tex`

- **What changed**
  - Reverted the Results §2.5 pH paragraph to the v3 wording: dropped the `\rev{}` block that summarized the pH-mismatch frequency test and acid--alk win-rate, and restored the original two sentences about the acidic community winning 56\% in Base versus 91\% in Nutr$+$ ($p < 0.0001$, Extended Data Fig.~8) and the mechanistic top-down conclusion.
  - Removed the "To integrate and tone down this observation, we added to Results \S2.5: \mschange{...}" sentence from the R1-2 response, since that manuscript change no longer exists. The deferral to Supplementary Note~7 / Supplementary Fig.~37 in the preceding sentence already covers the routing.
  - Supplementary Note~7, Supplementary Fig.~37, and cross-references from the supplementary alternative-models discussion and other reviewer responses are unchanged.

- **Type**
  - Manuscript revert
  - Response text cleanup

---

### R1-2 Fig.~5-scope sentence rephrased

- **Affected reviewer points**: R1-2.

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`

- **What changed**
  - Removed the awkward "We therefore keep ..." connective in the second R1-2 paragraph; the preceding sentences describe the acid--alk amplification and do not logically justify the all-events scope of Fig.~5.
  - Split the run-on sentence into two: one stating that Fig.~5 and the associated predictability analysis remain based on all eligible events, and one pointing to the pH-mismatch-specific analysis in Supplementary Note~7 and Supplementary Fig.~37. Eliminates the prose-level semicolon.

- **Type**
  - Response text cleanup

---

### R1-4 pool-size survival-ratio alignment

- **Affected reviewer points**: R1-4.

- **Files changed**
  - `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`
  - `latex/revision/revision_figure_folder/pool_size_analysis.pdf`
  - `latex/revision/revision_figure_folder/pool_size_analysis_AB.pdf`
  - `latex/supplementary_figs/pool_size_analysis.pdf`
  - `latex/revision/response/reviewer1_response.tex`
  - `latex/supplementary_sections/alternative_models_controls.tex`
  - `latex/supplementary_sections/pool_size_dependency.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/revision/point_by_point/P3_reanalysis/R1_4_pool_size/memo.md`

- **What changed**
  - Replaced the R1-4 panel B post-coalescence parental ASV retention ratio with the reviewer-requested assembly survival-ratio diagnostic, computed as realized parental ASV richness divided by inoculated species-pool size.
  - Regenerated and recopied `pool_size_analysis.pdf` and `pool_size_analysis_AB.pdf`.
  - Updated the R1-4 response, Supplementary Note 7 text, Supplementary Fig. 34 caption, figure provenance, and memo to report the survival-ratio statistic (Kruskal--Wallis $p = 5.65 \times 10^{-13}$) while preserving the key Dominance result ($\chi^2 = 2.24$, $p = 0.69$).
  - Replaced R1-4 author-written "same-vs-cross" phrasing with same-parental-community versus cross-parental-community phrasing in manuscript-bound text.
  - Follow-up trim: shortened the R1-4 response body by removing figure-navigation, methods-inventory, and repeated interpretation sentences; moved the "survival ratio can exceed one" caveat into the Response Fig. R1-4 caption.
  - Follow-up supplement polish: shortened the Supplementary Note 7 pool-size paragraph, removed pooled Dominance percentages from the note prose, softened "held within each nutrient condition" to "did not detect a pool-size effect within individual nutrient conditions," and replaced "ASV-based assembly survival ratio" with "ASV richness per inoculated species" in the note prose.
  - Response close-out simplified to state that Supplementary Note 7 and Supplementary Fig. 34 were updated, without reproducing the full edited supplementary text.

- **Type**
  - Figure regeneration
  - Response text cleanup
  - Supplementary text cleanup
  - Figure provenance

---

### R1-5 metric-robustness response tightened

- **Affected reviewer points**: R1-5.

- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`

- **What changed**
  - Replaced the imprecise contrast between "relative-abundance metrics" and Jensen--Shannon with "abundance-weighted parental-similarity metrics."
  - Added an explicit Extended Data Fig. 2 pointer for the metric-comparison evidence.
  - Synchronized the quoted Extended Data Fig. 2 caption text in the response with the actual caption by including the final interpretive sentence about Jaccard and Jensen--Shannon as complementary metrics.

- **Type**
  - Response text cleanup

---

### R2-5 natural-community wording tightened

- **Affected reviewer points**: R2-5.

- **Files changed**
  - `latex/sections/title_abstract.tex`
  - `latex/sections/introduction.tex`
  - `latex/sections/methods.tex`
  - `latex/sections/results.tex`
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/revision/new review responses_2026-05-14/reviewer2_agents/R2_Q5_natural_community_preselection/response_fragment.tex`

- **What changed**
  - Aligned the Abstract, Introduction, and Methods with the R2-5 limitation by replacing broad natural-community/generalization language with natural sample-derived enrichment language.
  - Replaced the broad natural-community subsection title with the shorter caveated phrase "natural sample-derived enrichments."
  - Updated the Fig. 6 caption to avoid implying unfiltered natural environmental communities.
  - Smoothed the opening Results sentence and changed "Natural communities showed..." to "These enrichments showed..." for consistency.
  - Revised the R2-5 response to say the analysis tests retained post-stabilization source-level taxonomic differences, rather than implying that pre-to-post taxonomic erasure was measured.
  - Expanded the R2-5 manuscript-change close-out so it explicitly states that the natural-community framing was narrowed in the Abstract, Introduction, Methods, Results subsection title, and Fig. 6 caption.
  - Matched Response Fig. R2-5 caption panel labels to the lowercase panel letters in the figure.
  - Marked the older isolated R2-Q5 response fragment as superseded by the active response and figure.

- **Type**
  - Manuscript wording cleanup
  - Response text cleanup
  - Superseded-fragment annotation

---

## 2026-05-18

### R3-4 Discussion caveat wording tightened

- **Affected reviewer points**: R3-4, with consistency to R3-5 scope wording.

- **Files changed**
  - `latex/sections/discussion.tex`
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Replaced the Discussion caveat phrase about the empirical pairwise assay and theoretical model with a shorter statement that both the experimental system and model focus on a competition-dominated regime.
  - Updated the exact R3-4 response-letter `\mschange{}` quote so the response remains synchronized with the manuscript source.

- **Type**
  - Manuscript wording cleanup
  - Response quote synchronization

---

### R2-4 response split into two subquestions

- **Affected reviewer points**: R2-4, with cross-reference to R2-2.

- **Files changed**
  - `latex/revision/response/reviewer2_response.tex`

- **What changed**
  - Split R2-4 into two reviewer-comment/response blocks: one for clarifying pairwise selection correlation and one for the requested gLV invasion-fitness connection.
  - Revised the invasion-fitness block to refer back to the R2-2 framing that pairwise invasion assays primarily quantify experimental interaction strength in the gLV framework, while also serving as a two-species empirical approximation to invasion resistance / invasion fitness.
  - Removed the detailed auxiliary invasion-concordance paragraph and Response Fig.~R2-5 from the reviewer-facing R2-4 response, retaining only a concise cross-reference to the Supplementary Note and manuscript change.
  - Repositioned the Results \S2.2 manuscript-change quote under the selection-correlation clarification subquestion, and shortened the invasion-fitness subquestion to avoid repeating the Supplementary Note summary.
  - Tightened the first R2-4 subquestion around the operational meaning and limits of pairwise selection correlation, and added explicit quoted manuscript changes for the Results metric definition, Results gLV interpretation sentence, and Discussion limitation.
  - Clarified that the concordance component is related to co-occurrence/co-exclusion, while the same-parental-community versus cross-parental-community contrast tests whether concordant fates are structured by parental-community origin.
  - Expanded the explanation of the null model as a within-event shuffle of species' parental-origin labels, and replaced the ambiguous "positive pairwise selection correlation" phrasing with the more precise same-origin versus cross-origin concordance contrast.
  - Merged the two explanatory paragraphs in the first R2-4 subquestion into a single connected response paragraph.
  - Condensed repeated terminology in the first R2-4 response paragraph, distinguishing the raw concordance quantity from the same-versus-cross contrast more directly.
  - Replaced "concordance" terminology in the first R2-4 explanatory paragraph with "raw pair-level shared fate" and reframed the same-versus-cross sentence as a direct comparison against the shuffled parental-origin null.
  - Updated the Results \S2.2 quoted manuscript sentence and source text from "excess same-parent concordance" to "excess same-parent shared fate" for terminology consistency.
  - Moved the Results \S2.2 gLV interpretation quote from the selection-correlation clarification subquestion to the invasion-fitness subquestion.
  - Expanded the Results \S2.2 metric-definition sentence into two sentences, explicitly stating that same-parental-community and cross-parental-community shared-fate correlations are compared to test whether pair-level fate coupling depends on parental-community origin.
  - Refined the Results \S2.2 metric-definition quote to state more directly that the comparison tests whether species that assembled together show stronger coupled survival or extinction, indicating that parental-community origin predicts pair-level fate during coalescence.
  - Revised the same sentence to say parental-community origin affects pair-level fate coupling during coalescence, matching the intended interpretation of the metric.
  - Moved the Discussion mechanistic-limitation quote from the selection-correlation clarification subquestion to the invasion-fitness / framework subquestion.
  - Added an explicit Discussion limitation that the evidence for community-level selection is operational and outcome-based, assessed from parental-community similarity after coalescence and pairwise species-fate correlation rather than direct measurement of the mechanistic selection pressures generating those outcomes.
  - Refactored the R2-4 second subquestion to separate the pairwise invasion assay from the pairwise selection-correlation metric: the former is a two-species invasion-resistance / interaction-strength approximation, while the latter quantifies assembly-history-dependent fate coupling during community coalescence.
  - Removed the added Supplementary Note 4 ``Connection to invasion fitness'' subsection to avoid implying that pairwise selection correlation is derived from the pairwise invasion assays or is itself a per-capita growth-rate estimate.
  - Updated Supplementary Note 4 wording from concordance/mechanistic-basis language to shared-fate and outcome-level hallmark language.
  - Removed the Results \S2.2 gLV interpretation sentence and the corresponding R2-4 response quote, because the pairwise selection-correlation clarification is better handled by distinguishing it from the pairwise invasion assay rather than adding an additional gLV interpretation sentence.
  - Minor grammar pass on R2-4 and Results \S2.2 wording: clarified that the pairwise assay and pairwise selection-correlation metric are distinct measurements, changed ``between pairs'' to ``across species pairs,'' and revised ``stronger coupled'' to ``more strongly coupled.''
  - Replaced repeated ``readout'' wording in R2-1--R2-2 with ``operational measure'' or ``empirical proxy'' for invasion resistance.

- **Type**
  - Response text restructuring

---

## 2026-05-16

### R3-4 mutualism subquestion answered directly

- **Affected reviewer points**: R3-4, R3-5.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/revision/revision_figure_folder/R3_4_mutualistic_pair_fraction.pdf`
  - `latex/revision/revision_figure_folder/R3_4_mean_variance_grid.pdf`
  - `latex/revision/revision_figure_folder/source.md`
  - `latex/supplementary_sections/simulations.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/supplementary_figs/R3_4_mutualistic_pair_fraction.pdf`
  - `latex/supplementary_figs/R3_4_mean_variance_grid.pdf`
  - `latex/supplementary_figs/file_source.md`
  - `../code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mutualistic_pair_fraction.py`
  - `../code/Figure_revision/R3_3_nonCompetitive_gLV/make_mutualistic_pair_fraction_figure.py`
  - `../code/Figure_revision/R3_3_nonCompetitive_gLV/mutualistic_pair_fraction_results.json`
  - `../code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mean_variance_grid.py`
  - `../code/Figure_revision/R3_3_nonCompetitive_gLV/make_mean_variance_grid_figure.py`
  - `../code/Figure_revision/R3_3_nonCompetitive_gLV/mean_variance_grid_results.json`
  - `../code/Figure_revision/R3_4_mutualistic_pair_fraction.pdf`
  - `../code/Figure_revision/R3_4_mean_variance_grid.pdf`

- **What changed**
  - Moved the reviewer's mutualism question out of the R3-5 cross-reference-only answer and made it a separate subquestion inside R3-4.
  - Added a direct answer distinguishing three meanings: mutualism is outside the baseline competition-only gLV, mutualism can be a strong ecological interaction by effect magnitude, and mutualism would not appear as strong invasion resistance in the empirical failed-invasion readout.
  - Tied the answer to existing evidence from Response Fig.~R3-4a and to the existing Supplementary Methods and Discussion scope caveats.
  - Reordered the R3-4 figures so Response Figs.~R3-4a,b immediately follow the first facilitation/model-scope response, while Response Figs.~R3-4c,d follow the mutualism subquestion and reciprocal pair-coupling clarification.
  - Refactored the first R3-4 response paragraph to remove the early "toned down claims" clause and explicitly introduce the two simulation extensions: facilitative-tail mixed-sign coefficients and reciprocal-coefficient correlation structure.
  - Reordered the opening R3-4 prose so empirical support for the competition-only approximation appears first, followed by the broader-context simulation extensions.
  - Added the R3-4 robustness simulations to Supplementary Note 3, with the mixed-sign facilitative-tail analysis as Supplementary Fig.~37 and the reciprocal pair-coupling analysis as Supplementary Fig.~38.
  - Corrected reciprocal pair-coupling terminology after source-code audit: the sweep varies reciprocal sign/correlation structure with antisymmetric exploitation for `p < 0` and symmetric competition for `p > 0`; it is not described as retaining a strictly non-negative marginal or as a non-facilitative model.
  - Shortened the first R3-4 response paragraph to three sentences, keeping only the empirical rationale for treating competition as the major interaction source in this experiment.
  - Moved the reciprocal pair-coupling paragraph and Response Figs.~R3-4c,d back into the first R3-4 model-scope response, before the separate mutualism subquestion.
  - Added a weak bidirectional mutualistic-pair fraction sweep for the separate mutualism subquestion: 0, 10, 20, 30, or 40% of unordered species pairs are sampled with both reciprocal coefficients from `U[-0.2 mu, 0]`, while all other interactions remain competitive.
  - Added this new analysis as Response Fig.~R3-4e and Supplementary Fig.~39, with provenance in both figure-source logs.
  - Updated the mutualism answer to state that mutualism can be a strong positive interaction by effect magnitude but is distinct from strong competitive exclusion under the invasion-resistance readout; the new sweep shows weak mutualistic pairs do not remove the $\mu$-dependent Dominance trend.
  - Added a mean-vs-variance coefficient sweep as Response Fig.~R3-4f and Supplementary Fig.~40: $\alpha_{ij}\sim U[m-h,m+h]$ with `m = 0, 0.20, 0.40, 0.60, 0.80` and `h = 0, 0.20, 0.40, 0.60, 0.80`, so `std(alpha) = h/sqrt(3)`.
  - Updated the mutualism/interaction-strength answer to clarify that coefficient mean alone is not sufficient in this sweep: all `h=0` cells were Mixture, while increasing `h` at fixed `m` increased Dominance and same-parent concordance. Dominance correlated more strongly with `h`/standard deviation than with `m` across the 25 cells.

- **Type**
  - Simulation robustness analysis
  - Response text edit
  - Supplementary text edit
  - Supplementary figure integration

### R3-2 additive-null analysis integrated into Supplementary Information

- **Affected reviewer points**: R3-2.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/supplementary_sections/skewness_null_model.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/supplementary_figs/Fig_R3_2_additive_null_comparison.pdf`
  - `latex/supplementary_figs/file_source.md`

- **What changed**
  - Added the simple additive null model comparison used as Response Fig.~R3-2A to the Supplementary Information as Supplementary Fig.~35.
  - Expanded Supplementary Note 1 to explain the Euclidean-norm imbalance effect under the simple additive model, including why low-richness vectors can be sensitive to abundance unevenness among a small number of taxa.
  - Updated the R3-2 response to state that this case-by-case additive-null analysis is now included in the Supplementary Information.

- **Type**
  - Supplementary figure integration
  - Supplementary text edit
  - Response text edit

### R3-3 richness-confound response restructured

- **Affected reviewer points**: R3-3.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/sections/results.tex`
  - `latex/supplementary_sections/figures.tex`
  - `latex/supplementary_figs/Fig_R3_3_sim_parent_norm_asymmetry.pdf`
  - `latex/supplementary_figs/file_source.md`

- **What changed**
  - Removed the problematic explicit R3-2C cross-reference from the R3-3 experimental-null sentence and pointed the experimental additive-null claim to Response Fig.~R3-2A.
  - Moved the simulation norm/additive-null diagnostic into the second paragraph, where it now directly explains Response Fig.~R3-3B.
  - Replaced the previous high-$\mu$ composition-shuffling-null framing with the three representative main-figure interaction strengths: the simple additive null gives 0.0%, 5.7%, and 16.2% Dominance at $\mu = 0.3$, $0.6$, and $0.8$, whereas the actual post-assembly coalescence simulations give 20.4%, 61.0%, and 69.5% Dominance.
  - Removed the R3-3 Results \S2.3 manuscript-change quote from the response and restored the main Results paragraph to its previous wording without the simple-additive-null insertion.
  - Removed the independent pairwise selection-correlation paragraph from the R3-3 response.
  - Standardized the local R3 wording to use "simple additive null model" rather than "pair-specific simple additive nulls."
  - Added Response Fig.~R3-3B to the Supplementary Information as Supplementary Fig.~36 and documented its provenance.

- **Type**
  - Response text restructuring
  - Supplementary figure integration

---

## 2026-05-16

### R2-4 pairwise selection correlation response merge

- **Affected reviewer points**: R2-4.

- **Files changed**
  - `latex/revision/response/reviewer2_response.tex`

- **What changed**
  - Merged the cleaner framing from the isolated `new review responses_2026-05-14/reviewer2_agents/R2_Q4_pairwise_selection_correlation` audit into the active R2-4 response.
  - Consolidated the three split reviewer-comment fragments into one R2-4 reviewer comment and rewrote the response around three elements: metric definition, invasion-fitness interpretation, and inference boundary.
  - Kept the existing Response Fig. R2-5 and added a final manuscript-change close-out after the figure, including the exact Results sentence rendered with `\mschange{}`.

- **Type**
  - Response text edit
  - Response format cleanup

### R2-5 natural-community pre-selection response merge

- **Affected reviewer points**: R2-5.

- **Files changed**
  - `latex/revision/response/reviewer2_response.tex`
  - `latex/sections/results.tex`
  - `latex/sections/discussion.tex`
  - `latex/revision/revision_figure_folder/Fig_R2_5_post_stabilization_taxonomic_distinctness.pdf`
  - `latex/revision/revision_figure_folder/source.md`

- **What changed**
  - Merged accepted material from the isolated `new review responses_2026-05-14/reviewer2_agents/R2_Q5_natural_community_preselection` audit into the active R2-5 response.
  - Added a response-only post-stabilization taxonomic distinctness figure and reported same-source versus different-source ASV Jaccard similarities across media.
  - Strengthened the R2-5 response and Discussion caveat to state that the current data cannot quantify pre-to-post taxonomic convergence or functional convergence.
  - Narrowed the natural-community Results and Fig. 6 title so the claim is explicitly about laboratory-stabilized natural sample-derived communities rather than unfiltered natural ecosystems.
  - Follow-up format pass: added a final R2-5 manuscript-change close-out after the response-only figure, with exact Results and Fig. 6 title wording rendered using `\mschange{}`.

- **Type**
  - Response text edit
  - Manuscript text/caption edit
  - Response figure import
  - Figure provenance update

### Response letter reviewer order

- **Affected reviewer points**: Global response-letter structure.

- **Files changed**
  - `latex/revision/response_letter.tex`

- **What changed**
  - Changed the compiled response-letter order from Reviewer 3, Reviewer 2, Reviewer 1 to Reviewer 2, Reviewer 3, Reviewer 1.

- **Type**
  - Response-letter structure cleanup

### R3-3 richness response cleanup

- **Affected reviewer points**: R3-3.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`
  - `latex/sections/results.tex`

- **What changed**
  - Removed the red `\mschange{}` paragraph that proposed adding a Results \S2.4 final-richness sentence to the response.
  - Replaced the response's all-event coalesced-richness medians with the figure-script means: `13.0`, `9.9`, and `8.5` ASVs for Nutr-, Base, and Nutr+, respectively.
  - Removed the related richness-reduction sentence from the main Results nutrient-gradient paragraph.

- **Type**
  - Response text cleanup
  - Manuscript text cleanup

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

### R3-3 richness median formatting

- **Affected reviewer points**: R3-3.

- **Files changed**
  - `latex/revision/response/reviewer3_response.tex`

- **What changed**
  - Formatted final coalesced-community richness medians in the response text and manuscript-change quote with one decimal place: `13.0`, `7.0`, and `9.0` ASVs.

- **Type**
  - Response text formatting cleanup

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
## 2026-06-03 — Response-letter quote alignment audit

- **Affected reviewer points**: R1-5, R1-9, R2-1, R2-4, R2-6, R3-4.
- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`
    - Updated the Extended Data Fig. 2 metric-divergence quote and the Discussion "cohesion without cooperation" quote to match the current manuscript/supplementary wording.
  - `latex/revision/response/reviewer2_response.tex`
    - Updated nutrient-gradient, invasion-resistance, metric-divergence, and gLV-distribution quotes to match the current main/supplementary wording.
  - `latex/revision/response/reviewer3_response.tex`
    - Updated the competition-only model and Discussion limitation quotes to match the current supplementary methods and Discussion wording.
- **Type**
  - Response letter quote alignment

---

## 2026-06-03 — R2 minor-comments terminology and logic polish

- **Affected reviewer points**: R2 minor comments, R1-8 cross-reference.
- **Files changed**
  - `latex/sections/results.tex`
    - Fig. 2 caption: changed the null-label wording from "species origin labels" to "parental-affiliation labels" for consistency with Supplementary Note 2.
  - `latex/supplementary_sections/supplementary_methods.tex`
    - Clarified pH measurement wording and replicate-variability assessment.
    - Rephrased the gLV coefficient interpretation as an effective coefficient in the per-capita growth-rate equation.
  - `latex/revision/response/reviewer1_response.tex`
    - Updated the Fig. 2D quote to match the current caption.
  - `latex/revision/response/reviewer2_response.tex`
    - Polished R2 minor-comments responses for visualization, pH measurement, coefficient interpretation, terminology, and typographical correction.
  - `latex/revision/response_letter.tex`
    - Changed summary wording from "passive or simple explanations" to "alternative or simpler explanations."
- **Type**
  - Manuscript caption edit
  - Supplementary Methods text edit
  - Response letter wording and quote alignment

---

## 2026-06-03 — Fresh response/main alignment audit

- **Affected reviewer points**: R2-1, R2-4, R3-1, R3-2.
- **Files changed**
  - `latex/revision/response/reviewer2_response.tex`
    - Marked the nutrient-gradient quote as an excerpt and updated the Methods failed-invasion quote to match the current sentence.
  - `latex/revision/response/reviewer3_response.tex`
    - Updated the similarity-metric quotes and corrected the R3-2 retention-threshold quote to match the current Supplementary Note 1 wording.
- **Type**
  - Response letter quote alignment

---

## 2026-06-03 — Discussion scope of community-level selection shortened

- **Affected reviewer points**: R2-2, R2-4.
- **Files changed**
  - `latex/sections/discussion.tex`
    - Shortened the community-level selection scope paragraph so it defines the term operationally, briefly lists alternative mechanisms, and points detailed passive/null-model controls to Supplementary Note 5.
    - Removed the detailed pairwise-selection-correlation interpretation from this Discussion paragraph.
  - `latex/revision/response/reviewer2_response.tex`
    - Updated the R2-2 and R2-4 response text/quotes to match the revised Discussion scope paragraph and to keep pairwise-selection-correlation interpretation in Results/Supplementary Note 2.
- **Type**
  - Manuscript text edit
  - Response letter quote alignment

---

## 2026-06-03 — Concise natural-community pre-selection caveat

- **Affected reviewer points**: R2-5, R3 natural-community tone-down.
- **Files changed**
  - `latex/sections/results.tex`
    - §2.6: condensed the natural-community stabilization/pre-selection caveat and replaced "argue against" with a softer statement that retained richness and source-specific taxonomic structure indicate stabilization did not produce complete ASV- or genus-level taxonomic collapse.
  - `latex/revision/response/reviewer2_response.tex`
    - Updated the quoted manuscript change for R2-5 to match the concise §2.6 wording.
  - `latex/revision/response/reviewer3_response.tex`
    - Updated the quoted manuscript change for the natural-community tone-down response to match the concise §2.6 wording.
- **Type**
  - Manuscript text edit
  - Response letter quote alignment

---

## 2026-06-03 — R1-2 pH-mismatch response clarified

- **Affected reviewer points**: R1-2.
- **Files changed**
  - `latex/revision/response/reviewer1_response.tex`
    - Combined the reviewer context and question into a single comment block.
    - Rewrote the response to separate Dominance-frequency enrichment from acidic-parent winner-direction analysis.
    - Toned the interpretation so pH contrast is described as a Nutr$+$ contributor rather than a complete explanation.
  - `latex/supplementary_sections/alternative_models_controls.tex`
    - Added the strict same-pH versus acidic--alkaline Dominance-frequency comparison to Supplementary Note 5.
  - `latex/revision/response/reviewer1_response.tex`
    - Restored Response Fig.~R1-2 to the active response letter.
  - `latex/revision/point_by_point/P3_reanalysis/R1_2_pH_dominance/make_response_figure.py`
    - Added a reproducible script for the strict-threshold R1-2 response/supplementary figure.
  - `latex/revision/revision_figure_folder/Fig_R1_2_acidalk_per_medium.pdf`
    - Regenerated the response figure with current strict-threshold counts, replacing the superseded broad-split figure while matching the archived figure's compact stacked-bar / signed-outcome styling.
  - `latex/supplementary_figs/Fig_R1_2_acidalk_per_medium.pdf`
    - Added the same strict-threshold plot as Supplementary Fig.~46.
  - `latex/supplementary_sections/figures.tex`
    - Added Supplementary Fig.~46 with the strict pH-contrast Dominance-frequency and winner-direction panels.
  - `latex/revision/revision_figure_folder/source.md`
    - Documented the source and interpretation of the regenerated R1-2 response/supplementary figure.
- **Type**
  - Response letter logic polish
  - Supplementary text edit
  - Response figure restoration

---
