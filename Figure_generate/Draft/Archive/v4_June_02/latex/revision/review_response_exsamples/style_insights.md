# Response Style Insights from Gore eLife Examples

This folder contains local HTML, full Markdown conversions, and extracted author-response sections from four eLife peer-review pages:

- `58144`: Inversion of pheromone preference optimizes foraging in C. elegans, eLife 2021
- `07935`: Phenotypic states become increasingly sensitive to perturbations near a bifurcation in a synthetic gene network, eLife 2015
- `01169`: Spatial dilemmas of diffusible public goods, eLife 2013
- `67175`: Environmental fluctuations reshape an unexpected diversity-disturbance relationship in a microbial community, eLife 2021

Source URLs:

- https://elifesciences.org/articles/58144/peer-reviews
- https://elifesciences.org/articles/07935/peer-reviews
- https://elifesciences.org/articles/01169/peer-reviews
- https://elifesciences.org/articles/67175/peer-reviews

## Local Files

For each paper, there are three useful local file types:

- `*_peer_reviews.html`: raw downloaded eLife page
- `*_peer_reviews.md`: full page converted to Markdown, including decision letter and author response
- `*_author_response.md`: extracted author-response section only

## Shared Response Pattern

The responses are direct but not terse. They usually follow this sequence:

1. Quote or restate the reviewer concern.
2. Open with agreement, thanks, or apology when clarity was lacking.
3. Answer the scientific point immediately.
4. Give the evidence, analysis, model change, or conceptual reason.
5. State exactly what was changed in the manuscript, often with line numbers, figure names, captions, or inserted text.

Common opening moves:

- "We agree that..."
- "We thank the reviewers for..."
- "We apologize that we were not more clear..."
- "This is an excellent point."
- "Thank you for pointing this out."
- "The labeling is correct; we apologize for any confusion."

The tone is deferential without surrendering the core claim. The authors often concede wording, scope, framing, or clarity, while preserving the central result with a more precise claim.

## How They Handle Criticism

When the reviewer is correct:

- Accept the point plainly.
- Say what changed.
- Quote or summarize the new manuscript text.
- Avoid arguing.

Example pattern:

> We agree that the previous wording was too broad. We have revised the Title, Abstract, and Introduction to make clear that most results use a synthetic circuit.

When the reviewer identifies ambiguity:

- Apologize for lack of clarity.
- Explain the intended meaning.
- Add a caption, paragraph, or wording change.

Example pattern:

> We apologize for any confusion. The labeling is correct because the winning species is determined by the lowest resource requirement at the specified mortality rate. We have added a sentence to the figure caption.

When the reviewer asks for more experiments or analyses:

- If feasible, perform the analysis and report the result.
- If not feasible, explain the limitation, tone down the claim, and add discussion.
- Do not overpromise.

Example pattern:

> These experiments could strengthen the conclusion. Given the current data, we instead changed the wording and added a discussion of the limitation.

When the reviewer challenges novelty or generality:

- Identify the specific general claim that remains.
- Distinguish the present work from prior work.
- Avoid broad defensive claims.
- Add citations or discussion to place the work better.

Example pattern:

> In addition to the known effect, our model makes the unexpected prediction that the outcome depends only on public goods received by a cell and its immediate neighbors.

## Manuscript-Change Style

These examples are very explicit about changes. They use phrases like:

- "We have added..."
- "We have revised..."
- "We have changed the caption..."
- "We now discuss..."
- "The main text now reads..."
- "This has been added as a panel to..."
- "We have incorporated the suggested references..."

They frequently include:

- figure names
- supplement names
- line numbers
- exact inserted paragraphs
- exact caption text
- citations added

For the current rebuttal, this maps well to the local rule that every response should end with a manuscript change or a clear reason for no change.

## Evidence Style

The stronger examples do not merely say that a point was addressed. They report what was found:

- new simulations up to a specified scale
- added supplementary figures
- figure panels supporting a claim
- experimental limitations and confounds
- model assumptions and where they were relaxed
- whether an effect is qualitative, quantitative, or limited

They also distinguish evidence strength:

- "definitive evidence" versus "consistent with"
- "most parsimonious explanation"
- "working hypothesis"
- "qualitatively change" versus "relative impact decreases"
- "sufficient condition" versus "necessary condition"

This is important for our response letter because several reviewer points involve mixed or conditional results.

## Unified Style to Emulate

Across the examples, the strongest recurring style is not paper-specific. It is a consistent response posture:

- respectful but not verbose
- specific about what changed
- precise about what the evidence does and does not show
- willing to soften claims when support is incomplete
- careful to distinguish explanation, new analysis, manuscript edits, and remaining limitations

For our responses, use the examples as a single shared style reference rather than choosing one paper as the model.

## Rules to Internalize for Current Responses

1. Lead with the answer, not the backstory.
2. Acknowledge the reviewer before explaining.
3. Concede wording, scope, or missing clarity freely.
4. Preserve the main result only when the data support it.
5. Use "we agree" only when we accept the premise or changed the framing.
6. Use an apology for labeling, notation, terminology, unclear captions, or missing explanation.
7. For weak or mixed evidence, say exactly what is supported and what remains unresolved.
8. Every response should name the concrete manuscript action.
9. Prefer "we have revised/added/changed" over vague "we addressed."
10. When no new analysis is possible, narrow the claim and add limitation text.
11. When a model assumption is challenged, say whether relaxing it changes the qualitative conclusion.
12. When a reviewer asks about generality, answer with the mechanism and its boundary conditions.
13. Include exact figure, supplement, section, or caption references whenever possible.
14. Quote new manuscript text only when it helps the reviewer see the change.
15. Keep the tone calm, factual, and non-defensive.

## Useful Sentence Templates

- "We agree that the previous wording overstated this point, and we have revised the text to make the claim more precise."
- "We apologize for the lack of clarity. The intended comparison was..., and we have clarified this in the caption."
- "This is an important distinction. The new analysis shows..., while... remains a limitation."
- "To test whether this explanation was sufficient, we performed..."
- "The result did not qualitatively change when..., although the effect size was reduced."
- "Because the current data cannot distinguish these alternatives definitively, we have toned down the conclusion and added a limitation."
- "We have added the following sentence to the Discussion:"
- "We have revised the caption to state explicitly that..."
- "We do not interpret this as evidence for..., but rather as evidence that..."

## Caution for Our Local Rules

The downloaded examples often quote long manuscript passages and sometimes use long responses. Our local `response/README.md` is stricter:

- answer in the first sentence
- keep responses concise
- avoid itemization inside a single response
- do not overclaim manuscript integration
- include status and confidence lines
- highlight manuscript-bound text in blue

So the examples should guide tone and argumentative posture, but the local response-letter rules still control final formatting.
