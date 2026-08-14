# Supplementary Figure Format Campaign — NATECOLEVOL-26010384A

**Opened:** 2026-08-01
**Goal:** bring all 65 supplementary + Extended Data figure PDFs into compliance with the
Nature Ecology & Evolution artwork requirements for **text size** and **colour**.

This file is the single source of truth for the campaign. Every agent reads it before
working and records its changes in `changelog/WS-<id>.md`.

---

## 1. Scope

### In scope
| Requirement | Rule |
|---|---|
| **Text size** | All text between **5 pt and 7 pt at print size**. |
| **Colour** | RGB colour mode. No CMYK, Separation, or DeviceN. |

Mathtext sub/superscripts are **in scope** when they are the reason text falls below 5 pt
(matplotlib renders them at 0.7x the base size, so a 7 pt base yields a 4.9 pt subscript).

### Explicitly OUT of scope for this campaign
- Typeface family (Arial vs DejaVu Sans mathtext fallback).
- Font embedding / Type 3 fonts.
- Figure content, data, panel arrangement, or scientific meaning.

Do **not** fix Type 3 or DejaVu issues here even where you see them. They are tracked
separately. Changing `pdf.fonttype` alters the output PDF and would confound this campaign.

---

## 2. Print-size model (validated — do not re-derive)

Figures are matplotlib PDFs included into the SI LaTeX at a fraction of `\textwidth`.

```
SI \textwidth = 451.28 bp = 6.268 in = 159.2 mm   (a4paper, 1in margins)
scale    = (include_multiplier * 451.28) / native_pdf_width_bp
print_pt = native_font_pt * scale
```

Validated against the compiled `supplementary.pdf`: predicted text reproduces the
compiled document exactly — 25,525 characters predicted vs 25,525 observed, and all 85
distinct predicted print sizes present.

### The 1.4x band constraint
The legal band is 5-7 pt, a ratio of only **1.4x**. A figure whose native font sizes span
more than 1.4x **cannot be fixed by rescaling at any include width** — its font sizes must
be harmonised in the generating script. The verifier reports this automatically.

### Extended Data figures: dual constraint
ED figures are built 180 mm wide by `latex/figures/extended_data/rebuild_and_fit_a4.py`
and Nature typesets them as **separate files at native size**, but they also appear inside
the SI at 143-159 mm. They must satisfy **both** measures:

- standalone: `print_pt == native_pt`, so native must be within 5-7 pt
- in-SI: `native_pt * scale` must be within 5-7 pt, where scale is 0.796-0.975

Combining these gives the campaign rule for every ED figure:

> **All ED figure text must be 6.3-7.0 pt native.**

This resolves the standalone-vs-SI ambiguity without narrowing either requirement.
Target the middle of that window (**6.5 pt**) for body text.

---

## 3. Targets

| Figure class | Target |
|---|---|
| Supplementary figures (non-ED) | print **5.5-6.8 pt** (aim centre ~6.2 pt) |
| Extended Data figures | native **6.3-7.0 pt** (aim ~6.5 pt) |

Aim for the interior of the band, not its edges — `bbox_inches='tight'` shifts the native
canvas size slightly between runs, which moves `scale` and can push an edge value out.

---

## 4. The two levers

**(a) LaTeX include width** — edit `\includegraphics[width=...]` in
`latex/supplementary_sections/figures.tex`. Cheapest, no regeneration. Only works when the
figure's native span ratio is <= 1.4.

**(b) Generating-script font sizes / figsize** — required whenever the span ratio exceeds
1.4, or when the figure is already at `\textwidth` and still too small.

Prefer (a) when it suffices. Prefer (b) when a width change would make the printed panel
unreasonably small (below ~45 mm) or when the figure must stay full width.

---

## 5. Rules for agents

1. **Never edit `Figure_generate/code/common_setup.py`.** Many scripts import it; a change
   there silently affects figures owned by other workstreams. If your figure's only fix
   appears to require it, stop and report instead.
2. **Stay inside your assigned scripts.** Workstreams are script-disjoint by construction.
   If you find your figure needs a script owned by another workstream, report it, do not edit.
3. **Do not run `rebuild_and_fit_a4.py`.** ED composites are rebuilt centrally in Wave 2
   after all panel scripts are fixed. Fix the panel sources only.
4. **Back up before regenerating.** A backup of all figure PDFs exists at
   `figure_format_campaign/backup_figs_20260801/`. Figure PDFs are **gitignored and
   untracked** — there is no other safety net. Scripts under `Figure_generate/code/` *are*
   git-tracked and recoverable.
5. **Watch for shared scripts producing already-passing figures.** Some scripts emit several
   figures. Check the baseline table before editing; do not regress a passing figure.
6. **Verify your own work** with the campaign verifier before reporting:
   ```
   /Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py <substring>
   ```
7. **Sync both trees.** Every regenerated PDF must be copied to BOTH:
   - `Draft/v5/latex/supplementary_figs/` (and `latex/figures/extended_data/`)
   - `Draft/v5/revision_submission/00_submit_new/Supplementary_Information_LaTeX_Source/supplementary_figs/`
     (and `.../Supplementary_Information_LaTeX_Source/figures/extended_data/`)
   Any `.tex` width change must likewise be applied to both `latex/supplementary_sections/`
   and `.../Supplementary_Information_LaTeX_Source/supplementary_sections/`.
   Remember the submission tree defines neither `\rev` nor `\revsecond`.
8. **Record every change** in `changelog/WS-<id>.md` using the template in section 8.
9. If a figure cannot be brought into compliance without a layout redesign (splitting
   panels, changing orientation), **do not redesign it** — report it as blocked with your
   reasoning. That is an author decision.

---

## 6. Workstream assignment

| WS | Scripts owned | Figures | Wave |
|---|---|---|---|
| **A** | `plot_stacked_bar_class_fractions.py` | Fig_S26 + panel sources for ED2, ED4, ED5f | 1 |
| **B** | `generate_pie_plots.py` | 9 coalescence_matrix panels | 1 |
| **C** | `make_mixed_sign_higher_order_figure.py`, `make_R3_3_figure.py`, `make_p_axis_fine_figure.py`, `make_mutualistic_pair_fraction_figure.py`, `make_mean_variance_grid_figure.py`, `make_Q5_phase_figures.py` | 6 R3_4 / pH-feedback figures | 1 |
| **D** | `generate_fig1_1.py`, `build_phylogeny.py`, `plot_pairwise_matrix_dynamics_improved.py`, `plot_interaction_matrix.py` | 8 figures | 1 |
| **E** | `analyze_continuous_similarity.py`, `analyze_OD_density.py`, `analyze_sim_parent_norm_asymmetry.py`, `analyze_invasion_fitness.py` | 8 figures | 1 |
| **F** | `plot_rank_abundance_natural.py`, `plot_rank_abundance_parental_vs_coalesced.py`, `analyze_natural_taxonomic_distinctness.py`, `analyze_pool_size.py` | 8 figures | 1 |
| **G** | LaTeX-width-only changes + `plot_assembly_effect_mean_interaction.py`, `plot_monoculture_od_growth_histograms.py`, `plot_overlap_fraction_histogram.py`, `plot_single_comparison.py`, `make_response_figure.py`, `create_two_panel_figure.py` | 15 figures | 1 |
| **H** | `analyze_additive_null.py` (ED3), `make_ed_fig5_combined.py` (ED6), `plot_correlation_barplots_clean.py` (ED7), `plot_ph_figures_revised.py` (ED8 — **must not regress Fig_S23**), ED1 source | ED panel sources | 1 |
| **Z** | `rebuild_and_fit_a4.py`, final sync, recompile | ED composites 1-8 | 2 (central) |

---

## 7. Baseline (2026-08-01, before any change)

Measured by `verify_figures.py`:

- **Colour: 65/65 PASS.** All DeviceRGB. Nothing to do for requirement 3 — but re-verify
  after regenerating, since a changed backend or colormap could introduce CMYK.
- **Text size: 2/65 PASS.** Only `Fig_S23_ASV_vs_pH_combined.pdf` (5.06-6.33 pt) and
  `ED_Fig1_combined.pdf` (6.69 pt, in-SI measure only).
- 31 figures contain text below 5 pt; 37 contain text above 7 pt.
- **Extended Data: 0/8 dual-compliant.** ED1 passes in-SI but fails standalone at 8.41 pt.
- Worst offenders: `coalescence_matrix_*_s24` at **1.73 pt**; the R3_4 family at
  **1.79 pt**; `ph_feedback_alternative_model` at **2.54 pt**.
- `timeseries_Base_combined.pdf` has **no vector text** (flat 270 dpi raster) — text size is
  not measurable and this campaign cannot fix it. Colour is RGB. Reported, not actioned.

Known systemic causes:
1. Hard-coded `x1.3` font multiplier in `plot_stacked_bar_class_fractions.py` (WS A).
2. Mathtext 0.7x sub/superscript shrink pushing subscripts below 5 pt (many WS).
3. Figures authored on very wide canvases then compressed into 6.27 in (WS B, C).
4. `LABEL_PT = 8.0` in `rebuild_and_fit_a4.py` putting ED panel letters at 7.08 pt (WS Z).

---

## 8. Changelog format

Each agent writes `changelog/WS-<id>.md`:

```markdown
# Workstream <id> — <title>

**Agent run:** <date>
**Scripts owned:** ...

## Changes made

### <figure-file.pdf>
- **Before:** print X.XX-Y.YY pt (FAIL, reason)
- **Lever:** (a) LaTeX width / (b) script fonts / both
- **Edits:**
  - `path/to/script.py:LINE` — `fontsize=12` -> `fontsize=7`
  - `latex/supplementary_sections/figures.tex:LINE` — `width=0.9\textwidth` -> `width=0.75\textwidth`
- **Regenerated:** yes/no — command used
- **Synced to submission tree:** yes/no
- **After:** print X.XX-Y.YY pt (PASS)

## Blocked / not fixed
### <figure-file.pdf>
- Reason, and what decision is needed from the author.

## Side effects
- Any other file the regeneration overwrote.
```

---

## 9. Status

| Wave | State |
|---|---|
| Wave 1 (WS A-H) | **complete** 2026-08-01 |
| Wave 2 (WS Z — ED recomposition) | **complete** 2026-08-01 |
| Author decisions | **5 figures pending** (section 10.3) |
| Final SI recompile + zips | pending |

## 10. Consolidated results

### 10.1 Headline

| Metric | Baseline | After campaign |
|---|---|---|
| Text size PASS | **2 / 65** | **59 / 65** |
| Colour (RGB) PASS | 65 / 65 | **65 / 65** |
| ED figures dual-compliant (standalone + in-SI) | 0 / 8 | **6 / 8** |

Text below 5 pt went from 31 figures to 4; text above 7 pt from 37 figures to 0.
Worst remaining value is 3.83 pt (ED 5 panel f), down from 1.73 pt.

Per-workstream changelogs are in `changelog/WS-*.md`. Every figure was verified with
`verify_figures.py`, and every regenerated PDF was confirmed byte-identical across both trees.

| WS | Result |
|---|---|
| A | Fig_S26 pass; ED2 + ED4 panel sources pass dual; ED5 panel f blocked |
| B | 6 / 9 coalescence matrices pass; 3 `_s24` blocked |
| C | 6 / 6 pass |
| D | 8 / 8 pass |
| E | 8 / 8 pass |
| F | 7 / 8 pass; `natural_taxonomic_distinctness` blocked |
| G | 12 / 15 pass; 3 handed to COORD |
| H | ED 3, 6, 7, 8 panel sources pass; ED 1 blocked |
| COORD | 3 / 3 pass (the figures WS G handed over) |
| Z | `LABEL_PT` 8.0 -> 6.8; ED 5 panels a-e 8.0 -> 7.5 pt; all 8 ED composites rebuilt |

### 10.2 Cross-cutting findings

1. **Mathtext is provably incompatible with the 5-7 pt band.** Matplotlib renders a
   sub/superscript at exactly 0.7x its base, so any mathtext-bearing label has an internal
   span of 1/0.7 = **1.4286**, above the band's 1.40 ratio — at every width and every figsize.
   Diagnostic: any too-small tier equal to 0.7x another tier in the same figure. Affected
   figures were fixed by rewriting labels without mathtext.
2. **Log-axis tick labels have the same defect.** `10^n` ticks put the exponent at 0.7x the
   mantissa. Any log axis is an automatic fail. Fixed with plain-decimal or e-notation
   formatters (WS E, WS F).
3. **Unicode superscripts are NOT a safe substitute.** Arial has no U+207B and no subscript
   digits U+2080-2089. Matplotlib silently draws `.notdef`, the glyph vanishes from the
   extracted text, **and the figure then scores PASS**. Caught by WS G before it shipped.
   Rule adopted mid-campaign: **rewrite in plain ASCII**, and re-extract every rewritten
   label from the regenerated PDF with fitz to confirm it character-for-character. Greek
   letters at base size (alpha, mu, gamma, lambda) are present in Arial and were verified
   safe where retained.
4. **Compliance does not imply legibility.** Six collisions were found by rasterising and
   inspecting regenerated figures, and would otherwise have shipped as compliant-but-degraded
   (WS B, C, D, F). Font enlargement in dense panels must always be visually checked.
5. **Some constraints are scale-invariant.** Where a label's width is set by content and the
   canvas is width-limited, changing figsize moves the fit factor by exactly the same ratio,
   so the printed pt size does not move at all. This is why ED 1 and ED 5 panel f cannot be
   fixed by any resizing — only by changing what is drawn. Verified algebraically and
   empirically in both cases.

### 10.3 Blocked — author decisions required

| Figure | Issue | Cheapest fix |
|---|---|---|
| `coalescence_matrix_{Nutr-,Base,Nutr+}_s24` | 24 labels across 114.6 mm; at any size >= 5 pt they overlap by ~1.2 mm | Promote each to its own figure at 0.95-1.0\textwidth. Verified candidates parked in `WS-B_blocked_s24_candidates_0.95tw/`. Dropping them into the current 3-panel layout would need ~249 mm against a 246 mm `\textheight`. |
| `ED_Fig5_combined` (panel f) | Per-bar `(164/1200)` counts capped at ~4.6 pt **at any canvas size** — scale-invariant | Flip `S12_SHOW_TOTALS = False` (switch already added by WS A, currently off). Annotation becomes `14%` / `164` at 6.5 pt. Denominator is constant (n = 1200, except two 24-species bars at n = 1194) so one caption sentence restores it. |
| `natural_taxonomic_distinctness` | `n=6` / `n=60` / `n=435` labels sit 0.18 in apart; collide at any size clearing 5 pt | Move the sample sizes into the caption. The same n triple repeats three times per panel. |
| `ED_Fig1_combined` | Passes in-SI (6.69 pt) but **fails standalone at 8.41 pt**; width-limited taxonomy table, so scale-invariant | Reduce content width (abbreviate taxonomy columns) or reissue as a Supplementary Table. |
| `timeseries_Base_combined` | Flat 270 dpi raster, no vector text, no generating script exists. Also below Nature's 300 dpi floor | Re-assemble from the surviving per-panel SVGs in `code/Figure/Fig1_1_Plots/`. Out of reach of this campaign. |

### 10.4 Pre-existing issues surfaced (not caused by, and out of scope for, this campaign)

- **`Fig_R1_1B_OD_vs_PDI.pdf` was stale** — the shipped SI copy did not match its generating
  script. Regenerated from the canonical source named in `supplementary_figs/file_source.md`.
- **9 figures embed Type 3 fonts**, traced to six scripts missing `pdf.fonttype = 42`.
  Deliberately not fixed — typeface/embedding is outside this campaign.
- **`common_setup.py::Community_PermutateList` is nondeterministic** (`list(set(...))` under
  Python hash randomisation), so coalescence-matrix row/column order changes between runs.
  Cosmetic but not reproducible; `PYTHONHASHSEED=0` would pin it.
- **ED 7 sample sizes** in the regenerated `correlation_summary_clean.csv` are n = 90/88/87,
  against the caption's 90/83/90. Pre-existing and independent of this campaign; no such
  number appears inside the figure artwork.
- **ED 3 and ED 7 artwork drift** — both deployed PDFs predated committed script edits, so
  regenerating necessarily ships newer labels/markers. Verified: data, means and stars
  unchanged.
- **`build_phylogeny.py` hard-codes a copy to the deleted `Draft/v3/`**; recommend repointing.
- **Verifier blind spot:** in Type 3 figures a U+2014 renders correctly but does not survive
  text extraction, so character counts are undercounted for those three files. No compliance
  impact (all their remaining glyphs are 12-13 pt).
