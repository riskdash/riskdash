function [total_value total_guarantee total_delta]=housing_refinance(new_homes,new_house_prices,hpi, mortgage_rates, risk_free,time_structural_shift)
% Calculates the total_value of houses (new and cash-out refinanced), the
% total value of mortgage lender guarantees and the aggregate sensitivity
% Parameters:
% new_homes A monthly timeseries of the number of new homes A nx1 vector
% new_house_prices A monthly timeseries for the price of new houses A nx1 vector
% hpi A monthly timeseries for HPI. Used to determine the value growth
% of existing houses A nx1 vectr
% mortgage_rates A monthly timeseries of mortgage rates A nx1 vector
% risk_free Risk-free rate monthly timeseries A nx1 vector
% time_structural_shift The time after that the probability of refinancing
% changes from 0.003 to 0.009
% Outputs:
% total_value The total value houses (new and cash-out refinanced)
% total_guarantee the total value of mortgage lender guarantees
% total_delta The aggregate sensitivity of the guarantees


loan_to_value_ratio = 0.85; % this is set to 0.85 in the simulation
rent_yield = 0.04;
house_volatility = 0.08;


n = length(new_homes);
total_value=zeros(n,1);
% for t=1:n
%     total_value(t) = new_homes(t)*new_house_prices(t);
%     for i=1:t-1
%         mortgage_rate = mortgage_rates(i);% This is in annualized terms
%         value_house = new_house_prices(i);
%         % This is the current loan to value ratio for a loan started at i
%         current_ltv = loan_to_value(i,t, mortgage_rate, loan_to_value_ratio, value_house, hpi);
%         p_surv = prob_survival(i,t-1, mortgage_rate, loan_to_value_ratio, value_house, hpi,time_structural_shift);
%         p_ref = prob_refinance(t,current_ltv,time_structural_shift);
%         total_value(t) = total_value(t) + total_value(i)*p_surv*p_ref*calc_value_house(i,t,hpi,new_house_prices)/value_house;
%     end
% end

% Total guarantees and total_delta
total_guarantee = zeros(n,1);
total_delta = zeros(n,1);
for t=1:n
    for i=1:t
        mortgage_rate = mortgage_rates(i);% This is in annualized terms
        value_house = new_house_prices(i);
        p_surv = prob_survival(i,t, mortgage_rate, loan_to_value_ratio, value_house, hpi,time_structural_shift);
        current_value_house = calc_value_house(i,t,hpi,new_house_prices)
        current_ltv = loan_to_value(i,t, mortgage_rate, loan_to_value_ratio, value_house, hpi);
        rates = risk_free(t);
        time_left = 360-(t-i);% Months left (it is a 30-year loan)
        
        [put_delta, put_gamma, put_vega, put_value] = getOptionPrice(current_value_house,current_ltv,house_volatility,rent_yield,rates,mortgage_rate,time_left);%guarantee(i,t);
        
        total_guarantee(t) = total_guarantee(t)+total_value(t)*p_surv*put_value/value_house;
        total_delta(t) = total_delta(t)+total_value(t)*p_surv*put_delta/value_house;
    end
end
