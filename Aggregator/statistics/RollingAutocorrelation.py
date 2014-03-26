'''
Created on Mar 26, 2014

@author: Hanwen Xu

Has scripts for the rolling autocorrelation functions
'''


import numpy as np
from Autocorrelation import autocorr
from SummaryStatistic import getIndData
import matplotlib.pyplot as plt

standardIndices = ['SP500', 'brokers', 'banks', 'insurers', 'liquid', 'illiquid']
HFIndices_raw = ['', 'Global Macro ', 'Long/Short Equity ']

def genRollAutocorr():
    for ind in standardIndices+HFIndices_raw:
        ROR, indNew = getIndData(ind, 'ROR')
        Date, indNew = getIndData(ind, 'Date')
        end = len(ROR)
        rollingac = []
        upbound = []
        lowbound = []
        for i in range(36, end):
            sampleY = ROR[i-36:i]
            sampleX = Date[i]
            r, se = autocorr(sampleY, 1)
            rollingac.append(r)
            upbound.append(r+1.96*se)
            lowbound.append(r-1.96*se)
        rAC = np.array(rollingac)
        uB = np.array(upbound)
        lB = np.array(lowbound)
        tAxis = Date[36:]
        print len(tAxis), len(rAC)
        fig, ax = plt.subplots()
        ax.plot_date(tAxis, rAC, linestyle='--')
        ax.set_title('%s'%(indNew))
        #ax.annotate('Test', (mdates.date2num(tAxis[1]), rAC[1]), xytext=(15, 15), textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
        
        fig.autofmt_xdate()
        plt.show()
        
if __name__ == '__main__':
    #pullSummarizedStatistics()
    genRollAutocorr()