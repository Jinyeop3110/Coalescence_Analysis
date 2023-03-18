%addpath('/Users/jysong/Desktop/MATLAB/GoreLab_new/JY_functions');

function PH_struct=ODread_CC_NC(fpath,OD_correction_function_path,index)
load(OD_correction_function_path)
filename=fpath;
PH_struct=struct;
PH_struct.LN=zeros(15,2,7);
PH_struct.MN=zeros(15,2,7);
PH_struct.HN=zeros(15,2,7);

for ii=1:7
    sheet = ii;
    xlRange = 'B25:M32';
    subsetA = xlsread(filename,sheet,xlRange);
    disp("open filedir ")

    y=subsetA/10;

    %% This part depends on arrangement of samples on the plate
    for i=1:15
        if i<=8
            i_=i;
            j_=1;
        else
            i_=i-8;
            j_=2;
        end

        PH_struct.LN(i,1,ii)=y(i_,j_);
        PH_struct.LN(i,2,ii)=y(i_,j_+2);

    end

    for i=1:15
        if i<=8
            i_=i;
            j_=1;
        else
            i_=i-8;
            j_=2;
        end

        PH_struct.MN(i,1,ii)=y(i_,j_+4);
        PH_struct.MN(i,2,ii)=y(i_,j_+6);

    end

    for i=1:15
        if i<=8
            i_=i;
            j_=1;
        else
            i_=i-8;
            j_=2;
        end

        PH_struct.HN(i,1,ii)=y(i_,j_+8);
        PH_struct.HN(i,2,ii)=y(i_,j_+10);

    end

end
end
