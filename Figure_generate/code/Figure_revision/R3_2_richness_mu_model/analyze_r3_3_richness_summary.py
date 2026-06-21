#!/usr/bin/env python3
"""Richness-only summary for Reviewer 3 point R3-3."""

from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
import seaborn as sns


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", ".."))
CODE_DIR = os.path.join(PROJECT_ROOT, "Figure_generate", "code")
sys.path.insert(0, CODE_DIR)

_prev_cwd = os.getcwd()
os.chdir(CODE_DIR)
from common_setup import exception_list  # noqa: E402
os.chdir(_prev_cwd)


sns.set_style("ticks")
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["figure.dpi"] = 200
mpl.rcParams["font.size"] = 8
mpl.rcParams["axes.linewidth"] = 0.5
plt.rcParams["text.usetex"] = False
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

THRESHOLD = 0.001
MM = 0.1 / 2.54
MEDIUM_ORDER = ["L", "M", "H"]
MEDIUM_LABELS = {"L": "Nutr-", "M": "Base", "H": "Nutr+"}
POOL_SIZES = [6, 12, 24]
POOL_COLORS = {6: "#4A90D9", 12: "#2ECC71", 24: "#E67E22"}


def get_pool_size_coal(cidx: int) -> int | None:
    cidx = int(cidx)
    if cidx <= 14:
        return 6
    if cidx <= 41:
        return 12
    if cidx <= 47:
        return 24
    return None


def richness_from_row(row: pd.Series, threshold: float = THRESHOLD) -> int:
    abundances = np.asarray(row.iloc[1:], dtype=float)
    return int(np.sum(abundances > threshold))


def load_simulation_richness() -> pd.DataFrame:
    data_path = os.path.join(
        CODE_DIR,
        "Simulation_Data",
        "48species_200reps_fine",
        "Community_200reps_fine.json",
    )
    with open(data_path, "r") as handle:
        sim_data = json.load(handle)

    rows = []
    for mu_key in sorted(sim_data.keys(), key=float):
        mu = float(mu_key)
        sc_richness = []
        cc_richness = []
        for rep_data in sim_data[mu_key].values():
            for vec in rep_data["sc_list"].values():
                sc_richness.append(int(np.sum(np.asarray(vec, dtype=float) > THRESHOLD)))
            for vec in rep_data["cc_list"].values():
                cc_richness.append(int(np.sum(np.asarray(vec, dtype=float) > THRESHOLD)))
        rows.append(
            {
                "mu": mu,
                "sub_mean": float(np.mean(sc_richness)),
                "sub_sem": float(np.std(sc_richness, ddof=1) / np.sqrt(len(sc_richness))),
                "coal_mean": float(np.mean(cc_richness)),
                "coal_sem": float(np.std(cc_richness, ddof=1) / np.sqrt(len(cc_richness))),
            }
        )
    return pd.DataFrame(rows)


def load_experimental_coalesced_richness() -> pd.DataFrame:
    asv_path = os.path.join(PROJECT_ROOT, "Postprocessed", "processed_Sequences_synthetic.xlsx")
    coalescence_path = os.path.join(PROJECT_ROOT, "Analyzed", "processed_CoalescenceEvent_synthetic.xlsx")
    asv_data = pd.read_excel(asv_path)
    coalescence_data = pd.read_excel(coalescence_path)

    richness_lookup = {
        row["SampleIDX"]: richness_from_row(row)
        for _, row in asv_data.iterrows()
    }

    rows = []
    for _, row in coalescence_data.iterrows():
        sid = row["SampleIDX"]
        if sid in exception_list:
            continue
        pool_size = get_pool_size_coal(row["CommunityIDX"])
        if pool_size is None or sid not in richness_lookup:
            continue
        rows.append(
            {
                "SampleIDX": sid,
                "Medium": row["Medium"],
                "PoolSize": pool_size,
                "Richness": richness_lookup[sid],
            }
        )
    return pd.DataFrame(rows)


def make_figure(sim: pd.DataFrame, exp: pd.DataFrame, out_pdf: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(135 * MM, 58 * MM))

    ax = axes[0]
    ax.errorbar(
        sim["mu"],
        sim["sub_mean"],
        yerr=sim["sub_sem"],
        fmt="o-",
        color="#1f77b4",
        markersize=3,
        linewidth=1.1,
        capsize=2,
        capthick=0.5,
        elinewidth=0.5,
        label="Sub-community",
    )
    ax.errorbar(
        sim["mu"],
        sim["coal_mean"],
        yerr=sim["coal_sem"],
        fmt="s-",
        color="#2ca02c",
        markersize=3,
        linewidth=1.1,
        capsize=2,
        capthick=0.5,
        elinewidth=0.5,
        label="Coalesced",
    )
    ax.set_xlabel(r"Interaction strength $\mu$")
    ax.set_ylabel("Final richness")
    ax.set_xlim(0, 1.25)
    ax.set_ylim(bottom=0)
    ax.set_title("A  Simulation", fontsize=8, fontweight="bold", loc="left")
    ax.legend(frameon=False, fontsize=6, loc="upper right")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax = axes[1]
    positions = np.arange(len(MEDIUM_ORDER)) + 1
    width = 0.24
    offsets = [-width, 0, width]
    rng = np.random.default_rng(42)
    for offset, pool_size in zip(offsets, POOL_SIZES):
        data = [
            exp[(exp["Medium"] == medium) & (exp["PoolSize"] == pool_size)]["Richness"].dropna().values
            for medium in MEDIUM_ORDER
        ]
        pos = positions + offset
        bp = ax.boxplot(
            data,
            positions=pos,
            widths=0.18,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": "black", "linewidth": 1},
            whiskerprops={"linewidth": 0.5},
            capprops={"linewidth": 0.5},
            boxprops={"linewidth": 0.5},
        )
        for patch in bp["boxes"]:
            patch.set_facecolor(POOL_COLORS[pool_size])
            patch.set_alpha(0.55)
        for x, vals in zip(pos, data):
            if len(vals) == 0:
                continue
            jitter = rng.uniform(-0.035, 0.035, size=len(vals))
            ax.scatter(
                np.full(len(vals), x) + jitter,
                vals,
                s=5,
                color=POOL_COLORS[pool_size],
                alpha=0.45,
                edgecolors="none",
                zorder=5,
            )
    ax.set_xticks(positions)
    ax.set_xticklabels([MEDIUM_LABELS[m] for m in MEDIUM_ORDER])
    ax.set_xlabel("Medium")
    ax.set_ylabel("Final richness (ASVs)")
    ax.set_title("B  Experiment", fontsize=8, fontweight="bold", loc="left")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, 22)
    ax.legend(
        handles=[
            mpl.patches.Patch(
                facecolor=POOL_COLORS[pool_size],
                edgecolor="black",
                alpha=0.55,
                label=f"{pool_size} species",
            )
            for pool_size in POOL_SIZES
        ],
        fontsize=6,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.52, 1.12),
        ncol=3,
        columnspacing=0.5,
        handlelength=1.0,
        title="Initial pool",
        title_fontsize=6,
    )

    sns.despine(fig=fig)
    fig.tight_layout(w_pad=1.3)
    fig.savefig(out_pdf, bbox_inches="tight", dpi=300)
    fig.savefig(out_pdf.replace(".pdf", ".png"), bbox_inches="tight", dpi=300)
    plt.close(fig)


def main() -> None:
    sim = load_simulation_richness()
    exp = load_experimental_coalesced_richness()
    sim.to_csv(os.path.join(SCRIPT_DIR, "r3_3_simulation_richness_summary.csv"), index=False)
    exp.to_csv(os.path.join(SCRIPT_DIR, "r3_3_experimental_coalesced_richness.csv"), index=False)
    make_figure(sim, exp, os.path.join(SCRIPT_DIR, "Fig_R3_3_richness_summary.pdf"))

    print("Simulation richness:")
    print(sim.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\nExperimental coalesced richness by medium:")
    summary = exp.groupby("Medium")["Richness"].agg(["count", "median", "mean", "std"])
    print(summary.to_string(float_format=lambda x: f"{x:.3f}"))


if __name__ == "__main__":
    main()
