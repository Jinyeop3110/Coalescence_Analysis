#!/usr/bin/env python3
"""
Analyze why MN and HN have such different R² values
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
print("ANALYZING WHY MN vs HN HAVE DIFFERENT R² VALUES")
print("="*80)

Mono_Count_data, Pairwise_Count_data = getPairwiseCountData()

results = {}

for medium in ['M', 'H']:
    data_p_1, data_p_2, _, data_p_ratio = getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium+'N')

    x_all = []
    y_all = []
    mixing_strengths = []
    dominant_fractions = []

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
            c_mix = np.array(Processed_sequences_synthetic.iloc[idx[i]].values.tolist()[1:])
            c_1 = np.array(Processed_sequences_synthetic.iloc[idx_1[i]].values.tolist()[1:])
            c_2 = np.array(Processed_sequences_synthetic.iloc[idx_2[i]].values.tolist()[1:])
            c_1 = c_1*(c_1>1e-4)
            c_2 = c_2*(c_2>1e-4)

            try:
                u, v, k = metric_VectorDecomposition_onlyPositive(c_1, c_2, c_mix)
                if np.isnan(u) or np.isnan(v) or np.isnan(k) or np.isinf(u) or np.isinf(v) or np.isinf(k):
                    continue

                mixing_strength = u**2 + v**2
                if mixing_strength <= 0.5:
                    continue

                vector_similarity_score = np.arctan(u / (v + 1e-8)) / (np.pi / 2)
                if np.isnan(vector_similarity_score) or np.isinf(vector_similarity_score):
                    continue

                C1 = np.argmax(c_1)
                C2 = np.argmax(c_2)

                if C1 >= 12 or C2 >= 12:
                    continue
                if data_p_ratio[C1, C2] == None:
                    continue

                # Calculate dominant species fraction in c_mix
                dominant_frac = c_mix[C1] + c_mix[C2]

                x_raw = 1 - np.mean([1-data_p_ratio[C1,C2], data_p_ratio[C2,C1]])
                ratio = x_raw / (1 - x_raw + 1e-8)
                x = np.arctan(ratio) / (np.pi / 2)
                y = vector_similarity_score

                x_all.append(x)
                y_all.append(y)
                mixing_strengths.append(mixing_strength)
                dominant_fractions.append(dominant_frac)
            except:
                continue

    x_all = np.array(x_all)
    y_all = np.array(y_all)
    mixing_strengths = np.array(mixing_strengths)
    dominant_fractions = np.array(dominant_fractions)

    results[medium] = {
        'x': x_all,
        'y': y_all,
        'mixing': mixing_strengths,
        'dominant_frac': dominant_fractions
    }

print("\n" + "="*80)
print("COMPARISON: MN vs HN")
print("="*80)

for medium in ['M', 'H']:
    r = results[medium]
    print(f"\n{medium}N:")
    print(f"  Sample size: {len(r['x'])} unique events")
    print(f"  Mixing strength - Mean: {np.mean(r['mixing']):.3f}, Median: {np.median(r['mixing']):.3f}")
    print(f"  Dominant fraction - Mean: {np.mean(r['dominant_frac']):.3f}, Median: {np.median(r['dominant_frac']):.3f}")
    print(f"  X (species) variance: {np.var(r['x']):.4f}")
    print(f"  Y (community) variance: {np.var(r['y']):.4f}")

print("\n" + "="*80)
print("KEY DIFFERENCES")
print("="*80)

m_mixing = results['M']['mixing']
h_mixing = results['H']['mixing']
m_dom = results['M']['dominant_frac']
h_dom = results['H']['dominant_frac']

print(f"\n1. MIXING STRENGTH:")
print(f"   MN: {np.mean(m_mixing):.3f} ± {np.std(m_mixing):.3f}")
print(f"   HN: {np.mean(h_mixing):.3f} ± {np.std(h_mixing):.3f}")
print(f"   → HN has {'HIGHER' if np.mean(h_mixing) > np.mean(m_mixing) else 'LOWER'} mixing strength")

print(f"\n2. DOMINANT SPECIES FRACTION IN COALESCED COMMUNITY:")
print(f"   MN: {np.mean(m_dom):.3f} ± {np.std(m_dom):.3f}")
print(f"   HN: {np.mean(h_dom):.3f} ± {np.std(h_dom):.3f}")
print(f"   → HN has {'HIGHER' if np.mean(h_dom) > np.mean(m_dom) else 'LOWER'} dominant fraction")

print(f"\n3. SAMPLE SIZE:")
print(f"   MN: {len(results['M']['x'])} events")
print(f"   HN: {len(results['H']['x'])} events")
print(f"   → HN has {len(results['H']['x']) - len(results['M']['x'])} more events ({(len(results['H']['x'])/len(results['M']['x']) - 1)*100:.0f}% more)")

# Check distribution of x values
print(f"\n4. X-AXIS (SPECIES DOMINANCE) DISTRIBUTION:")
# Count how many x values are near extremes (0 or 1)
m_extreme = np.sum((results['M']['x'] < 0.2) | (results['M']['x'] > 0.8))
h_extreme = np.sum((results['H']['x'] < 0.2) | (results['H']['x'] > 0.8))
print(f"   MN: {m_extreme}/{len(results['M']['x'])} ({m_extreme/len(results['M']['x'])*100:.1f}%) near extremes (x<0.2 or x>0.8)")
print(f"   HN: {h_extreme}/{len(results['H']['x'])} ({h_extreme/len(results['H']['x'])*100:.1f}%) near extremes (x<0.2 or x>0.8)")

print(f"\n5. ALIGNMENT (X and Y on same side of 0.5):")
m_aligned = np.sum(((results['M']['x'] > 0.5) & (results['M']['y'] > 0.5)) | ((results['M']['x'] < 0.5) & (results['M']['y'] < 0.5)))
h_aligned = np.sum(((results['H']['x'] > 0.5) & (results['H']['y'] > 0.5)) | ((results['H']['x'] < 0.5) & (results['H']['y'] < 0.5)))
print(f"   MN: {m_aligned}/{len(results['M']['x'])} ({m_aligned/len(results['M']['x'])*100:.1f}%) aligned")
print(f"   HN: {h_aligned}/{len(results['H']['x'])} ({h_aligned/len(results['H']['x'])*100:.1f}%) aligned")

print("\n" + "="*80)
print("BIOLOGICAL INTERPRETATION")
print("="*80)
print("""
The 4.6x difference in R² (MN: 0.106 vs HN: 0.492) suggests:

HYPOTHESIS 1: Stronger top-down control at high nutrients
- HN has stronger competition → dominant species matter more
- MN has weaker competition → community-level effects matter more
- Pairwise species outcomes predict community outcomes better when competition is strong

HYPOTHESIS 2: Data quality/clarity differences
- HN may have clearer dominant species (higher dominant fraction)
- HN may have more decisive pairwise outcomes (more extreme x values)
- Better signal-to-noise ratio at high nutrients

HYPOTHESIS 3: Different ecological regimes
- MN: Intermediate competition, many species coexist, complex dynamics
- HN: Strong competition, dominant species control outcomes, simpler dynamics
- The top-down hypothesis works better in simple, competitive environments
""")
