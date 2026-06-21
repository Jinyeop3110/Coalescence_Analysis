# Supplementary Figures Source Documentation

## monoculture_od_growth_histograms.pdf
- **Source**: `Figure_generate/code/Figure/Monoculture_OD_Growth/monoculture_od_growth_histograms.pdf`
- **Code**: `Figure_generate/code/plot_monoculture_od_growth_histograms.py`
- **Description**: Two-panel histogram showing phenotypic diversity of bacterial isolates in monoculture. Left panel: Distribution of optical density (OD600) across 55 ASVs with OD > 0.1 (mean = 0.446, std = 0.119). Right panel: Distribution of growth rates (h^-1) across 60 ASVs (mean = 11.11 h^-1, std = 3.32 h^-1). Data from `ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/220910_54isolatesOD_flat100um.xlsx`.

## overlap_fraction_histogram.pdf
- **Source**: `Figure_generate/code/Figure/Overlap_Fraction/overlap_fraction_histogram.pdf`
- **Code**: `Figure_generate/code/plot_overlap_fraction_histogram.py`
- **Description**: Three-panel histogram showing the fraction of ASVs in coalesced communities that were present in BOTH parental communities before mixing, across three nutrient conditions. Nutr-: mean = 0.100 ± 0.098 (n=94); Base: mean = 0.217 ± 0.257 (n=94); Nutr+: mean = 0.172 ± 0.246 (n=94). Uses ASVs_overlap1_3 column from `Analyzed/processed_CoalescenceEvent_synthetic.xlsx`. Low overlap fractions indicate most surviving ASVs originated from only one parent, consistent with one-sided community-level selection.

## Fig_robustness_comparison_MN_merged.svg
- **Source**: `Figure_generate/code/Figure/PhaseDiagram_robustness_to_metrics/Fig_robustness_comparison_MN_merged.svg`
- **Code**: `Figure_generate/code/plot_phase_diagram_robustness_to_metrics.py`
- **Description**: Pie charts comparing coalescence outcome classification across 5 different distance metrics (Vector Decomposition, Euclidean, Bray-Curtis, Jensen-Shannon, Jaccard). Shows robustness of classification to metric choice. MN medium, all pool sizes merged (n=83).

## Fig_1-3_phylogeny_tree.pdf / Fig_1-3_phylogeny_tree.svg
- **Source**: `Figure_generate/code/Figure/Fig1_1_Plots/Fig_1-3_phylogeny_tree.pdf`
- **Code**: `Figure_generate/code/build_phylogeny.py`
- **Description**: Phylogenetic tree of the 50 bacterial ASVs used in coalescence experiments. Uses inferno colormap with seed=4 for consistency with pie charts.

## taxonomy_color_map.svg
- **Source**: `Figure_generate/code/Figure/Fig1_1_Plots/taxonomy_color_map.svg`
- **Code**: `Figure_generate/code/generate_fig1_1.py` (function: `plot_taxonomy_colormap()`)
- **Description**: ASV color legend showing the inferno colormap used across all figures. Lists all 50 ASVs with their full taxonomy (kingdom, phylum, class, order, family, genus). Uses same colormap as pie charts and timeseries for consistency.

## correlation_barplot_LN.svg / correlation_barplot_MN.svg / correlation_barplot_HN.svg
- **Source**: `Figure_generate/code/Figure/AsymmetricityNullModelAnalysis/correlation_analysis/`
- **Code**: `Figure_generate/code/plot_correlation_barplots_clean.py`
- **Description**: Pairwise selection correlation barplots comparing same-parent vs cross-parent species pairs. Shows correlated fates of species from same parental community. Y-range fixed at -0.2 to 0.6 for consistency.

## PieCharts/Subcommunities/
- **Source**: `Figure_generate/code/Figure/PieCharts/Subcommunities/`
- **Code**: `Figure_generate/code/generate_pie_plots.py`
- **Description**: Pie charts showing species composition of parental communities before coalescence. Files named `subcommunities_{medium}_s{pool}.png/svg` where medium is Nutr+/Base/Nutr- and pool is 6/12/24. Each figure shows Replicate 1 (left) and Replicate 2 (right) with sample IDs and community indices.

## PieCharts/CoalescenceMatrices/
- **Source**: `Figure_generate/code/Figure/PieCharts/CoalescenceMatrices/`
- **Code**: `Figure_generate/code/generate_pie_plots.py`
- **Description**: N×N matrices of pie charts showing coalescence outcomes for all pairwise combinations of parental communities. Files named `coalescence_matrix_{medium}_s{pool}.png/svg`. Upper triangle shows coalesced community composition for each parent pair. Organized by medium (Nutr+/Base/Nutr-) and species pool size (6/12/24).

## Assembly Effect Analysis Figures

### Fig_assembly_effect_experimental.svg
- **Source**: `Figure_generate/code/Figure/Assembly_effect/Fig_assembly_effect_parent_vs_coalesced.svg`
- **Code**: `Figure_generate/code/analyze_assembly_effect_outcomes.py`
- **Description**: Pie charts comparing coalescence vs direct assembly outcomes in experimental data across nutrient levels (Nutr-, Base, Nutr+). Top row shows coalescence outcomes, bottom row shows direct assembly outcomes. Categories: CLS (community-level selection), Mixing, Restructuring.

### Fig_assembly_effect_simulation.svg
- **Source**: `Figure_generate/code/Figure/Assembly_effect_simulation/Fig_assembly_effect_parent_vs_coalesced.svg`
- **Code**: `Figure_generate/code/plot_assembly_effect_simulation.py`
- **Description**: Pie charts comparing coalescence vs direct assembly outcomes in Lotka-Volterra simulations across different mean interaction strengths (μ=0.2, 0.4, 0.6, 0.8, 1.0). Top row shows coalescence outcomes, bottom row shows direct assembly outcomes. Categories: CLS, Mixing, Restructuring.

### Assembly_effect_scatter_combined.svg / Assembly_effect_scatter_combined.png
- **Source**: `Figure_generate/code/Figure/Assembly_effect_simulation/Assembly_effect_scatter_combined.svg`
- **Code**: `Figure_generate/code/plot_assembly_effect_mean_interaction.py`
- **Description**: Scatter plot showing mean pairwise interaction strength before vs after assembly. Red line/points: pre-assembly (inter-community) interactions. Blue line/points: post-assembly (intra-community) interactions. Demonstrates assembly effect: species that survive assembly tend to have weaker mutual interactions.

## Pairwise Species Invasion Assays

### Pairwise_Matrix_Dynamics_LN_improved.svg / .png / .pdf
- **Source**: `Figure_generate/code/Figure/PairwiseMatrixDynamics/Pairwise_Matrix_Dynamics_LN_improved.svg`
- **Code**: `Figure_generate/code/plot_pairwise_matrix_dynamics_improved.py`
- **Description**: 12×12 matrix showing pairwise species 95:5 invasion assay outcomes for Nutr- medium. Each cell [i,j] shows species i's frequency trajectory when competing with species j, starting from two initial conditions (5% blue line, 95% orange line). Background colors indicate outcome: green=Coexistence, red=Exclusion, purple=Bistability. Includes pie chart summary of outcome distribution.

### Pairwise_Matrix_Dynamics_MN_improved.svg / .png / .pdf
- **Source**: `Figure_generate/code/Figure/PairwiseMatrixDynamics/Pairwise_Matrix_Dynamics_MN_improved.svg`
- **Code**: `Figure_generate/code/plot_pairwise_matrix_dynamics_improved.py`
- **Description**: 12×12 matrix showing pairwise species 95:5 invasion assay outcomes for Base medium. Same format as LN. Shows increased exclusion compared to Nutr- medium.

### Pairwise_Matrix_Dynamics_HN_improved.svg / .png / .pdf
- **Source**: `Figure_generate/code/Figure/PairwiseMatrixDynamics/Pairwise_Matrix_Dynamics_HN_improved.svg`
- **Code**: `Figure_generate/code/plot_pairwise_matrix_dynamics_improved.py`
- **Description**: 12×12 matrix showing pairwise species 95:5 invasion assay outcomes for Nutr+ medium. Same format as LN. Shows highest exclusion and bistability rates among the three nutrient conditions.

## Natural Sample-Derived Communities

### Fig_natural_communities_coalescence.pdf
- **Source**: User-provided figure (Asset 52.pdf)
- **Code**: `Figure_generate/code/vector_decomp_natural.py` (analysis), `Figure_generate/code/plot_phase_diagram_natural.py` (phase diagrams)
- **Description**: Coalescence experiments using natural sample-derived communities.
  - **Panel A**: Experimental workflow - 6 natural environmental samples → community assembly (7 rounds serial growth-dilution) → coalescence (50:50 mixing) → post-coalescence stabilization (7 rounds) → 16S rRNA sequencing, OD, pH measurement. N_Isolates=6, N_Communities=6, N_Coalesced=16.
  - **Panel B**: Phase diagrams showing Similarity(C,A) vs Similarity(C,B) for natural communities across Nutr-, Base, Nutr+ media, with SPR histograms below.
  - **Panel C**: Stacked bar chart showing coalescence outcome fractions (CLS, M, R) across media conditions. Demonstrates that CLS patterns observed in synthetic communities generalize to naturally-derived communities.

## Skewness Null Model Analysis

### rank_abundance_parental_vs_coalesced_Base.pdf
- **Source**: `Figure_generate/code/Figure/SkewedDistributionTest/rank_abundance_parental_vs_coalesced_M.{png,svg,pdf}`
- **Code**: `Figure_generate/code/SkewedDistributionTest/plot_rank_abundance_parental_vs_coalesced.py`
- **Description**: Rank-abundance curves comparing parental vs coalesced communities in Base medium. (A) Parental communities (n=59, Gini=0.62±0.19). (B) Coalesced communities (n=94, Gini=0.64±0.15). Uses COLORMAP medium color (#802000).

### rank_abundance_parental_vs_coalesced_Nutr-.pdf
- **Source**: `Figure_generate/code/Figure/SkewedDistributionTest/rank_abundance_parental_vs_coalesced_L.{png,svg,pdf}`
- **Code**: `Figure_generate/code/SkewedDistributionTest/plot_rank_abundance_parental_vs_coalesced.py`
- **Description**: Rank-abundance curves comparing parental vs coalesced communities in Nutr- medium. (A) Parental communities (n=60, Gini=0.63±0.09). (B) Coalesced communities (n=92, Gini=0.61±0.12). Uses COLORMAP medium color (#A7216A).

### rank_abundance_parental_vs_coalesced_Nutr+.pdf
- **Source**: `Figure_generate/code/Figure/SkewedDistributionTest/rank_abundance_parental_vs_coalesced_H.{png,svg,pdf}`
- **Code**: `Figure_generate/code/SkewedDistributionTest/plot_rank_abundance_parental_vs_coalesced.py`
- **Description**: Rank-abundance curves comparing parental vs coalesced communities in Nutr+ medium. (A) Parental communities (n=60, Gini=0.64±0.17). (B) Coalesced communities (n=94, Gini=0.66±0.14). Uses COLORMAP medium color (#E24912).

### skewness_null_comparison.png / skewness_null_comparison.svg / skewness_null_comparison.pdf
- **Source**: `Figure_generate/code/Figure/SkewedDistributionTest/skewness_null_comparison_synthetic.{png,svg,pdf}`
- **Code**: `Figure_generate/code/SkewedDistributionTest/plot_single_comparison.py`
- **Description**: Scatter plot with mean ± SEM comparing experimental one-sided selection against two null models testing whether skewed parental abundance distributions explain the observed asymmetric outcomes. Shows 100 randomly sampled points with jitter as background, and mean as squares with error bars. Null models: (1) Abundance-weighted random selection - species survival probability proportional to abundance in combined pool; (2) Shuffled abundance - abundances randomly permuted within each parent before neutral mixing. Both null models show significantly lower one-sided selection than experimental data (p < 0.001), indicating skewness alone does not explain the pattern.
