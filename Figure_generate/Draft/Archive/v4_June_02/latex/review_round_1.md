# Critical Review - Round 1: Comprehensive Manuscript Assessment

---

## PART I: MAJOR CONCEPTUAL ISSUES

### 1. Definition and Operationalization of "Community-Level Selection"

**Core Concern:** The term "community-level selection" (CLS) is central to the argument, but the operationalization (one parental community dominating in similarity space) may not actually demonstrate *selection* at the community level.

#### Questions:
- How do you distinguish between (a) true community-level selection where emergent properties of the community are under selection, versus (b) coincidental co-retention of species from one parent because they share individually favorable traits (e.g., pH tolerance, growth rate)?
- The Gilpin (1994) and Tikhonov (2016) frameworks cited involve communities having "collective fitness"—but the gLV model with random interactions doesn't explicitly model any collective property. What exactly is being "selected" at the community level?
- Could the observed CLS simply reflect that species from one community happen to have higher individual fitness than those from the other, without any emergent group-level property being selected?
- The term "selection" implies a heritable, fitness-based process. In what sense is CLS "selection" rather than simply "competitive exclusion at the community scale"?

---

### 2. Circularity in the Assembly Effect Argument

**Core Concern:** The logic connecting assembly, internal coherence, and CLS may be circular or tautological.

#### Questions:
- If assembly removes strong competitors, wouldn't surviving community members simply not compete much with each other? Then isn't the coalescence outcome determined by which *cross-community* interactions are stronger, not by any within-community property?
- The positive selection correlation in Figure 2D (same-parent species pairs) could arise because species from the same parent share similar environmental tolerances (e.g., pH preference, nutrient requirements) rather than because they were "selected together" as a unit. How do you rule out this confound?
- Is "internal coherence" a cause of CLS, or simply a redescription of the observation that species from one community tend to survive together?
- You show that assembly reduces mean interaction strength within communities (Fig. 2C), but this doesn't necessarily imply coherence during coalescence—it could simply mean less internal competition. What is the causal mechanism linking reduced within-community competition to one-sided coalescence outcomes?

---

### 3. The "Emergent" vs "Species-Driven" Regime Distinction

**Core Concern:** The claim of two distinct mechanistic regimes (emergent vs species-driven) is based primarily on R² values from linear regression, which may not support the strong mechanistic claims made.

#### Questions:
- The difference between R² = 0.11 (Base) and R² = 0.49 (Nutr+) is interpreted as evidence for two qualitatively different regimes. But couldn't this simply reflect a continuous increase in dominant species influence rather than a regime transition?
- How do you define the boundary between "emergent" and "species-driven" regimes? Is there a critical R² threshold, or is this a post-hoc interpretation?
- R² = 0.11 in Base medium is called "emergent regime" but R² = 0.49 still leaves 51% of variance unexplained. Why isn't Nutr+ also partially emergent?
- The pH mechanism described (acidic communities winning 91% of matchups) suggests the outcome is determined by a *species-level trait* (pH modification ability), not by emergent community properties. Doesn't this undermine the "community-level selection" framing?
- If dominant species' pH modification determines outcomes, isn't this simply species-level selection where pH-modifying species happen to come from the same parent community?

---

### 4. pH as the Dominant Mechanism

**Core Concern:** The new data on pH (Supplementary Figs. S23-S25) suggests pH modification may be the primary driver, which has significant implications for the interpretation.

#### Questions:
- If acidic communities win 91% of matchups in Nutr+ (n=32), this seems like a strong, simple predictor. Why isn't pH modification the main story rather than "interaction strength"?
- Does pH modification confound the nutrient-interaction strength relationship? Higher nutrients → more metabolic activity → larger pH shifts → more exclusion. This isn't necessarily "stronger interactions" in the gLV sense.
- The gLV model has no pH dynamics. How can a model without the proposed mechanism (pH modification) reproduce the experimental patterns? Does this suggest pH is not actually necessary, or that the model captures the phenomenon for wrong reasons?
- Have you tested whether pH-neutral or buffered conditions would eliminate CLS even at high nutrient concentrations?

---

## PART II: METHODOLOGICAL ISSUES

### 5. Cosine Similarity as Outcome Metric

**Core Concern:** The choice and implementation of the similarity metric significantly affects outcome classification.

#### Questions:
- If one community has 2 dominant species at 45% each and another has 10 species at 10% each, won't the cosine similarity be heavily influenced by which dominant species survive?
- How sensitive are classifications (CLS vs Mixture vs Restructuring) to the choice of metric? The paper mentions Supplementary Fig. 4 shows robustness, but have you tested with Bray-Curtis dissimilarity, weighted UniFrac, or Jensen-Shannon divergence?
- What normalization procedure is used—L2 normalization (for true cosine similarity) or simple relative abundances?
- The 0.1% threshold for species presence—how was this chosen, and how sensitive are results to this cutoff?
- How are the boundaries between CLS, Mixture, and Restructuring defined in the similarity space? Are these arbitrary, or derived from some principled criterion?

---

### 6. The "Interaction Strength" Parameter (μ)

**Core Concern:** The model's interaction strength parameter may oversimplify real microbial interactions.

#### Questions:
- Real microbial communities include facilitation, cross-feeding, and metabolic dependencies—not just competition. How would predictions change if positive interactions were included?
- The gLV framework assumes pairwise interactions, but higher-order interactions are increasingly recognized as important. Have you considered extending the model?
- Why draw competition coefficients from a uniform distribution? Empirical interaction matrices often show different distributions (e.g., lognormal, with many weak and few strong interactions).
- What is the biological interpretation of μ in real systems? Is there a way to empirically estimate μ for natural communities beyond the invasion proxy?
- You set g_i = k_i = 1 for all species. How sensitive are results to heterogeneity in growth rates and carrying capacities?

---

### 7. Nutrient Concentration as Interaction Strength Proxy

**Core Concern:** The causal chain (higher nutrients → stronger competition → more CLS) involves multiple confounds.

#### Questions:
- Higher nutrients could also change: (a) growth rates differentially across species, (b) metabolic strategies, (c) pH modification magnitude, (d) carrying capacities, (e) resource competition type. How do you isolate "interaction strength" from these confounds?
- The invasion assay calibration (Fig. 4B) shows failed invasion frequency, but this could reflect competitive *asymmetry* rather than overall mean interaction strength. A system with many unidirectional competitive outcomes could have low μ but high exclusion rates.
- Have you measured actual pairwise interaction coefficients (e.g., via Friedman et al. or Venturelli et al. methods) rather than using invasion outcomes as a proxy?
- The calibration of experimental μ values (≈0.5, 0.7, 0.9 for Nutr−, Base, Nutr+) from failed invasion frequency—what is the functional form of this mapping, and how confident are you in these estimates?
- The Base medium has 5 g/L glucose and 4 g/L urea, while the Results section describes it as having "moderate interaction strength." But moderate relative to what? Natural environments?

---

### 8. Experimental Design and Sample Size

**Core Concern:** Several aspects of the experimental design raise questions about statistical power and generalizability.

#### Questions:
- The 42 parental communities were assembled by "sequential assignment" (strains 1-6, 7-12, etc.). Does this introduce systematic biases in phylogenetic or functional composition between communities?
- With 54 isolates and communities of 6-24 species, there is substantial overlap in strain usage across communities. How does this non-independence affect statistical analyses?
- Only 16 coalescence events for natural communities across 3 nutrient conditions—this is quite limited. Can you draw robust conclusions about interaction-strength dependence with ~5 events per condition?
- The 12 "most abundant isolates" used for invasion assays—are these representative of the full library? Could there be ascertainment bias?
- Why only 2 biological replicates per parental community? What is the reproducibility of coalescence outcomes?

---

## PART III: STATISTICAL AND ANALYTICAL ISSUES

### 9. Null Model Adequacy

**Core Concern:** The null models used (abundance-weighted random selection, shuffled abundance) may not capture all relevant null expectations.

#### Questions:
- Both null models assume no correlation in species selection, but a more relevant null might incorporate shared environmental preferences. Have you tested null models that account for phylogenetic or functional similarity?
- The null models don't account for the possibility that species from one parent happen to have higher mean fitness. A null model where each species has an independent survival probability drawn from a distribution would be informative.
- Supplementary Fig. 8 shows experimental asymmetry exceeds null expectations—but by how much? What is the effect size?

---

### 10. Regression and Correlation Analysis

**Core Concern:** Linear regression may not be the appropriate framework for analyzing the PDI relationship.

#### Questions:
- PDI is bounded between 0 and 1—linear regression assumptions may be violated. Have you considered beta regression or other methods for bounded outcomes?
- The R² values reported (0.00, 0.11, 0.49) don't include confidence intervals. What is the uncertainty in these estimates?
- Is the relationship between invasion success and PDI actually linear? The scatter plots in Fig. 5C suggest possible nonlinearity.
- Pairwise selection correlation (Fig. 2D) uses a permutation test, but what is the test statistic? Is it robust to the non-independence of species pairs from the same community?

---

### 11. Multiple Testing and p-value Reporting

**Core Concern:** Multiple comparisons are made without apparent correction.

#### Questions:
- How many statistical tests were performed across the study? Is there correction for multiple comparisons?
- Several p-values are reported as "< 0.001" or "< 0.0001"—what are the exact values?
- The 91% win rate for acidic vs. alkaline communities (n=32, p<0.0001) uses what test? Binomial? And is n=32 the number of independent matchups, or are communities reused?

---

## PART IV: FRAMING AND LITERATURE ISSUES

### 12. Clements vs. Gleason Framing

**Core Concern:** The Clements/Gleason framing may be oversimplified or historically inaccurate.

#### Questions:
- The Clements/Gleason debate was about community assembly along environmental gradients, not about competition between communities. Is this framing appropriate for coalescence?
- Modern community ecology has largely moved beyond this dichotomy. Is framing the paper around this historical debate the most effective approach?
- The paper claims to "reconcile" conflicting observations, but does it actually resolve the Clements/Gleason debate, or simply show that different conditions yield different outcomes (which was already known)?

---

### 13. Literature Positioning and Claims of Novelty

**Core Concern:** Some claims of novelty or priority may be overstated.

#### Questions:
- The Discussion claims "first experimental demonstration of alternating regimes in community coalescence." Is this accurate? Lu et al. (2022) and others have done extensive coalescence experiments.
- The relationship between interaction strength and community dynamics has been explored extensively (Hu 2022, Ratzke 2020, Hu 2025 are all cited). What is genuinely new here beyond applying these ideas to coalescence?
- Tikhonov (2016) and Lechón (2021) already modeled coalescence with resource-consumer models. How does the gLV approach here differ fundamentally?

---

### 14. Generalizability Claims

**Core Concern:** Claims about generalizability to natural systems and other contexts may be overstated.

#### Questions:
- The natural community experiments (n=16 events, 6 samples) provide limited evidence for generalizability. Can you claim this "demonstrates that community-level selection is a robust phenomenon"?
- All experiments are in well-mixed liquid culture. How relevant are these findings to spatially structured natural environments?
- The 54 isolates come from Cambridge, MA soil/plant surfaces. How generalizable are these findings to other ecosystems (marine, gut, etc.)?
- The paper suggests results explain differences between microbial and macroscopic systems, but no macroscopic data are presented.

---

## PART V: MISSING ELEMENTS

### 15. Alternative Explanations Not Fully Addressed

#### Questions:
- **Phylogenetic signal:** Could CLS reflect phylogenetic clustering within parents rather than ecological coherence? Species from the same parent may be more closely related and share traits.
- **Founder effects:** The 1:1 mixing ratio assumes equal inoculum. But if one parent has higher cell density (biomass), wouldn't that community have an advantage independent of "coherence"?
- **Stochasticity:** What is the role of demographic stochasticity, especially at low abundances during coalescence? Is CLS partly a stochastic phenomenon?
- **Alternative stable states:** Could some Restructuring outcomes reflect alternative stable states rather than ecological reorganization?

---

### 16. Temporal Dynamics

**Core Concern:** The paper focuses on endpoint outcomes, but the dynamics of coalescence may be informative.

#### Questions:
- The time series in Fig. 1D show rapid displacement, but only 12 trajectories are shown. Is this representative?
- How quickly do outcomes stabilize? Are 7 days of post-coalescence stabilization always sufficient?
- Could transient dynamics (e.g., priority effects within the coalescence) affect outcomes? What if mixing ratio varied?

---

### 17. Reproducibility and Robustness

#### Questions:
- What is the reproducibility of coalescence outcomes? If you repeated the same A+B coalescence, would you get the same result?
- Are outcomes deterministic or stochastic? What fraction of variance is explained by parental identity vs. random variation?
- The Supplementary Figs 9-12 show robustness to model parameters—but have you tested robustness to experimental variations (mixing ratio, stabilization time, temperature)?

---

## SUMMARY TABLE

| Issue | Category | Severity | Key Concern |
|-------|----------|----------|-------------|
| 1. CLS definition | Conceptual | Major | May not demonstrate community-level property |
| 2. Assembly effect circularity | Conceptual | Major | Causal logic may be tautological |
| 3. Emergent vs species-driven | Conceptual | Major | Based only on R² differences |
| 4. pH mechanism | Conceptual | Major | May undermine CLS framing |
| 5. Cosine similarity | Methodological | Moderate | Metric choice affects classification |
| 6. Model simplifications | Methodological | Moderate | gLV may miss key biology |
| 7. Nutrient-interaction confounds | Methodological | Major | Multiple variables co-vary |
| 8. Sample sizes | Methodological | Moderate | Limited natural community data |
| 9. Null models | Statistical | Moderate | May not capture relevant nulls |
| 10. Regression methods | Statistical | Minor | Bounded outcome issues |
| 11. Multiple testing | Statistical | Minor | No apparent correction |
| 12. Clements/Gleason framing | Framing | Minor | May be oversimplified |
| 13. Novelty claims | Framing | Moderate | Some claims may be overstated |
| 14. Generalizability | Framing | Moderate | Limited evidence for broad claims |
| 15. Alternative explanations | Missing | Major | Phylogeny, founder effects, stochasticity |
| 16. Temporal dynamics | Missing | Moderate | Endpoint focus may miss dynamics |
| 17. Reproducibility | Missing | Moderate | Not explicitly addressed |

---

## PRIORITY ISSUES FOR RESPONSE

1. **Clarify what "community-level selection" means mechanistically** and how it differs from coincidental co-retention of species with shared traits
2. **Address the pH mechanism** more directly in the main text—it may be the most parsimonious explanation
3. **Strengthen the null model comparisons** to rule out phylogenetic/functional similarity as explanation
4. **Acknowledge limitations** of the nutrient-as-interaction-strength proxy more explicitly
5. **Clarify the emergent/species-driven distinction** with more rigorous criteria
