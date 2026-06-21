# Response Tailoring Policy for `v4`

**Paper:** Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence  
**Stage:** rebuttal/revision response tailoring  
**Working directory:** `Figure_generate/Draft/v4/`  
**Primary response source:** `latex/revision/response_letter.tex`

This policy governs LLM-agent edits during the next response-tailoring iteration. It is modeled on a camera-ready editing policy structure, but adapted for this manuscript's rebuttal workflow: reviewer responses, manuscript/supplement synchronization, revision figures, and evidence traceability.

## 1. Scope

The next response-tailoring iteration starts from the current `v4` LaTeX source and may incorporate only:

1. reviewer concerns from `latex/review_round_1.md`, `latex/review_round_2.md`, and the quoted comments in `latex/revision/response/*.tex`;
2. commitments already made in the response letter or revision history;
3. evidence from completed analyses, point-by-point memos, figures, scripts, or verified manuscript text;
4. clear presentation improvements needed to make the response letter, manuscript, supplement, and figure captions internally consistent.

Do not add new scientific claims, new analyses, new figures, or broad manuscript rewrites unless they directly answer a reviewer concern, correct a factual problem, or resolve an inconsistency created by the rebuttal.

Minimal-change rule: preserve the current `v4` revision shape as much as possible. Prefer local response edits over restructuring, concise clarifications over new paragraphs, and supplementary routing over main-text expansion when the issue does not require main-text treatment.

Any optional edit that is not directly tied to a reviewer concern, response commitment, factual correction, or consistency problem must be justified in `revision_history.md` before or during the edit session.

## 2. Required Change Tracking

Every meaningful response-tailoring change must be logged in `revision_history.md`.

Every substantive manuscript or supplementary text change should be wrapped in `\rev{...}` while the rebuttal revision is under review. The `\rev{}` macro is defined in both `latex/main.tex` and `latex/supplementary.tex`.

Every exact manuscript-bound passage quoted inside the response letter should be wrapped in `\mschange{...}` according to `latex/revision/response/README.md`.

Pure deletions, figure replacements, bibliography changes, label/key renames, and formatting-only fixes cannot always be wrapped. They must still be logged.

For each change batch, record:

- date;
- affected reviewer point(s);
- files changed;
- source/reason;
- justification under the minimal-change rule;
- exact content summary;
- whether the change is response text, manuscript text, supplementary text, figure/provenance, analysis/code, or workflow infrastructure;
- verification status;
- remaining risk or follow-up.

Update the history in the same work session as the edit. If an edit is later revised or reverted, add a new history entry rather than silently changing the old one.

## 3. Evidence Standard

All scientific claims in the response letter, manuscript, and supplement must be grounded in one of these sources:

- active manuscript source in `latex/sections/` and `latex/supplementary_sections/`;
- active LaTeX response source in `latex/revision/response/*.tex`;
- point-by-point memos in `latex/revision/point_by_point/`;
- figure provenance in `latex/revision/revision_figure_folder/source.md` and `latex/supplementary_figs/file_source.md`;
- analysis scripts and outputs under `Figure_generate/code/Figure_revision/`;
- original processed data or verified analysis outputs when a number is not already summarized in a memo;
- explicit author guidance supplied in the conversation.

Source-of-truth priority when documents conflict:

1. raw data, verified scripts, or regenerated figure outputs;
2. point-by-point memo results and figure provenance;
3. active manuscript and supplementary LaTeX source;
4. active response-letter LaTeX source;
5. `revision_history.md`;
6. older Markdown drafts, deprecated response files, archived notes, or examples.

If two high-priority sources conflict, stop and record the conflict in `revision_history.md` before choosing wording.

Do not report a number, statistical test, figure result, or mechanistic interpretation from memory. Verify it in the relevant memo, figure, script, or source file.

## 4. Response Commitments To Honor

The response letter must not get ahead of the manuscript or supplement.

If a response says:

- "we have added";
- "we now show";
- "we revised";
- "we clarified";
- "the manuscript now";
- "Supplementary Fig.";

then the corresponding manuscript, supplementary, figure, caption, or provenance change must already exist in the active source.

If the change is only planned, the response must say so explicitly. Do not imply a completed manuscript change before it exists.

For every major reviewer point, it should be possible to answer:

- What reviewer concern is being answered?
- What evidence supports the answer?
- Which figure, table, or analysis file supports the answer?
- Which manuscript or supplementary file changed?
- Does the response quote the exact inserted wording with `\mschange{...}` when appropriate?

If this mapping is unclear, the response-tailoring task is not complete.

## 5. Response-Letter Style Gates

The canonical response-letter style rules are in `latex/revision/response/README.md`. This policy follows that file when there is any conflict.

Apply these gates to every response subsection:

- Answer the reviewer directly in the first sentence after the acknowledgement.
- Use evidence: numbers, figures, statistical tests, or explicit manuscript changes.
- Keep a non-defensive tone: thank, acknowledge, answer, evidence, manuscript change.
- Use connected prose, not itemized mini-rebuttals, except for genuine lists of minor independent fixes.
- Avoid em-dashes in author-written response prose. Use commas, parentheses, semicolons, colons, or new sentences.
- Use bold sparingly, at most one key term per response in running prose.
- Use `\reviewercomment{...}` for reviewer comments and normal black prose for author responses.
- Use `\mschange{...}` for exact manuscript-bound wording quoted in the response.
- Do not include workflow-only status or confidence markers in reviewer-facing compiled files.

Response examples in `latex/revision/review_response_exsamples/` are style references only. They are not evidence sources for this paper.

## 6. Manuscript And Supplement Synchronization

Response tailoring must check both main and supplementary source when the issue touches terminology, figures, statistics, or claims.

Main manuscript source:

- `latex/main.tex`
- `latex/sections/*.tex`

Supplementary source:

- `latex/supplementary.tex`
- `latex/supplementary_sections/*.tex`

Response source:

- `latex/revision/response_letter.tex`
- `latex/revision/response/reviewer1_response.tex`
- `latex/revision/response/reviewer2_response.tex`
- `latex/revision/response/reviewer3_response.tex`

Terminology standards in `latex/writing_rules.md` apply across manuscript, supplement, response prose, response captions, figure labels, and provenance files.

High-risk terminology checks:

- `CLS`, `Mixture`, `Restructuring`;
- `Base medium`, `Nutr$-$`, `Nutr$+$`;
- `community-level selection`;
- `top-down regime`, `emergent regime`;
- `parental community` / `parental communities`;
- `post-coalescence community` or `coalesced community`;
- `resource-consumer` theory/models;
- `30-fold serial dilution` or explicit `$\times$30 every 24~h` wording.

Reviewer-quoted text is exempt from terminology normalization unless the quote is being paraphrased by the authors.

## 7. Figure And Analysis Boundaries

Revision-only figures used in the response letter must be stored in:

- `latex/revision/revision_figure_folder/`

Every imported or regenerated response figure must have provenance in:

- `latex/revision/revision_figure_folder/source.md`

If the same or related figure appears in the supplement, also update:

- `latex/supplementary_figs/file_source.md`;
- the relevant caption in `latex/supplementary_sections/figures.tex` or other supplementary section files.

Do not link the response letter to scattered analysis-output paths. Keep the response package self-contained.

If a figure label or terminology changes, check:

- the generating script;
- the copied PDF;
- response caption;
- supplementary caption, if applicable;
- source/provenance Markdown.

## 8. Verification Policy

After each substantive response-tailoring batch:

1. compile the response letter from `latex/revision/`;
2. compile the main manuscript from `latex/`;
3. compile the supplement from `latex/` when supplementary files changed;
4. inspect compile errors and important warnings;
5. inspect diffs or targeted file changes for accidental broad rewrites;
6. run targeted text checks for stale terminology, Unicode punctuation, TODO-like markers, anonymous planning text, and unwrapped major manuscript insertions;
7. verify that response claims map to manuscript/supplement/figure source;
8. update `revision_history.md` with verification results.

Recommended commands, adjusted as needed for the local TeX setup:

```sh
cd latex/revision && latexmk -pdf -interaction=nonstopmode response_letter.tex
cd latex && latexmk -pdf -interaction=nonstopmode main.tex
cd latex && latexmk -pdf -interaction=nonstopmode supplementary.tex
grep -R -n "TODO\\|NEEDS\\|Status:\\|Confidence:" latex/sections latex/supplementary_sections latex/revision/response
grep -R -n "—\\|–\\|‘\\|’\\|“\\|”" latex/sections latex/supplementary_sections latex/revision/response
grep -R -n "Mixing\\|parent communities\\|parent community\\|consumer-resource" latex/sections latex/supplementary_sections latex/revision/response
```

If a build cannot run because of local tool problems or missing files, log that explicitly in `revision_history.md`.

## 9. External Review Pass

For large or high-risk response-tailoring batches, request a read-only external-review pass from a separate reviewer agent before marking the batch complete.

The reviewer should inspect the actual changed files plus nearby context and check:

- whether the response directly addresses the intended reviewer concern;
- whether all claims are supported by evidence;
- whether manuscript-bound response promises are actually integrated;
- whether terminology is consistent across main text, supplement, response, captions, and provenance;
- whether the response is too defensive, too expansive, or too vague;
- whether `\rev{}` and `\mschange{}` are used correctly;
- whether any optional edit violates the minimal-change rule.

The main editing agent must not treat the external review as automatically correct. Each actionable finding should be accepted, revised, or explicitly deferred, and the resolution should be logged.

## 10. Human-Approval Policy

LLM-agent edits may prepare a polished response-tailoring draft, but the following require author confirmation before final submission:

- final reviewer-response tone and strategic framing;
- any new claim not already present in a memo, figure, script, or manuscript source;
- whether to include new analyses in the main text, supplement, response-only figures, or not at all;
- any deletion of a response point that was previously promised;
- final decision to remove, neutralize, or keep visible `\rev{}` markings;
- final submitted PDFs and cover/response-letter package.

Do not mark the response package submission-ready until:

- response, main manuscript, and supplement compile when applicable;
- response claims match actual manuscript/supplement/figure source;
- `revision_history.md` is current;
- no workflow-only status markers remain in reviewer-facing compiled files;
- unresolved high-risk conflicts are either fixed or explicitly deferred by the author.

## 11. Practical Agent Workflow

For each reviewer-driven tailoring task:

1. identify the reviewer point and current response subsection;
2. check the relevant point-by-point memo, figure provenance, and active manuscript/supplement source;
3. decide whether the task is response-only, manuscript-only, supplement-only, figure/provenance, or cross-document;
4. make the smallest adequate edit;
5. wrap substantive manuscript/supplement changes in `\rev{...}`;
6. wrap exact manuscript-bound response quotes in `\mschange{...}`;
7. synchronize terminology and figure references across all touched files;
8. compile the relevant LaTeX targets;
9. run targeted consistency checks;
10. update `revision_history.md`;
11. summarize remaining risks or required author decisions.

This workflow is intended to keep the next response-tailoring pass auditable: every reviewer answer should connect to evidence, every manuscript promise should exist in source, and every substantive edit should be recoverable from the revision history.
