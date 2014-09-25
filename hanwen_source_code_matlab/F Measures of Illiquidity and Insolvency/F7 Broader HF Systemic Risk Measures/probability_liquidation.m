function p = probability_liquidation(coefficients, age, prev_assets, returns, flows)
% Calculates the probability of liquidation of a fund. This is to follows
% the function probability_liquidation_model which calculates the
% coefficients by learning from sample data
% Parameters:
% coefficient The 9 coeffs returned by the function probability_liquidation_model
% age The age of the fund
% prev_assets The assets under management of the fund last year
% returns A 3x1 vector for the returns of the last 3 years going backwards
% i.e returns(1) are the current returns
% flows A 3x1 vector for the flows of the last 3 years going backwards
% i.e flows(1) are the current flows

linear_term = coefficients'*[1 age prev_assets returns' flows']';

p = exp(linear_term)/(1+exp(linear_term));