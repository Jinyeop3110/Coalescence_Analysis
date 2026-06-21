# To Jiliang pH / Growth Export

Generated on 2026-05-17 with:

```bash
python To_Jiliang_20260517/make_to_jiliang_excel.py
```

Main output:

- `To_Jiliang_pH_growth_20260517.xlsx`

Data sources used:

- `Postprocessed/Metadata.xlsx`: community endpoint pH, OD, and growth-rate metrics from `ExperimentalResult/ExperimentalDataProcessing.m`.
- `Postprocessed/Metadata_Isolates.xlsx`: monoculture isolate growth-rate metrics and max growth-curve OD from `ExperimentalResult/IsolateExperimentalDataProcessing.m`.
- `ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/230623_pH.xlsx`: monoculture pH after 15 h.
- `ExperimentalResult/Data/2208_Coalescence_processed/pH_isolates/220910_54isolatesOD_flat100um.xlsx`: monoculture endpoint OD.

Workbook sheets:

- `sources`: provenance notes.
- `community_samples`: one row per community sample, with pH day 1-7, pH change, OD day 1-7, max endpoint OD, and growth-rate metrics.
- `community_summary`: grouped mean/std/median/count by origin, medium, and single vs coalesced community.
- `SC_vs_CC`: single-community vs coalesced-community mean differences by origin and medium.
- `monoculture_isolates`: isolate-level monoculture pH, OD, growth rates, and max growth-curve OD.
- `monoculture_summary`: isolate-level summary statistics.
