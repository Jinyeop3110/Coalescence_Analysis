# P3.2 — pH × Dominance: Acid-Alk Pairs per Medium

## Reviewer: R1, Point #2 (Major)
## Status: COMPLETED (revised 2026-04-20)
## Confidence: High for Nutr+ "acidic parent wins" signal; low for pair-type frequency test

### Reviewer Comment
"Does Dominance become more likely when parents have different pH (acidic vs alkaline) vs same pH?"

### What They Want
A direct test of the pH modification hypothesis: if pH is the key mechanism, then mixing an acidic community with an alkaline one should create a strong selective filter, making Dominance more likely. The analysis did not find significant support for that frequency-level prediction.

### Analysis Plan (current framing)
Script: `Figure_generate/code/Figure_revision/R1_2_pH_dominance/analyze_pH_dominance.py`

Because LN (Nutr−) has no acidic parents, the per-medium analysis is restricted to Base (MN) and Nutr+ (HN). The reviewer's question is addressed in two complementary ways:

1. **Does pH mismatch alone increase Dominance frequency?** Full class distribution (Dominance / Mixing / Restructuring) across three pair types (Acid-Alk, Acid-Acid, Alk-Alk) per medium. Tested with a 2-way Fisher exact test comparing Acid-Alk vs pooled same-pH (Acid-Acid ∪ Alk-Alk).
2. **Within Acid-Alk pairs, does the acidic parent win?** Signed asymmetry = +asymmetry if the acidic parent was the winner (u > v for acidic side), −asymmetry otherwise. Per-medium binomial test (acid wins vs 50%) and one-sample t-test (mean signed asymmetry vs 0).

### Key Results

**Pair-type counts (260 events total)**:
- Acid-Acid: 40 (LN 0, Base 6, Nutr+ 34)
- Acid-Alk: 88 (LN 0, Base 44, Nutr+ 44)
- Alk-Alk: 132 (LN 90, Base 30, Nutr+ 12)

**(1) Pair-type Dominance frequency per medium** (Acid-Alk vs pooled same-pH; 2-way Fisher):
- Base: Acid-Alk 61.4% (27/44) vs same-pH 69.4% (25/36); OR = 0.70, Fisher p = 0.49 (n.s., direction negative)
- Nutr+: Acid-Alk 79.5% (35/44) vs same-pH 71.7% (33/46); OR = 1.53, Fisher p = 0.47 (n.s., direction positive)
- Full class fractions (Dom/Mix/Rest) shown in Response Fig. R1-2 (left, middle).

**(2) Within Acid-Alk pairs — acidic parent wins**:
- Base: 63.6% (28/44), binomial p = 0.10; signed asymmetry = +0.28, one-sample t p = 0.030
- Nutr+: **86.4% (38/44), binomial p = 9.4×10⁻⁷; signed asymmetry = +0.64, one-sample t p = 2.4×10⁻⁸**

### Interpretation for Response
Pair-type alone (Acid-Alk vs same-pH) is not a strong predictor of Dominance frequency within either medium. The low power is due to small cell sizes (e.g., Base Acid-Acid n = 6; Nutr+ Alk-Alk n = 12), a Nutr+ ceiling effect where Dominance is already ~70–80% for all pair types, and the fact that binary acid/alk classification discards continuous pH information. Dominance frequency is driven by the combined interaction landscape, not by pH mismatch alone.

The frequency-level test requested by the reviewer is negative: pH mismatch does not significantly increase Dominance frequency within either Base or Nutr+. The directional test is narrower: within Acid-Alk pairs in Nutr+, the acidic parent is the winner in 38/44 = 86% of events. This supports pH modification as one possible contributor to winner identity in Nutr+, not as a sole or general explanation for Nutr+ Dominance frequency. The signal is weaker in Base, consistent with the more collective nature of Base coalescence (see R1-3).

### Figures Generated
- `Fig_R1_2_acidalk_per_medium.pdf` — 3 panels: (1) Base stacked class fractions by pair type, (2) Nutr+ stacked class fractions by pair type, (3) signed asymmetry for Acid-Alk pairs in Base and Nutr+.
- Previous figures `Fig_R1_2a/b/c` are deprecated and were moved to `revision/deprecated/R1_2_obsolete/`.

### Changes to Manuscript
Added a short paragraph to Results §2.5 (after the ED Fig. 8 discussion):

> "Whereas pH mismatch alone does not significantly increase Dominance frequency, within acid–alk pairs the acidic parent preferentially wins in Nutr+ (38/44 events, p < 10⁻⁶; Supplementary Fig. 36), consistent with acidification as one possible contributor to winner identity under high-nutrient conditions. Thus, pH modification may contribute to winner identity in Nutr+, but pH alone does not explain the observed Nutr+ Dominance pattern."
