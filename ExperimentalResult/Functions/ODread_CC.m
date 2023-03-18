%addpath('/Users/jysong/Desktop/MATLAB/GoreLab_new/JY_functions');

function OD_struct=ODread_CC(fpath,OD_correction_function_path,index)
load(OD_correction_function_path)
filename=fpath;
OD_struct=struct;

OD_struct.s6=zeros(14,2,7);
OD_struct.s12=zeros(27,2,7);
OD_struct.s24=zeros(6,2,7);

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
    for i=1:14
        i_=i-12*floor((i-1)/12);
        j_=1+floor((i-1)/12);
        OD_struct.s6(i,1,ii)=y(j_,i_);
        OD_struct.s6(i,2,ii)=y(9-j_,13-i_);
    end

    for i=1:27
        i_=i+14-12*floor((i+14-1)/12);
        j_=1+floor((i+14-1)/12);

        OD_struct.s12(i,1,ii)=y(j_,i_);
        OD_struct.s12(i,2,ii)=y(9-j_,13-i_);
    end


    for i=1:6
        i_=i+42-12*floor((i+42-1)/12);
        j_=1+floor((i+42-1)/12);

        OD_struct.s24(i,1,ii)=y(j_,i_);
        OD_struct.s24(i,2,ii)=y(9-j_,13-i_);
    end


end
end
