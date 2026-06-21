# Reporting Summary Copy/Paste Draft

This file is for filling the Nature Reporting Summary by copy/paste. It does not edit the PDF.

Source form:

- `nr-reporting-summary_blank.pdf`

Manuscript sources checked:

- `latex/sections/methods.tex`
- `latex/supplementary_sections/supplementary_methods.tex`
- `revision_submission/preparation/data_code_availability/DATA_CODE_AVAILABILITY_DRAFT.md`

Items marked `VERIFY` should be checked before portal submission.

## Paper Information

### Title

```text
Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence
```

### Corresponding Author

```text
Jeff Gore
```

### Authors

```text
Jinyeop Song, Jiliang Hu, Jeff Gore
```

### Last Updated

```text
June 16, 2026
```

## Field Selection

Recommended field-specific section:

```text
Ecological, evolutionary & environmental sciences
```

Study involved field work:

```text
Yes
```

Rationale: the study uses bacterial isolates and natural communities derived from environmental samples collected in Cambridge, MA, USA. Most experiments were laboratory microcosm experiments, but the sample origin includes field-collected environmental material.

## Statistics Checklist

The PDF statistics section is mostly a confirmation checklist. Suggested entries:

| Item | Suggested status | Notes |
| --- | --- | --- |
| Exact sample size for each group/condition | Confirmed | Main text, Methods, Supplementary Methods, and legends report n values for major analyses. |
| Whether measurements were distinct or repeated | Confirmed | Biological replicates are retained as separate event-level observations where stated. |
| Statistical tests and one- or two-sided status | Confirmed | Methods state that tests are two-sided unless explicitly stated otherwise. |
| Covariates tested | Confirmed | Mixed-effects models control for parental richness and community identity where used. |
| Assumptions or corrections | VERIFY | Confirm whether a multiple-comparison correction statement is needed. |
| Descriptive statistics and uncertainty | Confirmed | Means and s.e.m. are stated where error bars are shown. |
| Null-hypothesis statistics and p values | Confirmed | P values and tests are given in the relevant text/legends. |
| Bayesian analysis | Not applicable | No Bayesian analysis is reported. |
| Hierarchical/complex designs | Confirmed | Mixed-effects analyses are described for nutrient-dependence controls. |
| Effect sizes | Confirmed | R2, correlation coefficients, outcome fractions, and related estimates are reported where relevant. |

## Software And Code

### Data Collection

```text
Experimental data were collected using standard laboratory instruments and associated acquisition workflows. Optical density at 600 nm was measured with a BioTek Synergy H1 plate reader. Community pH was measured with an Apera Instruments PH5500 pH meter. 16S rRNA amplicon sequencing was performed by Argonne National Laboratory on an Illumina MiSeq platform. Final compositions in pairwise invasion assays were determined by colony counting. No custom software was used for experimental data acquisition. VERIFY instrument-control software versions if the portal requires them.
```

### Data Analysis

```text
16S rRNA amplicon reads were demultiplexed and denoised using QIIME2 and DADA2, and ASVs were taxonomically classified against the SILVA v138 database. Most analyses were performed in Python 3.11 using NumPy, pandas, SciPy and scikit-learn. Mixed-effects models were fit in R using lme4. Custom scripts were used for generalized Lotka-Volterra simulations, coalescence outcome classification, statistical analyses, and figure generation. All code used for simulation and analysis is available via GitHub at https://github.com/Jinyeop3110/interspecies-interaction-derive-Community-Level-Selection. VERIFY final package versions and whether a permanent Zenodo DOI will be added.
```

## Data Availability

### Revision-Stage Paste Text

```text
Isolates and communities are available upon request. All data are available in the Supplementary Information and via Dryad at http://datadryad.org/share/LINK_NOT_FOR_PUBLICATION/kQACU7LCmQclVZfGZk0bS5ZPUVL_grhwah2zvFY4m9s. Raw sequencing reads are available via Dryad, as stated in the Methods. VERIFY that the private Dryad reviewer link works and that raw 16S reads, processed abundance tables, metadata, taxonomy tables, simulation outputs, and figure source data are all included.
```

### Final-Publication Template

Use only after public accessions/DOIs are confirmed.

```text
Raw sequencing reads, processed community-composition tables, sample metadata, taxonomic annotations, simulation outputs, and figure source data are available from Dryad at [DRYAD DOI]. Isolates and communities are available upon request. Code used for simulations, analyses, and figure generation is available at GitHub (https://github.com/Jinyeop3110/interspecies-interaction-derive-Community-Level-Selection) and archived at [ZENODO OR OTHER CODE DOI, IF AVAILABLE].
```

## EEE Study Design

Use this section if the form asks for "Ecological, evolutionary & environmental sciences study design".

### Study Description

```text
This is a quantitative experimental and theoretical study of microbial community coalescence. Synthetic parental communities were assembled from a 54-isolate environmental bacterial library, stabilized by serial transfer, mixed pairwise at a 1:1 volume ratio, and propagated to post-coalescence endpoints under three nutrient conditions: Nutr-, Base, and Nutr+. Treatment factors included nutrient condition, inoculated richness, parental-community identity, and, in simulations, the generalized Lotka-Volterra interaction-strength parameter mu. Community composition was measured from 16S rRNA amplicon sequencing and analyzed as ASV relative-abundance profiles. Coalescence outcomes were classified as Dominance, Mixture, or Restructuring using predefined similarity-based criteria. Pairwise invasion assays and generalized Lotka-Volterra simulations were used to test interaction-dependent mechanisms, and natural sample-derived communities provided an additional test in taxonomically richer environmental assemblages.
```

### Research Sample

```text
The synthetic-community experiments used a library of 54 bacterial isolates derived from environmental samples collected in Cambridge, MA, USA, including soil, tree surface, and flower stamen environments. The isolate library spans 29 families across Proteobacteria, Firmicutes, and Bacteroidota. Natural sample-derived communities were generated from six additional environmental samples from soil, compost, and decomposing organic matter collected in Cambridge, MA, USA. These samples were chosen to provide environmentally derived bacterial communities with broad taxonomic, growth, and environmental-modification diversity. The study did not involve human participants, human data, vertebrate animals, or clinical samples.
```

### Sampling Strategy

```text
No formal statistical sample-size calculation was performed. Experimental sample sizes were chosen based on the 54-isolate library size, the combinatorial design of non-overlapping or partially overlapping parental communities, 96-well plate capacity, and feasibility of serial-transfer coalescence experiments. Synthetic parental communities were assembled at inoculated richness levels of 6, 12, or 24 species, yielding 30 parental communities. Forty-seven synthetic coalescence pairs were planned with two biological replicates each, yielding 94 total Base-medium events before exclusions and 83 valid Base-medium events after sequencing failures or contamination were removed. Nutrient-perturbation coalescence experiments included Nutr- n = 90, Base n = 83, and Nutr+ n = 90 events. Pairwise invasion assays tested the 12 most abundant isolates in both directions across three media, corresponding to 132 directional assays per medium. Natural sample-derived experiments used 15 pairwise coalescence events with two biological replicates per event, yielding n = 30 events per nutrient condition. Main generalized Lotka-Volterra simulation panels used n = 1,200 coalescence simulations per condition where stated.
```

### Data Collection

```text
Jinyeop Song and Jiliang Hu performed the experiments. Isolates and communities were grown in 300 microliter volumes in 96-well deep-well plates at 25 C with shaking at 800 rpm. Parental communities were stabilized through seven daily 30-fold serial dilutions before coalescence. Coalescence experiments mixed two pre-stabilized parental communities at equal volume ratio and propagated the mixtures through seven additional daily serial transfers. Community composition was measured by V4-region 16S rRNA amplicon sequencing after DNA extraction with the QIAGEN DNeasy PowerSoil kit. Optical density was measured with a BioTek Synergy H1 plate reader, and pH was measured with an Apera Instruments PH5500 pH meter. Pairwise invasion endpoints were measured by colony counting after seven daily dilution cycles.
```

### Timing And Spatial Scale

```text
Environmental samples and isolates were collected in Cambridge, MA, USA, and experiments were performed as laboratory microcosms in 300 microliter wells. Synthetic and natural communities were propagated by daily 30-fold serial transfer, with seven transfers before coalescence and seven transfers after coalescence for endpoint measurements. The spatial scale of the experiments was the microplate well, and the spatial scale of environmental sampling was local Cambridge, MA microhabitats. VERIFY exact start and stop dates of environmental sampling, culture experiments, sequencing, and analysis before submission if the portal requires calendar dates.
```

### Data Exclusions

```text
ASV tables were filtered to retain taxa with at least 0.1% relative abundance in any sample, matching the extinction threshold used in simulations. In the Base synthetic coalescence experiment, 47 planned coalescence pairs with two biological replicates yielded 94 total events; 11 events were excluded due to sequencing failures or contamination, resulting in 83 valid Base-medium events. Simulated species with relative abundance below 0.1% were set to zero at assembly and coalescence endpoints. Exclusions were based on sequencing quality, contamination, missing/invalid data, or predefined abundance thresholds, not on the direction or class of coalescence outcome. VERIFY whether any additional sample exclusions occurred in Nutr-, Nutr+, natural-community, invasion-assay, or revision-control analyses.
```

### Reproducibility

```text
Synthetic coalescence pairs were performed with two biological replicates where planned, and natural sample-derived coalescence events were performed with two biological replicates per pair. Communities were stabilized through repeated serial-transfer cycles before coalescence and propagated through repeated serial transfers after coalescence before endpoint sequencing. Pairwise invasion assays tested each isolate pair in reciprocal resident-invader directions across media. Simulation results were reproduced across independent random interaction matrices and randomized parental-community assignments, with robustness analyses using alternative model assumptions. Failed or invalid samples are described under Data exclusions.
```

### Randomization

```text
Synthetic parental communities were assembled by predefined assignment of isolates from the strain library into non-overlapping or partially overlapping species pools rather than by random allocation. Pairwise coalescence events were then constructed systematically from stabilized parental communities according to the experimental design. Pairwise invasion assays tested all pairwise combinations among the 12 most abundant isolates in both resident-invader directions. In generalized Lotka-Volterra simulations, species identities were randomly permuted and assigned to parental communities, and independent interaction matrices were sampled for each replicate. Because the laboratory allocation was design-based rather than randomized, covariates were controlled by using predefined community construction rules, matched culture conditions, the same serial-transfer protocol, and within-design comparisons across nutrient conditions. VERIFY whether plate position, processing order, or sequencing order were randomized or blocked.
```

### Blinding

```text
Blinding was not used. Outcome classification and statistical analyses were computed from sequencing-derived ASV relative-abundance tables, colony-count thresholds, and predefined quantitative criteria. Because the primary outcomes were algorithmic or threshold-based rather than subjective visual classifications, blinding was not central to outcome assignment. VERIFY whether any manual colony counting, sample handling, or data-processing steps were performed blind to treatment condition.
```

## Field Work, Collection And Transport

Use this section because the study used environmental isolates and natural community samples.

### Field Conditions

```text
Environmental material was collected from local microhabitats in Cambridge, MA, USA, including soil, tree surface, flower stamen, compost, and decomposing organic matter. Field conditions were not experimental treatment variables, and subsequent experiments were performed under controlled laboratory conditions. VERIFY whether collection temperature, weather, season, or other field-condition metadata should be reported.
```

### Location

```text
Samples were collected in Cambridge, MA, USA, from local soil, tree surface, flower stamen, compost, and decomposing organic matter microhabitats. VERIFY whether exact site descriptions, GPS coordinates, or institutional location details should be added before submission.
```

### Access And Import/Export

```text
Samples were collected locally in Cambridge, MA, USA and were not imported or exported internationally. VERIFY that no site-specific permits were required and that no protected habitats or protected species were sampled.
```

### Disturbance

```text
Sampling disturbance was minimal and limited to collecting small amounts of environmental material or surface-associated microbial samples for laboratory enrichment and isolate recovery. No large-scale habitat manipulation was performed.
```

## Optional Life Sciences Study Design

Use this only if the portal asks for the shorter "Life sciences study design" section instead of, or in addition to, the EEE section.

### Sample Size

```text
No formal statistical sample-size calculation was performed. Sample sizes were determined by the 54-isolate library, the predefined community-assembly design, 96-well plate capacity, and the feasible number of serial-transfer coalescence experiments. Synthetic analyses included 30 parental communities and 83 valid Base-medium coalescence events after exclusions. Nutrient-perturbation experiments included Nutr- n = 90, Base n = 83, and Nutr+ n = 90 events. Natural sample-derived experiments used n = 30 events per nutrient condition. Pairwise invasion assays used 132 directional assays per medium. Main generalized Lotka-Volterra simulation panels used n = 1,200 coalescence simulations per condition where stated.
```

### Data Exclusions

```text
ASV tables were filtered at a 0.1% relative-abundance threshold. In Base synthetic coalescence experiments, 11 of 94 planned events were excluded because of sequencing failures or contamination, leaving 83 valid events. Simulated taxa below the 0.1% relative-abundance threshold were set to zero. Exclusions were based on predefined abundance thresholds, sequencing failures, contamination, or invalid/missing data, not on the observed coalescence outcome. VERIFY any additional exclusions in nutrient-perturbation, natural-community, pairwise-invasion, or revision-control analyses.
```

### Replication

```text
Synthetic and natural sample-derived coalescence experiments used biological replicates where planned, with natural sample-derived events performed as two biological replicates per pair. Communities were stabilized before coalescence and propagated after coalescence through repeated serial-transfer cycles. Pairwise invasion assays tested reciprocal resident-invader directions. Simulation results were repeated across independently sampled interaction matrices and parental-community assignments.
```

### Randomization

```text
Laboratory community assembly used predefined design-based assignment of isolates and parental communities rather than random allocation. Pairwise coalescence and invasion assays followed systematic experimental designs. Simulations used randomized species permutations, random parental-community assignment after permutation, and independently sampled interaction matrices. VERIFY whether plate positions or processing order were randomized or blocked.
```

### Blinding

```text
Blinding was not used because outcome classification and statistical analyses were computed from sequencing-derived abundance tables, colony-count thresholds, and predefined quantitative criteria. VERIFY whether any manual sample-processing or colony-counting steps were blind to treatment condition.
```

## Specific Materials, Systems And Methods

Suggested selections:

| Module | Suggested entry |
| --- | --- |
| Antibodies | No |
| Cell lines | No |
| Palaeontology | No |
| Animals and other organisms | No vertebrate animals. Microbial environmental isolates are described in the EEE section. |
| Clinical data | No |
| Dual use research of concern | No, unless institutional review says otherwise. |
| Plants | No plant genotypes, seed stocks, or plant transformation experiments. Environmental plant-associated microbial sampling is described under field collection. |
| ChIP-seq | No |
| Flow cytometry | No |
| MRI | No |

## Final Checks Before Copy/Paste

- Replace `VERIFY` statements with final facts or remove them.
- Confirm exact experiment and collection dates if the portal requires them.
- Confirm whether the Dryad private-review link is acceptable for revision upload.
- Confirm whether raw 16S reads are deposited in Dryad only or also in SRA/ENA/DDBJ.
- Confirm package versions for QIIME2, DADA2, NumPy, pandas, SciPy, scikit-learn, R, and lme4.
- Confirm whether any plate-position, processing-order, or sequencing-order randomization/blocking occurred.
- Confirm whether any exclusions beyond the Base-medium 11 sequencing/contamination exclusions should be listed.
