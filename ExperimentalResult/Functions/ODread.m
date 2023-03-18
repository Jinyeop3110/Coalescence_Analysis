addpath('/Users/jysong/Desktop/MATLAB/GoreLab_new/JY_functions');

function Data_indexed=ODread(file_dir,OD_correction_function_path)
    load(OD_correction_function_path)
    filename=file_dir;
    sheet = 1;
    xlRange = 'B25:M32';
    subsetA = xlsread(filename,sheet,xlRange);
    disp("open filedir ")

    y=subsetA/10;
    Noise=mean(y(y<1.05*min(y(:))));
    y=y-Noise;
    
    for i=1:size(y,1)
    y(i,:) = OD_correction_function(y(i,:))';
    end

    Community_Number=16;
    Replicate_Number=3;
    Data_indexed=cell(Community_Number,Replicate_Number);
    %% This part depends on arrangement of samples on the plate
    for i=1:12
        for j=1:3
            Data_indexed{i,j}=mean(y(j,i));
        end
    end

    for i=13:16
        for j=1:3
            Data_indexed{i,j}=mean(y(j+4,i-12));
        end
    end
end
