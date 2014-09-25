function val = cca_fun(equity, volatility, risk_free_rate, default_barrier, time_to_maturity, asset_price, asset_vol)
% Helper function to solve the system of non-linear equations in CCA
% Parameters:
% equity The market value of the equity of the company
% volatility The volatility of the equity
% risk_free_rate The risk free rate
% default_barrier Face value of the outstanding debt at maturity
% time_to_maturity Time to maturity of the debt
% asset_price The market value fo the assets
% asset_vol The volatility of the market value fo the assets

d1 = (ln(asset_price/default_barrier)+(risk_free_rate + (asset_vol^2)/2)*time_to_maturity)/(asset_vol*sqrt(time_to_maturity));
d2 = d1 - asset_vol*sqrt(time_to_maturity);

x = [asset_price; asset_vol];

val(1) = @(x) (equity - asset_price*normcdf(d1)+default_barrier*exp(-risk_free_rate*time_to_maturity)*normcdf(d2));
val(2) = @(x) ( equity*volatility - asset_price*asset_vol*normcdf(d1));