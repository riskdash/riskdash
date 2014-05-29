'''
Created on Mar 27, 2014

@author: Hanwen Xu
'''

import numpy as np
from SummaryStatistic import getIndData
import datetime as dt
import matplotlib.pyplot as plt
from DataTools import getNames
import pickle, sys
from DatabaseTools import addMonths

'''
for the given index names and time window, calculates the eigVal and eigVectors

===Input===
index_names:  the name of the indices
index:  if true, then perform analysis on indices. If false, the perform analysis on top 100 companies
startDate:  Datetime object, which specifies the beginning of time to select data
endDate:  Datetime object, which specifies the end of time to select data
===Output===
eigVal:  the eigenvalues of the PCA analysis
eigVec:  the eigenvectors of the PCA analysis
'''
def PCA(index_names=[], window = 36, index=False, startDate = dt.date(1994, 01, 01), endDate = dt.date(2013, 01, 01)):
    if index:
        for i, ind in enumerate(index_names):
            ROR, newInd = getIndData(ind, 'ROR', startDate, endDate)
            #print newInd
            listtmp = np.ndarray.tolist(ROR)
            #print len(listtmp)
            if i==0:
                RORs = np.array([listtmp])
            else:
                RORs = np.append(RORs, [listtmp], axis= 0)
        #print RORs
        covMat = np.cov(RORs)
    else:
        npNarr, npDarr = getNames(endDate, window=window)
        covMat = np.cov(npDarr)
        
    eigVal, eigVec = np.linalg.eig(covMat)
    return eigVal, eigVec
'''
given eigenvalues, return the cumulative risk fraction
===Input===
eigVal:  The eigenvalues
===Output===
returns the CRF for the given eigVal
'''
def CumulRiskFrac(eigVal):
    sort1 = sorted(eigVal, reverse=True)
    return sort1[0]/sum(sort1)

'''
generate the rolling CumulRisk fraction for the index names

Returns an array [dateArray, crfArray], where dateArray is an array of dates, and crfArray is an array of CRF values
They are 1-to-1 aligned.
'''
def rollingCumulRiskFrac(window= 36):
    now = dt.datetime.now()
    precalculatedDict = {}
    iDate = dt.datetime(1996, 1, 31)
    rollingCRF = []
    tAxis = []
    while iDate < now:
        try:
            eigVal, eigVec = PCA(endDate = iDate, window=window)
            crf = CumulRiskFrac(eigVal)
            rollingCRF.append(crf)
            tAxis.append(iDate)
            precalculatedDict[iDate]= [eigVal, eigVec]
            iDate = addMonths(iDate, 1)
            print iDate.strftime('%Y/%m/%d %H:%M:%S')
        except:
            print "Unexpected error:", sys.exc_info()[0]
            iDate = now
    Nameoutput = open('PCAPrecomputed.pkl', 'wb')
    pickle.dump(precalculatedDict, Nameoutput)
    
    
    fig, ax = plt.subplots()
    ax.plot_date(tAxis, rollingCRF, linestyle='--')
    ax.set_title('Rolling CRF')
    #ax.annotate('Test', (mdates.date2num(tAxis[1]), rAC[1]), xytext=(15, 15), textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
         
    fig.autofmt_xdate()
    plt.show()
    
    return [tAxis, rollingCRF]

if __name__ == '__main__':
    #pullSummarizedStatistics()
    #genRollAutocorr()
    #index_names = ['', 'brokers', 'banks', 'insurers']
    #eigVal, eigVec = PCA()
    #print eigVal
    #print eigVec
    #frac1 = CumulRiskFrac(eigVal)
    #print "The value over all time is %5.6f"%frac1
    rollingCumulRiskFrac()
    
    