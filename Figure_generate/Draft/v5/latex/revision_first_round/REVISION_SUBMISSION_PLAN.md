# Nature Ecology & Evolution Revision Submission Plan

Working folder:
`/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v5/latex/revision`

Assumption for this plan: the scientific response text and revised manuscript content are ready. The remaining work is submission packaging, consistency checking, data/code compliance, and portal upload preparation.

## Submission Goal

Prepare a complete revised submission package for Nature Ecology & Evolution that contains:

- revised manuscript
- response to reviewers
- revised Supplementary Information
- updated main and supplementary figures
- cover letter
- Reporting Summary
- data availability and code availability materials
- figure source data where appropriate
- administrative declarations required by the submission portal

## Local Files And Roles

### Response package

- Primary response source: `response_letter.tex`
- Reviewer-specific response files:
  - `response/reviewer1_response.tex`
  - `response/reviewer2_response.tex`
  - `response/reviewer3_response.tex`
- Compiled response output: `response_letter.pdf`
- Revision-response figures: `revision_figure_folder/`
- Figure provenance for response figures: `revision_figure_folder/source.md`

### Manuscript package

- Main manuscript source: `../main.tex`
- Main manuscript PDF: `../main.pdf`
- Main manuscript DOCX if needed: `../main_paper.docx`
- Supplementary source: `../supplementary.tex`
- Supplementary PDF: `../supplementary.pdf`
- Supplementary DOCX if needed: `../supplementary.docx`
- Cover letter source: `../cover_letter.tex`
- Cover letter PDF: `../cover_letter.pdf`

### Figure revision workspace

- Adobe/reference figure assets: `revision_for_figure/`
- Fig. 2A matrix assets for reviewer R1-7: `revision_for_figure/Fig2A/`
- Response-only figure assets: `revision_figure_folder/`

## Packaging Strategy

### 1. Build a clean revision PDF set

Compile the current manuscript, Supplementary Information, response letter, and cover letter. The minimum internal review PDF set should be:

- `../main.pdf`
- `../supplementary.pdf`
- `response_letter.pdf`
- `../cover_letter.pdf`

If the portal requests editable final files, prepare TeX/LaTeX sources or Word files according to the current submission-stage requirement. Nature allows flexible initial/revision formatting, but after accepted-in-principle the final manuscript must be supplied as Word or TeX/LaTeX rather than PDF only.

### 2. Make response/manuscript claims consistent

Every response phrase such as "we have added", "we now show", or "we performed" must correspond to a real manuscript, SI, figure, or response-letter change.

Priority checks:

- R1-7 must say the post-assembly interaction matrix is incorporated into Fig. 2A, not added as Supplementary Fig. 27, if that is the final plan.
- Fig. 2A caption must mention the post-assembly survivor interaction matrix.
- Supplementary figure numbering must not contain stale references to a removed Supplementary Fig. 27.
- `revision_figure_folder/source.md` must only describe response-letter figures actually used in the response.

### 3. Prepare data and code compliance items

Nature Ecology & Evolution requires availability statements for original research. For this manuscript, the likely required package is:

- raw sequencing reads in SRA/ENA/DDBJ, with accession or private reviewer link
- processed ASV/OTU/count table
- taxonomy table
- sample metadata and medium/treatment metadata
- code repository for analyses, simulations, and figure generation
- simulation data or scripts sufficient to regenerate simulation panels
- README describing how to reproduce manuscript figures
- Code Availability statement in the manuscript
- Data Availability statement in the manuscript

If private review access is used, record the exact reviewer-access token or temporary URL before submission.

### 4. Prepare figure source data

Nature encourages source data, and figure-level source data is especially useful for statistical plots. Prepare one source-data workbook or CSV bundle with tabs/files for:

- Fig. 1 panels
- Fig. 2 panels, including simulation outcome data and interaction-matrix summary statistics
- Fig. 3 panels
- Fig. 4 panels
- Extended Data or Supplementary statistical plots if requested or central
- statistical tests reported in the main text, figure captions, and rebuttal

The source data should contain plotted values and grouping variables, not just final image files.

### 5. Complete reporting and administrative documents

Prepare or update:

- Nature Reporting Summary
- competing interests statement
- author contributions
- acknowledgements and funding
- ethics/biosafety permits if applicable
- AI-use disclosure if substantive AI use affected scientific content
- ORCID and author details in the portal
- suggested/excluded reviewer fields if the portal asks

### 6. Final portal upload package

Create a final local submission folder after all checks pass. Suggested folder name:

`submission_package_YYYYMMDD/`

Recommended contents:

- `main_revised.pdf`
- manuscript source or DOCX if requested by portal
- `supplementary_revised.pdf`
- SI source or DOCX if requested by portal
- `response_to_reviewers.pdf`
- `cover_letter.pdf`
- main figure files if requested separately
- supplementary figure files if requested separately
- source data workbook/ZIP
- Reporting Summary
- data/code availability notes with accession links
- any repository private-access instructions

## Official Guidance Checked

- Nature Ecology & Evolution submission guidelines: https://www.nature.com/natecolevol/submission-guidelines
- Initial formatting: https://www.nature.com/natecolevol/submission-guidelines/initial-formatting
- Accepted-in-principle and formatting: https://www.nature.com/natecolevol/submission-guidelines/aip-and-formatting
- Reporting standards, data availability, and code availability: https://www.nature.com/natecolevol/editorial-policies/reporting-standards
- Peer review and transparent peer review: https://www.nature.com/natecolevol/editorial-policies/peer-review
- Image integrity: https://www.nature.com/natecolevol/editorial-policies/image-integrity
- AI policy: https://www.nature.com/natecolevol/editorial-policies/ai

