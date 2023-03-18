function [gr_type1,gr_type2, gr_type3] = GRcalculate(ODt,Time)
set(0,'defaultAxesFontSize',16)


maxval=max(ODt);
maxval_2=mean(ODt(find(ODt>maxval*0.9)));
topwindowind=(min(find(ODt>maxval_2*0.8)));
bottomwindowind=max(find(Time<2000));

x_=Time(bottomwindowind:topwindowind)';
y_=log(ODt(bottomwindowind:topwindowind))';
X_=[ones(length(x_),1) x_];
b1=X_\y_;
yCalc1 = X_*b1;

growth_rate=b1(2);
gr_type1=growth_rate*3600;



minval=mean(ODt(ODt<min(ODt)*1.1));
yind=min(find(minval*15<ODt));
time_list_halfreach_min=Time(yind)/3600;
if isempty(time_list_halfreach_min)
    gr_type2=0;
else
    gr_type2=log(15)/time_list_halfreach_min;
end

maxval=mean(ODt(ODt>max(ODt)*0.90));
yind=max(find(maxval/2>ODt));
time_list_halfreach_max=Time(yind)/3600;
if isempty(time_list_halfreach_max)
    gr_type3=0;
else
    gr_type3=log(15)/time_list_halfreach_max;
end




end

