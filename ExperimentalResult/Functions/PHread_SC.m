%addpath('/Users/jysong/Desktop/MATLAB/GoreLab_new/JY_functions');

function OD_struct=ODread_SC(fpath,OD_correction_function_path,index)
    load(OD_correction_function_path)
    filename=fpath;
    OD_struct=struct;
    OD_struct.s6=zeros(9,2,7);
    OD_struct.s12=zeros(9,2,7);
    OD_struct.s24=zeros(12,2,7);

    for ii=1:7
        sheet = ii;
        xlRange = 'B25:M32';
        subsetA = xlsread(filename,sheet,xlRange);
        disp("open filedir ")
    
        y=subsetA/10;
        
    %% This part depends on arrangement of samples on the plate
        for i=1:9
            for j=1:2
                OD_struct.s6(i,j,ii)=y(j,i);
            end
        end

        for i=1:9
            for j=1:2
                OD_struct.s12(i,j,ii)=y(j+3,i);
            end
                end
        for i=1:12
            for j=1:2
                OD_struct.s24(i,j,ii)=y(j+6,i);
            end
        end
    end
end
