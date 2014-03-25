'''
Created on Mar 24, 2014

@author: Hanwen Xu
'''
import numpy as np
from scipy import stats

'''
Calculates the sample autocorrelation coefficient, and the standard error of estimation of the coefficient

Requires: x to be a numpy array, at least two elements
        k to be an integer >= 1
        
Returns: 
    (R, P):   R is the autocorrelation coefficient, P is the p-value of the statistic
'''
def autocorr(x, k):
    c0 = stats.tvar(x) #sample variance
    mu = stats.tmean(x) #sample mean
    r_arr = []
    
    T = float(len(x))
    
    for j in range(1, k+1):
        T1 = int(T-j)
        cj = 0.0
        for i in xrange(T1):
            cj += (x[i] - mu)*(x[i+j]-mu)
        cj = cj/T
        rj = cj/c0
        r_arr.append(rj)
    r = np.array(r_arr)
    norm2 = np.linalg.norm(r[:-1], 2)**2
    vark = 1/T * (1+ 2*norm2)
    SEk = np.sqrt(vark)
    tval = r_arr[-1]/SEk
    pval = 1 - stats.norm.cdf(tval)
    return r_arr[-1], pval