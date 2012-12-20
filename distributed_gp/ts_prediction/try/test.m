function [A B ] =test()

data = zeros(100,2);

for i = 1:3000
    data(i,:) = mvnrnd([0.1,5]', [0.0000001,0;0,0.0000001]');
end


xinit = rand(1,2);

sigma_prob = [0.1,0;0,0.1;]



target = @(x) ( gaussianProb(x,data) );
%proppdf = @(x,y) (normpdf(x,y,sigma_prop));
proppdf = @(x,y) log(mvnpdf(x,y,sigma_prob));

proprnd = @(x) x+(mvnrnd([0,0],sigma_prob));


[SMPL ACCEPT] = mhsample(xinit, 5000, 'logpdf', target, 'logproppdf', proppdf, 'proprnd', proprnd, 'burnin',100, 'symmetric',1);


A = SMPL;
B = ACCEPT;



end