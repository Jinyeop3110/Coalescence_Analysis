OD_correction_function_path='/Users/jysong/Desktop/MATLAB/general_functions/OD_correction_function_2202.mat'
folder_path='ExperimentalResult/Data/2208_Coalescence_processed/growth/'


fpath=[folder_path 'LN_SC_day7_GR.xlsx'];
[Time,Temp, LN_SC_GC]=GCread_SC(fpath,OD_correction_function_path)
fpath=[folder_path 'MN_SC_day7_GR.xlsx'];
[Time,Temp, MN_SC_GC]=GCread_SC(fpath,OD_correction_function_path)
fpath=[folder_path 'HN_SC_day7_GR.xlsx'];
[Time,Temp, HN_SC_GC]=GCread_SC(fpath,OD_correction_function_path)


fpath=[folder_path 'LN_CC_day7_GR.xlsx'];
[Time,Temp, LN_CC_GC]=GCread_CC(fpath,OD_correction_function_path)
fpath=[folder_path 'MN_CC_day7_GR.xlsx'];
[Time,Temp, MN_CC_GC]=GCread_CC(fpath,OD_correction_function_path)
fpath=[folder_path 'HN_CC_day7_GR.xlsx'];
[Time,Temp, HN_CC_GC]=GCread_CC(fpath,OD_correction_function_path)


fpath=[folder_path 'NCS_SC_day7_GR.xlsx'];
[Time,Temp, NCS_SC_GC]=GCread_SC_NC(fpath,OD_correction_function_path)

fpath=[folder_path 'NCS_CC_day7_GR.xlsx'];
[Time,Temp, NCS_CC_GC]=GCread_CC_NC(fpath,OD_correction_function_path)


%%