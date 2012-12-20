function [ prob ] = gaussianProb( x, D )
%GAUSSIANPROB Summary of this function goes here
%   Detailed explanation goes here

p = 2;

prob = 0;

%D = D - repmat(x,[1000,1]);

size(D)
prob = log(1/((2*pi).^2))  * length(D);


'haha'
D = D';
for i = 1:length(D)
    data = D(:,i);
    
    prob =+ (-0.5*(data-x')'*(data-x'));
    %prob = prob * 1.0/((2*pi))*exp(-0.5*(data-x')'*(data-x'));
    
end

prob

end

