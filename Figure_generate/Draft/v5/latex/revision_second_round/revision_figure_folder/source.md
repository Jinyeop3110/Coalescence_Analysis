# Second-Round Response Figure Provenance

This directory stores response-only figures used by
`../response_letter.tex`. It is intentionally empty at scaffold creation.

For every imported or regenerated figure, record:

- copied filename;
- original source path;
- generating script;
- source data or analysis output;
- reviewer point;
- short scientific description;
- whether the same asset also appears in the manuscript or Supplementary Information.

Do not link the response letter directly to figure files elsewhere in the
project. Copy reviewer-facing response figures here and keep this provenance
map current.

## Supplementary Fig. 14 OD-pH update

- **generated filename**: `latex/supplementary_figs/Fig_R1_1B_OD_vs_PDI.pdf`
- **generating script**: `public_code_repo/figures/supplementary/make_supp_fig14_od_ph.py`
- **source data**: `public_code_repo/data/Metadata.xlsx`, `public_code_repo/data/processed_CoalescenceEvent_synthetic.xlsx`, `public_code_repo/data/processed_Sequences_synthetic.xlsx`
- **reviewer point**: Reviewer 1 suggested checking whether the lower-OD Nutr$+$ winner pattern relates to parental-community pH.
- **description**: Existing signed OD-difference-vs-PDI control retained as the top row; a second row was added showing the direct association between endpoint OD$_{600}$ and endpoint pH across parental-community replicates in each medium.
- **manuscript status**: appears in the Supplementary Information as Supplementary Fig. 14.

## Proposed Fig. 1 outcome-comparison panel, simulation at mu = 0.6

- **generated filenames**: `fig1_outcome_comparison_simulation_mu0p6.pdf`, `.svg`, and `.png`; tabulated counts in `fig1_outcome_comparison_simulation_mu0p6_counts.csv`
- **generating script**: `make_fig1_outcome_comparison_simulation_mu0p6.py`, using the shared layout in `make_fig1_outcome_comparison.py`
- **source data**: `Figure_generate/code/Simulation_Data/coalescence_vs_direct_50reps/Community_coalescence_50reps.json` and `Community_direct_50reps.json`
- **upstream analysis**: the coalescence and direct-assembly classifications reuse `Figure_generate/code/plot_assembly_effect_separate_pies.py`; the event-matched simple additive null replaces each valid coalescence outcome with `c1 + c2` and applies that same classifier
- **reviewer point**: second-round Reviewer 2 clarification of Dominance as the compositional signature of origin-correlated persistence, with the coalescence-versus-direct-assembly comparison providing the assembly-history test
- **description**: three stacked bars at interaction-strength parameter value mu = 0.6. Coalescence gives Dominance/Mixture/Restructuring counts 295/96/108 (n = 499); direct assembly gives 99/93/308 (n = 500); and the coalescence-event-matched simple additive null gives 1/498/0 (n = 499).
- **manuscript status**: candidate response/main-figure artwork only; it is not currently included in the manuscript, Supplementary Information, or clean submission tree
