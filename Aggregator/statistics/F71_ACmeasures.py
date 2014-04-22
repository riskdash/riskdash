'''
Created on Apr 18, 2014

@author: Hanwen Xu
'''

from DataTools import getNames
from Autocorrelation import autocorr
import datetime as dt
from DatabaseFiller.DatabaseTools import addMonths
import pickle, sys
'''
Generate the Q-statistic from the F7.1 in the survey analytics.  Takes the 6 autocorrelation coefficients, 
and generates the Q statistic for the top 25 hedge funds. 

input: end date,
'''
def Qstatistic(endDate, n=25):
    Qarray = []
    nameArray, dataArray = getNames(endDate, inst=['hedgefunds'], numComps = n)
    k = 6 #lag steps we want to analyze
    for data in dataArray:
        r_arr, se = autocorr(data, k, SE=True)
        T = len(data)
        sum1 =  0.0
        for i in range(1, k+1):
            #print r_arr
            sum1+= r_arr[i]**2/(T-i)
        sum1 = sum1*T*(T+2)
        Qarray.append(sum1)
    print Qarray
    return nameArray, Qarray

'''
Generate the rolling QStat for the specified number of companies
'''
def rollQStat(n=25):
    now = dt.datetime.now()
    precalculatedDict = {}
    iDate = dt.datetime(1996, 1, 31)
    while iDate < now:
        try:
            nameArray, Qarray = Qstatistic(iDate)
            precalculatedDict[iDate]= [nameArray, Qarray]
            iDate = addMonths(iDate, 1)
            print iDate.strftime('%Y/%m/%d %H:%M:%S')
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
    Nameoutput = open('Qstatistic.pkl', 'wb')
    pickle.dump(precalculatedDict, Nameoutput)
    

'''
Return a weighted aggregate illiquidity measure from F7.1 in the survey analytics.  Takes first order autocorrelation
weighted by AUM.  
'''
def AggregateIlliquidity(endDate, n=25):
    nameArray, dataArray = getNames(endDate, inst=['hedgefunds'], numComps = n)
    k = 1 #lag steps we want to analyze
    sumAUM = 0.0
    for name in nameArray:
        sumAUM += float(name[1])
    rho_prime = 0.0
    for ind, data in enumerate(dataArray):
        r_arr, se = autocorr(data, k, SE=True)
        rho = r_arr[-1]
        weight = float(nameArray[ind][1])/sumAUM
        rho_prime += weight*rho
    return rho_prime

def rollAggIlliquid(n=25):
    now = dt.datetime.now()
    precalculatedDict = {}
    iDate = dt.datetime(1996, 1, 31)
    while iDate < now:
        try:
            rho_prime = AggregateIlliquidity(iDate)
            precalculatedDict[iDate]= rho_prime
            iDate = addMonths(iDate, 1)
            print iDate.strftime('%Y/%m/%d %H:%M:%S')
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
    Nameoutput = open('AggregateIlliquidity.pkl', 'wb')
    pickle.dump(precalculatedDict, Nameoutput)

if __name__ == '__main__':
    #rollQStat()
    print "q stat done"
    rollAggIlliquid()
    print "agg Illiquid done"