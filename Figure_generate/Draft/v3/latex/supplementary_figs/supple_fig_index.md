# Supplementary Figure Index

This document maps the supplementary figure definitions in `supplementary_sections/figures.tex` to the actual figure files in `supplementary_figs/`.

## Mapping Summary

| Fig # | Caption (from figures.tex) | Available File | Status |
|-------|---------------------------|----------------|--------|
| S1 | Table of phylogenetic taxonomy for 43 ASV isolates | `taxonomy_color_map.svg` | MATCHED |
| S2 | Phylogeny map (EMBL) | `Fig_1-3_phylogeny_tree.pdf` | MATCHED |
| S3 | Time series in Base media | - | MISSING |
| S4 | Robustness of Fig.1 across various similarity metrics | `Fig_robustness_comparison_MN_merged.svg` | MATCHED |
| S5 | Selection Preference Ratio in Base media | `correlation_barplot_MN.svg` | MATCHED |
| S6 | Simulation: growth-rate heterogeneity | - | MISSING |
| S7 | Simulation: carrying-capacity variation | - | MISSING |
| S8 | Simulation: alternative α_ij sampling distributions | - | MISSING |
| S9 | Nutr- pairwise invasion | `Pairwise_Matrix_Dynamics_LN_improved.pdf` | MATCHED |
| S10 | Base pairwise invasion | `Pairwise_Matrix_Dynamics_MN_improved.pdf` | MATCHED |
| S11 | Nutr+ pairwise invasion | `Pairwise_Matrix_Dynamics_HN_improved.pdf` | MATCHED |
| S12 | Nutr- time series | - | MISSING |
| S13 | Nutr+ time series | - | MISSING |
| SX | Selection Preference Ratio in Nutr-/Nutr+ media | `correlation_barplot_LN.svg`, `correlation_barplot_HN.svg` | MATCHED |
| S14 | Linear coefficients of fitted regression model | - | MISSING |
| S15 | Species correlated with final pH | - | MISSING |
| S16 | Introducing more hierarchical effective interactions | - | MISSING |

## Additional Figures (Added to figures.tex)

These figures were added as new supplementary figures at the end of figures.tex:

| Label | File(s) | Description |
|-------|---------|-------------|
| `fig:suppl_assembly_exp` | `Fig_assembly_effect_experimental.svg` | Assembly effect comparison (experimental) |
| `fig:suppl_assembly_sim` | `Fig_assembly_effect_simulation.svg` | Assembly effect comparison (simulation) |
| `fig:suppl_assembly_scatter` | `Assembly_effect_scatter_combined.png` | Assembly effect scatter plot |
| `fig:suppl_subcommunities_LN` | `PieCharts/Subcommunities/subcommunities_Nutr-_s*.png` | Parental communities in Nutr- |
| `fig:suppl_subcommunities_MN` | `PieCharts/Subcommunities/subcommunities_Base_s*.png` | Parental communities in Base |
| `fig:suppl_subcommunities_HN` | `PieCharts/Subcommunities/subcommunities_Nutr+_s*.png` | Parental communities in Nutr+ |
| `fig:suppl_coalescence_LN` | `PieCharts/CoalescenceMatrices/coalescence_matrix_Nutr-_s*.png` | Coalescence matrices in Nutr- |
| `fig:suppl_coalescence_MN` | `PieCharts/CoalescenceMatrices/coalescence_matrix_Base_s*.png` | Coalescence matrices in Base |
| `fig:suppl_coalescence_HN` | `PieCharts/CoalescenceMatrices/coalescence_matrix_Nutr+_s*.png` | Coalescence matrices in Nutr+ |
| `fig:suppl_rank_abundance_Base` | `rank_abundance_parental_vs_coalesced_Base.pdf` | Rank-abundance: parental vs coalesced (Base) |
| `fig:suppl_rank_abundance_LN` | `rank_abundance_parental_vs_coalesced_Nutr-.pdf` | Rank-abundance: parental vs coalesced (Nutr-) |
| `fig:suppl_rank_abundance_HN` | `rank_abundance_parental_vs_coalesced_Nutr+.pdf` | Rank-abundance: parental vs coalesced (Nutr+) |
| `fig:suppl_skewness_null` | `skewness_null_comparison.pdf` | Skewness null model test for one-sided selection |
| `fig:suppl_s29` | `correlation_vs_interaction_strength.pdf` | Pairwise selection correlation vs interaction strength |
| `fig:suppl_s30` | `monoculture_od_growth_histograms.pdf` | Monoculture OD and growth rate histograms |
| `fig:suppl_s31` | `overlap_fraction_histogram.pdf` | Overlap fraction of coalesced ASVs across media |

## Detailed Mappings

### S1: Taxonomy Table
- **Caption**: Table of phylogenetic taxonomy for 43 ASV isolates used in the experiment.
- **File**: `taxonomy_color_map.svg`
- **Notes**: Shows ASV color legend with full taxonomy (kingdom, phylum, class, order, family, genus)

### S2: Phylogeny Map
- **Caption**: Phylogeny map (EMBL).
- **File**: `Fig_1-3_phylogeny_tree.pdf` (or `.svg`)
- **Notes**: Phylogenetic tree of 50 bacterial ASVs, uses inferno colormap

### S4: Robustness Analysis
- **Caption**: Robustness of Fig.1 across various similarity metrics.
- **File**: `Fig_robustness_comparison_MN_merged.svg`
- **Notes**: Pie charts comparing classification across 5 distance metrics (Vector Decomposition, Euclidean, Bray-Curtis, Jensen-Shannon, Jaccard). MN medium, n=83.

### S5: Selection Preference Ratio (Base)
- **Caption**: Selection Preference Ratio of experiment and null model in Base media.
- **File**: `correlation_barplot_MN.svg`
- **Notes**: Pairwise selection correlation barplots, same-parent vs cross-parent species pairs

### S9-S11: Pairwise Invasion Assays
- **S9 (Nutr-)**: `Pairwise_Matrix_Dynamics_LN_improved.pdf`
- **S10 (Base)**: `Pairwise_Matrix_Dynamics_MN_improved.pdf`
- **S11 (Nutr+)**: `Pairwise_Matrix_Dynamics_HN_improved.pdf`
- **Notes**: 12x12 matrices showing 95:5 invasion assay outcomes. Background colors: green=Coexistence, red=Exclusion, purple=Bistability.

### SX: Selection Preference Ratio (Nutr-/Nutr+)
- **Caption**: Selection Preference Ratio of experiment and null model in Nutr-/Nutr+ media.
- **Files**: `correlation_barplot_LN.svg`, `correlation_barplot_HN.svg`
- **Notes**: May need to combine into a single figure or split into two

## Missing Figures (need to be generated)

1. **S3**: Time series in Base media
2. **S6**: Simulation: growth-rate heterogeneity
3. **S7**: Simulation: carrying-capacity variation
4. **S8**: Simulation: alternative α_ij sampling distributions
5. **S12**: Nutr- time series
6. **S13**: Nutr+ time series
7. **S14**: Linear coefficients of fitted regression model
8. **S15**: Species correlated with final pH
9. **S16**: Introducing more hierarchical effective interactions

## File Format Notes

- PDF files are preferred for LaTeX compilation (vector format, best quality)
- SVG files available as source/editable versions
- PNG files available as raster backups
- For figures with multiple formats, use PDF in LaTeX: `\includegraphics{supplementary_figs/filename.pdf}`
