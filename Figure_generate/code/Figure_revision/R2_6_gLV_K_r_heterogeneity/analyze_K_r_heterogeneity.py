#!/usr/bin/env python3
"""
K/r heterogeneity stress test for the gLV OD-direction failure mode.

Question
--------
Can simple species-level heterogeneity in carrying capacity (K_i) or intrinsic
growth rate (r_i) make a competition-only random-alpha gLV reproduce the
experimental "denser parent loses" pattern, while preserving the interaction-
strength dependent increase in Dominance?

This script runs a focused sweep:
    K_sd, r_sd in {0, 0.5, 1.0}
    mu in {0.3, 0.6, 0.8}

K_i and r_i are sampled from Normal(1, sd^2) truncated to positive values.
The output is a JSON event table, a summary CSV, and two memo-ready figures.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.integrate import solve_ivp

SCRIPT_DIR = Path(__file__).resolve().parent
CODE_DIR = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(CODE_DIR))
os.chdir(CODE_DIR)

from COLORMAP import PHASE_DIAGRAM_COLORS
from common_setup import (
    calculate_assymetricity,
    characterize_case,
    metric_VectorDecomposition_onlyPositive,
    mm,
)

sns.set_style("ticks")
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["font.size"] = 8
mpl.rcParams["axes.linewidth"] = 0.5
mpl.rcParams["xtick.direction"] = "in"
mpl.rcParams["ytick.direction"] = "in"
mpl.rcParams["xtick.major.width"] = 0.5
mpl.rcParams["ytick.major.width"] = 0.5
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
plt.rcParams["text.usetex"] = False

OUTCOME_LABEL = {0: "Dominance", 1: "Mixing", 2: "Restructuring"}
OUTCOME_COLOR = {
    0: PHASE_DIAGRAM_COLORS["dominance"],
    1: PHASE_DIAGRAM_COLORS["mixing"],
    2: PHASE_DIAGRAM_COLORS["restructuring"],
}


@dataclass
class SimConfig:
    n_species: int = 48
    n_communities: int = 4
    species_per_community: int = 12
    reps: int = 100
    mu_values: tuple[float, ...] = (0.3, 0.6, 0.8)
    sd_values: tuple[float, ...] = (0.0, 0.5, 1.0)
    t_end: float = 2000.0
    extinction_threshold: float = 1e-3


def canonical_seed(mu: float, rep: int) -> int:
    """Seed used by run_48species_100reps_final.py."""
    return int(mu * 1000) + rep * 10000 + 12345


def positive_normal(rng: np.random.Generator, mean: float, sd: float, size: int) -> np.ndarray:
    """Sample Normal(mean, sd^2) values by rejection, preserving positivity."""
    if sd == 0:
        return np.full(size, mean, dtype=float)
    out = rng.normal(mean, sd, size=size)
    bad = out <= 0
    while bad.any():
        out[bad] = rng.normal(mean, sd, size=bad.sum())
        bad = out <= 0
    return out


def run_glv_ode(y0: np.ndarray, present: np.ndarray, interaction: np.ndarray,
                growth: np.ndarray, carrying: np.ndarray, cfg: SimConfig,
                method: str) -> np.ndarray | None:
    """Run the same finite-time ODE endpoint used by the paper's gLV pipeline."""
    idx = np.where(present)[0].tolist()
    y0_simul = y0[idx]
    interaction_simul = interaction[np.ix_(idx, idx)]
    growth_simul = growth[idx]
    carrying_simul = carrying[idx]

    def rhs(_t: float, y: np.ndarray) -> np.ndarray:
        dydt = np.zeros_like(y)
        for i in range(len(y)):
            dydt[i] = growth_simul[i] * y[i] * (
                1 - np.sum(interaction_simul[i, :] * y) / carrying_simul[i]
            )
        return dydt

    # The exact K_sd=r_sd=0 baseline uses RK45 to match the manuscript pipeline.
    # Heterogeneous K/r cases use LSODA to avoid pathological RK45 runtimes.
    kwargs = {"rtol": 1e-6}
    if method == "LSODA":
        kwargs["atol"] = 1e-9
    sol = solve_ivp(rhs, [0, cfg.t_end], y0_simul, method=method, **kwargs)
    if (not sol.success) or sol.y.size == 0:
        return None
    y_final = sol.y[:, -1]
    if not np.all(np.isfinite(y_final)):
        return None
    out = np.zeros_like(y0)
    for i, species_idx in enumerate(idx):
        out[species_idx] = y_final[i]
    return out


def initialize_species_pool_canonical(rng: np.random.RandomState, mu: float, cfg: SimConfig) -> np.ndarray:
    """Match initialize_species_pool() in run_48species_100reps_final.py."""
    interaction = np.zeros((cfg.n_species, cfg.n_species))
    for i in range(cfg.n_species):
        for j in range(cfg.n_species):
            interaction[i, j] = 2.0 * mu * rng.random_sample()
    np.fill_diagonal(interaction, 1.0)
    return interaction


def initialize_communities_canonical(rng: np.random.RandomState, cfg: SimConfig) -> np.ndarray:
    """Match initialize_random_communities() in run_48species_100reps_final.py."""
    communities = np.zeros((cfg.n_communities, cfg.n_species), dtype=bool)
    species = rng.permutation(cfg.n_species)
    for i in range(cfg.n_communities):
        start = i * cfg.species_per_community
        stop = start + cfg.species_per_community
        communities[i, species[start:stop]] = True
    return communities


def canonical_ecology(mu: float, rep: int, cfg: SimConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the interaction matrix, community masks, and y seed from the canonical pipeline."""
    rng = np.random.RandomState(canonical_seed(mu, rep))
    interaction = initialize_species_pool_canonical(rng, mu, cfg)
    communities = initialize_communities_canonical(rng, cfg)
    y_seed = rng.rand(cfg.n_species) * 0.1
    return interaction, communities, y_seed


def kr_seed(mu: float, k_sd: float, r_sd: float, rep: int) -> int:
    return (
        canonical_seed(mu, rep)
        + int(k_sd * 100) * 1_000_000
        + int(r_sd * 100) * 10_000_000
        + 531_977
    )


def simulate_one_rep(mu: float, k_sd: float, r_sd: float, rep: int, cfg: SimConfig) -> list[dict]:
    interaction, communities, y_seed = canonical_ecology(mu, rep, cfg)
    kr_rng = np.random.default_rng(kr_seed(mu, k_sd, r_sd, rep))
    growth = positive_normal(kr_rng, 1.0, r_sd, cfg.n_species)
    carrying = positive_normal(kr_rng, 1.0, k_sd, cfg.n_species)
    ode_method = "RK45" if (k_sd == 0 and r_sd == 0) else "LSODA"

    parents = {}
    for i in range(cfg.n_communities):
        y0 = np.zeros(cfg.n_species)
        y0[communities[i]] = y_seed[communities[i]]
        parents[i] = run_glv_ode(y0, communities[i], interaction, growth, carrying, cfg, ode_method)
        if parents[i] is None:
            return []
        parents[i][parents[i] < cfg.extinction_threshold] = 0

    records = []
    for i in range(cfg.n_communities):
        for j in range(i + 1, cfg.n_communities):
            c1 = parents[i]
            c2 = parents[j]
            y0 = 0.5 * (c1 + c2)
            survived = y0 > cfg.extinction_threshold
            cmix = run_glv_ode(y0, survived, interaction, growth, carrying, cfg, ode_method)
            if cmix is None:
                continue
            cmix[cmix < cfg.extinction_threshold] = 0

            try:
                u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
            except Exception:
                continue
            x_val, y_val = calculate_assymetricity(u, v, k)
            outcome = characterize_case(x_val, y_val)
            if outcome is None:
                continue

            biom1 = float(c1.sum())
            biom2 = float(c2.sum())
            denom = u + v
            pdi = float(u / denom) if denom > 0 else np.nan
            winner = 1 if u > v else 2
            winner_biomass = biom1 if winner == 1 else biom2
            loser_biomass = biom2 if winner == 1 else biom1

            records.append({
                "mu": mu,
                "k_sd": k_sd,
                "r_sd": r_sd,
                "rep": rep,
                "pair": f"{i}_{j}",
                "seed": canonical_seed(mu, rep),
                "outcome": int(outcome),
                "u": float(u),
                "v": float(v),
                "k": float(k),
                "x": float(x_val),
                "y": float(y_val),
                "pdi": pdi,
                "biomass_1": biom1,
                "biomass_2": biom2,
                "delta_biomass": biom1 - biom2,
                "winner": winner,
                "winner_biomass": float(winner_biomass),
                "loser_biomass": float(loser_biomass),
                "winner_denser": bool(winner_biomass > loser_biomass),
            })
    return records


def simulate_task(args: tuple[float, float, float, int, SimConfig]) -> list[dict]:
    mu, k_sd, r_sd, rep, cfg = args
    return simulate_one_rep(mu, k_sd, r_sd, rep, cfg)


def simulate(cfg: SimConfig, workers: int = 1) -> pd.DataFrame:
    all_records = []
    tasks = [
        (mu, k_sd, r_sd, rep, cfg)
        for k_sd in cfg.sd_values
        for r_sd in cfg.sd_values
        for mu in cfg.mu_values
        for rep in range(cfg.reps)
    ]
    total = len(tasks)
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(simulate_task, task) for task in tasks]
            for done, future in enumerate(as_completed(futures), start=1):
                all_records.extend(future.result())
                if done % 20 == 0 or done == total:
                    print(f"  progress {done}/{total}", flush=True)
        return pd.DataFrame(all_records)

    done = 0
    for k_sd in cfg.sd_values:
        for r_sd in cfg.sd_values:
            for mu in cfg.mu_values:
                print(f"[simulate] K_sd={k_sd:.2f} r_sd={r_sd:.2f} mu={mu:.2f}", flush=True)
                for rep in range(cfg.reps):
                    all_records.extend(simulate_one_rep(mu, k_sd, r_sd, rep, cfg))
                    done += 1
                    if done % 50 == 0 or done == total:
                        print(f"  progress {done}/{total}", flush=True)
    return pd.DataFrame(all_records)


def summarize(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (k_sd, r_sd, mu), sub in events.groupby(["k_sd", "r_sd", "mu"]):
        row = {
            "k_sd": k_sd,
            "r_sd": r_sd,
            "mu": mu,
            "n_events": len(sub),
        }
        for outcome, label in OUTCOME_LABEL.items():
            row[f"{label.lower()}_fraction"] = float((sub["outcome"] == outcome).mean())

        dom = sub[sub["outcome"] == 0].copy()
        row["n_dominance"] = len(dom)
        if len(dom):
            n_denser = int(dom["winner_denser"].sum())
            row["winner_denser_count"] = n_denser
            row["winner_denser_fraction"] = float(n_denser / len(dom))
            row["winner_denser_binom_p"] = float(stats.binomtest(n_denser, len(dom), 0.5).pvalue)
        else:
            row["winner_denser_count"] = 0
            row["winner_denser_fraction"] = np.nan
            row["winner_denser_binom_p"] = np.nan

        valid = sub.dropna(subset=["delta_biomass", "pdi"])
        if len(valid) >= 3:
            rho, pval = stats.spearmanr(valid["delta_biomass"], valid["pdi"])
            row["delta_biomass_pdi_spearman_rho"] = float(rho)
            row["delta_biomass_pdi_spearman_p"] = float(pval)
        else:
            row["delta_biomass_pdi_spearman_rho"] = np.nan
            row["delta_biomass_pdi_spearman_p"] = np.nan
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["k_sd", "r_sd", "mu"])


def make_phase_figure(summary: pd.DataFrame, outdir: Path) -> None:
    fig, axes = plt.subplots(4, 4, figsize=(170 * mm, 150 * mm), sharex=True, sharey=True)
    sd_values = sorted(summary["k_sd"].unique())
    r_values = sorted(summary["r_sd"].unique())
    for row_i, k_sd in enumerate(sd_values):
        for col_i, r_sd in enumerate(r_values):
            ax = axes[row_i, col_i]
            sub = summary[(summary["k_sd"] == k_sd) & (summary["r_sd"] == r_sd)]
            for outcome, label in OUTCOME_LABEL.items():
                y_col = f"{label.lower()}_fraction"
                ax.plot(
                    sub["mu"],
                    sub[y_col],
                    marker="o",
                    ms=3,
                    lw=1.0,
                    color=OUTCOME_COLOR[outcome],
                    label=label if row_i == 0 and col_i == 0 else None,
                )
            ax.set_title(f"K sd={k_sd:g}, r sd={r_sd:g}", fontsize=7)
            ax.set_ylim(-0.03, 1.03)
            ax.set_xticks([0.3, 0.6, 0.8])
            if row_i == len(sd_values) - 1:
                ax.set_xlabel(r"$\mu$")
            if col_i == 0:
                ax.set_ylabel("fraction")
            sns.despine(ax=ax)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.01))
    fig.suptitle("K/r heterogeneity: outcome class fractions", y=1.045, fontsize=10)
    fig.tight_layout()
    for ext in ["pdf", "png", "svg"]:
        fig.savefig(outdir / f"Fig_Q6_Kr_phase_trend.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def make_winner_figure(summary: pd.DataFrame, outdir: Path) -> None:
    anchor = summary[summary["mu"].isin([0.3, 0.6, 0.8])].copy()
    anchor["condition"] = anchor.apply(lambda r: f"K{r.k_sd:g}\nr{r.r_sd:g}", axis=1)
    anchor["mean_sd"] = anchor.apply(lambda r: f"K sd={r.k_sd:g}, r sd={r.r_sd:g}", axis=1)

    fig, axes = plt.subplots(1, 3, figsize=(175 * mm, 55 * mm), sharey=True)
    for ax, mu, title in zip(axes, [0.3, 0.6, 0.8], [r"$\mu=0.3$", r"$\mu=0.6$", r"$\mu=0.8$"]):
        sub = anchor[anchor["mu"] == mu].sort_values(["k_sd", "r_sd"])
        x = np.arange(len(sub))
        ax.axhline(0.5, color="black", ls="--", lw=0.7, alpha=0.65)
        colors = [
            plt.cm.viridis((row.k_sd + row.r_sd) / 2.0)
            for row in sub.itertuples()
        ]
        ax.bar(x, sub["winner_denser_fraction"], color=colors, edgecolor="black", linewidth=0.3)
        ax.set_title(title, fontsize=9)
        ax.set_ylim(0, 1)
        ax.set_xticks(x)
        ax.set_xticklabels(sub["condition"], rotation=90, fontsize=5)
        if ax is axes[0]:
            ax.set_ylabel("Dominance events:\nwinner denser fraction")
        sns.despine(ax=ax)
    fig.tight_layout()
    for ext in ["pdf", "png", "svg"]:
        fig.savefig(outdir / f"Fig_Q6_Kr_winner_direction.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def make_medium_variant_zoom_figures(events: pd.DataFrame, outdir: Path) -> None:
    """Make LN/MN/HN memo figures in the same style as the simulation zoom panels."""
    medium_info = [
        (0.3, "LN", r"Nutr$-$  ($\mu=0.3$)"),
        (0.6, "MN", r"Base  ($\mu=0.6$)"),
        (0.8, "HN", r"Nutr$+$  ($\mu=0.8$)"),
    ]
    variant_rows = [
        (0.0, 0.0, "baseline"),
        (0.5, 0.0, r"$K$ sd=0.5"),
        (1.0, 0.0, r"$K$ sd=1.0"),
        (0.0, 0.5, r"$r$ sd=0.5"),
        (0.0, 1.0, r"$r$ sd=1.0"),
        (0.5, 0.5, r"$K,r$ sd=0.5"),
        (1.0, 1.0, r"$K,r$ sd=1.0"),
    ]

    for mu, tag, medium_pretty in medium_info:
        fig, axes = plt.subplots(
            len(variant_rows),
            2,
            figsize=(150 * mm, 38 * mm * len(variant_rows)),
            facecolor="w",
        )

        for row_i, (k_sd, r_sd, row_label) in enumerate(variant_rows):
            sub = events[
                (np.isclose(events["mu"], mu))
                & (np.isclose(events["k_sd"], k_sd))
                & (np.isclose(events["r_sd"], r_sd))
            ].copy()

            ax_a, ax_b = axes[row_i, 0], axes[row_i, 1]
            if sub.empty:
                ax_a.text(0.5, 0.5, "missing", transform=ax_a.transAxes, ha="center", va="center")
                ax_b.text(0.5, 0.5, "missing", transform=ax_b.transAxes, ha="center", va="center")
                continue

            biomass_all = pd.concat([sub["biomass_1"], sub["biomass_2"]], ignore_index=True)
            biom_span = float(biomass_all.max() - biomass_all.min() + 1e-9)
            biom_lo = max(float(biomass_all.min() - 0.02 * biom_span), 0.0)
            biom_hi = float(biomass_all.max() + 0.02 * biom_span)
            d_abs_max = float(np.nanmax(np.abs(sub["delta_biomass"]))) * 1.10
            if d_abs_max == 0:
                d_abs_max = 1.0

            dom = sub[sub["outcome"] == 0].copy()
            ax_a.plot([biom_lo, biom_hi], [biom_lo, biom_hi], "--", color="gray", lw=0.6, alpha=0.7)
            if not dom.empty:
                n_denser = int(dom["winner_denser"].sum())
                n_dom = int(len(dom))
                frac = n_denser / n_dom
                binom_p = stats.binomtest(n_denser, n_dom, 0.5).pvalue
                ax_a.scatter(
                    dom["loser_biomass"],
                    dom["winner_biomass"],
                    s=14,
                    color=OUTCOME_COLOR[0],
                    alpha=0.65,
                    edgecolors="black",
                    linewidths=0.25,
                )
                ax_a.text(
                    0.03,
                    0.97,
                    f"{row_label}\nwinner denser:\n{n_denser}/{n_dom} ({frac:.0%})\n"
                    f"p={binom_p:.2g}",
                    transform=ax_a.transAxes,
                    fontsize=6.2,
                    va="top",
                    ha="left",
                )
            else:
                ax_a.text(0.03, 0.97, f"{row_label}\nno Dominance", transform=ax_a.transAxes,
                          fontsize=6.2, va="top", ha="left")
            ax_a.set_xlim(biom_lo, biom_hi)
            ax_a.set_ylim(biom_lo, biom_hi)
            ax_a.set_aspect("equal", adjustable="box")
            if row_i == 0:
                ax_a.set_title(f"{medium_pretty}: winner vs loser biomass", fontsize=8.5)
            if row_i == len(variant_rows) - 1:
                ax_a.set_xlabel(r"Loser biomass  $\sum_i y_i$", fontsize=7)
            ax_a.set_ylabel(r"Winner biomass", fontsize=7)
            ax_a.tick_params(labelsize=6)
            sns.despine(ax=ax_a)

            valid = sub.dropna(subset=["delta_biomass", "pdi"])
            ax_b.axhline(0.5, color="gray", ls="--", lw=0.5, alpha=0.6)
            ax_b.axvline(0.0, color="gray", ls="--", lw=0.5, alpha=0.6)
            ax_b.axhline(0.75, color="black", ls=":", lw=0.55, alpha=0.7)
            ax_b.axhline(0.25, color="black", ls=":", lw=0.55, alpha=0.7)
            ax_b.scatter(
                -valid["delta_biomass"],
                1.0 - valid["pdi"],
                s=7,
                color="lightgray",
                alpha=0.25,
                linewidths=0,
                zorder=1,
            )
            for outcome_val, label in OUTCOME_LABEL.items():
                m = valid["outcome"] == outcome_val
                if m.any():
                    ax_b.scatter(
                        valid.loc[m, "delta_biomass"],
                        valid.loc[m, "pdi"],
                        s=9,
                        color=OUTCOME_COLOR[outcome_val],
                        alpha=0.68,
                        edgecolors="none",
                        label=label if row_i == 0 else None,
                        zorder=2,
                    )
            if len(valid) >= 3:
                fit = np.polyfit(valid["delta_biomass"], valid["pdi"], 1)
                xs = np.linspace(-d_abs_max, d_abs_max, 100)
                ax_b.plot(xs, fit[0] * xs + fit[1], color="black", lw=0.8, alpha=0.8, zorder=3)
                rho, pval = stats.spearmanr(valid["delta_biomass"], valid["pdi"])
                ax_b.text(
                    0.03,
                    0.97,
                    f"rho={rho:+.2f}, p={pval:.1g}\nslope={fit[0]:+.2f}\nn={len(valid)}",
                    transform=ax_b.transAxes,
                    fontsize=6.2,
                    va="top",
                    ha="left",
                )
            ax_b.set_xlim(-d_abs_max, d_abs_max)
            ax_b.set_ylim(-0.03, 1.03)
            if row_i == 0:
                ax_b.set_title(f"{medium_pretty}: signed $\\Delta$biomass vs PDI", fontsize=8.5)
                ax_b.legend(loc="lower right", fontsize=5.7, frameon=False, handletextpad=0.2)
            if row_i == len(variant_rows) - 1:
                ax_b.set_xlabel(r"biomass$_{\mathrm{Sub1}}-$biomass$_{\mathrm{Sub2}}$", fontsize=7)
            ax_b.set_ylabel(r"PDI $=u/(u+v)$", fontsize=7)
            ax_b.tick_params(labelsize=6)
            sns.despine(ax=ax_b)

        fig.suptitle(f"K/r heterogeneity variants, {medium_pretty}", fontsize=10, y=0.995)
        fig.tight_layout(rect=(0, 0, 1, 0.992))
        for ext in ["pdf", "png", "svg"]:
            fig.savefig(outdir / f"Fig_Q6_Kr_{tag}_sim_variants.{ext}", dpi=300, bbox_inches="tight")
        plt.close(fig)


def draw_zoom_pair(ax_a, ax_b, sub: pd.DataFrame, row_label: str, title_prefix: str,
                   show_xlabel: bool, show_ylabel: bool, show_legend: bool) -> None:
    """Draw the two-panel winner-biomass / signed-biomass-PDI diagnostic."""
    if sub.empty:
        ax_a.text(0.5, 0.5, "missing", transform=ax_a.transAxes, ha="center", va="center")
        ax_b.text(0.5, 0.5, "missing", transform=ax_b.transAxes, ha="center", va="center")
        return

    biomass_all = pd.concat([sub["biomass_1"], sub["biomass_2"]], ignore_index=True)
    biom_span = float(biomass_all.max() - biomass_all.min() + 1e-9)
    biom_lo = max(float(biomass_all.min() - 0.02 * biom_span), 0.0)
    biom_hi = float(biomass_all.max() + 0.02 * biom_span)
    d_abs_max = float(np.nanmax(np.abs(sub["delta_biomass"]))) * 1.10
    if d_abs_max == 0:
        d_abs_max = 1.0

    dom = sub[sub["outcome"] == 0].copy()
    ax_a.plot([biom_lo, biom_hi], [biom_lo, biom_hi], "--", color="gray", lw=0.55, alpha=0.7)
    if not dom.empty:
        n_denser = int(dom["winner_denser"].sum())
        n_dom = int(len(dom))
        frac = n_denser / n_dom
        ax_a.scatter(
            dom["loser_biomass"],
            dom["winner_biomass"],
            s=9,
            color=OUTCOME_COLOR[0],
            alpha=0.65,
            edgecolors="black",
            linewidths=0.2,
        )
        ax_a.text(
            0.03,
            0.97,
            f"{row_label}\n{n_denser}/{n_dom} ({frac:.0%})",
            transform=ax_a.transAxes,
            fontsize=5.2,
            va="top",
            ha="left",
        )
    else:
        ax_a.text(0.03, 0.97, f"{row_label}\nno Dom", transform=ax_a.transAxes,
                  fontsize=5.2, va="top", ha="left")
    ax_a.set_xlim(biom_lo, biom_hi)
    ax_a.set_ylim(biom_lo, biom_hi)
    ax_a.set_aspect("equal", adjustable="box")
    ax_a.set_title(f"{title_prefix}: winner vs loser", fontsize=6.3)
    if show_xlabel:
        ax_a.set_xlabel(r"Loser biomass", fontsize=5.8)
    if show_ylabel:
        ax_a.set_ylabel(r"Winner biomass", fontsize=5.8)
    ax_a.tick_params(labelsize=5)
    sns.despine(ax=ax_a)

    valid = sub.dropna(subset=["delta_biomass", "pdi"])
    ax_b.axhline(0.5, color="gray", ls="--", lw=0.45, alpha=0.6)
    ax_b.axvline(0.0, color="gray", ls="--", lw=0.45, alpha=0.6)
    ax_b.axhline(0.75, color="black", ls=":", lw=0.5, alpha=0.7)
    ax_b.axhline(0.25, color="black", ls=":", lw=0.5, alpha=0.7)
    ax_b.scatter(
        -valid["delta_biomass"],
        1.0 - valid["pdi"],
        s=4,
        color="lightgray",
        alpha=0.22,
        linewidths=0,
        zorder=1,
    )
    for outcome_val, label in OUTCOME_LABEL.items():
        m = valid["outcome"] == outcome_val
        if m.any():
            ax_b.scatter(
                valid.loc[m, "delta_biomass"],
                valid.loc[m, "pdi"],
                s=5,
                color=OUTCOME_COLOR[outcome_val],
                alpha=0.68,
                edgecolors="none",
                label=label if show_legend else None,
                zorder=2,
            )
    if len(valid) >= 3:
        fit = np.polyfit(valid["delta_biomass"], valid["pdi"], 1)
        xs = np.linspace(-d_abs_max, d_abs_max, 100)
        ax_b.plot(xs, fit[0] * xs + fit[1], color="black", lw=0.65, alpha=0.8, zorder=3)
        rho, pval = stats.spearmanr(valid["delta_biomass"], valid["pdi"])
        ax_b.text(
            0.03,
            0.97,
            f"rho={rho:+.2f}\np={pval:.1g}\nn={len(valid)}",
            transform=ax_b.transAxes,
            fontsize=5.2,
            va="top",
            ha="left",
        )
    ax_b.set_xlim(-d_abs_max, d_abs_max)
    ax_b.set_ylim(-0.03, 1.03)
    ax_b.set_title(f"{title_prefix}: dBiomass vs PDI", fontsize=6.3)
    if show_xlabel:
        ax_b.set_xlabel(r"$\Delta$biomass", fontsize=5.8)
    if show_ylabel:
        ax_b.set_ylabel(r"PDI", fontsize=5.8)
    if show_legend:
        ax_b.legend(loc="lower right", fontsize=4.8, frameon=False, handletextpad=0.2)
    ax_b.tick_params(labelsize=5)
    sns.despine(ax=ax_b)


def make_single_axis_all_media_figures(events: pd.DataFrame, outdir: Path) -> None:
    """Make one K-only and one r-only all-media figure."""
    media = [
        (0.3, "LN", r"LN $\mu=0.3$"),
        (0.6, "MN", r"MN $\mu=0.6$"),
        (0.8, "HN", r"HN $\mu=0.8$"),
    ]
    for axis_name, fixed_col, varied_col, out_suffix, title in [
        ("K", "r_sd", "k_sd", "Kstd_all_media", r"$K$ heterogeneity only ($r$ sd=0)"),
        ("r", "k_sd", "r_sd", "Rstd_all_media", r"$r$ heterogeneity only ($K$ sd=0)"),
    ]:
        sigmas = sorted(events.loc[np.isclose(events[fixed_col], 0.0), varied_col].unique())
        fig, axes = plt.subplots(
            len(sigmas),
            6,
            figsize=(235 * mm, 34 * mm * len(sigmas)),
            facecolor="w",
        )
        for row_i, sigma in enumerate(sigmas):
            for med_i, (mu, _tag, med_label) in enumerate(media):
                sub = events[
                    (np.isclose(events["mu"], mu))
                    & (np.isclose(events[fixed_col], 0.0))
                    & (np.isclose(events[varied_col], sigma))
                ].copy()
                ax_a = axes[row_i, 2 * med_i]
                ax_b = axes[row_i, 2 * med_i + 1]
                draw_zoom_pair(
                    ax_a,
                    ax_b,
                    sub,
                    rf"${axis_name}$ sd={sigma:g}",
                    med_label,
                    show_xlabel=row_i == len(sigmas) - 1,
                    show_ylabel=med_i == 0,
                    show_legend=(row_i == 0 and med_i == 2),
                )
        fig.suptitle(title, fontsize=10, y=0.995)
        fig.tight_layout(rect=(0, 0, 1, 0.988), w_pad=0.6, h_pad=0.9)
        for ext in ["pdf", "png", "svg"]:
            fig.savefig(outdir / f"Fig_Q6_Kr_{out_suffix}.{ext}", dpi=300, bbox_inches="tight")
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=40)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    cfg = SimConfig(reps=args.reps)
    outdir = SCRIPT_DIR
    events_path = outdir / "kr_heterogeneity_events.csv"
    summary_path = outdir / "kr_heterogeneity_summary.csv"
    json_path = outdir / "kr_heterogeneity_results.json"

    if events_path.exists() and not args.force:
        print(f"[load] {events_path}")
        events = pd.read_csv(events_path)
    else:
        events = simulate(cfg, workers=args.workers)
        events.to_csv(events_path, index=False)
        with open(json_path, "w") as f:
            json.dump({"config": asdict(cfg), "events": events.to_dict(orient="records")}, f)
        print(f"[write] {events_path}")
        print(f"[write] {json_path}")

    summary = summarize(events)
    summary.to_csv(summary_path, index=False)
    print(f"[write] {summary_path}")
    make_phase_figure(summary, outdir)
    make_winner_figure(summary, outdir)
    make_medium_variant_zoom_figures(events, outdir)
    make_single_axis_all_media_figures(events, outdir)

    print("\n===== K/r heterogeneity summary =====")
    for mu in cfg.mu_values:
        sub = summary[summary["mu"] == mu]
        print(
            f"mu={mu:.1f}: Dominance range "
            f"{sub['dominance_fraction'].min():.2f}-{sub['dominance_fraction'].max():.2f}; "
            f"winner-denser range "
            f"{sub['winner_denser_fraction'].min():.2f}-{sub['winner_denser_fraction'].max():.2f}; "
            f"rho range "
            f"{sub['delta_biomass_pdi_spearman_rho'].min():+.2f}-"
            f"{sub['delta_biomass_pdi_spearman_rho'].max():+.2f}"
        )
    print("===== Done =====")


if __name__ == "__main__":
    main()
