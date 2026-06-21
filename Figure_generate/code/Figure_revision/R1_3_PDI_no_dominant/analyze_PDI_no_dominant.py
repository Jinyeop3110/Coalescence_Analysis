"""
analyze_PDI_no_dominant.py  (R1-3)

Purpose: Test whether the PDI (Predictive Dominance Index) correlation in
Fig. 5C is circular -- i.e., does the correlation survive when the dominant
species is removed from parent and coalesced compositions before re-
calculating vector decomposition?

Analyses:
  (a) Original Fig. 5C-style scatter (M+H combined) for reference
  (b) Same scatter but with dominant species removed + renormalized
  (c) Comparison of R^2 (original vs dominant-removed)

Figures saved alongside this script (.svg, .pdf, .png at 300 dpi).
"""

import sys, os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
np.random.seed(42)

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(CODE_DIR, "..", ".."))
sys.path.insert(0, CODE_DIR)

# ---------------------------------------------------------------------------
# Import project-wide setup
# ---------------------------------------------------------------------------
os.chdir(CODE_DIR)
from common_setup import (
    Coalescence_data,
    Processed_sequences_synthetic,
    Syn_Coal_IDX,
    exception_list,
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case,
    mm,
)
from COLORMAP import (
    PHASE_DIAGRAM_COLORS,
    get_medium_colors,
)

# ---------------------------------------------------------------------------
# Style overrides
# ---------------------------------------------------------------------------
sns.set_style("ticks")
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
plt.rcParams['text.usetex'] = False

COLOR_DOM  = PHASE_DIAGRAM_COLORS['dominance']
COLOR_MIX  = PHASE_DIAGRAM_COLORS['mixing']
COLOR_REST = PHASE_DIAGRAM_COLORS['restructuring']
MEDIUM_CLR = get_medium_colors()


def format_p_value(p_value):
    """Compact p-value formatting for figure annotations."""
    if not np.isfinite(p_value):
        return 'n/a'
    if p_value < 1e-3:
        return f'{p_value:.1e}'
    return f'{p_value:.3f}'

# ---------------------------------------------------------------------------
# Load pairwise count data (from experimental colony counting)
# ---------------------------------------------------------------------------
def getPairwiseCountData():
    """Load pairwise count data from experimental files."""
    # Primary path
    Pairwise_Count_data_path = os.path.join(
        PROJECT_ROOT, "Postprocessed",
        "PairwiseColonyCountings_processed_230915.xlsx"
    )
    if not os.path.exists(Pairwise_Count_data_path):
        # Fallback: try legacy path
        Pairwise_Count_data_path = os.path.join(
            PROJECT_ROOT, "ExperimentalResult", "Data",
            "2208_Coalescence_processed", "PairwiseAssay",
            "230816_PairwiseAssay_All_analyzed.xlsx"
        )

    # Sheet names: LN_mono, MN_mono, HN_mono, LN_1, LN_2, MN_1, MN_2, HN_1, HN_2
    Mono_Count_data = {}
    Pairwise_Count_data = {}
    for medium in ["LN", "MN", "HN"]:
        Data = pd.read_excel(Pairwise_Count_data_path, sheet_name=f"{medium}_mono")
        Data = np.array(Data.values[:, 1:])
        Mono_Count_data[medium] = Data

    for medium in ["LN", "MN", "HN"]:
        Data_1 = pd.read_excel(Pairwise_Count_data_path, sheet_name=f"{medium}_1")
        Data_1 = np.array(Data_1.values[:, 1:])
        Data_2 = pd.read_excel(Pairwise_Count_data_path, sheet_name=f"{medium}_2")
        Data_2 = np.array(Data_2.values[:, 1:])
        Data = np.stack([Data_1, Data_2])
        Pairwise_Count_data[medium] = Data

    return Mono_Count_data, Pairwise_Count_data


def getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium_type):
    """Process pairwise count data to calculate ratios."""
    data_m = np.mean(Mono_Count_data[medium_type], 0)  # average replicates -> (12,)
    data_p_1 = Pairwise_Count_data[medium_type][0, :]
    data_p_2 = Pairwise_Count_data[medium_type][1, :]
    data_flag = np.array([[None] * 12] * 12)
    data_p_1_converted = np.array([[None] * 12] * 12)
    data_p_2_converted = np.array([[None] * 12] * 12)
    data_p_ratio = np.array([[None] * 12] * 12)

    for i in range(12):
        for j in range(12):
            if np.isnan(data_p_1[i, j]):
                data_flag[i, j] = 'case0'
            else:
                if data_p_1[i, j] == 1 and data_p_2[i, j] == 0:
                    data_flag[i, j] = 'case1'
                    data_p_1_converted[i, j] = 1
                    data_p_2_converted[i, j] = 0
                    data_p_ratio[i, j] = 1
                elif data_p_1[i, j] == 0 and data_p_2[i, j] == 1:
                    data_flag[i, j] = 'case2'
                    data_p_1_converted[i, j] = 0
                    data_p_2_converted[i, j] = 1
                    data_p_ratio[i, j] = 0
                else:
                    data_flag[i, j] = 'case3'
                    data_p_1_converted[i, j] = data_p_1[i, j] / data_m[i]
                    data_p_2_converted[i, j] = data_p_2[i, j] / data_m[j]
                    if data_p_1_converted[i, j] + data_p_2_converted[i, j] > 0:
                        data_p_ratio[i, j] = (data_p_1_converted[i, j]
                                               / (data_p_1_converted[i, j] + data_p_2_converted[i, j]))
                    else:
                        data_p_ratio[i, j] = None

    return data_p_1, data_p_2, data_flag, data_p_ratio


# ===========================================================================
# Core analysis: compute PDI correlation with and without dominant species
# ===========================================================================

def compute_pdi_data(remove_dominant=False, removal_mode='mix', medium_filter=None):
    """
    Compute the PDI scatter data (x = species-level dominance, y = community-
    level dominance) for M and H media combined, or a single medium.

    Inclusion criteria are anchored to the original Fig. 5C-style calculation:
    an event must be non-restructuring before any dominant-species removal and
    must have a valid pairwise-assay lookup for the original two parent-dominant
    species. Removal modes then change only the community-level PDI calculation
    on that original-selected event set.

    Parameters
    ----------
    remove_dominant : bool
        If False, no removal (original Fig 5C). If True, apply `removal_mode`.
    removal_mode : {'mix', 'parents'}
        'mix'     → remove argmax(c_mix) from all three vectors (original logic,
                    targets the species that defined the Dominance outcome).
        'parents' → remove argmax(c_1) AND argmax(c_2) from all three vectors
                    (symmetric: removes each parental community's own dominant species).
    medium_filter : {'M', 'H', None}
        If 'M' or 'H', restrict to that medium. If None, combine both.

    Returns
    -------
    dict with keys: x_orig, y_orig, x_dup, y_dup, pool, medium,
                    slope, intercept, r_squared, n_events
    """
    try:
        Mono_Count_data, Pairwise_Count_data = getPairwiseCountData()
    except Exception as e:
        print(f"WARNING: Could not load pairwise count data: {e}")
        print("Falling back to vector-decomposition-only analysis without species-level PDI.")
        return None

    all_x_orig = []
    all_y_orig = []
    all_pool = []
    all_medium = []
    n_failed = 0
    n_empty_after_removal = 0

    mediums_to_run = ['M', 'H'] if medium_filter is None else [medium_filter]
    for medium in mediums_to_run:
        data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData(
            Mono_Count_data, Pairwise_Count_data, medium + 'N')

        for pool_size in [6, 12, 24]:
            type_name = medium + f'N_{pool_size}'
            IDX_list = Syn_Coal_IDX[type_name]
            idx = np.squeeze([np.where(Coalescence_data['SampleIDX'] == x) for x in IDX_list])
            coal_rows = Coalescence_data.iloc[idx]
            idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x) for x in coal_rows["SampleIDX_Sub1"].tolist()])
            idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x) for x in coal_rows["SampleIDX_Sub2"].tolist()])
            idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x) for x in IDX_list])

            for i in range(len(idx)):
                c_mix = np.array(Processed_sequences_synthetic.iloc[idx[i]].values[1:], dtype=float)
                c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values[1:], dtype=float)
                c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values[1:], dtype=float)
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)

                # Identify most abundant species in parents (for pairwise lookup)
                C1_orig = np.argmax(c_1)
                C2_orig = np.argmax(c_2)

                # Original Fig. 5C-style vector decomposition defines the event
                # set for all columns. This prevents the "dominant removed"
                # panels from silently changing the filter because their
                # recalculated PDI shifts an event across the restructuring
                # boundary.
                try:
                    u_orig_filter, v_orig_filter, k_orig_filter = metric_VectorDecomposition_onlyPositive(
                        c_1, c_2, c_mix)
                except Exception:
                    # VectorDecomposition can fail on degenerate compositions
                    # (e.g., one parent is all zeros after threshold filtering)
                    n_failed += 1
                    continue

                original_retention = u_orig_filter**2 + v_orig_filter**2
                if original_retention <= 0.5:
                    continue

                if remove_dominant:
                    c_1_mod = c_1.copy()
                    c_2_mod = c_2.copy()
                    c_mix_mod = c_mix.copy()

                    if removal_mode == 'mix':
                        # Remove argmax(c_mix) from all three
                        dom_idx = [np.argmax(c_mix)]
                    elif removal_mode == 'parents':
                        # Remove argmax(c_1) AND argmax(c_2) from all three
                        dom_idx = list({int(np.argmax(c_1)), int(np.argmax(c_2))})
                    else:
                        raise ValueError(f"Unknown removal_mode: {removal_mode}")

                    for di in dom_idx:
                        c_1_mod[di] = 0
                        c_2_mod[di] = 0
                        c_mix_mod[di] = 0

                    # Renormalize
                    s1 = np.sum(c_1_mod)
                    s2 = np.sum(c_2_mod)
                    sm = np.sum(c_mix_mod)
                    if s1 <= 0 or s2 <= 0 or sm <= 0:
                        n_empty_after_removal += 1
                        continue
                    c_1_mod = c_1_mod / s1
                    c_2_mod = c_2_mod / s2
                    c_mix_mod = c_mix_mod / sm

                    try:
                        u, v, k = metric_VectorDecomposition_onlyPositive(c_1_mod, c_2_mod, c_mix_mod)
                    except Exception:
                        # VectorDecomposition can fail when modified compositions are
                        # near-zero or numerically degenerate after dominant removal
                        n_failed += 1
                        continue
                else:
                    u, v, k = u_orig_filter, v_orig_filter, k_orig_filter

                # Community-level dominance score
                vector_similarity_score = np.arctan(u / (v + 1e-8)) - np.pi / 4

                if np.isnan(vector_similarity_score) or np.isinf(vector_similarity_score):
                    continue

                # Species must be within pairwise matrix bounds
                if C1_orig >= 12 or C2_orig >= 12:
                    continue
                if data_p_ratio[C1_orig, C2_orig] is None:
                    continue

                # Species-level dominance (from pairwise assay)
                species_dom = np.mean([1 - data_p_ratio[C1_orig, C2_orig],
                                       data_p_ratio[C2_orig, C1_orig]])
                x_raw = 1 - species_dom
                ratio = x_raw / (1 - x_raw + 1e-8)
                x_norm = np.arctan(ratio) / (np.pi / 2)

                all_x_orig.append(x_norm)
                all_y_orig.append(vector_similarity_score)
                all_pool.append(pool_size)
                all_medium.append(medium)

    print(f"Events failed: {n_failed}")
    if remove_dominant:
        print(f"Events empty after {removal_mode} removal: {n_empty_after_removal}")

    x_orig = np.array(all_x_orig)
    y_orig = np.array(all_y_orig)
    pool_arr = np.array(all_pool)
    med_arr = np.array(all_medium)

    # Duplicate (reflection symmetry)
    x_dup = np.concatenate([x_orig, 1 - x_orig])
    y_dup = np.concatenate([y_orig, -y_orig])

    # Note: R^2 computed on reflection-duplicated data (2N points) to enforce symmetry
    if len(x_dup) > 2:
        slope, intercept = np.polyfit(x_dup, y_dup, 1)
        y_pred = slope * x_dup + intercept
        ss_res = np.sum((y_dup - y_pred) ** 2)
        ss_tot = np.sum((y_dup - np.mean(y_dup)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    else:
        slope = intercept = r_squared = 0

    return {
        'x_orig': x_orig, 'y_orig': y_orig,
        'x_dup': x_dup, 'y_dup': y_dup,
        'pool': pool_arr, 'medium': med_arr,
        'slope': slope, 'intercept': intercept, 'r_squared': r_squared,
        'n_events': len(x_orig),
    }


# ===========================================================================
# Shared event iterator — used by compute_vd_pdi_data() and top-K loop
# ===========================================================================

def _iter_coal_events():
    """
    Yield (sample_idx, medium_label, pool_size, c_1, c_2, c_mix) for every
    valid coalescence event.  Threshold-filtered (>1e-4) arrays are returned.
    """
    mediums_loop = ['L', 'M', 'H']
    medium_labels_loop = ['LN', 'MN', 'HN']
    pool_sizes_loop = [6, 12, 24]

    for m_i, medium in enumerate(mediums_loop):
        for sp in pool_sizes_loop:
            key = f"{medium_labels_loop[m_i]}_{sp}"
            coal_idx_list = Syn_Coal_IDX.get(key, [])
            if len(coal_idx_list) == 0:
                continue

            for sample_idx in coal_idx_list:
                if sample_idx in exception_list:
                    continue

                seq_idx = np.where(Processed_sequences_synthetic['SampleIDX'] == sample_idx)[0]
                row_coal = Coalescence_data[Coalescence_data['SampleIDX'] == sample_idx]
                if row_coal.empty or len(seq_idx) == 0:
                    continue

                sub1_id = row_coal['SampleIDX_Sub1'].values[0]
                sub2_id = row_coal['SampleIDX_Sub2'].values[0]

                seq_idx1 = np.where(Processed_sequences_synthetic['SampleIDX'] == sub1_id)[0]
                seq_idx2 = np.where(Processed_sequences_synthetic['SampleIDX'] == sub2_id)[0]
                if len(seq_idx1) == 0 or len(seq_idx2) == 0:
                    continue

                c_mix = np.array(Processed_sequences_synthetic.iloc[seq_idx[0]].values[1:], dtype=float)
                c_1 = np.array(Processed_sequences_synthetic.iloc[seq_idx1[0]].values[1:], dtype=float)
                c_2 = np.array(Processed_sequences_synthetic.iloc[seq_idx2[0]].values[1:], dtype=float)
                c_1 = c_1 * (c_1 > 1e-4)
                c_2 = c_2 * (c_2 > 1e-4)

                yield sample_idx, medium_labels_loop[m_i], sp, c_1, c_2, c_mix


# ===========================================================================
# Alternative analysis: vector-decomposition-only PDI (no pairwise assay)
# ===========================================================================

def compute_vd_pdi_data():
    """
    Compute PDI using only vector decomposition (no pairwise assay data).
    Returns a DataFrame with original and dominant-removed VD results per event.
    """
    records = []

    for sample_idx, medium_label, sp, c_1, c_2, c_mix in _iter_coal_events():
        # Original VD
        try:
            u_orig, v_orig, k_orig = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
        except Exception:
            continue
        x_val, y_val = calculate_assymetricity(u_orig, v_orig, k_orig)
        outcome_orig = characterize_case(x_val, y_val)
        if outcome_orig is None:
            continue

        # Modified VD (remove dominant species from coalesced)
        dom_species = np.argmax(c_mix)
        c_1m, c_2m, c_mm = c_1.copy(), c_2.copy(), c_mix.copy()
        c_1m[dom_species] = c_2m[dom_species] = c_mm[dom_species] = 0

        s1, s2, sm = np.sum(c_1m), np.sum(c_2m), np.sum(c_mm)
        if s1 <= 0 or s2 <= 0 or sm <= 0:
            u_mod = v_mod = k_mod = np.nan
            outcome_mod = None
        else:
            c_1m /= s1
            c_2m /= s2
            c_mm /= sm
            try:
                u_mod, v_mod, k_mod = metric_VectorDecomposition_onlyPositive(c_1m, c_2m, c_mm)
            except Exception:
                u_mod = v_mod = k_mod = np.nan
                outcome_mod = None
            else:
                x_m, y_m = calculate_assymetricity(u_mod, v_mod, k_mod)
                outcome_mod = characterize_case(x_m, y_m)

        records.append({
            'SampleIDX': sample_idx,
            'Medium': medium_label,
            'PoolSize': sp,
            'u_orig': u_orig, 'v_orig': v_orig, 'k_orig': k_orig,
            'outcome_orig': outcome_orig,
            'u_mod': u_mod, 'v_mod': v_mod, 'k_mod': k_mod,
            'outcome_mod': outcome_mod,
            'dom_species': dom_species,
        })

    return pd.DataFrame(records)


# ===========================================================================
# Run analyses
# ===========================================================================

print("=" * 60)
print("R1-3: PDI Without Dominant Species (Circularity Check)")
print("=" * 60)

# --- Try PDI with pairwise data (Fig 5C replication) ---
data_orig = compute_pdi_data(remove_dominant=False)
data_mod  = compute_pdi_data(remove_dominant=True)

if data_orig is not None and data_mod is not None:
    print(f"\n--- PDI Correlation (Fig 5C style, M+H combined) ---")
    print(f"Original:        n={data_orig['n_events']}, R^2={data_orig['r_squared']:.4f}, "
          f"slope={data_orig['slope']:.4f}")
    print(f"Dominant removed: n={data_mod['n_events']}, R^2={data_mod['r_squared']:.4f}, "
          f"slope={data_mod['slope']:.4f}")
    print(f"R^2 change: {data_mod['r_squared'] - data_orig['r_squared']:.4f}")

    # Fraction of aligned points
    for label, d in [('Original', data_orig), ('Dominant removed', data_mod)]:
        aligned = ((d['x_dup'] > 0.5) & (d['y_dup'] > 0)) | ((d['x_dup'] < 0.5) & (d['y_dup'] < 0))
        frac = np.mean(aligned)
        print(f"  {label} aligned fraction: {frac:.3f}")

    HAS_PAIRWISE = True
else:
    print("\nPairwise count data not available. Using vector-decomposition-only analysis.")
    HAS_PAIRWISE = False

# --- VD-only analysis (always available) ---
vd_df = compute_vd_pdi_data()
print(f"\n--- Vector Decomposition Only (all media, all pools) ---")
print(f"Total events: {len(vd_df)}")

# Compare outcome classifications
for outcome_name, outcome_val in [('Dominance', 0), ('Mixture', 1), ('Restructuring', 2)]:
    n_orig = (vd_df['outcome_orig'] == outcome_val).sum()
    n_mod = (vd_df['outcome_mod'] == outcome_val).sum()
    print(f"  {outcome_name}: orig={n_orig}, dom-removed={n_mod}")

# Among original Dominance events, what happens after removal?
dom_events = vd_df[vd_df['outcome_orig'] == 0].copy()
print(f"\n--- Dominance events after dominant species removal ---")
print(f"Total Dominance events: {len(dom_events)}")
for outcome_name, outcome_val in [('Dominance', 0), ('Mixture', 1), ('Restructuring', 2)]:
    n = (dom_events['outcome_mod'] == outcome_val).sum()
    print(f"  Reclassified as {outcome_name}: {n} ({n/len(dom_events)*100:.1f}%)")
n_none = dom_events['outcome_mod'].isna().sum()
print(f"  Unclassifiable (empty after removal): {n_none} ({n_none/len(dom_events)*100:.1f}%)")

# Correlation of VD coefficients (orig vs mod) for direction consistency
valid = dom_events.dropna(subset=['u_mod', 'v_mod'])
if len(valid) > 5:
    # Direction: which parent dominates? u > v means parent 1 wins
    orig_direction = np.sign(valid['u_orig'] - valid['v_orig'])
    mod_direction = np.sign(valid['u_mod'] - valid['v_mod'])
    agree = (orig_direction == mod_direction).mean()
    print(f"\n  Direction agreement (same winner): {agree:.3f} ({int(agree*len(valid))}/{len(valid)})")

    # Correlation of asymmetricity scores
    orig_score = np.arctan(valid['u_orig'] / (valid['v_orig'] + 1e-8)) - np.pi/4
    mod_score = np.arctan(valid['u_mod'] / (valid['v_mod'] + 1e-8)) - np.pi/4
    rho, pval = stats.spearmanr(orig_score, mod_score)
    print(f"  Spearman correlation (orig vs mod community score): rho={rho:.4f}, p={pval:.4e}")


# ============================================================================
# FIGURES
# ============================================================================

# --------------------------------------------------------------------------
# Figure (a) + (b): Side-by-side scatter if pairwise data available
# --------------------------------------------------------------------------
if HAS_PAIRWISE:
    fig, axes = plt.subplots(1, 2, figsize=(100*mm, 50*mm), facecolor='w', sharey=True)

    for panel_i, (d, title_str, ax) in enumerate(zip(
            [data_orig, data_mod],
            ['Original', 'Dominant species removed'],
            axes)):

        # Heatmap background
        section_size_x = 1.0/3 + 1e-8
        section_size_y = (np.pi/2)/3 + 1e-8
        sections_x = np.arange(0, 1.1, section_size_x)
        sections_y = np.arange(-np.pi/4, np.pi/4 + section_size_y, section_size_y)
        count_matrix = np.zeros((len(sections_x)-1, len(sections_y)-1))
        for ii in range(len(sections_x)-1):
            for jj in range(len(sections_y)-1):
                count_matrix[ii, jj] = np.sum(
                    (d['x_dup'] >= sections_x[ii]) & (d['x_dup'] < sections_x[ii+1]) &
                    (d['y_dup'] >= sections_y[jj]) & (d['y_dup'] < sections_y[jj+1]))
        ax.pcolormesh(sections_x, sections_y, count_matrix, cmap='gist_yarg', alpha=0.1)

        markers = {6: 'o', 12: 's', 24: '^'}
        for medium in ['M', 'H']:
            mask_m = d['medium'] == medium
            color = MEDIUM_CLR[1] if medium == 'M' else MEDIUM_CLR[2]

            # Duplicated (grey)
            x_dup_m = 1 - d['x_orig'][mask_m]
            y_dup_m = -d['y_orig'][mask_m]
            for ps in [6, 12, 24]:
                mask_ps = d['pool'][mask_m] == ps
                if np.any(mask_ps):
                    ax.scatter(x_dup_m[mask_ps], y_dup_m[mask_ps],
                               color='grey', s=12, alpha=0.2, marker=markers[ps], zorder=1)

            # Original (colored)
            for ps in [6, 12, 24]:
                mask_ps = d['pool'][mask_m] == ps
                if np.any(mask_ps):
                    ax.scatter(d['x_orig'][mask_m][mask_ps], d['y_orig'][mask_m][mask_ps],
                               color=color, s=12, alpha=0.5, marker=markers[ps], zorder=2)

        # Regression line
        ax.plot([0, 1], d['slope'] * np.array([0, 1]) + d['intercept'],
                'k-', linewidth=1, alpha=0.7)

        ax.annotate(f'$R^2$ = {d["r_squared"]:.2f}\nn = {d["n_events"]}',
                    xy=(0.95, 0.05), xycoords='axes fraction',
                    fontsize=7, ha='right', va='bottom')
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-np.pi/4 - 0.05, np.pi/4 + 0.05)
        ax.set_xticks([0, 1])
        ax.set_yticks([-np.pi/4, 0, np.pi/4])
        ax.set_yticklabels([r'$-\pi/4$', '0', r'$\pi/4$'])
        ax.set_xlabel('Species-level dominance', fontsize=8)
        if panel_i == 0:
            ax.set_ylabel('Community-level dominance', fontsize=8)
        ax.set_title(title_str, fontsize=7)
        sns.despine(ax=ax)

    fig.tight_layout()
    for ext in ['svg', 'pdf', 'png']:
        fig.savefig(os.path.join(SCRIPT_DIR, f'Fig_R1_3ab_PDI_comparison.{ext}'),
                    dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"\nFigure (a+b) saved to {SCRIPT_DIR}")


# --------------------------------------------------------------------------
# Figure (c): VD-based outcome reclassification after removal
# --------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(100*mm, 45*mm), facecolor='w')

# Panel c1: Stacked bar of reclassified outcomes for Dominance events
ax = axes[0]
dom_events_clean = dom_events.dropna(subset=['outcome_mod'])
n_stay_dom = (dom_events_clean['outcome_mod'] == 0).sum()
n_become_mix = (dom_events_clean['outcome_mod'] == 1).sum()
n_become_rest = (dom_events_clean['outcome_mod'] == 2).sum()
n_total = len(dom_events_clean)

fracs = [n_stay_dom/n_total, n_become_mix/n_total, n_become_rest/n_total]
labels = ['Still Dominance', 'Became Mixture', 'Became Restructuring']
colors_bars = [COLOR_DOM, COLOR_MIX, COLOR_REST]

bars = ax.bar(np.arange(3), fracs, color=colors_bars, alpha=0.7,
              edgecolor='black', linewidth=0.5, width=0.6)
for bar, frac, (n, label_str) in zip(bars, fracs, zip([n_stay_dom, n_become_mix, n_become_rest], labels)):
    ax.text(bar.get_x() + bar.get_width()/2, frac + 0.02,
            f'{n}/{n_total}', ha='center', va='bottom', fontsize=6)

ax.set_xticks(np.arange(3))
ax.set_xticklabels(['Dom', 'Mix', 'Rest'], fontsize=7)
ax.set_ylabel('Fraction of orig. Dominance events', fontsize=7)
ax.set_ylim(0, 1)
ax.set_title('After dominant sp. removal', fontsize=7)
sns.despine(ax=ax)

# Panel c2: Scatter of original vs modified community score (direction)
ax = axes[1]
valid = dom_events.dropna(subset=['u_mod', 'v_mod']).copy()
if len(valid) > 0:
    orig_score = np.arctan(valid['u_orig'].values / (valid['v_orig'].values + 1e-8)) - np.pi/4
    mod_score = np.arctan(valid['u_mod'].values / (valid['v_mod'].values + 1e-8)) - np.pi/4

    # Color by medium
    for med, color in zip(['LN', 'MN', 'HN'], MEDIUM_CLR):
        mask_m = valid['Medium'] == med
        ax.scatter(orig_score[mask_m], mod_score[mask_m],
                   s=6, color=color, alpha=0.5, label=med, edgecolors='none')

    # Diagonal
    lims = [min(orig_score.min(), mod_score.min()),
            max(orig_score.max(), mod_score.max())]
    ax.plot(lims, lims, 'k--', linewidth=0.5, alpha=0.3)
    ax.axhline(0, color='gray', linewidth=0.3, alpha=0.3)
    ax.axvline(0, color='gray', linewidth=0.3, alpha=0.3)

    rho_val, p_val = stats.spearmanr(orig_score, mod_score)
    ax.annotate(f'Spearman $\\rho$ = {rho_val:.2f}\np = {p_val:.2e}',
                xy=(0.05, 0.95), xycoords='axes fraction',
                fontsize=6, ha='left', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax.set_xlabel('Original community score', fontsize=7)
ax.set_ylabel('Dom.-removed community score', fontsize=7)
ax.legend(fontsize=5, frameon=False, loc='lower right')
sns.despine(ax=ax)

fig.tight_layout()
for ext in ['svg', 'pdf', 'png']:
    fig.savefig(os.path.join(SCRIPT_DIR, f'Fig_R1_3c_VD_reclassification.{ext}'),
                dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"Figure (c) saved to {SCRIPT_DIR}")


# --------------------------------------------------------------------------
# Figure (d): R^2 comparison bar (if pairwise data available)
# --------------------------------------------------------------------------
if HAS_PAIRWISE:
    fig, ax = plt.subplots(figsize=(40*mm, 45*mm), facecolor='w')

    r2_vals = [data_orig['r_squared'], data_mod['r_squared']]
    labels = ['Original', 'Dom.\nremoved']
    bar_colors = ['#555555', COLOR_DOM]

    bars = ax.bar(np.arange(2), r2_vals, color=bar_colors, alpha=0.7,
                  edgecolor='black', linewidth=0.5, width=0.5)
    for bar, r2 in zip(bars, r2_vals):
        ax.text(bar.get_x() + bar.get_width()/2, r2 + 0.02,
                f'{r2:.2f}', ha='center', va='bottom', fontsize=7)

    ax.set_xticks(np.arange(2))
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel(r'$R^2$', fontsize=8)
    ax.set_ylim(0, max(r2_vals)*1.3 if max(r2_vals) > 0 else 1)
    ax.set_title('PDI correlation', fontsize=7)
    sns.despine(ax=ax)

    fig.tight_layout()
    for ext in ['svg', 'pdf', 'png']:
        fig.savefig(os.path.join(SCRIPT_DIR, f'Fig_R1_3d_R2_comparison.{ext}'),
                    dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Figure (d) saved to {SCRIPT_DIR}")


# ==========================================================================
# Per-medium comparison: Base (M) vs Nutr+ (H) × {Original, Dom-from-mix,
# Dom-from-each-parent}. Addresses reviewer R1-3 concern that removing the
# mix-winner's species may not be the most neutral circularity test.
# ==========================================================================
if HAS_PAIRWISE:
    print("\n" + "=" * 60)
    print("PER-MEDIUM COMPARISON (Base / Nutr+) × (orig / mix / parents)")
    print("=" * 60)

    perm_data = {}
    for med_key, med_label in [('M', 'Base'), ('H', 'Nutr+')]:
        perm_data[med_key] = {
            'orig':    compute_pdi_data(remove_dominant=False, medium_filter=med_key),
            'mix':     compute_pdi_data(remove_dominant=True,  removal_mode='mix',
                                        medium_filter=med_key),
            'parents': compute_pdi_data(remove_dominant=True,  removal_mode='parents',
                                        medium_filter=med_key),
        }
        for mode in ['orig', 'mix', 'parents']:
            d = perm_data[med_key][mode]
            if d is None:
                continue
            print(f"  {med_label:6s} | {mode:8s} | n={d['n_events']:3d}, "
                  f"R^2={d['r_squared']:.3f}, slope={d['slope']:.3f}")

    # --- 2×3 scatter grid ---
    fig_pm, axes_pm = plt.subplots(2, 3, figsize=(135 * mm, 85 * mm),
                                    facecolor='w', sharex=True, sharey=True)
    col_titles = ['Original',
                  'Dominant from mix\nremoved',
                  'Dominant from each parental\ncommunity removed']
    row_labels = ['Base (MN)', 'Nutr$^+$ (HN)']
    markers = {6: 'o', 12: 's', 24: '^'}

    for ri, med_key in enumerate(['M', 'H']):
        medium_color = MEDIUM_CLR[1] if med_key == 'M' else MEDIUM_CLR[2]
        for ci, mode in enumerate(['orig', 'mix', 'parents']):
            ax = axes_pm[ri, ci]
            d = perm_data[med_key][mode]
            if d is None or d['n_events'] == 0:
                ax.text(0.5, 0.5, 'no data', ha='center', va='center',
                        transform=ax.transAxes, fontsize=7)
                continue

            # Duplicated (grey reflection)
            for ps in [6, 12, 24]:
                mask = d['pool'] == ps
                if np.any(mask):
                    ax.scatter(1 - d['x_orig'][mask], -d['y_orig'][mask],
                               color='grey', s=10, alpha=0.25,
                               marker=markers[ps], zorder=1,
                               edgecolors='none')
            # Original (colored)
            for ps in [6, 12, 24]:
                mask = d['pool'] == ps
                if np.any(mask):
                    ax.scatter(d['x_orig'][mask], d['y_orig'][mask],
                               color=medium_color, s=12, alpha=0.65,
                               marker=markers[ps], zorder=2,
                               edgecolors='none')

            # Regression line
            ax.plot([0, 1], d['slope'] * np.array([0, 1]) + d['intercept'],
                    'k-', linewidth=0.8, alpha=0.7)

            finite_orig = np.isfinite(d['x_orig']) & np.isfinite(d['y_orig'])
            if np.sum(finite_orig) > 3:
                lr_orig = stats.linregress(d['x_orig'][finite_orig],
                                            d['y_orig'][finite_orig])
                rho_orig, p_spear = stats.spearmanr(d['x_orig'][finite_orig],
                                                     d['y_orig'][finite_orig])
                annotation = (
                    f'$R^2$={d["r_squared"]:.2f}, slope={d["slope"]:.2f}\n'
                    f'$\\rho_S$={rho_orig:.2f}, p={format_p_value(p_spear)}'
                )
            else:
                annotation = (
                    f'$R^2$={d["r_squared"]:.2f}, slope={d["slope"]:.2f}'
                )

            ax.annotate(annotation,
                        xy=(0.95, 0.05), xycoords='axes fraction',
                        fontsize=6.5, ha='right', va='bottom')

            ax.set_xlim(-0.05, 1.05)
            ax.set_ylim(-np.pi / 4 - 0.05, np.pi / 4 + 0.05)
            ax.set_xticks([0, 0.5, 1])
            ax.set_yticks([-np.pi / 4, 0, np.pi / 4])
            ax.set_yticklabels([r'$-\pi/4$', '0', r'$\pi/4$'])
            ax.axhline(0, color='gray', linewidth=0.3, alpha=0.4)
            ax.axvline(0.5, color='gray', linewidth=0.3, alpha=0.4)

            if ri == 0:
                ax.set_title(col_titles[ci], fontsize=7)
            if ri == 1:
                ax.set_xlabel('Species-level dominance', fontsize=7)
            if ci == 0:
                ax.set_ylabel(f'{row_labels[ri]}\ncommunity-level dom.',
                              fontsize=7)
            sns.despine(ax=ax)

    fig_pm.tight_layout()
    for ext in ['svg', 'pdf', 'png']:
        fig_pm.savefig(os.path.join(SCRIPT_DIR,
                                     f'Fig_R1_3_per_medium_scatter.{ext}'),
                       dpi=300, bbox_inches='tight')
    plt.close(fig_pm)
    print(f"Per-medium scatter grid saved to {SCRIPT_DIR}")

    # --- Summary bar chart: R^2 grouped by medium × strategy ---
    fig_bar, ax_bar = plt.subplots(figsize=(70 * mm, 55 * mm), facecolor='w')
    strategies = ['orig', 'mix', 'parents']
    strat_labels = ['Original', 'Dom(mix)\nremoved', 'Dom(parental)\nremoved']
    med_order = [('M', 'Base', MEDIUM_CLR[1]), ('H', 'Nutr$^+$', MEDIUM_CLR[2])]
    width = 0.35
    xpos = np.arange(len(strategies))

    for off_i, (med_key, med_label, clr) in enumerate(med_order):
        r2s = [perm_data[med_key][s]['r_squared']
               if perm_data[med_key][s] is not None else 0
               for s in strategies]
        bars = ax_bar.bar(xpos + (off_i - 0.5) * width, r2s,
                          width=width, color=clr, alpha=0.75,
                          edgecolor='black', linewidth=0.5, label=med_label)
        for b, v in zip(bars, r2s):
            ax_bar.text(b.get_x() + b.get_width() / 2, v + 0.008,
                        f'{v:.2f}', ha='center', va='bottom', fontsize=6)

    ax_bar.set_xticks(xpos)
    ax_bar.set_xticklabels(strat_labels, fontsize=7)
    ax_bar.set_ylabel(r'$R^2$ (community vs species PDI)', fontsize=7)
    ax_bar.set_ylim(0, max(0.5, 1.25 * max(
        perm_data[m][s]['r_squared']
        for m in ['M', 'H'] for s in strategies
        if perm_data[m][s] is not None)))
    ax_bar.legend(fontsize=6, frameon=False, loc='upper right')
    ax_bar.set_title('PDI correlation by medium and removal strategy',
                     fontsize=7)
    sns.despine(ax=ax_bar)
    fig_bar.tight_layout()
    for ext in ['svg', 'pdf', 'png']:
        fig_bar.savefig(os.path.join(SCRIPT_DIR,
                                      f'Fig_R1_3_per_medium_R2.{ext}'),
                        dpi=300, bbox_inches='tight')
    plt.close(fig_bar)
    print(f"Per-medium R^2 bar chart saved to {SCRIPT_DIR}")


# ==========================================================================
# Per-medium VD-only direction agreement for both removal strategies
# ==========================================================================
print("\n" + "=" * 60)
print("DIRECTION AGREEMENT by medium × removal strategy")
print("=" * 60)

per_med_dir = {}
for med_target in ['LN', 'MN', 'HN']:
    per_med_dir[med_target] = {}
    for strat in ['mix', 'parents']:
        orig_scores = []
        mod_scores = []
        for sample_idx, medium_label, sp, c_1, c_2, c_mix in _iter_coal_events():
            if medium_label != med_target:
                continue
            try:
                u_o, v_o, _ = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
            except Exception:
                continue
            os_ = np.arctan(u_o / (v_o + 1e-8)) - np.pi / 4

            if strat == 'mix':
                dom_idx = [int(np.argmax(c_mix))]
            else:  # 'parents'
                dom_idx = list({int(np.argmax(c_1)), int(np.argmax(c_2))})

            c1m, c2m, cmm = c_1.copy(), c_2.copy(), c_mix.copy()
            for di in dom_idx:
                c1m[di] = c2m[di] = cmm[di] = 0
            s1, s2, sm = np.sum(c1m), np.sum(c2m), np.sum(cmm)
            if s1 <= 0 or s2 <= 0 or sm <= 0:
                continue
            c1m /= s1; c2m /= s2; cmm /= sm
            try:
                u_m, v_m, _ = metric_VectorDecomposition_onlyPositive(c1m, c2m, cmm)
            except Exception:
                continue
            ms_ = np.arctan(u_m / (v_m + 1e-8)) - np.pi / 4
            orig_scores.append(os_)
            mod_scores.append(ms_)

        if len(orig_scores) > 3:
            oa_raw = np.array(orig_scores)
            ma_raw = np.array(mod_scores)
            # Filter NaN/Inf from either array (VD degeneracy after removal can
            # yield 0/0 or u=v=0 cases that produce NaN community scores)
            finite = np.isfinite(oa_raw) & np.isfinite(ma_raw)
            oa = oa_raw[finite]
            ma = ma_raw[finite]
            n_nan = int((~finite).sum())
            agree = np.mean(np.sign(oa) == np.sign(ma)) if len(oa) else np.nan
            rho, p_ = stats.spearmanr(oa, ma) if len(oa) > 3 else (np.nan, np.nan)
            per_med_dir[med_target][strat] = dict(n=len(oa), agree=agree,
                                                   rho=rho, p=p_, n_nan=n_nan)
            print(f"  {med_target} | {strat:8s}: n={len(oa):3d} "
                  f"(dropped {n_nan} NaN), dir-agree={agree:.3f}, "
                  f"rho={rho:.3f} (p={p_:.2e})")
        else:
            per_med_dir[med_target][strat] = None


# ==========================================================================
# Top-K sensitivity analysis: remove 1, 2, or 3 most abundant species
# This addresses the recommendation to show how robust the circularity finding
# is when removing the top K (not just top 1) species from each event.
# ==========================================================================
print("\n" + "=" * 60)
print("TOP-K SENSITIVITY: R^2 after removing top K species")
print("=" * 60)

k_values = [1, 2, 3]
topk_results = {}

for k_remove in k_values:
    direction_agree_list = []
    orig_scores_list = []
    modk_scores_list = []
    n_failed_k = 0
    n_empty = 0

    for sample_idx, medium_label, sp, c_1, c_2, c_mix in _iter_coal_events():
        # Original VD
        try:
            u_orig, v_orig, k_orig = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
        except Exception:
            continue
        orig_score = np.arctan(u_orig / (v_orig + 1e-8)) - np.pi / 4

        # Remove top-K species (by abundance in mix) from all three vectors
        top_k_idx = np.argsort(c_mix)[::-1][:k_remove]
        c_1m, c_2m, c_mm = c_1.copy(), c_2.copy(), c_mix.copy()
        c_1m[top_k_idx] = c_2m[top_k_idx] = c_mm[top_k_idx] = 0

        s1, s2, sm = np.sum(c_1m), np.sum(c_2m), np.sum(c_mm)
        if s1 <= 0 or s2 <= 0 or sm <= 0:
            n_empty += 1
            continue
        c_1m /= s1
        c_2m /= s2
        c_mm /= sm

        try:
            u_mod, v_mod, k_mod = metric_VectorDecomposition_onlyPositive(c_1m, c_2m, c_mm)
        except Exception:
            n_failed_k += 1
            continue
        modk_score = np.arctan(u_mod / (v_mod + 1e-8)) - np.pi / 4

        orig_scores_list.append(orig_score)
        modk_scores_list.append(modk_score)
        direction_agree_list.append(int(np.sign(orig_score) == np.sign(modk_score)))

    orig_arr = np.array(orig_scores_list)
    modk_arr = np.array(modk_scores_list)

    if len(orig_arr) > 2:
        slope_k, intercept_k = np.polyfit(orig_arr, modk_arr, 1)
        ss_res = np.sum((modk_arr - (slope_k * orig_arr + intercept_k)) ** 2)
        ss_tot = np.sum((modk_arr - np.mean(modk_arr)) ** 2)
        r2_k = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        rho_k, p_k = stats.spearmanr(orig_arr, modk_arr)
    else:
        r2_k = rho_k = p_k = 0

    dir_agree = np.mean(direction_agree_list) if direction_agree_list else 0
    topk_results[k_remove] = {
        'n': len(orig_arr), 'r2': r2_k, 'rho': rho_k, 'p': p_k,
        'dir_agree': dir_agree, 'n_empty': n_empty, 'n_failed': n_failed_k,
    }
    print(f"\n  K={k_remove}: n={len(orig_arr)}, R^2={r2_k:.4f}, "
          f"Spearman rho={rho_k:.4f} (p={p_k:.2e}), "
          f"direction agree={dir_agree:.3f}, empty={n_empty}, failed={n_failed_k}")

# Figure: R^2 vs K (summary bar chart)
# K=0 and K=1 use pairwise-assay method (consistent with manuscript Fig 5C, M+H only)
# K=2 and K=3 are VD-only extensions (all media). Bars are colour-coded by method.
fig_topk, axes_topk = plt.subplots(1, 2, figsize=(110 * mm, 45 * mm), facecolor='w')

# Panel 1: Pairwise-assay R^2 for K=0 and K=1 (direct Fig 5C replication)
ax_topk = axes_topk[0]
if HAS_PAIRWISE:
    pa_r2s = [data_orig['r_squared'], data_mod['r_squared']]
    pa_labels = ['K=0\n(original)', 'K=1\n(pairwise)']
    pa_colors = ['#555555', COLOR_DOM]
    bars_pa = ax_topk.bar(np.arange(2), pa_r2s, color=pa_colors, alpha=0.7,
                           edgecolor='black', linewidth=0.5, width=0.5)
    for bar, r2 in zip(bars_pa, pa_r2s):
        ax_topk.text(bar.get_x() + bar.get_width() / 2, r2 + 0.005,
                     f'{r2:.2f}', ha='center', va='bottom', fontsize=7)
    ax_topk.set_xticks(np.arange(2))
    ax_topk.set_xticklabels(pa_labels, fontsize=7)
    ax_topk.set_ylim(0, max(pa_r2s) * 1.4 if max(pa_r2s) > 0 else 0.5)
    ax_topk.set_title('Pairwise-assay\n(M+H only, Fig 5C method)', fontsize=6)
else:
    ax_topk.text(0.5, 0.5, 'Pairwise data\nnot available', ha='center', va='center',
                 transform=ax_topk.transAxes, fontsize=7)
ax_topk.set_ylabel(r'$R^2$ (community vs species PDI)', fontsize=7)
sns.despine(ax=ax_topk)

# Panel 2: VD-only direction agreement for K=1,2,3 (consistent comparison across K)
ax_topk2 = axes_topk[1]
vd_dir = [topk_results[k]['dir_agree'] for k in k_values]
vd_rho  = [topk_results[k]['rho'] for k in k_values]
x_pos = np.arange(len(k_values))
bars_vd = ax_topk2.bar(x_pos, vd_dir, color=COLOR_DOM, alpha=0.7,
                        edgecolor='black', linewidth=0.5, width=0.5)
for bar, d in zip(bars_vd, vd_dir):
    ax_topk2.text(bar.get_x() + bar.get_width() / 2, d + 0.01,
                  f'{d:.2f}', ha='center', va='bottom', fontsize=7)
ax_topk2.axhline(0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.5,
                  label='Chance (0.5)')
ax_topk2.set_xticks(x_pos)
ax_topk2.set_xticklabels([f'K={k}' for k in k_values], fontsize=7)
ax_topk2.set_ylabel('Direction agreement\n(same winner after removal)', fontsize=7)
ax_topk2.set_ylim(0, 1.05)
ax_topk2.set_title('VD-only (all media)\ndirection stability', fontsize=6)
ax_topk2.legend(fontsize=6, frameon=False)
sns.despine(ax=ax_topk2)

fig_topk.tight_layout()
for ext in ['svg', 'pdf', 'png']:
    fig_topk.savefig(os.path.join(SCRIPT_DIR, f'Fig_R1_3_topK_sensitivity.{ext}'),
                     dpi=300, bbox_inches='tight')
plt.close(fig_topk)
print(f"\nTop-K sensitivity figure saved to {SCRIPT_DIR}")

print("\n===== Done (R1-3: PDI Circularity Check) =====")
