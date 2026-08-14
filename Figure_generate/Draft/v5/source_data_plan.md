# Source Data workbook — plan

Single `.xlsx`, one sheet per dataset, covering the figure source data that is **not** raw
sequencing and **not** community composition. Drafted 2026-08-01.

Target filename: `Source_Data.xlsx`, delivered alongside the manuscript and mirrored into the
Dryad deposit.

---

## 1. Scope

Three tiers of data exist behind the display items. Only the third belongs in this workbook.

| Tier | What | Where it goes |
|---|---|---|
| Raw reads | Demultiplexed 16S V4 fastq | NCBI SRA (tracker ED-18) |
| Composition | Per-sample ASV relative-abundance vectors, raw ASV counts | Dryad, as now |
| **Everything else** | **Phenotype measurements, colony counts, per-event derived scalars, simulation summaries** | **This workbook** |

The dividing line that matters: a sheet belongs here if it holds **the numbers that are actually
plotted**, and those numbers are not themselves a composition vector. A rank-abundance curve is a
composition vector drawn sideways, so it stays on Dryad. A per-event dominance index is a scalar
derived from composition, so it comes here.

One consequence worth stating up front: **building this workbook resolves tracker ED-20.** The
pairwise invasion assay outcomes behind Fig. 4b and Fig. 5c are currently in the working tree only
(`Postprocessed/PairwiseColonyCountings_processed_230915.xlsx`) and are absent from Dryad, which is
why `fig5/README.md` records panel c as unreproducible. Sheets S06 to S08 put them in the package
and make "Source data for the figures are provided within this deposit" true on that point.

---

## 2. Sheet inventory

21 sheets. Excel caps sheet names at 31 characters; every name below is within that.

### Orientation

| Sheet | Contents |
|---|---|
| `00_README` | What the file is, the Dryad DOI, the SRA accession once minted, units, missing-value convention, and one row per sheet describing it. |
| `01_figure_index` | One row per display item (Figs. 1–6, ED 1–8, Supp. 1–46), naming the sheet(s) that carry its source data, or recording that it is composition data on Dryad, an illustration, or not covered. This is the sheet a referee actually navigates by. |

### Measured phenotype — the true source data

| Sheet | Contents | Working-tree source | Serves |
|---|---|---|---|
| `02_isolates` | The 54 isolates: index, phylum/family/genus, environmental source, and a flag for the 12 used in the invasion panel | taxonomy assignment; `SEQanalysis/` | ED Fig. 1, Supp. Fig. 1 |
| `03_monoculture_growth` | Per isolate × medium: OD600 and day-7 growth rate | `ExperimentalResult/Data/2208_Coalescence_processed/Isolates/{L,M,H}N_ISO_GR.xlsx` | Supp. Fig. 33 |
| `04_monoculture_pH` | Per isolate: endpoint monoculture pH, and the acidifier/alkalinizer class derived from it | `.../pH_isolates/` | Supp. Figs. 17, 18 |
| `05_community_OD_pH` | Per sample × cycle 1–7: OD600, pH, plus the three growth-curve fields | `Postprocessed/Metadata.xlsx` (`fieldOD1-7`, `fieldPH1-7`, `fieldGC1-3`; 588 rows, OD complete, pH 581–582 of 588) | Supp. Figs. 14, 15, 45, 46; ED Fig. 8; Fig. 5b |
| `06_invasion_counts` | Long format, one row per (medium, replicate, resident, invader): raw CFU counts both directions | `PairwiseColonyCountings_processed_230915.xlsx` sheets `LN_1/LN_2/MN_1/MN_2/HN_1/HN_2` (12×12 each) | Supp. Figs. 7–9 |
| `07_invasion_mono` | Monoculture CFU controls per isolate × medium × replicate | same file, sheets `LN_mono/MN_mono/HN_mono` | invasion normalisation |
| `08_invasion_outcomes` | Per pair × medium: classified outcome (coexistence / exclusion / bistability), failed-invasion flag | same file, sheets `LN/MN/HN` (the human-readable "N win" calls) | **Fig. 4b**, **Fig. 5c**, Supp. Figs. 7–9 |

The three `LN/MN/HN` sheets in the working file mix a text call ("3 win", "82-0.5") with a numeric
block in the same sheet. These need parsing into a clean two-column result, not copying verbatim.

### Derived per-event scalars

| Sheet | Contents | Source | Serves |
|---|---|---|---|
| `09_events_synthetic` | One row per synthetic coalescence event: sample ID, the two parent IDs, medium, replicate, richness class, retention `r`, PDI, outcome class, ASV-overlap counts | `Analyzed/processed_CoalescenceEvent_synthetic.xlsx` (282 rows) recomputed through `coalescence.decomposition`, not the precomputed `Similarity*` columns | Fig. 1e, Fig. 4c/d, Supp. Figs. 10–12, 27–29, 34, 37, 44 |
| `10_events_natural` | Same, natural communities | `processed_CoalescenceEvent_natural.xlsx` | Fig. 6b/c, Supp. Fig. 35 |
| `11_diversity` | Per community: richness and diversity at the five abundance thresholds | `processed_Communities_synthetic.xlsx` / `_natural.xlsx` (462 rows, `DiversityR/SN/SS_1..5`) | Supp. Fig. 22 |
| `12_metric_sensitivity` | Outcome distribution under Bray-Curtis, Jaccard, Jensen-Shannon and inner product | the `Assymetricity_{BC,J,JS,DP}_*` columns | ED Fig. 2 |
| `13_additive_null` | Event-matched additive null model results | `extended_supplementary/base_raw_count_additive_null_events.csv` | ED Fig. 3, Supp. Figs. 38, 44 |
| `14_selection_correlation` | Experimental pairwise selection correlation per medium | derived | ED Fig. 7, Fig. 2d (experimental half) |

`09` and `10` are the workhorses — between them they carry the plotted quantity for six main
panels and roughly fifteen supplementary figures. Recompute rather than lift the precomputed
columns: `data/README.md` states the figures deliberately ignore those and rederive from the
composition vectors, and the two disagree wherever parents share species.

Apply `coalescence.io.EXCLUDED_SAMPLES` (22 quality-control wells) and carry an `excluded`
boolean rather than silently dropping rows, so the published *n* is reconstructable either way.

### Simulation

Regenerable from seeded code, so these carry **plotted summary values, not raw dumps**.

| Sheet | Contents | Serves |
|---|---|---|
| `15_sim_events` | Simulated events at the representative μ: coordinates, PDI, outcome class | Fig. 2b, ED Fig. 5 |
| `16_sim_outcome_vs_mu` | Outcome fractions across μ = 0 to 1.2 | Fig. 3a/b, Supp. Fig. 13 |
| `17_sim_interaction` | Interaction coefficients before and after assembly, paired | Fig. 2c, Supp. Figs. 3, 32 |
| `18_sim_selcorr_vs_mu` | Pairwise selection correlation against μ | Fig. 2d, ED Fig. 6, Supp. Fig. 36 |
| `19_sim_sensitivity` | Alternative-ensemble sweeps: Gaussian/Gamma coefficients, growth-rate and carrying-capacity heterogeneity, mixed-sign and mutualistic-pair variants, pH-feedback model | Supp. Figs. 4, 5, 6, 39–43 |
| `20_sim_assembly_effect` | Coalescence versus direct-assembly comparison | ED Fig. 4, Supp. Fig. 23 |

---

## 3. Gaps — resolve before building

1. **Time-series composition (Fig. 1d, Supp. Figs. 2, 30, 31).** `Metadata.xlsx` carries
   `Timepoint == 'F'` for all 588 rows, and `fig1/README.md` states plainly that the per-cycle
   sequencing is not in the archive. The published panels exist, so the per-cycle data existed at
   some point. Either locate it or record these panels as not covered. This is composition data
   and so would go to Dryad, not this workbook, but the index sheet has to say which.
2. **ED Fig. 5 panel f.** Tracker ED-11 records that no plotting script survives in the tree, the
   archive or the public repo. If the script is gone the underlying numbers may be too.
3. **Supp. Fig. 1, the phylogenetic tree.** Not tabular. Deliver the alignment and Newick file to
   Dryad and cross-reference from `01_figure_index`; do not force it into a sheet.
4. **Isolate taxonomy for `02_isolates`.** ED Fig. 1 is a rendered table; I have not yet found the
   table that generated it as data. Needs locating or reconstructing from the SILVA assignment.
5. **Simulation sheets are the largest build cost.** Six sheets spanning ~20 supplementary
   figures, and the sweeps have to be re-run to export their plotted values. If effort needs
   cutting, cut here first and cite the seeded code instead — that argument does not work for
   Tiers above, where no code can regenerate a colony count.

---

## 4. Conventions

- One row per observation, long format, no merged cells, no colour-as-data, no formulas.
- Every sheet repeats its key columns (`SampleIDX`, `Medium`, `Replicate`) rather than relying on
  position, so a sheet is meaningful pulled out on its own.
- `Medium` is written as the published labels `Nutr-` / `Base` / `Nutr+`, with the internal
  `L` / `M` / `H` kept in a second column so the sheets join back to the Dryad tables.
- Units in the header, in parentheses.
- Empty cell means not measured; never zero-fill.
- Panel letters lowercase, matching the captions.

## 5. Build order

1. Confirm the five gaps above.
2. Sheets `06`–`08` first — they are the ones that are nowhere else and they close ED-20.
3. Sheets `02`–`05`, straight extraction from the experimental tables.
4. Sheets `09`–`14`, generated through `coalescence.decomposition` so they match the figures.
5. Sheets `15`–`20`, re-running the sweeps.
6. `00_README` and `01_figure_index` last, once the sheet list is final.
7. Add the workbook to the Dryad deposit and to the Data Availability statement in **both** trees.
