# Workstream F — rank-abundance, taxonomic distinctness, pool size

**Agent run:** 2026-08-01
**Scripts owned:**
- `Figure_generate/code/plot_rank_abundance_natural.py`
- `Figure_generate/code/SkewedDistributionTest/plot_rank_abundance_parental_vs_coalesced.py`
- `Figure_generate/code/Figure_revision/R2_5_natural_taxonomic_distinctness/analyze_natural_taxonomic_distinctness.py`
- `Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`

**Result: 7 of 8 figures now PASS text size. 8 of 8 PASS colour (all DeviceRGB).**
`natural_taxonomic_distinctness.pdf` is **blocked** — see below.

---

## Changes made

### rank_abundance_natural_Nutr-.pdf / rank_abundance_natural_Base.pdf / rank_abundance_natural_Nutr+.pdf

- **Before:** print 5.42-9.29 pt (FAIL — 10/11/12 pt tiers all above 7 pt)
- **Lever:** (b) script fonts only. LaTeX width left at `0.85\textwidth`; `figures.tex` untouched.
- **Edits** (`Figure_generate/code/plot_rank_abundance_natural.py`):
  - `:26` — `plt.rcParams['font.size'] = 10` -> `= 8` (drives tick labels)
  - `:205`, `:254` — Gini/richness annotation boxes `fontsize=9` -> `fontsize=8`
  - `:207-208`, `:256-257` — axis labels `fontsize=10` -> `fontsize=8`
  - `:209`, `:258` — panel titles `fontsize=11` -> `fontsize=8.5`
  - `:212`, `:261` — panel letters A/B `fontsize=12` -> `fontsize=8.5`
  - `:267` — suptitle `fontsize=12` -> `fontsize=8.5`
  - `:139` — **new helper `_set_plain_log_yticks()`**, called at `:214` and `:263`.
    Replaces the log y-axis `10^-4 … 10^0` mathtext labels with plain decimals
    (`0.0001 … 1`) and clears minor tick labels. **Rationale, important:** matplotlib
    renders a mathtext superscript at 0.7x the base size. The legal band is 5-7 pt,
    a ratio of exactly 1.4; the mathtext shrink is 1/0.7 = 1.43. A `10^x` tick label
    therefore can *never* have both its mantissa and its exponent inside the band at
    any font size or include width (mantissa <= 7 pt forces exponent <= 4.9 pt).
    This is the same class of fix other workstreams applied to `OD$_{600}$` /
    `$c_{max}$` subscripts. No numbers or data changed — only the tick label notation.
- **Regenerated:** yes —
  `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python plot_rank_abundance_natural.py`
- **Synced to submission tree:** yes (both `latex/supplementary_figs/` and
  `revision_submission/00_submit_new/.../supplementary_figs/`, byte-identical)
- **After:** print **6.11-6.51 pt** (PASS). Only two native tiers remain (8 and 8.5 pt),
  span ratio 1.06 — comfortably inside the 1.4x band, so this figure is insensitive
  to future `bbox_inches='tight'` drift.
- **Visual check:** rendered at 200 dpi, no label collisions; decimal y-tick labels fit
  without crowding the y-axis label.

### rank_abundance_parental_vs_coalesced_Base.pdf / _Nutr-.pdf / _Nutr+.pdf

- **Before:** print 5.40-9.26 pt (FAIL — 10/11/12 pt tiers above 7 pt; native span 1.71x)
- **Lever:** (b) script fonts only. Width kept at `0.85\textwidth` as instructed.
- **Edits** (`Figure_generate/code/SkewedDistributionTest/plot_rank_abundance_parental_vs_coalesced.py`):
  - `:31` — `plt.rcParams['font.size'] = 10` -> `= 8`
  - `:163`, `:205` — Gini annotation `fontsize=9` -> `fontsize=8`
  - `:165-166`, `:207-208` — axis labels `fontsize=10` -> `fontsize=8`
  - `:167`, `:209` — panel titles `fontsize=11` -> `fontsize=8.5`
  - `:170`, `:212` — panel letters `fontsize=12` -> `fontsize=8.5`
  - `:217` — suptitle `fontsize=12` -> `fontsize=8.5`
  - `:104` — same `_set_plain_log_yticks()` helper, called at `:172` and `:214`
    (same mathtext rationale as above; at `font.size=8` the exponents would have
    landed at 5.6 pt native = 4.28 pt print, below the floor)
  - `common_setup.py` was **not** touched (this script imports it).
- **Regenerated:** yes —
  `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python SkewedDistributionTest/plot_rank_abundance_parental_vs_coalesced.py`
  (must be run with cwd = `Figure_generate/code`; `common_setup.py` uses relative data paths)
  Script writes `Figure/SkewedDistributionTest/rank_abundance_parental_vs_coalesced_{L,M,H}.pdf`;
  SI filenames map L->Nutr-, M->Base, H->Nutr+.
- **Synced to submission tree:** yes (byte-identical in both trees)
- **After:** print **6.12-6.51 pt** (PASS), native span 1.06x.
- **Data unchanged:** regenerated Gini/n values reproduce the previous figure exactly
  (e.g. Base parental 0.62+/-0.18, n=30; coalesced 0.63+/-0.16, n=83).

### pool_size_analysis.pdf

- **Before:** print 3.82-6.11 pt (FAIL — 5 pt legends -> 3.82 pt, 6 pt legends -> 4.59 pt).
  Already at `\textwidth`, so no rescaling headroom; native span 1.60x.
- **Lever:** (b) script fonts, plus legend *geometry* tightening (see collision note)
- **Edits** (`Figure_generate/code/Figure_revision/R1_4_pool_size/analyze_pool_size.py`,
  main 2x3 figure only — lines ~473-698):
  - `:517`, `:562`, `:592` — legend `fontsize=6` -> `fontsize=7` (panels A, B, C)
  - `:519`, `:564`, `:594` — `title_fontsize=6` -> `title_fontsize=7`
  - `:627`, `:690` — legend `fontsize=5` -> `fontsize=7` (panels D, F)
  - `:656` — legend `fontsize=6` -> `fontsize=7` (panel E)
  - `:518`, `:563`, `:593`, `:628`, `:657`, `:691` — legend geometry tightened
    (`columnspacing` 0.5/0.6 -> 0.4, `handlelength` 1.0/1.2 -> 0.8,
    added `handletextpad=0.4`, `labelspacing` 0.2 -> 0.15 in D/F).
    **Why:** at 7 pt the panel F legend grew wide enough to sit on top of the
    `pool size = 4` data markers, and panel A's legend spilled toward panel B.
    Tightening the handle/column padding restores the original legend footprint.
    Verified by 500 dpi crop comparison against `backup_figs_20260801`.
  - Titles/ticks left at 8 pt (already 6.07 pt print).
- **Regenerated:** yes —
  `cd Figure_generate/code/Figure_revision/R1_4_pool_size && /Users/jysong/miniforge3/bin/python analyze_pool_size.py`
- **Synced to submission tree:** yes (byte-identical in both trees)
- **After:** print **5.31-6.07 pt** (PASS), native span 1.14x.
- **Visual check:** all six panels rendered and inspected; no text overlap. Panel A/B
  legend swatches still sit in front of the tallest whiskers, exactly as in the
  pre-campaign figure — unchanged, not a regression.

---

## Blocked / not fixed

### natural_taxonomic_distinctness.pdf — still FAIL (3.81-6.23 pt)

The 5.5 pt tier (138 chars: the `n=6` / `n=60` / `n=435` sample-size annotations above
panels **b** and **e**) **cannot be brought to 5 pt print without a layout change.**

Arithmetic:
- The figure is saved with no `bbox_inches='tight'`, so native size is exactly
  8.6 x 5.6 in and `scale = 0.95 * 451.28 / 619.2 = 0.6924` — deterministic.
- 5 pt print therefore needs **>= 7.22 pt native**.
- The three labels sit at adjacent categorical x positions, **0.18 in apart in native
  figure coordinates**. `n=435` in Arial is ~0.276 in wide at 7.5 pt. They overlap.
  Confirmed empirically: I set them to 7.5 pt, regenerated, and the 600 dpi crop shows
  `n=60` and `n=435` printing on top of each other (`n=60n=435`). That edit has been
  **reverted**; the shipped PDF keeps them at 5.5 pt.
- Changing the include width does **not** help: it scales text and spacing together, so
  the collision geometry is invariant. Changing `figsize` does not help either — a wider
  canvas lowers `scale`, which raises the required native size by the same factor.

**Decision needed from the author** (rule 9 — I did not redesign). Any one of these fixes it:
1. Move the sample sizes to the SI caption and delete the in-figure annotations
   (the values are identical across all three media — n=6 / n=60 / n=435 — so they are
   already redundant three times over in each of panels b and e).
2. Collapse the three labels into one per medium group, e.g. `n = 6 / 60 / 435` centred
   over each group. ~0.42 in wide at 7.5 pt against a 0.54 in group width — fits, and
   preserves the S / D / C reading order.
3. Rotate the labels 90 degrees and raise the panel `ylim` to ~1.15 to make headroom.

Changes to this script that **were** kept (safe, and they pre-position the figure to pass
the moment the n= labels are resolved):
- `:248` — `"font.size": 8` -> `8.5` (bulk text 5.54 -> **5.89 pt** print, more centred)
- `:403` — panel titles `fontsize=8.5` -> `9` (5.89 -> **6.23 pt** print)
- `:313`, `:360` — left at `fontsize=5.5` (**blocked tier**, 3.81 pt print)

Regenerated and synced anyway (`Fig_R2_5_natural_taxonomic_distinctness.pdf` ->
`natural_taxonomic_distinctness.pdf` in both trees), since every tier except the blocked
one is now compliant.

---

## Side effects

- `analyze_pool_size.py` regenerates all of its own outputs in
  `Figure_generate/code/Figure_revision/R1_4_pool_size/`:
  `pool_size_analysis.{svg,pdf,png}`, `pool_size_analysis_AB.{svg,pdf,png}`,
  `pool_size_by_medium.{svg,pdf,png}`. Expected. Only `pool_size_analysis.pdf` is an SI
  figure; the other two are response-letter exports and their **font sizes were left
  unchanged** (`:747-749`, `:792-794` at 6 pt; `:840` at 5.5 pt) so the response letter
  is not altered by this campaign.
- `analyze_natural_taxonomic_distinctness.py` also rewrites
  `natural_taxonomic_distinctness_summary.txt` and the `.png` next to it. Numbers unchanged.
- `plot_rank_abundance_natural.py` and `plot_rank_abundance_parental_vs_coalesced.py`
  also write `.svg` (and the latter a `.png`) siblings. Not used by the SI.
- No `.tex` file was modified by this workstream.
- `common_setup.py` was not modified.

## Verification

```
cd Figure_generate/Draft/v5
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py rank_abundance_natural
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py rank_abundance_parental_vs_coalesced
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py pool_size_analysis
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py natural_taxonomic_distinctness
```

| figure | mult | scale | print pt | size | colour |
|---|---|---|---|---|---|
| rank_abundance_natural_Nutr-.pdf | 0.85 | 0.764 | 6.11-6.50 | PASS | OK |
| rank_abundance_natural_Base.pdf | 0.85 | 0.765 | 6.12-6.51 | PASS | OK |
| rank_abundance_natural_Nutr+.pdf | 0.85 | 0.765 | 6.12-6.51 | PASS | OK |
| rank_abundance_parental_vs_coalesced_Base.pdf | 0.85 | 0.765 | 6.12-6.51 | PASS | OK |
| rank_abundance_parental_vs_coalesced_Nutr-.pdf | 0.85 | 0.765 | 6.12-6.51 | PASS | OK |
| rank_abundance_parental_vs_coalesced_Nutr+.pdf | 0.85 | 0.765 | 6.12-6.51 | PASS | OK |
| pool_size_analysis.pdf | 1.00 | 0.758 | 5.31-6.07 | PASS | OK |
| natural_taxonomic_distinctness.pdf | 0.95 | 0.692 | 3.81-6.23 | **FAIL** (blocked) | OK |
