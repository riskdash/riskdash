function [capital_losses defaulted_banks] = credit_funding_shock(default_bank, capitals, interbank_loans, lambda, rho, delta)
% Simulates a credit and funding shock in the banking system
% Parameters:
% default_bank The bank that is initially triggered to default An integer
% 1<=default_bank <=n
% capitals The capitals of the banks. A nx1 vector. A bank defauls if its
% capital becomes negative
% interbank_loans A nxn matrix describing the loans between banks. The
% (i,j) component denotes a loan from bank j to bank i
% lambda The loss given default parameter. In the paper it is set to 1
% rho The loss of funding fraction. In the paper it is equal to 0.35
% delta The loss parameter due to forced selling. In the paper it is set to
% 1
% Output: 
% capital_losses The capital losses per surviving banks. 
% defaulted_banks The banks that default. A nx1 binary vector where 1 denotes
% default

num_banks = length(capitals);
initial_capitals = capitals;
defaulted_banks = zeros(num_banks,1);
examined_defaulted_banks = zeros(num_banks,1);

% Set to 1 the bank that triggers the credit and funding shock
defaulted_banks(default_bank) = 1;

% As long as there is a bank that has defaulted but we have not yet 
% simulated its consequences
while sum(defaulted_banks ~=examined_defaulted_banks)~=0
    
    triggered_bank = find(defaulted_banks~=examined_defaulted_banks,1);
    examined_defaulted_banks(triggered_bank) = 1;
    
    for i=1:num_banks
        if i~=triggered_bank
            capitals(i) = capitals(i) - delta*rho*interbank_loans(triggered_bank, i) - lambda*interbank_loans(i,triggered_bank);
        end
    end
    
    % If the capital is negative the bank has defaulted
    defaulted_banks(capitals < 0) = 1;

end
    
    
capital_losses = initial_capitals - capitals;
% For the defaulted banks the losses are equal to their initial capital
capital_losses(defaulted_banks>0) = initial_capitals(defaulted_banks>0);
    
   




















