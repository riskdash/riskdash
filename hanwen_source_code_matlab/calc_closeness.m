function cl = calc_closeness(adjacency_matrix, node)
% Calculates the closeness of a node in a network
% Parameters:
% adjaceny_matrix The adjacency matrix of the network
% node The node

% Find the distances from the node to all other nodes
distances = dijkstra(adjacency_matrix, node);

% Find the distances for the reachable nodes (including the same node)
reachable_nodes_distances = distances(distances<inf);

% We need to exclude the node itself when we divide
cl = sum(reachable_nodes_distances)/(length(reachable_nodes_distances) - 1);