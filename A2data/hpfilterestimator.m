
	%A2
	%This file takes a two column n row data set and puts it through the 
	%hpfilter to calculate the gap between the trend and the original data 

function [gaps] = hpfilterestimator(indicator)

% get the data from the indicator 
num_years = size(indicator, 1);
% we need a buffer so the the data has something to compare against
buffer = 2;
gaps = zeros(num_years-buffer+1,2);
for t=buffer:num_years
		% trend is the result from hpfilter applied to indicator
		% indicator is a m by n matrix with m samples and n time_series
		% m = row, n = column
		% in our case, m =1, n=historical to 2014
        % 1600 for quarterly, 100 for yearly
        trend = hpfilter(indicator(1:t,2),100);
        % Gap is the difference of the original data and the trend
        % first column gives the time
        gaps(t-buffer+1,1) = indicator(t,1);
        difference(t) = trend(t) - indicator(t,2);
        gaps(t-buffer+1,2) = (difference(t)/indicator(t,2))*100;
end

%gap = gaps;