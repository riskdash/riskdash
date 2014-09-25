function t = modified_sign(y)
% Finds the sign of vector.
% If an element is 0 it returns the sign of the most recent non-zero
% element. If no most recent non-zero element exists it returns 0
t = zeros(length(y),1);
t(1) = sign(y(1));
for i=1:length(y)
    t(i) = sign(y(i));
    if t(i) == 0
        t(i)=t(i-1);
    end
end