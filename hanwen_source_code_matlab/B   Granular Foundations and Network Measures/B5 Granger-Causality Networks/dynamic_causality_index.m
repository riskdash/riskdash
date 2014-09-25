function [connection_matrix_robust, connection_matrix, dci] = dynamic_causality_index(asset_returns, statistical_significance_threshold)
% Based on the paper "Econometric Measures of Systemic Risk in the Finance
% and Insurance Sectors" by M. Billio, M. Getmansky, A.W. Lo, L. Pelizzon
% Calculates the dynamic causality index and the adjacency matrix of linear
% Granger causal relationships for different institutions based on their
% returns
% Parameters:
% asset_returns The time series of institutions returns. A nxk matrix.
% Rows are  the different dates. Columns are the different institutions
% statistical_significance_threshold The threshold for p-value that
% determines if the linear Granger causal relationship is statistically
% significant. Usually 0.05 or 0.01.
% Output:
% connection_matrix_robust The adjacency matrix describing the linear Granger
% causal relationships among the institutions. If connection_matrix(i,j) =
% 1 then institution i affects institution j. It corrects for
% autocorrelations and heteroskedasticity
% connection_matrix The adjacency matrix describing the linear Granger
% causal relationships among the institutions. If connection_matrix(i,j) =
% 1 then institution i affects institution j. It does not correct for
% autocorrelations and heteroskedasticity
% dci The dynamic causality index for the robust matrix

num_institutions = size(asset_returns,2);
connection_matrix_robust = zeros(num_institutions);
connection_matrix = zeros(num_institutions);

% For each pair of different institutions find the p-value of their linear
% Granger causal relationship and if this relationship is significant
for i = 1:num_institutions
    for j = 1:num_institutions
        if i~=j
            [p_value_robust p_value] = linear_granger_causality(asset_returns(:,i), asset_returns(:,j));
            if p_value_robust < statistical_significance_threshold
                % The relationship is significant
                connection_matrix_robust(i,j) = 1;
            end
            if p_value < statistical_significance_threshold
                % The relationship is significant
                connection_matrix(i,j) = 1;
            end
            
        end
    end
end

% Maximum possible number of relationships are all the pairs of different
% institutions
maximum_possible_num_causal_relationships = num_institutions^2 - num_institutions;
num_causal_relationships = sum(sum(connection_matrix_robust));

% Dynamic Causality Index
dci = num_causal_relationships/maximum_possible_num_causal_relationships;

