function dcovar = delta_co_var(output_returns, input_returns, lagged_factors_returns, quantile)
% Based on the paper "CoVar", Tobias Adrian and Markus K. Brunnermeier
% Calculates the delta_covar of output institution (or system) on another
% institution
% Parameters:
% output_returns The returns of the output institution or system. A nx1
% vector
% input_returns The returns of the input institution whose contribution we
% want to quantify. A nx1 vector
% lagged_factors_returns The lagged returns (lag = 1) for the factors as used in 
% eq. 6 of the paper. A matrix (n+1)xk.
% quantile The quantile we want to use (0.05 or 0.01) in the paper

% Default value quantile = 0.05
if nargin < 4
    quantile = 0.05;
end

if nargin < 3
    lagged_factors_returns = [];
end

num_periods = size(output_returns,1);
median_percentile = 0.5;

% Calculate the median state of the input institution
X = [ones(num_periods,1) lagged_factors_returns(1:end-1,:)];
y = input_returns;
betas = quantile_regression(y,X,median_percentile);
if nargin<3
    % lagged_factors_returns is empty
    median_input_state = betas(1);
else
    median_input_state = [1 lagged_factors_returns(end,:)]*betas;
end

% Calculate the distressed state of the input institution
betas = quantile_regression(y,X,quantile);
if nargin < 3
    % lagged_factors_returns is empty
    distressed_input_state = betas(1);
else
    distressed_input_state = [1 lagged_factors_returns(end,:)]*betas;
end


% Quantile regression of the output_institution or system on lagged factors
% and input institution
X = [ones(num_periods,1) input_returns lagged_factors_returns(1:end-1,:)];
y = output_returns;
betas = quantile_regression(y,X,quantile);

% Definition of delta_co_var equation (9)
dcovar = betas(2)*(distressed_input_state - median_input_state);






