# Supplementary Materials Review Report: Paragraph-by-Paragraph Analysis

This report evaluates each section and figure in the Supplementary Information for the manuscript "Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence" to assess whether they are necessary and how they support the main text.

---

## Summary Table

| Section/Figure | Verdict | Recommendation |
|----------------|---------|----------------|
| Supplementary Methods | **ESSENTIAL** | Keep - required for reproducibility |
| Supplementary Note 1 (Null Models) | **ESSENTIAL** | Keep - validates key claim |
| Supplementary Note 2 (Assembly Effect) | **ESSENTIAL** | Keep - explains mechanism |
| Supplementary Note 3 (Simulation Robustness) | **ESSENTIAL** | Keep - validates model |
| Supplementary Note 4 (Pairwise Selection) | **ESSENTIAL** | Keep - key evidence |
| Supplementary Note 5 (Invasion Experiments) | **ESSENTIAL** | Keep - methods detail |
| Extended Data Figs 1-8 | **ESSENTIAL** | Keep - directly referenced |
| Suppl. Figs 1-2 (Strain characterization) | **ESSENTIAL** | Keep - basic characterization |
| Suppl. Figs 3-5 (Simulation robustness) | **ESSENTIAL** | Keep - validates robustness |
| Suppl. Figs 6-8 (Invasion matrices) | **ESSENTIAL** | Keep - supports Fig 4 |
| Suppl. Figs 9-10 (pH mechanism) | **ESSENTIAL** | Keep - supports Fig 5 |
| Suppl. Figs 11-13 (Rank-abundance) | **MODERATE** | Consider condensing |
| Suppl. Figs 14-16 (Coalescence matrices) | **MODERATE** | Consider condensing |
| Suppl. Figs 17-18 (Time series) | **LOW** | Could be removed |
| Suppl. Figs 19-20 (Assembly effect) | **ESSENTIAL** | Keep - supports Note 2 |
| Suppl. Figs 21-22 (Monoculture/Overlap) | **MODERATE** | Keep 21, consider 22 |
| Suppl. Figs 23-26 (Natural communities) | **ESSENTIAL** | Keep - supports Fig 6 |

---

## Detailed Paragraph-by-Paragraph Analysis

---

## SUPPLEMENTARY METHODS

### Microbial Strain Library, Media, and Culture (Lines 10-19)

**Content:** Describes 54 bacterial isolates, phylogenetic diversity, media composition, and culture conditions.

**Main Text Reference:** Methods section "Microbial Strain Library and Culture Conditions" (lines 8-12 in methods.tex) provides brief description and explicitly refers to "Supplementary Fig. 1" and "Supplementary Methods."

**Verdict:** **ESSENTIAL**
- Required for reproducibility
- Main text explicitly refers to this section
- Cannot be shortened further without losing critical methodological detail

---

### Construction of Parental Communities and Community Coalescence (Lines 25-31)

**Content:** Details parental community construction (P6, P12, P24), coalescence pair compositions, and stabilization protocol.

**Main Text Reference:** Methods "Community Assembly and Coalescence Experiments" (lines 15-19) provides summary and refers to "Supplementary Methods" for full details.

**Verdict:** **ESSENTIAL**
- Required for replication
- Provides species survival ratio (74 +/- 2%) cited in main text Results (line 20 in results.tex)
- Contains critical experimental details not in main text

---

### 16S rRNA Sequencing and Data Processing (Lines 36-41)

**Content:** DNA extraction protocol, sequencing parameters, DADA2 pipeline, ASV filtering.

**Main Text Reference:** Methods "16S rRNA Sequencing" (lines 22-26) summarizes and refers to "Supplementary Methods."

**Verdict:** **ESSENTIAL**
- Standard practice for sequencing studies
- Contains technical parameters needed for reproducibility

---

### Similarity-Based Classification of Coalescence Outcomes (Lines 47-68)

**Content:** L2 normalization, cosine similarity, linear decomposition, PDI calculation, classification thresholds.

**Main Text Reference:** Methods "Classification of Coalescence Outcomes" (lines 29-33) gives overview and refers to "Supplementary Methods." The PDI equation is formally defined here and used throughout main text Figures 3-6.

**Verdict:** **ESSENTIAL**
- Mathematical framework is central to all main figures
- Classification thresholds (x^2 = 0.5, PDI 0.25/0.75) must be justified
- Cannot be moved to main text due to length

---

### Lotka-Volterra Simulations (Lines 73-88)

**Content:** gLV equations, parameter choices, equilibration protocol, coalescence simulation procedure.

**Main Text Reference:** Methods "Lotka-Volterra Simulations" (lines 36-40) summarizes and refers to "Supplementary Methods."

**Verdict:** **ESSENTIAL**
- Model is central to Figures 2-3
- Implementation details required for reproducibility
- Species pool partitioning scheme must be documented

---

### Pairwise Invasion Assays (Lines 93-97)

**Content:** Invasion experiment protocol, outcome classification criteria.

**Main Text Reference:** Methods "Pairwise Invasion Assays" (lines 43-47) summarizes key details.

**Verdict:** **ESSENTIAL**
- Supports Figure 4B (interaction strength calibration)
- Classification criteria (coexistence >10%, exclusion <1%) needed

---

### Natural Sample-Derived Communities (Lines 102-106)

**Content:** Sample collection, enrichment protocol, coalescence design.

**Main Text Reference:** Methods "Natural Sample-Derived Communities" (lines 51-55) provides summary.

**Verdict:** **ESSENTIAL**
- Supports Figure 6
- Protocol details required for reproducibility

---

### Statistical Analyses (Lines 111-123)

**Content:** Statistical tests used, significance thresholds.

**Main Text Reference:** Methods "Statistical Analyses" (lines 58-62) summarizes.

**Verdict:** **ESSENTIAL**
- Required for all statistical claims in main text
- Standard practice

---

### Optical Density Measurements (Lines 129-133)

**Content:** OD measurement protocol, normalization procedure.

**Main Text Reference:** Not explicitly cited but supports experimental normalization.

**Verdict:** **MODERATE**
- Standard protocol, but brief
- Keep for completeness

---

### Monoculture Characterization (Lines 138-142)

**Content:** Growth rate and pH modification measurements for 54 isolates.

**Main Text Reference:** Referenced via Supplementary Figs 9, 21 in main text.

**Verdict:** **ESSENTIAL**
- Supports pH mechanism discussion in Results section 3.5
- Documents phenotypic diversity of strain library

---

### Sensitivity Analysis (Lines 147-155)

**Content:** Robustness of classification metrics and simulation distributions.

**Main Text Reference:** Extended Data Fig 7 (metric robustness) and Supplementary Fig 5 (distribution robustness) cited in main text.

**Verdict:** **ESSENTIAL**
- Validates that main findings are not artifacts of methodological choices

---

## SUPPLEMENTARY NOTE 1: Null Models and Statistical Controls

**Content:** Two null models testing whether skewed abundance distributions explain Dominance: (1) abundance-weighted random selection, (2) shuffled abundance.

**Main Text Reference:** Results section "Coalescence frequently yields asymmetric outcomes" (lines 24-25) states: "To rule out this possibility, we compared experimental outcomes against two null models... The experimentally observed asymmetry in Dominance significantly exceeded both null expectations (Extended Data Fig. 1)."

**Verdict:** **ESSENTIAL**
- Directly addresses potential confound (abundance skewness)
- Statistical validation is critical for the Dominance claim
- Results (p < 10^-18, p < 10^-11) strongly support main conclusion
- Cannot be removed without weakening the paper

---

## SUPPLEMENTARY NOTE 2: Assembly Effect Analysis

**Content:** Compares coalescence to "direct assembly" control; shows assembly reduces mean interaction strength and increases Dominance probability.

**Main Text Reference:**
- Results section "Random competitive interactions reproduce asymmetric outcomes" (lines 46-47): "During assembly, competitive exclusion filters out species with strong mutual interactions... We quantified this effect by measuring pairwise selection correlation."
- Extended Data Fig 5 explicitly referenced in main text

**Verdict:** **ESSENTIAL**
- Provides mechanistic explanation for why Dominance emerges
- Quantifies assembly filtering effect (key to community-level selection argument)
- Simulation comparison (coalescence vs direct assembly) is compelling evidence
- Keep entire section

---

## SUPPLEMENTARY NOTE 3: Simulation Robustness

**Content:** Tests robustness to interaction coefficient distributions (Uniform, Gaussian, Gamma) and community size (4-48 species).

**Main Text Reference:**
- Results section (line 63-64): "These patterns were robust to variation in carrying capacities, interaction distributions, similarity metrics, and community size (Supplementary Figs. 3-5; Extended Data Fig. 4)."

**Verdict:** **ESSENTIAL**
- Main text explicitly claims robustness; this provides evidence
- Distribution robustness validates use of uniform distribution in main analysis
- Community size robustness shows findings apply across experimental range

---

## SUPPLEMENTARY NOTE 4: Pairwise Selection Correlation

**Content:** Mathematical definition of selection correlation metric; concordance rate calculation.

**Main Text Reference:**
- Results sections 3.2 (Figure 2d) and 3.4 (Extended Data Fig 3) use this metric
- Figure 2 caption: "Pairwise selection correlation. Species pairs from the same parental community show positive correlation"

**Verdict:** **ESSENTIAL**
- The selection correlation metric is central evidence for community-level selection
- Mathematical definition must be documented
- Results (Delta increasing with mu) directly support main claims

---

## SUPPLEMENTARY NOTE 5: Pairwise Invasion Experiments

**Content:** Detailed protocol for reciprocal invasion assays; outcome classification.

**Main Text Reference:**
- Methods "Pairwise Invasion Assays" refers to Supplementary Methods
- Figure 4B uses these data

**Verdict:** **ESSENTIAL**
- Protocol details required for reproducibility
- Outcome classification criteria important for interpretation

---

## EXTENDED DATA FIGURES

### Extended Data Fig 1: Skewness Null Model

**Main Text Reference:** Results line 24-25 explicitly cites this figure.

**Verdict:** **ESSENTIAL** - Validates that Dominance is not due to abundance skewness

---

### Extended Data Fig 2: Pairwise Selection Correlation (Simulation)

**Main Text Reference:** Results section 3.3 (line 63-64) cites this for correlation vs interaction strength.

**Verdict:** **ESSENTIAL** - Key evidence for interaction-strength dependence of selection correlation

---

### Extended Data Fig 3: Pairwise Selection Correlation (Experimental)

**Main Text Reference:** Results section 3.4 (line 82-83): "We further confirmed... through pairwise selection correlation analysis (Extended Data Fig. 3)."

**Verdict:** **ESSENTIAL** - Experimental validation of simulation predictions

---

### Extended Data Fig 4: Species Number Ablation

**Main Text Reference:** Results line 63-64 explicitly cites this figure.

**Verdict:** **ESSENTIAL** - Validates robustness across community sizes

---

### Extended Data Fig 5: Assembly Effect Simulation

**Main Text Reference:** Supplementary Note 2 references this; main text discusses assembly effect mechanism.

**Verdict:** **ESSENTIAL** - Key comparison between coalescence and direct assembly

---

### Extended Data Fig 6: Time Series Base Medium

**Main Text Reference:** Results section 3.1 (line 22-23): "Representative time series illustrate the spectrum of post-coalescence dynamics (Fig 1D)." This extends those examples.

**Verdict:** **ESSENTIAL** - Provides additional time course examples mentioned in main text

---

### Extended Data Fig 7: Robustness of Metrics

**Main Text Reference:** Results line 24: "This pattern of Dominance as the most frequent outcome was robust across variants of similarity metrics (Extended Data Fig. 7)."

**Verdict:** **ESSENTIAL** - Validates classification is metric-independent

---

### Extended Data Fig 8: pH vs Coalescence Outcome

**Main Text Reference:** Results section 3.5 (line 101-102): "In coalescence events between acidic and alkaline parental communities... (Extended Data Fig. 8)."

**Verdict:** **ESSENTIAL** - Supports pH mechanism for top-down regime

---

## SUPPLEMENTARY FIGURES

### Supplementary Fig 1-2: Taxonomy and Phylogeny

**Main Text Reference:** Methods and Results mention "54 bacterial isolates... spanning 29 families" (Supplementary Figs 1, 2).

**Verdict:** **ESSENTIAL**
- Basic strain characterization required
- Phylogenetic diversity claim needs documentation

---

### Supplementary Figs 3-5: Simulation Robustness (Growth rate, Carrying capacity, Distributions)

**Main Text Reference:** Results line 63-64 cites "Supplementary Figs. 3-5."

**Verdict:** **ESSENTIAL**
- Directly cited in main text
- Validates simulation robustness

---

### Supplementary Figs 6-8: Pairwise Invasion Matrices

**Main Text Reference:** Figure 4B uses invasion data; Supplementary Note 5 references these.

**Verdict:** **ESSENTIAL**
- Shows raw invasion data underlying Figure 4B
- Documents interaction strength differences across media

---

### Supplementary Figs 9-10: pH Mechanism

**Main Text Reference:** Results section 3.5 (lines 100-102) references "Supplementary Figs. 9, 10."

**Verdict:** **ESSENTIAL**
- Supports mechanistic claim about pH modification
- Documents monoculture pH modification and ASV-pH relationships

---

### Supplementary Figs 11-13: Rank-Abundance Curves (Synthetic Communities)

**Main Text Reference:** Not explicitly cited in main text.

**Verdict:** **MODERATE**
- Shows abundance distributions, but not central to main argument
- **Recommendation:** Could be condensed to single figure with all three media, or moved to data repository
- Gini coefficients are mentioned but not emphasized in main text

---

### Supplementary Figs 14-16: Coalescence Outcome Matrices

**Main Text Reference:** Not explicitly cited in main text.

**Verdict:** **MODERATE**
- Provides visual summary of all coalescence outcomes
- Useful for readers wanting detailed breakdown by richness level
- **Recommendation:** Could condense to representative examples or keep for completeness
- These are informative but not essential for main claims

---

### Supplementary Figs 17-18: Additional Time Series (Nutr-, Nutr+)

**Main Text Reference:** Not explicitly cited; extends Extended Data Fig 6.

**Verdict:** **LOW PRIORITY**
- Extended Data Fig 6 already shows time series for Base medium
- Main text Figure 1D shows representative dynamics
- **Recommendation:** Could be removed or consolidated
- These add incremental value but are not essential

---

### Supplementary Figs 19-20: Assembly Effect

**Main Text Reference:** Supplementary Note 2 references these; assembly mechanism discussed in Results.

**Verdict:** **ESSENTIAL**
- Fig 19 shows assembly reduces interaction strength (key mechanism)
- Fig 20 shows experimental validation
- Both support Supplementary Note 2

---

### Supplementary Fig 21: Monoculture OD and Growth Rate

**Main Text Reference:** Supplementary Methods mentions phenotypic diversity; not explicitly cited in main Results.

**Verdict:** **MODERATE**
- Documents phenotypic diversity of strain library
- **Recommendation:** Keep - provides basic strain characterization

---

### Supplementary Fig 22: Overlap Fraction Histogram (Synthetic)

**Main Text Reference:** Not explicitly cited in main text.

**Verdict:** **MODERATE**
- Shows most surviving ASVs come from one parent (supports Dominance)
- Provides additional quantification of one-sided outcomes
- **Recommendation:** Consider keeping as it reinforces Dominance finding

---

### Supplementary Figs 23-26: Natural Community Characterization

**Main Text Reference:** Results section 3.6 (line 119) mentions "higher ASV richness" and "low ASV overlap (Supplementary Figs. 23-26)."

**Verdict:** **ESSENTIAL**
- Explicitly cited in main text
- Supports Figure 6 claims about natural communities
- Documents differences between synthetic and natural communities

---

## OVERALL RECOMMENDATIONS

### Sections to KEEP (Essential):

1. **All Supplementary Methods** - Required for reproducibility
2. **All Supplementary Notes 1-5** - Each supports specific main text claims
3. **All Extended Data Figures 1-8** - All explicitly cited
4. **Supplementary Figs 1-2** - Strain characterization
5. **Supplementary Figs 3-5** - Simulation robustness (cited)
6. **Supplementary Figs 6-8** - Invasion matrices (support Fig 4)
7. **Supplementary Figs 9-10** - pH mechanism (cited)
8. **Supplementary Figs 19-20** - Assembly effect (support Note 2)
9. **Supplementary Fig 21** - Monoculture characterization
10. **Supplementary Figs 23-26** - Natural communities (cited)

### Sections that COULD BE CONDENSED:

1. **Supplementary Figs 11-13** (Rank-abundance curves for synthetic communities)
   - Currently 3 separate figures for 3 media conditions
   - Could combine into single 3-panel figure
   - Not explicitly cited in main text

2. **Supplementary Figs 14-16** (Coalescence matrices)
   - 3 figures x 3 richness levels = 9 panels total
   - Visually informative but repetitive
   - Could show 1 representative or move to data repository

### Sections that COULD BE REMOVED:

1. **Supplementary Figs 17-18** (Additional time series for Nutr-, Nutr+)
   - Main text Fig 1D and Extended Data Fig 6 already show dynamics
   - These provide incremental additional examples
   - Low information value relative to space

2. **Supplementary Fig 22** (Overlap fraction histogram - synthetic)
   - Interesting but not cited in main text
   - Message already conveyed by Dominance statistics
   - However, consider keeping as it provides complementary evidence

---

## FIGURE CROSS-REFERENCE CHECK

Checking all supplementary figure citations in main text:

| Main Text Citation | Figure | Status |
|-------------------|--------|--------|
| Results (line 20): "Supplementary Figs. 1, 2" | Taxonomy, Phylogeny | PRESENT |
| Results (line 63-64): "Supplementary Figs. 3-5" | Simulation robustness | PRESENT |
| Results (line 78): "Supplementary Figs. 6-8" | Pairwise invasion | PRESENT |
| Results (line 101): "Supplementary Fig. 9" | Monoculture pH | PRESENT |
| Results (line 101): "Supplementary Fig. 10" | ASV vs pH | PRESENT |
| Results (line 119): "Supplementary Figs. 23-26" | Natural communities | PRESENT |
| Extended Data Fig 5: "Supplementary Fig. 19" | Assembly effect | PRESENT |
| Suppl Fig 20 caption: "Extended Data Fig. 5, Supplementary Fig. 19" | Cross-reference | PRESENT |

All cited supplementary figures are present and necessary.

---

## CONCLUSION

The supplementary materials are **generally well-organized and necessary**. The main areas for potential reduction are:

1. **Rank-abundance curves (Figs 11-13)**: Could condense but provide useful characterization
2. **Coalescence matrices (Figs 14-16)**: Informative but space-intensive
3. **Additional time series (Figs 17-18)**: Lowest priority; could remove

**Overall verdict:** The supplementary materials strongly support the main text. Each Supplementary Note addresses a specific methodological concern or provides essential mechanistic insight. The Extended Data Figures are all directly cited. Most Supplementary Figures are either cited or provide essential characterization. Only Figs 11-13, 14-16, 17-18, and 22 could potentially be condensed or removed without weakening the scientific argument.

The current organization follows the main text structure well, with methods first, then notes corresponding to each major result, followed by figures in order of appearance.
