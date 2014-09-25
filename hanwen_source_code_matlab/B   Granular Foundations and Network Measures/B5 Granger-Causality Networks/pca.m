function [Sigma, eigenvalues, eigenvectors] = pca(asset_returns)
% Calculates the covariance matrix of
% the returns for different assets and its eigenvalues and eigenvectors 
% Parameters:
% asset_Returns The time series of asset returns. A nxk matrix. Rows are 
% the different dates. Columns are the different assets
% Output:
% Sigma The covariance matrix of the asset returns
% eigenvalues The eigenvalues of the covariance matrix
% eigenvectors A matrix with the corresponing eigenvectors of the 
% covariance matrix as its columns

% Calculate the covariance matrix
Sigma = cov(asset_returns);

% Find the eigenvalues and eigenvectors
[eigenvectors lambda]  = eig(Sigma);
eigenvalues = diag(lambda);




