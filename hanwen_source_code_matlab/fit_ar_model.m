function [regressor_coefficients, order] = fit_ar_model(y_series, max_order)
% Fits an AR model to the y-series. It selects the order that is less than
% max_order and minimizes the BIC
% Parameters:
% y_series A nx1 vector that we 'll fit an AR model to.
% max_order The maximum order of AR model we will try

n = length(y_series);
BIC = zeros(max_order,1);
betas = zeros(max_order+1,max_order);

for order = 1:max_order
    % Form the response variables and covariates
    y = y_series(order+1:end);
    X = zeros(n-order,order); 
    for j = 1:order
        X(:,j) = y_series(order+1-j:end-j);   
    end
  
    whichstats = {'beta', 'r'};
    % The constant term is added automatically
    stats = regstats(y,X,'linear',whichstats);
    betas(1:order+1,order) = stats.beta;
    r = stats.r;
    
    % Instead of s^2 we use the maximum likelihood estimate of variance
    % i.e. we divide r'*r by n instead of n - num_regressors
    BIC(order)=n*log(r'*r/n)+order*log(n);
end

% Find the minimum bic and the corresponding regressor coefficients
[bic_min, min_order] = min(BIC);
regressor_coefficients = betas(1:min_order+1,min_order);
order = min_order;