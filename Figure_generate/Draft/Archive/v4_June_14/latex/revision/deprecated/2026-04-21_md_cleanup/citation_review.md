# Citation Review Report

**Manuscript:** Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence
**Date:** 2026-02-03
**Scope:** All citations in main text (abstract, introduction, results, discussion) and supplementary materials

---

## Summary

Reviewed all citations across the manuscript. Most citations are bibliographically correct and contextually appropriate. Found **3 issues requiring action**, **4 minor concerns worth noting**, and confirmed the remainder are accurate.

---

## Issues Requiring Action

### 1. WRONG AUTHORS -- Huet2025 (references.bib line 618)

**Location:** Introduction (line 9, `introduction.tex`)
**Bib entry authors:** Huet, Sebastien; Romdhane, Sana; Breuil, Marie-Christine; Riviere, David; Moenne-Loccoz, Yvan; Ranjard, Lionel
**Actual authors:** Huet, Sarah; Romdhane, Sana; Breuil, Marie-Christine; Bru, David; Mounier, Arnaud; Philippot, Laurent; Spor, Ayme

The first name is wrong (Sebastien vs. Sarah), and the last four co-authors are entirely different people. The author list appears to have been copied from the earlier Huet2023 entry (a different paper from a partially overlapping group at the same Dijon lab). The title, journal (ISME Communications), volume, pages, year, and DOI are all correct -- only the author list needs fixing.

**Fix:** Replace the author field in the `Huet2025` bib entry with the correct authors.

---

### 2. POOR FIT -- Debray2022 citation (introduction.tex line 11)

**Location:** Introduction paragraph 3
**Current usage:** "Because species within such communities have been filtered to coexist, their survival outcomes become coupled, producing asymmetric post-coalescence communities dominated by one parental community \citep{Debray2022}."
**Problem:** Debray et al. (2022) is a review about **priority effects in microbiome assembly** -- how arrival order shapes community composition. It is not about coalescence asymmetry or the coupling of species survival outcomes in pre-assembled communities. The specific claim about competitive filtering producing asymmetric post-coalescence dominance is the core argument of Gilpin (1994), Tikhonov (2016), and Lechon (2021), all of which are already cited in the same paragraph. Debray et al. defines "community coalescence" in a glossary box and mentions it as a context where priority effects matter, but does not develop the argument attributed to it here.

**Fix:** Consider replacing with a more directly relevant citation (e.g., Tikhonov2016, DiazColunga2022, or Sierocinski2017), or repositioning Debray2022 to a sentence about priority effects.

---

### 3. QUESTIONABLE FIT -- Lopes2024 citation (discussion.tex line 16)

**Location:** Discussion paragraph 4
**Current usage:** "...host filtering, priority effects, and spatial structure further influence successful colonization, making coalescence a useful framework for predicting and steering microbiome transfer \citep{Liu2024, Smillie2018, Lopes2024}."
**Problem:** Lopes et al. (2024) is about **cooperative growth driving multistability** in microbial communities. It does not discuss host filtering, spatial structure, coalescence, or microbiome transfer. The paper's focus is on how cooperative (positive) interactions underlie bistability in pairwise interactions that scale to community-level multistability. While multistability is conceptually related to priority effects, the paper does not address the specific topics in this sentence.

**Fix:** Consider moving this citation to a sentence about alternative stable states or multistability. Liu2024 and Smillie2018 are appropriate for the current sentence.

---

## Minor Concerns (Worth Noting)

### 4. Slightly imprecise -- DiazColunga2022 (introduction.tex line 11)

**Current text:** "correlated selection between dominant and subdominant taxa has been observed across 100 coalescence experiments"
**Actual:** The paper states "over 100 invasion **and** coalescence experiments" -- the count includes both invasion experiments (single species invading a community) and coalescence experiments (community vs. community). Not all 100+ were coalescence experiments.

**Suggestion:** Change to "over 100 invasion and coalescence experiments" for precision.

---

### 5. Tangential -- Lovelock1979 (introduction.tex line 7)

**Current usage:** Cited alongside Clements1916, Clements1936, Odum1969, and WilsonSober1989 for the "superorganism" view of communities with emergent properties.
**Issue:** The Gaia hypothesis is about Earth as a planetary-scale self-regulating system, not about ecological communities as superorganisms in the Clementsian sense. While Clements and Lovelock share a loose conceptual lineage through the superorganism metaphor, Lovelock's work is about geophysiology and biogeochemical feedbacks, not community assembly or community-level selection. The other four references in this cluster are all directly relevant.

**Suggestion:** Consider removing Lovelock1979 from this citation cluster, or broadening the sentence to acknowledge the planetary-scale extension of the superorganism idea. This is minor and defensible as-is.

---

### 6. Slight overstatement -- BentonEmerson2007 (introduction.tex line 13)

**Current text:** "species from the same community rarely go extinct together in the fossil record"
**Actual:** Benton & Emerson (2007) is a broad review about diversification dynamics. It discusses the Gleasonian/individualistic paradigm and how species responded individually to Quaternary climate changes (shifting ranges rather than going extinct as cohesive units). The specific claim "species from the same community rarely go extinct together" is a reasonable inference from the paper's discussion of Gleasonian dynamics, but it is not a direct finding or conclusion of the paper.

**Suggestion:** Consider softening to "species appear to respond independently to environmental changes in the fossil record" or supplementing with a more targeted reference on community disassembly in the fossil record.

---

### 7. Imprecise description -- Goldman2025 + Walton2025 (introduction.tex lines 13-14)

**Current text:** "Strain-resolved metagenomic analyses of in vitro gut microbial communities showed species-level dynamics rather than community-level selection, with recruiting surviving species originating from both parental communities"
**Issues:**
- "Strain-resolved metagenomic analyses" applies to Walton2025 (which tracks marker SNVs to distinguish conspecific strains) but **not** to Goldman2025 (which works at the species level using community composition tracking and consumer-resource modeling).
- Walton2025 actually shows **strain-level** (intra-species) dynamics, which is finer resolution than "species-level dynamics."

**Suggestion:** Use a more general phrasing like "Detailed compositional and strain-resolved analyses" or split the sentence to describe each paper's methodology more precisely.

---

## Confirmed Correct Citations

The following citations were verified for both bibliographic accuracy and contextual appropriateness:

| Citation | Section | Verification |
|----------|---------|-------------|
| Clements1916 | Introduction | Correct -- foundational superorganism reference |
| Clements1936 | Introduction | Correct -- climax community elaboration |
| Gleason1939 | Introduction | Correct -- widely cited expanded version of 1926 paper |
| Cain1947, Mason1947, Whittaker1967 | Introduction | Correct -- Gleasonian individualistic tradition |
| Odum1969 | Introduction | Correct -- ecosystem development/superorganism |
| WilsonSober1989 | Introduction | Correct -- reviving superorganism concept |
| Rillig2015 | Introduction, Discussion | Correct -- foundational coalescence review |
| Lechon2021 | Introduction, Results | Correct -- resource-consumer model for coalescence |
| Huet2023 | Introduction | Correct -- soil coalescence experiments |
| Bresciani2025 | Introduction | Correct -- verified, published 2025 |
| Liu2024 | Introduction, Discussion | Correct -- coalescence drivers/consequences review |
| Sarkar2024 | Introduction | Correct -- microbial transmission in social microbiome |
| Xiao2020 | Introduction | Correct -- FMT ecological framework |
| Gupta2016 | Introduction | Correct -- FMT review |
| Gilpin1994 | Introduction, Results | Correct -- foundational community-level competition theory |
| Tikhonov2016 | Introduction, Discussion | Correct -- resource-consumer cohesion model |
| Vermeij1991 | Introduction, Discussion | Correct -- biotic interchange review; minor note that "niche partitioning" is inferred rather than explicitly stated |
| Brochet2021 | Introduction | Correct metadata; note this is about niche partitioning within the honey bee gut, not a coalescence study |
| VanderGucht2007 | Introduction, Discussion | Correct -- species sorting vs. mass effects in bacterial communities |
| Walton2025 | Introduction, Discussion | Correct -- bioRxiv preprint (Nov 2025), verified real |
| Goldman2025 | Introduction, Discussion | Correct -- PNAS 2025, verified |
| Hu2022 | Results | Correct -- emergent ecological phases, nutrient-interaction link |
| Hu2025 | Results, Discussion | Correct -- dynamical regimes and invasion |
| Ratzke2020 | Results, Discussion | Correct -- interaction strength determines biodiversity/stability |
| Ratzke2018 | Results | Correct -- pH-mediated bacterial interactions |
| Rillig2017, Castledine2020 | Results, Discussion | Correct -- coalescence reviews |
| Nadell2016 | Discussion | Correct -- biofilm spatial structure and interactions |
| Kurkjian2021 | Discussion | Correct -- interaction impact on invasion/colonization |
| Fukami2015 | Discussion | Correct -- historical contingency and priority effects |
| Tropini2017 | Discussion | Correct -- gut spatial organization |
| Smillie2018 | Discussion | Correct -- strain engraftment in FMT |
| Marsland2019 | Discussion | Correct -- energy flux and microbial diversity |
| Madeira2022 | Supplementary | Correct -- EMBL-EBI tools |
| Callahan2016 (DADA2) | Methods/Supplementary | Correct -- referenced in methods context |
| Quast2013 (SILVA) | Methods/Supplementary | Correct -- SILVA database |

---

## Supplementary-Specific Notes

The supplementary materials (Notes 1-5, Figures, Extended Data) contain very few additional citations beyond those already verified in the main text. The two supplementary-specific citations (Madeira2022 for phylogenetic tree construction, and implicit references to DADA2/SILVA for sequencing pipeline) are both correct and appropriately used.

---

## VanderGucht2007 -- Minor Bib Note

The bib entry lists the first author's given name as "Koenraad" but PubMed records indicate the first author is "Katleen Van der Gucht" (Koenraad Muylaert is actually the third author). This does not affect the rendered citation since bibliography styles use "Van der Gucht, K. et al." which is correct for either name, but the first name in the bib entry is technically wrong.
