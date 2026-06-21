#!/usr/bin/env python3
"""
Reproduce Reviewer 3's geometric null-model figures under L1 and L2 normalization.

This script generates reviewer-style similarity maps for N = 2, 4, 6, 8 under
four geometric null constructions:
1. Random-restructuring null model with abundances ~ U(0, 1)
2. Random-restructuring null model with abundances ~ 10^U(-3, 0)
3. Simple additive null model n_C = n_A + n_B with abundances ~ U(0, 1)
4. Simple additive null model n_C = n_A + n_B with abundances ~ 10^U(-3, 0)

For each construction, the same simulation is repeated under:
- L1 normalization  (contrast only; never used in the manuscript)
- L2 normalization  (the manuscript's implemented metric)

The L2 path calls common_setup.metric_VectorDecomposition_onlyPositive
-> calculate_assymetricity -> characterize_case directly, i.e. the exact
pipeline that produces Fig. 1E in the main paper. For non-overlapping
parents (which is the case in all four constructions below), the
manuscript pipeline reduces analytically to raw cosine similarity on
L2-normalized vectors, but we go through the real functions to remove
any chance of implementation drift.

The L1 path has no manuscript counterpart; it applies L1 normalization,
computes raw dot products, and feeds the result through the same
common_setup.characterize_case thresholds so that only the normalization
choice differs between the two figures.

The scatter panels show both retention-boundary conventions:
- r = 1/2, the boundary used in the reviewer's geometric phase diagrams
- r = 1/sqrt(2), the boundary used by the manuscript classifier

The stacked bars report classifications under the manuscript boundary.
The output is two 3x5 panel figures (one per normalization), plus a summary CSV.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, CODE_DIR)
# common_setup has import-time side effects (loads Excel); must be in CODE_DIR
# when imported. Save and restore the caller's CWD so downstream os.path
# resolution in this script still happens from SCRIPT_DIR.
_prev_cwd = os.getcwd()
os.chdir(CODE_DIR)
from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
)
os.chdir(_prev_cwd)


SEED = 42
N_VALUES = [2, 4, 6, 8]
N_SAMPLES = 1000

DOM_COLOR = "#ef8a7a"
MIX_COLOR = "#98d87a"
REST_COLOR = "#b26bd2"


@dataclass(frozen=True)
class CaseSpec:
    key: str
    title: str
    panel_label: str


CASE_SPECS = [
    CaseSpec("uniform_random", "Random-restructuring null model, abundances ~ U(0, 1)", "A"),
    CaseSpec("skewed_random", "Random-restructuring null model, abundances ~ 10^U(-3, 0)", "B"),
    CaseSpec("additive_uniform", "Simple additive null model, abundances ~ U(0, 1)", "C"),
    CaseSpec("additive_skewed", "Simple additive null model, abundances ~ 10^U(-3, 0)", "D"),
]


CLASS_LABELS = {0: "Dominance", 1: "Mixture", 2: "Restructuring"}
N_INDEX = {n: i for i, n in enumerate(N_VALUES)}
SEED_OFFSETS = {
    "l1": {
        "uniform_random": 0,
        "skewed_random": 4,
        "additive_uniform": 8,
        "additive_skewed": 24,
    },
    "l2": {
        "uniform_random": 12,
        "skewed_random": 16,
        "additive_uniform": 20,
        "additive_skewed": 28,
    },
}


def seed_for(norm_kind: str, case_key: str, n: int) -> int:
    return SEED + SEED_OFFSETS[norm_kind][case_key] + N_INDEX[n]


def l1_normalize(vec: np.ndarray) -> np.ndarray:
    """L1 normalization for the contrast figure only. The manuscript never uses L1."""
    vec = np.asarray(vec, dtype=float)
    denom = float(np.sum(vec))
    if denom <= 0:
        return vec.copy()
    return vec / denom


def _class_from_int(cls_int: int | None) -> str:
    """characterize_case() returns None for exact boundaries (x^2 == 0.5 or
    y == 0.5), which are measure-zero in continuous MC. Map to Restructuring
    so downstream code can treat the label as a string unconditionally.
    """
    if cls_int is None:
        cls_int = 2
    return CLASS_LABELS[cls_int]


def evaluate_L2_manuscript(
    parent_a: np.ndarray, parent_b: np.ndarray, offspring: np.ndarray
) -> tuple[float, float, str]:
    """Run the exact manuscript pipeline (common_setup) on (A, B, C).

    Returns (u, v, class_label), where (u, v) are the L2-decomposition
    coefficients on the (parent_a, parent_b) basis after nonnegative clipping
    and renormalization to the unit arc. For non-overlapping parents these
    equal Sim(A,C) and Sim(B,C), so the scatter layout is identical to the
    prior raw-dot-product implementation.
    """
    u, v, k = metric_VectorDecomposition_onlyPositive(parent_a, parent_b, offspring)
    x, y = calculate_assymetricity(u, v, k)
    return float(u), float(v), _class_from_int(characterize_case(x, y))


def evaluate_L1_analogue(
    parent_a: np.ndarray, parent_b: np.ndarray, offspring: np.ndarray
) -> tuple[float, float, str]:
    """L1 normalize, then apply the manuscript's classification thresholds.

    No vector decomposition is performed: under L1 normalization the unit
    vectors do not lie on an orthonormal sphere and the decomposition has no
    clean geometric meaning. We therefore feed the raw (Sim_A, Sim_B) pair
    through common_setup.characterize_case, matching the L2 path in its
    threshold logic but differing only in the normalization step.
    """
    a = l1_normalize(parent_a)
    b = l1_normalize(parent_b)
    c = l1_normalize(offspring)
    sim_a = float(np.dot(a, c))
    sim_b = float(np.dot(b, c))
    x_mag = math.sqrt(sim_a ** 2 + sim_b ** 2)
    if sim_b <= 0:
        angle = math.pi / 2
    else:
        angle = math.atan(sim_a / sim_b)
    y_asym = abs(abs(angle) - math.pi / 4) / (math.pi / 4)
    return sim_a, sim_b, _class_from_int(characterize_case(x_mag, y_asym))


def sample_parent_pair_uniform(rng: np.random.Generator, n: int) -> tuple[np.ndarray, np.ndarray]:
    a = np.zeros(2 * n)
    b = np.zeros(2 * n)
    a[:n] = rng.uniform(0.0, 1.0, size=n)
    b[n:] = rng.uniform(0.0, 1.0, size=n)
    return a, b


def sample_parent_pair_skewed(rng: np.random.Generator, n: int) -> tuple[np.ndarray, np.ndarray]:
    a = np.zeros(2 * n)
    b = np.zeros(2 * n)
    a[:n] = 10 ** rng.uniform(-3.0, 0.0, size=n)
    b[n:] = 10 ** rng.uniform(-3.0, 0.0, size=n)
    return a, b


def sample_random_restructuring(
    rng: np.random.Generator, parent_a: np.ndarray, parent_b: np.ndarray
) -> np.ndarray:
    pooled = np.concatenate([parent_a[parent_a > 0], parent_b[parent_b > 0]])
    n = len(pooled) // 2
    idx = rng.choice(len(parent_a), size=n, replace=False)
    offspring = np.zeros_like(parent_a)
    # Match the reviewer-stated null literally: C keeps N nonzero entries whose
    # values are sampled from the 2N parental nonzero abundances, without
    # reusing a parental abundance value within the same event.
    offspring[idx] = rng.choice(pooled, size=n, replace=False)
    return offspring


def sample_additive(parent_a: np.ndarray, parent_b: np.ndarray) -> np.ndarray:
    return parent_a + parent_b


def simulate_case(case_key: str, norm_kind: str, n: int, n_samples: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sims_a = []
    sims_b = []
    classes = []
    evaluator = evaluate_L2_manuscript if norm_kind == "l2" else evaluate_L1_analogue

    for _ in range(n_samples):
        if case_key == "uniform_random":
            parent_a, parent_b = sample_parent_pair_uniform(rng, n)
            offspring = sample_random_restructuring(rng, parent_a, parent_b)
        elif case_key == "skewed_random":
            parent_a, parent_b = sample_parent_pair_skewed(rng, n)
            offspring = sample_random_restructuring(rng, parent_a, parent_b)
        elif case_key == "additive_uniform":
            parent_a, parent_b = sample_parent_pair_uniform(rng, n)
            offspring = sample_additive(parent_a, parent_b)
        elif case_key == "additive_skewed":
            parent_a, parent_b = sample_parent_pair_skewed(rng, n)
            offspring = sample_additive(parent_a, parent_b)
        else:
            raise ValueError(f"Unknown case: {case_key}")

        sim_a, sim_b, cls = evaluator(parent_a, parent_b, offspring)
        sims_a.append(sim_a)
        sims_b.append(sim_b)
        classes.append(cls)

    return pd.DataFrame(
        {
            "case": case_key,
            "norm": norm_kind,
            "N": n,
            "sim_a": sims_a,
            "sim_b": sims_b,
            "class": classes,
        }
    )


def verify_L2_against_raw_dot_product(n_check: int = 100, tol: float = 1e-10) -> None:
    """Runtime assertion: the manuscript pipeline (evaluate_L2_manuscript) must
    give the same scatter coordinates and classification as a raw L2 dot
    product for the reviewer's null constructions, because the parental
    supports are non-overlapping.

    This protects against future drift in common_setup from silently changing
    what Figs. R3-2.0a/b mean.
    """
    rng = np.random.default_rng(SEED - 1)
    max_coord_diff = 0.0
    class_disagreements = 0
    total = 0
    for case in CASE_SPECS:
        for n in N_VALUES:
            for _ in range(n_check):
                if case.key == "uniform_random":
                    a, b = sample_parent_pair_uniform(rng, n)
                    c = sample_random_restructuring(rng, a, b)
                elif case.key == "skewed_random":
                    a, b = sample_parent_pair_skewed(rng, n)
                    c = sample_random_restructuring(rng, a, b)
                elif case.key == "additive_uniform":
                    a, b = sample_parent_pair_uniform(rng, n)
                    c = sample_additive(a, b)
                elif case.key == "additive_skewed":
                    a, b = sample_parent_pair_skewed(rng, n)
                    c = sample_additive(a, b)
                else:
                    raise ValueError(f"Unknown case: {case.key}")

                u_new, v_new, cls_new = evaluate_L2_manuscript(a, b, c)

                a_l2 = a / np.linalg.norm(a)
                b_l2 = b / np.linalg.norm(b)
                c_l2 = c / np.linalg.norm(c)
                sim_a_raw = float(np.dot(a_l2, c_l2))
                sim_b_raw = float(np.dot(b_l2, c_l2))

                max_coord_diff = max(
                    max_coord_diff,
                    abs(u_new - sim_a_raw),
                    abs(v_new - sim_b_raw),
                )
                total += 1
                if cls_new != classify_raw_for_verification(sim_a_raw, sim_b_raw):
                    class_disagreements += 1

    print(
        f"[verify L2] n={total} events; "
        f"max |u_new - Sim_A_raw| over scatter coords = {max_coord_diff:.2e} "
        f"(tolerance {tol:.0e}); class disagreements = {class_disagreements}"
    )
    if max_coord_diff > tol:
        raise AssertionError(
            f"L2 pipeline drift: common_setup decomposition differs from raw "
            f"L2 dot product by {max_coord_diff:.3e}, exceeding {tol:.0e}."
        )
    if class_disagreements != 0:
        raise AssertionError(
            f"L2 classification drift: {class_disagreements}/{total} events "
            f"classified differently by manuscript pipeline vs raw-dot-product."
        )


def classify_raw_for_verification(sim_a: float, sim_b: float) -> str:
    """Raw-dot-product classifier, used only by verify_L2_against_raw_dot_product."""
    x_mag = math.sqrt(sim_a ** 2 + sim_b ** 2)
    if sim_b <= 0:
        angle = math.pi / 2
    else:
        angle = math.atan(sim_a / sim_b)
    y_asym = abs(abs(angle) - math.pi / 4) / (math.pi / 4)
    return _class_from_int(characterize_case(x_mag, y_asym))


def draw_reference_boundaries(ax: plt.Axes, show_legend: bool = False) -> None:
    theta = np.linspace(0, np.pi / 2, 300)
    ax.plot(np.cos(theta), np.sin(theta), color="black", linewidth=2.0)
    reviewer_r = 0.5
    manuscript_r = math.sqrt(0.5)
    reviewer_line, = ax.plot(
        reviewer_r * np.cos(theta),
        reviewer_r * np.sin(theta),
        color="0.55",
        linewidth=1.0,
        linestyle=(0, (1, 2)),
        label=r"reviewer $r=1/2$",
    )
    manuscript_line, = ax.plot(
        manuscript_r * np.cos(theta),
        manuscript_r * np.sin(theta),
        color="black",
        linewidth=1.0,
        linestyle=(0, (4, 4)),
        label=r"manuscript $r=1/\sqrt{2}$",
    )
    for ang in (np.pi / 8, 3 * np.pi / 8):
        ax.plot([0, math.cos(ang)], [0, math.sin(ang)],
                color="black", linewidth=1.0, linestyle=(0, (4, 4)))
    if show_legend:
        ax.legend(
            handles=[reviewer_line, manuscript_line],
            loc="upper right",
            fontsize=5.5,
            frameon=False,
            handlelength=1.8,
            borderpad=0.1,
            labelspacing=0.2,
        )
    ax.plot([0, 0], [0, 1], color="black", linewidth=1.2)
    ax.plot([0, 1], [0, 0], color="black", linewidth=1.2)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_aspect("equal")
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.tick_params(length=0, pad=1)
    for spine in ax.spines.values():
        spine.set_visible(False)


def plot_norm_figure(all_df: pd.DataFrame, norm_kind: str, out_pdf: str) -> None:
    """Reviewer-style layout: 3 rows (null models) x [4 sim-maps + 1 stacked-bar],
    row subtitles placed above each row, minimal axis clutter.
    """
    n_rows = len(CASE_SPECS)
    fig, axes = plt.subplots(
        n_rows, 5, figsize=(11.5, 7.8),
        gridspec_kw={"width_ratios": [1, 1, 1, 1, 0.85]}
    )

    for row_idx, case in enumerate(CASE_SPECS):
        case_df = all_df[(all_df["case"] == case.key) & (all_df["norm"] == norm_kind)]
        is_last_row = row_idx == n_rows - 1

        for col_idx, n in enumerate(N_VALUES):
            ax = axes[row_idx, col_idx]
            sub = case_df[case_df["N"] == n]
            ax.scatter(
                sub["sim_a"], sub["sim_b"],
                s=4, alpha=0.18, color="black", linewidths=0
            )
            draw_reference_boundaries(ax, show_legend=(row_idx == 0 and col_idx == 0))
            ax.set_title(f"N = {n}", fontsize=10, pad=3)

            if col_idx == 0:
                ax.set_ylabel(r"$\mathrm{Sim}\,(B,C)$", fontsize=11)
            else:
                ax.set_ylabel("")
                ax.set_yticklabels([])
            if is_last_row:
                ax.set_xlabel(r"$\mathrm{Sim}\,(A,C)$", fontsize=11)
            else:
                ax.set_xlabel("")
                ax.set_xticklabels([])

        bar_ax = axes[row_idx, 4]
        frac_df = (
            case_df.groupby(["N", "class"]).size().unstack(fill_value=0)
            .reindex(index=N_VALUES)
            .reindex(columns=["Dominance", "Mixture", "Restructuring"], fill_value=0)
        )
        frac_df = frac_df.div(frac_df.sum(axis=1), axis=0)
        x = np.arange(len(N_VALUES))
        base = np.zeros(len(N_VALUES))
        for cls, color in [("Dominance", DOM_COLOR), ("Mixture", MIX_COLOR), ("Restructuring", REST_COLOR)]:
            vals = frac_df[cls].to_numpy()
            bar_ax.bar(x, vals, bottom=base, color=color, width=0.9, edgecolor="none")
            base += vals
        bar_ax.set_ylim(0, 1)
        bar_ax.set_xticks(x)
        bar_ax.set_xticklabels([f"N = {n}" for n in N_VALUES], rotation=35, ha="right", fontsize=9)
        bar_ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
        bar_ax.set_ylabel("Fraction", fontsize=11)
        if row_idx == 0:
            bar_ax.text(0.05, 0.88, "Restructuring", transform=bar_ax.transAxes, fontsize=9)
            bar_ax.text(0.13, 0.49, "Mixture", transform=bar_ax.transAxes, fontsize=9)
            bar_ax.text(0.18, 0.12, "Dominance", transform=bar_ax.transAxes, fontsize=9)
        for spine in ["top", "right"]:
            bar_ax.spines[spine].set_visible(False)
        bar_ax.tick_params(axis="x", pad=1)

    fig.subplots_adjust(
        left=0.07, right=0.97, top=0.93, bottom=0.08,
        wspace=0.30, hspace=0.92,
    )

    # Row subtitles placed above each row so the null construction is visible
    # before reading across the N columns.
    fig.canvas.draw()
    for row_idx, case in enumerate(CASE_SPECS):
        row_axes = [axes[row_idx, c] for c in range(5)]
        pos_bboxes = [ax.get_position() for ax in row_axes]
        y_above = max(bb.y1 for bb in pos_bboxes) + 0.035
        x_center = 0.5 * (pos_bboxes[0].x0 + pos_bboxes[-1].x1)
        fig.text(
            x_center,
            y_above,
            f"{case.panel_label}. {case.title}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf.replace(".pdf", ".png"), dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    # Before anything else, assert the L2 path still agrees with a raw L2 dot
    # product. A failure here means common_setup has changed in a way that
    # silently alters Fig. R3-2.0a; stop and investigate rather than ship.
    verify_L2_against_raw_dot_product(n_check=100)

    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = here
    records = []

    for norm_kind in ("l1", "l2"):
        for case in CASE_SPECS:
            for n in N_VALUES:
                records.append(simulate_case(case.key, norm_kind, n, N_SAMPLES, seed_for(norm_kind, case.key, n)))

    all_df = pd.concat(records, ignore_index=True)
    all_df.to_csv(os.path.join(out_dir, "reviewer_norm_comparison_points.csv"), index=False)

    summary = (
        all_df.groupby(["norm", "case", "N", "class"]).size().unstack(fill_value=0)
        .reindex(columns=["Dominance", "Mixture", "Restructuring"], fill_value=0)
        .reset_index()
    )
    summary["total"] = summary[["Dominance", "Mixture", "Restructuring"]].sum(axis=1)
    for cls in ["Dominance", "Mixture", "Restructuring"]:
        summary[f"{cls}_fraction"] = summary[cls] / summary["total"]
    summary.to_csv(os.path.join(out_dir, "reviewer_norm_comparison_summary.csv"), index=False)

    plot_norm_figure(all_df, "l1", os.path.join(out_dir, "Fig_R3_2_reviewer_reproduction_L1.pdf"))
    plot_norm_figure(all_df, "l2", os.path.join(out_dir, "Fig_R3_2_reviewer_reproduction_L2.pdf"))

    print("Saved:")
    print(f"  {os.path.join(out_dir, 'Fig_R3_2_reviewer_reproduction_L1.pdf')}")
    print(f"  {os.path.join(out_dir, 'Fig_R3_2_reviewer_reproduction_L2.pdf')}")
    print(f"  {os.path.join(out_dir, 'reviewer_norm_comparison_summary.csv')}")


if __name__ == "__main__":
    main()
