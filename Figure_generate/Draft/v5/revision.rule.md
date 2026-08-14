# Revision Rules for `v5`

This file defines the working rules for rebuttal-stage manuscript revision in `Figure_generate/Draft/v5`.

These rules are intended to be strong rules, not loose suggestions.

---

## Core Principle

`v5` is now a rebuttal-integrated draft.

That means every revision should be synchronized across:
- manuscript text in `latex/`
- reviewer response materials in `latex/revision_second_round/`
- revision-specific figures and provenance

No response should claim a manuscript change unless that change exists in the manuscript source.

---

## Strong Rules

### 1. Response letter must not get ahead of the manuscript

If the rebuttal says:
- "we have added"
- "we now show"
- "we revised the manuscript"

then the corresponding change must already exist in:
- `latex/sections/*.tex`, or
- `latex/supplementary_sections/*.tex`, or
- manuscript-facing figure/caption files

If the change is not yet integrated, the response must say so explicitly:
- "we performed this analysis and plan to integrate it"
- "this follow-up analysis is prepared but not yet incorporated"

Any such point must also be recorded as blocked in `latex/revision_second_round/second_review_action_tracker.md`, with a short blocker note identifying which manuscript file or section is pending, and the unresolved text in the letter must remain inside a `\draftresponse{...}` block so a final build cannot be produced by accident. Points may only be marked `done` after the corresponding manuscript/supplementary edit is actually applied, not merely planned.

### 2. All newly revised manuscript text should be marked by revision round

For first-round revision text already in the manuscript, use or preserve:
```tex
\rev{new or revised text here}
```

For second-round revision text, use:
```tex
\revsecond{new or revised text here}
```

The `\rev{}` and `\revsecond{}` commands are defined in:
- `latex/main.tex`
- `latex/supplementary.tex`

Rendering rule:
- `\rev{...}` renders first-round revision text in red.
- `\revsecond{...}` renders second-round revision text in blue in both `main.pdf` and `supplementary.pdf`.

This rule applies to:
- main text revisions
- supplementary text revisions
- new caption text added for rebuttal

Do not silently insert major revised text without the correct round-specific revision macro during the rebuttal stage.

### 3. Revision-only figures must be localized

Any figure used in the response letter should be copied into:
- `latex/revision_second_round/revision_figure_folder/`

Do not link the LaTeX response package directly to scattered figure paths in:
- `Figure_generate/code/Figure_revision/...`

This keeps the rebuttal package self-contained and auditable.

### 4. Every imported revision figure must be documented

Whenever a PDF is added to `latex/revision_second_round/revision_figure_folder/`, update:
- `latex/revision_second_round/revision_figure_folder/source.md`

Each entry should include:
- copied filename
- original source path
- generating script
- short scientific description

### 5. Every meaningful revision must be logged

Whenever I make a real change in `v5`, I should update:
- `revision_history.md`

The history must be organized by reviewer question whenever possible.

Each log entry should record:
- date
- affected reviewer point(s)
- files changed
- what changed
- whether the change is manuscript text, response text, figure import, or workflow infrastructure

### 6. Point-by-point memos remain the evidence layer

Before integrating new claims into the manuscript or response letter, check the relevant memo in:
- `latex/revision_second_round/point_by_point/...`

The memo is the evidence source for:
- what was analyzed
- what figures were generated
- what interpretation is justified

Do not overstate beyond the memo.

### 7. Use the LaTeX response package as the submission-facing source

For rebuttal writing, the primary files are:
- `latex/revision_second_round/response_letter.tex`
- `latex/revision_second_round/response/reviewer1_response.tex`
- `latex/revision_second_round/response/reviewer2_response.tex`
- `latex/revision_second_round/response/reviewer3_response.tex`

The Markdown response files are planning drafts only.

If Markdown and LaTeX disagree, the LaTeX files should be treated as the current submission-style version.

### 8. Keep reviewer-to-manuscript traceability explicit

For every major reviewer point, it should be possible to answer:
- Which figure supports the response?
- Which manuscript file was changed?
- Which supplementary file was changed?

If that mapping is unclear, the revision is not complete.

### 9. Prefer small, traceable manuscript edits over broad rewrites

During rebuttal integration:
- make targeted changes
- mark first-round changes with `\rev{}` and second-round changes with `\revsecond{}`
- log them in `revision_history.md`

Avoid large untracked rewrites that make reviewer mapping difficult.

### 10. Always preserve compileability

After substantial changes to:
- `latex/main.tex`
- `latex/supplementary.tex`
- `latex/revision_second_round/response_letter.tex`

run a compile check when practical.

The goal is that the rebuttal package and manuscript sources remain working documents, not half-broken drafts.

### 11. Response-letter style conventions

The response-letter style rules are defined in `latex/revision_second_round/response/README.md`. Every reviewer-response subsection must comply; the rules most often violated are summarized here for convenience:

- **Prose, not itemization (README rule 6).** No `\begin{itemize}`, `\begin{enumerate}`, `\paragraph{(a)/(b)}`, or bold paragraph-leads that act as numbered subclaims (`\textbf{(1) Does X predict Y?}`, `\textbf{Crucially, ...}`). Use connected paragraphs.
- **Bold sparingly (README rule 9).** Reserve `\textbf{}`/`\bm{}` for at most one key term per response inside running prose. Do not bold whole sentences, findings, statistics, or $p$-values for visual callouts. Figure panel labels in captions are exempt.
- **Highlight manuscript-bound text in blue (README rule 10).** Any exact wording that will be inserted into or substituted in the manuscript/supplementary is rendered in `\textcolor{blue}{...}`. This also makes it visually obvious which sentences carry the \texttt{Rule 1} promise and must be traceable into the manuscript source.
- **Status tracking (retired as an in-letter marker).** Earlier rounds required every response subsection to open with a `\statusline{<status>}{<confidence>}` marker rendered in red. This is **not** used in the second-round package, and the macro is not defined in `response_letter.tex`. An internal triage marker rendered inside the reviewer-facing PDF is the wrong place for it, and the marker was never adopted in practice. Per-point status is tracked instead in `latex/revision_second_round/second_review_action_tracker.md`, which is the authority for whether a point is `todo`, `check`, `done`, `in-progress`, `no-action`, or `defer-until-editorial-checklist`. Draft safety inside the letter is enforced separately by `\responsedrafttrue` and `\draftresponse{...}`, which raise a compile error if an unresolved block survives into a final build.
- **No em-dashes (README rule 8).** Do not use `---` in LaTeX or `—` in Markdown; use commas, parentheses, semicolons, colons, or new sentences.

If the LaTeX response file conflicts with README.md, README.md is canonical for style; this file is canonical for integration workflow.

### 12. Rebuttal terminology must match manuscript terminology, including figure labels

The terminology standards in `latex/writing_rules.md` apply to:
- manuscript text
- supplementary text
- response-letter prose and captions
- response-only figure labels
- response-figure generation code
- `latex/revision_second_round/revision_figure_folder/source.md`

The terminology checks most likely to be missed in the rebuttal package are:
- Use `parental community` / `parental communities` when referring to the two communities being coalesced. Do not use `parent` or `parents` as standalone nouns in author-written prose or captions. Reviewer-quoted text is exempt. **Figure labels are also exempt** (author decision, 2026-08-01): axis labels and legend entries inside artwork use the sentence-case short forms `Same parent` and `Cross parents`, because the full term wraps and drops the label under the 5 pt floor. A caption quoting such a label must reproduce it as drawn.
- Use `Mixture` for the outcome class. Do not use `Mixing` as the class label in author-written prose, captions, legends, stacked bars, figure annotations, or provenance descriptions. Reviewer-quoted text is exempt.

When a response figure is regenerated or imported, check both:
- the LaTeX caption in `latex/revision_second_round/response/reviewer*_response.tex`
- the generating script under `Figure_generate/code/Figure_revision/...`

If a figure label changes, regenerate the source PDF, copy it into `latex/revision_second_round/revision_figure_folder/`, update any manuscript-facing copy if the same PDF is reused in `latex/supplementary_figs/`, and update `source.md` if its description contains the old terminology.

---

## Practical Workflow

For each reviewer-driven change:

1. Confirm evidence in `point_by_point/.../memo.md`
2. Update manuscript text in `latex/...` using `\revsecond{}` for second-round changes
3. Update or import the supporting figure if needed
4. Check response terminology in both captions and figure-generation code, especially `parental community/communities` and `Mixture`
5. Update `revision_figure_folder/source.md` if a response figure is added or regenerated
6. Update the LaTeX rebuttal response, quoting manuscript-bound wording in `\mschange{}`
7. Update the point's status in `second_review_action_tracker.md` (`todo` $\to$ `check` $\to$ `done`, or back to `todo` if a manuscript edit is pending)
8. Log the change in `revision_history.md`

---

## Scope of This Rule File

This file governs rebuttal-stage work in:
- `/Figure_generate/Draft/v5/`

It is specifically meant to keep:
- manuscript edits
- response-letter edits
- figure imports
- revision logs

in sync.
