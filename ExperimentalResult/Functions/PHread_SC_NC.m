%addpath('/Users/jysong/Desktop/MATLAB/GoreLab_new/JY_functions');

function PH_struct=PHread_SC_NC(fpath,OD_correction_function_path,index)
    load(OD_correction_function_path)
    filename=fpath;
    PH_struct=struct;
    PH_struct.LN=zeros(6,3,7);
    PH_struct.MN=zeros(6,3,7);
    PH_struct.HN=zeros(6,3,7);

    for ii=1:7
        sheet = ii;
        xlRange = 'B25:M32';
        subsetA = xlsread(filename,sheet,xlRange);
        disp("open filedir ")
        
        y=subsetA/10;

    %% This part depends on arrangement of samples on the plate
        for i=1:6
            for j=1:3
                PH_struct.LN(i,j,ii)=y(i,j);
            end
        end

        for i=1:6
            for j=1:3
                PH_struct.MN(i,j,ii)=y(i,j+3);
            end
                end
        for i=1:6
            for j=1:3
                PH_struct.HN(i,j,ii)=y(i,j+6);
            end
        end
    end
end
