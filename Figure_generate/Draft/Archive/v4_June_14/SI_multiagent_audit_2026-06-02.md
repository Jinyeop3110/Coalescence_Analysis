# Supplementary Information Multi-Agent Audit - 2026-06-02

Scope: only the five Supplementary Notes plus `supplementary_sections/figures.tex` and `supplementary_sections/extended_data.tex`.

Files reviewed:

- `skewness_null_model.tex` (Supplementary Note 1)
- `assembly_effect.tex` (Supplementary Note 2)
- `simulations.tex` (Supplementary Note 3)
- `invasion.tex` (Supplementary Note 4)
- `alternative_models_controls.tex` (Supplementary Note 5)
- `extended_data.tex`
- `figures.tex`

Severity: **[CRITICAL]** = likely blocks SI self-containment or argument clarity; **[WARNING]** = fix before submission; **[NOTE]** = low-priority clarification.

---

## Agreed Findings

These were flagged by at least two agents or independently confirmed during synthesis.

### [CRITICAL] Note 4 is disconnected from its natural figures

**Location:** `supplementary_sections/invasion.tex:7-9`; `figures.tex` Supplementary Figs. 5-7

**Agents:** A, B, C

Note 4 states that competitive exclusion increases with nutrient concentration and that Nutr+ produces more frequent exclusion, but it cites no figure. Supplementary Figs. 5-7 are the obvious support:

- Fig. 5 caption: Nutr- pairwise invasion outcomes; low failed invasion frequency.
- Fig. 6 caption: Base pairwise invasion outcomes; intermediate failed invasion frequency.
- Fig. 7 caption: Nutr+ pairwise invasion outcomes; high failed invasion frequency.

**Problem:** The Note makes a central directional claim without directing the reader to the relevant evidence. There is also terminology drift: Note 4 says "competitive exclusion", while captions say "failed invasion frequency".

**Recommended fix:** Add explicit citations to Supplementary Figs. 5-7 in Note 4 and harmonize wording, for example by defining failed invasion as the operational measure of competitive exclusion.

### [WARNING] Note 2 overstates what ED Fig. 6 says about experimental pairwise selection correlation

**Location:** `supplementary_sections/assembly_effect.tex:21`; `extended_data.tex:54`

**Agents:** A, C

Note 2 says: "In both simulations ... and experiments ..., we observed same > 0 and cross < 0, with Delta increasing with interaction strength."

ED Fig. 6 caption says Nutr- has "no significant difference", Base has "intermediate differences", and Nutr+ has significantly higher within-community correlation than cross-community correlation.

**Problem:** ED Fig. 5 supports the simulated same-positive/cross-negative trend. ED Fig. 6 supports a nutrient-condition trend in experiments, but does not explicitly support cross-community negativity or monotonic Delta across all experimental conditions.

**Recommended fix:** Split the sentence into simulation and experimental claims. For experiments, say only what ED Fig. 6 supports unless the figure annotations show the stronger statement.

### [WARNING] Supplementary Figs. 10-12 have ambiguous sample counts

**Location:** `figures.tex:143,151,159`

**Agents:** C; synthesis confirms conflict with other captions/Notes

Rank-abundance captions report coalesced-community counts of Base n=94, Nutr- n=92, and Nutr+ n=94. Other SI locations use Base n=83 and Fig. 21 reports Nutr- n=90, Base n=83, Nutr+ n=90. The same captions report parental-community counts n=59 or n=60, while the tracked design quantity is 30 parental communities.

**Problem:** These may be replicate/profile counts rather than unique coalescence events or unique parental communities, but the captions do not define the counting unit.

**Recommended fix:** Clarify the denominator in each caption, e.g. "sequenced community profiles" versus "unique coalescence events" versus "unique parental communities".

### [WARNING] Many Supplementary Figures have no narrative home in Notes 1-5

**Location:** `figures.tex` Supplementary Figs. 1-3, 5-17, 20-27

**Agents:** B; synthesis confirms by citation sweep

These 24 figures are not cited in any of the five Supplementary Note bodies. This includes isolate phylogeny, growth-rate/carrying-capacity robustness, invasion matrices, pH figures, rank-abundance curves, coalescence matrices, time series, overlap fractions, natural-community figures, and assembly-filtering matrices.

**Problem:** The SI can be hard to use as a standalone reference because many figures are present only as captions, without a Note that explains why they matter.

**Recommended fix:** Add a top-level SI roadmap or a figure-to-topic table mapping Supplementary Figs. 1-44 and ED Figs. 1-8 to their Note/main-text home. Also add direct citations where figures support Note claims.

---

## Agent A Only - Scientific Argument Gaps

### [CRITICAL] Note 1 abundance-skew null model result is uncited

**Location:** `supplementary_sections/skewness_null_model.tex:43`

Note 1 gives quantitative null-model results: experimental parental asymmetry mean 0.698 (n=83), abundance-weighted null mean 0.476, shuffled null mean 0.557, both highly significant.

**Problem:** This is a central support for "abundance skewness alone cannot explain" Dominance, but no figure is cited.

**Recommended fix:** Cite the figure containing these null-model results, or add/identify a figure if this result is text-only.

### [WARNING] Note 5 pool-size ablation cites Fig. 34 for interaction-matrix reconstruction

**Location:** `supplementary_sections/alternative_models_controls.tex:11`; `figures.tex:416`

Note 5 says reconstructed post-assembly interaction matrices showed lower within-community than between-community interaction strengths across pool sizes. The paragraph cites Supplementary Fig. 34, whose caption describes richness, dominance frequency, and pairwise species selection, not reconstructed matrices.

**Recommended fix:** Cite the correct matrix figure if available, or remove the matrix-specific claim from this paragraph.

### [WARNING] Note 2 assembly mechanism needs one more reasoning step

**Location:** `supplementary_sections/assembly_effect.tex:10,14`

Fig. 18 supports reduced post-assembly interaction strength, but the Note also says the reduction becomes more pronounced at higher mu because stronger competition drives more extinctions. Fig. 19 supports Base/Nutr+ coalescence versus direct assembly, but the Nutr- explanation is stated as likely weaker competitive interactions without direct support in that paragraph.

**Recommended fix:** Add a bridge sentence or citation connecting nutrient-limited weaker interactions to the invasion/interaction evidence.

### [NOTE] Some quantitative claims in captions/Notes need explicit support

**Locations:** `skewness_null_model.tex:33`; `simulations.tex:19`

The nutrient-dependent continuous-similarity trend across Supplementary Figs. 29-32 requires comparing separate panels, and the Pearson correlations in the mean-vs-variance sweep are not mentioned in Fig. 42's caption.

**Recommended fix:** Either add those quantitative details to the relevant captions or soften the Note text.

---

## Agent B Only - Navigation Problems

### [WARNING] Note 3 opening does not preview the robustness section

**Location:** `supplementary_sections/simulations.tex:7`

The opening explains mu but not the full purpose: distribution shape, richness, facilitation, reciprocal coupling, mutualism, and mean-vs-variance robustness.

**Recommended fix:** Add a short roadmap sentence after the first paragraph.

### [WARNING] Note 5 opening dives into OD before giving a roadmap

**Location:** `supplementary_sections/alternative_models_controls.tex:7`

The Note covers OD/biomass loading, pool size, pH feedback, dominant-species removal, additive nulls, and facilitation-related model variants, but the first paragraph only frames OD.

**Recommended fix:** Add a compact opening sentence listing the control classes covered.

### [WARNING] Supplementary Fig. 29 caption lacks a key-result statement

**Location:** `figures.tex:376`

The caption says what is plotted, but not the takeaway or why the figure exists beyond method transparency.

**Recommended fix:** Add one sentence linking the continuous distributions to the robustness of categorical outcome classification.

### [NOTE] Caption self-containment can be improved for ED Fig. 1, Supp Fig. 8, and Supp Fig. 22

**Locations:** `extended_data.tex:14`; `figures.tex:121,320`

These captions say what is plotted, but their purpose in the SI argument is not fully explicit.

**Recommended fix:** Add one short "why this figure exists" sentence to each.

---

## Agent C Only - Internal Consistency

### [NOTE] Metric terminology drifts across Notes and captions

**Locations:** `assembly_effect.tex:21`; `alternative_models_controls.tex:11`; `figures.tex:416,482`

Terms include "pairwise selection correlation", "pairwise species selection", "pairwise-selection gap", and "same-parent concordance". They appear related but are not explicitly mapped.

**Recommended fix:** Standardize terms where possible. If metrics differ, define the relationship once.

### [NOTE] Interaction-distribution notation drifts

**Locations:** `simulations.tex:7,9`; `extended_data.tex:38`; `figures.tex:474`

The baseline distribution appears as `U[0,2\mu]`, `U[0, 2\mu]`, and `U(0, 2\mu)`.

**Recommended fix:** Use one notation consistently, preferably `U[0,2\mu]` if treating the support as a closed interval.

### [NOTE] Cross-note references checked out

Note 5 references Supplementary Notes 1 and 3 accurately, and Extended Data captions pointing to Notes 1 and 3 match their contents.

---

## Verdicts

- **Agent A:** Major revision of SI structure. Several central claims are plausible but not explicitly tied to figure evidence, especially null-model and invasion-assay claims.
- **Agent B:** Difficult to navigate. Many Supplementary Figures are uncited by the Notes, and several captions/openings assume main-text context.
- **Agent C:** Minor issues. No major contradictions, but sample counts and metric terms need clarification.
- **Overall:** Major revision of SI self-containment. The science narrative is mostly internally consistent, but the SI needs explicit figure citations, clearer figure homes, and count/terminology cleanup before it can stand alone.
