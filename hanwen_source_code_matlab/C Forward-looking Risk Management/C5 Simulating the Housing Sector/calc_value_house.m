function v = calc_value_house(begin_time, t, hpi, nhp)
% Calculates the value of a house from vintage begin_time at time t
% Parameters:
% begin_time The vintage of the house 1<=begin_time<=t<=length(hpi)
% t The time we want to calculate the value of the house 
% hpi Home price index monthly timeseries. A nx1 vector
% nhp New house prices monthly timeseries A nx1 vector

v = nhp(begin_time)*hpi(t)/hpi(begin_time);