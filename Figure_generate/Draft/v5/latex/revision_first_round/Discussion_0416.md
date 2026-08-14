# Discussion Notes — 04/17 Meeting with Jeff

## Overall Assessment

- Reviewer 1: Generally satisfied. Requests several new analyses for richer interpretation.
- Reviewer 2: Positive but significant feedback on framing and technical aspects. Core question: "Community-level selection vs. Environmental selection."
- Reviewer 3: Neutral. Critical concern about similarity metric. Wants new metrics/analyses justifying community-level selection beyond just prevalence of Dominance.
- No new experiments requested. All questions are valid and constructive with clear suggestions for additional analysis.

**Plan:** Add analyses, prepare initial response by ~April 31, then discuss.

---

## PI Discussion Points (04/17)

1. **Can community OD explain PDI?** — Test whether absolute density differences between parental communities drive Dominance outcomes.

2. **Pairwise model is not the only framework** — The fact that the pairwise gLV model explains most results does not mean it's the only valid framework. Include a new model (e.g., pH-based model).

3. **Provide gLV failure modes clearly** — Where does the model break down? Be explicit.

4. **Pure pH model → acidic pH wins. Does this contradict gLV?** — Check whether a simple "acidic always wins" rule contradicts gLV predictions.

5. **Simulate geometric factor / asymmetric factor** — Address Reviewer 3's dimensionality concern through simulation. Sounds good.

6. **Very clearly introduce why we picked gLV model** — Motivate the model choice up front.

7. **Show aspects of data not explained by model** — For scientific honesty and compatibility with other models.

---

## Reviewer 1

### R1-1. OD as alternative explanation for Dominance
If community A has 10x the density of community B, rare species in A may outnumber dominant species in B after 1:1 mixing. Dominance could reflect initial absolute abundance advantage.

**Action:** Correlation between parental community OD ratio and PDI. Correlation between species absolute abundance (OD × relative abundance) and retention.

### R1-2. pH mismatch predicts Dominance?
If pH modification drives top-down regime, Dominance should be more likely when combining acidic vs alkaline communities compared to same-pH pairs.

**Action:** Compare Dominance % for pH-mismatched vs same-pH parental pairs.

### R1-3. Circularity in Fig 5C — PDI excluding dominant species
If dominant species are included in PDI, correlation with dominant species competition may be circular.

**Action:** Recalculate PDI excluding dominant species. Redo Fig 5C regression with new PDI.

### R1-4. Pool size effects — more detail
Is there an effect of initial richness (6, 12, 24) in experiments? Why no effect in model?

**Action:** Dominance fraction vs initial richness (experiments). Realized richness, survival ratio, interaction strength vs initial richness (model). Caveat: limited pool size variations; simulations show no clear trend across S=6–24.

### R1-5. Similarity metric robustness claim is misleading
Line 134: "robust across variants" but JS and Jaccard gave different results.

**Action:** Revise text to clearly note JS and Jaccard are outliers. Additional analysis if possible: why are they outliers?

### R1-6. Gray points in figures are confusing
Gray mirror points in Figs 1E, 4C, 5C, 6B not clearly explained.

**Action:** Already modified figures.

### R1-7. Show interaction matrix after assembly in Fig 2A
Would help see block structure.

**Action:** Already modified figures.

### R1-8. Fig 2D — points vs squares unclear
Squares (means) don't visually match points. Gray horizontal bars not explained.

**Action:** Already modified figures.

### R1-9. Emphasize "cohesion without cooperation" in Discussion
Counterintuitive finding deserves more emphasis. Connect to Tikhonov.

**Action:** Emphasize relation with Tikhonov et al.

### R1-10. ED Fig 5C missing means
**Action:** Fixed.

### R1-11. SI reference to wrong ED Fig
Should be ED Fig. 4, not 5.

**Action:** Fixed.

---

## Reviewer 2

### R2-1. Nutrient enrichment ≠ interaction strength (MAJOR)
Nutrient enrichment simultaneously affects carrying capacities, metabolic rates, environmental modification (pH), and competition/facilitation balance. Cites Duan et al. (2025): resource supply can cancel out in effective gLV mapping. Suggests reframing in terms of "interaction intensity and environmental feedbacks."

**Action:**
1. Clarify that our framework defines interaction strength relative to normalized abundance, not per-capita basis. This accounts for biomass/dominance shifts.
2. Emphasize interaction strength as a coarse-grained universal parameter that could include multiple underlying mechanisms, generalizing our argument to broader contexts.
3. Show that our definition and argument agrees with Duan et al. (2025), Goldford et al. (2018), Estrela et al. (2021).
4. Modify the main text with clarifying argument.

### R2-2. Evidence for community-level selection — alternative explanations
Dominance + correlated persistence could arise from shared environmental filtering, correlated traits, pH tolerance. Nutr+ regime may be strong environmental filtering, not community-level selection. Also: clarify ecological meaning of "failed invasion" — connect to invasion fitness.

**Action:** Add subsection on "Alternative Drivers of Community Dominance," specifically addressing nutrient-rich regime as filtering case. Argument: each species can grow and sustain in our medium, so survival/extinction cannot be simply interpreted by environmental change or filtering — dominant factor is interactions with other community members. Clarify repeatedly that our framework defines interactions to incorporate various mechanisms including environmental modifications, fitness co-selections, etc.

### R2-3. Classification of coalescence outcomes — continuous measures
Outcomes are continuous, not discrete. Present continuous similarity measures alongside categorical. The dot-product vs Jaccard divergence in Nutr- is informative.

**Action:** Acknowledge that boundary choice could change classification results. Present continuous similarity measures alongside categorical outcomes. Edit text for biological interpretation of "restructuring." Edit text discussing dot-product vs Jaccard comparison — different metrics bring different biases (e.g., varying weight on low-abundance species). Also connect to Reviewer 3's dimensionality concern.

### R2-4. Pairwise selection correlation interpretation
Closely related to co-occurrence patterns. Not clear whether correlations reflect ecological interactions, shared environmental responses, or methodological effects. Suggests linking to invasion fitness in gLV framework.

**Action:** Connected to R2-1. Potential argument: each species can grow and sustain in our medium, so survival/extinction is driven by interactions. Clarify that our framework defines interactions to incorporate various mechanisms.

### R2-5. Natural community pre-selection effects
Lab stabilization in defined media may drive convergence toward limited functional guilds (cf. Goldford et al. 2018), making natural communities functionally similar to synthetic ones.

**Action:** Discuss pre-selection effects more explicitly. Clarify taxonomic/functional convergence during stabilization.

### R2-6. gLV model framing
Limited to competitive interactions, no pH dynamics. Frame as phenomenological, not mechanistic. Clarify biological interpretation of interaction coefficient distributions.

**Action:** Explicitly frame gLV as phenomenological, not mechanistic. Connect interaction strength with biological interpretations.

### R2-Minor
- Improve pairwise correlation visualization. → Fixed.
- Specify pH measurement protocol. → Added to supplementary.
- Clarify interaction coefficient distribution interpretation. → Fixed.
- Consistent terminology/notation. → Fixed.
- Typo: "generalis ability" → "generalisability". → Fixed.

---

## Reviewer 3

### R3-1. Dimensionality artifact in similarity metrics (CRITICAL)
Positive unit vectors are more likely to be close to orthogonal in lower dimensions → Dominance is geometrically expected in low-diversity communities. ED Fig. 3 compares distributions, but many individual "Dominance" cases may be compatible with a simple null model. Need case-by-case comparison with additive null n_C,null = n_A + n_B.

**Action:**
1. Diversity-adjusted dominance class boundaries: Scale threshold using dimensionality normalization proportional to 1/√(N_eff), where N_eff = inverse Simpson index.
2. New metric: case-by-case comparison to additive null n_C,null = n_A + n_B. Quantify deviation from additive null toward single parental state. Continuous statistical measure of "asymmetry" complementing categorical results.

### R3-2. Interaction strength, diversity, and Dominance frequency
Increasing μ decreases diversity, and lower diversity geometrically increases Dominance. Is the Dominance increase just a diversity artifact? Also: how does richness change across media conditions?

**Action:** Run analysis from R3-1 across nutrient conditions and simulations. Provide convincing evidence that Dominance effect is real beyond statistical artifacts.

### R3-3. gLV limited to competitive interactions — natural communities
Facilitative interactions (cross-feeding) are important. Natural communities show more Restructuring. Claims in §2.6 and Discussion should be toned down.

**Action:** Modify the main text. Tone down claims.

### R3-4. "Interaction strength" vs "competition strength" terminology
In gLV context, all interactions are competitive. Term "interaction strength" may confuse.

**Action:** Emphasize that prior works (Robert May, Jiliang Hu, etc.) use "interaction strength" as standard terminology.
