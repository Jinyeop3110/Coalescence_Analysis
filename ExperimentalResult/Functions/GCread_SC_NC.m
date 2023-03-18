%addpath('/Users/jysong/Desktop/MATLAB/GoreLab_new/JY_functions');
%%GRowth Curve

function [Time, Temperature, GC_struct]=GCread_SC_NC(fpath,OD_correction_function_path)

load(OD_correction_function_path)
filename=fpath;
GC_struct=struct;
GC_struct.LN=cell(6,3);
GC_struct.MN=cell(6,3);
GC_struct.HN=cell(6,3);


for ii=1:1
    sheet = ii;
    xlRange = 'B35:MH132';
    subsetA = xlsread(filename,sheet,xlRange);

    Time=subsetA(1,:);
    Tmax=3600*20;
    tirange=1:max(find(Time<Tmax));
    Time=subsetA(1,tirange);
    Temperature=subsetA(2,tirange);
    y=subsetA(3:end,tirange);
    Noise=1.01*min(y,[],1);
    y=y-Noise;
    Data=y;
    y=cell(8,12);
    for i_=1:size(Data,1)
        i=1+floor((i_-1)/12);
        j=i_-12*floor((i_-1)/12);
        y{i,j} = OD_correction_function(Data(i_,:))';
    end

    %% This part depends on arrangement of samples on the plate
    for i=1:6
        for j=1:3
            GC_struct.LN{i,j}=y{i,j};
        end
    end

    for i=1:6
        for j=1:3
            GC_struct.MN{i,j}=y{i,j+3};
        end
    end
    for i=1:6
        for j=1:3
            GC_struct.HN{i,j}=y{i,j+6};
        end
    end
end

end
%
%
% %%
%
% set(0,'defaultAxesFontSize',16)
%
% % subcom_num=16;
% % nutrient_num=3;
% % nutrient_list=["LN","HN","CN"]
% % mix_num=78;
% % data_type=["name", "type", "index", "condition","name(index)", "pH", "OD"]
% % data=struct;
%
%
% %OD
% %work_dir="/Users/jinyeopsong/Desktop/Gore_lab/Exp_Nov_2021/OD"
% file_dir="/Users/jysong/Desktop/Gore_lab/Data/220324_Coalescence_OD/0422_timeseriesOD_80isolates_LN.xlsx";
% %file_dir="/Users/jinyeopsong/Desktop/Gore_lab/Data/220426_124species/0428_timeseries_2S.xlsx";
%
% %files=dir(work_dir+"/*_*_*.xlsx");
% %fullpaths = fullfile({files.folder}, {files.name});
%
%
% filename=file_dir;
%
%
% sheet = 1;
% xlRange = 'B35:MH132';
% subsetA = xlsread(filename,sheet,xlRange);
%
% Time=subsetA(1,:);
% Tmax=3600*20;
% tirange=1:max(find(Time<Tmax));
% Time=subsetA(1,tirange);
% Temperature=subsetA(2,tirange);
% y=subsetA(3:end,tirange);
% Noise=1.01*min(y,[],1);
% y=y-Noise;
% for i=1:size(y,1)
%     y(i,:) = OD_correction_function(y(i,:))';
% end
%
% Community_Number=80;
% Replicate_Number=1;
% Data_indexed=cell(Community_Number,Replicate_Number);
% %% This part depends on arrangement of samples on the plate
% for i=1:10
%     for j=1:8
%         Data_indexed{10*(j-1)+i,1}=y(12*(j-1)+i,:);
%     end
% end
%
%
% %%
% %close all;
% filename="growth_80isolates_LN.mat"
% varname_list=['LN']
% %ccap_list=[ccap.LN; ccap.MN; ccap.HN; ccap.CN]
% growth=struct;
% gr_list=zeros(size(Data_indexed));
%
% figure('Renderer', 'painters', 'Position', [10 10 1200 900])
% for i=1:size(Data_indexed)
%     graph_flag=(i>0 && i<=0+16);
%     if graph_flag
%         subplot(4,4,i-0)
%     end
%     for j=1:Replicate_Number
%         y=Data_indexed{i,j};
%         maxval=max(y);
%         maxval_2=mean(y(find(y>maxval*0.7)));
%         topwindowind=(min(find(y>maxval_2*0.6)));
%         bottomwindowind=max(find(Time<4000));
%
%         x_=Time(bottomwindowind:topwindowind)';
%         y_=log(y(bottomwindowind:topwindowind))';
%         X_=[ones(length(x_),1) x_];
%         b1=X_\y_;
%         yCalc1 = X_*b1;
%         if graph_flag
%             plot(x_,exp(yCalc1),'r');hold on;
%         end
%         growth_rate=b1(2);
%         gr_list(i,j)=growth_rate*3600;
%         if graph_flag
%             plot(Time,y); hold on;
%             line([Time(topwindowind) Time(topwindowind)],[0.01 2]);hold on;
%             line([Time(bottomwindowind) Time(bottomwindowind)],[0.01 2]); hold on;
%             %line([min(tirange) max(tirange)]*Time_interval,[ccap_list(ii,i+22-24*ii) ccap_list(ii,i+22-24*ii)],'Color','red','LineStyle','--
%         end
%
%     end
%     if graph_flag
%         xlabel("Time (h)")
%         ylabel("OD$_{600}$",'interpreter','latex')
%         axis([0 max(Time) 0.02 1.3])
%         grid on
%         set(gca, 'YScale', 'log')
%         title([varname_list ', idx :' int2str(i)])
%
%         xticks([0,  2, 4, 6, 8]*3600)
%         xticklabels({'0','2','4','6','8'})
%     end
% end
%
%
% %save(filename,'growth')
% save(strcat(filename,"_gr_list_type1.mat"),'gr_list')
% saveas(gcf,strcat(filename,"_individuals_plots.png"))
%
%
%
% %%
%
% figure('Renderer', 'painters', 'Position', [10 10 1200 900])
% for i=1:size(Data_indexed)
%     subplot(4,4,i)
%     for j=1:1
%         y=Data_indexed{i,j};
%         window_size=3600;
%         window_interval=600;
%         window_center_pos=window_size/2;
%         while window_center_pos<max(Time)
%             topwindowind=max(find(Time<window_center_pos+window_size/2));
%             bottomwindowind=min(find(Time>window_center_pos-window_size/2));
%             x_=Time(bottomwindowind:topwindowind)';
%             y_=log(y(bottomwindowind:topwindowind))';
%             X_=[ones(length(x_),1) x_];
%             b1=X_\y_;
%             yCalc1 = X_*b1;
%             growth_rate=b1(2)*3600;
%             scatter(window_center_pos,growth_rate,'*','b'); hold on;
%             window_center_pos=window_center_pos+window_interval;
%         end
%         line([0 max(Time)],[gr_list(i,j) gr_list(i,j)],'Color','red','LineStyle','--');hold on;
%         %line([min(tirange) max(tirange)]*Time_interval,[ccap_list(ii,i+22-24*ii) ccap_list(ii,i+22-24*ii)],'Color','red','LineStyle','--')
%
%     end
%     xlabel("Time (h)")
%     ylabel("growth rate$1/h$",'interpreter','latex')
%     axis([0 max(Time) 0 1.3])
%     grid on
%     %set(gca, 'YScale', 'log')
%     title([varname_list ', idx :' int2str(i)])
%
%     xticks([0, 2, 4, 6, 8]*3600)
%     xticklabels({'0','2','4','6','8'})
% end
% saveas(gcf,strcat(filename,"_hourwindow_grfitting_plots.png"))
%
%
% %%
% gr_list_halfreach_max=zeros(size(Data_indexed));
% gr_list_halfreach_min=zeros(size(Data_indexed));
% time_list_halfreach_max=zeros(size(Data_indexed));
% time_list_halfreach_min=zeros(size(Data_indexed));
% ccap=zeros(size(Data_indexed));
%
% for i=1:size(Data_indexed)
%     for j=1:Replicate_Number
%         y=Data_indexed{i,j};
%         minval=mean(y(y<min(y)*1.1));
%         yind=min(find(minval*15<y));
%         if ~isempty(Time(yind))
%             time_list_halfreach_min(i,j)=Time(yind)/3600;
%             gr_list_halfreach_min(i,j)=log(15)/time_list_halfreach_min(i,j);
%         end
%         %
%
%         maxval=mean(y(y>max(y)*0.95));
%         yind=max(find(maxval/2>y));
%         if ~isempty(Time(yind))
%             time_list_halfreach_max(i,j)=Time(yind)/3600;
%             gr_list_halfreach_max(i,j)=log(15)/time_list_halfreach_max(i,j);
%         end
%
%         ccap(i,j)=mean(y(y>max(y)*0.95));
%
%     end
%
% end
% % figure('Renderer', 'painters', 'Position', [10 10 1200 900])
% % scatter(mean(gr_list,2),mean(gr_list_halfreach_min,2),'*','blue');hold on;
% % scatter(mean(gr_list,2),mean(gr_list_halfreach_max,2),'*','red');hold on;
% % scatter(mean(gr_list,2),mean((gr_list_halfreach_min+gr_list_halfreach_max)/2,2),'*','black');hold on;
% % xlabel("gr $1/h$",'interpreter','latex')
% % ylabel("gr ** $1/h$",'interpreter','latex')
% % axis([0.5 1.1 0.5 1.1])
% % grid on
% % gr_list_type3=(gr_list_halfreach_max)
% % mean(gr_list_type3)
% % sqrt(var(gr_list_type3))
%
% save(strcat(filename,"_gr_list_type2.mat"),'gr_list_halfreach_min','gr_list_halfreach_max')
% save(strcat(filename,"_ccap_fromTimeseries.mat"),'ccap')
%

