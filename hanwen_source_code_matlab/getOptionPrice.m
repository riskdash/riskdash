function [Put_Delta, Put_Gamma, Put_Vega, Put_Value] = getOptionPrice(current_house_value,ltv,house_volatility,rent_yield,risk_free_rate,mortgage_rate,time_left)
% Calculates the greeks and the value of the embedded Bermudan put option
% in a mortgage using binomial tree
% Parameters:
% current_house_value The current value of the house
% ltv The loan-to-value ratio
% house_volatility The volatility of the house price (e.g. 0.2) in
% annualized terms
% rent_yield The rental yield (e.g 0.04) in annualized terms
% risk_free_rate The risk free rate in annualized terms
% mortgage_rate The mortgage rate in annualized terms
% time_left Time till maturity of the mortgage

if timeLeft < 0
    Put_Delta = 0;
    Put_Gamma = 0;
    Put_Vega = 0;
    Put_Value = 0;
else
    
    mortgage_amount = current_house_value*ltv;
    
    
    StartDate = dateFromIndex(1); % It doesn't matter which dates you pick
    MaturityDate = dateFromIndex(1+time_left);
    TimeSpec = crrtimespec(StartDate, MaturityDate, time_left);
    
    DividendType = 'constant';
    ExDividendDates = TimeSpec.dObs(2:end)';
    
    StockSpec = stockspec(house_volatility,current_house_value,DividendType,rent_yield,ExDividendDates);
    
    RateSpec = intenvset('Rates', risk_free_rate, 'StartDates',StartDate, 'EndDates', MaturityDate,'Compounding', -1);
    
    CRRTree = crrtree(StockSpec, RateSpec, TimeSpec);
    % We need to divide the mortgage rate with 12 since it is annualized
    [Principal, Interest, Balance, Payment] = amortize(mortgage_rate/12,time_left, mortgage_amount);
    
    OptSpec = 'Put';
    Strike = Balance;
    Settle = StartDate;
    ExerciseDates = [TimeSpec.dObs(2:end)];
    InstSet = instoptstock(OptSpec, Strike, Settle, ExerciseDates);
    
    [Put_Delta, Put_Gamma, Put_Vega, Put_Value] = crrsens(CRRTree, InstSet);
end