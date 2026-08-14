# Workstream COORD — coordinator-owned fixes

**Agent run:** 2026-08-01
**Scripts owned:** figures left unassigned or blocked by other workstreams, picked up after
their owning workstream completed.

These three figures were reported blocked by WS G. All three failed on exactly one tier —
a mathtext sub/superscript rendered at 0.7x its base, which cannot fit the 5-7 pt band at
any width (0.7 inverts to a 1.4286 internal span vs the band's 1.40 ratio). All three were
fixed by rewriting the label in plain ASCII, per the correction issued to WS C/D/E after WS G
discovered that Unicode superscripts silently render as `.notdef` in Arial and vanish from
the extracted text while still scoring PASS.

Every rewritten label was re-extracted from the regenerated PDF with fitz and compared
character-for-character before the figure was accepted.

## Changes made

### monoculture_od_growth_histograms.pdf
- **Before:** print 4.38-6.83 pt (FAIL). Single offending character: the `-1` exponent of
  `h$^{-1}$` at native 7.70 pt (0.7 x 11 pt).
- **Lever:** (b) script — mathtext removal only. No font size changed.
- **Edits:**
  - `Figure_generate/code/plot_monoculture_od_growth_histograms.py:241` and `:257` —
    `'Growth Rate (h$^{-1}$)'` -> `'Growth Rate (1/h)'` (both occurrences)
- **Regenerated:** yes — `cd Figure_generate/code && python plot_monoculture_od_growth_histograms.py`
- **Text verified:** extracted string is exactly `Growth Rate (1/h)`.
- **Synced to submission tree:** yes, byte-identical (`cmp` clean).
- **After:** print **5.12-6.83 pt (PASS)**, native span 12/9 = 1.33.

### Fig_R1_1B_OD_vs_PDI.pdf
- **Before:** print 4.91-7.01 pt (FAIL). Offending tier: three `600` subscript characters at
  native 5.60 pt (0.7 x 8 pt).
- **Note:** WS G had already established the shipped SI copy was **stale** and did not match
  its generating script, and regenerated it. This entry is the follow-on mathtext fix.
- **Canonical script confirmed:** `latex/supplementary_figs/file_source.md` names
  `public_code_repo/pipeline/04_figure_generation/supplementary/generate_figure.py`.
  (WS E separately escalated uncertainty about which script is canonical — this resolves it.
  `analyze_OD_density.py` emits a differently-shaped figure and is NOT the source.)
- **Lever:** both.
- **Edits:**
  - `Draft/v5/public_code_repo/pipeline/04_figure_generation/supplementary/generate_figure.py:144` —
    `r"Endpoint OD$_{600}$"` -> `"Endpoint OD600"`
  - `latex/supplementary_sections/figures.tex:162` and submission-tree copy —
    `width=0.83\textwidth` -> `width=0.81\textwidth`
- **Why 0.81 and not WS G's 0.83:** at 0.83 the 8 pt tier lands at 7.01 pt, inside the
  verifier's 0.05 pt tolerance but on the ceiling. CAMPAIGN.md section 3 asks for the band
  interior because `bbox_inches='tight'` shifts the native canvas between runs. 0.81 gives
  5.56-6.84 pt with margin at both ends.
- **Regenerated:** yes — `COALESCENCE_FIGURE_OUT=<tmp> python generate_figure.py`, output
  `supp_fig14_od_vs_ph.pdf` installed as `Fig_R1_1B_OD_vs_PDI.pdf`.
- **Text verified:** all three x-labels extract as exactly `Endpoint OD600`; the 5.60 pt tier
  is gone (tiers now 6.5 / 7.0 / 8.0).
- **Synced to submission tree:** yes.
- **After:** print **5.56-6.84 pt (PASS)**.

### Fig_R1_3_per_medium_scatter.pdf
- **Before:** print 3.79-6.66 pt (FAIL). Two offending tiers: native 4.55 pt (`R^2`
  superscript and `rho_S` subscript, 0.7 x 6.5) and native 4.90 pt (the `+` of `Nutr$^+$`,
  0.7 x 7.0).
- **Script had no assigned owner** — WS G flagged this. Picked up here.
- **Correction to the WS G brief:** my brief stated this figure's native span was 1.23 and
  called it a pure one-lever width fix. That was wrong — it read 5.41 as a native size when
  it was the *print* size of a 4.55 pt tier. The true span was 8.0/4.55 = 1.76, so no width
  could have fixed it. WS G caught this.
- **Lever:** (b) script — mathtext removal only. No font size changed.
- **Edits:** `Figure_generate/code/Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
  - `:721` — `'Nutr$^+$ (HN)'` -> `'Nutr+ (HN)'`
  - `:762`, `:767` — `f'$R^2$=...'` -> `f'R^2=...'`
  - `:763` — `f'$\\rho_S$=...'` -> `f'rho_S=...'`
  - The `$-\pi/4$` / `$\pi/4$` y-tick labels at `:778` were **left as mathtext** — they render
    at full base size (8.0 pt native -> 6.66 pt print), so they are in band and not a problem.
- **Regenerated:** yes — `cd Figure_generate/code && python Figure_revision/R1_3_PDI_no_dominant/analyze_PDI_no_dominant.py`
- **Text verified:** annotations extract as `R^2=0.11, slope=0.49`, `rho_S=0.21, p=0.227`,
  row label as `Nutr+ (HN)`. The 4.55 and 4.90 tiers are gone (tiers now 6.5 / 7.0 / 8.0,
  span 1.23).
- **Width:** left at WS G's `0.70\textwidth`, which is correct now that the mathtext is gone.
- **Synced to submission tree:** yes, byte-identical.
- **After:** print **5.41-6.66 pt (PASS)**.

## Side effects
- `analyze_PDI_no_dominant.py` is a full analysis script; running it rewrote its other
  outputs in `Figure_revision/R1_3_PDI_no_dominant/` (top-K sensitivity figure, CSVs).
  None of those are SI figures and none were copied into either SI tree.
- `generate_figure.py` was run with `COALESCENCE_FIGURE_OUT` pointed at a scratch directory,
  so the `public_code_repo` panel directory was not modified.

## Blocked
None from this workstream — all three assigned figures now pass.
