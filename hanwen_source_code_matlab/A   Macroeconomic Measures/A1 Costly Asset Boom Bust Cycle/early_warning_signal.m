function [true_pos true_neg usefulness dp] = early_warning_signal(indicator, booms, theta, percentile,num_periods)
% Calculates some metrics of an indicator to be used as an early 
% warning signal of costly asset price booms
% Parameters:
% indicator The indicator timeseries A nx1 vector
% booms A binary timeseries where 1 denotes a costly boom A nx1 vector
% theta risk_aversion_parameter
% percentile The percentile of the distribution of the indicator 
% when it is exceeded a warning signal for a costly boom is issued 
% 0<= percentile <=1
% num_periods The number of periods into the future that an issued warning
% signal indicates there will be a costly boom. In the paper it is set to 6
% Outputs:
% true_pos The true positives of the warning signal
% true_neg The true negatives of the warning signal
% usefulness The usefulness of the indicator
% dp The difference between conditional and uncoditional probabilities of
% true postive 

n = length(indicator);

% First find the threshold when exceeded the indicator issues a signal
threshold = prctile(indicator,percentile*100);

% The values in the "confusion" matrix
A = 0;
B = 0;
C = 0;
D = 0;

for i=1:n-num_periods
    % If the indicator is greater than the threshold a signal is issued
    signal_issued = indicator(i) > threshold;
    % Find if there is an asset price costly boom in the next num_periods
    has_costly_boom = sum(booms(i+1:i+num_periods)) > 0
    
    if signal_issued
        if has_costly_boom
            A = A+1;
        else
            B=B+1;
        end
    else
        if has_costly_boom 
            C = C+1;
        else
            D = D+1;
        end
    end
end

true_pos = A/(A+B);
true_neg = D/(C+D);
L = theta *C/(A+C) + (1-theta)* B/(B+D);
usefulness = min(theta, 1-theta) - L;
dp = true_pos - (A+C)/(A+B+C+D);

