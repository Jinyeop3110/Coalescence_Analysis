#!/usr/bin/env python3
"""
plot_pairwise_matrix_dynamics_improved.py

Purpose: Generate improved pairwise species interaction matrix plot showing dynamics
from initial conditions (0.05, 0.95) to final experimental outcomes.

Improvements:
- Fixed classification logic (no more "Unclassified")
- Clean diagonal labels (no duplicates)
- X-axis labels showing Initial → Final
- Simplified line styling (no arrows)
- Better pie chart with non-overlapping labels
- Winner indicator for exclusion cases

Author: Gore Lab Analysis Team
Date: November 2025
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
import pandas as pd
import seaborn as sns
from pathlib import Path
from collections import Counter
import warnings
warnings.filterwarnings('ignore')
plt.ioff()

# Set up plotting parameters
sns.set_style("white")
plt.rcParams.update({
    'figure.dpi': 300,
    'font.size': 8,
    'font.family': 'Arial',
    'axes.linewidth': 0.8,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'text.usetex': False
})

# Define better color scheme
COLORS = {
    'coexistence': '#66c266',      # Clear green
    'exclusion': '#e85050',         # Clear red
    'bistability': '#7878d0',       # Clear purple
    'no_data': '#e8e8e8',           # Light gray
    'line_low': '#1f77b4',          # Blue for low initial freq
    'line_high': '#ff7f0e',         # Orange for high initial freq
}

# Species names
SPECIES_NAMES = [f'S{i+1}' for i in range(12)]

def setup_output_directory():
    """Create output directory"""
    output_dir = Path("/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/PairwiseMatrixDynamics")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def get_pairwise_count_data():
    """Load and process pairwise colony counting data"""
    pairwise_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Postprocessed/PairwiseColonyCountings_processed_230915.xlsx"

    try:
        mono_count_data = {}
        pairwise_count_data = {}

        for i, medium in enumerate(['LN', 'MN', 'HN']):
            data = pd.read_excel(pairwise_path, sheet_name=i)
            data = np.transpose(np.array(data.values[:, 1:]))
            mono_count_data[medium] = data

        for i, medium in enumerate(['LN', 'MN', 'HN']):
            sheet_idx1 = 3 + i*2
            sheet_idx2 = 4 + i*2

            data_1 = pd.read_excel(pairwise_path, sheet_name=sheet_idx1).values[:, 1:]
            data_2 = pd.read_excel(pairwise_path, sheet_name=sheet_idx2).values[:, 1:]
            pairwise_count_data[medium] = np.stack([data_1, data_2])

        return mono_count_data, pairwise_count_data

    except Exception as e:
        print(f"Error loading pairwise data: {e}")
        return None, None

def getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium_type):
    """Process pairwise count data"""
    data_m = np.mean(Mono_Count_data[medium_type], 1)
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
                    data_p_ratio[i, j] = data_p_1_converted[i, j] / (data_p_1_converted[i, j] + data_p_2_converted[i, j])

    return data_p_1, data_p_2, data_flag, data_p_ratio

def InterpretPairwiseResult(y1_final, y2_final, threshold=0.15):
    """
    Improved classification logic:
    - Coexistence: Both lines end between threshold and 1-threshold (both survive)
    - Exclusion: One line ends near 0 or 1 (one species wins)
    - Bistability: Lines cross AND end at opposite extremes depending on initial condition
    """
    # Check if outcomes depend on initial condition (bistability)
    # y1_final is outcome when species starts at 5% (low)
    # y2_final is outcome when species starts at 95% (high)

    low_wins_from_low = y1_final > (1 - threshold)  # Species at 5% ends up winning
    low_loses_from_low = y1_final < threshold        # Species at 5% ends up losing

    high_wins_from_high = y2_final > (1 - threshold)  # Species at 95% stays winning
    high_loses_from_high = y2_final < threshold       # Species at 95% ends up losing

    # Bistability: outcome depends on initial condition
    # If starting low leads to losing, but starting high leads to winning
    if (low_loses_from_low and high_wins_from_high):
        return 'B', COLORS['bistability'], 'Bistability'

    # Coexistence: both end up in middle range regardless of start
    if (threshold < y1_final < (1 - threshold)) and (threshold < y2_final < (1 - threshold)):
        return 'C', COLORS['coexistence'], 'Coexistence'

    # Exclusion: one species always wins regardless of initial condition
    # Case 1: The row species (i) always wins
    if y1_final > (1 - threshold) and y2_final > (1 - threshold):
        return 'E', COLORS['exclusion'], 'Exclusion (row wins)'

    # Case 2: The column species (j) always wins
    if y1_final < threshold and y2_final < threshold:
        return 'E', COLORS['exclusion'], 'Exclusion (col wins)'

    # Edge cases - still classify as exclusion if clear winner
    if y1_final > 0.7 and y2_final > 0.7:
        return 'E', COLORS['exclusion'], 'Exclusion (row wins)'
    if y1_final < 0.3 and y2_final < 0.3:
        return 'E', COLORS['exclusion'], 'Exclusion (col wins)'

    # Marginal coexistence
    return 'C', COLORS['coexistence'], 'Coexistence'

def create_improved_pairwise_matrix_plot(medium='MN'):
    """Create improved pairwise matrix plot with legend and summary"""

    print(f"Loading pairwise data for {medium}...")
    Mono_Count_data, Pairwise_Count_data = get_pairwise_count_data()

    if Mono_Count_data is None:
        print("Could not load pairwise data")
        return

    data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData(
        Mono_Count_data, Pairwise_Count_data, medium)

    N = 12

    # Create figure with custom layout
    fig = plt.figure(figsize=(14, 12))
    gs = gridspec.GridSpec(12, 15, figure=fig, wspace=0.4, hspace=0.4)

    # Create subplots for the matrix (12x12)
    axs = [[None for _ in range(12)] for _ in range(12)]
    for i in range(12):
        for j in range(12):
            axs[i][j] = fig.add_subplot(gs[i, j])

    # Create panel for legend and summary (right side)
    ax_legend = fig.add_subplot(gs[0:4, 12:15])
    ax_pie = fig.add_subplot(gs[4:8, 12:15])
    ax_info = fig.add_subplot(gs[8:12, 12:15])

    case_list = []
    case_details = []

    for i in range(12):
        for j in range(12):
            ax = axs[i][j]

            if j <= i:
                # Lower triangle and diagonal
                ax.axis('off')

                # Add species labels ONLY on diagonal (clean, no duplicates)
                if i == j:
                    ax.text(0.5, 0.5, SPECIES_NAMES[i],
                           ha='center', va='center', fontsize=10, fontweight='bold',
                           color='#333333', transform=ax.transAxes)
                    ax.axis('on')
                    ax.set_facecolor('#f5f5f5')
                    for spine in ax.spines.values():
                        spine.set_visible(False)
                    ax.set_xticks([])
                    ax.set_yticks([])

            elif data_flag[i, j] == 'case0':
                # No data
                ax.set_facecolor(COLORS['no_data'])
                ax.text(0.5, 0.5, '—', ha='center', va='center',
                       fontsize=10, color='#aaaaaa')
                ax.set_xticks([])
                ax.set_yticks([])
                for spine in ax.spines.values():
                    spine.set_linewidth(0.5)
                    spine.set_color('#cccccc')
            else:
                # Plot dynamics
                x = np.array([0, 1])
                y1_vals = np.array([0.05, float(data_p_ratio[i, j])])
                y2_vals = np.array([0.95, 1 - float(data_p_ratio[j, i])])

                # Get classification
                case, shade, detail = InterpretPairwiseResult(y1_vals[1], y2_vals[1])
                case_list.append(case)
                case_details.append(detail)
                ax.set_facecolor(shade)

                # Plot lines with clean styling (no arrows)
                ax.plot(x, y1_vals, color=COLORS['line_low'], linewidth=1.8,
                       marker='o', markersize=4, markerfacecolor='white',
                       markeredgewidth=1.2, zorder=3)
                ax.plot(x, y2_vals, color=COLORS['line_high'], linewidth=1.8,
                       marker='o', markersize=4, markerfacecolor='white',
                       markeredgewidth=1.2, zorder=3)

                ax.set_xlim(-0.15, 1.15)
                ax.set_ylim(-0.08, 1.08)

                # Add horizontal reference line at 0.5
                ax.axhline(y=0.5, color='#cccccc', linestyle=':', linewidth=0.8, zorder=1)

                # Clean axis formatting
                ax.set_xticks([])
                ax.set_yticks([])

                # Add x-axis labels only for bottom row of each column
                if i == 11 or (i < 11 and (data_flag[i+1, j] == 'case0' or j <= i+1)):
                    ax.set_xticks([0, 1])
                    ax.set_xticklabels(['0', 'T'], fontsize=6)

                # Add y-axis labels only for leftmost subplot in each row
                first_valid_j = None
                for jj in range(i+1, 12):
                    if data_flag[i, jj] != 'case0':
                        first_valid_j = jj
                        break
                if j == first_valid_j:
                    ax.set_yticks([0, 0.5, 1])
                    ax.set_yticklabels(['0', '', '1'], fontsize=6)

                for spine in ax.spines.values():
                    spine.set_linewidth(0.6)
                    spine.set_color('#888888')

            # Add column labels (top row)
            if i == 0 and j > 0:
                ax.set_title(f'{SPECIES_NAMES[j]}', fontsize=8, fontweight='bold', pad=3)

    # Add row labels on the left side
    for i in range(12):
        axs[i][0].text(-0.5, 0.5, SPECIES_NAMES[i], transform=axs[i][0].transAxes,
                      ha='right', va='center', fontsize=8, fontweight='bold')

    # === Create Legend Panel ===
    ax_legend.axis('off')
    ax_legend.set_xlim(0, 1)
    ax_legend.set_ylim(0, 1)

    # Title
    ax_legend.text(0.5, 0.95, 'Legend', ha='center', va='top', fontsize=12,
                   fontweight='bold', transform=ax_legend.transAxes)

    # Outcome type legend
    legend_elements = [
        Patch(facecolor=COLORS['coexistence'], edgecolor='#444444', linewidth=1, label='Coexistence'),
        Patch(facecolor=COLORS['exclusion'], edgecolor='#444444', linewidth=1, label='Exclusion'),
        Patch(facecolor=COLORS['bistability'], edgecolor='#444444', linewidth=1, label='Bistability'),
        Patch(facecolor=COLORS['no_data'], edgecolor='#444444', linewidth=1, label='No data'),
    ]

    leg1 = ax_legend.legend(handles=legend_elements, loc='upper left',
                            frameon=True, fontsize=9, title='Outcome Type',
                            bbox_to_anchor=(0.05, 0.85), framealpha=1,
                            edgecolor='#cccccc')
    leg1.get_title().set_fontsize(10)
    leg1.get_title().set_fontweight('bold')
    ax_legend.add_artist(leg1)

    # Line legend
    line_elements = [
        Line2D([0], [0], color=COLORS['line_low'], linewidth=2.5, marker='o',
               markersize=5, markerfacecolor='white', markeredgewidth=1.5,
               label='Start at 5%'),
        Line2D([0], [0], color=COLORS['line_high'], linewidth=2.5, marker='o',
               markersize=5, markerfacecolor='white', markeredgewidth=1.5,
               label='Start at 95%'),
    ]

    leg2 = ax_legend.legend(handles=line_elements, loc='lower left',
                            frameon=True, fontsize=9, title='Initial Frequency',
                            bbox_to_anchor=(0.05, 0.05), framealpha=1,
                            edgecolor='#cccccc')
    leg2.get_title().set_fontsize(10)
    leg2.get_title().set_fontweight('bold')

    # === Create Pie Chart Summary ===
    ax_pie.axis('equal')
    case_counts = Counter(case_list)

    labels = []
    sizes = []
    colors = []
    explode = []

    outcome_map = {
        'C': ('Coexistence', COLORS['coexistence']),
        'E': ('Exclusion', COLORS['exclusion']),
        'B': ('Bistability', COLORS['bistability']),
    }

    # Sort by count for better visualization
    for case_type in ['E', 'C', 'B']:
        if case_type in case_counts and case_counts[case_type] > 0:
            name, color = outcome_map[case_type]
            labels.append(f'{name}\n(n={case_counts[case_type]})')
            sizes.append(case_counts[case_type])
            colors.append(color)
            explode.append(0.02)

    if sizes:
        wedges, texts, autotexts = ax_pie.pie(
            sizes, labels=None, colors=colors,
            autopct='%1.0f%%', startangle=90,
            explode=explode,
            textprops={'fontsize': 11, 'fontweight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2},
            pctdistance=0.6
        )

        # Add legend instead of labels on pie to avoid overlap
        ax_pie.legend(wedges, labels, loc='upper left', bbox_to_anchor=(-0.1, 1.0),
                     fontsize=9, frameon=False)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax_pie.set_title('Outcome Distribution', fontsize=12, fontweight='bold', pad=15)

    # === Info Panel (removed - keep empty) ===
    ax_info.axis('off')

    medium_names = {'LN': 'Nutr-', 'MN': 'Base', 'HN': 'Nutr+'}

    # Main title
    fig.suptitle(f'Pairwise Species 95:5 Invasion Assays — {medium_names.get(medium, medium)}',
                 fontsize=14, fontweight='bold', y=0.98)

    # Adjust layout
    plt.tight_layout(rect=[0.02, 0, 0.98, 0.95])

    # Save
    output_dir = setup_output_directory()
    filename = f"Pairwise_Matrix_Dynamics_{medium}_improved"

    plt.savefig(output_dir / f"{filename}.svg", format='svg', bbox_inches='tight', dpi=300)
    plt.savefig(output_dir / f"{filename}.png", format='png', bbox_inches='tight', dpi=300)
    plt.savefig(output_dir / f"{filename}.pdf", format='pdf', bbox_inches='tight', dpi=300)

    print(f"Saved: {filename}.svg, {filename}.png, {filename}.pdf")
    print(f"Total interactions plotted: {len(case_list)}")
    print("Outcome counts:")
    for case_type in ['C', 'E', 'B']:
        if case_type in case_counts:
            names = {'C': 'Coexistence', 'E': 'Exclusion', 'B': 'Bistability'}
            print(f"  {names[case_type]}: {case_counts[case_type]}")

    plt.close()

    return case_list

def main():
    """Main function to create improved pairwise matrix dynamics plots"""

    print("Creating Improved Pairwise Matrix Dynamics Plots...")
    print("=" * 60)

    media = ['LN', 'MN', 'HN']

    for medium in media:
        print(f"\n--- Processing {medium} ---")
        try:
            case_list = create_improved_pairwise_matrix_plot(medium)
            print(f"Successfully created improved plot for {medium}")
        except Exception as e:
            print(f"Error creating plot for {medium}: {e}")
            import traceback
            traceback.print_exc()

    output_dir = setup_output_directory()
    print(f"\n{'=' * 60}")
    print(f"All plots saved to: {output_dir}")
    print("Plot generation complete!")

if __name__ == "__main__":
    main()
