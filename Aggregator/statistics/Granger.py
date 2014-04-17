'''
Created on Mar 27, 2014

@author: Hanwen Xu
'''

import numpy as np
import datetime as dt
from HacRegression import HAC_Regression
from time import time
from DataTools import getNames
from DatabaseFiller.DatabaseTools import addMonths
import pickle, sys

'''
return a matrix with p-values of granger causality metrics
Each X value will be the input instituion returns, Y is the output

'''
def grangerCausality(npDArray):
    
    p_values = []
    for i, Xraw in enumerate(npDArray):
        #print i, Xraw
        row_pvalues = []
        for j, Yraw in enumerate(npDArray):
            if i!=j:
                #form the response in the regression equation
                y = np.array(Yraw[1:])
                #form the regressors
                X1 = np.array([Xraw[:-1], Yraw[:-1]])
                X = X1.T
                #print X, y
                try:
                    olsModel, V_hat = HAC_Regression(y, X, 0.1)
                    if i==1 and j==2:
                        olsModel.summary()
                    row_pvalues.append(olsModel.p[1])
                except:
                    print "position %d and %d have a singular matrix"%(i, j)
                    row_pvalues.append(1)
            else:
                row_pvalues.append(1)
        p_values.append(row_pvalues)
            #perform heteroscedastic and autocorrelation consistent regression
    p_values = np.array(p_values)
    return p_values

'''
Returns the granger p-values for the given time
===Input===
aDate:  datetime object for the end date
===Output===
npNArray:  the names of the companies
p_values:  the matrix of p-values

'''
def getGCPvalues(aDate= dt.date(2013, 01, 01)):
    
    tick = time()
    npNArray, npDArray = getNames(aDate)
    p_values = grangerCausality(npDArray)
    tock = time()
    print 'getting p-values takes %f' %(tock-tick)
    return npNArray, p_values


'''
Pull all the data for granger, and then store it into a dictionary
'''
def generateAllGrangerMonths():
    
    now = dt.datetime.now()
    precalculatedDict = {}
    iDate = dt.datetime(1996, 1, 31)
    while iDate < now:
        try:
            npNArray, p_values = getGCPvalues(aDate= dt.date(2013, 01, 01))
            precalculatedDict[iDate]= [npNArray, p_values]
            iDate = addMonths(iDate, 1)
            print iDate.strftime('%Y/%m/%d %H:%M:%S')
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
    Nameoutput = open('GrangerPrecomputed.pkl', 'wb')
    pickle.dump(precalculatedDict, Nameoutput)
        
if __name__ == '__main__':
    #pullSummarizedStatistics()
    #genRollAutocorr()
    aDate = dt.datetime(2013, 12, 1)
    npNar1, npDar1 = getGCPvalues(aDate)
    
    '''
    Dataoutput = open('GrangerData.pkl', 'rb')
    Nameoutput = open('GrangerNames.pkl', 'rb')
    npNArray = pickle.load(Nameoutput)
    npDArray = pickle.load(Dataoutput)
    p_value_matrix = grangerCausality(npNArray, npDArray)
    print p_value_matrix[1][2]
    '''
    #names, p_values= getGCPvalues()
    #print p_values
    #generateAllGrangerMonths()
    Nameoutput = open('GrangerNames.pkl', 'rb')
    npNArray = pickle.load(Nameoutput)
    print npNArray
    print npNar1
