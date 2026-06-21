LaTeX source bundle for revised submission
Prepared: 2026-06-17

Main manuscript:
- Source entry point: main.tex
- Compiled reference PDF: Main_revised_compiled.pdf
- Compile command: latexmk -pdf main.tex

Supplementary Information:
- Source entry point: supplementary.tex
- Compiled reference PDF: Supplementary_Information_revised_compiled.pdf
- Compile command: latexmk -pdf supplementary.tex

Response to reviewers/editor:
- Source entry point: revision/response_letter.tex
- Compiled reference PDF: Response_to_Reviewers_and_Editor.pdf
- Compile command from this folder: cd revision && latexmk -pdf response_letter.tex

Other included submission files:
- Reporting_Summary_Revised.pdf

Bibliography:
- references.bib is included.
- main.bbl, supplementary.bbl, and revision/response_letter.bbl are included.
- naturemag.bst is included in this folder for portability.

Notes:
- The manuscript source uses subdirectories for sections and figures.
- Compiled PDFs are included as reference outputs.
- This TeX bundle is intended as the LaTeX-route submission package because Word conversion was not sufficiently faithful.
