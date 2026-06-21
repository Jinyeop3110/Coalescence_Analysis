#!/usr/bin/env python3
"""
Export compact interaction-matrix assets for inserting into main Fig. 2A.

The existing R1-7 figure is a full supplementary-style panel. This script
produces small standalone heatmaps suitable for manual placement in Adobe.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
CODE_DIR = SCRIPT_DIR.parents[1]
DATA_PATH = (
    CODE_DIR
    / "Simulation_Data"
    / "48species_10reps_fine_WITH_MATRICES"
    / "Community_10reps_fine_WITH_MATRICES.json"
)
OUT_DIR = SCRIPT_DIR / "fig2a_matrix_assets"

TARGET_MU = "0.50"
THRESHOLD = 1e-3
SPECIES_PER_COMMUNITY = 12


mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["font.size"] = 7
mpl.rcParams["axes.linewidth"] = 0.5
mpl.rcParams["xtick.direction"] = "in"
mpl.rcParams["ytick.direction"] = "in"


def survivors(vec: list[float] | np.ndarray) -> np.ndarray:
    return np.where(np.asarray(vec) > THRESHOLD)[0]


def choose_balanced_rep(reps: dict) -> str:
    """Choose the same kind of visually useful replicate as the R1-7 script."""
    best_rep = None
    best_score = -np.inf

    for rep_key, rep_data in reps.items():
        sc_list = rep_data["sc_list"]
        counts = [len(survivors(sc_list[key])) for key in sorted(sc_list.keys(), key=int)]
        min_surv = min(counts)
        total_surv = sum(counts)
        score = min_surv * 10 + total_surv

        if min_surv >= 2 and score > best_score:
            best_score = score
            best_rep = rep_key

    return best_rep if best_rep is not None else next(iter(reps))


def ordered_survivor_indices(rep_data: dict, comm_a: str = "0", comm_b: str = "1"):
    sc_list = rep_data["sc_list"]
    surv_a = survivors(sc_list[comm_a])
    surv_b = survivors(sc_list[comm_b])

    shared = np.intersect1d(surv_a, surv_b)
    only_a = np.setdiff1d(surv_a, shared)
    only_b = np.setdiff1d(surv_b, shared)
    ordered = np.concatenate([only_a, shared, only_b])
    return ordered, len(only_a), len(shared), len(only_b)


def ordered_initial_indices(rep_data: dict, comm_a: int = 0, comm_b: int = 1):
    """
    Reconstruct the two initially seeded parental communities for this replicate.

    The simulation script seeded NumPy, drew the full interaction matrix, then
    used np.random.permutation(N) to assign four non-overlapping communities.
    The JSON stores the seed and interaction matrix but not the community
    library, so we replay only the RNG consumption needed to recover membership.
    """
    interaction = np.asarray(rep_data["parameters"]["interaction_matrix"], dtype=float)
    n_species = interaction.shape[0]
    seed = int(rep_data["parameters"]["seed"])

    np.random.seed(seed)
    _ = np.random.random((n_species, n_species))
    all_species = np.random.permutation(n_species)

    start_a = comm_a * SPECIES_PER_COMMUNITY
    start_b = comm_b * SPECIES_PER_COMMUNITY
    initial_a = all_species[start_a:start_a + SPECIES_PER_COMMUNITY]
    initial_b = all_species[start_b:start_b + SPECIES_PER_COMMUNITY]

    return np.concatenate([initial_a, initial_b]), len(initial_a), len(initial_b)


def save_all(fig: plt.Figure, stem: str) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    for ext in ("png", "pdf", "svg"):
        path = OUT_DIR / f"{stem}.{ext}"
        fig.savefig(path, bbox_inches="tight", dpi=600, transparent=True)
        print(f"saved {path}")
    plt.close(fig)


def draw_heatmap(
    matrix: np.ndarray,
    stem: str,
    *,
    title: str | None = None,
    n_a: int | None = None,
    n_shared: int = 0,
    show_labels: bool = False,
    show_colorbar: bool = False,
    cmap: str = "Greys",
    vmax: float = 1.0,
) -> None:
    fig, ax = plt.subplots(figsize=(1.45, 1.45))
    shown = matrix.copy()
    np.fill_diagonal(shown, np.nan)

    im = ax.imshow(shown, cmap=cmap, vmin=0, vmax=vmax, interpolation="nearest")

    if n_a is not None:
        boundary = n_a - 0.5
        ax.axhline(boundary, color="white", linewidth=1.2)
        ax.axvline(boundary, color="white", linewidth=1.2)
        if n_shared:
            boundary2 = n_a + n_shared - 0.5
            ax.axhline(boundary2, color="white", linewidth=0.8, linestyle="--")
            ax.axvline(boundary2, color="white", linewidth=0.8, linestyle="--")

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color("black")

    if title:
        ax.set_title(title, pad=3, fontsize=7)

    if show_labels and n_a is not None:
        y_label = matrix.shape[0] + 0.55
        ax.text((n_a - 1) / 2, y_label, "Community A", color="#b2182b",
                ha="center", va="top", fontsize=6)
        n_b = matrix.shape[0] - n_a - n_shared
        ax.text(n_a + n_shared + (n_b - 1) / 2, y_label, "Community B",
                color="#2166ac", ha="center", va="top", fontsize=6)

    if show_colorbar:
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        cbar.set_label(r"$\alpha_{ij}$", fontsize=7)
        cbar.ax.tick_params(labelsize=6, width=0.4, length=2)

    save_all(fig, stem)


def draw_before_after_strip(
    before: np.ndarray,
    after: np.ndarray,
    before_n_a: int,
    after_n_a: int,
    after_n_shared: int,
    vmax: float,
    stem: str,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(3.4, 1.55))
    for ax, matrix, title, draw_boundary in [
        (axes[0], before, "Before assembly", True),
        (axes[1], after, "After assembly", True),
    ]:
        shown = matrix.copy()
        np.fill_diagonal(shown, np.nan)
        ax.imshow(shown, cmap="Greys", vmin=0, vmax=vmax, interpolation="nearest")
        ax.set_title(title, pad=2, fontsize=7)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_linewidth(0.5)
            spine.set_color("black")
        if draw_boundary:
            boundary = (before_n_a if title.startswith("Before") else after_n_a) - 0.5
            ax.axhline(boundary, color="white", linewidth=1.2)
            ax.axvline(boundary, color="white", linewidth=1.2)
            if (not title.startswith("Before")) and after_n_shared:
                boundary2 = after_n_a + after_n_shared - 0.5
                ax.axhline(boundary2, color="white", linewidth=0.8, linestyle="--")
                ax.axvline(boundary2, color="white", linewidth=0.8, linestyle="--")
    fig.subplots_adjust(wspace=0.14)
    save_all(fig, stem)


def main() -> None:
    with open(DATA_PATH) as handle:
        sim_data = json.load(handle)

    target_mu = TARGET_MU if TARGET_MU in sim_data else sorted(sim_data.keys(), key=float)[0]
    reps = sim_data[target_mu]
    rep_key = choose_balanced_rep(reps)
    rep_data = reps[rep_key]

    interaction = np.asarray(rep_data["parameters"]["interaction_matrix"], dtype=float)
    ordered, n_a, n_shared, n_b = ordered_survivor_indices(rep_data)
    after = interaction[np.ix_(ordered, ordered)]

    initial_ordered, initial_n_a, initial_n_b = ordered_initial_indices(rep_data)
    before = interaction[np.ix_(initial_ordered, initial_ordered)]

    # A matching-size random submatrix is still useful if a same-size visual
    # control is needed, but it should not be used to imply pre/post species
    # counts.
    matched_random = interaction[np.ix_(np.arange(len(ordered)), np.arange(len(ordered)))]

    mu = float(target_mu)
    vmax = 2 * mu

    print(
        f"mu={target_mu}, rep={rep_key}, initial A={initial_n_a}, initial B={initial_n_b}, "
        f"survivors A={n_a}, shared={n_shared}, B={n_b}"
    )
    print(f"output directory: {OUT_DIR}")

    draw_heatmap(
        before,
        "fig2a_before_assembly_matrix_24species_clean",
        title=None,
        n_a=initial_n_a,
        show_colorbar=False,
        vmax=vmax,
    )
    draw_heatmap(
        before,
        "fig2a_before_assembly_matrix_24species_labeled",
        title="Before assembly",
        n_a=initial_n_a,
        show_labels=True,
        show_colorbar=False,
        vmax=vmax,
    )
    draw_heatmap(
        matched_random,
        "fig2a_random_matrix_matched_size_visual_control",
        title=None,
        show_colorbar=False,
        vmax=vmax,
    )
    draw_heatmap(
        after,
        "fig2a_after_assembly_matrix_14survivors_clean",
        title=None,
        n_a=n_a,
        n_shared=n_shared,
        show_colorbar=False,
        vmax=vmax,
    )
    draw_heatmap(
        after,
        "fig2a_after_assembly_matrix_14survivors_labeled",
        title="After assembly",
        n_a=n_a,
        n_shared=n_shared,
        show_labels=True,
        show_colorbar=False,
        vmax=vmax,
    )
    draw_heatmap(
        after,
        "fig2a_after_assembly_matrix_14survivors_with_colorbar",
        title=None,
        n_a=n_a,
        n_shared=n_shared,
        show_labels=False,
        show_colorbar=True,
        vmax=vmax,
    )
    draw_before_after_strip(
        before,
        after,
        initial_n_a,
        n_a,
        n_shared,
        vmax,
        "fig2a_true_before_after_size_change_strip",
    )


if __name__ == "__main__":
    main()
