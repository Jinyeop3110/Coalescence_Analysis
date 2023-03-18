OD_correction_function_path='/Users/jysong/Desktop/MATLAB/general_functions/OD_correction_function_2202.mat'
folder_path='ExperimentalResult/Data/2208_Coalescence_processed/pH/'

fpath=[folder_path 'LN_SC_pH.xlsx'];
LN_SC_PH=PHread_SC(fpath,OD_correction_function_path)
fpath=[folder_path 'MN_SC_pH.xlsx'];
MN_SC_PH=PHread_SC(fpath,OD_correction_function_path)
fpath=[folder_path 'HN_SC_pH.xlsx'];
HN_SC_PH=PHread_SC(fpath,OD_correction_function_path)

fpath=[folder_path 'LN_CC_pH.xlsx'];
LN_CC_PH=PHread_CC(fpath,OD_correction_function_path)
fpath=[folder_path 'MN_CC_pH.xlsx'];
MN_CC_PH=PHread_CC(fpath,OD_correction_function_path)
fpath=[folder_path 'HN_CC_pH.xlsx'];
HN_CC_PH=PHread_CC(fpath,OD_correction_function_path)

fpath=[folder_path 'NCS_SC_pH.xlsx'];
NCS_SC_PH=PHread_SC_NC(fpath,OD_correction_function_path);

fpath=[folder_path 'NCS_CC_pH.xlsx'];
NCS_CC_PH=PHread_CC_NC(fpath,OD_correction_function_path);

disp("init_PH finished")
