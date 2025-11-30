from common_setup import *

print('Processed_sequences_synthetic columns:')
print(Processed_sequences_synthetic.columns.tolist())

print('\nCoalescence_data columns:')
print(Coalescence_data.columns.tolist())

print('\nFirst 5 SampleIDX examples:')
print(Processed_sequences_synthetic['SampleIDX'].head(5).tolist())

print('\nFirst 5 Coalescence SampleIDX examples:')
print(Coalescence_data['SampleIDX'].head(5).tolist())