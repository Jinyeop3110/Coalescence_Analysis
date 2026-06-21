#!/usr/bin/env python3
"""Write nutrient-dependent coalescence outcome statistics for Supplementary Table 1."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


SCRIPT_PATH = Path(__file__).resolve()
OUT_DIR = SCRIPT_PATH.parent
V4_DIR = OUT_DIR.parents[2]
SESSION_DIR = V4_DIR.parents[2]
CODE_DIR = SESSION_DIR / "Figure_generate" / "code"

os.chdir(CODE_DIR)
sys.path.insert(0, str(CODE_DIR))

from common_setup import (  # noqa: E402
    Coalescence_data,
    Processed_sequences_synthetic,
    Syn_Coal_IDX,
    exception_list,
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
)


MEDIA = ["LN", "MN", "HN"]
MEDIA_LABELS = {"LN": "Nutr-", "MN": "Base", "HN": "Nutr+"}
OUTCOMES = {0: "Dominance", 1: "Mixture", 2: "Restructuring"}


def abundance_vector(sample_id: str) -> np.ndarray | None:
    rows = Processed_sequences_synthetic[Processed_sequences_synthetic["SampleIDX"] == sample_id]
    if rows.empty:
        return None
    vector = rows.iloc[0, 1:].values.astype(float)
    vector = np.nan_to_num(vector, nan=0.0)
    return vector * (vector > 1e-4)


def outcome_records() -> pd.DataFrame:
    records = []
    for medium in MEDIA:
        for pool_size in [6, 12, 24]:
            key = f"{medium}_{pool_size}"
            for sample_id in Syn_Coal_IDX.get(key, []):
                if sample_id in exception_list:
                    continue
                row = Coalescence_data[Coalescence_data["SampleIDX"] == sample_id]
                if row.empty:
                    continue
                row = row.iloc[0]

                offspring = abundance_vector(sample_id)
                parent1 = abundance_vector(row["SampleIDX_Sub1"])
                parent2 = abundance_vector(row["SampleIDX_Sub2"])
                if offspring is None or parent1 is None or parent2 is None:
                    continue

                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(parent1, parent2, offspring)
                except Exception:
                    continue
                x_val, y_val = calculate_assymetricity(u, v, k)
                outcome = characterize_case(x_val, y_val)
                if outcome is None:
                    continue

                records.append(
                    {
                        "sample_id": sample_id,
                        "medium": medium,
                        "medium_label": MEDIA_LABELS[medium],
                        "pool_size": pool_size,
                        "outcome_code": outcome,
                        "outcome": OUTCOMES[outcome],
                    }
                )
    return pd.DataFrame(records)


def cochran_armitage(counts: np.ndarray, outcome_col: int) -> tuple[float, float, float]:
    scores = np.arange(counts.shape[0], dtype=float)
    successes = counts[:, outcome_col]
    totals = counts.sum(axis=1)
    pooled = successes.sum() / totals.sum()
    score_mean = np.average(scores, weights=totals)
    numerator = np.sum(scores * (successes - totals * pooled))
    denominator = np.sqrt(pooled * (1 - pooled) * np.sum(totals * (scores - score_mean) ** 2))
    z_stat = numerator / denominator
    chi2_stat = z_stat**2
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return float(z_stat), float(chi2_stat), float(p_value)


def main() -> None:
    records = outcome_records()
    counts = (
        records.groupby(["medium", "medium_label", "outcome_code", "outcome"])
        .size()
        .reset_index(name="count")
    )
    counts["medium"] = pd.Categorical(counts["medium"], categories=MEDIA, ordered=True)
    counts = counts.sort_values(["medium", "outcome_code"])

    count_matrix = (
        counts.pivot(index="medium", columns="outcome_code", values="count")
        .reindex(MEDIA)
        .reindex(columns=[0, 1, 2])
        .fillna(0)
        .astype(int)
        .to_numpy()
    )

    chi2_stat, chi2_p, chi2_dof, _ = stats.chi2_contingency(count_matrix)
    test_rows = [
        {
            "test": "three_category_outcome_distribution_chi_square",
            "statistic": "chi_square",
            "value": float(chi2_stat),
            "df": int(chi2_dof),
            "p_value": float(chi2_p),
        }
    ]

    for outcome_col, outcome_name in OUTCOMES.items():
        z_stat, chi2_trend, p_value = cochran_armitage(count_matrix, outcome_col)
        test_rows.append(
            {
                "test": f"{outcome_name.lower()}_cochran_armitage_trend",
                "statistic": "chi_square",
                "value": chi2_trend,
                "df": 1,
                "p_value": p_value,
                "z_statistic": z_stat,
            }
        )

    counts.to_csv(OUT_DIR / "nutrient_outcome_counts.csv", index=False)
    pd.DataFrame(test_rows).to_csv(OUT_DIR / "nutrient_outcome_tests.csv", index=False)
    print(f"Saved {OUT_DIR / 'nutrient_outcome_counts.csv'}")
    print(f"Saved {OUT_DIR / 'nutrient_outcome_tests.csv'}")


if __name__ == "__main__":
    main()
