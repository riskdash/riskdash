function directed = directed_banking_linkages(initial_net_bank_claims, initial_net_non_bank_claims, final_net_bank_claims, final_net_non_bank_claims)
% Calculates the diretced network of banking linkages for n
% countries between two time instants t1 and t2
% Parameters:
% initial_net_bank_claims A nxn matrix. Its (i,j) component shows the 
% net bank claims from country i to banks in country j at t1. Antisymmetric
% matrix
% initial_net_non_bank_claims. A nxn matrix. Its (i,j) component shows the 
% net claims from banks in country i to non-banks in country j at t1
% final_net_bank_claims A nxn matrix. Its (i,j) component shows the 
% net bank claims from country i to banks in country j at t2. Antisymmetric
% matrix
% final_net_non_bank_claims. A nxn matrix. Its (i,j) component shows the 
% net claims from banks in country i to non-banks in country j at t2

initial_net_claims =  initial_net_bank_claims+initial_net_non_bank_claims - initial_net_non_bank_claims';
final_net_claims = final_net_bank_claims + final_net_non_bank_claims - final_net_non_bank_claims';

% Change between t1 and t2
diff_mat = final_net_claims - initial_net_claims;

% If (i,j) element is positive put 1 otherwise 0
directed = diff_mat>0;

num_countries = size(initial_net_bank_claims,1);
% If initial_net_bank_claims and final_net_bank_claims have 0 diagonals
% this is not needed but in any case
for i=1:num_countries
    directed(i,i)=0;
end





