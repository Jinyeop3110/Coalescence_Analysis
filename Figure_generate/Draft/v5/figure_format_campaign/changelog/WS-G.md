# Workstream G — LaTeX-width fixes + small single-figure script fixes

**Agent run:** 2026-08-01
**Scripts owned:** `plot_assembly_effect_mean_interaction.py`, `plot_monoculture_od_growth_histograms.py`,
`plot_overlap_fraction_histogram.py`, `plot_overlap_fraction_histogram_natural.py`,
`SkewedDistributionTest/plot_single_comparison.py`,
`.../P3_reanalysis/R1_2_pH_dominance/make_response_figure.py`,
`public_code_repo/pipeline/04_figure_generation/supplementary/generate_figure.py`
plus LaTeX-width-only edits in `supplementary_sections/figures.tex` (both trees).

**Result: 12 of 15 figures PASS. 3 blocked** — all three for the same structural reason
(see "The mathtext wall" below). Colour: 15/15 DeviceRGB, unchanged.

---

## !! Two campaign-level findings, read these first

### (1) The mathtext wall — mathtext sub/superscripts are *provably* incompatible with the 5–7 pt band

Matplotlib renders a mathtext sub/superscript at exactly **0.7x** its own label's base size.
Both sizes appear in the same PDF, so for a label of native size `X` at scale `s`:

```
subscript print = 0.7 * X * s  >= 5.0   ->   X*s >= 7.143
base      print =       X * s  <= 7.0
```

These cannot both hold. The internal span of any single mathtext-bearing label is
**1/0.7 = 1.4286 > 1.40**, regardless of include width, figsize, or how the *other* font
tiers are harmonised. No combination of the campaign's two levers can fix it.

This is not specific to WS G. The baseline shows the same 4.9 pt / 4.55 pt `600`, `2`, `+`
tiers in `Fig_R1_1A_winner_loser_OD.pdf`, `Fig_R1_1C_pairwise_corr_vs_OD.pdf` and others.
**Any figure whose verifier output shows a "too small" tier equal to 0.7x one of its other
tiers is in this category and is unfixable as scoped.**

### (2) The prescribed Unicode workaround silently deletes glyphs under `font.family = 'Arial'`

The campaign brief prescribed replacing mathtext with literal Unicode
(`Growth Rate (h$^{-1}$)` -> `Growth Rate (h⁻¹)`; `OD$_{600}$` -> `OD₆₀₀`).
I applied it, and it *does* make the verifier pass — **because the glyphs disappear.**

Arial has no U+207B (superscript minus) and no subscript digits U+2080–U+2089.
Matplotlib emits `UserWarning: Glyph 8315 ... missing from font(s) Arial` and writes a
`.notdef` box. Extracted text after the "fix" was literally `'Growth Rate (h'` — the
exponent was gone from the axis label. That is a silent content regression, strictly worse
than an undersized exponent, so **I reverted both Unicode edits** and both scripts are back
to byte-identical originals (confirmed clean in `git status`).

**The one thing that does work** (tested, `mpl 3.10.5`): a font *fallback list*

```python
rcParams['font.family'] = ['Arial', 'DejaVu Sans']   # a LIST, not 'sans-serif'
```

Verified: Arial stays primary for every glyph it has; only U+207B / U+2080–9 come from
DejaVu, and both fonts embed correctly. Setting `font.sans-serif = ['Arial','DejaVu Sans']`
with `font.family='sans-serif'` does **not** work — no fallback occurs, glyphs still tofu.

This introduces **no new typeface** relative to baseline: those figures already embed
DejaVuSans today, because that is exactly what mathtext falls back to (see the baseline
`fonts:` lines for `monoculture_od_growth_histograms.pdf` and `Fig_R1_1B_OD_vs_PDI.pdf`).

I did **not** apply it, because CAMPAIGN §1 puts typeface family out of scope and my brief
explicitly forbade font-family edits. **This is the decision the coordinator/author needs to
make**, and it unblocks all three of my blocked figures plus several in other workstreams.

---

## Changes made

### Part 1 — LaTeX width only (no regeneration)

Applied identically to `latex/supplementary_sections/figures.tex` **and**
`revision_submission/00_submit_new/Supplementary_Information_LaTeX_Source/supplementary_sections/figures.tex`
(line numbers are identical in both files; verified `includegraphics` lines now match exactly).

#### Fig_phase_diagram_ablation_{growth_std01,growth_std02,k_std01,k_std02,gaussian,gamma}.pdf
- **Before:** print 10.48 pt flat (FAIL, too large; `width=\textwidth` inside a `0.48\textwidth` subfigure)
- **Lever:** (a) LaTeX width
- **Edits:** `figures.tex:52,57,68,73,84,89` — `width=\textwidth` -> `width=0.62\textwidth`
  (effective multiplier 0.48 x 0.62 = 0.298)
- **Regenerated:** no. `common_setup.py` untouched, as instructed.
- **Synced to submission tree:** yes
- **After:** print **6.50 pt** flat (PASS) x6

#### two_panel_ph_asv_figure.pdf
- **Before:** print 6.35–8.17 pt (FAIL, 8.0 and 9.0 pt tiers too large)
- **Lever:** (a) LaTeX width
- **Edits:** `figures.tex:192` — `width=0.9\textwidth` -> `width=0.75\textwidth`
- **Regenerated:** no
- **Synced to submission tree:** yes
- **After:** print **5.29–6.81 pt** (PASS)

### Part 2 — script fixes

#### overlap_fraction_histogram.pdf
- **Before:** print 4.51–6.01 pt (FAIL, 9 pt tier -> 4.51)
- **Lever:** (b) script fonts
- **Edits:**
  - `code/plot_overlap_fraction_histogram.py:33` — `rcParams['legend.fontsize'] = 9` -> `10`
  - `code/plot_overlap_fraction_histogram.py:96` — Mean/Std `ax.text(..., fontsize=9)` -> `fontsize=10`
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python plot_overlap_fraction_histogram.py`
- **Synced to submission tree:** yes
- **After:** print **5.01–6.01 pt** (PASS)

#### overlap_fraction_histogram_natural.pdf
- **Before:** print 4.51–6.01 pt (FAIL, same cause)
- **Lever:** (b) script fonts
- **Edits:**
  - `code/plot_overlap_fraction_histogram_natural.py:27` — `rcParams['legend.fontsize'] = 9` -> `10`
  - `code/plot_overlap_fraction_histogram_natural.py:89` — `ax.text(..., fontsize=9)` -> `fontsize=10`
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python plot_overlap_fraction_histogram_natural.py`
- **Synced to submission tree:** yes
- **After:** print **5.01–6.01 pt** (PASS)

#### Assembly_effect_scatter_combined.pdf
- **Before:** print 10.05–15.64 pt (FAIL, native 9/12/14, span ratio 1.56 — not rescalable)
- **Lever:** (b) script fonts; include width deliberately kept at `0.6\textwidth`
- **Edits:** `code/plot_assembly_effect_mean_interaction.py`
  - `:23` `font.size` 12 -> **5.5**
  - `:24` `axes.labelsize` 14 -> **6.2**
  - `:25` `axes.titlesize` 14 -> **6.2**
  - `:26,:27` `xtick.labelsize` / `ytick.labelsize` 12 -> **5.5**
  - `:28` `legend.fontsize` 11 -> **5.5**
  - `:332,:333` `set_xlabel/set_ylabel(..., fontsize=14)` -> `fontsize=6.2`
  - `:334` `ax.legend(..., fontsize=9)` -> `fontsize=5.5`
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python plot_assembly_effect_mean_interaction.py`
- **Synced to submission tree:** yes
- **After:** print **5.80–6.54 pt** (PASS). Native canvas shrank 3.366 -> 3.566 in, so the
  realised scale is 1.054 (not the predicted 1.117) — the result still lands mid-band.

#### skewness_null_comparison.pdf
- **Before:** print 11.52–12.80 pt (FAIL, a 2.69 in figure blown up at scale 1.28)
- **Lever:** both
- **Edits:**
  - `code/SkewedDistributionTest/plot_single_comparison.py:35` — `font.size` 10 -> **6.0**
  - `:125, :131, :135, :139` — all four `fontsize=9` -> **`fontsize=7.0`**
  - `figures.tex:497` — `width=0.55\textwidth` -> `width=0.42\textwidth`
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python SkewedDistributionTest/plot_single_comparison.py`
  (must run from `code/`, not from the script's own directory — `common_setup` uses
  `../../Analyzed/...` relative paths and fails otherwise)
- **Statistical side effect:** this script has no plot-only mode; it re-runs the 500-permutation
  null models. It is seeded (`np.random.seed(42)`), and the regenerated
  `skewness_null_comparison_synthetic_base_summary.csv` is **byte-identical** to the previous
  one (diff clean). Reported stats unchanged: Exp mean 0.812 (n=83); vs abundance-weighted
  U=32188, p=7.93e-16; vs shuffled U=32050, p=1.85e-15. No scientific content changed.
- **Note:** the script writes `skewness_null_comparison_synthetic_base.pdf`; it was copied to
  the SI filename `skewness_null_comparison.pdf` in both trees.
- **Synced to submission tree:** yes
- **After:** print **5.61–6.54 pt** (PASS)

#### Fig_R1_2_acidalk_per_medium.pdf
- **Before:** print 6.01–8.84 pt (FAIL, 8 pt and 10 pt tiers too large)
- **Lever:** (b) script fonts
- **Edits:** `Draft/v5/latex/revision_first_round/point_by_point/P3_reanalysis/R1_2_pH_dominance/make_response_figure.py`
  - `:62` — `"font.size": 8` -> `7.0`
  - `:118` — `ax.set_title(medium, ..., fontsize=10)` -> `fontsize=7.5`
  - `:178` — `ax.set_title("Acid-Alk pairs only", fontsize=10)` -> `fontsize=7.5`
  - `"font.family": "DejaVu Sans"` at `:63` left untouched, as instructed.
- **Regenerated:** yes — `cd .../R1_2_pH_dominance && /Users/jysong/miniforge3/bin/python make_response_figure.py`
- **Synced to submission tree:** yes (the script itself writes to
  `latex/revision/revision_figure_folder/` and `latex/supplementary_figs/`; I copied to the
  submission tree manually)
- **After:** print **6.05–6.67 pt** (PASS)
- **Caution:** this script is **untracked in git** (`?? make_response_figure.py`), so unlike
  the other scripts I edited it has no git recovery path.

---

## Blocked / not fixed

All three are blocked by **the mathtext wall** (finding 1). Each is one `rcParams` line away
from passing *if* finding 2's font-fallback is approved; none is fixable without it.

### Fig_R1_1B_OD_vs_PDI.pdf — **plus a stale-artwork finding, see below**
- **State:** print **4.91–7.01 pt** (FAIL). Only the three `600` subscript characters fail,
  by 0.09 pt. The 8.0 pt tier at 7.01 is inside the verifier's 0.05 tolerance.
- **Blocking tier:** native 5.6 pt = 0.7 x 8.0 pt, the mathtext subscript of
  `ax.set_xlabel(r"Endpoint OD$_{600}$")` (`generate_figure.py:144`).
- Native span 8.0/5.6 = 1.4286. I searched the width space exhaustively: satisfying the
  5 pt floor needs scale >= 0.8839 and the 7 pt ceiling needs scale <= 0.8813. **Empty by
  0.003.** `0.83\textwidth` is the minimum-damage point (3 characters short by 0.09 pt);
  `0.85` flips it to 29 characters over by 0.18 pt.
- **Fix if approved:** add `'DejaVu Sans'` to the family list in
  `public_code_repo/pipeline/04_figure_generation/_common.py:use_paper_style()` and change
  the xlabel to `"Endpoint OD₆₀₀"`. That removes the 5.6 tier entirely, leaving
  {6.5, 7.0, 8.0}, span 1.23, and `0.80–0.83\textwidth` then gives ~5.5–6.8 pt. Note
  `_common.py` is shared with other public_code_repo panels — coordinator call, not mine.

- **STALENESS FINDING (actioned):** the shipped SI PDF **did not match its own generating
  script**. Shipped: 6.032 x 3.256 in, Type 3 DejaVu, tiers {4.9, 6.5, 7.0}. Script output:
  5.934 x 3.215 in, Type0 Arial, tiers {5.6, 6.5, 7.0, 8.0}. I regenerated
  (`cd Draft/v5/public_code_repo && python pipeline/04_figure_generation/supplementary/generate_figure.py`)
  and installed `panels/supp_fig14_od_vs_ph.pdf` as `Fig_R1_1B_OD_vs_PDI.pdf` in **both**
  trees, and set the include to `width=0.83\textwidth` (`figures.tex:162`). The SI now shows
  the figure its published code actually produces. Reported Spearman values in the
  regenerated panel: Nutr- rho=-0.243 p=0.021; Base rho=-0.144 p=0.193; Nutr+ rho=-0.600
  p=3.96e-10 (top row) — worth a glance against the SI caption text.
  As expected the fonts changed from Type 3 DejaVu to Type0 Arial; no Type-3-motivated edits
  were made by me. **`latex/supplementary_figs/Fig_R1_1B_OD_vs_PDI.svg` is now stale** —
  the script only emits `.pdf`. It is not referenced by the LaTeX.

### monoculture_od_growth_histograms.pdf
- **State:** print **4.38–6.83 pt** (FAIL). Exactly one character fails: the `1` of the
  `h$^{-1}$` superscript in `Growth Rate (h$^{-1}$)` (`:241` and `:257`), native
  7.7 = 0.7 x 11. Every other tier (9/10/11/12) already prints 5.12–6.83, in band.
- The brief's Unicode fix was applied, verified to pass, then **reverted** — it deleted the
  exponent glyph (finding 2). Script is back to its original tracked state.
- Width is not a lever: native span 12/7.7 = 1.56.
- **Fix if approved:** family fallback list + `'Growth Rate (h⁻¹)'`. That leaves tiers
  9–12 (span 1.33) at the current `0.9\textwidth`, i.e. 5.12–6.83 pt = PASS with no other edit.

### Fig_R1_3_per_medium_scatter.pdf
- **Before:** print 5.41–9.51 pt at `\textwidth` (FAIL, 245 characters too large)
- **Now:** print **3.79–6.66 pt** at `0.70\textwidth` (still FAIL, but 13 characters out of
  band instead of 245). I kept the width change — it is the correct final width once the
  mathtext is removed, and it is a strict improvement in the meantime.
- **The brief's arithmetic for this figure was wrong.** It gave "native span 1.23, pure
  one-lever fix, result 5.41–6.66". The 5.41 in the baseline is the *print* size of a
  4.55 pt native tier; shrinking the include scales that tier too, down to 3.79. Real native
  span is 8.0/4.55 = **1.76**, so no width works.
- **Blocking tiers:** native 4.55 = 0.7 x 6.5 and 4.90 = 0.7 x 7.0 — the superscripts in
  `$R^2$`, `$\rho_S$` and `Nutr$^+$`.
- **Script is `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
  (lines 721, 762–763, 767) — it is assigned to NO workstream in CAMPAIGN §6.** I did not
  edit it: my brief scoped this figure as LaTeX-width-only, and it is a 1025-line analysis
  script that also emits `Fig_R1_3ab_PDI_comparison`, `Fig_R1_3c_VD_reclassification`,
  `Fig_R1_3d_R2_comparison`, `Fig_R1_3_topK_sensitivity` and a bar figure. It needs an owner.
- **Fix if approved:** family fallback list + `R²` / `ρ_S` / `Nutr⁺` as literal text, then
  `0.70\textwidth` gives 5.41–6.66 pt exactly as the brief predicted.

---

## Side effects

- `Figure_generate/code/Figure/Overlap_Fraction/overlap_fraction_barplot.{pdf,png,svg}` was
  rewritten by `plot_overlap_fraction_histogram.py`. **Not referenced by the SI** (confirmed:
  no `overlap_fraction_barplot` in either `figures.tex`), so harmless.
- `.svg` and `.png` siblings of every regenerated figure were rewritten in the `code/Figure/`
  working directories. None of them is included by the LaTeX.
- `plot_assembly_effect_mean_interaction.py` resolves its input relative to `code/` but its
  output relative to the repo root, so running it from `code/` creates a nested
  `code/Figure_generate/code/Figure/...` path. I collected the PDF from there and **removed
  the stray nested `Figure_generate/` directory** under `code/`. The canonical
  `code/Figure/Assembly_effect_simulation/*.pdf` was therefore NOT refreshed — only the two
  SI trees hold the new version. Pre-existing path bug, not introduced here.
- `Figure_generate/code/Figure/SkewedDistributionTest/skewness_null_comparison_synthetic_base_summary.csv`
  rewritten, byte-identical.
- `Draft/v5/latex/revision/revision_figure_folder/Fig_R1_2_acidalk_per_medium.pdf` rewritten
  (second output target hard-coded in `make_response_figure.py`); it now matches the SI copy.
- `public_code_repo/.../supplementary/panels/supp_fig14_od_vs_ph.pdf` rewritten in place.
- `latex/supplementary_figs/Fig_R1_1B_OD_vs_PDI.svg` is now stale relative to the `.pdf`.

## Rules compliance

- `common_setup.py`: **not touched.**
- `pdf.fonttype`, `ps.fonttype`, `font.family`: **not changed anywhere.**
- `rebuild_and_fit_a4.py`: not run.
- Both trees synced; all 7 regenerated PDFs verified byte-identical across trees, and the
  `includegraphics` lines of the two `figures.tex` files verified identical.
- Colour re-verified after regeneration: all 15 figures DeviceRGB.
