#!/usr/bin/env python3
"""
Count data points in AbundantRemoved plot with and without mixing filter
"""

import numpy as np
import pandas as pd
from common_setup import *

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

def getPairwiseCountData():
    Pairwise_Count_data_path = '../../Postprocessed/PairwiseColonyCountings_processed_230915.xlsx'
    Mono_Count_data = {}
    Pairwise_Count_data = {}
    for i, medium in enumerate(['LN', 'MN', 'HN']):
        Data = pd.read_excel(Pairwise_Count_data_path, sheet_name=i)
        Data = np.transpose(np.array(Data.values[:,1:]))
        Mono_Count_data[medium] = Data
    for i, medium in enumerate(['LN', 'MN', 'HN']):
        sheet1 = 3 + i*2
        sheet2 = 4 + i*2
        Data_1 = pd.read_excel(Pairwise_Count_data_path, sheet_name=sheet1)
        Data_1 = np.array(Data_1.values[:,1:])
        Data_2 = pd.read_excel(Pairwise_Count_data_path, sheet_name=sheet2)
        Data_2 = np.array(Data_2.values[:,1:])
        Data = np.stack([Data_1, Data_2])
        Pairwise_Count_data[medium] = Data
    return Mono_Count_data, Pairwise_Count_data

def getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium_type):
    data_m = np.mean(Mono_Count_data[medium_type], 1)
    data_p_1 = Pairwise_Count_data[medium_type][0,:]
    data_p_2 = Pairwise_Count_data[medium_type][1,:]
    data_p_ratio = np.array([[None] * 12]*12)
    for i in range(12):
        for j in range(12):
            if np.isnan(data_p_1[i,j]):
                continue
            else:
                if data_p_1[i,j]==1 and data_p_2[i,j]==0:
                    data_p_ratio[i,j] = 1
                elif data_p_1[i,j]==0 and data_p_2[i,j]==1:
                    data_p_ratio[i,j] = 0
                else:
                    data_p_1_converted = data_p_1[i,j]/data_m[i]
                    data_p_2_converted = data_p_2[i,j]/data_m[j]
                    if data_p_1_converted + data_p_2_converted > 0:
                        data_p_ratio[i,j] = data_p_1_converted/(data_p_1_converted+data_p_2_converted)
    return data_p_1, data_p_2, None, data_p_ratio

print("="*80)
print("COUNTING DATA POINTS IN ABUNDANTREMOVED PLOT")
print("="*80)

Mono_Count_data, Pairwise_Count_data = getPairwiseCountData()

for medium in ['M', 'H']:
    print(f"\n{'='*80}")
    print(f"MEDIUM: {medium}N")
    print(f"{'='*80}")

    data_p_1, data_p_2, _, data_p_ratio = getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium+'N')

    count_before_mixing_filter = 0
    count_after_mixing_filter = 0

    for pool_size in [6, 12, 24]:
        type_name = medium + f'N_{pool_size}'
        IDX_list = Syn_Coal_IDX[type_name]
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_1 = Coalescence_data.iloc[idx]['SampleIDX_Sub1'].tolist()
        idx_1 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_1])
        idx = np.squeeze([np.where(Coalescence_data['SampleIDX']==x) for x in IDX_list])
        idx_2 = Coalescence_data.iloc[idx]['SampleIDX_Sub2'].tolist()
        idx_2 = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in idx_2])
        idx = np.squeeze([np.where(Processed_sequences_synthetic['SampleIDX']==x) for x in IDX_list])

        for i in range(len(idx)):
            c_mix = Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:]
            c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
            c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
            c_1 = c_1*(c_1>1e-4)
            c_2 = c_2*(c_2>1e-4)

            C1_idx = np.argmax(c_1)
            C2_idx = np.argmax(c_2)
            C1 = C1_idx
            C2 = C2_idx

            # Remove dominant species
            c_1_removed = c_1.copy()
            c_2_removed = c_2.copy()
            c_mix_removed = np.array(c_mix.copy())

            c_1_removed[C1_idx] = 0
            c_1_removed[C2_idx] = 0
            c_2_removed[C1_idx] = 0
            c_2_removed[C2_idx] = 0
            c_mix_removed[C1_idx] = 0
            c_mix_removed[C2_idx] = 0

            if np.sum(c_1_removed) > 0:
                c_1_removed = c_1_removed / np.sum(c_1_removed)
            if np.sum(c_2_removed) > 0:
                c_2_removed = c_2_removed / np.sum(c_2_removed)
            if np.sum(c_mix_removed) > 0:
                c_mix_removed = c_mix_removed / np.sum(c_mix_removed)

            if np.sum(c_1_removed) == 0 or np.sum(c_2_removed) == 0 or np.sum(c_mix_removed) == 0:
                continue

            try:
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1_removed, c_2_removed, c_mix_removed)

                if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                    continue

                vector_similarity_score = np.arctan(u / (v + 1e-8)) / (np.pi / 2)
                if np.isnan(vector_similarity_score) or np.isinf(vector_similarity_score):
                    continue

                if C1 >= 12 or C2 >= 12:
                    continue

                if data_p_ratio[C1, C2] == None:
                    continue

                # Count BEFORE mixing filter
                count_before_mixing_filter += 1

                # Check mixing filter
                mixing_strength = u**2 + v**2
                if mixing_strength > 0.5:
                    count_after_mixing_filter += 1

            except:
                continue

    print(f"Data points BEFORE mixing filter (u²+v² > 0.5): {count_before_mixing_filter}")
    print(f"Data points AFTER mixing filter (u²+v² > 0.5):  {count_after_mixing_filter}")
    print(f"Filtered out: {count_before_mixing_filter - count_after_mixing_filter} ({(count_before_mixing_filter - count_after_mixing_filter)/count_before_mixing_filter*100:.1f}%)")
    print(f"After duplication: {count_after_mixing_filter * 2}")
