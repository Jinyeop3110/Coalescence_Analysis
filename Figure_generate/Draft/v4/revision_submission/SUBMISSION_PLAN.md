# Revision Submission Plan

Prepared: 2026-06-16

## Submission Route

Primary route: submit the highlighted Word manuscript, because the editor explicitly requested a highlighted manuscript text file in Microsoft Word format.

The LaTeX source zip is retained as a backup/source package. Upload it only if the portal requests source files or if the Word manuscript is not accepted/usable in the manuscript slot.

Use this folder:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/`

Use the folder zip only if the portal offers a bulk-upload option:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip`

Do not upload files from:

`99_NOT_FOR_UPLOAD_WORKING_FILES/`

## Pre-upload Gate

Do not submit the ready-folder zip until these checks are resolved:

1. Reporting Summary
   - The staged file `00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/06_Reporting_Summary_Revised.pdf` must be treated as pending until it is refilled or replaced.
   - Reason: the current PDF is an Adobe XFA form. Standard PDF renderers show only the Adobe placeholder page, and the embedded XFA data inspected locally contains older Life Sciences wording rather than the audited Ecological, evolutionary & environmental sciences wording.
   - Required correction: refill the official Nature Reporting Summary form from the audited working text, then replace `06_Reporting_Summary_Revised.pdf` in the ready folder.
   - Authoritative local source for refilling:
     - `99_NOT_FOR_UPLOAD_WORKING_FILES/preparation/reporting_summary/reporting_summary_working.html`
     - `99_NOT_FOR_UPLOAD_WORKING_FILES/preparation/reporting_summary/REPORTING_SUMMARY_HTML_AUDIT.md`
   - Do not upload a Reporting Summary that still says `No data were excluded from the analyses`, because the audited wording identifies 11 excluded Base-medium events out of 94 planned events.
   - Do not upload a Reporting Summary that says laboratory samples or bacterial isolates were randomly allocated unless plate/sample/order randomization has been confirmed. The supported wording is design-based laboratory assignment, with randomization used in simulations.

2. Remaining Reporting Summary confirmations
   - Resolve or deliberately answer every remaining `NEED_USER_INPUT` item in the audited working text before producing the final PDF.
   - Highest-risk items: extra exclusions outside Base, plate/sample/sequencing order randomization, blinding of manual steps, exact field collection dates/site/permit/disturbance details, and software/package versions.

3. Source Data
   - No final `Source_Data.xlsx` or source-data zip is currently in the ready folder.
   - This is not necessarily required for revision upload unless the portal asks for it, but if MTS provides a Source Data slot, create and upload a final source-data workbook or source-data zip.
   - Draft source-data planning files are in `99_NOT_FOR_UPLOAD_WORKING_FILES/preparation/source_data/`; they are not final upload files.

## Upload Order

1. Main manuscript
   - Upload `02_Main_Manuscript_Revised_Highlighted.docx` in the manuscript text-file slot.
   - This Word file is formatted for review with red revision text, numeric citations, continuous line numbering, one-inch margins, 12 pt body text, and an unheaded introductory opening after the abstract.
   - If the portal asks for source files, upload `02_Main_Manuscript_Revised_LaTeX_Source.zip` as source/backup.
   - If the portal asks for a compiled manuscript PDF, upload `02_Main_Manuscript_Revised_Compiled.pdf`.
   - The compiled PDF is the marked/revised version: `\rev{...}` is defined as red text in `main.tex`.

2. Response to reviewers/editor
   - Upload `04_Response_to_Reviewers_and_Editor.pdf`.

3. Supplementary Information
   - Upload `05_Supplementary_Information_Revised.pdf`.

4. Reporting Summary
   - Upload `06_Reporting_Summary_Revised.pdf` only after the pre-upload Reporting Summary gate above is satisfied.
   - If the portal itself provides the editable Reporting Summary fields, paste from the audited working HTML rather than relying on the currently staged XFA data.

5. Extended Data figures
   - Upload the PDFs in `07_Extended_Data_Figures/` only if the portal asks for separate Extended Data files.
   - If the portal does not ask for them separately, keep them available but avoid duplicate upload unless requested.

6. Cover letter
   - Do not upload a cover letter for this submission plan.
   - The previous cover-letter files were moved to `99_NOT_FOR_UPLOAD_WORKING_FILES/cover_letter_not_for_submission/`.

## Portal Risk

This package now includes a highlighted Word manuscript to align with the editor's instruction. Because it was converted from LaTeX, the Word file should still be visually spot-checked against the compiled PDF before upload, especially equations, citations, title/affiliation formatting, figure placement, line numbering, and red revision coloring.

If the portal rejects the Word conversion or requires a different source-file workflow, use the LaTeX source zip as the fallback and contact the editorial office if needed. Suggested wording:

> We prepared the revision in LaTeX, and Word conversion introduced formatting problems. May we submit the revised manuscript as LaTeX source together with the compiled marked PDF?

## Exact Conversion And Replacement Workflow

### Word manuscript conversion

Current accepted output:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/02_Main_Manuscript_Revised_Highlighted.docx`

How it was produced:

1. Convert the LaTeX manuscript to DOCX with Pandoc using Nature numeric/superscript citation styling.
2. Preserve revised text by mapping LaTeX `\rev{...}` spans to a red Word character style named `RevisionRed`.
3. Use a conversion-only LaTeX copy for the problematic display equation so Pandoc can convert it to Word OMML math rather than raw TeX.
4. Post-process the DOCX to restore the title/author/affiliation block.
5. Post-process the DOCX again for Nature-style review formatting: 12 pt Times New Roman-compatible body text, compact title/headings, continuous line numbering, one-inch margins, and no visible generated `Introduction` heading.
6. Copy the final DOCX into the ready folder.

Mechanical checks to repeat after any Word regeneration:

Run from `revision_submission/`:

```bash
unzip -t 00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/02_Main_Manuscript_Revised_Highlighted.docx
textutil -convert txt -stdout 00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/02_Main_Manuscript_Revised_Highlighted.docx | sed -n '1,40p'
unzip -p 00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/02_Main_Manuscript_Revised_Highlighted.docx word/document.xml | rg 'lnNumType|pgMar|\\textcolor|\\frac|eq:similarity'
```

Expected results:

- DOCX archive validates.
- Extracted text begins with title, authors, MIT affiliation, abstract, then the unheaded first introductory paragraph.
- `lnNumType` and one-inch `pgMar` metadata are present.
- No raw `\textcolor`, `\frac`, or `eq:similarity` strings remain.

### Reporting Summary conversion

Current staged file:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/06_Reporting_Summary_Revised.pdf`

Status:

- Pending replacement or refill before upload.
- The official Nature Reporting Summary PDF is an Adobe XFA form. Browser Preview/Poppler-style renderers may show only a placeholder page; use Adobe Acrobat/Reader or the MTS form interface.

Required precise workflow:

1. Open the audited working copy:
   - `99_NOT_FOR_UPLOAD_WORKING_FILES/preparation/reporting_summary/reporting_summary_working.html`
2. Resolve all remaining `NEED_USER_INPUT` text.
3. Paste the final answers into the official Nature Reporting Summary form, using the Ecological, evolutionary & environmental sciences section.
4. Save/export the completed form as `06_Reporting_Summary_Revised.pdf`.
5. Replace the file in `00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/`.
6. Verify the saved form by reopening it in Adobe Acrobat/Reader or by checking the portal preview after upload.
7. If the portal preview cannot display the XFA PDF, use the portal's editable checklist fields if available and paste directly from the audited working HTML.

Minimum content checks for the final Reporting Summary:

- Field-specific section is Ecological, evolutionary & environmental sciences.
- Field work/source material is disclosed because environmental samples came from Cambridge, MA, USA.
- Base-medium exclusions state 94 planned events, 11 excluded because of sequencing failures or contamination, 83 valid events.
- Randomization distinguishes laboratory design-based assignment from simulation randomization.
- Blinding states that outcome classification was algorithmic/threshold-based and identifies any manual steps as unblinded or confirmed if blinded.
- Software/code text includes Python 3.11, NumPy, pandas, SciPy, scikit-learn, R/lme4 if used, DADA2/QIIME2/SILVA as supported, plus exact versions where confirmed.
- Data availability uses the public Dryad DOI if final: `10.5061/dryad.2z34tmq0z`.
- No `NEED_USER_INPUT`, `VERIFY`, placeholder, or private reviewer-link text remains.

### Rebuilding the ready-folder zip

After replacing any ready-folder file:

Run from `revision_submission/`:

```bash
rm -f 00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip
zip -r -X 00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip 00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL
unzip -t 00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip
unzip -l 00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip | rg -i 'cover|~\$|tmp' && { echo 'unexpected file found'; exit 1; } || echo 'no cover/temp files found'
```

Expected result:

- Zip archive validates.
- No cover letter, Word lock file, temp file, or working draft appears in the ready zip.

## Technical Check Of LaTeX Source Zip

The LaTeX source zip is:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/02_Main_Manuscript_Revised_LaTeX_Source.zip`

It includes the files needed to compile the current manuscript package:

- Main manuscript entry point: `main.tex`
- Supplementary Information entry point: `supplementary.tex`
- Response letter entry point: `revision/response_letter.tex`
- Main manuscript sections in `sections/`
- Supplementary sections in `supplementary_sections/`
- Main figures in `figures/`
- Extended Data figures in `figures/extended_data/`
- Supplementary figures in `supplementary_figs/`
- Response figures in `revision/revision_figure_folder/`
- Reviewer response source files in `revision/response/`
- Bibliography files: `references.bib`, `main.bbl`, `supplementary.bbl`, `revision/response_letter.bbl`
- Bibliography style: `naturemag.bst`
- Compiled reference PDFs:
  - `Main_revised_compiled.pdf`
  - `Supplementary_Information_revised_compiled.pdf`
  - `Response_to_Reviewers_and_Editor.pdf`
  - `Reporting_Summary_Revised.pdf`
- Compile instructions: `README_compile.txt`

Marked-revision formatting:

- In `main.tex`, `\rev{...}` is defined as `\textcolor{red}{...}`.
- In `supplementary.tex`, `\rev{...}` is defined as `\textcolor{red}{...}`.
- Therefore, the compiled main manuscript and Supplementary Information show `\rev{...}` changes in red.
- The response letter uses separate response-letter color macros; manuscript-change quotations are shown in dark red there.

Verification completed:

- Staged `main.tex` compiled successfully with `latexmk -pdf main.tex`.
- Staged `supplementary.tex` compiled successfully with `latexmk -pdf supplementary.tex`.
- Staged `revision/response_letter.tex` compiled successfully with `latexmk -pdf response_letter.tex`.
- `02_Main_Manuscript_Revised_LaTeX_Source.zip` passed `unzip -t`.
- `00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip` passed `unzip -t`.

Zip inventory:

- `02_Main_Manuscript_Revised_Highlighted.docx`: about 14 MB.
- `02_Main_Manuscript_Revised_LaTeX_Source.zip`: about 51 MB.
- `00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip`: about 87 MB.
- Source zip contains 25 `.tex` files, 184 `.pdf` files, 1 `.bib` file, 3 `.bbl` files, and 1 `.bst` file.

## Technical Answer

Yes, the LaTeX source zip includes the figures and source files needed by the current TeX manuscript, Supplementary Information, and response letter. This is supported by the successful staged compiles.

It does not include raw data, source data workbooks, analysis code, or unrelated working drafts. Those are separate from the manuscript TeX source package and should only be uploaded if the portal specifically asks for them.
