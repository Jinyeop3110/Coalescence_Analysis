# Reviewer 2 Reflection

Date: 2026-04-22

Scope: detailed evaluation of `latex/revision/response/reviewer2_response.tex` against a rebuttal-quality rubric emphasizing (i) accuracy to the real reviewer concern, (ii) directness, (iii) respectful tone, (iv) distinction between changed text and argument, (v) evidence support, (vi) concession, (vii) claim calibration, (viii) specificity, (ix) completeness without bloat, (x) internal consistency with the manuscript, and (xi) reviewer psychology.

Primary files checked:

- `latex/revision/response/reviewer2_response.tex`
- `latex/sections/results.tex`
- `latex/sections/discussion.tex`
- `latex/supplementary_sections/supplementary_methods.tex`

Secondary context checked:

- `latex/revision/response/README.md`
- `revision.rule.md`

## Executive Summary

Reviewer 2 is the most conceptually important rebuttal section because this reviewer is not mainly disputing a number or a figure. They are challenging the paper's interpretive discipline. The best Reviewer 2 responses therefore need to do three things simultaneously:

1. show that the concern was heard in its strongest form
2. narrow or recalibrate the claim where needed
3. make the paper easier to accept by telling the reviewer exactly what changed

At present, Reviewer 2 is uneven.

- `R2-1` is strong and close to submission-ready.
- `R2-6` is also solid, though it could be more specific.
- `R2-2` and `R2-3` contain useful material but are not yet optimally framed for reviewer psychology.
- `R2-4` is unfinished and currently the weakest scientifically presentable response because it still contains a placeholder and an under-specified manuscript-change statement.
- `R2-5` is too compressed relative to the sophistication of the reviewer's concern.
- `R2 minor` is not submission-ready because it still contains a placeholder and no checkable mapping.

The biggest global issue is not scientific weakness. It is rebuttal hygiene. Several responses still sound like internal working notes rather than a finished reviewer-facing package. The reviewer should not have to infer which points are integrated, which are pending, or where to verify them.

## Rubric

Scored on a 1-5 scale:

- Concern captured correctly
- Direct answer
- Tone
- Evidence / revision support
- Claim calibration
- Specificity
- Persuasiveness

Interpretation:

- `5`: strong submission-ready response
- `4`: good, only moderate polishing needed
- `3`: substantively useful but structurally or rhetorically incomplete
- `2`: significant revision needed before submission
- `1`: not reviewer-ready

## Global Observations

### What Reviewer 2 is actually worried about

Reviewer 2 is consistently pressing on a small set of conceptual risks:

1. whether "interaction strength" is being treated too simplistically
2. whether "community-level selection" is being over-inferred from correlated persistence
3. whether categorical outcome classes are being overinterpreted relative to underlying continuous geometry
4. whether pairwise selection correlation has a clear ecological meaning
5. whether the natural-community result is being overgeneralized despite laboratory pre-selection
6. whether the gLV model is being sold too mechanistically

This reviewer is not hostile. They are asking for conceptual honesty, better calibration, and more explicit bridge language between experiment, theory, and interpretation.

Responses that do best with this reviewer are the ones that:

- concede the valid part early
- state the narrower intended claim
- point to exact text changes
- avoid sounding like they are trying to "win" a philosophical argument

### Current strengths of the Reviewer 2 package

- The tone is mostly calm and non-defensive.
- There is genuine manuscript integration for several major points.
- The strongest responses already move in the right direction by reframing rather than stonewalling.
- The manuscript itself now contains useful caveat language in Discussion and Results that materially improves the paper.

### Current weaknesses of the Reviewer 2 package

- Some points still contain placeholders.
- Some responses are stronger than the concrete manuscript changes they actually document.
- Some "manuscript change" blocks under-report the real conceptual move and instead mention only a citation or one sentence.
- Some pending work is presented in a way that will create verification friction for the reviewer.
- The package is not yet fully synchronized between response rhetoric and finished paper state.

## Detailed Point-by-Point Review

## R2-1. Nutrient Enrichment Versus Interaction Strength

### Reviewer's actual concern

The reviewer is not saying the nutrient result is wrong. They are saying the causal interpretation may be over-simplified. Specifically:

- nutrient enrichment changes many ecological processes at once
- pH and environmental feedbacks are already implicated in the paper
- consumer-resource theory does not imply a simple monotonic mapping from supply to pairwise interaction strength
- the paper should not speak as if nutrient concentration cleanly equals stronger pairwise competition

This is a concern about framing, not about whether the empirical trend exists.

### Current response

Location:

- `latex/revision/response/reviewer2_response.tex:20-35`

### What is working well

1. The response captures the concern accurately.

The opening sentence directly agrees with the reviewer's main point:

- nutrient enrichment is multifaceted
- the mapping is not mathematically self-evident

This is exactly the right starting move for this reviewer.

2. The response is direct.

Within the first paragraph it says, in effect:

- yes, we agree with the complication
- our framework is coarse-grained
- we revised the manuscript accordingly

That is efficient and reviewer-friendly.

3. The response makes a real conceptual move.

It does not just defend the original wording. It narrows the claim. The key move is:

- interaction strength is defined operationally at the level of failed invasion / invasion resistance
- the gLV parameter is phenomenological rather than a direct mechanistic nutrient proxy

That is the correct rebuttal strategy.

4. The response points to real integrated manuscript edits.

The quoted manuscript changes correspond to actual text now present in:

- `latex/sections/results.tex:79`
- `latex/sections/discussion.tex:18`
- `latex/supplementary_sections/supplementary_methods.tex:81`

This is exactly the kind of traceability that reduces reviewer friction.

5. The response uses appropriate concession without capitulation.

It says the original scalar framing was too simple, but preserves the paper's narrower operational claim. That is persuasive.

### What is still weak

1. One sentence is rhetorically riskier than necessary.

At `reviewer2_response.tex:23`, the sentence:

> "The reviewer's concern ... is therefore a feature that is correctly captured by our metric rather than a confounder of it."

is intellectually understandable, but rhetorically sharper than it needs to be.

Why this matters:

- It can sound like the reviewer is being lectured.
- It implies the concern is fully dissolved rather than partially absorbed.
- Reviewer 2 is exactly the sort of reader who will react better to calibrated language than to a verbal reversal.

Safer alternative style:

- "Our metric is intended to absorb these mechanisms at the outcome level, rather than treat them as separable confounders."
- "We therefore revised the manuscript to make explicit that our use of interaction strength is operational and phenomenological, not a direct per-capita mechanistic claim."

2. The response is slightly longer than necessary.

The substance is strong, but the second paragraph could be tightened by 15-20% without losing content. Reviewer 2 will appreciate a cleaner arc.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `4`
- Evidence / revision support: `5`
- Claim calibration: `5`
- Specificity: `5`
- Persuasiveness: `4.5`

Overall: `4.5 / 5`

### Recommendation

Keep the structure. Only soften the one risky sentence and trim slightly.

## R2-2. Alternative Explanations for Community-Level Selection

### Reviewer's actual concern

This is one of Reviewer 2's core conceptual objections.

They are saying:

- dominance plus correlated persistence is not uniquely diagnostic of community-level selection
- environmental filtering, pH tolerance, and correlated traits could create similar patterns
- Nutr+ may be especially vulnerable to this alternative interpretation
- "failed invasion" should also be framed in ecological terms, namely invasion resistance / invasion fitness

This is fundamentally an interpretive challenge, not a request for extra nulls alone.

### Current response

Location:

- `latex/revision/response/reviewer2_response.tex:49-69`

### What is working well

1. The opening concession is good.

The first sentence directly says:

- correlated persistence is not uniquely diagnostic

This is exactly the right concession.

2. The response does include real counterarguments.

It uses:

- alternative-mechanism discussion in the Discussion
- monoculture viability
- pairwise-selection-correlation argument against pure hitchhiking
- gLV sufficiency argument
- assembly-history comparison

This is not an empty rebuttal. There is serious work here.

3. The response also adds extra simple-retention tests.

The density and pool-size arguments are useful supporting evidence, and the associated figure makes the response feel evidence-based rather than purely verbal.

4. The invasion-resistance clarification is directionally right.

The reviewer explicitly asked for this framing, and the response at least acknowledges it.

### What is weak

1. The response drifts from the reviewer's main objection.

The first paragraph is on target. The second paragraph shifts heavily into density and pool-size nulls.

Those tests are useful, but they are not the center of the reviewer's concern. Reviewer 2 is primarily asking:

- are you over-interpreting correlated persistence as community-level selection?
- especially in the pH-heavy Nutr+ regime?

Density and pool-size are more naturally supplementary support than the main answer.

2. The manuscript-change block is too narrow compared with the argument above it.

At `reviewer2_response.tex:67-69`, the documented manuscript changes are:

- adding `Mansour2018`
- planning to add an invasion-resistance sentence

But the argument above claimed much more:

- clarified alternative mechanisms
- interpreted Nutr+ more carefully
- linked failed invasion to invasion resistance

The response therefore feels broader than the explicit paper changes it documents.

3. The response does not cleanly separate:

- what was newly argued in the rebuttal
- what was newly inserted into the manuscript
- what remains pending

That weakens criterion 4 from the rubric.

4. The response should more explicitly narrow the claim in Nutr+.

It gestures toward this by calling Nutr+ "top-down," but the best version would explicitly say something like:

- "We agree that the Nutr+ regime can reflect strong environmental filtering imposed by dominant taxa, and we no longer present community-level selection as implying a uniform mechanism across media."

That would make the concession more legible.

5. The invasion-fitness portion is deferred too much to R2-4.

The reviewer bundled two linked concerns into R2-2. It is reasonable to cross-reference R2-4, but the response should still resolve the ecological meaning of failed invasion more concretely within this point.

### Score

- Concern captured correctly: `4`
- Direct answer: `3.5`
- Tone: `4.5`
- Evidence / revision support: `3.5`
- Claim calibration: `4`
- Specificity: `3`
- Persuasiveness: `3`

Overall: `3 / 5`

### Recommendation

Restructure the response around this arc:

1. concede that correlated persistence is not uniquely diagnostic
2. state the narrower claim now made in the manuscript
3. say explicitly how Nutr+ is framed more carefully
4. mention density/pool-size as additional support, not as the centerpiece
5. clearly separate integrated vs pending manuscript edits

## R2-3. Continuous Measures Alongside Categorical Outcomes

### Reviewer's actual concern

The reviewer accepts that categorical classes are useful, but wants:

- continuous measures shown alongside categories
- a clearer biological definition of "Restructuring"
- more explicit discussion of what metric disagreements mean, especially in weak-interaction conditions

This is partly a presentation concern and partly a claim-calibration concern.

### Current response

Location:

- `latex/revision/response/reviewer2_response.tex:83-94`

### What is working well

1. The response addresses the first requested item directly.

It immediately introduces:

- continuous PDI
- retention magnitude

and it presents a response figure.

2. The response makes a good conceptual point.

It says the categorical structure sits on top of a real continuous geometry, rather than replacing it. That is a persuasive way to answer the reviewer.

3. The response acknowledges threshold dependence.

This is a strong concession and exactly what the reviewer wanted to hear.

4. The proposed interpretation of metric disagreement is useful.

The distinction between abundance-weighted metrics and presence/absence-sensitive metrics is a sensible and reviewer-friendly explanation.

### What is weak

1. Too much of the response remains future-tense.

At `reviewer2_response.tex:86`, the response says:

- "we will add a new Supplementary Figure"

At `reviewer2_response.tex:94`, all the changes are listed as pending integration.

That is a problem because the response otherwise reads as if the issue has already been closed.

2. The response does not clearly distinguish between:

- what is already in the manuscript
- what exists only as a response figure
- what is planned but not yet integrated

That makes the response harder to verify.

3. The biological interpretation of "Restructuring" is currently only proposed, not shown as integrated.

Since the reviewer explicitly asked for this clarification, that point should either be fully integrated or clearly marked blocked.

4. The threshold-sensitivity promise is potentially high value, but dangerous if not actually in the paper.

This kind of promise is exactly what can make the rebuttal sound stronger than the manuscript.

### Score

- Concern captured correctly: `4.5`
- Direct answer: `4`
- Tone: `4.5`
- Evidence / revision support: `3.5`
- Claim calibration: `4.5`
- Specificity: `3.5`
- Persuasiveness: `3.5`

Overall: `3.5 / 5`

### Recommendation

Decide which state this point is in.

If the text and new supplementary figure are already integrated:

- cite exact section / figure / caption locations
- remove future-tense language

If not integrated:

- change the status to `Blocked`
- make the pending nature explicit from the first paragraph

## R2-4. Interpretation of Pairwise Selection Correlation

### Reviewer's actual concern

This reviewer is not rejecting the metric. They are saying:

- the interpretation is unclear
- it could be mistaken for co-occurrence or methodological artifact
- the paper would benefit from a short conceptual bridge to invasion fitness in the gLV framework

This is a request for interpretive clarification and theoretical integration.

### Current response

Location:

- `latex/revision/response/reviewer2_response.tex:103-114`

### What is working well

1. The response is short and direct.

It does not wander. It tries to connect pairwise selection correlation to invasion fitness quickly.

2. The general direction is good.

The idea that pairwise assays approximate two-species invasion fitness and community coalescence reflects correlated invasion success is a good bridge.

3. The presence of a response figure is helpful.

It signals that serious work was done.

### What is weak

1. This point is not submission-ready because it contains a placeholder.

At `reviewer2_response.tex:104`:

- `new Supplementary Fig. [PLACEHOLDER]`

This alone makes the response incomplete.

2. The manuscript-change statement is not specific enough.

At `reviewer2_response.tex:114`, the response says:

- "Added new paragraph to Supplementary Note 4, referencing invasion fitness framework and new figure."

This is too vague for a reviewer-facing rebuttal. It should include:

- the exact supplementary section location
- the exact new figure number
- ideally the new quoted sentence or paragraph

3. The response may be introducing terminology not clearly established in the manuscript.

The phrase "excess concordance" appears in `reviewer2_response.tex:104`, but the response does not show whether that exact term is now used in the paper or only in the rebuttal. This risks inconsistency.

4. The response does not explicitly answer the methodological-artifact concern.

The reviewer asked whether the observed correlations reflect:

- ecological interactions
- shared environmental responses
- methodological effects

The current response mostly answers the ecological side, but does not explicitly close the loop on the artifact concern.

5. The response is under-documented relative to its conceptual importance.

Because this is an interpretation-heavy point, the reviewer needs a very easy verification path.

### Score

- Concern captured correctly: `4`
- Direct answer: `3.5`
- Tone: `4.5`
- Evidence / revision support: `2`
- Claim calibration: `3.5`
- Specificity: `1.5`
- Persuasiveness: `2`

Overall: `2 / 5`

### Recommendation

This should be rewritten before submission.

Minimum necessary improvements:

1. remove placeholder
2. specify exact supplementary figure number
3. quote the exact new paragraph added to Supplementary Note 4
4. explicitly say how the revised wording distinguishes ecological interpretation from mere co-occurrence / artifact

## R2-5. Pre-selection of Natural Communities

### Reviewer's actual concern

The reviewer is not objecting to the natural-community experiment itself. They are warning that:

- the stabilization phase in defined medium may pre-select the communities
- this could reduce heterogeneity and make them more synthetic-like
- the paper should discuss this explicitly
- the paper should clarify the extent of convergence

This is mainly a generalizability and caveat-framing point.

### Current response

Location:

- `latex/revision/response/reviewer2_response.tex:127-128`

### What is working well

1. The response agrees immediately.

That is the right opening.

2. The response provides some factual support:

- natural communities retained higher ASV richness
- overlap remained low
- the nutrient trend was preserved

These are useful facts.

3. The manuscript does now contain a caveat paragraph.

This exists in:

- `latex/sections/discussion.tex:20`

and is a strong paper-level improvement.

### What is weak

1. The response is too compressed.

For a thoughtful reviewer who raised a legitimate generalizability caveat, this answer reads more like an internal note than a finished rebuttal.

2. The response does not really answer the "extent of convergence" request.

It gives richness and overlap facts, which are relevant, but it does not explicitly say:

- we cannot directly quantify functional convergence from the current data
- we therefore narrowed the claim and added a caveat

That concession would be persuasive.

3. The response does not specify the manuscript change.

It says:

- "We have expanded the Discussion caveat"

but does not quote the new text or point precisely enough to where it lives.

4. The response should more clearly narrow the paper's generality claim.

Reviewer 2 is concerned about overgeneralization. The rebuttal should explicitly say that the natural-community result is now framed as qualitative support under the tested laboratory stabilization protocol, not as broad evidence that all natural communities behave this way.

### Score

- Concern captured correctly: `3.5`
- Direct answer: `3`
- Tone: `4.5`
- Evidence / revision support: `3`
- Claim calibration: `3`
- Specificity: `2`
- Persuasiveness: `2.5`

Overall: `2.5 / 5`

### Recommendation

Expand this into a full rebuttal paragraph with this structure:

1. agree that pre-selection during stabilization is a real limitation
2. say what the current data can and cannot establish about convergence
3. note the facts that argue convergence was incomplete
4. quote the new Discussion caveat
5. explicitly narrow the generality claim

## R2-6. Frame gLV as Phenomenological

### Reviewer's actual concern

The reviewer is asking for:

- explicit framing of gLV as phenomenological rather than mechanistic
- clearer biological interpretation of the interaction distributions
- clearer meaning of `mu`

This is a model-framing request.

### Current response

Location:

- `latex/revision/response/reviewer2_response.tex:137-140`

### What is working well

1. The response is direct.

It immediately says the model description was revised.

2. The response matches the reviewer's request.

It covers:

- phenomenological framing
- meaning of `alpha_ij`
- meaning of `mu`

3. The underlying manuscript support is real.

Relevant text now exists in:

- `latex/sections/discussion.tex:18`
- `latex/supplementary_sections/supplementary_methods.tex:81`

### What is weak

1. The response should cite exact locations.

It currently quotes the text but does not explicitly say where in the paper the reviewer can find it.

2. It slightly duplicates material already used in R2-1.

This is not a major problem, but the distinction should be cleaner:

- `R2-1`: why nutrient enrichment is not treated mechanistically
- `R2-6`: why gLV itself is framed phenomenologically

### Score

- Concern captured correctly: `5`
- Direct answer: `4.5`
- Tone: `4.5`
- Evidence / revision support: `4.5`
- Claim calibration: `5`
- Specificity: `3.5`
- Persuasiveness: `4`

Overall: `4 / 5`

### Recommendation

Keep the response, but add exact manuscript section references.

## R2 Minor Comments

### Reviewer's actual concern

These are several implementation-level cleanup requests:

- pairwise-correlation visualization
- pH measurement protocol
- interpretation of coefficient distributions
- notation consistency
- typo correction

### Current response

Location:

- `latex/revision/response/reviewer2_response.tex:155-156`

### What is weak

1. The response contains a placeholder.

At `reviewer2_response.tex:156`:

- `[PLACEHOLDER --- confirm final styling]`

This is not reviewer-ready.

2. The response is too vague.

It should map each minor comment to one concrete revision location.

For example:

- pairwise-correlation styling: exact figure or caption updated
- pH protocol: exact Methods location
- coefficient interpretation: exact Supplementary Methods location
- terminology sweep: exact sections
- typo: exact corrected word location

3. The response creates verification work for the reviewer.

This is the opposite of what minor-comment responses should do. Minor comments should be the easiest section in the rebuttal to accept.

### Score

- Concern captured correctly: `4`
- Direct answer: `2.5`
- Tone: `4`
- Evidence / revision support: `2`
- Claim calibration: `4`
- Specificity: `1`
- Persuasiveness: `2`

Overall: `2 / 5`

### Recommendation

Replace with a short checkable itemized or compact prose mapping:

- visualization updated in Figure 2D / caption
- pH protocol added in Supplementary Methods at exact subsection
- coefficient interpretation clarified in Supplementary Methods
- terminology unified in Results / Discussion
- typo corrected at exact location

## Cross-Response Consistency Review

## 1. Consistency with manuscript state

There is partial but not complete consistency.

Clearly integrated and checkable:

- `R2-1` manuscript changes
- `R2-6` manuscript changes
- `R2-5` discussion caveat exists in the paper
- `R2-2` alternative-mechanism paragraph exists in the Discussion

Not yet fully clean:

- `R2-2` invasion-resistance statement is explicitly marked pending
- `R2-3` still frames key additions as pending
- `R2-4` does not yet give a verifiable paper location and still has a placeholder
- `R2 minor` still has a placeholder

Conclusion:

Reviewer 2 currently mixes finished and unfinished states. Before submission, either:

- complete the pending integrations and update the response accordingly

or

- clearly mark those points as `Blocked`

The current "Before review" labels are not enough to resolve the ambiguity for an internal polishing pass.

## 2. Terminology consistency

There is one notable conceptual inconsistency.

The response package still uses "top-down regime" in places, including:

- `latex/sections/discussion.tex:8`
- `latex/sections/results.tex:98-100`

If the team has decided that "species-driven regime" is preferred, then Reviewer 2 is exactly the reviewer most likely to be sensitive to this distinction. The terminology should be harmonized across:

- manuscript
- rebuttal
- figures / captions

## 3. Style consistency with response rules

Generally good:

- prose-first structure
- calm tone
- evidence-based framing

Needs cleanup:

- placeholders
- overlong some paragraphs
- manuscript-change statements uneven in specificity

## Reviewer Psychology Assessment

## What will likely work well on Reviewer 2

- early concessions in `R2-1`
- explicit phenomenological framing
- added caveat language in Discussion
- effort to distinguish operational from mechanistic interpretation

## What may still irritate Reviewer 2

- any placeholder or vague "we added a paragraph"
- any sense that the rebuttal is stronger than the actual manuscript
- any residual language implying that alternative explanations have been fully dismissed rather than bounded
- any terminology inconsistency around community-level versus species-driven interpretation

## What would make acceptance easier

The reviewer should feel:

- "they heard the conceptual concern"
- "they narrowed the claim where appropriate"
- "I can verify every change easily"

The current draft achieves the first two best in `R2-1` and `R2-6`, but not yet consistently across all Reviewer 2 points.

## Consolidated Scores

| Point | Concern | Direct | Tone | Evidence | Calibration | Specificity | Persuasive | Overall |
|------|---------|--------|------|----------|-------------|-------------|------------|---------|
| R2-1 | 5 | 5 | 4 | 5 | 5 | 5 | 4.5 | 4.5 |
| R2-2 | 4 | 3.5 | 4.5 | 3.5 | 4 | 3 | 3 | 3.0 |
| R2-3 | 4.5 | 4 | 4.5 | 3.5 | 4.5 | 3.5 | 3.5 | 3.5 |
| R2-4 | 4 | 3.5 | 4.5 | 2 | 3.5 | 1.5 | 2 | 2.0 |
| R2-5 | 3.5 | 3 | 4.5 | 3 | 3 | 2 | 2.5 | 2.5 |
| R2-6 | 5 | 4.5 | 4.5 | 4.5 | 5 | 3.5 | 4 | 4.0 |
| R2 minor | 4 | 2.5 | 4 | 2 | 4 | 1 | 2 | 2.0 |

## Priority Ranking for Revision

### Highest priority

1. `R2-4`
2. `R2-5`
3. `R2 minor`

Reason:

- these are the least reviewer-ready
- they contain either placeholders or insufficiently checkable revision claims

### Medium priority

4. `R2-2`
5. `R2-3`

Reason:

- both have good substance but need better rhetorical centering and state clarity

### Low priority

6. `R2-1`
7. `R2-6`

Reason:

- these are fundamentally strong already

## Concrete Editing Recommendations

## R2-1

- Soften "feature rather than confounder" phrasing.
- Trim repetition slightly.

## R2-2

- Re-center on the interpretive objection.
- State the narrower claim explicitly.
- Make Nutr+ concession more explicit.
- Move density/pool-size to supporting evidence.
- Expand the manuscript-change block to match the actual argument.

## R2-3

- Decide whether threshold-sensitivity and restructuring-text edits are integrated or pending.
- If pending, mark status accordingly.
- If integrated, cite exact locations and remove future tense.

## R2-4

- Remove placeholder.
- Give exact supplementary figure number.
- Quote the exact new paragraph.
- Explicitly address the concern about methodological interpretation, not only ecological interpretation.

## R2-5

- Expand into a full response paragraph.
- Concede limitation explicitly.
- State what cannot yet be inferred about convergence.
- Quote the Discussion caveat added to the manuscript.
- Narrow generality claims explicitly.

## R2 minor

- Remove placeholder.
- Make each minor comment checkable in one sentence.

## Bottom Line

Reviewer 2 can become a strong section, but only if the current draft is pushed from "good internal logic" to "finished external rebuttal." The scientific direction is mostly right. The remaining work is to improve calibration, verification, and closure.

The central principle for the next revision pass should be:

- do not defend more than the paper now claims
- do not promise more than the paper now contains
- make every response easy for the reviewer to verify in under a minute

If those three conditions are enforced, Reviewer 2 can become one of the strongest parts of the response letter.
