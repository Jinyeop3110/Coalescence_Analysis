%%
set(0,'defaultAxesFontSize',25)
session_name="Analyzed"

if ~isfolder(cd+"/"+session_name)
    mkdir(cd+"/"+session_name)
end

%%
%% Generate indexes
global ProcessedSeq Metadata CoalRecipe ProcessedSim

%% communities

ID_list=CommunityPermutate_Sim();

T=table;
for id_i=1:size(ID_list,1)
    disp(ID_list(id_i,:));
    T_toadd=struct;
    ID=ID_list(id_i,:);
    ProS=ProcessedSim(id_i,:);
    T_toadd.SampleIDX=ProS.SampleIDX;
    T_toadd.CommunityIDX=ProS.CommunityIDX;
    T_toadd.Max_S=ProS.Max_S;
    T_toadd.S=ProS.S;
    T_toadd.I=ProS.I;
    A=GetCommunity_Sim(ProS,'x3');
    A1=GetCommunity_Sim(ProS,'x1');
    A2=GetCommunity_Sim(ProS,'x2');

    Threshold_level=[0.1, 0.033, 0.01, 0.0033, 0.001];
    T_toadd.Threshold_num=length(Threshold_level);

    for i=1:T_toadd.Threshold_num
        threshold=Threshold_level(i);
        T_toadd.("Threshold_level_"+string(i))=threshold;
        
        T_toadd.("SimilarityTo1_BC_"+string(i))=SimilarityTo1(A,A1,A2,threshold,@SimilarityBC);
        T_toadd.("SimilarityTo1_J_"+string(i))=SimilarityTo1(A,A1,A2,threshold,@SimilarityJ);
        T_toadd.("SimilarityTo1_JS_"+string(i))=SimilarityTo1(A,A1,A2,threshold,@SimilarityJS);
        T_toadd.("SimilarityTo2_BC_" + string(i)) = SimilarityTo2(A, A1, A2, threshold, @SimilarityBC);
        T_toadd.("SimilarityTo2_J_" + string(i)) = SimilarityTo2(A, A1, A2, threshold, @SimilarityJ);
        T_toadd.("SimilarityTo2_JS_" + string(i)) = SimilarityTo2(A, A1, A2, threshold, @SimilarityJS);
                    
        T_toadd.("Additivity1_" + string(i)) = Additivity1(A, A1, A2, threshold);
        T_toadd.("Additivity2_" + string(i)) = Additivity2(A, A1, A2, threshold);
        T_toadd.("Additivity3_" + string(i)) = Additivity3(A, A1, A2, threshold);
        
        T_toadd.("Assymetricity_BC_" + string(i)) = Assymetricity_basedOnSimilarity(A, A1, A2, threshold, @SimilarityBC);
        T_toadd.("Assymetricity_J_" + string(i)) = Assymetricity_basedOnSimilarity(A, A1, A2, threshold, @SimilarityJ);
        T_toadd.("Assymetricity_JS_" + string(i)) = Assymetricity_basedOnSimilarity(A, A1, A2, threshold, @SimilarityJS);
        T_toadd.("Assymetricity1_" + string(i)) = Assymetricity1(A, A1, A2, threshold);
        T_toadd.("Assymetricity2_" + string(i)) = Assymetricity2(A, A1, A2, threshold);
        T_toadd.("Assymetricity3_" + string(i)) = Assymetricity3(A, A1, A2, threshold);


        T_toadd.("ASVs_notinsub1_"+string(i))=ASVs_fraction_notinsub1(A, A1, A2, threshold);
        T_toadd.("ASVs_notinsub2_"+string(i))=ASVs_fraction_notinsub2(A, A1, A2, threshold);
        T_toadd.("ASVs_overlap1_"+string(i))=ASVs_fraction_overlap1(A, A1, A2, threshold);
        T_toadd.("ASVs_overlap2_"+string(i))=ASVs_fraction_overlap2(A, A1, A2, threshold);
        %idx=find((Metadata.Timepoint==Timepoint).*(Metadata.CommunityOrigin==CommunityOrigin).*(Metadata.Medium==Medium).*(Metadata.CoalescenceType==CoalescenceType));
        %O=cell2mat(Metadata.SampleIDX(idx,:))
    end

    T=[T; struct2table(T_toadd)];

end


filename = session_name +['/processed_CoalescenceEvent_simulation.xlsx'];
writetable(T,filename,'Sheet',1);


%%





%%
function O=GetCommunity_Sim(ProS,type)
    idx=contains(ProS.Properties.VariableNames,type);
    O=table2array(ProS(1,idx));
end


function O=CommunityPermutate_Sim()
    global ProcessedSim
    O=cell2mat(ProcessedSim.SampleIDX);
end

%%

function O=CommunityPermutate(Timepoint,CommunityOrigin, Medium, CoalescenceType)
    global Metadata
    idx=find((Metadata.Timepoint==Timepoint).*(Metadata.CommunityOrigin==CommunityOrigin).*(Metadata.Medium==Medium).*(Metadata.CoalescenceType==CoalescenceType));
    O=cell2mat(Metadata.SampleIDX(idx,:))  
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

function O=SimilarityBC(A,B,threshold)
    % BAsed on richness
    O=sum(min(A,B));
end

function O=SimilarityJS(A,B,threshold)
    % BAsed on richness
    A_=A+1e-10;
    B_=B+1e-10;
    x=(A_+B_)/2;
    O=1-sqrt(0.5*sum(A_.*(log(A_)-log(x)))+0.5*sum(B_.*(log(B_)-log(x))));
    
end

function O=SimilarityJ(A,B,threshold)
    % BAsed on richness
    O=sum((A>threshold) & (B>threshold))/sum((A>threshold) | (B>threshold));
end

function O=SimilarityTo1(A,A1,A2,threshold,f_similarity)
    % BAsed on richness
    O=f_similarity(A,A1,threshold)/(f_similarity(A,A1,threshold)+f_similarity(A,A2,threshold));
end

function O=SimilarityTo2(A,A1,A2,threshold,f_similarity)
    % BAsed on richness
    O=f_similarity(A,A2,threshold)/(f_similarity(A,A1,threshold)+f_similarity(A,A2,threshold));
end

function O=Additivity1(A,A1,A2,threshold)
    % BAsed on richness
    O=sum(A>threshold)/(sum(A1>threshold)+sum(A2>threshold)-sum((A1>threshold).*(A2>threshold)));
end

function O=Additivity2(A,A1,A2,threshold)
    % BAsed on richness
    O=sum((A>threshold).*((A1>threshold) | (A2>threshold)))/(sum((A1>threshold) | (A2>threshold)));
end

function O=Additivity3(A,A1,A2,threshold)
    % BAsed on richness
    O=sum((A>threshold).*((A1>threshold) | (A2>threshold)))/(sum(A1>threshold)+sum(A2>threshold));
end

function O=ASVs_fraction_notinsub1(A,A1,A2,threshold)
    O=sum(A.*(1-((A1>threshold)|(A2>threshold)))>threshold)/(sum(A>threshold)+1e-10);
end

function O=ASVs_fraction_notinsub2(A,A1,A2,threshold)
    O=sum(A.*(1-((A1>threshold)|(A2>threshold))));
end

function O=ASVs_fraction_overlap1(A,A1,A2,threshold)
    O=sum((A.*(A1>threshold).*(A2>threshold))>threshold)/(sum(A>threshold)+1e-10);
end

function O=ASVs_fraction_overlap2(A,A1,A2,threshold)
    O=sum(A.*(A1>threshold).*(A2>threshold));
end


function O=Assymetricity_basedOnSimilarity(A,A1,A2,threshold,f_similarity)
    O=2*abs(f_similarity(A,A1,threshold)/(f_similarity(A,A1,threshold)+f_similarity(A,A2,threshold))-0.5);
end


function O=Assymetricity1(A,A1,A2,threshold)
    O=sum(sign(A.*(A1>threshold)-A.*(A2>threshold)))/sum(sign(A.*(A1>threshold)+A.*(A2>threshold)));
    O=abs(O);

end

function O=Assymetricity2(A,A1,A2,threshold)
    O=sum(A.*(A1>threshold)-A.*(A2>threshold))/sum(A.*(A1>threshold)+A.*(A2>threshold)-(A.*(A1>threshold).*(A2>threshold)));
    O=abs(O);
end

function O=Assymetricity3(A,A1,A2,threshold)
    O=sum(A.*(A1>threshold)-A.*(A2>threshold))/sum(A.*(A1>threshold)+A.*(A2>threshold)-2*(A.*(A1>threshold).*(A2>threshold)));
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
    idx=find(ProcessedSeq.SampleIDX==string(SampleIdx));
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


end



