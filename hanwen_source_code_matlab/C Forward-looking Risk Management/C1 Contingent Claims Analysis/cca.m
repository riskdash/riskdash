function [put_price systemic_risk_indicator_contribution] = cca(equity, volatility, risk_free_rate, default_barrier, time_to_maturity, cds_spread)
% Based on the paper "Systemic CCA - A Model Approach to Systemic Risk" by
% D. F. Gray, A.A. Jobst
% Calculates the price of the put option and the contribution  of the 
% company to the systemic risk indicator suggested in the paper
% Parameters:
% equity The market value of the equity of the company
% volatility The volatility of the equity
% risk_free_rate The risk free rate
% default_barrier Face value of the outstanding debt at maturity
% time_to_maturity Time to maturity of the debt
% cds_spread The cds spread
% Outputs:
% put_price The price of the put
% systemic_risk_indicator_contribution The contribution of this firl to the
% systemic risk indicator


% Ugly expression. Its a vector function which we 'll set to 0
% Equations 99 and 100 in the Systemic Risk document
val = @(x)[ (equity - x(1)*normcdf(( (log(x(1)/default_barrier)+(risk_free_rate + (x(2)^2)/2)*time_to_maturity)/(x(2)*sqrt(time_to_maturity)) ))+default_barrier*exp(-risk_free_rate*time_to_maturity)*normcdf(( (log(x(1)/default_barrier)+(risk_free_rate + (x(2)^2)/2)*time_to_maturity)/(x(2)*sqrt(time_to_maturity)) - x(2)*sqrt(time_to_maturity) )));
         ( equity*volatility - x(1)*x(2)*normcdf(( (log(x(1)/default_barrier)+(risk_free_rate + (x(2)^2)/2)*time_to_maturity)/(x(2)*sqrt(time_to_maturity)) )))];



% We need to solve a system of non-linear equations for asset price and
% asset volatility
% For this we need to guess an initial point
% Set the initial point equal to equity and its volatility 
x0 = [equity; volatility];

% x is a 2d vector Its first component is asset_price At and its second
% component is asset volatility 
[x,fval] = fsolve(val,x0);


d1 = (log(x(1)/default_barrier)+(risk_free_rate + (x(2)^2)/2)*time_to_maturity)/(x(2)*sqrt(time_to_maturity));
d2 = d1 - x(2)*sqrt(time_to_maturity);

% The price of the put
put_price = default_barrier *exp(-risk_free_rate*time_to_maturity)*normcdf(-d2)-x(1)*normcdf(-d1);

% Risky debt
debt = default_barrier*exp(-risk_free_rate*time_to_maturity) - put_price;

% The price of the CDS put option
cds_put=(1-exp(-(cds_spread/10000)*(default_barrier/debt-1)*time_to_maturity))*default_barrier*exp(-risk_free_rate*time_to_maturity);

systemic_risk_indicator_contribution = put_price - cds_put;











