'''
Created on Mar 26, 2014

@author: Hanwen Xu

Has scripts for the rolling autocorrelation functions
'''


import numpy as np
from Autocorrelation import autocorr
from SummaryStatistic import getIndData
import matplotlib.pyplot as plt
import pickle

standardIndices = ['SP500', 'brokers', 'banks', 'insurers', 'liquid', 'illiquid']
HFIndices_raw = ['', 'Global Macro ', 'Long/Short Equity ']


'''
'''
def genRollAutocorr():
    output = {}
    for ind in standardIndices+HFIndices_raw:
        ROR, indNew = getIndData(ind, 'ROR')
        Date, indNew = getIndData(ind, 'Date')
        end = len(ROR)
        rollingac = []
        upbound = []
        lowbound = []
        for i in range(36, end):
            sampleY = ROR[i-36:i]
            #sampleX = Date[i]
            r, se = autocorr(sampleY, 1)
            rollingac.append(r)
            upbound.append(r+1.96*se)
            lowbound.append(r-1.96*se)
        rAC = np.array(rollingac)
        uB = np.array(upbound)
        lB = np.array(lowbound)
        tAxis = Date[36:]
        print len(tAxis), len(rAC)
        #fig, ax = plt.subplots()
        #ax.plot_date(tAxis, rAC, linestyle='--')
        #ax.set_title('%s'%(indNew))
        #ax.annotate('Test', (mdates.date2num(tAxis[1]), rAC[1]), xytext=(15, 15), textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
        
        #fig.autofmt_xdate()
        #plt.show()
        output[indNew] = [rAC, uB, lB]
        
    #Dateoutput = open('RollingAC.pkl', 'wb')
    #pickle.dump(output, Dateoutput)
    
'''
Generate the rolling 36 month cross-correlations for each of the 6 combinations
with the four indices: Hedge fund, Bank, Insurer, and Broker.
Generates same time, -1 lag, and +1 lag

Returns:  Dictionary with the keys being the combination in tuplet of strings, and the values being
three numpy areas, with -1, 0, and +1 lag in cross correlation
'''
def rollCrossCorr():
    Indices = ["", 'brokers', 'banks', 'insurers']
    #note, ROR of hedge fund starts one month before the other 3 indices
    RORs = []
    newIndices = []
    for ind in Indices:
        ROR, newInd = getIndData(ind, 'ROR')
        newIndices.append(newInd)
        if ind == "":
            ROR = ROR[1:]
        RORs.append(ROR)
    end = len(ROR)
    print end
    Date, indNew = getIndData(ind, 'Date')
    
    resultsDict = {}
    for i in range(len(Indices)-1):
        for j in range(i+1, len(Indices)):
            rollcc = []
            rollcc_lag1 = []  #-1 lag
            rollcc_flag1 = []  #+1 lag
            ror1 = RORs[i]
            ror2 = RORs[j]
            for k in range(37, end-1):
                Y1 = ror1[k-36:k]
                Y20 = ror2[k-36:k] #lag 0
                Y21  = ror2[k-37:k-1]  #lag 1
                Y22 = ror2[k-35:k+1]   #lag -1
                
                set1 = np.array([Y1, Y20])
                set2 = np.array([Y1, Y21])
                set3 = np.array([Y1, Y22])
                #print i, set1
                r1 = np.corrcoef(set1)
                r2 = np.corrcoef(set2)
                r3 = np.corrcoef(set3)
                rollcc.append(r1[0, 1])
                rollcc_lag1.append(r2[0, 1])
                rollcc_flag1.append(r3[0, 1])
            rcc = np.array(rollcc)
            rccl1 = np.array(rollcc_lag1)
            rccfl1 = np.array(rollcc_flag1)
            resultsDict['%s vs. %s'%(newIndices[i], newIndices[j])] = [rcc, rccl1, rccfl1]

    tAxis = Date[37:-1]
    for title in resultsDict.keys():
        fig, ax = plt.subplots()
        ax.plot_date(tAxis, resultsDict[title][0], linestyle='--', color='r', fillstyle='none', label="No Lag")
        ax.plot_date(tAxis, resultsDict[title][1], linestyle='--', color = 'b',fillstyle='none', label="Lag = 1")
        ax.plot_date(tAxis, resultsDict[title][2], linestyle='--', color = 'g', fillstyle='none',label="Lag = -1")
        ax.set_title('%s'%(title))
        
        
        handles, labels = ax.get_legend_handles_labels()
        
        # reverse the order
        ax.legend(handles, labels)
        ax.legend(bbox_to_anchor=(0., -.1, 1., .102), loc=2,ncol=3, mode="expand", borderaxespad=0.)
        #ax.annotate('Test', (mdates.date2num(tAxis[1]), rAC[1]), xytext=(15, 15), textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
        
        fig.autofmt_xdate()
        plt.show()
    
    return resultsDict
        
if __name__ == '__main__':
    #pullSummarizedStatistics()
    #genRollAutocorr()
    rollCrossCorr()