function distances = dijkstra(A,node)
% Implements the Dijkstra algorithm
% Returns the distance from a single vertex to all others, doesn't save the path
% Paramters: 
% A the adjacency matrix nxn
% node The initial node from which we calculate all the shortest paths to
% any other node
% Outputs: 
% shortest path lengths between the initial and all other nodes

num_nodes = size(A,1);
% Initialize all the distances to inf
distances = inf*ones(1,num_nodes); % distance s-all nodes
% Self-distance is 0
distances(node) = 0;    

% set of nodes not examined
T = 1:num_nodes;    

while ~(isempty(T))
    [d_min,index] = min(distances(T));
    
    for j=1:length(T)
        % If there is connection and current distance is closer, update it 
        if A(T(index),T(j))>0 && distances(T(j))>distances(T(index))+A(T(index),T(j))
            distances(T(j))=distances(T(index))+A(T(index),T(j));
        end
    end
    
    % Remove from the set of nodes not examined
    T = setdiff(T,T(index));
end