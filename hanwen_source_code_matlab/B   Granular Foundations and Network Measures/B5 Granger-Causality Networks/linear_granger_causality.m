function  [p_value_robust p_value] = linear_granger_causality(input_institution_returns, output_institution_returns)
% Calculates the p-value of the linear Granger causal relationship between
% input_institution_returns and output_institution_returns
% Parameters:
% input_institution_returns. The time series returns of the input
% institution. An nx1 vector
% output_institution_returns. The time series returns of the output
% institution. An nx1 vector

num_periods = size(input_institution_returns,1);
% Form the response in the regression equation
y = output_institution_returns(2:num_periods,1);

% Form the regressors
X = [output_institution_returns(1:num_periods-1) input_institution_returns(1:num_periods-1)];

% Truncation lag fraction for the HAC is chosen .1
[betas, V_hat] = hac_regression(y,X,0.1);

p_value_robust = 1 - normcdf(betas(2)/sqrt(V_hat(2,2)/(num_periods-1)));

% a check for the usual estimator
residuals = y - X*betas;
s_squared = residuals'*residuals/(num_periods-3);
C = inv(X'*X);
t_stat = betas(2)/sqrt(s_squared*C(2,2));
p_value = 1-normcdf(t_stat);
