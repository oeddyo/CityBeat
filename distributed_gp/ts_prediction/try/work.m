function [A B ] =work()

data = zeros(1000,2);

for i = 1:1000
    data(i,:) = mvnrnd([1,1]', [1,0;0,1]');
end


xinit = rand(6,1);





weights = [0.3 0.7];
mus = [0 10];
sigmas = [2 2];
Nsamples = 500000;
x = zeros(Nsamples,1);
sigma_prop = 5;

xinit = 20*rand(1,1);


target = @(x) (mogProb(x, weights, mus, sigmas));
proppdf = @(x,y) (normpdf(x,y,sigma_prop));
proprnd = @(x) x+sigma_prop*randn(1,1);


[SMPL ACCEPT] = mhsample(xinit, 2000, 'pdf', target, 'proppdf', proppdf, 'proprnd', proprnd);


A = SMPL;
B = ACCEPT;



end