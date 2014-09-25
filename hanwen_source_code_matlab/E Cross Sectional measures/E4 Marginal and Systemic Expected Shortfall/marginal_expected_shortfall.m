function mes = marginal_expected_shortfall(firm_returns, market_returns)
% Calculates the marginal expected shortfall of a firm
% Parameters:
% firm_returns The timeseries of returns for the firm
% market_returns The timeseries of returns for the market

% We need to have the same days for market_returns and firm_returns
if length(firm_returns)~=length(market_returns)
    error('Unequal number of days for firm and market');
end

% Find the 5% quantile the market return
low_threshold = prctile(market_returns,5);

% Find the 5% worst days for the market return
worst_days = market_returns < low_threshold;

% Take the average of the firm's returns during the worst days of the
% market
mes = mean(firm_returns(worst_days));



