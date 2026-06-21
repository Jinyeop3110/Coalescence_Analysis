# Reporting Summary HTML Audit

Date: 2026-06-16

Working directory:

- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v4`

Files edited:

- `revision_submission/preparation/reporting_summary/reporting_summary_working.html`
- `revision_submission/preparation/reporting_summary/REPORTING_SUMMARY_HTML_AUDIT.md`

Files intentionally not edited:

- Main manuscript, Supplementary Information, response letter, figure captions, bibliography, source data, and all `latex/sections/*`, `latex/supplementary_sections/*`, `latex/main.tex`, `latex/supplementary.tex`, and `latex/revision/*` files.

## Workflow

The requested Writer, Reviewer, and Judge loop was applied section-by-section.

- Writer: drafted concise copy-ready Reporting Summary text using the evidence files and the user's required known values.
- Reviewer: checked factual support, missing details, field length, overstatement risk, and whether `NEED_USER_INPUT` was required.
- Judge: accepted supported text into the HTML, retained `NEED_USER_INPUT` markers for missing or uncertain details, and did not invent facts.

## Evidence Files Used

- `revision_submission/preparation/reporting_summary/REPORTING_SUMMARY_COPYPASTE_DRAFT.md`
- `revision_submission/preparation/reporting_summary/REPORTING_SUMMARY_DRAFT_NOTES.md`
- `revision_submission/preparation/data_code_availability/DATA_CODE_AVAILABILITY_DRAFT.md`
- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `latex/sections/title_abstract.tex`
- `latex/sections/results.tex` for stated nutrient-condition sample sizes, main simulation sample sizes, and figure-cited statistics
- `latex/supplementary_sections/tables.tex` for statistical reporting details, sidedness, no Bayesian analyses, and no formal multiple-comparison correction
- `latex/supplementary_sections/figures.tex` only where useful for Spearman/Fisher/control wording and sample-size verification

## Section-by-section Audit

### Paper information

Final text inserted:

- Title: `Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence`
- Corresponding author: `Jeff Gore`
- Authors: `Jinyeop Song, Jiliang Hu, Jeff Gore`
- Affiliation: `Department of Physics, Massachusetts Institute of Technology, Cambridge, MA, USA`

Evidence source file(s):

- `latex/sections/title_abstract.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`
- `REPORTING_SUMMARY_DRAFT_NOTES.md`

Confidence: high

Reviewer concerns addressed:

- Kept paper metadata identical to title/author evidence.

Judge decision: ACCEPT

Remaining `NEED_USER_INPUT` items: none

Suggested manuscript/SI change for user decision: none

### Field selection

Final text inserted:

`Ecological, evolutionary & environmental sciences`

`Yes. The study uses bacterial isolates and natural communities derived from environmental samples collected in Cambridge, MA, USA. Most experiments were controlled laboratory microcosm experiments, but the source material included field-collected environmental samples.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: high

Reviewer concerns addressed:

- Explicitly distinguished field-collected source material from controlled laboratory experiments.

Judge decision: ACCEPT

Remaining `NEED_USER_INPUT` items: none

Suggested manuscript/SI change for user decision: none

### Statistics checklist

Final text inserted:

`Statistical significance was defined as p < 0.05. All tests were two-sided unless explicitly stated otherwise. The manuscript reports paired t-tests for simulated interaction-strength summaries before and after assembly; a one-sided paired Wilcoxon signed-rank test for the Base-medium additive-null parental-asymmetry comparison; permutation tests with 1,000 permutations for pairwise selection correlations; Mann-Whitney U tests for comparisons with null distributions; chi-square tests for trend for outcome-fraction shifts across nutrient conditions; Fisher exact tests for categorical outcome comparisons; linear regression for prediction of coalescence outcomes from dominant-species competition; Spearman rank correlations for revision controls; and mixed-effects models in R/lme4 to control for parental richness and community identity where relevant. No Bayesian analyses were performed. No formal multiple-comparison correction was applied.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `latex/supplementary_sections/tables.tex`
- `latex/supplementary_sections/figures.tex`

Confidence: high

Reviewer concerns addressed:

- The earlier multiple-comparison uncertainty was resolved because Supplementary Methods explicitly states that no formal multiple-comparison correction was applied.
- Added the explicitly one-sided paired Wilcoxon signed-rank test for the Base-medium additive-null comparison so sidedness is not underreported.
- Spearman and Fisher tests were included only where figure/table evidence supports them.
- Bayesian analysis was stated as not performed based on Supplementary Methods/Table evidence.

Judge decision: ACCEPT

Remaining `NEED_USER_INPUT` items: none

Suggested manuscript/SI change for user decision: none

### Software and code

Final text inserted:

`Experimental data were collected using standard laboratory instruments and associated acquisition workflows. OD600 was measured with a BioTek Synergy H1 plate reader. Community pH was measured with an Apera Instruments PH5500 pH meter. 16S rRNA amplicon sequencing was performed by Argonne National Laboratory on an Illumina MiSeq platform. Final compositions in pairwise invasion assays were determined by colony counting. NEED_USER_INPUT: What instrument-control software, if any, should be reported for the BioTek plate reader, pH meter workflow, or sequencing facility?`

`16S rRNA amplicon reads were demultiplexed and denoised using QIIME2 and DADA2, and ASVs were taxonomically classified against the SILVA v138 database. Most analyses were performed in Python 3.11 using NumPy, pandas, SciPy, and scikit-learn. Mixed-effects models were fit in R using lme4. Custom scripts were used for generalized Lotka-Volterra simulations, coalescence outcome classification, statistical analyses, and figure generation. All code used for simulation and analysis is available via GitHub at https://github.com/Jinyeop3110/interspecies-interaction-derive-Community-Level-Selection. NEED_USER_INPUT: What exact package versions should be reported for QIIME2, DADA2, NumPy, pandas, SciPy, scikit-learn, R, and lme4? NEED_USER_INPUT: Will the GitHub repository be archived with Zenodo or another DOI-minting service?`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `revision_submission/preparation/data_code_availability/DATA_CODE_AVAILABILITY_DRAFT.md`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: medium

Reviewer concerns addressed:

- Package families and Python version are supported, but exact package versions are not in the evidence files.
- GitHub URL is supported; archival DOI is not yet confirmed.
- Data-collection software versions and whether instrument-control software should be reported are not in the evidence files, so a user-input marker was retained.
- Removed the first-pass statement that no custom acquisition software was used because it was not directly supported by the evidence files.

Judge decision: NEED_USER_INPUT for version/archive details; accepted supported instrument and code text

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: What instrument-control software, if any, should be reported for the BioTek plate reader, pH meter workflow, or sequencing facility?
- NEED_USER_INPUT: What exact package versions should be reported for QIIME2, DADA2, NumPy, pandas, SciPy, scikit-learn, R, and lme4?
- NEED_USER_INPUT: Will the GitHub repository be archived with Zenodo or another DOI-minting service?

Suggested manuscript/SI change for user decision:

- If a code DOI is minted, consider adding it to the manuscript Code Availability statement before final publication.

### Data availability

Final text inserted:

`Isolates and communities are available upon request. All data are available in the Supplementary Information and via Dryad at http://datadryad.org/share/LINK_NOT_FOR_PUBLICATION/kQACU7LCmQclVZfGZk0bS5ZPUVL_grhwah2zvFY4m9s. Raw sequencing reads are stated in the Methods as available via Dryad. NEED_USER_INPUT: Confirm that the private Dryad reviewer link works and contains raw 16S reads, processed abundance tables, metadata, taxonomy tables, simulation outputs, and figure source data. NEED_USER_INPUT: Are raw 16S reads deposited only in Dryad, or also in SRA/ENA/DDBJ? NEED_USER_INPUT: What public Dryad DOI/accession should replace the private reviewer link before publication?`

Evidence source file(s):

- `latex/sections/methods.tex`
- `revision_submission/preparation/data_code_availability/DATA_CODE_AVAILABILITY_DRAFT.md`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: medium

Reviewer concerns addressed:

- Used the current revision-stage Dryad statement without replacing it with an unconfirmed public DOI.
- Kept raw-read repository and Dryad-content checks as user-input items.

Judge decision: NEED_USER_INPUT for repository contents, raw-read repository scope, and public DOI/accession

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Confirm that the private Dryad reviewer link works and contains raw 16S reads, processed abundance tables, metadata, taxonomy tables, simulation outputs, and figure source data.
- NEED_USER_INPUT: Are raw 16S reads deposited only in Dryad, or also in SRA/ENA/DDBJ?
- NEED_USER_INPUT: What public Dryad DOI/accession should replace the private reviewer link before publication?

Suggested manuscript/SI change for user decision:

- Replace the private Dryad reviewer link in manuscript Data Availability with the public Dryad DOI/accession before publication.
- If raw reads are also in SRA/ENA/DDBJ, add the accession to the manuscript Data Availability statement.

### EEE study design - Study description

Final text inserted:

`This is a quantitative experimental and theoretical study of microbial community coalescence. Synthetic parental communities were assembled from a 54-isolate environmental bacterial library, stabilized by serial transfer, mixed pairwise at a 1:1 volume ratio, and propagated to post-coalescence endpoints under three nutrient conditions: Nutr-, Base, and Nutr+. Treatment factors included nutrient condition, inoculated richness, parental-community identity, and, in simulations, the generalized Lotka-Volterra interaction-strength parameter mu. Community composition was measured from V4 16S rRNA amplicon sequencing and analyzed as ASV relative-abundance profiles. Coalescence outcomes were classified as Dominance, Mixture, or Restructuring using predefined similarity-based criteria. Pairwise invasion assays and generalized Lotka-Volterra simulations were used to test interaction-dependent mechanisms, and natural sample-derived communities provided an additional test in taxonomically richer environmental assemblages.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `latex/sections/title_abstract.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: high

Reviewer concerns addressed:

- Kept the description concise and mechanism-neutral enough for Reporting Summary use.

Judge decision: ACCEPT

Remaining `NEED_USER_INPUT` items: none

Suggested manuscript/SI change for user decision: none

### EEE study design - Research sample

Final text inserted:

`The synthetic-community experiments used a library of 54 bacterial isolates derived from environmental samples collected in Cambridge, MA, USA, including soil, tree surface, and flower stamen environments. The isolate library spans 29 families across Proteobacteria, Firmicutes, and Bacteroidota. Natural sample-derived communities were generated from six additional environmental samples from soil, compost, and decomposing organic matter collected in Cambridge, MA, USA. These samples provided environmentally derived bacterial communities with broad taxonomic, growth, and environmental-modification diversity. The study did not involve human participants, human data, vertebrate animals, or clinical samples.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: high

Reviewer concerns addressed:

- Avoided implying exact GPS locations or dates not present in evidence.

Judge decision: ACCEPT

Remaining `NEED_USER_INPUT` items: none in this field

Suggested manuscript/SI change for user decision: none

### EEE study design - Sampling strategy

Final text inserted:

`No formal statistical sample-size calculation is described in the available methods or statistical reporting table. Experimental sample sizes were chosen based on the 54-isolate library size, the combinatorial design of non-overlapping or partially overlapping parental communities, 96-well plate capacity, and feasibility of serial-transfer coalescence experiments. Synthetic parental communities were assembled at inoculated richness levels of 6, 12, or 24 species, yielding 30 parental communities. Forty-seven synthetic coalescence pairs were planned with two biological replicates each, yielding 94 total Base-medium events before exclusions and 83 valid Base-medium events after sequencing failures or contamination were removed. Nutrient-perturbation coalescence experiments included Nutr- n = 90, Base n = 83, and Nutr+ n = 90 events. Pairwise invasion assays tested the 12 most abundant isolates in both directions, corresponding to 132 directional assays per medium. Natural sample-derived experiments used 15 pairwise coalescence events with two biological replicates per event, yielding n = 30 events per nutrient condition. Main generalized Lotka-Volterra simulation panels used n = 1,200 coalescence simulations per condition where stated. NEED_USER_INPUT: Confirm that no formal statistical sample-size or power calculation was performed.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `latex/sections/results.tex`
- `latex/supplementary_sections/tables.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`
- `REPORTING_SUMMARY_DRAFT_NOTES.md`

Confidence: high for numeric values; medium for sample-size-calculation status pending user confirmation

Reviewer concerns addressed:

- Included only traceable sample sizes requested by the user and supported by methods/results/table evidence.
- Did not generalize sample sizes to every figure panel.
- Replaced the definitive "no formal sample-size calculation was performed" claim with a statement limited to the available evidence and a user-input confirmation marker.

Judge decision: NEED_USER_INPUT for formal sample-size/power-calculation status

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Confirm that no formal statistical sample-size or power calculation was performed.

Suggested manuscript/SI change for user decision:

- If the authors confirm that no formal sample-size or power calculation was performed and want the statement manuscript-backed, they could add it to Methods or Supplementary Methods, but this is not required for the Reporting Summary draft.

### EEE study design - Data collection

Final text inserted:

`Jinyeop Song and Jiliang Hu performed the experiments. Isolates and communities were grown in 300 microliter volumes in 96-well deep-well plates at 25 C with shaking at 800 rpm. Parental communities were stabilized through seven daily 30-fold serial dilutions before coalescence. Coalescence experiments mixed two pre-stabilized parental communities at equal volume ratio and propagated the mixtures through seven additional daily serial transfers. Community composition was measured by V4-region 16S rRNA amplicon sequencing after DNA extraction with the QIAGEN DNeasy PowerSoil kit. OD600 was measured with a BioTek Synergy H1 plate reader, and pH was measured with an Apera Instruments PH5500 pH meter. Pairwise invasion endpoints were measured by colony counting after seven daily dilution cycles.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: high

Reviewer concerns addressed:

- Retained experimental personnel from the reporting-summary draft and all technical details from Methods/Supplementary Methods.

Judge decision: ACCEPT

Remaining `NEED_USER_INPUT` items: none in this field

Suggested manuscript/SI change for user decision: none

### EEE study design - Timing and spatial scale

Final text inserted:

`Environmental samples and isolates were collected in Cambridge, MA, USA, and experiments were performed as laboratory microcosms in 300 microliter wells. Synthetic and natural communities were propagated by daily 30-fold serial transfer, with seven transfers before coalescence and seven transfers after coalescence for endpoint measurements. The spatial scale of the experiments was the microplate well, and the spatial scale of environmental sampling was local Cambridge, MA microhabitats. NEED_USER_INPUT: What were the exact collection dates or date ranges?`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: medium

Reviewer concerns addressed:

- Exact dates are missing from evidence, so the HTML keeps a user-input marker.

Judge decision: NEED_USER_INPUT for collection dates

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: What were the exact collection dates or date ranges?

Suggested manuscript/SI change for user decision:

- If collection dates are required by the journal form, consider adding collection date ranges to Methods or Supplementary Methods as well.

### EEE study design - Data exclusions

Final text inserted:

`ASV tables were filtered to retain taxa with at least 0.1% relative abundance in any sample, matching the extinction threshold used in simulations. In the Base synthetic coalescence experiment, 47 planned coalescence pairs with two biological replicates yielded 94 total events; 11 events were excluded due to sequencing failures or contamination, resulting in 83 valid Base-medium events. Simulated species with relative abundance below 0.1% were set to zero at assembly and coalescence endpoints. The available evidence identifies sequencing failures, contamination, and predefined abundance thresholds as exclusion or filtering criteria. NEED_USER_INPUT: Were any additional samples or events excluded in Nutr-, Nutr+, natural-community, pairwise-invasion, or revision-control analyses? NEED_USER_INPUT: Confirm that exclusions were not based on the observed coalescence outcome.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`
- `REPORTING_SUMMARY_DRAFT_NOTES.md`

Confidence: medium

Reviewer concerns addressed:

- Known Base exclusions are stated precisely.
- Additional possible exclusions are not assumed; user-input markers remain.
- Removed the first-pass claim that exclusions were not outcome-dependent and replaced it with an explicit confirmation request.

Judge decision: NEED_USER_INPUT for additional exclusion categories outside the known Base exclusions

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Were any additional samples or events excluded in Nutr-, Nutr+, natural-community, pairwise-invasion, or revision-control analyses?
- NEED_USER_INPUT: Confirm that exclusions were not based on the observed coalescence outcome.

Suggested manuscript/SI change for user decision:

- If additional exclusions exist, consider adding them to Supplementary Methods or a supplementary statistical reporting table.

### EEE study design - Reproducibility

Final text inserted:

`Synthetic coalescence pairs were performed with two biological replicates where planned, and natural sample-derived coalescence events were performed with two biological replicates per pair. Communities were stabilized through repeated serial-transfer cycles before coalescence and propagated through repeated serial transfers after coalescence before endpoint sequencing. Pairwise invasion assays tested each isolate pair in reciprocal resident-invader directions across media. Simulation results were reproduced across independent random interaction matrices and randomized parental-community assignments, with robustness analyses using alternative model assumptions. Failed or invalid samples are described under Data exclusions.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `latex/supplementary_sections/tables.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: high

Reviewer concerns addressed:

- Avoided claiming technical sequencing replicates because they are not evidenced.

Judge decision: ACCEPT

Remaining `NEED_USER_INPUT` items: none in this field

Suggested manuscript/SI change for user decision: none

### EEE study design - Randomization

Final text inserted:

`Synthetic parental communities were assembled by predefined design-based assignment of isolates from the strain library into non-overlapping or partially overlapping species pools rather than by random allocation. Pairwise coalescence events were constructed systematically from stabilized parental communities according to the experimental design. Pairwise invasion assays tested all pairwise combinations among the 12 most abundant isolates in both resident-invader directions. In generalized Lotka-Volterra simulations, species identities were randomly permuted and assigned to parental communities after permutation, and independent interaction matrices were sampled for each replicate. NEED_USER_INPUT: Were plate positions, sample processing order, or sequencing order randomized or blocked?`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`
- `REPORTING_SUMMARY_DRAFT_NOTES.md`

Confidence: medium

Reviewer concerns addressed:

- Did not claim lab randomization beyond supported design-based assignment.
- Clearly separated simulation randomization from laboratory design.

Judge decision: NEED_USER_INPUT for plate/process/sequencing randomization or blocking

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Were plate positions, sample processing order, or sequencing order randomized or blocked?

Suggested manuscript/SI change for user decision:

- If randomization or blocking occurred, consider adding a concise statement to Methods or Supplementary Methods.

### EEE study design - Blinding

Final text inserted:

`No blinding is described in the available methods. Outcome classification and statistical analyses were computed from sequencing-derived ASV relative-abundance tables, colony-count thresholds, and predefined quantitative criteria. Because the primary outcomes were algorithmic or threshold-based rather than subjective visual classifications, blinding was not central to outcome assignment. NEED_USER_INPUT: Confirm whether any experimental, manual colony-counting, sample-handling, or data-processing steps were performed blind to treatment condition.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`
- `REPORTING_SUMMARY_DRAFT_NOTES.md`

Confidence: medium

Reviewer concerns addressed:

- Avoided a definitive no-blinding claim because the available methods do not describe blinding status for all experimental and manual steps.

Judge decision: NEED_USER_INPUT for experimental/manual colony-counting/sample-handling/data-processing blinding

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Confirm whether any experimental, manual colony-counting, sample-handling, or data-processing steps were performed blind to treatment condition.

Suggested manuscript/SI change for user decision:

- If any manual steps were blinded, consider adding that statement to Methods or the Reporting Summary final response.

### Field work - Field conditions

Final text inserted:

`Environmental material was collected from local microhabitats in Cambridge, MA, USA, including soil, tree surface, flower stamen, compost, and decomposing organic matter. Field conditions were not experimental treatment variables, and subsequent experiments were performed under controlled laboratory conditions. NEED_USER_INPUT: Should temperature, weather, season, or other field-condition metadata be reported?`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: medium

Reviewer concerns addressed:

- Did not invent weather, temperature, or season details.

Judge decision: NEED_USER_INPUT for field-condition metadata

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Should temperature, weather, season, or other field-condition metadata be reported?

Suggested manuscript/SI change for user decision:

- If field-condition metadata are available and relevant, consider adding them to Supplementary Methods.

### Field work - Location

Final text inserted:

`Samples were collected in Cambridge, MA, USA, from local soil, tree surface, flower stamen, compost, and decomposing organic matter microhabitats. NEED_USER_INPUT: Should exact GPS coordinates or site descriptions be included?`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: medium

Reviewer concerns addressed:

- Did not invent exact collection sites or coordinates.

Judge decision: NEED_USER_INPUT for GPS/site-description detail

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Should exact GPS coordinates or site descriptions be included?

Suggested manuscript/SI change for user decision:

- If exact sites or coordinates should be disclosed, consider adding them to Methods or Supplementary Methods.

### Field work - Access and import/export

Final text inserted:

`Samples were collected locally in Cambridge, MA, USA; no international import/export is described in the available methods. NEED_USER_INPUT: Confirm whether any permits were required, whether any protected habitats or protected species were sampled, and whether any international import/export or regulated sample transfer occurred.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: low to medium

Reviewer concerns addressed:

- Local collection is supported; import/export, regulated-transfer, permit, and protected-area/species status are not evidenced, so these remain user-input items.

Judge decision: NEED_USER_INPUT for permits/protected habitats/protected species/import-export/regulated transfer

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Confirm whether any permits were required, whether any protected habitats or protected species were sampled, and whether any international import/export or regulated sample transfer occurred.

Suggested manuscript/SI change for user decision:

- If permits, protected sites/species, import/export, or regulated transfers were involved, add the relevant access/permit/transfer statement to Methods.

### Field work - Disturbance

Final text inserted:

`Environmental sampling was limited to collecting material or surface-associated microbial samples for laboratory enrichment and isolate recovery; no large-scale habitat manipulation is described in the available methods. NEED_USER_INPUT: Confirm whether any field disturbance beyond small sample collection should be reported.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: low to medium

Reviewer concerns addressed:

- Removed the first-pass definitive statement that disturbance was minimal, because the evidence files do not describe exact sample amounts or field disturbance.
- Framed the statement around what is described in the available methods and retained a user-input marker.

Judge decision: NEED_USER_INPUT for field disturbance confirmation

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Confirm whether any field disturbance beyond small sample collection should be reported.

Suggested manuscript/SI change for user decision:

- If field disturbance details are required by the final form, consider adding a concise statement to Methods or Supplementary Methods.

### Optional Life sciences study design

Final text inserted:

- Sample size: same supported sample-size text as EEE Sampling strategy, shortened for Life sciences form fields, with the same sample-size/power-calculation confirmation marker.
- Data exclusions: same supported exclusions as EEE Data exclusions, with the same remaining additional-exclusions and outcome-dependence confirmation markers.
- Replication: synthetic and natural biological replicates, repeated serial transfers, reciprocal invasion directions, and independent simulation matrices/assignments.
- Randomization: design-based laboratory assignment and randomized simulations, with the same plate/process/sequencing randomization user-input marker.
- Blinding: no blinding described in the available methods, with the same experimental/manual-step blinding user-input marker.

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `latex/supplementary_sections/tables.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: medium to high

Reviewer concerns addressed:

- Included this section as optional because the recommended field selection is EEE, but Nature forms sometimes request Life sciences-style fields.
- Did not add new facts beyond the EEE fields.

Judge decision: ACCEPT with repeated `NEED_USER_INPUT` markers where the same uncertainties apply

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Were any additional samples or events excluded in Nutr-, Nutr+, natural-community, pairwise-invasion, or revision-control analyses?
- NEED_USER_INPUT: Confirm that exclusions were not based on the observed coalescence outcome.
- NEED_USER_INPUT: Confirm that no formal statistical sample-size or power calculation was performed.
- NEED_USER_INPUT: Were plate positions, sample processing order, or sequencing order randomized or blocked?
- NEED_USER_INPUT: Confirm whether any experimental, manual colony-counting, sample-handling, or data-processing steps were performed blind to treatment condition.

Suggested manuscript/SI change for user decision: same as matching EEE entries

### Specific materials, systems and methods

Final text inserted:

- Antibodies: `This study did not use antibodies.`
- Cell lines: `This study did not use cell lines.`
- Palaeontology: `This study did not involve palaeontological specimens.`
- Vertebrate animals: `This study did not involve vertebrate animals or regulated animal experiments.`
- Other organisms / microbial isolates: `The study used environmental bacterial isolates and microbial communities. Their source, culture conditions, and experimental use are described under the Ecological, evolutionary & environmental sciences study design section.`
- Human participants / human data: `This study did not involve human participants, human data, or human biological material.`
- Clinical data: `This study did not involve clinical data.`
- Dual use research of concern: `This study does not report experiments expected to constitute dual use research of concern. NEED_USER_INPUT: Confirm that institutional review did not identify dual use research of concern.`
- Plants: `This study did not involve plant genotypes, seed stocks, plant transformation, or plant growth experiments. Some environmental microbial isolates were derived from plant-associated or decomposing organic material, as described under field collection.`
- ChIP-seq: `This study did not use ChIP-seq.`
- Flow cytometry: `This study did not use flow cytometry.`
- MRI: `This study did not use MRI.`

Evidence source file(s):

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `REPORTING_SUMMARY_COPYPASTE_DRAFT.md`

Confidence: high for inapplicable modules except dual use; medium for dual use pending institutional confirmation

Reviewer concerns addressed:

- Avoided one-word `N/A` answers.
- Preserved the required full-sentence human, animal, and plant answers.
- Added an explicit microbial-isolate row so Nature's broader organism-related module is not treated as only a vertebrate-animal question.
- Retained a user-input marker for institutional dual-use confirmation.

Judge decision: ACCEPT with `NEED_USER_INPUT` for dual-use institutional confirmation

Remaining `NEED_USER_INPUT` items:

- NEED_USER_INPUT: Confirm that institutional review did not identify dual use research of concern.

Suggested manuscript/SI change for user decision: none unless institutional review requires a statement.

## Remaining NEED_USER_INPUT Items

- NEED_USER_INPUT: What instrument-control software, if any, should be reported for the BioTek plate reader, pH meter workflow, or sequencing facility?
- NEED_USER_INPUT: What exact package versions should be reported for QIIME2, DADA2, NumPy, pandas, SciPy, scikit-learn, R, and lme4?
- NEED_USER_INPUT: Will the GitHub repository be archived with Zenodo or another DOI-minting service?
- NEED_USER_INPUT: Confirm that the private Dryad reviewer link works and contains raw 16S reads, processed abundance tables, metadata, taxonomy tables, simulation outputs, and figure source data.
- NEED_USER_INPUT: Are raw 16S reads deposited only in Dryad, or also in SRA/ENA/DDBJ?
- NEED_USER_INPUT: What public Dryad DOI/accession should replace the private reviewer link before publication?
- NEED_USER_INPUT: What were the exact collection dates or date ranges?
- NEED_USER_INPUT: Confirm that no formal statistical sample-size or power calculation was performed.
- NEED_USER_INPUT: Were any additional samples or events excluded in Nutr-, Nutr+, natural-community, pairwise-invasion, or revision-control analyses?
- NEED_USER_INPUT: Confirm that exclusions were not based on the observed coalescence outcome.
- NEED_USER_INPUT: Were plate positions, sample processing order, or sequencing order randomized or blocked?
- NEED_USER_INPUT: Confirm whether any experimental, manual colony-counting, sample-handling, or data-processing steps were performed blind to treatment condition.
- NEED_USER_INPUT: Should temperature, weather, season, or other field-condition metadata be reported?
- NEED_USER_INPUT: Should exact GPS coordinates or site descriptions be included?
- NEED_USER_INPUT: Confirm whether any permits were required, whether any protected habitats or protected species were sampled, and whether any international import/export or regulated sample transfer occurred.
- NEED_USER_INPUT: Confirm whether any field disturbance beyond small sample collection should be reported.
- NEED_USER_INPUT: Confirm that institutional review did not identify dual use research of concern.

## Suggested manuscript/SI change for user decision

- Replace the private Dryad reviewer link in manuscript Data Availability with the public Dryad DOI/accession before publication.
- If raw reads are also in SRA/ENA/DDBJ, add the public accession to the manuscript Data Availability statement.
- If a code DOI is minted, consider adding it to the manuscript Code Availability statement before final publication.
- If additional exclusions beyond the known Base synthetic coalescence exclusions occurred, add them to Supplementary Methods or the statistical reporting table.
- If no formal sample-size or power calculation was performed and the authors want manuscript-backed support for that Reporting Summary answer, consider adding a concise statement to Methods or Supplementary Methods.
- If exclusions were not outcome-dependent, consider adding that concise confirmation to the Reporting Summary final response and, if useful, to Supplementary Methods.
- If plate/process/sequencing randomization or blocking occurred, consider adding it to Methods or Supplementary Methods.
- If collection dates, GPS/site descriptions, field-condition metadata, permits, disturbance, protected-site/protected-species, import/export, or regulated-transfer statements are required by the final form, consider adding concise supporting text to Methods or Supplementary Methods.

## Final Judge Summary

The HTML working file was created because no prior `reporting_summary_working.html` existed. Supported sections were accepted into the HTML. Missing or uncertain details were marked with explicit `NEED_USER_INPUT` strings rather than inferred. No manuscript, Supplementary Information, response letter, figure caption, bibliography, or source-data file was edited.
