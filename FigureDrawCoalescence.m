%%
set(0,'defaultAxesFontSize',25)
session_name="Drawings"

if ~isfolder(cd+"/"+session_name)
    mkdir(cd+"/"+session_name)
end



%% Figure 1
% ASVs detected 


%% Defining the Synthetic IDX
Mediums=["LN", "MN", "HN"];
Species_pools=[6, 12, 24];
Synthetic_IDX.LN_6=CommunityPermutate_withSpeciesPoolsize("F","S", "L", "C",6);
Synthetic_IDX.LN_12=CommunityPermutate_withSpeciesPoolsize("F","S", "L", "C",12);
Synthetic_IDX.LN_24=CommunityPermutate_withSpeciesPoolsize("F","S", "L", "C",24);
Synthetic_IDX.MN_6=CommunityPermutate_withSpeciesPoolsize("F","S", "M", "C",6);
Synthetic_IDX.MN_12=CommunityPermutate_withSpeciesPoolsize("F","S", "M", "C",12);
Synthetic_IDX.MN_24=CommunityPermutate_withSpeciesPoolsize("F","S", "M", "C",24);
Synthetic_IDX.HN_6=CommunityPermutate_withSpeciesPoolsize("F", "S", "H", "C",6);
Synthetic_IDX.HN_12=CommunityPermutate_withSpeciesPoolsize("F", "S", "H", "C",12);
Synthetic_IDX.HN_24=CommunityPermutate_withSpeciesPoolsize("F", "S", "H", "C",24);
%%
getIDX(Coalescence_data,IDX)
cellfun(@(x) getIDX(Coalescence_data,x),string(Synthetic_IDX.HN_24))
%% Figure 2
% Basing thing : Additivity by Species number and mediums
%Community_data
%Coalescence_data


figure('Renderer', 'painters', 'Position', [10 10 900 700])
data_list=[];
type_list=[];
Variable2plot="Assymetricity1_1"
Name2show=Variable2plot


for j=1:3
    for i=1:3
        M=Mediums(i);
        S=Species_pools(j);
        type=M+'_'+S;
        IDX=cellfun(@(x) getIDX(Coalescence_data,x),string(Synthetic_IDX.(type)));
        data=Coalescence_data(IDX,:).(Variable2plot);
        data_list=[data_list; data];
        type_list=[type_list; repmat(type,length(data),1)];
    end
end



daynames = ["LN_6" "LN_12" "LN_24" "MN_6" "MN_12" "MN_24" "HN_6" "HN_12" "HN_24"];
x = categorical(type_list,daynames);
y = data_list;
C=colororder;
vs = violinplot(y, x,'QuartileStyle','shadow','ViolinAlpha',0.2,'MarkerSize',100,'ShowData',false,'ShowBox', false, 'ShowMean', true, 'QuartileStyle','boxplot');
hold on
%swarmchart(x,y,'filled','MarkerFaceAlpha',0.5,'MarkerEdgeAlpha',0.5);
%boxplot(data,cellstr(type))
%scat
hold on

ylabel(Variable2plot)

h=get(gca,'xlabel')
set(h, 'FontSize', 10) 
%title("Assymetricity / Uniform")




%%



%% Coalesced community
ID_list=[CommunityPermutate("F","S", "L", "C"); CommunityPermutate("F","S", "M", "C"); CommunityPermutate("F","S", "H", "C")];
T=table;
for idx=1:size(ID_list,1)
    disp(ID_list(idx,:));
    ID=ID_list(idx,:);
    S=GetCommunity(ID);
    [S1,S2]=GetSubcommunities(ID);
    A=GetAbundance(S);
    A1=GetAbundance(S1);
    A2=GetAbundance(S2);

    S.CommunityIDX=string(S.CommunityIDX);
    T_toadd=S;
    threshold=1e-3;
    %T_toadd.SampleIDX= S.SampleIDX;
    T_toadd.SampleIDX_Sub1= S1.SampleIDX;
    T_toadd.SampleIDX_Sub2= S2.SampleIDX;

    T_toadd.Diversity1=Diversity1(A,threshold);
    T_toadd.Diversity2=Diversity2(A,threshold);
    T_toadd.Diversity3=Diversity3(A,threshold);
    T_toadd.Additivity1=Additivity1(A,A1,A2,threshold);
    T_toadd.Additivity2=Additivity2(A,A1,A2,threshold);

    T_toadd.Overalp=Overalp(A,A1,A2,threshold);
    T_toadd.Assymetricity1=Assymetricity1(A,A1,A2,threshold);
    T_toadd.Assymetricity2=Assymetricity2(A,A1,A2,threshold);

    %idx=find((Metadata.Timepoint==Timepoint).*(Metadata.CommunityOrigin==CommunityOrigin).*(Metadata.Medium==Medium).*(Metadata.CoalescenceType==CoalescenceType));
    %O=cell2mat(Metadata.SampleIDX(idx,:))  
    T=[T; struct2table(T_toadd)];

end


filename = session_name +'/ CoalescenceAnalyzed_Synthetic.xlsx';
writetable(T,filename,'Sheet',1);



%%
function O= getIDX(Coalescence_data,IDX)
     O=find(cellfun(@(x) strcmp(x,IDX), Coalescence_data.SampleIDX))
end

function O=CommunityPermutate(Timepoint,CommunityOrigin, Medium, CoalescenceType)
    global Metadata
    idx=find((Metadata.Timepoint==Timepoint).*(Metadata.CommunityOrigin==CommunityOrigin).*(Metadata.Medium==Medium).*(Metadata.CoalescenceType==CoalescenceType));
    O=cell2mat(Metadata.SampleIDX(idx,:))  
end

function O=CommunityPermutate_withSpeciesPoolsize(Timepoint,CommunityOrigin, Medium, CoalescenceType,species_pool_num)
    global Metadata
    idx=(Metadata.Timepoint==Timepoint).*(Metadata.CommunityOrigin==CommunityOrigin).*(Metadata.Medium==Medium).*(Metadata.CoalescenceType==CoalescenceType);
    
    communityIDX=cellfun(@str2num, Metadata.CommunityIDX);
    if CoalescenceType=='S'
        if species_pool_num==6
            idx=idx.*(communityIDX<=9)
        elseif species_pool_num==12
            idx=idx.*(communityIDX>9 & communityIDX<=18)
        elseif species_pool_num==24
            idx=idx.*(communityIDX>18 & communityIDX<=30)
        end
    elseif  CoalescenceType=='C'
        if species_pool_num==6
            idx=idx.*(communityIDX<=14)
        elseif species_pool_num==12
            idx=idx.*(communityIDX>14 & communityIDX<=41)
        elseif species_pool_num==24
            idx=idx.*(communityIDX>41 & communityIDX<=47)
        end            
    end
    
    O=cell2mat(Metadata.SampleIDX(find(idx),:))  
end


function O=Diversity1(A,threshold)
    O=sum(A>threshold);
end

function O=Diversity2(A,threshold)
    O=-sum(A.*log(A+1e-6));
end

function O=Diversity3(A,threshold)
    if sum(A)<0.9
        O=0;
    else
        O=1/sum(A.^2);
    end
end


function O=Additivity1(A,A1,A2,threshold)
    O=sum(A>threshold)/(sum(A1>threshold)+sum(A2>threshold));
end

function O=Additivity2(A,A1,A2,threshold)
    % BAsed on diversity3
    O=Diversity3(A,threshold)-(Diversity3(A1,threshold)+Diversity3(A2,threshold))/2;
end


function O=Overalp(A,A1,A2,threshold)
    O=sum(A.*(A1>threshold).*(A2>threshold));
end

function O=Assymetricity1(A,A1,A2,threshold)
    O=sum(A.*(A1>threshold)-A.*(A2>threshold))/sum(A.*(A1>threshold)+A.*(A2>threshold)-(A.*(A1>threshold).*(A2>threshold)));
    O=abs(O);
end

function O=Assymetricity2(A,A1,A2,threshold)
    O=sum(sign(A.*(A1>threshold)-A.*(A2>threshold)))/sum(sign(A.*(A1>threshold)+A.*(A2>threshold)));
    O=abs(O);

end

function [c] = appendStruct(a,b)
%APPENDSTRUCT Appends two structures ignoring duplicates
%   Developed to append two structs while handling cases of non-unique
%   fieldnames.  The default keeps the last occurance of the duplicates in
%   the appended structure.
    ab = [struct2cell(a); struct2cell(b)];
    abNames = [fieldnames(a); fieldnames(b)];
    [~,iab] = unique(abNames,'last');
    c = cell2struct(ab(iab),abNames(iab));
end


function T=makeTable(T,A,B)
    fn = fieldnames(A);
    
    for i = 1:numel(fn)
        fni = string(fn(i));
        fieldA = A.(fni);
        fieldB = B.(fni);

        T=assignin(T, fni, fieldA,fieldB);
    end
end

function T=assignin(T, fni, fieldA, fieldB)
    Samplename="P"+string(fieldA')+"-"+arrayfun(@(x) sprintf('%02d',x), fieldB', 'UniformOutput', false);
    IDX=100*fieldA'+fieldB';
    Type={}
    Type(1:length(fieldA),1)={fni};
    CommunityIDX=(1:length(fieldA))';

    T_toadd=[array2table(Samplename), array2table(IDX), cell2table(Type), array2table(CommunityIDX)]
    T=[T; T_toadd]
end

%%
function O=ParseDescription(description)
    global Metadata

    %Example of description

    parsed= split(description,'_');
    idx=(Metadata.Timepoint==parsed(1)) ...
    & (Metadata.CommunityOrigin==parsed(2)) ...
    & (Metadata.Medium==parsed(3)) ...
    & (Metadata.CoalescenceType==parsed(4)) ...
    & (Metadata.Replicate==parsed(5)) ...
    & (Metadata.CommunityIDX==parsed(6));

    O=table2struct(Metadata(idx,:));
end

function O=getDescription(T)
    O=string(T.Timepoint)+'_'+string(T.CommunityOrigin)+'_'+string(T.Medium)+'_'+string(T.CoalescenceType)+'_'+string(T.Replicate)+'_'+string(T.CommunityIDX);

end

function O=GetAbundance(S)
    global ProcessedSeq

    SampleIdx=S.SampleIDX;
    idx=find(ProcessedSeq.SampleIdx==string(SampleIdx));
    if isempty(idx)
        O=ProcessedSeq(1,:);
        O=zeros(size(table2array(O(1,2:end))));

    else
        O=ProcessedSeq(idx,:);
        O=table2array(O(1,2:end));
    end
end

function S=GetCommunity(SampleIdx)
    global Metadata

    idx=(Metadata.SampleIDX==string(SampleIdx));
    S=table2struct(Metadata(idx,:));
    
end

function [S1,S2]=GetSubcommunities(SampleIdx)
    global Metadata

    idx=(Metadata.SampleIDX==string(SampleIdx));
    O=table2struct(Metadata(idx,:));
    description=getDescription(O);
    parsed= split(description,'_')'

    if parsed(4) ~= "C"
        error("Sample ID : "+SampleIdx + " is not Coalesced community")
    end
    %disp(O)
    coalidx=str2num(O.CommunityIDX);
    %disp(coalidx)
    [sidx1, sidx2]=CoalIdx2SubIdxs(coalidx);
    disp(sidx1);disp(sidx2)
    O1=O;
    O1.CoalescenceType='S';
    O1.CommunityIDX=char(string(sidx1));
    disp(getDescription(O1))
    S1= ParseDescription(getDescription(O1));

    O2=O;
    O2.CoalescenceType='S';
    O2.CommunityIDX=char(string(sidx2));
    S2= ParseDescription(getDescription(O2));
end


function [A,B]=CoalIdx2SubIdxs(coalidx)
    global CoalRecipe
    idx=find(CoalRecipe.CommunityIDX_Coal==coalidx);
    disp(idx)
    A=CoalRecipe.CommunityIDX_Sub1(idx);
    B=CoalRecipe.CommunityIDX_Sub2(idx);
end

function CalculateSimilarities(Ab1,Ab2)
    
end

function CalculateAssymetricity(Ab1,Ab2)
    
end
%






