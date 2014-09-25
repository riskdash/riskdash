function var = turbulence_var(asset_returns,portfolio, q)
% Calculates the value-at-risk of a portfolio using only data from
% turbulent periods. Turbulence is defined at a q-percentile
% Parameters:
% asset_returns A matrix of asset returns. Rows are different dates.
% Columns are different assets.
% portfolio The portfolio weights
% q The percentile
% Output:
% var the turbulence value-at-risk of the portfolio

[turbulence_series, threshold, turbulent_periods] = turbulence(asset_returns,q);

% Find the portfolio returns only at the turbulent periods
portfolio_returns = portfolio'*asset_returns(turbulent_periods,:);

% Find the variance-at-risk i.e. the 5% percentile
var = prctile(portfolio_returns,5);



