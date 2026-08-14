# Second-Round Response Package

The files in this directory are the reviewer-specific sources included by
`../response_letter.tex`.

## Files

- `reviewer1_response.tex`: Reviewer 1 minor comments and code-availability response.
- `reviewer2_response.tex`: Reviewer 2 conceptual clarification about Dominance, origin-correlated persistence, and prior assembly.
- `reviewer3_response.tex`: acknowledgement of Reviewer 3's approval.

## Draft safety

`../response_letter.tex` currently has `\responsedrafttrue`. In this mode, the
compiled document displays a prominent working-draft banner and unresolved
`\draftresponse{...}` blocks appear as gray drafting notes.

Before generating a reviewer-facing PDF:

1. Replace every `\draftresponse{...}` block with a complete author response.
2. Confirm that every claimed manuscript change exists in the active main or supplementary source.
3. Quote exact second-round manuscript wording with `\mschange{...}`.
4. Change `\responsedrafttrue` to `\responsedraftfalse`.
5. Compile from `latex/revision_second_round/` and inspect the resulting PDF.
6. Confirm that no draft banner, drafting note, TODO, or placeholder remains.

## Style

- Answer the reviewer directly in the first sentence.
- Use a concise thank, acknowledge, answer, evidence, manuscript-change structure.
- Keep author responses in connected prose rather than itemized mini-rebuttals.
- Reviewer comments use `\reviewercomment{...}`.
- Exact manuscript-bound wording uses `\mschange{...}` and must match the active source.
- Do not use em dashes in author-written prose.
- Use `Dominance`, `Mixture`, and `Restructuring` consistently.
- Distinguish Dominance as a compositional signature from the broader interpretation of community-level selection.
- Do not add response-only figures directly from scattered analysis paths. Copy them into `../revision_figure_folder/` and document them in its `source.md`.

The project-level rules in `../../../revision.rule.md`,
`../../../response_tailoring_policy.md`, and `../../writing_rules.md` remain
authoritative.
