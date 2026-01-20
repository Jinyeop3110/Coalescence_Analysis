#Version Numbers Used to Generate this Pset:
#seaborn=0.11.2
#scipy==1.8.0
#numpy==1.22.2
#matplotlib==3.5.1

import scipy as sp
from pylab import *
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator,FormatStrFormatter,MaxNLocator
import pandas as pd
import seaborn as sns
import collections
from IPython.display import clear_output
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

DataTitle="Data_dynamics"

colors=colors = ['#A7216A',  # rich magenta-purple
          '#802000',
          '#E24912',  # deep orange-red
          ]


np.random.seed(1)
if not os.path.exists(DataTitle):

   # Create a new directory because it does not exist
   os.makedirs(DataTitle)
   print("The new directory is created!")

mm = 0.1/2.54
os.environ['PATH'] = os.environ['PATH'] + ':/Library/TeX/texbin/latex'
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.minor.width'] = 0.4
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.minor.width'] = 0.4
mpl.rcParams['ytick.major.width'] = 0.5

plt.rcParams['text.usetex'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


from matplotlib.colors import ListedColormap, LinearSegmentedColormap

my_cmap = ListedColormap(['#00429d', '#4771b2', '#73a2c6', '#a5d5d8', '#ffffe0', '#ffbcaf', '#f4777f', '#cf3759', '#93003a'], name="my_cmap")
my_cmap_r = my_cmap.reversed()
mpl.colormaps.register(cmap=my_cmap)
mpl.colormaps.register(cmap=my_cmap_r)




def getIDX(data, IDX):
    O = np.flatnonzero([x == IDX for x in data['SampleIDX']])
    return np.array(O)

def getAbundance(Processed_sequences,IDX):
    SampleIdx= np.flatnonzero([x == IDX for x in Processed_sequences['SampleIDX']])
    if not any(SampleIdx):
        return
    else:
        O=Processed_sequences.iloc[SampleIdx].values.tolist()[0][1:]
        return O

def getAbundance_fromList(Processed_sequences,IDX_list):
    IDX_list_=np.squeeze([np.where(Processed_sequences['SampleIDX']==x) for x in IDX_list])
    return (np.array(Processed_sequences.iloc[IDX_list_].values)[:,1:]).astype(float)

def Community_PermutateList_simulation(I,S):
    global Metadata,exception_list
    sample_num=500
    O=(3*(I-1)+(S-1))*500+np.arange(0,500)
    return O

def CommunityPermutate(Timepoint, CommunityOrigin, Medium, CoalescenceType):
    global Metadata
    idx = np.where((Metadata['Timepoint'] == Timepoint) &
                   (Metadata['CommunityOrigin'] == CommunityOrigin) &
                   (Metadata['Medium'] == Medium) &
                   (Metadata['CoalescenceType'] == CoalescenceType))[0]
    O = np.concatenate(Metadata['SampleIDX'][idx])
    return O

def CommunityPermutate_withSpeciesPoolsize(Timepoint, CommunityOrigin, Medium, CoalescenceType, species_pool_num):
    global Metadata,exception_list
    idx = (Metadata['Timepoint'] == Timepoint) & \
          (Metadata['CommunityOrigin'] == CommunityOrigin) & \
          (Metadata['Medium'] == Medium) & \
          (Metadata['CoalescenceType'] == CoalescenceType)

    communityIDX = np.array([int(x) for x in Metadata['CommunityIDX']])
    if CoalescenceType == 'S':
        if species_pool_num == 6:
            idx = idx & (communityIDX <= 9)
        elif species_pool_num == 12:
            idx = idx & ((communityIDX > 9) & (communityIDX <= 18))
        elif species_pool_num == 24:
            idx = idx & ((communityIDX > 18) & (communityIDX <= 30))
    elif CoalescenceType == 'C':
        if species_pool_num == 6:
            idx = idx & (communityIDX <= 14)
        elif species_pool_num == 12:
            idx = idx & ((communityIDX > 14) & (communityIDX <= 41))
        elif species_pool_num == 24:
            idx = idx & ((communityIDX > 41) & (communityIDX <= 47))

    O = Metadata['SampleIDX'][idx]
    O = list(set(O) - set(exception_list))
    return O

def Community_PermutateList(Timepoint, CommunityOrigin, Medium, CoalescenceType, species_pool_num=0, Replicate=-1):
    global Metadata,exception_list
    
    if Replicate==-1:
        idx = (Metadata['Timepoint'] == Timepoint) & \
              (Metadata['CommunityOrigin'] == CommunityOrigin) & \
              (Metadata['Medium'] == Medium) & \
              (Metadata['CoalescenceType'] == CoalescenceType)
    elif Replicate == 1 or Replicate == 2 : 
        idx = (Metadata['Timepoint'] == Timepoint) & \
              (Metadata['CommunityOrigin'] == CommunityOrigin) & \
              (Metadata['Medium'] == Medium) & \
              (Metadata['CoalescenceType'] == CoalescenceType) & \
              (Metadata['Replicate'] == Replicate)
    else : 
        raise ValueError("Invalid input")

    
    if CommunityOrigin=='S':
        communityIDX = np.array([int(x) for x in Metadata['CommunityIDX']])
        if CoalescenceType == 'S':
            if species_pool_num == 6:
                idx = idx & (communityIDX <= 9)
            elif species_pool_num == 12:
                idx = idx & ((communityIDX > 9) & (communityIDX <= 18))
            elif species_pool_num == 24:
                idx = idx & ((communityIDX > 18) & (communityIDX <= 30))
            elif species_pool_num ==0:
                idx = idx
        elif CoalescenceType == 'C':
            if species_pool_num == 6:
                idx = idx & (communityIDX <= 14)
            elif species_pool_num == 12:
                idx = idx & ((communityIDX > 14) & (communityIDX <= 41))
            elif species_pool_num == 24:
                idx = idx & ((communityIDX > 41) & (communityIDX <= 47))
            elif species_pool_num ==0:
                idx = idx
    elif CommunityOrigin=='N':
        communityIDX = np.array([int(x) for x in Metadata['CommunityIDX']])
        
    O = Metadata['SampleIDX'][idx]
    O = list(set(O) - set(exception_list))
    return O

def getCommunities(Communities_data,IDX_list):
    IDX_list_=np.squeeze([np.where(Communities_data['SampleIDX']==x) for x in IDX_list])
    return (Communities_data.iloc[IDX_list_])

def getCoalescence(Coalescence_data,IDX_list):
    IDX_list_=np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])#IDX_list_
    return (Coalescence_data.iloc[IDX_list_])

Coalescence_data_synthetic_path ="../../Analyzed/processed_CoalescenceEvent_synthetic.xlsx"
Communities_data_synthetic_path ="../../Analyzed/processed_Communities_synthetic.xlsx"
Coalescence_data_natural_path ="../../Analyzed/processed_CoalescenceEvent_natural.xlsx"
Communities_data_natural_path ="../../Analyzed/processed_Communities_natural.xlsx"
Coalescence_recipe_path="../../Postprocessed/CoalescenceRecipe.xlsx"
Meta_data_path="../../Postprocessed/Metadata.xlsx"
Processed_sequences_synthetic_path="../../Postprocessed/processed_Sequences_synthetic.xlsx"
Processed_sequences_natural_path="../../Postprocessed/processed_Sequences_natural.xlsx"
Coalescence_data_sim_path="../../Analyzed/processed_CoalescenceEvent_simulation_uniform.xlsx"
#Communities_data_sim_path="Analyzed/processed_Communities_simulation_uniform.xlsx"

Coalescence_data=pd.concat([pd.read_excel(Coalescence_data_synthetic_path),pd.read_excel(Coalescence_data_natural_path)])
Communities_data=pd.concat([pd.read_excel(Communities_data_synthetic_path),pd.read_excel(Communities_data_natural_path)])
Coalescence_data_sim=pd.read_excel(Coalescence_data_sim_path)
#Communities_data_sim=pd.read_excel(Communities_data_sim_path)

Coalescence_recipe=pd.read_excel(Coalescence_recipe_path,sheet_name=0)
Coalescence_natural_recipe=pd.read_excel(Coalescence_recipe_path,sheet_name=1)
Metadata=pd.read_excel(Meta_data_path)
Processed_sequences_synthetic=pd.read_excel(Processed_sequences_synthetic_path)
Processed_sequences_natural=pd.read_excel(Processed_sequences_natural_path)

exception_list=['P4-02','P4-03','P4-23','P4-24','P7-97', 'P8-12']+['P8-91'] + ['P5-73', 'P5-69','P5-64','P5-61','P5-59', 'P5-56'] + ['P5-47', 'P5-50'] + ['P5-39', 'P5-87', 'P5-54', 'P6-02', 'P6-47', 'P6-74', 'P6-57']
#'P4-02','P4-03','P4-23','P4-24','P7-97', 'P8-12' : These cases are for no reads in coalescence result
# 'P8-91' : no file
#['P5-73', 'P5-69','P5-64','P5-61','P5-59', 'P5-56'] : MN E7 is missing
# 'P6-67' : is too low reads( 500)
# 'P5-47', 'P5-50' : MN24 CC, too much unwanted ASVs(maybe due to wrong labeling)
# ['P5-39', 'P5-87', 'P5-54', 'P6-02', 'P6-47', 'P6-74', 'P6-57'] : ASV not in sub 2> 0.3

I = [0.33, 0.66, 0.99]
species_pools = [6, 12, 24]
sample_num=500
Syn_Simulation_IDX = {
    "I1_S1": Community_PermutateList_simulation(1,1),
    "I1_S2": Community_PermutateList_simulation(1,2),
    "I1_S3": Community_PermutateList_simulation(1,3),
    "I2_S1": Community_PermutateList_simulation(2,1),
    "I2_S2": Community_PermutateList_simulation(2,2),
    "I2_S3": Community_PermutateList_simulation(2,3),
    "I3_S1": Community_PermutateList_simulation(3,1),
    "I3_S2": Community_PermutateList_simulation(3,2),
    "I3_S3": Community_PermutateList_simulation(3,3),
}
mediums_pools = ["LN", "MN", "HN"]
species_pools = [6, 12, 24]
Syn_Coal_IDX = {
    "LN_6": Community_PermutateList("F", "S", "L", "C", 6),
    "LN_12": Community_PermutateList("F", "S", "L", "C", 12),
    "LN_24": Community_PermutateList("F", "S", "L", "C", 24),
    "MN_6": Community_PermutateList("F", "S", "M", "C", 6),
    "MN_12": Community_PermutateList("F", "S", "M", "C", 12),
    "MN_24": Community_PermutateList("F", "S", "M", "C", 24),
    "HN_6": Community_PermutateList("F", "S", "H", "C", 6),
    "HN_12": Community_PermutateList("F", "S", "H", "C", 12),
    "HN_24": Community_PermutateList("F", "S", "H", "C", 24)
}
Syn_Sub_IDX = {
    "LN_6": Community_PermutateList("F", "S", "L", "S", 6),
    "LN_12": Community_PermutateList("F", "S", "L", "S", 12),
    "LN_24": Community_PermutateList("F", "S", "L", "S", 24),
    "MN_6": Community_PermutateList("F", "S", "M", "S", 6),
    "MN_12": Community_PermutateList("F", "S", "M", "S", 12),
    "MN_24": Community_PermutateList("F", "S", "M", "S", 24),
    "HN_6": Community_PermutateList("F", "S", "H", "S", 6),
    "HN_12": Community_PermutateList("F", "S", "H", "S", 12),
    "HN_24": Community_PermutateList("F", "S", "H", "S", 24)
}
Nat_Coal_IDX = {
    "LN": Community_PermutateList("F", "N", "L", "C"),
    "MN": Community_PermutateList("F", "N", "M", "C"),
    "HN": Community_PermutateList("F", "N", "H", "C")
}
Nat_Sub_IDX = {
    "LN": Community_PermutateList("F", "N", "L", "S"),
    "MN": Community_PermutateList("F", "N", "M", "S"),
    "HN": Community_PermutateList("F", "N", "H", "S")
}



def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm


def metric_VectorDecomposition_onlyPositive(u,v,m):
    u=normalize(u)
    v=normalize(v)
    m=normalize(m)
    
    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])

    e12=np.matmul(np.linalg.inv(A),np.array([np.sum(m*u), np.sum(m*v)]))
    
    x1=(e12[0])*(e12[0]>0)
    x2=(e12[1])*(e12[1]>0)
    x3=np.linalg.norm(m-(e12[0]*u)-(e12[1]*v))
    convert=np.sqrt((1-x3**2)/(x1**2+x2**2))
    
    return convert*x1, convert*x2, x3


def uniform_distribution(u,o):
    return (2*u+2*o)*np.random.random()-o

def input_distribution():
    k=0.8
    return np.random.exponential(k)

def InitializeCommunityPool(N, num_C, num_S, I,g,k, save_path="Data/test"):
    CommunitiesLibrary=np.zeros([num_C, N])
    for i in range(num_C):
        #CommunitiesLibrary[i,random.sample(list(np.arange(N)), num_S)]=1
        CommunitiesLibrary[i,np.arange(num_S*i,num_S*(i+1))]=1
    df1=pd.DataFrame(CommunitiesLibrary)
    with pd.ExcelWriter(save_path+'/commuityLibrary.xlsx') as writer:  
        df1.to_excel(writer,sheet_name='Sheet1')
    return CommunitiesLibrary

def InitializeRandomCommunityPool(N, num_C, num_S, I,g,k, save_path="Data/test"):
    CommunitiesLibrary=np.zeros([num_C, N])
    for i in range(num_C):
        CommunitiesLibrary[i,random.sample(list(np.arange(N)), num_S)]=1
    df1=pd.DataFrame(CommunitiesLibrary)
    with pd.ExcelWriter(save_path+'/commuityLibrary.xlsx') as writer:  
        df1.to_excel(writer,sheet_name='Sheet1')
    return CommunitiesLibrary



def calculate_assymetricity(u,v,k):
    """
    Calculate asymmetricity coordinates (x, y) from vector decomposition coefficients.

    Args:
        u: Coefficient for parent community 1
        v: Coefficient for parent community 2
        k: Coefficient for novel/restructured component (not used in calculation)

    Returns:
        x: Combined magnitude of both parent coefficients
        y: Asymmetricity measure (0 = balanced, 1 = highly asymmetric)
    """
    x=np.sqrt(np.array(u)**2+np.array(v)**2)
    y=np.abs(np.abs(np.arctan(np.array(u)/np.array(v)))-np.pi/4)/(np.pi/4)
    return x,y

def characterize_case(x,y):
    """
    Classify coalescence outcome using asymmetricity (x, y) coordinates.

    Classification rules:
    - if (x² > 0.5) and (y > 0.5): DOMINANCE (high magnitude + asymmetric) → class 0
    - if (x² > 0.5) and (y < 0.5): MIXING (high magnitude + symmetric) → class 1
    - if (x² < 0.5): RESTRUCTURING (low magnitude overall) → class 2

    Args:
        x: Combined magnitude of parent coefficients
        y: Asymmetricity measure

    Returns:
        int: 0 (Dominance), 1 (Mixing), or 2 (Restructuring)
    """
    if (x**2>0.5)*(y>0.5):
        return 0
    if (x**2>0.5)*(y<0.5):
        return 1
    if (x**2<0.5):
        return 2

def characterize_case_direct(x1, x2, x3):
    """
    DEPRECATED: Alternative classification system using direct thresholds on (x1, x2, x3).

    NOTE: This function is no longer used. The current classification uses
    characterize_case() with calculate_assymetricity() transformation.
    Kept for reference and potential future use.

    Classification rules:
    - if x1 > sqrt(0.5): DOMINANCE (community 1 wins) → class 0
    - elif x2 > sqrt(0.5): DOMINANCE (community 2 wins) → class 0
    - elif x3 > sqrt(0.5): RESTRUCTURING → class 2
    - else: MIXING → class 1

    Threshold: sqrt(0.5) ≈ 0.707107 (tighter boundary)

    Args:
        x1: Coefficient for parent community 1
        x2: Coefficient for parent community 2
        x3: Coefficient for novel/restructured component

    Returns:
        int: 0 (Dominance), 1 (Mixing), or 2 (Restructuring)
    """
    threshold = 0.5 ** 0.5  # sqrt(0.5) ≈ 0.707107

    if x1 > threshold:
        return 0  # Dominance (c1 wins)
    elif x2 > threshold:
        return 0  # Dominance (c2 wins)
    elif x3 > threshold:
        return 2  # Restructuring
    else:
        return 1  # Mixing
    


import numpy as np
import matplotlib.pyplot as plt

def create_phase_diagram(
    type_names,
    data1_set,
    data2_set,
    data3_set,
    custom_x_ticks=None,
    custom_x_labels=None,
    output_filename="../figure/Fig_phase_diagram.svg",
    plot_boundary=False,
):
    """
    Creates a stacked–filled bar plot of three classes 
    (Dominance, Mixing, Restructuring) across given type names.
    """
    n_types = len(type_names)
    class1_fractions = np.zeros(n_types + 1)
    class2_fractions = np.zeros(n_types + 1)
    class3_fractions = np.zeros(n_types + 1)

    # Import phase diagram colors from centralized COLORMAP
    from COLORMAP import get_phase_diagram_colors
    colors = get_phase_diagram_colors()  # [dominance, mixing, restructuring]

    for c_i, type_name in enumerate(type_names):
        class1_count = 0
        class2_count = 0
        class3_count = 0

        for j in range(len(data1_set[type_name])):
            # Get vector decomposition coefficients
            u = data1_set[type_name][j]
            v = data2_set[type_name][j]
            k = data3_set[type_name][j]

            # Transform to asymmetricity coordinates
            x, y = calculate_assymetricity(u, v, k)

            # Classify using asymmetricity-based boundaries
            ii = characterize_case(x, y)
            if ii == 0:
                class1_count += 1
            elif ii == 1:
                class2_count += 1
            else:
                class3_count += 1

        total = class1_count + class2_count + class3_count
        if total > 0:
            class1_fractions[c_i] = class1_count / total
            class2_fractions[c_i] = class2_count / total
            class3_fractions[c_i] = class3_count / total

    mm = 1 / 25.4 * 72
    fig_width = 60 * mm
    fig_height = 60 * mm

    fig, ax1 = plt.subplots(figsize=(fig_width / 72, fig_height / 72), facecolor='w')

    x_vals = np.arange(n_types + 1)

    fill1 = ax1.fill_between(
        x_vals,
        0,
        class1_fractions,
        step='post',
        color=colors[0],
        alpha=0.85,
        edgecolor='none'
    )
    fill2 = ax1.fill_between(
        x_vals,
        class1_fractions,
        class1_fractions + class2_fractions,
        step='post',
        color=colors[1],
        alpha=0.85,
        edgecolor='none'
    )
    fill3 = ax1.fill_between(
        x_vals,
        class1_fractions + class2_fractions,
        class1_fractions + class2_fractions + class3_fractions,
        step='post',
        color=colors[2],
        alpha=0.85,
        edgecolor='none'
    )

    ax1.set_ylabel('Fraction')
    ax1.set_xlabel(r'Interaction Strength $\mu$')
    ax1.set_xlim([0, n_types])
    ax1.set_ylim([0, 1])
    ax1.set_xticks([])
    ax1.set_xticks(custom_x_ticks, custom_x_labels)
    
    # Set custom y-axis ticks to show only 0 and 1
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['0', '1'])

    if plot_boundary:
        for boundary in range(1, n_types):
            ax1.axvline(
                x=boundary,
                color='black',
                linestyle='--',
                alpha=0.5,
                linewidth=1
            )

    # -- Single annotation per class --

    font_size = 7
    x_mid = n_types / 2

    # y positions: mean across all types
    y_dom = np.mean(class1_fractions[:n_types]) / 2
    y_mix = np.mean(class1_fractions[:n_types] + class2_fractions[:n_types] / 2)
    y_rest = np.mean(class1_fractions[:n_types] + class2_fractions[:n_types] + class3_fractions[:n_types] / 2)
    '''
        if np.max(class1_fractions) > 0.05:
            ax1.text(x_mid, y_dom, 'Dominance', ha='center', va='center', fontsize=font_size, color='white', weight='bold')
        if np.max(class2_fractions) > 0.05:
            ax1.text(x_mid, y_mix, 'Mixing', ha='center', va='center', fontsize=font_size, color='black', weight='bold')
        if np.max(class3_fractions) > 0.05:
            ax1.text(x_mid, y_rest, 'Restructuring', ha='center', va='center', fontsize=font_size, color='black', weight='bold')
    '''
    fig.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.show()




def drawPairwiseChange(i, j, x):
    # This is just a sample function. Replace this with your function.
    return np.sin(i*x) + np.cos(j*x)

def InterpretPairwiseResult(y1,y2):
    if y1==1 and y2==1:
        return 'E',(0.85, 0.7, 0.7) #E : competitive exclusion
    elif y1==0 and y2==0:
        return 'E',(0.85, 0.7, 0.7) #E : competitive exclusion
    elif y1==0 and y2==1:
        return 'B',(0.7, 0.7, 0.9) #B : Bistability
    elif y1>0 and y1<1 and y2>0 and y2<1:
        return 'C',(0.7, 0.85, 0.7) #C : Coexistence
    else:
        return 'U',(0.5, 0.5, 0.5) #U : Unclassified

def mask_equal(u,v,m):
    u_m=np.array(u)>0
    v_m=np.array(v)>0
    shared=u_m*v_m
    mask1=u_m-shared*(np.array(v)/(np.array(u)+np.array(v)+1e-8))
    mask2=1-mask1
    return mask1, mask2

def NbyNcomposition(Coalescence_data, Coal_IDX_list, Sub_IDX_list):
    N=len(Sub_IDX_list)
    Coal_matrix={}
    Coal_keys={}
    Coal_mask1={}
    Coal_mask2={}
    Sub_keys={}
    Sub_matrix={}
    for SampleIDX in Coal_IDX_list:
        idx=np.where(Coalescence_data['SampleIDX']==SampleIDX)
        subSampleIDX1=Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()[0]
        subSampleIDX2=Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()[0]
        Sub_IDX_list_array = np.atleast_1d(Sub_IDX_list)
        where_result1 = np.where(Sub_IDX_list_array==subSampleIDX1)
        subSampleIDX1 = np.atleast_1d(where_result1[0])[0] if len(where_result1[0]) > 0 else 0
        where_result2 = np.where(Sub_IDX_list_array==subSampleIDX2) 
        subSampleIDX2 = np.atleast_1d(where_result2[0])[0] if len(where_result2[0]) > 0 else 0
        IDX_list_=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in [SampleIDX]])
        df=Processed_sequences_synthetic.iloc[IDX_list_]
        c_mix=df.values[1:].tolist()
        ID_mix=df.values[0]
        
        SampleIDX=Coalescence_data.iloc[idx]["SampleIDX_Sub1"].tolist()[0]
        IDX_list_=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in [SampleIDX]])
        if (IDX_list_.size==0):
            continue
        df=Processed_sequences_synthetic.iloc[IDX_list_]
        c_1=df.values[1:].tolist()
        ID_1=df.values[0]   
        
        SampleIDX=Coalescence_data.iloc[idx]["SampleIDX_Sub2"].tolist()[0]
        IDX_list_=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in [SampleIDX]])
        if (IDX_list_.size==0):
            continue
        df=Processed_sequences_synthetic.iloc[IDX_list_]
        c_2=df.values[1:].tolist()
        ID_2=df.values[0]          
        
        mask_1,mask_2=mask_equal(c_1,c_2,c_mix)
        
        
        i=min(subSampleIDX1,subSampleIDX2)
        j=max(subSampleIDX1,subSampleIDX2)
        Coal_matrix[i,j]=c_mix
        Coal_keys[i,j]=ID_mix
        Coal_mask1[i,j]=mask_1
        Coal_mask2[i,j]=mask_2
        
        
    for SampleIDX in Sub_IDX_list:
        IDX_list_=np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in [SampleIDX]])
        if (IDX_list_.size==0):
            continue
        df=Processed_sequences_synthetic.iloc[IDX_list_]
        Sub_IDX_list_array = np.atleast_1d(Sub_IDX_list)
        where_result = np.where(Sub_IDX_list_array==SampleIDX)
        i = np.atleast_1d(where_result[0])[0] if len(where_result[0]) > 0 else 0
        Sub_matrix[i]=df.values[1:].tolist()
        Sub_keys[i]=df.values[0]
        
    return Coal_matrix, Sub_matrix, Coal_keys, Sub_keys,Coal_mask1,Coal_mask2



def extract_sc_cc_numeric(loaded_results, rep_num, intensity_index):
    """
    Extracts and converts sc_list and cc_list for a specified intensity and replicate number.

    Parameters
    ----------
    loaded_results : dict
        The nested dictionary containing all results.
    rep_num : int
        The replicate number corresponding to 'community_n' (0 to 9).
    intensity_index : int, optional
        The index of the intensity to select (0-based). Defaults to 2 (third intensity).

    Returns
    -------
    sc_list_numeric : dict
        Sub-community list with integer keys.
    cc_list_numeric : dict
        Coalescence list with tuple integer keys.

    Raises
    ------
    ValueError
        If the loaded_results does not contain enough intensity levels,
        or if the specified community does not exist.
    """
    import sys

    # 1. Retrieve the specified intensity key
    intensity_keys = sorted(loaded_results.keys())
    if len(intensity_keys) <= intensity_index:
        raise ValueError(f"The loaded_results dictionary does not contain an intensity at index {intensity_index}.")

    intensity_key = intensity_keys[intensity_index]
    print(f"Selected Intensity: {intensity_key}")

    # 2. Construct the community key
    community_key = f'community_{rep_num}'
    print(f"Selected Community: {community_key}")

    # 3. Access the community data
    community_data = loaded_results.get(intensity_key, {}).get(community_key, {})
    if not community_data:
        raise ValueError(f"Community '{community_key}' not found under intensity '{intensity_key}'.")

    # 4. Extract sc_list and cc_list
    sc_list = community_data.get('sc_list', {})
    cc_list = community_data.get('cc_list', {})

    # 5. Convert sc_list keys from strings to integers
    sc_list_numeric = {}
    for k, v in sc_list.items():
        try:
            key_num = int(k)
            sc_list_numeric[key_num] = v
        except ValueError:
            print(f"Warning: Invalid sc_list key '{k}'. Skipping.", file=sys.stderr)

    # 6. Convert cc_list keys from 'x_y' strings to (x, y) tuples of integers
    cc_list_numeric = {}
    for k, v in cc_list.items():
        try:
            key_tuple = tuple(int(part) for part in k.split('_'))
            if len(key_tuple) != 2:
                raise ValueError
            cc_list_numeric[key_tuple] = v
        except ValueError:
            print(f"Warning: Invalid cc_list key '{k}'. Expected format 'x_y'. Skipping.", file=sys.stderr)

    return sc_list_numeric, cc_list_numeric


def prepare_X1_X2_y(loaded_results, rep_num, intensity_index,  eps=1e-4):
    # Extract sc_list and cc_list with numeric keys
    sc_list_numeric, cc_list_numeric = extract_sc_cc_numeric(loaded_results, rep_num, intensity_index)

    X1_all, X2_all, y_all = [], [], []

    # Iterate over each coalescence pair
    for (c1_idx, c2_idx), cmix in cc_list_numeric.items():
        c1 = sc_list_numeric.get(c1_idx)
        c2 = sc_list_numeric.get(c2_idx)

        if c1 is None or c2 is None:
            print(f"Warning: Sub-community indices {c1_idx}, {c2_idx} not found. Skipping.", file=sys.stderr)
            continue

        # Apply the metric function
        try:
            u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
        except np.linalg.LinAlgError as e:
            if 'Singular matrix' in str(e):
                print("Singular matrix error occurred.")
                print(f"c1: {c1}")
                print(f"c2: {c2}")
                print(f"cmix: {cmix}")
                u1=u2=1/sqrt(2)
                k=None
                
        # Calculate y

        # Append to the lists
        X1_all.append(c1)
        X2_all.append(c2)
        y_all.append(cmix)

    return np.array(X1_all), np.array(X2_all), np.array(y_all)



def prepare_dominance(loaded_results, rep_num, intensity_index,  eps=1e-4):
    # Extract sc_list and cc_list with numeric keys
    sc_list_numeric, cc_list_numeric = extract_sc_cc_numeric(loaded_results, rep_num, intensity_index)

    y_all = []

    # Iterate over each coalescence pair
    for (c1_idx, c2_idx), cmix in cc_list_numeric.items():
        c1 = sc_list_numeric.get(c1_idx)
        c2 = sc_list_numeric.get(c2_idx)

        if c1 is None or c2 is None:
            print(f"Warning: Sub-community indices {c1_idx}, {c2_idx} not found. Skipping.", file=sys.stderr)
            continue

        # Apply the metric function
        try:
            u, v, k = metric_VectorDecomposition_onlyPositive(c1, c2, cmix)
        except np.linalg.LinAlgError as e:
            if 'Singular matrix' in str(e):
                print("Singular matrix error occurred.")
                print(f"c1: {c1}")
                print(f"c2: {c2}")
                print(f"cmix: {cmix}")
                u=v=1/sqrt(2)
                k=0
        # Calculate y
        x,y=calculate_assymetricity(u,v,k)
        y = characterize_case(x,y)
        y_all.append(y)

    return np.array(y_all)


