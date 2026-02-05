# Critical Review — Round 2: Deep Dive After Full Manuscript Read

Building on the Round 1 review, this round focuses on issues that become apparent only after reading the full text, supplementary materials, and methods in detail. The goal is to identify internal inconsistencies, logical gaps, and weaknesses in evidence that a careful referee would flag.

---

## PART I: INTERNAL INCONSISTENCIES AND LOGICAL GAPS

### 1. The "Top-Down Regime" Violates Writing Rules and Undermines the Core Thesis

**Problem:** The abstract, results, and discussion all use "top-down regime," while the writing rules explicitly mandate "species-driven regime." But this is more than a terminology issue—it exposes a conceptual tension at the heart of the paper.

- The paper's central claim is that strong interactions produce **community-level selection**. But the "top-down" / "species-driven" regime in Nutr+ shows that outcomes are predicted by **one dominant species** (R² = 0.49) and its **pH modification** (91% win rate for acidic communities). This is, by definition, species-level selection—a single species' trait determines the community's fate.
- The paper tries to have it both ways: calling Nutr+ outcomes "community-level selection" (because species from the winning parent co-persist) while simultaneously showing that a single species' pH modification is the causal mechanism. The co-persistence of other species may simply be hitchhiking on the dominant species' environmental modification, not evidence of collective dynamics.
- **Critical question:** If you knocked out only the dominant species from the winning community before coalescence, would the outcome reverse? If yes, this is species-level selection with community-level consequences, not community-level selection per se. This experiment would be decisive.

### 2. Conflation of "Correlated Persistence" with "Community-Level Selection"

**Problem:** The paper equates correlated species persistence within a parental community with community-level selection, but these are not the same thing.

- Correlated persistence can arise from multiple mechanisms that are not community-level selection:
  - **Shared environmental tolerance:** Species from the same parent may share pH tolerance, giving correlated survival without any interspecies interaction effects.
  - **Dominant species environment modification:** If one dominant species acidifies the medium, all acid-tolerant species (which happen to be from the same parent due to shared assembly history in the same pH environment) survive together. This is environmental filtering, not community-level selection.
  - **Passive hitchhiking:** If one community's species collectively reach higher biomass faster, rare species from the losing community may be diluted below detection simply due to carrying capacity limits, not competitive exclusion.
- The null models (Extended Data Fig. 1) test against abundance-weighted random and shuffled-abundance baselines, but neither accounts for shared environmental tolerances within parental communities. A more stringent null would randomize species across parents while preserving their trait distributions.

### 3. The Assembly Effect Argument Has a Gap

**Problem:** The paper argues: assembly filters out strong competitors → surviving species have weak mutual interactions → these species persist together during coalescence. But this causal chain has a missing link.

- Reduced within-community competition after assembly does not logically imply that these species will **win together** during coalescence. It only means they won't exclude *each other*. The coalescence outcome depends on **cross-community** interaction strength, which assembly does not filter.
- The assembly effect analysis (Extended Data Fig. 5, Supplementary Figs. 19-20) shows that coalescence produces more Dominance than direct assembly. But this could simply mean that pre-assembled communities have more uneven abundance distributions (one dominant species), giving one community a numerical advantage in the initial mixing—not that assembly creates "coherence."
- The paper shows assembly reduces mean within-community interaction strength (Fig. 2C), but never shows what happens to the **cross-community** interaction distribution. If assembly also systematically changes cross-community interaction structure, the argument is incomplete.

### 4. The μ Calibration Chain Is Weak

**Problem:** The paper calibrates experimental interaction strengths as μ ≈ 0.5 (Nutr−), 0.7 (Base), 0.9 (Nutr+) based on failed invasion frequency. This calibration has several problems:

- The calibration assumes a uniform interaction distribution, which is a model assumption, not an empirical fact. Different distributions (Gaussian, Gamma) would give different μ estimates for the same failed invasion frequency.
- Failed invasion frequency measures competitive *asymmetry* (whether one species excludes another), not mean interaction *strength*. A system with many strongly asymmetric but individually moderate interactions could show high failed invasion frequency with moderate μ.
- Only 12 of 54 isolates were used for invasion assays. These are the "most abundant," which are systematically biased toward competitively superior species. The interaction statistics of these 12 may not represent the full 54-species pool.
- The mapping from failed invasion frequency to μ is presented in Supplementary Methods but the functional form and uncertainty of this mapping are not clearly described. Is it linear? What are the confidence intervals on μ estimates?

---

## PART II: EVIDENCE QUALITY AND STATISTICAL CONCERNS

### 5. The R² = 0.11 vs. R² = 0.49 Distinction Is Overinterpreted

**Problem:** The paper builds an entire regime framework on the difference between two R² values from linear regression, but this distinction is fragile.

- R² = 0.11 (Base, n = 47 Dominance events) has a reported p = 0.03. This means there *is* a statistically significant relationship between dominant species competition and PDI, even in the "emergent regime." The paper describes Base as having "weak" predictive power, but a significant p-value means the dominant species *does* predict outcomes to some degree. The two regimes may be quantitative, not qualitative.
- R² = 0.49 (Nutr+, n ≈ 68 Dominance events) still leaves 51% of variance unexplained. By the paper's own logic, Nutr+ is partly "emergent" too.
- No confidence intervals are reported for R² values. Bootstrap or permutation-based CIs would clarify whether 0.11 and 0.49 are statistically distinguishable.
- The paper does not test whether the *difference* between R² values is statistically significant. It could be that these are drawn from the same underlying relationship with different noise levels.
- PDI is bounded [0, 1], and linear regression assumes an unbounded response. This is a technical violation that could bias R² estimates, particularly near the boundaries. Beta regression would be more appropriate.

### 6. The pH Mechanism Evidence Is Incomplete

**Problem:** pH is presented as the mechanistic explanation for the species-driven regime, but the evidence is correlational and the key controls are missing.

- The claim that "acidic communities win 91% of the time in Nutr+" (n = 32) is compelling but only applies to matchups between pH < 6.5 and pH > 7.5 communities. What about the matchups between communities with similar pH? These are excluded from the analysis but may be informative.
- The Extended Data Fig. 8 shows pH difference predicts outcomes in Nutr+ (R² = 0.29) but not Base (R² = 0.02). However, R² = 0.29 in Nutr+ is actually *lower* than the R² = 0.49 from dominant species competition. This means pH explains less variance than the dominant species identity itself—so pH may be a correlated but not causal factor.
- A critical missing experiment: coalescence in **pH-buffered** Nutr+ medium. If Dominance frequency drops in buffered Nutr+ to levels similar to Base, this would confirm pH as the causal mechanism. Without this control, pH modification is correlational evidence only.
- The paper does not discuss what determines the outcome when both communities have similar pH values. If Dominance still occurs between same-pH communities, the pH mechanism cannot be the full story even in Nutr+.

### 7. Natural Community Data Is Underpowered

**Problem:** The natural community experiments (Figure 6) are the paper's main claim to generalizability, but the evidence is thin.

- Only 6 environmental samples, producing 15 unique pairwise coalescence events per condition (with 2 biological replicates each, n = 30). After classification into 3 outcome types, cell sizes are very small (e.g., 37% of 30 = ~11 Dominance events in Nutr−).
- No pairwise selection correlation analysis is reported for natural communities. This was the key evidence for community-level selection in synthetic communities—its absence for natural communities is a significant gap.
- No invasion assays were performed for natural communities, so there is no independent validation that nutrient concentration modulates interaction strength in these more complex assemblages.
- Natural communities have different and variable richness (13.7 ± 7.2 ASVs) compared to synthetic communities (9.8 ± 4.8 ASVs). The higher Restructuring fraction in natural communities could reflect this richness difference rather than "greater taxonomic diversity and more complex interaction networks."
- The environmental samples are all from Cambridge, MA, and all terrestrial. The claim of generalizability would be stronger with samples from fundamentally different environments (aquatic, host-associated, etc.).

### 8. Reproducibility of Individual Coalescence Events Is Not Demonstrated

**Problem:** The paper reports that natural community experiments used 2 biological replicates, but never reports the concordance rate between replicates.

- If the same A + B coalescence is performed twice, do both replicates give the same outcome classification? If concordance is, say, 70%, then outcome classification has substantial stochastic noise, which would affect all downstream analyses.
- For synthetic communities, the Methods state 2 biological replicates per parental community, but it's unclear whether the 83 coalescence events in Base medium include replicates or are unique pairs.
- No variance or error bars are shown for individual coalescence events on the similarity maps—each event is plotted as a single point.

---

## PART III: METHODOLOGICAL BLIND SPOTS

### 9. The Classification Boundaries Are Arbitrary and Untested for Sensitivity

**Problem:** The outcome classification (Dominance/Mixture/Restructuring) uses specific thresholds (x² = 0.5 for Restructuring; PDI = 0.25/0.75 for Dominance vs. Mixture) that are defined by convention.

- The 0.25/0.75 PDI threshold corresponds to a ~3:1 contribution ratio. Why 3:1 and not 2:1 or 4:1? The choice matters: a more stringent threshold (e.g., 4:1) would reclassify some Dominance events as Mixture, potentially weakening the main result.
- The paper claims robustness across 5 similarity metrics (Extended Data Fig. 7, <15% variation), but does not report sensitivity to the **classification thresholds** within any given metric. A sensitivity analysis sweeping PDI thresholds from 0.1/0.9 to 0.4/0.6 would be informative.
- The x² = 0.5 threshold for Restructuring means that events where parents explain exactly 50% of the offspring composition are classified as Restructuring. Is there a biological justification for this cutoff?

### 10. The gLV Model Lacks Key Biology That May Be Driving Experimental Results

**Problem:** The gLV model is used to explain experimental results, but it lacks the very mechanism (pH modification) that the paper identifies as the key driver in the species-driven regime.

- The gLV model has no environmental modification, no pH dynamics, no metabolite-mediated interactions. Yet it reproduces the outcome statistics. This means either: (a) pH is not actually necessary for Dominance (contradicting the pH analysis in Fig. 5), or (b) the gLV model captures the outcomes for the wrong reasons.
- If (b), then the model's predictions about interaction strength controlling outcomes may be coincidentally correct rather than mechanistically correct. The model would be fitting the pattern without capturing the process.
- The paper acknowledges that "both our experimental system and theoretical model are dominated by competitive interactions" (Discussion), but this is an understatement. The model *only* has competition (α_ij > 0 for all i, j), while real communities include facilitation, cross-feeding, and environmental modification that may qualitatively change dynamics.
- A consumer-resource model with explicit metabolite dynamics and pH (as in Tikhonov 2016 or Goldford et al. 2018) would be a more mechanistically appropriate model for this system. The paper should discuss why a simpler but less mechanistic model was chosen.

### 11. The Sequential Assignment of Strains to Communities May Introduce Bias

**Problem:** Strains were assigned to communities by sequential numbering (strains 1-6, 7-12, etc.). If strains were numbered in isolation/collection order, this could introduce systematic biases.

- Strains isolated from the same environment may have adjacent numbers, meaning P6 communities could be phylogenetically or functionally clustered by environment of origin.
- This is particularly concerning for P24 communities, which are "partially overlapping" (only two non-overlapping sets of 24 from 54 isolates). The degree of overlap and its impact on coalescence outcomes is not analyzed.
- The paper should clarify whether strain numbering reflects isolation order and whether any randomization was applied.

### 12. OD Normalization Before Coalescence May Not Equalize Competition

**Problem:** Communities were normalized to equivalent OD600 before coalescence mixing. But OD600 measures total biomass, not total cell count.

- Species differ in cell size and optical properties. Equal OD does not mean equal cell number. A community dominated by large cells could have fewer individuals (and lower effective population size) than one dominated by small cells, creating a systematic advantage for the small-cell community independent of interaction strength.
- This is especially relevant for the initial dynamics of coalescence, where numerical advantage could matter before competitive interactions have time to play out.

---

## PART IV: WRITING AND PRESENTATION ISSUES

### 13. The Abstract Contains a Typo and Terminology Violations

- "that that communities" — double "that" on the last line.
- "top-down regime" should be "species-driven regime" per writing rules.
- "Dominance" is used as the primary outcome term throughout, while writing rules specify "CLS" as primary.

### 14. The Introduction Oversells the Reconciliation

- The last paragraph of the Introduction claims: "These results reconcile conflicting observations by establishing interaction strength as the control parameter for community-level selection." But this is a hypothesis validated in one experimental system (bacteria in liquid culture), not a reconciliation of conflicting observations across diverse systems.
- The Discussion's attempt to explain Goldman 2025 and Walton 2025 (gut microbiome studies) by analogy to Nutr− is speculative. BHI medium has very different composition from Nutr−, and the gut microbiome communities are fundamentally different in diversity and interaction structure from 54-species lab communities.

### 15. Figure Captions Are Inconsistent

- Fig. 1 caption refers to "Fig. 1" but uses lowercase for panels (a, b, c, d, e).
- Fig. 6 caption references "Fig. 1c" (lowercase) while other captions use various conventions.
- Some captions report exact n values and statistical tests; others do not. For example, Fig. 3 caption does not report the number of coalescence events per community size in the robustness analysis.

### 16. The Discussion Is Missing Key Limitations

The Discussion acknowledges the limitation of competitive-only interactions and steady-state focus, but omits:

- The arbitrary classification thresholds and their potential impact on conclusions.
- The small sample size of natural community experiments.
- The inability to distinguish pH-mediated environmental filtering from true community-level selection.
- The fact that the gLV model lacks the pH mechanism identified as the key driver in Nutr+.
- The potential for biomass/OD normalization artifacts.

---

## PART V: STRUCTURAL AND NARRATIVE ISSUES

### 17. The Narrative Arc Is Inverted for the Species-Driven Regime

**Problem:** The paper argues: interaction strength increases → Dominance increases → community-level selection. But the species-driven regime in Nutr+ actually shows: interaction strength increases → one dominant species takes over → that species' pH modification determines outcomes. This is a narrative arc toward *less* community-level behavior, not more.

- In Base medium (moderate μ), the outcome is genuinely hard to predict from any single species → this is arguably the most "community-level" behavior.
- In Nutr+ (high μ), the outcome is predictable from one species → this is arguably the least "community-level" behavior.
- The paper should acknowledge that the strongest evidence for *emergent* community-level selection is at intermediate interaction strength, not the highest. The two regimes have qualitatively different implications for the Clements-Gleason debate, and the paper glosses over this.

### 18. The Simulation-Experiment Agreement May Be Superficial

**Problem:** The paper emphasizes that the gLV model at μ = 0.6 reproduces the experimental Dominance frequency (61% vs. 65%). But this agreement may be less meaningful than it appears.

- The model has one free parameter (μ) and is fit to one observable (outcome frequencies). Matching one number with one parameter is not a stringent test.
- The model does not simultaneously fit: (a) the magnitude of pairwise selection correlation, (b) the R² of dominant species prediction, (c) the PDI distribution shape, (d) the Restructuring fraction. Are all of these quantitatively matched, or just the Dominance frequency?
- The robustness analyses (Supplementary Figs. 3-5) show that different distributions and parameters give qualitatively similar patterns. This means the model is not very constraining—many parameter combinations give "high Dominance," so matching the experiment is not surprising.

### 19. Missing Discussion of Neutral/Stochastic Processes

**Problem:** The paper frames outcomes entirely in terms of deterministic competitive dynamics, but stochastic processes may play an important role.

- During the 1:1 mixing and subsequent serial dilution (×30 every 24 h), rare species face demographic stochasticity. Species near the detection threshold (0.1%) could be lost stochastically, not through competitive exclusion.
- The ×30 daily dilution creates a minimum viable population. Species below ~3% of carrying capacity after dilution could be lost to drift in a single cycle. This could create apparent Dominance through stochastic loss rather than deterministic competition.
- The paper should discuss whether the ×30 dilution factor influences outcome frequencies and whether a less aggressive dilution (e.g., ×5) would shift outcomes toward Mixture.

---

## UPDATED PRIORITY ISSUES (Cumulative from Rounds 1 and 2)

| Priority | Issue | Why It Matters |
|----------|-------|----------------|
| 1 | Species-driven regime undermines community-level selection claim | The strongest interactions lead to outcomes determined by individual species, not communities |
| 2 | Correlated persistence ≠ community-level selection | Need to rule out hitchhiking, shared tolerance, environmental filtering |
| 3 | pH mechanism is correlational, not causal | Missing buffered-medium control experiment |
| 4 | gLV model lacks the identified mechanism (pH) | Model-experiment agreement may be coincidental |
| 5 | R² comparison between regimes not statistically tested | Two-regime framework rests on an untested comparison |
| 6 | Natural community data is underpowered | Key generalizability claim rests on n ≈ 10 events per outcome per condition |
| 7 | Classification thresholds are arbitrary | Conclusions may be sensitive to threshold choice |
| 8 | μ calibration chain is weak | Experimental μ estimates depend on model assumptions |
| 9 | Reproducibility not demonstrated | No replicate concordance reported |
| 10 | Abstract and text violate writing rules | "top-down regime," double "that," inconsistent terminology |
