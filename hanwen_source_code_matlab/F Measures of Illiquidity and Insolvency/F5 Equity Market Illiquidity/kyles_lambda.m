function mli = kyles_lambda(returns, prices, volumes)
% Calculates the Kyle's lambda (price impact liquidity measure)
% Parameters:
% returns The returns of different securities. Rows are different dates and
% columns are different securities
% prices The closing prices of the securites. Rows are different dates and
% columns are different securities
% voumes The trading volumes of the securities. Rows are different dates
% and columns are different securities

num_days = size(returns,1);
num_securities = size(returns,2);

lambdas = zeros(num_securities,1);

% Loop through all the securities
for security = 1:num_securities
    y = returns(:,security);
    t = modified_sign(y); 
    X = [ones(num_days,1) t.*log(prices(:,security).*volumes(security))];
    
    betas = regress(y,X);
    lambdas(security) = betas(2);
    
end


% Aggregate measure of market liquidity
mli = mean(lambdas);