#!/usr/bin/env python3
"""Generate the simulation outcome comparison at mu = 0.6.

All three bars are calculated from the assembly-history simulation dataset.
The simple additive null is event matched to the coalescence bar: for every
valid coalescence event, its outcome vector is replaced by c1 + c2 and passed
through the same classifier.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from make_fig1_outcome_comparison import render_outcome_comparison


HERE = Path(__file__).resolve().parent
CODE_DIR = HERE.parents[4] / "code"
DATA_DIR = CODE_DIR / "Simulation_Data" / "coalescence_vs_direct_50reps"
COALESCENCE_FILE = DATA_DIR / "Community_coalescence_50reps.json"
DIRECT_FILE = DATA_DIR / "Community_direct_50reps.json"
OUT_STEM = HERE / "fig1_outcome_comparison_simulation_mu0p6"
SUMMARY_CSV = HERE / "fig1_outcome_comparison_simulation_mu0p6_counts.csv"
MU = 0.6
OUTCOME_NAMES = {0: "Dominance", 1: "Mixture", 2: "Restructuring"}


# Reuse the exact metric and classifier that generated the published
# coalescence-versus-direct-assembly simulation figure.
sys.path.insert(0, str(CODE_DIR))
previous_cwd = Path.cwd()
try:
    os.chdir(CODE_DIR)
    from plot_assembly_effect_separate_pies import (  # noqa: E402
        classify_outcome,
        metric_VectorDecomposition_onlyPositive,
    )
finally:
    os.chdir(previous_cwd)


def classify(c1: np.ndarray, c2: np.ndarray, outcome: np.ndarray) -> int | None:
    """Classify one event, returning None for the same invalid cases as upstream."""
    try:
        with np.errstate(divide="ignore", invalid="ignore"):
            u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, outcome)
        if np.isnan(np.asarray([u, v, k], dtype=float)).any():
            return None
        return classify_outcome(u, v, k)
    except (ValueError, TypeError, np.linalg.LinAlgError):
        return None


def load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def count_coalescence_and_null(data: dict) -> tuple[Counter, Counter]:
    coalescence = Counter()
    additive_null = Counter()
    key_fragment = f"mean{MU:.2f}_"
    for combo_key, combo in data.items():
        if key_fragment not in combo_key:
            continue
        for rep_data in combo.values():
            c1 = np.asarray(rep_data["sc_list"]["c1"], dtype=float)
            c2 = np.asarray(rep_data["sc_list"]["c2"], dtype=float)
            observed = np.asarray(rep_data["cc_list"]["c1_c2"], dtype=float)
            observed_class = classify(c1, c2, observed)
            null_class = classify(c1, c2, c1 + c2)
            if observed_class is not None:
                coalescence[observed_class] += 1
            if null_class is not None:
                additive_null[null_class] += 1
    return coalescence, additive_null


def count_direct_assembly(data: dict) -> Counter:
    direct = Counter()
    key_fragment = f"mean{MU:.2f}_"
    for combo_key, combo in data.items():
        if key_fragment not in combo_key:
            continue
        for rep_data in combo.values():
            c1 = np.asarray(rep_data["sc_list"]["c1"], dtype=float)
            c2 = np.asarray(rep_data["sc_list"]["c2"], dtype=float)
            outcome = np.asarray(rep_data["cc_list"]["c1_c2"], dtype=float)
            outcome_class = classify(c1, c2, outcome)
            if outcome_class is not None:
                direct[outcome_class] += 1
    return direct


def ordered_counts(counts: Counter) -> tuple[int, int, int]:
    return tuple(counts[index] for index in range(3))


def write_summary(groups: list[tuple[str, tuple[int, int, int]]]) -> None:
    with SUMMARY_CSV.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["mu", "group", "outcome", "count", "total", "fraction"])
        for group, counts in groups:
            total = sum(counts)
            for outcome, count in zip(OUTCOME_NAMES.values(), counts):
                writer.writerow([MU, group.replace("\n", " "), outcome, count, total, count / total])


def main() -> None:
    coalescence_data = load_json(COALESCENCE_FILE)
    direct_data = load_json(DIRECT_FILE)
    coalescence, additive_null = count_coalescence_and_null(coalescence_data)
    direct = count_direct_assembly(direct_data)

    groups = [
        ("Coalescence", ordered_counts(coalescence)),
        ("Direct\nAssembly", ordered_counts(direct)),
        ("Null model", ordered_counts(additive_null)),
    ]
    if sum(groups[0][1]) != sum(groups[2][1]):
        raise RuntimeError("The coalescence and event-matched null totals must agree")

    write_summary(groups)
    render_outcome_comparison(
        groups,
        OUT_STEM,
        title="Simulation (μ = 0.6)",
        labels_at_top=False,
    )
    print(f"Saved count summary to {SUMMARY_CSV}")


if __name__ == "__main__":
    main()
