# Workstream A — stacked-bar class-fraction figures

**Agent run:** 2026-08-01
**Scripts owned:** `Figure_generate/code/plot_stacked_bar_class_fractions.py`
**Figures:** Fig_S26 (SI) + panel sources for ED Fig. 2, ED Fig. 4, ED Fig. 5f

## Root cause removed

Every font size in the script was a hard-coded `base * 1.3` literal
(`10.4 # 8 * 1.3`, `14.3 # 11 * 1.3`, `15.6 # 12 * 1.3`, `16.9 # 13 * 1.3`, ...),
and y-tick labels were left at the `common_setup` rcParam default of 8 pt, so
each figure spanned 8.0-16.9 pt native — a ratio of 2.11, far outside the 1.4x
band. All literals are gone. Sizes now come from four named dicts at the top of
the file (`FS_S4`, `FS_S25`, `FS_S26`, `FS_S12`), each derived from the size the
figure is actually reproduced at, and y-tick sizes are now set explicitly with
`ax.tick_params(labelsize=...)` instead of inheriting the rcParam.

**In-figure titles were kept, not moved to the captions.** Harmonising the sizes
alone was sufficient to land every figure inside the band, so removing the titles
was not needed to pass. Doing it anyway would have meant editing captions in
`figures.tex` and `extended_data.tex` in both trees, which WS G is concurrently
editing for include widths, for no compliance gain. Nature's preference against
in-figure titles is real but is a house-style matter outside this campaign's
stated scope (text size + colour). Flagged for the author, not actioned.

## Changes made

### Fig_S26_assembly_effect_experimental_stacked_bar.pdf

- **Before:** print 4.92-10.38 pt (FAIL; native 8.0-16.9, span ratio 2.11, NOT
  rescalable at any include width)
- **Lever:** (b) script fonts only. No `.tex` change; still `width=0.7\textwidth`.
- **Edits:**
  - `plot_stacked_bar_class_fractions.py` — new `FS_S26 = dict(annot=7.1,
    tick=7.1, label=7.4, legend=7.1, title=7.7)`; `create_two_row_stacked_bar_plot`
    now takes a `fonts` dict instead of the `9.1 / 11.7 / 13 / 14.3 / 16.9`
    literals, and sets `ax.tick_params(axis='y', labelsize=...)`.
  - figsize unchanged at `(6, 6)`. The native canvas shrank 7.141 -> 5.229 in
    because the 16.9 pt suptitle was what forced the old width; `scale` rose
    0.6144 -> 0.8391 accordingly, which is why the native sizes needed are lower
    than the 8.14-11.39 pt window computed from the old canvas.
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python plot_stacked_bar_class_fractions.py`
- **Synced to submission tree:** yes
- **After:** print **5.96-6.46 pt (PASS)**, native span ratio 1.08, colour DeviceRGB OK.
  Verified with `verify_figures.py Fig_S26`.

### Fig_S4_robustness_metrics_stacked_bar.pdf -> ED_Fig2_combined.pdf

- **Before:** native 8.0-15.6 pt on a 202.1 mm canvas; ED2 composite 7.13-13.90 pt
  standalone (FAIL both measures).
- **Lever:** (b) script fonts + figsize.
- **Edits:**
  - `FS_S4 = dict(annot=6.5, tick=6.5, label=6.7, legend=6.5, title=6.8)`
  - call site figsize `(8, 5)` -> `(7.10, 4.46)`, so the native canvas is
    **179.5 mm**, just under the 180 mm two-column width. `rebuild_and_fit_a4.fit()`
    therefore leaves it at scale 1.000 and the native sizes *are* the standalone
    sizes — no fit-factor arithmetic to get wrong.
- **Regenerated:** yes. **Synced:** yes (SI copy + all four ED directories).
- **After:** standalone **6.50-6.80 pt (OK)**, in-SI at 0.9\textwidth
  **5.19-5.43 pt (PASS)** — dual-compliant.

### Fig_S25_assembly_effect_simulation_stacked_bar.pdf -> ED_Fig4_combined.pdf

- **Before:** native 8.0-16.9 pt on a 222.2 mm canvas; ED4 composite 6.48-13.69 pt
  standalone (FAIL both measures).
- **Lever:** (b) script fonts + figsize.
- **Edits:**
  - `FS_S25 = dict(annot=6.5, tick=6.5, label=6.7, legend=6.5, title=6.8)`
  - call site figsize `(10, 6)` -> `(8.11, 5.51)`. Needed two passes: with the
    smaller legend font the tight bbox first collapsed to 159.9 mm, which would
    have made ED4 a 160 mm figure; the second pass lands it at **180.2 mm**
    (fit factor 0.9988, i.e. effectively native).
- **Regenerated:** yes. **Synced:** yes (SI copy + all four ED directories).
- **After:** standalone **6.50-6.80 pt (OK)**, in-SI at 0.95\textwidth
  **5.45-5.71 pt (PASS)** — dual-compliant.

### Fig_S12_species_ablation_stacked_bar.pdf -> panel f of ED Fig. 5

- **Before:** native 7.8-14.3 pt on a 302.8 mm canvas. ED5 draws this panel
  168 mm wide, fit factor 0.5548, giving **3.83-7.01 pt in the SI** — five of the
  six size tiers illegal, and the worst text in ED5.
- **Lever:** (b) script fonts. **Canvas deliberately NOT shrunk** — see below.
- **Edits:**
  - `S12_FIT = 168.0 / 302.8`; `FS_S12` derives tick/label/legend/title as
    `6.5 / S12_FIT` and `6.6 / S12_FIT` -> 11.7 and 11.9 pt native, i.e. 6.49 and
    6.60 pt in the composite.
  - The legend was given compact geometry (`handlelength=1.2, handletextpad=0.4,
    labelspacing=0.3, borderpad=0.3, borderaxespad=0.3`) so that the larger font
    does not enlarge the legend box. The legend already overlapped two bar
    annotations in the μ=0.3 panel before this campaign; the footprint is now
    back to its original size, so the occlusion is unchanged, not worsened.
  - New `S12_SHOW_TOTALS` switch (default `True` = current behaviour) — see
    Blocked, below.
- **Regenerated:** yes. **Synced:** SI copy updated, and
  `latex/figures/extended_data/panel_sources/ED_Fig4f_species_ablation_bar.pdf`
  replaced.
- **After (panel source, native):** 7.8 pt annotations + **11.7 / 11.9 pt**
  everything else, canvas 303.0 x 100.8 mm (aspect unchanged, so ED5's composed
  height does not move). Predicted in the rebuilt ED5: **6.49 and 6.60 pt**, plus
  the 4.33 pt annotations that remain blocked.

## Blocked / not fixed

### ED Fig. 5 panel f — the per-bar `(count/total)` annotations

They stay at 7.8 pt native = **4.33 pt in the composite**, below the 5 pt floor.
This is geometric, not a font choice:

- ED5 draws panel f 168 mm = 476 pt wide over 18 bar positions, so the bar pitch
  is ~25 pt (measured in the current PDF: 43.5 pt at a 302.8 mm canvas).
- The widest annotation, `(1033/1200)`, measures 42.1 pt at 7.8 pt, i.e. **5.40 em**.
- Largest non-colliding size = 25 pt / 5.40 em = **~4.6 pt in the composite**,
  and this is scale-invariant: enlarging or shrinking the source canvas moves the
  fit factor by exactly the same ratio. Shrinking the canvas to the suggested
  6.6 x 2.2 in and setting 6.5 pt fonts produces heavy text overlap, not a fix.

So no canvas size or font size makes these annotations legal while the string
stays `(count/total)`. Two author decisions would resolve it, both one-line:

1. **Preferred — flip `S12_SHOW_TOTALS = False`** in the script. The annotation
   becomes `14%` over `164`, which is 1.67 em and fits comfortably; `FS_S12`
   then automatically sets the annotation to 11.7 pt native = 6.5 pt in the
   composite and panel f becomes fully compliant. No count is lost. The
   denominator is constant — n = 1200 community pairs for every bar except the
   two 24-species bars at μ=0.6 and μ=0.8, which are n = 1194 — so one sentence
   in the ED5 caption restores it exactly.
2. Split panel f into two rows of stacked bars in `rebuild_and_fit_a4.py`
   (WS Z's file, and a layout redesign — rule 9 says not to do this unasked).

Per CAMPAIGN rules 5 and 9 I did neither, and left the default at the existing
behaviour so the shipped figure is unchanged in content.

## Side effects

- The `latex/supplementary_figs/` copies of `Fig_S4_*`, `Fig_S12_*` and
  `Fig_S25_*` were **stale January builds** (legend read `CLS` / `Mixing`, x-axis
  read `Species per community`) and are not referenced by any `.tex` file. They
  have been refreshed along with everything else, so they now match the ED panel
  sources. No `.tex` reference changed. Only `Fig_S26` is actually included in
  the SI.
- `ED_Fig2_combined.pdf` and `ED_Fig4_combined.pdf` are single-panel copies —
  `combine_extended_figures.py` builds them with `copy_file()` from
  `archive/ED_Fig7_robustness_metrics.pdf` and `archive/ED_Fig5_assembly_effect_simulation.pdf`,
  **and that `archive/` directory no longer exists**, so neither script can
  regenerate them. I therefore wrote the regenerated figures straight into all
  four ED directories. Both are <= 180.2 mm wide, so `rebuild_and_fit_a4.fit()`
  is a no-op (scale 1.000 and 0.9988) and running it will not disturb them.
- `rebuild_and_fit_a4.py` was **not** run (rule 3). `ED_Fig5_combined.pdf` still
  contains the old panel f and must be rebuilt in Wave 2.
- SVG siblings in `Figure_generate/code/Figure/StackedBar_ClassFractions/` were
  rewritten by the same script run. They are not referenced by the SI.
- Original PDFs/SVGs backed up outside the repo before regenerating.

## For WS Z (Wave 2)

- ED2 and ED4 are already at their final size; `fit()` will report scale 1.000 /
  0.999 and change nothing.
- ED5 must be rebuilt to pick up the new panel f. Expected afterwards: panel f
  contributes **4.33 pt** (annotations, blocked) and **6.49 / 6.60 pt**
  (ticks, axis labels, legend, panel titles). The remaining ED5 failures are then
  panels a-e (not WS A) and the 8.0 pt `LABEL_PT` panel letters (WS Z).
