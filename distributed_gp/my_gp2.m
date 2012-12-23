function [t mu sigma] = my_gp2(trainingDataFile, testDataFile, outputFile, uniqueIndex)
addpath(genpath('/grad/users/kx19/CityBeat/distributed_gp/GPLM_toolbox/gpml-matlab'));

data = load(trainingDataFile);

idx = isnan(data(:,2)) | data(:,2)==-1 ;
data = eliminate_outlier(data,3);
%remove all the failure data because API sometimes give invalid response
data = data(~idx,:);


training = data;
testing = load(testDataFile);

%[training, testing]  = data_split(data, .8);

d = 3;

k1 = {@covProd,{ @covSEiso, @covPeriodic}};
k2 =  { @covProd,{@covPeriodic, @covRQiso}};
covfunc =  {@covSum,{k1,k2}} ;

hyp.lik = 0.1;

x = training(:,1);
y = training(:,2);

nlml = 10000000;

best_hyp_cov = [];


for i = 1:30
    hyp.cov = log(rand(11,1)*20);
    [hyp,fX,i] = minimize(hyp, @gp, -200, @infExact, [], covfunc, @likGauss, x, y-mean(y));
    nlml2 = gp(hyp,@infExact, [], covfunc, @likGauss, x,y-mean(y));
    if nlml2<nlml
        nlml = nlml2;
        best_hyp = hyp
    end
end


hyp = best_hyp

xx = testing(:,1);
%yy = testing(:,2);


[mu s2] = gp(hyp, @infExact, [], covfunc, @likGauss, x, y-mean(y), xx);

outputMatrix = [xx mu+mean(y) s2];
%csvwrite(outputFile, outputMatrix);
dlmwrite(outputFile, outputMatrix, 'delimiter',',','precision',15)

h=figure; 
plot(x, y, 'b--', 'LineWidth', 2); hold on
xlabel('Day');
ylabel('Population');
f = [mu+3*sqrt(s2); flipdim(mu-3*sqrt(s2),1)] + mean(y);
fill([xx; flipdim(xx,1)], f, [7 7 7]/8); hold on          % show predictions
plot(xx, mu+mean(y), 'r--', 'LineWidth', 2);
my_path = '/grad/users/kx19/CityBeat/distributed_gp/tmp/';
print(h, '-depsc', [my_path 'pic' num2str(uniqueIndex)]);
choice = 0;

%if choice==0
 %   f = [mu+3*sqrt(s2); flipdim(mu-3*sqrt(s2),1)] + mean(y);
%    fill([xx; flipdim(xx,1)], f, [7 7 7]/8); hold on;           % show predictions
%    % plot(x,y,'k'); plot(xx,yy,'r-') ;plot(xx,mu+mean(y),'bx');                              % with the data
%else
 %   f = [mu+sqrt(s2); flipdim(mu-2*sqrt(s2),1)] + mean(y);
 %   fill([zz; flipdim(zz,1)], f, [7 7 7]/8); hold on;           % show predictions
 %   %plot(x,y,'k.'); plot(xx,yy,'r.')                               % with the data
 %   plot(xx, mu+mean(y), 'g.');
%end
%hold on


%[mu s2 fmu fs2 lp] = gp(hyp, @infExact, [], covfunc, @likGauss, x, y-mean(y), x, y) ;
%    f = [mu+2*sqrt(s2); flipdim(mu-2*sqrt(s2),1)] + mean(y);
%    fill([x; flipdim(x,1)], f, [7 7 7]/8); hold on;           % show predictions
%plot(x,mu+mean(y),'y');      plot(x,y,'r')                        % with the data



%nlml = gp(hyp, @infExact, [], covfunc, @likGauss, x, y-mean(y))
%res = validate(mu+mean(y), yy, 1)
quit
end
