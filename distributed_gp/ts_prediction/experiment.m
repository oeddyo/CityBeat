clear
%data = load('instagram_20min.csv');
data = load('instagram_ts_by_20min.csv');
%data = [[1:1:300]', rand([300,1])]




idx = data(:,2)>0;
data = data( idx,:);


tic
size(data)
nPeople = data(:, 2);
day = data(:, 1);

cutoff = 8
x = day(day<cutoff); y = nPeople(day<cutoff);
xx = day(day>cutoff); yy = nPeople(day>cutoff);

k1 = @covSEiso;        %2             % covariance contributions, long term trend
k2 = {@covProd, {@covPeriodic, @covSEisoU}};    %3, 1  % close to periodic component
k3 = @covRQiso;             % 3        % fluctations with different length-scales
k4 = @covSEiso;              %2   % very short term (month to month) correlations 
k5 = @covNoise;             %1
%covfunc = {@covSum, {k1, k2, k3, k4}};                % add up covariance terms
covfunc = {@covSum, {k1, k2, k3, k4,k5}};                % add up covariance terms

hyp.cov = [4 4 0 0 1 4 0 0 -1 -2 -2 0]; hyp.lik = -2;               % init hypers


[hyp,fX,i] = minimize(hyp, @gp, -500, @infExact, [], covfunc, @likGauss, x, y-mean(y));

zz = (cutoff+1/24:1/72:cutoff+10)';

[mu s2] = gp(hyp, @infExact, [], covfunc, @likGauss, x, y-mean(y), zz);

choice = 0

if choice==0
    f = [mu+sqrt(s2); flipdim(mu-3*sqrt(s2),1)] + mean(y);
    fill([zz; flipdim(zz,1)], f, [7 7 7]/8); hold on;           % show predictions
    plot(x,y,'b'); plot(xx,yy,'r-') ;plot(zz,mu+mean(y),'y');                              % with the data
else
    f = [mu+sqrt(s2); flipdim(mu-3*sqrt(s2),1)] + mean(y);
    fill([zz; flipdim(zz,1)], f, [7 7 7]/8); hold on;           % show predictions
    plot(x,y,'b.'); plot(xx,yy,'r.')                               % with the data
    plot(xx, mu+mean(y), 'g.');
end
toc

