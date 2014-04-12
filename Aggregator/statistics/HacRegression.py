'''
Created on Apr 12, 2014

@author: Hanwen Xu

Calculates the regression coefficients and the HAC "heteroskedasticity
and autocorrelation consistent estimator)
Parameters:
y The dependent variable An nx1 vector
X The covariates. An nxk vector
truncation_lag_to_observations_ratio The truncation lag to number of
observations ratio used to construct the HAC estimator
Output:
betas The regressor coefficients A kx1 vector
V_hat The HAC estimator
'''

import numpy as np

from OLS import ols
from scipy.linalg import inv

def HAC_Regression(y, X, truncation_lag):
    n = len(y)
    #regress y on X
    model1 = ols(y, X, 'y', ['x-lag1', 'y-lag1'])
    #calculate the residuals
    residuals = model1.e
    
    Q_hat = 1.0*np.dot(X.T, X)/n
    L = int(round(truncation_lag*n))
    H = np.dot(np.diag(residuals), X)
    omega_hat = np.dot(H.T, H)/n
    for k in range(L-1):
        omega_temp = np.zeros((2,2))
        for i in range(n-k-1):
            h1 = np.array([H[i]])
            h2 = np.array([H[i+k+1]])
            #print h1
            #print h2
            omega_temp += np.dot(h1.T, h2)
        omega_temp = omega_temp/(n-k+1)
        new_term = (L-k-1)/L*(omega_temp+omega_temp.T)
        omega_hat = omega_hat+new_term;
    V_int = inv(Q_hat).dot(omega_hat)
    V_hat = V_int.dot(inv(Q_hat))
    return model1, V_hat
    
    