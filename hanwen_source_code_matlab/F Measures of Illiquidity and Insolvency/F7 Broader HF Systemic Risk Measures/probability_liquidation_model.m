function coeffs = probability_liquidation_model(aums, returns, flows, is_liquidated_series)
% Calculates the coefficients in the logit model for probability of
% liquidation of a fund
% Parameters:
% aums The series of AUMS for the different funds A nxk matrix Rows are the
% different months Columns are the different funds
% returns The series of returns for the different funds A nxk matrix Rows 
% are the different months Columns are the different funds
% flows The series of flows for the different funds A nxk matrix Rows are 
% the different months Columns are the different funds
% is_liquidated_series A binary matrix nxk. The i,j component = 1 denotes 
% that fund j is liquidated at period i

num_months = size(aums,1);
num_funds = size(aums,2);

% Lets form the matrix X and y for the logistic regression
% 8 is the number of regressors in the model

% Every num_months-2 group refers to a fund
X = [];
y = [];
for i=1:num_funds
    fund_matrix = [[3:num_months]' aums(2:num_months-1,i) returns(3:num_months,i) returns(2:num_months-1,i) returns(1:num_months-2,i) flows(3:num_months,i) flows(2:num_months-1,i) flows(1:num_months-2,i)];
    X =  [X;fund_matrix];
    y = [y;is_liquidated_series(3:num_months,i)];
end

% It adds automatically the constant
coeffs = glmfit(X, [y ones(length(y),1)], 'binomial', 'link', 'logit');