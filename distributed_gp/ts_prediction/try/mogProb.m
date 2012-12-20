function p = mogProb(x, mixWeights, mu, sigma)
% p(n) = sum_k w(k) N(x(n)|mu(k), sigma(k))

K = length(mixWeights);
N = length(x);
p = zeros(N,1);
for k=1:K
  p = p + mixWeights(k)*mvnpdf(x(:), mu(k), sigma(k));
end

end
