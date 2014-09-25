function betas = quantile_regression(y,X,q)
% Calculates the q-quantile regression coefficients
% Parameters:
% y The response variable n x 1 vector
% X the matrix of regressors n x k vector
% q the quantile i.e. 0.5 for median regression

n = size(X,1);
k = size(X,2);
betas = 0;

% First way using CVX
% You will need to install cvx and run cvx_setup
cvx_begin
cvx_quiet(true)
    variable u_pos(n)
    variable u_neg(n)
    variable betas(k)
    minimize q*sum(u_pos) + (1-q)*sum(u_neg)
    subject to
        u_pos>=0;
        u_neg>=0;
        X*betas+u_pos-u_neg == y;
cvx_end

% Second way
% LP in Matlab
c = [q*ones(n,1); (1-q)*ones(n,1); zeros(k,1)];
A = [-eye(n) zeros(n) zeros(n,k);
     zeros(n) -eye(n) zeros(n,k)
     zeros(k,2*n+k)];
 b = zeros(2*n+k,1);
 
 Aeq = [eye(n) -eye(n) X];
 beq = y;
 lin_betas = linprog(c,A,b,Aeq,beq);
 betas = lin_betas(end-k+1:end);
 
 
 
 % 
 
 

