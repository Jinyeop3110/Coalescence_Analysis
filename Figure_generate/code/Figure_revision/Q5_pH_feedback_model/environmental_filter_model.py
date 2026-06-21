"""
environmental_filter_model.py
=============================

Trait-based environmental-filtering null model for internal memo Q5b.

This model deliberately contains no pairwise interactions and no explicit
environmental dynamics. Species have a latent trait z_i. Each nutrient
condition exposes a medium-specific niche filter with center theta, breadth
sigma, and strength gamma:

    w_i(m) = exp(-((z_i - theta_m)^2) / (2 sigma_m^2)) ** gamma_m

Parents assemble by weighting initial abundances by w_i(m), thresholding
low-abundance survivors, and normalizing. Coalescence mixes the two assembled
parents 50/50 and applies the same medium filter again. The output abundance
vectors can be sent directly through the same L2/cosine classification helpers
used by the gLV and pH Q5 models.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

import pH_feedback_model as phmod


@dataclass(frozen=True)
class FilterParams:
    """Parameters for a nutrient-specific trait filter."""

    name: str
    theta: float
    sigma: float
    gamma: float
    threshold: float = 0.02


@dataclass
class TraitPool:
    """Species-level latent trait pool."""

    z: np.ndarray

    def N(self) -> int:
        return int(self.z.shape[0])


DEFAULT_FILTER_LEVELS = [
    FilterParams("Nutr-", theta=0.0, sigma=1.0, gamma=2.80),
    FilterParams("Base", theta=0.0, sigma=1.0, gamma=7.95),
    FilterParams("Nutr+", theta=0.0, sigma=1.0, gamma=10.15),
]


def normalize(x: np.ndarray) -> np.ndarray:
    """Return a sum-normalized copy, preserving all-zero vectors."""

    x = np.asarray(x, dtype=float).copy()
    total = float(np.sum(x))
    if total <= 0:
        return x
    return x / total


def sample_trait_pool(N: int, rng: np.random.Generator) -> TraitPool:
    """Draw species latent traits."""

    return TraitPool(z=rng.normal(loc=0.0, scale=1.0, size=N))


def filter_weights(pool: TraitPool, params: FilterParams) -> np.ndarray:
    """Compute medium-specific trait-match weights."""

    base = np.exp(-((pool.z - params.theta) ** 2) / (2.0 * params.sigma ** 2))
    return base ** params.gamma


def apply_filter(
    abundances: np.ndarray,
    weights: np.ndarray,
    threshold: float,
) -> np.ndarray:
    """Apply the environmental filter and threshold low relative abundances."""

    out = normalize(np.asarray(abundances, dtype=float) * weights)
    out[out < threshold] = 0.0
    return normalize(out)


def assemble_parent(
    pool: TraitPool,
    species_mask: np.ndarray,
    params: FilterParams,
    rng: np.random.Generator,
    n0_cv: float = 0.25,
) -> np.ndarray:
    """Assemble one parent under the nutrient-specific filter."""

    N = pool.N()
    init = np.zeros(N)
    n_species = int(np.sum(species_mask))
    if n_species == 0:
        return init
    init[species_mask] = rng.lognormal(mean=0.0, sigma=n0_cv, size=n_species)
    return apply_filter(init, filter_weights(pool, params), params.threshold)


def assemble_pool(
    pool: TraitPool,
    params: FilterParams,
    num_C: int,
    sp_per_C: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, list[np.ndarray]]:
    """Partition a trait pool into parents and assemble each parent."""

    N = pool.N()
    if num_C * sp_per_C > N:
        raise ValueError(f"Need {num_C * sp_per_C} species, but pool has N={N}.")
    perm = rng.permutation(N)
    masks = np.zeros((num_C, N), dtype=bool)
    parents = []
    for c in range(num_C):
        masks[c, perm[c * sp_per_C:(c + 1) * sp_per_C]] = True
        parents.append(assemble_parent(pool, masks[c], params, rng))
    return masks, parents


def run_coalescence(
    pool: TraitPool,
    params: FilterParams,
    n_A: np.ndarray,
    n_B: np.ndarray,
) -> np.ndarray:
    """Mix two parents 50/50 and reapply the same environmental filter."""

    mixed = 0.5 * (np.asarray(n_A, dtype=float) + np.asarray(n_B, dtype=float))
    return apply_filter(mixed, filter_weights(pool, params), params.threshold)


def classify_coalescence(n_A: np.ndarray, n_B: np.ndarray, n_C: np.ndarray):
    """Use the shared Q5 outcome-classification helper."""

    return phmod.classify_coalescence(n_A, n_B, n_C)


def selection_phi(n_A: np.ndarray, n_B: np.ndarray, n_C: np.ndarray) -> float:
    """Use the shared origin-to-persistence correlation helper."""

    return phmod.selection_phi(n_A, n_B, n_C)
