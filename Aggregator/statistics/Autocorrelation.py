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
        
        
r_k = c_k/c_0
c_0 is sample variance
c_k = 1/T \sum_(t=1)^(t=T-k)(y_t-y\hat)(y_(t+k) -y\hat)
        
Returns: 
    (R, P):   R is the autocorrelation coefficient, P is the p-value of the statistic
'''
def autocorr(x, k, SE=False):
    c0 = stats.tvar(x) #sample variance
    mu = stats.tmean(x) #sample mean
    r_arr = [1]
    
    T = float(len(x))
    
    for j in range(1, k+1):
        T1 = int(T-j)
        cj = 0.0
        for i in xrange(T1):
            cj += (x[i] - mu)*(x[i+j]-mu)
        cj = cj/T
        rj = cj/c0
        r_arr.append(rj)
    SEk = autocorrSE(r_arr, k, T)
    tval = r_arr[-1]/SEk
    pval = 1 - stats.norm.cdf(tval)
    if SE:
        return r_arr, SEk
    else:
        return r_arr, pval
    
'''
returns the SE value given the auto-corr array r_arr, and the lag k
'''
def autocorrSE(r_arr, k, T):
    r = np.array(r_arr[1:])
    norm2 = np.linalg.norm(r[:-1], 2)**2
    vark = 1/T * (1+ 2*norm2)
    SEk = np.sqrt(vark)
    return SEk