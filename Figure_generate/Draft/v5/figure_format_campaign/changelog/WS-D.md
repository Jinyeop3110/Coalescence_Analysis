# Workstream D — timeseries panels, phylogeny, pairwise matrices, interaction matrix

**Agent run:** 2026-08-01
**Scripts owned:**
- `Figure_generate/code/generate_fig1_1.py`
- `Figure_generate/code/build_phylogeny.py`
- `Figure_generate/code/plot_pairwise_matrix_dynamics_improved.py`
- `Figure_generate/code/Figure_revision/R1_7_interaction_matrix/plot_interaction_matrix.py`

**Result: 8/8 figures PASS text size, 8/8 PASS colour (all DeviceRGB). Nothing blocked.**

| figure | before | after |
|---|---|---|
| `Fig_1-3_timeseries_Nutr-_ex1_merged.pdf` | 11.30-13.18 | **5.64-6.58** |
| `Fig_1-3_timeseries_Nutr-_ex2_merged.pdf` | 11.29-13.17 | **5.64-6.58** |
| `Fig_1-3_timeseries_Nutr+_ex1_merged.pdf` | 12.56-14.65 | **5.66-6.60** |
| `Fig_1-3_phylogeny_tree.pdf` | 3.31-5.67 | **5.72-6.67** |
| `Pairwise_Matrix_Dynamics_LN_improved.pdf` | 2.94-6.86 | **5.83-6.32** |
| `Pairwise_Matrix_Dynamics_MN_improved.pdf` | 2.94-6.86 | **5.83-6.32** |
| `Pairwise_Matrix_Dynamics_HN_improved.pdf` | 2.94-6.86 | **5.83-6.32** |
| `interaction_matrix_post_assembly.pdf` | 3.58-6.22 | **5.85-6.22** |

No LaTeX include width was changed, so `supplementary_sections/figures.tex` is untouched in
both trees. All fixes are lever (b), in the generating scripts.

---

## Changes made

### timeseries_merged/Fig_1-3_timeseries_{Nutr-_ex1, Nutr-_ex2, Nutr+_ex1}_merged.pdf

- **Before:** 11.30-13.18 / 11.29-13.17 / 12.56-14.65 pt (FAIL, all TOO_LARGE). A 38 mm-wide
  native design blown up ~1.9x into a 72-80 mm slot.
- **Lever:** (b) script — canvas enlarged, font sizes left at 6/7 pt.
- **Edits:**
  - `generate_fig1_1.py:45-52` — new constants `SI_MERGED_FIGSIZE_045 = (72*mm, 49.5*mm)` and
    `SI_MERGED_FIGSIZE_050 = (80.5*mm, 55.3*mm)` (original aspect 32:22 preserved).
  - `generate_fig1_1.py:438-449` — `plot_timeseries_merged(...)` gained a
    `figsize=(32*mm, 22*mm)` keyword (the original value) plus a docstring note.
  - `generate_fig1_1.py:498` — `plt.figure(figsize=(32*mm, 22*mm))` -> `plt.figure(figsize=figsize)`.
  - `generate_fig1_1.py:726, 759, 896` — the three SI call sites now pass
    `figsize=SI_MERGED_FIGSIZE_045` / `SI_MERGED_FIGSIZE_050`.
  - The canvas sizes were solved for empirically: native width grows as
    `0.2951 + 0.03759 * figsize_mm` inches under `bbox_inches='tight'`; two iterations
    landed scale at 0.940/0.944.
- **Deliberately NOT changed:** the three `Base_ex*` merged panels use the same function but are
  not in the SI (they feed the main-text Fig. 1 composite). They keep the default 32 x 22 mm
  canvas and were verified byte-for-pixel identical after regeneration.
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python generate_fig1_1.py`
- **Synced to submission tree:** yes.
- **After:** 5.64-6.58 / 5.64-6.58 / 5.66-6.60 pt (PASS). Panel layout unchanged (verified by
  400 dpi render).

### Fig_1-3_phylogeny_tree.pdf

- **Before:** 3.31-5.67 pt (FAIL, TOO_SMALL). Native sizes 7/8/10/12 span 1.71x, above the 1.4x
  band, so fonts had to be harmonised regardless of include width.
- **Lever:** (b) script fonts.
- **Edits:**
  - `build_phylogeny.py:20-26` — new `LEAF_LABEL_PT = 12`, `TITLE_PT = 14` with a comment
    explaining the 0.9\textwidth reduction.
  - `build_phylogeny.py:296-297` — leaf labels `fontsize=8` -> `LEAF_LABEL_PT`.
  - `build_phylogeny.py:349-350` — right-hand ASV-ID labels `fontsize=7` -> `LEAF_LABEL_PT`.
  - `build_phylogeny.py:356-357` — xlabel `fontsize=10` -> `LEAF_LABEL_PT`, plus a new
    `ax.tick_params(axis='x', labelsize=LEAF_LABEL_PT)` (the x tick labels were previously
    inheriting 8 pt and would have been left behind at 3.8 pt print).
  - `build_phylogeny.py:358-359` — title `fontsize=12` -> `TITLE_PT`.
  - `build_phylogeny.py:327-331` — bar-to-ID-column gap `+ 0.005` -> `+ 0.013` (see below).
- **Collision fix:** at 12 pt the deepest leaf label, `ASV1 (Lactococcus)`, overran its abundance
  bar and collided with its own ASV-ID label. Widening only the gap between the bars and the ID
  column (a 0.008 data-unit spacing constant, ~1.2% of the axis) cleared it. Bar positions,
  topology and all other content are unchanged; verified against the baseline render.
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/envs/coalescence/bin/python build_phylogeny.py`
  (the `coalescence` env is the one with Biopython; the miniforge base python has no `Bio`).
  The NJ tree rebuild is deterministic — topology is identical to the baseline figure.
- **Synced to submission tree:** yes.
- **After:** 5.72-6.67 pt (PASS). All 50 leaf rows legible, no overlaps (110 dpi full render +
  500 dpi zoom on the ASV1 row).

### Pairwise_Matrix_Dynamics_{LN,MN,HN}_improved.pdf

- **Before:** 2.94-6.86 pt (FAIL). Native sizes 6/8/9/10/11/12/14 span 2.33x — far outside the
  1.4x band.
- **Lever:** (b) script fonts. `figsize` was left at `(14, 12)`; the enlarged text raised the
  tight-bbox native width only from 11.511 to 11.610 in, so scale barely moved (0.4900 -> 0.4859).
- **Edits** (all in `plot_pairwise_matrix_dynamics_improved.py`):
  - `:35-41` — new `BODY_PT = 12`, `HEAD_PT = 13` constants, declared before the rcParams block.
  - `:47` — `'font.size': 8` -> `BODY_PT`.
  - `:222` diagonal species labels `10` -> `BODY_PT`; `:235` no-data em-dash `10` -> `BODY_PT`.
  - `:274` x tick labels `['0','T']` `6` -> `BODY_PT`; `:284` y tick labels `['0','','1']` `6` -> `BODY_PT`.
  - `:292` column titles `8` -> `BODY_PT`; `:297` row labels `8` -> `BODY_PT`.
  - `:305` 'Legend' `12` -> `HEAD_PT`; `:317`/`:335` legend entries `9` -> `BODY_PT`;
    `:320`/`:338` legend titles `10` -> `HEAD_PT`.
  - `:370` pie autopct `11` -> `BODY_PT`; `:379` pie legend `9` -> `BODY_PT`;
    `:386` 'Outcome Distribution' `12` -> `HEAD_PT`; `:395` suptitle `14` -> `HEAD_PT`.
  - `:376-380` — the pie's category legend moved from `loc='upper left', bbox_to_anchor=(-0.1, 1.0)`
    to `loc='upper center', bbox_to_anchor=(0.5, -0.02)`.
- **Collision fix:** the pie legend already grazed the wedges at 9 pt; at `BODY_PT` it sat squarely
  on top of the pie. It now sits below the pie, in the `ax_info` panel row that the script
  already leaves deliberately empty. No gridspec or data change.
- **Regenerated:** yes — `cd Figure_generate/code && /Users/jysong/miniforge3/bin/python plot_pairwise_matrix_dynamics_improved.py`
  (regenerates .svg/.png/.pdf for all three media; all six extra files also synced).
- **Synced to submission tree:** yes (pdf + png + svg).
- **After:** 5.83-6.32 pt (PASS). The 12x12 grid of tick labels does NOT collide at 12 pt native —
  the inter-cell gap is ~19 pt against ~8 pt labels. Verified at 130 dpi full render.

### interaction_matrix_post_assembly.pdf

- **Before:** 3.58-6.22 pt (FAIL). Included at 0.82\textwidth, scale 0.7316.
- **Lever:** (b) script fonts + mathtext removal.
- **Edits** (all in `Figure_revision/R1_7_interaction_matrix/plot_interaction_matrix.py`):
  - `:47-56` — new `BODY_PT = 8.0`, `HEAD_PT = 8.5` constants with the mathtext rationale.
  - `:20` — added `import matplotlib.transforms as mtransforms`.
  - `:121` ylabel `7` -> `BODY_PT`; `:123` matrix note `5.6` -> `BODY_PT`.
  - `:265` 'Rep. N' title `7.5` -> `BODY_PT`; `:268`/`:270` panel letters `8.5` -> `HEAD_PT`.
  - `:274-275` colourbar label `7` -> `BODY_PT` and tick `labelsize=6` -> `BODY_PT`.
  - `:306` significance stars `8` -> `BODY_PT`; `:309` x tick labels `7` -> `BODY_PT`;
    `:310` ylabel `7` -> `BODY_PT`; `:319` panel C title `8.5` -> `HEAD_PT`;
    `:320` y tick `labelsize=7` -> `BODY_PT`.
  - `:313-318` 'pool mean' `5.5` -> `BODY_PT`, and repositioned (see below).
- **Mathtext removed:** `r'Interaction coefficient $\alpha_{ij}$'` and `r'Mean $\alpha_{ij}$'`
  rendered `ij` at 0.7x base — 4.9 pt native, 3.58 pt print, and unfixable at any width because
  a mathtext subscript alone spans 1/0.7 = 1.4286 > the 1.40 band. Both are now literal
  full-size strings: `'Interaction coefficient αij'` and `'Mean αij'`.
- **Collision fix:** at 8 pt the grey 'pool mean' annotation became ~1 data unit wide and ran over
  the 'Between' box, which straddles the pool-mean line. It is now anchored to the left edge of
  panel C with a blended transform (axes fraction in x, data in y) and sits in clear whitespace.
- **Regenerated:** yes — `cd Figure_generate/code/Figure_revision/R1_7_interaction_matrix && /Users/jysong/miniforge3/bin/python plot_interaction_matrix.py`
- **Synced to submission tree:** yes. Note the script writes `interaction_matrix_assembly.pdf`;
  the SI filename is `interaction_matrix_post_assembly.pdf`, and both trees were updated under
  that name.
- **After:** 5.85-6.22 pt (PASS).

---

## Coordinator correction on Unicode — actioned

The coordinator warned mid-run that Unicode super/subscripts (U+207B, U+2080-2089) are absent from
Arial, that matplotlib emits `.notdef` for them, and that the character then vanishes from the PDF
while still scoring PASS.

**Checked, and my rewrite is clean.** The only non-ASCII character I introduced is U+03B1
(GREEK SMALL LETTER ALPHA), not a sub/superscript form. Extracting the regenerated PDF with fitz
returns, character for character:

```
'Interaction coefficient αij'   font=ArialMT   size=8.0
'Mean αij'                      font=ArialMT   size=8.0
```

i.e. the exact strings passed to matplotlib, rendered in Arial itself with no fallback and no
dropped glyph. The `ij` is full-size ASCII. I re-ran the same extraction over all eight of my
regenerated PDFs; the other seven are pure ASCII. No ASCII-only redo was needed.

## Side effects

- `generate_fig1_1.py` has no partial entry point, so the full `main()` ran and rewrote every
  file under `Figure_generate/code/Figure/Fig1_1_Plots/`. I diffed all regenerated PDFs against a
  pre-run backup at 150 dpi: **only my three target files changed**; every other output
  (composition diagrams, taxonomy colormap, the 30 individual `timeseries/` panels, the three
  `Base_ex*` merged panels) is pixel-identical.
- `build_phylogeny.py` also rewrites `Data/phylogeny_{sequences.fasta, metadata.tsv, colors.tsv,
  distances.xlsx}` and `Figure/Fig1_1_Plots/phylogeny_tree.newick` (deterministic, same content).
- `build_phylogeny.py:387-392` still hard-codes a copy to `Draft/v3/latex/supplementary_figs/`,
  a tree that no longer exists. Running it re-creates a stub `Draft/v3/` directory. I deleted the
  stub and copied to the two v5 trees by hand rather than edit a path outside this campaign's
  remit. **Recommend the coordinator repoint that path to v5** in a follow-up.
- `plot_pairwise_matrix_dynamics_improved.py` and `plot_interaction_matrix.py` each also emit
  .svg/.png siblings, which were regenerated. The pairwise .svg/.png were synced to both trees
  (they exist there); `interaction_matrix_*.svg/.png` exist only in the code tree.
- `plot_interaction_matrix.py` also regenerates `interaction_matrix_mu_comparison.{pdf,svg,png}`.
  That figure is not in the SI and I left its font sizes untouched.

## Observations for the coordinator (not actioned)

- **Pre-existing dropped em-dash in the pairwise matrices.** `plot_pairwise_matrix_dynamics_improved.py`
  writes U+2014 in the suptitle (`'... Invasion Assays — Nutr-'`) and in the no-data cells. It
  **renders correctly** but does not survive text extraction — fitz returns
  `'Pairwise Species 95:5 Invasion Assays '`. This is true of the baseline PDF as well, so it is
  not a regression, and it is a Type 3 ToUnicode artifact rather than a missing glyph (this script
  emits Type 3, which is out of campaign scope). It does mean the verifier slightly undercounts
  characters for these three figures. No compliance impact: every remaining glyph is 12 or 13 pt.
- **Pre-existing pie autopct overlap** in the pairwise figures: for LN the `13%` and `2%` wedge
  labels overlap each other because the bistability wedge is 1/61. Identical in the baseline;
  fixing it needs a label-placement decision by the author.
- `plot_pairwise_matrix_dynamics_improved.py` emits Type 3 fonts. Noted, not touched, per scope.
