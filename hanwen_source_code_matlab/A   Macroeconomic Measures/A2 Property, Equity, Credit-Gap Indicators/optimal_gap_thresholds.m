function [nts_thresholds, true_positive_thresholds] = optimal_gap_thresholds(indicators_series, is_crisis_series,horizon, max_thresholds)
% Based on the paper "Towards an operational framework for financial
% stability:"fuzzy" measurement and its consequences by C. Borio, M.
% Drehmann
% Calculates the optimal gap thresholds according to nts ratio and
% true positive rate
% Parameters:
% indicators_series The joint signal indicators yearly time series. 
% A matrix nx2.
% is_crisis_series A binary nx1 vector. 1 signals that there is a crisis
% horizon In the paper it is set 1 to 3 years
% max_thresholds A 2x1 vector with the meximum thresholds for the two
% indicators. They are integer values. 
% Output:
% nts_thresholds The optimal thresholds for the two indicators when the
% objective function is nts A 2x1 vector
% true_positive_thresholds The optimal thresholds for the two indicators 
% when the objective function is true_positive rate. A 2x1 vector

% We check only integer thresholds as in the paper
nts = zeros(max_thresholds(1), max_thresholds(2));
true_positives = zeros(max_thresholds(1), max_thresholds(2));;


for i=1:max_thresholds(1)
    for j=1:max_thresholds(2)
        thresholds = [i;j];
        [noise_to_signal num_predicted_crises] = joint_gap_indicators(indicators_series, thresholds, is_crisis_series, horizon);
        nts(i,j) = noise_to_signal;
        true_positives(i,j) = num_predicted_crises;
    end
end


% Find the optimal thresholds for the nts objective
[vals ind] =  min(nts);
[val index] = min(vals);
nts_thresholds = [ind(index);index];

% Find the optimal thresholds fpr the true positive objective
[vals ind] =  max(true_positives);
[val index] = max(vals);
true_positive_thresholds = [ind(index);index];



