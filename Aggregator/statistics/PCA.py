'''
Created on Mar 27, 2014

@author: Hanwen Xu
'''

import numpy as np
from SummaryStatistic import getIndData

def PCA(index_names, endDate = '20140101'):
    for i, ind in enumerate(index_names):
        ROR, newInd = getIndData(ind, 'ROR')
        print newInd
        listtmp = np.ndarray.tolist(ROR)
        print len(listtmp)
        if i==0:
            RORs = np.array([listtmp])
        else:
            RORs = np.append(RORs, [listtmp], axis= 0)
    print RORs
    
    covMat = np.cov(RORs)
    eigVal, eigVec = np.linalg.eig(covMat)
    return eigVal, eigVec

'''
given eigenvalues, return the cumulative risk fraction
'''
def CumulRiskFrac(eigVal):
    sort1 = sorted(eigVal, reverse=True)
    return sort1[0]/sum(sort1)

if __name__ == '__main__':
    #pullSummarizedStatistics()
    #genRollAutocorr()
    index_names = ['', 'brokers', 'banks', 'insurers']
    eigVal, eigVec = PCA(index_names)
    print eigVal
    print eigVec
    frac1 = CumulRiskFrac(eigVal)
    print frac1