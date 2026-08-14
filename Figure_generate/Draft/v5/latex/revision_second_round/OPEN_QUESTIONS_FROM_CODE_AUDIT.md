# Open questions from the code audit

Prepared 2026-07-29, while rebuilding the public code repository for R1's
code-availability comment.

Rebuilding the analysis from the archived data surfaced four points that need an
author's judgement before resubmission. Two touch text already written for this
revision round, so they are on the critical path. Two are lower stakes.

None of them changes a conclusion of the paper. Three are wording or reporting
questions; one is a data-integrity issue in a supplementary file.

---

## 1. The simulation design described in the manuscript may not match what was run

**CLOSED 2026-08-08 by author decision — no manuscript change.** The `num_C = 2`
notebooks in the tree are demonstration code, not the production runs behind the
published panels. The four-community, 54-species-pool design described in Methods and
in the R1-7 response stands as written. The cache-overwrite caveat below is why the
tree cannot show this on its own.

**Priority: high — this text was written for the current revision round.**

### What the manuscript says

Methods:

> From a pool of 54 species, we assembled four non-overlapping parental
> communities of 12 species each (no shared species per pair), yielding six
> pairwise coalescence events per replicate.

Results, added this round as `\revsecond` in answer to R1-7:

> We repeated this four-community procedure 200 times at μ = 0.6, yielding
> 200 × 6 = 1,200 random coalescence events

### What the code shows

Every simulation notebook calls `InitializeCommunityPool(N, num_C, num_S, ...)`
with **`num_C = 2`**. Reading the `commuityLibrary.xlsx` written by each run,
across 26 cached simulation sessions in `Main_Fig_2`, `Main_Fig_6`,
`Main_Fig_7` and `Main_Fig_9`:

| Communities per replicate | Sessions |
|---|---|
| 2 | 26 |
| 4 | 0 |

Pool sizes are 24, 30, 48, 72, 90, 96 and 120 — always exactly
2 × species-per-community. **No session uses a 54-species pool.**

Three further observations point the same way:

- `Data/VectorDecomposition`, written by the vector-decomposition notebook, is
  12 μ values × 100 replicates = **1,200 simulations in total** — a natural
  reading of "1,200" that is not 1,200 per μ.
- Re-running the model at μ = 0.6, the two-community configuration best
  reproduces the published Fig. 2b:

  | Configuration | n | Dominance | Mixture | Restructuring |
  |---|---|---|---|---|
  | 2 communities, pool 24, 1,200 reps | 1,200 | 59.7% | 15.0% | 25.3% |
  | 4 communities, pool 48, 200 reps | 1,200 | 61.3% | 16.2% | 22.5% |
  | 4 communities, pool 54, 200 reps | 1,200 | 57.4% | 17.0% | 25.6% |
  | **published** | **1,200** | **61%** | **13%** | **26%** |

- Supplementary Note 2 reports the assembly effect over **600 paired pre/post
  summaries** with `t_599`. 300 replicates × 2 communities gives exactly 600.

### Why it matters

R1 asked precisely this question:

> Is there a reason why this procedure is necessary, as opposed to just
> directly sampling 1200 pairs of parental communities?

The revision answered by asserting the four-community design. If the runs were
two-community, the honest answer is the opposite: yes, pairs were sampled
directly, and both the Methods text and the R1-7 response need correcting.

### Caveat

`commuityLibrary.xlsx` and `parameter.xlsx` are overwritten on every run, so
these files record the *last* run in each directory, not provably the runs
behind the published panels. A four-community sweep could have been run and its
cache overwritten. But no four-community code path exists anywhere in the tree.

### What is needed

Confirmation from whoever ran the simulations of whether a four-community,
54-species-pool sweep was ever run. If not, Methods and the R1-7 response both
need revising before resubmission.

---

## 2. Methods describes the similarity metric as cosine similarity

**CLOSED 2026-08-08 by author decision — no manuscript change.** The Methods wording
stands as written. Accepted risk, recorded so it is not rediscovered: a reader
implementing the Methods text literally obtains Dominance fractions of 31/51/69%
against the published 39/65/76%. Reopen only if a reviewer or the editor raises it.

**Priority: high — affects reproducibility of the central metric.**

Methods states:

> Similarity was computed as cosine similarity between community composition
> (relative-abundance) vectors

The implementation is not a cosine similarity. It expresses the coalesced
community in the basis spanned by the two parental vectors, solving the 2×2 Gram
system and rescaling the coefficients onto the unit sphere. The two agree only
when the parental communities share no species — which experimentally they
generally do.

The practical consequence: implementing the Methods text literally gives
Dominance fractions of 31% / 51% / 69% against the published 39% / 65% / 76%.
A reader attempting to reproduce the classification from the paper alone cannot.
Using the actual decomposition reproduces the published values exactly.

**Suggested fix:** one or two sentences in Methods describing the decomposition,
or a pointer to the Supplementary Methods normalization section. Low cost, and
it forecloses a reproducibility complaint.

---

## 3. Figure 5b, Base medium — RESOLVED, no action needed

Recorded here because it was previously listed as an open question.

The recomputed Base value differed from the published 51% by nine percentage
points. The cause was in the re-implementation, not the manuscript: the
published panel covers the **12-species parental communities only** and
averages over individual cultures, whereas the re-implementation pooled all
three richness classes and averaged replicates within each community first.

With the original selection restored, all three media reproduce:

| | Published | Recomputed |
|---|---|---|
| Nutr− | 44 ± 2% | 43.8 ± 2.1% |
| Base | 51 ± 5% | 51.1 ± 5.1% |
| Nutr+ | 67 ± 4% | 66.9 ± 4.2% |

## 3b. Extended Data Fig. 6 reports n = 83 for Nutr+, where every other count is 90

**RESOLVED 2026-08-08 — this item was wrong. n = 83 is correct for Nutr+.**

The figure is Extended Data Fig. **7** after the 2026-07-31 renumbering.

Re-running `analyze_pairwise_correlations_per_event` with `common_setup.exception_list`
applied reproduces the published caption exactly on all three panels:

| Panel | n | Δ | p | Caption |
|---|---|---|---|---|
| Nutr− | 90 | 0.0164 | 0.307 | n = 90, Δ = 0.016, p = 0.307 ✓ |
| Base | 83 | 0.2354 | <0.001 | n = 83, Δ = 0.235 ✓ |
| Nutr+ | **83** | **0.1407** | <0.001 | n = 83, Δ = 0.141 ✓ |

Δ = 0.141 is the value obtained from the 83-event set, which is what makes 83 the
self-consistent reading.

Event accounting, 94 wells per medium. Nutr−: 4 dropped by the ≥3-species validity
filter, the same 4 the QC list drops, so 90. Base: 6 with no sequence data, 5 QC, so 83.
Nutr+: 7 dropped by the validity filter, 4 QC (P6-02, P6-47, P6-57, P6-74), so 83.
Base and Nutr+ both landing on 83 is a coincidence of different filters, **not** a value
copied across from Base.

Nutr+ legitimately has 90 events for outcome classification in Fig. 4d and 83 for this
metric; the difference is the ≥3-species requirement on the coalesced community, which
outcome classification does not impose. The caption now says so explicitly.

**Why this item got it wrong:** the re-implementation applied the QC exclusions but not
the ≥3-species filter, giving n = 90 with Δ = 0.134, which matches neither the figure nor
the data.

**Real bug found while resolving this**, still open: `plot_correlation_barplots_clean.py`
imports `Coalescence_data` from `common_setup` but never applies `exception_list`, so
re-running it yields 90/88/87 with Δ = 0.016/0.230/0.136 and silently includes nine
QC-failed wells. That run produced the `correlation_summary_clean.csv` mismatch recorded
in `CAMPAIGN.md` 10.4. The deployed artwork carries only significance stars, so no figure
is affected, but the script should apply the exclusion list before it is next run.

---

### Original text of this item, retained for history

**Priority: medium — a reported sample size.**

The Extended Data Fig. 6 caption gives the three event counts as *n* = 90
(Nutr−), 83 (Base), 83 (Nutr+). Figure 4d gives 90 / 83 / 90, and the outcome
table reproduces 90 / 83 / 90 exactly.

Reimplementing the selection-correlation metric with the original's
event-validity filters — an event is dropped when neither parent contributes
two assignable species, or either contributes none, or a pair class comes out
empty — reproduces Nutr− at n = 90 and Base at n = 83, but leaves Nutr+ at 90,
not 83. The effect size also differs slightly there: Δ = 0.134 against a
published 0.141, while Nutr− (0.016) and Base (0.235) match exactly.

Two readings. Either the Nutr+ panel applies a further exclusion not present in
the code I could find, or 83 was carried across from the Base entry in error
and the true value is 90. The Δ difference is mild evidence for the first.

Neither reading changes the conclusion: the Nutr+ separation is significant
(p < 0.001) under both.

**What is needed:** confirmation of the Nutr+ event count for that panel.

---

## 4. Taxonomy sheet misaligned in `processed_Sequences_natural.xlsx`

**Priority: medium — data integrity, no known effect on results.**

The natural-community sequence file has **130 abundance columns in sheet 1 but
124 taxonomy rows in sheet 2**, so past the first dropped index, ASV column *k*
does not correspond to taxonomy row *k*.

Cause: the `Filtering` helper in `PostProcessingSequences_natural.m` applies a
Shannon-diversity criterion that removes entries from the ASV index vector
without removing the corresponding columns from the abundance matrix. On the
synthetic data the criterion selects nothing and the two stay aligned; on the
natural data it selects six.

Sheet 1 is unaffected, so Fig. 6 and every composition analysis are correct —
these reproduce the published values exactly.

**What is needed:** confirmation that no figure assigns taxonomic names to
natural-community ASVs. If one does, its labels are wrong and need regenerating.

---

## Also worth noting

Two items found and resolved, recorded here because they were previously
undocumented anywhere:

- **The quality-control exclusion list** (22 wells) existed only inline in the
  figure notebooks. It is what makes the outcome fractions match the published
  values, including the event counts n = 90/83/90. It is now a documented
  constant in the public code. Consider a sentence in Methods stating that
  samples failing culture or sequencing were excluded, since a reader working
  from the deposited tables would otherwise obtain n = 92/88/94.

- **The reverse-read error model** in the DADA2 workflow is learned from the
  forward filtered files (`learnErrors(filtFs)` where `filtRs` was intended).
  The effect is likely negligible — the manual ASV merge step absorbs
  over-splitting, and the composition tables reproduce exactly — but note that
  the merge uses hardcoded column indices, so correcting the error model and
  re-running would require rebuilding that merge map by hand. Recorded in the
  public repository rather than silently patched.
