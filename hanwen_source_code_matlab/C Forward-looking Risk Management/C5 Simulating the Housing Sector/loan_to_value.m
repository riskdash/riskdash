function ltv = loan_to_value(i,t, mortgage_rate, ltv_initial, value_house, hpi)
% Calculates the loan-to-value ratio for a home initially purchased in vintage i 
% by time t
% Parameters
% i The vintage when the house was purchased
% t The time we calculate the laon-to-value ratio
% mortgage_rate The fixed rate for a conventional 30-yr fixed-rate mortgage
% ltv_initial The initial loan-to-value ration 
% value_house The value of the house
% hpi Home price index monthly timeseries. A nx1 vector

current_loan = balance_loan(i,t,mortgage_rate, ltv_initial, value_house);


current_value = value_house*hpi(t)/hpi(i);
ltv = current_loan/current_value; 