#!/usr/bin/env python
"""
R3-2b: Richness vs mu in gLV Model — Geometric Null Model Comparison

This script addresses Reviewer 3's concern that increasing interaction strength
mu simply kills species (lower richness), and that Dominance is geometrically
easier at low richness.

We compare the observed Dominance fraction to a composition-shuffling geometric
null model.  For each trial at a given mu the null model samples two observed
steady-state abundance vectors, randomly permutes species identities in each
vector independently (preserving abundance unevenness while breaking species-
specific correlations), averages them to simulate coalescence, and classifies
the outcome.

If Dominance_observed >> Dominance_null(richness(mu)), then the ecological
mechanism goes beyond simple geometric effects of reduced richness.

Data source: existing simulation JSON from 200reps_fine (24 mu values, 200 reps).
"""

import os
import sys
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ─── Path setup ───────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.insert(0, CODE_DIR)

from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
)
from COLORMAP import (
    PHASE_DIAGRAM_COLORS,
    get_phase_diagram_colors,
    SECONDARY_COLORS,
)

# ─── Figure style ─────────────────────────────────────────────────────────────
sns.set_style("ticks")
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.4
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.4
mpl.rcParams['ytick.major.width'] = 0.5
plt.rcParams['text.usetex'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

mm = 0.1 / 2.54  # mm to inches conversion factor


# ─── Helper functions ─────────────────────────────────────────────────────────
# normalize, metric_VectorDecomposition_onlyPositive, calculate_assymetricity,
# and characterize_case are imported from common_setup above.


def count_richness(abundance_vec, threshold=1e-3):
    """Count number of species with abundance above threshold."""
    return int(np.sum(np.array(abundance_vec) > threshold))


def classify_coalescence(c1, c2, cmix):
    """Classify a coalescence event into Dominance/Mixture/Restructuring."""
    try:
        u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
        x, y = calculate_assymetricity(u, v, k)
        return characterize_case(x, y)
    except (np.linalg.LinAlgError, ZeroDivisionError):
        return None


# ─── Geometric null model ────────────────────────────────────────────────────

def geometric_null_from_observed(observed_compositions, n_samples=5000,
                                  total_species=48):
    """
    Composition-matched geometric null model.

    Uses the actual observed abundance distributions from gLV simulations,
    but randomly shuffles species identities. This preserves the unevenness
    of real communities while breaking the species-specific correlations
    created by ecological assembly.

    For each trial:
      1. Sample two observed composition vectors (from the same mu).
      2. Randomly permute species labels in each vector independently.
      3. Average the two permuted vectors to simulate coalescence.
      4. Classify the outcome.

    If observed Dominance >> null Dominance, the ecological structure of
    species identities (not just composition shape) drives the outcome.

    Parameters
    ----------
    observed_compositions : list of ndarray
        List of observed steady-state abundance vectors at a given mu.
    n_samples : int
        Number of Monte Carlo samples.
    total_species : int
        Length of the abundance vector.

    Returns
    -------
    fractions : dict
        {'dominance': float, 'mixing': float, 'restructuring': float}
    """
    counts = {0: 0, 1: 0, 2: 0}
    n_obs = len(observed_compositions)
    if n_obs < 2:
        return {'dominance': 0.0, 'mixing': 0.0, 'restructuring': 0.0}

    for _ in range(n_samples):
        # Sample two observed compositions
        i, j = np.random.choice(n_obs, size=2, replace=False)
        vec_a = np.array(observed_compositions[i]).copy()
        vec_b = np.array(observed_compositions[j]).copy()

        # Randomly permute species identities independently
        perm_a = np.random.permutation(total_species)
        perm_b = np.random.permutation(total_species)
        vec_a_shuffled = vec_a[perm_a]
        vec_b_shuffled = vec_b[perm_b]

        # Coalesce by averaging
        vec_mix = (vec_a_shuffled + vec_b_shuffled) / 2.0

        # Classify
        cls = classify_coalescence(vec_a_shuffled, vec_b_shuffled, vec_mix)
        if cls is not None:
            counts[cls] += 1

    total = sum(counts.values())
    if total == 0:
        return {'dominance': 0.0, 'mixing': 0.0, 'restructuring': 0.0}

    return {
        'dominance': counts[0] / total,
        'mixing': counts[1] / total,
        'restructuring': counts[2] / total,
    }


# ─── Main analysis ───────────────────────────────────────────────────────────

def main():
    np.random.seed(42)

    # Load simulation data (200 reps, 24 mu values)
    data_path = os.path.join(
        CODE_DIR,
        'Simulation_Data',
        '48species_200reps_fine',
        'Community_200reps_fine.json',
    )
    print(f"Loading simulation data from:\n  {data_path}")
    with open(data_path, 'r') as f:
        sim_data = json.load(f)

    mu_values = sorted(sim_data.keys(), key=float)
    print(f"Found {len(mu_values)} mu values: {mu_values[0]} to {mu_values[-1]}")
    print(f"Reps per mu: {len(sim_data[mu_values[0]])}")

    # ── Step 1: Compute richness and outcome fractions per mu ─────────────
    results = {}

    for mu_key in mu_values:
        mu = float(mu_key)
        reps = sim_data[mu_key]

        sc_richness_all = []
        cc_richness_all = []
        outcomes_all = []

        for rep_key, rep_data in reps.items():
            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            # Richness of assembled sub-communities
            for sc_key, sc_vec in sc_list.items():
                sc_richness_all.append(count_richness(sc_vec))

            # Coalescence outcomes and richness
            for cc_key, cc_vec in cc_list.items():
                cc_richness_all.append(count_richness(cc_vec))

                # Get parent communities
                parts = cc_key.split('_')
                c1_vec = sc_list[parts[0]]
                c2_vec = sc_list[parts[1]]

                cls = classify_coalescence(c1_vec, c2_vec, cc_vec)
                if cls is not None:
                    outcomes_all.append(cls)

        n_total = len(outcomes_all)
        dom_frac = outcomes_all.count(0) / n_total if n_total > 0 else 0
        mix_frac = outcomes_all.count(1) / n_total if n_total > 0 else 0
        res_frac = outcomes_all.count(2) / n_total if n_total > 0 else 0

        results[mu] = {
            'sc_richness': sc_richness_all,
            'cc_richness': cc_richness_all,
            'mean_sc_richness': np.mean(sc_richness_all),
            'std_sc_richness': np.std(sc_richness_all),
            'mean_cc_richness': np.mean(cc_richness_all),
            'dominance_frac': dom_frac,
            'mixing_frac': mix_frac,
            'restructuring_frac': res_frac,
            'n_events': n_total,
        }

        print(f"  mu={mu:.2f}: mean SC richness={np.mean(sc_richness_all):.1f}, "
              f"Dom={dom_frac:.3f}, Mix={mix_frac:.3f}, Res={res_frac:.3f}")

    # ── Step 2: Composition-matched geometric null model with bootstrap CIs ──
    print("\nComputing composition-matched geometric null model...")
    print("  (Preserves abundance unevenness, shuffles species identities)")
    N_NULL_SAMPLES = 5000   # null samples per mu (each is a Bernoulli trial)

    null_results = {}
    for mu in sorted(results.keys()):
        # Collect all observed sub-community compositions at this mu
        observed_comps = []
        mu_key_str = f"{mu:.2f}"
        for rep_key, rep_data in sim_data[mu_key_str].items():
            for sc_key, sc_vec in rep_data['sc_list'].items():
                observed_comps.append(np.array(sc_vec))

        null_fracs = geometric_null_from_observed(
            observed_comps, n_samples=N_NULL_SAMPLES, total_species=48
        )

        # Bootstrap CI: resample null outcomes to estimate sampling uncertainty
        # Each null sample is a Bernoulli trial (Dominance=1 or not=0)
        # We use binomial CI (Wilson) on n=N_NULL_SAMPLES, k=dom_count
        dom_count = round(null_fracs['dominance'] * N_NULL_SAMPLES)
        z = 1.96
        n = N_NULL_SAMPLES
        p_hat = dom_count / n
        denom = 1 + z**2 / n
        centre = (p_hat + z**2 / (2 * n)) / denom
        margin = (z * np.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))) / denom
        ci_lo = max(0.0, centre - margin)
        ci_hi = min(1.0, centre + margin)

        null_results[mu] = {**null_fracs, 'ci_lo': ci_lo, 'ci_hi': ci_hi}
        print(f"  mu={mu:.2f}: richness={results[mu]['mean_sc_richness']:.1f}, "
              f"null_Dom={null_fracs['dominance']:.3f} "
              f"[{ci_lo:.3f}, {ci_hi:.3f}], "
              f"null_Mix={null_fracs['mixing']:.3f}")

    # ── Step 3: Prepare plot data ─────────────────────────────────────────
    mu_arr = np.array(sorted(results.keys()))
    mean_sc_rich = np.array([results[mu]['mean_sc_richness'] for mu in mu_arr])
    std_sc_rich = np.array([results[mu]['std_sc_richness'] for mu in mu_arr])
    mean_cc_rich = np.array([results[mu]['mean_cc_richness'] for mu in mu_arr])

    dom_obs = np.array([results[mu]['dominance_frac'] for mu in mu_arr])
    mix_obs = np.array([results[mu]['mixing_frac'] for mu in mu_arr])
    res_obs = np.array([results[mu]['restructuring_frac'] for mu in mu_arr])

    dom_null = np.array([null_results[mu]['dominance'] for mu in mu_arr])
    mix_null = np.array([null_results[mu]['mixing'] for mu in mu_arr])
    res_null = np.array([null_results[mu]['restructuring'] for mu in mu_arr])
    dom_null_lo = np.array([null_results[mu]['ci_lo'] for mu in mu_arr])
    dom_null_hi = np.array([null_results[mu]['ci_hi'] for mu in mu_arr])

    excess_dom = dom_obs - dom_null

    # ── Step 4: Create figures ────────────────────────────────────────────
    phase_colors = get_phase_diagram_colors()
    color_dom = phase_colors[0]
    color_mix = phase_colors[1]
    color_res = phase_colors[2]

    # --- Figure: 3-panel ---
    fig, axes = plt.subplots(1, 3, figsize=(180 * mm, 55 * mm))

    # Panel A: Mean richness vs mu
    ax = axes[0]
    ax.errorbar(mu_arr, mean_sc_rich, yerr=std_sc_rich / np.sqrt(200),
                fmt='o-', color='#1f77b4', markersize=3, linewidth=1,
                label='Sub-community', capsize=2, capthick=0.5, elinewidth=0.5)
    ax.plot(mu_arr, mean_cc_rich, 's-', color='#2ca02c', markersize=3,
            linewidth=1, label='Coalesced')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel('Mean richness')
    ax.legend(fontsize=6, frameon=False)
    ax.set_xlim([0, 1.25])
    ax.set_ylim(bottom=0)
    ax.set_title('A', fontsize=10, fontweight='bold', loc='left')
    sns.despine(ax=ax)

    # Panel B: Dominance fraction — observed vs geometric null
    ax = axes[1]
    ax.plot(mu_arr, dom_obs, 'o-', color=color_dom, markersize=3,
            linewidth=1, label='Observed')
    ax.plot(mu_arr, dom_null, 's--', color=color_dom, markersize=3,
            linewidth=1, alpha=0.6, markerfacecolor='white',
            markeredgecolor=color_dom, label='Geometric null')
    ax.fill_between(mu_arr, dom_null, dom_obs, alpha=0.15, color=color_dom)
    # Bootstrap 95% CI on null (Wilson interval)
    ax.fill_between(mu_arr, dom_null_lo, dom_null_hi, alpha=0.25, color=color_dom,
                    linewidth=0, label='Null 95% CI')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel('Dominance fraction')
    ax.legend(fontsize=6, frameon=False)
    ax.set_xlim([0, 1.25])
    ax.set_ylim([0, 1])
    ax.set_title('B', fontsize=10, fontweight='bold', loc='left')
    sns.despine(ax=ax)

    # Panel C: Excess Dominance
    ax = axes[2]
    ax.bar(mu_arr, excess_dom, width=0.04, color=color_dom, alpha=0.7,
           edgecolor='none')
    ax.axhline(0, color='black', linewidth=0.5, linestyle='-')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel('Excess Dominance\n(observed $-$ null)')
    ax.set_xlim([0, 1.25])
    ax.set_title('C', fontsize=10, fontweight='bold', loc='left')
    sns.despine(ax=ax)

    plt.tight_layout()

    # Save
    for ext in ['svg', 'pdf', 'png']:
        out_path = os.path.join(SCRIPT_DIR, f'richness_mu_analysis.{ext}')
        fig.savefig(out_path, bbox_inches='tight', dpi=300)
        print(f"Saved: {out_path}")
    plt.close(fig)

    # --- Supplementary: Stacked phase diagram with null overlay ---
    fig2, axes2 = plt.subplots(1, 2, figsize=(140 * mm, 60 * mm))

    # Panel: Observed stacked
    ax = axes2[0]
    ax.fill_between(mu_arr, 0, dom_obs, color=color_dom, alpha=0.85,
                    label='Dominance')
    ax.fill_between(mu_arr, dom_obs, dom_obs + mix_obs, color=color_mix,
                    alpha=0.85, label='Mixture')
    ax.fill_between(mu_arr, dom_obs + mix_obs, dom_obs + mix_obs + res_obs,
                    color=color_res, alpha=0.85, label='Restructuring')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel('Fraction')
    ax.set_xlim([mu_arr[0], mu_arr[-1]])
    ax.set_ylim([0, 1])
    ax.set_title('Observed', fontsize=8, fontweight='bold')
    ax.legend(fontsize=5, frameon=False, loc='center right')
    sns.despine(ax=ax)

    # Panel: Null stacked
    ax = axes2[1]
    ax.fill_between(mu_arr, 0, dom_null, color=color_dom, alpha=0.85,
                    label='Dominance')
    ax.fill_between(mu_arr, dom_null, dom_null + mix_null, color=color_mix,
                    alpha=0.85, label='Mixture')
    ax.fill_between(mu_arr, dom_null + mix_null,
                    dom_null + mix_null + res_null,
                    color=color_res, alpha=0.85, label='Restructuring')
    ax.set_xlabel(r'Interaction strength $\mu$')
    ax.set_ylabel('Fraction')
    ax.set_xlim([mu_arr[0], mu_arr[-1]])
    ax.set_ylim([0, 1])
    ax.set_title('Geometric null', fontsize=8, fontweight='bold')
    ax.legend(fontsize=5, frameon=False, loc='center right')
    sns.despine(ax=ax)

    plt.tight_layout()

    for ext in ['svg', 'pdf', 'png']:
        out_path = os.path.join(SCRIPT_DIR, f'richness_mu_stacked.{ext}')
        fig2.savefig(out_path, bbox_inches='tight', dpi=300)
        print(f"Saved: {out_path}")
    plt.close(fig2)

    # --- Print summary statistics ---
    print("\n" + "=" * 70)
    print("SUMMARY: Richness vs mu — Geometric Null Model Comparison")
    print("=" * 70)
    print(f"{'mu':>6s}  {'Rich_SC':>8s}  {'Rich_CC':>8s}  {'Dom_obs':>8s}  "
          f"{'Dom_null':>9s}  {'Excess':>8s}")
    print("-" * 60)
    for mu in mu_arr:
        print(f"{mu:6.2f}  {results[mu]['mean_sc_richness']:8.1f}  "
              f"{results[mu]['mean_cc_richness']:8.1f}  "
              f"{results[mu]['dominance_frac']:8.3f}  "
              f"{null_results[mu]['dominance']:9.3f}  "
              f"{results[mu]['dominance_frac'] - null_results[mu]['dominance']:8.3f}")

    # Correlation between excess dominance and mu
    r, p = stats.pearsonr(mu_arr, excess_dom)
    print(f"\nCorrelation (excess Dominance vs mu): r={r:.3f}, p={p:.2e}")

    # Key finding
    mean_excess = np.mean(excess_dom[mu_arr >= 0.3])
    print(f"\nMean excess Dominance for mu >= 0.3: {mean_excess:.3f}")
    print("If positive, ecological mechanism goes BEYOND geometric richness effect.")

    print("\nDone.")


if __name__ == '__main__':
    main()
