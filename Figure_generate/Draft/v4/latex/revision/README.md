# Revision Workspace

**Paper:** Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence

This folder is the working area for revision planning, reviewer-response drafting, and revision-specific figures. It now supports both:
- lightweight drafting in Markdown
- a compileable LaTeX response-letter package for submission-style rebuttal writing

The LaTeX package should be treated as the primary response-letter target going forward.

---

## Purpose

This `revision/` directory is meant to do four related jobs:

1. Track reviewer comments and PI discussion notes.
2. Organize point-by-point analysis tasks and memo summaries.
3. Collect revision-only figures generated outside the main manuscript figure folders.
4. Assemble a formal response letter in LaTeX.

In other words, this is not just a notes folder. It is the revision-management layer that connects reviewer comments, analysis outputs, manuscript changes, and response-letter drafting.

---

## Directory Structure

```text
revision/
├── README.md
├── Discussion_0416.md
├── response_letter.tex
├── response_letter.pdf
├── revision_figure_folder/
│   ├── *.pdf
│   └── source.md
├── response/
│   ├── reviewer1_response.tex
│   ├── reviewer2_response.tex
│   └── reviewer3_response.tex
├── point_by_point/
│   ├── MASTER_REVISION_PLAN.md
│   ├── CRITIQUE_SUMMARY.md
│   ├── P1_text_fixes/
│   ├── P2_figure_fixes/
│   ├── P3_reanalysis/
│   ├── P4_new_simulations/
│   ├── P5_manuscript_integration/
│   └── P6_response_letter/
├── converted/
├── raw/
└── deprecated/
```

---

## Key Files

### `response_letter.tex`

This is the main compileable response-letter entrypoint.

- It pulls in the reviewer-specific LaTeX sections from `response/`.
- It uses figures stored locally in `revision_figure_folder/`.
- It should be the file you compile when building the current response draft.

If the rebuttal is being prepared for circulation or submission, this is the file to update.

### `response/`

This folder contains the submission-style LaTeX reviewer responses.

#### LaTeX files
- `reviewer1_response.tex`
- `reviewer2_response.tex`
- `reviewer3_response.tex`

These are the reviewer sections actually used by `response_letter.tex`.

They should contain:
- the quoted reviewer comment
- the polished prose response
- any embedded revision figures
- careful distinctions between completed analyses and still-pending follow-up work

The Markdown planning drafts (`reviewer{1,2,3}_response.md`) were moved to `deprecated/2026-04-21_md_cleanup/` on 2026-04-21 once the LaTeX versions became authoritative.

### `revision_figure_folder/`

This folder contains the local copy of all revision-response figures used in the rebuttal package.

This folder exists for two reasons:

1. **Self-containment**
   The response letter should not depend on scattered figure paths across `Figure_generate/code/Figure_revision/...`.

2. **Auditability**
   A reviewer-facing figure used in the response should be easy to locate, inspect, and map back to its generating script.

#### What belongs here
- Revision-only PDFs copied from `Figure_generate/code/Figure_revision/...`
- Only figures intended for the rebuttal letter or revision discussion
- Not the main manuscript figures unless they are specifically being cited as revision evidence

#### `source.md`

The file `revision_figure_folder/source.md` is the provenance map for this folder.

It should document, for each imported response figure:
- the copied filename in `revision_figure_folder/`
- the original source path
- the generating script
- a short description of what the figure shows

This file should be updated whenever new revision figures are copied in.

---

## Point-by-Point Workflow

### `point_by_point/`

This is the revision task-management structure.

It organizes the work into phases:
- `P1_text_fixes`
- `P2_figure_fixes`
- `P3_reanalysis`
- `P4_new_simulations`
- `P5_manuscript_integration`
- `P6_response_letter`

Each analysis folder usually contains a `memo.md` summarizing:
- the reviewer concern
- what was done
- the key results
- generated figures
- suggested manuscript changes

### `MASTER_REVISION_PLAN.md`

This is the high-level task board.

Use it to track:
- what is complete
- what is pending
- what newly proposed analyses have been added

### `CRITIQUE_SUMMARY.md`

This is the audit / quality-control summary for the revision analyses and scripts.

Use it to record:
- fixes applied
- remaining concerns
- recommendations for response-letter framing

---

## Recommended Working Model

### 1. Plan in Markdown, deliver in LaTeX

Use the Markdown files for brainstorming and TODO capture.
Use the LaTeX files for the actual rebuttal letter.

That means:
- `.md` files are flexible planning notes
- `.tex` files are reviewer-facing draft text

### 2. Keep figures local to the rebuttal package

When a revision analysis produces a figure that should appear in the response letter:

1. Generate it in `Figure_generate/code/Figure_revision/...`
2. Copy the PDF into `revision_figure_folder/`
3. Add an entry to `revision_figure_folder/source.md`
4. Insert it into the relevant `reviewerN_response.tex`

This keeps the rebuttal package stable and portable.

### 3. Do not overclaim completion

In the LaTeX responses:
- only say “we have added” if the manuscript source actually contains the change
- only say “we performed” if the analysis and figure really exist
- if an item is planned but not integrated, say so explicitly

This is especially important because the revision package can get ahead of the manuscript source if the response letter is drafted before all `.tex` manuscript edits are merged.

---

## Updating the Response Letter

### When a new analysis is completed

1. Update the relevant `point_by_point/.../memo.md`
2. Copy the resulting PDF into `revision_figure_folder/`
3. Add the provenance entry to `revision_figure_folder/source.md`
4. Update the relevant `reviewerN_response.tex`
5. Recompile `response_letter.tex`

### When the manuscript text is revised

1. Update the manuscript `.tex` files in `latex/sections/` or `latex/supplementary_sections/`
2. If the response letter mentions the change, make sure the wording matches reality
3. Prefer citing section names or exact file/line references when doing a final polish pass

### When PI discussion changes the plan

1. Add or update a `Discussion_MMDD.md` note
2. Reflect any new tasks in `MASTER_REVISION_PLAN.md`
3. Add new `point_by_point` memo folders if needed

---

## Current Status Summary

### Already present
- Compileable LaTeX response-letter package
- Local revision-figure folder with imported PDFs
- Figure provenance map in `revision_figure_folder/source.md`
- Point-by-point memo structure for completed and planned analyses

### Still requires care
- Some response prose may get ahead of manuscript integration
- Figure captions in the rebuttal should stay explicit about which panel or statistic supports the claim
- Markdown drafts may lag behind the LaTeX versions

---

## Practical Rule

If you are unsure where to edit:

- edit `response_letter.tex` or `response/reviewerN_response.tex` if the goal is the rebuttal letter
- edit `revision_figure_folder/source.md` if you added a new response figure
- edit `point_by_point/.../memo.md` if you completed or revised an analysis
- edit `MASTER_REVISION_PLAN.md` if the overall revision scope changed

If the goal is submission-ready reviewer response, start from the LaTeX package, not the Markdown files.
