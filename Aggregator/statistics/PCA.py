'''
Created on Mar 27, 2014

@author: Hanwen Xu
'''

import numpy as np
from SummaryStatistic import getIndData

def PCA(index_names):
    RORs = []
    for ind in index_names:
        ROR, newInd = getIndData(ind, 'ROR')
        print newInd
        RORs.append(ROR)
    asset_returns = np.array(RORs)
    covMat = np.cov(asset_returns)
    eigVal, eigVec = np.linalg.eig(covMat)
    return eigVal, eigVec

if __name__ == '__main__':
    #pullSummarizedStatistics()
    #genRollAutocorr()
    PCA()