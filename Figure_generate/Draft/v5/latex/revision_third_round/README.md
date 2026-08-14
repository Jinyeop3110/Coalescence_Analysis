# Third-round revision workspace

Manuscript: **NATECOLEVOL-26010384A**

This directory tracks the Nature Ecology & Evolution author checklist and final
acceptance-stage requirements. It is an internal working directory. Files here
are not submission deliverables unless a file is explicitly identified as one.

## Authoritative manuscript locations

- Core working source: `../../latex/` (the parent directory of this workspace)
- Clean submission package: `../../revision_submission/00_submit_new/`
- Clean main source: `../../revision_submission/00_submit_new/Main_Manuscript_Revised_LaTeX_Source/`
- Clean Supplementary Information source: `../../revision_submission/00_submit_new/Supplementary_Information_LaTeX_Source/`

Edit the core source first, then apply the equivalent change to the appropriate
clean submission source without overwriting submission-specific differences.
After source changes, rebuild both affected documents and refresh the
submission-facing PDF and source ZIP.

## Current files

- `AUTHOR_CHECKLIST_TRACKER.md` — authoritative parse of the pasted checklist,
  with detailed action IDs, logical journal-row crosswalk, statuses, external
  deliverables, and response-writing rules.
- `HISTORY.md` — append-only record of third-round decisions, edits, packaging,
  and verification.
- `README.md` — this workflow and directory map.

## Add these directories only when populated

```text
revision_third_round/
├── source/       # untouched files received from the journal
├── responses/    # completed checklist, cover-letter summary, response files
└── audits/       # word-count, figure, statistics, rights, and package reports
```

Recommended source names:

- `source/author_checklist_original.docx`
- `source/marked_manuscript_original.docx` or `.pdf`
- `source/reporting_summary_original.pdf`
- `source/inventory_template_original.docx`

Recommended response and audit names:

- `responses/author_checklist_response.docx`
- `responses/cover_letter_summary.md`
- `audits/main_text_word_count.md`
- `audits/figure_and_statistics_audit.md`
- `audits/data_code_and_accession_audit.md`
- `audits/rights_and_biorender_audit.md`
- `audits/final_submission_inventory.md`

Do not place duplicate working copies of `main.tex`, `supplementary.tex`, figure
assets, or their section files here. Their canonical copies remain in the core
and submission trees above.

## Workflow for each checklist item

1. Locate the logical journal row (`JR-*`) and its detailed action IDs (`AC-*`).
2. Check the current core source, clean submission source, compiled PDF, figure
   artwork, analysis output, or external form as required.
3. Record any author decision before editing when scientific interpretation,
   authorship, funding, rights, data deposition, or study design is involved.
4. Make the smallest supported change in the core and submission trees.
5. Compile and inspect all affected PDFs; refresh submission ZIPs when their
   contents change.
6. Update the tracker status and draft a concrete journal response that states
   exactly what was checked or changed.
7. Append a dated entry to `HISTORY.md`, including files, decisions, validation,
   and any remaining external obligation.

## Status and evidence rules

- `Done` requires verification of the submission-facing artifact, not only a
  source edit.
- `Author confirmation` remains open until the author supplies or approves the
  information.
- `External` remains open until the repository, portal, Adobe PDF, or Word-form
  action has actually occurred.
- `Conditional` requires an explicit applicability decision; do not silently
  treat it as complete.
- Exact statistics must be traceable to authoritative data or analysis output.
- Do not invent accessions, DOIs, grant numbers, software versions, rights
  status, or coauthor confirmations.

## Round boundaries

Use this directory for the third-round author checklist and production-readiness
work. Reviewer-response material from earlier rounds remains in
`revision_first_round/` and `revision_second_round/`. The project-wide
`../../revision_history.md` may receive concise milestone summaries, but the
detailed authoritative log for this round is `HISTORY.md`.

