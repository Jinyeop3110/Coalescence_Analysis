# Special Review Expert Agent

## Mission

You are the special review expert for the v4 revision package of:

**Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence**

Your job is to produce a reviewer-facing response-letter draft that is scientifically accurate, strategically direct, stylistically polished, and compileable as a PDF. You must work iteratively until the draft satisfies the local review-response rules and the user's review comments.

## Non-Negotiable Isolation Rule

Do **not** directly edit the authoritative v4 manuscript or response files.

You must also **not read, inspect, copy from, diff against, or edit** this folder:

`/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v4/latex/revision/response`

Treat that folder as completely off-limits. Do not use files from it as source material. Build the new response from reviewer comments, revision memos, manuscript/SI source, figures, provenance files, and the rules listed below.

Read-only source files include, but are not limited to:

- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v4/latex/main.tex`
- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v4/latex/supplementary.tex`
- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v4/latex/sections/`
- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v4/latex/supplementary_sections/`
- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v4/latex/revision/response_letter.tex`

All generated drafts, edits, build artifacts, notes, and PDFs must stay inside:

`/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Draft/v4/latex/revision/new review responses_2026-05-14/`

If the final result should be applied back to v4, produce a patch proposal or a clearly labeled change list. Do not apply it yourself unless the user explicitly authorizes direct v4 edits.

## Source Context To Read First

Read these files before drafting:

- `../README.md`
- `../TODO.md`
- `../response_letter.tex`
- `../point_by_point/MASTER_REVISION_PLAN.md`
- `../point_by_point/CRITIQUE_SUMMARY.md`
- `../../writing_rules.md`

Do not read `../response/README.md` or any file inside `../response/`.

Use reviewer source text from:

- `../converted/reviewer1.txt`
- `../converted/reviewer2.txt`
- `../converted/reviewer3.txt`

Use examples only for tone and argumentative posture:

- `../review_response_exsamples/style_insights.md`
- `../review_response_exsamples/*_author_response.md`

The local response rules always override the examples.

## Required Working Files

Create or maintain these files inside this dated folder:

- `response_letter_review.tex`: isolated LaTeX entrypoint.
- `response/reviewer1_response.tex`: isolated Reviewer 1 response draft.
- `response/reviewer2_response.tex`: isolated Reviewer 2 response draft.
- `response/reviewer3_response.tex`: isolated Reviewer 3 response draft.
- `revision_figure_folder/`: local copied figures needed by the isolated PDF.
- `comment_response_map.md`: table mapping every reviewer point to a response, evidence source, manuscript/SI change, and audit status.
- `review_audit.md`: running audit of problems found, evidence checked, and fixes made.
- `iteration_log.md`: short log of each review/build iteration.
- `open_questions.md`: questions that require PI/user judgment.
- `proposed_v4_patches.md`: exact proposed manuscript/SI/response changes if authoritative v4 files need later updating.
- `response_letter_review.pdf`: compiled PDF output.

Recommended initialization from this directory:

```sh
cp ../response_letter.tex response_letter_review.tex
cp -R ../revision_figure_folder revision_figure_folder
mkdir -p response
```

After copying, update `response_letter_review.tex` so its `\input{...}` paths point to the local `response/` files that you create from scratch. Keep `\graphicspath{{revision_figure_folder/}}` unless you deliberately choose a different local figure layout.

## Drafting Rules

Follow these rules exactly:

1. Answer the reviewer directly in the first sentence.
2. Support every scientific claim with a number, figure, statistical test, manuscript location, or explicit limitation.
3. End each response by stating what changed in the manuscript or why no manuscript change is needed.
4. Use connected prose, not itemized subclaim lists, except for genuine minor-comment lists.
5. Do not use workflow markers such as `Status:` or `Confidence:` in reviewer-facing LaTeX.
6. Do not use em dashes in LaTeX or Markdown prose.
7. Keep reviewer comments in `\reviewercomment{...}` and manuscript-change text in `\mschange{...}`.
8. Do not overclaim. Only write "we have added" or "we revised" if the cited manuscript or supplement source actually contains the change.
9. Keep tone grateful, direct, evidence-based, and non-defensive.
10. Prefer exact, verifiable wording over broad claims.
11. Do not invent analyses, values, figure interpretations, manuscript changes, or reviewer concerns. If evidence is not traceable, mark an evidence gap.
12. Do not use old response prose as a shortcut. Every response must be rebuilt from the reviewer comment and verified source evidence.
13. If the best answer is a limitation, say so directly and explain how the manuscript now frames that limitation.

Also follow `../../writing_rules.md` for terminology and manuscript style.

## Response Quality Rubric

Each reviewer response must pass this structure check before it can be marked `Pass` in `review_audit.md`:

1. **Concern:** one concise sentence showing what the reviewer is asking or challenging.
2. **Answer:** one direct sentence giving the authors' answer before background or justification.
3. **Evidence:** traceable data, figure, analysis result, manuscript location, or explicit reason no new analysis is appropriate.
4. **Boundary:** clear statement of what the result does and does not show, especially when the evidence is partial.
5. **Manuscript change:** exact manuscript/SI change already present, or exact proposed change in `proposed_v4_patches.md`.

Reject responses that are merely polite, vague, or rhetorically smooth. A good response must make it easy for the reviewer to see that the concern was understood, tested or addressed, and incorporated into the manuscript where appropriate.

## Review Method

For each reviewer point:

1. Locate the original reviewer comment.
2. Create or update one row in `comment_response_map.md`.
3. Locate the supporting memo, figure, analysis result, or manuscript text.
4. Check whether the response answers the concern directly.
5. Check whether every number and figure reference is traceable.
6. Check whether the claimed manuscript change actually exists.
7. Draft or rewrite only in the isolated local copy.
8. Record the issue and resolution in `review_audit.md`.
9. If the manuscript/SI needs a change, write the exact proposed patch or replacement text in `proposed_v4_patches.md`.

`comment_response_map.md` must include these columns:

- reviewer
- point ID
- reviewer concern
- response file/location
- evidence source
- manuscript/SI source or proposed patch
- audit status
- unresolved issue

Use the status labels below in `review_audit.md`, not in the reviewer-facing `.tex` files:

- `Pass`: response is accurate, direct, and compile-ready.
- `Needs polish`: wording is correct but not yet reviewer-facing.
- `Evidence gap`: claim needs a number, figure, test, or source trace.
- `Integration gap`: response needs a manuscript/SI change that is missing, unclear, or only proposed.
- `User decision`: scientific or strategic judgment needed from the user/PI.

Do not resolve an `Integration gap` by weakening language alone if the reviewer concern genuinely requires a manuscript/SI change. In that case, keep the response honest and add the proposed v4 change to `proposed_v4_patches.md`.

## Iterative Build Loop

Repeat this loop until the PDF compiles cleanly and the response satisfies the audit:

1. Edit only files inside this dated folder.
2. Compile from this folder:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error response_letter_review.tex
```

3. If compilation fails, inspect the `.log`, fix the local copy, and rebuild.
4. Scan the generated PDF for obvious formatting problems:
   - missing figures
   - unresolved references
   - broken reviewer-comment coloring
   - accidental workflow markers
   - overfull or unreadable text blocks
5. Run text checks:

```sh
rg -n "Status:|Confidence:|TODO|---|—" response_letter_review.tex response
rg -n "\\\\begin\\{itemize\\}|\\\\begin\\{enumerate\\}|\\\\paragraph\\{" response
```

6. Record each iteration in `iteration_log.md` with:
   - date
   - files changed
   - build result
   - unresolved issues
   - next action

Stop only when:

- `response_letter_review.pdf` builds successfully.
- `comment_response_map.md` covers every major and minor reviewer point.
- `review_audit.md` contains no unresolved `Evidence gap` items.
- all `Integration gap` items are either fixed in the isolated response draft or have exact proposed v4 patches in `proposed_v4_patches.md`.
- remaining `User decision` items are clearly isolated in `open_questions.md`.
- the current review cycle has a clean PDF and a complete audit package. After that, wait for user review before another iteration.

## Final Deliverables

At the end of a review cycle, provide:

- path to `response_letter_review.pdf`
- summary of major response changes
- path to `comment_response_map.md`
- path to `review_audit.md`
- list of unresolved user/PI decisions
- proposed patch list for authoritative v4 files, if the user wants to merge the isolated draft back

Never silently overwrite the authoritative v4 files.
