function l = balance_loan(i,t, mortgage_rate, ltv_initial, value_house)
% Calculates the loan value for a home initially purchased in vintage i 
% by time t
% Parameters
% i The vintage when the house was purchased
% t The time we calculate the balance of the remaining loan
% mortgage_rate The annualized fixed rate for a conventional 30-yr 
% fixed-rate mortgage
% ltv_initial The initial loan-to-value ratio
% value_house The value of the house

monthly_rate = mortgage_rate/12;
initial_loan = ltv_initial*value_house;

% This is the constant montly payment for 360 months
payment = initial_loan*monthly_rate/(1-1/(1+monthly_rate)^360);

paid_amount = 0;
for k = 1: t-i
    paid_amount = paid_amount + payment/(1+monthly_rate)^(361-k);
end

l = initial_loan-paid_amount;
