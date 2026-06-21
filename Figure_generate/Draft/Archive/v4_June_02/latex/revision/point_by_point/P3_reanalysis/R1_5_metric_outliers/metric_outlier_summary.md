# R1-5 Metric-Outlier Audit

Events analyzed: 83 Base-medium synthetic coalescence events after the existing exclusion list.

## Outcome Counts

- vector: Dominance 54/83 (65.1%), Mixture 3/83 (3.6%), Restructuring 26/83 (31.3%)
- euclidean: Dominance 47/83 (56.6%), Mixture 9/83 (10.8%), Restructuring 27/83 (32.5%)
- bray_curtis: Dominance 44/83 (53.0%), Mixture 18/83 (21.7%), Restructuring 21/83 (25.3%)
- jensen_shannon: Dominance 20/83 (24.1%), Mixture 34/83 (41.0%), Restructuring 29/83 (34.9%)
- jaccard: Dominance 21/83 (25.3%), Mixture 27/83 (32.5%), Restructuring 35/83 (42.2%)

## Confusion Versus Vector Decomposition

### jensen_shannon

| vector        |   Dominance |   Mixture |   Restructuring |
|:--------------|------------:|----------:|----------------:|
| Dominance     |          19 |        30 |               5 |
| Mixture       |           0 |         3 |               0 |
| Restructuring |           1 |         1 |              24 |

### jaccard

| vector        |   Dominance |   Mixture |   Restructuring |
|:--------------|------------:|----------:|----------------:|
| Dominance     |          13 |        19 |              22 |
| Mixture       |           2 |         1 |               0 |
| Restructuring |           6 |         7 |              13 |

## Dominance-Loss Feature Summary

### jensen_shannon

| metric         | feature                                   |   dominance_lost_n |   dominance_stable_n |   dominance_lost_median |   dominance_stable_median |   mannwhitney_p |
|:---------------|:------------------------------------------|-------------------:|---------------------:|------------------------:|--------------------------:|----------------:|
| jensen_shannon | retained_abundance_skew                   |                 35 |                   19 |                 0.897   |                  1        |         0.0795  |
| jensen_shannon | retained_richness_skew                    |                 35 |                   19 |                 0.6     |                  1        |         0.3881  |
| jensen_shannon | mix_richness                              |                 35 |                   19 |                 8       |                  6        |         0.05207 |
| jensen_shannon | retained_richness                         |                 35 |                   19 |                 5       |                  3        |         0.1544  |
| jensen_shannon | rare_taxa_count                           |                 35 |                   19 |                 4       |                  3        |         0.8124  |
| jensen_shannon | rare_abundance_fraction                   |                 35 |                   19 |                 0.01494 |                  0.008281 |         0.5371  |
| jensen_shannon | rare_retained_taxa_fraction               |                 35 |                   19 |                 0.25    |                  0.3571   |         0.1921  |
| jensen_shannon | abundance_skew_high_but_richness_skew_low |                 35 |                   19 |                 0.1714  |                  0.3158   |         0.3066  |

### jaccard

| metric   | feature                                   |   dominance_lost_n |   dominance_stable_n |   dominance_lost_median |   dominance_stable_median |   mannwhitney_p |
|:---------|:------------------------------------------|-------------------:|---------------------:|------------------------:|--------------------------:|----------------:|
| jaccard  | retained_abundance_skew                   |                 41 |                   13 |                 0.897   |                  1        |        0.006182 |
| jaccard  | retained_richness_skew                    |                 41 |                   13 |                 0.3333  |                  1        |        0.003958 |
| jaccard  | mix_richness                              |                 41 |                   13 |                 7       |                  6        |        0.9919   |
| jaccard  | retained_richness                         |                 41 |                   13 |                 4       |                  5        |        0.4205   |
| jaccard  | rare_taxa_count                           |                 41 |                   13 |                 3       |                  5        |        0.4691   |
| jaccard  | rare_abundance_fraction                   |                 41 |                   13 |                 0.01064 |                  0.009273 |        1        |
| jaccard  | rare_retained_taxa_fraction               |                 41 |                   13 |                 0.2857  |                  0.4444   |        0.46     |
| jaccard  | abundance_skew_high_but_richness_skew_low |                 41 |                   13 |                 0.2683  |                  0.07692  |        0.2538   |

- jensen_shannon reclassified 35/54 vector-Dominance events (64.8%) as non-Dominance.
- jaccard reclassified 41/54 vector-Dominance events (75.9%) as non-Dominance.
