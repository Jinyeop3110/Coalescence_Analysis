# Workstream E — R2-3 continuous similarity, R1-1 OD density, R3-3 parent norm, R2-4 invasion fitness

**Agent run:** 2026-08-01
**Scripts owned:**
- `Figure_generate/code/Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
- `Figure_generate/code/Figure_revision/R1_1_OD_density/analyze_OD_density.py`
- `Figure_generate/code/Figure_revision/R3_2_richness_mu_model/analyze_sim_parent_norm_asymmetry.py`
- `Figure_generate/code/Figure_revision/R2_4_invasion_fitness/analyze_invasion_fitness.py`

**Result: 8/8 assigned figures PASS text size; colour DeviceRGB throughout (unchanged).**

| figure | before (print pt) | after (print pt) |
|---|---|---|
| marginal_distributions_base_only.pdf | 5.39-7.70 FAIL | **6.18-6.18 PASS** |
| marginal_distributions_nutr_minus_only.pdf | 5.39-7.69 FAIL | **6.23-6.23 PASS** |
| marginal_distributions_nutr_plus_only.pdf | 5.39-7.69 FAIL | **6.18-6.18 PASS** |
| boundary_sensitivity_by_medium.pdf | 6.69-10.91 FAIL | **6.01-6.52 PASS** |
| Fig_R1_1A_winner_loser_OD.pdf | 4.70-8.64 FAIL | **6.15-6.63 PASS** |
| Fig_R1_1C_pairwise_corr_vs_OD.pdf | 3.09-8.46 FAIL | **6.09-6.55 PASS** |
| Fig_R3_3_sim_parent_norm_asymmetry.pdf | 4.03-6.90 FAIL | **6.11-6.47 PASS** |
| invasion_fitness_supp.pdf | 4.16-7.44 FAIL | **5.76-6.65 PASS** |

---

## Changes made

### marginal_distributions_base_only.pdf / _nutr_minus_only.pdf / _nutr_plus_only.pdf
- **Before:** print 5.39-7.70 pt (FAIL — native 8 pt tier too large; native 5.6 pt mathtext superscript already near the floor)
- **Lever:** (b) script fonts only; LaTeX width unchanged at `0.9\textwidth`
- **Edits** (`Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`):
  - `:54` — `mpl.rcParams['font.size'] = 8` -> `6.5` (script-wide; all four of this script's SI figures are WS-E-owned)
  - `:374,377,389,392,404,407` (Base-only block) and `:437,440,451,454,465,468` (per-medium function) —
    dropped the explicit `fontsize=8` on every `set_xlabel`/`set_ylabel` (now inherit 6.5); titles `fontsize=7` -> `6.5`
  - `:404`, `:465` — `r'Retention ($x^2$)'` -> `'Retention (x^2)'` (plain ASCII, full size; mathtext `x^2`
    rendered the `2` at 0.7x = 4.9 pt native, which no include width can rescale into band)
- **Regenerated:** yes — `cd Figure_generate/code && MPLBACKEND=Agg /Users/jysong/miniforge3/bin/python Figure_revision/R2_3_continuous_similarity/analyze_continuous_similarity.py`
  (must run with cwd = `Figure_generate/code`; `common_setup.py` resolves data paths relatively)
- **Synced to submission tree:** yes
- **After:** single 6.5 pt native tier -> print 6.18 / 6.23 / 6.18 pt (PASS)

### boundary_sensitivity_by_medium.pdf
- **Before:** print 6.69-10.91 pt (FAIL — 4.594 in native stretched into 6.268 in, scale 1.364)
- **Lever:** both
- **Edits:**
  - `analyze_continuous_similarity.py:528,529,531,534` — xlabel/ylabel/title `fontsize=7` -> `6.5`; panel letter `A` `fontsize=8` -> `6.5`
  - `analyze_continuous_similarity.py:542,543,545,547` — same for panel B; `r'Minimum retention $x^2$'` -> `'Minimum retention x^2'`
    and `r'PDI boundary ($x^2 > 0.5$)'` -> `'PDI boundary (x^2 > 0.5)'`
  - tick `labelsize=6` left unchanged (`:550`)
  - `latex/supplementary_sections/figures.tex:439` — `width=\textwidth` -> `width=0.73\textwidth`
  - `Supplementary_Information_LaTeX_Source/supplementary_sections/figures.tex:439` — same
- **Regenerated:** yes (same command as above)
- **Synced to submission tree:** yes
- **After:** native 6.0/6.5 pt, scale 1.002 -> print 6.01-6.52 pt (PASS). Printed width 116 mm (58 mm per panel).

### Fig_R1_1A_winner_loser_OD.pdf
- **Before:** print 4.70-8.64 pt (FAIL — `OD$_{600}$` subscript at 4.70 pt, titles at 8.64 pt)
- **Lever:** (b) script fonts only; LaTeX width unchanged at `0.9\textwidth`
- **Edits** (`Figure_revision/R1_1_OD_density/analyze_OD_density.py`):
  - `:74` — `mpl.rcParams['font.size'] = 8` -> `6.5`
  - `:245` — in-panel binomial annotation `fontsize=6` -> `6.5`
  - `:247` — medium titles `fontsize=9` -> `7`
  - `:251`, `:253` — `'Loser OD$_{600}$'` -> `'Loser OD600'`, `'Winner OD$_{600}$'` -> `'Winner OD600'`
- **Regenerated:** yes — `cd Figure_generate/code && MPLBACKEND=Agg /Users/jysong/miniforge3/bin/python Figure_revision/R1_1_OD_density/analyze_OD_density.py`
- **Synced to submission tree:** yes
- **After:** native 6.5/7.0 pt -> print 6.15-6.63 pt (PASS)

### Fig_R1_1C_pairwise_corr_vs_OD.pdf
- **Before:** print 3.09-8.46 pt (FAIL — eight native tiers spanning 3.29-9.0 pt, ratio 2.74; admissible
  include-width interval formally empty, so harmonisation in-script was mandatory)
- **Lever:** (b) script fonts only; LaTeX width unchanged at `\textwidth`
- **Edits** (`analyze_OD_density.py`):
  - `:74` — base `font.size` 8 -> 6.5 (shared with Fig_R1_1A above)
  - `:363-367` — tertile annotation text `f'OD$_{{600}}$ = {lo}-{hi}'` -> `f'{lo}-{hi}'`. Keeping the
    `OD600 =` prefix at a legal size would have made the three per-panel labels overlap; the OD identity is
    now carried by the row label and the row-2 x-axis label (see below).
  - `:411` — tertile range text `fontsize=4.7` -> `6.5`
  - `:415` — legend `fontsize=6` -> `6.5`
  - `:418` — medium titles `fontsize=9` -> `7`
  - `:434` — in-panel Low/Mid/High labels `fontsize=5.5` -> `6.5`
  - `:453` — Spearman annotation `fontsize=6` -> `6.5`
  - `:460` — `r'Parental community OD$_{600}$'` -> `'Parental community OD600'`
  - `:467-470` — row labels `fontsize=8` -> `7`, retitled `'OD tertiles'` -> `'Parental OD600 tertiles'` and
    `'Per-event OD'` -> `'Per-event parental OD600'`
- **Regenerated:** yes (same command as Fig_R1_1A)
- **Synced to submission tree:** yes
- **After:** native 6.5/7.0 pt -> print 6.09-6.55 pt (PASS). Checked the rendered PNG: no label collisions;
  the enlarged tertile-range labels clear each other, and the top-left legend clears the bars.

### Fig_R3_3_sim_parent_norm_asymmetry.pdf
- **Before:** print 4.03-6.90 pt (FAIL — native span 5.6-9.6 pt = 1.71x, not rescalable)
- **Lever:** (b) script fonts only; canvas kept at `figsize=(8.7, 2.7)`, LaTeX width unchanged at `\textwidth`
- **Edits** (`Figure_revision/R3_2_richness_mu_model/analyze_sim_parent_norm_asymmetry.py`):
  - `:14` — added `import matplotlib.ticker as mticker`
  - `:33-40` — **local** rcParams overrides after the `common_setup` import (`common_setup.py` NOT touched):
    `font.size = LABEL_PT = 8.5`, `axes.titlesize = PANEL_PT = 9.0` (was inherited `font.size=8` +
    `'large'` = 9.6 for the A/B/C panel letters)
  - `:42-59` — new `_apply_plain_log_ticks(axis, style)` helper; applied to the panel A y-axis (`:180`,
    plain style -> `0.8 0.9 1 2`) and the panel B y-axis (`:212`, sci style -> `1e1 1e3 … 1e11`).
    **Why:** log tick labels were `10^n` mathtext, whose exponent renders at 0.7x the mantissa. That is a
    hard 1.43x internal span, wider than the 1.4x legal band, so *no* combination of font size and include
    width can make `10^n` ticks compliant. Plain / e-notation text keeps every glyph full size.
  - `:183`, `:215` — `r"sub-community $\|n\|_2$"` -> `"sub-community L2 norm"`,
    `r"parental $\|n\|_2$ fold difference"` -> `"parental L2-norm fold difference"` (same 0.7x subscript problem)
  - `:184`, `:208`, `:216`, `:239` — legends `fontsize=6` -> `LABEL_PT`, PDI annotation `fontsize=6.5` -> `LABEL_PT`
- **Regenerated:** yes — `cd Figure_generate/code && MPLBACKEND=Agg /Users/jysong/miniforge3/bin/python Figure_revision/R3_2_richness_mu_model/analyze_sim_parent_norm_asymmetry.py`
- **Synced to submission tree:** yes
- **After:** native 8.5/9.0 pt, scale 0.719 -> print 6.11-6.47 pt (PASS). PNG checked: enlarged legends still
  sit clear of the data in all three panels.

### invasion_fitness_supp.pdf  (generated as `invasion_fitness_analysis.pdf`, renamed on copy)
- **Before:** print 4.16-7.44 pt (FAIL — native span 5.6-10 pt = 1.79x, not rescalable)
- **Lever:** both
- **Edits** (`Figure_revision/R2_4_invasion_fitness/analyze_invasion_fitness.py`):
  - `:48` — `mpl.rcParams['font.size'] = 8` -> `7.5`
  - `:276`, `:284`, `:305` — in-panel annotations and legend `fontsize=6` -> `6.5`
  - `:286-289` — `r'Invasion fitness $\lambda_i$'` / `$\lambda_j$` -> `'Invasion fitness λ (species i)'` /
    `'(species j)'` (Unicode lambda at full size; the mathtext `i`/`j` subscripts were 5.6 pt native = 4.16 pt print)
  - `:291`, `:308`, `:319` — panel letters A/B/C `fontsize=10` -> `7.5`
  - `latex/supplementary_sections/figures.tex:431` — `width=0.85\textwidth` -> `width=\textwidth`
  - `Supplementary_Information_LaTeX_Source/supplementary_sections/figures.tex:431` — same
- **Regenerated:** yes — `cd Figure_generate/code && MPLBACKEND=Agg /Users/jysong/miniforge3/bin/python Figure_revision/R2_4_invasion_fitness/analyze_invasion_fitness.py`
- **Synced to submission tree:** yes (copied `invasion_fitness_analysis.pdf` -> `supplementary_figs/invasion_fitness_supp.pdf`
  in both trees, matching the existing SI filename)
- **After:** native 6.5/7.0/7.5 pt, scale 0.887 -> print 5.76-6.65 pt (PASS)

---

## Verification

```
cd Figure_generate/Draft/v5
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py marginal_distributions
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py boundary_sensitivity
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py Fig_R1_1A
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py Fig_R1_1C
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py Fig_R3_3
/Users/jysong/miniforge3/bin/python figure_format_campaign/verify_figures.py invasion_fitness_supp
```
All 8 report `PASS` for size and `OK` for colour. The eight PDFs are md5-identical between
`latex/supplementary_figs/` and `.../Supplementary_Information_LaTeX_Source/supplementary_figs/`.

---

## Blocked / not fixed

### Fig_R1_1B_OD_vs_PDI.pdf — NOT actioned (not in the WS-E assignment; needs an owner)
`analyze_OD_density.py` (my script) contains a Fig_R1_1B block, **but the `Fig_R1_1B_OD_vs_PDI.pdf`
currently in the SI was not produced by it**: the SI file is 6.032 x 3.256 in with Type-3 DejaVu-only fonts and
native tiers 4.9 / 6.5 / 7.0 pt, whereas this script's block emits a 150 x 55 mm Arial figure with tiers
4.9 / 6.0 / 7.0 / 8.0 / 9.0 pt. Its true generator is elsewhere (SI copy dated Jul 29, script output dated Jun 16).
I therefore **did not copy** my regenerated `Fig_R1_1B_OD_vs_PDI.pdf` over the SI file — doing so would have
swapped in a visibly different figure under the cover of a formatting campaign.

It remains non-compliant (print 5.09-7.27 pt) and is **not fixable by width alone**: its native span is
4.9-7.0 pt = 1.43x, just over the 1.4x band. Author decision needed on which script is canonical for this
figure before its fonts can be harmonised.

### Correction applied mid-run: no Unicode super/subscripts
The first build of the four `analyze_continuous_similarity.py` figures used `x²` (U+00B2). On the
coordinator's correction — matplotlib writes .notdef for glyphs Arial lacks, and the character then
disappears from the extracted text while the verifier still reports PASS — those labels were rebuilt in
plain ASCII (`x^2`) and the figures regenerated and re-copied.

Every rewritten label was then re-extracted from the shipped PDF with `fitz` and compared character for
character. Result (all present and correct):

| figure | extracted label |
|---|---|
| marginal_distributions_* | `Retention (x^2)` |
| boundary_sensitivity_by_medium | `PDI boundary (x^2 > 0.5)`, `Minimum retention x^2` |
| Fig_R1_1A_winner_loser_OD | `Loser OD600`, `Winner OD600` |
| Fig_R1_1C_pairwise_corr_vs_OD | `Parental community OD600`, `Parental OD600 tertiles`, `Per-event parental OD600` |
| Fig_R3_3_sim_parent_norm_asymmetry | `sub-community L2 norm`, `parental L2-norm fold difference`, ticks `1e1`…`1e11` |
| invasion_fitness_supp | `Invasion fitness λ (species i)` / `(species j)` |

One non-ASCII character was introduced deliberately and survives verification: **U+03BB (λ)** in
`invasion_fitness_supp`, replacing the mathtext `$\lambda_i$`. It is a base-line Greek letter, not a
super/subscript, Arial contains it, it extracts exactly as `Invasion fitness λ (species i)`, and it renders
correctly in the PNG. The same figure already carried μ from pre-existing mathtext. Everything else in these
six figures is ASCII apart from pre-existing full-size mathtext glyphs (π, −, ≥, ρ, μ), all of which were
confirmed present in the extracted text.

### Note on mathtext (applies to several figures above)
Four separate labels had to be rewritten as literal text (`x²`, `OD600`, `λ (species i)`, `L2 norm`, and the
`10^n` log ticks) because matplotlib renders mathtext sub/superscripts at exactly 0.7x the base size — a fixed
1.43x internal span that exceeds the 1.4x width of the 5-7 pt band. Any figure that mixes a mathtext
sub/superscript with full-size text at the same font size is unfixable by rescaling, by construction.

---

## Side effects

Each `analyze_*.py` runs a full analysis and rewrites other artefacts in its own source directory. None of
these are referenced by `figures.tex`, and **none were copied into either SI tree**:

- `R2_3_continuous_similarity/`: `scatter_retention_vs_PDI`, `marginal_distributions_by_medium`,
  `scatter_by_medium`, `bray_curtis_similarity`, `threshold_sensitivity` (.svg/.pdf/.png each), plus the
  .svg/.png siblings of the four SI figures. Their fonts also shifted with the script-wide `font.size` change.
  A stale `marginal_distributions_by_medium.pdf` exists in both SI figure folders but is not `\includegraphics`d
  anywhere; left untouched.
- `R1_1_OD_density/`: `Fig_R1_1B_OD_vs_PDI.{pdf,svg,png}` rewritten in the source dir only (see Blocked above),
  plus .svg/.png siblings of 1A and 1C.
- `R3_2_richness_mu_model/`: `sim_parent_norm_vectors.csv`, `sim_parent_norm_events.csv`,
  `sim_parent_norm_summary.csv` and the .png rewritten (values reproduced identically).
- `R2_4_invasion_fitness/`: `invasion_fitness_distributions.{svg,pdf,png}` and the .svg/.png siblings of the
  main figure rewritten.

No changes to `common_setup.py`, `pdf.fonttype`, or font family. All numeric results printed by the four
scripts reproduce the previously reported values.
