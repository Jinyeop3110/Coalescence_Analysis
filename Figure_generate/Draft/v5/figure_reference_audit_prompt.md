# Prompt: Figure, Reference, and Submission Audit for v5

You are auditing a LaTeX manuscript revision for internal consistency before submission. Work in:

`/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v5/latex`

Primary files:

- Main manuscript: `main.tex` plus `sections/*.tex`
- Supplementary information: `supplementary.tex` plus `supplementary_sections/*.tex`
- Bibliography: `references.bib`
- Figure assets: `figures/`, `figures/extended_data/`, and `supplementary_figs/`

Treat `main.tex` and `supplementary.tex` as separate compiled documents unless a specific submission workflow requires merging them. Both define `\graphicspath{{figures/}}`, so figure paths may resolve either relative to `latex/` or through `latex/figures/`.

## Scope

Check the draft for figure-reference, citation-reference, and submission-readiness issues. Do not rewrite prose unless a specific inconsistency requires a minimal proposed fix. Ignore archive, backup, deprecated, and revision-planning folders unless the active source imports them.

## Required Checks

1. Compile/reference health
   - Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex supplementary.tex`.
   - Inspect `main.log` and `supplementary.log` for undefined references, undefined citations, multiply defined labels, missing files, overfull boxes that affect captions/tables, and package warnings relevant to output correctness.
   - If the build is already up to date, still inspect the current logs and source.

2. Label and reference integrity
   - Build an inventory of all `\label{...}` entries in active source files.
   - Build an inventory of all `\ref{...}`, `\figref{...}`, `\tabref{...}`, `\eqnref{...}`, `\secref{...}`, `\autoref{...}`, `\cref{...}`, and `\Cref{...}` uses.
   - Verify every used label exists.
   - Flag duplicate labels within each compiled document. Also flag labels duplicated across main and supplement if they could become ambiguous in a merged submission bundle.
   - Do not count macro definitions such as `\newcommand{\figref}[1]{Fig.~\ref{#1}}` as real references.

3. Figure file integrity
   - Verify every `\includegraphics{...}` target exists, accounting for `\graphicspath{{figures/}}` and common extensions such as `.pdf`, `.png`, `.jpg`, and `.jpeg`.
   - Flag active figure files that appear mismatched to their caption or figure number.
   - Flag references to backup, obsolete, internal, or reviewer-only figure assets if they appear in active source.

4. Figure numbering and first-use order
   - Main manuscript should have main figures labeled and captioned as Fig. 1 through Fig. 6.
   - Supplementary active source should have Extended Data Fig. 1 through Extended Data Fig. 8 and Supplementary Fig. 1 through Supplementary Fig. 46.
   - Check that text references to main figures, Extended Data figures, and Supplementary figures point to existing active figures.
   - Check whether figures are first mentioned in a logical order. Flag serious out-of-order references where a reader encounters a later figure before the key earlier figure without reason.
   - Check manual references like `Fig.~1c`, `Extended Data Fig.~5a--d`, and `Supplementary Figs.~10--12` against captions and panel lettering.

5. Caption-to-panel consistency
   - For each active figure, compare caption panel calls (`a`, `b`, `c`, etc.) with the visual figure if possible using `main.pdf`, `supplementary.pdf`, and source PDFs.
   - Flag captions that mention panels not visible in the figure, missing panel letters, incorrect panel order, inconsistent capitalization, or panel references in text that are not described in captions.

6. Citation and bibliography integrity
   - Inventory all `\citep{...}`, `\citet{...}`, and related citation commands in active source.
   - Verify every cited key exists in `references.bib`.
   - Verify no active bibliography entry is malformed.
   - If possible, check DOI metadata for cited papers and flag mismatches in title, year, journal, volume, issue, pages, or first author.
   - Flag preprints that may now have peer-reviewed versions if the manuscript is being submitted as final.

7. Submission-readiness markers
   - Search active source for `TODO`, `FIXME`, `TBD`, `XXX`, `LINK_NOT_FOR_PUBLICATION`, `\todo{...}`, `\jynote{...}`, `\jy{...}`, `\rev{...}`, and `\rollback{...}`.
   - Flag visible revision markup such as `\rev{...}` if the submission PDF should be clean rather than marked-up.
   - Flag line numbering or color markup if journal submission requires a clean version.
   - Flag private review-response language, internal notes, placeholders, or non-public URLs in active source.

8. Cross-document consistency
   - Check that claims in figure captions match the Results, Methods, and Supplementary Notes, especially sample sizes, media names (`Nutr-`, `Base`, `Nutr+`), thresholds, test names, p-values, and figure panel interpretations.
   - Check that main-text references to supplementary material use the same figure numbers and terminology as the supplementary captions.
   - Check that Extended Data figure order and Supplementary figure order match the evidence trail described near the top of `supplementary.tex`.

## Output Format

Return findings first, sorted by severity:

`Severity - file:line - issue - why it matters - proposed minimal fix`

Use these severity levels:

- Critical: breaks build, missing figure/citation/reference, or wrong figure number.
- Major: likely submission or reader-facing error, including incorrect caption/panel mapping or stale placeholder.
- Minor: style, clarity, ordering, or cleanup issue that does not affect correctness.

After findings, include:

- Clean checks: a short list of checks that passed.
- Figure inventory: counts and active labels for main figures, Extended Data figures, and Supplementary figures.
- Build status: whether `main.pdf` and `supplementary.pdf` compile cleanly.
- Residual risks: any checks that require human visual inspection or source data verification.

Do not make silent edits. If proposing edits, give exact file and line references and the smallest patch needed.
