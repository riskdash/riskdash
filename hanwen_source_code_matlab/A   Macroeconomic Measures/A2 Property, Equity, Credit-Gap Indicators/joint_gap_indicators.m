function [nts num_predicted_crises] = joint_gap_indicators(indicators_series, thresholds, is_crisis_series, horizon)
% Calculates the signal to noise ratio and the number of predicted crises 
% of joint signal indicators for particular thresholds
% Parameters:
% indicators_series The joint signal indicators yearly time series. 
% A matrix nx2.
% thresholds The thresholds used to signal a crisis. A 2x1 vector
% is_crisis_series A binary nx1 vector. 1 signals that there is a crisis
% horizon In the paper it is set 1 to 3 years

num_years = size(indicators_series,1);
buffer_length = 10;

successes = 0;
false_alarms = 0;
missed_crises = 0;
negative_successes = 0;

% We need to have at least 10 years of data
if num_years < buffer_length
    error('Not enought years of data.');
end

% We 'll run the HP filters from year buffer_length to num_years-horizon 
gaps = zeros(num_years-buffer_length+1-horizon,2);
for t=buffer_length:num_years-horizon
    for i=1:2
        trend = hpfilter(indicators_series(1:t,i),1600);
        % Gap is the difference of the value of the time_series and the
        % trend
        gaps(t-buffer_length+1,i) = trend(t) - indicators_series(t,i);
    end
    
    % If both of the gaps are greater than the corresponding thresholds
    % then we have a signal that there will be a crisis in the next horizon
    % years
    if sum(gaps(t-buffer_length+1,:)>thresholds')==2
        if sum(is_crisis_series(t+1:t+horizon))>0
            successes = successes + 1;
        else
            false_alarms = false_alarms+1;
        end
        
    else
        % No crisis is predicted for the next horizon years
        if sum(is_crisis_series(t+1:t+horizon))>0
            missed_crises = missed_crises + 1;
        else
            negative_successes = negative_successes+1;
        end
    end
end


type_I_error = 0;
type_II_error = 0;
if (false_alarms + negative_successes) ~=0
    type_II_error = false_alarms/(false_alarms + negative_successes);
end
if (missed_crises + successes) ~=0
    type_I_error = missed_crises/(missed_crises + successes);
end

nts = type_II_error/(1-type_I_error);
num_predicted_crises = successes;
















