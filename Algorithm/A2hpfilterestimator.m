% Macroeconomic Measures, EWI Gaps A2
% note: use 1600 for quarterly data, 100 for yearly
%
% expects a two column t row data set and puts it through the 
% hpfilter to calculate the gap between the trend and the original data 
% needs license R2014 for the hpfilter
% needs to be run with the data from each country

% takes in an indicator file and returns the corresponding gaps
function [gaps] = A2hpfilterestimator(indicator)

% get the data from the indicator 
% get the number of years
num_years = size(indicator, 1);
% needs a buffer as the original so the the data has something to compare against
buffer = 2;

% create a two column array
gaps = zeros(num_years-buffer+1,2);

% populate the array
for t=buffer:num_years
		% trend is the result from hpfilter applied to indicator
		% indicator is a m by n matrix with m samples and n time_series
		% m = row, n = column
		% in our case, m =1, n=historical to 2014
        % 1600 for quarterly, 100 for yearly
        trend = hpfilter(indicator(1:t,2),100);
        % Gap is the difference of the original data and the trend

        % populate the first column with the time
        gaps(t-buffer+1,1) = indicator(t,1);
        difference(t) = trend(t) - indicator(t,2);
        % calculate the percentage change
        gaps(t-buffer+1,2) = (difference(t)/indicator(t,2))*100;
end