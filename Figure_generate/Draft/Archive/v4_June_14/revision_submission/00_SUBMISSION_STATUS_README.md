# Revision Submission Status

Prepared: 2026-06-16

Use this simplified folder for the current TeX-route upload set:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/`

Current contents:

- `01_Cover_Letter_Revision.pdf`
- `02_Main_Manuscript_Revised_LaTeX_Source.zip`
- `02_Main_Manuscript_Revised_Compiled.pdf`
- `04_Response_to_Reviewers_and_Editor.pdf`
- `05_Supplementary_Information_Revised.pdf`
- `06_Reporting_Summary_Revised.pdf`
- `07_Extended_Data_Figures/`

Current folder zip:

`00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL.zip`

LaTeX source bundle status:

- The staged `main.tex` compiled successfully with `latexmk -pdf main.tex`.
- The staged `supplementary.tex` compiled successfully with `latexmk -pdf supplementary.tex`.
- The staged `revision/response_letter.tex` compiled successfully with `latexmk -pdf response_letter.tex`.
- `naturemag.bst`, `.bbl` files, `references.bib`, figures, and compiled reference PDFs are included in the LaTeX source zip.

Important submission risk:

- The editor requested a highlighted Microsoft Word manuscript. This TeX-route package is being used because Word conversion was not sufficiently faithful.
- If the portal/editor rejects a LaTeX source zip for the revised manuscript, the remaining fallback is to ask the editorial office whether TeX source plus compiled PDF is acceptable, or create a manually checked highlighted Word manuscript.

Older preparation/archive material is stored in:

`99_NOT_FOR_UPLOAD_WORKING_FILES/`
