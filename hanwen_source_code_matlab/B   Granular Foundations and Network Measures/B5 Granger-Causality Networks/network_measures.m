function [in_connections, out_connections, in_out_connections, in_from_other, out_to_other, in_out_other, closeness, eigenvector_centrality]= network_measures(adjacency_matrix, groups)
% For all the nodes of the network it calculates some network measures
% Parameters:
% adjacency_matrix The adjacency matri describing the network. A nxn matrix
% groups A vector describing the different categories of nodes. i.e. if
% group = [2 6] that means that we have 3 groups of nodes. Group 1
% nodes 1,2, Group 2 nodes 3,4,5,6 Group 3 nodes 7 till n
% Outputs:
% in_connections For each node the number of incoming links
% out_connections For each node the number of outcoming links
% in_out_connections For each node the sum of incoming and outcoming links
% in_from_other For each node the number of incoming links from nodes in
% different categories
% out_to_other For each node the number of outcoming links to nodes in
% different categories
% in_out_other For each node the sum of in_from_other and out_to_other
% closeness For each node the average shortest path lengths to reachable
% nodes
% eigenvector_centrality For each node its eigenvector centrality

num_nodes = size(adjacency_matrix,1);

in_connections = zeros(num_nodes,1);
out_connections = zeros(num_nodes,1);
in_out_connections = zeros(num_nodes,1);
in_from_other = zeros(num_nodes,1);
out_to_other = zeros(num_nodes,1);
in_out_other = zeros(num_nodes,1);
closeness = zeros(num_nodes,1);
eigenvector_centrality = zeros(num_nodes,1);

for j = 1:num_nodes
    in_connections(j) = sum(adjacency_matrix(:,j));
    out_connections(j) = sum(adjacency_matrix(j,:));
end

in_out_connections = in_connections + out_connections;


for j=1:num_nodes
    % Find the begin index and the end index where node j belongs to
    [begin_group end_group] = find_group_node(j,groups, num_nodes);
    in_from_other = in_connections(j) - sum(adjacency_matrix(begin_group:end_group, j));
    out_to_other = out_connections(j) - sum(adjacency_matrix(j,begin_group:end_group));
end

in_out_other = in_from_other + out_to_other;

for j=1:num_nodes
    closeness(j) = calc_closeness(adjacency_matrix, j);
end

[eigenvectors, eigenvalues] = eig(adjacency_matrix);
[vals ind] = sort(diag(eigenvalues))
eigenvector_centrality = eigenvectors(:,ind);




