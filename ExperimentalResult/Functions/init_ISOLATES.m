OD_correction_function_path='/Users/jysong/Desktop/MATLAB/general_functions/OD_correction_function_2202.mat'
folder_path='ExperimentalResult/Data/2208_Coalescence_processed/Isolates/'

fpath=[folder_path 'LN_ISO_GR.xlsx'];
[Time,Temp, LN_ISO_GC]=GCread_ISOLATES(fpath,OD_correction_function_path)

fpath=[folder_path 'MN_ISO_GR.xlsx'];
[Time,Temp, MN_ISO_GC]=GCread_ISOLATES(fpath,OD_correction_function_path)

fpath=[folder_path 'HN_ISO_GR.xlsx'];
[Time,Temp, HN_ISO_GC]=GCread_ISOLATES(fpath,OD_correction_function_path)

disp("init_ISOLATES finished")
