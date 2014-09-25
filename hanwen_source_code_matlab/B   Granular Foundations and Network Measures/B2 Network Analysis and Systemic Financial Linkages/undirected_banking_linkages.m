function undirected = undirected_banking_linkages(bank_claims, non_bank_claims, non_bank_liabilities)
% Calculates the undirected network of banking linkages for n
% countries
% Parameters:
% bank_claims A nxn matrix. Its (i,j) component shows the bank claims from 
% country i to banks in country j.
% non_bank_claims. A nxn matrix. Its (i,j) component shows the claims from
% banks in country i to non-banks in country j
% non_bank_liabilities A nxn matrix. Its (i,j) component shows the
% liabilities of banks in i to non-banks in j.

num_countries = size(bank_claims,1);

undirected = bank_claims + non_bank_claims + non_bank_liabilities;
% We need also to add the claims and liabilities from j to i making the
% matrix symmetric
undirected = undirected+undirected';

% Null the diagonal to avoid self-loops
for i=1:num_countries
    undirected(i,i)=0;
end




