function ret = contrarian_trading_strategy(input_returns, realized_returns)
% Calculates the cumulative return of the contrarian trading strategy
% Parameters:
% input_returns The returns of the securities used to calculate the weights
% of the strategy. Rows are the different periods. Columns are the different
% securities
% realized_returns The realized returns of the securities to calculate the
% performance of the strategy. Rows are the different periods. 
% Columns are the different securities 

num_periods = size(input_returns,1);
num_securities = size(input_returns,2);

ret = 1;
for period = 1:num_periods
    
    % Market Portfolio
    Rm = 1/num_securities*ones(num_securities,1)'*input_returns(period,:)';
    % Strategy
    unnormalized_weights = - 1/num_securities*(input_returns(period,:) - Rm);
    size_p = sum(abs(unnormalized_weights))/2;
    % Divide by the amount of money to support the position
    normalized_weights = unnormalized_weights/size_p;
    
    realized_return = normalized_weights*realized_returns(period,:)';
    ret = ret*(1+realized_return);    
end

