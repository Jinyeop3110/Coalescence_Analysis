# Critique Summary & Fixes Applied

Date: 2026-04-15 (updated)

## Overview

10 critique agents reviewed all Phase 1–4 work. Critical and high-priority fixes have been applied. This document summarizes what was found, what was fixed, and what remains as recommendations for the response letter framing.

---

## FIXES APPLIED

### Code Fixes (all scripts)

| Script | Fix | Status |
|--------|-----|--------|
| R3-1 additive null | Replaced duplicated functions with canonical imports from `common_setup.py` (removed `+1e-30` epsilon divergence) | DONE |
| R3-1 additive null | Removed dead code (`FancyArrowPatch`, `MEDIUM_LABELS`) | DONE |
| R3-1 additive null | Fixed all `fontsize=7` → `fontsize=8` | DONE |
| R3-1 additive null | Added panel labels (a), (b), (c) to multi-panel figures | DONE |
| R1-1 OD density | Replaced deprecated `binom_test` → `binomtest().pvalue` | DONE |
| R1-1 OD density | Added `pdf.fonttype=42`, `ps.fonttype=42`, tick width rcParams | DONE |
| R1-1 OD density | Added failure counter for silent exception handler | DONE |
| R1-1 OD density | Applied `>1e-4` threshold to `c_mix` consistently | DONE |
| R1-2 pH dominance | Added `pdf.fonttype=42`, `ps.fonttype=42` | DONE |
| R1-2 pH dominance | Fixed Wilson CI (was Wald) — implemented actual Wilson formula | DONE |
| R1-2 pH dominance | Added `np.random.seed(42)` for jitter reproducibility | DONE |
| R1-3 PDI no dominant | Removed dead `calculate_assymetricity_direction` function | DONE |
| R1-3 PDI no dominant | Added failure counter and explanatory comments to exception handlers | DONE |
| R1-3 PDI no dominant | Added `np.random.seed(42)` | DONE |
| R1-3 PDI no dominant | Added explicit comment that R² is on reflection-duplicated data | DONE |
| R1-3 PDI no dominant | Increased marker size `s=4` → `s=12` | DONE |
| R3-2b richness-mu | Replaced duplicated functions with canonical imports | DONE |
| R3-2b richness-mu | Added `np.random.seed(42)` | DONE |
| R3-2b richness-mu | Fixed stale module docstring (said "Dirichlet" but uses composition shuffling) | DONE |
| R2-3 continuous similarity | Replaced `os.chdir` hack with `sys.path.insert` | DONE |
| R2-3 continuous similarity | Added explanatory comment for reimplemented `get_abundance` | DONE |
| R2-3 continuous similarity | Added `np.random.seed(42)` | DONE |
| R1-4 pool size | Fixed error bar comment "Wilson" → "Wald" | DONE |
| R1-7 interaction matrix | Removed dead code (TwoSlopeNorm, I_random, cc_list, unused COLORMAP imports) | DONE |
| R1-7 interaction matrix | Added `np.random.seed(42)` | DONE |
| R1-7 interaction matrix | Fixed hardcoded `range(4)` → derived from data | DONE |
| R1-7 interaction matrix | Fixed double-title issue on Panel A/B | DONE |

### Text Fixes (LaTeX)

| File | Fix | Status |
|------|-----|--------|
| results.tex | Removed "We emphasize" → direct statement; added specific examples (pH, cross-feeding, carrying capacity) | DONE |
| results.tex | Removed redundant last sentence in natural communities section | DONE |
| discussion.tex | Changed "We note that" → direct statement in alternative mechanisms paragraph | DONE |
| discussion.tex | Replaced "per se" and "surf" with formal phrasing | DONE |
| discussion.tex | Fixed "internally compatible" → "mutually weakly competing" | DONE |
| discussion.tex | Changed "single-axis control" → "simplified scalar proxy" | DONE |
| discussion.tex | Softened unsupported "abundance-controlled" claim | DONE |
| supplementary_methods.tex | Reconciled "<15% variation" claim with softened results.tex language | DONE |

---

## REMAINING RECOMMENDATIONS — STATUS

All recommendations have been implemented in code. Items below are marked DONE.
Framing for the response letter remains pending (Phase 6).

### R1-1 OD density — DONE
- ~~Consider multivariate model controlling for medium/pool size~~ → **Added** multivariate logistic `Dominance ~ relDeltaOD + Medium + PoolSize`
- Response letter framing: separate two findings clearly — (1) OD difference predicts Dominance frequency (moderate effect); (2) denser parent does NOT win (strong negative, 26.8%)

### R1-2 pH dominance — DONE
- ~~Simpson's paradox concern: present medium-stratified results as primary~~ → **Added** medium-stratified Fisher exact tests (printed per medium)
- ~~Consider multivariate logistic with Medium and PoolSize~~ → **Added** multivariate logistic `Dominance ~ deltaPH + Medium + PoolSize`
- Response letter framing: pH is weak predictor (ρ=0.15), likely downstream marker of composition; stratified results show aggregate p=0.012 may be driven by LN having 0 different-pH events

### R1-3 PDI circularity — DONE
- ~~Consider top-K sensitivity analysis (remove 1, 2, 3 species)~~ → **Added** top-K for K=1,2,3; new figure `Fig_R1_3_topK_sensitivity`
- ~~Bar chart mixed pairwise-assay R² (K=0) with VD-only R² (K=1,2,3)~~ → **Redesigned** as 2-panel figure: Panel 1 = pairwise-assay R² for K=0 and K=1 (consistent with Fig 5C); Panel 2 = VD-only direction agreement for K=1,2,3
- Response letter framing: R² drop 0.34→0.07 is near-complete collapse; frame honestly, with direction preservation (≈68%) as secondary finding

### R3-1 Additive null — DONE
- ~~Consider mixing-ratio sweep (α * n_A + (1-α) * n_B)~~ → **Added** sweep over α∈[0,1] (21 steps); new figure `fig9_mixing_ratio_sweep`
- Response letter framing: result is mathematically expected (additive null at α=0.5 trivially classifies as Mixing); connect to ED Fig. 3 permutation null

### R3-2a Richness — DONE
- ~~Critical gap: logistic regression `Dominance ~ richness + medium`~~ → **Added** 4-model logistic (medium-only, richness-only, richness+medium, Shannon+medium)
- ~~Add Shannon diversity as second metric~~ → **Added** `compute_shannon()` and Shannon+medium model
- Response letter framing: connect R3-2a, R3-2b, R3-1 in manuscript text as a unified richness confound story

### R3-2b Richness-mu — DONE
- ~~Add bootstrap CIs on null curve~~ → **Added** Wilson 95% CI on null Dominance fraction; CI band shown in Panel B
- Response letter framing: null model tests richness+unevenness jointly (composition shuffling, not Dirichlet); note that observed Dominance >> null at high μ is the key finding

### R1-7 Interaction matrix — DONE
- ~~No statistical test~~ → **Added** Mann-Whitney U test for within vs between community interaction strengths
- Response letter framing: block structure interpretation = within < between means competitive release after assembly, not internal cohesion

### R2-3 Continuous similarity — DONE
- ~~Missing threshold sensitivity sweep~~ → **Added** sweep over [0.0001, 0.001, 0.01, 0.033]; new figure `threshold_sensitivity`
- Response letter framing: Bray-Curtis should be elevated from afterthought to co-primary metric alongside cosine similarity

### Phase 1 Text — DONE
- ~~Verify Duan2025 citation~~ → **Confirmed** Reviewer 2 cited the Pawar-group bioRxiv (Duan Q, Harcombe W, Savage V, Mustri M, Smith TP, Pawar S). Added `DuanPawar2025` to references.bib. Existing `Duan2025` (Duan/Bueno/Dai, Nat Eco Evo) retained separately.

---

## Scripts that need re-running after fixes

All scripts with code changes should be re-run to regenerate figures:
- R3-1 (imports changed, fontsize changed, panel labels added; **+mixing-ratio sweep fig9**)
- R1-1 (threshold, deprecation, rcParams; **+multivariate logistic regression**)
- R1-2 (Wilson CI, rcParams, seed; **+multivariate logistic + medium-stratified Fisher**)
- R1-3 (marker size, dead code, seed; **+top-K sensitivity analysis fig_topK**)
- R3-2b (imports changed, seed, docstring; **+Wilson CI bands on null curve**)
- R2-3 (chdir hack, seed; **+threshold sensitivity sweep fig_thresh**)
- R1-7 (dead code, hardcoded range, titles, seed; **+Mann-Whitney U test + significance bracket**)
- R3-2a (**+Shannon diversity + logistic regression Dominance~richness+medium**)
- R1-4 (comment fix only — no visual change, re-run optional)

## Code additions — 2026-04-15 (Round 1)

| Script | Addition |
|--------|----------|
| R1-1 | Added multivariate logistic regression `Dominance ~ relDeltaOD + Medium + PoolSize` |
| R1-2 | Added multivariate logistic `Dominance ~ deltaPH + Medium + PoolSize`; medium-stratified Fisher exact tests |
| R1-3 | Added top-K sensitivity analysis (K=1,2,3): R² and direction agreement after removing top-K species; new figure `Fig_R1_3_topK_sensitivity` |
| R3-1 | Added mixing-ratio sweep (α∈[0,1], 21 steps): new figure `fig9_mixing_ratio_sweep` |
| R3-2a | Added `compute_shannon()`; 4-model logistic regression (medium-only, richness-only, richness+medium, Shannon+medium) |
| R3-2b | Added Wilson 95% CI on null Dominance fraction; `fill_between` CI band in Panel B |
| R1-7 | Added `from scipy import stats`; Mann-Whitney U test for within vs between; significance bracket on Panel C boxplot |
| R2-3 | Added threshold sensitivity sweep [0.0001, 0.001, 0.01, 0.033]; new figure `threshold_sensitivity` |
| references.bib | Added `DuanPawar2025` (Duan/Harcombe/Savage/Mustri/Smith/Pawar, bioRxiv 2025) — paper actually cited by Reviewer 2. Existing `Duan2025` retained. |

## Bug fixes — 2026-04-15 (Round 2, critical review)

Six bugs discovered and fixed during a post-implementation audit:

| # | Script | Bug | Fix |
|---|--------|-----|-----|
| 1 | R3-1 additive null | Dead vestigial inner loop iterating `df` inside the `for alpha in alphas:` block — assigned to unused local vars (`sid`, `sid_sub1 = event["obs_class"]`, `n_A_vec`) | Removed all 4 lines |
| 2 | R3-1 additive null | `medium_labels_short` had L↔M swapped (`"L": "MN (Base)"`, `"M": "LN (Nutr$-$)"`) — L=Low Nutrients should map to LN | Fixed: `{"L": "LN (Nutr$-$)", "M": "MN (Base)", "H": "HN (Nutr$+$)"}` |
| 3 | R3-2a richness media | `Processed_sequences_synthetic` spuriously imported from `common_setup` — not needed; `asv_data` already loaded directly | Removed from import list |
| 4 | R3-2b richness-mu | `N_BOOTSTRAP = 200` defined but never used — Wilson CI (not bootstrap) was actually computed | Removed variable; updated comment to say "Wilson CI" |
| 5 | R1-7 interaction matrix | Significance bracket anchor used `max(np.max(within_means), np.max(between_means))` — ignores `showfliers=False`, bracket floats above visible plot | Fixed: `whisker_top = max(Q3 + 1.5*IQR)` for each group to match actual boxplot extent |
| 6 | R1-3 PDI no dominant | Original bar chart mixed pairwise-assay R² (K=0, from `data_orig`) with VD-only R² (K=1,2,3) — apples-to-oranges comparison | Redesigned as 2-panel figure: Panel 1 = pairwise-assay R² for K=0,1; Panel 2 = VD-only direction agreement for K=1,2,3 |
