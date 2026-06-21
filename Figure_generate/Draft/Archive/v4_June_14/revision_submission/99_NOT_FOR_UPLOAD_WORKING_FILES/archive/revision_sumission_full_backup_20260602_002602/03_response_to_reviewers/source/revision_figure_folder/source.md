# Revision Response Figures Source Documentation

This document records the provenance of the revision-response figures copied into `latex/revision/revision_figure_folder/`.

## Fig_R2_5_post_stabilization_taxonomic_distinctness.pdf
- **Source**: `Figure_generate/Draft/v4/latex/revision/new review responses_2026-05-14/reviewer2_agents/R2_Q5_natural_community_preselection/figures/post_stabilization_taxonomic_distinctness.pdf`
- **Code**: `Figure_generate/Draft/v4/latex/revision/new review responses_2026-05-14/reviewer2_agents/R2_Q5_natural_community_preselection/figure_code/plot_post_stabilization_taxonomic_distinctness.py`
- **Description**: Superseded response-only taxonomic distinctness check for Reviewer 2 point R2-5. Pairwise ASV Jaccard similarity and Bray-Curtis similarity are computed among natural sample-derived parental communities after seven serial growth-dilution cycles in defined laboratory media, using ASVs above the 0.1% relative-abundance threshold. Comparisons are grouped by same-source versus different-source environmental sample pairs. The analysis is restricted to post-stabilization samples and therefore does not measure pre-to-post stabilization convergence or functional convergence.

## Fig_R2_5_natural_taxonomic_distinctness.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_5_natural_taxonomic_distinctness/Fig_R2_5_natural_taxonomic_distinctness.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_5_natural_taxonomic_distinctness/analyze_natural_taxonomic_distinctness.py`
- **Data summary**: `Figure_generate/code/Figure_revision/R2_5_natural_taxonomic_distinctness/natural_taxonomic_distinctness_summary.txt`
- **Description**: Current Response Fig. R2-5 for Reviewer 2 point R2-5, also promoted to the Supplementary Information as Supplementary Fig. 44 (byte-identical copy at `latex/supplementary_figs/natural_taxonomic_distinctness.pdf` — re-run the script and re-copy both files together when updating). The analysis uses the raw natural ASV table `SEQanalysis/onlyNatural/M_OTUtableGreenGenes.csv` and matched taxonomy annotations `SEQanalysis/onlyNatural/M_TAXAtableGreenGenes.csv`. It quantifies ASV- and Genus-level richness of natural parental and coalesced communities, pairwise Jaccard similarity among same-source stabilized parental replicates (S; n=6 pairs/medium), different-source stabilized parental communities (D; n=60 pairs/medium), and final coalesced communities (C; n=435 pairs/medium) within each medium, and the similarity of each final coalesced community to its own two parents versus unrelated stabilized parental communities from the same medium (n=30 events/medium). Per-box n values are annotated on panels b,e and per-medium one-sided paired Wilcoxon signed-rank p-values are annotated on panels c,f (own-parent similarity exceeded unrelated-parent similarity in every medium, all p < 1e-6 at the ASV and Genus levels). The summary file reports these per-medium statistics plus Family- and Phylum-collapsed checks. Unresolved higher-rank taxonomy labels are kept ASV-specific rather than pooled into one artificial unresolved taxon. The analysis uses post-stabilization 16S profiles and ASVs above the 0.1% relative-abundance threshold, so it tests for complete post-stabilization taxonomic collapse and retained parent-specific taxonomic signal but cannot measure pre-to-post enrichment convergence or functional convergence.

## Reviewer3_attachment_figures.pdf
- **Source**: `Figure_generate/Draft/v4/latex/revision/raw/3_reviewer_attachment_1_1773936948_convrt.pdf`
- **Code**: reviewer-supplied attachment (no generating script in repository)
- **Description**: Cropped response-letter copy of the PDF attached by Reviewer 3 containing Reviewer Figures 1--3; this is a reviewer-supplied attachment and is not assigned a Response Fig. R3-2 number. The raw A4 attachment is preserved at the source path above. The figure shows how the occupancy of the `Sim(A,C)` versus `Sim(B,C)` similarity plane changes with richness under three null constructions: random restructuring with roughly uniform abundances, random restructuring with uneven abundances, and simple additive mixing `n_C = n_A + n_B`. Copied into the local rebuttal figure folder so the reviewer’s geometric examples can be referenced directly in the response package.

## Fig_R3_2_reviewer_reproduction_L1.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_reviewer_reproduction_L1.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/reproduce_reviewer_norm_figures.py`
- **Description**: Reviewer-style null-model reproduction under L1 normalization. Four row subtitles identify the null constructions: A, random restructuring with abundances ~ U(0, 1); B, random restructuring with abundances ~ 10^U(-3, 0); C, simple additive mixing with abundances ~ U(0, 1); and D, simple additive mixing with abundances ~ 10^U(-3, 0). Each row shows similarity maps for `N = 2, 4, 6, 8` plus the resulting Dominance/Mixture/Restructuring fractions under the manuscript classifier. Scatter panels overlay both the reviewer's visual retention boundary (`r = 1/2`) and the manuscript classifier boundary (`r = 1/sqrt(2)`). Used in the R3-2 response to show that the reviewer's geometric examples are not reproduced by the manuscript's metric when L1 normalization is used.

## Fig_R3_2_reviewer_reproduction_L2.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_reviewer_reproduction_L2.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/reproduce_reviewer_norm_figures.py`
- **Description**: Reviewer-style null-model reproduction under L2 normalization. Four row subtitles identify the null constructions: A, random restructuring with abundances ~ U(0, 1); B, random restructuring with abundances ~ 10^U(-3, 0); C, simple additive mixing with abundances ~ U(0, 1); and D, simple additive mixing with abundances ~ 10^U(-3, 0). Each row shows similarity maps for `N = 2, 4, 6, 8` plus the resulting Dominance/Mixture/Restructuring fractions under the manuscript classifier. Scatter panels overlay both the reviewer's visual retention boundary (`r = 1/2`) and the manuscript classifier boundary (`r = 1/sqrt(2)`). Used in the R3-2 response to show that the reviewer's qualitative geometric effect is recovered under L2/cosine normalization, while the manuscript boundary classifies random restructuring primarily as Restructuring at moderate-to-large `N`, uniform additive mixing primarily as Mixture, and skewed additive mixing as high-retention but asymmetric at low `N`.

## Fig_R3_2_parent_norm_asymmetry.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/Fig_R3_2_parent_norm_asymmetry.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_reviewer_norm_comparison/analyze_parent_norm_asymmetry.py`
- **Description**: Experimental check of the raw-count norm-imbalance caveat. The experimental panels start from the raw ASV count table `SEQanalysis/excludeNatural/M_OTUtableGreenGenes.csv` before sample-wise normalization. Panel A shows density distributions of raw ASV count-vector L2 norms per parental community in each nutrient condition. Panel B shows the fold difference in raw count-vector L2 norm between the two parental communities in each experimental coalescence pair, alongside skewed-abundance simple-additive toy models at `N = 2` and `N = 4`. Panel C shows per-medium classification fractions for the simple additive null model computed from the paired parental raw abundance vectors, with Mixture counts labeled.

## Fig_R1_1A_winner_loser_OD.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_R1_1A_winner_loser_OD.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_OD_density.py`
- **Description**: 1x3 scatter of Winner OD vs Loser OD for Dominance events, one subplot per medium (Nutr-, Base, Nutr+), with y=x reference and per-panel counts for "Higher-OD parental community wins" plus a binomial-test p value. Axes extend slightly below OD = 0 and points are semi-transparent so low-OD and overlapping Dominance events remain visible.

## Fig_R1_1B_OD_vs_PDI.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_R1_1B_OD_vs_PDI.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_OD_density.py`
- **Description**: Per-event scatter of signed OD difference (OD_A - OD_B) versus manuscript-defined PDI = (2/pi) arctan(u/v), separately for each medium, with Spearman rho and p value annotated at the bottom of each panel. Reflected gray points included for symmetry.

## Fig_R1_1C_pairwise_corr_vs_OD.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_R1_1C_pairwise_corr_vs_OD.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_OD_density.py`
- **Description**: Within-community pairwise selection correlation vs parental-community OD in a compact 2x3 grid (columns = Nutr-, Base, Nutr+). Top row: parental communities are grouped by low/mid/high within-medium OD tertile; bars show within-community pairwise selection correlation with bootstrap 95% CIs, and a fixed dashed gray reference line shows the medium-level mean cross-community correlation with a bootstrap CI band. Bottom row: per-event parental-community observations plotted by OD and within-community pairwise selection correlation, with low/mid/high OD boundary lines and region labels, Spearman rho, and p value.

## Fig_R1_2_acidalk_per_medium.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_2_pH_dominance/Fig_R1_2_acidalk_per_medium.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_2_pH_dominance/analyze_pH_dominance.py`
- **Description**: Four-panel figure for R1-2, per medium (Base and Nutr+, since LN has no acidic parental communities). Panels 1-2: stacked outcome-class fractions (Dominance / Mixture / Restructuring) for the three pH-pair types ordered as Acid-Alk, Acid-Acid, Alk-Alk, with a 2-way Fisher test annotation comparing Acid-Alk vs pooled same-pH. Panel 3: signed asymmetry for all pH-pair types (positive = lower-pH parental community won). Panel 4: signed asymmetry for Acid-Alk pairs only (positive = acidic parental community won). Previous `Fig_R1_2a/b/c` figures were superseded and moved to `deprecated/R1_2_obsolete/`.

## Fig_R1_3ab_PDI_comparison.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/Fig_R1_3ab_PDI_comparison.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
- **Description**: Side-by-side comparison of the original Fig. 5C-style relationship and the dominant-species-removed reanalysis. The event filter is anchored to the original Fig. 5C-style calculation: events must be non-Restructuring before dominant-species removal and must have a valid pairwise-assay lookup. Dominant-removal panels change only the community-level PDI calculation, except for events that become mathematically empty after removal.

## Fig_R1_3_per_medium_scatter.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/Fig_R1_3_per_medium_scatter.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
- **Description**: Current Response Fig. R1-3. A 2x3 per-medium scatter grid comparing Original, dominant-from-mix removed, and dominant-from-each-parent removed PDI calculations for Base and Nutr+. Base and Nutr+ are not pooled. The plotted event set is anchored to the Original calculation in each medium; removal columns recompute community-level PDI on that original-selected set and only lose events that become empty after species removal. Panel annotations include reflected-data R2/slope values used for Fig. 5C-style plotting and independent-event Spearman rho/p values used for the correlation test.

## Fig_R1_3_per_medium_R2.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/Fig_R1_3_per_medium_R2.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
- **Description**: Companion R1-3 bar chart summarizing per-medium R^2 for the Original, dominant-from-mix removed, and dominant-from-each-parent removed PDI calculations under the same Original-anchored filtering convention used for `Fig_R1_3_per_medium_scatter.pdf`.

## Fig_R1_3c_VD_reclassification.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/Fig_R1_3c_VD_reclassification.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
- **Description**: Outcome reclassification after removing the dominant species from the compositions.

## Fig_R1_3d_R2_comparison.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/Fig_R1_3d_R2_comparison.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
- **Description**: Summary comparison of predictive power before and after dominant-species removal.

## pool_size_analysis.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_4_pool_size/pool_size_analysis.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`
- **Description**: 2x3 composite for the R1-4 response. A realized parental richness (experiment, box+jitter, ASVs) shown by medium and grouped/colored by initial species pool size. B ASV-based assembly survival ratio, computed as realized parental ASV richness divided by inoculated species-pool size. C experimental Dominance fraction shown by medium, with bars grouped and colored by initial species pool size (chi-square p=0.69 pooled across media). D experimental pairwise species selection grouped by initial species pool size, using the same concordance-based metric as Fig. 2D. E model Dominance fraction grouped by mu x pool size. F model pairwise species selection at mu in {0.30, 0.60, 0.80}, pool sizes 4/6/9/12/24/48 (100 reps each; interaction matrices reconstructed from saved seeds). Core message: Dominance frequency is set primarily by mu / nutrient condition, not by pool size, while the same-parental-community versus cross-parental-community pairwise-selection gap can increase with pool size. Terminology: "pairwise species selection" matches the manuscript (Fig. 2D); earlier revisions used the phrase "co-persistence" for the same quantity.

## pool_size_by_medium.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_4_pool_size/pool_size_by_medium.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`
- **Description**: Supplementary breakdown of experimental parental richness by pool size, faceted by medium, with per-medium Kruskal-Wallis p-values.

## pool_size_analysis_AB.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_4_pool_size/pool_size_analysis_AB.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`
- **Response letter reference**: Previously used in R3-3; superseded by `Fig_R3_3_richness_summary.pdf`.
- **Description**: Two-panel export reusing the experimental A/B panels from the R1-4 pool-size analysis. Panel A shows realized parental richness by medium and initial pool size. Panel B shows the ASV-based assembly survival ratio by medium and initial pool size. Generated as a standalone response figure so related richness-control responses can show the experimental richness diagnostics without reproducing the full six-panel R1-4 figure.

## interaction_matrix_assembly.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/interaction_matrix_assembly.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/plot_interaction_matrix.py`
- **Description**: Multi-example interaction-matrix visualization for R1-7 / Supplementary Fig. 27. Three rows show before-versus-after assembly matrices for example replicates at `\mu = 0.50`, with seeded-species and survivor-count annotations for parental communities A and B. The summary panel compares within-community and between-community interaction coefficients across all 10 full-matrix simulation replicates.

## interaction_matrix_mu_comparison.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/interaction_matrix_mu_comparison.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/plot_interaction_matrix.py`
- **Description**: Comparison of within-community and between-community interaction strengths across `\mu`.

## marginal_distributions_base_only.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/marginal_distributions_base_only.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Three-panel Base-medium continuous-distribution figure. Panels show manuscript PDI, computed as `(2/pi) arctan(u/v)` and reflection-symmetrized for visualization; asymmetry magnitude `y`; and squared retention magnitude `r^2`. Integrated as Supplementary Fig. 29.
- **Manuscript destination**: Supplementary Fig. 29 (copied to `latex/supplementary_figs/marginal_distributions_base_only.pdf`; entry in `latex/supplementary_sections/figures.tex`).

## marginal_distributions_by_medium.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/marginal_distributions_by_medium.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Three-by-three per-medium continuous-distribution figure. Rows show Nutr-, Base, and Nutr+; columns show manuscript PDI, computed as `(2/pi) arctan(u/v)` and reflection-symmetrized for visualization; asymmetry magnitude `y`; and squared retention magnitude `r^2`. Used as Response Fig. R2-3.
- **Manuscript destination**: The Supplementary Information uses separate one-medium panels: Supplementary Fig. 29 (Base), Supplementary Fig. 30 (Nutr-), and Supplementary Fig. 31 (Nutr+).

## marginal_distributions_nutr_minus_only.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/marginal_distributions_nutr_minus_only.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Three-panel Nutr-minus continuous-distribution figure. Panels show manuscript PDI, asymmetry magnitude `y`, and squared retention magnitude `r^2`.
- **Manuscript destination**: Supplementary Fig. 30 (copied to `latex/supplementary_figs/marginal_distributions_nutr_minus_only.pdf`; entry in `latex/supplementary_sections/figures.tex`).

## marginal_distributions_nutr_plus_only.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/marginal_distributions_nutr_plus_only.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Three-panel Nutr-plus continuous-distribution figure. Panels show manuscript PDI, asymmetry magnitude `y`, and squared retention magnitude `r^2`.
- **Manuscript destination**: Supplementary Fig. 31 (copied to `latex/supplementary_figs/marginal_distributions_nutr_plus_only.pdf`; entry in `latex/supplementary_sections/figures.tex`).

## boundary_sensitivity_by_medium.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/boundary_sensitivity_by_medium.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- **Description**: Two-panel boundary-sensitivity analysis for R2-3. Panel A recomputes Dominance fractions while varying the PDI boundary, expressed as the distance from equal parental contribution `|PDI - 0.5|`, with retention fixed at `r^2 > 0.5`. Panel B recomputes Dominance fractions while varying the retention boundary `r^2` with the PDI boundary fixed at the manuscript baseline. The manuscript baseline is marked by dashed lines. Used as Response Fig. R2-4.
- **Manuscript destination**: Supplementary Fig. 32 (copied to `latex/supplementary_figs/boundary_sensitivity_by_medium.pdf`; entry in `latex/supplementary_sections/figures.tex`).

## invasion_fitness_analysis.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_4_invasion_fitness/invasion_fitness_analysis.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_4_invasion_fitness/analyze_invasion_fitness.py`
- **Description**: Main invasion-fitness figure linking pairwise selection correlation to correlated invasion outcomes in the gLV model. Key result: excess same-parent selection correlation (observed minus origin-shuffle null) tracks $\mu$ with Pearson r = 0.870, p = 3.2e-8.
- **Manuscript destination**: Supplementary Fig. 28 (copied to `latex/supplementary_figs/invasion_fitness_supp.pdf`; entered in `latex/supplementary_sections/figures.tex`).

## invasion_fitness_distributions.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_4_invasion_fitness/invasion_fitness_distributions.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_4_invasion_fitness/analyze_invasion_fitness.py`
- **Description**: Distributional view of invasion fitness across selected interaction strengths.

## Fig_R3_2_additive_null_comparison.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/Fig_R3_2_additive_null_comparison.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Active Response Fig. R3-2A and Extended Data Fig. 3 focused on Base-medium synthetic coalescence events and the raw-count additive null motivated by Response Fig. R3-2C. Panel A shows the manuscript-style similarity quarter circle with raw-count additive null points, experimental points, and arrows for five randomly selected event-matched null-to-experiment pairs. Panel B shows directional paired PDI/asymmetry arrows from each raw-count null to its corresponding experimental outcome, with auxiliary lines at 0.25, 0.5, and 0.75. Panel C shows the class-transition heatmap with raw-count null class on the x-axis and experimental class on the y-axis.

## fig1_paired_classification.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/fig1_paired_classification.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Superseded standalone panel now merged into `Fig_R3_2_additive_null_comparison.pdf`; observed outcome counts versus case-by-case additive-null outcome counts.

## fig2_delta_PDI_histogram.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/fig2_delta_PDI_histogram.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Distribution of observed-minus-null asymmetry values.

## fig3_contingency_heatmap.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/fig3_contingency_heatmap.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Contingency table comparing observed and null classifications.

## fig4_per_medium_panels.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/fig4_per_medium_panels.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Per-medium observed versus null classification panels.

## fig5_per_medium_contingency.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/fig5_per_medium_contingency.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Per-medium contingency heatmaps for the additive-null comparison.

## fig6_asymmetricity_space.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/fig6_asymmetricity_space.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Superseded standalone panel now merged into `Fig_R3_2_additive_null_comparison.pdf`; observed and additive-null offspring compared in the same retention-asymmetry space.

## fig7_per_medium_delta_PDI.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/fig7_per_medium_delta_PDI.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Medium-specific distributions of the observed-minus-null asymmetry shift.

## fig8_transition_diagram.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additive_null/fig8_transition_diagram.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **Description**: Transition diagram from additive-null classifications to observed classifications.

## richness_by_medium.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_richness_media/richness_by_medium.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_richness_media/analyze_richness_media.py`
- **Description**: Experimental richness distributions across nutrient conditions for parental and coalesced communities.

## richness_coalesced_vs_parental.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_richness_media/richness_coalesced_vs_parental.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_richness_media/analyze_richness_media.py`
- **Description**: Relationship between parental richness and coalesced richness across media.

## richness_thresholds.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_richness_media/richness_thresholds.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_richness_media/analyze_richness_media.py`
- **Description**: Richness robustness analysis across multiple abundance thresholds.

## richness_mu_analysis.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/richness_mu_analysis.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/analyze_richness_mu.py`
- **Description**: Simulation analysis of richness, observed Dominance, null Dominance, and excess Dominance across interaction strengths.

## Fig_R3_3_sim_parent_norm_asymmetry.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/Fig_R3_3_sim_parent_norm_asymmetry.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/analyze_sim_parent_norm_asymmetry.py`
- **Description**: Simulation diagnostics for parent-vector Euclidean norms, paired-parent norm fold differences, and simple-additive-null classifications across interaction strengths.

## Fig_R3_3_richness_summary.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/Fig_R3_3_richness_summary.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/analyze_r3_3_richness_summary.py`
- **Response letter reference**: Response Fig.~R3-3A.
- **Description**: Two-panel richness-only summary for R3-3. Panel A shows final richness of simulated post-assembly sub-communities and coalesced communities across interaction strength. Panel B shows final coalesced-community richness across media and initial pool size in the synthetic-community experiment.

## richness_mu_stacked.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/richness_mu_stacked.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/analyze_richness_mu.py`
- **Description**: Stacked comparison of observed and null outcome structure across interaction strengths.

## interaction_matrix_post_assembly.pdf (copied to latex/supplementary_figs/)
- **Source**: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/interaction_matrix_assembly.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/plot_interaction_matrix.py`
- **Manuscript destination**: `latex/supplementary_figs/interaction_matrix_post_assembly.pdf` (Supplementary Fig. 27)
- **Response letter reference**: `revision_figure_folder/interaction_matrix_assembly.pdf` (as Response Fig. R1-7)
- **Description**: Post-assembly interaction matrices showing assembly-filtered block structure, using a grayscale interaction-strength scale matched to the Fig. 2A matrix assets. Three example replicates show 12+12 seeded species before assembly and the corresponding post-assembly survivor matrices after filtering. Within-community coefficients (mean 0.389) are significantly lower than between-community coefficients (mean 0.500; Mann-Whitney U, p < 0.001), showing that assembly filters surviving communities into mutually weakly competing groups while cross-community coefficients remain near the pool mean.

## Fig_R3_1_diversity_adjusted_sweep.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/Fig_R3_1_diversity_adjusted_sweep.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/analyze_diversity_adjusted.py`
- **Response letter reference**: Response Fig. R3-1C (diversity-adjusted Dominance threshold sweep).
- **Description**: Three-panel figure. (a) Per-event PDI (y) vs inverse-Simpson N_eff(n_C) colored by medium, with adjusted threshold curves y_adj(N_eff) = 0.5 + k/sqrt(N_eff) overlaid for k in {0, 0.5, 1.0, 2.0}. (b) Dominance fraction vs adjustment strength k, overall and per medium. (c) Fate of the 157 baseline (k=0) Dominance events as k tightens (still-Dominance / flipped to Mixture / flipped to Restructuring).

## Fig_R3_1_per_medium_richness.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/Fig_R3_1_per_medium_richness.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/analyze_diversity_adjusted.py`
- **Response letter reference**: Response Fig. R3-1D (richness stratification).
- **Description**: Two-panel figure. (a) Inverse-Simpson N_eff(n_C) distribution per medium (box + jitter); Nutr- median 4.38, Base 2.80, Nutr+ 2.15. (b) Baseline (k=0) Dominance fraction by N_eff tertile, split per medium, showing the global low-tertile enrichment is driven primarily by HN events (which dominate the low-N_eff bin).

## Fig_NullA_permutation.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additional_nulls/Fig_NullA_permutation.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additional_nulls/analyze_additional_nulls.py`
- **Response letter reference**: Response Fig. R3-1E (richness-matched identity-permuted null).
- **Description**: Three-panel figure. (a) Per-event Null A Dominance rate (500 draws per event; n_C rank-abundance preserved, identities reassigned from supp(n_A U n_B)) vs observed class. (b) Per-medium Observed vs Null A mean +/- bootstrap 95% CI. (c) Stratified by N_eff tertile: Observed 85.2% / 58.6% / 35.2% (low / mid / high) vs Null A 19.4% / 11.1% / 6.4%.

## Fig_NullB_bootstrap.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additional_nulls/Fig_NullB_bootstrap.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additional_nulls/analyze_additional_nulls.py`
- **Response letter reference**: Response Fig. R3-1F (richness-stratified bootstrap null, conservative variant).
- **Description**: Three-panel figure. (a) Per-medium Observed Dominance (bar) vs Null B Dominance rate in two variants: within-medium same-N_eff-quartile and any-medium same-N_eff-quartile. (b) Dominance fraction vs N_eff quartile bin, Observed vs both Null B variants. (c) Per-event Null B (within) Dominance rate by N_eff tertile.

## Fig_NullC_mixing_sweep.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additional_nulls/Fig_NullC_mixing_sweep.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additional_nulls/analyze_additional_nulls.py`
- **Response letter reference**: Response Fig. R3-1G (weighted mixing sweep, alpha in [0,1]).
- **Description**: Four-panel figure. (a) Pooled classification fraction (Dominance / Mixture / Restructuring) as a function of alpha for n_C_null = alpha*n_A + (1-alpha)*n_B. (b) Per-medium Dominance vs alpha. (c) Per-event count of alpha values classified as Dominance (out of 11). (d) Stacked classification fractions for MN medium. At alpha = 0.5, Dominance fraction is 0% in every medium, confirming the additive null classification.

## Fig_R3_1_all_nulls_summary.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_additional_nulls/Fig_R3_1_all_nulls_summary.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_additional_nulls/analyze_additional_nulls.py`
- **Response letter reference**: Response Fig. R3-1H (all-nulls summary).
- **Description**: Single-panel grouped bar summary comparing per-medium Dominance rate for Observed, Additive null, Null A, Null B (within-medium), Null B (any-medium), Null C @ alpha=0.5, Null C any-alpha. LN/MN/HN ordering preserved across every null.

## Fig_R3_1_diversity_adjusted_joint.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/Fig_R3_1_diversity_adjusted_joint.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R3_1_diversity_adjusted/analyze_diversity_adjusted.py`
- **Response letter reference**: Response Fig. R3-1K (joint-axis diversity-adjusted threshold, sensitivity check for Option H).
- **Description**: Six-panel joint sensitivity analysis with simultaneous adjustment of PDI (y) and retention (r^2) thresholds: y_adj = min(1, 0.5 + k_y/sqrt(N_eff)) AND r^2_adj = min(1, 0.5 + k_x/sqrt(N_eff)). (a) Diagonal sweep k_y = k_x = k showing overall + per-medium Dominance fraction, with y-only sweep (Option H) overlaid as dashed gray for comparison. (b) Stacked Dominance / Mixture / Restructuring class composition along the diagonal. (c) Heatmap of pooled Dominance fraction over the 5x5 (k_y, k_x) grid. (d-f) Per-medium Dominance heatmaps for LN / MN / HN. Key numbers at diagonal k = 0.5: overall Dom 25.1% (vs 35.7% for y-only), per-medium LN 8.9% / MN 24.1% / HN 42.2%; nutrient ordering LN < MN < HN preserved and widened (HN/LN ratio 4.7x vs 1.94x at baseline). At k >= 0.75 the classifier is over-corrected (Restructuring > 84%).

## internal_LN_OD_PDI_zoom.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_LN_zoom_combined.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_per_medium_OD_PDI_zoom.py` (generalized successor to the prior LN-only `analyze_LN_OD_PDI_zoom.py`; the old script is retained but no longer cited.)
- **Used by**: `latex/revision/internal_memo.tex` (Fig. LN-zoom, \S Q1 "In Nutr- (LN), can community OD explain PDI?"). Not a reviewer-facing figure; supports the internal memo only.
- **Description**: Two-panel LN-only zoomed reanalysis of Response Fig. R1-1A/B, auto-scaled to the Nutr- OD window [0.35, 0.57]. (a) Winner vs loser OD for the 35 LN Dominance events with y=x reference; winner is denser in 13/35 (37%), binomial p=0.18. The OD axes extend slightly below zero and points are semi-transparent for low-OD/overlap readability. (b) Signed dOD (OD_Sub1 - OD_Sub2) vs PDI=u/(u+v) for all n=90 LN events, colored by outcome, with reflected gray points for symmetry and a linear fit overlaid; Spearman rho=-0.24 (p=0.021), Pearson r=-0.24 (p=0.021), slope=-0.79. Auxiliary dotted horizontal lines at PDI=0.25 and 0.75 mark the round-number Dominance/Mixture boundary (exact classifier boundary in PDI is approximately 0.29/0.71). Confirms that within the tight LN OD window, the same "denser parental community loses slightly" trend as Base and Nutr+ holds but is small in magnitude and consistent with interaction-driven rather than biomass-driven exclusion.

## internal_Q5_filter_rank_abundance_parentfit.pdf
- **Source**: `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Fig_Q5_filter_rank_abundance_parentfit.pdf`
- **Code**: `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/make_Q5_filter_rank_abundance_parentfit.py`
- **Used by**: `latex/revision/internal_memo.tex` (Q5b trait-based environmental filtering section).
- **Description**: Three-panel internal diagnostic for the environmental-filtering null after fitting parental rank-abundance structure rather than coalesced richness alone. Fixed theta=0, sigma=1, threshold=0.001, global n0_cv=1.25; medium-specific gamma values are Nutr- 5.0, Base 11.5, Nutr+ 40.5. Panel A compares observed and model parental top-12 rank-abundance curves, panel B shows predicted coalesced outcome fractions, and panel C shows predicted coalesced richness. Dominance rises with filter strength (8.4%, 15.1%, 29.6%), while Restructuring remains essentially absent (0.03%, 0%, 0.23%).

## internal_MN_OD_PDI_zoom.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_MN_zoom_combined.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_per_medium_OD_PDI_zoom.py`
- **Used by**: `latex/revision/internal_memo.tex` (Fig. MN-zoom, \S Q1; companion to LN-zoom). Not reviewer-facing.
- **Description**: Two-panel Base (MN) zoomed reanalysis of Response Fig. R1-1A/B, auto-scaled to the MN OD window [0.061, 1.692]. (a) Winner vs loser OD for the 54 MN Dominance events with y=x reference; winner is denser in 20/54 (37%), binomial p=0.076. The OD axes extend slightly below zero and points are semi-transparent for low-OD/overlap readability. (b) Signed dOD vs PDI for all n=83 MN events, colored by outcome, with reflected gray points for symmetry and a linear fit overlaid; Spearman rho=-0.14 (p=0.19), Pearson r computed together with slope in the figure annotation. Auxiliary dotted horizontal lines at PDI=0.25 and 0.75 mark the round-number Dominance/Mixture boundary. The weak negative slope is consistent in sign with LN and HN but not individually significant.

## internal_HN_OD_PDI_zoom.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_HN_zoom_combined.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_per_medium_OD_PDI_zoom.py`
- **Used by**: `latex/revision/internal_memo.tex` (Fig. HN-zoom, \S Q1; companion to LN-zoom). Not reviewer-facing.
- **Description**: Two-panel Nutr+ (HN) zoomed reanalysis of Response Fig. R1-1A/B, auto-scaled to the HN OD window [0.051, 2.033]. (a) Winner vs loser OD for the 68 HN Dominance events with y=x reference; winner is denser in only 9/68 (13%), binomial p=3.9e-10 - the strongly negative "denser parental community loses" signal driving the across-media trend. The OD axes extend slightly below zero and points are semi-transparent for low-OD/overlap readability. (b) Signed dOD vs PDI for all n=90 HN events, colored by outcome, with reflected gray points for symmetry and a linear fit overlaid; Spearman rho=-0.60 (p=4.0e-10). Auxiliary dotted horizontal lines at PDI=0.25 and 0.75 mark the round-number Dominance/Mixture boundary. Panel (a) is the R2-1 signature of interaction-driven (not biomass-driven) exclusion - in HN the denser parental community is typically an acid producer that nonetheless loses the coalescence.

## internal_LN_biomass_PDI_zoom_simulation.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_LN_zoom_simulation_combined.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_per_medium_biomass_PDI_zoom_simulation.py`
- **Data**: `Figure_generate/code/Simulation_Data/48species_100reps_final/Community_100reps_final.json` (canonical 48-species 100-rep main-text gLV run, generated by `run_48species_100reps_final.py`).
- **Used by**: `latex/revision/internal_memo.tex` (Fig. LN-sim, \S Q1 "gLV-simulation counterpart"). Internal-memo only; not reviewer-facing.
- **Description**: Simulation analogue of Fig. LN-zoom (experimental Nutr-) at mu=0.3. Two panels, same rendering recipe as the experimental zoom but with community OD replaced by total final-day biomass Sum_i y_i. (a) Winner biomass vs loser biomass for the 111 Dominance events among n=600 coalescence events (100 reps x 6 pairs); winner is denser in 96/111 (86%, binomial p=1.2e-15). (b) Signed dbiomass vs PDI for all n=600 events, colored by Dom/Mix/Rest outcome, with reflected gray points for symmetry and a linear fit overlaid; Spearman rho=+0.42 (p=5.5e-27), Pearson r=+0.34, slope=+0.35. Auxiliary dotted horizontal lines at PDI=0.25 and 0.75 mark the round-number Dominance/Mixture boundary. Sign is opposite to experimental LN (experimental rho=-0.24), confirming that the baseline competition-only gLV predicts "denser parental community wins" whereas the data show the opposite.

## internal_MN_biomass_PDI_zoom_simulation.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_MN_zoom_simulation_combined.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_per_medium_biomass_PDI_zoom_simulation.py`
- **Data**: `Figure_generate/code/Simulation_Data/48species_100reps_final/Community_100reps_final.json`.
- **Used by**: `latex/revision/internal_memo.tex` (Fig. MN-sim, \S Q1). Internal-memo only.
- **Description**: Simulation analogue at mu=0.6 (Base). (a) Winner vs loser total biomass for the 357 Dominance events (of n=600); winner is denser in 233/357 (65%, binomial p=8.4e-9). (b) Signed dbiomass vs PDI for all n=600 events with linear fit; Spearman rho=+0.29 (p=1.2e-12), slope=+0.41. Sign is opposite to experimental MN. Companion panel to Fig. LN-sim and HN-sim.

## internal_HN_biomass_PDI_zoom_simulation.pdf
- **Source**: `Figure_generate/code/Figure_revision/R1_1_OD_density/Fig_HN_zoom_simulation_combined.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_per_medium_biomass_PDI_zoom_simulation.py`
- **Data**: `Figure_generate/code/Simulation_Data/48species_100reps_final/Community_100reps_final.json`.
- **Used by**: `latex/revision/internal_memo.tex` (Fig. HN-sim, \S Q1). Internal-memo only. This is the load-bearing contrast figure.
- **Description**: Simulation analogue at mu=0.8 (Nutr+). (a) Winner vs loser total biomass for the 418 Dominance events (of n=600); winner is denser in 271/418 (65%, binomial p=1.4e-9). (b) Signed dbiomass vs PDI for all n=600 events with linear fit; Spearman rho=+0.30 (p=2.7e-14), slope=+0.41. Experimentally HN shows 13% winner-denser and rho=-0.60; the baseline gLV produces the exact opposite sign on both diagnostics. This is the clean demonstration that the Nutr+ "denser parental community loses" signature cannot be produced by a random-alpha_{ij} competition-only gLV and must arise from species-identity mechanisms (pH-mediated acid-producer asymmetry; see R1-2 and Fig. Q3).

## internal_Q3_pH_rule_vs_gLV.pdf
- **Source**: `Figure_generate/code/Figure_revision/Q3_pH_rule_vs_gLV/Fig_Q3_pH_rule_vs_gLV.pdf`
- **Code**: `Figure_generate/code/Figure_revision/Q3_pH_rule_vs_gLV/analyze_pH_rule_vs_gLV.py`
- **Used by**: `latex/revision/internal_memo.tex` (Fig. Q3, \S Q3 "Pure pH model vs. gLV"). Internal-memo only; not reviewer-facing.
- **Description**: Two-panel comparison of the minimal "acidic parental community wins" pH rule and the gLV framework on orthogonal prediction axes. (a) Winner-direction axis: fraction of acid-alk Dominance events in which the acidic parental community won, per medium (Nutr-, Base, Nutr+). 19/27=70% in Base (binom p=0.052) and 30/35=86% in Nutr+ (p=2.2e-5); Nutr- has no acid-alk events. Wilson 95% CI; gLV-implicit 50% baseline as dashed reference. (b) Class-frequency axis: observed Dominance fraction per medium versus comp-regime gLV prediction at nearest simulated mu (mu=0.3/0.6/0.8 from R3_3_nonCompetitive_gLV/non_competitive_results.json). Observed: 39/65/76 percent; gLV: 22/60/73 percent. Nutr- undershoot reflects the mu=0.3 reference vs calibrated mu~0.5 offset. Key conclusion: the two models make predictions on different axes (winner direction vs class frequency) and so cannot refute each other; they are complementary. See Q5 for Ratzke-Gore-style pH-feedback mechanistic model that would subsume both axes.

## Fig_Q6_Kr_Kstd_all_media.pdf and Fig_Q6_Kr_Rstd_all_media.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_6_gLV_K_r_heterogeneity/Fig_Q6_Kr_{Kstd,Rstd}_all_media.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_6_gLV_K_r_heterogeneity/analyze_K_r_heterogeneity.py`
- **Data**: 40-rep finite-time gLV K/r heterogeneity sweep written to `kr_heterogeneity_events.csv` and summarized in `kr_heterogeneity_summary.csv`.
- **Used by**: `latex/revision/internal_memo.tex` (Q1 K/r heterogeneity stress test). Internal-memo only; not reviewer-facing.
- **Description**: Two all-media variants of the LN-sim/MN-sim/HN-sim biomass-PDI diagnostic. `Fig_Q6_Kr_Kstd_all_media.pdf` varies carrying-capacity heterogeneity (`K` sd = 0, 0.5, 1.0) with `r` sd fixed at 0 across LN/MN/HN. `Fig_Q6_Kr_Rstd_all_media.pdf` varies growth-rate heterogeneity (`r` sd = 0, 0.5, 1.0) with `K` sd fixed at 0 across LN/MN/HN. Both use positive-truncated Normal draws. Across all valid rows the signed biomass-PDI correlation remains positive and the denser parental community wins more than half of Dominance events, so simple positive K or r heterogeneity does not reproduce the experimental Nutr+ denser-parental-community-loses pattern.

## Fig_Q6_Kr_LN_sim_variants.pdf, Fig_Q6_Kr_MN_sim_variants.pdf, Fig_Q6_Kr_HN_sim_variants.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_6_gLV_K_r_heterogeneity/Fig_Q6_Kr_{LN,MN,HN}_sim_variants.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_6_gLV_K_r_heterogeneity/analyze_K_r_heterogeneity.py`
- **Status**: Generated but no longer embedded in `internal_memo.tex`; superseded there by the two all-media K-only and r-only figures above.
- **Description**: Medium-specific multi-row variants of the same K/r sweep.

## Fig_Q6_Kr_phase_trend.pdf and Fig_Q6_Kr_winner_direction.pdf
- **Source**: `Figure_generate/code/Figure_revision/R2_6_gLV_K_r_heterogeneity/Fig_Q6_Kr_{phase_trend,winner_direction}.pdf`
- **Code**: `Figure_generate/code/Figure_revision/R2_6_gLV_K_r_heterogeneity/analyze_K_r_heterogeneity.py`
- **Data**: same 40-rep finite-time K/r heterogeneity sweep as above.
- **Used by**: internal summary / QC; not currently embedded in `internal_memo.tex`.
- **Description**: Compact summary figures for the K/r heterogeneity sweep. `Fig_Q6_Kr_phase_trend.pdf` shows outcome-class fractions across `mu` for each K/r grid point. `Fig_Q6_Kr_winner_direction.pdf` summarizes the Dominance-event winner-denser fraction across the same grid.

## internal_Q5_phase_gLV.pdf, internal_Q5_phase_pH.pdf, internal_Q5_phase_hybrid.pdf
- **Source**: `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Fig_Q5_phase_{gLV,pH,hybrid}.pdf`
- **Code**:
  - `simulate_Q5_phase_diagrams.py` - driver that runs all three models at three matched interaction-strength levels (weak/mid/strong) and dumps per-event (sim_a, sim_b, class, phi) rows to `Q5_phase_events.csv`.
  - `make_Q5_phase_figures.py` - renders three per-model phase-diagram figures in the Response Fig. R3-2.0a style (scatter in Sim(A,C)-Sim(B,C) plane with classifier boundary arcs + adjacent stacked-bar phase panel). Updated 2026-04-30 to color scatter points by outcome class and add tiny deterministic visual jitter so endpoint piles, especially pH Restructuring events at (0,0), (1,0), and (0,1), are visible.
- **Used by**: `latex/revision/internal_memo.tex` (Figs. Q5-gLV, Q5-pH, Q5-hybrid in \S Q5). `internal_Q5_phase_pH.pdf` is also used as Response Fig. R2-2B in `latex/revision/response/reviewer2_response.tex`.
- **Description**: Per-model phase diagrams adopting the R3-2.0a reviewer-style rendering. Each figure has 4 panels: A/B/C = scatter of per-event (Sim(A,C), Sim(B,C)) at weak/mid/strong interaction strength with the paper's classifier boundaries overlaid (outer arc r=1, inner arc r=1/sqrt(2), radial dashed lines at pi/8 and 3pi/8); D = stacked phase-diagram bar chart. Distinctive visual signatures:
  - gLV: interior-diffuse scatter, drifts to axes as mu rises.
  - pH-feedback: updated 2026-04-30 to the original-code-like Gaussian/logistic model with continuous plain p relaxation. Coalescence initializes the environmental coordinate from the stabilized parents, `p_AB,0 = (p_A + p_B)/2`, matching the 50/50 biomass merge rather than resetting to fresh medium. Degenerate pH events where A, B, or C has no surviving species are excluded from the D/M/R denominator. The representative phase panels use cmax=1e-10/1e-9/3e-8 with 100 pools; Dominance is 0/37/56% over valid events.
  - pH+LV hybrid: points concentrated at endpoints (1,0) and (0,1), Dominance saturated at 70-88%.

## internal_Q5_three_models_per_model.pdf
- **Source**: `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Fig_Q5_three_models_per_model.pdf`
- **Code**: three simulators + unified driver + plotting script under `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/`:
  - `pH_feedback_model.py` - Ratzke & Gore 2018 PLOS Biology Eqs. 1-2 ODE simulator (Model 2, pure pH feedback).
  - `pH_plus_LV_model.py` - pH+LV hybrid (Model 3); Ratzke pH ODE + gLV competition matrix with A_ii=1, A_ij~U(0, 2mu). Adapted from the user's `/Users/jysong/Desktop/Codes/pH_model_Simulation/LV.py` (`gLV_pH_set1`), re-grounded on the Ratzke pH ODE.
  - `simulate_Q5_all_models.py` - unified driver; runs all three models on a shared (mu, tau) grid; writes `Q5_all_models_results.json`.
  - `make_Q5_comparison_per_model.py` - renders the per-model comparison figure.
- **Used by**: `latex/revision/internal_memo.tex` (Fig. Q5, \S Q5 "Beyond the pairwise model"). Internal-memo only; not reviewer-facing.
- **Description**: Per-model comparison of coalescence models on a common classification pipeline (same common_setup helpers). The pure pH-feedback panel uses plotted representative points cmax=1e-10/1e-9/3e-8 with 100 pools and excludes degenerate events where A, B, or C has no survivor. Coalescence initializes the environmental coordinate from the stabilized parents, `p_AB,0 = (p_A + p_B)/2`. Updated 2026-04-30: pure pH-feedback now uses the original-code-like Gaussian/logistic model with continuous plain p relaxation. Key numbers: gLV Dom 0/18/60/88%, |phi| 0.21/0.21/0.47/0.86; pH-only representative Dom 2/37/59%, |phi| 0.29/0.59/0.79. The full original pH grid remains diagnostic for collapse: cmax >= 1e-6 has 79-85 excluded events per 100. Load-bearing interpretation after the degenerate-filter update: pure pH feedback can produce asymmetric replacement in a clean intermediate-strength range, but the original-grid high end is not interpretable as ordinary coalescence.

## internal_Q5_phase_filter.pdf
- **Source**: `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Fig_Q5_phase_filter.pdf`
- **Code**: `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/environmental_filter_model.py`, `simulate_Q5_phase_environmental_filter.py`, and `make_Q5_phase_environmental_filter.py`
- **Used by**: `latex/revision/internal_memo.tex` (\S Q5b "Trait-based environmental filtering model for nutrient-dependent niche availability"). Internal-memo only; not reviewer-facing.
- **Description**: Trait-based environmental-filtering null model in the same 4-panel layout as Fig. Q5-pH. Species have latent traits `z_i ~ N(0,1)`. Each nutrient condition applies a Gaussian niche filter with fixed center and breadth (`theta=0`, `sigma=1`) and only the strength exponent `gamma` varies. The calibrated settings are Nutr- `gamma=2.80`, Base `gamma=7.95`, and Nutr+ `gamma=10.15`, with relative-abundance threshold `0.02`. These values were chosen to match the observed P12 coalesced richness means. The regenerated 500-pool-per-condition simulation gives mean coalesced richness 13.5 / 9.8 / 8.8 and Dominance 0.0% / 1.2% / 1.0% for Nutr- / Base / Nutr+, respectively. Interpretation: richness-matched environmental filtering alone reproduces the richness scale but remains overwhelmingly Mixture, so it does not explain the observed nutrient-dependent Dominance trend.

## R3_3_combined.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_3_combined.pdf`
- **Code**:
  - Panels A-D (experiment): `Figure_generate/code/Figure_revision/R3_3_pair_additivity/analyze_pair_additivity.py` + `make_R3_3_figure.py`.
  - Panels E-H (simulation): `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_non_competitive.py` + `make_R3_3_figure.py`.
- **Response letter reference**: Superseded R3-4 composite. The current R3-4 response now uses the split figures `R3_4_experiment.pdf`, `R3_4_mixed_sign_higher_order.pdf`, `R3_4_simulation.pdf`, `R3_4_pair_coupling_fine.pdf`, `R3_4_mutualistic_pair_fraction.pdf`, and `R3_4_mean_variance_grid.pdf` as Response Figs.~R3-4a--f.
- **Description**: Eight-panel figure.
  - **A-C** scatter of coculture CFU total ($C_i + C_j$) vs. monoculture CFU sum ($M_i + M_j$) for each medium, using the 12-isolate pairwise invasion assay (colony counts from `Postprocessed/PairwiseColonyCountings_processed_230915.xlsx`). Dashed line is additivity. Annotations: % sub-additive ($C_i+C_j < M_i+M_j$) and % with Relative Yield Total ($RYT = C_i/M_i + C_j/M_j$) below 1.
  - **D** per-medium bar chart of % sub-additive (light blue) and % RYT $<$ 1 (dark blue). Values: sub-add. 80 / 93 / 90; RYT$<$1 20 / 69 / 88 for Nutr-/Base/Nutr+.
  - **E-G** stacked outcome fractions (Dominance / Mixture / Restructuring) at $\mu = 0.30, 0.60, 0.80$ for three gLV regimes: comp (baseline, $\alpha_{ij} \sim U[0, 2\mu]$), exploit (15\% of pairs have $\alpha_{ji}$ flipped to $U[-0.4 \cdot 2\mu, 0]$), cooperate (15\% of pairs have both $\alpha_{ij}, \alpha_{ji} \sim U[-0.4 \cdot 2\mu, 0]$). Stability: row-sum criterion within each 12-species community (diag $>$ sum of negatives); hard-reject otherwise, re-sample up to 200 times.
  - **H** pairwise selection correlation $|\phi|$ (origin $\to$ persistence) across the three $\mu$ values for each regime.
  - Data: 60 pools $\times$ 6 coalescence events = up to 360 events per (\mu, regime). Rejection rates are highest for coop at high $\mu$ (coop15 at $\mu=0.80$ yielded 78 events after 954 rejections; reported fractions are still representative but sampling-limited).

## R3_4_mixed_sign_higher_order.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_mixed_sign_higher_order.pdf`
- **Code**:
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mixed_sign_higher_order.py`
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mixed_sign_higher_order_figure.py`
- **Response letter reference**: Response Fig.~R3-4b in `reviewer3_response.tex`.
- **Description**: Five-panel stacked-bar sweep of a true mixed-sign facilitative-tail gLV with density-dependent self-limitation. Dynamics: `dn_i/dt = n_i (1 - (A n)_i - gamma n_i^2)`, with `gamma = 0.10`. Off-diagonal coefficients are sampled iid from `U[-f mu, (2+f) mu]`, preserving mean interaction coefficient `E[alpha_ij] = mu` while increasing the expected facilitative fraction `P(alpha < 0)` from 0 to 22.2% as `f` goes from 0 to 0.8. New top insets show the analytic density of the normalized coefficient `alpha/mu`, with negative support colored red and nonnegative support colored gray; these are formula-derived histograms, not Monte Carlo coefficient samples. Grid: `mu = 0.30, 0.60, 0.80`; `f = 0, 0.10, 0.20, 0.40, 0.80`; 200 pools per cell; 48 species split into four 12-species communities; up to 1200 coalescence events per cell. Numerical integration used LSODA because mixed-sign higher-order dynamics can be stiff near the facilitation/self-limitation boundary. Main result: Dominance still rises with `mu` at every `f`; at low `mu`, increasing the facilitative tail shifts outcomes away from Mixture toward both Dominance and Restructuring (Dom/Mix/Res at `mu=0.30`: 18/73/9% at `f=0`, 43/33/24% at `f=0.8`). At high `mu`, Dominance remains high across the facilitative tail (about 70-76%). Rejection and coalescence-failure counts remain modest after adding `gamma = 0.10`.

## R3_4_experiment.pdf and R3_4_simulation.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_experiment.pdf` and `Figure_generate/code/Figure_revision/R3_4_simulation.pdf`
- **Code**:
  - Experimental panels: `Figure_generate/code/Figure_revision/R3_3_pair_additivity/analyze_pair_additivity.py`
  - Figure rendering: `Figure_generate/code/Figure_revision/R3_3_pair_additivity/make_R3_3_figure.py`
  - Simulation data used for R3_4_simulation.pdf: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/p_axis_results.json`, generated by `simulate_p_axis.py`
- **Response letter reference**: Response Fig. R3-4a (`R3_4_experiment.pdf`) and Response Fig. R3-4c (`R3_4_simulation.pdf`).
- **Description**: `R3_4_experiment.pdf` shows species-level coculture suppression for the 12-isolate assay. Panels A-C plot each focal ASV's coculture CFU (`C_i`, averaged across available invasion directions) against that same ASV's monoculture CFU (`M_i`); points below the diagonal are directly suppressed in coculture. Panel D summarizes the fraction of species-in-pair observations below monoculture expectation: 79 / 84 / 93% for Nutr- / Base / Nutr+. The same underlying data retain the stricter pair-level RYT<1 fractions 20 / 69 / 88% for Nutr- / Base / Nutr+, but those stricter summaries are not used in the current response prose. `R3_4_simulation.pdf` shows the reciprocal pair-coupling robustness sweep. Panels are ordered monotonically by `p`: `p=-1`, `p=-0.5`, `p=0`, `p=+0.5`, `p=+1`. New top insets show the analytic directed-coefficient distribution of `alpha/mu` implied by each `p` value, with negative coefficients colored red and nonnegative coefficients colored gray; these are sampler-definition histograms, not Monte Carlo samples. For each `p`, stacked bars show Dominance / Mixture / Restructuring at `mu = 0.30, 0.60, 0.80`. Stored fractions in `p_axis_results.json` sum to 1.000000 in every (`p`, `mu`) cell. Key Dominance fractions by `p=-1/-0.5/0/+0.5/+1`: at `mu=0.30`, 43.8/35.8/18.4/34.8/47.5%; at `mu=0.60`, 68.8/58.0/60.0/75.3/77.2%; at `mu=0.80`, 78.1/66.0/70.5/78.0/79.6%.

## R3_4_pair_coupling_fine.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_pair_coupling_fine.pdf`
- **Code**:
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_p_axis_fine.py`
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_p_axis_fine_figure.py`
- **Response letter reference**: Response Fig. R3-4d.
- **Description**: Fine reciprocal pair-coupling sweep using the same sampler as Response Fig. R3-4c. The sweep uses `p = -1, -0.8, ..., +0.8, +1` for each `mu = 0.30, 0.60, 0.80`, with 200 pools per cell. New top strips show representative analytic directed-coefficient distributions for `p=-1`, `p=0`, and `p=+1`; they are formula-derived references for the sampler, not Monte Carlo coefficient samples. Fractions in `p_axis_fine_results.json` sum to 1.000000 in all 33 cells; the minimum usable event count is 1158 out of 1200. Dominance fractions across `p=-1,-0.8,-0.6,-0.4,-0.2,0,+0.2,+0.4,+0.6,+0.8,+1`: at `mu=0.30`, 43.2/39.8/37.7/31.3/27.1/21.8/25.1/32.8/39.0/43.6/46.8%; at `mu=0.60`, 70.2/68.7/59.5/58.1/59.7/63.6/68.9/72.1/74.6/75.6/78.3%; at `mu=0.80`, 77.1/71.7/67.8/68.3/64.9/72.3/75.8/78.0/80.3/77.4/78.4%.

## R3_4_mutualistic_pair_fraction.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_mutualistic_pair_fraction.pdf`
- **Code**:
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mutualistic_pair_fraction.py`
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mutualistic_pair_fraction_figure.py`
- **Data**: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/mutualistic_pair_fraction_results.json`
- **Response letter reference**: Response Fig. R3-4e.
- **Description**: Weak bidirectional mutualistic-pair fraction sweep added for the reviewer's mutualism subquestion. For `q = 0, 0.10, 0.20, 0.30, 0.40` of unordered species pairs, both reciprocal coefficients are drawn from `U[-0.2 mu, 0]`, corresponding to weak positive ecological interactions under the manuscript sign convention. Remaining off-diagonal coefficients are sampled from the baseline competitive distribution `U[0, 2mu]`. Dynamics use density-dependent self-limitation, `dn_i/dt = n_i (1 - (A n)_i - gamma n_i^2)`, with `gamma = 0.10`, and the same assembly/coalescence/classification pipeline as the facilitative-tail robustness analysis. Grid: `mu = 0.30, 0.60, 0.80`; 200 pools per cell; up to 1200 coalescence events per cell. Dominance fractions by `q=0/0.10/0.20/0.30/0.40`: at `mu=0.30`, 18.2/31.0/33.6/30.5/25.5%; at `mu=0.60`, 58.5/70.2/69.8/67.3/58.7%; at `mu=0.80`, 71.4/77.5/75.8/72.3/69.4%.

## R3_4_mean_variance_grid.pdf
- **Source**: `Figure_generate/code/Figure_revision/R3_4_mean_variance_grid.pdf`
- **Code**:
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/simulate_mean_variance_grid.py`
  - `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mean_variance_grid_figure.py`
- **Data**: `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/mean_variance_grid_results.json`
- **Response letter reference**: Response Fig. R3-4f.
- **Description**: Mean-vs-variance interaction-coefficient sweep added to separate the mean coefficient from coefficient variance. Off-diagonal coefficients are drawn from `U[m - h, m + h]`, with `m = 0, 0.20, 0.40, 0.60, 0.80` and `h = 0, 0.20, 0.40, 0.60, 0.80`, so `std(alpha) = h/sqrt(3)`. Negative coefficients, corresponding to positive ecological interactions under the manuscript sign convention, occur when `h > m`. Dynamics use density-dependent self-limitation with `gamma = 0.10`; each cell uses 200 pools and up to 1200 coalescence events. Dominance fractions by `h=0/0.20/0.40/0.60/0.80`, with columns `m=0/0.20/0.40/0.60/0.80`: `0.0/0.0/0.0/0.0/0.0`, `0.0/1.1/8.0/24.0/47.8`, `8.8/24.8/40.0/46.8/62.8`, `20.5/39.6/49.1/58.6/70.7`, and `28.0/47.0/57.4/62.7/72.8`. Across the 25 cells, Dominance correlates more strongly with `h` (or coefficient standard deviation) than with `m` (descriptive Pearson `r=0.78` vs `0.53`).
