# Response Letter: Criteria & Priorities

## Rules (apply to every response)

1. **Accuracy.** Numbers must match the analysis scripts and figures exactly. If a result is mixed, report both sides.
2. **Directness.** Answer the reviewer's question in the first sentence. No motivational framing ("To address this, we performed...").
3. **Evidence.** Every claim is backed by a number, figure, or statistical test. No "we believe..." without data.
4. **Manuscript integration.** Every response ends by stating what changed in the manuscript: a figure added, a sentence revised (quoted), or a clear justification for no change.
5. **Tone.** Thank, acknowledge, answer, evidence, manuscript change, in that order. Never defensive.
6. **Prose, not itemization.** Use connected paragraphs; avoid `\paragraph{(a)/(b)/(c)}`, numbered subclaims, `\begin{enumerate}`, or `\begin{itemize}` inside a single response. Bold paragraph-leads that function as numbered subclaims (e.g., `\textbf{(1) Does X predict Y?}`, `\textbf{First, ...}`, `\textbf{Crucially, ...}`) are also prohibited, since they are subclaims with a different shape. Exception: genuine lists of distinct minor items, and figure-panel labels inside captions.
7. **Conciseness.** Keep each response at or below its tier cap (see below). If over, compress before adding evidence. Prefer inline parenthetical statistics over separate explanatory sentences.
8. **No em-dashes.** Do not use `---` in LaTeX or `—` in Markdown prose. Use commas, parentheses, semicolons, colons, or new sentences.
9. **Bold sparingly.** Reserve `\textbf{}` and `\bm{}` for emphasizing at most one key term per response inside running prose. Do not bold whole sentences, key findings, statistics, or $p$-values for visual "callout" — the evidence should carry the weight, not the formatting. Figure panel labels in captions (`\textbf{(A)}`, `\textbf{Left}`, etc.) are exempt.
10. **Use the response-letter color scheme.** Reviewer comments should be rendered in sky blue via `\reviewercomment{...}`. Author responses should remain black via normal prose after `\responselabel`. Any wording that will be inserted into, or substituted in, the main manuscript or supplement should be rendered in red using `\mschange{...}`. This applies to the "Manuscript change" quote at the end of each response and to any in-line paraphrase of exact proposed manuscript text.
11. **No workflow triage markers in reviewer-facing files.** Do not include `Status:` or `Confidence:` lines in the compiled response letter.
