"""
make_Q5_filter_rank_abundance_parentfit.py
==========================================

Render a compact diagnostic for the parent-rank-abundance-calibrated
environmental-filter model.

Outputs:
    Q5_filter_rank_abundance_parentfit_summary.csv
    Fig_Q5_filter_rank_abundance_parentfit.{pdf,png,svg}
"""

from __future__ import annotations

import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CODE_DIR = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import environmental_filter_model as filt
import pH_feedback_model as phmod


SEED = 20260511
THRESHOLD = 0.001
N_POOL = 24
SP_PER_PARENT = 12
N_POOLS = 3000
N0_CV = 1.25
MEDIUMS = ["Nutr-", "Base", "Nutr+"]
MEDIUM_CODE_MAP = {"L": "Nutr-", "M": "Base", "H": "Nutr+"}
PARAMS = {
    "Nutr-": filt.FilterParams("Nutr-", theta=0.0, sigma=1.0, gamma=5.0, threshold=THRESHOLD),
    "Base": filt.FilterParams("Base", theta=0.0, sigma=1.0, gamma=11.5, threshold=THRESHOLD),
    "Nutr+": filt.FilterParams("Nutr+", theta=0.0, sigma=1.0, gamma=40.5, threshold=THRESHOLD),
}
EXCEPTION_LIST = {
    "P4-02", "P4-03", "P4-23", "P4-24",
    "P7-97", "P8-12", "P8-91",
    "P5-73", "P5-69", "P5-64", "P5-61", "P5-59", "P5-56",
    "P5-47", "P5-50", "P5-39", "P5-87", "P5-54",
    "P6-02", "P6-47", "P6-74", "P6-57",
}
OUTCOME_COLORS = {
    "Dominance": "#1f77b4",
    "Mixture": "#9ecae1",
    "Restructuring": "#d62728",
}
OUTCOMES = ["Dominance", "Mixture", "Restructuring"]


sns.set_style("ticks")
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["font.size"] = 8
mpl.rcParams["axes.linewidth"] = 0.5
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["text.usetex"] = False


def abundance_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith("NormalizedAbundance")]


def threshold_normalize(x: np.ndarray, threshold: float = THRESHOLD) -> np.ndarray:
    y = np.asarray(x, dtype=float).copy()
    y[y < threshold] = 0.0
    total = float(y.sum())
    if total > 0:
        y /= total
    return y


def rank_curve(x: np.ndarray, max_rank: int = SP_PER_PARENT) -> np.ndarray:
    y = threshold_normalize(x)
    positive = np.sort(y[y > 0.0])[::-1]
    return np.r_[positive, np.zeros(max(0, max_rank - len(positive)))][:max_rank]


def load_observed_parent_ranks() -> dict[str, np.ndarray]:
    seq = pd.read_excel(os.path.join(ROOT, "Postprocessed", "processed_Sequences_synthetic.xlsx"))
    seq = seq.set_index("SampleIDX")
    metadata = pd.read_excel(os.path.join(ROOT, "Analyzed", "processed_CoalescenceEvent_synthetic.xlsx"))
    ab_cols = abundance_columns(seq)

    coalesced = metadata[
        (metadata["CoalescenceType"] == "C")
        & (metadata["CommunityIDX"].between(15, 41))
        & (~metadata["SampleIDX"].isin(EXCEPTION_LIST))
    ].copy()

    ranks = {medium: [] for medium in MEDIUMS}
    seen: set[str] = set()
    for _, row in coalesced.iterrows():
        medium = MEDIUM_CODE_MAP[row["Medium"]]
        for col in ("SampleIDX_Sub1", "SampleIDX_Sub2"):
            sample_id = row[col]
            if sample_id in seen:
                continue
            seen.add(sample_id)
            ranks[medium].append(rank_curve(seq.loc[sample_id, ab_cols].to_numpy(dtype=float)))

    return {medium: np.vstack(ranks[medium]) for medium in MEDIUMS}


def richness(x: np.ndarray) -> int:
    return int(np.sum(np.asarray(x) > phmod.EXTINCTION))


def simulate_parentfit_model() -> tuple[dict[str, np.ndarray], pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    parent_ranks = {medium: [] for medium in MEDIUMS}
    event_rows = []

    for medium in MEDIUMS:
        params = PARAMS[medium]
        for pool_idx in range(N_POOLS):
            pool = filt.sample_trait_pool(N_POOL, rng)
            perm = rng.permutation(N_POOL)
            parents = []
            for c in range(2):
                mask = np.zeros(N_POOL, dtype=bool)
                mask[perm[c * SP_PER_PARENT:(c + 1) * SP_PER_PARENT]] = True
                parent = filt.assemble_parent(pool, mask, params, rng, n0_cv=N0_CV)
                parents.append(parent)
                parent_ranks[medium].append(rank_curve(parent))

            n_c = filt.run_coalescence(pool, params, parents[0], parents[1])
            if not (
                np.any(parents[0] > phmod.EXTINCTION)
                and np.any(parents[1] > phmod.EXTINCTION)
                and np.any(n_c > phmod.EXTINCTION)
            ):
                continue

            outcome, pdi, u, v, k = filt.classify_coalescence(parents[0], parents[1], n_c)
            sorted_c = np.sort(n_c)[::-1]
            event_rows.append({
                "medium": medium,
                "pool": pool_idx,
                "gamma": params.gamma,
                "theta": params.theta,
                "sigma": params.sigma,
                "threshold": params.threshold,
                "n0_cv": N0_CV,
                "outcome": outcome,
                "pdi": pdi,
                "richness_a": richness(parents[0]),
                "richness_b": richness(parents[1]),
                "richness_c": richness(n_c),
                "top1_c": float(sorted_c[:1].sum()),
                "top3_c": float(sorted_c[:3].sum()),
            })

    parent_ranks = {medium: np.vstack(parent_ranks[medium]) for medium in MEDIUMS}
    return parent_ranks, pd.DataFrame(event_rows)


def summarize_events(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for medium in MEDIUMS:
        sub = events[events["medium"] == medium]
        row = {
            "medium": medium,
            "n_events": len(sub),
            "gamma": PARAMS[medium].gamma,
            "theta": PARAMS[medium].theta,
            "sigma": PARAMS[medium].sigma,
            "threshold": THRESHOLD,
            "n0_cv": N0_CV,
            "mean_richness_c": sub["richness_c"].mean(),
            "median_richness_c": sub["richness_c"].median(),
            "min_richness_c": sub["richness_c"].min(),
            "max_richness_c": sub["richness_c"].max(),
            "mean_top1_c": sub["top1_c"].mean(),
            "mean_top3_c": sub["top3_c"].mean(),
        }
        for outcome in OUTCOMES:
            row[f"pct_{outcome.lower()}"] = 100.0 * (sub["outcome"] == outcome).mean()
        rows.append(row)
    return pd.DataFrame(rows)


def plot_rank_curves(ax, observed: dict[str, np.ndarray], model: dict[str, np.ndarray]) -> None:
    x = np.arange(1, SP_PER_PARENT + 1)
    colors = {"Nutr-": "#4c78a8", "Base": "#f58518", "Nutr+": "#54a24b"}
    for medium in MEDIUMS:
        obs_mean = observed[medium].mean(axis=0)
        mod_mean = model[medium].mean(axis=0)
        ax.plot(x, obs_mean, color=colors[medium], linewidth=1.8, label=f"{medium} obs")
        ax.plot(x, mod_mean, color=colors[medium], linewidth=1.4, linestyle="--", label=f"{medium} model")
    ax.set_yscale("log")
    ax.set_xlabel("parental rank")
    ax.set_ylabel("relative abundance")
    ax.set_title("parent rank-abundance fit", fontsize=8, pad=4)
    ax.set_xticks([1, 3, 6, 9, 12])
    ax.set_ylim(0.0008, 0.9)
    ax.legend(frameon=False, fontsize=6, ncol=2, handlelength=1.6)
    sns.despine(ax=ax)


def plot_outcomes(ax, events: pd.DataFrame) -> None:
    x = np.arange(len(MEDIUMS))
    bottoms = np.zeros(len(MEDIUMS))
    for outcome in OUTCOMES:
        heights = np.array([
            100.0 * (events.loc[events["medium"] == medium, "outcome"] == outcome).mean()
            for medium in MEDIUMS
        ])
        ax.bar(
            x,
            heights,
            bottom=bottoms,
            color=OUTCOME_COLORS[outcome],
            edgecolor="black",
            linewidth=0.3,
            width=0.7,
            label=outcome,
        )
        if outcome in {"Dominance", "Restructuring"}:
            for xi, base, h in zip(x, bottoms, heights):
                label = f"{h:.1f}%" if h < 1 else f"{h:.0f}%"
                y = base + h / 2 if h > 6 else base + h + 2
                ax.text(
                    xi,
                    y,
                    label,
                    ha="center",
                    va="center" if h > 6 else "bottom",
                    fontsize=6.5,
                    color="white" if h > 8 else "black",
                    fontweight="bold" if outcome == "Dominance" else "normal",
                )
        bottoms += heights
    ax.set_xticks(x)
    ax.set_xticklabels([
        "Nutr$-$\n$\\gamma$=5.0",
        "Base\n$\\gamma$=11.5",
        "Nutr$+$\n$\\gamma$=40.5",
    ])
    ax.set_ylabel("% coalesced outcomes")
    ax.set_ylim(0, 105)
    ax.set_title("predicted outcomes", fontsize=8, pad=4)
    ax.legend(frameon=False, fontsize=6.5, loc="upper left", bbox_to_anchor=(1.02, 1.0))
    sns.despine(ax=ax)


def plot_richness(ax, summary: pd.DataFrame) -> None:
    x = np.arange(len(MEDIUMS))
    means = summary["mean_richness_c"].to_numpy(dtype=float)
    lows = means - summary["min_richness_c"].to_numpy(dtype=float)
    highs = summary["max_richness_c"].to_numpy(dtype=float) - means
    ax.bar(x, means, color=["#4c78a8", "#f58518", "#54a24b"], edgecolor="black", linewidth=0.3, width=0.65)
    ax.errorbar(x, means, yerr=np.vstack([lows, highs]), color="black", linestyle="none", linewidth=0.8, capsize=2)
    for xi, mean, med in zip(x, means, summary["median_richness_c"]):
        ax.text(xi, mean + 0.45, f"{mean:.1f}", ha="center", va="bottom", fontsize=7, fontweight="bold")
        ax.text(xi, 0.7, f"med {med:.0f}", ha="center", va="bottom", fontsize=6.5)
    ax.set_xticks(x)
    ax.set_xticklabels(["Nutr$-$", "Base", "Nutr$+$"])
    ax.set_ylabel("coalesced richness")
    ax.set_ylim(0, 24)
    ax.set_title("predicted coalesced richness", fontsize=8, pad=4)
    sns.despine(ax=ax)


def main() -> None:
    observed = load_observed_parent_ranks()
    model_parent_ranks, events = simulate_parentfit_model()
    summary = summarize_events(events)
    summary.to_csv(os.path.join(HERE, "Q5_filter_rank_abundance_parentfit_summary.csv"), index=False)

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(10.8, 3.0),
        gridspec_kw={"width_ratios": [1.25, 1.0, 0.95], "wspace": 0.55},
    )
    plot_rank_curves(axes[0], observed, model_parent_ranks)
    plot_outcomes(axes[1], events)
    plot_richness(axes[2], summary)
    fig.suptitle(
        "Q5 / environmental filtering calibrated to parental rank-abundance",
        fontsize=9.5,
        y=1.04,
    )

    out_base = os.path.join(HERE, "Fig_Q5_filter_rank_abundance_parentfit")
    for ext in ("pdf", "png", "svg"):
        fig.savefig(f"{out_base}.{ext}", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(summary.to_string(index=False))
    print(f"Wrote {out_base}.pdf")


if __name__ == "__main__":
    main()
