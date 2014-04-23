'''
Created on Apr 23, 2014

@author: Hanwen Xu
'''

import numpy as np

'''
Calculates the metrics of indicator for early warning signal of costly asset booms

---Input---
indicator:  time series array, nx1, of the indicator
booms:  A binary time series, nx1, where 1 indicates a costly boom
theta:  risk aversion parameter, from 0.2-0.8
percentile:  percentile of distribution of the indicator, a warning
indicator is true if it exceeds the percentile.  
0<=percentile<=100
num_periods:  the number of periods into the future that an issued warning signal
indicates there will be a costly boom.
---Outputs---
true_pos:  The true positives of the warning signal
true_neg:  The true negatives of the warning signal
usefulness:  usefulness of this indicator
dp:  Difference between conditional and unconditional probabilities of true positive
'''
def EarlyWarningSignal(indicator, booms, theta, percentile, num_periods):
    n = len(indicator)
    
    indic = np.array(indicator)
    
    #find the threshold when the indicator exceeds a signal
    threshold = np.percentile(indic, percentile)
    
    #The values in the "confusion" matrix
    A = 0
    B = 0
    C = 0
    D = 0
    
    for i in range(n-num_periods):
        #if the indicator is greater than the threshold, a signal is issued
        signal_issued = indicator[i] > threshold
        #Find if there is an asset price constly boom in the next num_periods
        has_costly_boom = sum(booms[i+1:i+num_periods]) > 0
        if signal_issued:
            if has_costly_boom:
                A = A+1
            else:
                B = B+1
        else:
            if has_costly_boom:
                C = C+1
            else:
                D = D+1
    
    true_pos = A/(A+B)
    true_neg = D/(C+D)
    L = theta * C/(A+C) + (1-theta)*B/(B+D)
    usefulness = min(theta, 1-theta)- L
    dp = true_pos - (A+C)/(A+B+C+D)
    
    return true_pos, true_neg, L, usefulness, dp
        

if __name__ == '__main__':
    pass