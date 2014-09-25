function p = prob_refinance(t, ltv,time_structural_shift)
% Calculates the probability of refinancing at time t
% Paramters:
% t the time at which we want to calculate the probability of refinance
% ltv The loan-to-value ratio at time t

if ltv >0.85 || ltv < 0
    p = 0;
else
    if t<time_structural_shift
        p = 0.003;
    else
        p = 0.009;
    end
end