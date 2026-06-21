# Response to Reviewer 2

We thank the reviewer for their thoughtful and constructive comments, which have significantly improved the conceptual clarity of the manuscript. Below we address each point.

---

## R2-1. Nutrient enrichment ≠ interaction strength (MAJOR)

> *The central claim of the paper is that increasing nutrient supply strengthens interactions, which in turn drives a shift toward community-level selection. While this is an appealing and intuitive interpretation, it may be overly simplified.*
>
> *Nutrient enrichment simultaneously affects multiple ecological processes, including: species' carrying capacities, metabolic rates, environmental modification (e.g. pH shifts), the balance of competition and facilitation.*
>
> *Indeed, the manuscript itself shows that pH modification by dominant taxa plays a strong role in the nutrient-rich regime. This suggests that the observed transition may reflect changes in environmental feedbacks and dominance structure, rather than a simple increase in pairwise interaction strength.*
>
> *This raises an important conceptual point: Is the observed shift in coalescence outcomes driven by increased interaction strength per se, or by other effects of resource enrichment?*
>
> *We therefore suggest reframing this result more broadly in terms of changes in interaction intensity and environmental feedbacks, rather than interpreting nutrient enrichment as a direct proxy for stronger interactions. This would align well with recent work highlighting the role of environmentally mediated interactions in microbial communities [Goldford et al., 2018, Estrela et al., 2021].*
>
> *From a consumer-resource perspective, it is also not mathematically self-evident that increasing resource supply monotonically increases effective pairwise interaction strengths. In our recent theoretical work [Duan et al., 2025], we show that when mapping mechanistic consumer-resource dynamics to effective Lotka-Volterra coefficients, the external supply rate can cancel out under broad conditions, provided that resources are not strictly limiting and metabolic strategies remain fixed.*
>
> *Under such conditions, resource enrichment increases total biomass but does not necessarily increase mean per-capita competition strength. Instead, enrichment restructures the interaction network through changes in equilibrium abundances and environmental feedbacks. This distinction is important, as it suggests that the observed transition may reflect a reorganisation of interaction structure rather than a simple scaling of interaction strength.*
>
> *A brief discussion of these issues would significantly strengthen the conceptual clarity of the manuscript.*

**Summary:** Nutrient enrichment is a complex perturbation — not simply equivalent to increasing the gLV parameter μ. Reframe "interaction strength" as a coarse-grained parameter encompassing multiple mechanisms. Cite Duan et al. (2025).

**Analysis result:** Text revisions applied (P1.11). References added: Duan et al. (2025, bioRxiv — Pawar group), Goldford et al. (2018), Estrela et al. (2021).

**Draft response text:**

We fully agree with the reviewer that nutrient enrichment is a multifaceted perturbation that cannot be reduced to a scalar increase in pairwise interaction coefficients. We have substantially revised the relevant sections to address this concern.

First, we now explicitly acknowledge that nutrient enrichment simultaneously affects carrying capacities, metabolic rates, environmental modification (e.g., pH shifts), and the balance of competitive and facilitative interactions, citing Duan et al. (2025) and Goldford et al. (2018). We frame the gLV parameter μ as a coarse-grained phenomenological proxy for the net intensity of competitive interactions, rather than a mechanistic parameter that maps directly to nutrient concentration.

Second, we clarify that our experimental proxy for interaction strength — the frequency of failed pairwise invasions — measures the population-level outcome of competition, integrating over all underlying mechanisms (resource competition, pH modification, metabolic interference). This definition is compatible with the reviewer's observation that enrichment restructures interaction networks rather than simply scaling them.

Third, we discuss that the monotonic increase in failed invasions with nutrient supply provides direct experimental evidence that the overall competitive environment intensifies across our nutrient gradient, even if the mechanistic basis differs from a simple increase in per-capita α coefficients. We cite Estrela et al. (2021) for the role of metabolic rules in shaping community assembly.

**Manuscript locations:**

Results §2.4, add after line ~195 (after introducing nutrient conditions):

> "We note that nutrient enrichment is a complex perturbation that simultaneously affects carrying capacities, metabolic rates, and the balance of competitive and facilitative interactions (Duan et al. 2025). It is therefore not equivalent to a simple increase in pairwise interaction coefficients. Nevertheless, higher nutrient concentration amplifies consumer–resource feedbacks and intensifies environmental modification (Ratzke et al. 2020). While nutrient enrichment is not a simple proxy for the gLV parameter μ, it consistently increased the frequency of failed pairwise invasions — our experimental proxy for the overall intensity of competitive interactions."

Discussion, expand existing paragraph (~line 380):

> "Our experimental design of using nutrient concentration to modulate interaction strength relies on the well-established observation that higher nutrient supply intensifies competitive exclusion in microbial communities (Hu et al. 2022, Ratzke et al. 2020). However, as noted by Duan et al. (2025), mapping mechanistic consumer–resource dynamics to effective Lotka–Volterra coefficients reveals that external supply rate can cancel out under broad conditions, suggesting that enrichment may restructure interaction networks rather than simply scale them. The gLV parameter μ therefore serves as a simplified scalar proxy for mean competitive intensity, and the mapping between nutrient concentration and μ is necessarily approximate. Nevertheless, the monotonic increase in failed pairwise invasions with nutrient supply provides direct experimental evidence that the overall competitive environment intensifies across our gradient."

DONE in P1.11.

---

## R2-2. Alternative explanations for community-level selection

> *The manuscript interprets dominance of one parental community and correlated persistence of its taxa as evidence for community-level selection. We find this interpretation interesting and potentially insightful, but it is not uniquely diagnostic on its own.*
>
> *Similar patterns could arise from: shared environmental filtering, correlated traits within parental communities, environmental modification (e.g. pH tolerance).*
>
> *In particular, the nutrient-rich regime appears consistent with strong environmental filtering imposed by a small number of dominant taxa, which may not require invoking selection acting at the level of the community as a unit.*
>
> *We therefore recommend clarifying the interpretation of "community-level selection," and explicitly discussing alternative mechanisms that could generate similar patterns. This distinction has been discussed in previous work on community coalescence and microbial assembly [Mansour et al., 2018, Rillig et al., 2015].*
>
> *Relatedly, we suggest clarifying the ecological meaning of "failed invasion." At present it is primarily used as a proxy for interaction strength, but it is also naturally interpretable as invasion resistance (i.e. whether a rare invader can establish). Framing this more explicitly in terms of invasion fitness would help connect the experimental results to ecological theory and may provide additional insight into the observed patterns.*

**Summary:** Dominance + correlated persistence is not uniquely diagnostic of community-level selection. Alternative mechanisms (environmental filtering, correlated traits, pH tolerance) could produce similar patterns. Clarify "failed invasion" in terms of invasion fitness.

**Analysis result:** Text revisions applied (P1.9). Invasion fitness analysis done (P4.3, `invasion_fitness_analysis.pdf`).

**Draft response text:**

We agree that correlated species persistence is not uniquely diagnostic of community-level selection, and we have added a dedicated paragraph in the Discussion addressing alternative mechanisms:

1. **Environmental filtering:** Species from the same parental community may share environmental tolerances (e.g., pH preference), causing them to respond similarly to conditions created by the dominant community. However, all 54 isolates in our library grow successfully in monoculture across all three media conditions, indicating that extinction during coalescence arises from interspecies interactions rather than environmental intolerance per se.

2. **Correlated traits:** Species within a parental community could converge on similar growth rates or competitive abilities. However, the gLV model — which assigns identical growth rates to all species — reproduces both Dominance and positive within-community selection correlation, indicating that trait homogeneity is not required.

3. **Assembly history effect:** The comparison between pre-assembled and directly assembled communities (ED Fig. 7) shows that shared assembly history, not just shared traits, contributes to correlated persistence.

4. **Nutr+ as environmental filtering:** We now explicitly acknowledge that the Nutr+ regime exhibits characteristics consistent with strong environmental filtering imposed by dominant pH-modifying taxa. We frame this as the "top-down regime" where community-level selection is mediated by a small number of keystone species.

Regarding "failed invasion," we now frame this as measuring invasion resistance — the inability of a rare species to establish in a resident community — and connect it to the concept of invasion fitness in the gLV framework (new Supplementary Fig. [PLACEHOLDER], `invasion_fitness_analysis.pdf`).

**Manuscript locations:**

Discussion, expanded alternative mechanisms paragraph (after ~line 355):

> [PLACEHOLDER — This paragraph has been substantially expanded in P1.9. Verify final wording integrates all four points above. Add reference to Mansour et al. 2018.]

Results §2.4, clarify "failed invasion":

> "The fraction of failed invasions — events where the invader remains below 1% relative abundance, interpretable as the invasion resistance of the resident — served as our proxy for the overall intensity of competitive interactions."

---

## R2-3. Classification — continuous measures

> *The classification into Dominance, Mixture, and Restructuring is useful and provides a clear framework for summarising outcomes. However, it depends on thresholding a continuous similarity measure.*
>
> *As noted in the broader literature [Mansour et al., 2018], coalescence outcomes often lie along a continuum rather than discrete categories. In addition, the distinction between mixture and restructuring is not entirely straightforward biologically, particularly because abundance changes contribute to classification.*
>
> *We suggest that the authors: present continuous similarity measures alongside categorical outcomes, clarify the biological interpretation of "restructuring".*
>
> *We also find the comparison between dot product and Jaccard metrics in Extended Data Fig. 2 potentially very informative. The divergence between these metrics in low-nutrient environments may itself provide evidence that species-level processes dominate in that regime, and this could be discussed more explicitly.*

**Summary:** Present continuous measures alongside categorical. Clarify "restructuring." Discuss dot-product vs Jaccard divergence.

**Analysis result:** DONE (P3.6). Continuous similarity scatter plots generated. Threshold sensitivity analysis done.

**Figures:** `scatter_retention_vs_PDI.pdf`, `marginal_distributions_by_medium.pdf`, `scatter_by_medium.pdf`, `bray_curtis_similarity.pdf`

**Draft response text:**

We now present continuous similarity measures (retention magnitude and PDI) alongside categorical outcomes in new Supplementary Fig. [PLACEHOLDER]. The continuous distributions confirm that the categorical classification captures robust trends: PDI distributions shift from unimodal (centred near 0.5) in Nutr− to bimodal in Base and Nutr+, consistent with a transition from species-level to community-level dynamics.

We have clarified the biological interpretation of Restructuring: it represents cases where the coalesced community converges to a novel compositional state not closely resembling either parent, likely arising from cross-community interactions that produce new stable configurations.

Regarding the dot-product vs Jaccard divergence: we now discuss that in Nutr− medium, the two metrics diverge because Jaccard (which weighs presence/absence) captures species-level turnover, while the dot product (which weighs abundance) is sensitive to quantitative shifts. This divergence itself supports the conclusion that species-level processes dominate under weak interactions, as the reviewer suggests.

We also performed a sensitivity analysis across multiple abundance thresholds (0.01%, 0.1%, 1%, 3.3%), confirming that our qualitative conclusions are robust to threshold choice.

**Manuscript locations:**

Results §2.1, add after classification description:

> "We note that these categories discretize a continuous spectrum. We present continuous retention magnitude and PDI distributions in Supplementary Fig. [X], which confirm that the transition from Mixture to Dominance is gradual and robust to threshold choice (Supplementary Fig. [Y])."

Discussion or Results §2.1, add on metric divergence:

> [PLACEHOLDER — draft sentence on dot-product vs Jaccard divergence in Nutr− as evidence for species-level processes]

---

## R2-4. Pairwise selection correlation interpretation

> *The pairwise "selection correlation" metric is an interesting attempt to quantify lineage-level coherence, but its interpretation remains somewhat unclear.*
>
> *It appears closely related to co-occurrence patterns, and it is not fully clear whether the observed correlations reflect ecological interactions, shared environmental responses, or methodological effects. We find this analysis potentially insightful, but its conceptual interpretation would benefit from clarification.*
>
> *We suggest adding a short paragraph linking this metric more explicitly to invasion fitness in a gLV framework. In that context, invasion fitness corresponds to the growth rate of a species when rare in a resident community. The pairwise invasion assays can then be interpreted as empirical approximations of invasion fitness in two-species systems, while coalescence outcomes reflect correlations in invasion success across many species.*
>
> *This would provide a unifying theoretical framework linking pairwise assays, community coalescence, and the notion of community-level selection.*

**Summary:** Link pairwise selection correlation to invasion fitness. Provide unifying framework.

**Analysis result:** DONE (P4.3). Invasion concordance analysis shows excess concordance correlates with μ (r = 0.870, p = 3.2e-08).

**Figures:** `invasion_fitness_analysis.pdf`, `invasion_fitness_distributions.pdf`

**Draft response text:**

We have added a paragraph connecting our pairwise selection correlation to the invasion fitness framework. In the gLV model, the invasion fitness of species i into a resident community is r_i − Σ_j α_ij n_j*, where n_j* is the resident equilibrium abundance. Species from the same pre-assembled community tend to have correlated invasion outcomes because assembly has filtered them into groups with low mutual competition (α_ij small within-community) but potentially high competition from outsiders (α_ij unfiltered between-community). We quantified this as "excess concordance" — the degree to which same-community species pairs share invasion outcomes beyond random expectation — and show that this measure increases monotonically with interaction strength μ (Pearson r = 0.870, p = 3.2 × 10⁻⁸; new Supplementary Fig. [PLACEHOLDER]).

This framework provides the unifying link the reviewer suggests: pairwise invasion assays approximate two-species invasion fitness; pairwise selection correlation during coalescence measures correlated multi-species invasion success; and the transition from uncorrelated to correlated invasion outcomes with increasing μ corresponds to the shift from species-level to community-level selection.

**Manuscript location:** Supplementary Note 4 (Pairwise Selection Correlation), add new paragraph:

> [PLACEHOLDER — insert theoretical connection to invasion fitness, referencing new Supplementary Fig.]

---

## R2-5. Natural community pre-selection effects

> *The inclusion of natural communities is an important strength of the study. However, the use of a common stabilisation phase in defined media may introduce pre-selection effects that reduce ecological heterogeneity across communities.*
>
> *In particular, incubating diverse natural communities in simplified media is known to drive convergence toward a limited set of functional guilds [Goldford et al., 2018]. As a result, the "natural" communities used here may already be filtered to resemble the synthetic communities, potentially contributing to the similarity of results across systems.*
>
> *We therefore suggest that the authors: discuss the potential effects of this pre-selection more explicitly, clarify the extent to which taxonomic or functional convergence occurs during the stabilisation phase.*

**Summary:** Lab stabilization may pre-select natural communities toward synthetic-like composition.

**Analysis result:** Text revision applied (P1.10).

**Draft response text:**

We agree that seven serial growth–dilution cycles in defined laboratory media likely selects for species that thrive under these specific culture conditions, potentially reducing effective diversity and making natural communities functionally more similar to our synthetic consortia. This pre-selection could contribute to the convergent coalescence patterns observed between natural and synthetic communities, as documented by Goldford et al. (2018) for similar serial-dilution protocols.

However, we note that: (1) natural communities retained higher ASV richness than synthetic communities (mean 13.7 vs 9.8 ASVs), indicating that substantial diversity persists after stabilization; (2) ASV overlap between communities from different samples remained low (Supplementary Figs. 22–25); and (3) the qualitative trend of increasing Dominance with nutrient concentration is preserved across both community types, which is the key claim.

We have expanded the Discussion caveat on this point and suggest that future work using culture-independent approaches or shorter stabilization periods could help disentangle laboratory adaptation from intrinsic ecological dynamics.

**Manuscript location:** Discussion, expanded pre-selection paragraph (~line 375). DONE in P1.10.

---

## R2-6. Frame gLV as phenomenological

> *The gLV model successfully reproduces the qualitative transition in coalescence outcomes and serves as a useful minimal framework. However, it is limited to purely competitive interactions and does not explicitly capture environmentally mediated effects such as pH modification.*
>
> *We therefore suggest framing the model more explicitly as a phenomenological rather than mechanistic description of the system.*
>
> *In addition, while the robustness analysis across interaction coefficient distributions is appreciated, a brief discussion of the biological interpretation of these distributions would be helpful. In particular, clarifying how the mean interaction strength parameter (μ) relates to underlying ecological processes would improve interpretability.*

**Summary:** Frame gLV as phenomenological. Clarify biological meaning of μ and interaction distributions.

**Analysis result:** Text revisions applied (P1.6, P1.13).

**Draft response text:**

We have revised the model description to explicitly frame the gLV as a phenomenological framework:

> "The gLV model serves as a phenomenological framework to explore how the statistical properties of interaction coefficients shape coalescence outcomes, rather than as a mechanistic model of the specific biochemical interactions (e.g., pH modification, metabolic cross-feeding, carrying capacity variation) underlying our experimental observations."

We have also added to the Supplementary Methods a paragraph clarifying the biological interpretation of the interaction coefficients:

> "Each α_ij represents the net per-capita effect of species j on species i's per-capita growth rate, encompassing both direct mechanisms (e.g., resource competition, interference) and indirect mechanisms (e.g., metabolite-mediated inhibition, pH modification). The mean interaction strength μ parameterizes the average intensity of interspecific competition, with larger μ corresponding to stronger average competitive suppression."

**Manuscript locations:** Results §2.2 (DONE in P1.6), Supplementary Methods (DONE in P1.13).

---

## R2-Minor

> *Improve the visualisation of pairwise correlation results, as the separation between groups is not visually clear.*

**Status:** DONE (P2.4). [PLACEHOLDER — confirm final styling choices: larger markers, violin plots, etc.]

> *Specify how pH was measured (e.g. continuously or at endpoints), and whether variability across replicates was assessed.*

**Status:** DONE. Added to Supplementary Methods.

> *Clarify the biological interpretation of the interaction coefficient distributions used in the theoretical model.*

**Status:** DONE (P1.13).

> *Ensure consistent terminology and notation throughout (e.g. "pairwise", "community-level", α_ij).*

**Status:** DONE (P1.3).

> *Correct minor typographical issues, including "generalis ability" -> "generalisability".*

**Status:** DONE (P1.1).
