OD_correction_function_path='/Users/jysong/Desktop/MATLAB/general_functions/OD_correction_function_2202.mat'
folder_path='ExperimentalResult/Data/2208_Coalescence_processed/OD/'
fpath=[folder_path 'LN_SC_OD.xlsx'];
LN_SC_OD=ODread_SC(fpath,OD_correction_function_path)
fpath=[folder_path 'MN_SC_OD.xlsx'];
MN_SC_OD=ODread_SC(fpath,OD_correction_function_path)
fpath=[folder_path 'HN_SC_OD.xlsx'];
HN_SC_OD=ODread_SC(fpath,OD_correction_function_path)

fpath=[folder_path 'LN_CC_OD.xlsx'];
LN_CC_OD=ODread_CC(fpath,OD_correction_function_path)
fpath=[folder_path 'MN_CC_OD.xlsx'];
MN_CC_OD=ODread_CC(fpath,OD_correction_function_path)
fpath=[folder_path 'HN_CC_OD.xlsx'];
HN_CC_OD=ODread_CC(fpath,OD_correction_function_path)

fpath=[folder_path 'NCS_SC_OD.xlsx'];
NCS_SC_OD=ODread_SC_NC(fpath,OD_correction_function_path);

fpath=[folder_path 'NCS_CC_OD.xlsx'];
NCS_CC_OD=ODread_CC_NC(fpath,OD_correction_function_path);

disp("init_OD finished")