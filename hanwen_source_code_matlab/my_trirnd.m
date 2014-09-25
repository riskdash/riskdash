function r = my_trirnd(min_val, mode, max_val, n)
% Creates a sample of random variables from a triangular distribution
% Parameters:
% min_val The min value of the support function of the triangular
% distribution
% mode The mode of the distribution
% max_val The max value of the support function of the triangular
% distribution
% n The number of samples will be created

% This is the cdf for the mode. For a symmetric triangular distribution
% will be 0.5
F_mode = (mode-min_val)^2/((max_val-min_val)*(mode-min_val));

% Create a uniform random vector
u = rand(n,1);

r = zeros(n,1);
% Create the random sample
for i=1:n
    if u(i)<F_mode
        r(i) = min_val + sqrt(u(i)*(max_val-min_val)*(mode-min_val));
    else
        r(i) = max_val - sqrt((1-u(i))*(max_val-min_val)*(max_val-mode));
    end
end

