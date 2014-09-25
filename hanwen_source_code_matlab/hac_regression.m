function [betas, V_hat] = hac_regression(y,X, truncation_lag_to_observations_ratio)
% Calculates the regression coefficients and the HAC "heteroskedasticity
% and autocorrelation consistent estimator)
% Parameters:
% y The dependent variable An nx1 vector
% X The covariates. An nxk vector
% truncation_lag_to_observations_ratio The truncation lag to number of
% observations ratio used to construct the HAC estimator
% Output:
% betas The regressor coefficients A kx1 vector
% V_hat The HAC estimator
n = length(y);
% Regress y on X
betas = regress(y,X);
% Calculate the residuals
residuals = y - X*betas;


Q_hat = X'*X/n;

% Newey West estimator
L = round(truncation_lag_to_observations_ratio*n); 
H = diag(residuals)*X;
omega_hat = H'*H/n;  
for k = 1:L-1
    omega_temp = 0;
    for i = 1:n-k
        omega_temp = omega_temp + H(i,:)'*H(i+k,:);
    end
    omega_temp = omega_temp/(n-k);
    new_term = (L - k)/L *(omega_temp + omega_temp');
    omega_hat = omega_hat + new_term;
end

V_hat = inv(Q_hat)*omega_hat*inv(Q_hat);



