%addpath('/Users/jysong/Desktop/MATLAB/GoreLab_new/JY_functions');

function OD_struct=ODread_SC_NC(fpath,OD_correction_function_path,index)
    load(OD_correction_function_path)
    filename=fpath;
    OD_struct=struct;
    OD_struct.LN=zeros(6,3,7);
    OD_struct.MN=zeros(6,3,7);
    OD_struct.HN=zeros(6,3,7);

    for ii=1:7
        sheet = ii;
        xlRange = 'B25:M32';
        subsetA = xlsread(filename,sheet,xlRange);
        disp("open filedir ")
    
        y=subsetA;
        Noise=mean(y(y<1.05*min(y(:))));
        y=y-Noise;
        
        for i=1:size(y,1)
        y(i,:) = OD_correction_function(y(i,:))';
        end
    
        Community_Number=16;
        Replicate_Number=3;
    %% This part depends on arrangement of samples on the plate
        for i=1:6
            for j=1:3
                OD_struct.LN(i,j,ii)=y(i,j);
            end
        end

        for i=1:6
            for j=1:3
                OD_struct.MN(i,j,ii)=y(i,j+3);
            end
                end
        for i=1:6
            for j=1:3
                OD_struct.HN(i,j,ii)=y(i,j+6);
            end
        end
    end
end
