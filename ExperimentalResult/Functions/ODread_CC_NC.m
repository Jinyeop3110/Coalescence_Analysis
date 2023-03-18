%addpath('/Users/jysong/Desktop/MATLAB/GoreLab_new/JY_functions');

function OD_struct=ODread_CC_NC(fpath,OD_correction_function_path,index)
load(OD_correction_function_path)
filename=fpath;
OD_struct=struct;
OD_struct.LN=zeros(15,2,7);
OD_struct.MN=zeros(15,2,7);
OD_struct.HN=zeros(15,2,7);

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
    for i=1:15
        if i<=8
            i_=i;
            j_=1;
        else
            i_=i-8;
            j_=2;
        end

        OD_struct.LN(i,1,ii)=y(i_,j_);
        OD_struct.LN(i,2,ii)=y(i_,j_+2);

    end

    for i=1:15
        if i<=8
            i_=i;
            j_=1;
        else
            i_=i-8;
            j_=2;
        end

        OD_struct.MN(i,1,ii)=y(i_,j_+4);
        OD_struct.MN(i,2,ii)=y(i_,j_+6);

    end

    for i=1:15
        if i<=8
            i_=i;
            j_=1;
        else
            i_=i-8;
            j_=2;
        end

        OD_struct.HN(i,1,ii)=y(i_,j_+8);
        OD_struct.HN(i,2,ii)=y(i_,j_+10);

    end

end
end
