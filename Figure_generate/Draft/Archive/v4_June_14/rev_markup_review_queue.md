# `\rev{}` Edit Review Queue

Scope: revised text in the files included by `latex/main.tex`.

Use this as a one-by-one decision queue. Tell me an item ID, and I will bring up that item with context and options before applying any change.

## Queue

| ID | Location | Importance | Confidence | Status |
|---|---|---|---|---|
| R01 | `latex/sections/title_abstract.tex:29` | High | High | Applied |
| R02 | `latex/sections/introduction.tex:15` | High | High | Applied |
| R03 | `latex/sections/results.tex:18` | High | High | Pending |
| R04 | `latex/sections/results.tex:18` | High | High | Applied |
| R05 | `latex/sections/results.tex:24` | Medium | High | Applied |
| R06 | `latex/sections/results.tex:24` | High | High | Applied |
| R07 | `latex/sections/results.tex:44` | Low | High | Applied |
| R08 | `latex/sections/results.tex:79` | Medium | High | Applied |
| R09 | `latex/sections/results.tex:81` | Medium | High | Applied |
| R10 | `latex/sections/results.tex:81` | Medium | High | Applied |
| R11 | `latex/sections/results.tex:98` | Medium | High | Applied |
| R12 | `latex/sections/results.tex:100` | Low | Medium | Applied |
| R13 | `latex/sections/results.tex:100` | Medium | High | Applied |
| R14 | `latex/sections/results.tex:100` | High | High | Applied |
| R15 | `latex/sections/results.tex:113` | High | High | Applied |
| R16 | `latex/sections/results.tex:120` | Medium | High | Skipped |
| R17 | `latex/sections/discussion.tex:8` | High | High | Skipped |
| R18 | `latex/sections/discussion.tex:14` | High | High | Skipped |
| R19 | `latex/sections/methods.tex:25` | Medium | High | Applied |
| R20 | `latex/sections/methods.tex:32` | Low | Medium | Skipped |
| R21 | `latex/sections/methods.tex:39` | Low | High | Applied |

---

## R01

**Location:** `latex/sections/title_abstract.tex:29`

**Original**

```tex
\rev{These patterns also appear in taxonomically richer communities derived from natural environmental samples.}
```

**Suggested**

```tex
\rev{A similar nutrient-dependent shift toward Dominance was also observed in taxonomically richer, laboratory-stabilized communities derived from natural environmental samples.}
```

**Why:** Avoids overextending the natural-community data to all mechanisms/patterns.

**Confidence:** High

**Importance:** High

---

## R02

**Location:** `latex/sections/introduction.tex:15`

**Original**

```tex
\rev{A phenomenological generalized Lotka--Volterra (gLV) model with minimal pairwise interactions reproduces these experimental observations, and the patterns also appear in taxonomically richer communities derived from natural environmental samples.}
```

**Suggested**

```tex
\rev{A phenomenological generalized Lotka--Volterra (gLV) model with randomly sampled pairwise competitive interactions recapitulates the observed Dominance/Mixture transition, and a similar nutrient-dependent shift toward Dominance appears in taxonomically richer, laboratory-stabilized communities derived from natural environmental samples.}
```

**Why:** “Minimal pairwise interactions” is ambiguous, and “reproduces these experimental observations” is broader than what the model supports.

**Confidence:** High

**Importance:** High

---

## R03

**Location:** `latex/sections/results.tex:18`

**Original**

```tex
\rev{Restructuring denotes low parental retention: the coalesced community is not well explained by the parental communities or their combination, and may reflect a new stable composition produced by previously unseen cross-community species interactions.}
```

**Suggested**

```tex
\rev{Restructuring denotes low parental retention: the coalesced community has low parental retention under this metric, consistent with substantial post-coalescence reorganization that could involve new cross-community interactions.}
```

**Why:** Low retention does not by itself establish stability or causation by cross-community interactions.

**Confidence:** High

**Importance:** High

---

## R04

**Location:** `latex/sections/results.tex:18`

**Original**

```tex
\rev{Crucially, Dominance provides outcome-level evidence for origin-correlated persistence: one parental community displaces the other while retaining its internal compositional structure, indicating that its species persist collectively.}
```

**Suggested**

```tex
\rev{Dominance is an endpoint pattern consistent with origin-correlated persistence: the coalesced community closely resembles one parent and not the other. We test collective species persistence below using pairwise selection correlations.}
```

**Why:** Endpoint similarity alone does not prove displacement dynamics or collective persistence.

**Confidence:** High

**Importance:** High

---

## R05

**Location:** `latex/sections/results.tex:24`

**Original**

```tex
\rev{This pattern of Dominance as the most frequent outcome was robust under similarity metric choices including Euclidean distance and Bray--Curtis dissimilarity (Extended Data Fig.~2).}
```

**Suggested**

```tex
\rev{This pattern of Dominance as the most frequent outcome was robust to alternative compositional metrics, including Euclidean distance and Bray--Curtis dissimilarity (Extended Data Fig.~2).}
```

**Why:** Euclidean distance and Bray--Curtis are distance/dissimilarity metrics, so “similarity metric choices” is imprecise.

**Confidence:** High

**Importance:** Medium

---

## R06

**Location:** `latex/sections/results.tex:24`

**Original**

```tex
Together, these controls support that Dominance reflects correlated species selection within parental communities.
```

**Suggested**

```tex
Together, these controls argue that Base-medium Dominance is not explained by passive additive mixing or abundance skew alone, supporting an origin-correlated persistence interpretation together with the pairwise fate-correlation analyses below.
```

**Why:** The null controls argue against passive mixing, but do not alone establish correlated species selection.

**Confidence:** High

**Importance:** High

---

## R07

**Location:** `latex/sections/results.tex:44`

**Original**

```tex
We simulated 1,200 random coalescence events at \rev{interaction-strength parameter value} $\mu = 0.6$
```

**Suggested**

```tex
We simulated 1,200 random coalescence events at \rev{an interaction-strength parameter value of} $\mu = 0.6$
```

**Why:** Fixes missing article/preposition.

**Confidence:** High

**Importance:** Low

---

## R08

**Location:** `latex/sections/results.tex:79`

**Original**

```tex
we conducted additional coalescence experiments by removing or augmenting glucose and urea in the Base medium used in \figref{fig:fig1} (Methods).
```

**Suggested**

```tex
we conducted additional coalescence experiments by removing glucose and urea from the Base medium used in \figref{fig:fig1} or increasing their concentrations (Methods).
```

**Why:** “Removing ... in” is awkward; “augmenting” is less direct than “increasing their concentrations.”

**Applied as**

```tex
we conducted additional coalescence experiments by removing glucose and urea from the Base medium or increasing their concentrations (Methods).
```

**Rebuttal response:** Updated the matching quoted manuscript text in `latex/revision/response/reviewer2_response.tex`.

**Confidence:** High

**Importance:** Medium

---

## R09

**Location:** `latex/sections/results.tex:81`

**Original**

```tex
\rev{We then performed coalescence experiments in Nutr$-$ and Nutr$+$ media using the same parental community library to examine whether this nutrient-dependent change in invasion resistance is accompanied by the predicted shift in coalescence outcomes.}
```

**Suggested**

```tex
\rev{We then performed coalescence experiments in Nutr$-$ and Nutr$+$ media using the same strain library and parental-community assembly scheme to examine whether this nutrient-dependent change in invasion resistance is accompanied by the predicted shift in coalescence outcomes.}
```

**Why:** “Parental community library” is unclear and overlaps confusingly with “strain library.”

**Applied as**

```tex
\rev{We then performed coalescence experiments in Nutr$-$ and Nutr$+$ media using the same parental-community assembly scheme to examine whether this nutrient-dependent change in invasion resistance is accompanied by the predicted shift in coalescence outcomes.}
```

**Rebuttal response:** Checked active response files; no active rebuttal quote used the old “parental community library” wording.

**Confidence:** High

**Importance:** Medium

---

## R10

**Location:** `latex/sections/results.tex:81`

**Original**

```tex
including biomass heterogeneity and initial pool-size effects
```

**Suggested**

```tex
including parental-community biomass heterogeneity and initial richness effects
```

**Why:** In the experimental context, “pool size” sounds simulation-specific; the relevant experimental variable appears to be initial richness.

**Confidence:** High

**Importance:** Medium

---

## R11

**Location:** `latex/sections/results.tex:98`

**Original**

```tex
indicating that it is not solely a PDI circularity artifact.
```

**Suggested**

```tex
indicating that it is not solely an artifact of using those same dominant species in the PDI calculation.
```

**Why:** “PDI circularity artifact” is compressed jargon.

**Confidence:** High

**Importance:** Medium

---

## R12

**Location:** `latex/sections/results.tex:100`

**Original**

```tex
they \rev{are predictive of} the community's overall pH
```

**Suggested**

```tex
their identities \rev{predict} the community's overall pH
```

**Why:** Species are not themselves “predictive”; their identities/phenotypes predict pH.

**Confidence:** Medium

**Importance:** Low

---

## R13

**Location:** `latex/sections/results.tex:100`

**Original**

```tex
\rev{A complementary pH-pairing analysis showed that pH effects do not explain the full Dominance pattern: acid--alk pairings were not significantly enriched for Dominance relative to pairings in which both parental communities had similar pH in either Base or Nutr$+$ medium (Fisher's exact tests, $p = 0.49$ and $p = 0.47$; Supplementary Fig.~19).}
```

**Suggested**

```tex
\rev{A complementary acidic--alkaline parental-community pair analysis showed that parental-community pH contrast alone does not explain the full Dominance pattern: acidic--alkaline pairings were not significantly enriched for Dominance relative to pairings in which both parental communities had similar pH in either Base or Nutr$+$ medium (Fisher's exact tests, $p = 0.49$ and $p = 0.47$; Supplementary Fig.~19).}
```

**Why:** “pH-pairing” is nonstandard, “acid--alk” is informal, and “pH effects” is too broad for this analysis.

**Applied as:** Superseded by the current Results paragraph, which now states that the pH-based analysis addresses winner direction in high-contrast acidic--alkaline pairings and does not by itself account for the full Dominance pattern.

**Confidence:** High

**Importance:** Medium

---

## R14

**Location:** `latex/sections/results.tex:100`

**Original**

```tex
pH effects do not explain the full Dominance pattern
```

**Suggested**

```tex
parental-community pH contrast alone does not explain the full Dominance pattern
```

**Why:** The analysis tests parental pH contrast, not all possible pH-mediated effects.

**Applied as:** Superseded by the current Results paragraph, which limits the claim to a pH-based analysis of winner direction in high-contrast acidic--alkaline pairings and states that this analysis does not by itself account for the full Dominance pattern.

**Confidence:** High

**Importance:** High

---

## R15

**Location:** `latex/sections/results.tex:113`

**Original**

```tex
\subsection{\texorpdfstring{\rev{Interaction-dependent coalescence outcomes in natural sample-derived communities}}{Interaction-dependent coalescence outcomes in natural sample-derived communities}}
```

**Suggested**

```tex
\subsection{\texorpdfstring{\rev{Nutrient-dependent coalescence outcomes in natural sample-derived communities}}{Nutrient-dependent coalescence outcomes in natural sample-derived communities}}
```

**Why:** The natural-community experiment manipulates nutrient condition; interaction dependence is inferred.

**Confidence:** High

**Importance:** High

---

## R16

**Location:** `latex/sections/results.tex:120`

**Original**

```tex
\rev{These communities showed higher Restructuring fractions, possibly reflecting greater taxonomic diversity and more complex interaction networks. These results suggest that the nutrient-dependent increase in Dominance observed in synthetic consortia is also present in taxonomically richer natural sample-derived communities.}
```

**Suggested**

```tex
\rev{These communities showed higher Restructuring fractions than synthetic communities, possibly reflecting higher ASV richness, different enrichment histories, or unmeasured interaction structure. These results suggest that the nutrient-dependent increase in Dominance observed in synthetic consortia is also present in taxonomically richer natural sample-derived communities.}
```

**Why:** “Higher” needs a comparison, and “more complex interaction networks” is not directly measured.

**Confidence:** High

**Importance:** Medium

---

## R17

**Location:** `latex/sections/discussion.tex:8`

**Original**

```tex
\rev{Furthermore, predictability analyses suggest two routes associated with Dominance. In the top-down regime, dominant taxa and environmental feedbacks, including pH modification, may bias winner identity. In the emergent regime, collective multi-species dynamics govern outcomes and dominant-species-based prediction is insufficient.}
```

**Suggested**

```tex
\rev{Furthermore, predictability analyses suggest two routes to Dominance. In the top-down regime, dominant taxa and environmental feedbacks, including pH modification, may bias winner identity. In the emergent regime, outcomes are not well predicted by dominant-species assays, consistent with contributions from collective multi-species dynamics.}
```

**Why:** Poor dominant-species prediction supports consistency with collective dynamics, but does not prove that they “govern” outcomes.

**Confidence:** High

**Importance:** High

---

## R18

**Location:** `latex/sections/discussion.tex:14`

**Original**

```tex
\rev{Notably, and perhaps counterintuitively, our results demonstrate that community-level selection can emerge without cooperative interactions between species, consistent with predictions from Tikhonov's resource-competition models \citep{Tikhonov2016} and classical Lotka--Volterra theory \citep{May1972, Grilli2017}. Community-level selection is often attributed to cooperative mechanisms such as cross-feeding or division of labor. By contrast, our model shows that assembly history and competitive interactions can be sufficient to generate correlated species fates during coalescence.}
```

**Suggested**

```tex
\rev{Notably, and perhaps counterintuitively, our competition-only model demonstrates that origin-correlated persistence can emerge in the absence of explicit cooperative interactions, consistent with predictions from Tikhonov's resource-competition models \citep{Tikhonov2016} and classical Lotka--Volterra theory \citep{May1972, Grilli2017}. Community-level selection is often attributed to cooperative mechanisms such as cross-feeding or division of labor. By contrast, our model shows that assembly history and competitive interactions can be sufficient to generate correlated species fates during coalescence.}
```

**Why:** The empirical system may include facilitation/cross-feeding; the competition-only claim is supported by the model.

**Confidence:** High

**Importance:** High

---

## R19

**Location:** `latex/sections/methods.tex:25`

**Original**

```tex
\rev{In experimental analyses, the community composition vector was the ASV-abundance vector derived from these 16S profiles.}
```

**Suggested**

```tex
\rev{In experimental analyses, the community composition vector was the ASV relative-abundance vector derived from these 16S profiles.}
```

**Why:** Clarifies that this is not a raw count vector.

**Confidence:** High

**Importance:** Medium

---

## R20

**Location:** `latex/sections/methods.tex:32`

**Original**

```tex
\rev{Community pH was measured using a benchtop pH meter (Apera Instruments PH5500).}
```

**Suggested**

```tex
\rev{Culture pH was measured using a benchtop pH meter (Apera Instruments PH5500).}
```

**Why:** pH is measured for the culture medium/supernatant, not literally the community.

**Confidence:** Medium

**Importance:** Low

---

## R21

**Location:** `latex/sections/methods.tex:39`

**Original**

```tex
\rev{The Restructuring boundary is defined by $r^2 \leq 0.5$, equivalently a retention radius $r \leq 1/\sqrt{2}$ in the similarity map.}
```

**Suggested**

```tex
\rev{The Restructuring boundary is defined by $r^2 \leq 0.5$, equivalently by a retention radius $r \leq 1/\sqrt{2}$ in the similarity map.}
```

**Why:** Fixes the grammatical break after “equivalently.”

**Confidence:** High

**Importance:** Low
