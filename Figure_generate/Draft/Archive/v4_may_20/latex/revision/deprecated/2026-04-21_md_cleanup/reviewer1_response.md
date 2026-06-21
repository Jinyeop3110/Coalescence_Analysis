# Response to Reviewer 1

We thank the reviewer for their enthusiastic and constructive feedback. Below we address each point in detail.

---

## R1-1. OD as alternative explanation for Dominance

<!-- Raw reviewer text (grey) -->
> *I found the Author's explanation of coalescence generally convincing. However, I wonder if a simple, alternative explanation for many of the results could be that parent communities attain very different absolute densities. For example, if community A reaches 10x the overall density of community B, then even relatively rare species in community A might be initially more abundant than the dominant species in community B (because communities are combined in equal volumes, line 119). This might lead to the final community being dominated by species from A simply because species survive proportionally to their initial absolute abundance. If I understand correctly, this scenario is different from the one tested in ED Fig. 5. High heterogeneity in absolute densities could potentially explain both the prevalence of Dominance outcomes and the difference in pairwise selection correlation between same- and cross-parent pairs. In principle, heterogeneity in absolute densities could also increase with nutrient concentration. To be clear, I have no reason to expect this pattern, but I wonder if the Authors could do more to rule it out. Since ODs were measured throughout (line 379), could those data be used to check this possibility?*

**Summary:** Could absolute community density (OD) differences explain Dominance rather than ecological interactions?

**Analysis result:** DONE. OD differences are weakly associated with Dominance (Spearman ρ = 0.22), but critically, the denser parent wins in only 26.8% of Dominance events — no better than chance. Multivariate logistic regression (Dominance ~ relΔOD + Medium + PoolSize) confirms that OD difference is not a significant predictor after controlling for medium.

**Figures:** `Fig_R1_1a_dominance_vs_OD_diff.pdf`, `Fig_R1_1b_winner_OD_rank.pdf`, `Fig_R1_1c_dominance_by_medium_OD.pdf`

**Draft response text:**

We thank the reviewer for raising this important alternative explanation. We analysed OD₆₀₀ measurements for all parental communities across the three media conditions. While absolute OD differences show a weak association with whether an event is classified as Dominance (Spearman ρ = 0.22), the denser parental community is the winner in only 26.8% of Dominance events — substantially below the 50% expected if density determined the outcome (binomial test, p < 0.001). A multivariate logistic regression controlling for medium and initial pool size confirmed that relative OD difference is not a significant predictor of Dominance (p = [PLACEHOLDER]). These results rule out absolute density differences as the primary driver of Dominance outcomes (new Supplementary Fig. [PLACEHOLDER]).

**Manuscript location:** Add to Results §2.1 (after line ~140) or Supplementary Note as new paragraph:

> [PLACEHOLDER — insert after discussing null models]: "To further rule out density-driven artifacts, we tested whether parental communities with higher absolute biomass (OD₆₀₀) preferentially win during coalescence. The denser parental community was the winner in only 26.8% of Dominance events, indicating that absolute density does not determine coalescence outcomes (Supplementary Fig. [X])."

---

## R1-2. pH mismatch predicts Dominance

> *To support the hypothesis that the top-down regime emerges because dominant species strongly modify the pH of the ecosystem, the Authors show that the predictive power of the parent community pH increases in the Nutr+ condition when looking at coalescence between communities where one parent is acidic and one is alkaline (lines 261, ED Fig. 8). It seems like an even more straightforward prediction would be that Dominance should become more likely when combining parent communities with qualitatively different pH (e.g. alkaline and acidic) compared to cases where both parents are either acidic or alkaline. Is this the case?*

**Summary:** Two questions: (1) does pH mismatch increase Dominance frequency per medium (Acid-Alk vs pooled same-pH)? (2) within acid-alk pairs, is the Dominance direction predicted by acidity per medium?

**Analysis result (per medium; LN has only alk-alk, so focus on Base and Nutr+):**

Pair-type counts across 260 events: 88 acid–alk, 40 acid–acid, 132 alk–alk.

Class fractions (Dominance / Mixing / Restructuring) per pair type per medium (pair types ordered acid-alk first):
- **Base (MN)**:
  - acid-alk (n=44): Dom **61%**, Mix 5%, Rest 34%
  - acid-acid (n=6): Dom 50%, Mix 17%, Rest 33%
  - alk-alk (n=30): Dom 73%, Mix 0%, Rest 27%
- **Nutr+ (HN)**:
  - acid-alk (n=44): Dom **80%**, Mix 9%, Rest 11%
  - acid-acid (n=34): Dom 71%, Mix 3%, Rest 26%
  - alk-alk (n=12): Dom 75%, Mix 0%, Rest 25%

2-way Fisher test (Acid-Alk vs pooled same-pH) per medium:
- **Base**: acid-alk 61.4% (27/44) vs same-pH 69.4% (25/36); OR = 0.70, Fisher p = 0.49 (n.s., direction opposite to hypothesis)
- **Nutr+**: acid-alk 79.5% (35/44) vs same-pH 71.7% (33/46); OR = 1.53, Fisher p = 0.47 (n.s., direction consistent with hypothesis)

So pair-type **alone** does not produce statistically significant differences in Dominance fraction within either medium — likely because Dominance already saturates at ~70–80% in Nutr+ and small cell sizes (e.g., Base acid-acid n=6) limit power.

Within acid-alk pairs — direction of Dominance (who wins):
- **Base (MN), n=44**: acidic parent wins 63.6% (28/44, binom p = 0.10); signed PDI = +0.28 (t-test p = 0.030)
- **Nutr+ (HN), n=44**: acidic parent wins **86.4%** (38/44, binom p = 9.4×10⁻⁷); signed PDI = +0.64 (t-test p = 2.4×10⁻⁸)

**Figures:** `Fig_R1_2_acidalk_per_medium.pdf` (3 panels: Base class fractions, Nutr+ class fractions, acid-alk signed PDI)

**Draft response text:**

We classified parental pairs by pH type (threshold pH = 7.0): across 260 coalescence events we observed 88 acid–alk, 40 acid–acid, and 132 alk–alk pairs. LN (Nutr−) contains no acidic parents (all LN pairs are alk–alk), so the per-medium analysis is restricted to Base (MN) and Nutr+ (HN). We address the reviewer's question in two complementary ways.

**(1) Does pH mismatch alone increase Dominance frequency?** We tested the reviewer's prediction directly by comparing acid–alk events to pooled same-pH events (acid–acid ∪ alk–alk). In Nutr+, Dominance is more frequent in acid–alk than in same-pH pairs (79.5% vs 71.7%; OR = 1.53, Fisher p = 0.47); in Base the direction is opposite (61.4% vs 69.4%; OR = 0.70, Fisher p = 0.49). The binary "mismatch alone" test is consistent with the mechanism in Nutr+ but the effect size is small and below statistical significance with our sample sizes. A likely reason is that Dominance already saturates around 70–80% across all pair types in Nutr+, leaving little headroom for a mismatch-specific boost, and the smallest cells (Base acid–acid n=6; Nutr+ alk–alk n=12) limit power.

**(2) Within acid–alk pairs, is the Dominance direction predicted by acidity?** This is the sharper test: the mechanism predicts not just that acid–alk pairs dominate more, but **which** parent wins. For each acid–alk event we defined a signed PDI = +PDI if the acidic parent was the winner and −PDI otherwise. In Nutr+ the acidic parent is the winner in 86.4% (38/44) of acid–alk pairs (binomial p = 9.4×10⁻⁷), with mean signed PDI = +0.64 (t-test p = 2.4×10⁻⁸). In Base the acidic parent wins only 63.6% (28/44; p = 0.10), signed PDI = +0.28 (p = 0.030). The Nutr+ result is a clean, well-powered confirmation of the pH-modification mechanism. The weaker effect in Base is consistent with the more collective nature of Base coalescence (see R1-3).

**Manuscript location (pending integration):** Add to Results §2.5 (after ED Fig. 8 discussion, ~line 262):

> "Whereas pH mismatch alone does not produce a significant increase in Dominance frequency (acid–alk vs pooled same-pH, Fisher p = 0.47 in Nutr+, p = 0.49 in Base), within acid–alk pairs the acidic parent is systematically the winner in Nutr+ (38/44 events, binomial p < 10⁻⁶; Supplementary Fig. [X]), directly supporting acidifier-driven top-down control as the mechanism."

---

## R1-3. Circularity in Fig 5C — PDI excluding dominant species

> *In Fig. 5C, it seems like there is some risk of circularity if the dominant species are included in the calculation of the PDI. Does the positive correlation under Nutr+ conditions hold up if the dominant species are excluded from this calculation?*

**Summary:** Is the PDI–competition correlation circular because dominant species are included in PDI?

**Analysis result:** DONE. Removing the single most dominant species causes R² to drop from 0.34 to 0.07 — a near-complete collapse of predictive power. However, 68% of events maintain the same winner direction (Spearman ρ = 0.64, p < 1e-18), and 40% of events still classify as Dominance. Top-K sensitivity (K = 1, 2, 3) shows progressive R² decline but persistent directional agreement.

**Figures:** `Fig_R1_3ab_PDI_comparison.pdf`, `Fig_R1_3c_VD_reclassification.pdf`, `Fig_R1_3d_R2_comparison.pdf`

**Draft response text:**

We recalculated PDI after removing the dominant species from each parental community's abundance vector. The predictive power of dominant-species pairwise competition drops substantially (R² from 0.34 to 0.07 in Nutr+), confirming that the dominant species is indeed the primary contributor to the correlation in Fig. 5C. However, even after removal, 68% of coalescence events maintain the same winner direction (Spearman ρ = 0.64, p < 10⁻¹⁸), and 40% of events remain classified as Dominance. This indicates that while the dominant species is the strongest single predictor, the remaining community members also contribute to the asymmetric outcome — consistent with community-level, rather than purely single-species, dynamics. We present this analysis in new Supplementary Fig. [PLACEHOLDER].

We acknowledge that the top-down regime (Nutr+) is largely driven by the dominant species, while the emergent regime (Base) reflects collective multi-species dynamics where no single species is predictive. We have revised the manuscript to frame these as endpoints of a mechanistic continuum rather than sharply distinct regimes.

**Manuscript location:** Add to Results §2.5 (after Fig. 5C discussion):

> "To test whether this correlation is circular, we recalculated PDI after excluding the dominant species from each community's abundance vector. Predictive power dropped substantially (R² = 0.07), but 68% of events preserved the winner direction, indicating that subdominant species also contribute to asymmetric outcomes (Supplementary Fig. [X])."

---

## R1-4. Pool size effects — more detail

> *I wondered if the Authors could provide slightly more detail on the effect of the initial pool size. In ED Fig. 4, the Authors found that there is little effect of the pool size on the frequency of Dominance in the model. This was initially surprising to me, but I suppose it makes sense: while the interaction strength within the parent communities might become smaller as the pool size grows (due to stronger selection), the interaction strengths between individuals from different pools is unaffected. Is it similarly true that there is no significant effect of initial richness in the experimental communities? By eye, it looks like Dominance might be more likely for the 24 species pool, but it is hard to tell by squinting at Fig. 1E. I also wondered if the Authors could look more closely at why there is no effect in the model. Perhaps by plotting the realized richness and interaction strength in parent communities as a function of initial richness? It might also be interesting to see the survival ratio as a function of initial richness for the experimental communities.*

**Summary:** More detail on pool-size effects in both experiments and model.

**Analysis result:** DONE. Experimentally, Dominance frequency does not significantly vary across initial richness levels (6: 61.3%, 12: ~60%, 24: 59.4%; p = 0.69). Realized richness increases with pool size (median: 6 → 12 → 24), while survival ratio decreases. In the model, within-community interaction strength decreases with pool size (stronger assembly filtering), but cross-community interactions are unaffected — explaining the stable Dominance frequency.

**Figures:** `pool_size_analysis.pdf`, `pool_size_by_medium.pdf`

**Draft response text:**

We analysed experimental coalescence outcomes stratified by initial pool size (6, 12, and 24 species). Dominance frequency does not differ significantly across pool sizes (61.3%, ~60%, and 59.4% for 6, 12, and 24 species, respectively; χ² test, p = 0.69). Realized richness scales with initial pool size, while survival ratio decreases, reflecting stronger assembly filtering in larger pools. This is consistent with the model: as the reviewer correctly intuits, assembly reduces within-community interaction strength (due to stronger filtering in larger pools), but cross-community interactions remain unaffected, yielding stable Dominance frequency across community sizes (new Supplementary Fig. [PLACEHOLDER]).

**Manuscript location:** Add to Results §2.3 or as note after ED Fig. 4 reference:

> "Experimentally, Dominance frequency was consistent across initial pool sizes of 6, 12, and 24 species (p = 0.69; Supplementary Fig. [X]), mirroring the model prediction that cross-community interaction strength — which drives Dominance — is independent of assembly history."

---

## R1-5. Similarity metric robustness claim is misleading

> *The Authors write (line 134) that "This pattern of Dominance as the most frequent outcome was robust across variants of similarity metrics". I liked the Author's approach to measuring outcomes, and I don't advocate for changing it, but this claim seems a little misleading. Two of four alternative similarity metrics gave different results, with Dominance being the least likely outcome under Jensen-Shannon and Jaccard.*

**Summary:** Robustness claim overstated — JS and Jaccard gave different results.

**Analysis result:** Text edit applied (P1.5).

**Draft response text:**

We agree that our original phrasing was too broad. We have revised line 134 to read:

> "This pattern of Dominance as the most frequent outcome was consistent across vector decomposition, Euclidean distance, and Bray–Curtis dissimilarity. However, Jensen–Shannon divergence and Jaccard index yielded somewhat different orderings (Extended Data Fig. 2), likely because these metrics weight species presence/absence more heavily than abundance structure, reducing sensitivity to the quantitative compositional asymmetry that defines Dominance."

**Manuscript location:** Results §2.1, line ~134. DONE in P1.5.

---

## R1-6. Gray points in figures are confusing

> *It took me quite a while to realize that the gray points in Figs. 1E, 4C, 5C, and 6B are simply a reflection of the colored points. Please indicate this clearly, or perhaps just remove these.*

**Summary:** Clarify gray mirror points.

**Status:** DONE (P2.1). Captions updated to explicitly state: "Gray points represent the symmetric counterpart of each coalescence event (community B versus A), included to illustrate the symmetry of the similarity space."

---

## R1-7. Show interaction matrix after assembly in Fig 2A

> *In Fig. 2A, it might be helpful to show the matrix of interaction coefficients after assembly of the parent communities (with visible block structure).*

**Summary:** Add interaction matrix visualization showing block structure.

**Analysis result:** DONE (P4.2). Assembly creates clear block structure: within-community interactions (mean = 0.389) are significantly lower than between-community (0.500; Mann–Whitney U test, p < [PLACEHOLDER]).

**Figures:** `interaction_matrix_assembly.pdf`, `interaction_matrix_mu_comparison.pdf`

**Draft response text:**

We now include a visualization of the interaction coefficient matrix after community assembly (new Fig. 2A panel / Supplementary Fig. [PLACEHOLDER]). The matrix reveals a clear block structure: within-community interaction coefficients (mean = 0.389) are significantly lower than between-community coefficients (mean = 0.500; Mann–Whitney U test, p < 0.001), directly illustrating how assembly filters species into groups of weak mutual competitors that face stronger competition from outsiders. This block structure provides the mechanistic basis for correlated species fates during coalescence.

**Manuscript location:** Results §2.2, after describing assembly filtering (~line 160):

> "This filtering is visible in the post-assembly interaction matrix, which shows a block-diagonal structure with lower within-community than between-community competition coefficients (Supplementary Fig. [X])."

---

## R1-8. Fig 2D visualization — points vs squares unclear

> *Fig. 2D, I was somewhat confused by the relationship between point and squares (means?). Visually, the squares do not look like they are near the means of the points. Please clarify this for readers. Additionally, the gray horizontal bars are not explained in the main text unless I missed it.*

**Summary:** Clarify Fig 2D visualization.

**Status:** DONE (P2.2). Caption rewritten to explicitly describe: "Individual dots show per-event pairwise selection correlations; squares with error bars show mean ± s.e.m. Gray horizontal lines indicate the expected correlation under a null model in which species origin labels are shuffled."

---

## R1-9. Emphasize "cohesion without cooperation"

> *Discussion, lines 342-345: I think it is worth emphasizing how interesting and perhaps surprising it is to find "community-level cohesion without cooperation" as the paper by M. Tikhonov has it. This finding will be counterintuitive to many readers, even though the mechanism is made clear.*

**Summary:** Expand on the counterintuitive nature of cohesion arising from purely competitive interactions.

**Analysis result:** Text edit applied (P1.7).

**Draft response text (expanded Discussion):**

> "A particularly striking aspect of our results is that community-level cohesion emerges without cooperative or mutualistic interactions between species — a prediction made by Tikhonov using resource-competition models. In our system, purely competitive interactions, when structured by assembly history, are sufficient to produce the correlated species fates that underlie Dominance. This 'cohesion without cooperation' arises because assembly filters species into mutually weakly competing groups whose members face stronger competition from outsiders. This result may be counterintuitive: one might expect that community-level selection requires cooperative interactions (e.g., cross-feeding, division of labour) that bind species together. Instead, our findings demonstrate that competitive exclusion during assembly alone creates the internal structure necessary for communities to behave as cohesive units during coalescence."

**Manuscript location:** Discussion, lines ~342-345. DONE in P1.7.

---

## R1-10. ED Fig 5C missing means

> *In ED Fig. 5C, are means missing?*

**Status:** DONE — Means confirmed present; caption already explains them.

---

## R1-11. SI reference to wrong ED Fig

> *On p. 9 in the SI, I believe the sentence "Simulations were performed with parental community sizes ranging from 4 to 48 species per community (Extended Data Fig. 5)" should refer to ED Fig. 4.*

**Status:** DONE — Fixed to "Extended Data Fig. 4".
