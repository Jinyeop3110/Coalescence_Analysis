# Workstream C — R3_4 gLV sensitivity figures + pH-feedback alternative model

**Agent run:** 2026-08-01
**Scripts owned:**
- `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mixed_sign_higher_order_figure.py`
- `Figure_generate/code/Figure_revision/R3_3_pair_additivity/make_R3_3_figure.py`
- `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_p_axis_fine_figure.py`
- `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mutualistic_pair_fraction_figure.py`
- `Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/make_mean_variance_grid_figure.py`
- `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/make_Q5_phase_figures.py`

**Result: 6/6 PASS** (text size and colour). No LaTeX include width was changed —
every fix is script-side, as required (all six were already at or near `\textwidth`).

Common pattern applied to all six: the native canvas was reduced so the PDF prints
at scale 0.80-0.89 instead of 0.48-0.60, and every font size was harmonised into a
narrow native band (6.4-7.4 pt) so the printed span sits inside 5.5-6.4 pt with
margin on both sides of the 5-7 pt requirement.

Mathtext sub/superscripts that could not reach 5 pt at any legible base size were
rewritten as literal text (`$\alpha_{ij}/\mu$` -> `αij/μ`, `$h/\sqrt{3}$` -> `h/√3`,
`$c_{max}$` -> `cmax`). This is not merely convenient: a label containing a
sub/superscript spans `1/0.7 = 1.4286` internally, which exceeds the 1.40 band ratio
at every possible width and figsize, so such labels are provably incompatible with
the 5-7 pt requirement. See the glyph-survival audit below.

---

## Changes made

### R3_4_mixed_sign_higher_order.pdf
- **Before:** print 1.79-4.83 pt (FAIL; native span ratio 2.70, far beyond the 1.4x band)
- **Lever:** (b) script fonts + canvas
- **Edits** (`.../R3_3_nonCompetitive_gLV/make_mixed_sign_higher_order_figure.py`):
  - L131 `figsize=(15.0, 4.35)` -> `figsize=(7.6, 3.4)` (native 12.973 in -> 7.278 in, scale 0.483 -> 0.861)
  - L40 `font.size` 7.5 -> 6.8
  - inset x label `r'normalized coefficient $\alpha_{ij}/\mu$'` @5.3 -> `'αij/μ'` @6.4 (subscript would print at 2.24 pt)
  - inset y label / inset tick labels 5.3 / 5.0 -> 6.4
  - inset `$\alpha<0$` / `$\alpha\geq0$` 5.0 -> 6.4; `α<0` moved to the free upper-left corner of the inset and colour-keyed teal, `α≥0` to the upper-right — at 6.4 pt the negative-support block is too narrow to hold the label inline (they collided in B-D). `axvline` now stops at `ymax=0.80` to leave that strip clear.
  - bar `%` labels 7 -> 6.8; `P(α<0)` annotation 6.7 -> 6.8; y label 7.5 -> 6.8; tick labels 6.5 -> 6.8; legend 6.2 -> 6.8; panel titles 8.5 -> 6.8; suptitle 10 -> 7.2
  - x tick labels `'$\mu$={mu:.2f}'` -> `'{mu:.2f}'` and the five per-panel x labels replaced by one `fig.supxlabel('mean interaction coefficient $\mu$')` — five copies of the full wording ran into one another at this width. Wording is unchanged, it is just printed once.
- **Regenerated:** yes — `/Users/jysong/miniforge3/bin/python make_mixed_sign_higher_order_figure.py`
- **Synced to submission tree:** yes
- **After:** print 5.51-6.20 pt (PASS), colour DeviceRGB

### R3_4_simulation.pdf
- **Before:** print 1.79-4.11 pt (FAIL; span ratio 2.29)
- **Lever:** (b) script fonts + canvas
- **Edits** (`.../R3_3_pair_additivity/make_R3_3_figure.py`, `make_figure_simulation` path only):
  - L243 `figsize=(15.0, 4.2)` -> `figsize=(7.6, 3.4)` (scale 0.483 -> 0.861)
  - `P_VALUES` panel titles wrapped over two lines (e.g. `'antisymmetric\nexploitation ($p=-1$)'`) — no wording changed; a single line would have run into the neighbouring panel's title. The analytic inset was raised from `y=1.10` to `y=1.17` to clear the two-line titles.
  - same inset treatment as above: `'directed coefficient $\alpha_{ij}/\mu$'` @5.3 -> `'αij/μ'` @6.4; density/tick labels -> 6.4; α<0 / α≥0 repositioned to the inset corners @6.4; `axvline(ymax=0.80)`; `set_xlim(-2.0, 2.0)` -> `(-2.4, 2.4)` so the `-2` x tick label clears the `0` y tick label
  - bar `%` 7 -> 6.8; x tick labels `'$\mu$={mu:.2f}'` -> `'{mu:.2f}'` @6.8; y label 7.5 -> 6.8; panel titles 8.5 -> 6.8; legend 6.2 -> 6.8; tick labels 6.5 -> 6.8
  - per-panel x label replaced by one `fig.supxlabel('interaction strength $\mu$')`
  - **module-level `rcParams['font.size']` deliberately left at 7.5** so the sibling figure `R3_4_experiment.pdf` (not an SI figure; used by `revision_first_round/response/reviewer3_response.tex`) is unaffected.
- **Regenerated:** yes — `/Users/jysong/miniforge3/bin/python make_R3_3_figure.py`
- **Synced to submission tree:** yes
- **After:** print 5.51-5.86 pt (PASS), colour DeviceRGB

### R3_4_pair_coupling_fine.pdf
- **Before:** print 2.24-6.03 pt (FAIL; span ratio 2.70)
- **Lever:** (b) script fonts + canvas
- **Edits** (`.../R3_3_nonCompetitive_gLV/make_p_axis_fine_figure.py`):
  - L95 `figsize=(11.2, 4.35)` -> `figsize=(7.0, 3.2)` (native 10.395 in -> 7.078 in, scale 0.603 -> 0.885)
  - L38 `font.size` 8 -> 6.8
  - inset x label `r'directed coefficient $\alpha_{ij}/\mu$'` @5.3 -> `'directed coefficient αij/μ'` @6.4 (full wording kept — this figure has only 3 panels and the room exists); inset y label and tick labels -> 6.4
  - panel titles 9 -> 7.0; `pair-coupling $p$` and `% outcomes` pinned at 6.8; suptitle 10 -> 7.2
- **Regenerated:** yes — `/Users/jysong/miniforge3/bin/python make_p_axis_fine_figure.py`
- **Synced to submission tree:** yes
- **After:** print 5.67-6.38 pt (PASS), colour DeviceRGB

### R3_4_mutualistic_pair_fraction.pdf
- **Before:** print 1.79-4.83 pt (FAIL; span ratio 2.70)
- **Lever:** (b) script fonts + canvas
- **Edits** (`.../R3_3_nonCompetitive_gLV/make_mutualistic_pair_fraction_figure.py`):
  - L140 `figsize=(15.0, 4.35)` -> `figsize=(7.6, 3.4)` (scale 0.483 -> 0.861)
  - L41 `font.size` 7.5 -> 6.8
  - identical inset treatment to `mixed_sign` (label -> `'αij/μ'` @6.4, α<0 / α≥0 to the inset corners, `axvline(ymax=0.80)`)
  - inset x ticks `[-0.2, 0, 1, 2]` -> `[0, 1, 2]`: at 6.4 pt the `-0.2` label printed on top of the `0` label. The support edge is stated in the figure title and in the caption.
  - suptitle rewritten as literal text — `$\alpha_{{ij}},\alpha_{{ji}}\sim U[-0.2\mu,0]$; $\gamma=0.10$` -> `(αij, αji ~ U[-0.2μ, 0]; γ = 0.10)` @7.2 (the nested subscripts printed at 3.4 pt)
  - bar `%` 7 -> 6.8; `q` annotation 6.7 -> 6.8; x tick labels -> `'{mu:.2f}'` @6.8; y label 7.5 -> 6.8; panel titles 8.5 -> 6.8; legend 6.2 -> 6.8; tick labels 6.5 -> 6.8
  - per-panel x label replaced by one `fig.supxlabel('mean competitive coefficient $\mu$')`
- **Regenerated:** yes — `/Users/jysong/miniforge3/bin/python make_mutualistic_pair_fraction_figure.py`
- **Synced to submission tree:** yes
- **After:** print 5.51-6.20 pt (PASS), colour DeviceRGB

### R3_4_mean_variance_grid.pdf
- **Before:** print 3.47-8.55 pt (FAIL at both ends)
- **Lever:** (b) script fonts only — `figsize` unchanged at `(7.2, 6.0)`, include stays `0.92\textwidth`
- **Edits** (`.../R3_3_nonCompetitive_gLV/make_mean_variance_grid_figure.py`):
  - `fig.suptitle('Mean-vs-variance sweep of interaction coefficients ($\alpha_{ij}\sim U[m-h,m+h]$)', fontsize=10.5)` **removed** (it printed at 8.55 pt, and its subscript at 5.98 pt; there is no size that satisfies both). The identical statement is already carried verbatim by the caption of Supplementary Fig. 42 in **both** trees — "Off-diagonal coefficients are sampled from $\alpha_{ij}\sim U[m-h,m+h]$" — so **no caption edit was needed and nothing was lost**.
  - `y` label `'coefficient std $h/\sqrt{3}$'` -> `'coefficient std h/√3'` (the `\sqrt` glyph printed at 3.47 pt), size kept at 7.5
  - bottom `fig.text`: `negative $\alpha_{ij}$ values` -> `negative αij values` (subscript printed at 3.99 pt); size 7.0 -> 7.5
  - heatmap cell annotations 6.0 -> 7.0 (both `annotate_percent` and `draw_phi_heatmap`)
  - x/y tick labels 6.5 -> 7.0; colorbar tick labels 6.0 -> 7.0; colorbar labels 6.5 -> 7.0
  - panel titles 8.5 -> 8.3
- **Regenerated:** yes — `/Users/jysong/miniforge3/bin/python make_mean_variance_grid_figure.py`
- **Synced to submission tree:** yes
- **After:** print 5.57-6.61 pt (PASS), colour DeviceRGB

### ph_feedback_alternative_model.pdf (built as `Fig_Q5_phase_pH.pdf`)
- **Before:** print 2.54-5.58 pt (FAIL; span ratio 2.20)
- **Lever:** (b) script fonts + canvas
- **Edits** (`.../Q5_pH_feedback_model/make_Q5_phase_figures.py`):
  - L143 `figsize=(11.5, 3.3)` -> `figsize=(7.0, 2.1)` (native 10.327 in -> 6.771 in, scale 0.558 -> 0.852)
  - L43 `font.size` 8 -> 6.5
  - `STRENGTHS` restructured from `(key, label)` to `(key, short_label, full_label)`. The parameter strings now appear **only** in the scatter-panel titles; the bar panel's x tick labels are just `weak` / `mid` / `strong`. In the previous figure the three long labels under the bar panel **already overlapped each other illegibly** (visible in `backup_figs_20260801/supplementary_figs/ph_feedback_alternative_model.pdf`) — this removes the collision as well as the size violation.
  - `$c_{max}$` -> literal `cmax` in those labels (the subscript printed at 2.54 pt)
  - scatter titles / axis labels 8 -> 7.0; bar `%` labels 7 -> 6.5; `% outcomes` and `phase diagram` 8 -> 7.0; panel letters 10 -> 7.4; suptitle 9.5 -> 7.4; legend stays 6.5
- **Regenerated:** yes — `/Users/jysong/miniforge3/bin/python make_Q5_phase_figures.py`
- **Copied and renamed:** `Fig_Q5_phase_pH.pdf` -> `supplementary_figs/ph_feedback_alternative_model.pdf` in both trees
- **After:** print 5.54-6.30 pt (PASS), colour DeviceRGB

---

## Verification

```
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py R3_4
  R3_4_mixed_sign_higher_order.pdf     1.00  0.861   5.51-6.20   PASS  OK
  R3_4_simulation.pdf                  1.00  0.861   5.51-5.86   PASS  OK
  R3_4_pair_coupling_fine.pdf          1.00  0.885   5.67-6.38   PASS  OK
  R3_4_mutualistic_pair_fraction.pdf   1.00  0.861   5.51-6.20   PASS  OK
  R3_4_mean_variance_grid.pdf          0.92  0.796   5.57-6.61   PASS  OK
  TOTAL 5   size PASS 5   size FAIL 0

/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py ph_feedback
  ph_feedback_alternative_model.pdf    0.92  0.852   5.54-6.30   PASS  OK
  TOTAL 1   size PASS 1   size FAIL 0
```

All six were additionally rasterised at 150-350 dpi and inspected for label
collisions after the canvas reduction. Three collisions introduced by the larger
relative text were found and fixed (per-panel x labels running together; the
`α<0` / `α≥0` inset labels; the `-0.2` / `0` inset ticks), plus one pre-existing
collision fixed (the pH figure's bar x tick labels). The final renders are clean.

## Glyph-survival audit of the rewritten labels (coordinator correction, 2026-08-01)

The coordinator warned that Unicode superscript/subscript characters (U+207B,
U+2080-U+2089) are absent from Arial, that matplotlib silently emits `.notdef` for
them, and that the character then disappears from the extracted text — a mangled
label that still scores PASS. Every label I rewrote was therefore re-extracted from
the regenerated PDFs with `fitz` and compared character for character.

Result: **no Unicode sub/superscript characters were used anywhere in these six
figures**, and all ten rewritten labels survive as byte-exact single spans in the
embedded `ArialMT` subset:

| figure | expected span | spans found | font |
|---|---|---|---|
| R3_4_mixed_sign_higher_order | `αij/μ` | 5/5 | ArialMT |
| R3_4_simulation | `αij/μ` | 5/5 | ArialMT |
| R3_4_pair_coupling_fine | `directed coefficient αij/μ` | 3/3 | ArialMT |
| R3_4_mutualistic_pair_fraction | `αij/μ` | 5/5 | ArialMT |
| R3_4_mutualistic_pair_fraction | `Weak mutualistic-pair sweep (αij, αji ~ U[-0.2μ, 0]; γ = 0.10)` | 1/1 | ArialMT |
| R3_4_mean_variance_grid | `coefficient std h/√3` | 4/4 | ArialMT |
| R3_4_mean_variance_grid | `...contains negative αij values (positive ecological effects).` | 1/1 | ArialMT |
| ph_feedback_alternative_model | `weak (μ=0.3, cmax=1e-10)` | 1/1 | ArialMT |
| ph_feedback_alternative_model | `mid (μ=0.6, cmax=1e-9)` | 1/1 | ArialMT |
| ph_feedback_alternative_model | `strong (μ=0.9, cmax=3e-8)` | 1/1 | ArialMT |

The only non-ASCII characters introduced are `α` U+03B1, `μ` U+03BC, `γ` U+03B3 and
`√` U+221A. All four are real Arial glyphs, all are embedded in each PDF's font
subset (so downstream rendering does not depend on Arial being installed), and all
were additionally confirmed **visually** in 150-350 dpi rasters of every figure —
the radical and the Greek letters draw correctly, no `.notdef` boxes.

These were kept rather than converted to `alpha_ij/mu`-style ASCII for one reason:
each of these figures still contains mathtext Greek elsewhere that is *not* a
sub/superscript and therefore stays (`interaction strength $\mu$`, `$P(\alpha<0)$`,
`$\mu=0.30$` titles). Spelling the same symbols out as ASCII in the neighbouring
label would have made the same figure show `μ` and `mu` side by side. If the
coordinator prefers campaign-wide ASCII regardless, this is a three-line change per
script — say the word.

Reproduce with:
```
cd Draft/v5/latex/supplementary_figs
/Users/jysong/miniforge3/bin/python -c "import fitz; p=fitz.open('R3_4_mean_variance_grid.pdf')[0]; \
print([s['text'] for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']])"
```

## Blocked / not fixed

None. All six figures are compliant. No layout redesign (panel splitting or
re-orientation) was required, so CAMPAIGN.md rule 9 was not invoked.

## Side effects

- `Figure_generate/code/Figure_revision/R3_4_experiment.pdf/.png/.svg` were
  rewritten by rerunning `make_R3_3_figure.py`, but **their content is unchanged**:
  no code on the `make_figure_experiment` path was touched and the module-level
  `rcParams` were deliberately left alone for exactly this reason. This figure is
  not an SI figure (it is used by `latex/revision_first_round/response/reviewer3_response.tex`,
  which reads its own copy).
- `Figure_generate/code/Figure_revision/Q5_pH_feedback_model/Fig_Q5_phase_gLV.*`
  and `Fig_Q5_phase_hybrid.*` **did change** (same script, shared styling). Neither
  is an SI figure. The first-round internal memo references separate files named
  `internal_Q5_phase_gLV.pdf` / `internal_Q5_phase_hybrid_*.pdf` in a different
  directory; those copies were not touched.
- `Draft/v5/latex/supplementary_figs/internal_Q5_phase_pH.pdf` is a stale,
  unreferenced-by-the-SI copy. Left untouched.
- `.png` / `.svg` siblings of the six figures were regenerated in
  `Figure_generate/code/Figure_revision/` (the scripts always emit all three
  formats). Only the `.pdf`s are carried into the two LaTeX trees, matching what
  was already there.
- No `.tex` file was modified by this workstream.
