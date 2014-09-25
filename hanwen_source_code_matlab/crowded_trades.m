function crowdedness  = crowded_trades(funds_returns, factor_returns, factor_index, threshold)
% Calculates the crowdedness series of a factor
% Parameters:
% funds_returns A matrix of funds returns. Rows are different dates.
% Columns are different assets.
% factor returns. A matrix of funds returns. Rows are different dates.
% Columns are different assets. For the paper there are 4 factors i.e. 4
% cols
% factor_index The factor whose crowdedness we want to calculate
% threshold. If it is specified then crowdedness is found with respect to beta great than threshold

% If we do not specify the threshold then set it to 1.96 (5% significance)
if nargin < 4
    threshold = 1.96;
end

num_factors = size(factor_returns, 2);
if (factor_index > num_factors ) || (factor_index < 1)
    error('Bad factor index.');
end

% We need to have the same days for returns of factors and returns of funds
if size(funds_returns,1)~=size(factor_returns,1)
    error('Unequal number of days for funds and factors');
end

num_days = size(funds_returns, 1);
num_funds= size(funds_returns, 2);

% Initialize
positive_funds = 0;
negative_funds = 0;
for i = 1:num_funds
    output = funds_returns(:,i);
    
    % Regress each fund's returns on the factors and a constant
    whichstats = {'beta', 'tstat'};
    stats = regstats(output,factor_returns,'linear',whichstats);
    betas = stats.beta;
    
    t_stat = stats.tstat.t;
    
    if nargin < 4
        % Check significance for the particular factor
        t_stat_factor = t_stat(factor_index+1);
        if  t_stat_factor > threshold
            positive_funds = positive_funds + 1;
        end
        if t_stat_factor < -threshold
            negative_funds = negative_funds + 1;
        end
        
    end
    
    if nargin == 4
        % Check the value of beta with respect to the threshold
        beta_factor = betas(factor_index+1);
        if  beta_factor > threshold
            positive_funds = positive_funds + 1;
        end
        if beta_factor < -threshold
            negative_funds = negative_funds + 1;
        end
        
    end
    
end


crowdedness = (positive_funds - negative_funds)/num_funds;






