function ses = systemic_expected_shortfall(mes_training_sample, lvg_training_sample, ses_training_sample, mes_firm, lvg_firm)
% Calculates the systemic expected shortfall for a firm
% Parameters:
% mes_training_sample The marginal expected shortfalls for the training
% sample of firms as a n x 1 vector
% lvg_training_sample The leverages for the training sample of firms as a
% n x 1 vector
% ses_training_sample The systemic expected shortfalls for the training
% sample of firms as a n x 1 vector
% mes_firm The marginal expected shortfall for the firm
% lvg_firm The leverage for the firm

num_firms = length(mes_training_sample);

% Regressors
X = [ones(num_firms,1) mes_training_sample lvg_training_sample];

% Regress systemic expected shortfall on marginal expected shortfall and
% leverage
betas = regress(ses_training_sample, X);

b = betas(2);
c = betas(3);
ses = (b*mes_firm + c*lvg_firm)/(b+c);
