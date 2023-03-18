%% Load
addpath(genpath('..'));
set(0,'defaultAxesFontSize',22)

run('init_PH.m')
run('init_OD.m')
run('init_GC.m')
run('init_CC_idx.m')

%% community time series


%% SC time-series, MN
figure('Renderer', 'painters', 'Position', [10 10 900 700])
Legend=[];
c_code=colororder;

%
[p_OD_list, p_PH_list,f_list]=FluctuationInference(Merge(MN_SC_OD),Merge(MN_SC_PH),0.25,0.5)

data_pH=FinalDay(MN_SC_PH)
data_OD=FinalDay(MN_SC_OD)
Plot_pHvOD(data_pH(logical(1-f_list)),data_OD(logical(1-f_list)),c_code(1,:),"Stable"); hold on;
Plot_pHvOD(data_pH(f_list),data_OD(f_list),c_code(2,:),"Fluctuating"); hold on;

% data_pH=FinalDay(MN_CC_PH)
% data_OD=FinalDay(MN_CC_OD)
% Plot_pHvOD(data_pH,data_OD,c_code(2,:),"MN CC")

f=get(gca,'Children');
legend()

xlabel('pH','Interpreter','latex')
ylabel('OD600','Interpreter','latex')
axis([3 10 0 2.0])
title("daily OD / MN")

%% SC time-series, HN
figure('Renderer', 'painters', 'Position', [10 10 900 700])
Legend=[];
c_code=colororder;

%
[p_OD_list, p_PH_list,f_list]=FluctuationInference(Merge(HN_SC_OD),Merge(HN_SC_PH),0.25,0.5)

data_pH=FinalDay(HN_SC_PH)
data_OD=FinalDay(HN_SC_OD)
Plot_pHvOD(data_pH(logical(1-f_list)),data_OD(logical(1-f_list)),c_code(1,:),"Stable"); hold on;
Plot_pHvOD(data_pH(f_list),data_OD(f_list),c_code(2,:),"Fluctuating"); hold on;

% data_pH=FinalDay(MN_CC_PH)
% data_OD=FinalDay(MN_CC_OD)
% Plot_pHvOD(data_pH,data_OD,c_code(2,:),"MN CC")

f=get(gca,'Children');
legend()

xlabel('pH','Interpreter','latex')
ylabel('OD600','Interpreter','latex')
axis([3 10 0 2.0])
title("daily OD / HN")

%%
function output=FinalDay(input)
hold on
output=[]
temp=input.s6(:,:,end);
output=[output; temp(:)]
temp=input.s12(:,:,end);
output=[output; temp(:)]
temp=input.s24(:,:,end);
output=[output; temp(:)]
end


function Plot_pHvOD(data_pH,data_OD,color,dispname)
hold on

scatter(data_pH,data_OD,'filled','MarkerFaceColor',color,'DisplayName',dispname)
hold off
end

%%
function Plot_7daysTimeseries(data,color,dispname)
hold on
data=reshape(data,[],7);
for i=1:size(data,1)
    plot(1:7,data(i,:),'Color',color,'DisplayName',dispname);
end
hold off
end

function Plot_7daysTimeseries_FluctuationInference(data,f_list, color_list,dispname_list)
hold on
data=reshape(data,[],7);
for i=1:size(data,1)
    plot(1:7,data(i,:),'Color',color_list(f_list(i)+1,:),'DisplayName',dispname_list(f_list(i)+1));
end
hold off
end


function [p_OD_list, p_PH_list, f_list]=FluctuationInference(ODdata, PHdata, ODthreshold, PHthreshold)
ODdata=reshape(ODdata,[],7);

p_OD_list=arrayfun(@(x) isODFluctuation(ODdata(x,:)), 1:size(ODdata,1));
p_PH_list=arrayfun(@(x) isPHFluctuation(PHdata(x,:)), 1:size(ODdata,1));

f_list=((p_OD_list>ODthreshold)+(p_PH_list>PHthreshold))>0;
end

function p=isODFluctuation(dailyOD)
p=std(dailyOD(5:7))/mean(dailyOD(5:7));
end

function p=isPHFluctuation(dailyPH)
p=max(dailyPH(5:7))-min(dailyPH(5:7));
end


function output=Merge(input)
    output=[];
    temp=reshape(input.s6,[],7);
    output=[output; temp]
    temp=reshape(input.s12,[],7);
    output=[output; temp]
    temp=reshape(input.s24,[],7);
    output=[output; temp]
end


