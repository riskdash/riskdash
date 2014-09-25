function  ar = absorption_ratio(asset_returns, fraction_eigenvectors)
% Calculates the absorption ratio for a time series of asset returns
% Arguments:
% asset_returns A matrix of asset returns. Rows are different dates.
% Columns are different assets. In the paper number of rows = 500.
% fraction_eigenvectors The fraction of eigenvectos used to calculate the
% absorption ratio. In the paper it is 0.2

num_assets = size(asset_returns,2);

% Calculate the covariance matrix
Sigma = cov(asset_returns);

% Find the eigenvalues
eigenvalues  = eig(Sigma);
% Sort in ascending order
sorted_eigenvalues = sort(eigenvalues);
num_eigenvalues = round(fraction_eigenvectors*num_assets);

% Calculation of the absorption ratio
numerator = sum(sorted_eigenvalues(end-num_eigenvalues+1:end));
denominator = trace(Sigma);
ar = numerator/denominator;

