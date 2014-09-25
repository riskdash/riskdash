clear all;
clc;


n=500;
new_homes = 10*rand(n,1);
new_house_prices = 100*rand(n,1);
home_price_index = 100+[1:n]'+rand(n,1);
mortgage_rates = 0.12 + 0.01*randn(n,1);
risk_free = .04*ones(n,1);
time_structural_shift = 80;

[total_value total_guarantee total_delta]=housing_refinance(new_homes,new_house_prices,home_price_index, mortgage_rates, risk_free,time_structural_shift)  

% Test loan
i = 10;
t = 15;
mortgage_rate = mortgage_rates(i);
value_house = 100;
ltv_initial = 0.85;
balance = balance_loan(i,t, mortgage_rate, ltv_initial, value_house);

 [prinp, intp, bal, p] = amortize(mortgage_rate/12, 360, ltv_initial*value_house);
 
 balance - bal(t-i)
 
 

