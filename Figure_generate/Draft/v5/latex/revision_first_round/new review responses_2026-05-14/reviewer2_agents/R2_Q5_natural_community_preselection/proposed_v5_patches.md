# Proposed v5 Patches: Reviewer 2, Question 5

Authoritative v5 files were not edited. These are proposed changes for the coordinating revision worker or PI to apply if accepted.

## 1. Results: Narrow Natural-Community Claim

File: `Figure_generate/Draft/v5/latex/sections/results.tex`

Replace the final `\rev{...}` sentence in the natural-community Results paragraph at line 122:

```tex
\rev{These results suggest that the nutrient-dependent increase in Dominance observed in synthetic consortia is also present in laboratory-stabilized communities derived from taxonomically richer natural samples.}
```

with:

```tex
\rev{These results suggest that the nutrient-dependent increase in Dominance observed in synthetic consortia is also present in laboratory-stabilized communities derived from taxonomically richer natural samples. Because these communities were enriched for seven serial growth-dilution cycles before coalescence, we interpret this comparison as a test of natural sample-derived laboratory enrichments rather than of unfiltered natural communities.}
```

Rationale: preserves the supported qualitative result while making the stabilization filter explicit.

## 2. Figure 6 Caption: Avoid Overstating Generality

File: `Figure_generate/Draft/v5/latex/sections/results.tex`

Replace the Fig. 6 caption title:

```tex
\caption{\textbf{Fig.~6. Dominance generalizes to natural sample-derived communities.}
```

with:

```tex
\caption{\textbf{Fig.~6. Dominance patterns in laboratory-stabilized natural sample-derived communities.}
```

Rationale: avoids implying broad generality to unfiltered natural ecosystems.

## 3. Discussion: Replace Current Pre-Selection Caveat With More Explicit Limitation

File: `Figure_generate/Draft/v5/latex/sections/discussion.tex`

Replace the current pre-selection paragraph at line 20:

```tex
\rev{A related caveat concerns our natural community experiments. The stabilization phase, seven serial growth-dilution cycles in defined laboratory media, may pre-select natural communities toward species that thrive under these specific culture conditions, potentially reducing effective diversity and making natural communities functionally more similar to our synthetic consortia. This pre-selection could contribute to the convergent coalescence patterns observed between natural and synthetic communities, though it is unlikely to account fully for the qualitative trend of increasing Dominance with nutrient concentration, which is preserved across both community types. Future work using culture-independent approaches or broader environmental sampling could help disentangle the contributions of laboratory adaptation from intrinsic ecological dynamics.}
```

with:

```tex
\rev{A related caveat concerns our natural community experiments. The stabilization phase, seven serial growth-dilution cycles in defined laboratory media, may pre-select natural communities toward taxa and metabolic strategies that thrive under these culture conditions \citep{Goldford2018}, potentially reducing effective ecological heterogeneity and making natural sample-derived communities more similar to our synthetic consortia. Our post-stabilization 16S data show that this filtering was not complete at the ASV level: natural sample-derived parental communities retained higher richness than the synthetic parental communities ($13.7 \pm 7.2$ versus $9.8 \pm 4.8$ ASVs above the 0.1\% threshold) and low ASV overlap among communities from different source samples (Supplementary Figs.~22--25). However, because we did not sequence the original environmental inocula before enrichment, we cannot quantify taxonomic convergence during stabilization. We also cannot directly test functional convergence because these experiments used 16S community profiling rather than functional metagenomic, metabolomic, or trait-resolved measurements. Thus, pre-selection could contribute to the convergent coalescence patterns observed between synthetic and natural sample-derived communities, and the natural-community results should be interpreted as evidence that the nutrient-dependent increase in Dominance occurs in taxonomically richer laboratory-stabilized enrichments, not as evidence for unrestricted generality across unfiltered natural ecosystems. Future work using culture-independent time series or broader environmental sampling could help disentangle laboratory adaptation from intrinsic ecological dynamics.}
```

Rationale: directly answers the reviewer request to discuss pre-selection and clarify what can and cannot be said about taxonomic and functional convergence.

## 4. Optional SI Or Response-Figure Integration

No required SI patch is proposed. The response-only figure in this worker folder is useful for the rebuttal but is not necessary for the manuscript because the same core natural-community evidence is already represented in Fig. 6 and Supplementary Figs. 22-25. If the team wants to integrate the response-only analysis into the SI, add it as a short supplementary figure rather than replacing existing natural-community figures.
