from common_setup import *

print('Checking available species numbers in data...')
print('Unique Community Size values:', sorted(Processed_sequences_synthetic['Community Size'].unique()))

print('\nChecking SampleIDX patterns:')
for s in [6, 12, 24]:
    count = len([idx for idx in Processed_sequences_synthetic['SampleIDX'] if f'_S_{s}_' in str(idx)])
    print(f'S{s} samples: {count}')

print('\nChecking coalescence data:')
for s in [6, 12, 24]:
    count = len([idx for idx in Coalescence_data['SampleIDX'] if f'_S_{s}_' in str(idx)])
    print(f'S{s} coalescence samples: {count}')

print('\nSample SampleIDX examples:')
print(Processed_sequences_synthetic['SampleIDX'].head(10).tolist())