# Third-round revision history

This is the append-only detailed history for the third-round Nature Ecology &
Evolution author checklist for manuscript **NATECOLEVOL-26010384A**.

Each new entry should include:

- date and checklist/action IDs;
- author or editor decision;
- files changed in the core and submission trees;
- compiled or packaged artifacts refreshed;
- verification performed;
- remaining author or external obligations.

Do not rewrite earlier decisions when they are superseded. Add a new entry that
identifies the earlier entry and explains the replacement decision.

---

## 2026-08-14 — Third-round workspace initialized and checklist parsed

- **Scope:** Editor author checklist for manuscript NATECOLEVOL-26010384A.
- Created `revision_third_round/` because no third-round directory or original
  checklist file was present in the tree.
- Parsed the author-supplied checklist into `AUTHOR_CHECKLIST_TRACKER.md`.
- Preserved the editor's proposed title and abstract verbatim.
- Created 50 detailed action IDs (`AC-01`–`AC-50`), nine upload items
  (`UP-01`–`UP-09`), and a crosswalk covering 36 logical guidance blocks
  (`JR-01`–`JR-36`).
- Added AC-50 during the completeness review for the opening instruction to
  inspect any additional editor-marked manuscript edits; this instruction was
  missing as a discrete action in the first parse.
- Clarified that exact Word-table row boundaries cannot be certified from the
  pasted plain text. The original checklist `.docx` is still needed before the
  response table is finalized.
- Verified that the supplied final-artwork PDF and dynamic Reporting Summary
  PDF endpoints are active. The linked `.docx` endpoints identify Word files,
  although they cannot be content-parsed by the web checker. Legacy Nature
  policy URLs redirect to current Nature Portfolio policy pages.
- **Manuscript edits:** none for this initialization entry.
- **Outstanding source materials:** original checklist `.docx`, any marked-up
  manuscript supplied by the editor, current Reporting Summary smart PDF, and
  Inventory of Supporting Information template/completed file.

## 2026-08-14 — Supplementary Fig. 22 threshold wording standardized

- **Related scope:** Supplementary Figure statistical-reporting checklist.
- **Author decisions:** Supplementary Fig. 13 accepted unchanged;
  Supplementary Figs. 24–26 accepted unchanged; Supplementary Figs. 30–31
  accepted unchanged. Supplementary Fig. 22 should report the common threshold
  rather than six individual numerical values.
- Changed the Supplementary Fig. 22 caption from `all $p<10^{-6}$` to
  `all $p<0.001$` in:
  - `latex/supplementary_sections/figures.tex`
  - `revision_submission/00_submit_new/Supplementary_Information_LaTeX_Source/supplementary_sections/figures.tex`
- Rebuilt both Supplementary Information sources successfully at 64 pages.
- Refreshed:
  - `revision_submission/00_submit_new/Supplementary_Information.pdf`
  - `revision_submission/00_submit_new/Supplementary_Information_LaTeX_Source.zip`
- Verified the packaged source and submission-facing PDF both contain
  `all p < 0.001`; the top-level PDF and the clean source PDF are byte-identical.

## 2026-08-14 — Two-pass completion audit

- Located and checked the original author-checklist `.docx` in
  `revision_submission/00_submit_new/`; this supersedes the initialization
  entry's statement that the original checklist was still needed.
- Marked the following detailed actions **Done** after a second check of the
  core source, clean submission source, and compiled submission PDFs where
  applicable: AC-01, AC-04, AC-05, AC-07, AC-08, AC-10, AC-14, and AC-38.
- Updated `response.md` only for the corresponding seven complete journal rows:
  JR-01, JR-04, JR-06, JR-07, JR-09, JR-12, and JR-27.
- The remaining actions stay open, conditional, external, or pending author
  confirmation; no response text has been added for them.

## 2026-08-14 — Parse audit (5 parallel agents) and status corrections

- **Scope:** Verified `AUTHOR_CHECKLIST_TRACKER.md`'s parsed requirements and
  statuses against the original checklist docx located in
  `revision_submission/00_submit_new/`, split across five independent audits
  (Sections A–D, E, F–G, H–J, K–L plus the upload list).
- Confirmed AC-01 (title) and AC-02 (abstract) required text matches the source
  verbatim, and that every figure/panel citation in Section E (AC-11–AC-21)
  matches the source character-for-character.
- Corrected two status misclassifications found by the audit:
  - **AC-33**: changed `Open` → `Conditional` (bar-chart data-point overlay
    only applies where a Supplementary Figure uses a bar chart; this now
    matches the conditional treatment already given to sibling item AC-37 from
    the same five-part source list).
  - **AC-30**: changed `Conditional` → `Open` (the Methods materials-reuse
    statement is required unconditionally in the source; only the sharing-
    contact sub-clause is conditional, which is now reflected in the parsed
    requirement text rather than the top-level status).
- **Author decision on AC-02:** the manuscript abstract (identical in
  `latex/sections/title_abstract.tex` and
  `revision_submission/00_submit_new/Main_Manuscript_Revised_LaTeX_Source/sections/title_abstract.tex`)
  keeps two wording choices that diverge from the editor's proposed text:
  "modeling" (US spelling) instead of "modelling", and "dominance of one
  parental community" instead of "single-community dominance" (a deliberate
  second-round edit, marked `\rev{}` in the source). Author confirmed both are
  acceptable as-is. Marked AC-02 **Done** on this basis; no manuscript edit was
  made.
- Minor wording-fidelity issues noted by the audit but left unresolved pending
  author direction: AC-05's "numerical order" is not stated in the source
  (only "in order"); AC-10's quoted example says "Supplementary Fig. 3" where
  the source says "Supplementary Figure 3"; AC-03 drops the source's "could
  delay the production of your paper" consequence clause; AC-24 strengthens
  "should" (source) to "must"; AC-26 shifts "the statement must comply" to
  "the dataset must comply"; UP-03 is labeled `Open` while UP-07/UP-09 (similar
  form-style deliverables) are labeled `External`.
- **Manuscript edits:** none (AC-02's text was already in place; only tracker
  status/text updated).
