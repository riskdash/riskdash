function forecast_error = stress_scenario_selection(gdp_growth_series)
% Based on paper: "Macro Stress Tests and Crises: What can we learn? R.
% Alfaro, M. Drehman, 2009
% Calculates the worst forecast error in an AR process which is
% subsequently used as a stress scenario
% Parameters:
% gdp_growth_series The gdp growth series as an nx1 vector

num_periods = length(gdp_growth_series);
max_order = 2;

% Find the AR model that minimizes the BIC score
[regressor_coefficients order] = fit_ar_model(gdp_growth_series, max_order)

% Find the most negative forecast error of the selected model
forecast_errors = zeros(num_periods-order,1);
for i=order+1:num_periods
    realized_gdp_growth = gdp_growth_series(i);
    predicted_gdp_growth = regressor_coefficients'*[1;gdp_growth_series(i-1:-1:i-order)];
    
    forecast_errors(i-1) = realized_gdp_growth - predicted_gdp_growth; 
end

forecast_error = min(forecast_errors);