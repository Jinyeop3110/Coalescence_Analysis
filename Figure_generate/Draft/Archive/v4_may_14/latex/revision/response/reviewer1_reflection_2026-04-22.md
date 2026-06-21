# Reviewer 1 Reflection

Date: 2026-04-22

Scope: detailed evaluation of `latex/revision/response/reviewer1_response.tex` against a rebuttal-quality rubric emphasizing (i) accuracy to the reviewer's actual concern, (ii) directness, (iii) respectful tone, (iv) distinction between changed text and argument, (v) evidence support, (vi) concession, (vii) claim calibration, (viii) specificity, (ix) completeness without bloat, (x) internal consistency with the manuscript, and (xi) reviewer psychology.

Primary files checked:

- `latex/revision/response/reviewer1_response.tex`
- `latex/sections/results.tex`
- `latex/sections/discussion.tex`
- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `latex/supplementary_sections/extended_data.tex`
- `latex/supplementary_sections/figures.tex`

Secondary context checked:

- `latex/revision/response/README.md`
- `revision.rule.md`

## Executive Summary

Reviewer 1 is broadly favorable and mostly asks for:

1. additional checks against alternative explanations
2. clarification of figure presentation
3. slightly deeper interpretation of specific analyses
4. a few small text/reference fixes

That means the standard for a strong Reviewer 1 rebuttal is different from Reviewer 2. Reviewer 1 does not need long conceptual defense. Reviewer 1 needs clean closure. The best responses should therefore be:

- brisk
- concrete
- easy to verify
- visibly responsive to the exact analysis or display issue raised

At present, the Reviewer 1 section is scientifically strong but operationally mixed.

- The completed points are generally very good.
- The blocked points often contain strong evidence and useful figures.
- The biggest weakness is that several major responses remain in a "prepared but not integrated" state, so the rebuttal package still reads partly like an internal working draft.

The best parts of Reviewer 1 are:

- `R1-5`
- `R1-6`
- `R1-7`
- `R1-8`
- `R1-9`

These are concise, direct, and easy for the reviewer to accept.

The main risk areas are:

- `R1-1`
- `R1-2`
- `R1-3`
- `R1-4`

These are not weak scientifically. The risk is rebuttal-state mismatch:

- they present substantial new analyses
- they include convincing response figures
- but they are still explicitly pending manuscript integration

That is acceptable for internal drafting, but before submission the team will need to decide whether these points are:

- fully integrated and updated as such

or

- intentionally left as response-only analyses with very clear blocked wording

Right now they sit in between.

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
- `3`: substantively useful but structurally incomplete
- `2`: significant revision needed before submission
- `1`: not reviewer-ready

## Global Observations

### What Reviewer 1 is actually worried about

Reviewer 1 is mainly testing robustness. The central pattern is:

- "Could a simpler explanation account for this?"
- "Can you clarify this figure or interpretation?"
- "Can you make one point more explicit in the paper?"

This reviewer is not trying to overturn the manuscript. They are probing whether the conclusions survive obvious alternative explanations and whether the figures are reader-friendly.

That means the optimal response style is:

- agree when reasonable
- answer the exact question quickly
- show the new number / figure / caption change
- close with the concrete manuscript update

### Current strengths of the Reviewer 1 package

- Tone is consistently appreciative and non-defensive.
- Most responses are very concrete.
- The analysis-heavy points use real figures and real numbers.
- The display-fix points are appropriately short.
- The completed points feel easy for the reviewer to accept.

### Current weaknesses of the Reviewer 1 package

- Several major responses remain blocked and still contain placeholder-style `Supplementary Fig.~[X]`.
- Some blocked points are already highly polished scientifically but not yet synchronized with actual manuscript/supplement state.
- The response package is currently better than the integrated manuscript for some Reviewer 1 issues.
- A few response figures are probably larger than necessary for the point they support.

## Detailed Point-by-Point Review

## R1-1. Absolute Density as an Alternative Explanation for Dominance

### Reviewer's actual concern

Reviewer 1 asks whether differences in absolute biomass or OD between parents could explain:

- Dominance direction
- same-parent versus cross-parent pairwise selection correlation
- possibly the nutrient dependence of these patterns

This is a strong and fair alternative-mechanism question. The reviewer is not saying the paper is wrong. They are saying: if OD was measured, can you rule this out directly?

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:15-40`

### What is working well

1. The response captures the concern exactly.

It directly tests the three natural versions of the OD hypothesis:

- denser parent wins more often
- signed OD difference predicts PDI
- mean OD predicts pairwise selection correlation structure

That is very well aligned to the reviewer's actual objection.

2. The response is evidence-rich.

This is one of the strongest data-driven responses in the file. It contains:

- pooled numbers
- per-medium numbers
- directionally interpretable statistics
- a three-figure package

The reviewer should feel that the authors took the objection seriously.

3. The answer is direct.

The opening sentence:

- "None supported an absolute-density explanation."

is exactly the right style.

4. The response closes the loop well scientifically.

It does not just check one proxy. It checks both outcome direction and correlated species fate. That is persuasive.

### What is weak

1. The response is long, and the three full-width figures may be more than necessary.

Scientifically the material is strong, but rhetorically the point could likely land with:

- one tighter opening paragraph
- one compact summary sentence for the correlation analysis
- possibly smaller or combined figures if space matters

2. The manuscript-change block is still fully pending.

At `reviewer1_response.tex:40`, the response promises:

- Results insertion
- new supplementary figure

but the cited figure number is still `[X]`.

This is the main weakness. The issue is not substance. It is state.

3. The point is currently better as a rebuttal than as part of the paper.

If this analysis is important enough to rebut a clean alternative explanation, integrating it into the manuscript or supplementary will materially strengthen the paper. Keeping it response-only is possible, but then the blocked framing needs to remain very explicit.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `4.5`
- Evidence / revision support: `4`
- Claim calibration: `5`
- Specificity: `4`
- Persuasiveness: `4.5`

Overall: `4 / 5`

### Recommendation

Scientifically keep it. Operationally either:

- integrate and assign a real supplementary figure number

or

- keep blocked but shorten slightly and make the pending state unmistakable

## R1-2. Does pH Mismatch Predict Dominance?

### Reviewer's actual concern

Reviewer 1 asks a very precise mechanistic follow-up:

- if pH mismatch matters, is Dominance more likely for acid-vs-alkaline pairings than same-pH pairings?

This is narrower than the paper's existing pH argument. It is a nice test because it asks for a more direct consequence of the proposed mechanism.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:49-60`

### What is working well

1. The response answers directly in the first sentence.

The structure is excellent:

- "Yes in Nutr+, although..."

That is exactly what a reviewer wants.

2. The response distinguishes two different questions:

- Does pH mismatch increase the fraction of Dominance?
- Does pH mismatch predict which parent wins?

This is a strong analytical move because it accepts the reviewer's framing but clarifies that the cleaner signal is directional rather than categorical.

3. The claim is well calibrated.

The response does not overclaim significance on the Dominance-frequency comparison. It explicitly says:

- not significant
- small categories

That is credible and persuasive.

4. The figure seems well matched to the question.

Unlike some response figures, this one feels directly tailored to the reviewer's request.

### What is weak

1. The first sentence could be slightly cleaner.

"Yes in Nutr+, although the stronger pattern is..." is good, but because the first test is actually not significant, a more precise opener might be:

- "Not as a significant increase in Dominance frequency, but yes as a strong predictor of which parent wins in Nutr+."

That would reduce even slight ambiguity.

2. The manuscript-change block is still pending and still contains `[X]`.

Again, the weakness is state, not science.

3. The response arguably should say more explicitly why this still supports the mechanism.

It currently does this indirectly. A short sentence clarifying that the mechanism predicts directional asymmetry more strongly than a class-frequency shift would strengthen the logic.

### Score

- Concern captured correctly: `5`
- Direct answer: `4.5`
- Tone: `4.5`
- Evidence / revision support: `4`
- Claim calibration: `5`
- Specificity: `4`
- Persuasiveness: `4`

Overall: `4 / 5`

### Recommendation

Keep the structure and numbers. Improve only:

- the first sentence for precision
- the integration state

## R1-3. Circularity in Fig. 5C, PDI Excluding Dominant Species

### Reviewer's actual concern

Reviewer 1 asks whether the Fig. 5C result is partly circular because the dominant species contributes both to the explanatory pairwise-competition variable and to the outcome metric PDI.

This is an important credibility check. The reviewer is not asking for perfection. They want to know whether the effect survives after removing the obvious circular contribution.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:69-80`

### What is working well

1. The response answers the exact concern.

It says:

- the correlation weakens substantially
- but does not disappear
- therefore the result is not purely circular

That is the right substantive answer.

2. The response shows appropriate concession.

This is one of the best aspects of the point. It does not try to hide that:

- `R^2` drops a lot

That honesty increases credibility.

3. The use of two removal strategies is strong.

That signals careful thinking rather than a one-off robustness check.

4. The interpretation is nuanced.

The final sentence distinguishes:

- Nutr+ as more dominant-species-driven
- Base as more distributed across the community

This actually strengthens the regime narrative by making it less binary and more mechanistically credible.

### What is weak

1. The response is somewhat dense.

For a reviewer-facing reply, this many numbers in one paragraph may be a bit heavy. The underlying science is good, but readability could improve with slightly clearer signposting.

2. The response might benefit from one explicit sentence saying what changed in the manuscript claim.

For example:

- "We now present the dominant-species result as the strongest single contributor in Nutr+, not as a fully sufficient explanation."

That would make the claim-calibration benefit more explicit.

3. The manuscript-change block is again pending with `[X]`.

As with `R1-1` and `R1-2`, the response is stronger than the integrated paper state.

### Score

- Concern captured correctly: `5`
- Direct answer: `4.5`
- Tone: `4.5`
- Evidence / revision support: `4`
- Claim calibration: `5`
- Specificity: `4`
- Persuasiveness: `4.5`

Overall: `4 / 5`

### Recommendation

This is a good response. The main task is integration and slight readability cleanup.

## R1-4. Pool-Size Effects

### Reviewer's actual concern

Reviewer 1 is asking for:

- whether the experimental system also shows no pool-size effect
- why the model shows weak pool-size dependence
- whether realized richness / interaction structure help explain that result

This is partly a replication-of-model logic question and partly a mechanism question.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:89-98`

### What is working well

1. The response captures the question accurately.

It answers both:

- experiment
- model mechanism

2. The response gives the reviewer more than they asked for.

It provides:

- experimental null result
- realized parental richness result
- model within vs between `alpha_ij`
- same/cross co-persistence
- scalar `|phi|` summary

This is substantial and serious work.

3. The mechanistic explanation is coherent.

The key answer is:

- between-community competition is pool-size invariant
- within-community competition decreases mildly with larger pools
- `mu`, not pool size, is the dominant determinant

That is exactly the kind of explanation Reviewer 1 was inviting.

### What is weak

1. This point is close to being too heavy for a response.

Scientifically it is good, but rhetorically it starts to feel like a mini-results section. It may be more detail than the reviewer needs in the main body of the rebuttal.

2. The response says "survival ratio" in the reviewer's question, but the answer does not explicitly close that exact loop.

It discusses realized richness and the model mechanism, which is likely enough in practice, but the response could say explicitly whether experimental survival ratio itself was examined or whether realized richness is the chosen empirical proxy.

3. The manuscript-change block is still pending.

Again the main weakness is that the paper itself does not yet visibly contain all the material the response is presenting.

### Score

- Concern captured correctly: `5`
- Direct answer: `4.5`
- Tone: `4.5`
- Evidence / revision support: `4`
- Claim calibration: `5`
- Specificity: `4`
- Persuasiveness: `4`

Overall: `4 / 5`

### Recommendation

Keep the scientific structure. Consider trimming some detail and explicitly addressing the experimental survival-ratio phrase.

## R1-5. Similarity-Metric Robustness Claim

### Reviewer's actual concern

Reviewer 1 is not asking to change the method. They are asking the authors not to overstate the robustness claim when two alternative metrics actually reverse the ordering.

This is a claim-calibration request.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:106-107`

### What is working well

1. The response is exemplary in directness.

It opens:

- "We agree..."

and immediately states what was softened.

2. The concession is exactly right.

The response does not defend the old wording. It corrects it.

3. The manuscript wording is concrete and checkable.

This is a model response:

- exact revised sentence
- exact caption-level adjustment
- claim narrowed to abundance-weighted metrics

4. Reviewer psychology is excellent here.

The reviewer should feel heard and rewarded for catching a real overstatement.

### What is weak

Very little. The only minor improvement would be to name the exact location in the paper more explicitly, but the response is already strong enough.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `5`
- Evidence / revision support: `5`
- Claim calibration: `5`
- Specificity: `4.5`
- Persuasiveness: `5`

Overall: `5 / 5`

### Recommendation

Use this response as a model for several other points.

## R1-6. Gray Reflected Points in Figures

### Reviewer's actual concern

The reviewer was confused by a display choice and wanted either:

- explicit explanation

or

- removal

This is a straightforward figure-clarity point.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:116-117`

### What is working well

1. The response is concise and direct.

2. The change is exactly responsive.

3. The paper-level wording is quoted concretely.

4. The response distinguishes Fig. 5C as requiring slightly different wording.

That last detail is good because it shows care rather than boilerplate.

### What is weak

Almost nothing. This is a good display-fix response.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `5`
- Evidence / revision support: `5`
- Claim calibration: `5`
- Specificity: `5`
- Persuasiveness: `5`

Overall: `5 / 5`

### Recommendation

No substantive change needed.

## R1-7. Interaction Matrix After Assembly

### Reviewer's actual concern

The reviewer wants a visualization of post-assembly interaction structure, ideally showing the block structure the text invokes.

This is a concrete visualization request with mechanistic relevance.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:126-135`

### What is working well

1. The response does exactly what the reviewer asked.

2. It explains why the figure was placed in the Supplement rather than Fig. 2A itself.

That is a very good rebuttal move because it answers the reviewer while preserving manuscript design discipline.

3. The added manuscript sentence is precise and easy to verify.

4. The response links the figure to the paper's mechanism clearly.

### What is weak

Only minor points:

- The response figure may not be strictly necessary if the supplementary figure is already integrated, but including it is still reasonable.
- Exact section or line references could be added, though the current response is already quite clear.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `5`
- Evidence / revision support: `5`
- Claim calibration: `5`
- Specificity: `4.5`
- Persuasiveness: `5`

Overall: `5 / 5`

### Recommendation

No substantive change needed.

## R1-8. Fig. 2D Visualization

### Reviewer's actual concern

The reviewer was confused about:

- what the dots represent
- what the squares represent
- what the gray horizontal bars mean

This is a figure-legend clarity point.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:143-144`

### What is working well

1. The response cleanly decomposes the confusion into two parts.

2. It provides the exact caption text added.

3. It explains why the squares and dots need not coincide.

4. It resolves the gray-line explanation explicitly.

This is another strong example of a reviewer-friendly figure-fix response.

### What is weak

Little to nothing. The point is appropriately concise.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `5`
- Evidence / revision support: `5`
- Claim calibration: `5`
- Specificity: `5`
- Persuasiveness: `5`

Overall: `5 / 5`

### Recommendation

No substantive change needed.

## R1-9. Emphasize "Cohesion Without Cooperation"

### Reviewer's actual concern

The reviewer wants the paper to emphasize a concept they view as interesting and counterintuitive:

- community-level cohesion without cooperation

This is mainly a discussion-emphasis point.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:153-154`

### What is working well

1. The response agrees directly.

2. The inserted sentence is appropriate in tone and placement.

3. The response explains where the sentence sits in the Discussion logic.

That last part is useful because it tells the reviewer the emphasis was not just appended randomly.

### What is weak

Very little. If anything, the point could cite the exact Discussion location, but that is optional.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `5`
- Evidence / revision support: `4.5`
- Claim calibration: `5`
- Specificity: `4.5`
- Persuasiveness: `5`

Overall: `4.5 / 5`

### Recommendation

No substantive change needed.

## R1-10. Means Missing in Extended Data Fig. 5C

### Reviewer's actual concern

The reviewer suspects the mean markers may be missing.

This is a tiny figure-verification point.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:163-166`

### What is working well

1. The response is appropriately brief.

2. It does not manufacture a fake change when none was needed.

3. It says no manuscript change was needed.

That honesty is good.

### What is weak

It might help to say explicitly that no figure revision was needed either, only verification. But this is very minor.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `5`
- Evidence / revision support: `4`
- Claim calibration: `5`
- Specificity: `4`
- Persuasiveness: `4.5`

Overall: `4.5 / 5`

### Recommendation

Optional micro-polish only.

## R1-11. Incorrect Extended Data Reference in the SI

### Reviewer's actual concern

A straightforward cross-reference correction.

### Current response

Location:

- `latex/revision/response/reviewer1_response.tex:175-176`

### What is working well

1. Perfectly concise.

2. Exactly responsive.

3. Easy to verify.

This is what a minor-correction rebuttal should look like.

### What is weak

Nothing meaningful.

### Score

- Concern captured correctly: `5`
- Direct answer: `5`
- Tone: `5`
- Evidence / revision support: `5`
- Claim calibration: `5`
- Specificity: `5`
- Persuasiveness: `5`

Overall: `5 / 5`

### Recommendation

No change needed.

## Cross-Response Consistency Review

## 1. Completed versus blocked state

Reviewer 1 is sharply split into two groups.

Clearly completed and paper-synchronized:

- `R1-5`
- `R1-6`
- `R1-7`
- `R1-8`
- `R1-9`
- `R1-10`
- `R1-11`

Prepared but not fully integrated:

- `R1-1`
- `R1-2`
- `R1-3`
- `R1-4`

This split is not itself a problem. In fact, the status markers make the state legible. The problem is that the blocked points are already very polished and use almost-final prose, but still contain:

- `Supplementary Fig.~[X]`
- manuscript changes phrased as plans

That creates an unstable in-between state. Before submission, those four points should not remain half-final.

## 2. Consistency with manuscript state

The completed Reviewer 1 points are well synchronized with the current paper.

Examples:

- metric robustness is reflected in `latex/supplementary_sections/extended_data.tex:22`
- post-assembly matrix is reflected in `latex/supplementary_sections/figures.tex:358`
- reflected gray points are described in captions
- discussion emphasis on cohesion without cooperation is present in `latex/sections/discussion.tex:11`

The blocked points, however, are clearly stronger than the currently integrated manuscript state. That is acceptable only if the final response letter preserves the blocked wording and does not imply those analyses are already in the paper.

## 3. Style consistency with response rules

Strengths:

- mostly prose-first
- calm tone
- evidence-centered
- manuscript-change sections usually present

Potential issues:

- some blocked points are long enough to feel like mini-results sections
- several response figures are full-width and may be more than needed
- placeholder figure numbering remains

## Reviewer Psychology Assessment

## What Reviewer 1 will likely appreciate

- the seriousness with which alternative explanations were tested
- the clean fixes to figure confusion
- the willingness to soften overstatements
- the added block-structure figure
- the explicit emphasis on "cohesion without cooperation"

## What could still create friction

- if blocked points remain blocked at submission time
- if the response looks more complete than the manuscript
- if placeholder supplementary figure numbers remain
- if long analysis-heavy responses become harder to parse than necessary

Reviewer 1 is likely easy to satisfy if the authors make the paper-response mapping clean. This reviewer is not looking for a fight. They are looking for closure.

## Consolidated Scores

| Point | Concern | Direct | Tone | Evidence | Calibration | Specificity | Persuasive | Overall |
|------|---------|--------|------|----------|-------------|-------------|------------|---------|
| R1-1 | 5 | 5 | 4.5 | 4 | 5 | 4 | 4.5 | 4.0 |
| R1-2 | 5 | 4.5 | 4.5 | 4 | 5 | 4 | 4 | 4.0 |
| R1-3 | 5 | 4.5 | 4.5 | 4 | 5 | 4 | 4.5 | 4.0 |
| R1-4 | 5 | 4.5 | 4.5 | 4 | 5 | 4 | 4 | 4.0 |
| R1-5 | 5 | 5 | 5 | 5 | 5 | 4.5 | 5 | 5.0 |
| R1-6 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5.0 |
| R1-7 | 5 | 5 | 5 | 5 | 5 | 4.5 | 5 | 5.0 |
| R1-8 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5.0 |
| R1-9 | 5 | 5 | 5 | 4.5 | 5 | 4.5 | 5 | 4.5 |
| R1-10 | 5 | 5 | 5 | 4 | 5 | 4 | 4.5 | 4.5 |
| R1-11 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5.0 |

## Priority Ranking for Revision

### Highest priority

1. `R1-1`
2. `R1-2`
3. `R1-3`
4. `R1-4`

Reason:

- not because the science is weak
- because they are still in a blocked / semi-integrated state

### Lower priority

5. `R1-9`
6. `R1-10`

Reason:

- already good, only optional micro-polish

### Essentially done

7. `R1-5`
8. `R1-6`
9. `R1-7`
10. `R1-8`
11. `R1-11`

## Concrete Editing Recommendations

## R1-1

- Keep the core evidence.
- Consider trimming slightly.
- Replace `Supplementary Fig.~[X]` with a real number once integrated.
- If not integrated, keep the blocked status and perhaps shorten the manuscript-change block.

## R1-2

- Make the first sentence even more precise about what is and is not significant.
- Integrate or assign a real supplementary figure number.

## R1-3

- Keep the concession that the signal weakens after dominant-species removal.
- Consider one sentence explicitly stating the revised, narrower claim.
- Integrate or assign a real supplementary figure number.

## R1-4

- Consider trimming slightly.
- Explicitly say whether experimental survival ratio was separately analyzed or whether realized richness is the operative experimental proxy.
- Integrate or assign a real supplementary figure number.

## R1-5

- No substantive change.

## R1-6

- No substantive change.

## R1-7

- No substantive change.

## R1-8

- No substantive change.

## R1-9

- Optional: add exact Discussion location.

## R1-10

- Optional: note that no figure revision was needed, only verification.

## R1-11

- No substantive change.

## Bottom Line

Reviewer 1 is in better shape than Reviewer 2 overall. The completed Reviewer 1 responses are often excellent. The outstanding work is mostly not conceptual. It is integration and closure.

The central principle for the final pass on Reviewer 1 should be:

- for completed points, keep the answers short and verifiable
- for blocked points, either integrate fully or remain transparently blocked
- do not leave major analyses in a half-finished state with placeholder supplementary figure numbers

If that cleanup is done, Reviewer 1 should become the easiest section of the rebuttal for reviewers and editor to accept.
