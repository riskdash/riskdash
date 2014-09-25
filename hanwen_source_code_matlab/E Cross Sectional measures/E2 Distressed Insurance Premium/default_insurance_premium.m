function dip = default_insurance_premium(default_probabilities, correlations)
% Calculated the default insurance premium
% Parameters:
% default_probabilities The default probabilities of the banks. A nx1
% vector
% correlations The correlation matrix of the assets' returns of the banks

num_banks = length(default_probabilities);

% Find the default thresholds for each bank We assume that the returns are
% standard normally distributed
default_thresholds = norminv(default_probabilities);

% Generate 500000 random Gaussian vectors
num_repetitions = 500000;
R = chol(correlations);
z = randn(num_repetitions,num_banks)*R;

% Find the probability distribution of joint defaults
default_distribution = zeros(num_banks+1,1); % 0,1,.., num_banks
for i=1:num_repetitions
    num_defaults = sum(z(i,:)<default_thresholds');
    default_distribution(num_defaults+1) = default_distribution(num_defaults+1)+1;
end

default_distribution = default_distribution/num_repetitions;

num_repetitions = 1000;

losses_given_default = zeros(num_banks,num_repetitions);
% Calculate the distribution of total losses
for k = 1:num_banks
    lgd = 0;
    for i = 1:k
        lgd = lgd + my_trirnd(0.1,0.55,1,num_repetitions);
    end
    losses_given_default(k,:) = lgd;
end

% Maximum losses are N. Divide this into N*100 intervals.
% Find the probability distribution of total losses in the default case
intervals = 100;
prob_losses = zeros(num_banks*intervals,1);

for i=1:num_banks
    for j=1:num_repetitions
        % Multiply losses_given_default(i,j) by intervals to find the right slot in the
        % prob_losses. Then we increment this by probability of i defaults
        prob_losses(ceil(losses_given_default(i,j)*intervals),1) = prob_losses(ceil(losses_given_default(i,j)*intervals),1)+default_distribution(i+1);
    end
end

% Convert it to probability
prob_losses = prob_losses/num_repetitions;

% Find the probability thaat the losses are great than 0.15 the total
% liabilities i.e. > 0.15*N
prob_great_losses = sum(prob_losses(15*num_banks:end));

% expected losses given that losses are above 15% of the sector
exp_losses = [15*num_banks:100*num_banks]*prob_losses(15*num_banks:end)/(100*prob_great_losses);

dip = prob_great_losses*exp_losses;








