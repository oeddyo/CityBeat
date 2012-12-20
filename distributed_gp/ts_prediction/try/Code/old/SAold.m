function [x, samples, fn, naccept] = SAold(target, proposal, xinit, maxIter, targetArgs, proposalArgs, ...
					temp, thresh);
% Simulated annealing algorithm
% 
% Inputs (similar to MH.m)
% target returns the unnormalized log posterior, called as 'p = exp(target(x, targetArgs{:}))'
% proposal is a fn, as 'xprime = proposal(x, proposalArgs{:})' where x is a 1xd vector
% xinit is a 1xd vector specifying the initial state
% maxIter - max number of iterations
% targetArgs - cell array passed to target
% proposalArgs - cell array passed to proposal
% temp(s) = temperature at step s
%
% Outputs
% x = optimal set of arguments
% samples(s,:) is the s'th sample (of size d)
% fn(s) is the function value at the s'th sample
% naccept = number of accepted moves

thresh  
d = length(xinit);
samples = zeros(Nsamples, d);
x = xinit(:)';
naccept = 0;
logpOld = feval(target, x, targetArgs{:});
for t=1:Nsamples
  xprime = feval(proposal, x, proposalArgs{:});
  logpNew = feval(target, xprime, targetArgs{:});
  % log( p^(1/T)) = 1/T log p
  alpha = exp((logpNew - logpOld)/temp(t));
  r = min(1, alpha);
  u = rand(1,1);
  if u < r
    x = xprime;
    naccept = naccept + 1;
    logpOld = logpNew;
  end
  samples(t,:) = x;
  fn(t) = logpOld;
end


  
