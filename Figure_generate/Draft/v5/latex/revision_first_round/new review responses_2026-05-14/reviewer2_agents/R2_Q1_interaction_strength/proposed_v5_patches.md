# Proposed v5 Patches: Reviewer 2 Q1

These patches are proposed only. This worker did not edit authoritative v5 manuscript, SI, revision, or response files.

## 1. Results subsection title

File: `Figure_generate/Draft/v5/latex/sections/results.tex`

Current:

```tex
\subsection{Nutrient-dependent interaction strength in experiments recapitulates model predictions}
```

Proposed:

```tex
\subsection{Nutrient-dependent interaction intensity and environmental feedbacks recapitulate model predictions}
```

Rationale: avoids treating nutrient concentration as a direct scalar proxy for pairwise coefficients.

## 2. Results nutrient-gradient opening

File: `Figure_generate/Draft/v5/latex/sections/results.tex`

Replace the paragraph beginning with `Following prior work showing that nutrient concentration intensifies microbial competition` and the next sentence beginning with `Given that nutrient concentration modulates interaction strength` with:

```tex
Following prior work showing that nutrient concentration can intensify microbial competition and environmentally mediated inhibition \citep{Hu2022,Ratzke2020,Hu2025}, we conducted additional coalescence experiments by removing or augmenting glucose and urea in the Base medium used in \figref{fig:fig1} (Methods). This yielded two additional media conditions (\figref{fig:fig4}A): Nutr$-$ (no added glucose/urea) and Nutr$+$ (high supplementation). We treat this manipulation as a perturbation of net interaction intensity and environmental feedbacks, not as a direct measurement of a single pairwise interaction coefficient. To operationally quantify its effect, we measured failed invasion frequency using pairwise invasion assays among the 12 most abundant isolates (95:5 initial frequency; Methods, Supplementary Figs.~7--9). The fraction of failed invasions increased monotonically with nutrient supply (Nutr$-$: $2 \pm 1\%$; Base: $33 \pm 4\%$; Nutr$+$: $48 \pm 4\%$; mean $\pm$ s.e.m.; \figref{fig:fig4}B), indicating that invasion resistance increases across the nutrient gradient.

We then performed coalescence experiments in Nutr$-$ and Nutr$+$ media using the same parental community library to examine whether this nutrient-dependent change in invasion resistance and environmental feedbacks is accompanied by the predicted shift in coalescence outcomes.
```

Rationale: preserves the empirical evidence while removing the unsupported claim that nutrient supply directly strengthens all effective pairwise interactions.

## 3. Fig. 4 caption title and first sentences

File: `Figure_generate/Draft/v5/latex/sections/results.tex`

Current:

```tex
\caption{\textbf{Fig.~4. Nutrient concentration modulates interaction strength and validates model predictions.} Experimental manipulation of nutrient concentration confirms that stronger interactions shift coalescence outcomes from Mixture toward Dominance.
```

Proposed:

```tex
\caption{\textbf{Fig.~4. Nutrient concentration modulates invasion resistance and coalescence outcomes.} Experimental manipulation of nutrient concentration tests whether increased operational interaction intensity and environmental feedbacks shift coalescence outcomes from Mixture toward Dominance.
```

Rationale: makes Fig. 4 consistent with the response to Reviewer 2 Q1.

## 4. Introduction final framing paragraph

File: `Figure_generate/Draft/v5/latex/sections/introduction.tex`

Replace the final sentence of the main introductory framing paragraph:

```tex
These results reconcile conflicting observations by establishing interaction strength as the control parameter for community-level selection.
```

with:

```tex
These results reconcile conflicting observations by identifying interaction intensity, environmental feedbacks, and assembly-generated interaction structure as key determinants of when community-level selection emerges.
```

Rationale: addresses the reviewer's concern at the level of the central claim.

## 5. Discussion caveat paragraph with citations

File: `Figure_generate/Draft/v5/latex/sections/discussion.tex`

Replace the paragraph beginning with `Our experimental design of using nutrient concentration to modulate interaction strength relies` with:

```tex
Our experimental design uses nutrient concentration to perturb net interaction intensity and environmental feedbacks, but this should not be read as a direct monotonic mapping from external resource supply to effective pairwise Lotka--Volterra coefficients. The gLV parameter $\mu$ is a simplified scalar model parameter, and the mapping between nutrient concentration and $\mu$ is necessarily approximate. This phenomenological mapping is intended to capture the net interaction intensity expressed in invasion outcomes, rather than to identify a unique biochemical mechanism. In our experiments, the nutrient-dependent increase in invasion resistance could reflect several non-mutually exclusive processes, including denser resource competition, increased metabolic activity, environmental modification such as pH shifts, changes in carrying capacities, and changes in competition--facilitation balance. This broader interpretation is consistent with work showing that microbial communities can assemble through environmental feedbacks and nutrient-mediated ecological structure \citep{Goldford2018,Estrela2021}, and with consumer-resource theory showing that external supply rate need not map monotonically onto effective Lotka--Volterra coefficients under broad conditions \citep{DuanPawar2025}. Nevertheless, the monotonic increase in failed pairwise invasions with nutrient supply provides direct experimental evidence that invasion resistance increases across our nutrient gradient, and the qualitative agreement between model predictions and experimental outcomes across all three conditions supports the utility of this coarse-grained framework.
```

Rationale: directly acknowledges the Duan et al. consumer-resource point and incorporates the reviewer-suggested environmental-feedback literature.

## 6. Discussion opening sentence

File: `Figure_generate/Draft/v5/latex/sections/discussion.tex`

Current:

```tex
Our work demonstrates that interspecies interaction strength governs community coalescence outcomes, determining both the dominant outcome type and the level at which selection operates.
```

Proposed:

```tex
Our work demonstrates that interaction intensity, environmental feedbacks, and assembly-generated interaction structure govern community coalescence outcomes, determining both the dominant outcome type and the level at which selection operates.
```

Rationale: aligns the first Discussion sentence with the narrowed claim.

## 7. No SI patch required beyond current v5 text

The current Supplementary Methods already states that each gLV `alpha_ij` is an effective per-capita term that can absorb indirect inhibitory mechanisms such as pH modification, that the model does not dynamically represent pH or other environmental state variables, and that `mu` parameterizes average interspecific competition only within the simulated gLV system. No additional SI change is required for Q1 unless the main-text terminology changes create cross-reference needs.
