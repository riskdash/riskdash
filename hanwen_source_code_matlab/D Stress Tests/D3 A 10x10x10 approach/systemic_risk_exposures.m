function res = systemic_risk_exposures(exposures,k)
% This is based on the paper "Systemic Risk Exposures: A 10-by-10-by-10
% approach" by D.Duffie
% For each stress test, for each important institution it gives the
% k companies that the important institution has largest exposures on. 
% Parameters:
% exposures The exposures of the important institutions under different 
% stress tests (gains or losses). An n-p-m matrix. There are m stress 
% tests and n important institutions. For each test for each important 
% insitution there are exposures to p companies.  

num_important_institutions = size(exposures,1);
num_stress_tests = size(exposures,3);

res = zeros(num_important_institutions, k, num_stress_tests);

for test = 1:num_stress_tests
    for institution = 1:num_important_institutions
        [sorted, index] = sort(exposures(institution,:,test));
        res(institution,:,test) = index(1:k);
    end
end




