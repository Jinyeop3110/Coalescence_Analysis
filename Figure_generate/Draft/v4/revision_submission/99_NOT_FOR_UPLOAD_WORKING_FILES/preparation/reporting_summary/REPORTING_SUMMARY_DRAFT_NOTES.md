# Reporting Summary Draft Notes

Official form downloaded here:

- `nr-reporting-summary_blank.pdf`

Official source:

- https://nature.com/documents/nr-reporting-summary.pdf

Use Adobe Reader to complete the PDF form. Browser PDF viewers may not save the fillable fields correctly.

## Paper

Title:

`Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence`

Corresponding author:

`Jeff Gore`

Authors:

`Jinyeop Song, Jiliang Hu, Jeff Gore`

## Reporting Summary Content To Fill

### Statistics

Likely relevant notes from the manuscript:

- Statistical significance defined as `p < 0.05`.
- Paired t-tests compare interaction strength values before and after assembly.
- Permutation tests with 1,000 permutations assess pairwise selection correlations.
- Mann-Whitney U tests compare experimental values against null distributions.
- Chi-square tests for trend assess outcome fraction shifts across nutrient conditions.
- Fisher exact tests compare categorical outcomes between conditions.
- Linear regression quantifies predictability of coalescence outcomes from dominant-species competition.
- Spearman correlations are used in some revision analyses and supplementary controls.
- Error bars are mean plus/minus s.e.m. unless noted otherwise.

Need verify before final form:

- exact software versions for Python/R/packages
- whether all tests are one-sided or two-sided in every figure/caption
- multiple-comparison correction policy, if any
- exact sample sizes for each figure panel

### Sample Size

Likely values from current manuscript:

- Base synthetic coalescence: `n = 83` pairwise coalescence events.
- Nutrient perturbation coalescence: Nutr- `n = 90`, Base `n = 83`, Nutr+ `n = 90`.
- Pairwise invasion assays: `n = 132` assays per medium.
- Natural sample-derived coalescence: `n = 30` events per condition.
- gLV simulations in main panels: `n = 1,200` simulations per condition where stated.

Need verify before final form:

- whether biological replicates should be counted separately or summarized by event in each analysis
- exact exclusion criteria for failed sequencing, low abundance, or invalid pairwise correlations
- whether sample sizes were predetermined or constrained by experimental design

### Randomization

Draft wording to adapt:

`Synthetic parental communities were assembled by assigning bacterial isolates from the strain library to predefined non-overlapping species pools. Pairwise coalescence events were then constructed from stabilized parental communities according to the experimental design. The gLV simulations used random draws of interaction matrices and random species assignment to parental communities as specified in the Methods and Supplementary Methods.`

Need verify:

- whether plate positions, community pairings, or sample processing order were randomized
- whether any blocking by plate, medium, or batch should be stated

### Blinding

Draft wording to adapt:

`Blinding was not used because outcome classification and statistical analyses were computed from sequencing-derived abundance tables and predefined quantitative criteria.`

Need verify:

- whether colony-counting or manual pH/OD steps could have involved subjective scoring

### Data Exclusions

Draft wording to adapt:

`ASVs were filtered using a relative-abundance threshold of 0.1%, matching the extinction threshold used in simulations. Additional exclusions, if any, should be listed explicitly from the analysis scripts and figure captions.`

Need verify:

- any samples removed for low sequencing depth, contamination, failed growth, missing OD/pH, or invalid coalescence classification

### Replication

Draft wording to adapt:

`Synthetic and natural sample-derived communities were propagated through repeated serial-transfer cycles before and after coalescence. Natural sample-derived coalescence experiments used two biological replicates per pairwise event. Simulation results are based on independent random interaction matrices and replicate community assemblies.`

Need verify:

- exact biological replicate handling for the synthetic community experiments
- whether technical sequencing replicates exist

### Software And Code

Current manuscript statement:

`All code used for simulation and analysis is available via GitHub at https://github.com/Jinyeop3110/interspecies-interaction-derive-Community-Level-Selection.`

Need finalize:

- Python version
- R version if R scripts are included
- major package versions
- archival DOI if GitHub is archived with Zenodo

### Data Availability

Current manuscript statement:

`Isolates and communities are available upon request. All data are available in the Supplementary Information and via Dryad at http://datadryad.org/share/LINK_NOT_FOR_PUBLICATION/kQACU7LCmQclVZfGZk0bS5ZPUVL_grhwah2zvFY4m9s.`

Need finalize:

- confirm private Dryad link works for reviewers
- replace `LINK_NOT_FOR_PUBLICATION` with public DOI/accession before publication
- confirm whether raw 16S reads are in Dryad only or also SRA/ENA/DDBJ

