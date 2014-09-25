function [turbulence_series, threshold, turbulent_periods] = turbulence(asset_returns,q)
% Calculates the turbulence of each period, the q-percentile of turbulence distribution and the turbulent periods 
% Parameters:
% asset_returns A matrix of asset returns. Rows are different dates.
% Columns are different assets.
% q The percentile. In the paper q = 0.75
% Output:
% turbulence_series The turbulence for each period in the sample
% threshold The q-percentile of turbulence distribution
% turbulent_periods The periods where turbulence > quantile

num_days = size(asset_returns,1);
% Find the mean return and covariance of asset returns
mu = mean(asset_returns, 1)';
Sigma = cov(asset_returns);


turbulence_series = zeros(num_days,1);
% Calculate the turbulence for each period
for i=1:num_days
    y = asset_returns(i,:)';
    turbulence_series(i) = (y-mu)'*inv(Sigma)*(y-mu);
end

% Find the threshold that characterizes turbulence
threshold = prctile(turbulence_series,100*q);

% Find the turbulent periods
turbulent_periods = find(turbulence_series > threshold);
