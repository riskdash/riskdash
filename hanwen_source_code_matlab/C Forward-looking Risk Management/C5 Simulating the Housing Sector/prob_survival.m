function p = prob_survival(begin_time, t, mortgage_rate, ltv_initial, value_house, hpi, time_structural_shift)
% Calculates the probability that a new home from vintage begin_time has not
% underone a cash-out refinancing by time t
% Parameters:
% begin_time The vintage when the house was bought
% t The time till when we want to calculate the prob of survival 
% mortgage_rate The fixed rate for a conventional 30-yr fixed-rate mortgage
% at begin_time
% ltv_initial The initial loan-to-value ratio 
% value_house The value of the house at begin_time
% hpi Home price index monthly timeseries. A nx1 vector
% time_structural_shift The time after that the probability of refinancing
% changes from 0.003 to 0.009
p = 1;
for k = 1:t-begin_time
    ltv = loan_to_value(begin_time,begin_time+k, mortgage_rate, ltv_initial, value_house, hpi);
    p = p*(1-prob_refinance(begin_time+k, ltv, time_structural_shift));
end