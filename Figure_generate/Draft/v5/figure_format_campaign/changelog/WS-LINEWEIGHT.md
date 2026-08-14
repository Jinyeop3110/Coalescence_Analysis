# Workstream LINEWEIGHT — Extended Data stroke widths (tracker ED-15) + panel labels (ED-14, ED-16)

**Agent run:** 2026-08-01
**Scripts owned:**
- `Figure_generate/code/Figure_revision/R3_1_additive_null/analyze_additive_null.py` (ED 3)
- `Figure_generate/code/make_ed_fig5_combined.py` (ED 6 panel sources)
- `Figure_generate/code/plot_correlation_barplots_clean.py` (ED 7 panel sources)
- `Figure_generate/code/plot_ph_figures_revised.py` (ED 8 — must not regress Fig. S23)

This is a separate requirement from the text-size/colour campaign recorded in
`CAMPAIGN.md`, and it was **not** measured there. The governing text is the Extended Data
guide, not the artwork guide:

> "Lines and strokes should be set between 0.25 and 1 pt."
> https://www.nature.com/documents/Extended_Data_guide.pdf

A new verifier, `figure_format_campaign/measure_linewidths.py`, reads stroke widths out of
the PDF content stream with fitz. Extended Data publishes standalone at native size, so the
recorded width IS the printed width and no scale model is needed — unlike text size, where
the include multiplier matters.

## Baseline (before any change)

| ED | range | verdict |
|---|---|---|
| 1 | 0.57 | PASS |
| 2 | 0.50-1.00 | PASS |
| **3** | 0.50-**1.50** | FAIL |
| 4 | 0.50-1.00 | PASS |
| 5 | 0.28-0.57 | PASS |
| **6** | 0.73-**2.95** | FAIL |
| **7** | 0.44-**1.77** | FAIL |
| **8** | 0.50-**2.00** | FAIL |

4 / 8 within spec, matching the tracker's ED-15 estimate.

## Approach

Placement in the composite shrinks strokes by the same factor as text (0.88-1.00 depending
on the figure), so the ceiling only ever helps and the binding constraint is the value set
in the panel script. Every offending stroke was capped at **0.9 pt** rather than 1.0 pt, so
that the run-to-run drift in native canvas size from `bbox_inches='tight'` cannot push a
figure over the ceiling. In each script the value is a named constant carrying the spec
quotation, so it is not silently raised later — the same pattern the campaign used for the
`ED_*_PT` text constants.

## Changes made

### ED_Fig3_combined.pdf (`analyze_additive_null.py`)
- **Before:** 0.50-1.50 pt (FAIL — similarity-boundary arc at 1.5, annotation arrows at 1.2)
- **Lever:** (b) script only.
- **Edits:**
  - `:601-606` — added `ED_MAX_LW = 0.9` with the spec quotation and fit factor.
  - `:615` — similarity-boundary arc `linewidth=1.5` -> `ED_MAX_LW`.
  - `:654` — representative-event arrows `"linewidth": 1.2` -> `ED_MAX_LW`.
- **Regenerated:** yes — `cd Figure_generate/code && ~/miniforge3/bin/python Figure_revision/R3_1_additive_null/analyze_additive_null.py`
- **After:** 0.50-1.00 pt (PASS)

### ED_Fig6_combined.pdf (`make_ed_fig5_combined.py`, panels a-d)
- **Before:** 0.73-2.95 pt (FAIL — the worst offender in the set)
- **Edits:**
  - `:51-61` — added `MAX_LW = 0.9`.
  - `:167` — null-mean reference line `linewidth=2` -> `MAX_LW`.
  - `:175,180,190,195` — both errorbar calls, `capthick=1.2` and `linewidth=1.2` -> `MAX_LW`.
  - `:235-239` — panel d: the "Random selection" trace was `linewidth=3`; the two marker
    traces carried no explicit width and so inherited the matplotlib default of 1.5, which
    is where the composite's unexplained 1.473 pt tier came from. All three now `MAX_LW`,
    and the two marker traces also get `markeredgewidth=MAX_LW`.
- **After:** 0.73-0.98 pt (PASS)

### ED_Fig7_combined.pdf (`plot_correlation_barplots_clean.py`, panels a-c)
- **Before:** 0.44-1.77 pt (FAIL)
- **Edits:**
  - `:139-145` — added `ED_MAX_LW = 0.9`.
  - `:194-206` — both errorbar calls `capthick=1.5`/`linewidth=1.5` and the random-selection
    baseline `linewidth=2` -> `ED_MAX_LW`.
- **After:** 0.44-0.80 pt (PASS)

### ED_Fig8_combined.pdf (`plot_ph_figures_revised.py`)
- **Before:** 0.50-2.00 pt (FAIL)
- **Edits:**
  - `:311-317` — added `ED_MAX_LW = 0.9`, declared **inside** the S24 function rather than
    at module scope, for the same reason the point sizes are: this module also builds
    Fig. S23, which already complies and must not be disturbed.
  - `:341` — regression line `linewidth=2` -> `ED_MAX_LW`.
  - `:346` — the PDI = 0.5 reference `axhline` carried no explicit width and inherited the
    1.5 default; now `ED_MAX_LW`.
- **After:** 0.50-1.00 pt (PASS)
- **Fig. S23 not regressed:** re-verified at 5.06-6.33 pt print, PASS, unchanged.

## Panel-label text (ED-14)

Author decision 2026-08-01: `parent`/`parents` are permitted inside figure artwork, so the
ED 6 and ED 7 axis labels keep the short form and move to sentence case, "Same parent" /
"Cross parents". `writing_rules.md` rule 4 and `revision.rule.md` rule 12 now record the
exception. Panel d of ED 6 also had its legend entries and its two axis titles moved to
sentence case; it was the only place in that figure using Title Case, against panels a-c.

The substantive defect ED-14 exposed was in the caption, not the artwork: the ED 6 caption
quoted its legend as "Same parental community" / "Cross-community", which is text that has
never appeared in the figure. Corrected in both trees to quote the labels as drawn.

## Verification

- `measure_linewidths.py`: **8 / 8** ED composites within 0.25-1 pt, from 4 / 8.
- `verify_figures.py`: text sizes and RGB unchanged on every touched figure. ED 3 and ED 8
  PASS on both the in-SI and standalone measures.
- ED 6 and ED 7 rendered at 200 dpi and inspected. No collisions introduced; the significance
  brackets in ED 7 panels b and c sit oddly, but identically so in
  `backup_figs_20260801/`, so that is pre-existing and untouched here.
- Both SI documents recompiled: 61 pages, 0 undefined references, 0 errors.

## Side effects

- Regenerating ED 7's panels also rewrote `correlation_summary_clean.csv`, reproducing the
  n = 90/88/87 already recorded in `CAMPAIGN.md` 10.4 against the caption's 90/83/90. This
  is pre-existing and independent of this work; no such number appears in the artwork.
- `plot_ph_figures_revised.py` rewrote Fig. S23's `.svg`/`.png`/`.pdf` in its own output
  directory. The deployed SI copy was deliberately **not** replaced, since its code path was
  not touched and the deployed file already passes.

## Verifier caveat worth knowing

`verify_figures.py` reports ED 5, 6 and 7 as text-size FAIL solely because their panel
letters are 8.00 pt, above its 7 pt ceiling. That is not a defect: Nature's specifications
name panel letters as an explicit exception at 8 pt bold lowercase, which is why
`rebuild_and_fit_a4.py` sets `LABEL_PT = 8.0`. The verifier predates that finding and does
not model the exception. ED 6 and ED 7 have no other violation and should be read as
compliant. ED 5's genuine failure is panel f at 4.43 pt, the blocked item in `CAMPAIGN.md`
10.3.
