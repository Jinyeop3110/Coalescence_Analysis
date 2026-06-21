# Word Conversion Report

Prepared: 2026-06-16

## Recommended Word File

Use:

`02_Main_Manuscript_Revised_Highlighted.docx`

Copied to:

`../00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/02_Main_Manuscript_Revised_Highlighted.docx`

## Conversion Method

- Tool: Pandoc 3.7.0.2.
- Main conversion path: LaTeX to DOCX.
- Citation style: `nature.csl` from the official Citation Style Language styles repository, used to keep citations numeric/superscript rather than author-year.
- Red revision handling: `pandoc_revision_style.lua` maps LaTeX red revision spans to the Word character style `RevisionRed`.
- Reference DOCX: `reference_revision_red.docx`, generated from Pandoc's default reference DOCX and patched to define `RevisionRed` as red text.
- Equation handling: a conversion-only copy of `latex/sections/results.tex` unwrapped one `\rev{...}` display-equation wrapper so Pandoc could convert it to Word OMML math instead of raw TeX.
- DOCX post-processing: `color_similarity_equation_docx.py` applied `RevisionRed` and `FF0000` color to the converted similarity equation's OMML math runs.
- Title-block post-processing: `patch_docx_title_block.py` restored the author affiliation line that Pandoc dropped from the LaTeX `authblk` title block.
- Nature-formatting post-processing: `format_nature_eco_evo_docx.py` normalized the derived Word file to a reviewer-friendly manuscript layout: Times New Roman-compatible 12 pt body text, compact 14 pt title, 12 pt headings, continuous line numbering, one-inch margins, and no visible generated `Introduction` heading.

Original manuscript/SI LaTeX source files were not edited.

## Other Routes Tested

- Direct Pandoc conversion succeeded, but the similarity equation rendered as raw TeX because Pandoc could not parse `\textcolor{red}{...}` inside display math.
- TeX4ht/make4ht produced a valid ODT and preserved red spans in the ODT, but the ODT-to-DOCX conversions tested here were not acceptable:
  - Pandoc ODT-to-DOCX stripped the generated red text styles.
  - macOS `textutil` ODT-to-DOCX produced a tiny DOCX without embedded figures and with many math expressions missing from plain-text extraction.
- LibreOffice/soffice was not installed locally, so a LibreOffice ODT-to-DOCX export could not be tested.

## Mechanical Checks Passed

- `unzip -t 02_Main_Manuscript_Revised_Highlighted.docx`: no archive errors.
- Embedded main figures: 6 files in `word/media/`.
- Red revision markers in final DOCX XML:
  - `RevisionRed`: 203 occurrences.
  - Direct red equation color `FF0000`: 46 occurrences.
- Nature-formatting metadata:
  - Continuous line numbering is present in `word/document.xml`.
  - Page margins are set to one inch.
  - Body/document default styles use Times New Roman-compatible 12 pt formatting.
  - The generated `Introduction` heading was removed; the abstract is followed directly by the opening paragraph.
- Raw failed-conversion strings: no `\textcolor`, `\frac`, or `eq:similarity` strings found in final `word/document.xml`.
- Citations: spot-checked as numeric superscript ranges in the DOCX XML/text extraction.
- Title block: spot-checked as title, authors with superscript `1`, and MIT affiliation before the abstract.

## Manual Check Still Needed

Before final MTS upload, open the DOCX in Microsoft Word and compare against:

`../00_READY_TO_SUBMIT_TEX_ROUTE_CHECK_PORTAL/02_Main_Manuscript_Revised_Compiled.pdf`

Spot-check:

- All display equations and inline math.
- The similarity equation near the start of Results.
- Citations and reference formatting.
- Figure placement and figure captions.
- Red revision coloring throughout.
