"""
Figure 1-1 Generation Script
Generates composition diagrams and time series plots for main figure 1.

Version Numbers Used:
- seaborn==0.11.2
- scipy==1.8.0
- numpy==1.22.2
- matplotlib==3.5.1
"""

import scipy as sp
from pylab import *
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, MaxNLocator
import pandas as pd
import seaborn as sns
import collections
import random
import openpyxl
import os
sns.set_style("ticks")
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, explained_variance_score, r2_score
from sklearn.preprocessing import PolynomialFeatures
import pickle
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


# ============================================================================
# Configuration and Setup
# ============================================================================

FigureTitle = "Figure/Fig1_1_Plots"
np.random.seed(1)

if not os.path.exists(FigureTitle):
    os.makedirs(FigureTitle)
    print("The new directory is created!")

mm = 0.1 / 2.54
os.environ['PATH'] = os.environ['PATH'] + ':/Library/TeX/texbin/latex'
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['figure.dpi'] = 600
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.4
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.4
mpl.rcParams['ytick.major.width'] = 0.5

plt.rcParams['text.usetex'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


# ============================================================================
# Custom Colormap
# ============================================================================

my_cmap = ListedColormap(['#00429d', '#4771b2', '#73a2c6', '#a5d5d8', '#ffffe0',
                          '#ffbcaf', '#f4777f', '#cf3759', '#93003a'], name="my_cmap")
my_cmap_r = my_cmap.reversed()
mpl.colormaps.register(cmap=my_cmap)
mpl.colormaps.register(cmap=my_cmap_r)


# ============================================================================
# Data Loading
# ============================================================================

def load_data():
    """Load all required data files."""
    Coalescence_data_synthetic_path = "../../Analyzed/processed_CoalescenceEvent_synthetic.xlsx"
    Communities_data_synthetic_path = "../../Analyzed/processed_Communities_synthetic.xlsx"
    Coalescence_data_natural_path = "../../Analyzed/processed_CoalescenceEvent_natural.xlsx"
    Communities_data_natural_path = "../../Analyzed/processed_Communities_natural.xlsx"
    Coalescence_recipe_path = "../../Postprocessed/CoalescenceRecipe.xlsx"
    Meta_data_path = "../../Postprocessed/Metadata.xlsx"
    Processed_sequences_synthetic_path = "../../Postprocessed/processed_Sequences_synthetic.xlsx"
    Processed_sequences_natural_path = "../../Postprocessed/processed_Sequences_natural.xlsx"
    Coalescence_data_sim_path = "../../Analyzed/processed_CoalescenceEvent_simulation_uniform.xlsx"

    Coalescence_data = pd.concat([pd.read_excel(Coalescence_data_synthetic_path),
                                  pd.read_excel(Coalescence_data_natural_path)])
    Communities_data = pd.concat([pd.read_excel(Communities_data_synthetic_path),
                                  pd.read_excel(Communities_data_natural_path)])
    Coalescence_data_sim = pd.read_excel(Coalescence_data_sim_path)
    Coalescence_recipe = pd.read_excel(Coalescence_recipe_path, sheet_name=0)
    Coalescence_natural_recipe = pd.read_excel(Coalescence_recipe_path, sheet_name=1)
    Metadata = pd.read_excel(Meta_data_path)
    Processed_sequences_synthetic = pd.read_excel(Processed_sequences_synthetic_path)
    Processed_sequences_natural = pd.read_excel(Processed_sequences_natural_path)

    return {
        'Coalescence_data': Coalescence_data,
        'Communities_data': Communities_data,
        'Coalescence_data_sim': Coalescence_data_sim,
        'Coalescence_recipe': Coalescence_recipe,
        'Coalescence_natural_recipe': Coalescence_natural_recipe,
        'Metadata': Metadata,
        'Processed_sequences_synthetic': Processed_sequences_synthetic,
        'Processed_sequences_natural': Processed_sequences_natural
    }


# ============================================================================
# Helper Functions
# ============================================================================

def getIDX(data, IDX):
    O = np.flatnonzero([x == IDX for x in data['SampleIDX']])
    return np.array(O)


def getAbundance(Processed_sequences, IDX):
    SampleIdx = np.flatnonzero([x == IDX for x in Processed_sequences['SampleIDX']])
    if not any(SampleIdx):
        return
    else:
        O = Processed_sequences.iloc[SampleIdx].values.tolist()[0][1:]
        return O


def getAbundance_fromList(Processed_sequences, IDX_list):
    IDX_list_ = np.squeeze([np.where(Processed_sequences['SampleIDX'] == x) for x in IDX_list])
    return (np.array(Processed_sequences.iloc[IDX_list_].values)[:, 1:]).astype(float)


def Community_PermutateList_simulation(I, S):
    sample_num = 100
    O = (3 * (I - 1) + (S - 1)) * 100 + np.arange(0, 100)
    return O


def Community_PermutateList(Timepoint, CommunityOrigin, Medium, CoalescenceType,
                            species_pool_num=0, Replicate=-1, Metadata=None, exception_list=None):
    if exception_list is None:
        exception_list = []

    if Replicate == -1:
        idx = (Metadata['Timepoint'] == Timepoint) & \
              (Metadata['CommunityOrigin'] == CommunityOrigin) & \
              (Metadata['Medium'] == Medium) & \
              (Metadata['CoalescenceType'] == CoalescenceType)
    elif Replicate == 1 or Replicate == 2:
        idx = (Metadata['Timepoint'] == Timepoint) & \
              (Metadata['CommunityOrigin'] == CommunityOrigin) & \
              (Metadata['Medium'] == Medium) & \
              (Metadata['CoalescenceType'] == CoalescenceType) & \
              (Metadata['Replicate'] == Replicate)
    else:
        raise ValueError("Invalid input")

    if CommunityOrigin == 'S':
        communityIDX = np.array([int(x) for x in Metadata['CommunityIDX']])
        if CoalescenceType == 'S':
            if species_pool_num == 6:
                idx = idx & (communityIDX <= 9)
            elif species_pool_num == 12:
                idx = idx & ((communityIDX > 9) & (communityIDX <= 18))
            elif species_pool_num == 24:
                idx = idx & ((communityIDX > 18) & (communityIDX <= 30))
            elif species_pool_num == 0:
                idx = idx
        elif CoalescenceType == 'C':
            if species_pool_num == 6:
                idx = idx & (communityIDX <= 14)
            elif species_pool_num == 12:
                idx = idx & ((communityIDX > 14) & (communityIDX <= 41))
            elif species_pool_num == 24:
                idx = idx & ((communityIDX > 41) & (communityIDX <= 47))
            elif species_pool_num == 0:
                idx = idx
    elif CommunityOrigin == 'N':
        communityIDX = np.array([int(x) for x in Metadata['CommunityIDX']])

    O = Metadata['SampleIDX'][idx]
    O = list(set(O) - set(exception_list))
    return O


def getCommunities(Communities_data, IDX_list):
    IDX_list_ = np.squeeze([np.where(Communities_data['SampleIDX'] == x) for x in IDX_list])
    return (Communities_data.iloc[IDX_list_])


def settingTheColor(seed=4):
    """Generate and shuffle color palette for ASV visualization.
    Uses inferno colormap to match pie charts in generate_pie_plots.py."""
    np.random.seed(seed)
    try:
        inferno = plt.colormaps.get_cmap('inferno').resampled(43)
    except AttributeError:
        from matplotlib import cm as mpl_cm
        inferno = mpl_cm.get_cmap('inferno', 43)
    colors = [inferno(i)[:3] for i in range(43)]
    np.random.shuffle(colors)
    return colors


# ============================================================================
# Plotting Functions
# ============================================================================

def plot_taxonomy_colormap():
    """Generate taxonomy colormap figure from Species_phylogeny.xlsx."""
    # Load taxonomy data from Excel file
    phylo_df = pd.read_excel('Data/Species_phylogeny.xlsx', sheet_name='Organized')

    # Sort by ASV number (extract number from ASV index like ASV1 -> 1)
    phylo_df['ASV_num'] = phylo_df['ASV index'].str.replace('ASV', '').astype(int)
    phylo_df = phylo_df.sort_values('ASV_num').reset_index(drop=True)

    # Remap to consecutive numbering (ASV1, ASV2, ASV3...ASV50 without gaps)
    phylo_df['ASV_remapped'] = ['ASV' + str(i+1) for i in range(len(phylo_df))]

    # Build data list from Excel
    data = []
    for idx, row in phylo_df.iterrows():
        asv_id_original = str(row['ASV index'])
        asv_id_remapped = str(row['ASV_remapped'])
        kingdom = str(row['Kingdom']) if pd.notna(row['Kingdom']) else 'NA'
        phylum = str(row['Phylum']) if pd.notna(row['Phylum']) else 'NA'
        class_name = str(row['Class']) if pd.notna(row['Class']) else 'NA'
        order = str(row['Order']) if pd.notna(row['Order']) else 'NA'
        family = str(row['Family']) if pd.notna(row['Family']) else 'NA'
        genus = str(row['Genus']) if pd.notna(row['Genus']) else 'NA'

        # Use only remapped ASV ID (consecutive numbering without gaps)
        data.append([asv_id_remapped, kingdom, phylum, class_name, order, family, genus])

    # Use inferno colormap to match pie charts in generate_pie_plots.py
    np.random.seed(4)
    try:
        inferno = plt.colormaps.get_cmap('inferno').resampled(len(data))
    except AttributeError:
        from matplotlib import cm as mpl_cm
        inferno = mpl_cm.get_cmap('inferno', len(data))
    colors = [inferno(i)[:3] for i in range(len(data))]
    np.random.shuffle(colors)
    color_map = colors[::-1]

    fig, ax = plt.subplots(figsize=(8, 15))
    block_width = 0.015
    y = 0
    spacing = 0.004

    for i, row in enumerate(data[::-1]):
        species = row[0]
        taxonomy = row[1:]
        color = color_map[i]

        ax.add_patch(plt.Rectangle((0, y), block_width * 2, block_width, color=color))

        formatted_taxonomy = [f"{level[0]}-{level[1]}" for level in zip("kpcofg", taxonomy)]
        text = species + ', ' + ", ".join(formatted_taxonomy)
        ax.text(block_width * 2 + spacing, y + 0.5 * block_width, text, va='center', fontsize=12)

        y += block_width + spacing

    ax.set_aspect('equal')
    ax.set_xlim(0, block_width + 0.1)
    ax.set_ylim(0, y)
    ax.axis('off')

    plt.savefig(f'{FigureTitle}/taxonomy_color_map.svg', format='svg', bbox_inches='tight')
    plt.savefig(f'{FigureTitle}/taxonomy_color_map.png', format='png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{FigureTitle}/taxonomy_color_map.pdf', format='pdf', bbox_inches='tight')
    plt.close()


def plot_composition_diagram(Processed_sequences_synthetic, IDX_list, comm_type, filename):
    """Plot composition diagram for communities."""
    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                            for x in IDX_list])
    df = Processed_sequences_synthetic.iloc[IDX_list_]

    color_map = settingTheColor()

    degList = [i for i in df.columns if i[0:4] == 'Norm']
    degList_ = [i.replace('NormalizedAbundance', 'ASV') for i in degList]
    bar_l = np.array(range(df.shape[0]))

    f, ax = plt.subplots(1, figsize=(len(IDX_list) * 4 * mm, 8 * 4 * mm),
                        facecolor='w', edgecolor='k')

    x_scale = 0.5
    bottom = np.zeros_like(bar_l).astype('float')

    for i, deg in enumerate(degList):
        ax.bar(bar_l * x_scale, df[deg], width=0.9 * x_scale, bottom=bottom,
               label=degList_[i], linewidth=0, color=color_map[i])
        bottom += df[deg].values

    for i, IDX in enumerate(df['SampleIDX'].tolist()):
        ax.text(bar_l[i] * x_scale, 1.01, "$C_{" + str(i + 1) + "}$",
                ha='center', va='bottom', fontsize=1.2)

    ax.set_xticks(bar_l)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])

    f.subplots_adjust(right=0.75, bottom=0.4)
    f.savefig(filename, bbox_inches='tight')
    plt.close(f)


def plot_timeseries_sub(Processed_sequences_synthetic, IDX_list, mask, filename):
    """Plot time series for subcommunities."""
    np.random.seed(42)
    # Handle variable-length sample lists robustly
    IDX_list_ = []
    for x in IDX_list:
        idx = np.where(Processed_sequences_synthetic['SampleIDX'] == x)[0]
        if len(idx) > 0:
            IDX_list_.append(idx[0])
    df = Processed_sequences_synthetic.iloc[IDX_list_]

    new_row = {"SampleIDX": "Randi"}
    random_initial_value = np.random.rand(43) * mask
    random_initial_value = random_initial_value / sum(random_initial_value)

    for i in range(1, 44):
        column_name = f"NormalizedAbundance{i}"
        new_row[column_name] = random_initial_value[i - 1]

    new_row_df = pd.DataFrame([new_row])
    df = pd.concat([new_row_df, df], ignore_index=True)

    color_map = settingTheColor()
    degList = [i for i in df.columns if i[0:4] == 'Norm']
    degList_ = [i.replace('NormalizedAbundance', 'ASV') for i in degList]
    bar_l = np.array(range(df.shape[0]))

    f, ax = plt.subplots(1, figsize=(len(IDX_list) * 3 * mm, 8 * 4 * mm),
                        facecolor='w', edgecolor='k')

    x_scale = 0.5
    bottom = np.zeros_like(bar_l).astype('float')

    for i, deg in enumerate(degList):
        ax.bar(bar_l * x_scale, df[deg], width=0.9 * x_scale, bottom=bottom,
               label=degList_[i], linewidth=0, color=color_map[i])
        bottom += df[deg].values

    ax.set_xticks(bar_l)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    f.subplots_adjust(right=0.75, bottom=0.4)

    f.savefig(filename, bbox_inches='tight')
    f.savefig(filename.replace('.svg', '.pdf'), bbox_inches='tight')
    plt.close(f)


def plot_timeseries_coal(Processed_sequences_synthetic, IDX_list, mask_1, mask_2,
                        species_1, species_2, filename):
    """Plot time series for coalescence communities."""
    np.random.seed(42)
    mask_2 = ~mask_1
    # Handle variable-length sample lists robustly
    IDX_list_ = []
    for x in IDX_list:
        idx = np.where(Processed_sequences_synthetic['SampleIDX'] == x)[0]
        if len(idx) > 0:
            IDX_list_.append(idx[0])
    df = Processed_sequences_synthetic.iloc[IDX_list_]

    new_row = {"SampleIDX": "Mixedi"}
    random_initial_value = (species_1 * 0.5 + species_2 * 0.5) * (mask_1 + mask_2)
    random_initial_value = random_initial_value / sum(random_initial_value)

    for i in range(1, 44):
        column_name = f"NormalizedAbundance{i}"
        new_row[column_name] = random_initial_value[i - 1]

    new_row_df = pd.DataFrame([new_row])
    df = pd.concat([new_row_df, df], ignore_index=True)

    color_map = settingTheColor()
    degList = [i for i in df.columns if i[0:4] == 'Norm']
    degList_ = [i.replace('NormalizedAbundance', 'ASV') for i in degList]
    bar_l = np.array(range(df.shape[0]))

    f, ax = plt.subplots(1, figsize=(len(IDX_list) * 3 * mm, 8 * 4 * mm),
                        facecolor='w', edgecolor='k')

    x_scale = 0.5
    bottom = np.zeros_like(bar_l).astype('float')

    plotting_index_1 = np.where(mask_1)[0]
    plotting_index_2 = np.where(mask_2)[0]

    for i in plotting_index_1:
        deg = f"NormalizedAbundance{i + 1}"
        ax.bar(bar_l * x_scale, df[deg], width=0.9 * x_scale, bottom=bottom,
               label=degList_[i], linewidth=0, color=color_map[i])
        bottom += df[deg].values

    ax.bar(bar_l * x_scale, 0, width=0.9 * x_scale, bottom=bottom, label='',
           linewidth=0.5, edgecolor='red', color='red')

    for i in plotting_index_2:
        deg = f"NormalizedAbundance{i + 1}"
        ax.bar(bar_l * x_scale, df[deg], width=0.9 * x_scale, bottom=bottom,
               label=degList_[i], linewidth=0, color=color_map[i])
        bottom += df[deg].values

    ax.set_xticks(bar_l)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    f.subplots_adjust(right=0.75, bottom=0.4)

    f.savefig(filename, bbox_inches='tight')
    f.savefig(filename.replace('.svg', '.pdf'), bbox_inches='tight')
    plt.close(f)


def plot_timeseries_merged(Processed_sequences_synthetic, IDX_list_sub1, IDX_list_sub2,
                           IDX_list_coal, mask_1, species_1, species_2, filename):
    """Plot merged time series with sub1 + sub2 -> coal layout with clean arrow."""
    np.random.seed(42)
    mask_2 = ~mask_1
    color_map = settingTheColor()

    # Helper to get dataframe with initial random row
    def get_df_with_initial(IDX_list, mask, is_coal=False):
        IDX_list_ = []
        for x in IDX_list:
            idx = np.where(Processed_sequences_synthetic['SampleIDX'] == x)[0]
            if len(idx) > 0:
                IDX_list_.append(idx[0])
        df = Processed_sequences_synthetic.iloc[IDX_list_]

        if is_coal:
            new_row = {"SampleIDX": "Mixedi"}
            random_initial_value = (species_1 * 0.5 + species_2 * 0.5) * (mask_1 + mask_2)
        else:
            new_row = {"SampleIDX": "Randi"}
            random_initial_value = np.random.rand(43) * mask

        random_initial_value = random_initial_value / sum(random_initial_value)
        for i in range(1, 44):
            new_row[f"NormalizedAbundance{i}"] = random_initial_value[i - 1]

        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([new_row_df, df], ignore_index=True)
        return df

    # Get data for each panel
    df_sub1 = get_df_with_initial(IDX_list_sub1, mask_1)
    df_sub2 = get_df_with_initial(IDX_list_sub2, mask_2)
    df_coal = get_df_with_initial(IDX_list_coal, None, is_coal=True)

    n_sub1 = len(df_sub1)
    n_sub2 = len(df_sub2)
    n_coal = len(df_coal)

    # Create figure with GridSpec for layout (increased size for labels)
    # Left side: sub1 (top) + sub2 (bottom), Right side: coal
    fig = plt.figure(figsize=(28 * mm, 22 * mm), facecolor='w')

    # Calculate widths based on number of bars
    left_width = max(n_sub1, n_sub2)
    right_width = n_coal

    gs = fig.add_gridspec(2, 3, width_ratios=[left_width, 1.2, right_width],
                          height_ratios=[1, 1], wspace=0.15, hspace=0.25)

    ax_sub1 = fig.add_subplot(gs[0, 0])
    ax_sub2 = fig.add_subplot(gs[1, 0])
    ax_arrow = fig.add_subplot(gs[:, 1])
    ax_coal = fig.add_subplot(gs[:, 2])

    x_scale = 0.5

    # Plot sub1 (top left)
    degList = [i for i in df_sub1.columns if i[0:4] == 'Norm']
    bar_l = np.array(range(n_sub1))
    bottom = np.zeros(n_sub1).astype('float')
    for i, deg in enumerate(degList):
        ax_sub1.bar(bar_l * x_scale, df_sub1[deg], width=0.9 * x_scale, bottom=bottom,
                   linewidth=0, color=color_map[i])
        bottom += df_sub1[deg].values
    ax_sub1.set_xlim(-0.5 * x_scale, (n_sub1 - 0.5) * x_scale)
    ax_sub1.set_ylim(0, 1)
    # Add y-axis label for sub1 (shared label for both parent panels)
    ax_sub1.set_ylabel('Relative\nAbundance', fontsize=7, labelpad=2)
    ax_sub1.set_yticks([0, 1])
    ax_sub1.set_yticklabels(['0', '1'], fontsize=6)
    ax_sub1.tick_params(axis='y', length=2, pad=1)
    ax_sub1.set_xticks([])
    # Only show left spine
    ax_sub1.spines['top'].set_visible(False)
    ax_sub1.spines['right'].set_visible(False)
    ax_sub1.spines['bottom'].set_visible(False)
    ax_sub1.spines['left'].set_linewidth(0.5)

    # Plot sub2 (bottom left)
    bar_l = np.array(range(n_sub2))
    bottom = np.zeros(n_sub2).astype('float')
    for i, deg in enumerate(degList):
        ax_sub2.bar(bar_l * x_scale, df_sub2[deg], width=0.9 * x_scale, bottom=bottom,
                   linewidth=0, color=color_map[i])
        bottom += df_sub2[deg].values
    ax_sub2.set_xlim(-0.5 * x_scale, (n_sub2 - 0.5) * x_scale)
    ax_sub2.set_ylim(0, 1)
    # Add x-axis label for sub2
    ax_sub2.set_xlabel('Cycle', fontsize=7, labelpad=2)
    ax_sub2.set_xticks([i * x_scale for i in range(n_sub2)])
    ax_sub2.set_xticklabels([str(i) for i in range(n_sub2)], fontsize=6)
    ax_sub2.tick_params(axis='x', length=2, pad=1)
    ax_sub2.set_yticks([0, 1])
    ax_sub2.set_yticklabels(['0', '1'], fontsize=6)
    ax_sub2.tick_params(axis='y', length=2, pad=1)
    # Only show left and bottom spines
    ax_sub2.spines['top'].set_visible(False)
    ax_sub2.spines['right'].set_visible(False)
    ax_sub2.spines['left'].set_linewidth(0.5)
    ax_sub2.spines['bottom'].set_linewidth(0.5)

    # Draw clean arrow in middle panel (replacing curly brace)
    ax_arrow.set_xlim(0, 1)
    ax_arrow.set_ylim(0, 1)
    ax_arrow.axis('off')

    # Add "+" symbol between parent panels
    ax_arrow.text(0.15, 0.5, '+', fontsize=12, ha='center', va='center',
                  fontweight='bold')

    # Draw clean horizontal arrow
    ax_arrow.annotate('', xy=(0.92, 0.5), xytext=(0.35, 0.5),
                      arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

    # Plot coal (right side, spanning both rows)
    bar_l = np.array(range(n_coal))
    bottom = np.zeros(n_coal).astype('float')

    plotting_index_1 = np.where(mask_1)[0]
    plotting_index_2 = np.where(mask_2)[0]

    for i in plotting_index_1:
        deg = f"NormalizedAbundance{i + 1}"
        ax_coal.bar(bar_l * x_scale, df_coal[deg], width=0.9 * x_scale, bottom=bottom,
                   linewidth=0, color=color_map[i])
        bottom += df_coal[deg].values

    # Add separator line
    ax_coal.axhline(y=bottom[0], color='black', linestyle='--', linewidth=0.5, alpha=0.5)

    for i in plotting_index_2:
        deg = f"NormalizedAbundance{i + 1}"
        ax_coal.bar(bar_l * x_scale, df_coal[deg], width=0.9 * x_scale, bottom=bottom,
                   linewidth=0, color=color_map[i])
        bottom += df_coal[deg].values

    ax_coal.set_xlim(-0.5 * x_scale, (n_coal - 0.5) * x_scale)
    ax_coal.set_ylim(0, 1)
    # Add x-axis label for coalesced panel
    ax_coal.set_xlabel('Cycle', fontsize=7, labelpad=2)
    ax_coal.set_xticks([i * x_scale for i in range(n_coal)])
    ax_coal.set_xticklabels([str(i) for i in range(n_coal)], fontsize=6)
    ax_coal.tick_params(axis='x', length=2, pad=1)
    ax_coal.set_yticks([0, 1])
    ax_coal.set_yticklabels(['0', '1'], fontsize=6)
    ax_coal.tick_params(axis='y', length=2, pad=1)
    # Only show left and bottom spines
    ax_coal.spines['top'].set_visible(False)
    ax_coal.spines['right'].set_visible(False)
    ax_coal.spines['left'].set_linewidth(0.5)
    ax_coal.spines['bottom'].set_linewidth(0.5)

    plt.savefig(filename, bbox_inches='tight')
    plt.savefig(filename.replace('.svg', '.pdf'), bbox_inches='tight')
    plt.close(fig)


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main function to generate all Figure 1-1 plots."""
    # Load data
    data_dict = load_data()
    Metadata = data_dict['Metadata']
    Processed_sequences_synthetic = data_dict['Processed_sequences_synthetic']

    # Create subdirectories for timeseries plots
    timeseries_dir = f'{FigureTitle}/timeseries'
    timeseries_merged_dir = f'{FigureTitle}/timeseries_merged'
    if not os.path.exists(timeseries_dir):
        os.makedirs(timeseries_dir)
    if not os.path.exists(timeseries_merged_dir):
        os.makedirs(timeseries_merged_dir)

    # Exception list
    exception_list = ['P4-02', 'P4-03', 'P4-23', 'P4-24', 'P7-97', 'P8-12', 'P8-91',
                     'P5-73', 'P5-69', 'P5-64', 'P5-61', 'P5-59', 'P5-56',
                     'P5-47', 'P5-50', 'P5-39', 'P5-87', 'P5-54', 'P6-02',
                     'P6-47', 'P6-74', 'P6-57']

    # Define sample lists for different conditions
    # LN conditions
    IDX_list_A1 = ['P3-07', 'P3-08', 'P3-09', 'P3-10', 'P3-11', 'P3-12']
    IDX_list_A2 = ['P3-19', 'P3-20', 'P3-21', 'P3-22', 'P3-23', 'P3-24']
    IDX_list_A3 = ['P3-31', 'P3-32', 'P3-33', 'P3-34', 'P3-35', 'P3-36', 'P2-63']
    IDX_list_A4 = ['P3-43', 'P3-44', 'P3-45', 'P3-46', 'P3-47', 'P3-48', 'P2-64']
    IDX_list_A5 = ['P3-55', 'P3-56', 'P3-57', 'P3-58', 'P3-59', 'P3-60']
    IDX_list_A6 = ['P3-67', 'P3-68', 'P3-69', 'P3-70', 'P3-71', 'P3-72', 'P4-53']

    # MN SC12 conditions
    IDX_list_D2 = ['P1-10', 'P1-11', 'P1-12', 'P1-34', 'P1-35', 'P1-36']
    IDX_list_D8 = ['P1-22', 'P1-23', 'P1-24', 'P1-46', 'P1-47', 'P1-48']
    # MN CC12
    IDX_list_B12 = ['P8-34', 'P8-35', 'P8-36', 'P8-70', 'P8-71', 'P8-72']
    # MN CC24
    IDX_list_D9 = ['P8-46', 'P8-47', 'P8-48', 'P8-82', 'P8-83', 'P8-84']
    IDX_list_D11 = ['P8-58', 'P8-59', 'P8-60', 'P8-94', 'P8-95', 'P8-96']
    # MN SC24
    IDX_list_G9 = ['P2-22', 'P2-23', 'P2-24', 'P2-70', 'P2-71', 'P2-72']
    IDX_list_G5 = ['P2-10', 'P2-11', 'P2-12', 'P2-58', 'P2-59', 'P2-60']
    IDX_list_G10 = ['P2-46', 'P2-47', 'P2-48', 'P2-94', 'P2-95', 'P2-96']
    IDX_list_G6 = ['P2-34', 'P2-35', 'P2-36', 'P2-82', 'P2-83', 'P2-84']

    # HN conditions
    IDX_list_B1 = ['P8-01', 'P8-02', 'P8-03', 'P8-04', 'P8-05', 'P8-06']
    IDX_list_B2 = ['P8-13', 'P8-15', 'P8-16', 'P8-17', 'P8-18']
    IDX_list_B3 = ['P8-25', 'P8-26', 'P8-27', 'P8-28', 'P8-29', 'P8-30']
    IDX_list_B4 = ['P8-31', 'P8-32', 'P8-33', 'P8-34', 'P8-35', 'P8-36']
    IDX_list_B5 = ['P8-07', 'P8-08', 'P8-09', 'P8-10', 'P8-11', 'P8-12']
    IDX_list_B6 = ['P8-19', 'P8-20', 'P8-21', 'P8-22', 'P8-23', 'P8-24']

    # Generate taxonomy colormap
    print("Generating taxonomy colormap...")
    plot_taxonomy_colormap()

    # Generate composition diagrams for Fig 1-3
    print("Generating composition diagrams...")
    IDX_list_subcomm = np.sort(Community_PermutateList("F", "S", "M", "S", 12, 1,
                                                        Metadata=Metadata,
                                                        exception_list=exception_list))
    plot_composition_diagram(Processed_sequences_synthetic, IDX_list_subcomm, "subcomm",
                           f'{FigureTitle}/Fig_1-3_compositionDiagram_subcomm_rep1.svg')

    IDX_list_mixed = np.sort(Community_PermutateList("F", "S", "M", "C", 12, 1,
                                                     Metadata=Metadata,
                                                     exception_list=exception_list))
    plot_composition_diagram(Processed_sequences_synthetic, IDX_list_mixed, "mixed",
                           f'{FigureTitle}/Fig_1-3_compositionDiagram_mixed_rep1.svg')

    # Generate time series plots for Nutr- (LN) example 1
    print("Generating time series for Nutr- example 1...")
    IDX_list_sub1 = IDX_list_A1
    IDX_list_sub2 = IDX_list_A2
    IDX_list_coal = IDX_list_A6

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub1])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub1_final = df.iloc[-1].values[1:]

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub2])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub2_final = df.iloc[-1].values[1:]

    sub1_mask = (sub1_final > sub2_final)
    sub2_mask = (sub2_final > sub1_final)

    # Individual plots to timeseries folder
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub1, sub1_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Nutr-_ex1_sub1.svg')
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub2, sub2_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Nutr-_ex1_sub2.svg')
    plot_timeseries_coal(Processed_sequences_synthetic, IDX_list_coal, sub1_mask,
                        sub2_mask, sub1_final, sub2_final,
                        f'{timeseries_dir}/Fig_1-3_timeseries_Nutr-_ex1_coal.svg')
    # Merged plot to timeseries_merged folder
    plot_timeseries_merged(Processed_sequences_synthetic, IDX_list_sub1, IDX_list_sub2,
                          IDX_list_coal, sub1_mask, sub1_final, sub2_final,
                          f'{timeseries_merged_dir}/Fig_1-3_timeseries_Nutr-_ex1_merged.svg')

    # Generate time series plots for Nutr- (LN) example 2
    print("Generating time series for Nutr- example 2...")
    IDX_list_sub1 = IDX_list_A4
    IDX_list_sub2 = IDX_list_A3
    IDX_list_coal = IDX_list_A6

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub1])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub1_final = df.iloc[-1].values[1:]

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub2])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub2_final = df.iloc[-1].values[1:]

    sub1_mask = (sub1_final > sub2_final)
    sub2_mask = (sub2_final > sub1_final)

    # Individual plots to timeseries folder
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub1, sub1_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Nutr-_ex2_sub1.svg')
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub2, sub2_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Nutr-_ex2_sub2.svg')
    plot_timeseries_coal(Processed_sequences_synthetic, IDX_list_coal, sub1_mask,
                        sub2_mask, sub1_final, sub2_final,
                        f'{timeseries_dir}/Fig_1-3_timeseries_Nutr-_ex2_coal.svg')
    # Merged plot to timeseries_merged folder
    plot_timeseries_merged(Processed_sequences_synthetic, IDX_list_sub1, IDX_list_sub2,
                          IDX_list_coal, sub1_mask, sub1_final, sub2_final,
                          f'{timeseries_merged_dir}/Fig_1-3_timeseries_Nutr-_ex2_merged.svg')

    # ========================================================================
    # Base (MN - Medium Nutrient) Time Series
    # ========================================================================
    # From notebook: D2+D8->B12, G5+G6->D9, G9+G10->D11
    print("Generating time series for Base...")

    # Base Example 1: D2 + D8 -> B12 (SC12 coalescence)
    IDX_list_sub1 = IDX_list_D2
    IDX_list_sub2 = IDX_list_D8
    IDX_list_coal = IDX_list_B12

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub1])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub1_final = df.iloc[-1].values[1:]

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub2])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub2_final = df.iloc[-1].values[1:]

    sub1_mask = (sub1_final > sub2_final)
    sub2_mask = (sub2_final > sub1_final)

    # Individual plots to timeseries folder
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub1, sub1_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex1_sub1.svg')
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub2, sub2_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex1_sub2.svg')
    plot_timeseries_coal(Processed_sequences_synthetic, IDX_list_coal, sub1_mask,
                        sub2_mask, sub1_final, sub2_final,
                        f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex1_coal.svg')
    # Merged plot to timeseries_merged folder
    plot_timeseries_merged(Processed_sequences_synthetic, IDX_list_sub1, IDX_list_sub2,
                          IDX_list_coal, sub1_mask, sub1_final, sub2_final,
                          f'{timeseries_merged_dir}/Fig_1-3_timeseries_Base_ex1_merged.svg')

    # Base Example 2: G6 + G9 -> D9 (SC24 coalescence)
    IDX_list_sub1 = IDX_list_G6
    IDX_list_sub2 = IDX_list_G9
    IDX_list_coal = IDX_list_D9

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub1])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub1_final = df.iloc[-1].values[1:]

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub2])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub2_final = df.iloc[-1].values[1:]

    sub1_mask = (sub1_final > sub2_final)
    sub2_mask = (sub2_final > sub1_final)

    # Individual plots to timeseries folder
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub1, sub1_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex2_sub1.svg')
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub2, sub2_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex2_sub2.svg')
    plot_timeseries_coal(Processed_sequences_synthetic, IDX_list_coal, sub1_mask,
                        sub2_mask, sub1_final, sub2_final,
                        f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex2_coal.svg')
    # Merged plot to timeseries_merged folder
    plot_timeseries_merged(Processed_sequences_synthetic, IDX_list_sub1, IDX_list_sub2,
                          IDX_list_coal, sub1_mask, sub1_final, sub2_final,
                          f'{timeseries_merged_dir}/Fig_1-3_timeseries_Base_ex2_merged.svg')

    # Base Example 3: G5 + G10 -> D11 (SC24 coalescence)
    IDX_list_sub1 = IDX_list_G5
    IDX_list_sub2 = IDX_list_G10
    IDX_list_coal = IDX_list_D11

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub1])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub1_final = df.iloc[-1].values[1:]

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub2])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub2_final = df.iloc[-1].values[1:]

    sub1_mask = (sub1_final > sub2_final)
    sub2_mask = (sub2_final > sub1_final)

    # Individual plots to timeseries folder
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub1, sub1_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex3_sub1.svg')
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub2, sub2_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex3_sub2.svg')
    plot_timeseries_coal(Processed_sequences_synthetic, IDX_list_coal, sub1_mask,
                        sub2_mask, sub1_final, sub2_final,
                        f'{timeseries_dir}/Fig_1-3_timeseries_Base_ex3_coal.svg')
    # Merged plot to timeseries_merged folder
    plot_timeseries_merged(Processed_sequences_synthetic, IDX_list_sub1, IDX_list_sub2,
                          IDX_list_coal, sub1_mask, sub1_final, sub2_final,
                          f'{timeseries_merged_dir}/Fig_1-3_timeseries_Base_ex3_merged.svg')

    # ========================================================================
    # Nutr+ (HN - High Nutrient) Time Series
    # ========================================================================
    # From notebook: B1+B2->B4
    print("Generating time series for Nutr+...")

    # Nutr+ Example 1: B1 + B2 -> B4
    IDX_list_sub1 = IDX_list_B1
    IDX_list_sub2 = IDX_list_B2
    IDX_list_coal = IDX_list_B4

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub1])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub1_final = df.iloc[-1].values[1:]

    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                           for x in IDX_list_sub2])
    df = Processed_sequences_synthetic.iloc[IDX_list_]
    sub2_final = df.iloc[-1].values[1:]

    sub1_mask = (sub1_final > sub2_final)
    sub2_mask = (sub2_final > sub1_final)

    # Individual plots to timeseries folder
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub1, sub1_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Nutr+_ex1_sub1.svg')
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub2, sub2_mask,
                       f'{timeseries_dir}/Fig_1-3_timeseries_Nutr+_ex1_sub2.svg')
    plot_timeseries_coal(Processed_sequences_synthetic, IDX_list_coal, sub1_mask,
                        sub2_mask, sub1_final, sub2_final,
                        f'{timeseries_dir}/Fig_1-3_timeseries_Nutr+_ex1_coal.svg')
    # Merged plot to timeseries_merged folder
    plot_timeseries_merged(Processed_sequences_synthetic, IDX_list_sub1, IDX_list_sub2,
                          IDX_list_coal, sub1_mask, sub1_final, sub2_final,
                          f'{timeseries_merged_dir}/Fig_1-3_timeseries_Nutr+_ex1_merged.svg')

    # ========================================================================
    # Natural Community Time Series
    # ========================================================================
    # Natural subcommunities: P3 plate (6 communities, each with replicates)
    # Natural coalescence: P7 plate
    print("Generating time series for Natural communities...")

    Processed_sequences_natural = data_dict['Processed_sequences_natural']

    # Natural subcommunity sample lists (P3 plate)
    # Community 1: P3-01 (L, rep1), P3-02 (L, rep2), P3-03 (M, rep1), P3-04 (M, rep2), P3-05 (H, rep1), P3-06 (H, rep2)
    # Community 2: P3-13 to P3-18
    # etc.

    # For natural, each community has samples across media and replicates (not time series)
    # Let's use M medium samples for consistency
    IDX_list_Nat_sub1 = ['P3-03', 'P3-04']  # Community 1, M medium, rep1 & rep2
    IDX_list_Nat_sub2 = ['P3-15', 'P3-16']  # Community 2, M medium, rep1 & rep2
    IDX_list_Nat_sub3 = ['P3-27', 'P3-28']  # Community 3, M medium

    # Natural coalescence (P7 plate) - Coal 1 = Community 1 + Community 2
    IDX_list_Nat_coal1 = ['P7-03', 'P7-04']  # M medium coalescence of 1+2

    # For natural communities, we need different plotting since structure is different
    # Natural has final compositions only, not time series
    # Let's create a simple composition comparison plot instead

    def plot_natural_composition(Processed_sequences_natural, sub1_ids, sub2_ids, coal_ids, filename):
        """Plot natural community compositions side by side."""
        color_map = settingTheColor()

        # Get compositions
        all_ids = sub1_ids + sub2_ids + coal_ids
        IDX_list_ = []
        for x in all_ids:
            idx = np.where(Processed_sequences_natural['SampleIDX'] == x)[0]
            if len(idx) > 0:
                IDX_list_.append(idx[0])

        if len(IDX_list_) == 0:
            print(f"Warning: No samples found for {filename}")
            return

        df = Processed_sequences_natural.iloc[IDX_list_]

        degList = [i for i in df.columns if i[0:4] == 'Norm']
        bar_l = np.array(range(df.shape[0]))

        f, ax = plt.subplots(1, figsize=(len(all_ids) * 4 * mm, 8 * 4 * mm),
                            facecolor='w', edgecolor='k')

        x_scale = 0.5
        bottom = np.zeros_like(bar_l).astype('float')

        # Use up to 43 colors (matching synthetic) or all available
        n_species = min(43, len(degList))
        for i in range(n_species):
            deg = degList[i]
            ax.bar(bar_l * x_scale, df[deg], width=0.9 * x_scale, bottom=bottom,
                   linewidth=0, color=color_map[i % len(color_map)])
            bottom += df[deg].values

        # Add remaining species with repeated colors if needed
        for i in range(n_species, len(degList)):
            deg = degList[i]
            ax.bar(bar_l * x_scale, df[deg], width=0.9 * x_scale, bottom=bottom,
                   linewidth=0, color=color_map[i % len(color_map)])
            bottom += df[deg].values

        ax.set_xticks(bar_l)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        f.subplots_adjust(right=0.75, bottom=0.4)

        f.savefig(filename, bbox_inches='tight')
        plt.close(f)

    # Plot natural community compositions
    plot_natural_composition(Processed_sequences_natural,
                            IDX_list_Nat_sub1, IDX_list_Nat_sub2, IDX_list_Nat_coal1,
                            f'{FigureTitle}/Fig_1-3_natural_composition_ex1.svg')

    # Additional natural examples
    # Example 2: Community 3 + Community 4
    IDX_list_Nat_sub3 = ['P3-27', 'P3-28']  # Community 3, M medium
    IDX_list_Nat_sub4 = ['P3-39', 'P3-40']  # Community 4, M medium
    IDX_list_Nat_coal2 = ['P7-09', 'P7-10']  # Coalescence of 3+4 (recipe row 9)

    plot_natural_composition(Processed_sequences_natural,
                            IDX_list_Nat_sub3, IDX_list_Nat_sub4, IDX_list_Nat_coal2,
                            f'{FigureTitle}/Fig_1-3_natural_composition_ex2.svg')

    # Generate phylogenetic tree
    print("Generating phylogenetic tree...")
    try:
        import build_phylogeny
        tree, df_phylo, abundances = build_phylogeny.main(output_dir=FigureTitle, data_dir='Data')
        print("Phylogenetic tree generated successfully!")
    except Exception as e:
        print(f"Warning: Could not generate phylogenetic tree: {e}")
        print("Continuing with other figures...")

    print("All figures generated successfully!")


if __name__ == "__main__":
    main()
