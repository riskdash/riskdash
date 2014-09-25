function [thetas, ksi] = return_smoothing(hedge_fund_returns, factor_returns, lag)
% Calculates the smoothing weights and the parameter ksi for a hedge fund
% Parameters:
% hedge_fund_returns. The returns of the hedge fund. A nx1 vector
% factor_returns. The returns of a benchmark factor (like S&P 500). 
% A nx1 vector
% lag Thenumber of years going back that the smoothing takes place
% Output:
% thetas The smoothing weights
% ksi The sum of the squares of the smoothing weights

n = length(hedge_fund_returns);

% The first lag entries are ignored 
y = hedge_fund_returns(lag+1:end);
% Let's form the matrix X
X = ones(n-lag,lag+2);
for i=0:lag
    X(:,i+2)= factor_returns(lag+1-i:n-i);
end

gammas = regress(y,X);

thetas = gammas(2:end)/sum(gammas(2:end));

ksi = thetas'*thetas;


