# SI Structure Audit — Multi-Agent Discussion
**Date:** 2026-06-02
**Scope:** Supplementary Notes 1–5 · Extended Data Figs 1–8 · Supplementary Figs 1–44
**Method:** Three parallel agents with distinct analytical roles

| Agent | Role | Verdict |
|-------|------|---------|
| A — Skeptical Reviewer | Scientific argument quality | **Major revision** |
| B — First-time Reader | Navigability & self-containment | **Difficult to navigate** |
| C — Consistency Checker | Internal consistency | **Minor issues** |

---

## Agreed Findings (flagged by 2+ agents — highest confidence)

These should be addressed first.

---

### AG-1 [CRITICAL] Note 4 cites none of its own figures (Supp Figs 5–7)
**Agents:** A + B

Note 4 ("Nutrient perturbation and pairwise invasion resistance") is the empirical keystone linking pairwise physiology to community-level Dominance. It now reads as two paragraphs — one that describes the assay setup (with a cross-reference to Supplementary Methods) and one that states results — but **Supp Figs 5, 6, and 7** (the pairwise invasion matrices for Nutr−, Base, Nutr+) are never cited in the Note body. A reader of Note 4 cannot verify the directional claim or trace the data.

**Fix:** Insert figure citations in Note 4 paragraph 2: reference Supp Figs.~5--7 when stating the exclusion-frequency gradient across nutrient conditions.

---

### AG-2 [CRITICAL] Note 4 has no mechanistic bridge from pairwise exclusion to community Dominance
**Agents:** A + B

Note 4's final paragraph states: *"The frequency of competitive exclusion increased with nutrient concentration, consistent with the coalescence outcome patterns observed in community experiments."* This is the central mechanistic claim of the paper, yet the logical step connecting pairwise exclusion rates to community-level Dominance probability is **never stated**. Why does higher pairwise exclusion produce community-level Dominance rather than higher Restructuring? The reasoning is assumed self-evident.

**Fix:** Add 1–2 sentences in Note 4 explaining the link: higher pairwise exclusion during coalescence means that species from the stronger community more consistently exclude cross-community invaders, producing correlated species fates (Dominance) rather than ecological reorganization (Restructuring).

---

### AG-3 [CRITICAL] No SI roadmap paragraph
**Agents:** A (implicit) + B (explicit)

There is no opening paragraph or section in the SI that tells the reader what the five Notes cover and how they relate to each other. A reader landing on the SI cold must infer its logic from five titles alone.

**Fix:** Add a brief paragraph at the top of the compiled SI (in `supplementary.tex` or as a preamble in `supplementary_methods.tex`) listing the five Notes with one sentence each, e.g.:
> *"Supplementary Note 1 defines the outcome classification framework and null models. Note 2 characterizes assembly history effects. Note 3 reports simulation robustness. Note 4 presents pairwise invasion assay results. Note 5 rules out alternative mechanisms."*

---

### AG-4 [CRITICAL] Supp Figs 2 and 3 not cited in Note 3 body
**Agents:** A (implied — Note 3 conclusion unsupported) + B (explicit)

Note 3 ("Simulation Robustness") cites only Supp Fig 4 (distribution shape) and ED Fig 4 (species-number ablation) in its body. **Supp Figs 2 and 3** (growth-rate heterogeneity and carrying-capacity variation ablations) are never mentioned in Note 3. These are Note 3's primary robustness figures yet they have no narrative anchor in the SI.

**Fix:** Insert citations in Note 3: after the sentence describing growth-rate and K-variation robustness, add "(Supplementary Figs.~2--3)".

---

### AG-5 [WARNING] Note 3 opens mid-argument, missing purpose statement
**Agents:** A + B

Note 3's first sentence begins: *"In the main simulations, we use μ as a minimal one-parameter control…"* This presupposes the reader already knows what the main simulations showed and why robustness is being tested. The "why this Note exists" question is never answered.

**Fix:** Add a 1-sentence opener: *"We tested whether the Dominance transition observed in the main simulations is robust to alternative model assumptions, including growth-rate heterogeneity, carrying-capacity variation, alternative interaction-coefficient distributions, and facilitative interactions."*

---

### AG-6 [WARNING] Note 1 opens with equations, no purpose statement
**Agents:** A + B

Note 1 dives immediately into the PDI/cosine-similarity math (Eq. 1) without a preamble explaining why this Note exists. A reader cannot tell from the opening whether Note 1 is defining the classification system for the first time, defending a methodological choice, or presenting null models.

**Fix:** Prepend 1 sentence: *"This Note formalizes the outcome classification framework, demonstrates robustness to alternative similarity metrics, and tests whether Dominance can arise from passive additive mixing via null models."*

---

## Agent A Only — Scientific Argument Quality

---

### A-1 [CRITICAL] Note 2: "more variable results" unquantified
Note 2, line ~14: *"The Nutr− condition showed more variable results, likely due to weaker competitive interactions in nutrient-limited environments."* The Supp Fig 19 caption shows stacked bar plots with percentages — no variance or confidence intervals. The variability claim is unquantified and the mechanistic attribution ("weaker competitive interactions") is an interpretation with no direct test or forward reference.

**Fix:** Either quantify the variability (e.g., add s.e.m. to the Note) or soften the language to "the Nutr− condition showed a different distribution of outcomes (Supplementary Fig.~19), consistent with weaker competitive interactions (see Supplementary Note~4)."

---

### A-2 [WARNING] Note 1: n=83 not identified as Base medium only
Note 1, null model paragraph: *"Experimental data showed mean parental asymmetry of 0.698 (n = 83)."* The n=83 applies only to Base medium. A reader of Note 1 in isolation cannot tell this is not the full experiment-wide sample.

**Fix:** Add "(Base medium)" after n=83.

---

### A-3 [WARNING] Note 5: OD-PDI negative association stated without mechanistic bridge
Note 5 states the higher-OD community won only 37% of Base Dominance events and that ΔOD was *strongly negatively* associated with PDI in Nutr+. This counterintuitive direction is stated as a one-sentence conclusion without explanation. A reader may wonder whether the negative association itself is a confound (e.g., acidifying species grow to lower OD but win via pH).

**Fix:** Add a sentence acknowledging and addressing the counterintuitive direction: *"The negative association between OD and winning likely reflects that acid-producing species, which tend to dominate in Nutr+, grow to lower final OD than alkalizers."*

---

### A-4 [WARNING] Note 2: within-parent metric not connected to Δ metric
Note 2 uses a separate "excess same-parent shared fate" metric (Pearson r = 0.870, Supp Fig 28) without explaining how it relates to the Δ = ρ_same − ρ_cross metric used in the rest of Note 2 and in ED Fig 5. The logical connection between the two metrics is assumed.

**Fix:** Add one sentence in Note 2 explaining the relationship: *"This within-community metric measures the same phenomenon as the same-minus-cross pairwise selection correlation (Δ) used in the main analysis but is computed independently of cross-community pairs, providing a conservative lower-bound estimate."*

---

### A-5 [NOTE] Note 5: null result stated without power consideration
Note 5, line ~15: Fisher's exact test for pH-pairing effect gives p=0.49, stated as evidence against the hypothesis. No power analysis or equivalence test is reported for what may be a small subset of events.

**Fix:** Add a parenthetical: *"(note: this test has limited power given the subset sizes; the null result should be interpreted as absence of a large effect rather than absence of any effect)."*

---

## Agent B Only — Navigability

---

### B-1 [WARNING] 25 of 44 Supplementary Figures never cited in any Note body

The following figures have no citation in Notes 1–5. Figures cited only in the main text are expected; what is problematic are figures with no Note anchor and captions that don't explain their own purpose:

| Cluster | Figures | Problem |
|---------|---------|---------|
| Invasion matrices | Figs 5, 6, 7 | Note 4's natural home — never cited there |
| Robustness ablations | Figs 2, 3 | Note 3's natural home — never cited there |
| Assembly history | Fig 27 | Directly relevant to Note 2 — not cited |
| Rank-abundance / time series | Figs 10–17 | Purely descriptive; no Note anchor |
| Natural communities | Figs 20–27, 44 | No Note home |

**Fix (priority):** At minimum, cite Figs 5–7 in Note 4, Figs 2–3 in Note 3, and Fig 27 in Note 2. The purely descriptive figures (10–17) are acceptable without Note citations if their captions are self-contained.

---

### B-2 [WARNING] Note ordering is partially illogical

Current order: Classification (1) → Assembly history (2) → Simulation robustness (3) → Invasion assays (4) → Alternative models (5).

Notes 2 and 3 use the interaction-strength framework before Note 4 establishes empirical evidence for it. A reader building their understanding progressively would expect invasion evidence (Note 4) to precede the robustness analysis (Note 3) and the assembly-effect analysis (Note 2).

**Fix (discussion item):** Consider reordering to: 1 → 4 → 2 → 3 → 5. This is a structural judgment call requiring author input, but the current order creates backward dependencies.

---

### B-3 [WARNING] ED Fig 3 and ED Fig 7 captions don't state "why this figure exists"

- **ED Fig 3**: The caption states the result (additive null → Mixture, Wilcoxon p) and now ends with "See Supplementary Note~1 for full analysis." But it does not state the scientific purpose: *why* is an additive null model needed? A standalone reader doesn't know.
- **ED Fig 7**: The caption states the result (assembly → higher Dominance) but gives no sentence explaining the logic of why assembly history should matter.

**Fix:** Add one purpose sentence to each caption. For ED Fig 3: *"This null model tests whether Dominance can arise from passive additive mixing of unequal parental composition vectors rather than from correlated competitive selection."* For ED Fig 7: *"This figure tests whether the assembly process itself—not interaction strength alone—shapes the probability of Dominance by filtering species before coalescence."*

---

### B-4 [WARNING] No cross-references between Notes

No Note refers readers to another Note for related content, except Note 5 → Note 1. Notes 2, 3, and 4 operate as independent documents.

**Fix:** Add brief cross-references. For example: Note 4 should end with "see Supplementary Note~5 for tests of whether biomass heterogeneity or pool-size effects confound this result"; Note 3 should reference Note 2 for the assembly-filter mechanism that underlies the robustness analyses.

---

### B-5 [NOTE] Note ordering Note 4 too short to stand alone

Note 4 is now 9 lines after the W-8 edit. It reads more like a methods supplement than a scientific note. Consider whether it should be merged into Note 1 (which also addresses the invasion-resistance → outcome relationship) or expanded with a more complete analysis paragraph.

---

## Agent C Only — Internal Consistency

---

### C-1 [CRITICAL] Note 3 / Supp Fig 39 — facilitative fraction mismatch

Note 3 states the facilitative-tail sweep covers f ∈ {0, 0.10, 0.20, 0.40, 0.80}. At f = 0.80, P(α_ij < 0) = 0.80/(2+0.80) ≈ 28.6%. The Supp Fig 39 caption states the range reaches *"22.2%."* These are irreconcilable:
- 22.2% corresponds to f ≈ 0.571, which is not in the stated set
- f = 0.80 gives 28.6%, not 22.2%
- f = 0.40 gives 16.7%, also not 22.2%

**Fix:** Verify the actual f values used in the simulation script and correct whichever location is wrong. This is a numerical error in either the Note or the caption.

---

### C-2 [NOTE] Terminology drift: "interaction strength" vs "interaction-strength parameter"

| Note | Usage |
|------|-------|
| Note 2 | "interaction strength" (bare), 5 instances |
| Note 3 | "interaction-strength parameter μ" (consistent) |
| Note 5 | Mixed — both bare and with "parameter" |
| Supp Figs 2, 3 captions | "increasing interaction strength" (bare) |

The bare form is never ambiguous in context (μ is always cited nearby), but the phrasing is not uniform. **Suggested standard:** use "interaction-strength parameter μ" on first mention in each Note, then "μ" alone thereafter.

---

### C-3 [NOTE] "competitive exclusion" vs "failed invasion" terminology drift

Note 4 uses "competitive exclusion" as the primary label for failed invasions. Supp Figs 5–7 captions use "failed invasion frequency." The paper's established terminology (used in the main text) is "failed invasions." Note 4 should be updated to use "failed invasion" as the primary term.

---

### C-4 [NOTE] Supp Fig 4 caption omits variance formula

Note 3 describes the Gaussian and Gamma distributions as having "matched variance μ²/3." Supp Fig 4 caption says only "same mean and variance." A reader of the caption cannot verify the parameterization. Not a contradiction, but an omission worth filling.

---

## Panel Verdicts and Overall Recommendation

| Agent | Verdict |
|-------|---------|
| A (scientific argument) | **Major revision** — Note 4 is the keystone and currently lacks citations and mechanistic reasoning |
| B (navigability) | **Difficult to navigate** — 25/44 figures orphaned from Notes; no roadmap; illogical Note order |
| C (internal consistency) | **Minor issues** — one numerical mismatch (Fig 39 facilitative fraction), minor terminology drift |

### Overall: Major revision before submission

The SI is internally consistent and all figures exist. The scientific analyses are sound. However, the SI has two structural problems that a reviewer or reader will notice immediately:

1. **Note 4 is broken** — the empirical bridge between pairwise physiology and community outcomes (the paper's central mechanism) is stated without citations, without quantification, and without the reasoning step connecting the two levels. This is the highest-priority fix.

2. **The SI is not self-navigable** — more than half the figures are unanchored in any Note body, there is no roadmap, and Notes 1 and 3 do not explain their own purpose in their opening paragraphs. A referee reading only the SI cannot follow the argument without the main text.

---

## Action checklist (priority order)

### Must fix (submission-blocking)
- [ ] **AG-1** Add Supp Figs.~5--7 citations to Note 4 body
- [ ] **AG-2** Add mechanistic bridge sentence to Note 4 (pairwise exclusion → community Dominance)
- [ ] **AG-3** Add SI roadmap paragraph to `supplementary.tex` preamble
- [ ] **AG-4** Add Supp Figs.~2--3 citations to Note 3 body
- [ ] **C-1**  Verify and correct facilitative-fraction number in Note 3 or Supp Fig 39 caption

### Should fix (argument quality)
- [ ] **AG-5** Add purpose sentence to Note 3 opening
- [ ] **AG-6** Add purpose sentence to Note 1 opening
- [ ] **A-1**  Quantify or soften "more variable results" in Note 2
- [ ] **A-2**  Add "(Base medium)" qualifier to n=83 in Note 1 null model paragraph
- [ ] **B-3**  Add purpose sentence to ED Fig 3 and ED Fig 7 captions
- [ ] **B-4**  Add cross-references between Notes

### Author judgment required
- [ ] **B-2**  Note reordering: consider moving Note 4 before Notes 2–3
- [ ] **B-5**  Note 4 length: expand or merge into another Note?
- [ ] **A-3**  Add mechanistic explanation for counterintuitive OD-PDI negative association
- [ ] **A-4**  Connect within-parent metric to Δ metric in Note 2
- [ ] **A-5**  Add power caveat to Note 5 null result

### Low priority
- [ ] **C-2**  Standardize "interaction-strength parameter μ" across Notes 2, 3, 5
- [ ] **C-3**  Replace "competitive exclusion" with "failed invasion" in Note 4
- [ ] **C-4**  Add variance formula to Supp Fig 4 caption
- [ ] **B-1**  Add Note citations for Supp Figs 2–3, 5–7, 27 (covers orphaned clusters)
