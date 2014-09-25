function c = co_risk(output_cds_spreads, input_cds_spreads, risk_factors_series,q,risk_factors_values )
% Calculates the conditional co-risk between two institutions
% Parameters:
% output_cds_spreads The cds-spreads time series for the output firm. A nx1
% vector
% input_cds_spreads The cds-spreads time series for the input firm. A nx1
% vector
% risk_factors_series Risk-factors time series. A n x k matrix
% q the quantile. The paper uses q = 0.95
% risk_factors_values the values of the risk factors at the period we 
% calculate the co-risk. A 1 x k vector

num_dates = size(output_cds_spreads,1);

% Run the quantile regression
y = output_cds_spreads;
X = [ones(num_dates,1) risk_factors_series input_cds_spreads];
betas = quantile_regression(y,X,q);

% Calculate the q-percentile of cds-spreads time series
input_cds_quantile = prctile(input_cds_spreads,100*q);
output_cds_quantile = prctile(output_cds_spreads,100*q);

c = 100*((betas(1) + betas(end)*output_cds_quantile+betas(2:end-1)'*risk_factors_values')/input_cds_quantile-1);

