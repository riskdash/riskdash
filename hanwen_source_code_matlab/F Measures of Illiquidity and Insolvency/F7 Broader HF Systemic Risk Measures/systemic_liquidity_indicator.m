function [q_stats sys_liquidity_ind] = systemic_liquidity_indicator(funds_returns, assets_under_management)
% Calculates the Q-stats for each fund and the systemic liquidity indicator
% Paramaters:
% funds_returns The monthly returns of the funds. A nxk matrix.  Rows are 
% the different periods  Columns are the different funds. 
% assets_under_management The assets under management for the different
% funds A kx1 vector
% Outputs:
% q_stats The q-statistics for the different funds' returns. A kx1 vector
% sys_liquidity_ind The systemic liquidity indicator

num_funds = size(funds_returns,2);
q_stats = zeros(num_funds,1); 

for i=1:num_funds
    % Find the Ljung-Box statistic
    [h pval stat] = lbqtest(funds_returns(:,i),'lags',6);
    q_stats(i) = stat;
    
    rho = autocorr(funds_returns(:,i), 1);
    % 1st order autocorrelation
    rhos(i) = rho(2);
end

sys_liquidity_ind = rhos*assets_under_management/sum(assets_under_management);








