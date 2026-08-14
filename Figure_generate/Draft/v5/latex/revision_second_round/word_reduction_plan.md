# Word-Reduction Plan (Editor Request: shorten toward 3,500 words)

Prepared 2026-07-31. Revised 2026-08-08 after context and style review of the
Tier 1 draft. Working plan only; no manuscript file has been edited for length
yet.

**Editor request:** "Please try to shorten the manuscript closer to 3500 words,
perhaps by shortening the Introduction."

**Counting rule (author-confirmed):** Introduction + Results + Discussion only.
Figure legends, Abstract, Methods, and references do not count.

---

## 1. Baseline

| Component | Words | Counted? |
|---|---:|---|
| Introduction | 755 | yes |
| Results | 2,902 | yes |
| Discussion | 702 | yes |
| **Counted total** | **4,359** | |
| Figure legends (6) | 953 | no |
| Abstract | 199 | no |
| Methods | 1,228 | no |

**Gap to target: 859 words, or 20% of counted text. This number is now firm.**

Note on structure: both the live manuscript and the clean submission source now
keep the six main legends in `sections/figure_legends.tex`. Neither copy is
counted under the author-confirmed rule. Any relocation into a legend must be
made in both files, preserving revision markup only in the live source.

### Results broken out by subsection

| Subsection | Words |
|---|---:|
| 1. Community-level selection is prevalent | 777 |
| 2. Theoretical model with random interactions | 536 |
| 3. Interaction strength controls outcome type | 333 |
| 4. Nutrient-dependent invasion resistance | 425 |
| 5. Predictability reveals two regimes | 537 |
| 6. Natural sample-derived communities | 328 |

### Legend headroom (uncounted, so this is free space)

| Legend | Words |
|---|---:|
| Fig. 1 | 153 |
| Fig. 2 | 207 |
| Fig. 3 | 104 |
| Fig. 4 | 195 |
| Fig. 5 | 145 |
| Fig. 6 | 143 |

---

## 2. The Introduction cannot absorb this alone

The whole Introduction is 755 words. Deleting all of it lands at 3,604, still
above target. A realistic 30% Introduction cut yields 235 words. The remaining
~620 must come from Results (67% of counted text) and Discussion.

This should be stated plainly to the editor: we followed the suggestion, but
reaching 3,500 required trimming Results and Discussion as well.

---

## 3. Constraint map: what must not be touched

### 3a. Verbatim-locked sentences

The second-round response letter quotes three manuscript sentences inside
`\mschange{}`. Under `revision.rule.md` Rule 1 these must remain word-for-word,
or the letter has to be updated in the same pass. Two of the three are in the
Introduction, the section the editor asked us to cut.

| Location | Point | Sentence opens |
|---|---|---|
| `introduction.tex` | R1-3 | "Together, these findings suggest that species-level selection may occur during coalescence when cross-community competitive exclusion is limited..." |
| `introduction.tex` | R1-4 | "Empirical work reports that coexistence between species from different source communities via niche partitioning is more common than competitive exclusion..." |
| `title_abstract.tex` | R1-2 | "A similar nutrient-dependent shift toward dominance of one parental community also appears..." |

**Consequence: Introduction paragraph 4 is off limits in its entirety.** Both
locked sentences live there, and the surrounding sentences are the evidence they
depend on.

Verified: none of the three sits in any Results or Discussion passage targeted
below, so every cut and relocation in this plan is Rule 1 safe.

### 3b. Revision-marked text

| Section | Total | Reviewer-marked | Freely editable |
|---|---:|---:|---:|
| Introduction | 755 | ~136 (18%) | ~619 |
| Results | 2,902 | ~1,017 (35%) | ~1,885 |
| Discussion | 702 | 193 (27%) | ~509 |

Anything inside `\rev{}` or `\revsecond{}` answers a reviewer point. It can be
tightened or relocated, but not deleted.

### 3c. Do not touch pending the code audit

`OPEN_QUESTIONS_FROM_CODE_AUDIT.md` item 1 is unresolved: the Methods and
Results four-community / 54-species-pool description may not match what was
actually simulated. **Leave the four-community sentences in Results section 2
alone.** They may need rewriting on scientific grounds, and that rewrite should
not collide with a length edit.

---

## 4. Primary strategy: relocate before deleting

Because legends are not counted, **moving a sentence from body text into a
figure legend reduces the counted total by its full length while keeping every
word in the manuscript.** No content is lost, no citation is dropped, no
reviewer-driven text disappears, and Rule 1 is satisfied because the text still
exists in the manuscript.

This is strictly safer than deletion and should be the backbone of the work.
Relocation is especially suited to:

- enumerated robustness checks and their supplementary pointers
- statistical restatements that support a panel rather than the argument
- sample-size and descriptive statistics tied to one figure

Two constraints:

1. Check the format checklist for a per-legend word cap. Current legends run 104
   to 207 words, so there is likely headroom, but confirm before loading Fig. 3
   (104 words, the most headroom) and Fig. 6 (143).
2. Relocated `\rev{}` / `\revsecond{}` text keeps its macro in the live source so
   the round-marking stays correct in its new location.

---

## 5. Tier 1: safe cuts (365 words as revised, lands at ~3,994)

Duplication and Methods restatement only. No scientific content, statistic,
sample size, citation, or reviewer-driven sentence is removed.

### Introduction: 151 words

**I-1. Closing paragraph, 197 to 145 (save 52).**

The paragraph re-previews every result. Measured overlap with the Abstract: 8
shared six-word sequences, including one near-verbatim sentence ("a similar
nutrient-dependent shift toward dominance ... also appears in taxonomically
richer communities derived from natural environmental samples"). That is the
R1-2 sentence, and the copy the letter quotes is the one in the Abstract, so
removing the Introduction copy touches nothing locked.

- Condense the four preview sentences to two sentences that preserve the
  interaction-strength transition, correlated persistence, gLV support,
  nutrient dependence in synthetic and natural sample-derived communities, and
  the two mechanistic regimes.
- Keep the gap statement, "Here, we combine empirical and theoretical
  approaches...", the first-use definitions of Dominance, Mixture, and
  Restructuring (needed before Results), and the closing reconciliation sentence.

**I-2. Coalescence-contexts catalogue, paragraph 2 (save 33).**
Four worked examples carrying 7 citations. Compress to one sentence naming the
contexts, retaining all 7 citations and the contrast between correlated and
parental-origin-independent species fates.

**I-3. Clements/Gleason framing, paragraph 1 (save 36).**
Keep both paradigm names and all 9 citations; the Discussion calls back to "the
Clements--Gleason debate", so both names must survive. Trim the expository
glosses and fold "Historically, this tension has been framed..." into the next
sentence.

**I-4. Holistic-evidence paragraph, paragraph 3 (save 30).**
Keep all four claims. Compress, rather than delete, the assembly-filtering to
coupled-fates mechanism, and keep `Debray2022` attached to that claim.

**Introduction paragraph 4: no cut.** See 3a.

### Discussion: 94 words

**D-1. Priority-effects parallel, paragraph 3 (save 28).** Three sentences
develop then restate the parallel. Compress to two short sentences plus
citations, without the categorical claim that parental identity matters only
under strong interactions.

**D-2. Limitations and outlook, paragraph 5 (save 35).** Compress the
environmental-heterogeneity list and the host-associated sentence. Keep the
operational-definition caveat, which is R2-1 relevant.

**D-3. Paragraph 2 closing sentence (save 31).** "This framework provides a
unified perspective..." restates paragraph 1's Clements--Gleason sentence.
Verified 2026-07-31: not inside any `\rev{}` span, so free to cut. The four
marked Discussion spans are the predictability-regimes sentence (40w), the
coarse-grained-descriptor caveat (29w), the no-cooperation-needed paragraph
(95w), and the operational-definition sentence (33w). D-1 and D-2 work around
those.

### Results: 120 words, method-restatement and local redundancy only

**R-1. Section 1 paragraph 1 (save 40).** The second Restructuring definition
(33w, marked `\rev{}`, restates the definition one sentence earlier) and the
"To address this, we asked how often..." sentence restating the opener. Retain
a short transition into the worked example.
Protect the R2-1 sentence "Throughout, Dominance is the outcome-level
signature...".

**R-2. Section 1 paragraph 2 (save 52).** The full Base-medium recipe and the
"29 families across three phyla" detail are repeated in `methods.tex`. Keep the
phylogenetic-breadth claim, survival-ratio statistic, sample sizes, and all
figure references.

**R-3. Section 2 paragraph 1 (save 28).** The phenomenological-framework caveat
(40w, `\rev{}`) overlaps the Discussion's coarse-grained-descriptor sentence;
tighten it while preserving the distinction between statistical interaction
coefficients and experimental biochemical mechanisms. Protect the R1-7
four-community sentence, see 3c.

---

## 5b. Tier 1B: 134 further words (added 2026-08-01), lands at ~3,860

The first Tier 1 draft saved 389 words, but context and style review reduced that
to 365 words so that the Introduction retains every headline result, the
species-level/community-level contrast, and the assembly-to-coupled-fates
mechanism. Tier 1B closes part of the remaining shortfall with the same grade of
edit. All six items are in Results, which is where the remaining redundancy
sits. Side-by-side draft:
`length_reduction_review_tier1b.pdf`.

| ID | Location | Words | Saves | Markup |
|---|---|---|---:|---|
| R-4 | §1 ¶1, after Eq. 1: symbol list + similarity-map sentence | 92→63 | 29 | `\rev{}`, compressed |
| R-9 | §1 ¶4: null-model opener and closing restatement | 90→64 | 26 | `\rev{}` / `\revsecond{}`, compressed |
| R-5 | §2 ¶2 closing sentence, duplicates sentence 3 earlier | 78→54 | 24 | none |
| R-8 | §5 opening sentence, recaps §4 | 67→44 | 23 | none |
| R-7 | §4 ¶2 closing sentence, clause after the colon | 70→51 | 19 | `\revsecond{}`, shortened |
| R-6 | §3 opening sentence, recap transition | 47→34 | 13 | none |
| | **Total** | **444→310** | **134** | |

60 of the 134 come from text with no revision markup at all (R-5, R-6, R-8). The
other three compress marked text without removing the reviewer-facing claim.

Notes:
- **R-4 merges with R-1**: R-4 edits exactly the passage R-1 elides as
  "[… equation and definitions unchanged …]". Apply them as one paragraph edit.
- R-9 checked against the second-round response letter: the null-model passage is
  not quoted there, so no `\mschange{}` lock applies.
- R-8 removes an Extended Data Fig. 7 reference; the same figure is already cited
  in §4, so no reference is orphaned.

Revised running position: 4,359 − 365 (Tier 1) − 134 (Tier 1B) = **3,860**.
Tier 2 must therefore cover **360** words.

---

## 6. Tier 2: approximately 360 words required to land at 3,500

Now required, not optional. Mostly relocation rather than deletion, per section 4.

| ID | Item | Words | Method | Marked |
|---|---|---:|---|---|
| T2-1 | Section 3 robustness sentence: five model variations plus Supplementary Figs. 4-6, 39-41 and ED Fig. 5 | 64 | Relocate to Fig. 3 legend (104w, most headroom) | `\rev{}` |
| T2-2 | Section 5 dominant-species-excluded recalculation (Spearman, two p-values, Supplementary Fig. 16) | 58 | Relocate to Fig. 5 legend | `\rev{}`, R1-14 |
| T2-3 | Section 5 pH-contrast numeric detail (n = 41, n = 32, Fisher's exact p) | ~40 | Relocate to Fig. 5 or ED Fig. 8 legend; keep the interpretive clause in body | `\rev{}` |
| T2-4 | Section 4 outcome fractions restated in prose and again in the Fig. 4 legend | ~35 | Delete from prose; already in the legend verbatim | partly |
| T2-5 | Section 6 richness statistics (13.7 +/- 7.2 vs 9.8 +/- 4.8 ASVs) | ~30 | Relocate to Fig. 6 legend | `\rev{}` |
| T2-6 | Section 6 paragraph 1 transition restating the synthetic-community setup | 55 | Compress to ~20 | partly |
| T2-7 | Section 1 paragraph 3 representative time-series description | ~25 | Compress; the trajectories are visible in Fig. 1D | no |
| T2-8 | Section 3 PDI definition, also defined in Methods | ~25 | Compress to a Methods pointer | no |
| | **Current identified total** | **~332** | | |

The currently identified Tier 2 items leave roughly 28 words still to find,
before accounting for noise in the counting method. T2-6 and T2-7 have enough
room for that additional reduction, but their final wording must receive the
same context-and-style review as Tier 1.

**Sequencing note:** do T2-4 first. It is the only pure duplication in Tier 2
and needs no legend edit.

---

## 7. Residual questions

**7a. Per-legend word cap.** Confirm against the format checklist before
relocating into Fig. 3 and Fig. 6. If a cap bites, T2-1 and T2-5 fall back to
compression in place, which costs roughly 30 of the 347.

**7b. Abstract length.** The Abstract is 199 words and is not part of this
count, but if the checklist caps it (commonly 150) that is a separate cut which
would supersede the abstract wording just agreed with the editor.

**7c. Markup convention for pure length edits.** Deletions leave no trace, but
condensed sentences are technically second-round changes. Two options:

1. Mark condensed sentences `\revsecond{}`. Consistent with Rule 2, but turns
   much of the Introduction blue for what is an editorial trim.
2. Leave length-only edits unmarked, and record in `revision_history.md` that
   the pass was editorial rather than reviewer-driven.

Recommendation: option 2, except that text surviving inside an existing `\rev{}`
span keeps its wrapper, and relocated marked text keeps its macro in its new
location. **Author decision needed.**

---

## 8. Execution checklist (per edit)

1. Apply to `latex/sections/*.tex` (marked-up source). Main-legend edits go in
   `latex/sections/figure_legends.tex`.
2. Apply the same edit, without macros, to
   `revision_submission/00_submit_new/Main_Manuscript_Revised_LaTeX_Source/sections/*.tex`.
   Main-legend edits likewise go to `sections/figure_legends.tex`.
   The two sources still differ by roughly 59 words of retained copy-edit, so
   match each file's local wording rather than pasting one string into both.
3. Supplementary sources are unaffected unless an ED legend is used for T2-3.
4. Re-run the word count and record the new counted total.
5. Re-check the three `\mschange{}` quotes still match the manuscript exactly.
6. Compile `latex/main.tex` and the submission source with
   `latexmk -pdf -interaction=nonstopmode -halt-on-error`; confirm 0 undefined
   citations, 0 undefined references, and check the page count.
7. Log the pass in `revision_history.md` with affected reviewer points, files
   changed, what changed, and type.

---

## 9. Summary

| Stage | Cut | Running total |
|---|---:|---:|
| Baseline | | 4,359 |
| Tier 1 after context/style review (10 items, `..._review_v2.pdf`) | 365 | 3,994 |
| Tier 1B (6 items, `..._review_tier1b.pdf`) | 134 | 3,860 |
| Tier 2, mostly relocation to legends | ~360 required | ~3,500 |

Tier 1 removes duplication and Methods restatement. Tier 2 moves supporting
detail into uncounted legends rather than deleting it. Together they reach the
target without losing a single result, statistic, or citation.
