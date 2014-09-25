function ar_shift = dar(absorption_ratios, fraction)
% Calculates the standardized AR shift
% Arguments:
% abpsorption_ratios A vector of absorption ratios. In the paper absorption
% ratios are given for 1 year
% fraction Number of days in the short term absorption ratio over number of days in the long term absorption ratio. In
% the paper 15/252 if we consider a year having 252 absorption ratios

   [num_rows, num_cols] = size(absorption_ratios);
   if (num_rows ~= 1) && (num_cols ~=1)
    error('The absoprtion_ratios is a 1-d vector');
   end
   
   num_days = length(absorption_ratios);
   num_days_short_term = round(fraction*num_days);
   
   % Calculate the AR shift
   % For the short term absorption ratio take the last num_days_short_term days
   numerator = mean(absorption_ratios(end-num_days_short_term+1:end)) - mean(absorption_ratios);
   denominator = std(absorption_ratios);
   ar_shift = numerator/denominator;
   
  
  
