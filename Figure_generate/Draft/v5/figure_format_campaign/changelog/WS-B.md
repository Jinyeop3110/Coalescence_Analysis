# Workstream B — Coalescence outcome matrices (pie-chart panels)

**Agent run:** 2026-08-01
**Scripts owned:** `Figure_generate/code/generate_pie_plots.py`
**Figures:** 9 × `latex/supplementary_figs/PieCharts/CoalescenceMatrices/coalescence_matrix_{Nutr-,Base,Nutr+}_s{6,12,24}.pdf`
(Supplementary Figs. 27-29, each panel included at `0.72\textwidth` = 114.6 mm)

## Approach

All nine panels shared one root cause: a canvas built at `(n1+n2+1)*1.2` inches
(17.9-23.5 in wide) that LaTeX then compressed to 114.6 mm, plus a 9 pt / 14 pt
font mixture whose 1.56x span exceeded the 1.4x legal band. Both had to change.

The script now (a) builds the panels on a compact canvas (`CELL_IN = 0.38` in per
matrix cell), and (b) uses **one harmonised font size for every label**, solved
for numerically just before saving so that the printed size lands on
`TARGET_PRINT_PT = 6.0`:

```
print_pt = native_pt * (SI_INCLUDE_MULT * SI_TEXTWIDTH_BP) / pdf_width_bp
```

Because `bbox_inches='tight'` makes the saved width depend on the font size (the
first and last column labels overhang the grid), the solver iterates
set-size → draw → measure `fig.get_tightbbox()` → recompute, converging in 3-4
passes. The header (suptitle, replicate labels, two-line column labels) and the
figure height are re-derived from the font size on every pass, so nothing
collides and the panel keeps the same printed footprint as before.

The resulting native sizes are figure-specific (9.4-9.9 pt for s6/s12,
13.1 pt for s24) — a single hard-coded value could not have served all nine.

## Changes made

### coalescence_matrix_{Nutr-,Base,Nutr+}_s6.pdf, _s12.pdf  (6 figures)
- **Before:** print 2.27-3.54 pt (s6/s12) and 2.40-3.73 pt (Base_s12) — FAIL,
  both TOO_SMALL and span ratio 1.56 > 1.4
- **Lever:** (b) generating-script geometry + font sizes. No LaTeX change.
- **Edits** (all in `Figure_generate/code/generate_pie_plots.py`):
  - `:23-47` — new module-level campaign constants: `SI_TEXTWIDTH_BP=451.28`,
    `SI_INCLUDE_MULT=0.72`, `TARGET_PRINT_PT=6.0`, `SAVE_PAD_IN=0.1`,
    `CELL_IN=0.38`, `GRID_W_FRAC=0.775`, `HEADER_FS=5.2`, `CELL_H_FRAC=0.90`
  - `:385-391` — `figsize=((n1+n2+1)*1.2, max(n1,n2)*1.2)` ->
    `figsize=((n1+n2+1)*CELL_IN/GRID_W_FRAC, max(n1,n2)*CELL_IN*CELL_H_FRAC)`;
    canvas 17.9x9.6 in -> 7.4x4.0 in (s6/s12), 23.5x12.7 -> 9.8x5.2 in (s24)
  - `:395-399` — `suptitle(..., fontsize=14)` -> `fontsize=fs`, `va='center'`,
    y-position re-derived from `fs` each pass
  - `:446-454` and `:505-513` — `set_ylabel(..., fontsize=9)` /
    `set_title(..., fontsize=9)` -> `fontsize=fs`, artists collected in
    `campaign_texts`
  - `:456-461` and `:515-520` — `fig.text(..., 'Replicate 1/2', fontsize=14)` ->
    `fontsize=fs`, `va='center'`, y re-derived from `fs`
  - `:521-551` — new iterative font-size solver + `fig.subplots_adjust` /
    `fig.set_size_inches` layout update, run immediately before `savefig`
- **Regenerated:** yes.
  ```
  cd Figure_generate/code
  /Users/jysong/miniforge3/bin/python - <<'EOF'
  import matplotlib; matplotlib.use("Agg")
  import generate_pie_plots as g
  colors, iso = g.get_taxonomic_colormap_and_sorting()
  cm = g.get_coalescence_matrix_data(g.Metadata, g.Coalescence_data)
  g.plot_coalescence_matrices(cm, colors, iso, "Figure/PieCharts/CoalescenceMatrices")
  EOF
  ```
  (`main()` was deliberately not called, so the unrelated Subcommunities pie
  charts that it also rewrites were left untouched.)
- **Synced to submission tree:** yes — `.pdf/.png/.svg` copied to both
  `latex/supplementary_figs/PieCharts/CoalescenceMatrices/` and
  `revision_submission/00_submit_new/Supplementary_Information_LaTeX_Source/supplementary_figs/PieCharts/CoalescenceMatrices/`
- **After:** print **6.00-6.01 pt (PASS)**, colour DeviceRGB (OK), single font
  size throughout (span ratio 1.00)
- **Collision check:** rendered at print size and inspected. Adjacent column
  labels (`P1-01`, ...) clear each other by **+0.28 mm** (s6/s12) and
  **+0.62 mm** (Base_s12); title/replicate/label rows clear vertically by
  +0.40 / +1.37 mm. Tight but legible and non-overlapping.
- **Printed footprint:** 114.6 x 61.3 mm (was 114.6 x 61.6 mm) and
  114.6 x 64.0 mm for Base_s12 (was 64.9 mm) — every panel is now marginally
  *shorter* than the version it replaces, so Supplementary Figs. 27-29 cannot
  overflow the page as a result of this change.

## Blocked / not fixed

### coalescence_matrix_{Nutr-,Base,Nutr+}_s24.pdf  (3 figures)
**Still the baseline files: print 1.73-2.69 pt, FAIL.** Deliberately not replaced.

These are 12x12 + 12x12 matrices: 24 label columns across a 114.6 mm panel gives
a **4.4 mm column pitch**, while the sample-ID labels (`P2-52`, five glyphs of
Arial) are **5.7 mm wide at 6 pt** and 5.2 mm wide even at the 5.0 pt floor. The
script change does make them compliant (verified: 6.00 pt, one font size), but
the labels then **overlap by 1.2 mm — about 22% of each label**, rendering the
header an illegible run-on string (`P1-5D2-5D2-5P2-5...`). Per CAMPAIGN.md rule 9
this is a layout problem, not a font problem, so the panels were left alone and
the compliant-but-overlapping output was not shipped.

**Decision needed from the author.** The geometry is unambiguous: at 6 pt the s24
matrices need at least **0.95\textwidth (151.2 mm)** to keep the labels apart.
Measured candidates (all three media, generated with `SI_INCLUDE_MULT = 0.95`)
are parked at
`figure_format_campaign/WS-B_blocked_s24_candidates_0.95tw/` —
they print at 151.2 x 77.8 mm, 6.00 pt, minimum label gap **+0.25 mm**
(the same margin the accepted s6/s12 panels have). Measured alternatives:
0.85\textwidth still overlaps (-0.39 mm); 1.0\textwidth gives +0.56 mm.

The catch is vertical space. Dropping a 77.8 mm s24 panel into the existing
three-panel figure gives 61.3 + 61.3 + 77.8 = 200.4 mm of artwork; with the
`0.5cm` gaps, three sub-captions and the main caption that is ~249 mm against a
246 mm `\textheight`, i.e. a marginal overflow. Shrinking the s6/s12 panels to
compensate is not available — at 6 pt they already overlap below ~0.69\textwidth.

So the realistic options are:
1. **(recommended)** Promote each s24 matrix to its own single-panel
   supplementary figure at `0.95\textwidth`-`\textwidth`, leaving Supplementary
   Figs. 27-29 with the s6 and s12 panels. Copy in the parked candidates
   (regenerate at `\textwidth` if 1.0 is chosen: set `SI_INCLUDE_MULT = 1.0`).
2. Keep the three-panel layout, raise only the s24 sub-figure to
   `0.95\textwidth`, and buy the ~3 mm by trimming the caption or the two
   `\vspace{0.5cm}` gaps.
3. Accept the s24 panels as a documented exception to the 5 pt rule.

Whichever is chosen, the `.tex` width must be edited in **both**
`latex/supplementary_sections/figures.tex` (lines 303, 328, 353) and the matching
`Supplementary_Information_LaTeX_Source/supplementary_sections/figures.tex`, and
`SI_INCLUDE_MULT` in `generate_pie_plots.py` must be set to the same value before
regenerating (it is a per-figure constant today; if the s6/s12 and s24 panels end
up at different widths it needs to become a per-`species_pool` lookup).

## Side effects

- **Row/column ordering of the matrices changes on every regeneration.**
  `Community_PermutateList()` in `common_setup.py:169-171` ends with
  `list(set(O) - set(exception_list))`; Python randomises string hashing per
  process, so the order of the parental samples along both axes is
  nondeterministic. The regenerated s6/s12 panels therefore show the same pies
  with the rows/columns permuted relative to the previously shipped files. The
  figure remains internally consistent (labels move with their pies) and no
  caption or body text refers to a specific cell, so this is cosmetic — but
  **any workstream regenerating a figure that uses `Community_PermutateList`
  will see the same reshuffle**, and exporting `PYTHONHASHSEED=0` before running
  would at least make it reproducible. Not fixed here: `common_setup.py` is
  off-limits (rule 1).
- `Figure_generate/code/Figure/PieCharts/CoalescenceMatrices/` (the script's own
  output directory, not a shipped tree) now also holds the compliant-but-
  overlapping `_s24` renders from the last run. The shipped trees still carry the
  original s24 files.
- No `.tex` file was modified. `common_setup.py` was not touched.
- Nothing outside the coalescence matrices was regenerated (the subcommunity pie
  charts produced by the same script were not rerun).
