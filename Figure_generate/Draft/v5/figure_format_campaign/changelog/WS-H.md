# Workstream H — Extended Data panel sources

**Agent run:** 2026-08-01
**Scripts owned:**
- `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py` (ED 3)
- `Figure_generate/code/make_ed_fig5_combined.py` (ED 6 panel sources)
- `Figure_generate/code/plot_correlation_barplots_clean.py` (ED 7 panel sources)
- `Figure_generate/code/plot_ph_figures_revised.py` (ED 8 — must not regress Fig_S23)
- ED 1 source (traced, **blocked**, see below)

`rebuild_and_fit_a4.py` was **not** run (campaign rule 3). ED 6 and ED 7 composites are
still the old files on disk; they become compliant only after Wave 2 rebuilds them from
the panel sources fixed here.

## Fit factors (re-derived from `rebuild_and_fit_a4.py`, not taken on trust)

| ED | pipeline | placement scale | `fit()` scale | script pt -> composite native |
|---|---|---|---|---|
| 3 | `Fig_R3_2_...pdf` copied whole, then `fit()` | — | `180 / 180.22 = 0.9988` | x0.9988 |
| 6 | `build()` a–c in 53.33 mm cell, d in 92.40 mm box, then `fit()` | 0.8753 (a–c), 0.9593 (d) | 1.0000 (151.54 mm < 185 cap) | x0.8753 / x0.9593 |
| 7 | `build()` a–c in 53.33 mm cell, then `fit()` | 0.8510 | 1.0000 (71.04 mm < 185 cap) | x0.8510 |
| 8 | `Fig_S24_...pdf` copied whole, then `fit()` | — | 1.0000 (139.15 mm < 180 mm target) | x1.0000 |

Note: the audit's suggestion of **8.5 pt for the ED 7 panels is wrong** — 8.5 x 0.851 =
7.23 pt composite, over the 7.0 pt ceiling. The correct value is 7.6 pt (see below).

## Changes made

### ED_Fig3_combined.pdf (`Fig_R3_2_additive_null_comparison.pdf`)
- **Before:** in-SI 5.28–7.92 pt / standalone (native) 5.97–8.96 pt — FAIL, the 9 pt panel
  letters and heat-map counts exceed 7.0 pt native and the 6 pt legend is under 6.3 pt.
- **Lever:** (b) script fonts only.
- **Edits** — all inside the `fig_combined` block, three named constants introduced:
  - `analyze_additive_null.py:598-600` — added `ED_BODY_PT = 6.6`, `ED_SMALL_PT = 6.4`,
    `ED_LETTER_PT = 6.9` with a comment recording the fit factor.
  - `:677-683` — `fontsize=8` x3 -> `ED_BODY_PT`; `fontsize=5.8` (legend) -> `ED_SMALL_PT`;
    added `axc0.tick_params(labelsize=ED_BODY_PT)` (ticks previously inherited
    `rcParams["font.size"]=8`).
  - `:714-717` — `set_xticklabels` given `fontsize=ED_BODY_PT`; ylabel/title `8` ->
    `ED_BODY_PT`; added `axc1.tick_params(labelsize=ED_BODY_PT)`.
  - `:726-732` — annotation `fontsize=6` -> `ED_SMALL_PT`, and its text changed from
    `"Wilcoxon $p=5.9\times10^{-14}$"` to `"Wilcoxon $p$ = 5.9e-14"`. **Reason:** matplotlib
    renders a mathtext superscript at 0.7x the base size. At any legal ED base size
    (<= 7.0 pt) the exponent lands at <= 4.9 pt, under the 5 pt floor — this is the
    in-scope mathtext case named in CAMPAIGN.md section 1. Unicode superscripts were tried
    first and rejected: Arial has no U+207B/U+2074 and the fallback drew missing-glyph
    boxes (verified by rendering). The exact p value is typeset properly in the caption.
  - `:753` — heat-map `annot_kws={"size": 9}` -> `ED_LETTER_PT`.
  - `:757-761` — `set_xticklabels`/`set_yticklabels`/xlabel/ylabel/title `8` -> `ED_BODY_PT`.
  - `:769` — bold panel letters `fontsize=9` -> `ED_LETTER_PT`.
- **Regenerated:** yes —
  `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python Figure_revision/R3_1_additive_null/analyze_additive_null.py`
  (must be run from `code/`; `common_setup` uses relative data paths).
- **Synced:** yes — `latex/supplementary_figs/`, the SI submission tree's
  `supplementary_figs/`, and `ED_Fig3_combined.pdf` in all four ED dirs.
- **After:** native 180.22 x 74.05 mm. Script 6.40 / 6.60 / 6.90 pt ->
  **composite native 6.39 / 6.59 / 6.89 pt**. Verifier: `PASS` in-SI 5.65–6.10,
  `OK` standalone 6.40–6.90. Colour DeviceRGB.

### ED_Fig6_combined.pdf — panel sources `panel_sources/ED_Fig2{a,b,c,d}*.pdf`
- **Before:** in-SI 6.79–8.49 pt / standalone 7.68–9.60 pt — FAIL.
- **Lever:** (b) script fonts. Figure geometry left alone.
- **Edits** in `make_ed_fig5_combined.py`:
  - `:29-49` — `OUT_DIR` repointed from **`Draft/v4`** (deleted; the script could not run at
    all) to `Draft/v5`, and `ARCHIVE_DIR` from `archive/` to `panel_sources/`, which is
    where `rebuild_and_fit_a4.py` actually reads the panels from. Added
    `PANEL_ABC_PT = 7.4` and `PANEL_D_PT = 6.8` with the placement-factor derivation.
  - `:194,199,200,201` — panels a–c: stars `10`, xticklabels `10`, ylabel `10`,
    y `labelsize=9` -> `PANEL_ABC_PT`.
  - `:225,226,230,231` — panel d: xlabel `10`, ylabel `10`, `labelsize=9`,
    legend `fontsize=8` -> `PANEL_D_PT`.
  - `:288` — removed the trailing `combine_figure(...)` call and the
    `from combine_extended_figures import combine_figure` import. That call rasterised
    every panel to a 300 dpi JPEG (forbidden for line art) and wrote the
    pre-renumbering name `ED_Fig5_combined.pdf`. Composition is `rebuild_and_fit_a4.py`'s
    job. **This is a behaviour change beyond fonts** — flagged, see Side effects.
  - Per instruction, the missing `rcParams` (the reason ED 6 is Type 3) was left alone.
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python make_ed_fig5_combined.py`
- **Synced:** panel sources live only in `latex/figures/extended_data/panel_sources/`;
  the submission trees carry composites only, which Wave 2 distributes.
- **After (predicted, needs Wave 2):** panels a–c 60.93 mm wide -> x0.8753;
  panel d 96.32 mm -> x0.9593; composite 180.0 x 151.54 mm, `fit()` = 1.0000.
  Script 7.4 pt -> **6.48 pt composite native**; script 6.8 pt -> **6.52 pt**.
  Whole-figure span 6.48–6.52 pt. Colour DeviceRGB.

### ED_Fig7_combined.pdf — panel sources `panel_sources/ED_Fig3{a,b,c}*.pdf`
- **Before:** in-SI 6.81–8.32 pt / standalone 7.70–9.41 pt — FAIL.
- **Lever:** (b) script fonts. **No data filtering, sample selection or statistics touched.**
- **Edits** in `plot_correlation_barplots_clean.py`, all inside `plot_clean_barplots`:
  - `:133-138` — added `ED_PANEL_PT = 7.6` with the placement-factor derivation.
  - `:221` — significance stars `fontsize=9` -> `ED_PANEL_PT`.
  - `:223` — ylabel `fontsize=11` -> `ED_PANEL_PT`.
  - `:225` — xticklabels `fontsize=10` -> `ED_PANEL_PT`.
  - `:230` — y `labelsize=10` -> `ED_PANEL_PT`.
- **Regenerated:** yes. The permutation null in
  `analyze_pairwise_correlations_per_event` is **not seeded**, so the analysis was run
  exactly once and cached, and only the plotting was re-executed, via
  `/Users/jysong/miniforge3/bin/python <scratchpad>/run_ed7.py` (driver calls the module's
  own `load_all_coalescence_data`, `analyze_pairwise_correlations_per_event` and
  `plot_clean_barplots` unchanged). Equivalent to
  `cd Figure_generate/code && python plot_correlation_barplots_clean.py`.
- **Synced:** `correlation_barplot_{LN,MN,HN}.pdf` copied to
  `panel_sources/ED_Fig3{a,b,c}_correlation_{Nutr-,Base,Nutr+}.pdf`.
- **After (predicted, needs Wave 2):** panels 62.67 mm wide -> x0.8510; composite
  180.0 x 71.04 mm, `fit()` = 1.0000. Script 7.6 pt -> **6.47 pt composite native**
  (single tier). Colour DeviceRGB.

### ED_Fig8_combined.pdf (`Fig_S24_pH_diff_vs_outcome_Base_Nutr+.pdf`)
- **Before:** in-SI 7.80–11.69 pt / native 8/9/10/12 pt — FAIL, native span 1.50 > 1.4.
- **Lever:** (b) script fonts, applied **per call only**, never via `rcParams`, so that
  `Fig_S23_ASV_vs_pH_combined.pdf` (one of the two baseline passes, built by the same
  module from `from common_setup import *`) is untouched.
- **Edits** in `plot_ph_figures_revised.py`, all inside `plot_ph_diff_vs_outcome_two_panel`:
  - `:310-311` — added `ED_BODY_PT = 6.6`, `ED_TITLE_PT = 6.9` above the `plt.subplots` call.
  - `:338` — R²/p annotation `fontsize=10` -> `ED_BODY_PT`.
  - `:346-350` — xlabel and ylabel given explicit `fontsize=ED_BODY_PT` (they previously
    inherited `common_setup`'s `font.size=8`); added `ax.tick_params(labelsize=ED_BODY_PT)`
    for the same reason; panel title `fontsize=12` -> `ED_TITLE_PT`.
  - `:354-360` — "Acidic wins" / "Alkaline wins" / "n = N" `fontsize=9` -> `ED_BODY_PT`.
  - `figsize=(140*mm, 65*mm)` left unchanged.
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python plot_ph_figures_revised.py`
- **Synced:** yes — `latex/supplementary_figs/`, SI submission tree `supplementary_figs/`,
  and `ED_Fig8_combined.pdf` in all four ED dirs.
- **After:** native 139.15 x 64.43 mm, `fit()` = 1.0000, so script pt == composite native.
  **6.60 / 6.90 pt native**, span ratio 1.05. Verifier: `PASS` in-SI 6.42–6.71,
  `OK` standalone 6.60–6.90. Colour DeviceRGB.

### Fig_S23_ASV_vs_pH_combined.pdf — regression check
Re-verified after the `plot_ph_figures_revised.py` run:
`verify_figures.py Fig_S23` -> **5.06–6.33 pt, PASS, colour OK** — identical to baseline.
The regenerated file is byte-different (timestamp only) but has the same page size
(238.94 x 118.78 mm) and the same 8 / 9 / 10 pt tiers, so the deployed copies were
deliberately **left untouched**.

## Blocked / not fixed

### ED_Fig1_combined.pdf — cross-workstream, needs Workstream D
- Traced: `combine_extended_figures.py:207` copies
  `latex/supplementary_figs/taxonomy_color_map.pdf` verbatim to `ED_Fig1_combined.pdf`,
  and `rebuild_and_fit_a4.py` then scales it. Its only generator is
  **`Figure_generate/code/generate_fig1_1.py::plot_taxonomy_colormap()`** (function at
  `:220`, `figsize=(8, 15)` at `:258`, the single `fontsize=12` at `:269`, saved at `:283`)
  — a script owned by **Workstream D**, so campaign rule 2 forbids me editing it.
- Numbers for whoever fixes it: source PDF is 256.71 x 298.45 mm; `fit()` scale is
  `min(180/256.71, 210/298.45) = 0.7012`, width-limited, giving 12 x 0.7012 = 8.41 pt
  native (matches the baseline). A naive target is `6.5 / 0.7012 = 9.3 pt`, but the fit
  factor is **coupled** to the font size: the page is text-width dominated, so shrinking
  the type narrows the tight bbox and raises the fit factor. If it becomes height-limited
  the factor is capped at `210/298.45 = 0.7036`. Whoever changes it must regenerate and
  re-measure rather than trust the arithmetic — and should also check whether ED 1's
  reported column of >5,000 glyphs stays legible.
- ED 1 currently passes the in-SI measure (6.69 pt) and fails only standalone (8.41 pt).

### Panel letters on ED 5, 6, 7 — Workstream Z
`rebuild_and_fit_a4.py:63` sets `LABEL_PT = 8.0`. With `fit()` = 1.000 for ED 6 and ED 7
this puts the bold `a`/`b`/`c`/`d` at **8.00 pt native (7.08 pt in-SI)** — over the ceiling
and the only remaining violation in those two figures after this workstream's changes.
Already noted as systemic cause 4 in CAMPAIGN.md section 7; it is WS Z's line to change.
Setting `LABEL_PT = 6.8` would put them at 6.80 pt native / 6.01 pt in-SI.

## Side effects

1. **ED 3 content drift (pre-existing, now surfaced).** The deployed
   `Fig_R3_2_additive_null_comparison.pdf` was dated 2026-05-16 and predated a 2026-06-03
   edit to `analyze_additive_null.py`. Regenerating necessarily ships the newer labels:
   "Base medium similarity map" -> "Base raw-count similarity map"; "Paired PDI" ->
   "Paired asymmetry"; ylabel "PDI / asymmetry y" -> "asymmetry y = |2PDI−1|";
   "Raw-count null class" -> "Additive-null class"; "Experiment class" -> "Observed class";
   legend "raw-count null"/"experiment" -> "additive null"/"observed"; and a new
   "77/83 higher asymmetry / Wilcoxon p = 5.9e-14" annotation in panel b. The new wording
   matches the Extended Data Fig. 3 caption better than the old ("simple additive null
   model", "$|2\mathrm{PDI}-1|$"), so this looks like a sync that was simply never done —
   but it is a visible change and the author should eyeball it.
2. **ED 7 content drift (pre-existing, now surfaced).** Commit `f191430` (2026-06-21)
   changed `plot_correlation_barplots_clean.py` mean-marker `markersize` 12 -> 6 and the
   y-axis `MultipleLocator` 0.1 -> 0.2, but the deployed panels were never regenerated.
   The new panels therefore show smaller mean squares with visible error-bar caps and
   y ticks every 0.2. Scatter points, means and significance stars are unchanged
   (verified by rendering old vs new side by side).
3. **`make_ed_fig5_combined.py` no longer builds a composite.** See the ED 6 entry — the
   `combine_figure` call and its import were removed. Anyone who relied on this script
   emitting `ED_Fig5_combined.pdf` must now run `rebuild_and_fit_a4.py`.
4. **`correlation_summary_clean.csv` overwritten** at
   `code/Figure/AsymmetricityNullModelAnalysis/correlation_analysis/`. It is gitignored, so
   the previous copy is gone. Its `n_events` (90 / 88 / 87) and `Δ` (0.0164 / 0.2298 /
   0.1363) do **not** match the numbers in the ED Fig. 7 caption (n = 90 / 83 / 90,
   Δ = 0.016 / 0.235 / 0.141). This mismatch is **pre-existing and independent of this
   campaign** — I changed no filtering, selection or statistics, and none of these numbers
   are printed inside the figure — but it is the sample-size question flagged in my brief
   and it is unresolved.
5. Other outputs overwritten in place, none of them SI figures:
   `code/Figure_revision/R3_1_additive_null/fig1..fig9*.{pdf,png,svg}` and
   `base_raw_count_additive_null_events.csv` (script-local, not referenced by any `.tex`);
   `code/Figure/pH_Analysis/Fig_S23*` and `Fig_S24*`;
   `code/Figure/AsymmetricityNullModelAnalysis/correlation_analysis/correlation_barplot_*`.
6. No `.tex` width changes were needed or made by this workstream.
