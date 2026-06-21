# Revision Submission TODO

Assumption: the response letter and updated manuscript text are scientifically ready. This checklist starts from that point.

## A. Build Final Documents

- [ ] Compile `../main.tex` to `../main.pdf`.
- [ ] Compile `../supplementary.tex` to `../supplementary.pdf`.
- [ ] Compile `response_letter.tex` to `response_letter.pdf`.
- [ ] Compile `../cover_letter.tex` to `../cover_letter.pdf`.
- [ ] Check all PDFs open without missing figures, blank pages, unresolved references, or bad line breaks.
- [ ] If the portal requests editable files, prepare `../main_paper.docx`, `../supplementary.docx`, or the TeX source bundle.

## B. Response-Manuscript Consistency

- [ ] Search the response for "we have added", "we now", "we performed", and confirm each claim exists in the manuscript, SI, or response figures.
- [ ] Confirm R1-7 says the post-assembly interaction matrix was added to Fig. 2A, not Supplementary Fig. 27, if that is the final decision.
- [ ] Confirm Fig. 2A contains the selected post-assembly survivor interaction matrix asset from `revision_for_figure/Fig2A/`.
- [ ] Confirm the Fig. 2 caption explains that the post-assembly matrix is restricted to surviving species and illustrates weaker within-community competition.
- [ ] Remove or revise stale Supplementary Fig. 27 references if the separate supplementary interaction-matrix figure is abandoned.
- [ ] Verify reviewer comment order and numbering in `response_letter.pdf`.

## C. Figure And Source-Data Package

- [ ] Export final main figures at journal-quality resolution.
- [ ] Export final Supplementary/Extended Data figures if requested separately.
- [ ] Check figure labels, panel letters, legends, colors, and scale bars after Adobe assembly.
- [ ] Confirm all figure files match the manuscript captions.
- [ ] Prepare source data for main statistical figures.
- [ ] Include Fig. 2 source data: simulation outcomes, pairwise-interaction summaries, pairwise-selection-correlation values, and interaction-matrix summary values.
- [ ] Prepare a source-data README that maps each tab/file to figure panels.

## D. Data Availability

- [ ] Confirm raw sequencing reads are deposited in SRA, ENA, DDBJ, or equivalent.
- [ ] Record accession numbers or private reviewer-access links.
- [ ] Confirm processed abundance tables are deposited or included in a repository.
- [ ] Confirm taxonomy table is deposited or included.
- [ ] Confirm sample metadata and treatment/medium metadata are deposited or included.
- [ ] Update the manuscript Data Availability statement with exact links/accessions.
- [ ] Test private reviewer-access links in a clean browser session.

## E. Code Availability

- [ ] Prepare a code repository or archive for analysis, simulation, and figure-generation scripts.
- [ ] Add a README explaining environment setup and how to regenerate main results/figures.
- [ ] Include or link simulation input/output files needed for reproducibility.
- [ ] Mint a DOI if using Zenodo or a comparable archive.
- [ ] Update the manuscript Code Availability statement with exact repository/DOI information.
- [ ] Test repository access from a clean browser session.

## F. Reporting And Declarations

- [ ] Complete or update the Nature Reporting Summary.
- [ ] Confirm competing interests statement.
- [ ] Confirm author contributions.
- [ ] Confirm acknowledgements and funding.
- [ ] Confirm any ethics, permits, or biosafety statements if applicable.
- [ ] Decide whether any AI-use disclosure is needed beyond copy editing.
- [ ] Confirm author names, affiliations, emails, and ORCIDs in the submission portal.

## G. Final Internal Review

- [ ] Read `response_letter.pdf` once continuously as if you are the editor.
- [ ] Read the revised abstract, introduction, Fig. 2 section, discussion, and limitations for consistency with the rebuttal.
- [ ] Check that new claims introduced during revision are backed by figures, stats, or citations.
- [ ] Check all references compile and bibliography entries are complete.
- [ ] Check spelling of Nature Ecology & Evolution, reviewer labels, figure numbers, and supplement labels.
- [ ] Make a final backup copy of the full `latex/` folder or commit the final state.

## H. Final Upload Folder

- [ ] Create `submission_package_YYYYMMDD/` under `latex/revision/`.
- [ ] Copy final `main_revised.pdf`.
- [ ] Copy final `supplementary_revised.pdf`.
- [ ] Copy final `response_to_reviewers.pdf`.
- [ ] Copy final `cover_letter.pdf`.
- [ ] Copy final figure files if the portal requests separate figure uploads.
- [ ] Copy source-data workbook or ZIP.
- [ ] Copy Reporting Summary.
- [ ] Add a plain-text `UPLOAD_NOTES.txt` containing data/code accession links and any private reviewer-access instructions.
- [ ] Upload files to the Nature portal and verify each file type is assigned correctly.
- [ ] Download or save the submission confirmation.

