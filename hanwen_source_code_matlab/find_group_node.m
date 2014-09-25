function [begin_group, end_group] = find_group_node(node, groups, num_nodes)
% Finds the group where node j belongs to
% Parameters:
% node The node whose group we want to find
% groups A vector describing the different categories. i.e. if
% groups = [2 6] that means that we have 3 groups. Group 1
% has 1,2, Group 2 has 3,4,5,6 Group 3 nodes 7 till num_nodes
% num_elements The number of nodes

if node > num_nodes
    error('Index cannot exceed the number of nodes');
end

k = length(groups);
if node <=groups(1)
    begin_group = 1;
    end_group = groups(1);
elseif node > groups(k)
    begin_group = groups(k)+1;
    end_group = num_nodes;
else
    for i=1:k-1
        if node > groups(i) && node <= groups(i+1)
            begin_group = groups(i)+1;
            end_group = groups(i+1);
        end
    end
    
end