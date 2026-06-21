# Revision Submission Status

Prepared: 2026-06-16

Use this simplified folder for the current upload set:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/`

Current contents:

- `02_Main_Manuscript_Revised_Highlighted.docx`
- `02_Main_Manuscript_Revised_LaTeX_Source.zip`
- `02_Main_Manuscript_Revised_Compiled.pdf`
- `04_Response_to_Reviewers_and_Editor.pdf`
- `05_Supplementary_Information_Revised.pdf`
- `06_Reporting_Summary_Revised.pdf`
- `07_Extended_Data_Figures/`

Cover letter status:

- No cover letter is included in the current upload package.
- Previous cover-letter files were moved to `99_NOT_FOR_UPLOAD_WORKING_FILES/cover_letter_not_for_submission/`.

Current folder zip:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip`

LaTeX source bundle status:

- The staged `main.tex` compiled successfully with `latexmk -pdf main.tex`.
- The staged `supplementary.tex` compiled successfully with `latexmk -pdf supplementary.tex`.
- The staged `revision/response_letter.tex` compiled successfully with `latexmk -pdf response_letter.tex`.
- `naturemag.bst`, `.bbl` files, `references.bib`, figures, and compiled reference PDFs are included in the LaTeX source zip.

Word manuscript status:

- `02_Main_Manuscript_Revised_Highlighted.docx` was generated from LaTeX using Pandoc, Nature CSL numeric citations, a conversion-only equation fix, and DOCX post-processing for red revision styling and the title affiliation block.
- A Nature-formatting pass was applied to the derived Word file: 12 pt Times New Roman-compatible body text, compact title/heading sizes, continuous line numbering, one-inch margins, and no visible generated `Introduction` heading.
- Mechanical checks passed: the DOCX opens as a valid zip archive, contains six embedded main figures, has no raw `\textcolor`/`\frac` strings, uses numeric citations, includes the MIT affiliation line, keeps 203 `RevisionRed` spans plus 46 red equation/color markers, and includes line-numbering metadata.
- Before final portal upload, visually spot-check the DOCX against `02_Main_Manuscript_Revised_Compiled.pdf`, especially equations, citations, title/affiliation formatting, figure placement, line numbering, and red revision coloring.

Important submission risk:

- The Word file aligns better with the editor's Microsoft Word request than a TeX-only submission.
- The LaTeX source zip remains available as backup/source material if the portal asks for source files or if the Word conversion is rejected.

Older preparation/archive material is stored in:

`99_NOT_FOR_UPLOAD_WORKING_FILES/`
