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
    """Generate and shuffle color palette for ASV visualization."""
    np.random.seed(seed)
    cm = sns.color_palette("husl", 43)
    np.random.shuffle(cm)
    return cm


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

    # Use settingTheColor with appropriate size for phylogeny data
    np.random.seed(4)
    cm = sns.color_palette("husl", len(data))
    np.random.shuffle(cm)
    color_map = cm[::-1]

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
    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                            for x in IDX_list])
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
    plt.close(f)


def plot_timeseries_coal(Processed_sequences_synthetic, IDX_list, mask_1, mask_2,
                        species_1, species_2, filename):
    """Plot time series for coalescence communities."""
    np.random.seed(42)
    mask_2 = ~mask_1
    IDX_list_ = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX'] == x)
                            for x in IDX_list])
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
    plt.close(f)


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main function to generate all Figure 1-1 plots."""
    # Load data
    data_dict = load_data()
    Metadata = data_dict['Metadata']
    Processed_sequences_synthetic = data_dict['Processed_sequences_synthetic']

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

    # MN conditions
    IDX_list_D2 = ['P1-10', 'P1-11', 'P1-12', 'P1-34', 'P1-35', 'P1-36']
    IDX_list_D8 = ['P1-22', 'P1-23', 'P1-24', 'P1-46', 'P1-47', 'P1-48']
    IDX_list_B12 = ['P8-34', 'P8-35', 'P8-36', 'P8-70', 'P8-71', 'P8-72']

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

    # Generate time series plots for LN example 1
    print("Generating time series for LN example 1...")
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

    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub1, sub1_mask,
                       f'{FigureTitle}/Fig_1-3_timeseries_ex1_sub1.svg')
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub2, sub2_mask,
                       f'{FigureTitle}/Fig_1-3_timeseries_ex1_sub2.svg')
    plot_timeseries_coal(Processed_sequences_synthetic, IDX_list_coal, sub1_mask,
                        sub2_mask, sub1_final, sub2_final,
                        f'{FigureTitle}/Fig_1-3_timeseries_ex1_coal.svg')

    # Generate time series plots for LN example 2
    print("Generating time series for LN example 2...")
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

    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub1, sub1_mask,
                       f'{FigureTitle}/Fig_1-3_timeseries_ex2_sub1.svg')
    plot_timeseries_sub(Processed_sequences_synthetic, IDX_list_sub2, sub2_mask,
                       f'{FigureTitle}/Fig_1-3_timeseries_ex2_sub2.svg')
    plot_timeseries_coal(Processed_sequences_synthetic, IDX_list_coal, sub1_mask,
                        sub2_mask, sub1_final, sub2_final,
                        f'{FigureTitle}/Fig_1-3_timeseries_ex2_coal.svg')

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
