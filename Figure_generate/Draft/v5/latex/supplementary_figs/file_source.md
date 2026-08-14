# Supplementary Figures Source Documentation

## interaction_matrix_post_assembly.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/interaction_matrix_assembly.pdf` (renamed on synchronization)
- **Code**: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/plot_interaction_matrix.py`
- **Description**: Supplementary Fig. 3. Panels a,b show one representative pre- and post-assembly interaction matrix. Panel c compares one independent within-community and between-community block mean per full-matrix simulation (`n = 10` paired simulations); the four diagonal parental blocks are counted once and all directed between-community blocks are included. Paired Wilcoxon signed-rank result: within mean 0.389, between mean 0.501, `W = 0`, `p = 0.001953125`.

## marginal_distributions_base_only.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/marginal_distributions_base_only.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Base-medium continuous distributions of PDI, parental asymmetry `|2PDI - 1|`, and squared parental retention. The PDI histogram is reflection-symmetrized (83 independent events, 166 plotted PDI values); panels b,c contain one value per event. Used as Supplementary Fig. 10.

## marginal_distributions_by_medium.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/marginal_distributions_by_medium.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Per-medium continuous distributions of PDI, asymmetry magnitude, and squared retention magnitude, with rows for Nutr-, Base, and Nutr+ and columns for the three metrics. Used as Response Fig. R2-3; the Supplementary Information uses separate one-medium panels.

## marginal_distributions_nutr_minus_only.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/marginal_distributions_nutr_minus_only.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Nutr-minus continuous distributions of PDI, parental asymmetry `|2PDI - 1|`, and squared parental retention. The PDI histogram is reflection-symmetrized (90 independent events, 180 plotted PDI values); panels b,c contain one value per event. Used as Supplementary Fig. 11.

## marginal_distributions_nutr_plus_only.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/marginal_distributions_nutr_plus_only.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Nutr-plus continuous distributions of PDI, parental asymmetry `|2PDI - 1|`, and squared parental retention. The PDI histogram is reflection-symmetrized (90 independent events, 180 plotted PDI values); panels b,c contain one value per event. Used as Supplementary Fig. 12.

## monoculture_od_growth_histograms.pdf
- **Source**: `Figure_generate/code/Figure/Monoculture_OD_Growth/monoculture_od_growth_histograms.pdf`
- **Code**: `Figure_generate/code/plot_monoculture_od_growth_histograms.py`
- **Description**: Two-panel histogram showing phenotypic diversity of the 54 bacterial isolates in Base medium. Endpoint OD600 and exponential growth rates are both derived from the 600-nm kinetic plate-reader series `ExperimentalResult/Data/2208_Coalescence_processed/Isolates/MN_ISO_GR.xlsx`, restricted to the documented isolate layout A1--F9. Growth-rate estimates are available for all 54 isolates (53 positive and one approximately zero). Used as Supplementary Fig. 33.

## overlap_fraction_histogram.pdf
- **Source**: `Figure_generate/code/Figure/Overlap_Fraction/overlap_fraction_histogram.pdf`
- **Code**: `Figure_generate/code/plot_overlap_fraction_histogram.py`
- **Description**: Three-panel histogram showing the fraction of ASVs above 1% in each coalesced community that were also above 1% in both parents. Nutr-: mean = 0.10 ± 0.10 (n=90); Base: mean = 0.24 ± 0.26 (n=83); Nutr+: mean = 0.18 ± 0.25 (n=90). Uses the threshold-level-3 column `ASVs_overlap1_3` from `Analyzed/processed_CoalescenceEvent_synthetic.xlsx`. The complementary fraction includes ASVs above 1% in exactly one parent or neither parent. Used as Supplementary Fig. 34.

## Fig_robustness_comparison_MN_merged.svg
- **Source**: `Figure_generate/code/Figure/PhaseDiagram_robustness_to_metrics/Fig_robustness_comparison_MN_merged.svg`
- **Code**: `Figure_generate/code/plot_phase_diagram_robustness_to_metrics.py`
- **Description**: Pie charts comparing coalescence outcome classification across 5 different distance metrics (Vector Decomposition, Euclidean, Bray-Curtis, Jensen-Shannon, Jaccard). Shows robustness of classification to metric choice. MN medium, all pool sizes merged (n=83).

## Fig_1-3_phylogeny_tree.pdf / Fig_1-3_phylogeny_tree.svg
- **Source**: `Figure_generate/code/Figure/Fig1_1_Plots/Fig_1-3_phylogeny_tree.pdf`
- **Code**: `Figure_generate/code/build_phylogeny.py`
- **Description**: Neighbor-joining tree of the 50 unique ASVs identified among the 54 bacterial isolates, based on the 252--253-bp 16S rRNA amplicon sequences in `Species_phylogeny.xlsx`. Uses the inferno colormap with seed=4 for consistency with pie charts. The plotting layout reserves a dedicated clearance between terminal labels and the abundance column so the longest-branch label, ASV1 (Lactococcus), does not overlap its rectangle.

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
- **Description**: N×N matrices of pie charts showing coalescence outcomes for all pairwise combinations of parental communities. Files named `coalescence_matrix_{medium}_s{pool}.png/svg`. Upper triangle shows coalesced community composition for each parental-community pair. Organized by medium (Nutr+/Base/Nutr-) and species pool size (6/12/24). Within each replicate, publication-facing labels use the concise indices C1, C2, and so forth; internal acquisition IDs such as `P8-53` are deliberately omitted.

## Assembly Effect Analysis Figures

### Fig_S26_assembly_effect_experimental_stacked_bar.pdf
- **Source**: `Figure_generate/code/Figure/StackedBar_ClassFractions/Fig_S26_assembly_effect_experimental_stacked_bar.pdf`
- **Code**: `Figure_generate/code/identify_assembly_pairs_CORRECT.py`; `Figure_generate/code/plot_stacked_bar_class_fractions.py`
- **Description**: Synthetic-community-only comparison of coalescence with direct assembly of the corresponding initial species pool. Records are restricted to valid samples and matched biological-replicate identifiers. Dominance/Mixture/Restructuring counts for coalescence are 17/21/2 (Nutr-, n=40), 23/2/11 (Base, n=36), and 30/1/10 (Nutr+, n=41); direct-assembly counts are 23/14/3, 13/2/21, and 31/1/9, respectively. Used as Supplementary Fig. 23.

### timeseries_merged/Fig_1-3_timeseries_Nutr-_* / Fig_1-3_timeseries_Nutr+_ex1_merged.pdf
- **Source**: `Figure_generate/code/Figure/Fig1_1_Plots/timeseries_merged/`
- **Code**: `Figure_generate/code/generate_fig1_1.py`
- **Description**: Measured relative-ASV-abundance time series for the Supplementary Figs. 30 and 31 examples. Only recorded samples are plotted, with cycle labels beginning at 1; no randomly generated parental composition or calculated 50:50 initial mixture is included. The community-event mappings remain those in the generating script pending independent design-record confirmation.

### Fig_assembly_effect_experimental.svg
- **Source**: `Figure_generate/code/Figure/Assembly_effect/Fig_assembly_effect_parent_vs_coalesced.svg`
- **Code**: `Figure_generate/code/analyze_assembly_effect_outcomes.py`
- **Description**: Pie charts comparing coalescence vs direct assembly outcomes in experimental data across nutrient levels (Nutr-, Base, Nutr+). Top row shows coalescence outcomes, bottom row shows direct assembly outcomes. Categories: Dominance, Mixture, Restructuring.

### Fig_assembly_effect_simulation.svg
- **Source**: `Figure_generate/code/Figure/Assembly_effect_simulation/Fig_assembly_effect_parent_vs_coalesced.svg`
- **Code**: `Figure_generate/code/plot_assembly_effect_simulation.py`
- **Description**: Pie charts comparing coalescence vs direct assembly outcomes in Lotka-Volterra simulations across different mean interaction strengths (μ=0.2, 0.4, 0.6, 0.8, 1.0). Top row shows coalescence outcomes, bottom row shows direct assembly outcomes. Categories: Dominance, Mixture, Restructuring.

### Assembly_effect_scatter_combined.svg / Assembly_effect_scatter_combined.png
- **Source**: `Figure_generate/code/Figure/Assembly_effect_simulation/Assembly_effect_scatter_combined.svg`
- **Code**: `Figure_generate/code/plot_assembly_effect_mean_interaction.py`
- **Description**: Scatter plot showing mean pairwise interaction strength across assembly stages. Red line/points are cross-parent interactions among species that survived separate assembly in the two parental communities; blue line/points are within-community interactions among species surviving after coalescence. The x coordinate is the full initially sampled matrix mean. Demonstrates that species surviving coalescence tend to have weaker mutual interactions.

## Pairwise Species Invasion Assays

### Pairwise_Matrix_Dynamics_LN_improved.svg / .png / .pdf
- **Source**: `Figure_generate/code/Figure/PairwiseMatrixDynamics/Pairwise_Matrix_Dynamics_LN_improved.svg`
- **Code**: `Figure_generate/code/plot_pairwise_matrix_dynamics_improved.py`
- **Description**: 12×12 matrix showing pairwise isolate 95:5 invasion assay outcomes for Nutr- medium. I1--I12 are fixed workbook assay-isolate indices, not ASV identifiers. Each cell shows reciprocal 5%/95% endpoints. Classification follows the Methods thresholds: Coexistence (both 10--90%), Exclusion (the same focal isolate above 99% or below 1% from both starts), Bistability (below 1% from the low start and above 99% from the high start), and Unassigned otherwise; gray denotes no paired data. Counts among 61 unordered pairs: 44/2/0/15.

### Pairwise_Matrix_Dynamics_MN_improved.svg / .png / .pdf
- **Source**: `Figure_generate/code/Figure/PairwiseMatrixDynamics/Pairwise_Matrix_Dynamics_MN_improved.svg`
- **Code**: `Figure_generate/code/plot_pairwise_matrix_dynamics_improved.py`
- **Description**: Base-medium counterpart using the same Methods-based classification and I1--I12 workbook indices. Counts among 61 unordered pairs: 12 Coexistence, 28 Exclusion, 3 Bistability, and 18 Unassigned.

### Pairwise_Matrix_Dynamics_HN_improved.svg / .png / .pdf
- **Source**: `Figure_generate/code/Figure/PairwiseMatrixDynamics/Pairwise_Matrix_Dynamics_HN_improved.svg`
- **Code**: `Figure_generate/code/plot_pairwise_matrix_dynamics_improved.py`
- **Description**: Nutr+-medium counterpart using the same Methods-based classification and I1--I12 workbook indices. Counts among 61 unordered pairs: 3 Coexistence, 33 Exclusion, 8 Bistability, and 17 Unassigned.

## Natural Sample-Derived Communities

### Fig_natural_communities_coalescence.pdf
- **Source**: User-provided figure (Asset 52.pdf)
- **Code**: `Figure_generate/code/vector_decomp_natural.py` (analysis), `Figure_generate/code/plot_phase_diagram_natural.py` (phase diagrams)
- **Description**: Coalescence experiments using natural sample-derived communities.
  - **Panel A**: Experimental workflow - 6 natural environmental samples → community assembly (7 rounds serial growth-dilution) → coalescence (50:50 mixing) → post-coalescence stabilization (7 rounds) → 16S rRNA sequencing, OD, pH measurement. N_Isolates=6, N_Communities=6, N_Coalesced=16.
  - **Panel B**: Phase diagrams showing Similarity(C,A) vs Similarity(C,B) for natural communities across Nutr-, Base, Nutr+ media, with SPR histograms below.
  - **Panel C**: Stacked bar chart showing coalescence outcome fractions (Dominance, Mixture, Restructuring) across media conditions. Shows that the nutrient-dependent outcome pattern observed in synthetic communities also appears in laboratory-stabilized natural sample-derived communities.

### rank_abundance_natural_Nutr-.pdf / rank_abundance_natural_Base.pdf / rank_abundance_natural_Nutr+.pdf
- **Source**: `Figure_generate/code/Figure/RankAbundance_Natural/rank_abundance_natural_{Nutr-,Base,Nutr+}.{pdf,svg}`
- **Code**: `Figure_generate/code/plot_rank_abundance_natural.py`
- **Description**: Rank-abundance curves for natural sample-derived parental communities (`n=12` per medium) and coalesced communities (`n=30` per medium). Panel summaries report mean $\pm$ sample s.d. for Gini coefficient and ASV richness above 0.1% relative abundance. Supplementary Figs. 19--21 use Nutr-, Base and Nutr+, respectively.

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

### Fig_R1_1B_OD_vs_PDI.pdf
- **Source**: `Figure_generate/Draft/v5/public_code_repo/pipeline/04_figure_generation/supplementary/panels/supp_fig14_od_vs_ph.{pdf,svg,png}`
- **Code**: `Figure_generate/Draft/v5/public_code_repo/pipeline/04_figure_generation/supplementary/generate_figure.py`
- **Description**: Two-row Supplementary Fig. 14. Panels a--c show signed parental-community OD difference versus PDI for independent coalescence events; parent-label-swapped reflections are displayed only for symmetry and excluded from inference. Panels d--f show endpoint OD$_{600}$ versus endpoint pH across parental-community replicates in Nutr-, Base and Nutr+.

### Fig_R1_1C_pairwise_corr_vs_OD.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_R1_1C_pairwise_corr_vs_OD.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_OD_density.py`
- **Description**: Within-community pairwise selection correlation versus parental-community OD, shown as a compact 2x3 layout with nutrient conditions as columns. Top-row confidence intervals use a cluster bootstrap that resamples complete coalescence events. The bottom row contains one paired A-minus-B OD and correlation contrast per event, avoiding inference on two reused-parent rows from the same event. Added as Supplementary Fig. 15 for the Reviewer 1 parental OD/biomass imbalance control.

### Fig_R1_3_per_medium_scatter.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/Fig_R1_3_per_medium_scatter.{pdf,svg,png}`
- **Code**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
- **Description**: Supplementary Fig. 16 dominant-species-removal control for the Fig. 5C PDI analysis. Rows show Base and Nutr+; columns show the original calculation, removal of the coalesced-community dominant species, and removal of each parental-community dominant species. Spearman tests use only independent, non-reflected events.

### Fig_R3_2_additive_null_comparison.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/Fig_R3_2_additive_null_comparison.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Coalescence-pair-specific simple additive null model comparison for Base medium coalescence outcomes. Panel A shows the manuscript-style similarity map with coalescence-pair-specific simple additive null model outcomes, observed coalesced communities, and example null-to-observed arrows. Panel B shows paired PDI/asymmetry shifts from each coalescence-pair-specific simple additive null model outcome to its corresponding observed outcome. Panel C shows class transitions from coalescence-pair-specific simple additive null model outcomes to observed coalesced communities. Promoted from Supplementary Fig. 38 to Extended Data Fig. 3 for the Reviewer 3 dimensionality and simple additive null-model response.

### Fig_R3_3_sim_parent_norm_asymmetry.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/Fig_R3_3_sim_parent_norm_asymmetry.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/analyze_sim_parent_norm_asymmetry.py`
- **Description**: Simulation parent-vector norm imbalance and simple additive null model classifications across interaction strength. Panel A shows Euclidean norms of assembled sub-community abundance vectors across $\mu$. Panel B shows fold differences in Euclidean norm between paired parental sub-communities in each simulated coalescence event. Panel C shows how often the simple additive null model is classified as Dominance, Mixture, or Restructuring across $\mu$. Added as Supplementary Fig. 38 for the Reviewer 3 richness/norm-imbalance response.

### R3_4_mixed_sign_higher_order.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_mixed_sign_higher_order.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mixed_sign_higher_order.py`; `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mixed_sign_higher_order_figure.py`
- **Description**: Mixed-sign facilitative-tail gLV robustness analysis. Off-diagonal coefficients are drawn iid from `U[-f mu, (2+f) mu]`, preserving the mean coefficient while allowing negative coefficients under the gLV sign convention. Labeled top insets show the analytic coefficient density. Density-dependent self-limitation prevents runaway growth. Added as Supplementary Fig. 39 for the Reviewer 3 facilitation-scope response.

### R3_4_simulation.pdf / R3_4_pair_coupling_fine.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_simulation.pdf`; `Figure_generate/code/Figure_revision/R3_4_pair_coupling_fine.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_p_axis.py`; `Figure_generate/code/Figure_revision/R3_3_pair_additivity/make_R3_3_figure.py`; `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_p_axis_fine_figure.py`
- **Description**: Reciprocal pair-coupling robustness analysis. Reciprocal coefficient structure is varied from antisymmetric exploitation (`p < 0`, one coefficient in a converted pair is negative) through the iid competitive baseline (`p = 0`) to symmetric competition (`p > 0`, both converted coefficients are positive and equal). Labeled top insets/strips show the analytic directed-coefficient distributions. Added together as Supplementary Fig. 40 for the Reviewer 3 interaction-structure response.

### R3_4_mutualistic_pair_fraction.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_mutualistic_pair_fraction.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mutualistic_pair_fraction.py`; `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mutualistic_pair_fraction_figure.py`
- **Data**: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/mutualistic_pair_fraction_results.json`
- **Description**: Weak bidirectional mutualistic-pair fraction sweep. For `q = 0, 0.10, 0.20, 0.30, 0.40` of unordered species pairs, both reciprocal coefficients are drawn from `U[-0.2 mu, 0]`, corresponding to weak positive ecological interactions under the manuscript sign convention. Remaining interactions are sampled from the baseline competitive distribution `U[0, 2mu]`. Labeled top insets show the resulting coefficient mixture. Dynamics include density-dependent self-limitation with `gamma = 0.10`. Added as Supplementary Fig. 41 for the Reviewer 3 mutualism subquestion.

### R3_4_mean_variance_grid.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_mean_variance_grid.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mean_variance_grid.py`; `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mean_variance_grid_figure.py`
- **Data**: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/mean_variance_grid_results.json`
- **Description**: Mean and variance of the interaction-coefficient distribution. Off-diagonal coefficients are drawn from `U[m - h, m + h]`, with `m = 0, 0.20, 0.40, 0.60, 0.80` and `h = 0, 0.20, 0.40, 0.60, 0.80`, giving `std(alpha) = h/sqrt(3)`. Negative coefficients are positive ecological interactions under the manuscript sign convention and occur when `h > m`. Dynamics include density-dependent self-limitation with `gamma = 0.10`. Added as Supplementary Fig. 42 for the Reviewer 3 interaction-strength/mutualism subquestion.

### natural_taxonomic_distinctness.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_5_natural_taxonomic_distinctness/Fig_R2_5_natural_taxonomic_distinctness.pdf` (copied to `latex/supplementary_figs/natural_taxonomic_distinctness.pdf`; byte-identical to the response-letter copy `latex/revision_first_round/revision_figure_folder/Fig_R2_5_natural_taxonomic_distinctness.pdf`; regenerate the source and re-copy both when updating)
- **Code**: `Figure_generate/code/Figure_revision/R2_5_natural_taxonomic_distinctness/analyze_natural_taxonomic_distinctness.py`
- **Data summary**: `Figure_generate/code/Figure_revision/R2_5_natural_taxonomic_distinctness/natural_taxonomic_distinctness_summary.txt`
- **Description**: Post-stabilization taxonomic-distinctness checks for natural sample-derived communities. Panels a,d, ASV/Genus richness of parental and coalesced communities by medium. Panels b,e, pairwise Jaccard similarity among same-source parental replicates (S; n=6 pairs/medium), different-source parental communities (D; n=60 pairs/medium), and coalesced communities (C; n=435 pairs/medium); these sample sizes are stated in the caption rather than repeated at sub-5-pt size on every box. Panels c,f, own parental-community versus unrelated parental-community Jaccard similarity for each coalesced community (n=30 events/medium); own-parent similarity exceeded unrelated-parent similarity in every medium (one-sided paired Wilcoxon signed-rank test, all p < 1e-6 at the ASV and Genus levels), with compliant-size per-medium p-values on the figure. Uses post-stabilization 16S profiles only; tests for complete post-stabilization taxonomic collapse and retained parental-community-specific signal, not pre-to-post enrichment or functional convergence. Added as Supplementary Fig. 22 for the Reviewer 2 natural-community pre-selection response (R2-5).

## Growth Rate Heterogeneity Ablation (S4)

### Fig_phase_diagram_ablation_growth_std01.pdf / Fig_phase_diagram_ablation_growth_std02.pdf
- **Source**: `Figure_generate/code/Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_growth_std01.pdf`
- **Code**: `Figure_generate/code/plot_phase_diagram_ablation_growth_rate.py`
- **Description**: Outcome-fraction sweeps with heterogeneous growth rates sampled from N(1, σ²), titled `σg = 0.1` and `σg = 0.2` in panels a,b. Shows that the qualitative transition from Mixture-dominated to Dominance/Restructuring outcomes is robust to growth-rate variation.

## Carrying Capacity Variation Ablation (S5)

### Fig_phase_diagram_ablation_k_std01.pdf / Fig_phase_diagram_ablation_k_std02.pdf
- **Source**: `Figure_generate/code/Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_k_std01.pdf`
- **Code**: `Figure_generate/code/plot_phase_diagram_ablation_carrying_capacity.py`
- **Description**: Outcome-fraction sweeps with heterogeneous carrying capacities sampled from N(1, σ²), titled `σK = 0.1` and `σK = 0.2` in panels a,b. Shows that the qualitative transition from Mixture-dominated to Dominance/Restructuring outcomes is robust to carrying-capacity variation.

## Interaction-distribution Ablation (S6)

### Fig_phase_diagram_ablation_gaussian.pdf / Fig_phase_diagram_ablation_gamma.pdf
- **Source**: `Figure_generate/code/Figure/PhaseDiagram_ablation/Fig_phase_diagram_ablation_{gaussian,gamma}.pdf`
- **Code**: `Figure_generate/code/convert_ablation_plots.py`; `Figure_generate/code/plot_phase_diagram_ablation.py`
- **Description**: Outcome-fraction sweeps across `μ = 0.05--1.20` for Gaussian and Gamma interaction-coefficient distributions, titled `Gaussian` and `Gamma` in panels a,b.

## Species Number Ablation (Extended Data Fig. 4)

### overview_ablation_species.pdf
- **Source**: `Figure_generate/code/Figure/PhaseDiagram_ablation_species_number/overview_ablation_species.pdf`
- **Code**: `Figure_generate/code/plot_phase_diagram_ablation_species_number.py`
- **Description**: Three-panel figure showing coalescence outcome fractions (Dominance, Mixture, Restructuring) across different numbers of species per parental community (4, 6, 9, 12, 24, 48) at three interaction strengths: (A) μ=0.3, (B) μ=0.6, and (C) μ=0.8. Demonstrates that Dominance frequency remains relatively stable across community sizes while Mixture decreases and Restructuring increases with larger communities. Generated from simulation data in `Simulation_Data/*percomm_ablation_species_number/` directories. The active SI presents this analysis as Extended Data Fig. 4.

## Species-pH Correlation (S17)

### two_panel_ph_asv_figure.pdf
- **Source**: `Figure_generate/code/Figure/pH_Analysis/two_panel_ph_asv_figure.{pdf,svg,png}`
- **Code**: `Figure_generate/code/create_two_panel_figure.py`
- **Description**: Supplementary Fig. 17 shows the distribution and individual values for the 54 intended monoculture wells A1--F9 after 15 h. The parser converts the workbook text entry `48?` to 4.8 and excludes off-layout controls A12 and C12. No ASV labels are assigned because the pH workbook contains no verified isolate-well-to-ASV mapping.

### Fig_S23_ASV_vs_pH_combined.pdf
- **Source**: `Figure_generate/code/Figure/pH_Analysis/Fig_S23_ASV_vs_pH_combined.{pdf,svg,png}`
- **Code**: `Figure_generate/code/plot_ph_figures_revised.py`
- **Description**: Supplementary Fig. 18 plots selected synthetic-community ASV abundances against stabilized parental-community pH in Base and Nutr+. Synthetic and independently processed natural-community ASV tables are not concatenated. Taxonomy is read from Sheet 2 of the processed synthetic-sequence workbook: ASV3 Lactococcus, ASV8 Pedobacter, ASV9 Chryseobacterium, ASV11 Exiguobacterium and ASV12 Leuconostoc. Pearson statistics are descriptive and unadjusted; no monoculture acidifier/alkalinizer identity is inferred without a verified mapping.
