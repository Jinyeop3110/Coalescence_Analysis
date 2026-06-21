# Q5 — pH-feedback alternative framework

This directory contains a non-gLV alternative coalescence simulator based on
the Gore lab's pH-feedback framework. Its purpose is to address internal
memo Q5: to show that a genuine alternative organising framework — one
that is not a reparameterisation of pairwise gLV — reproduces the
coalescence outcome taxonomy (Dominance / Mixture / Restructuring) and
supplies a winner-direction axis that the baseline gLV does not have.

## Framework

The ODE is an original-code-like pH-feedback model adapted from the public
Ratzke simulation code for a coalescence setting without explicit daily
serial dilution. In a community of species with densities n_i and shared
proton-concentration coordinate p,

    g_i(p)  = exp(−(p − p_o_i)^2 / (2 p_c^2))
    dn_i/dt = n_i (1 − n_i) [g_i(p)(k_growth + k_death) − k_death]
    dp/dt   = K Σ_i c_i n_i + λ_dil (p_fresh − p)

with original-code-like parameters: p_o_i ~ U(4.5, 9.5), p_c=2.5,
k_growth=10, k_death=10, K=1e10, and c_i ~ U(-interaction_strength,
interaction_strength). The additive relaxation term replaces the original
daily dilution and partial reset of p toward 7; p_fresh=7. Species i is an
"acidifier" if c_i > 0 and an "alkalinizer" if c_i < 0.

## Interaction-strength knob (analogue of μ)

In the pairwise gLV the tunable scalar μ is the mean off-diagonal
interaction magnitude. Here the analogue is |c|/σ — pH-modification
magnitude divided by pH tolerance. Ratzke, Barrere & Gore 2020
(Nat. Ecol. Evol. 4:376-383) established experimentally that **nutrient
concentration sets |c|**, which is exactly the knob (nutrients, LN → HN)
our paper tunes. The convenience function `scale_interaction_strength`
in `pH_feedback_model.py` multiplies |c| by a dimensionless `tension`
factor. Since the code sets the baseline `DEFAULT_C_MAG = 1e-10`, the
public-code interaction-strength grid maps to `tension =
interaction_strength / 1e-10`, i.e. `0, 1, 10, 100, 1e4, 1e5, 1e6,
1e8`. These are designed to be qualitatively analogous
to the μ = 0.3 / 0.6 / 0.8 sweep used in the gLV simulator at
`Figure_generate/code/Figure_revision/R3_3_nonCompetitive_gLV/`; the
mapping is not numerically 1-to-1 and calibration against a figure is a
follow-up task (see Limitations).

## File tree

- `pH_feedback_model.py` — core ODE RHS, species-pool sampling, pool
  assembly, coalescence, classification.
- `simulate_pH_coalescence.py` — thin driver; sweeps pH-tension, writes
  `pH_feedback_results.json` in the same schema as the gLV simulator.
- `environmental_filter_model.py` — trait-based environmental-filtering
  null model; species have latent traits and each nutrient condition applies
  a Gaussian niche filter. The current Q5b calibration fixes the filter
  center and breadth (`theta=0`, `sigma=1`) and varies only the strength
  exponent `gamma` to match observed P12 coalesced richness.
- `simulate_Q5_phase_environmental_filter.py` — writes event-level records
  for the filtering null to `Q5_phase_events_filter.csv`.
- `make_Q5_phase_environmental_filter.py` — renders
  `Fig_Q5_phase_filter.{pdf,png,svg}` in the same layout as the Q5 phase
  figures for gLV and pH feedback.
- `test_sanity.py` — biomass + pH bounds, steady state, shape parity
  with common_setup, monotonicity of tension knob.
- `README.md` — this file.

## Output schema

`pH_feedback_results.json` mirrors
`../R3_3_nonCompetitive_gLV/non_competitive_results.json`:

```
{
  "parameters": { ... },
  "results": {
    "pH_tau=1.00": {
      "regime": "pH_feedback",
      "pH_tension": 1.00,
      "interaction_strength": 1e-10,
      "n_events": ..., "rejects": ...,
      "frac_Dominance": ..., "frac_Mixture": ...,
      "frac_Restructuring": ...,
      "psc_phi": ...
    },
    "pH_tau=10.00": {...},
    "pH_tau=100.00": {...}
  }
}
```

## Running

```
cd Figure_generate/code/Figure_revision/Q5_pH_feedback_model
python test_sanity.py          # confirm correctness
python simulate_pH_coalescence.py
```

The demo sweep (24 species / pool, 12 species / parent, 2 parents / pool,
40 pools per tension, 3 tensions) takes a few minutes on a laptop.

## Sources

1. Ratzke C, Gore J. "Modifying and reacting to the environmental pH can
   drive bacterial interactions." *PLoS Biology* 16(3):e2004248 (2018).
   DOI: 10.1371/journal.pbio.2004248. Main-text Eqs. 1-2 + S1 Text.
2. Ratzke C, Barrere J, Gore J. "Strength of species interactions
   determines biodiversity and stability in microbial communities."
   *Nat. Ecol. Evol.* 4:376-383 (2020).
   DOI: 10.1038/s41559-020-1099-4. Nutrient → |c| → interaction strength.
3. Ratzke C, Denk J, Gore J. "Ecological suicide in microbes."
   *Nat. Ecol. Evol.* 2:867-872 (2018). Single-species version of the ODE.

## Limitations and open calibration questions

- The pH-pref distribution is U(2, 8) and σ is U(2, 5). These ranges are
  reasonable relative to the paper's p ∈ [0, 10] and σ ≈ 4, but they are
  not calibrated to the actual 12-isolate pH phenotype distribution from
  the Gore lab experiments (that would need per-isolate growth-vs-pH
  fits).
- All species share the same |c| (up to sign). A more realistic pool
  would draw |c_i| from a distribution; adding this is a one-line change
  in `sample_species_pool` once we know the distribution.
- The tension knob is defined here as a pure scaling of |c|. In the
  full Ratzke-Barrere-Gore framework, nutrient concentration also scales
  the effective K and the absolute growth rate. Including a nutrient-K
  coupling is a natural extension for a Q5 figure that quantitatively
  overlays tension onto μ.
- Coalescence here mixes parent abundances 50/50 and re-integrates from
  the neutral p0=5 starting pH. An alternative is to take the
  pre-coalescence parents' own final p as the mixed initial condition
  — this choice affects whether coalescence is "memory-free" (neutral
  start) or "environment-inherited". We use the neutral start to mirror
  the experimental dilution into fresh medium.
- I could not fetch the S1 Text of Ratzke & Gore 2018 directly (server
  403 on the figshare/PLOS storage link); I used the main-text equations
  verified from the PMC HTML render. The form is consistent across
  Ratzke 2018, Ratzke-Denk-Gore 2018, and Ratzke-Barrere-Gore 2020, so
  this is low-risk, but worth sanity-checking against the PDF when
  available.
