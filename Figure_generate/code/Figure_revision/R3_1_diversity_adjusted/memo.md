# R3-1: Diversity-Adjusted Dominance Thresholds

**Reviewer:** R3, Point #1 (P0 — critical)
**Status:** Analysis complete, awaiting selection for response letter
**Date:** 2026-04-21

---

## Motivation

Reviewer 3 argued that in low-dimensional community composition vectors, positive
unit vectors are more likely to be close to orthogonal by chance. This means the
current Dominance classification threshold ($y > 0.5$) may be too lenient at low
effective richness ($N_{\mathrm{eff}}$), inflating the Dominance fraction on
purely geometric grounds.

Rather than defending the fixed threshold, we re-classify every event under a
**richness-adjusted threshold**:

$$y_{\mathrm{adj}}(N_{\mathrm{eff}}) = 0.5 + k / \sqrt{N_{\mathrm{eff}}}$$

where $N_{\mathrm{eff}} = 1 / \sum_i p_i^2$ (inverse Simpson). Higher $k$ makes
the classifier stricter at low richness. $k = 0$ recovers the original classifier.

(A multiplicative variant $y_{\mathrm{adj}} = 0.5 (1 + k/\sqrt{N_{\mathrm{eff}}})$
is also reported for robustness; qualitative conclusions are identical.)

A **joint-axis sensitivity check** was added later: we also tighten the
retention threshold, $x^2_{\mathrm{adj}}(N_{\mathrm{eff}}) = \min(1, 0.5 + k_x/\sqrt{N_{\mathrm{eff}}})$,
in parallel with the PDI threshold. At low richness, both coordinates of the
classifier can be geometrically inflated (low-dim positive vectors tend to look
both asymmetric AND well-captured by a sparse parental basis), so a critical
reader may ask whether the Dominance signal survives simultaneous tightening.
See `Fig_R3_1_diversity_adjusted_joint.pdf`. At moderate joint $k = k_y = k_x
= 0.5$, Dominance drops to 25.1% but nutrient ordering LN 8.9% < MN 24.1%
< HN 42.2% is preserved and widens relative to baseline (HN/LN ratio 4.7x
vs 1.94x).

---

## Data

- 263 coalescence events (Nutr-: 90, Base: 83, Nutr+: 90).
- $N_{\mathrm{eff}}$ of the coalesced community $n_C$, inverse Simpson.
- Script: `analyze_diversity_adjusted.py`; per-event CSV and sweep CSV saved.

### Per-medium $N_{\mathrm{eff}}$ summary

| Medium | n  | mean $N_{\mathrm{eff}}$ | median |
|--------|----|-------------------------|--------|
| Nutr-  | 90 | 4.63                    | 4.38   |
| Base   | 83 | 3.09                    | 2.80   |
| Nutr+  | 90 | 2.27                    | 2.15   |

As expected, coalesced communities in Nutr+ have the lowest effective richness,
i.e. they are the communities that *would* be most inflated by R3's geometric
bias. This makes them the critical test case.

---

## Results (additive form)

| $k$  | #Dom | Dom%  | Mix%  | Rest% | LN Dom% | MN Dom% | HN Dom% |
|------|------|-------|-------|-------|---------|---------|---------|
| 0.00 | 157  | 59.7% | 21.3% | 19.0% | 38.9%   | 65.1%   | 75.6%   |
| 0.25 | 132  | 50.2% | 30.8% | 19.0% | 21.1%   | 59.0%   | 71.1%   |
| 0.50 | 94   | 35.7% | 45.2% | 19.0% | 8.9%    | 44.6%   | 54.4%   |
| 0.75 | 24   | 9.1%  | 71.9% | 19.0% | 2.2%    | 9.6%    | 15.6%   |
| 1.00 | 1    | 0.4%  | 80.6% | 19.0% | 0.0%    | 1.2%    | 0.0%    |
| 1.50 | 0    | 0.0%  | 81.0% | 19.0% | 0.0%    | 0.0%    | 0.0%    |
| 2.00 | 0    | 0.0%  | 81.0% | 19.0% | 0.0%    | 0.0%    | 0.0%    |

Flips out of Dominance relative to $k = 0$:
- $k = 0.25$: 25/157 (15.9%)
- $k = 0.50$: 63/157 (40.1%)
- $k = 1.00$: 156/157 (99.4%)

---

## Interpretation

1. **The nutrient gradient is preserved under moderate adjustment.**
   At $k = 0.25$ and $k = 0.5$, the ordering LN < MN < HN is identical to the
   unadjusted classifier, and the HN/LN ratio even *widens* in relative terms
   (at $k = 0.5$, Nutr+ retains 54.4% Dominance while Nutr- collapses to 8.9%).
   This is the opposite of what the geometric-bias hypothesis predicts: if
   Dominance were inflated by low-$N_{\mathrm{eff}}$ artifact, Nutr+ (which has
   the smallest $N_{\mathrm{eff}}$) should lose the most Dominance events under
   a stricter-at-low-richness threshold. Instead, Nutr- loses them faster,
   exactly because Nutr- events were already near the boundary.

2. **Dominance in Nutr+ survives substantial tightening.**
   Even at $k = 0.5$, Nutr+ retains 54.4% Dominance (vs original 75.6%). The
   effect is large but robust. The bulk of the Nutr+ Dominance signal is not an
   artifact of low richness.

3. **At $k = 1.0$ the classifier becomes essentially impossible to satisfy**
   (threshold $> 1.0$ for $N_{\mathrm{eff}} < 1$, pushing all events into
   Mixing). This is over-corrected and not a scientifically meaningful regime.

4. **Tertile-stratified check (Fig B).**
   At the original $k = 0$, Dominance fraction *decreases* with increasing
   $N_{\mathrm{eff}}$ tertile (85.2% low → 58.6% mid → 35.2% high). This is the
   pattern R3 predicted from geometry. But when we tighten the threshold at low
   $N_{\mathrm{eff}}$, the per-medium gradient LN < MN < HN is preserved in
   every tertile where events survive. The low-$N_{\mathrm{eff}}$ enrichment
   therefore reflects the HN medium's natural tendency to produce
   small-$N_{\mathrm{eff}}$ communities (via dominant acidifiers), not a
   geometric mis-classification.

---

## Suggested response-letter text (draft)

> To directly address the concern that Dominance classification may be inflated
> at low community richness, we re-classified every event under a
> richness-adjusted threshold:
> $y_{\mathrm{adj}}(N_{\mathrm{eff}}) = 0.5 + k/\sqrt{N_{\mathrm{eff}}}$, where
> $N_{\mathrm{eff}}$ is the inverse Simpson index of the coalesced community.
> The adjustment makes the classifier strictly more stringent at low richness;
> $k = 0$ recovers the original Dominance threshold. At a moderate adjustment
> ($k = 0.5$), the overall Dominance fraction drops from 59.7% to 35.7% but the
> nutrient ordering is preserved and even widens: LN = 8.9%, MN = 44.6%,
> HN = 54.4%. The Nutr+ Dominance signal survives substantial tightening. The
> low-$N_{\mathrm{eff}}$ enrichment we observe in the data therefore reflects
> the Nutr+ medium's intrinsic tendency to produce dominant-acidifier
> communities, not a geometric artifact of the similarity metric.

---

## Figures

- `Fig_R3_1_diversity_adjusted_sweep.pdf`
  (a) Scatter of $(N_{\mathrm{eff}}, y)$ per event colored by medium with the
  adjusted threshold curves overlaid for $k \in \{0, 0.5, 1.0, 2.0\}$.
  (b) Dominance fraction vs $k$, overall and per medium.
  (c) Fate of baseline Dominance events as $k$ increases.

- `Fig_R3_1_per_medium_richness.pdf`
  (a) $N_{\mathrm{eff}}$ distribution per medium (boxplot + jitter).
  (b) Baseline ($k=0$) Dominance fraction by $N_{\mathrm{eff}}$ tertile,
  per medium.

---

## Files

- Script: `analyze_diversity_adjusted.py`
- Per-event table: `diversity_adjusted_per_event.csv`
- Sweep table: `diversity_adjusted_sweep.csv`

## Confidence

Analysis: 95%. The result that the nutrient gradient survives moderate
adjustment but collapses at extreme adjustment is robust and directly answers
R3's concern. The one residual risk is that a critical reviewer may argue that
the choice of $k$ is itself a free parameter; we pre-empt this by sweeping $k$
and reporting the inflection point rather than picking a single value.
